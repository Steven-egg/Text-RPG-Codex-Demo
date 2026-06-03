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

    print("Workshop bridge smoke test ok")


if __name__ == "__main__":
    run_smoke_test()
