"""Focused contracts for the Johnson Wu maintenance fixes."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "03_engine", ROOT / "04_data"):
    sys.path.insert(0, str(module_root))

from data import DUNGEONS, JOBS, MONSTERS  # noqa: E402
from engine import game  # noqa: E402
from engine.gui_actions import GuiRuntimeSession  # noqa: E402
from engine.gui_presentation import resource_strip  # noqa: E402
from engine.gui_workshop_model import workshop_screen_model  # noqa: E402


def exploration(dungeon_id: str) -> dict:
    return {
        "dungeon_id": dungeon_id,
        "current_step": DUNGEONS[dungeon_id]["steps"],
        "run_log": {"gold": 10, "items": {}, "dungeon_id": dungeon_id},
        "events": [],
        "last_message": "",
        "status": "resolved",
    }


def session_with_state() -> GuiRuntimeSession:
    session = GuiRuntimeSession()
    session.new_game("Feedback QA", "warrior")
    return session


def verify_gui_defeat_ends_run() -> None:
    session = session_with_state()
    state = session.require_state()
    state["current_hp"] = -2
    session.exploration = exploration("dungeon_moss_cave")
    response = session.resolve_defeat("contract defeat")
    assert state["current_hp"] > 0
    assert session.exploration is None and session.combat is None
    assert response["screen_model"]["result_overlay"]["outcome"] == "defeat"
    town = session.dispatch("back_to_town_hub", {}, screen_id="combat_screen")
    assert town["screen_model"]["screen_id"] == "town_hub"


def verify_glen_endpoint_and_legacy_progress() -> None:
    session = session_with_state()
    session.exploration = exploration("dungeon_scorched_mine")
    response = session.dispatch("return_to_exploration", {}, screen_id="combat_screen")
    assert response["story_beat"]["id"] == "boss.before.boss_glen"
    assert game.boss_available_at_dungeon_end(session.require_state(), "dungeon_scorched_mine", "boss_glen")
    assert next(action for action in response["screen_model"]["actions"] if action["action_id"] == "challenge_boss")["enabled"]

    legacy = session_with_state()
    legacy.require_state()["flags"][game.BOSS_GLEN_SIGHTED_FLAG] = True
    legacy.exploration = exploration("dungeon_scorched_mine")
    legacy.dispatch("return_to_exploration", {}, screen_id="combat_screen")
    assert legacy.require_state()["flags"][game.BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG]


def verify_exp_settlement() -> None:
    state = game.create_state("EXP QA", next(iter(JOBS)))
    state["level"] = 5
    assert game.exp_reward_for_dungeon(state, 100, "dungeon_moss_cave")["awarded_exp"] == 100
    state["level"] = 6
    assert game.exp_reward_for_dungeon(state, 100, "dungeon_moss_cave")["awarded_exp"] == 20

    session = session_with_state()
    state = session.require_state()
    state["level"] = 6
    session.exploration = exploration("dungeon_moss_cave")
    session.start_combat("mon_moss_rat")
    before = state["exp"]
    session.resolve_victory(["EXP contract"])
    assert state["exp"] - before == int(MONSTERS["mon_moss_rat"]["exp"] * 0.2)


def verify_preview_beats_are_once_only() -> None:
    state = game.create_state("Preview QA", next(iter(JOBS)))
    temple = GuiRuntimeSession()
    temple.state = state
    assert temple.temple_screen_model()["story_beat"]["id"] == "guidance.promotion_preview"
    assert temple.temple_screen_model()["story_beat"] is None
    relic = temple.relic_preview_screen_model()
    assert relic["story_beat"]["id"] == "guidance.relic_preview"
    assert all(not slot["passive_enabled"] for slot in relic["slots"])


def verify_workshop_resolves_equipment_instances_and_supply_gate() -> None:
    session = session_with_state()
    state = session.require_state()
    game.add_item(state, "weapon_iron_sword", 1)
    sword_ref = next(key for key in state["inventory"] if key.startswith("eqi_"))
    session.dispatch("equip_weapon", {"item_id": sword_ref}, screen_id="workshop_screen")
    model = workshop_screen_model(state)
    sword = next(entry for entry in model["owned_equipment"] if entry["id"] == sword_ref)
    assert sword["base_item_id"] == "weapon_iron_sword"
    assert sword["equipped_slot"] == "weapon"

    assert not state["flags"].get("dungeon_cinder_seal_depths")
    state["flags"]["ash_guardian_defeated"] = True
    assert game.quest_unlocked(state, "quest_supply_upgrade")
    assert not state["flags"].get("dungeon_cinder_seal_depths")


def verify_resource_display_is_clean() -> None:
    state = game.create_state("Format QA", next(iter(JOBS)))
    state["current_hp"] = 91.0000000001
    state["current_mp"] = 12.5
    labels = {row["id"]: row["label"] for row in resource_strip(state)}
    assert labels["hp"].startswith("HP 91/")
    assert labels["mp"].startswith("MP 12.5/")


def main() -> None:
    verify_gui_defeat_ends_run()
    verify_glen_endpoint_and_legacy_progress()
    verify_exp_settlement()
    verify_preview_beats_are_once_only()
    verify_workshop_resolves_equipment_instances_and_supply_gate()
    verify_resource_display_is_clean()
    print("feedback maintenance contracts ok")


if __name__ == "__main__":
    main()
