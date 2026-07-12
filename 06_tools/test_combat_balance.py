from __future__ import annotations

"""Deterministic combat-balance harness.

This is deliberately a measurement tool, not a replacement for the interactive
combat loop.  It reports player actions required to defeat representative
monsters under three profiles:

* no equipment / basic attacks;
* region equipment / basic attacks;
* region equipment / job-specific rotation.

The report is intended to establish approved turn bands before monster values
or skill durations are changed.  Each scenario reseeds ``random`` so output is
stable across runs.
"""

import random
import sys
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from data import MONSTERS, SKILLS  # noqa: E402
from engine.game import player_attack, tick_effects  # noqa: E402
from engine.state import create_state, get_stats  # noqa: E402


SEED = 20260712
TARGET_EFFECT_DURATION = 5
# An unequipped magic job's physical basic attack can legitimately hit for the
# one-damage floor against a late-game boss.  Keep that diagnostic visible in
# the report instead of treating it as a harness failure.
MAX_PLAYER_ACTIONS = 5_000

JOBS = {
    "warrior": "劍士",
    "mage": "法師",
    "rogue": "盜賊",
    "cleric": "牧師",
}

REGIONS = {
    "ice": {
        "level": 15,
        "normal": "mon_ice_outer_guard",
        "boss": "boss_ice_final_seal_lord",
    },
    "earth": {
        "level": 23,
        "normal": "mon_earth_leyline_guard",
        "boss": "boss_earth_deep_leyline_lord",
    },
    "thunder": {
        "level": 30,
        "normal": "mon_thunder_array_guard",
        "boss": "boss_thunder_crown_storm_lord",
    },
    "final": {
        "level": 39,
        "normal": "mon_final_core_guard",
        "boss": "boss_final_demon_king",
    },
}

REGION_EQUIPMENT = {
    "ice": {
        "warrior": ("weapon_ice_warrior_01", "armor_ice_body_01", "acc_ice_accessory_01"),
        "mage": ("weapon_ice_mage_01", None, "acc_ice_accessory_01"),
        "rogue": ("weapon_ice_rogue_01", "armor_ice_rogue_body_01", "acc_ice_accessory_01"),
        "cleric": ("weapon_ice_priest_01", "armor_ice_body_01", "acc_ice_accessory_01"),
    },
    "earth": {
        "warrior": ("weapon_earth_warrior_01", "armor_earth_body_01", "acc_earth_accessory_01"),
        "mage": ("weapon_earth_mage_01", None, "acc_earth_accessory_01"),
        "rogue": ("weapon_earth_rogue_01", "armor_earth_rogue_body_01", "acc_earth_accessory_01"),
        "cleric": ("weapon_earth_priest_01", "armor_earth_body_01", "acc_earth_accessory_01"),
    },
    "thunder": {
        "warrior": ("weapon_thunder_warrior_01", "armor_thunder_body_01", "acc_thunder_accessory_01"),
        "mage": ("weapon_thunder_mage_01", None, "acc_thunder_accessory_01"),
        "rogue": ("weapon_thunder_rogue_01", "armor_thunder_rogue_body_01", "acc_thunder_accessory_01"),
        "cleric": ("weapon_thunder_priest_01", "armor_thunder_body_01", "acc_thunder_accessory_01"),
    },
    "final": {
        "warrior": ("weapon_final_warrior_01", "armor_final_body_01", "acc_final_accessory_01"),
        "mage": ("weapon_final_mage_01", None, "acc_final_accessory_01"),
        "rogue": ("weapon_final_rogue_01", "armor_final_rogue_body_01", "acc_final_accessory_01"),
        "cleric": ("weapon_final_priest_01", "armor_final_body_01", "acc_final_accessory_01"),
    },
}


@dataclass(frozen=True)
class Result:
    actions: int
    direct_damage: int
    dot_damage: int
    utility_actions: int


def build_state(job_key: str, region_id: str, equipped: bool) -> dict:
    state = create_state("Balance Tester", JOBS[job_key])
    state["level"] = REGIONS[region_id]["level"]
    if equipped:
        weapon, body, accessory = REGION_EQUIPMENT[region_id][job_key]
        state["equipment"].update({"weapon": weapon, "body": body, "accessory": accessory})
        if job_key == "rogue":
            # The Rogue's head-slot sleeve blade is a pseudo-offhand: it adds
            # stats and grants a 0.35x follow-up on ordinary attacks.
            state["equipment"]["head"] = "armor_rogue_sleeve_blade"
    stats = get_stats(state)
    state["current_hp"] = stats["max_hp"]
    state["current_mp"] = stats["max_mp"]
    return state


def rotation_skill(job_key: str, region_id: str, action: int) -> dict | None:
    if job_key == "warrior":
        return SKILLS["skill_power_slash"]
    if job_key == "mage":
        return SKILLS[f"skill_{region_id}_01"]
    if job_key == "rogue":
        phase = (action - 1) % 4
        if phase == 0:
            return SKILLS["skill_backstab"]
        if phase == 2:
            return SKILLS["skill_toxic_edge"]
        return None
    if job_key == "cleric" and (action - 1) % 5 == 0:
        return SKILLS["skill_sanctified_decay"]
    return None


