from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from engine.gui_actions import GuiRuntimeSession
from engine import game
from data import SHOP_INVENTORY, MAGIC_BOOKS, RECIPES


def run_visibility_test():
    print("Starting Regional Facility Visibility smoke test...")

    # Initialize a session and start new game (default region is border_fire)
    session = GuiRuntimeSession()
    session.new_game(name="測試旅人", job_id="mage")
    state = session.require_state()

    # Ensure Ice is NOT unlocked by default
    assert "unlock_ice_region" not in state["unlocked"]
    assert "unlock_ice_region" not in state["completed_quests"]

    # === 1. Verify in Border / Fire Region ===
    print("\n--- Verifying Border/Fire Region Visibility ---")
    session.current_region_id = "border_fire"

    # CLI Filters
    cli_travel_items = game.travel_shop_available_items(state, region_id="border_fire")
    cli_weapons = [w for w in SHOP_INVENTORY["weapon"] if game.EQUIPMENT[w].get("region", "border_fire") == "border_fire"]
    cli_armors = [a for a in SHOP_INVENTORY["armor"] if game.EQUIPMENT[a].get("region", "border_fire") == "border_fire"]
    cli_books = game.magic_shop_book_ids(region_id="border_fire")
    cli_recipes = [r_id for r_id, r in RECIPES.items() if r.get("region", "border_fire") == "border_fire" and (not r.get("base_item") or game.EQUIPMENT.get(list(r["output"].keys())[0], {}).get("slot") == "accessory") and game.recipe_available(state, r_id)]
    cli_upgrades = [r_id for r_id, r in RECIPES.items() if r.get("region", "border_fire") == "border_fire" and r.get("base_item") and game.EQUIPMENT.get(list(r["output"].keys())[0], {}).get("slot") != "accessory" and game.recipe_available(state, r_id)]

    # Verify CLI absolutely does NOT contain ice, earth, thunder, or final items
    for item_id in cli_travel_items:
        assert "_ice_" not in item_id and "_earth_" not in item_id and "_thunder_" not in item_id and "_final_" not in item_id
    for w_id in cli_weapons:
        assert "_ice_" not in w_id and "_earth_" not in w_id and "_thunder_" not in w_id and "_final_" not in w_id
    for a_id in cli_armors:
        assert "_ice_" not in a_id and "_earth_" not in a_id and "_thunder_" not in a_id and "_final_" not in a_id
    for b_id in cli_books:
        if b_id != "book_ice_needle":
            assert "_ice_" not in b_id
        assert "_earth_" not in b_id and "_thunder_" not in b_id and "_final_" not in b_id
    for r_id in cli_recipes:
        assert "_ice_" not in r_id and "_earth_" not in r_id and "_thunder_" not in r_id and "_final_" not in r_id
    for r_id in cli_upgrades:
        assert "_ice_" not in r_id and "_earth_" not in r_id and "_thunder_" not in r_id and "_final_" not in r_id

    print("CLI visibility in Border/Fire verified: No late-game elements visible.")

    # GUI Models
    gui_shop = session.screen_model("shop_screen")
    gui_magic = session.screen_model("magic_shop_screen")
    gui_synth = session.screen_model("synthesis_screen")
    gui_work = session.screen_model("workshop_screen")

    # Verify GUI matches CLI
    gui_travel_ids = [row["item_id"] for row in gui_shop["list_rows"] if game.is_shop_item_available(state, row["item_id"])]
    assert set(gui_travel_ids) == set(cli_travel_items)

    gui_book_ids = [row["book_id"] for row in gui_magic["list_rows"]]
    assert set(gui_book_ids) == set(cli_books)

    gui_recipe_ids = [row["recipe_id"] for row in gui_synth["recipe_rows"] if game.recipe_available(state, row["recipe_id"])]
    assert set(gui_recipe_ids) == set(cli_recipes)

    gui_weapon_ids = [w["id"] for w in gui_work["weapons"]]
    assert set(gui_weapon_ids) == set(cli_weapons)

    gui_armor_ids = [a["id"] for a in gui_work["armors"]]
    assert set(gui_armor_ids) == set(cli_armors)

    gui_upgrade_ids = [r["id"] for r in gui_work["upgrades"] if game.recipe_available(state, r["id"])]
    assert set(gui_upgrade_ids) == set(cli_upgrades)

    print("GUI Model visibility in Border/Fire matches CLI completely.")

    # === 2. Simulate Ice Region Unlock and switch region ===
    print("\n--- Verifying Ice Region Visibility (After unlock) ---")
    game.unlock(state, "unlock_ice_region")
    session.current_region_id = "ice"

    # CLI Filters
    cli_ice_travel = game.travel_shop_available_items(state, region_id="ice")
    cli_ice_weapons = [w for w in SHOP_INVENTORY["weapon"] if game.EQUIPMENT[w].get("region", "border_fire") == "ice"]
    cli_ice_armors = [a for a in SHOP_INVENTORY["armor"] if game.EQUIPMENT[a].get("region", "border_fire") == "ice"]
    cli_ice_books = game.magic_shop_book_ids(region_id="ice")
    cli_ice_recipes = [r_id for r_id, r in RECIPES.items() if r.get("region", "border_fire") == "ice" and (not r.get("base_item") or game.EQUIPMENT.get(list(r["output"].keys())[0], {}).get("slot") == "accessory") and game.recipe_available(state, r_id)]
    cli_ice_upgrades = [r_id for r_id, r in RECIPES.items() if r.get("region", "border_fire") == "ice" and r.get("base_item") and game.EQUIPMENT.get(list(r["output"].keys())[0], {}).get("slot") != "accessory" and game.recipe_available(state, r_id)]

    # Ensure Ice items exist
    assert len(cli_ice_travel) > 0
    assert len(cli_ice_weapons) > 0
    assert len(cli_ice_armors) > 0
    assert len(cli_ice_books) > 0
    assert len(cli_ice_recipes) > 0
    assert len(cli_ice_upgrades) > 0

    # Verify only Ice items show up, no Earth / Thunder / Final leak, and no Border/Fire items leak into Ice Shop
    for item_id in cli_ice_travel:
        assert "_ice_" in item_id
        assert "_earth_" not in item_id and "_thunder_" not in item_id and "_final_" not in item_id
    for w_id in cli_ice_weapons:
        assert "_ice_" in w_id
        assert "_earth_" not in w_id and "_thunder_" not in w_id and "_final_" not in w_id
    for a_id in cli_ice_armors:
        assert "_ice_" in a_id
        assert "_earth_" not in a_id and "_thunder_" not in a_id and "_final_" not in a_id
    for b_id in cli_ice_books:
        assert "_ice_" in b_id
        assert "_earth_" not in b_id and "_thunder_" not in b_id and "_final_" not in b_id
    for r_id in cli_ice_recipes:
        assert "_ice_" in r_id
        assert "_earth_" not in r_id and "_thunder_" not in r_id and "_final_" not in r_id
    for r_id in cli_ice_upgrades:
        assert "_ice_" in r_id
        assert "_earth_" not in r_id and "_thunder_" not in r_id and "_final_" not in r_id

    print("CLI visibility in Ice verified: Only Ice elements visible, no late-game or Border/Fire leak.")

    # GUI Models
    gui_ice_shop = session.screen_model("shop_screen")
    gui_ice_magic = session.screen_model("magic_shop_screen")
    gui_ice_synth = session.screen_model("synthesis_screen")
    gui_ice_work = session.screen_model("workshop_screen")

    gui_ice_travel_ids = [row["item_id"] for row in gui_ice_shop["list_rows"] if game.is_shop_item_available(state, row["item_id"])]
    assert set(gui_ice_travel_ids) == set(cli_ice_travel)

    gui_ice_book_ids = [row["book_id"] for row in gui_ice_magic["list_rows"]]
    assert set(gui_ice_book_ids) == set(cli_ice_books)

    gui_ice_recipe_ids = [row["recipe_id"] for row in gui_ice_synth["recipe_rows"] if game.recipe_available(state, row["recipe_id"])]
    assert set(gui_ice_recipe_ids) == set(cli_ice_recipes)

    gui_ice_weapon_ids = [w["id"] for w in gui_ice_work["weapons"]]
    assert set(gui_ice_weapon_ids) == set(cli_ice_weapons)

    gui_ice_armor_ids = [a["id"] for a in gui_ice_work["armors"]]
    assert set(gui_ice_armor_ids) == set(cli_ice_armors)

    gui_ice_upgrade_ids = [r["id"] for r in gui_ice_work["upgrades"] if game.recipe_available(state, r["id"])]
    assert set(gui_ice_upgrade_ids) == set(cli_ice_upgrades)

    print("GUI Model visibility in Ice matches CLI completely.")

    # === 3. Simulate Earth Region Unlock and switch region ===
    print("\n--- Verifying Earth Region Visibility (After unlock) ---")
    game.unlock(state, game.EARTH_REGION_UNLOCK)
    session.current_region_id = "earth"

    # CLI Filters
    cli_earth_travel = game.travel_shop_available_items(state, region_id="earth")
    cli_earth_weapons = [w for w in SHOP_INVENTORY["weapon"] if game.EQUIPMENT[w].get("region", "border_fire") == "earth"]
    cli_earth_armors = [a for a in SHOP_INVENTORY["armor"] if game.EQUIPMENT[a].get("region", "border_fire") == "earth"]
    cli_earth_books = game.magic_shop_book_ids(region_id="earth")
    cli_earth_recipes = [r_id for r_id, r in RECIPES.items() if r.get("region", "border_fire") == "earth" and (not r.get("base_item") or game.EQUIPMENT.get(list(r["output"].keys())[0], {}).get("slot") == "accessory") and game.recipe_available(state, r_id)]
    cli_earth_upgrades = [r_id for r_id, r in RECIPES.items() if r.get("region", "border_fire") == "earth" and r.get("base_item") and game.EQUIPMENT.get(list(r["output"].keys())[0], {}).get("slot") != "accessory" and game.recipe_available(state, r_id)]

    # Ensure Earth items exist
    assert len(cli_earth_travel) > 0
    assert len(cli_earth_weapons) > 0
    assert len(cli_earth_armors) > 0
    assert len(cli_earth_books) > 0
    assert len(cli_earth_recipes) > 0
    assert len(cli_earth_upgrades) > 0

    # Verify only Earth items show up
    for item_id in cli_earth_travel:
        assert "_earth_" in item_id
        assert "_ice_" not in item_id and "_thunder_" not in item_id and "_final_" not in item_id
    for w_id in cli_earth_weapons:
        assert "_earth_" in w_id
        assert "_ice_" not in w_id and "_thunder_" not in w_id and "_final_" not in w_id
    for a_id in cli_earth_armors:
        assert "_earth_" in a_id
        assert "_ice_" not in a_id and "_thunder_" not in a_id and "_final_" not in a_id
    for b_id in cli_earth_books:
        assert "_earth_" in b_id
        assert "_ice_" not in b_id and "_thunder_" not in b_id and "_final_" not in b_id
    for r_id in cli_earth_recipes:
        assert "_earth_" in r_id
        assert "_ice_" not in r_id and "_thunder_" not in r_id and "_final_" not in r_id
    for r_id in cli_earth_upgrades:
        assert "_earth_" in r_id
        assert "_ice_" not in r_id and "_thunder_" not in r_id and "_final_" not in r_id

    print("CLI visibility in Earth verified: Only Earth elements visible, no other region leak.")

    # GUI Models
    gui_earth_shop = session.screen_model("shop_screen")
    gui_earth_magic = session.screen_model("magic_shop_screen")
    gui_earth_synth = session.screen_model("synthesis_screen")
    gui_earth_work = session.screen_model("workshop_screen")

    gui_earth_travel_ids = [row["item_id"] for row in gui_earth_shop["list_rows"] if game.is_shop_item_available(state, row["item_id"])]
    assert set(gui_earth_travel_ids) == set(cli_earth_travel)

    gui_earth_book_ids = [row["book_id"] for row in gui_earth_magic["list_rows"]]
    assert set(gui_earth_book_ids) == set(cli_earth_books)

    gui_earth_recipe_ids = [row["recipe_id"] for row in gui_earth_synth["recipe_rows"] if game.recipe_available(state, row["recipe_id"])]
    assert set(gui_earth_recipe_ids) == set(cli_earth_recipes)

    gui_earth_weapon_ids = [w["id"] for w in gui_earth_work["weapons"]]
    assert set(gui_earth_weapon_ids) == set(cli_earth_weapons)

    gui_earth_armor_ids = [a["id"] for a in gui_earth_work["armors"]]
    assert set(gui_earth_armor_ids) == set(cli_earth_armors)

    gui_earth_upgrade_ids = [r["id"] for r in gui_earth_work["upgrades"] if game.recipe_available(state, r["id"])]
    assert set(gui_earth_upgrade_ids) == set(cli_earth_upgrades)

    print("GUI Model visibility in Earth matches CLI completely.")
    print("\nRegional Facility Visibility smoke test successfully completed all checks!")


if __name__ == "__main__":
    run_visibility_test()
