from __future__ import annotations

import math
from copy import deepcopy
from data import (
    JOBS,
    MONSTERS,
    DUNGEONS,
    EQUIPMENT,
    QUESTS,
    REGIONS,
    get_unlocked_regions,
)

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
        "storage_unlocked": False,
        "storage": {},
        "bestiary": [],
    }
    for item_id, qty in QUESTS["quest_register"]["reward"]["items"].items():
        add_item(state, item_id, qty)
    equip_item(state, "special_trial_badge", quiet=True)
    return state


def ensure_state_defaults(state: dict) -> dict:
    if not isinstance(state.get("flags"), dict):
        state["flags"] = {}
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
    return state


def add_item(state: dict, item_id: str, qty: int = 1) -> None:
    if qty <= 0:
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
    if state["inventory"].get(item_id, 0) > 0:
        return True
    return item_id in state["equipment"].values()


def consume_item_or_equipped(state: dict, item_id: str) -> bool:
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


def get_stats(state: dict, buffs: dict | None = None) -> dict:
    job = JOBS[state["job"]]
    stats = deepcopy(job["base"])
    level_bonus = state["level"] - 1
    for key, value in job["growth"].items():
        stats[key] += value * level_bonus
    extra_count = (state["level"] - 1) // 3
    for key, value in job["extra_every_3"].items():
        stats[key] = stats.get(key, 0) + value * extra_count

    stats["magic_attack"] = 0
    stats["fire_resist"] = 0
    stats["trap_evasion"] = 0
    stats["rare_drop"] = 0

    for item_id in state["equipment"].values():
        if not item_id:
            continue
        for key, value in EQUIPMENT[item_id].get("stats", {}).items():
            stats[key] = stats.get(key, 0) + value

    if buffs:
        if buffs.get("defense_up", 0) > 0:
            stats["defense"] = math.ceil(stats["defense"] * 1.2)
        if buffs.get("defense_down", 0) > 0:
            stats["defense"] = max(1, math.floor(stats["defense"] * 0.8))
        if buffs.get("quickstep", 0) > 0:
            stats["agility"] = math.ceil(stats["agility"] * 1.25)

    stats["fire_resist"] = min(stats.get("fire_resist", 0), 75)
    return stats


def clamp_vitals(state: dict) -> None:
    stats = get_stats(state)
    state["current_hp"] = max(0, min(state["current_hp"], stats["max_hp"]))
    state["current_mp"] = max(0, min(state["current_mp"], stats["max_mp"]))


def equip_item(state: dict, item_id: str, quiet: bool = False) -> bool:
    if item_id not in EQUIPMENT:
        return False
    eq = EQUIPMENT[item_id]
    if state["job"] not in eq["jobs"]:
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
