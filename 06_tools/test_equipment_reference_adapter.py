"""In-memory checks for the B4B-0 static/instance equipment reference adapter."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
for module_root in (REPO_ROOT / "03_engine", REPO_ROOT / "04_data"):
    if str(module_root) not in sys.path:
        sys.path.insert(0, str(module_root))

from data import EQUIPMENT
from engine.equipment_refs import equipment_base_id, resolve_equipment_ref
from engine.gui_actions import GuiRuntimeSession, get_inventory_preview_data, get_status_preview_data
from engine.gui_storage_model import storage_screen_model
from engine.state import create_state, equip_item, get_stats, owns_item_or_equipped


def run() -> None:
    state = create_state("adapter", "劍士")
    state["equipment_instances"] = {
        "eqi_0001": {
            "base_item_id": "weapon_wood_sword",
            "generation_version": 0,
            "roll_index": 0,
            "major_affix_id": None,
            "minor_affix_id": None,
        },
        "eqi_0002": {
            "base_item_id": "weapon_wood_sword",
            "generation_version": 0,
            "roll_index": 0,
            "major_affix_id": None,
            "minor_affix_id": None,
        },
    }
    state["inventory"] = {"eqi_0001": 1, "eqi_0002": 1}
    equipment_before = copy.deepcopy(EQUIPMENT)
    base_attack = get_stats(state)["attack"]

    assert equipment_base_id(state, "eqi_0001") == "weapon_wood_sword"
    assert resolve_equipment_ref(state, "eqi_0001")["base"]["name"] == EQUIPMENT["weapon_wood_sword"]["name"]
    assert equip_item(state, "eqi_0001", quiet=True)
    assert state["equipment"]["weapon"] == "eqi_0001"
    assert state["inventory"] == {"eqi_0002": 1}
    assert owns_item_or_equipped(state, "weapon_wood_sword")
    assert get_stats(state)["attack"] == base_attack + EQUIPMENT["weapon_wood_sword"]["stats"]["attack"]
    assert EQUIPMENT == equipment_before

    preview = get_inventory_preview_data(state)
    assert any(row["item_id"] == "eqi_0001" and row["category"] == "裝備" for row in preview)
    assert get_status_preview_data(state)["equipment"][0]["item_name"] == EQUIPMENT["weapon_wood_sword"]["name"]
    storage = storage_screen_model(state)
    assert storage["inventory_rows"][0]["category"] == "equipment"

    session = GuiRuntimeSession()
    session.state = state
    response = session.dispatch("equip_weapon", {"item_id": "eqi_0002"}, screen_id="workshop_screen")
    assert response["ok"] is True
    assert state["equipment"]["weapon"] == "eqi_0002"
    assert state["inventory"] == {"eqi_0001": 1}


if __name__ == "__main__":
    run()
    print("equipment reference adapter checks passed")
