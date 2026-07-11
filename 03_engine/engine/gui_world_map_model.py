from __future__ import annotations

from typing import Any
from data import (
    DUNGEONS,
    EQUIPMENT,
    ITEMS,
    JOBS,
    REGIONS,
    get_unlocked_regions,
)

from . import game
from .gui_presentation_helpers import player_model, boss_label

WORLD_MAP_PRESENTATION = {
    "dungeon_moss_cave": {
        "location_id": "moss_cave",
        "position": {"x": 24, "y": 48},
        "tone": "nature",
        "icon_token": "葉",
        "preview_role": "cave",
        "description": "潮濕陰暗的洞窟，布滿青苔與藤蔓，棲息著各種小型魔物。",
        "detail_note": "適合作為早期探索地點，live mode 會交由 Python runtime 驗證前往條件。",
        "exploration_rating": "低風險",
    },
    "dungeon_scorched_mine": {
        "location_id": "ember_quarry",
        "position": {"x": 49, "y": 42},
        "tone": "fire",
        "icon_token": "火",
        "preview_role": "quarry",
        "description": "黑色岩壁間冒著餘燼，舊礦道仍殘留火元素的熱度。",
        "detail_note": "推薦攜帶回復道具。live mode 會交由 Python runtime 驗證前往條件。",
        "exploration_rating": "中等風險",
    },
    "dungeon_ash_ravine": {
        "location_id": "ash_valley",
        "position": {"x": 48, "y": 67},
        "tone": "fire",
        "icon_token": "火",
        "preview_role": "valley",
        "description": "裂谷底部流動著暗紅熔脈，空氣裡混著鐵鏽與焦土味。",
        "detail_note": "比焦石礦坑更危險，適合裝備更新後挑戰。",
        "exploration_rating": "高風險",
    },
    "dungeon_cinder_seal_depths": {
        "location_id": "cinder_depths",
        "position": {"x": 64, "y": 82},
        "tone": "fire",
        "icon_token": "燼",
        "preview_role": "plateau",
        "description": "深處的岩層帶著燼印反光，火印線索在洞壁間若隱若現。",
        "detail_note": "目前由 runtime unlock 狀態決定是否可前往。",
        "exploration_rating": "高風險",
    },
    "dungeon_ice_minor_a": {
        "location_id": "ice_minor_a",
        "position": {"x": 67, "y": 18},
        "tone": "ice",
        "icon_token": "I",
        "preview_role": "wreck",
        "description": "Ice route minor dungeon A / playable skeleton.",
        "detail_note": "Ghost-Sail Wreck is a live runtime dungeon; names and art are placeholder.",
        "exploration_rating": "medium",
    },
    "dungeon_ice_minor_b": {
        "location_id": "ice_minor_b",
        "position": {"x": 76, "y": 28},
        "tone": "ice",
        "icon_token": "I",
        "preview_role": "cave",
        "description": "Ice route minor dungeon B / playable skeleton.",
        "detail_note": "Frostroot Cavern is a live runtime dungeon; names and art are placeholder.",
        "exploration_rating": "medium",
    },
    "dungeon_ice_main_phase_1": {
        "location_id": "ice_main_fortress",
        "position": {"x": 86, "y": 20},
        "tone": "ice",
        "icon_token": "I",
        "preview_role": "fortress",
        "description": "Frostiron Keep main dungeon / outer city phase.",
        "detail_note": "This is the same main dungeon location; phase 2 replaces it after Q3.",
        "exploration_rating": "high",
    },
    "dungeon_ice_main_phase_2": {
        "location_id": "ice_main_fortress",
        "position": {"x": 86, "y": 20},
        "tone": "ice",
        "icon_token": "I",
        "preview_role": "fortress",
        "description": "Frostiron Keep main dungeon / inner palace phase.",
        "detail_note": "This is the same main dungeon location; it is not a fourth Ice world-map location.",
        "exploration_rating": "high",
    },
}
WORLD_MAP_ROUTE_SEGMENTS = [
    {"id": "town_to_cave", "from": "border_town", "to": "moss_cave", "points": [[35, 22], [29, 34], [24, 48]]},
    {"id": "cave_to_quarry", "from": "moss_cave", "to": "ember_quarry", "points": [[24, 48], [37, 44], [49, 42]]},
    {"id": "quarry_to_valley", "from": "ember_quarry", "to": "ash_valley", "points": [[49, 42], [49, 55], [48, 67]]},
    {"id": "valley_to_depths", "from": "ash_valley", "to": "cinder_depths", "points": [[48, 67], [56, 77], [64, 82]]},
    {"id": "town_to_frost", "from": "border_town", "to": "frost_pass", "points": [[35, 22], [50, 15], [66, 18]]},
    {"id": "quarry_to_forest", "from": "ember_quarry", "to": "mist_forest", "points": [[49, 42], [62, 38], [75, 38]]},
    {"id": "forest_to_tower", "from": "mist_forest", "to": "moon_tower", "points": [[75, 38], [72, 49], [70, 57]]},
    {"id": "cave_to_ruins", "from": "moss_cave", "to": "drowned_ruins", "points": [[24, 48], [23, 64], [26, 78]]},
]
WORLD_MAP_PREVIEW_LOCATIONS = [
    {
        "location_id": "frost_pass",
        "label": "冰封峽谷",
        "description": "北方山脈被冰雪封住，峽谷入口覆著厚重霜霧。",
        "detail_note": "尚未解鎖。這裡只提供地圖瀏覽與 blocked action。",
        "position": {"x": 66, "y": 18},
        "tone": "ice",
        "icon_token": "冰",
        "locked_reason": "尚未取得北境通行線索",
        "attribute": "冰 / 山脈",
        "preview_role": "frost",
        "preview_image": "../dungeon_exploration/assets/ice-dungeon-explore-minor-a-candidate-v01.png",
    },
    {
        "location_id": "mist_forest",
        "label": "遺忘森林",
        "description": "林間常年飄著薄霧，路徑會在日落後改變方向。",
        "detail_note": "尚未解鎖。未來可接故事線索或公會委託。",
        "position": {"x": 75, "y": 38},
        "tone": "nature",
        "icon_token": "森",
        "locked_reason": "需要完成青苔洞窟後續調查",
        "attribute": "自然 / 幻霧",
        "preview_role": "forest",
        "preview_image": "../dungeon_exploration/assets/earth-dungeon-explore-minor-a-candidate-v01.png",
    },
    {
        "location_id": "moon_tower",
        "label": "影月塔",
        "description": "高塔矗立在灰白岩脊上，塔頂會在夜裡反射紫色月光。",
        "detail_note": "尚未解鎖。這裡只提供地圖瀏覽與 blocked action。",
        "position": {"x": 70, "y": 57},
        "tone": "arcane",
        "icon_token": "月",
        "locked_reason": "需要影月塔入口鑰印",
        "attribute": "秘法 / 月影",
        "preview_role": "tower",
        "preview_image": "../dungeon_exploration/assets/thunder-dungeon-explore-minor-a-candidate-v01.png",
    },
    {
        "location_id": "drowned_ruins",
        "label": "沉沒遺跡",
        "description": "海岸旁的古代遺跡半沉在潮水裡，退潮時才露出入口。",
        "detail_note": "尚未解鎖。可檢查低亮度地點和鎖定狀態。",
        "position": {"x": 26, "y": 78},
        "tone": "water",
        "icon_token": "潮",
        "locked_reason": "尚未取得潮汐時刻表",
        "attribute": "水 / 遺跡",
        "preview_role": "ruins",
        "preview_image": "../dungeon_exploration/assets/final-dungeon-explore-minor-a-candidate-v01.png",
    },
]

