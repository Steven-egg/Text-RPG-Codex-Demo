"""Focused B4B-5 instance-targeted equipment transaction checks."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "03_engine", ROOT / "04_data"):
    if str(module_root) not in sys.path:
        sys.path.insert(0, str(module_root))

from data import EQUIPMENT
from engine.equipment_refs import equipment_ref_count
from engine.facilities import craft_recipe_message, max_synthesis_count, recipe_base_owned_count
from engine.state import add_item, consume_equipment_reference, create_state, equip_item


def refs_for(state: dict, base_item_id: str) -> list[str]:
    return [
        reference_id
        for reference_id in state["inventory"]
        if state["equipment_instances"].get(reference_id, {}).get("base_item_id") == base_item_id
    ]


def run() -> None:
    state = create_state("recipe-boundary", "劍士")
    state["gold"] = 999
    add_item(state, "weapon_iron_sword", 2)
    add_item(state, "mat_cracked_stone", 5)
    add_item(state, "mat_scorched_iron", 1)
    first_ref, second_ref = refs_for(state, "weapon_iron_sword")
    state["equipment_instances"][first_ref]["major_affix_id"] = "major_sharp"
    assert equip_item(state, first_ref, quiet=True)
    recipe = {"base_item": "weapon_iron_sword", "gold": 180, "materials": {}}
    assert recipe_base_owned_count(state, recipe) == 2
    assert max_synthesis_count(state, "recipe_iron_sword_plus_1") == 1

    before = copy.deepcopy(state)
    assert consume_equipment_reference(state, second_ref)
    assert second_ref not in state["inventory"]
    assert state["equipment"]["weapon"] == first_ref
    assert state["equipment_instances"][first_ref] == before["equipment_instances"][first_ref]
    assert not consume_equipment_reference(state, second_ref)
    assert equipment_ref_count(state, "weapon_iron_sword", include_equipped=True) == 1

    state = before
    result = craft_recipe_message(state, "recipe_iron_sword_plus_1")
    assert result.startswith("完成：")
    assert state["equipment"]["weapon"] == first_ref
    assert second_ref not in state["inventory"]
    assert equipment_ref_count(state, "weapon_iron_sword", include_equipped=True) == 1
    assert equipment_ref_count(state, "weapon_iron_sword_plus_1") == 1
    assert EQUIPMENT["weapon_iron_sword"]["stats"] == {"attack": 12}


if __name__ == "__main__":
    run()
    print("equipment instance recipe boundary checks passed")
