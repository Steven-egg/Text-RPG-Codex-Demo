from __future__ import annotations

"""Deterministic Balance Architecture v2 QA harness.

This is an offline measurement surface.  It intentionally calls the live
combat helpers for attacks, skills, items, enemy turns, effects, relic
selection, and stat calculation, but it never saves state or changes gameplay
data.  B5 promotion and B6 affix values are in-memory QA overlays only.
"""

import argparse
import csv
import io
import json
import math
import random
import sys
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from data import EQUIPMENT, MONSTERS, RELICS, SKILLS  # noqa: E402
from engine import game  # noqa: E402
from engine.relic import select_relic_passive  # noqa: E402
from engine.state import create_state, get_stats  # noqa: E402


SCHEMA_VERSION = "balance-architecture-v2"
DEFAULT_SEEDS = (20260712, 20260713, 20260714, 20260715, 20260716)
LAYERS = ("B0", "B1", "B2", "B3", "B4", "B5", "B6")
MAX_PLAYER_ACTIONS = 500

JOBS = {
    "warrior": "\u528d\u58eb",
    "mage": "\u6cd5\u5e2b",
    "rogue": "\u76dc\u8cca",
    "cleric": "\u7267\u5e2b",
}

REGIONS = {
    "fire": {
        "level": 10,
        "normal": "mon_ember_stalker",
        "boss": "boss_cinder_seal_sentinel",
        "boss_action_cap": 10,
        "relic_count": 0,
    },
    "ice": {
        "level": 18,
        "normal": "mon_ice_outer_guard",
        "boss": "boss_ice_final_seal_lord",
        "boss_action_cap": 12,
        "relic_count": 1,
    },
    "earth": {
        "level": 25,
        "normal": "mon_earth_leyline_guard",
        "boss": "boss_earth_deep_leyline_lord",
        "boss_action_cap": 14,
        "relic_count": 2,
    },
    "thunder": {
        "level": 32,
        "normal": "mon_thunder_array_guard",
        "boss": "boss_thunder_crown_storm_lord",
        "boss_action_cap": 16,
        "relic_count": 3,
    },
    "final": {
        "level": 40,
        "normal": "mon_final_core_guard",
        "boss": "boss_final_demon_king",
        "boss_action_cap": 20,
        "relic_count": 4,
    },
}

# B1 is strictly weapon-only.  B2 and later use the resolved full loadout.
# The fire entries are the currently legal starter / early-fire items; later
# regions deliberately record every carried-forward slot in the output.
FULL_LOADOUTS = {
    "fire": {
        "warrior": {"weapon": "weapon_iron_sword", "head": "armor_leather_cap", "body": "armor_leather_armor", "accessory": "acc_scout_ring"},
        "mage": {"weapon": "weapon_oak_staff", "head": "armor_leather_cap", "body": "armor_traveler_cloth", "accessory": "acc_scout_ring"},
        "rogue": {"weapon": "weapon_hunter_dagger", "head": "armor_rogue_sleeve_blade", "body": "armor_leather_armor", "accessory": "acc_scout_ring"},
        "cleric": {"weapon": "weapon_oak_staff", "head": "armor_leather_cap", "body": "armor_leather_armor", "accessory": "acc_scout_ring"},
    },
    "ice": {
        "warrior": {"weapon": "weapon_ice_warrior_01", "head": "armor_ice_head_01", "body": "armor_ice_body_01", "accessory": "acc_ice_accessory_01"},
        "mage": {"weapon": "weapon_ice_mage_01", "head": "armor_ice_head_01", "body": "armor_traveler_cloth", "accessory": "acc_ice_accessory_01"},
        "rogue": {"weapon": "weapon_ice_rogue_01", "head": "armor_ice_rogue_sleeve_blade", "body": "armor_ice_rogue_body_01", "accessory": "acc_ice_accessory_01"},
        "cleric": {"weapon": "weapon_ice_priest_01", "head": "armor_ice_head_01", "body": "armor_ice_body_01", "accessory": "acc_ice_accessory_01"},
    },
    "earth": {
        "warrior": {"weapon": "weapon_earth_warrior_01", "head": "armor_earth_head_01", "body": "armor_earth_body_01", "accessory": "acc_earth_accessory_01"},
        "mage": {"weapon": "weapon_earth_mage_01", "head": "armor_earth_head_01", "body": "armor_traveler_cloth", "accessory": "acc_earth_accessory_01"},
        "rogue": {"weapon": "weapon_earth_rogue_01", "head": "armor_rogue_sleeve_blade", "body": "armor_earth_rogue_body_01", "accessory": "acc_earth_accessory_01"},
        "cleric": {"weapon": "weapon_earth_priest_01", "head": "armor_earth_head_01", "body": "armor_earth_body_01", "accessory": "acc_earth_accessory_01"},
    },
    "thunder": {
        "warrior": {"weapon": "weapon_thunder_warrior_01", "head": "armor_thunder_head_01", "body": "armor_thunder_body_01", "accessory": "acc_thunder_accessory_01"},
        "mage": {"weapon": "weapon_thunder_mage_01", "head": "armor_thunder_head_01", "body": "armor_traveler_cloth", "accessory": "acc_thunder_accessory_01"},
        "rogue": {"weapon": "weapon_thunder_rogue_01", "head": "armor_rogue_sleeve_blade", "body": "armor_thunder_rogue_body_01", "accessory": "acc_thunder_accessory_01"},
        "cleric": {"weapon": "weapon_thunder_priest_01", "head": "armor_thunder_head_01", "body": "armor_thunder_body_01", "accessory": "acc_thunder_accessory_01"},
    },
    "final": {
        "warrior": {"weapon": "weapon_final_warrior_01", "head": "armor_final_head_01", "body": "armor_final_body_01", "accessory": "acc_final_accessory_01"},
        "mage": {"weapon": "weapon_final_mage_01", "head": "armor_final_head_01", "body": "armor_traveler_cloth", "accessory": "acc_final_accessory_01"},
        "rogue": {"weapon": "weapon_final_rogue_01", "head": "armor_rogue_sleeve_blade", "body": "armor_final_rogue_body_01", "accessory": "acc_final_accessory_01"},
        "cleric": {"weapon": "weapon_final_priest_01", "head": "armor_final_head_01", "body": "armor_final_body_01", "accessory": "acc_final_accessory_01"},
    },
}

