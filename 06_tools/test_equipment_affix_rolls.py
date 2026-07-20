"""Focused B4B-4 deterministic equipment-affix roll checks."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "03_engine", ROOT / "04_data"):
    if str(module_root) not in sys.path:
        sys.path.insert(0, str(module_root))

from data import AFFIXES, EQUIPMENT
from engine.equipment_refs import equipment_base_id, resolve_equipment_ref
from engine.state import add_item, create_state, roll_equipment_instance


def seeded_state() -> dict:
    state = create_state("rolls", "劍士")
    state["run_seed"] = 246813579
    state["affix_roll_counter"] = 0
    return state


def run() -> None:
    affixes_before = copy.deepcopy(AFFIXES)
    equipment_before = copy.deepcopy(EQUIPMENT)
    first = seeded_state()
    second = seeded_state()

    first_refs = [roll_equipment_instance(first, "weapon_wood_sword") for _ in range(2)]
    second_refs = [roll_equipment_instance(second, "weapon_wood_sword") for _ in range(2)]
    assert first["affix_roll_counter"] == second["affix_roll_counter"] == 2
    for first_ref, second_ref, roll_index in zip(first_refs, second_refs, range(2)):
        first_instance = first["equipment_instances"][first_ref]
        second_instance = second["equipment_instances"][second_ref]
        assert first_instance == second_instance
        assert first_instance["roll_index"] == roll_index
        assert first_instance["generation_version"] == 1
        assert first_instance["major_affix_id"] == "major_sharp"
        assert first_instance["minor_affix_id"] == "minor_agile"
        assert first_ref not in first["inventory"]

    body_ref = roll_equipment_instance(first, "armor_leather_armor")
    body = first["equipment_instances"][body_ref]
    assert body["major_affix_id"] is None
    assert body["minor_affix_id"] in {"minor_agile", "minor_fire_ward"}
    resolved = resolve_equipment_ref(first, body_ref)
    assert resolved and resolved["affixes"]["minor"]["status"] == "valid"

    baseline = seeded_state()
    add_item(baseline, "weapon_wood_sword")
    normal_ref = next(
        reference_id
        for reference_id in baseline["inventory"]
        if equipment_base_id(baseline, reference_id) == "weapon_wood_sword"
    )
    assert baseline["equipment_instances"][normal_ref]["major_affix_id"] is None
    assert baseline["equipment_instances"][normal_ref]["minor_affix_id"] is None
    assert baseline["affix_roll_counter"] == 0

    for invalid_id in ("special_trial_badge", "missing_equipment"):
        state = seeded_state()
        before = copy.deepcopy(state)
        try:
            roll_equipment_instance(state, invalid_id)
            raise AssertionError("invalid equipment roll did not fail")
        except ValueError:
            assert state == before
    assert AFFIXES == affixes_before and EQUIPMENT == equipment_before


if __name__ == "__main__":
    run()
    print("equipment affix roll checks passed")
