from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "04_data"
ENGINE_ROOT = ROOT / "03_engine"
TOOLS_ROOT = ROOT / "06_tools"
if str(DATA_ROOT) not in sys.path:
    sys.path.insert(0, str(DATA_ROOT))
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from data import (  # noqa: E402
    DUNGEONS,
    EQUIPMENT,
    ITEMS,
    MAGIC_BOOKS,
    MATERIALS,
    MONSTERS,
    QUESTS,
    RECIPES,
    REGIONS,
    get_facility_display_name,
    get_facility_short_description,
)
from region_coverage_report import generate_report as generate_region_coverage  # noqa: E402
from engine import game  # noqa: E402
from engine.gui_actions import world_map_model  # noqa: E402


REGION_ORDER = ["border_fire", "ice", "earth", "thunder", "final"]
REGION_LABELS = {
    "border_fire": "Border / Fire",
    "ice": "Ice",
    "earth": "Earth",
    "thunder": "Thunder",
    "final": "Final",
}
REGION_TONES = {
    "border_fire": "fire",
    "ice": "ice",
    "earth": "nature",
    "thunder": "arcane",
    "final": "bone",
}
REGION_TOKENS = {
    "border_fire": "F",
    "ice": "I",
    "earth": "E",
    "thunder": "T",
    "final": "X",
}
REGION_X = {
    "border_fire": 12,
    "ice": 32,
    "earth": 52,
    "thunder": 72,
    "final": 90,
}
FACILITY_ORDER = [
    ("guild", "guild", "guild", "top_center_guild_hall"),
    ("inn", "bed", "rest", "left_inn"),
    ("travel_shop", "shop", "shop", "mid_left_market"),
    ("workshop", "hammer", "workshop", "right_workshop_group"),
    ("synthesis", "alchemy", "alchemy", "bottom_left_alchemy"),
    ("magic_shop", "magic", "magic", "right_arcane_shop"),
    ("temple", "temple", "temple", "bottom_center_temple"),
    ("relic_preview", "relic", "archive", "bottom_right_archive"),
    ("storage", "storage", "storage", "far_bottom_right_depot"),
]
FACILITY_DISPLAY_KEYS = {
    "guild": "guild",
    "inn": "inn",
    "travel_shop": "shop",
    "workshop": "weapon_workshop",
    "synthesis": "synthesis",
    "magic_shop": "magic_shop",
    "temple": "temple",
    "relic_preview": "relic",
    "storage": "storage",
}
WORLD_FIXTURE_PATHS = [
    ROOT / "07_gui_prototype" / "world_map" / "fixtures" / "world-map-default.json",
    ROOT / "07_gui_prototype" / "world_map" / "fixtures" / "world-map-frontier-alerts.json",
]
GUILD_FIXTURE_PATHS = [
    ROOT / "07_gui_prototype" / "guild_screen" / "fixtures" / "guild-default.json",
    ROOT / "07_gui_prototype" / "guild_screen" / "fixtures" / "guild-quest-ready.json",
]
TOWN_SLOT_PATH = ROOT / "07_gui_prototype" / "town_hub" / "fixtures" / "town-hub-regional-slots.json"
COMBAT_PLACEHOLDER_PATH = (
    ROOT / "07_gui_prototype" / "combat_screen" / "fixtures" / "combat-asset-slot-placeholder.json"
)
DUNGEON_DRIFT_REPLACEMENTS = {
    "ash_valley": "dungeon_ash_ravine",
    "ember_quarry": "dungeon_scorched_mine",
}
COMBAT_DRIFT_REPLACEMENTS = {
    "mon_ash_hound": "mon_ash_imp",
}
ID_DRIFT_REPLACEMENTS = {
    **DUNGEON_DRIFT_REPLACEMENTS,
    **COMBAT_DRIFT_REPLACEMENTS,
    "item_antidote": "item_herb_antidote",
    "item_small_potion": "item_potion_s",
    "item_guardian_charm": "acc_lucky_charm",
    "mat_iron_ore": "mat_scorched_iron",
    "mat_copper_powder": "mat_small_crystal",
    "mat_cloth": "mat_moss_fiber",
}


def item_label(data_id: str) -> str:
    if data_id.startswith("flag:"):
        return data_id.removeprefix("flag:")
    for table in (ITEMS, EQUIPMENT, MATERIALS, MAGIC_BOOKS, RECIPES, DUNGEONS, MONSTERS):
        if data_id in table:
            row = table[data_id]
            if isinstance(row, dict):
                return row.get("name") or row.get("title") or data_id
            return str(row)
    return data_id


