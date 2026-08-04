"""Focused live-GUI coverage for every authoritative recipe."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from data import EQUIPMENT, RECIPES, REGIONS
from engine import game
from engine.equipment_refs import equipment_ref_count, inventory_equipment_refs
from engine.gui_actions import GuiActionError, GuiRuntimeSession


JOB_TO_GUI_ID = {
    "劍士": "warrior",
    "法師": "mage",
    "盜賊": "rogue",
    "牧師": "cleric",
}


def compatible_job(recipe: dict) -> str:
    equipment_outputs = [item_id for item_id in recipe["output"] if item_id in EQUIPMENT]
    return EQUIPMENT[equipment_outputs[0]]["jobs"][0] if equipment_outputs else "劍士"


def seed_recipe_session(recipe_id: str) -> tuple[GuiRuntimeSession, dict, str, set[str]]:
    recipe = RECIPES[recipe_id]
    job = compatible_job(recipe)
    session = GuiRuntimeSession()
    session.new_game(f"coverage-{recipe_id}", JOB_TO_GUI_ID[job])
    state = session.require_state()
    region_id = game.recipe_region_id(recipe)
    region_unlock = REGIONS[region_id].get("unlock_key")
    if region_unlock:
        game.unlock(state, region_unlock)
    if recipe.get("unlock"):
        game.unlock(state, recipe["unlock"])
    session.set_current_region(region_id)
    state["gold"] = recipe["gold"] + 10
    for item_id, quantity in recipe["materials"].items():
        game.add_item(state, item_id, quantity)

    consumed_refs: set[str] = set()
    base_item = recipe.get("base_item")
    if base_item:
        game.add_item(state, base_item, 1)
        consumed_refs = set(inventory_equipment_refs(state, base_item))
        assert len(consumed_refs) == 1
    return session, state, region_id, consumed_refs


def verify_all_recipes_are_routed_and_executable() -> None:
    workshop_ids = {
        recipe_id
        for region_id in REGIONS
        for recipe_id in game.workshop_recipe_ids(region_id)
    }
    synthesis_ids = {
        recipe_id
        for region_id in REGIONS
        for recipe_id in game.synthesis_recipe_ids(region_id)
    }
    assert workshop_ids.isdisjoint(synthesis_ids)
    assert workshop_ids | synthesis_ids == set(RECIPES)
    assert len(RECIPES) == 40
    assert {
        region_id: sum(game.recipe_region_id(recipe) == region_id for recipe in RECIPES.values())
        for region_id in REGIONS
    } == {"border_fire": 9, "ice": 7, "earth": 7, "thunder": 7, "final": 10}
    assert sum(bool(recipe.get("base_item")) for recipe in RECIPES.values()) == 21

    for recipe_id, recipe in RECIPES.items():
        session, state, region_id, consumed_refs = seed_recipe_session(recipe_id)
        workshop_model = session.screen_model("workshop_screen")
        synthesis_model = session.screen_model("synthesis_screen")
        assert {row["id"] for row in workshop_model["upgrades"]} == set(game.workshop_recipe_ids(region_id))
        assert {row["recipe_id"] for row in synthesis_model["recipe_rows"]} == set(game.synthesis_recipe_ids(region_id))

        is_workshop = recipe_id in workshop_ids
        action_id = "upgrade_equipment" if is_workshop else "craft_recipe"
        screen_id = "workshop_screen" if is_workshop else "synthesis_screen"
        response = session.dispatch(action_id, {"recipe_id": recipe_id}, screen_id=screen_id)
        assert response["ok"] is True, recipe_id
        assert response["next_screen_id"] == screen_id
        if is_workshop:
            assert {row["id"] for row in response["screen_model"]["upgrades"]} == set(game.workshop_recipe_ids(region_id))
        else:
            assert {row["recipe_id"] for row in response["screen_model"]["recipe_rows"]} == set(game.synthesis_recipe_ids(region_id))
        assert state["gold"] == 10

        for reference_id in consumed_refs:
            assert reference_id not in state["inventory"]
            assert reference_id not in state["equipment_instances"]

        for output_id, quantity in recipe["output"].items():
            if output_id in EQUIPMENT:
                if EQUIPMENT[output_id]["slot"] == "special":
                    assert state["inventory"].get(output_id, 0) == quantity
                    equip_response = session.dispatch(
                        "equip_equipment",
                        {"item_id": output_id},
                        screen_id="world_map",
                    )
                    assert state["equipment"]["special"] == output_id
                    assert equip_response["next_screen_id"] == "world_map"
                else:
                    assert equipment_ref_count(state, output_id) == quantity
                    assert all(
                        state["equipment_instances"][reference_id]["base_item_id"] == output_id
                        for reference_id in inventory_equipment_refs(state, output_id)
                    )
            else:
                assert state["inventory"].get(output_id, 0) == quantity


def verify_player_facing_lock_and_route_messages() -> None:
    session = GuiRuntimeSession()
    session.new_game("locked-copy", "warrior")
    state = session.require_state()

    expected_copy = {
        "recipe_iron_sword_plus_1": "完成公會任務「洞窟採集」",
        "recipe_focus_pouch": "完成公會任務「魔晶研究」",
        "recipe_heat_charm": "在焦石礦坑擊敗熔岩小鬼",
        "recipe_ice_battle_01": "安置「火之聖印」",
        "recipe_final_upgrade_01": "安置火、冰、大地、雷鳴四枚聖印",
    }
    for recipe_id, expected in expected_copy.items():
        reason = game.recipe_locked_reason(state, recipe_id)
        assert reason and expected in reason
        assert "recipe_" not in reason and "unlock_" not in reason

    for recipe_id in RECIPES:
        condition = game.recipe_unlock_condition(recipe_id)
        reason = game.recipe_locked_reason(state, recipe_id)
        assert condition and "recipe_" not in condition and "unlock_" not in condition
        assert condition != "推進目前區域主線並取得配方授權"
        assert reason and condition in reason
        assert "recipe_" not in reason and "unlock_" not in reason

    synthesis_model = session.screen_model("synthesis_screen")
    focus_action = synthesis_model["recipe_details"]["recipe_focus_pouch"]["primary_action"]
    assert focus_action["enabled"] is False
    assert "完成公會任務「魔晶研究」" in focus_action["disabled_reason"]

    workshop_model = session.screen_model("workshop_screen")
    iron_upgrade = next(row for row in workshop_model["upgrades"] if row["id"] == "recipe_iron_sword_plus_1")
    assert iron_upgrade["unlocked"] is False
    assert "完成公會任務「洞窟採集」" in iron_upgrade["locked_reason"]

    game.unlock(state, "recipe_iron_sword_plus_1")
    try:
        session.dispatch("craft_recipe", {"recipe_id": "recipe_iron_sword_plus_1"}, screen_id="synthesis_screen")
        raise AssertionError("workshop recipe unexpectedly executed through synthesis")
    except GuiActionError as error:
        assert error.status == 409 and "工坊" in error.blocked_reason
        assert "白名單" not in str(error)

    game.unlock(state, "unlock_final_region_preview")
    try:
        session.dispatch("upgrade_equipment", {"recipe_id": "recipe_final_upgrade_01"}, screen_id="workshop_screen")
        raise AssertionError("cross-region recipe unexpectedly executed")
    except GuiActionError as error:
        assert error.status == 403 and "魔王城前線" in error.blocked_reason
        assert "recipe_" not in error.blocked_reason and "unlock_" not in error.blocked_reason


def verify_recipe_job_gate() -> None:
    session = GuiRuntimeSession()
    session.new_game("recipe-job-gate", "rogue")
    state = session.require_state()
    game.unlock(state, "unlock_ice_region")
    session.set_current_region("ice")
    game.add_item(state, "weapon_ice_warrior_01")
    game.add_item(state, "mat_ice_salt", 5)
    game.add_item(state, "mat_ice_saltcloth", 2)
    state["gold"] = 999
    row = next(
        row
        for row in session.screen_model("workshop_screen")["upgrades"]
        if row["id"] == "recipe_ice_upgrade_01"
    )
    assert row["unlocked"] is True
    assert row["job_compatible"] is False
    assert "目前職業「盜賊」" in row["job_blocked_reason"]
    before = copy.deepcopy(state)
    try:
        session.dispatch(
            "upgrade_equipment",
            {"recipe_id": "recipe_ice_upgrade_01"},
            screen_id="workshop_screen",
        )
        raise AssertionError("job-incompatible recipe unexpectedly executed")
    except GuiActionError as error:
        assert error.status == 403 and "目前職業「盜賊」" in error.blocked_reason
    assert state == before


def verify_recipe_ids_are_not_rendered_in_action_logs() -> None:
    workshop_script = (ROOT / "07_gui_prototype/workshop_screen/workshop-screen.js").read_text(encoding="utf-8")
    synthesis_script = (ROOT / "07_gui_prototype/synthesis_screen/synthesis-screen.js").read_text(encoding="utf-8")
    assert "delete detailsCopy.recipe_id" in workshop_script
    assert "delete publicPayload.recipe_id" in synthesis_script


def run() -> None:
    verify_all_recipes_are_routed_and_executable()
    verify_player_facing_lock_and_route_messages()
    verify_recipe_job_gate()
    verify_recipe_ids_are_not_rendered_in_action_logs()


if __name__ == "__main__":
    run()
    print("all 40 live GUI recipe coverage checks passed")
