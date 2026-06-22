from __future__ import annotations

from typing import Any


REGIONS = {
    "border_fire": {
        "name": "Border / Fire Route",
        "town_name": "邊境城鎮艾爾姆",
        "unlock_key": None,
        "dungeon_ids": [
            "dungeon_moss_cave",
            "dungeon_scorched_mine",
            "dungeon_ash_ravine",
            "dungeon_cinder_seal_depths",
        ],
        "quest_ids": [
            "quest_register",
            "quest_cave_gathering",
            "quest_magic_crystal",
            "quest_mine_scout",
            "quest_boss_glen",
            "quest_ash_ravine_scout",
            "quest_supply_upgrade",
            "quest_cinder_depths_scout",
        ],
    },
    "ice": {
        "name": "Ice Region",
        "town_name": "霜潮港",
        "unlock_key": "unlock_ice_region",
        "dungeon_ids": [
            "dungeon_ice_minor_a",
            "dungeon_ice_minor_b",
            "dungeon_ice_main_phase_1",
            "dungeon_ice_main_phase_2",
        ],
        "quest_ids": [
            "quest_ice_minor_a",
            "quest_ice_minor_b",
            "quest_ice_main_phase_1",
            "quest_ice_main_phase_2",
            "quest_ice_return_handoff",
        ],
    },
    "earth": {
        "name": "Earth Region",
        "town_name": "根環營地",
        "unlock_key": "unlock_earth_region_preview",
        "dungeon_ids": [
            "dungeon_earth_minor_a",
            "dungeon_earth_minor_b",
            "dungeon_earth_main_phase_1",
            "dungeon_earth_main_phase_2",
        ],
        "quest_ids": [
            "quest_earth_minor_a",
            "quest_earth_minor_b",
            "quest_earth_main_phase_1",
            "quest_earth_main_phase_2",
            "quest_earth_return_handoff",
        ],
    },
    "thunder": {
        "name": "Thunder Region",
        "town_name": "雷脊前哨",
        "unlock_key": "unlock_thunder_region_preview",
        "dungeon_ids": [
            "dungeon_thunder_minor_a",
            "dungeon_thunder_minor_b",
            "dungeon_thunder_main_phase_1",
            "dungeon_thunder_main_phase_2",
        ],
        "quest_ids": [
            "quest_thunder_minor_a",
            "quest_thunder_minor_b",
            "quest_thunder_main_phase_1",
            "quest_thunder_main_phase_2",
            "quest_thunder_return_handoff",
        ],
    },
    "final": {
        "name": "Final Region",
        "town_name": "魔王城前線",
        "unlock_key": "unlock_final_region_preview",
        "dungeon_ids": [
            "dungeon_final_minor_a",
            "dungeon_final_minor_b",
            "dungeon_final_main_phase_1",
            "dungeon_final_main_phase_2",
            "dungeon_final_main_phase_3",
        ],
        "quest_ids": [
            "quest_final_minor_a",
            "quest_final_minor_b",
            "quest_final_main_phase_1",
            "quest_final_main_phase_2",
            "quest_final_demon_king",
        ],
    },
}


def _is_unlocked(state: dict[str, Any], unlock_key: str | None) -> bool:
    if not unlock_key:
        return True
    return unlock_key in state.get("unlocked", []) or unlock_key in state.get("completed_quests", [])


def get_unlocked_regions(state: dict) -> list[str]:
    return [
        region_id
        for region_id, region in REGIONS.items()
        if _is_unlocked(state, region.get("unlock_key"))
    ]


def get_region_by_dungeon(dungeon_id: str) -> str:
    matches = [
        region_id
        for region_id, region in REGIONS.items()
        if dungeon_id in region.get("dungeon_ids", [])
    ]
    if len(matches) != 1:
        raise KeyError(f"Dungeon id must map to exactly one region: {dungeon_id}")
    return matches[0]


def get_region_by_quest(quest_id: str) -> str:
    matches = [
        region_id
        for region_id, region in REGIONS.items()
        if quest_id in region.get("quest_ids", [])
    ]
    if len(matches) != 1:
        raise KeyError(f"Quest id must map to exactly one region: {quest_id}")
    return matches[0]
