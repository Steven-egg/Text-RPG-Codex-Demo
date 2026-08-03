"""Focused regression for lightweight main-story beat contracts."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from data.dialogues import STORY_BEATS  # noqa: E402
from engine import dungeon, game  # noqa: E402
from engine.gui_actions import GuiRuntimeSession, action_response  # noqa: E402
from engine.story_beats import (  # noqa: E402
    STORY_BEAT_KEYS,
    STORY_BEAT_KINDS,
    STORY_BEAT_TONES,
    build_story_beat,
    story_seen_flag,
    take_story_beat,
)


MAIN_STORY_BOSSES = {
    "boss_cinder_seal_sentinel",
    "boss_ice_final_seal_lord",
    "boss_earth_deep_leyline_lord",
    "boss_thunder_crown_storm_lord",
    "boss_final_demon_king",
}
EXPECTED_IDS = {
    "prologue.new_game",
    "region.enter.ice",
    "region.enter.earth",
    "region.enter.thunder",
    "region.enter.final",
    "ending.main_story_clear",
    "boss.before.boss_glen",
    "guidance.promotion_preview",
    "guidance.relic_preview",
    *(f"boss.{timing}.{boss_id}" for boss_id in MAIN_STORY_BOSSES for timing in ("before", "after")),
}


def assert_story_beat(beat: dict, expected_id: str) -> None:
    assert set(beat) == STORY_BEAT_KEYS
    assert beat["id"] == expected_id
    assert beat["kind"] in STORY_BEAT_KINDS
    assert beat["tone"] in STORY_BEAT_TONES
    assert isinstance(beat["title"], str) and beat["title"]
    assert isinstance(beat["dismiss_label"], str) and beat["dismiss_label"]
    assert isinstance(beat["lines"], list) and 2 <= len(beat["lines"]) <= 5
    for line in beat["lines"]:
        assert isinstance(line, str) and line
        assert "\n" not in line
        assert re.search(r"<[^>]*>", line) is None


def verify_data_contract() -> None:
    assert set(STORY_BEATS) == EXPECTED_IDS
    for beat_id in EXPECTED_IDS:
        beat = build_story_beat(beat_id, {"player": "契約測試者", "job": "劍士"})
        assert beat is not None
        assert_story_beat(beat, beat_id)
    assert build_story_beat("missing.story.beat") is None
    relic_guidance = build_story_beat("guidance.relic_preview")
    assert relic_guidance is not None
    assert any("既有被動加成" in line for line in relic_guidance["lines"])
    assert not any("尚未實裝" in line for line in relic_guidance["lines"])
    print(f"[Pass] All {len(EXPECTED_IDS)} story nodes satisfy the exact presentation contract.")


def verify_seen_flags_and_legacy_state() -> None:
    legacy_state = {"flags": None}
    first = take_story_beat(legacy_state, "region.enter.ice")
    assert first is not None
    assert legacy_state == {"flags": {story_seen_flag("region.enter.ice"): True}}
    assert take_story_beat(legacy_state, "region.enter.ice") is None
    assert take_story_beat(legacy_state, "missing.story.beat") is None
    assert set(legacy_state) == {"flags"}
    print("[Pass] Repeat suppression uses only explicit story_seen flags.")


def verify_cli_hooks() -> None:
    with (
        patch("engine.game.title"),
        patch("engine.game.input", return_value="CLI 測試者"),
        patch("engine.game.menu", return_value=1),
        patch("engine.story_beats.render_panel") as story_panel,
    ):
        state = game.new_game()
    assert state["flags"][story_seen_flag("prologue.new_game")] is True
    assert story_panel.call_args.args[0] == STORY_BEATS["prologue.new_game"]["title"]

    game.unlock(state, game.ICE_REGION_UNLOCK)
    with (
        patch("engine.game.action_menu_panel", return_value=2),
        patch("engine.game.pause"),
        patch("engine.story_beats.render_panel") as story_panel,
    ):
        region_id = game.region_travel_menu(state, "border_fire")
    assert region_id == "ice"
    assert story_panel.call_args.args[0] == STORY_BEATS["region.enter.ice"]["title"]

    ending_state = game.create_state("結局測試者", next(iter(game.JOBS)))
    with (
        patch("engine.dungeon.pause"),
        patch("engine.dungeon.render_panel"),
        patch("engine.story_beats.render_panel") as story_panel,
    ):
        dungeon.show_main_story_ending(ending_state)
    assert story_panel.call_args.args[0] == STORY_BEATS["ending.main_story_clear"]["title"]
    print("[Pass] CLI hooks render the shared prologue, region, and ending data.")


def exploration_state(dungeon_id: str) -> dict:
    dungeon_data = game.DUNGEONS[dungeon_id]
    return {
        "dungeon_id": dungeon_id,
        "current_step": dungeon_data["steps"],
        "run_log": {"gold": 0, "items": {}},
        "events": [],
        "last_message": "",
        "status": "resolved",
    }


def verify_bridge_prologue_and_region() -> None:
    session = GuiRuntimeSession()
    response = session.new_game("Bridge 測試者", "warrior")
    assert_story_beat(response["story_beat"], "prologue.new_game")
    assert response["action_id"] == "start_new_game"
    assert response["next_route"] == "../town_hub/index.html?mode=live"
    assert response["screen_model"]["screen_id"] == "town_hub"

    empty_response = action_response("contract_probe", "ok", session.require_state(), screen_id=None)
    assert empty_response["story_beat"] is None

    state = session.require_state()
    game.unlock(state, game.ICE_REGION_UNLOCK)
    first_ice = session.travel_region({"region_id": "ice"})
    assert_story_beat(first_ice["story_beat"], "region.enter.ice")
    assert first_ice["next_route"] == "../world_map/index.html?mode=live"
    assert first_ice["screen_model"]["current_region_id"] == "ice"
    session.travel_region({"region_id": "border_fire"})
    repeat_ice = session.travel_region({"region_id": "ice"})
    assert repeat_ice["story_beat"] is None
    print("[Pass] Bridge responses attach prologue/first-region beats without changing routing.")


def verify_bridge_boss_before_after() -> None:
    session = GuiRuntimeSession()
    session.new_game("Boss Bridge 測試者", "warrior")
    state = session.require_state()
    state["completed_quests"].append("quest_cinder_depths_scout")
    session.exploration = exploration_state("dungeon_cinder_seal_depths")

    before = session.challenge_boss({})
    assert_story_beat(before["story_beat"], "boss.before.boss_cinder_seal_sentinel")
    assert before["action_id"] == "challenge_boss"
    assert before["next_route"] == "../combat_screen/index.html?mode=live"

    after = session.resolve_victory(["focused victory"])
    assert_story_beat(after["story_beat"], "boss.after.boss_cinder_seal_sentinel")
    assert after["action_id"] == "basic_attack"
    assert after["screen_model"]["screen_id"] == "combat_screen"
    assert game.clear_dungeon_boss(state, "boss_cinder_seal_sentinel", {"gold": 0, "items": {}}) is None
    print("[Pass] Boss challenge/victory responses carry shared before/after beats once.")


def verify_bridge_final_boss_sequence() -> None:
    session = GuiRuntimeSession()
    session.new_game("終門測試者", "warrior")
    session.exploration = exploration_state("dungeon_final_main_phase_3")
    session.start_combat("boss_final_demon_king", boss=True)

    victory = session.resolve_victory(["final focused victory"])
    assert_story_beat(victory["story_beat"], "boss.after.boss_final_demon_king")
    ending = session.dispatch("return_to_exploration", {}, screen_id="combat_screen")
    assert_story_beat(ending["story_beat"], "ending.main_story_clear")
    assert ending["next_route"] == "../dungeon_exploration/index.html?mode=live"
    assert "_ending_pending" not in session.require_state()
    print("[Pass] Final victory emits boss-after then ending as two compatible responses.")


def main() -> None:
    verify_data_contract()
    verify_seen_flags_and_legacy_state()
    verify_cli_hooks()
    verify_bridge_prologue_and_region()
    verify_bridge_boss_before_after()
    verify_bridge_final_boss_sequence()
    print("story beats regression ok")


if __name__ == "__main__":
    main()
