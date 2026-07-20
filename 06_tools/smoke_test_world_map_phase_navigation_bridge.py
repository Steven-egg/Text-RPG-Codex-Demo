from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from engine import game  # noqa: E402
from engine.gui_actions import GuiRuntimeSession  # noqa: E402
from engine.gui_world_map_model import REGION_DUNGEON_LAYOUTS, main_dungeon_model  # noqa: E402


def main_dungeon_location(model: dict, node_id: str) -> dict:
    return next(location for location in model["locations"] if location["location_id"] == node_id)


def run_smoke_test() -> None:
    print("Starting World Map main-dungeon phase bridge smoke test...")
    session = GuiRuntimeSession()
    session.load_demo_seed()
    state = session.require_state()
    game.unlock(state, "unlock_earth_region_preview")
    game.unlock(state, "dungeon_earth_main_phase_1")
    game.unlock(state, "dungeon_earth_main_phase_2")

    session.set_current_region("earth")
    earth_world = session.screen_model("world_map")
    earth_main = main_dungeon_location(earth_world, "dungeon_earth_main")
    contract = earth_main["main_dungeon"]

    assert contract["group_id"] == "dungeon_earth_main"
    assert contract["current_phase_index"] == 2
    assert [phase["dungeon_id"] for phase in contract["phases"]] == [
        "dungeon_earth_main_phase_1",
        "dungeon_earth_main_phase_2",
    ]

    phase_1, phase_2 = contract["phases"]
    assert phase_1["label"] == "外城遺構"
    assert phase_2["label"] == "深脈殿"
    assert phase_1["unlocked"] is True and phase_1["replayable"] is True
    assert phase_2["unlocked"] is True
    assert phase_1["primary_action"]["payload"]["dungeon_id"] == "dungeon_earth_main_phase_1"
    assert phase_2["primary_action"]["payload"]["dungeon_id"] == "dungeon_earth_main_phase_2"
    print(" - Earth returns a data-driven two-phase contract with phase 2 active.")

    response = session.dispatch("confirm_travel", phase_1["primary_action"]["payload"], screen_id="world_map")
    assert response["action_id"] == "confirm_travel"
    assert session.exploration is not None
    assert session.exploration["dungeon_id"] == "dungeon_earth_main_phase_1"
    print(" - The phase 1 action re-enters the existing runtime dungeon without a new action type.")

    empty_supplies = {
        "sustain_hp": {"item_id": None, "quantity": 0},
        "emergency_hp": {"item_id": None, "quantity": 0},
        "mp": {"item_id": None, "quantity": 0},
        "throwable": {"item_id": None, "quantity": 0},
    }
    assert game.configure_run_supplies(state, empty_supplies) == empty_supplies
    print(" - An empty four-slot supply configuration remains a valid expedition payload.")

    for region_id in ("ice", "earth", "thunder", "final"):
        slot = next(candidate for candidate in REGION_DUNGEON_LAYOUTS[region_id] if candidate.get("main_dungeon"))
        for dungeon_id in slot["dungeon_ids"]:
            game.unlock(state, dungeon_id)
        generic_contract = main_dungeon_model(state, slot, region_id)
        assert generic_contract is not None
        assert generic_contract["current_phase_index"] == len(slot["dungeon_ids"])
        assert len(generic_contract["phases"]) == len(slot["dungeon_ids"])
    print(" - The same contract covers Ice, Earth, Thunder, and three-phase Final without region-specific UI logic.")

    session.set_current_region("border_fire")
    fire_world = session.screen_model("world_map")
    assert all(location.get("main_dungeon") is None for location in fire_world["locations"])
    print(" - Ordinary dungeon nodes do not receive Main Dungeon phase controls.")
    print("World Map main-dungeon phase bridge smoke test passed.")


if __name__ == "__main__":
    run_smoke_test()