def measure_actions(job_key: str, region_id: str, enemy_id: str, profile: str) -> Result:
    random.seed(f"{SEED}:{job_key}:{region_id}:{enemy_id}:{profile}")
    equipped = profile != "naked_basic"
    rotation = profile == "equipped_rotation"
    state = build_state(job_key, region_id, equipped)
    enemy = deepcopy(MONSTERS[enemy_id])
    enemy_buffs: dict = {}
    player_buffs: dict = {}
    enemy_hp = enemy["hp"]
    direct_damage = 0
    dot_damage = 0
    utility_actions = 0

    for action in range(1, MAX_PLAYER_ACTIONS + 1):
        skill = rotation_skill(job_key, region_id, action) if rotation else None
        cleric_phase = (action - 1) % 5 if rotation and job_key == "cleric" else None
        if skill and skill["kind"] == "dot":
            enemy_buffs["sanctified_decay"] = skill["duration"]
            enemy_buffs["_dot_data"] = {
                "sanctified_decay": {
                    "multiplier": skill["multiplier"],
                    "damage_type": "magic",
                    "element": skill["element"],
                }
            }
        elif cleric_phase == 1:
            regen = SKILLS["skill_regeneration"]
            player_buffs["regeneration"] = regen["duration"]
            player_buffs["_regen_data"] = {
                "amount": regen["amount"],
                "multiplier": regen["multiplier"],
            }
            utility_actions += 1
        elif cleric_phase == 3:
            # Item use has no enemy damage here, but its action cost must be
            # included when comparing the Cleric's intended combat rhythm.
            utility_actions += 1
        else:
            action_result = player_attack(state, enemy, enemy_hp, skill, player_buffs, enemy_buffs)
            enemy_hp -= action_result.damage
            direct_damage += action_result.damage
        if enemy_hp <= 0:
            return Result(action, direct_damage, dot_damage, utility_actions)

        _, damage = tick_effects(state, player_buffs, enemy_buffs, enemy)
        enemy_hp -= damage
        dot_damage += damage
        if enemy_hp <= 0:
            return Result(action, direct_damage, dot_damage, utility_actions)

    raise AssertionError(f"{job_key}/{region_id}/{enemy_id}/{profile} exceeded {MAX_PLAYER_ACTIONS} actions")


def check_duration_contracts() -> None:
    dot_duration = SKILLS["skill_sanctified_decay"]["duration"]
    regen_duration = SKILLS["skill_regeneration"]["duration"]
    assert dot_duration > 0 and regen_duration > 0

    state = build_state("cleric", "ice", equipped=True)
    enemy = deepcopy(MONSTERS["mon_ice_outer_guard"])
    enemy_buffs = {
        "test_dot": dot_duration,
        "_dot_data": {
            "test_dot": {
                "multiplier": SKILLS["skill_sanctified_decay"]["multiplier"],
                "damage_type": "magic",
                "element": SKILLS["skill_sanctified_decay"]["element"],
            }
        },
    }
    dot_ticks = 0
    for _ in range(dot_duration):
        _, damage = tick_effects(state, {}, enemy_buffs, enemy)
        dot_ticks += int(damage > 0)
    assert dot_ticks == dot_duration
    assert "test_dot" not in enemy_buffs

    state["current_hp"] = 1
    regen = SKILLS["skill_regeneration"]
    player_buffs = {
        "regeneration": regen_duration,
        "_regen_data": {"amount": regen["amount"], "multiplier": regen["multiplier"]},
    }
    regen_ticks = 0
    for _ in range(regen_duration):
        hp_before = state["current_hp"]
        tick_effects(state, player_buffs, {})
        regen_ticks += int(state["current_hp"] > hp_before)
    assert regen_ticks == regen_duration
    assert "regeneration" not in player_buffs

    print(
        "Effect duration: "
        f"DoT={dot_duration} ({dot_ticks} ticks), regen={regen_duration} ({regen_ticks} ticks), "
        f"target={TARGET_EFFECT_DURATION} "
        f"({'READY' if dot_duration >= TARGET_EFFECT_DURATION and regen_duration >= TARGET_EFFECT_DURATION else 'PENDING DATA CHANGE'})"
    )


def check_magic_defense_fallback() -> None:
    for monster_id, monster in MONSTERS.items():
        effective_magic_defense = monster.get("magic_defense", monster["defense"])
        assert effective_magic_defense >= 0, monster_id


def print_measurements() -> None:
    print("profile,region,job,target,actions,direct_damage,dot_damage,utility_actions")
    for region_id, region in REGIONS.items():
        for job_key in JOBS:
            for profile in ("naked_basic", "equipped_basic", "equipped_rotation"):
                for target in ("normal", "boss"):
                    result = measure_actions(job_key, region_id, region[target], profile)
                    print(
                        f"{profile},{region_id},{job_key},{target},{result.actions},"
                        f"{result.direct_damage},{result.dot_damage},{result.utility_actions}"
                    )


def main() -> None:
    check_magic_defense_fallback()
    check_duration_contracts()
    print_measurements()
    print("Combat balance harness completed.")


if __name__ == "__main__":
    main()