CARRY_FORWARD_SLOTS = {
    ("ice", "mage"): ("body",),
    ("earth", "mage"): ("body",),
    ("thunder", "mage"): ("body",),
    ("final", "mage"): ("body",),
    ("earth", "rogue"): ("head",),
    ("thunder", "rogue"): ("head",),
    ("final", "rogue"): ("head",),
}

REGION_SKILLS = {
    "fire": {"warrior": "skill_power_slash", "mage_main": "skill_arcane_bolt", "mage_burst": "skill_spark"},
    "ice": {"warrior": "skill_ice_04", "mage_main": "skill_ice_needle", "mage_burst": "skill_ice_01"},
    "earth": {"warrior": "skill_earth_05", "mage_main": "skill_earth_01", "mage_burst": "skill_earth_02"},
    "thunder": {"warrior": "skill_thunder_05", "mage_main": "skill_thunder_01", "mage_burst": "skill_thunder_02"},
    "final": {"warrior": "skill_final_05", "mage_main": "skill_final_01", "mage_burst": "skill_final_02"},
}

MAGE_ROTATIONS = {
    # Fire is weak to the already-available Ice counterplay.
    "fire": ("skill_ice_needle", "skill_ice_needle"),
    "ice": ("skill_ice_needle", "skill_ice_01"),
    "earth": ("skill_spark", "skill_spark"),
    # Thunder is weak to the already-available Earth counterplay.
    "thunder": ("skill_earth_01", "skill_earth_02"),
    "final": ("skill_final_01", "skill_final_02"),
}

BENCHMARK_TARGETS = {
    "fire": {"normal_actions": (2, 5), "boss_actions": (6, 10), "boss_min_final_hp_ratio": 0.25},
    "ice": {"normal_actions": (2, 5), "boss_actions": (7, 12), "boss_min_final_hp_ratio": 0.25},
    "earth": {"normal_actions": (3, 6), "boss_actions": (8, 14), "boss_min_final_hp_ratio": 0.20},
    "thunder": {"normal_actions": (3, 6), "boss_actions": (9, 16), "boss_min_final_hp_ratio": 0.15},
    "final": {"normal_actions": (4, 7), "boss_actions": (12, 20), "boss_min_final_hp_ratio": 0.10},
}

RELIC_ORDER = (
    "relic_fire_seal",
    "relic_ice_marker_source",
    "relic_earth_marker_source",
    "relic_thunder_marker_source",
)
RELIC_CHOICES = {
    "warrior": ("fire_direct_damage", "ice_magic_defense", "earth_max_hp", "thunder_direct_physical_damage"),
    "mage": ("fire_direct_damage", "ice_direct_magic_damage", "earth_max_hp", "thunder_crit"),
    "rogue": ("fire_crit_damage", "ice_all_resist", "earth_dot_damage", "thunder_effect_accuracy"),
    "cleric": ("fire_direct_damage", "ice_max_mp", "earth_healing_regen", "thunder_all_resist"),
}

RUNTIME_STATS = {
    "attack", "magic_attack", "defense", "magic_defense", "agility", "effect_accuracy", "crit",
    "fire_resist", "ice_resist", "earth_resist", "thunder_resist", "trap_evasion", "rare_drop",
}
SANDBOX_ONLY_STATS = {
    "accuracy", "hp_max", "mp_max", "healing", "hp_regen", "mp_regen", "block_rate", "evasion", "crit_evasion",
}
POWER_WEIGHTS = {
    "attack": 1.00,
    "magic_attack": 1.00,
    "defense": 0.60,
    "magic_defense": 0.70,
    "agility": 1.50,
    "effect_accuracy": 0.75,
    "crit": 1.25,
    "fire_resist": 0.40,
    "ice_resist": 0.40,
    "earth_resist": 0.40,
    "thunder_resist": 0.40,
    "trap_evasion": 0.20,
    "rare_drop": 0.50,
}
QUALITY_ENVELOPES = {"normal": 0.00, "fine": 0.05, "rare": 0.10, "epic": 0.15, "legendary": 0.20}
PER_ITEM_STAT_CAPS = {
    "crit": 5,
    "effect_accuracy": 8,
    "agility": 5,
    "fire_resist": 15,
    "ice_resist": 15,
    "earth_resist": 15,
    "thunder_resist": 15,
}
LOADOUT_STAT_CAPS = {
    "crit": 8,
    "effect_accuracy": 15,
    "agility": 8,
    "fire_resist": 20,
    "ice_resist": 20,
    "earth_resist": 20,
    "thunder_resist": 20,
    "trap_evasion": 10,
    "rare_drop": 3,
}
SLOT_STATS = {
    "weapon": {"attack", "magic_attack", "agility", "effect_accuracy", "crit"},
    "head": {"defense", "magic_defense", "agility", "effect_accuracy", "crit", "fire_resist", "ice_resist", "earth_resist", "thunder_resist"},
    "body": {"defense", "magic_defense", "agility", "crit", "fire_resist", "ice_resist", "earth_resist", "thunder_resist"},
    "accessory": {"defense", "magic_defense", "agility", "effect_accuracy", "crit", "fire_resist", "ice_resist", "earth_resist", "thunder_resist", "trap_evasion", "rare_drop"},
    "special": {"defense", "magic_defense", "agility", "effect_accuracy", "crit", "fire_resist", "ice_resist", "earth_resist", "thunder_resist", "trap_evasion", "rare_drop"},
}

