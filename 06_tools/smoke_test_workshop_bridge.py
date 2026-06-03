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

    # 4. Blocked Path: Invalid item (not a weapon in SHOP_INVENTORY)
    try:
        session.dispatch("buy_equipment", {"item_id": "armor_round_shield"}, screen_id="workshop_screen")
        raise AssertionError("Expected non-weapon purchase to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 400
        print("Blocked Path (Non-weapon item) verified.")

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

    print("Workshop bridge smoke test ok")


if __name__ == "__main__":
    run_smoke_test()
