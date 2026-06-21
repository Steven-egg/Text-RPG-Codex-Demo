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
    assert len(model_relic["slots"]) == 4
    assert {slot["element_id"] for slot in model_relic["slots"]} == {"fire", "ice", "earth", "thunder"}
    # Check that fire preview is locked initially because the Temple lookup is not done.
    fire_slot = next(s for s in model_relic["slots"] if s["element_id"] == "fire")
    assert fire_slot["unlocked"] is False
    assert fire_slot["ready"] is False
    assert fire_slot["enshrined"] is False
    assert fire_slot["active"] is False
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
    state["inventory"]["key_fire_mark_shard"] = 3
    res_inq = session.dispatch("fire_mark_guild_inquiry", {}, screen_id="guild_screen")
    assert res_inq["ok"] is True
    assert state["flags"].get("fire_mark_guild_inquiry_done") is True

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

    # Now that lookup is done, the Fire marker core should be display-unlocked only.
    model_relic = session.screen_model("relic_preview_screen")
    fire_slot = next(s for s in model_relic["slots"] if s["element_id"] == "fire")
    assert fire_slot["unlocked"] is True
    assert fire_slot["ready"] is True
    assert fire_slot["enshrined"] is False
    assert fire_slot["active"] is False
    assert fire_slot["collected"] == 3
    print("Relic ready preview verified (fire seal can be enshrined).")

    # 5. Test Fire seal enshrinement through the compatibility action.
    res_attune = session.dispatch("attune_relic", {"relic_id": "relic_fire_seal"}, screen_id="relic_preview_screen")
    assert res_attune["ok"] is True
    assert "火之聖印" in res_attune["message"]
    assert state["inventory"].get("key_fire_mark_shard", 0) == 0
    assert state["inventory"].get("key_fire_seal", 0) == 1
    assert state["flags"].get("fire_seal_enshrined") is True
    assert game.is_unlocked(state, "unlock_ice_region")
    fire_slot = next(s for s in res_attune["screen_model"]["slots"] if s["element_id"] == "fire")
    assert fire_slot["ready"] is False
    assert fire_slot["enshrined"] is True
    assert fire_slot["active"] is False
    print("Fire seal enshrinement verified.")

    res_repeat = session.dispatch("attune_relic", {"relic_id": "火之聖印"}, screen_id="relic_preview_screen")
    assert res_repeat["ok"] is True
    assert "已安置" in res_repeat["message"]
    print("Repeated enshrinement returns completed hint.")

    # 6. Test regional marker sources convert into true seals without active effects.
    assert not game.is_unlocked(state, "unlock_final_region_preview")
    state["flags"]["ice_relic_marker_resolved"] = True
    state["inventory"]["key_ice_relic_marker_source"] = 1
    state["flags"]["earth_relic_marker_resolved"] = True
    state["inventory"]["key_earth_relic_marker_source"] = 1
    state["flags"]["thunder_relic_marker_resolved"] = True
    state["inventory"]["key_thunder_relic_marker_source"] = 1

    res_ice = session.dispatch("attune_relic", {"relic_id": "relic_ice_marker_source"}, screen_id="relic_preview_screen")
    assert res_ice["ok"] is True
    assert state["inventory"].get("key_ice_relic_marker_source", 0) == 0
    assert state["inventory"].get("key_ice_seal", 0) == 1
    assert state["flags"].get("ice_seal_enshrined") is True
    assert not game.is_unlocked(state, "unlock_final_region_preview")

    res_earth = session.dispatch("attune_relic", {"relic_id": "relic_earth_marker_source"}, screen_id="relic_preview_screen")
    assert res_earth["ok"] is True
    assert state["inventory"].get("key_earth_relic_marker_source", 0) == 0
    assert state["inventory"].get("key_earth_seal", 0) == 1
    assert state["flags"].get("earth_seal_enshrined") is True
    assert not game.is_unlocked(state, "unlock_final_region_preview")

    res_thunder = session.dispatch("attune_relic", {"relic_id": "relic_thunder_marker_source"}, screen_id="relic_preview_screen")
    assert res_thunder["ok"] is True
    assert state["inventory"].get("key_thunder_relic_marker_source", 0) == 0
    assert state["inventory"].get("key_thunder_seal", 0) == 1
    assert state["flags"].get("thunder_seal_enshrined") is True
    assert game.is_unlocked(state, "unlock_final_region_preview")
    thunder_slot = next(s for s in res_thunder["screen_model"]["slots"] if s["element_id"] == "thunder")
    assert thunder_slot["enshrined"] is True
    assert thunder_slot["active"] is False
    print("Regional seal enshrinement and Final gate verified.")

    print("Temple and Relic Preview bridge smoke test ok!")


if __name__ == "__main__":
    run_smoke_test()