RECORD_FIELDS = (
    "schema_version", "scenario_id", "seed", "rng_stream_id", "layer", "region", "benchmark_level", "job", "target_type", "enemy_id",
    "rotation_id", "result", "player_actions", "enemy_actions", "death_turn", "enemy_hp_remaining_on_death",
    "enemy_hp_remaining_at_end",
    "direct_damage", "dot_damage", "item_damage", "direct_damage_share", "dot_damage_share", "item_damage_share",
    "incoming_damage", "healing", "net_hp_delta_per_turn", "sustain_lock", "initial_hp", "final_hp", "final_hp_ratio",
    "initial_mp", "final_mp", "mp_spent", "mp_recovered", "hp_items_used", "mp_items_used", "battle_items_used",
    "relic_profile", "promotion_profile", "equipment_profile_id", "equipment_profile_complete", "carry_forward_slots",
    "quality_profile", "affix_profile", "quality_saturated", "equipment_base_power", "equipment_total_power",
    "quality_budget_cap", "affix_budget_spent",
    "gear_grind_equivalent",
)


def check_runtime_contracts() -> None:
    """Retain the prior harness's duration and magic-defense safety checks."""
    for monster_id, monster in MONSTERS.items():
        assert monster.get("magic_defense", monster["defense"]) >= 0, monster_id

    dot_duration = SKILLS["skill_sanctified_decay"]["duration"]
    regen_duration = SKILLS["skill_regeneration"]["duration"]
    assert dot_duration == 5 and regen_duration == 5
    state, _loadout, _complete, _carry, _relics = _build_state("cleric", "ice", "full", False, False)
    enemy = deepcopy(MONSTERS["mon_ice_outer_guard"])
    enemy_buffs = {
        "qa_dot": dot_duration,
        "_dot_data": {
            "qa_dot": {
                "multiplier": SKILLS["skill_sanctified_decay"]["multiplier"],
                "damage_type": "magic",
                "element": SKILLS["skill_sanctified_decay"]["element"],
            }
        },
    }
    dot_ticks = 0
    for _ in range(dot_duration):
        _events, damage = game.tick_effects(state, {}, enemy_buffs, enemy)
        dot_ticks += int(damage > 0)
    assert dot_ticks == dot_duration and "qa_dot" not in enemy_buffs

    state["current_hp"] = 1
    regen = SKILLS["skill_regeneration"]
    player_buffs = {"regeneration": regen_duration, "_regen_data": {"amount": regen["amount"], "multiplier": regen["multiplier"]}}
    regen_ticks = 0
    for _ in range(regen_duration):
        before = state["current_hp"]
        game.tick_effects(state, player_buffs, {})
        regen_ticks += int(state["current_hp"] > before)
    assert regen_ticks == regen_duration and "regeneration" not in player_buffs


def _loadout_status(region_id: str, job_key: str, profile: str) -> tuple[dict[str, str | None], str, str]:
    if profile == "naked":
        return {}, "naked", ""
    full = FULL_LOADOUTS[region_id][job_key]
    if profile == "weapon_only":
        return {"weapon": full["weapon"]}, "weapon-only", ""
    carry = CARRY_FORWARD_SLOTS.get((region_id, job_key), ())
    return dict(full), ("carry-forward" if carry else "complete"), ",".join(carry)


def _skill_ids(job_key: str, region_id: str) -> list[str]:
    base = list(create_state("Balance skill probe", JOBS[job_key])["learned_skills"])
    region = REGION_SKILLS[region_id]
    extras = [region["warrior"]] if job_key == "warrior" else []
    if job_key == "mage":
        extras = [region["mage_main"], region["mage_burst"], *MAGE_ROTATIONS[region_id]]
    return list(dict.fromkeys(base + [skill_id for skill_id in extras if skill_id in SKILLS]))


def _apply_relics(state: dict, job_key: str, region_id: str) -> list[str]:
    selected = []
    count = REGIONS[region_id]["relic_count"]
    for relic_id, choice_id in zip(RELIC_ORDER[:count], RELIC_CHOICES[job_key][:count], strict=True):
        state["flags"][RELICS[relic_id]["complete_flag"]] = True
        result = select_relic_passive(state, relic_id, choice_id)
        if result["status"] != "selected":
            raise AssertionError(result)
        selected.append(f"{relic_id}:{choice_id}")
    return selected


def _equipment_power(item_ids: Iterable[str | None]) -> float:
    total = 0.0
    for item_id in item_ids:
        if not item_id:
            continue
        for stat, value in EQUIPMENT[item_id].get("stats", {}).items():
            total += max(0, value) * POWER_WEIGHTS.get(stat, 0.0)
    return round(total, 2)


def _loadout_price(loadout: dict[str, str | None]) -> int:
    return sum(EQUIPMENT[item_id]["price"] for item_id in loadout.values() if item_id)


def _representative_normal_mean_gold(region_id: str) -> float:
    low, high = MONSTERS[REGIONS[region_id]["normal"]]["gold"]
    return (low + high) / 2


def _gear_grind_equivalent(loadout: dict[str, str | None], region_id: str) -> int:
    price = _loadout_price(loadout)
    return math.ceil(price / _representative_normal_mean_gold(region_id)) if price else 0


