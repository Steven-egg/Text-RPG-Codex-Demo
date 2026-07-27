from __future__ import annotations

"""Focused deterministic contracts for readable monster race gameplay data."""

import math
import sys
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from data import (  # noqa: E402
    MONSTERS,
    MONSTER_RACE_RULES,
    PHYSICAL_STATUS_EFFECTIVENESS_MULTIPLIERS,
)
from engine import game  # noqa: E402
from engine.state import create_state  # noqa: E402


VALID_RACES = {"beast", "humanoid", "plant", "construct", "spirit", "aberration"}


def enemy_for(race: str) -> dict:
    return {
        "name": f"{race} QA target",
        "race": race,
        "hp": 100,
        "attack": 40,
        "defense": 0,
        "magic_defense": 0,
        "agility": 0,
        "crit": 0,
        "element": "無",
    }


def test_data_contract_and_status_consumer() -> None:
    assert set(MONSTER_RACE_RULES) == VALID_RACES
    assert all(monster.get("race") in VALID_RACES for monster in MONSTERS.values())
    assert PHYSICAL_STATUS_EFFECTIVENESS_MULTIPLIERS == {
        "effective": 1.25,
        "normal": 1.0,
        "ineffective": 0.0,
    }
    for race, rule in MONSTER_RACE_RULES.items():
        target = enemy_for(race)
        assert game.monster_race_display_name(target) == rule["display_name"]
        assert game.monster_race_trait(target)["id"] == rule["trait"]["id"]
        for status, effectiveness in rule["physical_status"].items():
            assert game.physical_status_effectiveness(target, status) == effectiveness
            assert game.physical_status_damage_multiplier(target, status) == PHYSICAL_STATUS_EFFECTIVENESS_MULTIPLIERS[effectiveness]


def test_visible_one_shot_direct_wards() -> None:
    cases = (("construct", "physical"), ("spirit", "magic"))
    for race, damage_type in cases:
        target = enemy_for(race)
        buffs: dict = {}
        assert game.monster_race_trait_summary(target, buffs).endswith("1")
        reduced, events = game.apply_monster_race_direct_damage_trait(target, buffs, 100, damage_type)
        ratio = MONSTER_RACE_RULES[race]["trait"]["effect"]["ratio"]
        expected = math.ceil(100 * (1 - ratio))
        assert reduced == expected
        assert events and f"吸收 {100 - expected}" in events[0]
        assert game.monster_race_trait_summary(target, buffs).endswith("0")
        unchanged, second_events = game.apply_monster_race_direct_damage_trait(target, buffs, 100, damage_type)
        assert unchanged == 100 and not second_events

        other_type = "magic" if damage_type == "physical" else "physical"
        fresh_buffs: dict = {}
        unchanged, wrong_type_events = game.apply_monster_race_direct_damage_trait(target, fresh_buffs, 100, other_type)
        assert unchanged == 100 and not wrong_type_events


def test_plant_one_shot_regrowth() -> None:
    target = enemy_for("plant")
    buffs: dict = {}
    adjusted, events = game.apply_monster_race_threshold_recovery(target, 60, 20, buffs)
    assert adjusted == 12
    assert events == ["種族特性【紮根再生】發動，回復 8 HP。"]
    assert buffs[game.RACE_TRAIT_STATE_KEY]["healing"] == 8
    unchanged, second_events = game.apply_monster_race_threshold_recovery(target, 40, 20, buffs)
    assert unchanged == 20 and not second_events


def test_actual_plant_boss_probe() -> None:
    target = deepcopy(MONSTERS["boss_earth_rootwarden"])
    assert target["race"] == "plant" and target.get("boss") is True
    state = create_state("plant-probe", "牧師")
    enemy_hp = math.ceil(target["hp"] * 0.60)
    raw_damage = math.ceil(target["hp"] * 0.20)
    expected_heal = math.ceil(target["hp"] * MONSTER_RACE_RULES["plant"]["trait"]["effect"]["ratio"])
    with patch("engine.game.calc_player_damage", return_value=(raw_damage, False)):
        result = game.player_attack(state, target, enemy_hp, None, {}, {})
    assert result.damage == raw_damage - expected_heal
    assert any(f"回復 {expected_heal} HP" in event for event in result.events)


def test_threshold_and_action_count_enemy_traits() -> None:
    humanoid = enemy_for("humanoid")
    humanoid_buffs: dict = {}
    events = game.prepare_monster_race_enemy_turn(humanoid, 50, humanoid_buffs)
    assert events and humanoid_buffs["defense_up"] == 2
    assert not game.prepare_monster_race_enemy_turn(humanoid, 40, humanoid_buffs)

    state = create_state("race-contract", "牧師")
    beast = enemy_for("beast")
    baseline = game.calc_enemy_damage(deepcopy(beast), state, 1.0, "物理", {}, False)
    beast_buffs: dict = {}
    events = game.prepare_monster_race_enemy_turn(beast, 50, beast_buffs)
    assert events and beast["_race_next_attack_multiplier"] == MONSTER_RACE_RULES["beast"]["trait"]["effect"]["value"]
    boosted = game.calc_enemy_damage(beast, state, 1.0, "物理", {}, False)
    assert boosted > baseline and "_race_next_attack_multiplier" not in beast
    assert game.calc_enemy_damage(beast, state, 1.0, "物理", {}, False) == baseline

    aberration = enemy_for("aberration")
    aberration_buffs: dict = {}
    assert not game.prepare_monster_race_enemy_turn(aberration, 100, aberration_buffs)
    assert not game.prepare_monster_race_enemy_turn(aberration, 100, aberration_buffs)
    events = game.prepare_monster_race_enemy_turn(aberration, 100, aberration_buffs)
    assert events and aberration["_race_next_attack_multiplier"] == 1.15
    assert not game.prepare_monster_race_enemy_turn(aberration, 100, aberration_buffs)


def test_player_attack_and_panel_integration() -> None:
    state = create_state("race-contract", "牧師")
    construct = enemy_for("construct")
    enemy_buffs: dict = {}
    with patch("engine.game.calc_player_damage", return_value=(100, False)):
        result = game.player_attack(state, construct, construct["hp"], None, {}, enemy_buffs)
    expected = math.ceil(100 * (1 - MONSTER_RACE_RULES["construct"]["trait"]["effect"]["ratio"]))
    assert result.damage == expected
    assert any("可破裝甲" in event for event in result.events)
    lines = game.combat_panel_lines(state, construct, 20, 2, {}, enemy_buffs, "QA")
    assert any("種族 構裝" in line and "可破裝甲 0" in line for line in lines)


def main() -> None:
    test_data_contract_and_status_consumer()
    test_visible_one_shot_direct_wards()
    test_plant_one_shot_regrowth()
    test_actual_plant_boss_probe()
    test_threshold_and_action_count_enemy_traits()
    test_player_attack_and_panel_integration()
    print("monster race effect contracts passed")


if __name__ == "__main__":
    main()
