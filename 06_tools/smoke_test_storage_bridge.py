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

    # Verify inventory_rows lists the items and has them disabled
    inv_rows = unlocked_model["inventory_rows"]
    iron_row = next(r for r in inv_rows if r["item_id"] == "mat_iron_ore")
    assert iron_row["owned_count"] == 5
    assert iron_row["enabled"] is False  # MVP deposit is disabled
    assert "僅提供倉庫開啟" in iron_row["disabled_reason"]

    key_row = next(r for r in inv_rows if r["item_id"] == "key_fire_mark_shard")
    assert key_row["enabled"] is False
    assert "貴重物" in key_row["disabled_reason"]

    # Fill storage manually and verify display
    state["storage"]["mat_copper_powder"] = 12
    unlocked_model2 = session.screen_model("storage_screen")
    storage_rows = unlocked_model2["storage_rows"]
    copper_row = next(r for r in storage_rows if r["item_id"] == "mat_copper_powder")
    assert copper_row["owned_count"] == 12
    assert copper_row["enabled"] is False  # MVP withdraw is disabled
    assert "僅提供倉庫開啟" in copper_row["disabled_reason"]

    capacity_item2 = next(r for r in unlocked_model2["resource_strip"] if r["id"] == "storage_capacity")
    assert "1 / 10" in capacity_item2["label"]

    print("Storage Unlock & View Live MVP bridge smoke test passed successfully!")


if __name__ == "__main__":
    run_smoke_test()
