from __future__ import annotations

from typing import Any
from data import REGIONS
from . import game
from .gui_presentation import resource_strip
from .gui_presentation_helpers import state_summary
from .gui_world_map_model import (
    REGION_LABELS,
    REGION_TOWN_ASSETS,
    region_options_model,
    default_region_id,
)

FACILITY_VISUALS = {
    "guild": {"visual_group": "guild", "visual_anchor": "top_center_guild_hall"},
    "inn": {"visual_group": "rest", "visual_anchor": "left_inn"},
    "travel_shop": {"visual_group": "shop", "visual_anchor": "mid_left_market"},
    "workshop": {"visual_group": "workshop", "visual_anchor": "right_workshop_group"},
    "synthesis": {"visual_group": "alchemy", "visual_anchor": "bottom_left_alchemy"},
    "magic_shop": {"visual_group": "magic", "visual_anchor": "right_arcane_shop"},
    "temple": {"visual_group": "temple", "visual_anchor": "bottom_center_temple"},
    "relic_preview": {"visual_group": "archive", "visual_anchor": "bottom_right_archive"},
    "storage": {"visual_group": "storage", "visual_anchor": "far_bottom_right_depot"},
}


def legacy_town_hub_model(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "screen_id": "town_hub",
        "layout_family": "hub",
        "title": "艾爾姆城鎮 (Live)",
        "subtitle": "角色資源狀態與核心行為皆與 Python 遊戲引擎同步。",
        "resource_strip": resource_strip(state),
        "town_guidance": [
            "Live 模式：所有冒險行為皆經由 Python 核心驗證。",
            "可前往世界地圖繼續冒險，或在城鎮旅店進行休整。",
        ],
        "selected_facility_id": "guild",
        "facility_nodes": facility_nodes(state),
        "navigation_actions": [
            {"action_id": "open_world_map", "label": "前往世界地圖", "description": "離開城鎮，選擇下一個目的地。", "enabled": True, "payload": {}},
        ],
    }


def facility_nodes(state: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        facility(
            "guild",
            "冒險者工會",
            "前往冒險者工會，回報已通關的迷宮探索。",
            "guild",
            "open_facility",
            payload={"facility_id": "guild", "target_screen_id": "guild_screen"},
            target_screen_id="guild_screen",
            navigation_route="../guild_screen/index.html",
        ),
        facility(
            "inn",
            "旅店",
            "前往旅店，提供金幣休整並回復狀態。",
            "bed",
            "open_facility",
            payload={"facility_id": "inn", "target_screen_id": "inn_screen"},
            target_screen_id="inn_screen",
            navigation_route="../inn_screen/index.html",
        ),
        facility(
            "travel_shop",
            "旅人小鋪",
            "前往旅人小鋪購買消耗性補給品。",
            "shop",
            "open_facility",
            payload={"facility_id": "travel_shop", "target_screen_id": "shop_screen"},
            target_screen_id="shop_screen",
            navigation_route="../shop_screen/index.html",
            enabled=True,
        ),
        facility(
            "workshop",
            "鐵刃 / 堅甲工坊",
            "前往工坊購買武器。（MVP 僅開放武器購買，防具與強化尚不可用）",
            "hammer",
            "open_facility",
            payload={"facility_id": "workshop", "target_screen_id": "workshop_screen"},
            target_screen_id="workshop_screen",
            navigation_route="../workshop_screen/index.html",
            enabled=True,
        ),
        facility(
            "synthesis",
            "米菈合成屋",
            "前往米菈合成屋，進行物品與裝備的鍊金合成。" if game.is_unlocked(state, "shop_synthesis_01") else "米菈的店門半掩著。先完成工會任務「洞窟採集」吧。",
            "alchemy",
            "open_facility",
            payload={"facility_id": "synthesis", "target_screen_id": "synthesis_screen"},
            target_screen_id="synthesis_screen",
            navigation_route="../synthesis_screen/index.html",
            enabled=game.is_unlocked(state, "shop_synthesis_01"),
            disabled_reason="米菈的店門半掩著。先完成工會任務「洞窟採集」吧。",
        ),
        facility(
            "magic_shop",
            "星燈魔法商店",
            "前往星燈魔法商店學習與研讀術式魔法書。",
            "magic",
            "open_facility",
            payload={"facility_id": "magic_shop", "target_screen_id": "magic_shop_screen"},
            target_screen_id="magic_shop_screen",
            navigation_route="../magic_shop_screen/index.html",
            enabled=True,
        ),
        facility(
            "temple",
            "轉職神殿",
            "前往轉職神殿，進行職業晉升預覽與印記諮詢。",
            "temple",
            "open_facility",
            payload={"facility_id": "temple", "target_screen_id": "temple_screen"},
            target_screen_id="temple_screen",
            navigation_route="../temple_screen/index.html",
            enabled=True,
        ),
        facility(
            "relic_preview",
            "聖物調查",
            "前往神殿後側的遺跡調查，預覽未開啟的正式聖物玩法。",
            "relic",
            "open_facility",
            payload={"facility_id": "relic_preview", "target_screen_id": "relic_preview_screen"},
            target_screen_id="relic_preview_screen",
            navigation_route="../relic_preview_screen/index.html",
            enabled=True,
        ),
        facility(
            "storage",
            "城鎮倉庫",
            "前往城鎮倉庫，解鎖並檢視保管箱狀態；寄存與取出尚未開放。",
            "storage",
            "open_facility",
            payload={"facility_id": "storage", "target_screen_id": "storage_screen"},
            target_screen_id="storage_screen",
            navigation_route="../storage_screen/index.html",
            enabled=True,
        ),
    ]