def boss_label(boss_id: str | None) -> str:
    if not boss_id:
        return "無"
    return item_label(boss_id)


def reward_items(reward: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "item_id": item_id,
            "label": item_label(item_id),
            "quantity": quantity,
            "icon_id": "item",
        }
        for item_id, quantity in reward.get("items", {}).items()
    ]


def format_turn_in(turn_in: dict[str, int]) -> str:
    if not turn_in:
        return "無交付條件"
    return "、".join(f"{item_label(item_id)} x{quantity}" for item_id, quantity in turn_in.items())


def build_player() -> dict[str, Any]:
    return {
        "name": "米菈",
        "class_label": "冒險者",
        "level_label": "Lv12",
        "hp": {"label": "HP 160/160", "percent": 100},
        "mp": {"label": "MP 46/52", "percent": 88},
        "gold_label": "1957G",
    }


def build_menu_actions(*, alert: bool = False) -> list[dict[str, Any]]:
    return [
        {
            "action_id": "view_status",
            "label": "查看狀態",
            "description": "開啟角色狀態預覽。",
            "enabled": True,
            "disabled_reason": None,
            "payload": {},
        },
        {
            "action_id": "open_bestiary",
            "label": "圖鑑",
            "description": "查看已知敵人預覽。",
            "enabled": True,
            "disabled_reason": None,
            "payload": {},
        },
        {
            "action_id": "open_inventory",
            "label": "背包 / 裝備",
            "description": "查看背包與裝備預覽。",
            "enabled": True,
            "disabled_reason": None,
            "payload": {},
        },
        {
            "action_id": "save_game",
            "label": "儲存",
            "description": "static prototype 只記錄 UIAction。",
            "enabled": not alert,
            "disabled_reason": "警報 fixture 停用儲存按鈕，用來驗證 blocked UIAction。" if alert else None,
            "payload": {},
        },
        {
            "action_id": "open_settings",
            "label": "設定",
            "description": "切換 prototype 顯示設定。",
            "enabled": True,
            "disabled_reason": None,
            "payload": {},
        },
        {
            "action_id": "back_to_start_screen",
            "label": "回標題",
            "description": "返回 Start Screen static prototype。",
            "enabled": True,
            "disabled_reason": None,
            "payload": {},
        },
    ]


