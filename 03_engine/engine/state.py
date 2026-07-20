from __future__ import annotations

import math
import secrets
from copy import deepcopy
from data import (
    JOBS,
    MONSTERS,
    DUNGEONS,
    EQUIPMENT,
    ITEMS,
    QUESTS,
    REGIONS,
    RELICS,
    SKILLS,
    get_unlocked_regions,
)
from .equipment_refs import (
    equipment_base_id,
    equipment_ref_count,
    first_inventory_equipment_ref,
    resolve_equipment_ref,
)


def parent_job(job: str) -> str:
    return {
        "元素騎士": "劍士",
        "星詠者": "法師",
        "影行者": "盜賊",
        "聖印使": "牧師"
    }.get(job, job)


RUN_SUPPLY_CAPS = {"sustain_hp": 3, "emergency_hp": 1, "throwable": 2, "escape": 1}
RUN_SUPPLY_SUSTAIN_HP_ITEMS = {"item_potion_s", "item_potion_m"}
RUN_SUPPLY_EMERGENCY_HP_ITEMS = RUN_SUPPLY_SUSTAIN_HP_ITEMS | {
    "item_ice_potion_01", "item_earth_potion_01", "item_thunder_potion_01", "item_final_potion_01",
}
RUN_SUPPLY_MP_ITEMS = {
    "item_focus_drop", "item_ice_potion_02", "item_earth_potion_02", "item_thunder_potion_02", "item_final_potion_02",
}
RUN_SUPPLY_THROW_ITEMS = {
    "item_armor_piercer", "item_throw_fire", "item_throw_ice", "item_throw_earth", "item_throw_thunder",
    "item_sanctified_ash_vial", "item_rending_spike",
}
RUN_SUPPLY_ESCAPE_ITEM = "item_escape_scroll"

ICE_REGION_UNLOCK = "unlock_ice_region"
ICE_PHASE_2_DUNGEON_ID = "dungeon_ice_main_phase_2"
EARTH_PHASE_2_DUNGEON_ID = "dungeon_earth_main_phase_2"
THUNDER_PHASE_2_DUNGEON_ID = "dungeon_thunder_main_phase_2"
FINAL_PHASE_2_DUNGEON_ID = "dungeon_final_main_phase_2"
FINAL_PHASE_3_DUNGEON_ID = "dungeon_final_main_phase_3"
FINAL_REGION_UNLOCK = "unlock_final_region_preview"

BOSS_CLEAR_FLAGS = {
    "boss_glen": "boss_glen_defeated",
    "boss_ash_guardian": "ash_guardian_defeated",
    "boss_cinder_seal_sentinel": "cinder_seal_sentinel_defeated",
    "boss_ice_wreck_captain": "ice_wreck_captain_defeated",
    "boss_ice_frostroot_keeper": "ice_frostroot_keeper_defeated",
    "boss_ice_outer_gatewarden": "ice_outer_gatewarden_defeated",
    "boss_ice_final_seal_lord": "ice_final_boss_defeated",
    "boss_earth_rootwarden": "earth_rootwarden_defeated",
    "boss_earth_quarry_colossus": "earth_quarry_colossus_defeated",
    "boss_earth_outer_grovekeeper": "earth_outer_grovekeeper_defeated",
    "boss_earth_deep_leyline_lord": "earth_final_boss_defeated",
    "boss_thunder_plateau_beacon": "thunder_plateau_beacon_defeated",
    "boss_thunder_channel_keeper": "thunder_channel_keeper_defeated",
    "boss_thunder_lower_array_warden": "thunder_lower_array_warden_defeated",
    "boss_thunder_crown_storm_lord": "thunder_final_boss_defeated",
    "boss_final_echo_vanguard": "final_echo_vanguard_defeated",
    "boss_final_ruin_jailer": "final_ruin_jailer_defeated",
    "boss_final_echo_warden": "final_echo_warden_defeated",
    "boss_final_seal_core": "final_seal_core_defeated",
    "boss_final_demon_king": "final_demon_king_defeated",
}

