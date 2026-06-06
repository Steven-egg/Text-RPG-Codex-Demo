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


def run_smoke_test():
    print("Starting Guild Material Sell Bridge smoke test...")

    # 1. Setup a new game session
    session = GuiRuntimeSession()
    session.new_game(name="測試冒險者", job_id="warrior")
    state = session.require_state()

    # 2. Add some materials to player inventory and set starting Gold
    state["inventory"]["mat_moss_fiber"] = 10
    state["inventory"]["mat_cracked_stone"] = 5
    state["inventory"]["item_potion_s"] = 1  # consumable, not sellable at guild
    state["inventory"]["key_fire_mark_shard"] = 1  # key item, not sellable
    state["gold"] = 100

    # 3. Load guild screen and verify sellable materials are shaped correctly
    model = session.screen_model("guild_screen")
    assert "sellable_materials" in model
    materials = model["sellable_materials"]
    
    assert len(materials) == 2
    
    moss = next(m for m in materials if m["item_id"] == "mat_moss_fiber")
    assert moss["owned_count"] == 10
    assert moss["unit_price"] == 6
    assert moss["title"] == "青苔纖維"

    stone = next(m for m in materials if m["item_id"] == "mat_cracked_stone")
    assert stone["owned_count"] == 5
    assert stone["unit_price"] == 6
    assert stone["title"] == "破裂石片"

    print("Initial sellable materials list shape verified.")

    # 4. Try to sell invalid item ID
    try:
        session.dispatch("sell_guild_material", {"item_id": "invalid_item", "quantity": 1, "confirm": True}, screen_id="guild_screen")
        raise AssertionError("Expected invalid item to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 400
        assert "非登記收購素材" in str(err)
        print("Invalid item validation verified.")

    # 5. Try to sell item not in buyback prices (e.g., consumable potion)
    try:
        session.dispatch("sell_guild_material", {"item_id": "item_potion_s", "quantity": 1, "confirm": True}, screen_id="guild_screen")
        raise AssertionError("Expected unsellable item to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 400
        assert "非登記收購素材" in str(err)
        print("Unsellable item category validation verified.")

    # 6. Try to sell with invalid quantity format (zero, negative, float, bool)
    invalid_quantities = [0, -1, 1.5, True, False, "two"]
    for q in invalid_quantities:
        try:
            session.dispatch("sell_guild_material", {"item_id": "mat_moss_fiber", "quantity": q, "confirm": True}, screen_id="guild_screen")
            raise AssertionError(f"Expected quantity {q} to fail, but it succeeded.")
        except GuiActionError as err:
            assert err.status == 400
            assert "數量必須為正整數" in str(err)
    print("Invalid quantity formats validation verified.")

    # 7. Try to sell exceeding owned quantity
    try:
        session.dispatch("sell_guild_material", {"item_id": "mat_moss_fiber", "quantity": 11, "confirm": True}, screen_id="guild_screen")
        raise AssertionError("Expected exceeding quantity to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert "持有素材數量不足" in str(err)
        print("Exceeding quantity validation verified.")

    # 8. Try to sell with confirm=False (cancellation)
    try:
        session.dispatch("sell_guild_material", {"item_id": "mat_moss_fiber", "quantity": 5, "confirm": False}, screen_id="guild_screen")
        raise AssertionError("Expected confirm=False to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 400
        assert "出售已取消" in str(err)
        # Verify no gold or items were changed
        assert state["gold"] == 100
        assert state["inventory"]["mat_moss_fiber"] == 10
        print("Cancellation check verified.")

    # 9. Sell 3 mat_moss_fiber successfully
    res = session.dispatch("sell_guild_material", {"item_id": "mat_moss_fiber", "quantity": 3, "confirm": True}, screen_id="guild_screen")
    assert res["ok"] is True
    assert "成功出售 青苔纖維 x3" in res["message"]
    assert state["gold"] == 118  # 100 + 3 * 6 = 118
    assert state["inventory"]["mat_moss_fiber"] == 7
    
    # Check that returned screen model is immediately updated
    updated_materials = res["screen_model"]["sellable_materials"]
    updated_moss = next(m for m in updated_materials if m["item_id"] == "mat_moss_fiber")
    assert updated_moss["owned_count"] == 7
    print("Happy path sell transaction and model update verified.")

    # 10. Sell remaining 7 mat_moss_fiber (should exhaust)
    res2 = session.dispatch("sell_guild_material", {"item_id": "mat_moss_fiber", "quantity": 7, "confirm": True}, screen_id="guild_screen")
    assert res2["ok"] is True
    assert state["gold"] == 160  # 118 + 7 * 6 = 160
    assert "mat_moss_fiber" not in state["inventory"]
    
    # Check that mat_moss_fiber is no longer in sellable materials
    updated_materials2 = res2["screen_model"]["sellable_materials"]
    assert not any(m["item_id"] == "mat_moss_fiber" for m in updated_materials2)
    assert len(updated_materials2) == 1
    print("Material exhaustion and list removal verified.")

    # 11. Sell all 5 mat_cracked_stone to empty the sellable list completely
    res3 = session.dispatch("sell_guild_material", {"item_id": "mat_cracked_stone", "quantity": 5, "confirm": True}, screen_id="guild_screen")
    assert res3["ok"] is True
    assert state["gold"] == 190  # 160 + 5 * 6 = 190
    assert "mat_cracked_stone" not in state["inventory"]
    assert len(res3["screen_model"]["sellable_materials"]) == 0
    print("Complete sellable material list depletion verified.")

    print("Guild Material Sell Bridge smoke test passed successfully!")


if __name__ == "__main__":
    run_smoke_test()
