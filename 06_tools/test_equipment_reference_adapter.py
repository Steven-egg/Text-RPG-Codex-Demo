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
from engine.gui_actions import GuiActionError, GuiRuntimeSession, get_inventory_preview_data, get_status_preview_data
from engine.gui_storage_model import storage_screen_model
from engine.state import add_item, create_state, equip_item, get_stats, owns_item_or_equipped


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
    equipped_row = next(row for row in preview if row["item_id"] == "eqi_0001")
    assert equipped_row["category"] == "裝備"
    assert equipped_row["equipment"]["status_label"] == "已裝備"
    assert equipped_row["equipment"]["slot_label"] == "武器"
    assert equipped_row["equipment"]["stat_rows"]
    assert equipped_row["equipment"]["comparison"]["current_name"] == EQUIPMENT["weapon_wood_sword"]["name"]
    assert get_status_preview_data(state)["equipment"][0]["item_name"] == EQUIPMENT["weapon_wood_sword"]["name"]
    storage = storage_screen_model(state)
    assert storage["inventory_rows"][0]["category"] == "equipment"

    session = GuiRuntimeSession()
    session.state = state
    response = session.dispatch("equip_weapon", {"item_id": "eqi_0002"}, screen_id="workshop_screen")
    assert response["ok"] is True
    assert state["equipment"]["weapon"] == "eqi_0002"
    assert state["inventory"] == {"eqi_0001": 1}

    preview = get_inventory_preview_data(state)
    backpack_sword = next(row for row in preview if row["item_id"] == "eqi_0001")
    assert backpack_sword["equip_action"] == {
        "action_id": "equip_equipment",
        "label": "裝備",
        "enabled": True,
        "disabled_reason": None,
        "payload": {"item_id": "eqi_0001"},
    }
    response = session.dispatch("equip_equipment", {"item_id": "eqi_0001"}, screen_id="world_map")
    assert response["next_screen_id"] == "world_map"
    assert response["screen_model"]["utility_preview"]["type"] == "inventory"
    assert state["equipment"]["weapon"] == "eqi_0001"
    assert state["inventory"] == {"eqi_0002": 1}

    mage = create_state("preview-job-gate", "法師")
    add_item(mage, "weapon_wood_sword")
    mage_ref = next(ref for ref in mage["inventory"] if equipment_base_id(mage, ref) == "weapon_wood_sword")
    mage_row = next(row for row in get_inventory_preview_data(mage) if row["item_id"] == mage_ref)
    assert mage_row["equip_action"]["enabled"] is False
    mage_session = GuiRuntimeSession()
    mage_session.state = mage
    try:
        mage_session.dispatch("equip_equipment", {"item_id": mage_ref}, screen_id="world_map")
        raise AssertionError("job-incompatible inventory equipment unexpectedly equipped")
    except GuiActionError as error:
        assert error.status == 409 and error.blocked_reason == "職業不符"


if __name__ == "__main__":
    run()
    print("equipment reference adapter checks passed")
