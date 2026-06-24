from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from engine import game  # noqa: E402
from engine.gui_actions import GuiActionError, GuiRuntimeSession  # noqa: E402


FIRE_DUNGEON_NODES = {
    "dungeon_moss_cave",
    "dungeon_scorched_mine",
    "dungeon_ash_ravine",
    "dungeon_cinder_seal_depths",
}
ICE_DUNGEON_NODES = {
    "dungeon_ice_minor_a",
    "dungeon_ice_minor_b",
    "dungeon_ice_main",
}
FUTURE_REGION_IDS = {"earth", "thunder", "final"}


def location_ids(model: dict) -> set[str]:
    return {location["location_id"] for location in model["locations"]}


def assert_only_region(model: dict, region_id: str) -> None:
    assert all(location.get("region_id") == region_id for location in model["locations"])


def run_smoke_test() -> None:
    print("Starting region routing bridge smoke test...")
    session = GuiRuntimeSession()
    session.load_demo_seed()
    state = session.require_state()

    fire_world = session.screen_model("world_map")
    fire_ids = location_ids(fire_world)
    assert fire_world["current_region_id"] == "border_fire"
    assert fire_world["map_asset"].endswith("world-map-environment-v01.jpg")
    assert fire_ids == {"border_town", *FIRE_DUNGEON_NODES, "region_gate_ice"}
    assert not any(location.get("region_id") in FUTURE_REGION_IDS for location in fire_world["locations"])
    assert_only_region(fire_world, "border_fire")

    gate = next(location for location in fire_world["locations"] if location["location_id"] == "region_gate_ice")
    gate_options = {option["region_id"]: option for option in gate["options"]}
    assert set(gate_options) == {"ice", "earth", "thunder", "final"}
    assert gate_options["ice"]["enabled"] is False
    assert all(gate_options[region_id]["enabled"] is False for region_id in FUTURE_REGION_IDS)
    print(" - fire map is scoped to fire town, four fire dungeons, and the region gate.")

    game.unlock(state, game.ICE_REGION_UNLOCK)
    unlocked_fire_world = session.screen_model("world_map")
    unlocked_gate = next(location for location in unlocked_fire_world["locations"] if location["location_id"] == "region_gate_ice")
    unlocked_options = {option["region_id"]: option for option in unlocked_gate["options"]}
    assert unlocked_options["ice"]["enabled"] is True
    assert all(unlocked_options[region_id]["enabled"] is False for region_id in FUTURE_REGION_IDS)

    ice_response = session.dispatch("travel_region", {"region_id": "ice"}, screen_id="world_map")
    ice_world = ice_response["screen_model"]
    ice_ids = location_ids(ice_world)
    assert ice_world["current_region_id"] == "ice"
    assert ice_world["map_asset"].endswith("ice-world-map-placeholder-candidate-v01.png")
    assert ice_ids == {"town_ice", *ICE_DUNGEON_NODES, "region_gate_border"}
    assert_only_region(ice_world, "ice")
    assert not (FIRE_DUNGEON_NODES & ice_ids)
    print(" - unlocked gate switches to the Ice map with three Ice dungeon nodes and region_gate_border.")

    ice_gate = next(location for location in ice_world["locations"] if location["location_id"] == "region_gate_border")
    ice_gate_options = {option["region_id"]: option for option in ice_gate["options"]}
    assert set(ice_gate_options) == {"border_fire", "earth", "thunder", "final"}
    assert ice_gate_options["border_fire"]["enabled"] is True

    for r_id in FUTURE_REGION_IDS:
        opt = ice_gate_options[r_id]
        assert opt["enabled"] is False
        assert opt["disabled_reason"] is not None
        assert "label" in opt
        assert "name" in opt
        assert opt["action_id"] == "travel_region"
    print(" - Ice region gate options contain border_fire (enabled) and future regions (disabled).")

    guild = session.screen_model("guild_screen")
    assert guild["current_region_id"] == "ice"
    assert [filter_row["id"] for filter_row in guild["task_filters"]] == ["all", "ice"]
    assert guild["task_rows"]
    assert all(row.get("region_id") == "ice" for row in guild["task_rows"])
    print(" - guild model is filtered to Ice tasks after region travel.")

    town = session.screen_model("town_hub")
    assert town["current_region_id"] == "ice"
    assert town["selected_region_id"] == "ice"
    assert town["town_asset"].endswith("ice-town-hub-placeholder-candidate-v01.png")
    print(" - town hub carries Ice region context and placeholder asset.")

    try:
        session.dispatch("travel_region", {"region_id": "earth"}, screen_id="world_map")
    except GuiActionError as exc:
        assert exc.status == 403
    else:
        raise AssertionError("Earth travel should remain locked in this slice.")
    print(" - future regions remain locked from the gate.")

    back_response = session.dispatch("travel_region", {"region_id": "border_fire"}, screen_id="world_map")
    back_world = back_response["screen_model"]
    assert back_world["current_region_id"] == "border_fire"
    print(" - successfully traveled from Ice back to Border / Fire.")

    print("All region routing bridge smoke tests passed successfully!")


if __name__ == "__main__":
    run_smoke_test()