def _affix_profile(
    job_key: str,
    loadout: dict[str, str | None],
    profile: str,
) -> tuple[dict[str, dict[str, int]], str, str, float, float, bool]:
    """Return in-memory stats and accounting for B6's shared quality envelope."""
    base_power = _equipment_power(loadout.values())
    if profile == "gear_floor":
        return {}, "normal", "none", base_power, 0.0, False
    quality = "rare" if profile == "gear_median" else ("epic" if profile == "gear_ceiling" else "legendary")
    requested = {
        "warrior": (("weapon", "attack"), ("body", "defense"), ("head", "magic_defense"), ("accessory", "crit")),
        "mage": (("weapon", "magic_attack"), ("body", "defense"), ("head", "magic_defense"), ("accessory", "effect_accuracy")),
        "rogue": (("weapon", "attack"), ("body", "defense"), ("head", "agility"), ("accessory", "crit")),
        "cleric": (("weapon", "magic_attack"), ("weapon", "attack"), ("body", "defense"), ("accessory", "effect_accuracy")),
    }[job_key]
    totals = {
        stat: sum(max(0, EQUIPMENT[item_id].get("stats", {}).get(stat, 0)) for item_id in loadout.values() if item_id)
        for stat in LOADOUT_STAT_CAPS
    }
    adjustments: dict[str, dict[str, int]] = {}
    spent = 0.0
    saturated = False
    epic_adjustments: dict[str, dict[str, int]] | None = None
    cursor = 0
    for current_quality, envelope in QUALITY_ENVELOPES.items():
        cap = round(base_power * envelope, 2)
        while True:
            progressed = False
            for _ in requested:
                slot, stat = requested[cursor]
                cursor = (cursor + 1) % len(requested)
                item_id = loadout.get(slot)
                if not item_id:
                    continue
                weight = POWER_WEIGHTS[stat]
                if spent + weight > cap + 0.001:
                    continue
                delta = adjustments.get(item_id, {}).get(stat, 0)
                base_value = max(0, EQUIPMENT[item_id].get("stats", {}).get(stat, 0))
                item_cap = PER_ITEM_STAT_CAPS.get(stat, base_value + 20)
                loadout_cap = LOADOUT_STAT_CAPS.get(stat, totals.get(stat, 0) + 20)
                if base_value + delta >= item_cap or totals.get(stat, 0) >= loadout_cap:
                    continue
                adjustments.setdefault(item_id, {})[stat] = delta + 1
                totals[stat] = totals.get(stat, 0) + 1
                spent += weight
                progressed = True
                break
            if not progressed:
                saturated = spent + min(POWER_WEIGHTS[stat] for _slot, stat in requested) <= cap + 0.001
                break
        if current_quality == "epic":
            epic_adjustments = deepcopy(adjustments)
        if current_quality == quality:
            break
    if quality == "legendary" and adjustments == epic_adjustments:
        saturated = True
    affix_name = {
        "gear_median": "rare_quality",
        "gear_ceiling": "epic_prefix_suffix_shared_cap",
        "gear_legendary_sensitivity": "legendary_sensitivity_not_baseline",
    }[profile]
    return adjustments, quality, affix_name, base_power, round(spent, 2), saturated


@contextmanager
def _temporary_equipment_stats(adjustments: dict[str, dict[str, int]]):
    originals = {item_id: deepcopy(EQUIPMENT[item_id]["stats"]) for item_id in adjustments}
    try:
        for item_id, delta in adjustments.items():
            stats = EQUIPMENT[item_id]["stats"]
            for key, value in delta.items():
                stats[key] = stats.get(key, 0) + value
        yield
    finally:
        for item_id, stats in originals.items():
            EQUIPMENT[item_id]["stats"] = stats


def _comparison_seed(region_id: str, job_key: str, target_type: str, seed: int) -> str:
    """Comparable layers share this seed; layer/profile names never enter it."""
    return f"{SCHEMA_VERSION}:{region_id}:{job_key}:{target_type}:{seed}"


@contextmanager
def _common_random_stream(region_id: str, job_key: str, target_type: str, seed: int):
    original = random.getstate()
    random.seed(_comparison_seed(region_id, job_key, target_type, seed))
    try:
        yield
    finally:
        random.setstate(original)


@contextmanager
def _menu_choice(choice: int):
    original = game.action_menu_panel
    game.action_menu_panel = lambda *_args, **_kwargs: choice
    try:
        yield
    finally:
        game.action_menu_panel = original


def _invoke_skill(state: dict, enemy: dict, player_buffs: dict, enemy_buffs: dict, skill_id: str):
    choice = state["learned_skills"].index(skill_id) + 1
    with _menu_choice(choice):
        return game.skill_menu(state, enemy, player_buffs, enemy_buffs)


def use_tool_item_adapter(state: dict, boss: bool, enemy_buffs: dict, enemy: dict, item_id: str):
    """Thin non-interactive adapter over the live ``combat_item_menu`` behavior."""
    usable_ids = [
        candidate
        for candidate in ("item_potion_s", "item_potion_m", "item_focus_drop", "item_herb_antidote", "item_armor_piercer", "item_escape_scroll")
        if state["inventory"].get(candidate, 0) > 0
    ]
    if item_id not in usable_ids:
        raise ValueError(f"item adapter cannot select unavailable item: {item_id}")
    with _menu_choice(usable_ids.index(item_id) + 1):
        return game.combat_item_menu(state, boss, enemy_buffs, enemy)


