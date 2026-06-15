from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from engine import game
from engine.gui_actions import GuiActionError, GuiRuntimeSession


def boss_session(boss_id: str) -> tuple[GuiRuntimeSession, dict]:
    session = GuiRuntimeSession()
    session.new_game(name="Combat Bridge Tester", job_id="warrior")
    session.start_combat(boss_id, boss=True)
    return session, session.require_state()


def assert_blocked(action) -> GuiActionError:
    try:
        action()
    except GuiActionError as error:
        assert error.status == 409
        return error
    raise AssertionError("Expected combat action to be blocked.")


def verify_boss_retreat_block() -> None:
    session, state = boss_session("boss_glen")
    combat = session.require_combat()
    turn_before = combat["turn"]
    hp_before = state["current_hp"]

    error = assert_blocked(
        lambda: session.dispatch("retreat", {}, screen_id="combat_screen")
    )

    assert error.blocked_reason == "Boss 戰不可逃跑。"
    assert combat["turn"] == turn_before
    assert state["current_hp"] == hp_before
    assert combat["outcome"] is None

    retreat = next(
        action
        for action in session.combat_screen_model()["actions"]
        if action["action_id"] == "retreat"
    )
    assert retreat["enabled"] is False
    assert retreat["disabled_reason"] == "Boss 戰不可逃跑。"
    print("[Pass] Boss retreat is blocked without advancing combat.")


def verify_boss_escape_scroll_block() -> None:
    session, state = boss_session("boss_glen")
    state["inventory"]["item_escape_scroll"] = 1
    combat = session.require_combat()
    turn_before = combat["turn"]

    error = assert_blocked(
        lambda: session.dispatch(
            "use_item",
            {"item_id": "item_escape_scroll"},
            screen_id="combat_screen",
        )
    )

    assert error.blocked_reason == "Boss 戰不可使用逃脫卷軸。"
    assert state["inventory"]["item_escape_scroll"] == 1
    assert combat["turn"] == turn_before
    assert combat["outcome"] is None
    print("[Pass] Boss Escape Scroll is blocked without consumption or turn advance.")


def verify_boss_action_markers() -> None:
    thresholds = {
        "boss_glen": 0.60,
        "boss_ash_guardian": 0.45,
        "boss_cinder_seal_sentinel": 0.50,
    }
    for boss_id, threshold in thresholds.items():
        session, _ = boss_session(boss_id)
        combat = session.require_combat()
        combat["enemy_hp"] = max(1, int(combat["enemy"]["hp"] * threshold))

        session.dispatch("defend", {}, screen_id="combat_screen")

        assert combat["boss_marker"] is True
        assert combat["turn"] == 2
        assert combat["outcome"] is None
        print(f"[Pass] {boss_id} used its specialized action and saved its marker.")


def verify_action_loop_victory() -> None:
    session, state = boss_session("boss_glen")
    combat = session.require_combat()
    combat["enemy_hp"] = 1

    response = session.dispatch(
        "basic_attack",
        {"enemy_id": "boss_glen"},
        screen_id="combat_screen",
    )

    assert response["ok"] is True
    assert combat["outcome"] == "victory"
    assert state["flags"].get("boss_glen_defeated") is True
    assert state["inventory"].get("key_blood_map", 0) == 1
    print("[Pass] Boss victory resolved through the live combat action loop.")


def run_smoke_test() -> None:
    print("Starting Combat Bridge Boss Rule Parity smoke test...")
    verify_boss_retreat_block()
    verify_boss_escape_scroll_block()
    verify_boss_action_markers()
    verify_action_loop_victory()
    print("\nCombat Bridge Boss Rule Parity smoke test passed.")


if __name__ == "__main__":
    run_smoke_test()