EQUIPMENT_INSTANCE_STATE_VERSION = 2


def _next_equipment_instance_id(state: dict) -> str:
    instances = state.setdefault("equipment_instances", {})
    serial = len(instances) + 1
    while f"eqi_{serial:06d}" in instances:
        serial += 1
    return f"eqi_{serial:06d}"


def create_equipment_instance(state: dict, base_item_id: str, *, generation_version: int) -> str:
    if base_item_id not in EQUIPMENT or EQUIPMENT[base_item_id]["slot"] == "special":
        raise ValueError("Only non-special EQUIPMENT entries have instances.")
    reference_id = _next_equipment_instance_id(state)
    state.setdefault("equipment_instances", {})[reference_id] = {
        "base_item_id": base_item_id,
        "generation_version": generation_version,
        "roll_index": 0,
        "major_affix_id": None,
        "minor_affix_id": None,
    }
    return reference_id


def migrate_equipment_instances(state: dict) -> None:
    """Convert legacy non-special equipment references to unaffixed v0 copies."""
    if state.get("state_version", 1) >= EQUIPMENT_INSTANCE_STATE_VERSION:
        return
    state["run_seed"] = state.get("run_seed") if isinstance(state.get("run_seed"), int) and state["run_seed"] >= 0 else 0
    state["affix_roll_counter"] = 0
    state["equipment_instances"] = {}
    migrated_inventory = {}
    for item_id, quantity in state.get("inventory", {}).items():
        if item_id in EQUIPMENT and EQUIPMENT[item_id]["slot"] != "special":
            for _ in range(max(0, quantity if isinstance(quantity, int) else 0)):
                migrated_inventory[create_equipment_instance(state, item_id, generation_version=0)] = 1
        else:
            migrated_inventory[item_id] = quantity
    state["inventory"] = migrated_inventory
    for slot, item_id in state.get("equipment", {}).items():
        if item_id in EQUIPMENT and EQUIPMENT[item_id]["slot"] != "special":
            state["equipment"][slot] = create_equipment_instance(state, item_id, generation_version=0)
    state["state_version"] = EQUIPMENT_INSTANCE_STATE_VERSION


def is_key_item(item_id: str) -> bool:
    return item_id.startswith("key_")


def exp_to_next(level: int) -> int:
    return 70 + (level - 1) * 70


def create_state(name: str, job: str) -> dict:
    base = JOBS[job]["base"]
    state = {
        "name": name,
        "job": job,
        "level": 1,
        "exp": 0,
        "gold": 120,
        "guild_points": 0,
        "current_hp": base["max_hp"],
        "current_mp": base["max_mp"],
        "inventory": {},
        "equipment": {"weapon": None, "head": None, "body": None, "accessory": None, "special": None},
        "learned_skills": list(JOBS[job]["base_skills"]),
        "completed_quests": ["quest_register"],
        "unlocked": ["dungeon_moss_cave"],
        "cleared_dungeons": [],
        "flags": {},
        "relic_passives": {},
        "storage_unlocked": False,
        "storage": {},
        "bestiary": [],
        "state_version": EQUIPMENT_INSTANCE_STATE_VERSION,
        "run_seed": secrets.randbits(63),
        "affix_roll_counter": 0,
        "equipment_instances": {},
    }
    for item_id, qty in QUESTS["quest_register"]["reward"]["items"].items():
        add_item(state, item_id, qty)
    equip_item(state, "special_trial_badge", quiet=True)
    return state