DUNGEON_PREVIEW_ASSETS = {
    # Border / Fire
    "dungeon_moss_cave": "../dungeon_exploration/assets/moss-cave-exploration-v01.png",
    "dungeon_scorched_mine": "../dungeon_exploration/assets/ember-quarry-exploration-v01.png",
    "dungeon_ash_ravine": "../dungeon_exploration/assets/ash-ravine-exploration-v01.png",
    "dungeon_cinder_seal_depths": "../dungeon_exploration/assets/cinder-seal-depths-exploration-v01.png",
    # Ice
    "dungeon_ice_minor_a": "../dungeon_exploration/assets/ice-dungeon-explore-minor-a-candidate-v01.png",
    "dungeon_ice_minor_b": "../dungeon_exploration/assets/ice-dungeon-explore-minor-b-candidate-v01.png",
    "dungeon_ice_main_phase_1": "../dungeon_exploration/assets/ice-dungeon-explore-main-phase-1-candidate-v01.png",
    "dungeon_ice_main_phase_2": "../dungeon_exploration/assets/ice-dungeon-explore-main-phase-2-candidate-v01.png",
    # Earth
    "dungeon_earth_minor_a": "../dungeon_exploration/assets/earth-dungeon-explore-minor-a-candidate-v01.png",
    "dungeon_earth_minor_b": "../dungeon_exploration/assets/earth-dungeon-explore-minor-b-candidate-v01.png",
    "dungeon_earth_main_phase_1": "../dungeon_exploration/assets/earth-dungeon-explore-main-phase-1-candidate-v01.png",
    "dungeon_earth_main_phase_2": "../dungeon_exploration/assets/earth-dungeon-explore-main-phase-2-candidate-v01.png",
    # Thunder
    "dungeon_thunder_minor_a": "../dungeon_exploration/assets/thunder-dungeon-explore-minor-a-candidate-v01.png",
    "dungeon_thunder_minor_b": "../dungeon_exploration/assets/thunder-dungeon-explore-minor-b-candidate-v01.png",
    "dungeon_thunder_main_phase_1": "../dungeon_exploration/assets/thunder-dungeon-explore-main-phase-1-candidate-v01.png",
    "dungeon_thunder_main_phase_2": "../dungeon_exploration/assets/thunder-dungeon-explore-main-phase-2-candidate-v01.png",
    # Final
    "dungeon_final_minor_a": "../dungeon_exploration/assets/final-dungeon-explore-minor-a-candidate-v01.png",
    "dungeon_final_minor_b": "../dungeon_exploration/assets/final-dungeon-explore-minor-b-candidate-v01.png",
    "dungeon_final_main_phase_1": "../dungeon_exploration/assets/final-dungeon-explore-main-phase-1-candidate-v01.png",
    "dungeon_final_main_phase_2": "../dungeon_exploration/assets/final-dungeon-explore-main-phase-2-candidate-v01.png",
    "dungeon_final_main_phase_3": "../dungeon_exploration/assets/final-dungeon-explore-final-boss-hall-candidate-v01.png",
}