def facility(
    facility_id: str,
    label: str,
    description: str,
    icon_role: str,
    action_id: str,
    *,
    payload: dict[str, Any] | None = None,
    enabled: bool = True,
    target_screen_id: str | None = None,
    navigation_route: str | None = None,
    disabled_reason: str | None = None,
) -> dict[str, Any]:
    visual = FACILITY_VISUALS.get(facility_id, {})
    default_reason = "此設施的 Live 模式功能將在後續版本開放。"
    return {
        "facility_id": facility_id,
        "label": label,
        "description": description,
        "visual_group": visual.get("visual_group", facility_id),
        "visual_anchor": visual.get("visual_anchor", facility_id),
        "icon_role": icon_role,
        "enabled": enabled,
        "disabled_reason": None if enabled else (disabled_reason or default_reason),
        "badges": [],
        "primary_action": action_id,
        "payload": payload or {"facility_id": facility_id},
        "target_screen_id": target_screen_id,
        "navigation_route": navigation_route,
    }


def town_hub_model(state: dict[str, Any], selected_region_id: str | None = None) -> dict[str, Any]:
    region_id = default_region_id(state, selected_region_id)
    region = REGIONS[region_id]
    region_label = REGION_LABELS[region_id]
    town_name = region.get("town_name", region_label)
    return {
        "screen_id": "town_hub",
        "layout_family": "hub",
        "title": f"{town_name}",
        "subtitle": "薄霧散去，街道重新亮起微光。旅人們在廣場邊低聲交談。",
        "current_region_id": region_id,
        "selected_region_id": region_id,
        "current_region_label": region_label,
        "current_town_name": town_name,
        "town_asset": REGION_TOWN_ASSETS.get(region_id),
        "region_options": region_options_model(state, region_id),
        "resource_strip": resource_strip(state),
        "town_guidance": [
            "選擇設施進行整備，或前往世界地圖繼續冒險。",
        ],
        "selected_facility_id": "guild",
        "facility_nodes": facility_nodes(state),
        "navigation_actions": [
            {
                "action_id": "open_world_map",
                "label": "前往世界地圖",
                "description": "離開城鎮，選擇下一個目的地。",
                "enabled": True,
                "payload": {"region_id": region_id},
            },
        ],
    }


def inn_screen_model(state: dict[str, Any]) -> dict[str, Any]:
    summary = state_summary(state) or {}
    return {
        "screen_id": "inn_screen",
        "layout_family": "dialogue_node",
        "title": "艾爾姆旅店 (Live)",
        "subtitle": "與遊戲核心同步的休息休整服務。",
        "resource_strip": resource_strip(state),
        "feedback_message": None,
        "service": {
            "service_id": "overnight_rest",
            "label": "住宿休息",
            "description": "支付 30G 住宿費用，並由遊戲核心回復所有生命值與魔力值。",
            "cost": 30,
            "enabled": summary.get("gold", 0) >= 30,
            "disabled_reason": None if summary.get("gold", 0) >= 30 else "身上金幣不足。",
            "action_id": "rest_at_inn",
            "payload": {"service_id": "overnight_rest", "cost": 30},
        },
        "actions": [
            {
                "action_id": "rest_at_inn",
                "label": "休息休整",
                "description": "支付 30G 費用以完全回復狀態。",
                "enabled": summary.get("gold", 0) >= 30,
                "disabled_reason": None if summary.get("gold", 0) >= 30 else "身上金幣不足。",
                "payload": {"service_id": "overnight_rest", "cost": 30},
            }
        ],
        "navigation_actions": [
            {
                "action_id": "back_to_town_hub",
                "label": "返回城鎮",
                "description": "離開旅店返回城鎮廣場。",
                "enabled": True,
                "payload": {"from": "inn_screen"},
            }
        ],
    }