def _build_state(
    job_key: str,
    region_id: str,
    equipment_profile: str,
    with_relics: bool,
    boss: bool,
    loadout_override: dict[str, str | None] | None = None,
) -> tuple[dict, dict[str, str | None], str, str, list[str]]:
    state = create_state("Balance QA", JOBS[job_key])
    state["level"] = REGIONS[region_id]["level"]
    state["inventory"] = {}
    state["equipment"] = {"weapon": None, "head": None, "body": None, "accessory": None, "special": None}
    loadout, complete, carry = _loadout_status(region_id, job_key, equipment_profile)
    if loadout_override is not None:
        loadout, complete, carry = dict(loadout_override), "focused-isolate", ""
    state["equipment"].update(loadout)
    state["learned_skills"] = _skill_ids(job_key, region_id)
    relic_profile = _apply_relics(state, job_key, region_id) if with_relics else []
    if boss:
        state["inventory"] = {"item_potion_m": 2, "item_focus_drop": 1, "item_armor_piercer": 1}
    stats = get_stats(state)
    state["current_hp"] = stats["max_hp"]
    state["current_mp"] = stats["max_mp"]
    return state, loadout, complete, carry, relic_profile


def _rogue_status_effective(skill_id: str, enemy: dict) -> bool:
    effect = SKILLS[skill_id].get("on_hit")
    if not effect:
        return True
    return game.physical_status_effectiveness(enemy, effect["status"]) != "ineffective"


def _choose_rotation_action(
    job_key: str,
    region_id: str,
    enemy: dict,
    state: dict,
    player_buffs: dict,
    enemy_buffs: dict,
    turn: int,
    boss: bool,
    item_counts: dict[str, int],
) -> tuple[str, str | None]:
    if job_key == "warrior":
        skill_id = REGION_SKILLS[region_id]["warrior"]
        if game.physical_charge(player_buffs) >= 3 and state["current_mp"] >= SKILLS[skill_id]["mp"]:
            return "skill", skill_id
        return "normal", None
    if job_key == "mage":
        main, burst = MAGE_ROTATIONS[region_id]
        skill_id = burst if turn % 3 == 0 else main
        if state["current_mp"] >= SKILLS[skill_id]["mp"]:
            return "skill", skill_id
        return "normal", None
    if job_key == "rogue":
        candidates = (("skill_backstab", "bleed"), ("skill_toxic_edge", "poison"))
        candidates = sorted(
            candidates,
            key=lambda entry: {"effective": 0, "normal": 1, "ineffective": 2}[
                game.physical_status_effectiveness(enemy, entry[1])
            ],
        )
        for skill_id, status in candidates:
            if (
                game.physical_status_effectiveness(enemy, status) != "ineffective"
                and enemy_buffs.get(status, 0) <= 0
                and state["current_mp"] >= SKILLS[skill_id]["mp"]
            ):
                return "skill", skill_id
        return "normal", None

    decay_key = SKILLS["skill_sanctified_decay"]["name"]
    if enemy_buffs.get(decay_key, 0) <= 0 and state["current_mp"] >= SKILLS["skill_sanctified_decay"]["mp"]:
        return "skill", "skill_sanctified_decay"
    max_hp = get_stats(state, player_buffs)["max_hp"]
    if state["current_hp"] <= max_hp * 0.70 and player_buffs.get("regeneration", 0) <= 0 and state["current_mp"] >= SKILLS["skill_regeneration"]["mp"]:
        return "skill", "skill_regeneration"
    if boss and enemy["defense"] >= 40 and item_counts["battle"] == 0 and state["inventory"].get("item_armor_piercer", 0):
        return "item", "item_armor_piercer"
    if boss and state["current_hp"] <= max_hp * 0.25 and item_counts["hp"] < 2 and state["inventory"].get("item_potion_m", 0):
        return "item", "item_potion_m"
    if boss and state["current_mp"] < 4 and item_counts["mp"] < 1 and state["inventory"].get("item_focus_drop", 0):
        return "item", "item_focus_drop"
    return "normal", None


def _promotion_multiplier(profile: str, source: str) -> float:
    if profile == "none":
        return 1.0
    if profile == "promotion_branch_a":
        return 1.05
    if profile == "promotion_branch_b":
        return 1.10 if source in {"skill", "dot"} else 1.05
    raise ValueError(f"unknown promotion profile: {profile}")


def _clamped_hp(value: int, max_hp: int) -> int:
    return max(0, min(value, max_hp))


def _effective_hp_loss(before: int, after: int, max_hp: int) -> int:
    return max(0, _clamped_hp(before, max_hp) - _clamped_hp(after, max_hp))


def _tick_vital_measurement(state: dict, player_buffs: dict, before: int, after: int) -> tuple[int, int]:
    """Split a live burn/regen tick into effective damage and effective healing."""
    max_hp = get_stats(state)["max_hp"]
    burn_raw = max(1, math.ceil(max_hp * 0.05)) if player_buffs.get("burn", 0) > 0 else 0
    after_burn = before - burn_raw
    burn = _effective_hp_loss(before, after_burn, max_hp)
    healing = max(0, _clamped_hp(after, max_hp) - _clamped_hp(after_burn, max_hp))
    return burn, healing


def _round_outcome(player_hp: int, enemy_hp: int) -> str | None:
    """Match live combat: tick resolves, then player death has precedence."""
    if player_hp <= 0:
        return "player_death"
    if enemy_hp <= 0:
        return "victory"
    return None


def evaluate_benchmark_record(record: dict[str, Any]) -> dict[str, bool]:
    target = BENCHMARK_TARGETS[record["region"]]
    action_band = target["boss_actions" if record["target_type"] == "boss" else "normal_actions"]
    action_target_met = record["result"] == "victory" and action_band[0] <= record["player_actions"] <= action_band[1]
    hp_target_met = True
    if record["target_type"] == "boss":
        hp_target_met = record["result"] == "victory" and record["final_hp_ratio"] >= target["boss_min_final_hp_ratio"]
    return {"action_target_met": action_target_met, "boss_hp_target_met": hp_target_met}


