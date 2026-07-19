from __future__ import annotations

"""Focused deterministic checks for Combat Progression v1 foundation."""

import math
import random
import sys
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from data import EQUIPMENT, MONSTERS, SKILLS  # noqa: E402
from engine.game import (  # noqa: E402
    MAX_PHYSICAL_CHARGE,
    apply_dot,
    apply_weapon_effect,
    calc_player_damage,
    element_multiplier,
    get_stats,
    normal_attack_followup,
    passive_triggers_for_event,
    physical_charge,
    physical_status_damage_multiplier,
    physical_status_effectiveness,
    player_attack,
    skill_menu,
    tick_effects,
)
from engine.state import create_state, ensure_state_defaults  # noqa: E402

VALID_RACES = {"beast", "humanoid", "plant", "construct", "spirit", "aberration"}


def test_race_contract() -> None:
    assert MONSTERS
    assert all(monster.get("race") in VALID_RACES for monster in MONSTERS.values())
    expected = {
        "beast": {"bleed": "effective", "poison": "normal"},
        "humanoid": {"bleed": "effective", "poison": "normal"},
        "plant": {"bleed": "ineffective", "poison": "effective"},
        "construct": {"bleed": "ineffective", "poison": "ineffective"},
        "spirit": {"bleed": "ineffective", "poison": "ineffective"},
        "aberration": {"bleed": "normal", "poison": "effective"},
    }
    for race, statuses in expected.items():
        enemy = {"race": race}
        for status, effectiveness in statuses.items():
            assert physical_status_effectiveness(enemy, status) == effectiveness


def test_ineffective_status_skips_accuracy_roll() -> None:
    state = create_state("Foundation Tester", "盜賊")
    enemy = deepcopy(MONSTERS["mon_cracked_golem"])
    effect = SKILLS["skill_backstab"]["on_hit"]
    with patch("engine.game.random.randint", side_effect=AssertionError("accuracy roll must not run")):
        events, applied_status = apply_weapon_effect(state, enemy, effect, {})
    assert events
    assert applied_status is None


def count_ticks(state: dict, enemy: dict, status: str, duration: int, multiplier: float) -> tuple[int, list[int]]:
    enemy_buffs: dict = {}
    apply_dot(enemy_buffs, status, duration, multiplier, "physical", "物理")
    ticks = []
    for _ in range(duration + 1):
        _, damage = tick_effects(state, {}, enemy_buffs, enemy)
        ticks.append(damage)
    return sum(damage > 0 for damage in ticks), ticks


def test_status_durations_and_defense_bypass() -> None:
    state = create_state("Foundation Tester", "盜賊")
    low_defense = deepcopy(MONSTERS["mon_moss_rat"])
    high_defense = deepcopy(low_defense)
    high_defense["defense"] = 999_999
    bleed = SKILLS["skill_backstab"]["on_hit"]
    poison = SKILLS["skill_toxic_edge"]["on_hit"]
    assert bleed["duration"] == 3
    assert poison["duration"] == 5
    bleed_count, low_ticks = count_ticks(state, low_defense, "bleed", bleed["duration"], bleed["multiplier"])
    _, high_ticks = count_ticks(state, high_defense, "bleed", bleed["duration"], bleed["multiplier"])
    poison_count, _ = count_ticks(state, low_defense, "poison", poison["duration"], poison["multiplier"])
    assert bleed_count == 3
    assert poison_count == 5
    assert low_ticks == high_ticks


def test_physical_status_race_damage_multipliers() -> None:
    state = create_state("Foundation Tester", "盜賊")
    base_enemy = deepcopy(MONSTERS["mon_moss_rat"])
    base_enemy["defense"] = 999_999
    bleed = SKILLS["skill_backstab"]["on_hit"]
    poison = SKILLS["skill_toxic_edge"]["on_hit"]
    stats = get_stats(state)

    cases = (
        ("bleed", bleed, "beast", "aberration", "plant"),
        ("poison", poison, "plant", "beast", "construct"),
    )
    for status, effect, effective_race, normal_race, ineffective_race in cases:
        effective_enemy = deepcopy(base_enemy)
        effective_enemy["race"] = effective_race
        normal_enemy = deepcopy(base_enemy)
        normal_enemy["race"] = normal_race
        ineffective_enemy = deepcopy(base_enemy)
        ineffective_enemy["race"] = ineffective_race

        assert physical_status_damage_multiplier(effective_enemy, status) == 1.25
        assert physical_status_damage_multiplier(normal_enemy, status) == 1.0
        assert physical_status_damage_multiplier(ineffective_enemy, status) == 0.0

        _, effective_ticks = count_ticks(state, effective_enemy, status, effect["duration"], effect["multiplier"])
        _, normal_ticks = count_ticks(state, normal_enemy, status, effect["duration"], effect["multiplier"])
        ineffective_count, ineffective_ticks = count_ticks(state, ineffective_enemy, status, effect["duration"], effect["multiplier"])
        assert effective_ticks[0] == math.ceil(stats["attack"] * effect["multiplier"] * 1.25)
        assert normal_ticks[0] == math.ceil(stats["attack"] * effect["multiplier"])
        assert ineffective_count == 0
        assert not any(ineffective_ticks)


