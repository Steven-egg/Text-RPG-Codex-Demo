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
    print("Starting Temple and Relic Preview Live MVP bridge smoke test...")

    # 1. Initialize session
    session = GuiRuntimeSession()
    session.new_game(name="冒險先驅", job_id="warrior")
    state = session.require_state()

    print(f"Initial State: job={state['job']}, level={state['level']}, gold={state['gold']}")

    # 2. Test temple_screen_model and relic_preview_screen_model loading
    model_temple = session.screen_model("temple_screen")
    assert model_temple["screen_id"] == "temple_screen"
    assert "promotions" in model_temple
    assert "inquiries" in model_temple
    # Since we don't have Glen defeated yet, inquiries should be empty
    assert len(model_temple["inquiries"]) == 0
    print("Initial temple_screen_model loaded successfully.")

    model_relic = session.screen_model("relic_preview_screen")
    assert model_relic["screen_id"] == "relic_preview_screen"
    assert len(model_relic["slots"]) == 3
    # Check that fire relic (ash charm) is locked initially (because unlock_ash_ravine is not unlocked)
    fire_slot = next(s for s in model_relic["slots"] if s["element_id"] == "fire")
    assert fire_slot["unlocked"] is False
    print("Initial relic_preview_screen_model loaded successfully.")

    # 3. Test temple_pray action
    initial_gold = state["gold"]
    state["gold"] = 100
    res_pray = session.dispatch("temple_pray", {}, screen_id="temple_screen")
    assert res_pray["ok"] is True
    assert state["gold"] == 70  # Deducted 30G
    assert "月華庇護" in res_pray["message"]
    print("temple_pray action verified.")

    # 4. Test fire_mark_church_bridge and lookup progression
    # Set the prerequisites:
    # state["flags"]["fire_mark_guild_inquiry_done"] = True (from fire_mark_guild_inquiry)
    # state["inventory"]["key_fire_mark_shard"] = 3
    state["flags"]["fire_mark_guild_inquiry_done"] = True
    state["inventory"]["key_fire_mark_shard"] = 3

    # Check that temple model now has the bridge inquiry
    model_temple = session.screen_model("temple_screen")
    assert len(model_temple["inquiries"]) == 1
    assert model_temple["inquiries"][0]["action_id"] == "fire_mark_church_bridge"
    print("should_show_fire_mark_church_bridge conditions met & inquiry listed.")

    # Dispatch fire_mark_church_bridge
    res_bridge = session.dispatch("fire_mark_church_bridge", {}, screen_id="temple_screen")
    assert res_bridge["ok"] is True
    assert state["flags"].get("fire_mark_church_bridge_done") is True
    print("fire_mark_church_bridge action executed and flag set.")

    # Check that temple model now has the lookup inquiry
    model_temple = session.screen_model("temple_screen")
    assert len(model_temple["inquiries"]) == 1
    assert model_temple["inquiries"][0]["action_id"] == "fire_mark_church_lookup"
    print("should_show_fire_mark_church_lookup conditions met & inquiry listed.")

    # Dispatch fire_mark_church_lookup
    res_lookup = session.dispatch("fire_mark_church_lookup", {}, screen_id="temple_screen")
    assert res_lookup["ok"] is True
    assert state["flags"].get("fire_mark_church_lookup_done") is True
    print("fire_mark_church_lookup action executed and flag set.")

    # Now that lookup is done, let's unlock ash ravine to test relic unlock preview
    game.unlock(state, "unlock_ash_ravine")
    model_relic = session.screen_model("relic_preview_screen")
    fire_slot = next(s for s in model_relic["slots"] if s["element_id"] == "fire")
    assert fire_slot["unlocked"] is True
    assert fire_slot["active"] is True
    print("Relic unlock preview verified (relic_ash_charm becomes unlocked).")

    # 5. Test attune_relic action
    res_attune = session.dispatch("attune_relic", {"relic_id": "灰燼護符"}, screen_id="relic_preview_screen")
    assert res_attune["ok"] is True
    assert "尚未開放" in res_attune["message"]
    print("attune_relic action verified.")

    print("Temple and Relic Preview bridge smoke test ok!")


if __name__ == "__main__":
    run_smoke_test()