def _scenario_id(layer: str, region_id: str, job_key: str, target: str, profile: str, promotion: str, affix: str, seed: int) -> str:
    return ":".join((layer, region_id, job_key, target, profile, promotion, affix, str(seed)))


def measure_scenario(
    *,
    layer: str,
    region_id: str,
    job_key: str,
    target_type: str,
    seed: int,
    equipment_profile: str,
    rotation: bool,
    relics: bool,
    promotion_profile: str = "none",
    b6_profile: str | None = None,
    loadout_override: dict[str, str | None] | None = None,
    equipment_profile_id: str | None = None,
) -> dict[str, Any]:
    if layer not in LAYERS:
        raise ValueError(f"unknown layer: {layer}")
    if promotion_profile != "none" and REGIONS[region_id]["level"] < 12:
        raise ValueError("promotion overlays are limited to benchmark level 12 and above")
    enemy_id = REGIONS[region_id][target_type]
    boss = target_type == "boss"
    loadout, _complete, _carry = _loadout_status(region_id, job_key, equipment_profile)
    if loadout_override is not None:
        loadout = dict(loadout_override)
    if b6_profile:
        adjustments, quality_profile, affix_profile, base_power, affix_spent, quality_saturated = _affix_profile(job_key, loadout, b6_profile)
    else:
        adjustments, quality_profile, affix_profile = {}, "normal", "none"
        base_power, affix_spent = _equipment_power(loadout.values()), 0.0
        quality_saturated = False
    quality_cap = round(base_power * QUALITY_ENVELOPES[quality_profile], 2)
    if affix_spent > quality_cap + 0.001:
        raise AssertionError(f"affix budget exceeded: {affix_spent} > {quality_cap}")

    with _common_random_stream(region_id, job_key, target_type, seed), _temporary_equipment_stats(adjustments):
        state, _loadout, complete, carry, relic_profile = _build_state(
            job_key, region_id, equipment_profile, relics, boss, loadout_override,
        )
        enemy = deepcopy(MONSTERS[enemy_id])
        enemy_hp = enemy["hp"]
        player_buffs: dict[str, Any] = {}
        enemy_buffs: dict[str, Any] = {}
        boss_marker = False
        direct_damage = dot_damage = item_damage = incoming_damage = healing = 0
        mp_spent = mp_recovered = 0
        item_counts = {"hp": 0, "mp": 0, "battle": 0}
        enemy_actions = 0
        initial_hp, initial_mp = state["current_hp"], state["current_mp"]
        initial_max_hp = get_stats(state)["max_hp"]
        result = "timeout"
        death_turn: int | None = None

        for turn in range(1, MAX_PLAYER_ACTIONS + 1):
            source, value = _choose_rotation_action(job_key, region_id, enemy, state, player_buffs, enemy_buffs, turn, boss, item_counts) if rotation else ("normal", None)
            hp_before_action, mp_before_action = state["current_hp"], state["current_mp"]
            if source == "skill":
                action_result = _invoke_skill(state, enemy, player_buffs, enemy_buffs, value or "")
            elif source == "item":
                action_result = use_tool_item_adapter(state, boss, enemy_buffs, enemy, value or "")
                if value == "item_potion_m":
                    item_counts["hp"] += 1
                elif value == "item_focus_drop":
                    item_counts["mp"] += 1
                else:
                    item_counts["battle"] += 1
            else:
                action_result = game.player_attack(state, enemy, enemy_hp, None, player_buffs, enemy_buffs)
            mp_spent += max(0, mp_before_action - state["current_mp"])
            mp_recovered += max(0, state["current_mp"] - mp_before_action)
            action_max_hp = get_stats(state, player_buffs)["max_hp"]
            healing += max(0, _clamped_hp(state["current_hp"], action_max_hp) - _clamped_hp(hp_before_action, action_max_hp))
            applied_damage = math.ceil(action_result.damage * _promotion_multiplier(promotion_profile, source))
            effective_damage = min(max(0, enemy_hp), max(0, applied_damage))
            enemy_hp -= applied_damage
            if source == "item":
                item_damage += effective_damage
            else:
                direct_damage += effective_damage
            if enemy_hp <= 0:
                result = "victory"
                break

            hp_before_enemy = state["current_hp"]
            boss_marker, _events = game.dispatch_enemy_turn(
                enemy_id, enemy, enemy_hp, state, player_buffs, enemy_buffs, False, turn, boss_marker,
            )
            enemy_actions += 1
            enemy_phase_max_hp = get_stats(state, player_buffs)["max_hp"]
            incoming_damage += _effective_hp_loss(hp_before_enemy, state["current_hp"], enemy_phase_max_hp)

            hp_before_tick = state["current_hp"]
            tick_buffs = deepcopy(player_buffs)
            _events, tick_damage = game.tick_effects(state, player_buffs, enemy_buffs, enemy)
            burn_damage, tick_healing = _tick_vital_measurement(state, tick_buffs, hp_before_tick, state["current_hp"])
            incoming_damage += burn_damage
            healing += tick_healing
            tick_damage = math.ceil(tick_damage * _promotion_multiplier(promotion_profile, "dot"))
            effective_tick_damage = min(max(0, enemy_hp), max(0, tick_damage))
            enemy_hp -= tick_damage
            dot_damage += effective_tick_damage
            outcome = _round_outcome(state["current_hp"], enemy_hp)
            if outcome:
                result = outcome
                if outcome == "player_death":
                    death_turn = turn
                break

        player_actions = turn
        final_hp = max(0, state["current_hp"])
        total_damage = direct_damage + dot_damage + item_damage
        net_hp_delta = (final_hp - initial_hp) / max(1, player_actions)
        sustain_lock = bool(
            boss
            and enemy_actions > REGIONS[region_id]["boss_action_cap"]
            and healing / max(1, incoming_damage) >= 0.90
            and net_hp_delta >= -0.01 * initial_max_hp
        )
        return {
            "schema_version": SCHEMA_VERSION,
            "scenario_id": _scenario_id(
                layer, region_id, job_key, target_type,
                equipment_profile_id or b6_profile or equipment_profile,
                promotion_profile, affix_profile, seed,
            ),
            "seed": seed,
            "rng_stream_id": _comparison_seed(region_id, job_key, target_type, seed),
            "layer": layer,
            "region": region_id,
            "benchmark_level": REGIONS[region_id]["level"],
            "job": job_key,
            "target_type": target_type,
            "enemy_id": enemy_id,
            "rotation_id": "canonical_v2" if rotation else "basic_attack_only",
            "result": result,
            "player_actions": player_actions,
            "enemy_actions": enemy_actions,
            "death_turn": death_turn if result == "player_death" else None,
            "enemy_hp_remaining_on_death": max(0, enemy_hp) if result == "player_death" else None,
            "enemy_hp_remaining_at_end": max(0, enemy_hp),
            "direct_damage": direct_damage,
            "dot_damage": dot_damage,
            "item_damage": item_damage,
            "direct_damage_share": round(direct_damage / total_damage, 6) if total_damage else 0.0,
            "dot_damage_share": round(dot_damage / total_damage, 6) if total_damage else 0.0,
            "item_damage_share": round(item_damage / total_damage, 6) if total_damage else 0.0,
            "incoming_damage": incoming_damage,
            "healing": healing,
            "net_hp_delta_per_turn": round(net_hp_delta, 6),
            "sustain_lock": sustain_lock,
            "initial_hp": initial_hp,
            "final_hp": final_hp,
            "final_hp_ratio": round(final_hp / max(1, initial_hp), 6),
            "initial_mp": initial_mp,
            "final_mp": max(0, state["current_mp"]),
            "mp_spent": mp_spent,
            "mp_recovered": mp_recovered,
            "hp_items_used": item_counts["hp"],
            "mp_items_used": item_counts["mp"],
            "battle_items_used": item_counts["battle"],
            "relic_profile": ",".join(relic_profile) if relic_profile else "none",
            "promotion_profile": promotion_profile,
            "equipment_profile_id": equipment_profile_id or b6_profile or equipment_profile,
            "equipment_profile_complete": complete,
            "carry_forward_slots": carry,
            "quality_profile": quality_profile,
            "affix_profile": affix_profile,
            "quality_saturated": quality_saturated,
            "equipment_base_power": base_power,
            "equipment_total_power": round(base_power + affix_spent, 2),
            "quality_budget_cap": quality_cap,
            "affix_budget_spent": affix_spent,
            "gear_grind_equivalent": _gear_grind_equivalent(loadout, region_id),
        }


