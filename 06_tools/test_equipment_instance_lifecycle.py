"""Focused Phase 4B B4B-1 equipment instance lifecycle checks."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "03_engine", ROOT / "04_data"):
    if str(module_root) not in sys.path:
        sys.path.insert(0, str(module_root))

from data import EQUIPMENT
from engine.equipment_refs import equipment_base_id, first_inventory_equipment_ref
from engine.state import (
    EQUIPMENT_INSTANCE_STATE_VERSION,
    add_item,
    create_state,
    ensure_state_defaults,
    equipment_comparison,
    equip_item,
)


def assert_unaffixed_instance(state: dict, reference_id: str, base_item_id: str, generation_version: int) -> None:
    instance = state["equipment_instances"][reference_id]
    assert reference_id.startswith("eqi_")
    assert instance == {
        "base_item_id": base_item_id,
        "generation_version": generation_version,
        "roll_index": 0,
        "major_affix_id": None,
        "minor_affix_id": None,
    }


def run() -> None:
    equipment_before = copy.deepcopy(EQUIPMENT)
    legacy = {
        "job": "劍士",
        "current_hp": 38,
        "current_mp": 7,
        "inventory": {"weapon_wood_sword": 2, "special_trial_badge": 1, "item_potion_s": 3},
        "equipment": {"weapon": "weapon_wood_sword", "head": None, "body": None, "accessory": None, "special": "special_trial_badge"},
    }
    ensure_state_defaults(legacy)
    assert legacy["state_version"] == EQUIPMENT_INSTANCE_STATE_VERSION
    assert legacy["current_hp"] == 38 and legacy["current_mp"] == 7
    refs = [ref for ref in legacy["inventory"] if equipment_base_id(legacy, ref) == "weapon_wood_sword"]
    assert len(refs) == 2 and len(set(refs)) == 2
    for ref in refs:
        assert_unaffixed_instance(legacy, ref, "weapon_wood_sword", 0)
    equipped_ref = legacy["equipment"]["weapon"]
    assert equipped_ref not in refs
    assert_unaffixed_instance(legacy, equipped_ref, "weapon_wood_sword", 0)
    assert legacy["inventory"]["special_trial_badge"] == 1
    assert legacy["equipment"]["special"] == "special_trial_badge"
    assert legacy["affix_roll_counter"] == 0
    assert EQUIPMENT == equipment_before

    state = create_state("instances", "劍士")
    seed = state["run_seed"]
    add_item(state, "weapon_wood_sword", 2)
    produced = [ref for ref in state["inventory"] if equipment_base_id(state, ref) == "weapon_wood_sword"]
    assert len(produced) == 2 and len(set(produced)) == 2
    for ref in produced:
        assert_unaffixed_instance(state, ref, "weapon_wood_sword", 1)
    assert state["run_seed"] == seed
    assert state["affix_roll_counter"] == 0
    assert "special_trial_badge" not in state["equipment_instances"]
    assert EQUIPMENT == equipment_before

    candidate = first_inventory_equipment_ref(state, "weapon_wood_sword")
    before = copy.deepcopy(state)
    comparison = equipment_comparison(state, candidate)
    assert comparison["compatible"] is True
    assert comparison["candidate"]["quality"] == "normal"
    assert comparison["candidate"]["upgrade_level"] == 0
    assert comparison["equipped"] is None
    assert comparison["stats"]["attack"]["after"] - comparison["stats"]["attack"]["before"] == EQUIPMENT["weapon_wood_sword"]["stats"]["attack"]
    assert comparison["affixes"]["major"]["change"] == "unchanged"
    assert state == before and EQUIPMENT == equipment_before
    assert equip_item(state, candidate, quiet=True)
    comparison_after = equipment_comparison(state, produced[1])
    assert comparison_after["equipped"]["reference_id"] == candidate
    assert comparison_after["stats"]["attack"]["delta"] == 0

    incompatible = create_state("incompatible", "法師")
    add_item(incompatible, "weapon_wood_sword")
    blocked = equipment_comparison(incompatible, first_inventory_equipment_ref(incompatible, "weapon_wood_sword"))
    assert blocked["compatible"] is False and blocked["reason"]
    assert EQUIPMENT == equipment_before


if __name__ == "__main__":
    run()
    print("equipment instance lifecycle checks passed")
