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
from engine.equipment_refs import equipment_base_id, first_inventory_equipment_ref


def run_smoke_test():
    print("Starting Synthesis Mira Recipes Coverage bridge smoke test...")

    # ----------------------------------------------------
    # 1. Happy Path: recipe_piercing_bundle
    # ----------------------------------------------------
    session = GuiRuntimeSession()
    session.new_game(name="測試合成家", job_id="rogue")
    state = session.require_state()

    state["completed_quests"].append("quest_ash_ravine_scout")
    state["gold"] = 200
    state["inventory"]["mat_ravine_ash"] = 3
    state["inventory"]["mat_charred_iron"] = 2

    print(f"[Happy Path - piercing] Initial Gold: {state['gold']}, Inventory: {dict(state['inventory'])}")
    response = session.dispatch("craft_recipe", {"recipe_id": "recipe_piercing_bundle"}, screen_id="synthesis_screen")
    assert response["ok"] is True
    assert state["gold"] == 80  # 200 - 120 = 80G
    assert state["inventory"].get("mat_ravine_ash", 0) == 0  # 3 - 3 = 0
    assert state["inventory"].get("mat_charred_iron", 0) == 0  # 2 - 2 = 0
    assert state["inventory"]["item_armor_piercer"] == 3  # outputs 3 items
    print("Happy Path (piercing bundle) verified.")

    # ----------------------------------------------------
    # 2. Happy Path: recipe_fire_cloak
    # ----------------------------------------------------
    session_fc = GuiRuntimeSession()
    session_fc.new_game(name="測試合成家", job_id="rogue")
    state_fc = session_fc.require_state()

    game.unlock(state_fc, "recipe_fire_cloak")
    state_fc["gold"] = 400
    state_fc["inventory"]["mat_fire_stone"] = 5
    state_fc["inventory"]["mat_scorched_iron"] = 3

    print(f"[Happy Path - fire cloak] Initial Gold: {state_fc['gold']}, Inventory: {dict(state_fc['inventory'])}")
    response = session_fc.dispatch("craft_recipe", {"recipe_id": "recipe_fire_cloak"}, screen_id="synthesis_screen")
    assert response["ok"] is True
    assert state_fc["gold"] == 100  # 400 - 300 = 100G
    assert state_fc["inventory"]["mat_fire_stone"] == 2  # 5 - 3 = 2
    assert state_fc["inventory"]["mat_scorched_iron"] == 1  # 3 - 2 = 1
    fire_cloak = first_inventory_equipment_ref(state_fc, "acc_fire_cloak")
    assert fire_cloak and equipment_base_id(state_fc, fire_cloak) == "acc_fire_cloak"
    print("Happy Path (fire cloak) verified.")

    # ----------------------------------------------------
    # 3. Happy Path: recipe_focus_pouch
    # ----------------------------------------------------
    session_fp = GuiRuntimeSession()
    session_fp.new_game(name="測試合成家", job_id="rogue")
    state_fp = session_fp.require_state()

    game.unlock(state_fp, "recipe_focus_pouch")
    state_fp["gold"] = 300
    state_fp["inventory"]["mat_moss_fiber"] = 4
    state_fp["inventory"]["mat_small_crystal"] = 3

    print(f"[Happy Path - focus pouch] Initial Gold: {state_fp['gold']}, Inventory: {dict(state_fp['inventory'])}")
    response = session_fp.dispatch("craft_recipe", {"recipe_id": "recipe_focus_pouch"}, screen_id="synthesis_screen")
    assert response["ok"] is True
    assert state_fp["gold"] == 160  # 300 - 140 = 160G
    assert state_fp["inventory"]["mat_moss_fiber"] == 1  # 4 - 3 = 1
    assert state_fp["inventory"]["mat_small_crystal"] == 1  # 3 - 2 = 1
    assert state_fp["inventory"]["special_focus_pouch"] == 1
    equip_response = session_fp.dispatch(
        "equip_equipment",
        {"item_id": "special_focus_pouch"},
        screen_id="world_map",
    )
    assert state_fp["equipment"]["special"] == "special_focus_pouch"
    assert equip_response["screen_model"]["utility_preview"]["type"] == "inventory"
    print("Happy Path (focus pouch) verified.")

    # ----------------------------------------------------
    # 4. Happy Path: recipe_heat_charm (Base item in inventory)
    # ----------------------------------------------------
    session_hc1 = GuiRuntimeSession()
    session_hc1.new_game(name="測試合成家", job_id="rogue")
    state_hc1 = session_hc1.require_state()

    game.unlock(state_hc1, "recipe_heat_charm")
    state_hc1["gold"] = 500
    state_hc1["inventory"]["mat_fire_stone"] = 3
    state_hc1["inventory"]["mat_lava_shard"] = 2
    game.add_item(state_hc1, "acc_warm_stone", 1)

    print(f"[Happy Path - heat charm (inv)] Initial Gold: {state_hc1['gold']}, Inventory: {dict(state_hc1['inventory'])}")
    response = session_hc1.dispatch("craft_recipe", {"recipe_id": "recipe_heat_charm"}, screen_id="synthesis_screen")
    assert response["ok"] is True
    assert state_hc1["gold"] == 240  # 500 - 260 = 240G
    assert state_hc1["inventory"]["mat_fire_stone"] == 1  # 3 - 2 = 1
    assert state_hc1["inventory"]["mat_lava_shard"] == 1  # 2 - 1 = 1
    assert first_inventory_equipment_ref(state_hc1, "acc_warm_stone") is None  # consumed
    assert equipment_base_id(state_hc1, first_inventory_equipment_ref(state_hc1, "acc_warm_stone_plus")) == "acc_warm_stone_plus"
    print("Happy Path (heat charm, base item in inventory) verified.")

    # ----------------------------------------------------
    # 5. Happy Path: recipe_heat_charm (Base item equipped)
    # ----------------------------------------------------
    session_hc2 = GuiRuntimeSession()
    session_hc2.new_game(name="測試合成家", job_id="rogue")
    state_hc2 = session_hc2.require_state()

    game.unlock(state_hc2, "recipe_heat_charm")
    state_hc2["gold"] = 500
    state_hc2["inventory"]["mat_fire_stone"] = 3
    state_hc2["inventory"]["mat_lava_shard"] = 2
    # Equip the warm stone instead of keeping it in inventory
    game.add_item(state_hc2, "acc_warm_stone", 1)
    game.equip_item(state_hc2, first_inventory_equipment_ref(state_hc2, "acc_warm_stone"), quiet=True)

    print(f"[Happy Path - heat charm (equipped)] Initial Gold: {state_hc2['gold']}, Equipment: {state_hc2['equipment']}, Inventory: {dict(state_hc2['inventory'])}")
    response = session_hc2.dispatch("craft_recipe", {"recipe_id": "recipe_heat_charm"}, screen_id="synthesis_screen")
    assert response["ok"] is True
    assert state_hc2["gold"] == 240  # 500 - 260 = 240G
    assert state_hc2["inventory"]["mat_fire_stone"] == 1  # 3 - 2 = 1
    assert state_hc2["inventory"]["mat_lava_shard"] == 1  # 2 - 1 = 1
    assert state_hc2["equipment"].get("accessory") is None  # consumed from equipment slot
    assert equipment_base_id(state_hc2, first_inventory_equipment_ref(state_hc2, "acc_warm_stone_plus")) == "acc_warm_stone_plus"
    print("Happy Path (heat charm, base item equipped) verified.")

    # ----------------------------------------------------
    # 6. Blocked Path: Locked recipe
    # ----------------------------------------------------
    session_locked = GuiRuntimeSession()
    session_locked.new_game(name="測試合成家", job_id="rogue")
    state_locked = session_locked.require_state()
    # recipe_fire_cloak is NOT unlocked
    state_locked["gold"] = 500
    state_locked["inventory"]["mat_fire_stone"] = 5
    state_locked["inventory"]["mat_scorched_iron"] = 3

    try:
        session_locked.dispatch("craft_recipe", {"recipe_id": "recipe_fire_cloak"}, screen_id="synthesis_screen")
        raise AssertionError("Expected craft of locked recipe to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 403
        assert "完成公會任務「焦石偵查」" in err.blocked_reason
        assert "recipe_" not in err.blocked_reason and "unlock_" not in err.blocked_reason
        print("Blocked Path (Locked recipe) verified.")

    # ----------------------------------------------------
    # 7. Blocked Path: Low gold
    # ----------------------------------------------------
    session_gold = GuiRuntimeSession()
    session_gold.new_game(name="測試合成家", job_id="rogue")
    state_gold = session_gold.require_state()
    game.unlock(state_gold, "recipe_fire_cloak")
    state_gold["gold"] = 100  # needs 300G
    state_gold["inventory"]["mat_fire_stone"] = 5
    state_gold["inventory"]["mat_scorched_iron"] = 3

    try:
        session_gold.dispatch("craft_recipe", {"recipe_id": "recipe_fire_cloak"}, screen_id="synthesis_screen")
        raise AssertionError("Expected craft with low gold to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "金幣不足。"
        print("Blocked Path (Low gold) verified.")

    # ----------------------------------------------------
    # 8. Blocked Path: Missing materials
    # ----------------------------------------------------
    session_mats = GuiRuntimeSession()
    session_mats.new_game(name="測試合成家", job_id="rogue")
    state_mats = session_mats.require_state()
    game.unlock(state_mats, "recipe_fire_cloak")
    state_mats["gold"] = 500
    state_mats["inventory"]["mat_fire_stone"] = 1  # needs 3
    state_mats["inventory"]["mat_scorched_iron"] = 3

    try:
        session_mats.dispatch("craft_recipe", {"recipe_id": "recipe_fire_cloak"}, screen_id="synthesis_screen")
        raise AssertionError("Expected craft with missing materials to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "素材不足：火焰石缺 2（持有 1/需求 3）。"
        print("Blocked Path (Missing materials) verified.")

    # ----------------------------------------------------
    # 9. Blocked Path: Missing base item
    # ----------------------------------------------------
    session_base = GuiRuntimeSession()
    session_base.new_game(name="測試合成家", job_id="rogue")
    state_base = session_base.require_state()
    game.unlock(state_base, "recipe_heat_charm")
    state_base["gold"] = 500
    state_base["inventory"]["mat_fire_stone"] = 3
    state_base["inventory"]["mat_lava_shard"] = 2
    # No acc_warm_stone in inventory or equipment

    try:
        session_base.dispatch("craft_recipe", {"recipe_id": "recipe_heat_charm"}, screen_id="synthesis_screen")
        raise AssertionError("Expected craft with missing base item to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert "需要 暖石墜。" in err.blocked_reason
        print("Blocked Path (Missing base item) verified.")

    # ----------------------------------------------------
    # 10. Blocked Path: Workshop recipe sent to the synthesis action
    # ----------------------------------------------------
    session_non_white = GuiRuntimeSession()
    session_non_white.new_game(name="測試合成家", job_id="rogue")
    state_non_white = session_non_white.require_state()
    game.unlock(state_non_white, "recipe_iron_sword_plus_1")
    state_non_white["gold"] = 500
    state_non_white["inventory"]["mat_cracked_stone"] = 10
    state_non_white["inventory"]["mat_scorched_iron"] = 10
    game.add_item(state_non_white, "weapon_iron_sword", 1)

    try:
        session_non_white.dispatch("craft_recipe", {"recipe_id": "recipe_iron_sword_plus_1"}, screen_id="synthesis_screen")
        raise AssertionError("Expected workshop recipe on synthesis action to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert "工坊" in err.blocked_reason
        assert "白名單" not in str(err)
        print("Blocked Path (Wrong facility recipe) verified.")

    # ----------------------------------------------------
    # 11. Verify Synthesis Screen Model
    # ----------------------------------------------------
    session_model = GuiRuntimeSession()
    session_model.new_game(name="測試合成家", job_id="rogue")
    state_model = session_model.require_state()
    state_model["completed_quests"].append("quest_ash_ravine_scout")

    model = session_model.screen_model("synthesis_screen")
    assert model["screen_id"] == "facility_synthesis_screen"
    assert len(model["recipe_rows"]) == 7

    # Check category counts
    category_tabs = model["category_tabs"]
    assert any(tab["id"] == "all" and tab["count"] == 7 for tab in category_tabs)
    assert any(tab["id"] == "equipment" and tab["count"] == 3 for tab in category_tabs)
    assert any(tab["id"] == "battle" and tab["count"] == 4 for tab in category_tabs)

    # Check that locks and unlocks are correctly set
    rows = model["recipe_rows"]
    piercing_row = next(r for r in rows if r["recipe_id"] == "recipe_piercing_bundle")
    fire_cloak_row = next(r for r in rows if r["recipe_id"] == "recipe_fire_cloak")

    assert piercing_row["status_label"] != "尚未解鎖"  # because unlocked in session
    assert fire_cloak_row["status"] == "missing"  # because locked
    assert fire_cloak_row["status_label"] == "尚未解鎖"
    assert "完成公會任務「焦石偵查」" in fire_cloak_row["disabled_reason"]
    print("Synthesis Screen Model verified.")

    print("\nSynthesis bridge smoke test successfully completed all checks!")


if __name__ == "__main__":
    run_smoke_test()