def build_records(layers: Iterable[str] = LAYERS, seeds: Iterable[int] = DEFAULT_SEEDS) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    selected_layers = tuple(layers)
    for layer in selected_layers:
        if layer not in LAYERS:
            raise ValueError(f"unknown layer: {layer}")
        for region_id in REGIONS:
            for job_key in JOBS:
                for target_type in ("normal", "boss"):
                    for seed in seeds:
                        if layer == "B0":
                            records.append(measure_scenario(layer=layer, region_id=region_id, job_key=job_key, target_type=target_type, seed=seed, equipment_profile="naked", rotation=False, relics=False))
                        elif layer == "B1":
                            records.append(measure_scenario(layer=layer, region_id=region_id, job_key=job_key, target_type=target_type, seed=seed, equipment_profile="weapon_only", rotation=False, relics=False))
                        elif layer == "B2":
                            records.append(measure_scenario(layer=layer, region_id=region_id, job_key=job_key, target_type=target_type, seed=seed, equipment_profile="full", rotation=False, relics=False))
                        elif layer == "B3":
                            records.append(measure_scenario(layer=layer, region_id=region_id, job_key=job_key, target_type=target_type, seed=seed, equipment_profile="full", rotation=True, relics=False))
                        elif layer == "B4":
                            records.append(measure_scenario(layer=layer, region_id=region_id, job_key=job_key, target_type=target_type, seed=seed, equipment_profile="full", rotation=True, relics=True))
                        elif layer == "B5":
                            profiles = ("none",) if REGIONS[region_id]["level"] < 12 else ("none", "promotion_branch_a", "promotion_branch_b")
                            for profile in profiles:
                                records.append(measure_scenario(layer=layer, region_id=region_id, job_key=job_key, target_type=target_type, seed=seed, equipment_profile="full", rotation=True, relics=True, promotion_profile=profile))
                        else:  # B6
                            for profile in ("gear_floor", "gear_median", "gear_ceiling", "gear_legendary_sensitivity"):
                                records.append(measure_scenario(layer=layer, region_id=region_id, job_key=job_key, target_type=target_type, seed=seed, equipment_profile="full", rotation=True, relics=True, b6_profile=profile))
    return records


