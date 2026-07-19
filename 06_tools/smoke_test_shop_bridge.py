from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from engine.gui_actions import GuiRuntimeSession, GuiActionError
from engine import game
from engine.equipment_refs import equipment_base_id, first_inventory_equipment_ref
from data import SHOP_INVENTORY, ITEMS, EQUIPMENT


def run_smoke_test():
    print("Starting Shop Travel Inventory Live bridge smoke test...")

    # Initialize session
    session = GuiRuntimeSession()
    session.new_game(name="冒險旅人", job_id="rogue")
    state = session.require_state()

    # 1. Verify Shop model rows and categories
    model = session.screen_model("shop_screen")
    assert model["screen_id"] == "facility_shop_screen"

    rows = model["list_rows"]
    row_item_ids = [row["item_id"] for row in rows]
    expected_travel_items = [
        i_id for i_id in SHOP_INVENTORY["travel"]
        if (ITEMS.get(i_id) or EQUIPMENT.get(i_id, {})).get("region", "border_fire") == "border_fire"
    ]
    assert row_item_ids == expected_travel_items
    assert len(row_item_ids) == len(expected_travel_items)
    print("Shop model row IDs and order verified matches SHOP_INVENTORY['travel'].")

    # Verify category counts
    category_tabs = {tab["id"]: tab for tab in model["category_tabs"]}
    assert category_tabs["all"]["count"] == len(expected_travel_items)
    assert category_tabs["consumables"]["count"] == 4
    assert category_tabs["tactical"]["count"] == 5
    assert category_tabs["accessories"]["count"] == 3
    print("Category tabs and counts verified.")

    # 2. Happy Path Consumable Purchase (item_potion_s)
    state["gold"] = 100
    state["inventory"]["item_potion_s"] = 0

    response = session.dispatch("buy_item", {"item_id": "item_potion_s"}, screen_id="shop_screen")
    assert response["ok"] is True
    assert state["gold"] == 70  # 100 - 30 = 70G
    assert state["inventory"]["item_potion_s"] == 1
    print("Consumable (item_potion_s) purchase verified.")

    # 3. Happy Path Tactical/Battle Item Purchase (item_escape_scroll)
    # Unlock item_escape_scroll and give enough gold
    game.unlock(state, "item_escape_scroll")
    state["gold"] = 200
    state["inventory"]["item_escape_scroll"] = 0

    response = session.dispatch("buy_item", {"item_id": "item_escape_scroll"}, screen_id="shop_screen")
    assert response["ok"] is True
    assert state["gold"] == 80  # 200 - 120 = 80G
    assert state["inventory"]["item_escape_scroll"] == 1
    print("Tactical item (item_escape_scroll) purchase verified.")

    # 4. Happy Path Accessory Purchase (acc_lucky_charm)
    state["gold"] = 200
    state["equipment"]["accessory"] = None  # Ensure accessory is not equipped

    response = session.dispatch("buy_item", {"item_id": "acc_lucky_charm"}, screen_id="shop_screen")
    assert response["ok"] is True
    assert state["gold"] == 40  # 200 - 160 = 40G
    lucky_charm = first_inventory_equipment_ref(state, "acc_lucky_charm")
    assert lucky_charm and equipment_base_id(state, lucky_charm) == "acc_lucky_charm"
    assert state["equipment"]["accessory"] is None  # Verify accessory is NOT auto-equipped!
    print("Accessory (acc_lucky_charm) purchase verified (goes to inventory only, not auto-equipped).")

    # 5. Verify travel shop owned count includes equipped accessory
    # Currently 1 acc_lucky_charm in inventory, 0 in equipment.
    # Total owned should be 1.
    assert game.travel_shop_owned_count(state, "acc_lucky_charm") == 1

    # Equip the lucky charm manually
    game.equip_item(state, lucky_charm)
    # Now it is equipped (in equipment slot), and count in inventory should be 0.
    assert first_inventory_equipment_ref(state, "acc_lucky_charm") is None
    assert equipment_base_id(state, state["equipment"].get("accessory")) == "acc_lucky_charm"
    
    # Total owned count should still be 1 (because it includes equipped items)
    assert game.travel_shop_owned_count(state, "acc_lucky_charm") == 1
    
    # Let's verify this is reflected in the screen model
    model = session.screen_model("shop_screen")
    lucky_charm_details = model["item_details"]["acc_lucky_charm"]
    assert lucky_charm_details["owned_count"] == 1
    print("travel_shop_owned_count inclusion of equipped accessory verified.")

    # 6. Blocked Path: Locked item (item_potion_m is locked by default)
    session_locked = GuiRuntimeSession()
    session_locked.new_game(name="旅人", job_id="rogue")
    state_locked = session_locked.require_state()
    state_locked["gold"] = 500

    try:
        session_locked.dispatch("buy_item", {"item_id": "item_potion_m"}, screen_id="shop_screen")
        raise AssertionError("Expected locked item purchase to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "商品尚未解鎖或不可購買。"
        print("Blocked Path (Locked item) verified.")

    # 7. Blocked Path: Insufficient Gold
    session_gold = GuiRuntimeSession()
    session_gold.new_game(name="旅人", job_id="rogue")
    state_gold = session_gold.require_state()
    state_gold["gold"] = 10  # Lucky charm costs 160G

    try:
        session_gold.dispatch("buy_item", {"item_id": "acc_lucky_charm"}, screen_id="shop_screen")
        raise AssertionError("Expected insufficient gold purchase to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "金幣不足，無法購買該商品。"
        print("Blocked Path (Insufficient Gold) verified.")

    # 8. Blocked Path: Non-travel Item Rejected
    session_nontravel = GuiRuntimeSession()
    session_nontravel.new_game(name="旅人", job_id="rogue")
    state_nt = session_nontravel.require_state()
    state_nt["gold"] = 500

    try:
        session_nontravel.dispatch("buy_item", {"item_id": "weapon_wood_sword"}, screen_id="shop_screen")
        raise AssertionError("Expected non-travel item purchase to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 400
        assert "此商店不販售該商品" in str(err)
        print("Blocked Path (Non-travel item) verified.")

    print("Shop Travel Inventory bridge smoke test successfully completed all checks!")


if __name__ == "__main__":
    run_smoke_test()