def ensure_state_defaults(state: dict) -> dict:
    migrate_equipment_instances(state)
    state["state_version"] = EQUIPMENT_INSTANCE_STATE_VERSION
    if not isinstance(state.get("run_seed"), int) or state["run_seed"] < 0:
        state["run_seed"] = 0
    if not isinstance(state.get("affix_roll_counter"), int) or state["affix_roll_counter"] < 0:
        state["affix_roll_counter"] = 0
    if not isinstance(state.get("equipment_instances"), dict):
        state["equipment_instances"] = {}
    if not isinstance(state.get("learned_skills"), list):
        job_id = state.get("job")
        state["learned_skills"] = list(JOBS[job_id]["base_skills"]) if job_id in JOBS else []
    else:
        state["learned_skills"] = [skill_id for skill_id in state["learned_skills"] if skill_id in SKILLS]
    if not isinstance(state.get("flags"), dict):
        state["flags"] = {}
    raw_relic_passives = state.get("relic_passives")
    if not isinstance(raw_relic_passives, dict):
        raw_relic_passives = {}
    normalized_relic_passives = {}
    for relic_id, choice_id in raw_relic_passives.items():
        relic = RELICS.get(relic_id)
        if not relic or not state["flags"].get(relic.get("complete_flag")):
            continue
        choice_ids = {choice.get("id") for choice in relic.get("passive_choices", [])}
        if isinstance(choice_id, str) and choice_id in choice_ids:
            normalized_relic_passives[relic_id] = choice_id
    state["relic_passives"] = normalized_relic_passives
    state.setdefault("storage_unlocked", False)
    if not isinstance(state.get("storage"), dict):
        state["storage"] = {}
    else:
        for item_id, qty in list(state["storage"].items()):
            if not isinstance(qty, int) or qty <= 0:
                del state["storage"][item_id]
    if not isinstance(state.get("bestiary"), list):
        state["bestiary"] = []
    else:
        clean_bestiary = []
        seen = set()
        for monster_id in state["bestiary"]:
            if monster_id in MONSTERS and monster_id not in seen:
                clean_bestiary.append(monster_id)
                seen.add(monster_id)
        state["bestiary"] = clean_bestiary
    if state.get("run_supplies") is not None and not isinstance(state.get("run_supplies"), dict):
        state["run_supplies"] = None
    return state


def run_supply_mp_cap(state: dict) -> int:
    return 1 if state.get("job") in {"戰士", "盜賊"} else 2


def item_job_allowed(state: dict, item_id: str) -> bool:
    """Return whether an item is unrestricted or legal for the current job."""
    jobs = ITEMS.get(item_id, {}).get("jobs")
    return not jobs or state.get("job") in jobs


def configure_run_supplies(state: dict, selections: dict) -> dict:
    """Validate and activate one expedition's five supply groups.

    Items stay in the general inventory until consumed; this only records the
    legal per-run quantity, so unused supplies need no return operation.
    """
    if not isinstance(selections, dict):
        raise ValueError("補給配置必須是物件。")
    specs = {
        "sustain_hp": (RUN_SUPPLY_SUSTAIN_HP_ITEMS, RUN_SUPPLY_CAPS["sustain_hp"]),
        "emergency_hp": (RUN_SUPPLY_EMERGENCY_HP_ITEMS, RUN_SUPPLY_CAPS["emergency_hp"]),
        "mp": (RUN_SUPPLY_MP_ITEMS, run_supply_mp_cap(state)),
        "throwable": (RUN_SUPPLY_THROW_ITEMS, RUN_SUPPLY_CAPS["throwable"]),
        "escape": ({RUN_SUPPLY_ESCAPE_ITEM}, RUN_SUPPLY_CAPS["escape"]),
    }
    normalized: dict[str, dict[str, int | str | None]] = {}
    requested: dict[str, int] = {}
    for slot, (allowed, cap) in specs.items():
        raw = selections.get(slot) or {}
        item_id = raw.get("item_id") if isinstance(raw, dict) else None
        quantity = raw.get("quantity", 0) if isinstance(raw, dict) else 0
        if item_id in (None, ""):
            item_id, quantity = None, 0
        if item_id and not item_job_allowed(state, item_id):
            raise ValueError("Item is not compatible with the current job.")
        if item_id not in allowed and item_id is not None:
            raise ValueError(f"{slot} 不可放入此道具。")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0 or quantity > cap:
            raise ValueError(f"{slot} 的數量超出限制。")
        if quantity and not item_id:
            raise ValueError(f"{slot} 必須先選擇道具。")
        normalized[slot] = {"item_id": item_id, "quantity": quantity}
        if item_id:
            requested[item_id] = requested.get(item_id, 0) + quantity
    for item_id, quantity in requested.items():
        if quantity > state.get("inventory", {}).get(item_id, 0):
            raise ValueError(f"{ITEMS[item_id]['name']} 數量不足。")
    state["run_supplies"] = normalized
    return normalized


