"""Focused B4B-3a CLI affix presentation checks."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "03_engine", ROOT / "04_data"):
    if str(module_root) not in sys.path:
        sys.path.insert(0, str(module_root))

from data import AFFIXES, EQUIPMENT
from engine.formatting import equipment_affix_summary, equipment_summary, format_affix_view
from engine.state import add_item, create_state


def run() -> None:
    assert format_affix_view({"id": None, "status": "none"}) == "無"
    assert format_affix_view({"id": "missing", "status": "invalid_id"}) == "異常詞綴 (missing)"
    assert format_affix_view({
        "id": "major_sharp", "name": "鋒利", "tier": "major", "family": "physical_edge",
        "stats": {"attack": 1}, "status": "valid",
    }) == "鋒利 (attack +1)"
    assert equipment_affix_summary({"major": {"id": None, "status": "none"}, "minor": {"id": None, "status": "none"}}) == "主詞綴：無／次詞綴：無"

    state = create_state("cli", "劍士")
    add_item(state, "weapon_wood_sword")
    reference_id = next(ref for ref in state["inventory"] if state["equipment_instances"].get(ref, {}).get("base_item_id") == "weapon_wood_sword")
    state["equipment_instances"][reference_id]["major_affix_id"] = "major_sharp"
    summary = equipment_summary(reference_id, state)
    assert f"{EQUIPMENT['weapon_wood_sword']['stats']['attack'] + AFFIXES['major_sharp']['stats']['attack']:+}" in summary


if __name__ == "__main__":
    run()
    print("equipment CLI affix presentation checks passed")
