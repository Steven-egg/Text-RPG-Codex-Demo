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
    print("Starting Guild Quest Bridge smoke test...")

    # 1. Setup a new game session
    session = GuiRuntimeSession()
    session.new_game(name="測試冒險者", job_id="warrior")
    state = session.require_state()

    # The player starts with quest_register completed, quest_cave_gathering unlocked but incomplete
    assert "quest_register" in state["completed_quests"]
    assert "quest_cave_gathering" not in state["completed_quests"]

    # Verify Town Hub shows Synthesis Shop is LOCKED (disabled)
    town_model_1 = session.screen_model("town_hub")
    nodes_1 = town_model_1["facility_nodes"]
    synth_node_1 = next(n for n in nodes_1 if n["facility_id"] == "synthesis")
    assert synth_node_1["enabled"] is False
    assert "先完成工會任務" in synth_node_1["disabled_reason"]
    print("Locked Synthesis Shop node in Town Hub verified.")

    # Verify Guild Screen shows quest_cave_gathering in progress
    guild_model_1 = session.screen_model("guild_screen")
    quest_row_1 = next(r for r in guild_model_1["task_rows"] if r["task_id"] == "quest_cave_gathering")
    assert quest_row_1["status"] == "requirements_missing"
    assert quest_row_1["status_label"] == "條件不足"
    print("Quest 'quest_cave_gathering' in progress status verified.")

    # Try to submit quest without materials - should fail with 409
    try:
        session.dispatch("submit_quest", {"task_id": "quest_cave_gathering"}, screen_id="guild_screen")
        raise AssertionError("Expected submit_quest with missing materials to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert "交付條件尚未滿足" in str(err)
        print("Missing materials submission rejection verified.")

    # Give player the required materials: mat_moss_fiber x3, mat_cracked_stone x2
    state["inventory"]["mat_moss_fiber"] = 3
    state["inventory"]["mat_cracked_stone"] = 2
    state["gold"] = 100

    # Verify Guild Screen now shows quest_cave_gathering as "ready_to_submit"
    guild_model_2 = session.screen_model("guild_screen")
    quest_row_2 = next(r for r in guild_model_2["task_rows"] if r["task_id"] == "quest_cave_gathering")
    assert quest_row_2["status"] == "ready_to_submit"
    assert quest_row_2["status_label"] == "可回報"
    print("Quest 'quest_cave_gathering' ready-to-submit status verified.")

    # Submit quest with materials - should succeed!
    response = session.dispatch("submit_quest", {"task_id": "quest_cave_gathering"}, screen_id="guild_screen")
    assert response["ok"] is True
    assert "米菈合成屋已開放" in response["message"]

    # Verify materials are deducted, rewards are given
    assert state["inventory"].get("mat_moss_fiber", 0) == 0
    assert state["inventory"].get("mat_cracked_stone", 0) == 0
    assert state["gold"] == 220  # 100 + 120 (quest reward) = 220
    assert state["guild_points"] > 0
    assert "quest_cave_gathering" in state["completed_quests"]
    assert game.is_unlocked(state, "shop_synthesis_01")
    print("Quest successfully completed: items deducted, rewards given, and shop unlocked.")

    # Verify Town Hub now shows Synthesis Shop is UNLOCKED (enabled)
    town_model_2 = session.screen_model("town_hub")
    nodes_2 = town_model_2["facility_nodes"]
    synth_node_2 = next(n for n in nodes_2 if n["facility_id"] == "synthesis")
    assert synth_node_2["enabled"] is True
    print("Unlocked Synthesis Shop node in Town Hub verified.")

    # Verify we can view Synthesis screen
    synth_model = session.screen_model("synthesis_screen")
    assert synth_model["screen_id"] == "facility_synthesis_screen"
    print("Synthesis screen access verified.")

    print("Guild Quest Bridge smoke test passed successfully!")


if __name__ == "__main__":
    run_smoke_test()