def run_supply_item_quantity(state: dict, item_id: str) -> int:
    supplies = state.get("run_supplies")
    if supplies is None:  # Direct combat tools retain their legacy fixture behavior.
        return state.get("inventory", {}).get(item_id, 0)
    return sum(
        int(slot.get("quantity", 0))
        for slot in supplies.values()
        if isinstance(slot, dict) and slot.get("item_id") == item_id
    )


def consume_run_supply_item(state: dict, item_id: str) -> bool:
    if run_supply_item_quantity(state, item_id) <= 0 or not remove_item(state, item_id, 1):
        return False
    supplies = state.get("run_supplies")
    if isinstance(supplies, dict):
        for slot in supplies.values():
            if isinstance(slot, dict) and slot.get("item_id") == item_id and slot.get("quantity", 0) > 0:
                slot["quantity"] -= 1
                break
    return True


def add_item(state: dict, item_id: str, qty: int = 1) -> None:
    if qty <= 0:
        return
    if state.get("state_version", 1) >= EQUIPMENT_INSTANCE_STATE_VERSION and item_id in EQUIPMENT and EQUIPMENT[item_id]["slot"] != "special":
        for _ in range(qty):
            state["inventory"][create_equipment_instance(state, item_id, generation_version=1)] = 1
        return
    state["inventory"][item_id] = state["inventory"].get(item_id, 0) + qty


def remove_item(state: dict, item_id: str, qty: int = 1) -> bool:
    if qty <= 0:
        return True
    if state["inventory"].get(item_id, 0) < qty:
        return False
    state["inventory"][item_id] -= qty
    if state["inventory"][item_id] <= 0:
        del state["inventory"][item_id]
    return True


def add_storage_item(state: dict, item_id: str, qty: int = 1) -> None:
    if qty <= 0:
        return
    state["storage"][item_id] = state["storage"].get(item_id, 0) + qty


def remove_storage_item(state: dict, item_id: str, qty: int = 1) -> bool:
    if qty <= 0:
        return True
    if state["storage"].get(item_id, 0) < qty:
        return False
    state["storage"][item_id] -= qty
    if state["storage"][item_id] <= 0:
        del state["storage"][item_id]
    return True


def owns_item_or_equipped(state: dict, item_id: str) -> bool:
    if item_id in EQUIPMENT:
        return equipment_ref_count(state, item_id, include_equipped=True) > 0
    if state["inventory"].get(item_id, 0) > 0:
        return True
    return item_id in state["equipment"].values()


def consume_item_or_equipped(state: dict, item_id: str) -> bool:
    if item_id in EQUIPMENT:
        reference_id = first_inventory_equipment_ref(state, item_id)
        if reference_id and remove_item(state, reference_id, 1):
            return True
        for slot, equipped in state["equipment"].items():
            if equipment_base_id(state, equipped) == item_id:
                state["equipment"][slot] = None
                return True
        return False
    if remove_item(state, item_id, 1):
        return True
    for slot, equipped in state["equipment"].items():
        if equipped == item_id:
            state["equipment"][slot] = None
            return True
    return False


def unlock(state: dict, key: str) -> None:
    if key not in state["unlocked"]:
        state["unlocked"].append(key)