REGION_ORDER = ["border_fire", "ice", "earth", "thunder", "final"]
REGION_LABELS = {
    "border_fire": "烈焰邊境",
    "ice": "寒冰區域",
    "earth": "大地區域",
    "thunder": "風雷區域",
    "final": "終焉之地",
}
REGION_TONES = {
    "border_fire": "fire",
    "ice": "ice",
    "earth": "nature",
    "thunder": "arcane",
    "final": "bone",
}
REGION_TOKENS = {
    "border_fire": "火",
    "ice": "冰",
    "earth": "地",
    "thunder": "雷",
    "final": "終",
}
REGION_X = {
    "border_fire": 12,
    "ice": 32,
    "earth": 52,
    "thunder": 72,
    "final": 88,
}
REGION_TOWN_Y = 16
DUNGEON_Y = [34, 46, 58, 70, 82]
REGION_ROUTE_ENABLED = {"border_fire", "ice", "earth", "thunder", "final"}
REGION_GATE_DESTINATIONS = ["ice", "earth", "thunder", "final"]
REGION_MAP_ASSETS = {
    "border_fire": "./assets/world-map-environment-v01.jpg",
    "ice": "./assets/ice-world-map-placeholder-candidate-v01.png",
    "earth": "./assets/earth-world-map-placeholder-candidate-v01.png",
    "thunder": "./assets/thunder-world-map-placeholder-candidate-v01.png",
    "final": "./assets/final-world-map-placeholder-candidate-v01.png",
}
REGION_TOWN_ASSETS = {
    "border_fire": "../town_hub/assets/town-hub-environment-v01.jpg",
    "ice": "../town_hub/assets/ice-town-hub-placeholder-candidate-v01.png",
    "earth": "../town_hub/assets/earth-town-hub-placeholder-candidate-v01.png",
    "thunder": "../town_hub/assets/thunder-town-hub-placeholder-candidate-v01.png",
    "final": "../town_hub/assets/final-town-hub-placeholder-candidate-v02.png",
}
REGION_TOWN_POSITIONS = {
    "border_fire": {"x": 35, "y": 22},
    "ice": {"x": 21, "y": 77},
    "earth": {"x": 41, "y": 48},
    "thunder": {"x": 18, "y": 55},
    "final": {"x": 18, "y": 58},
}
REGION_GATE_POSITIONS = {
    "border_fire": {"x": 82, "y": 78},
    "ice": {"x": 47, "y": 92},
    "earth": {"x": 47, "y": 92},
    "thunder": {"x": 52, "y": 88},
    "final": {"x": 48, "y": 90},
}
REGION_DUNGEON_LAYOUTS = {
    "border_fire": [
        {"node_id": "dungeon_moss_cave", "dungeon_ids": ["dungeon_moss_cave"], "position": {"x": 24, "y": 48}, "preview_role": "cave"},
        {"node_id": "dungeon_scorched_mine", "dungeon_ids": ["dungeon_scorched_mine"], "position": {"x": 49, "y": 42}, "preview_role": "quarry"},
        {"node_id": "dungeon_ash_ravine", "dungeon_ids": ["dungeon_ash_ravine"], "position": {"x": 48, "y": 67}, "preview_role": "valley"},
        {"node_id": "dungeon_cinder_seal_depths", "dungeon_ids": ["dungeon_cinder_seal_depths"], "position": {"x": 64, "y": 82}, "preview_role": "cinder"},
    ],
    "ice": [
        {"node_id": "dungeon_ice_minor_a", "dungeon_ids": ["dungeon_ice_minor_a"], "position": {"x": 28, "y": 39}, "preview_role": "wreck"},
        {"node_id": "dungeon_ice_minor_b", "dungeon_ids": ["dungeon_ice_minor_b"], "position": {"x": 64, "y": 73}, "preview_role": "cave"},
        {
            "node_id": "dungeon_ice_main",
            "dungeon_ids": ["dungeon_ice_main_phase_1", "dungeon_ice_main_phase_2"],
            "position": {"x": 77, "y": 33},
            "preview_role": "fortress",
            "label": "霜鐵古城",
            "main_dungeon": True,
        },
    ],
    "earth": [
        {"node_id": "dungeon_earth_minor_a", "dungeon_ids": ["dungeon_earth_minor_a"], "position": {"x": 28, "y": 38}, "preview_role": "forest"},
        {"node_id": "dungeon_earth_minor_b", "dungeon_ids": ["dungeon_earth_minor_b"], "position": {"x": 50, "y": 79}, "preview_role": "quarry"},
        {
            "node_id": "dungeon_earth_main",
            "dungeon_ids": ["dungeon_earth_main_phase_1", "dungeon_earth_main_phase_2"],
            "position": {"x": 76, "y": 34},
            "preview_role": "forest",
            "label": "地脈石城",
            "main_dungeon": True,
        },
    ],
    "thunder": [
        {"node_id": "dungeon_thunder_minor_a", "dungeon_ids": ["dungeon_thunder_minor_a"], "position": {"x": 28, "y": 38}, "preview_role": "tower"},
        {"node_id": "dungeon_thunder_minor_b", "dungeon_ids": ["dungeon_thunder_minor_b"], "position": {"x": 64, "y": 55}, "preview_role": "tower"},
        {
            "node_id": "dungeon_thunder_main",
            "dungeon_ids": ["dungeon_thunder_main_phase_1", "dungeon_thunder_main_phase_2"],
            "position": {"x": 58, "y": 28},
            "preview_role": "tower",
            "label": "雷霆陣列",
            "main_dungeon": True,
        },
    ],
    "final": [
        {"node_id": "dungeon_final_minor_a", "dungeon_ids": ["dungeon_final_minor_a"], "position": {"x": 38, "y": 20}, "preview_role": "ruins"},
        {"node_id": "dungeon_final_minor_b", "dungeon_ids": ["dungeon_final_minor_b"], "position": {"x": 51, "y": 55}, "preview_role": "ruins"},
        {
            "node_id": "dungeon_final_main",
            "dungeon_ids": ["dungeon_final_main_phase_1", "dungeon_final_main_phase_2", "dungeon_final_main_phase_3"],
            "position": {"x": 64, "y": 14},
            "preview_role": "fortress",
            "label": "魔王城",
            "main_dungeon": True,
        },
    ],
}


