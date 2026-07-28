from __future__ import annotations

import sys
from pathlib import Path

# Resolve project paths
ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from engine.gui_actions import start_screen_model, GuiRuntimeSession, GuiActionError
from engine import game


def run_smoke_test():
    print("Starting core navigation and Inn bridge smoke test...")

    # 1. Verify start_screen_model(False) and start_screen_model(True) entry action shapes
    print("Step 1: Verifying start_screen_model entry action shapes...")

    # 1a. has_save is False
    model_no_save = start_screen_model(False)
    assert model_no_save["screen_id"] == "start_screen"
    assert model_no_save["layout_family"] == "entry"
    assert model_no_save["presentation"]["has_save"] is False
    assert "actions" in model_no_save
    assert len(model_no_save["actions"]) == 1
    assert model_no_save["actions"][0]["action_id"] == "start_new_game"
    print(" - start_screen_model(False) verified successfully.")

    # 1b. has_save is True
    model_has_save = start_screen_model(True)
    assert model_has_save["screen_id"] == "start_screen"
    assert model_has_save["layout_family"] == "entry"
    assert model_has_save["presentation"]["has_save"] is True
    assert "actions" in model_has_save
    assert len(model_has_save["actions"]) == 2
    action_ids = [act["action_id"] for act in model_has_save["actions"]]
    assert "load_game" in action_ids
    assert "restart_game" in action_ids
    print(" - start_screen_model(True) verified successfully.")

    # 2. Verify start_new_game creates in-memory state and returns Town Hub ScreenModel/route
    print("Step 2: Verifying start_new_game creation...")
    session = GuiRuntimeSession()
    assert not session.state_loaded

    res_new = session.dispatch("start_new_game", {"name": "測試冒險家", "job_id": "warrior"})
    assert res_new["ok"] is True
    assert res_new["action_id"] == "start_new_game"
    assert session.state_loaded
    assert session.state["name"] == "測試冒險家"
    assert session.state["job"] == "劍士"
    assert res_new["next_screen_id"] == "town_hub"
    assert "town_hub" in res_new["next_route"]
    assert res_new["screen_model"]["screen_id"] == "town_hub"
    print(" - start_new_game verified successfully.")

    # 3. Verify Town Hub ScreenModel can be generated and dispatches open_world_map
    print("Step 3: Verifying Town Hub and open_world_map...")
    town_model = session.screen_model("town_hub")
    assert town_model["screen_id"] == "town_hub"

    # Check that open_world_map action is available
    nav_actions = town_model.get("navigation_actions", [])
    assert any(act["action_id"] == "open_world_map" for act in nav_actions)

    res_map = session.dispatch("open_world_map", {}, screen_id="town_hub")
    assert res_map["ok"] is True
    assert res_map["action_id"] == "open_world_map"
    assert res_map["next_screen_id"] == "world_map"
    assert "world_map" in res_map["next_route"]
    assert res_map["screen_model"]["screen_id"] == "world_map"
    print(" - open_world_map verified successfully.")

    # 4. Verify World Map ScreenModel can be generated and dispatches back_to_town_hub
    print("Step 4: Verifying World Map and back_to_town_hub...")
    world_model = session.screen_model("world_map")
    assert world_model["screen_id"] == "world_map"

    # Find back_to_town_hub action in locations (border_town has it as primary_action)
    border_town_loc = next(loc for loc in world_model["locations"] if loc["location_id"] == "border_town")
    assert border_town_loc["primary_action"]["action_id"] == "back_to_town_hub"

    res_town = session.dispatch("back_to_town_hub", {}, screen_id="world_map")
    assert res_town["ok"] is True
    assert res_town["action_id"] == "back_to_town_hub"
    assert res_town["next_screen_id"] == "town_hub"
    assert "town_hub" in res_town["next_route"]
    assert res_town["screen_model"]["screen_id"] == "town_hub"
    print(" - back_to_town_hub verified successfully.")

    # 5. Verify Inn rest_at_inn happy path
    print("Step 5: Verifying Inn rest_at_inn happy path...")
    state = session.require_state()
    stats = game.get_stats(state)
    max_hp = stats["max_hp"]
    max_mp = stats["max_mp"]

    # Set partial HP/MP and sufficient gold (e.g. 100G)
    state["current_hp"] = max_hp - 10
    state["current_mp"] = max_mp - 5
    state["gold"] = 100

    # Dispatch rest_at_inn with screen_id="inn_screen" to verify it returns Inn ScreenModel
    res_rest = session.dispatch("rest_at_inn", {"service_id": "overnight_rest", "cost": 30}, screen_id="inn_screen")
    assert res_rest["ok"] is True
    assert res_rest["action_id"] == "rest_at_inn"

    # Verify deduction and restoration
    assert state["gold"] == 70  # 100 - 30
    assert state["current_hp"] == max_hp
    assert state["current_mp"] == max_mp
    assert res_rest["screen_model"]["screen_id"] == "inn_screen"
    print(" - rest_at_inn happy path verified successfully.")

    # 6. Verify Inn insufficient-Gold blocked path
    print("Step 6: Verifying Inn rest_at_inn insufficient-Gold blocked path...")
    # Set partial HP/MP and insufficient gold (e.g. 10G)
    state["current_hp"] = max_hp - 15
    state["current_mp"] = max_mp - 8
    state["gold"] = 10

    try:
        session.dispatch("rest_at_inn", {"service_id": "overnight_rest", "cost": 30}, screen_id="inn_screen")
        raise AssertionError("Expected rest_at_inn to fail with insufficient Gold, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert "身上金幣不足" in err.blocked_reason

        # Verify values remain unchanged
        assert state["gold"] == 10
        assert state["current_hp"] == max_hp - 15
        assert state["current_mp"] == max_mp - 8
        print(" - rest_at_inn blocked path verified successfully.")

    print("All core navigation and Inn bridge smoke tests passed successfully!")


if __name__ == "__main__":
    run_smoke_test()