def is_unlocked(state: dict, key: str | None) -> bool:
    if not key:
        return True
    return key in state.get("unlocked", []) or key in state.get("completed_quests", [])


def boss_clear_flag(boss_id: str | None) -> str | None:
    if not boss_id:
        return None
    return BOSS_CLEAR_FLAGS.get(boss_id)


def boss_defeated(state: dict, boss_id: str | None) -> bool:
    flag = boss_clear_flag(boss_id)
    return bool(flag and state.get("flags", {}).get(flag))


def player_facing_dungeon_ids(state: dict, region_id: str | None = None) -> list[str]:
    dungeon_ids = []
    allowed_dungeon_ids = None
    if region_id is not None and region_id in REGIONS:
        allowed_dungeon_ids = set(REGIONS[region_id]["dungeon_ids"])
    ice_phase_2_unlocked = is_unlocked(state, ICE_PHASE_2_DUNGEON_ID)
    earth_phase_2_unlocked = is_unlocked(state, EARTH_PHASE_2_DUNGEON_ID)
    thunder_phase_2_unlocked = is_unlocked(state, THUNDER_PHASE_2_DUNGEON_ID)
    final_phase_2_unlocked = is_unlocked(state, FINAL_PHASE_2_DUNGEON_ID)
    final_phase_3_unlocked = is_unlocked(state, FINAL_PHASE_3_DUNGEON_ID)
    for dungeon_id, dungeon in DUNGEONS.items():
        if allowed_dungeon_ids is not None and dungeon_id not in allowed_dungeon_ids:
            continue
        if dungeon_id == "dungeon_ice_main_phase_1" and ice_phase_2_unlocked:
            continue
        if dungeon_id == "dungeon_earth_main_phase_1" and earth_phase_2_unlocked:
            continue
        if dungeon_id == "dungeon_thunder_main_phase_1" and thunder_phase_2_unlocked:
            continue
        if dungeon_id == "dungeon_final_main_phase_1" and (final_phase_2_unlocked or final_phase_3_unlocked):
            continue
        if dungeon_id == "dungeon_final_main_phase_2" and final_phase_3_unlocked:
            continue
        if is_unlocked(state, dungeon.get("unlock")):
            dungeon_ids.append(dungeon_id)
    return dungeon_ids


def active_relic_passive_effects(state: dict) -> dict[str, int]:
    effects: dict[str, int] = {}
    selected = state.get("relic_passives", {})
    if not isinstance(selected, dict):
        return effects
    flags = state.get("flags", {})
    for relic_id, choice_id in selected.items():
        relic = RELICS.get(relic_id, {})
        if not flags.get(relic.get("complete_flag")):
            continue
        choice = next((entry for entry in relic.get("passive_choices", []) if entry.get("id") == choice_id), None)
        if not choice:
            continue
        for effect_id, value in choice.get("effect", {}).items():
            if isinstance(value, int):
                effects[effect_id] = effects.get(effect_id, 0) + value
    return effects