def region_town_location_id(region_id: str) -> str:
    return "border_town" if region_id == "border_fire" else f"town_{region_id}"


def region_route_status(unlocked_location_ids: set[str], *location_ids: str) -> str:
    return "open" if all(location_id in unlocked_location_ids for location_id in location_ids) else "locked"


def region_runtime_unlocked(state: dict[str, Any], region_id: str) -> bool:
    return region_id in set(get_unlocked_regions(state))


def region_route_enabled(state: dict[str, Any], region_id: str) -> bool:
    return region_id in REGION_ROUTE_ENABLED and region_runtime_unlocked(state, region_id)


def normalize_region_id(state: dict[str, Any], requested_region_id: str | None = None) -> str:
    if requested_region_id in REGION_ROUTE_ENABLED and region_route_enabled(state, str(requested_region_id)):
        return str(requested_region_id)
    return "border_fire"


def region_locked_reason(region_id: str) -> str:
    if region_id == "ice":
        return "寒冰區域將在烈焰之印路線完成後解鎖。"
    if region_id == "earth":
        return "大地區域將在完成寒冰區域任務後解鎖。"
    if region_id == "thunder":
        return "風雷區域將在完成大地區域任務後解鎖。"
    if region_id == "final":
        return "終焉之地需要供奉全部四顆元素印記。"
    return f"{REGION_LABELS.get(region_id, region_id)} 區域尚未解鎖。"


