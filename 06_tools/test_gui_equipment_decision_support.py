"""Focused regression checks for shop/backpack equipment decision support."""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
for module_root in (REPO_ROOT / "03_engine", REPO_ROOT / "04_data"):
    if str(module_root) not in sys.path:
        sys.path.insert(0, str(module_root))

from engine.equipment_refs import equipment_base_id
from engine.gui_actions import GuiRuntimeSession, get_inventory_preview_data
from engine.gui_workshop_model import workshop_screen_model
from engine.state import add_item, create_state, equip_item


def run() -> None:
    state = create_state("decision-support", "盜賊")
    state["gold"] = 1_000
    add_item(state, "weapon_hunter_dagger")
    dagger_ref = next(
        ref for ref in state["inventory"]
        if equipment_base_id(state, ref) == "weapon_hunter_dagger"
    )
    assert equip_item(state, dagger_ref, quiet=True)

    model = workshop_screen_model(state, "border_fire")
    dagger = next(row for row in model["weapons"] if row["id"] == "weapon_hunter_dagger")
    assert dagger["owned_count"] == 1
    assert dagger["equipped_same_base"] is True
    assert dagger["comparison"]["current_name"] == "獵人短匕"
    assert dagger["stat_rows"]

    session = GuiRuntimeSession()
    session.state = state
    response = session.dispatch(
        "buy_equipment",
        {"item_id": "armor_leather_armor"},
        screen_id="workshop_screen",
    )
    recipe = next(
        row for row in response["screen_model"]["upgrades"]
        if row["id"] == "recipe_leather_armor_plus_1"
    )
    assert recipe["base_inventory_count"] == 1
    assert recipe["base_owned_count"] == 1

    inventory = get_inventory_preview_data(state)
    equipped = next(row for row in inventory if row["item_id"] == dagger_ref)
    assert equipped["equipment"]["status_label"] == "已裝備"
    assert equipped["equipment"]["slot_label"] == "武器"
    assert equipped["equipment"]["stat_rows"]
    assert equipped["equipment"]["comparison"]["current_name"] == "獵人短匕"
    assert equipped["desc"] != "目前沒有額外用途提示。"

    workshop_source = (REPO_ROOT / "07_gui_prototype" / "workshop_screen" / "workshop-screen.js").read_text(encoding="utf-8")
    world_source = (REPO_ROOT / "07_gui_prototype" / "world_map" / "world-map.js").read_text(encoding="utf-8")
    assert "hasAuthoritativeCount" in workshop_source
    assert "item.base_owned_count" in workshop_source
    assert "data-equipment-row" in world_source
    assert "utility-equipment-stat" in world_source


if __name__ == "__main__":
    run()
    print("GUI equipment decision-support checks passed")