def get_stats(state: dict, buffs: dict | None = None) -> dict:
    job = JOBS[parent_job(state["job"])]
    stats = deepcopy(job["base"])
    level_bonus = state["level"] - 1
    for key, value in job["growth"].items():
        stats[key] += value * level_bonus
    extra_count = (state["level"] - 1) // 3
    for key, value in job["extra_every_3"].items():
        stats[key] = stats.get(key, 0) + value * extra_count

    stats.setdefault("magic_attack", 0)
    stats.setdefault("magic_defense", 0)
    stats.setdefault("effect_accuracy", 0)
    stats["fire_resist"] = 0
    stats["ice_resist"] = 0
    stats["earth_resist"] = 0
    stats["thunder_resist"] = 0
    stats["trap_evasion"] = 0
    stats["rare_drop"] = 0

    for item_id in state["equipment"].values():
        resolved = resolve_equipment_ref(state, item_id)
        if not resolved:
            continue
        for key, value in resolved["base"].get("stats", {}).items():
            stats[key] = stats.get(key, 0) + value

    relic_effects = active_relic_passive_effects(state)
    stats["crit"] = stats.get("crit", 0) + relic_effects.get("crit", 0)
    stats["effect_accuracy"] = stats.get("effect_accuracy", 0) + relic_effects.get("effect_accuracy", 0)
    for key in ("fire_resist", "ice_resist", "earth_resist", "thunder_resist"):
        stats[key] += relic_effects.get("all_element_resist", 0)

    if buffs:
        if buffs.get("defense_up", 0) > 0:
            stats["defense"] = math.ceil(stats["defense"] * 1.2)
        if buffs.get("defense_down", 0) > 0:
            stats["defense"] = max(1, math.floor(stats["defense"] * 0.8))
        if buffs.get("quickstep", 0) > 0:
            stats["agility"] = math.ceil(stats["agility"] * 1.25)
        for buff_key, bonuses in buffs.get("_buff_stat_data", {}).items():
            if buffs.get(buff_key, 0) <= 0:
                continue
            for stat_key, value in bonuses.items():
                stats[stat_key] = stats.get(stat_key, 0) + value

    for key, effect_key in (("max_hp", "max_hp_percent"), ("max_mp", "max_mp_percent"), ("magic_defense", "magic_defense_percent")):
        percent = relic_effects.get(effect_key, 0)
        if percent:
            stats[key] = math.ceil(stats[key] * (1 + percent / 100))

    if state.get("job") == "元素騎士":
        for key in ("fire_resist", "ice_resist", "earth_resist", "thunder_resist"):
            stats[key] = stats.get(key, 0) + 10
    elif state.get("job") == "星詠者":
        stats["crit"] = stats.get("crit", 0) + 15

    for key in ("fire_resist", "ice_resist", "earth_resist", "thunder_resist"):
        stats[key] = max(0, min(stats.get(key, 0), 75))
    return stats



def equipment_comparison(state: dict, candidate_reference_id: str) -> dict:
    """Return a side-effect-free candidate-versus-equipped comparison."""
    candidate = resolve_equipment_ref(state, candidate_reference_id)
    if not candidate:
        raise ValueError("Unknown equipment reference.")

    candidate_base = candidate["base"]
    slot = candidate_base["slot"]
    equipped_reference_id = state.get("equipment", {}).get(slot)
    equipped = resolve_equipment_ref(state, equipped_reference_id)
    compatible = parent_job(state.get("job")) in candidate_base.get("jobs", [])
    reason = None if compatible else "目前職業無法裝備此物品。"
    before = get_stats(state)
    simulated = deepcopy(state)
    simulated.setdefault("equipment", {})[slot] = candidate_reference_id
    after = get_stats(simulated) if compatible else before

    def presentation(resolved: dict | None) -> dict | None:
        if not resolved:
            return None
        instance = resolved.get("instance") or {}
        return {
            "reference_id": resolved["reference_id"],
            "base_item_id": resolved["base_item_id"],
            "name": resolved["base"]["name"],
            "quality": "normal",
            "upgrade_level": 0,
            "generation_version": instance.get("generation_version"),
            "major_affix_id": instance.get("major_affix_id"),
            "minor_affix_id": instance.get("minor_affix_id"),
        }

    def affix_change(before_id: str | None, after_id: str | None) -> str:
        if before_id == after_id:
            return "unchanged"
        if before_id is None:
            return "gained"
        if after_id is None:
            return "removed"
        return "replaced"

    stats = {
        key: {"before": before.get(key, 0), "after": after.get(key, 0), "delta": after.get(key, 0) - before.get(key, 0)}
        for key in sorted(set(before) | set(after))
    }
    candidate_view = presentation(candidate)
    equipped_view = presentation(equipped)
    return {
        "slot": slot,
        "compatible": compatible,
        "reason": reason,
        "candidate": candidate_view,
        "equipped": equipped_view,
        "stats": stats,
        "affixes": {
            "major": {
                "before": equipped_view["major_affix_id"] if equipped_view else None,
                "after": candidate_view["major_affix_id"],
                "change": affix_change(
                    equipped_view["major_affix_id"] if equipped_view else None,
                    candidate_view["major_affix_id"],
                ),
            },
            "minor": {
                "before": equipped_view["minor_affix_id"] if equipped_view else None,
                "after": candidate_view["minor_affix_id"],
                "change": affix_change(
                    equipped_view["minor_affix_id"] if equipped_view else None,
                    candidate_view["minor_affix_id"],
                ),
            },
        },
    }