def region_options_model(state: dict[str, Any], selected_region_id: str | None = None) -> list[dict[str, Any]]:
    current_region_id = normalize_region_id(state, selected_region_id)
    options = []
    for region_id in REGION_ORDER:
        region = REGIONS[region_id]
        runtime_unlocked = region_runtime_unlocked(state, region_id)
        route_enabled = region_route_enabled(state, region_id)
        options.append(
            {
                "region_id": region_id,
                "label": REGION_LABELS[region_id],
                "name": region.get("name", REGION_LABELS[region_id]),
                "town_name": region.get("town_name", REGION_LABELS[region_id]),
                "unlocked": runtime_unlocked,
                "route_enabled": route_enabled,
                "current": region_id == current_region_id,
                "unlock_key": region.get("unlock_key"),
                "dungeon_count": len(region.get("dungeon_ids", [])),
                "quest_count": len(region.get("quest_ids", [])),
                "disabled_reason": None if route_enabled else region_locked_reason(region_id),
            }
        )
    return options


def default_region_id(state: dict[str, Any], requested_region_id: str | None = None) -> str:
    return normalize_region_id(state, requested_region_id)


def region_for_dungeon_id(dungeon_id: str) -> str:
    for region_id, region in REGIONS.items():
        if dungeon_id in region.get("dungeon_ids", []):
            return region_id
    return "border_fire"


def active_dungeon_id_for_slot(state: dict[str, Any], slot: dict[str, Any]) -> str:
    dungeon_ids = slot.get("dungeon_ids", [])
    for dungeon_id in reversed(dungeon_ids):
        dungeon = DUNGEONS[dungeon_id]
        if game.is_unlocked(state, dungeon.get("unlock")):
            return dungeon_id
    return dungeon_ids[0]


def main_dungeon_model(state: dict[str, Any], slot: dict[str, Any], region_id: str) -> dict[str, Any] | None:
    """Return the display/action contract for a multi-phase world-map node."""
    dungeon_ids = slot.get("dungeon_ids", [])
    if not slot.get("main_dungeon"):
        return None

    active_dungeon_id = active_dungeon_id_for_slot(state, slot)
    phases = []
    for phase_index, phase_dungeon_id in enumerate(dungeon_ids, start=1):
        phase_dungeon = DUNGEONS[phase_dungeon_id]
        phase_unlocked = game.is_unlocked(state, phase_dungeon.get("unlock"))
        locked_reason = None if phase_unlocked else "此迷宮階段因核心劇情進度尚未解鎖。"
        phases.append(
            {
                "phase_index": phase_index,
                "dungeon_id": phase_dungeon_id,
                "label": phase_dungeon["name"],
                "description": (
                    f"{REGION_LABELS[region_id]}主線迷宮 階段 {phase_index}：推薦等級 {phase_dungeon['recommended']} / 探索步數 {phase_dungeon['steps']} 步 / 魔物種類 {len(phase_dungeon.get('monsters', []))} 種。"
                ),
                "detail_note": "本階段使用由遊戲核心驗證的旅行動作。",
                "unlocked": phase_unlocked,
                "replayable": phase_unlocked,
                "recommended_level": phase_dungeon["recommended"],
                "steps": f"{phase_dungeon['steps']}",
                "attribute": phase_dungeon.get("element", REGION_LABELS[region_id]),
                "clear_state": "已通關" if phase_dungeon_id in state.get("cleared_dungeons", []) else "未通關",
                "exploration_rating": "核心驗證",
                "boss": boss_label(phase_dungeon.get("boss")),
                "preview_role": slot.get("preview_role", "dungeon"),
                "preview_image": DUNGEON_PREVIEW_ASSETS.get(phase_dungeon_id),
                "primary_action": {
                    "action_id": "confirm_travel",
                    "label": "確認前往",
                    "enabled": phase_unlocked,
                    "disabled_reason": locked_reason,
                    "payload": {
                        "dungeon_id": phase_dungeon_id,
                        "location_id": slot["node_id"],
                        "region_id": region_id,
                    },
                },
            }
        )

    return {
        "group_id": slot["node_id"],
        "current_phase_index": next(
            phase["phase_index"] for phase in phases if phase["dungeon_id"] == active_dungeon_id
        ),
        "phases": phases,
    }


def region_gate_options_model(state: dict[str, Any], source_region_id: str) -> list[dict[str, Any]]:
    all_regions = ["border_fire", "ice", "earth", "thunder", "final"]
    destinations = [r for r in all_regions if r != source_region_id]
    options = []
    for region_id in destinations:
        route_enabled = region_route_enabled(state, region_id)
        options.append(
            {
                "region_id": region_id,
                "label": REGION_LABELS[region_id],
                "name": REGIONS[region_id].get("name", REGION_LABELS[region_id]),
                "town_name": REGIONS[region_id].get("town_name", REGION_LABELS[region_id]),
                "enabled": route_enabled,
                "unlocked": region_runtime_unlocked(state, region_id),
                "disabled_reason": None if route_enabled else region_locked_reason(region_id),
                "action_id": "travel_region",
                "payload": {"region_id": region_id},
            }
        )
    return options


