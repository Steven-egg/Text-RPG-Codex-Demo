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


def verify_run_supply_limits_and_mp_timing() -> None:
    session = GuiRuntimeSession()
    session.new_game(name="Supply Bridge Tester", job_id="mage")
    state = session.require_state()
    for item_id, quantity in {
        "item_potion_s": 4,
        "item_potion_m": 1,
        "item_focus_drop": 2,
        "item_armor_piercer": 2,
    }.items():
        game.add_item(state, item_id, quantity)
    game.configure_run_supplies(state, {
        "sustain_hp": {"item_id": "item_potion_s", "quantity": 3},
        "emergency_hp": {"item_id": "item_potion_m", "quantity": 1},
        "mp": {"item_id": "item_focus_drop", "quantity": 2},
        "throwable": {"item_id": "item_armor_piercer", "quantity": 2},
    })
    assert game.combat_item_quantity(state, "item_potion_s") == 3
    session.start_combat("mon_moss_rat", boss=False)
    combat = session.require_combat()
    turn_before = combat["turn"]
    session.dispatch("use_item", {"item_id": "item_focus_drop"}, screen_id="combat_screen")
    assert combat["turn"] == turn_before
    error = assert_blocked(
        lambda: session.dispatch("use_item", {"item_id": "item_focus_drop"}, screen_id="combat_screen")
    )
    assert error.blocked_reason == "本回合已使用 MP 藥水。"
    print("[Pass] Run supplies cap items and MP uses no action but only once per turn.")


def verify_regional_supply_slots_and_recovery() -> None:
    session = GuiRuntimeSession()
    session.new_game(name="Regional Supply Tester", job_id="mage")
    state = session.require_state()
    for item_id in ("item_ice_potion_01", "item_ice_potion_02"):
        game.add_item(state, item_id, 1)
    try:
        game.configure_run_supplies(state, {
            "sustain_hp": {"item_id": "item_ice_potion_01", "quantity": 1},
        })
    except ValueError:
        pass
    else:
        raise AssertionError("Regional HP potion must not enter the sustain slot.")

    game.configure_run_supplies(state, {
        "emergency_hp": {"item_id": "item_ice_potion_01", "quantity": 1},
        "mp": {"item_id": "item_ice_potion_02", "quantity": 1},
    })
    stats = game.get_stats(state)
    hp_recovery = game.combat_recovery_amount(state, "item_ice_potion_01")
    mp_recovery = game.combat_recovery_amount(state, "item_ice_potion_02")
    assert hp_recovery == max(120, game.math.ceil(stats["max_hp"] * 0.60))
    assert mp_recovery == max(30, game.math.ceil(stats["max_mp"] * 0.30))
    state["current_hp"] = 1
    state["current_mp"] = 0
    session.start_combat("mon_moss_rat", boss=False)
    combat = session.require_combat()
    assert {row["payload"]["item_id"] for row in session.combat_screen_model()["item_menu"]["items"]} >= {
        "item_ice_potion_01", "item_ice_potion_02",
    }
    session.use_combat_item("item_ice_potion_01")
    assert state["current_hp"] == min(stats["max_hp"], 1 + hp_recovery)
    turn_before = combat["turn"]
    session.dispatch("use_item", {"item_id": "item_ice_potion_02"}, screen_id="combat_screen")
    assert state["current_mp"] == min(stats["max_mp"], mp_recovery)
    assert combat["turn"] == turn_before
    print("[Pass] Regional HP/MP supplies use their dedicated slots and shared recovery formulas.")


def verify_throwable_contract_and_live_parity() -> None:
    state = game.create_state("Throwable Tester", "法師")
    for item_id in ("item_armor_piercer", "item_throw_ice"):
        game.add_item(state, item_id, 3)
    try:
        game.configure_run_supplies(state, {"throwable": {"item_id": "item_throw_ice", "quantity": 3}})
    except ValueError:
        pass
    else:
        raise AssertionError("Throwable supply slot must cap at two items per run.")

    physical_enemy = game.MONSTERS["boss_glen"]
    physical_damage, debuff_turns = game.combat_throwable_damage("item_armor_piercer", physical_enemy, {})
    assert physical_damage == game.math.ceil(90 - physical_enemy["defense"] * 0.6)
    assert debuff_turns == 5

    elemental_enemy = game.MONSTERS["boss_glen"]
    ice_damage, debuff_turns = game.combat_throwable_damage("item_throw_ice", elemental_enemy, {})
    assert ice_damage == game.math.ceil(45 * 1.25)
    assert debuff_turns == 0

    session = GuiRuntimeSession()
    session.new_game(name="Throwable Bridge Tester", job_id="mage")
    live_state = session.require_state()
    game.add_item(live_state, "item_throw_ice", 2)
    game.configure_run_supplies(live_state, {"throwable": {"item_id": "item_throw_ice", "quantity": 2}})
    session.start_combat("boss_glen", boss=True)
    combat = session.require_combat()
    enemy_hp = combat["enemy_hp"]
    assert "item_throw_ice" in {row["payload"]["item_id"] for row in session.combat_screen_model()["item_menu"]["items"]}
    session.dispatch("use_item", {"item_id": "item_throw_ice"}, screen_id="combat_screen")
    assert combat["enemy_hp"] == enemy_hp - ice_damage
    assert live_state["inventory"].get("item_throw_ice", 0) == 1
    print("[Pass] Throwables enforce a two-item run cap and share CLI/live GUI damage behavior.")


