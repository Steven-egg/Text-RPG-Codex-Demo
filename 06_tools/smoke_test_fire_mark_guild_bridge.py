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
    print("Starting Fire Mark Guild Inquiry bridge smoke test...")

    # 1. Blocked Path: Less than 3 shards
    session1 = GuiRuntimeSession()
    session1.new_game(name="測試冒險者", job_id="warrior")
    state1 = session1.require_state()
    state1["inventory"]["key_fire_mark_shard"] = 2

    try:
        session1.dispatch("fire_mark_guild_inquiry", {}, screen_id="guild_screen")
        raise AssertionError("Expected fire_mark_guild_inquiry with less than 3 shards to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "不符合詢問條件或已詢問過"
        assert not state1.get("flags", {}).get("fire_mark_guild_inquiry_done")
        print("Blocked Path (Less than 3 shards) verified.")

    # 2. Verify Guild model shows inquiry card when 3 shards are present
    session2 = GuiRuntimeSession()
    session2.new_game(name="測試冒險者", job_id="warrior")
    state2 = session2.require_state()
    
    # Complete prerequisites for Cinder depths scout and boss flags so we are in the "else" branch of guild story_hint_card
    state2.setdefault("completed_quests", []).extend([
        "quest_boss_glen",
        "quest_ash_ravine_scout",
        "quest_supply_upgrade",
        "quest_cinder_depths_scout"
    ])
    state2.setdefault("flags", {})
    state2["flags"]["ash_guardian_defeated"] = True
    state2["flags"]["cinder_seal_sentinel_defeated"] = True
    state2["inventory"]["key_fire_mark_shard"] = 3

    model = session2.screen_model("guild_screen")
    card = model["story_hint_card"]
    assert card["id"] == "story_hint_fire_mark_guild_inquiry"
    assert card["visible"] is True
    assert card["enabled"] is True
    assert card["primary_action"] == "fire_mark_guild_inquiry"
    # Verify shard requirement is shown
    assert any("三" in r["label"] or "火之印記碎片" in r["label"] for r in card["condition_rows"])
    print("Guild model shows active fire_mark_guild_inquiry card.")

    # 3. Happy Path: Dispatch inquiry action
    res = session2.dispatch("fire_mark_guild_inquiry", {}, screen_id="guild_screen")
    assert res["ok"] is True
    assert state2["flags"].get("fire_mark_guild_inquiry_done") is True
    print("Inquiry action dispatch verified.")

    # 4. Verify shards are NOT consumed
    assert state2["inventory"].get("key_fire_mark_shard", 0) == 3
    print("Shards are not consumed verified.")

    # 5. Blocked Path: Repeat dispatch is blocked
    try:
        session2.dispatch("fire_mark_guild_inquiry", {}, screen_id="guild_screen")
        raise AssertionError("Expected repeat dispatch to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "不符合詢問條件或已詢問過"
        print("Blocked Path (Repeat dispatch blocked) verified.")

    # 6. Verify Guild model directs player to Temple after completion
    model = session2.screen_model("guild_screen")
    card_done = model["story_hint_card"]
    assert card_done["id"] == "story_hint_fire_mark_guild_inquiry_done"
    assert card_done["enabled"] is False
    assert "神殿" in card_done["description"] or "大教堂" in card_done["description"]
    print("Guild model directs to Temple verified.")

    # 7. Verify Temple model naturally displays fire_mark_church_bridge
    # Temple needs 3 shards + fire_mark_guild_inquiry_done
    model_temple = session2.screen_model("temple_screen")
    assert len(model_temple["inquiries"]) == 1
    assert model_temple["inquiries"][0]["action_id"] == "fire_mark_church_bridge"
    print("Temple model displays fire_mark_church_bridge naturally verified.")

    print("\nFire Mark Guild Inquiry bridge smoke test completed successfully!")


if __name__ == "__main__":
    run_smoke_test()
