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


def run_progression_smoke_test():
    print("Starting Guild x Dungeon Progression Bridge smoke test...")

    # 1. Setup a new game session
    session = GuiRuntimeSession()
    session.new_game(name="冒險者卡特", job_id="warrior")
    state = session.require_state()

    # Verify initial state
    assert "quest_register" in state["completed_quests"]
    assert "quest_cave_gathering" not in state["completed_quests"]

    # 2. Complete Cave Gathering Quest to unlock Scorched Mine
    state["inventory"]["mat_moss_fiber"] = 3
    state["inventory"]["mat_cracked_stone"] = 2
    session.dispatch("submit_quest", {"task_id": "quest_cave_gathering"}, screen_id="guild_screen")
    assert "quest_cave_gathering" in state["completed_quests"]
    assert game.is_unlocked(state, "dungeon_scorched_mine")
    print("[Pass] Cave Gathering completed and Scorched Mine unlocked.")

    # 3. Complete Scorched Mine Scout Quest
    state["inventory"]["mat_fire_stone"] = 2
    session.dispatch("submit_quest", {"task_id": "quest_mine_scout"}, screen_id="guild_screen")
    assert "quest_mine_scout" in state["completed_quests"]
    assert game.quest_unlocked(state, "quest_boss_glen")
    print("[Pass] Mine Scout completed and Boss Quest unlocked.")

    # Verify quest_boss_glen and story_hint_card are both hidden before reaching 18/18
    guild_model_pre = session.screen_model("guild_screen")
    assert not any(r["task_id"] == "quest_boss_glen" for r in guild_model_pre["task_rows"])
    assert guild_model_pre["story_hint_card"]["visible"] is False
    print("[Pass] Boss quest and story hint card are both hidden before sighting.")

    # 4. Travel to Scorched Mine
    session.dispatch("confirm_travel", {"dungeon_id": "dungeon_scorched_mine"}, screen_id="world_map")
    assert session.exploration is not None
    assert session.exploration["dungeon_id"] == "dungeon_scorched_mine"
    assert session.exploration["current_step"] == 0
    assert session.exploration["status"] == "exploring"

    # Verify challenge_boss is NOT available at step 0
    expl_model_0 = session.screen_model("dungeon_exploration")
    actions_0 = expl_model_0["actions"]
    assert not any(a["action_id"] == "challenge_boss" for a in actions_0)
    print("[Pass] Boss challenge is hidden at step 0.")

    # 5. Advance to the end of the dungeon (step 18)
    session.exploration["current_step"] = 18

    # Verify Glen is sighted, challenge is disabled, and retreat is primary
    expl_model_18 = session.screen_model("dungeon_exploration")
    assert state["flags"].get("boss_glen_sighted") is True

    actions_18 = expl_model_18["actions"]
    boss_act = next((a for a in actions_18 if a["action_id"] == "challenge_boss"), None)
    assert boss_act is not None
    assert boss_act["enabled"] is False
    assert boss_act["disabled_reason"] == "先回工會確認這股氣息。"

    ret_act = next((a for a in actions_18 if a["action_id"] == "retreat"), None)
    assert ret_act is not None
    assert ret_act["primary"] is True
    print("[Pass] Boss challenge is disabled with correct reason before accepting investigation; retreat is primary.")

    # 6. Return to town and check Guild board
    session.dispatch("back_to_town_hub")
    assert session.exploration is None

    guild_model_sighted = session.screen_model("guild_screen")
    # Verify story hint is now visible and enabled
    assert guild_model_sighted["story_hint_card"]["visible"] is True
    assert guild_model_sighted["story_hint_card"]["enabled"] is True
    assert guild_model_sighted["story_hint_card"]["primary_action"] == "accept_boss_glen_investigation"
    print("[Pass] Story hint card is visible and enabled on Guild board.")

    # 7. Accept investigation
    session.dispatch("accept_boss_glen_investigation", screen_id="guild_screen")
    assert state["flags"].get("boss_glen_investigation_accepted") is True

    # Verify story hint card is still visible but accepted/disabled, and boss quest is visible but status is requirements_missing
    guild_model_accepted = session.screen_model("guild_screen")
    assert guild_model_accepted["story_hint_card"]["visible"] is True
    assert guild_model_accepted["story_hint_card"]["enabled"] is False
    assert guild_model_accepted["story_hint_card"]["primary_action"] == "unavailable"

    boss_quest_row = next(r for r in guild_model_accepted["task_rows"] if r["task_id"] == "quest_boss_glen")
    assert boss_quest_row["status"] == "requirements_missing"
    print("[Pass] Investigation accepted. Story hint is hidden, and boss quest is now listed as requirements_missing.")

    # 8. Travel back to Scorched Mine and reach step 18
    session.dispatch("confirm_travel", {"dungeon_id": "dungeon_scorched_mine"}, screen_id="world_map")
    session.exploration["current_step"] = 18

    # Verify challenge_boss is now enabled and primary
    expl_model_final = session.screen_model("dungeon_exploration")
    actions_final = expl_model_final["actions"]
    boss_act_final = next((a for a in actions_final if a["action_id"] == "challenge_boss"), None)
    assert boss_act_final is not None
    assert boss_act_final["enabled"] is True
    assert boss_act_final["primary"] is True
    print("[Pass] Boss challenge action is enabled and primary after accepting investigation.")

    # 9. Trigger Boss Challenge
    session.dispatch("challenge_boss", {"dungeon_id": "dungeon_scorched_mine"}, screen_id="dungeon_exploration")
    assert session.combat is not None
    assert session.combat["enemy_id"] == "boss_glen"
    assert session.combat["boss"] is True
    assert session.exploration["status"] == "combat"
    print("[Pass] Boss Glen combat successfully initiated.")

    # 10. Resolve combat in victory
    session.resolve_victory(["葛倫的防禦崩潰了！", "葛倫倒地。"])
    assert state["flags"].get("boss_glen_defeated") is True
    assert state["inventory"].get("key_blood_map", 0) == 1
    assert state["inventory"].get("key_fire_mark_shard", 0) == 1
    print("[Pass] Combat victory resolved, flags set, and quest key items dropped.")

    # 11. Return to town and open Guild board
    session.dispatch("back_to_town_hub")
    assert session.combat is None
    assert session.exploration is None

    guild_model_post = session.screen_model("guild_screen")
    # Verify story hint shows turn-in guidance
    assert guild_model_post["story_hint_card"]["visible"] is True
    assert guild_model_post["story_hint_card"]["id"] == "story_hint_boss_glen_defeated"

    boss_quest_row_post = next(r for r in guild_model_post["task_rows"] if r["task_id"] == "quest_boss_glen")
    assert boss_quest_row_post["status"] == "ready_to_submit"
    assert boss_quest_row_post["status_label"] == "可回報"
    print("[Pass] Boss quest displays as 'ready_to_submit' in Guild, and story hint shows turn-in guidance.")

    # 12. Submit Boss Quest
    session.dispatch("submit_quest", {"task_id": "quest_boss_glen"}, screen_id="guild_screen")
    assert "quest_boss_glen" in state["completed_quests"]
    assert game.is_unlocked(state, "unlock_ash_ravine")
    print("[Pass] Boss quest turned in successfully and Ash Ravine (Act 2) is unlocked!")

    print("\nAll progression coverage tests passed successfully!")


if __name__ == "__main__":
    run_progression_smoke_test()