def _classify_equipment(equipment_id: str, entry: dict, synthetic_spent: float | None = None, synthetic_cap: float | None = None) -> list[str]:
    findings: list[str] = []
    slot = entry.get("slot")
    if slot not in {"weapon", "head", "body", "accessory", "special"}:
        findings.append("SLOT_ILLEGAL")
    allowed_stats = set(SLOT_STATS.get(slot, ()))
    if slot == "head" and entry.get("normal_attack_followup"):
        allowed_stats.add("attack")
    for stat, value in entry.get("stats", {}).items():
        if stat in SANDBOX_ONLY_STATS or stat.endswith("_damage"):
            findings.append("SANDBOX_ONLY_STAT")
        elif stat not in RUNTIME_STATS:
            findings.append("SANDBOX_ONLY_STAT")
        elif stat not in allowed_stats:
            findings.append("SLOT_ILLEGAL")
        if value > PER_ITEM_STAT_CAPS.get(stat, value):
            findings.append("STACKING_ILLEGAL")
    followup = entry.get("normal_attack_followup")
    if followup:
        if slot != "head":
            findings.append("STACKING_ILLEGAL")
        findings.append("MANUAL_EFFECT_BUDGET")
        on_hit = followup.get("on_hit", {})
        if on_hit.get("status") in {"bleed", "poison"}:
            findings.append("MANUAL_EFFECT_BUDGET")
    if synthetic_spent is not None and synthetic_cap is not None and synthetic_spent > synthetic_cap + 0.001:
        findings.append("OVER_BUDGET")
    return list(dict.fromkeys(findings)) or ["SUPPORTED"]


def _classify_loadout(loadout: dict[str, str | None]) -> list[str]:
    totals: dict[str, int] = {}
    for item_id in loadout.values():
        if not item_id:
            continue
        for stat, value in EQUIPMENT[item_id].get("stats", {}).items():
            totals[stat] = totals.get(stat, 0) + max(0, value)
    return [stat for stat, cap in LOADOUT_STAT_CAPS.items() if totals.get(stat, 0) > cap]


def _lexicon_stat_summary() -> dict[str, str]:
    """Read, but never generate from, the legacy name lexicon for QA drift."""
    lexicon_path = ROOT / "06_tools" / "name_generation_lexicons.json"
    lexicon = json.loads(lexicon_path.read_text(encoding="utf-8"))
    keys: set[str] = set()

    def collect(value: Any) -> None:
        if isinstance(value, dict):
            stats = value.get("stats")
            if isinstance(stats, dict):
                keys.update(stats)
            for nested in value.values():
                collect(nested)
        elif isinstance(value, list):
            for nested in value:
                collect(nested)

    collect(lexicon)
    return {
        key: ("SUPPORTED" if key in RUNTIME_STATS else "SANDBOX_ONLY_STAT")
        for key in sorted(keys)
    }


def audit_equipment() -> dict[str, Any]:
    findings = {equipment_id: _classify_equipment(equipment_id, entry) for equipment_id, entry in sorted(EQUIPMENT.items())}
    loadout_stacking = {
        f"{region_id}:{job_key}": _classify_loadout(loadout)
        for region_id, jobs in FULL_LOADOUTS.items()
        for job_key, loadout in jobs.items()
    }
    manual = {}
    sleeve = dict(FULL_LOADOUTS["ice"]["rogue"])
    control = dict(sleeve)
    control["head"] = "armor_ice_head_01"
    for target_type in ("normal", "boss"):
        head_control = measure_scenario(
            layer="B2", region_id="ice", job_key="rogue", target_type=target_type,
            seed=DEFAULT_SEEDS[0], equipment_profile="full", rotation=False, relics=False,
            loadout_override=control, equipment_profile_id="head-control",
        )
        head_sleeve = measure_scenario(
            layer="B2", region_id="ice", job_key="rogue", target_type=target_type,
            seed=DEFAULT_SEEDS[0], equipment_profile="full", rotation=False, relics=False,
            loadout_override=sleeve, equipment_profile_id="head-sleeve",
        )
        manual[target_type] = {
            "control_head": control["head"],
            "sleeve_head": sleeve["head"],
            "other_slots_equal": all(control[slot] == sleeve[slot] for slot in ("weapon", "body", "accessory")),
            "control_player_actions": head_control["player_actions"],
            "sleeve_player_actions": head_sleeve["player_actions"],
            "control_direct_damage": head_control["direct_damage"],
            "sleeve_direct_damage": head_sleeve["direct_damage"],
            "action_delta": head_sleeve["player_actions"] - head_control["player_actions"],
        }
    return {
        "schema_version": SCHEMA_VERSION,
        "mode": "equipment_audit",
        "findings": findings,
        "loadout_stacking_overages": loadout_stacking,
        "lexicon_stat_summary": _lexicon_stat_summary(),
        "manual_effect_head_slot_isolate": manual,
    }


def render_records(records: list[dict[str, Any]], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(records, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=RECORD_FIELDS, lineterminator="\n", extrasaction="raise")
    writer.writeheader()
    writer.writerows(records)
    return stream.getvalue()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deterministic Balance Architecture v2 QA harness")
    parser.add_argument("--layers", default=",".join(LAYERS), help="comma-separated subset of B0..B6")
    parser.add_argument("--seeds", default=",".join(str(seed) for seed in DEFAULT_SEEDS), help="comma-separated integer seeds")
    parser.add_argument("--format", choices=("csv", "json"), default="csv")
    parser.add_argument("--audit-equipment", action="store_true", help="offline equipment / manual-effect audit only")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    check_runtime_contracts()
    if args.audit_equipment:
        print(json.dumps(audit_equipment(), ensure_ascii=True, sort_keys=True, separators=(",", ":")))
        return
    layers = tuple(layer.strip() for layer in args.layers.split(",") if layer.strip())
    seeds = tuple(int(seed.strip()) for seed in args.seeds.split(",") if seed.strip())
    print(render_records(build_records(layers, seeds), args.format), end="")


if __name__ == "__main__":
    main()