def clamp_vitals(state: dict) -> None:
    stats = get_stats(state)
    state["current_hp"] = max(0, min(state["current_hp"], stats["max_hp"]))
    state["current_mp"] = max(0, min(state["current_mp"], stats["max_mp"]))


def equip_item(state: dict, item_id: str, quiet: bool = False) -> bool:
    resolved = resolve_equipment_ref(state, item_id)
    if not resolved:
        return False
    eq = resolved["base"]
    if parent_job(state["job"]) not in eq["jobs"]:
        if not quiet:
            print(f"{state['job']}無法裝備 {eq['name']}。")
        return False
    if state["inventory"].get(item_id, 0) <= 0:
        if not quiet:
            print("背包中沒有這件裝備。")
        return False
    slot = eq["slot"]
    old = state["equipment"].get(slot)
    remove_item(state, item_id, 1)
    if old:
        add_item(state, old, 1)
    state["equipment"][slot] = item_id
    clamp_vitals(state)
    if not quiet:
        print(f"已裝備 {eq['name']}。")
    return True


def check_and_normalize_region(state: dict, region_id: str | None) -> str:
    if not region_id or region_id not in REGIONS:
        return "border_fire"
    if not is_unlocked(state, REGIONS[region_id].get("unlock_key")):
        return "border_fire"
    return region_id


BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG = "boss_glen_investigation_accepted"
EARTH_REGION_UNLOCK = "unlock_earth_region_preview"
THUNDER_REGION_UNLOCK = "unlock_thunder_region_preview"
FINAL_QUEST_ID = "quest_final_demon_king"


def can_pay_items(state: dict, cost: dict) -> bool:
    for item_id, qty in cost.items():
        if item_id.startswith("flag:"):
            flag = item_id.split(":", 1)[1]
            if not state["flags"].get(flag):
                return False
            continue
        if state["inventory"].get(item_id, 0) < qty:
            return False
    return True


def pay_items(state: dict, cost: dict) -> None:
    for item_id, qty in cost.items():
        if item_id.startswith("flag:"):
            continue
        remove_item(state, item_id, qty)