def legacy_world_map_model(state: dict[str, Any]) -> dict[str, Any]:
    locations = [
        {
            "location_id": "border_town",
            "label": "邊境城鎮 艾爾姆",
            "description": "旅程的據點，公會、旅店與工坊都集中在城牆內。",
            "detail_note": "目前所在城鎮。可從這裡返回 Town Hub live screen。",
            "position": {"x": 35, "y": 22},
            "tone": "town",
            "icon_token": "城",
            "unlocked": True,
            "locked_reason": None,
            "favorite": False,
            "status_label": "目前據點",
            "recommended_level": "安全",
            "steps": "0 步",
            "attribute": "城鎮 / 無",
            "clear_state": "可返回",
            "exploration_rating": "整備中",
            "boss": "無",
            "preview_role": "town",
            "primary_action": {
                "action_id": "back_to_town_hub",
                "label": "返回城鎮",
                "enabled": True,
                "disabled_reason": None,
                "payload": {"location_id": "border_town"},
            },
        }
    ]
    unlocked_location_ids = {"border_town"}
    for dungeon_id, dungeon in DUNGEONS.items():
        if dungeon_id == "dungeon_ice_main_phase_1" and game.is_unlocked(state, "dungeon_ice_main_phase_2"):
            continue
        if dungeon_id == "dungeon_ice_main_phase_2" and not game.is_unlocked(state, "dungeon_ice_main_phase_2"):
            continue
        presentation = WORLD_MAP_PRESENTATION.get(
            dungeon_id,
            {
                "location_id": dungeon_id,
                "position": {"x": 50, "y": 50},
                "tone": "fire" if "fire" in dungeon_id or "cinder" in dungeon_id else "nature",
                "icon_token": "地",
                "preview_role": "cave",
                "description": f"{dungeon['recommended']} / {dungeon['steps']} 步",
                "detail_note": "Live 模式將由遊戲核心驗證前往條件。",
                "exploration_rating": "核心驗證",
            },
        )
        unlocked = game.is_unlocked(state, dungeon.get("unlock"))
        location_id = presentation["location_id"]
        if unlocked:
            unlocked_location_ids.add(location_id)
        locations.append(
            {
                "location_id": location_id,
                "label": dungeon["name"],
                "description": presentation["description"],
                "detail_note": presentation["detail_note"],
                "position": presentation["position"],
                "tone": presentation["tone"],
                "icon_token": presentation["icon_token"],
                "unlocked": unlocked,
                "locked_reason": None if unlocked else "尚未由 runtime 解鎖。",
                "favorite": dungeon_id in {"dungeon_moss_cave", "dungeon_scorched_mine", "dungeon_ash_ravine"},
                "status_label": "可探索" if unlocked else "尚未解鎖",
                "recommended_level": dungeon["recommended"],
                "steps": f"{dungeon['steps']} 步",
                "attribute": dungeon["element"],
                "clear_state": "已通關" if dungeon_id in state.get("cleared_dungeons", []) else "未通關",
                "exploration_rating": presentation["exploration_rating"],
                "boss": boss_label(dungeon.get("boss")),
                "preview_role": presentation["preview_role"],
                "primary_action": {
                    "action_id": "confirm_travel",
                    "label": "確認前往",
                    "enabled": unlocked,
                    "disabled_reason": None if unlocked else "尚未由 runtime 解鎖。",
                    "payload": {"dungeon_id": dungeon_id, "location_id": location_id},
                },
            }
        )
    for location in WORLD_MAP_PREVIEW_LOCATIONS:
        locations.append(
            {
                **location,
                "unlocked": False,
                "favorite": False,
                "status_label": "尚未解鎖",
                "recommended_level": "未知",
                "steps": "未知",
                "clear_state": "鎖定",
                "exploration_rating": "無資料",
                "boss": "未知",
                "primary_action": {
                    "action_id": "confirm_travel",
                    "label": "確認前往",
                    "enabled": False,
                    "disabled_reason": location["locked_reason"],
                    "payload": {"location_id": location["location_id"]},
                },
            }
        )
    route_segments = [
        {
            "id": route["id"],
            "status": "open" if route["from"] in unlocked_location_ids and route["to"] in unlocked_location_ids else "locked",
            "points": route["points"],
        }
        for route in WORLD_MAP_ROUTE_SEGMENTS
    ]
    return {
        "screen_id": "world_map",
        "layout_family": "navigation_map",
        "title": "世界地圖",
        "subtitle": "Live 模式使用遊戲核心狀態；畫面結構與靜態原型保持一致。",
        "selected_location_id": next((location["location_id"] for location in locations if location["location_id"] != "border_town" and location["unlocked"]), "border_town"),
        "current_location_id": "border_town",
        "player": player_model(state),
        "menu_actions": [
            {"action_id": "view_status", "label": "查看狀態", "description": "查看冒險者的能力數值與目前裝備。", "enabled": True, "payload": {}},
            {"action_id": "open_bestiary", "label": "怪物圖鑑", "description": "查看冒險中已登錄的魔物資訊。", "enabled": True, "payload": {}},
            {"action_id": "open_inventory", "label": "背包 / 裝備", "description": "查看背包內持有的道具、裝備與素材。", "enabled": True, "payload": {}},
            {"action_id": "save_game", "label": "存檔", "description": "透過遊戲核心寫入目前的進度。", "enabled": True, "payload": {}},
            {"action_id": "open_settings", "label": "設定", "description": "調整遊戲設定。", "enabled": True, "payload": {}},
            {"action_id": "back_to_start_screen", "label": "回到標題", "description": "返回遊戲開始標題畫面。", "enabled": True, "payload": {}},
        ],
        "route_segments": route_segments,
        "locations": locations,
    }


