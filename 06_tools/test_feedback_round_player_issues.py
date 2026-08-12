"""Focused regressions for the August player-feedback maintenance round."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from data import EQUIPMENT, get_unlocked_regions  # noqa: E402
from engine import game  # noqa: E402
from engine.equipment_refs import equipment_base_id, equipment_ref_count, resolve_equipment_ref  # noqa: E402
from engine.gui_actions import GuiActionError, GuiRuntimeSession, get_status_preview_data  # noqa: E402
from engine.gui_presentation import display_hit_points, display_mana_points, equipment_stat_rows  # noqa: E402
from engine.gui_presentation_helpers import player_model  # noqa: E402
from engine.gui_workshop_model import workshop_screen_model  # noqa: E402


FIXTURE_PATH = ROOT / "06_tools" / "fixtures" / "saves" / "ice-entry.json"
FIRE_QUESTS = {
    "quest_register",
    "quest_cave_gathering",
    "quest_magic_crystal",
    "quest_mine_scout",
    "quest_boss_glen",
    "quest_ash_ravine_scout",
    "quest_supply_upgrade",
    "quest_cinder_depths_scout",
}
FIRE_DUNGEONS = {
    "dungeon_moss_cave",
    "dungeon_scorched_mine",
    "dungeon_ash_ravine",
    "dungeon_cinder_seal_depths",
}


def unlocked_workshop_session() -> tuple[GuiRuntimeSession, dict]:
    session = GuiRuntimeSession()
    session.new_game("工坊回歸測試", "warrior")
    state = session.require_state()
    state["completed_quests"].append("quest_cave_gathering")
    state["gold"] = 196
    return session, state


def material_row(recipe: dict, material_id: str) -> dict:
    return recipe["materials"][material_id]


def verify_workshop_material_details_and_instance_bases() -> None:
    session, state = unlocked_workshop_session()
    game.add_item(state, "armor_leather_armor")
    leather_ref = next(
        reference_id
        for reference_id in state["inventory"]
        if equipment_base_id(state, reference_id) == "armor_leather_armor"
    )
    assert game.equip_item(state, leather_ref, quiet=True)

    recipe = next(
        row
        for row in workshop_screen_model(state)["upgrades"]
        if row["id"] == "recipe_leather_armor_plus_1"
    )
    assert recipe["base_inventory_count"] == 0
    assert recipe["base_equipped"] is True
    assert recipe["base_owned_count"] == 1
    assert material_row(recipe, "mat_moss_fiber") == {
        "name": "青苔纖維",
        "owned": 0,
        "required": 4,
        "missing": 4,
        "satisfied": False,
    }
    assert material_row(recipe, "mat_cracked_stone") == {
        "name": "破裂石片",
        "owned": 0,
        "required": 3,
        "missing": 3,
        "satisfied": False,
    }
    assert recipe["material_shortage_message"] == (
        "素材不足：青苔纖維缺 4（持有 0/需求 4）、破裂石片缺 3（持有 0/需求 3）。"
    )

    before = copy.deepcopy(state)
    try:
        session.dispatch(
            "upgrade_equipment",
            {"recipe_id": "recipe_leather_armor_plus_1"},
            screen_id="workshop_screen",
        )
    except GuiActionError as error:
        assert error.status == 409
        assert error.blocked_reason == recipe["material_shortage_message"]
    else:
        raise AssertionError("material-deficient upgrade unexpectedly succeeded")
    assert state == before

    game.add_item(state, "mat_moss_fiber", 4)
    game.add_item(state, "mat_cracked_stone", 3)
    response = session.dispatch(
        "upgrade_equipment",
        {"recipe_id": "recipe_leather_armor_plus_1"},
        screen_id="workshop_screen",
    )
    assert response["ok"] is True
    assert state["equipment"]["body"] is None
    assert leather_ref not in state["equipment_instances"]
    assert equipment_ref_count(state, "armor_leather_armor_plus_1") == 1

    backpack_session, backpack_state = unlocked_workshop_session()
    game.add_item(backpack_state, "armor_leather_armor")
    game.add_item(backpack_state, "mat_moss_fiber", 4)
    game.add_item(backpack_state, "mat_cracked_stone", 3)
    backpack_session.dispatch(
        "upgrade_equipment",
        {"recipe_id": "recipe_leather_armor_plus_1"},
        screen_id="workshop_screen",
    )
    assert equipment_ref_count(backpack_state, "armor_leather_armor") == 0
    assert equipment_ref_count(backpack_state, "armor_leather_armor_plus_1") == 1


def verify_player_resource_formatting() -> None:
    assert display_hit_points(209.1) == "209"
    assert display_hit_points(215.6) == "216"
    assert display_mana_points(12.5) == "13"
    session = GuiRuntimeSession()
    session.new_game("資源格式測試", "warrior")
    state = session.require_state()
    state["current_hp"] = 91.0
    state["current_mp"] = 12.5
    session.start_combat("mon_cinder_bat")

    combat = session.combat_screen_model()
    assert combat["player"]["hp_label"] == "91 / 120"
    assert combat["player"]["mp_label"] == "13 / 20"
    assert "目前 MP 13/20" in combat["skill_menu"]["summary"]
    assert ".0" not in combat["player"]["hp_label"]

    world_player = player_model(state)
    assert world_player["hp"]["label"] == "HP 91/120"
    assert world_player["mp"]["label"] == "MP 13/20"
    status = get_status_preview_data(state)
    assert (status["hp_current"], status["hp_max"]) == ("91", "120")
    assert (status["mp_current"], status["mp_max"]) == ("13", "20")
    assert [row["key"] for row in equipment_stat_rows({"trap_evasion": 8, "attack": 3})] == ["attack"]


def verify_fire_clear_fixture_load_and_ice_route() -> None:
    raw = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    before = copy.deepcopy(raw)
    migrated = game.ensure_state_defaults(raw)
    assert migrated == before, "current-version fixture must load without migration drift"
    assert FIRE_QUESTS.issubset(migrated["completed_quests"])
    assert FIRE_DUNGEONS == set(migrated["cleared_dungeons"])
    assert migrated["flags"]["boss_glen_defeated"] is True
    assert migrated["flags"]["ash_guardian_defeated"] is True
    assert migrated["flags"]["cinder_seal_sentinel_defeated"] is True
    assert migrated["flags"]["fire_seal_enshrined"] is True
    assert get_unlocked_regions(migrated) == ["border_fire", "ice"]
    assert not any(quest_id.startswith("quest_ice_") for quest_id in migrated["completed_quests"])
    assert not any(dungeon_id.startswith("dungeon_ice_") for dungeon_id in migrated["cleared_dungeons"])
    assert "dungeon_ice_minor_a" in game.player_facing_dungeon_ids(migrated, "ice")

    expected_equipment = {
        "weapon": "weapon_iron_sword_plus_1",
        "head": "armor_leather_cap",
        "body": "armor_leather_armor_plus_1",
        "accessory": "acc_fire_cloak",
    }
    for slot, base_item_id in expected_equipment.items():
        reference_id = migrated["equipment"][slot]
        resolved = resolve_equipment_ref(migrated, reference_id)
        assert resolved and resolved["base_item_id"] == base_item_id
        assert resolved["quality"] == "fine"
        assert migrated["job"] in EQUIPMENT[base_item_id]["jobs"]

    workshop = workshop_screen_model(migrated, selected_region_id="ice")
    equipped_weapon = next(item for item in workshop["owned_equipment"] if item["equipped_slot"] == "weapon")
    assert equipped_weapon["slot_label"] == "武器"
    assert equipped_weapon["equipped_slot_label"] == "武器"
    assert equipped_weapon["status_label"] == "已裝備"
    assert equipped_weapon["comparison"] is not None
    assert all(row["key"] != "physical_charge_skill_bonus" or row["label"] == "蓄力技能傷害"
               for item in workshop["owned_equipment"] for row in item["stat_rows"])

    stats = game.get_stats(migrated)
    assert migrated["current_hp"] == stats["max_hp"]
    assert migrated["current_mp"] == stats["max_mp"]

    original_save_path = game.SAVE_PATH
    try:
        game.SAVE_PATH = FIXTURE_PATH
        session = GuiRuntimeSession()
        load_response = session.load_game()
        assert load_response["ok"] is True
        assert session.current_region_id == "border_fire"
        travel_response = session.dispatch(
            "travel_region",
            {"region_id": "ice"},
            screen_id="world_map",
        )
        assert travel_response["screen_model"]["current_region_id"] == "ice"
        assert session.require_state()["flags"]["current_region_id"] == "ice"
        assert not any(
            quest_id.startswith("quest_ice_")
            for quest_id in session.require_state()["completed_quests"]
        )
    finally:
        game.SAVE_PATH = original_save_path


def main() -> None:
    verify_workshop_material_details_and_instance_bases()
    verify_player_resource_formatting()
    verify_fire_clear_fixture_load_and_ice_route()
    print("player feedback round focused contracts passed")


if __name__ == "__main__":
    main()