def quest_unlocked(state: dict, quest_id: str) -> bool:
    if quest_id == "quest_register":
        return True
    if quest_id in {"quest_cave_gathering", "quest_magic_crystal"}:
        return "quest_register" in state["completed_quests"]
    if quest_id == "quest_mine_scout":
        return "quest_cave_gathering" in state["completed_quests"]
    if quest_id == "quest_boss_glen":
        return (
            "quest_mine_scout" in state["completed_quests"]
            and (
                state["flags"].get(BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG, False)
                or state["flags"].get("boss_glen_defeated", False)
                or quest_id in state["completed_quests"]
            )
        )
    if quest_id == "quest_ash_ravine_scout":
        return "quest_boss_glen" in state["completed_quests"]
    if quest_id == "quest_supply_upgrade":
        return state["flags"].get("ash_guardian_defeated", False)
    if quest_id == "quest_cinder_depths_scout":
        return "quest_supply_upgrade" in state["completed_quests"]
    if quest_id == "quest_ice_minor_a":
        return is_unlocked(state, ICE_REGION_UNLOCK)
    if quest_id == "quest_ice_minor_b":
        return "quest_ice_minor_a" in state["completed_quests"]
    if quest_id == "quest_ice_main_phase_1":
        return "quest_ice_minor_b" in state["completed_quests"]
    if quest_id == "quest_ice_main_phase_2":
        return "quest_ice_main_phase_1" in state["completed_quests"]
    if quest_id == "quest_ice_return_handoff":
        return "quest_ice_main_phase_2" in state["completed_quests"]
    if quest_id == "quest_earth_minor_a":
        return is_unlocked(state, EARTH_REGION_UNLOCK)
    if quest_id == "quest_earth_minor_b":
        return "quest_earth_minor_a" in state["completed_quests"]
    if quest_id == "quest_earth_main_phase_1":
        return "quest_earth_minor_b" in state["completed_quests"]
    if quest_id == "quest_earth_main_phase_2":
        return "quest_earth_main_phase_1" in state["completed_quests"]
    if quest_id == "quest_earth_return_handoff":
        return "quest_earth_main_phase_2" in state["completed_quests"]
    if quest_id == "quest_thunder_minor_a":
        return is_unlocked(state, THUNDER_REGION_UNLOCK)
    if quest_id == "quest_thunder_minor_b":
        return "quest_thunder_minor_a" in state["completed_quests"]
    if quest_id == "quest_thunder_main_phase_1":
        return "quest_thunder_minor_b" in state["completed_quests"]
    if quest_id == "quest_thunder_main_phase_2":
        return "quest_thunder_main_phase_1" in state["completed_quests"]
    if quest_id == "quest_thunder_return_handoff":
        return "quest_thunder_main_phase_2" in state["completed_quests"]
    if quest_id == "quest_final_minor_a":
        return is_unlocked(state, FINAL_REGION_UNLOCK)
    if quest_id == "quest_final_minor_b":
        return "quest_final_minor_a" in state["completed_quests"]
    if quest_id == "quest_final_main_phase_1":
        return "quest_final_minor_b" in state["completed_quests"]
    if quest_id == "quest_final_main_phase_2":
        return "quest_final_main_phase_1" in state["completed_quests"]
    if quest_id == FINAL_QUEST_ID:
        return "quest_final_main_phase_2" in state["completed_quests"]
    return False


def quest_ready(state: dict, quest_id: str) -> bool:
    if quest_id in state["completed_quests"]:
        return False
    return can_pay_items(state, QUESTS[quest_id]["turn_in"])


def player_summary_line(state: dict) -> str:
    clamp_vitals(state)
    stats = get_stats(state)
    return (
        f"{state['name']} / {state['job']} Lv{state['level']} / "
        f"HP {state['current_hp']}/{stats['max_hp']} / "
        f"MP {state['current_mp']}/{stats['max_mp']} / {state['gold']}G"
    )


def player_resource_lines(state: dict) -> list[str]:
    stats = get_stats(state)
    return [
        player_summary_line(state),
        f"工會積分 {state['guild_points']} / 經驗 {state['exp']}/{exp_to_next(state['level'])}",
        (
            f"攻擊 {stats['attack']} / 魔攻 {stats['magic_attack']} / 防禦 {stats['defense']} / 魔防 {stats['magic_defense']} / "
            f"敏捷 {stats['agility']} / 暴擊 {stats['crit']}% / 效果命中 {stats['effect_accuracy']}%"
        ),
        ] + [
            f"火抗 {stats['fire_resist']}% / 冰抗 {stats['ice_resist']}% / 地抗 {stats['earth_resist']}% / 雷抗 {stats['thunder_resist']}%"
        ]


def add_gold(state: dict, amount: int, run_log: dict | None = None) -> None:
    if amount <= 0:
        return
    state["gold"] += amount
    if run_log is not None:
        run_log["gold"] += amount


def add_loot(state: dict, item_id: str, qty: int, run_log: dict | None = None) -> None:
    add_item(state, item_id, qty)
    if run_log is not None:
        run_log["items"][item_id] = run_log["items"].get(item_id, 0) + qty