def world_map_model(state: dict[str, Any], selected_region_id: str | None = None) -> dict[str, Any]:
    region_id = normalize_region_id(state, selected_region_id)
    region = REGIONS[region_id]
    region_label = REGION_LABELS[region_id]
    town_name = region.get("town_name", region_label)
    town_id = region_town_location_id(region_id)
    locations: list[dict[str, Any]] = []
    route_segments: list[dict[str, Any]] = []
    unlocked_location_ids: set[str] = {town_id}

    locations.append(
        {
            "location_id": town_id,
            "region_id": region_id,
            "label": town_name,
            "description": f"{town_name}：{region_label}的中心城鎮。設施目前共用城鎮中心區域。",
            "detail_note": "區域內容與據點設施由遊戲核心橋接支援。",
            "position": REGION_TOWN_POSITIONS[region_id],
            "tone": "town",
            "icon_token": "鎮",
            "unlocked": True,
            "locked_reason": None,
            "favorite": region_id == "border_fire",
            "status_label": "城鎮中心",
            "recommended_level": "安全據點",
            "steps": "0 步",
            "attribute": region_label,
            "clear_state": "可返回",
            "exploration_rating": "安全",
            "boss": "-",
            "preview_role": "town",
            "preview_image": REGION_TOWN_ASSETS.get(region_id),
            "primary_action": {
                "action_id": "back_to_town_hub",
                "label": "進入城鎮",
                "enabled": True,
                "disabled_reason": None,
                "payload": {"region_id": region_id, "location_id": town_id, "town_name": town_name},
            },
        }
    )

    previous_id = town_id
    previous_position = REGION_TOWN_POSITIONS[region_id]
    for slot in REGION_DUNGEON_LAYOUTS[region_id]:
        dungeon_id = active_dungeon_id_for_slot(state, slot)
        dungeon = DUNGEONS[dungeon_id]
        node_id = slot["node_id"]
        main_dungeon = main_dungeon_model(state, slot, region_id)
        dungeon_unlocked = game.is_unlocked(state, dungeon.get("unlock"))
        locked_reason = None if dungeon_unlocked else "此迷宮因核心劇情進度尚未解鎖。"
        if dungeon_unlocked:
            unlocked_location_ids.add(node_id)

        locations.append(
            {
                "location_id": node_id,
                "region_id": region_id,
                "dungeon_id": dungeon_id,
                "dungeon_ids": slot.get("dungeon_ids", []),
                "main_dungeon": main_dungeon,
                "label": slot.get("label", dungeon["name"]),
                "description": (
                    f"{region_label} 迷宮（核心資料）：推薦等級 {dungeon['recommended']} / 探索步數 {dungeon['steps']} 步 / 魔物種類 {len(dungeon.get('monsters', []))} 種。"
                ),
                "detail_note": "此點位將傳送當前迷宮 ID 至遊戲核心處理。",
                "position": slot["position"],
                "tone": REGION_TONES[region_id],
                "icon_token": REGION_TOKENS[region_id],
                "unlocked": dungeon_unlocked,
                "locked_reason": locked_reason,
                "favorite": region_id == "border_fire",
                "status_label": "可探索" if dungeon_unlocked else "尚未解鎖",
                "recommended_level": dungeon["recommended"],
                "steps": f"{dungeon['steps']} 步",
                "attribute": dungeon.get("element", region_label),
                "clear_state": "已通關" if dungeon_id in state.get("cleared_dungeons", []) else "未通關",
                "exploration_rating": "核心驗證",
                "boss": boss_label(dungeon.get("boss")),
                "preview_role": slot.get("preview_role", "dungeon"),
                "preview_image": DUNGEON_PREVIEW_ASSETS.get(dungeon_id),
                "primary_action": {
                    "action_id": "confirm_travel",
                    "label": "確認前往",
                    "enabled": dungeon_unlocked,
                    "disabled_reason": locked_reason,
                    "payload": {"dungeon_id": dungeon_id, "location_id": node_id, "region_id": region_id},
                },
            }
        )
        route_segments.append(
            {
                "id": f"{previous_id}_to_{node_id}",
                "status": region_route_status(unlocked_location_ids, previous_id, node_id),
                "points": [
                    [previous_position["x"], previous_position["y"]],
                    [slot["position"]["x"], slot["position"]["y"]],
                ],
            }
        )
        previous_id = node_id
        previous_position = slot["position"]

    gate_options = region_gate_options_model(state, region_id)
    # Add status_label in Traditional Chinese to gate_options
    for opt in gate_options:
        opt["status_label"] = "已開放" if opt["enabled"] else "已鎖定"

    if region_id == "border_fire":
        ice_enabled = any(option["region_id"] == "ice" and option["enabled"] for option in gate_options)
        gate_unlocked = ice_enabled
        gate_locked_reason = None if ice_enabled else region_locked_reason("ice")
        gate_location_id = "region_gate_ice"
    else:
        gate_unlocked = True
        gate_locked_reason = None
        gate_location_id = "region_gate_border"

    region_gate = {
        "location_id": gate_location_id,
        "region_id": region_id,
        "label": "區域傳送陣",
        "description": "前往其他區域的傳送陣。" if region_id != "border_fire" else "完成烈焰印記路線後，可用於前往寒冰等其他區域的傳送陣。",
        "detail_note": "隨時可以返回烈焰邊境；後續區域在完成對應劇情後開放。" if region_id != "border_fire" else "此階段僅支援前往寒冰區域；其他區域在後續版本開放。",
        "position": REGION_GATE_POSITIONS[region_id],
        "tone": "gate",
        "icon_token": "門",
        "unlocked": gate_unlocked,
        "locked_reason": gate_locked_reason,
        "favorite": False,
        "status_label": "已開啟" if gate_unlocked else "鎖定中",
        "recommended_level": "傳送門",
        "steps": "0 步",
        "attribute": "返回區域" if region_id != "border_fire" else "新區域",
        "clear_state": "可前往" if gate_unlocked else "未開放",
        "exploration_rating": "區域移動",
        "boss": "-",
        "preview_role": "gate",
        "preview_image": "../dungeon_exploration/assets/final-dungeon-explore-minor-a-candidate-v01.png", # Use ruins as gate preview
        "options": gate_options,
        "primary_action": {
            "action_id": "open_region_gate",
            "label": "選擇區域",
            "enabled": True,
            "disabled_reason": None,
            "payload": {"source_region_id": region_id},
        },
    }
    locations.append(region_gate)
    route_segments.append(
        {
            "id": f"{previous_id}_to_{gate_location_id}",
            "status": "open" if gate_unlocked else "locked",
            "points": [
                [previous_position["x"], previous_position["y"]],
                [REGION_GATE_POSITIONS[region_id]["x"], REGION_GATE_POSITIONS[region_id]["y"]],
            ],
        }
    )

    selected_location_id = next(
        (location["location_id"] for location in locations if location["location_id"] != town_id and location["unlocked"]),
        town_id,
    )
    return {
        "screen_id": "world_map",
        "layout_family": "navigation_map",
        "title": "世界地圖",
        "subtitle": f"冒險地圖：{region_label}。",
        "selected_location_id": selected_location_id,
        "current_location_id": town_id,
        "current_region_id": region_id,
        "current_region_label": region_label,
        "current_town_name": town_name,
        "map_asset": REGION_MAP_ASSETS.get(region_id),
        "town_asset": REGION_TOWN_ASSETS.get(region_id),
        "region_gate": region_gate,
        "region_options": region_options_model(state, region_id),
        "player": player_model(state),
        "menu_actions": [
            {"action_id": "view_status", "label": "查看狀態", "description": "查看冒險者的能力數值與目前裝備。", "enabled": True, "payload": {}},
            {"action_id": "open_bestiary", "label": "怪物圖鑑", "description": "查看冒險中已登錄的魔物資訊。", "enabled": True, "payload": {}},
            {"action_id": "open_inventory", "label": "背包 / 裝備", "description": "查看背包內持有的道具、裝備與素材。", "enabled": True, "payload": {}},
            {"action_id": "save_game", "label": "存檔", "description": "透過遊戲核心寫入目前的進度。", "enabled": True, "payload": {}},
            {"action_id": "open_settings", "label": "設定", "description": "調整遊戲設定。", "enabled": True, "payload": {}},
            {"action_id": "back_to_start_screen", "label": "回到標題", "description": "返回遊戲開始標題畫面。", "enabled": True, "payload": {}},
        ],
        "route_segments": route_segments,
        "locations": locations,
    }
