"""Focused Phase 4B B4B-2 fixed-affix resolver and comparison checks."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "03_engine", ROOT / "04_data"):
    if str(module_root) not in sys.path:
        sys.path.insert(0, str(module_root))

from data import AFFIXES, EQUIPMENT
from engine.equipment_refs import resolve_equipment_ref
from engine.state import add_item, create_state, equipment_comparison, equip_item, get_stats


def run() -> None:
    state = create_state("affixes", "劍士")
    add_item(state, "weapon_wood_sword", 2)
    refs = [ref for ref in state["inventory"] if state["equipment_instances"].get(ref, {}).get("base_item_id") == "weapon_wood_sword"]
    sharp_ref, agile_ref = refs
    state["equipment_instances"][sharp_ref]["major_affix_id"] = "major_sharp"
    state["equipment_instances"][agile_ref]["minor_affix_id"] = "minor_agile"
    unequipped_stats = get_stats(state)

    data_before = copy.deepcopy(AFFIXES)
    equipment_before = copy.deepcopy(EQUIPMENT)
    resolved = resolve_equipment_ref(state, sharp_ref)
    assert resolved and resolved["base"]["stats"]["attack"] == EQUIPMENT["weapon_wood_sword"]["stats"]["attack"]
    assert resolved["effective_stats"]["attack"] == EQUIPMENT["weapon_wood_sword"]["stats"]["attack"] + AFFIXES["major_sharp"]["stats"]["attack"]
    assert resolved["affixes"]["major"] == {
        "id": "major_sharp", "name": AFFIXES["major_sharp"]["name"], "tier": "major",
        "family": AFFIXES["major_sharp"]["family"], "stats": AFFIXES["major_sharp"]["stats"], "status": "valid",
    }
    assert AFFIXES == data_before and EQUIPMENT == equipment_before

    assert equip_item(state, sharp_ref, quiet=True)
    assert get_stats(state)["attack"] == unequipped_stats["attack"] + EQUIPMENT["weapon_wood_sword"]["stats"]["attack"] + AFFIXES["major_sharp"]["stats"]["attack"]
    comparison = equipment_comparison(state, agile_ref)
    assert comparison["stats"]["attack"]["delta"] == -AFFIXES["major_sharp"]["stats"]["attack"]
    assert comparison["stats"]["agility"]["delta"] == AFFIXES["minor_agile"]["stats"]["agility"]
    assert comparison["affixes"]["major"]["change"] == "removed"
    assert comparison["affixes"]["major"]["before"] == "major_sharp"
    assert comparison["affixes"]["minor"]["after"] == "minor_agile"

    state["equipment_instances"][agile_ref]["major_affix_id"] = "minor_agile"
    state_before = copy.deepcopy(state)
    invalid = equipment_comparison(state, agile_ref)
    assert invalid["affixes"]["major"]["after_view"] == {"id": "minor_agile", "status": "invalid_tier"}
    assert invalid["stats"]["agility"]["delta"] == AFFIXES["minor_agile"]["stats"]["agility"]
    assert state == state_before

    state["equipment_instances"][agile_ref]["major_affix_id"] = "major_missing"
    invalid_id = equipment_comparison(state, agile_ref)
    assert invalid_id["affixes"]["major"]["after_view"] == {"id": "major_missing", "status": "invalid_id"}

    add_item(state, "armor_leather_armor")
    body_ref = next(ref for ref in state["inventory"] if state["equipment_instances"].get(ref, {}).get("base_item_id") == "armor_leather_armor")
    state["equipment_instances"][body_ref]["minor_affix_id"] = "minor_fire_ward"
    body_resolved = resolve_equipment_ref(state, body_ref)
    assert body_resolved and body_resolved["affix_stats"] == AFFIXES["minor_fire_ward"]["stats"]
    state["equipment_instances"][agile_ref]["minor_affix_id"] = "minor_fire_ward"
    invalid_slot = equipment_comparison(state, agile_ref)
    assert invalid_slot["affixes"]["minor"]["after_view"] == {"id": "minor_fire_ward", "status": "invalid_slot"}
    assert AFFIXES == data_before and EQUIPMENT == equipment_before


if __name__ == "__main__":
    run()
    print("equipment affix resolution checks passed")