def build_world_map_fixture(*, alert: bool = False) -> dict[str, Any]:
    state = game.create_state("Static Demo Adventurer", next(iter(game.JOBS)))
    state["level"] = 7
    state["gold"] = 1957
    for unlock_key in (
        "dungeon_moss_cave",
        "dungeon_scorched_mine",
        "dungeon_ash_ravine",
        "dungeon_cinder_seal_depths",
    ):
        game.unlock(state, unlock_key)
    if alert:
        game.unlock(state, game.ICE_REGION_UNLOCK)

    model = world_map_model(state, "border_fire")
    model["player"] = build_player()
    model["menu_actions"] = build_menu_actions(alert=alert)
    return model

    locations: list[dict[str, Any]] = []
    route_segments: list[dict[str, Any]] = []
    for region_index, region_id in enumerate(REGION_ORDER):
        region = REGIONS[region_id]
        x = REGION_X[region_id]
        hub_id = "border_town" if region_id == "border_fire" else f"town_{region_id}"
        region_label = REGION_LABELS[region_id]
        town_name = region.get("town_name", region_label)
        locations.append(
            {
                "location_id": hub_id,
                "region_id": region_id,
                "label": town_name,
                "description": f"{region_label} town hub shell. CLI facilities remain shared; region identity comes from data context.",
                "detail_note": "Static parity shell：城鎮節點只用於呈現正式版 region/town 輪廓，不新增 runtime town system。",
                "position": {"x": x, "y": 16},
                "tone": "town",
                "icon_token": "TOWN",
                "unlocked": True,
                "locked_reason": None,
                "favorite": region_id == "border_fire",
                "status_label": "城鎮",
                "recommended_level": "Hub",
                "steps": "0 步",
                "attribute": region_label,
                "clear_state": "可進入",
                "exploration_rating": "整備",
                "boss": "無",
                "preview_role": "town",
                "primary_action": {
                    "action_id": "back_to_town_hub",
                    "label": "前往城鎮",
                    "enabled": True,
                    "disabled_reason": None,
                    "payload": {"region_id": region_id, "location_id": hub_id, "town_name": town_name},
                },
            }
        )
        previous_id = hub_id
        dungeon_y = [34, 46, 58, 70, 82]
        for dungeon_index, dungeon_id in enumerate(region.get("dungeon_ids", [])):
            dungeon = DUNGEONS[dungeon_id]
            y = dungeon_y[min(dungeon_index, len(dungeon_y) - 1)]
            status = "warning" if alert and region_id == "border_fire" and dungeon_index >= 2 else "open"
            locations.append(
                {
                    "location_id": dungeon_id,
                    "region_id": region_id,
                    "label": dungeon["name"],
                    "description": (
                        f"{region_label} CLI dungeon skeleton：{dungeon['recommended']} / "
                        f"{dungeon['steps']} 步 / {len(dungeon.get('monsters', []))} 種一般敵人。"
                    ),
                    "detail_note": "由 CLI data 產生的 static fixture；payload 保留正式 dungeon_id，JS 不負責 gameplay 判定。",
                    "position": {"x": x + (dungeon_index % 2) * 6, "y": y},
                    "tone": REGION_TONES[region_id],
                    "icon_token": REGION_TOKENS[region_id],
                    "unlocked": True,
                    "locked_reason": None,
                    "favorite": region_id == "border_fire",
                    "status_label": "CLI 骨架",
                    "recommended_level": dungeon["recommended"],
                    "steps": f"{dungeon['steps']} 步",
                    "attribute": dungeon.get("element", region_label),
                    "clear_state": "未通關",
                    "exploration_rating": "fixture parity",
                    "boss": boss_label(dungeon.get("boss")),
                    "preview_role": "dungeon",
                    "primary_action": {
                        "action_id": "confirm_travel",
                        "label": "進入迷宮",
                        "enabled": True,
                        "disabled_reason": None,
                        "payload": {"dungeon_id": dungeon_id, "location_id": dungeon_id, "region_id": region_id},
                    },
                }
            )
            route_segments.append(
                {
                    "id": f"{previous_id}_to_{dungeon_id}",
                    "status": status,
                    "points": [
                        [x if previous_id == hub_id else x + ((dungeon_index - 1) % 2) * 6, 16 if previous_id == hub_id else dungeon_y[dungeon_index - 1]],
                        [x + (dungeon_index % 2) * 6, y],
                    ],
                }
            )
            previous_id = dungeon_id
        if region_index > 0:
            route_segments.append(
                {
                    "id": f"region_link_{REGION_ORDER[region_index - 1]}_to_{region_id}",
                    "status": "open",
                    "points": [[REGION_X[REGION_ORDER[region_index - 1]], 16], [x, 16]],
                }
            )

    return {
        "screen_id": "world_map",
        "title": "世界地圖",
        "subtitle": "CLI parity shell：只呈現正式 region / town / dungeon 輪廓，不保留舊假入口。",
        "selected_location_id": "dungeon_moss_cave" if not alert else "dungeon_scorched_mine",
        "current_location_id": "border_town",
        "player": build_player(),
        "menu_actions": build_menu_actions(alert=alert),
        "route_segments": route_segments,
        "locations": locations,
        "debug_notes": [
            "Generated by 06_tools/gui_static_parity_builder.py.",
            "Static fixture is not gameplay SSOT.",
            "Fake legacy locations such as moon_tower and drowned_ruins are intentionally omitted.",
        ],
    }


