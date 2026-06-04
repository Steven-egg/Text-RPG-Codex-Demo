from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from engine.gui_actions import GuiRuntimeSession, GuiActionError


def run_smoke_test():
    print("Starting Workshop Buy Weapon Live MVP bridge smoke test...")

    # 1. Happy Path: Warrior with enough Gold buys weapon_wood_sword
    session = GuiRuntimeSession()
    session.new_game(name="鐵刃勇士", job_id="warrior")
    state = session.require_state()

    state["gold"] = 100
    print(f"Initial State: job={state['job']}, gold={state['gold']}, inventory={dict(state['inventory'])}, equipment={state['equipment']}")

    response = session.dispatch("buy_equipment", {"item_id": "weapon_wood_sword"}, screen_id="workshop_screen")
    assert response["ok"] is True
    assert state["gold"] == 20  # 100 - 80 = 20G
    assert state["inventory"]["weapon_wood_sword"] == 1
    # Confirm equipped weapon has NOT changed (was special_trial_badge or None, not wood sword)
    assert state["equipment"].get("weapon") != "weapon_wood_sword"

    print("Happy Path verified: Gold deducted, inventory +1, equipment unchanged.")

    # 2. Blocked Path: Low Gold
    try:
        session.dispatch("buy_equipment", {"item_id": "weapon_iron_sword"}, screen_id="workshop_screen")
        raise AssertionError("Expected low Gold purchase to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "金幣不足"
        print("Blocked Path (Low Gold) verified.")

    # 3. Blocked Path: Job mismatch (Mage trying to buy sword)
    session2 = GuiRuntimeSession()
    session2.new_game(name="元素法師", job_id="mage")
    state2 = session2.require_state()
    state2["gold"] = 500

    try:
        session2.dispatch("buy_equipment", {"item_id": "weapon_iron_sword"}, screen_id="workshop_screen")
        raise AssertionError("Expected job mismatch to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "職業不合"
        print("Blocked Path (Job mismatch) verified.")

    # 4. Blocked Path: Invalid item (not sold in workshop)
    try:
        session.dispatch("buy_equipment", {"item_id": "item_potion_s"}, screen_id="workshop_screen")
        raise AssertionError("Expected non-workshop purchase to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 400
        print("Blocked Path (Non-workshop item) verified.")

    # 4.1 Happy Path: Buy Armor (armor_round_shield)
    state["gold"] = 200
    response_armor = session.dispatch("buy_equipment", {"item_id": "armor_round_shield"}, screen_id="workshop_screen")
    assert response_armor["ok"] is True
    assert state["gold"] == 20  # 200 - 180 = 20G
    assert state["inventory"]["armor_round_shield"] == 1
    print("Happy Path verified: Purchased armor (shield) successfully.")

    # 5. Happy Path: Equip wood sword
    # Warrior currently has weapon_wood_sword x1 in inventory, none equipped
    response = session.dispatch("equip_weapon", {"item_id": "weapon_wood_sword"}, screen_id="workshop_screen")
    assert response["ok"] is True
    assert state["equipment"]["weapon"] == "weapon_wood_sword"
    assert state["inventory"].get("weapon_wood_sword", 0) == 0
    print("Equip Weapon verified: weapon equipped, inventory count decreased.")

    # 6. Swap Weapon: Buy & equip iron sword, check old wood sword returns to inventory
    state["gold"] = 500
    session.dispatch("buy_equipment", {"item_id": "weapon_iron_sword"}, screen_id="workshop_screen")
    assert state["inventory"].get("weapon_iron_sword", 0) == 1

    response = session.dispatch("equip_weapon", {"item_id": "weapon_iron_sword"}, screen_id="workshop_screen")
    assert response["ok"] is True
    assert state["equipment"]["weapon"] == "weapon_iron_sword"
    assert state["inventory"].get("weapon_wood_sword", 0) == 1
    assert state["inventory"].get("weapon_iron_sword", 0) == 0
    print("Swap Weapon verified: new weapon equipped, old weapon returned to inventory.")

    # 7. Blocked Path: Equip missing weapon
    try:
        session.dispatch("equip_weapon", {"item_id": "weapon_iron_sword_plus_1"}, screen_id="workshop_screen")
        raise AssertionError("Expected missing weapon equip to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "背包中無此武器"
        print("Blocked Path (Missing weapon) verified.")

    # 8. Blocked Path: Equip job-mismatched weapon
    # Manually add Mage wand to inventory
    from engine import game
    game.add_item(state, "weapon_apprentice_wand", 1)
    try:
        session.dispatch("equip_weapon", {"item_id": "weapon_apprentice_wand"}, screen_id="workshop_screen")
        raise AssertionError("Expected job-mismatched weapon equip to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "職業不符"
        print("Blocked Path (Job mismatch weapon) verified.")

    # 9. Blocked Path: Equip non-weapon slot item
    # Manually add shield to inventory
    game.add_item(state, "armor_round_shield", 1)
    try:
        session.dispatch("equip_weapon", {"item_id": "armor_round_shield"}, screen_id="workshop_screen")
        raise AssertionError("Expected non-weapon equip to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 400
        print("Blocked Path (Non-weapon slot) verified.")

    # 10. Blocked Path: Equip already equipped weapon
    try:
        session.dispatch("equip_weapon", {"item_id": "weapon_iron_sword"}, screen_id="workshop_screen")
        raise AssertionError("Expected already equipped weapon to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "已裝備此武器"
        print("Blocked Path (Already equipped weapon) verified.")

    # 11. Happy Path: Equip body armor (equip_equipment)
    # Give Warrior armor_leather_armor
    game.add_item(state, "armor_leather_armor", 1)
    assert state["inventory"].get("armor_leather_armor", 0) == 1
    response = session.dispatch("equip_equipment", {"item_id": "armor_leather_armor"}, screen_id="workshop_screen")
    assert response["ok"] is True
    assert state["equipment"]["body"] == "armor_leather_armor"
    assert state["inventory"].get("armor_leather_armor", 0) == 0
    print("Equip Armor verified: armor equipped, inventory count decreased.")

    # 12. Swap Armor: Equip traveler cloth, check old leather armor returns to inventory
    game.add_item(state, "armor_traveler_cloth", 1)
    response = session.dispatch("equip_equipment", {"item_id": "armor_traveler_cloth"}, screen_id="workshop_screen")
    assert response["ok"] is True
    assert state["equipment"]["body"] == "armor_traveler_cloth"
    assert state["inventory"].get("armor_leather_armor", 0) == 1
    assert state["inventory"].get("armor_traveler_cloth", 0) == 0
    print("Swap Armor verified: new armor equipped, old armor returned to inventory.")

    # 13. Blocked Path: Equip job-mismatched armor
    game.add_item(state, "armor_rogue_sleeve_blade", 1)
    try:
        session.dispatch("equip_equipment", {"item_id": "armor_rogue_sleeve_blade"}, screen_id="workshop_screen")
        raise AssertionError("Expected job-mismatched armor equip to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "職業不符"
        print("Blocked Path (Job mismatch armor) verified.")

    # 14. Blocked Path: Equip missing armor
    try:
        session.dispatch("equip_equipment", {"item_id": "armor_leather_cap"}, screen_id="workshop_screen")
        raise AssertionError("Expected missing armor equip to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "背包中無此裝備"
        print("Blocked Path (Missing armor) verified.")

    # 15. Blocked Path: Equip already equipped armor
    try:
        session.dispatch("equip_equipment", {"item_id": "armor_traveler_cloth"}, screen_id="workshop_screen")
        raise AssertionError("Expected already equipped armor to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "已裝備此裝備"
        print("Blocked Path (Already equipped armor) verified.")

    # 16. Blocked Path: Upgrade recipe not unlocked
    try:
        session.dispatch("upgrade_equipment", {"recipe_id": "recipe_iron_sword_plus_1"}, screen_id="workshop_screen")
        raise AssertionError("Expected locked recipe upgrade to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "配方未解鎖"
        print("Blocked Path (Locked recipe upgrade) verified.")

    # 17. Blocked Path: Non-whitelisted recipe upgrade
    try:
        session.dispatch("upgrade_equipment", {"recipe_id": "recipe_fire_cloak"}, screen_id="workshop_screen")
        raise AssertionError("Expected non-whitelisted recipe upgrade to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 400
        print("Blocked Path (Non-whitelisted recipe upgrade) verified.")

    # 18. Blocked Path: Recipe upgrade low gold
    # Unlock recipe first
    state["completed_quests"].append("quest_cave_gathering")
    state["gold"] = 10
    # Add materials for iron sword +1
    game.add_item(state, "mat_cracked_stone", 5)
    game.add_item(state, "mat_scorched_iron", 1)
    # Ensure iron sword is equipped
    assert state["equipment"]["weapon"] == "weapon_iron_sword"
    try:
        session.dispatch("upgrade_equipment", {"recipe_id": "recipe_iron_sword_plus_1"}, screen_id="workshop_screen")
        raise AssertionError("Expected low gold upgrade to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "金幣不足"
        print("Blocked Path (Low gold recipe upgrade) verified.")

    # 19. Blocked Path: Recipe upgrade low materials
    state["gold"] = 200
    # Consume one of the materials to make it insufficient
    state["inventory"]["mat_cracked_stone"] = 4
    try:
        session.dispatch("upgrade_equipment", {"recipe_id": "recipe_iron_sword_plus_1"}, screen_id="workshop_screen")
        raise AssertionError("Expected low materials upgrade to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "材料不足"
        print("Blocked Path (Low materials recipe upgrade) verified.")

    # 20. Blocked Path: Recipe upgrade missing base item
    # Restore materials
    state["inventory"]["mat_cracked_stone"] = 5
    # Unequip and remove weapon_iron_sword
    state["equipment"]["weapon"] = None
    state["inventory"]["weapon_iron_sword"] = 0
    try:
        session.dispatch("upgrade_equipment", {"recipe_id": "recipe_iron_sword_plus_1"}, screen_id="workshop_screen")
        raise AssertionError("Expected missing base item upgrade to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "缺少基底裝備"
        print("Blocked Path (Missing base item recipe upgrade) verified.")

    # 21. Happy Path: Recipe upgrade success
    # Give base weapon back to inventory
    game.add_item(state, "weapon_iron_sword", 1)
    # Ensure materials are exactly right
    state["inventory"]["mat_cracked_stone"] = 5
    state["inventory"]["mat_scorched_iron"] = 1
    state["gold"] = 200

    response = session.dispatch("upgrade_equipment", {"recipe_id": "recipe_iron_sword_plus_1"}, screen_id="workshop_screen")
    assert response["ok"] is True
    assert state["gold"] == 20  # 200 - 180 = 20G
    assert state["inventory"].get("weapon_iron_sword_plus_1", 0) == 1
    assert state["inventory"].get("weapon_iron_sword", 0) == 0
    assert state["inventory"].get("mat_cracked_stone", 0) == 0
    assert state["inventory"].get("mat_scorched_iron", 0) == 0
    print("Happy Path: Recipe upgrade verified successfully!")

    # 22. Happy Path: Armor Recipe upgrade success (recipe_leather_armor_plus_1)
    # Ensure base armor is exactly 1 in inventory
    state["inventory"]["armor_leather_armor"] = 1
    # Ensure materials are exactly right
    state["inventory"]["mat_moss_fiber"] = 4
    state["inventory"]["mat_cracked_stone"] = 3
    state["gold"] = 200

    response = session.dispatch("upgrade_equipment", {"recipe_id": "recipe_leather_armor_plus_1"}, screen_id="workshop_screen")
    assert response["ok"] is True
    assert state["gold"] == 40  # 200 - 160 = 40G
    assert state["inventory"].get("armor_leather_armor_plus_1", 0) == 1
    assert state["inventory"].get("armor_leather_armor", 0) == 0
    assert state["inventory"].get("mat_moss_fiber", 0) == 0
    assert state["inventory"].get("mat_cracked_stone", 0) == 0
    print("Happy Path: Armor recipe upgrade verified successfully!")

    print("Workshop bridge smoke test ok")


if __name__ == "__main__":
    run_smoke_test()
