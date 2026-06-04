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


def run_smoke_test():
    print("Starting Synthesis Single Recipe Craft MVP bridge smoke test...")

    # 1. Happy Path: recipe_piercing_bundle is unlocked and player has enough gold/materials
    session = GuiRuntimeSession()
    session.new_game(name="測試合成家", job_id="rogue")
    state = session.require_state()

    # Unlock the recipe
    game.unlock(state, "recipe_piercing_bundle")
    
    # Give gold and materials
    state["gold"] = 200
    state["inventory"]["mat_scorched_iron"] = 3
    state["inventory"]["mat_cracked_stone"] = 4

    print(f"Initial State: gold={state['gold']}, inventory={dict(state['inventory'])}, unlocked={state.get('unlocked')}")

    # Perform crafting
    response = session.dispatch("craft_recipe", {"recipe_id": "recipe_piercing_bundle"}, screen_id="synthesis_screen")
    assert response["ok"] is True
    assert state["gold"] == 80  # 200 - 120 = 80G
    assert state["inventory"]["mat_scorched_iron"] == 1  # 3 - 2 = 1
    assert state["inventory"]["mat_cracked_stone"] == 1  # 4 - 3 = 1
    assert state["inventory"]["item_armor_piercer"] == 3  # outputs 3 items

    print("Happy Path verified: Gold deducted, materials paid, item crafted.")

    # 2. Blocked Path: Missing materials
    session2 = GuiRuntimeSession()
    session2.new_game(name="測試合成家", job_id="rogue")
    state2 = session2.require_state()
    game.unlock(state2, "recipe_piercing_bundle")
    state2["gold"] = 200
    state2["inventory"]["mat_scorched_iron"] = 1  # only 1 (needs 2)
    state2["inventory"]["mat_cracked_stone"] = 4

    try:
        session2.dispatch("craft_recipe", {"recipe_id": "recipe_piercing_bundle"}, screen_id="synthesis_screen")
        raise AssertionError("Expected crafting with missing materials to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "素材不足。"
        print("Blocked Path (Missing materials) verified.")

    # 3. Blocked Path: Locked recipe (recipe is not unlocked in state["unlocked"])
    session3 = GuiRuntimeSession()
    session3.new_game(name="測試合成家", job_id="rogue")
    state3 = session3.require_state()
    # recipe_piercing_bundle is NOT unlocked here
    state3["gold"] = 200
    state3["inventory"]["mat_scorched_iron"] = 3
    state3["inventory"]["mat_cracked_stone"] = 4

    try:
        session3.dispatch("craft_recipe", {"recipe_id": "recipe_piercing_bundle"}, screen_id="synthesis_screen")
        raise AssertionError("Expected locked recipe to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 403
        assert err.blocked_reason == "配方尚未解鎖。"
        print("Blocked Path (Locked recipe) verified.")

    # 4. Blocked Path: Non-whitelisted recipe
    session4 = GuiRuntimeSession()
    session4.new_game(name="測試合成家", job_id="rogue")
    state4 = session4.require_state()
    game.unlock(state4, "recipe_fire_cloak")
    state4["gold"] = 500
    state4["inventory"]["mat_fire_stone"] = 5
    state4["inventory"]["mat_scorched_iron"] = 5

    try:
        session4.dispatch("craft_recipe", {"recipe_id": "recipe_fire_cloak"}, screen_id="synthesis_screen")
        raise AssertionError("Expected non-whitelisted recipe to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 403
        assert "非白名單配方。" in str(err)
        print("Blocked Path (Non-whitelisted recipe) verified.")

    print("Synthesis bridge smoke test ok")


if __name__ == "__main__":
    run_smoke_test()