def test_physical_charge() -> None:
    warrior = create_state("Foundation Tester", "劍士")
    rogue = create_state("Foundation Tester", "盜賊")
    enemy = deepcopy(MONSTERS["mon_moss_rat"])
    enemy["hp"] = 999_999
    enemy_buffs: dict = {}
    warrior_buffs: dict = {}
    for expected in (1, 2, 3, 3):
        player_attack(warrior, enemy, enemy["hp"], None, warrior_buffs, enemy_buffs)
        assert physical_charge(warrior_buffs) == expected
    assert MAX_PHYSICAL_CHARGE == 3
    rogue_buffs: dict = {}
    player_attack(rogue, enemy, enemy["hp"], None, rogue_buffs, enemy_buffs)
    assert physical_charge(rogue_buffs) == 0
    final_skill = SKILLS["skill_final_05"]
    assert final_skill["charge_bonus_per_stack"] * 3 == 0.48
    random.seed(20260712)
    charged = player_attack(warrior, enemy, enemy["hp"], final_skill, warrior_buffs, enemy_buffs)
    assert physical_charge(warrior_buffs) == 0
    random.seed(20260712)
    uncharged = player_attack(warrior, enemy, enemy["hp"], final_skill, warrior_buffs, enemy_buffs)
    assert charged.damage > uncharged.damage
    warrior_buffs["_physical_charge"] = 2
    player_attack(warrior, enemy, enemy["hp"], SKILLS["skill_arcane_bolt"], warrior_buffs, enemy_buffs)
    assert physical_charge(warrior_buffs) == 2


def test_data_driven_rogue_pseudo_offhands() -> None:
    rogue = create_state("Foundation Tester", "盜賊")
    enemy = deepcopy(MONSTERS["mon_moss_rat"])
    enemy["hp"] = 999_999

    rogue["equipment"]["head"] = "armor_rogue_sleeve_blade"
    sleeve, sleeve_followup = normal_attack_followup(rogue, None)
    assert sleeve["name"] == "影袖副刃"
    assert sleeve_followup == EQUIPMENT["armor_rogue_sleeve_blade"]["normal_attack_followup"]
    assert normal_attack_followup(rogue, SKILLS["skill_backstab"]) is None
    sleeve_result = player_attack(rogue, enemy, enemy["hp"], None, {}, {})
    assert any("影袖副刃" in event and "追擊" in event for event in sleeve_result.events)

    rogue["equipment"]["head"] = "armor_ice_rogue_sleeve_blade"
    ice_followup = EQUIPMENT["armor_ice_rogue_sleeve_blade"]["normal_attack_followup"]
    assert ice_followup["on_hit"]["status"] == "bleed"
    assert ice_followup["on_hit"]["chance"] == 30
    enemy_buffs: dict = {}
    with patch("engine.game.random.randint", return_value=1):
        ice_result = player_attack(rogue, enemy, enemy["hp"], None, {}, enemy_buffs)
    assert any("霜痕袖刃" in event and "追擊" in event for event in ice_result.events)
    assert enemy_buffs["bleed"] == 3

    construct = deepcopy(MONSTERS["mon_cracked_golem"])
    construct["hp"] = 999_999
    construct_buffs: dict = {}
    construct_result = player_attack(rogue, construct, construct["hp"], None, {}, construct_buffs)
    assert "bleed" not in construct_buffs
    assert any("不受流血影響" in event for event in construct_result.events)


def test_removed_guardian_skills_are_filtered_from_legacy_state() -> None:
    state = create_state("Foundation Tester", "盜賊")
    removed_skill_ids = {
        "skill_guardian_rune",
        "skill_ice_03",
        "skill_earth_04",
        "skill_thunder_04",
        "skill_final_04",
    }
    state["learned_skills"].extend(removed_skill_ids)
    ensure_state_defaults(state)
    assert not (set(state["learned_skills"]) & removed_skill_ids)
    assert all(skill_id in SKILLS for skill_id in state["learned_skills"])