def verify_tactical_throwable_contract() -> None:
    cleric_job = next(job_id for job_id, job in game.JOBS.items() if "skill_sanctified_decay" in job["base_skills"])
    warrior_job = next(job_id for job_id, job in game.JOBS.items() if "skill_power_slash" in job["base_skills"])
    cleric = game.create_state("Tactical Cleric", cleric_job)
    warrior = game.create_state("Tactical Warrior", warrior_job)
    assert not game.item_job_allowed(warrior, "item_sanctified_ash_vial")
    game.add_item(cleric, "item_sanctified_ash_vial", 2)
    game.configure_run_supplies(cleric, {"throwable": {"item_id": "item_sanctified_ash_vial", "quantity": 2}})
    enemy = game.MONSTERS["boss_glen"]
    buffs = {}
    result = game.use_combat_throwable(cleric, "item_sanctified_ash_vial", enemy, buffs)
    assert result.damage == 20
    assert buffs["sanctified_erosion"] == 5
    game.apply_dot(buffs, "cleric_dot", 5, 0.1, "magic", "fire")
    game.use_combat_throwable(cleric, "item_sanctified_ash_vial", enemy, buffs)
    assert buffs["sanctified_erosion"] == 5 and buffs["cleric_dot"] == 5
    for expected_turns in range(4, -1, -1):
        _events, damage = game.tick_effects(cleric, {}, buffs, enemy)
        assert damage >= 15
        assert buffs.get("sanctified_erosion", 0) == expected_turns

    game.add_item(warrior, "item_rending_spike", 1)
    game.configure_run_supplies(warrior, {"throwable": {"item_id": "item_rending_spike", "quantity": 1}})
    rending_buffs = {}
    assert game.use_combat_throwable(warrior, "item_rending_spike", enemy, rending_buffs).damage == 25
    _events, rending_tick = game.tick_effects(warrior, {}, rending_buffs, enemy)
    assert rending_tick == 18

    session = GuiRuntimeSession()
    session.new_game(name="Tactical GUI Cleric", job_id="cleric")
    live_state = session.require_state()
    game.add_item(live_state, "item_sanctified_ash_vial", 1)
    game.configure_run_supplies(live_state, {"throwable": {"item_id": "item_sanctified_ash_vial", "quantity": 1}})
    session.start_combat("boss_glen", boss=True)
    combat = session.require_combat()
    enemy_hp = combat["enemy_hp"]
    session.dispatch("use_item", {"item_id": "item_sanctified_ash_vial"}, screen_id="combat_screen")
    assert combat["enemy_hp"] == enemy_hp - 35
    assert combat["enemy_buffs"].get("sanctified_erosion") == 4
    print("[Pass] Tactical throwables enforce jobs, refresh five-turn DoTs, coexist, and keep live GUI parity.")


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


def verify_dot_log_and_victory() -> None:
    session = GuiRuntimeSession()
    session.new_game(name="DoT Bridge Tester", job_id="rogue")
    session.start_combat("mon_moss_rat", boss=False)
    combat = session.require_combat()
    combat["enemy_hp"] = 1
    game.apply_dot(combat["enemy_buffs"], "bleed", 1, 0.45, "physical", "物理")

    response = session.dispatch("defend", {}, screen_id="combat_screen")

    assert response["ok"] is True
    assert combat["outcome"] == "victory"
    assert any("流血造成" in line for line in combat["battle_log"])
    assert not any("['" in line or line.endswith(": 6") for line in combat["battle_log"])
    print("[Pass] Live bridge records DoT as readable lines and resolves DoT victory.")


def run_smoke_test() -> None:
    print("Starting Combat Bridge Boss Rule Parity smoke test...")
    verify_boss_retreat_block()
    verify_run_supply_limits_and_mp_timing()
    verify_regional_supply_slots_and_recovery()
    verify_throwable_contract_and_live_parity()
    verify_tactical_throwable_contract()
    verify_boss_action_markers()
    verify_action_loop_victory()
    verify_dot_log_and_victory()
    print("\nCombat Bridge Boss Rule Parity smoke test passed.")


if __name__ == "__main__":
    run_smoke_test()