def build_task_filters(task_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    filters = [
        {"id": "all", "label": "全部任務", "count": len(task_rows), "selected": True, "enabled": True},
    ]
    for region_id in REGION_ORDER:
        count = sum(1 for row in task_rows if row["status"] == region_id)
        filters.append(
            {
                "id": region_id,
                "label": REGION_LABELS[region_id],
                "count": count,
                "selected": False,
                "enabled": count > 0,
            }
        )
    return filters


def build_guild_fixture(*, selected_region: str = "border_fire") -> dict[str, Any]:
    task_rows: list[dict[str, Any]] = []
    task_details: dict[str, Any] = {}
    reward_summaries: dict[str, Any] = {}
    condition_rows: dict[str, Any] = {}
    sort_key = 10
    for region_id in REGION_ORDER:
        for quest_id in REGIONS[region_id].get("quest_ids", []):
            quest = QUESTS[quest_id]
            task_rows.append(
                {
                    "task_id": quest_id,
                    "title": quest["title"],
                    "giver": quest.get("giver", "Guild"),
                    "status": region_id,
                    "region_id": region_id,
                    "status_label": REGION_LABELS[region_id],
                    "status_icon_id": "region",
                    "enabled": True,
                    "disabled_reason": None,
                    "sort_key": sort_key,
                }
            )
            sort_key += 10
            task_details[quest_id] = {
                "task_id": quest_id,
                "title": quest["title"],
                "giver": quest.get("giver", "Guild"),
                "description": quest.get("desc", ""),
                "status_label": REGION_LABELS[region_id],
                "related_unlocks": quest.get("unlocks", []),
                "notes": "CLI quest skeleton parity fixture：只呈現任務資料，不執行交付或進度變更。",
                "disabled_reason": "Static parity fixture 不送出正式任務行為。",
                "missing_feedback": {
                    "tone": "info",
                    "speaker": "諾亞",
                    "text": "這是 CLI 任務骨架對照列；正式可交付狀態仍以 runtime 為準。",
                },
            }
            reward = quest.get("reward", {})
            reward_summaries[quest_id] = {
                "gold": reward.get("gold", 0),
                "guild_points": reward.get("guild", 0),
                "items": reward_items(reward),
                "unlocks": quest.get("unlocks", []),
                "notes": "Rewards copied from CLI data for display parity only.",
            }
            turn_in = quest.get("turn_in", {})
            condition_rows[quest_id] = [
                {
                    "id": f"{quest_id}_condition_{index}",
                    "condition_type": "turn_in",
                    "label": item_label(item_id),
                    "required_value": f"x{quantity}",
                    "current_value": "runtime 判定",
                    "status": "not_applicable",
                    "status_label": "CLI 條件",
                    "status_icon_id": "condition",
                    "disabled_reason": None,
                    "source": "cli_data",
                }
                for index, (item_id, quantity) in enumerate(turn_in.items(), start=1)
            ] or [
                {
                    "id": f"{quest_id}_condition_none",
                    "condition_type": "none",
                    "label": "交付條件",
                    "required_value": "無",
                    "current_value": "無",
                    "status": "not_applicable",
                    "status_label": "無交付",
                    "status_icon_id": "none",
                    "disabled_reason": None,
                    "source": "cli_data",
                }
            ]

    selected_task_id = next(
        (row["task_id"] for row in task_rows if row["region_id"] == selected_region),
        task_rows[0]["task_id"],
    )
    return {
        "screen_id": "facility_guild_screen",
        "facility_id": "guild",
        "title": "冒險者工會 / CLI 任務骨架",
        "subtitle": "Guild parity shell：依 REGIONS + QUESTS 產生，region filter 只做靜態對照。",
        "visual_baseline_id": "gui_guild_screen_visual_baseline_v1",
        "npc": {"id": "guild_receptionist", "name": "諾亞", "role": "冒險者工會會長"},
        "task_filters": build_task_filters(task_rows),
        "selected_filter_id": "all",
        "selected_task_id": selected_task_id,
        "task_rows": task_rows,
        "story_hint_card": {"visible": False},
        "task_details": task_details,
        "reward_summaries": reward_summaries,
        "condition_rows": condition_rows,
        "feedback_message": {
            "tone": "info",
            "speaker": "諾亞",
            "text": "這份委託板由 CLI data 產生，用來檢查 GUI 是否看得到正式 region quest skeleton。",
        },
        "secondary_actions": [
            {
                "action_id": "back_to_town_hub",
                "label": "返回城鎮",
                "description": "回到 Town Hub static prototype。",
                "enabled": True,
                "disabled_reason": None,
                "payload": {},
                "visual_role": "secondary",
            }
        ],
        "empty_state": {
            "title": "沒有任務",
            "message": "目前沒有符合此 region filter 的 CLI 任務。",
            "suggested_action": "切換其他 region filter。",
        },
        "resource_strip": [
            {"id": "hero", "label": "米菈 / 冒險者 Lv12", "tone": "primary"},
            {"id": "hp", "label": "HP 160/160", "tone": "healthy"},
            {"id": "mp", "label": "MP 46/52", "tone": "mana"},
            {"id": "gold", "label": "1957G", "tone": "gold"},
            {"id": "guild_points", "label": "Guild 120", "tone": "neutral"},
        ],
        "sellable_materials": [
            {"item_id": "mat_moss_fiber", "title": item_label("mat_moss_fiber"), "owned_count": 8, "unit_price": 6},
            {"item_id": "mat_cracked_stone", "title": item_label("mat_cracked_stone"), "owned_count": 5, "unit_price": 6},
            {"item_id": "mat_small_crystal", "title": item_label("mat_small_crystal"), "owned_count": 2, "unit_price": 14},
        ],
        "debug_notes": [
            "Generated by 06_tools/gui_static_parity_builder.py.",
            "Rows use real QUESTS ids.",
            "Region filters are static prototype UI only.",
        ],
    }


def slot_gap_label(coverage: dict[str, Any], key: str) -> str:
    gaps = []
    for region_id in ["ice", "earth", "thunder", "final"]:
        slot = coverage[region_id][key]
        missing = max(0, slot["expected"] - slot["actual"])
        if missing:
            gaps.append(f"{REGION_LABELS[region_id]} {slot['actual']}/{slot['expected']}")
    return "；".join(gaps) if gaps else "已覆蓋"


def build_town_slot_fixture() -> dict[str, Any]:
    coverage = generate_region_coverage()
    facility_descriptions = {
        "guild": "Quest shell 已可從 CLI REGIONS/QUESTS 產生，適合做 region 任務對照。",
        "inn": "共用休息設施；目前不需要區域化 gameplay data。",
        "travel_shop": f"Regional shop slot placeholder：{slot_gap_label(coverage, 'shop_goods')}",
        "workshop": (
            f"Regional equipment placeholder：{slot_gap_label(coverage, 'equipment')}；"
            f"upgrade placeholder：{slot_gap_label(coverage, 'workshop_upgrades')}"
        ),
        "synthesis": f"Regional synthesis placeholder：{slot_gap_label(coverage, 'recipes')}",
        "magic_shop": f"Regional magic book placeholder：{slot_gap_label(coverage, 'magic_books')}",
        "temple": "Seal / class / lore preview shell；不開啟正式 class transfer 或 relic effects。",
        "relic_preview": "Four-seal relic v1 inspection shell；不呈現 active/passive/combat effect。",
        "storage": "共用倉庫設施；不開啟容量升級或 save schema 變更。",
    }
    facility_nodes = []
    for facility_id, icon_role, visual_group, visual_anchor in FACILITY_ORDER:
        display_key = FACILITY_DISPLAY_KEYS[facility_id]
        label = get_facility_display_name("border_fire", display_key)
        short = get_facility_short_description("border_fire", display_key)
        badges = []
        if facility_id in {"travel_shop", "workshop", "synthesis", "magic_shop"}:
            badges.append({"badge_id": "slot_placeholder", "label": "Slot plan", "kind": "notification", "priority": 60})
        if facility_id == "guild":
            badges.append({"badge_id": "quest_parity", "label": "28 quests", "kind": "notification", "priority": 80})
        facility_nodes.append(
            {
                "facility_id": facility_id,
                "label": label,
                "description": f"{short} / {facility_descriptions[facility_id]}",
                "visual_group": visual_group,
                "visual_anchor": visual_anchor,
                "icon_role": icon_role,
                "enabled": True,
                "disabled_reason": None,
                "badges": badges,
                "primary_action": "open_facility",
                "payload": {"facility_id": facility_id},
            }
        )

    return {
        "screen_id": "town_hub",
        "title": "Regional Facility Slot Shell",
        "subtitle": "Static fixture：呈現 CLI region facility slot 缺口，不新增正式 shop/equipment/recipe/book data。",
        "resource_strip": [
            {"id": "hero", "label": "米菈 / 冒險者 Lv12", "tone": "primary"},
            {"id": "hp", "label": "HP 160/160", "tone": "healthy"},
            {"id": "mp", "label": "MP 46/52", "tone": "mana"},
            {"id": "gold", "label": "1957G", "tone": "gold"},
            {"id": "guild_points", "label": "Guild 120", "tone": "neutral"},
        ],
        "town_guidance": [
            "這是 parity shell：GUI 先看得到 region facility slots，正式數值與解鎖仍留在 runtime/data planning gate。",
            "缺口來自 06_tools/region_coverage_report.py；placeholder 不代表 gameplay data 已落地。",
        ],
        "selected_facility_id": "guild",
        "facility_nodes": facility_nodes,
        "navigation_actions": [
            {
                "action_id": "open_world_map",
                "label": "前往世界地圖",
                "description": "回到 World Map CLI parity shell。",
                "enabled": True,
                "disabled_reason": None,
                "payload": {},
            }
        ],
        "debug_notes": [
            "Generated by 06_tools/gui_static_parity_builder.py.",
            "Facility placeholders are display-only.",
            "Do not treat fixture values as gameplay SSOT.",
        ],
    }


def build_combat_placeholder_fixture(enemy_id: str = "mon_ice_drowned_deckhand") -> dict[str, Any]:
    enemy = MONSTERS[enemy_id]
    return {
        "screen_id": "combat_screen",
        "title": "戰鬥",
        "subtitle": "Combat asset slot placeholder：敵人來自 CLI data，但目前沒有正式 GUI 貼圖。",
        "resource_strip": [{"label": "回合 1", "tone": "neutral"}],
        "player": {
            "name": "米菈",
            "class_label": "冒險者",
            "level_label": "Lv12",
            "hp_label": "160 / 160",
            "mp_label": "46 / 52",
            "status_label": "正常",
            "stance_label": "探索中",
        },
        "enemy": {
            "enemy_id": enemy_id,
            "name": enemy["name"],
            "hp_label": f"HP {enemy['hp']} / {enemy['hp']}",
            "hp_percent": 100,
            "attribute": enemy.get("element", "Unknown"),
            "status_label": "asset slot placeholder",
            "asset_slot": {
                "state": "placeholder",
                "reason": "No formal GUI monster image yet.",
            },
        },
        "command_message": "這個敵人 entry 已存在於 CLI data；GUI 目前只保留 asset slot，不補正式圖片。",
        "skill_menu": {"label": "技能", "title": "技能", "summary": "Static placeholder", "empty_message": "無", "items": []},
        "item_menu": {"label": "道具", "title": "道具", "summary": "Static placeholder", "empty_message": "無", "items": []},
        "battle_log": [
            f"{enemy['name']} 由 CLI MONSTERS 產生。",
            "這個 fixture 用來驗證 GUI fallback，不代表正式 asset pipeline 已開啟。",
        ],
        "actions": [
            {
                "action_id": "basic_attack",
                "label": "攻擊",
                "description": "記錄 UIAction；static prototype 不計算傷害。",
                "enabled": True,
                "disabled_reason": None,
                "primary": True,
                "payload": {"enemy_id": enemy_id},
                "feedback_message": "已送出 basic_attack；static prototype 不計算戰鬥結果。",
            },
            {
                "action_id": "retreat",
                "label": "撤退",
                "description": "回到探索畫面。",
                "enabled": True,
                "disabled_reason": None,
                "primary": False,
                "payload": {"enemy_id": enemy_id},
                "feedback_message": "已送出 retreat；static prototype 只記錄 UIAction。",
            },
        ],
    }


def replace_dungeon_fixture_ids() -> list[dict[str, str]]:
    changed = []
    fixtures_root = ROOT / "07_gui_prototype" / "dungeon_exploration" / "fixtures"
    for path in sorted(fixtures_root.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        dungeon = data.get("dungeon", {})
        old_id = dungeon.get("dungeon_id")
        new_id = DUNGEON_DRIFT_REPLACEMENTS.get(old_id)
        if not new_id:
            continue
        dungeon["dungeon_id"] = new_id
        data["dungeon"] = dungeon
        write_json(path, data)
        changed.append({"file": rel(path), "old": old_id, "new": new_id})
    return changed


def replace_combat_fixture_ids() -> list[dict[str, str]]:
    changed = []
    fixtures_root = ROOT / "07_gui_prototype" / "combat_screen" / "fixtures"
    for path in sorted(fixtures_root.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        enemy = data.get("enemy", {})
        old_id = enemy.get("enemy_id")
        new_id = COMBAT_DRIFT_REPLACEMENTS.get(old_id)
        if not new_id:
            continue
        enemy_data = MONSTERS[new_id]
        enemy["enemy_id"] = new_id
        enemy["name"] = enemy_data["name"]
        enemy["attribute"] = enemy_data.get("element", enemy.get("attribute", ""))
        data["enemy"] = enemy
        write_json(path, data)
        changed.append({"file": rel(path), "old": old_id, "new": new_id})
    return changed


def replace_known_ids(value: Any) -> tuple[Any, bool]:
    if isinstance(value, str):
        replacement = ID_DRIFT_REPLACEMENTS.get(value)
        return (replacement, True) if replacement else (value, False)
    if isinstance(value, list):
        changed = False
        result = []
        for item in value:
            new_item, item_changed = replace_known_ids(item)
            result.append(new_item)
            changed = changed or item_changed
        return result, changed
    if isinstance(value, dict):
        changed = False
        result = {}
        for key, item in value.items():
            new_item, item_changed = replace_known_ids(item)
            result[key] = new_item
            changed = changed or item_changed
        if "item_id" in result and result["item_id"] in ITEMS | EQUIPMENT | MATERIALS:
            label = item_label(result["item_id"])
            if result.get("title") and result.get("title") != label:
                result["title"] = label
                changed = True
            if result.get("label") and result.get("label") != label and key_is_item_label(result):
                result["label"] = label
                changed = True
        if "enemy_id" in result and result["enemy_id"] in MONSTERS:
            label = item_label(result["enemy_id"])
            if result.get("name") and result.get("name") != label:
                result["name"] = label
                changed = True
        if "dungeon_id" in result and result["dungeon_id"] in DUNGEONS:
            label = item_label(result["dungeon_id"])
            if result.get("name") and result.get("name") != label:
                result["name"] = label
                changed = True
        return result, changed
    return value, False


def key_is_item_label(row: dict[str, Any]) -> bool:
    return "item_id" in row and not {"action_id", "disabled_reason"} & set(row)


def normalize_known_fixture_drift() -> list[dict[str, str]]:
    changed_files = []
    for path in sorted((ROOT / "07_gui_prototype").rglob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        normalized, changed = replace_known_ids(data)
        if not changed:
            continue
        write_json(path, normalized)
        changed_files.append({"file": rel(path)})
    return changed_files


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def build_summary() -> dict[str, Any]:
    return {
        "source_tables": {
            "regions": len(REGIONS),
            "dungeons": len(DUNGEONS),
            "quests": len(QUESTS),
            "monsters": len(MONSTERS),
        },
        "generated_targets": [
            *(rel(path) for path in WORLD_FIXTURE_PATHS),
            *(rel(path) for path in GUILD_FIXTURE_PATHS),
            rel(TOWN_SLOT_PATH),
            rel(COMBAT_PLACEHOLDER_PATH),
        ],
        "omitted_legacy_world_locations": [
            "frost_pass",
            "mist_forest",
            "moon_tower",
            "drowned_ruins",
            "windbite_plateau",
        ],
        "drift_replacements": {
            "dungeon_ids": DUNGEON_DRIFT_REPLACEMENTS,
            "enemy_ids": COMBAT_DRIFT_REPLACEMENTS,
        },
    }


def write_all() -> dict[str, Any]:
    for index, path in enumerate(WORLD_FIXTURE_PATHS):
        write_json(path, build_world_map_fixture(alert=index == 1))
    for index, path in enumerate(GUILD_FIXTURE_PATHS):
        write_json(path, build_guild_fixture(selected_region="border_fire" if index == 0 else "ice"))
    write_json(TOWN_SLOT_PATH, build_town_slot_fixture())
    write_json(COMBAT_PLACEHOLDER_PATH, build_combat_placeholder_fixture())
    return {
        **build_summary(),
        "normalized_fixture_ids": normalize_known_fixture_drift(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build GUI static parity fixtures from CLI data without touching gameplay runtime."
    )
    parser.add_argument("--write", action="store_true", help="Write generated fixtures into 07_gui_prototype.")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = write_all() if args.write else build_summary()
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return
    print("# GUI Static Parity Builder")
    print()
    print(f"- Regions: {summary['source_tables']['regions']}")
    print(f"- Dungeons: {summary['source_tables']['dungeons']}")
    print(f"- Quests: {summary['source_tables']['quests']}")
    print(f"- Monsters: {summary['source_tables']['monsters']}")
    print()
    print("Generated targets:")
    for target in summary["generated_targets"]:
        print(f"- {target}")
    print()
    print("Omitted legacy world locations:")
    for location_id in summary["omitted_legacy_world_locations"]:
        print(f"- {location_id}")


if __name__ == "__main__":
    main()
