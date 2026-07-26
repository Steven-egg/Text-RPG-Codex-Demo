"""Focused regression checks for formal supplies and Rogue/Cleric quality gear."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "03_engine", ROOT / "04_data"):
    sys.path.insert(0, str(module_root))

from data import ITEMS, SHOP_INVENTORY
from engine.dungeon import boss_available_at_dungeon_end
from engine.equipment_quality import BOSS_QUALITY, QUALITY_AFFIX_MULTIPLIERS, QUALITY_ENVELOPES, roll_craft_quality
from engine.equipment_refs import resolve_equipment_ref
from engine.state import create_state, ensure_state_defaults, grant_quality_equipment


def run() -> None:
    assert ITEMS["item_potion_s"]["name"] == "旅行回復劑"
    assert ITEMS["item_focus_drop"]["name"] == "靈泉滴露"
    assert "item_potion_m" not in ITEMS and "item_potion_m" not in SHOP_INVENTORY["travel"]

    legacy = {"inventory": {"item_potion_m": 2}, "equipment": {}, "job": "盜賊"}
    ensure_state_defaults(legacy)
    assert legacy["inventory"]["item_potion_s"] == 4

    rogue = create_state("rogue", "盜賊")
    ref = grant_quality_equipment(rogue, "weapon_ice_rogue_01", "epic")
    resolved = resolve_equipment_ref(rogue, ref)
    assert resolved and resolved["quality"] == "epic"
    assert rogue["equipment_instances"][ref]["pattern_id"] in {"edge", "tempo"}
    assert QUALITY_ENVELOPES["legendary"] == 0.70
    assert QUALITY_AFFIX_MULTIPLIERS == {
        "fine": 1.00,
        "rare": 1.15,
        "epic": 1.35,
        "legendary": 1.60,
    }
    quality_attack_values = {}
    for quality in ("fine", "rare", "epic", "legendary"):
        quality_ref = grant_quality_equipment(rogue, "weapon_ice_rogue_01", quality)
        instance = rogue["equipment_instances"][quality_ref]
        # Keep the same legal pattern component so this test isolates quality
        # magnitude rather than the random pattern selection.
        instance["major_affix_id"] = "major_edge"
        instance["minor_affix_id"] = None
        quality_attack_values[quality] = resolve_equipment_ref(rogue, quality_ref)["affix_stats"]["attack"]
    assert list(quality_attack_values.values()) == [1.00, 1.15, 1.35, 1.60]
    assert {roll_craft_quality("ice") for _ in range(50)} <= {"fine", "rare"}
    assert BOSS_QUALITY["boss_final_demon_king"] == "legendary"

    warrior = create_state("warrior", "劍士")
    warrior["flags"]["ice_wreck_captain_defeated"] = False
    assert boss_available_at_dungeon_end(warrior, "dungeon_ice_minor_a", "boss_ice_wreck_captain")


if __name__ == "__main__":
    run()
    print("supply and quality v1 checks passed")