def test_passive_quickstep_charge_and_menu_filter() -> None:
    warrior = create_state("Foundation Tester", "劍士")
    warrior["learned_skills"] = ["skill_quickstep", "skill_final_05"]
    enemy = deepcopy(MONSTERS["mon_moss_rat"])
    enemy["hp"] = 999_999
    player_buffs: dict = {}
    for _ in range(3):
        player_attack(warrior, enemy, enemy["hp"], None, player_buffs, {})
    assert player_buffs["_warrior_quickstep_ready"]["damage_percent"] == 25
    assert skill_menu({**warrior, "learned_skills": ["skill_quickstep"]}, enemy, {}, {}).outcome == "cancel"
    random.seed(20260719)
    prepared = player_attack(warrior, enemy, enemy["hp"], SKILLS["skill_final_05"], player_buffs, {})
    assert physical_charge(player_buffs) == 0
    assert "_warrior_quickstep_ready" not in player_buffs
    baseline_buffs = {"_physical_charge": 3}
    random.seed(20260719)
    baseline = player_attack(warrior, enemy, enemy["hp"], SKILLS["skill_final_05"], baseline_buffs, {})
    assert prepared.damage > baseline.damage


def test_rogue_passive_pursuit_and_froststep_replacement() -> None:
    rogue = create_state("Foundation Tester", "盜賊")
    rogue["learned_skills"] = ["skill_quickstep", "skill_ice_05", "skill_backstab"]
    rogue["equipment"]["head"] = "armor_ice_rogue_sleeve_blade"
    triggers = passive_triggers_for_event(rogue, "physical_status_applied", status="bleed")
    assert len(triggers) == 1 and triggers[0]["skill_id"] == "skill_ice_05"
    enemy = deepcopy(MONSTERS["mon_moss_rat"])
    enemy["hp"] = 999_999
    player_buffs: dict = {}
    enemy_buffs: dict = {}
    with patch("engine.game.random.randint", return_value=1):
        player_attack(rogue, enemy, enemy["hp"], SKILLS["skill_backstab"], player_buffs, enemy_buffs)
        assert player_buffs["_rogue_pursuit"]["skill_id"] == "skill_ice_05"
        result = player_attack(rogue, enemy, enemy["hp"], None, player_buffs, enemy_buffs)
    assert any("霜速術追擊發動" in event for event in result.events)
    # The consumed window may be freshly re-armed only by this normal attack's
    # separate, successful sleeve-blade status application.
    assert player_buffs["_rogue_pursuit"]["skill_id"] == "skill_ice_05"


def test_cinder_mark_data_expires_without_overlap() -> None:
    mage = create_state("Foundation Tester", "法師")
    mage["learned_skills"] = ["skill_cinder_mark"]
    enemy = {"name": "Test Enemy", "element": "Ice", "defense": 1, "magic_defense": 1}
    enemy_buffs: dict = {}
    base_fire, _ = calc_player_damage(mage, enemy, SKILLS["skill_spark"], {}, enemy_buffs)
    base_ice, _ = calc_player_damage(mage, enemy, SKILLS["skill_ice_needle"], {}, enemy_buffs)
    base_multiplier = element_multiplier("fire", "ice", enemy_buffs)
    with patch("engine.game.action_menu_panel", return_value=1):
        skill_menu(mage, enemy, {}, enemy_buffs)
    assert enemy_buffs["cinder_mark"] == 5
    assert enemy_buffs["_debuff_data"]["cinder_mark"] == {"damage_percent": 50, "damage_scope": "elemental_magic"}
    assert element_multiplier("fire", "ice", enemy_buffs) == base_multiplier
    marked_fire, _ = calc_player_damage(mage, enemy, SKILLS["skill_spark"], {}, enemy_buffs)
    marked_ice, _ = calc_player_damage(mage, enemy, SKILLS["skill_ice_needle"], {}, enemy_buffs)
    assert marked_fire > base_fire and marked_ice > base_ice
    for _ in range(5):
        tick_effects(mage, {}, enemy_buffs)
    assert "cinder_mark" not in enemy_buffs
    assert "cinder_mark" not in enemy_buffs.get("_debuff_data", {})
    assert element_multiplier("fire", "ice", enemy_buffs) == base_multiplier


def main() -> None:
    test_race_contract()
    test_ineffective_status_skips_accuracy_roll()
    test_status_durations_and_defense_bypass()
    test_physical_status_race_damage_multipliers()
    test_physical_charge()
    test_data_driven_rogue_pseudo_offhands()
    test_removed_guardian_skills_are_filtered_from_legacy_state()
    test_passive_quickstep_charge_and_menu_filter()
    test_rogue_passive_pursuit_and_froststep_replacement()
    test_cinder_mark_data_expires_without_overlap()
    print("combat progression foundation checks ok")


if __name__ == "__main__":
    main()
