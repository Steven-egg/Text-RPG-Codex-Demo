from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from engine.gui_actions import GuiRuntimeSession, GuiActionError


def run_smoke_test():
    print("Starting Storage Unlock & View Live MVP bridge smoke test...")

    # 1. Setup session
    session = GuiRuntimeSession()
    session.new_game(name="測試保管家", job_id="rogue")
    state = session.require_state()

    # 2. Check Town Hub shows storage node is enabled
    town_model = session.screen_model("town_hub")
    nodes = town_model["facility_nodes"]
    storage_node = next(n for n in nodes if n["facility_id"] == "storage")
    assert storage_node["enabled"] is True
    print("Verified: Storage facility node is enabled in Town Hub.")

    # 3. Verify locked state is correct initially
    model = session.screen_model("storage_screen")
    assert model["storage_state"]["unlocked"] is False
    assert model["storage_state"]["unlock_cost"] == 500

    # Gold is 120G by default, so player cannot unlock
    assert state["gold"] == 120
    assert model["storage_state"]["can_unlock"] is False
    assert "金幣不足" in model["storage_state"]["disabled_reason"]
    print("Verified: Initial locked state details are correct.")

    # 4. Attempt to unlock with insufficient Gold -> should fail with 409
    try:
        session.dispatch("unlock_storage", {}, screen_id="storage_screen")
        raise AssertionError("Expected unlock_storage to fail with low Gold, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert "身上金幣不足" in err.blocked_reason
        print("Verified: Blocked path (insufficient gold) correctly rejected.")

    # 5. Set Gold to 600G (sufficient to unlock)
    state["gold"] = 600

    # Check screen model updates can_unlock status
    model2 = session.screen_model("storage_screen")
    assert model2["storage_state"]["can_unlock"] is True
    assert model2["storage_state"]["disabled_reason"] == ""
    print("Verified: can_unlock status updates when Gold is sufficient.")

    # Give player some items to verify item listing
    state["inventory"]["mat_iron_ore"] = 5
    state["inventory"]["item_potion_s"] = 3
    state["inventory"]["key_fire_mark_shard"] = 1

    # 6. Dispatch unlock_storage -> should succeed!
    response = session.dispatch("unlock_storage", {}, screen_id="storage_screen")
    assert response["ok"] is True
    assert state["storage_unlocked"] is True
    assert state["gold"] == 100  # 600 - 500 = 100G
    print("Verified: unlock_storage succeeded, gold deducted, status updated.")

    # 7. Check unlocked screen model properties
    unlocked_model = response["screen_model"]
    assert unlocked_model["storage_state"]["unlocked"] is True
    assert unlocked_model["storage_state"]["unlock_cost"] == 0
    assert unlocked_model["storage_state"]["can_unlock"] is False

    # Check capacity string shows 0 / 10
    capacity_item = next(r for r in unlocked_model["resource_strip"] if r["id"] == "storage_capacity")
    assert "0 / 10" in capacity_item["label"]

    # Verify inventory_rows lists the items and has them enabled
    inv_rows = unlocked_model["inventory_rows"]
    iron_row = next(r for r in inv_rows if r["item_id"] == "mat_iron_ore")
    assert iron_row["owned_count"] == 5
    assert iron_row["enabled"] is True
    assert iron_row["disabled_reason"] is None

    key_row = next(r for r in inv_rows if r["item_id"] == "key_fire_mark_shard")
    assert key_row["enabled"] is False
    assert "貴重物" in key_row["disabled_reason"]

    # 8. Test deposit_item action (mat_iron_ore x1)
    dep_res = session.dispatch("deposit_item", {"item_id": "mat_iron_ore", "quantity": 1}, screen_id="storage_screen")
    assert dep_res["ok"] is True
    assert state["inventory"]["mat_iron_ore"] == 4
    assert state["storage"]["mat_iron_ore"] == 1
    print("Verified: deposit_item successfully transfers item from inventory to storage.")

    # 9. Test withdraw_item action (mat_iron_ore x1)
    with_res = session.dispatch("withdraw_item", {"item_id": "mat_iron_ore", "quantity": 1}, screen_id="storage_screen")
    assert with_res["ok"] is True
    assert state["inventory"]["mat_iron_ore"] == 5
    assert "mat_iron_ore" not in state["storage"]
    print("Verified: withdraw_item successfully transfers item from storage back to inventory.")

    # 10. Check capacity limit blocking
    # Fill storage with 10 dummy items to trigger capacity limit
    state["storage"] = {f"mat_dummy_{i}": 1 for i in range(10)}
    model_full = session.screen_model("storage_screen")
    inv_rows_full = model_full["inventory_rows"]
    iron_row_full = next(r for r in inv_rows_full if r["item_id"] == "mat_iron_ore")

    # Iron ore is not in storage, and capacity is 10/10, so it should be blocked
    assert iron_row_full["enabled"] is False
    assert "倉庫容量已滿" in iron_row_full["disabled_reason"]

    # Try deposit when full -> should fail
    try:
        session.dispatch("deposit_item", {"item_id": "mat_iron_ore", "quantity": 1}, screen_id="storage_screen")
        raise AssertionError("Expected deposit to fail when storage is full, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert "倉庫容量已達上限" in err.blocked_reason
        print("Verified: Capacity limits are correctly enforced and block deposit actions.")

    # 測試異常數量阻擋
    # 10.1 存入數量為 0 -> 400
    try:
        session.dispatch("deposit_item", {"item_id": "mat_iron_ore", "quantity": 0}, screen_id="storage_screen")
        raise AssertionError("Expected deposit quantity 0 to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 400
        assert "轉移數量" in str(err)

    # 10.2 存入數量為負數 -> 400
    try:
        session.dispatch("deposit_item", {"item_id": "mat_iron_ore", "quantity": -5}, screen_id="storage_screen")
        raise AssertionError("Expected deposit negative quantity to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 400
        assert "轉移數量" in str(err)

    # 10.3 存入數量為非整數 (float) -> 400
    try:
        session.dispatch("deposit_item", {"item_id": "mat_iron_ore", "quantity": 1.5}, screen_id="storage_screen")
        raise AssertionError("Expected deposit float quantity to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 400
        assert "轉移數量" in str(err)

    # 10.4 存入數量為布林值 (bool) -> 400
    try:
        session.dispatch("deposit_item", {"item_id": "mat_iron_ore", "quantity": True}, screen_id="storage_screen")
        raise AssertionError("Expected deposit bool quantity to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 400
        assert "轉移數量" in str(err)

    # 10.5 取出數量為 0 -> 400
    # 先在倉庫放入一個以進行取出測試
    state["storage"]["mat_iron_ore"] = 5
    try:
        session.dispatch("withdraw_item", {"item_id": "mat_iron_ore", "quantity": 0}, screen_id="storage_screen")
        raise AssertionError("Expected withdraw quantity 0 to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 400
        assert "轉移數量" in str(err)

    # 10.6 取出數量為負數 -> 400
    try:
        session.dispatch("withdraw_item", {"item_id": "mat_iron_ore", "quantity": -3}, screen_id="storage_screen")
        raise AssertionError("Expected withdraw negative quantity to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 400
        assert "轉移數量" in str(err)

    # 10.7 取出數量為非整數 -> 400
    try:
        session.dispatch("withdraw_item", {"item_id": "mat_iron_ore", "quantity": 2.5}, screen_id="storage_screen")
        raise AssertionError("Expected withdraw float quantity to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 400
        assert "轉移數量" in str(err)

    print("Verified: Quantity type and value validations correctly enforced for deposit/withdraw.")

    # Clean up dummy storage to leave it clean
    state["storage"] = {}

    print("Storage Live MVP bridge smoke test passed successfully with deposit/withdraw coverage!")


if __name__ == "__main__":
    run_smoke_test()
