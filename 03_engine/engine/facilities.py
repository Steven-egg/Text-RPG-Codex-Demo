from __future__ import annotations

import math
import random

from data import (
    EQUIPMENT,
    ITEMS,
    MAGIC_BOOKS,
    MONSTERS,
    QUESTS,
    RECIPES,
    REGIONS,
    SHOP_INVENTORY,
    SKILLS,
    get_facility_display_name,
    get_npc_display_name,
    get_dialogue,
    has_template,
    say,
)
from .display import (
    action_menu_panel,
    title,
    pause,
    render_panel,
)
from .formatting import (
    item_name,
    format_items,
    equipment_summary,
)
from .previews import (
    get_preview_promotions_for_job,
)
from .state import (
    is_key_item,
    is_unlocked,
    unlock,
    add_item,
    remove_item,
    add_storage_item,
    remove_storage_item,
    owns_item_or_equipped,
    consume_item_or_equipped,
    parent_job,
    check_and_normalize_region,
    get_stats,
    clamp_vitals,
    can_pay_items,
    pay_items,
    quest_unlocked,
    quest_ready,
    player_summary_line,
    player_resource_lines,
    grant_quality_equipment,
)
from .equipment_refs import equipment_ref_count, equipped_reference_for_base
from .equipment_refs import inventory_equipment_refs, resolve_equipment_ref
from .equipment_quality import roll_craft_quality, sell_price, supports_quality_job, QUALITY_LABELS
from .relic import (
    ready_relic_names,
    relic_passive_menu,
    relic_preview_menu,
)
from .cli_helpers import (
    GUILD_MATERIAL_BUY_PRICES,
)

STORAGE_UNLOCK_COST = 500
STORAGE_CAPACITY = 10
TRAVEL_SHOP_CATEGORIES = ["全部", "補給品", "戰術道具", "飾品"]
MAGIC_SHOP_CATEGORIES = ["全部", "攻擊魔法", "恢復魔法", "輔助魔法", "特殊魔法"]
SYNTHESIS_CATEGORIES = ["全部", "裝備", "戰術道具"]
FIRE_MARK_GUILD_INQUIRY_FLAG = "fire_mark_guild_inquiry_done"
FIRE_MARK_CHURCH_BRIDGE_FLAG = "fire_mark_church_bridge_done"
FIRE_MARK_CHURCH_LOOKUP_FLAG = "fire_mark_church_lookup_done"
FIRE_MARK_SHARD_ID = "key_fire_mark_shard"
BOSS_GLEN_SIGHTED_FLAG = "boss_glen_sighted"
BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG = "boss_glen_investigation_accepted"
ICE_REGION_UNLOCK = "unlock_ice_region"
ICE_PHASE_2_DUNGEON_ID = "dungeon_ice_main_phase_2"
EARTH_REGION_UNLOCK = "unlock_earth_region_preview"
EARTH_PHASE_2_DUNGEON_ID = "dungeon_earth_main_phase_2"
THUNDER_REGION_UNLOCK = "unlock_thunder_region_preview"
THUNDER_PHASE_2_DUNGEON_ID = "dungeon_thunder_main_phase_2"
FINAL_REGION_UNLOCK = "unlock_final_region_preview"
FINAL_PHASE_2_DUNGEON_ID = "dungeon_final_main_phase_2"
FINAL_PHASE_3_DUNGEON_ID = "dungeon_final_main_phase_3"
FINAL_QUEST_ID = "quest_final_demon_king"
MAIN_STORY_CLEARED_FLAG = "main_story_cleared"


def next_step_hint(state: dict) -> str:
    if state.get("flags", {}).get(MAIN_STORY_CLEARED_FLAG):
        return "Main story cleared. Save if you want to keep this clear file, or start a new run from the title screen."
    if can_ask_fire_mark_guild_inquiry(state):
        return "三枚火之印記碎片正在共鳴，回冒險者工會詢問諾亞。"
    if should_show_fire_mark_church_lookup(state):
        return "回轉職神殿詢問賽恩的查閱結果。"
    if should_show_fire_mark_church_bridge(state):
        return "帶著三枚火之印記碎片前往轉職神殿。"
    if ready_relic_names(state):
        return f"前往聖物調查台安置聖印：{ready_relic_names(state)[0]}。"
    if "quest_cinder_depths_scout" in state["completed_quests"] and not state["flags"].get("cinder_seal_sentinel_defeated"):
        return "前往燼印深窟終點，挑戰燼印鎮衛。"
    if "quest_supply_upgrade" in state["completed_quests"] and "quest_cinder_depths_scout" not in state["completed_quests"]:
        return "探索燼印深窟並完成工會偵查委託。"
    if state["flags"].get("ash_guardian_defeated") and "quest_supply_upgrade" not in state["completed_quests"]:
        return "收集深窟素材，完成補給線升級。"
    if "quest_ash_ravine_scout" in state["completed_quests"] and not state["flags"].get("ash_guardian_defeated"):
        return "前往灰燼裂谷終點，挑戰灰燼守衛。"
    if "quest_boss_glen" in state["completed_quests"] and "quest_ash_ravine_scout" not in state["completed_quests"]:
        return "前往灰燼裂谷，帶回偵查素材。"
    if "quest_ice_main_phase_2" in state["completed_quests"] and "quest_ice_return_handoff" not in state["completed_quests"]:
        return "Return to the Guild and file the Ice seal handoff report."
    if "quest_earth_main_phase_2" in state["completed_quests"] and "quest_earth_return_handoff" not in state["completed_quests"]:
        return "Return to the Guild and file the Earth seal handoff report."
    if "quest_thunder_main_phase_2" in state["completed_quests"] and "quest_thunder_return_handoff" not in state["completed_quests"]:
        return "Return to the Guild and file the Thunder seal handoff report."
    if "quest_final_main_phase_2" in state["completed_quests"] and FINAL_QUEST_ID not in state["completed_quests"]:
        return "The Demon King's throne route is open. Enter the final phase and finish Q5."
    if "quest_final_main_phase_1" in state["completed_quests"] and "quest_final_main_phase_2" not in state["completed_quests"]:
        return "The final seal core is open. Defeat the Seal Core for Q4."
    if "quest_final_minor_b" in state["completed_quests"] and "quest_final_main_phase_1" not in state["completed_quests"]:
        return "The Demon King's Gate is open. Break the Elemental Echo Gate for Q3."
    if "quest_final_minor_a" in state["completed_quests"] and "quest_final_minor_b" not in state["completed_quests"]:
        return "Broken Seal Ruins is open. Gather final approach samples for Q2."
    if is_unlocked(state, FINAL_REGION_UNLOCK) and "quest_final_minor_a" not in state["completed_quests"]:
        return "Final region is open. Start with Echoing Frontline and prepare for the Demon King."
    if "quest_thunder_return_handoff" in state["completed_quests"] and not is_unlocked(state, FINAL_REGION_UNLOCK):
        return "四元素路線已回報。將四聖印安置到聖物調查台後，魔王城前線才會穩定開啟。"
    if "quest_thunder_main_phase_1" in state["completed_quests"] and "quest_thunder_main_phase_2" not in state["completed_quests"]:
        return "Lightning Tower crown route is open. Push to the Crown Array seal."
    if "quest_thunder_minor_b" in state["completed_quests"] and "quest_thunder_main_phase_1" not in state["completed_quests"]:
        return "Lightning Tower lower array is open. Defeat the Warden for Q3."
    if "quest_thunder_minor_a" in state["completed_quests"] and "quest_thunder_minor_b" not in state["completed_quests"]:
        return "Conductive Channel is open. Gather the anomaly samples for Q2."
    if is_unlocked(state, THUNDER_REGION_UNLOCK) and "quest_thunder_minor_a" not in state["completed_quests"]:
        return "Thunder route is open. Start with Stormbreak Plateau and report Q1 samples."
    if "quest_earth_main_phase_1" in state["completed_quests"] and "quest_earth_main_phase_2" not in state["completed_quests"]:
        return "Leyline Grove deeper route is open. Push to the Deep Heart seal."
    if "quest_earth_minor_b" in state["completed_quests"] and "quest_earth_main_phase_1" not in state["completed_quests"]:
        return "Leyline Grove outer ring is open. Defeat the Grovekeeper for Q3."
    if "quest_earth_minor_a" in state["completed_quests"] and "quest_earth_minor_b" not in state["completed_quests"]:
        return "Old Quarry Vein is open. Gather the anomaly samples for Q2."
    if is_unlocked(state, EARTH_REGION_UNLOCK) and "quest_earth_minor_a" not in state["completed_quests"]:
        return "Earth route is open. Start with Rootfall Wildwood and report Q1 samples."
    if "quest_ice_main_phase_1" in state["completed_quests"] and "quest_ice_main_phase_2" not in state["completed_quests"]:
        return "霜鐵古城 deeper route is open. Push to the inner palace seal."
    if "quest_ice_minor_b" in state["completed_quests"] and "quest_ice_main_phase_1" not in state["completed_quests"]:
        return "霜鐵古城 outer city is open. Defeat the Gatewarden for Q3."
    if "quest_ice_minor_a" in state["completed_quests"] and "quest_ice_minor_b" not in state["completed_quests"]:
        return "霜根岩窟 is open. Gather the anomaly samples for Q2."
    if is_unlocked(state, ICE_REGION_UNLOCK) and "quest_ice_minor_a" not in state["completed_quests"]:
        return "Ice route is open. Start with 幽帆沉船 and report Q1 samples."
    ready_titles = ready_quest_titles(state)
    if ready_titles:
        return f"工會有可交付委託：{ready_titles[0]}。"
    return "整備補給與裝備後，選擇下一座迷宮探索。"


def ready_quest_titles(state: dict) -> list[str]:
    return [
        QUESTS[quest_id]["title"]
        for quest_id in QUESTS
        if quest_unlocked(state, quest_id) and quest_ready(state, quest_id)
    ]


def town_hint_lines(state: dict) -> list[str]:
    hints = []
    main_hint = next_step_hint(state)
    if main_hint != "整備補給與裝備後，選擇下一座迷宮探索。":
        hints.append(main_hint)
    ready_titles = ready_quest_titles(state)
    if ready_titles and not main_hint.startswith("工會有可交付委託"):
        hints.append(f"工會有可交付委託：{'、'.join(ready_titles[:2])}。")
    stats = get_stats(state)
    if state["current_hp"] < stats["max_hp"] or state["current_mp"] < stats["max_mp"]:
        hints.append("旅館可回復 HP/MP，適合在長探索或 Boss 前使用。")
    if state["inventory"].get("item_potion_s", 0) + state["inventory"].get("item_potion_m", 0) == 0:
        hints.append("背包沒有藥水，旅人小鋪可補充探索容錯。")
    if not hints:
        hints.append("把探索收益轉成任務、裝備、技能或補給後再出發。")
    return hints


def guild_hint_lines(state: dict) -> list[str]:
    hints = []
    ready_titles = ready_quest_titles(state)
    if ready_titles:
        hints.append(f"可交付委託：{'、'.join(ready_titles[:2])}。")

    in_progress = []
    for quest_id, quest in QUESTS.items():
        if quest_unlocked(state, quest_id) and quest_id not in state["completed_quests"] and not quest_ready(state, quest_id):
            in_progress.append(f"{quest['title']} 需要 {format_items(quest['turn_in'])}")
    if in_progress:
        hints.append(f"進行中：{in_progress[0]}。")

    if "quest_ash_ravine_scout" in state["completed_quests"] and not state["flags"].get("ash_guardian_defeated"):
        hints.append("灰燼裂谷偵查已完成；灰燼守衛已可在裂谷終點挑戰。")
    elif state["flags"].get("ash_guardian_defeated") and "quest_supply_upgrade" not in state["completed_quests"]:
        hints.append("灰燼守衛已擊敗；補給線升級委託已開放。")
    elif "quest_cinder_depths_scout" in state["completed_quests"] and not state["flags"].get("cinder_seal_sentinel_defeated"):
        hints.append("燼印深窟偵查已完成；燼印鎮衛已可在深窟終點挑戰。")

    if not hints:
        hints.append(next_step_hint(state))
    return hints


def is_shop_item_available(state: dict, item_id: str) -> bool:
    data = ITEMS.get(item_id) or EQUIPMENT.get(item_id)
    if not data:
        return False
    return is_unlocked(state, data.get("unlock"))


def travel_shop_category(item_id: str) -> str:
    if item_id in EQUIPMENT:
        return "飾品"
    kind = ITEMS.get(item_id, {}).get("kind")
    if kind == "consumable":
        return "補給品"
    if kind in {"battle", "special"}:
        return "戰術道具"
    return "其他"


def travel_shop_owned_count(state: dict, item_id: str) -> int:
    if item_id in EQUIPMENT:
        return equipment_ref_count(state, item_id, include_equipped=True)
    owned = state["inventory"].get(item_id, 0)
    return owned


def travel_shop_available_items(state: dict, category: str = "全部", region_id: str = "border_fire") -> list[str]:
    available = [
        item_id for item_id in SHOP_INVENTORY["travel"]
        if is_shop_item_available(state, item_id)
        and (ITEMS.get(item_id) or EQUIPMENT.get(item_id)).get("region", "border_fire") == region_id
    ]
    if category == "全部":
        return available
    return [item_id for item_id in available if travel_shop_category(item_id) == category]


def travel_shop_item_detail(item_id: str) -> str:
    data = ITEMS.get(item_id) or EQUIPMENT[item_id]
    if item_id in EQUIPMENT:
        return equipment_summary(item_id)
    return data.get("desc", "")


def travel_shop_item_line(state: dict, item_id: str) -> str:
    data = ITEMS.get(item_id) or EQUIPMENT[item_id]
    return (
        f"{item_name(item_id)} / {travel_shop_category(item_id)} / "
        f"持有 x{travel_shop_owned_count(state, item_id)} / {data['price']}G / "
        f"{travel_shop_item_detail(item_id)}"
    )


def travel_shop_detail_lines(state: dict, item_id: str) -> list[str]:
    data = ITEMS.get(item_id) or EQUIPMENT[item_id]
    lines = [
        f"商品：{item_name(item_id)}",
        f"分類：{travel_shop_category(item_id)}",
        f"持有：x{travel_shop_owned_count(state, item_id)}",
        f"價格：{data['price']}G",
        f"效果：{travel_shop_item_detail(item_id)}",
        f"目前金幣：{state['gold']}G",
    ]
    if item_id in EQUIPMENT:
        lines.append(f"可用職業：{','.join(EQUIPMENT[item_id]['jobs'])}")
        lines.append("購買後會放入背包；仍需到背包/裝備中替換。")
    return lines


def buy_travel_shop_item(state: dict, item_id: str) -> str:
    data = ITEMS.get(item_id) or EQUIPMENT[item_id]
    price = data["price"]
    if state["gold"] < price:
        return "金幣不足。"
    if item_id in EQUIPMENT and state["job"] not in EQUIPMENT[item_id]["jobs"]:
        return f"{state['job']}無法使用這件裝備，先別買比較好。"
    state["gold"] -= price
    add_item(state, item_id, 1)
    return f"購買了 {item_name(item_id)}。"


def travel_shop_item_menu(state: dict, category: str, region_id: str = "border_fire") -> None:
    while True:
        item_ids = travel_shop_available_items(state, category, region_id)
        facility_name = get_facility_display_name(region_id, "shop")
        if not item_ids:
            render_panel(
                f"{facility_name} - 商品清單",
                [f"分類：{category}", "目前此分類沒有可購買商品。"],
                border_style="green",
            )
            pause()
            return
        choice = action_menu_panel(
            "選擇商品",
            [travel_shop_item_line(state, item_id) for item_id in item_ids],
            f"{facility_name} - 商品清單",
            header_lines=[
                f"持有金幣：{state['gold']}G",
                f"分類：{category} / 可購買商品 {len(item_ids)} 種",
            ],
            hint_lines=["選擇商品可查看效果、持有數與購買確認。"],
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        item_id = item_ids[choice - 1]
        action = action_menu_panel(
            "商品操作",
            ["購買 1 個"],
            f"{facility_name} - 商品詳情",
            header_lines=travel_shop_detail_lines(state, item_id),
            allow_back=True,
            border_style="green",
        )
        if action == 0:
            continue
        result = buy_travel_shop_item(state, item_id)
        render_panel(
            f"{facility_name} - 購買結果",
            [result, f"目前金幣：{state['gold']}G", f"{item_name(item_id)} 持有：x{travel_shop_owned_count(state, item_id)}"],
            border_style="green",
        )
        pause()


def travel_shop(state: dict, region_id: str = "border_fire") -> None:
    region_id = check_and_normalize_region(state, region_id)
    while True:
        available = travel_shop_available_items(state, region_id=region_id)
        category_options = []
        for category in TRAVEL_SHOP_CATEGORIES:
            count = len(travel_shop_available_items(state, category, region_id))
            category_options.append(f"{category} / {count} 種商品")
        shop_title = f"{get_facility_display_name(region_id, 'shop')} - {get_npc_display_name(region_id, 'rabi')}"
        choice = action_menu_panel(
            "選擇分類",
            category_options,
            shop_title,
            header_lines=[
                get_dialogue(region_id, "shop", "welcome"),
                f"持有金幣：{state['gold']}G",
                f"可購買商品：{len(available)} 種",
            ],
            hint_lines=["補給品提高探索容錯；戰術道具能處理長戰鬥；飾品需購買後手動裝備。"],
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        travel_shop_item_menu(state, TRAVEL_SHOP_CATEGORIES[choice - 1], region_id)


def equipment_owned_count(state: dict, item_id: str) -> int:
    return equipment_ref_count(state, item_id, include_equipped=True)


def equipment_status_line(state: dict, item_id: str) -> str:
    if equipped_reference_for_base(state, item_id):
        return "已裝備"
    owned = equipment_ref_count(state, item_id)
    if owned > 0:
        return f"背包 x{owned}"
    return "未持有"


def equipment_job_status(state: dict, item_id: str) -> str:
    return "可用" if state["job"] in EQUIPMENT[item_id]["jobs"] else "目前職業不可用"


def workshop_item_line(state: dict, item_id: str) -> str:
    eq = EQUIPMENT[item_id]
    return (
        f"{eq['name']} / {equipment_job_status(state, item_id)} / "
        f"{equipment_status_line(state, item_id)} / {eq['price']}G / {equipment_summary(item_id)}"
    )


def workshop_item_detail_lines(state: dict, item_id: str) -> list[str]:
    eq = EQUIPMENT[item_id]
    slot_names = {"weapon": "武器", "head": "頭部", "body": "身體", "accessory": "飾品", "special": "特殊"}
    lines = [
        f"裝備：{eq['name']}",
        f"欄位：{slot_names.get(eq['slot'], eq['slot'])} / {eq['subtype']}",
        f"狀態：{equipment_status_line(state, item_id)}",
        f"可用職業：{','.join(eq['jobs'])}",
        f"目前職業：{state['job']}（{equipment_job_status(state, item_id)}）",
        f"價格：{eq['price']}G / 目前金幣：{state['gold']}G",
        f"能力：{equipment_summary(item_id)}",
        f"說明：{eq['desc']}",
        "購買後會放入背包；仍需到背包/裝備中替換。",
    ]
    return lines


def buy_workshop_item(state: dict, item_id: str) -> str:
    eq = EQUIPMENT[item_id]
    if state["gold"] < eq["price"]:
        return "金幣不足。"
    if state["job"] not in eq["jobs"]:
        return f"{state['job']}無法使用這件裝備，先別買比較好。"
    state["gold"] -= eq["price"]
    add_item(state, item_id, 1)
    return f"購買了 {eq['name']}。"


def workshop_buy_menu(state: dict, title_text: str, item_ids: list[str], border_style: str) -> None:
    while True:
        available = [item_id for item_id in item_ids if is_shop_item_available(state, item_id)]
        if not available:
            render_panel(title_text, ["目前沒有可購買裝備。"], border_style=border_style)
            pause()
            return
        choice = action_menu_panel(
            "選擇裝備",
            [workshop_item_line(state, item_id) for item_id in available],
            title_text,
            header_lines=[
                f"持有金幣：{state['gold']}G",
                f"目前職業：{state['job']} / 商品 {len(available)} 種",
            ],
            hint_lines=["選擇裝備可查看完整能力、可用職業與購買確認。"],
            allow_back=True,
            border_style=border_style,
        )
        if choice == 0:
            return
        item_id = available[choice - 1]
        action = action_menu_panel(
            "裝備操作",
            ["購買 1 件"],
            f"{title_text} - 裝備詳情",
            header_lines=workshop_item_detail_lines(state, item_id),
            allow_back=True,
            border_style=border_style,
        )
        if action == 0:
            continue
        result = buy_workshop_item(state, item_id)
        render_panel(
            f"{title_text} - 購買結果",
            [
                result,
                f"目前金幣：{state['gold']}G",
                f"{item_name(item_id)} 狀態：{equipment_status_line(state, item_id)}",
            ],
            border_style=border_style,
        )
        pause()


def recipe_base_status(state: dict, recipe: dict) -> str:
    base_item = recipe.get("base_item")
    if not base_item:
        return "無"
    status = "足夠" if owns_item_or_equipped(state, base_item) else "不足"
    return f"{item_name(base_item)}（{status}）"


def recipe_material_status(state: dict, materials: dict) -> str:
    parts = []
    for item_id, qty in materials.items():
        owned = state["inventory"].get(item_id, 0)
        status = "足夠" if owned >= qty else "不足"
        parts.append(f"{item_name(item_id)} {owned}/{qty} {status}")
    return "、".join(parts) if parts else "無"


def recipe_output_summary(recipe: dict) -> str:
    return format_items(recipe["output"])


def workshop_recipe_line(state: dict, recipe_id: str) -> str:
    recipe = RECIPES[recipe_id]
    return (
        f"{recipe['name']} / {recipe['gold']}G / "
        f"基底：{recipe_base_status(state, recipe)} / "
        f"素材：{format_items(recipe['materials'])} / {recipe['desc']}"
    )


def workshop_recipe_detail_lines(state: dict, recipe_id: str) -> list[str]:
    recipe = RECIPES[recipe_id]
    return [
        f"強化：{recipe['name']}",
        f"完成品：{recipe_output_summary(recipe)}",
        f"基底裝備：{recipe_base_status(state, recipe)}",
        f"素材需求：{recipe_material_status(state, recipe['materials'])}",
        f"費用：{recipe['gold']}G / 目前金幣：{state['gold']}G",
        f"效果：{recipe['desc']}",
        "強化會消耗素材；若需要基底裝備，已裝備物也可被消耗。",
    ]


def craft_recipe_message(state: dict, recipe_id: str) -> str:
    recipe = RECIPES[recipe_id]
    if state["gold"] < recipe["gold"]:
        return "金幣不足。"
    if not can_pay_items(state, recipe["materials"]):
        return "素材不足。"
    base_item = recipe.get("base_item")
    if base_item and not owns_item_or_equipped(state, base_item):
        return f"需要 {item_name(base_item)}。"
    state["gold"] -= recipe["gold"]
    pay_items(state, recipe["materials"])
    if base_item:
        consume_item_or_equipped(state, base_item)
    for item_id, qty in recipe["output"].items():
        if (
            item_id in EQUIPMENT
            and EQUIPMENT[item_id].get("slot") != "special"
            and supports_quality_job(parent_job(state["job"]))
        ):
            quality = roll_craft_quality(recipe.get("region", "border_fire"))
            for _ in range(qty):
                grant_quality_equipment(state, item_id, quality)
        else:
            add_item(state, item_id, qty)
    return f"完成：{recipe['name']}。"


def workshop_upgrade_menu(state: dict, title_text: str, recipe_ids: list[str], border_style: str) -> None:
    while True:
        available = [recipe_id for recipe_id in recipe_ids if recipe_available(state, recipe_id)]
        if not available:
            render_panel(title_text, ["目前沒有可用強化配方。"], border_style=border_style)
            pause()
            return
        choice = action_menu_panel(
            "選擇強化",
            [workshop_recipe_line(state, recipe_id) for recipe_id in available],
            title_text,
            header_lines=[f"持有金幣：{state['gold']}G"],
            hint_lines=["選擇強化可查看基底裝備、素材狀態與完成品。"],
            allow_back=True,
            border_style=border_style,
        )
        if choice == 0:
            return
        recipe_id = available[choice - 1]
        action = action_menu_panel(
            "強化操作",
            ["進行強化"],
            f"{title_text} - 強化詳情",
            header_lines=workshop_recipe_detail_lines(state, recipe_id),
            allow_back=True,
            border_style=border_style,
        )
        if action == 0:
            continue
        result = craft_recipe_message(state, recipe_id)
        render_panel(
            f"{title_text} - 強化結果",
            [result, f"目前金幣：{state['gold']}G"],
            border_style=border_style,
        )
        pause()


def workshop_equipment_lines(state: dict, item_ids: list[str]) -> list[str]:
    slot_names = {"weapon": "武器", "head": "頭部", "body": "身體", "accessory": "飾品", "special": "特殊"}
    relevant_slots = []
    for item_id in item_ids:
        slot = EQUIPMENT[item_id]["slot"]
        if slot not in relevant_slots:
            relevant_slots.append(slot)
    lines = ["目前裝備："]
    for slot in relevant_slots:
        equipped = state["equipment"].get(slot)
        lines.append(f"{slot_names.get(slot, slot)}：{item_name(equipped, state) if equipped else '無'}")
    owned = [
        f"{item_name(item_id)} x{state['inventory'][item_id]} / {equipment_summary(item_id)}"
        for item_id in item_ids
        if state["inventory"].get(item_id, 0) > 0
    ]
    lines.append("")
    lines.append("背包中的本店裝備：")
    lines.extend(owned if owned else ["目前沒有本店裝備在背包中。"])
    return lines


def workshop_catalog(
    state: dict,
    title_text: str,
    option_buy: str,
    option_upgrade: str,
    item_ids: list[str],
    recipe_ids: list[str],
    intro_lines: list[str],
    hint_lines: list[str],
    border_style: str,
) -> None:
    while True:
        choice = action_menu_panel(
            title_text,
            [option_buy, option_upgrade, "我的裝備"],
            title_text,
            header_lines=[*intro_lines, f"持有金幣：{state['gold']}G"],
            hint_lines=hint_lines,
            allow_back=True,
            border_style=border_style,
        )
        if choice == 0:
            return
        if choice == 1:
            workshop_buy_menu(state, f"{title_text} - {option_buy}", item_ids, border_style)
        elif choice == 2:
            workshop_upgrade_menu(state, f"{title_text} - {option_upgrade}", recipe_ids, border_style)
        elif choice == 3:
            render_panel(f"{title_text} - 我的裝備", workshop_equipment_lines(state, item_ids), border_style=border_style)
            pause()


def magic_book_price(state: dict, book_id: str) -> int:
    price = MAGIC_BOOKS[book_id]["price"]
    if book_id == "book_spark" and "quest_magic_crystal" in state["completed_quests"]:
        price = max(0, price - 50)
    return price


def magic_shop_category(book_id: str) -> str:
    skill = SKILLS[MAGIC_BOOKS[book_id]["skill"]]
    kind = skill["kind"]
    if kind == "damage":
        return "攻擊魔法"
    if kind == "heal":
        return "恢復魔法"
    if kind == "buff":
        return "輔助魔法"
    if kind == "debuff":
        return "特殊魔法"
    return "特殊魔法"


def magic_book_status(state: dict, book_id: str) -> str:
    book = MAGIC_BOOKS[book_id]
    skill_id = book["skill"]
    price = magic_book_price(state, book_id)
    if skill_id in state["learned_skills"]:
        return "已學會"
    if state["job"] not in book["jobs"]:
        return "職業不符"
    if state["level"] < book["level"]:
        return f"等級不足 Lv{book['level']}"
    if state["gold"] < price:
        return "金幣不足"
    if not can_pay_items(state, book["materials"]):
        return "素材不足"
    return "可學習"


def magic_shop_book_ids(category: str = "全部", region_id: str = "border_fire") -> list[str]:
    book_ids = [
        book_id for book_id, book in MAGIC_BOOKS.items()
        if book.get("region", "border_fire") == region_id
    ]
    if category == "全部":
        return book_ids
    return [book_id for book_id in book_ids if magic_shop_category(book_id) == category]


def magic_material_status(state: dict, materials: dict) -> str:
    if not materials:
        return "無"
    parts = []
    for item_id, qty in materials.items():
        owned = state["inventory"].get(item_id, 0)
        status = "足夠" if owned >= qty else "不足"
        parts.append(f"{item_name(item_id)} {owned}/{qty} {status}")
    return "、".join(parts)


def magic_book_line(state: dict, book_id: str) -> str:
    book = MAGIC_BOOKS[book_id]
    skill = SKILLS[book["skill"]]
    price = magic_book_price(state, book_id)
    return (
        f"{book['name']} / {magic_shop_category(book_id)} / {magic_book_status(state, book_id)} / "
        f"{','.join(book['jobs'])} Lv{book['level']} / MP {skill['mp']} / {price}G / {skill['desc']}"
    )


def magic_book_detail_lines(state: dict, book_id: str) -> list[str]:
    book = MAGIC_BOOKS[book_id]
    skill = SKILLS[book["skill"]]
    price = magic_book_price(state, book_id)
    lines = [
        f"魔法書：{book['name']}",
        f"分類：{magic_shop_category(book_id)}",
        f"狀態：{magic_book_status(state, book_id)}",
        f"學會技能：{skill['name']} / MP {skill['mp']}",
        f"技能效果：{skill['desc']}",
        f"可用職業：{','.join(book['jobs'])}",
        f"目前職業：{state['job']}（{'可學' if state['job'] in book['jobs'] else '不可學'}）",
        f"等級需求：Lv{book['level']} / 目前 Lv{state['level']}",
        f"費用：{price}G / 目前金幣：{state['gold']}G",
        f"需求素材：{magic_material_status(state, book['materials'])}",
        "魔法書學會後會永久加入戰鬥技能。",
    ]
    if book_id == "book_spark" and "quest_magic_crystal" in state["completed_quests"]:
        lines.append("魔晶研究已完成，火花術書價格已折扣。")
    return lines


def learn_magic_book_message(state: dict, book_id: str) -> str:
    book = MAGIC_BOOKS[book_id]
    skill_id = book["skill"]
    price = magic_book_price(state, book_id)
    if skill_id in state["learned_skills"]:
        return "你已經學會這本書的技能。"
    if state["job"] not in book["jobs"]:
        return f"{state['job']}無法理解這本魔法書的核心術式。"
    if state["level"] < book["level"]:
        return f"等級不足，需要 Lv{book['level']}。"
    if state["gold"] < price:
        return "金幣不足。"
    if not can_pay_items(state, book["materials"]):
        return "素材不足。"
    state["gold"] -= price
    pay_items(state, book["materials"])
    state["learned_skills"].append(skill_id)
    return f"你學會了 {SKILLS[skill_id]['name']}。"


def magic_shop_book_menu(state: dict, category: str, region_id: str = "border_fire") -> None:
    while True:
        book_ids = magic_shop_book_ids(category, region_id)
        facility_name = get_facility_display_name(region_id, "magic_shop")
        if not book_ids:
            render_panel(
                f"{facility_name} - 魔法書列表",
                [f"分類：{category}", "目前此分類沒有魔法書。"],
                border_style="magenta",
            )
            pause()
            return
        choice = action_menu_panel(
            "選擇魔法書",
            [magic_book_line(state, book_id) for book_id in book_ids],
            f"{facility_name} - 魔法書列表",
            header_lines=[
                f"持有金幣：{state['gold']}G",
                f"分類：{category} / 魔法書 {len(book_ids)} 本",
            ],
            hint_lines=["選擇魔法書可查看技能、條件、素材狀態與學習確認。"],
            allow_back=True,
            border_style="magenta",
        )
        if choice == 0:
            return
        book_id = book_ids[choice - 1]
        action = action_menu_panel(
            "魔法書操作",
            ["學習魔法"],
            "星燈魔法商店 - 魔法書詳情",
            header_lines=magic_book_detail_lines(state, book_id),
            allow_back=True,
            border_style="magenta",
        )
        if action == 0:
            continue
        result = learn_magic_book_message(state, book_id)
        render_panel(
            "星燈魔法商店 - 學習結果",
            [
                result,
                f"目前金幣：{state['gold']}G",
                f"狀態：{magic_book_status(state, book_id)}",
            ],
            border_style="magenta",
        )
        pause()


def magic_shop(state: dict, region_id: str = "border_fire") -> None:
    region_id = check_and_normalize_region(state, region_id)
    while True:
        category_options = []
        for category in MAGIC_SHOP_CATEGORIES:
            count = len(magic_shop_book_ids(category, region_id))
            category_options.append(f"{category} / {count} 本魔法書")
        facility_name = get_facility_display_name(region_id, "magic_shop")
        welcome_text = get_dialogue(region_id, "magic_shop", "welcome")
        choice = action_menu_panel(
            "選擇分類",
            category_options,
            facility_name,
            header_lines=[
                welcome_text,
                f"持有金幣：{state['gold']}G",
            ],
            hint_lines=["依魔法功能分類瀏覽；選中魔法書後可查看職業、等級、素材與技能效果。"],
            allow_back=True,
            border_style="magenta",
        )
        if choice == 0:
            return
        magic_shop_book_menu(state, MAGIC_SHOP_CATEGORIES[choice - 1], region_id)


def recipe_region_id(recipe: dict) -> str:
    return recipe.get("region", "border_fire")


def recipe_equipment_outputs(recipe: dict, *, include_special: bool = True) -> list[str]:
    return [
        item_id
        for item_id in recipe.get("output", {})
        if item_id in EQUIPMENT and (include_special or EQUIPMENT[item_id].get("slot") != "special")
    ]


def recipe_job_compatible(state: dict, recipe_id: str) -> bool:
    recipe = RECIPES[recipe_id]
    job = parent_job(state["job"])
    equipment_outputs = recipe_equipment_outputs(recipe)
    if any(job not in EQUIPMENT[item_id].get("jobs", []) for item_id in equipment_outputs):
        return False
    quality_outputs = recipe_equipment_outputs(recipe, include_special=False)
    return not quality_outputs or supports_quality_job(job)


def recipe_unlock_condition(recipe_id: str) -> str:
    """Return a player-facing acquisition condition without exposing data IDs."""
    unlock_key = RECIPES[recipe_id].get("unlock")
    if not unlock_key:
        return "無需額外解鎖"
    if unlock_key in QUESTS:
        return f"完成公會任務「{QUESTS[unlock_key]['title']}」"

    fixed_conditions = {
        "recipe_heat_charm": "在焦石礦坑擊敗熔岩小鬼",
        ICE_REGION_UNLOCK: "於聖物調查台安置「火之聖印」，開啟極寒區域",
        FINAL_REGION_UNLOCK: "於聖物調查台安置火、冰、大地、雷鳴四枚聖印，開啟魔王城前線",
    }
    if unlock_key in fixed_conditions:
        return fixed_conditions[unlock_key]

    producers = [
        quest["title"]
        for quest in QUESTS.values()
        if unlock_key in quest.get("unlocks", [])
    ]
    if producers:
        return "完成公會任務「" + "」或「".join(producers) + "」"
    return "推進目前區域主線並取得配方授權"


def recipe_locked_reason(state: dict, recipe_id: str) -> str | None:
    if is_unlocked(state, RECIPES[recipe_id].get("unlock")):
        return None
    return f"配方尚未取得：{recipe_unlock_condition(recipe_id)}。"


def recipe_unavailable_reason(state: dict, recipe_id: str) -> str | None:
    if not recipe_job_compatible(state, recipe_id):
        output_names = "、".join(
            item_name(item_id) for item_id in recipe_equipment_outputs(RECIPES[recipe_id])
        )
        return f"目前職業「{state['job']}」無法使用產出裝備「{output_names}」。"
    return recipe_locked_reason(state, recipe_id)


def recipe_available(state: dict, recipe_id: str) -> bool:
    return recipe_unavailable_reason(state, recipe_id) is None


def workshop_recipe_ids(region_id: str) -> list[str]:
    return [
        recipe_id
        for recipe_id, recipe in RECIPES.items()
        if recipe_region_id(recipe) == region_id
        and recipe.get("base_item")
        and any(
            EQUIPMENT[item_id].get("slot") not in {"accessory", "special"}
            for item_id in recipe_equipment_outputs(recipe)
        )
    ]


def synthesis_recipe_ids(region_id: str) -> list[str]:
    return [
        recipe_id
        for recipe_id, recipe in RECIPES.items()
        if recipe_region_id(recipe) == region_id
        and (
            not recipe.get("base_item")
            or any(
                EQUIPMENT[item_id].get("slot") == "accessory"
                for item_id in recipe_equipment_outputs(recipe)
            )
        )
    ]


def synthesis_recipe_category(recipe_id: str) -> str:
    recipe = RECIPES[recipe_id]
    for item_id in recipe["output"]:
        if item_id in ITEMS and ITEMS[item_id].get("kind") == "battle":
            return "戰術道具"
    return "裝備"


def synthesis_available_recipes(state: dict, recipe_ids: list[str], category: str = "全部") -> list[str]:
    available = [recipe_id for recipe_id in recipe_ids if recipe_available(state, recipe_id)]
    if category == "全部":
        return available
    return [recipe_id for recipe_id in available if synthesis_recipe_category(recipe_id) == category]


def recipe_output_owned_status(state: dict, recipe: dict) -> str:
    parts = []
    for item_id in recipe["output"]:
        if item_id in EQUIPMENT:
            parts.append(f"{item_name(item_id)} x{equipment_owned_count(state, item_id)}（{equipment_status_line(state, item_id)}）")
        else:
            parts.append(f"{item_name(item_id)} x{state['inventory'].get(item_id, 0)}")
    return "、".join(parts) if parts else "無"


def recipe_base_owned_count(state: dict, recipe: dict) -> int:
    base_item = recipe.get("base_item")
    if not base_item:
        return 0
    if base_item in EQUIPMENT:
        return equipment_ref_count(state, base_item, include_equipped=True)
    return state["inventory"].get(base_item, 0) + (1 if base_item in state["equipment"].values() else 0)


def synthesis_recipe_status(state: dict, recipe_id: str) -> str:
    recipe = RECIPES[recipe_id]
    if state["gold"] < recipe["gold"]:
        return "金幣不足"
    if not can_pay_items(state, recipe["materials"]):
        return "素材不足"
    base_item = recipe.get("base_item")
    if base_item and not owns_item_or_equipped(state, base_item):
        return "基底不足"
    return "可製作"


def max_synthesis_count(state: dict, recipe_id: str) -> int:
    recipe = RECIPES[recipe_id]
    limits = []
    if recipe["gold"] > 0:
        limits.append(state["gold"] // recipe["gold"])
    for item_id, qty in recipe["materials"].items():
        limits.append(state["inventory"].get(item_id, 0) // qty)
    if recipe.get("base_item"):
        limits.append(recipe_base_owned_count(state, recipe))
    return min(limits) if limits else 0


def synthesis_recipe_line(state: dict, recipe_id: str) -> str:
    recipe = RECIPES[recipe_id]
    return (
        f"{recipe['name']} / {synthesis_recipe_category(recipe_id)} / "
        f"{synthesis_recipe_status(state, recipe_id)} / "
        f"產出：{recipe_output_summary(recipe)} / "
        f"持有：{recipe_output_owned_status(state, recipe)} / "
        f"最多 {max_synthesis_count(state, recipe_id)} 次 / "
        f"{recipe['gold']}G / 素材：{recipe_material_status(state, recipe['materials'])}"
    )


def synthesis_recipe_detail_lines(state: dict, recipe_id: str) -> list[str]:
    recipe = RECIPES[recipe_id]
    return [
        f"配方：{recipe['name']}",
        f"分類：{synthesis_recipe_category(recipe_id)}",
        f"狀態：{synthesis_recipe_status(state, recipe_id)}",
        f"產出：{recipe_output_summary(recipe)}",
        f"持有：{recipe_output_owned_status(state, recipe)}",
        f"基底：{recipe_base_status(state, recipe)}",
        f"素材需求：{recipe_material_status(state, recipe['materials'])}",
        f"最多可製作：{max_synthesis_count(state, recipe_id)} 次",
        f"費用：{recipe['gold']}G / 目前金幣：{state['gold']}G",
        f"效果：{recipe['desc']}",
        "合成會消耗素材；若需要基底裝備，已裝備物也可被消耗。",
    ]


def craft_recipe(state: dict, recipe_id: str) -> None:
    print(craft_recipe_message(state, recipe_id))


def craft_recipe_list_menu(state: dict, title_text: str, recipe_ids: list[str], category: str) -> None:
    while True:
        available = synthesis_available_recipes(state, recipe_ids, category)
        if not available:
            render_panel(
                f"{title_text} - 配方列表",
                [f"分類：{category}", "目前此分類沒有可用配方。"],
                border_style="green",
            )
            pause()
            return
        choice = action_menu_panel(
            "選擇配方",
            [synthesis_recipe_line(state, recipe_id) for recipe_id in available],
            f"{title_text} - 配方列表",
            header_lines=[
                f"持有金幣：{state['gold']}G",
                f"分類：{category} / 配方 {len(available)} 張",
            ],
            hint_lines=["選擇配方可查看完整材料狀態與合成確認。"],
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        recipe_id = available[choice - 1]
        action = action_menu_panel(
            "合成操作",
            ["進行合成"],
            f"{title_text} - 配方詳情",
            header_lines=synthesis_recipe_detail_lines(state, recipe_id),
            allow_back=True,
            border_style="green",
        )
        if action == 0:
            continue
        result = craft_recipe_message(state, recipe_id)
        recipe = RECIPES[recipe_id]
        render_panel(
            f"{title_text} - 合成結果",
            [
                result,
                f"目前金幣：{state['gold']}G",
                f"持有：{recipe_output_owned_status(state, recipe)}",
            ],
            border_style="green",
        )
        pause()


def craft_menu(state: dict, title_text: str, recipe_ids: list[str], region_id: str = "border_fire") -> None:
    title_text = get_facility_display_name(region_id, "synthesis")
    while True:
        available = synthesis_available_recipes(state, recipe_ids)
        if not available:
            render_panel(title_text, ["目前沒有可用配方。"], border_style="green")
            pause()
            return
        choice = action_menu_panel(
            "選擇分類",
            [
                f"{category} / {len(synthesis_available_recipes(state, recipe_ids, category))} 張配方"
                for category in SYNTHESIS_CATEGORIES
            ],
            title_text,
            header_lines=[
                get_dialogue(region_id, "synthesis", "welcome"),
                f"持有金幣：{state['gold']}G",
            ],
            hint_lines=["分類瀏覽可用配方；選中配方後會顯示產出、持有數、基底與素材狀態。"],
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        craft_recipe_list_menu(state, title_text, recipe_ids, SYNTHESIS_CATEGORIES[choice - 1])


def rest_inn(state: dict, region_id: str = "border_fire") -> None:
    stats = get_stats(state)
    title_text = get_facility_display_name(region_id, "inn")
    welcome_text = get_dialogue(region_id, "inn", "welcome")
    reject_text = get_dialogue(region_id, "inn", "reject")
    render_panel(
        title_text,
        [
            welcome_text,
            f"費用：30G / 目前金幣：{state['gold']}G",
            f"目前 HP {state['current_hp']}/{stats['max_hp']} / MP {state['current_mp']}/{stats['max_mp']}",
        ],
        border_style="green",
    )
    if state["gold"] < 30:
        print(reject_text)
        pause()
        return
    raw = input("要休息一晚嗎？(y/n) > ").strip().lower()
    if raw != "y":
        print("暫不休息。")
    else:
        state["gold"] -= 30
        state["current_hp"] = stats["max_hp"]
        state["current_mp"] = stats["max_mp"]
        print("你在旅館休息了一晚，HP/MP 回滿。")
    pause()


def storage_kind_count(state: dict) -> int:
    from .state import ensure_state_defaults
    ensure_state_defaults(state)
    return len(state["storage"])


def storage_has_room_for(state: dict, item_id: str) -> bool:
    from .state import ensure_state_defaults
    ensure_state_defaults(state)
    return item_id in state["storage"] or storage_kind_count(state) < STORAGE_CAPACITY


def prompt_quantity(action: str, item_id: str, available: int) -> int | None:
    raw = input(f"要{action}幾個 {item_name(item_id)}？目前有 {available} 個，輸入 0 取消 > ").strip()
    try:
        qty = int(raw)
    except ValueError:
        print("請輸入數字。")
        return None
    if qty == 0:
        print("取消。")
        return None
    if qty < 0:
        print("數量不能小於 0。")
        return None
    if qty > available:
        print("數量超過目前持有數量。")
        return None
    return qty


def show_storage(state: dict) -> None:
    from .state import ensure_state_defaults
    ensure_state_defaults(state)
    if not state["storage"]:
        render_panel("倉庫內容", ["倉庫目前是空的。"], border_style="green")
        return
    lines = [f"{item_name(item_id)} x{qty}" for item_id, qty in state["storage"].items()]
    render_panel("倉庫內容", lines, border_style="green")


def storage_deposit_menu(state: dict) -> None:
    from .state import ensure_state_defaults
    ensure_state_defaults(state)
    if not state["storage_unlocked"]:
        print("倉庫尚未開啟。")
        pause()
        return

    depositable_ids = [
        item_id
        for item_id, qty in state["inventory"].items()
        if qty > 0 and not is_key_item(item_id)
    ]
    if not depositable_ids:
        print("背包裡沒有可存入倉庫的物品。")
        pause()
        return

    options = []
    for item_id in depositable_ids:
        room_note = ""
        if item_id not in state["storage"] and storage_kind_count(state) >= STORAGE_CAPACITY:
            room_note = " / 倉庫已滿，無法新增種類"
        options.append(f"{item_name(item_id)} x{state['inventory'][item_id]}{room_note}")

    choice = action_menu_panel(
        "選擇要存入的物品",
        options,
        "倉庫存入",
        header_lines=[f"容量：{storage_kind_count(state)}/{STORAGE_CAPACITY} 種物品。"],
        allow_back=True,
        border_style="green",
    )
    if choice == 0:
        return

    item_id = depositable_ids[choice - 1]
    if not storage_has_room_for(state, item_id):
        print("倉庫已滿，無法存入新的物品種類。")
        pause()
        return

    qty = prompt_quantity("存入", item_id, state["inventory"].get(item_id, 0))
    if qty is None:
        pause()
        return

    if remove_item(state, item_id, qty):
        add_storage_item(state, item_id, qty)
        print(f"已存入 {item_name(item_id)} x{qty}。")
    else:
        print("背包中的物品數量不足。")
    pause()


def storage_withdraw_menu(state: dict) -> None:
    from .state import ensure_state_defaults
    ensure_state_defaults(state)
    if not state["storage_unlocked"]:
        print("倉庫尚未開啟。")
        pause()
        return
    if not state["storage"]:
        print("倉庫目前是空的。")
        pause()
        return

    item_ids = list(state["storage"].keys())
    options = [f"{item_name(item_id)} x{state['storage'][item_id]}" for item_id in item_ids]
    choice = action_menu_panel(
        "選擇要取出的物品",
        options,
        "倉庫取出",
        header_lines=[f"容量：{storage_kind_count(state)}/{STORAGE_CAPACITY} 種物品。"],
        allow_back=True,
        border_style="green",
    )
    if choice == 0:
        return

    item_id = item_ids[choice - 1]
    qty = prompt_quantity("取出", item_id, state["storage"].get(item_id, 0))
    if qty is None:
        pause()
        return

    if remove_storage_item(state, item_id, qty):
        add_item(state, item_id, qty)
        print(f"已取出 {item_name(item_id)} x{qty}。")
    else:
        print("倉庫中的物品數量不足。")
    pause()


def storage_menu(state: dict, region_id: str = "border_fire") -> None:
    from .state import ensure_state_defaults
    ensure_state_defaults(state)
    facility_name = get_facility_display_name(region_id, "storage")
    if not state["storage_unlocked"]:
        locked_msg = get_dialogue(region_id, "storage", "locked")
        render_panel(
            facility_name,
            [
                locked_msg,
                f"開啟 LV1 倉庫需要 {STORAGE_UNLOCK_COST}G。",
                f"目前金幣：{state['gold']}G / 容量：{STORAGE_CAPACITY} 種非關鍵物品。",
            ],
            border_style="green",
        )
        if state["gold"] < STORAGE_UNLOCK_COST:
            print("金幣不足，暫時無法開啟倉庫。")
            pause()
            return
        raw = input(f"要花費 {STORAGE_UNLOCK_COST}G 開啟倉庫嗎？(y/n) > ").strip().lower()
        if raw == "y":
            state["gold"] -= STORAGE_UNLOCK_COST
            state["storage_unlocked"] = True
            print(f"倉庫已開啟。容量：{STORAGE_CAPACITY} 種物品。")
        else:
            print("暫不開啟倉庫。")
        pause()
        return

    while True:
        unlocked_msg = get_dialogue(region_id, "storage", "unlocked")
        choice = action_menu_panel(
            "選擇動作",
            ["查看倉庫", "存入物品", "取出物品"],
            f"{facility_name} LV1",
            header_lines=[
                unlocked_msg,
                f"容量：{storage_kind_count(state)}/{STORAGE_CAPACITY} 種物品。",
            ],
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        if choice == 1:
            show_storage(state)
            pause()
        elif choice == 2:
            storage_deposit_menu(state)
        elif choice == 3:
            storage_withdraw_menu(state)



def can_accept_boss_glen_investigation(state: dict) -> bool:
    flags = state.setdefault("flags", {})
    return (
        flags.get(BOSS_GLEN_SIGHTED_FLAG, False)
        and not flags.get(BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG, False)
        and not flags.get("boss_glen_defeated", False)
    )


def accept_boss_glen_investigation(state: dict) -> bool:
    if not can_accept_boss_glen_investigation(state):
        return False
    state["flags"][BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG] = True
    return True


def boss_glen_investigation(state: dict) -> None:
    dungeon_name = DUNGEONS["dungeon_scorched_mine"]["name"]
    boss_name = MONSTERS["boss_glen"]["name"]
    title(f"{dungeon_name}異常調查")
    print(f"你向冒險者公會回報了{dungeon_name}深處的強敵。")
    print(f"公會正式委託你調查並討伐{boss_name}。")
    accept_boss_glen_investigation(state)


def fire_mark_guild_inquiry(state: dict) -> None:
    title("詢問三枚印記碎片的事情")
    print("你把三枚火之印記碎片放在諾亞面前。")
    print("碎片彼此靠近時，裂紋裡浮起微弱的紅光，像在回應同一個呼吸。")
    print()
    print("諾亞仔細翻過工會的舊紀錄，最後搖了搖頭：")
    print("「三枚碎片的反應已經很明顯，但工會沒有足夠資料判讀它真正的用途。」")
    print("「去教堂問問吧。教會保存的舊文獻，頁面上畫著三道分裂的火印。」")
    print()
    print("正式火之印記流程尚未開放；你已記下下一步該詢問教會。")
    state["flags"][FIRE_MARK_GUILD_INQUIRY_FLAG] = True


def guild_menu(state: dict, region_id: str = "border_fire") -> None:
    while True:
        options = ["查看委託任務", "收購素材"]
        glen_investigation_option = can_accept_boss_glen_investigation(state)
        if glen_investigation_option:
            options.append(f"接受{DUNGEONS['dungeon_scorched_mine']['name']}異常調查")
        inquiry_option = can_ask_fire_mark_guild_inquiry(state)
        if inquiry_option:
            options.append("詢問三枚印記碎片的事情")
        facility_name = get_facility_display_name(region_id, "guild")
        greeting = get_dialogue(region_id, "guild", "greeting")
        welcome = get_dialogue(region_id, "guild", "welcome")
        choice = action_menu_panel(
            "選擇服務",
            options,
            facility_name,
            header_lines=[
                greeting,
                welcome,
            ],
            hint_lines=guild_hint_lines(state),
            allow_back=True,
            border_style="cyan",
        )
        if choice == 0:
            return
        if choice == 1:
            guild_quest_menu(state, region_id)
        elif choice == 2:
            guild_material_buy_menu(state)
        elif glen_investigation_option and choice == 3:
            boss_glen_investigation(state)
            pause()
        elif inquiry_option and choice == 3 + int(glen_investigation_option):
            fire_mark_guild_inquiry(state)
            pause()


def can_ask_fire_mark_guild_inquiry(state: dict) -> bool:
    return (
        state["inventory"].get(FIRE_MARK_SHARD_ID, 0) >= 3
        and not state["flags"].get(FIRE_MARK_GUILD_INQUIRY_FLAG)
    )


def guild_quest_menu(state: dict, region_id: str = "border_fire") -> None:
    while True:
        allowed_quest_ids = set(REGIONS.get(region_id, REGIONS["border_fire"]).get("quest_ids", []))
        quest_ids = [qid for qid in QUESTS if qid in allowed_quest_ids and quest_unlocked(state, qid)]
        options = []
        for quest_id in quest_ids:
            quest = QUESTS[quest_id]
            if quest_id in state["completed_quests"]:
                status = "已完成"
            elif quest_ready(state, quest_id):
                status = "可交付"
            else:
                status = f"進行中，需求 {format_items(quest['turn_in'])}"
            options.append(f"{quest['title']} / {status}")
        choice = action_menu_panel(
            "選擇任務",
            options,
            "工會委託",
            header_lines=["委託清單會保留已完成任務，方便確認目前進度。"],
            hint_lines=guild_hint_lines(state),
            allow_back=True,
            border_style="cyan",
        )
        if choice == 0:
            return
        quest_id = quest_ids[choice - 1]
        show_or_complete_quest(state, quest_id)
        pause()


def guild_material_buy_menu(state: dict) -> None:
    while True:
        buyable_ids = [
            item_id
            for item_id in GUILD_MATERIAL_BUY_PRICES
            if state["inventory"].get(item_id, 0) > 0
        ]
        if not buyable_ids:
            render_panel(
                "工會收購素材",
                [
                    "諾亞推來一只木箱：「只收登記過的可重複素材，劇情物品我可不敢碰。」",
                    "背包裡沒有工會目前收購的素材。",
                ],
                border_style="cyan",
            )
            pause()
            return

        options = []
        for item_id in buyable_ids:
            qty = state["inventory"][item_id]
            price = GUILD_MATERIAL_BUY_PRICES[item_id]
            options.append(f"{item_name(item_id)} x{qty} / 單價 {price}G")

        choice = action_menu_panel(
            "選擇要出售的素材",
            options,
            "工會收購素材",
            header_lines=["諾亞推來一只木箱：「只收登記過的可重複素材，劇情物品我可不敢碰。」"],
            allow_back=True,
            border_style="cyan",
        )
        if choice == 0:
            return

        item_id = buyable_ids[choice - 1]
        owned = state["inventory"].get(item_id, 0)
        price = GUILD_MATERIAL_BUY_PRICES[item_id]
        raw = input(f"要出售幾個 {item_name(item_id)}？目前有 {owned} 個，輸入 0 取消 > ").strip()
        try:
            qty = int(raw)
        except ValueError:
            print("請輸入數字。")
            pause()
            continue

        if qty == 0:
            print("取消出售。")
            pause()
            continue
        if qty < 0:
            print("數量不能小於 0。")
            pause()
            continue
        if qty > owned:
            print("背包中的素材數量不足。")
            pause()
            continue

        total = qty * price
        print(f"收購價格：{item_name(item_id)} x{qty} = {total}G。")
        confirm = input("確定出售嗎？(y/n) > ").strip().lower()
        if confirm != "y":
            print("取消出售。")
            pause()
            continue

        remove_item(state, item_id, qty)
        state["gold"] += total
        print(f"已出售 {item_name(item_id)} x{qty}，獲得 {total}G。")
        pause()


def show_or_complete_quest(state: dict, quest_id: str) -> None:
    quest = QUESTS[quest_id]
    title(quest["title"])
    print(f"委託人：{quest['giver']}")
    print(quest["desc"])
    if quest_id in state["completed_quests"]:
        print("這個任務已完成。")
        return
    print(f"交付需求：{format_items(quest['turn_in'])}")
    if not quest_ready(state, quest_id):
        print("目前還不能交付。")
        return
    raw = input("要交付任務嗎？(y/n) > ").strip().lower()
    if raw != "y":
        return
    pay_items(state, quest["turn_in"])
    reward = quest["reward"]
    state["gold"] += reward.get("gold", 0)
    guild_gain = reward.get("guild", 0)
    if state["equipment"].get("special") == "special_trial_badge":
        guild_gain = math.ceil(guild_gain * 1.05)
    state["guild_points"] += guild_gain
    for item_id, qty in reward.get("items", {}).items():
        add_item(state, item_id, qty)
    for key in quest.get("unlocks", []):
        unlock(state, key)
    state["completed_quests"].append(quest_id)
    print(f"任務完成。獲得 {reward.get('gold', 0)}G、工會積分 +{guild_gain}。")
    quest_complete_key = f"quest_complete.{quest_id}"
    if has_template(quest_complete_key):
        lines = say(quest_complete_key)
        for line in lines:
            print(line)


def promotion_requirement_met(state: dict, requirement: dict) -> bool:
    kind = requirement.get("kind")
    if kind == "level":
        return state.get("level", 0) >= requirement.get("value", 0)
    if kind == "unlock":
        return is_unlocked(state, requirement.get("key"))
    if kind == "quest":
        return requirement.get("key") in state.get("completed_quests", [])
    if kind == "flag":
        return bool(state.get("flags", {}).get(requirement.get("key")))
    if kind == "item":
        return state.get("inventory", {}).get(requirement.get("key"), 0) > 0
    return False


def promotion_requirement_line(state: dict, requirement: dict) -> str:
    status = "已達成" if promotion_requirement_met(state, requirement) else "未達成"
    return f"- [{status}] {requirement['label']}"


def should_show_fire_mark_church_bridge(state: dict) -> bool:
    return (
        state["flags"].get(FIRE_MARK_GUILD_INQUIRY_FLAG, False)
        and state["inventory"].get(FIRE_MARK_SHARD_ID, 0) >= 3
        and not state["flags"].get(FIRE_MARK_CHURCH_BRIDGE_FLAG)
    )


def fire_mark_church_bridge(state: dict) -> None:
    print("賽恩聽完諾亞的轉介，視線落在三枚火之印記碎片上。")
    print("碎片的紅光在神殿石階間一明一滅，像是在尋找尚未打開的門。")
    print("「工會看不懂它，是因為這不是委託紀錄裡的東西。」賽恩低聲說。")
    print("「它不普通，但我還不能斷言它是什麼。我要花點時間查閱舊文獻。」")
    print("「先把碎片收好。等我整理出線索，再回神殿找我。」")
    print()
    print("你記下賽恩的囑咐：先保管碎片，稍後再回神殿詢問查閱結果。")
    state["flags"][FIRE_MARK_CHURCH_BRIDGE_FLAG] = True
    print()


def should_show_fire_mark_church_lookup(state: dict) -> bool:
    return (
        state["flags"].get(FIRE_MARK_CHURCH_BRIDGE_FLAG, False)
        and state["inventory"].get(FIRE_MARK_SHARD_ID, 0) >= 3
        and not state["flags"].get(FIRE_MARK_CHURCH_LOOKUP_FLAG)
    )


def fire_mark_church_lookup(state: dict) -> None:
    print("賽恩把翻開的舊文獻推到石桌中央，頁面上畫著三道分裂的火印。")
    print("「查到了。這三枚碎片不是完整的火之印記，而是它尚未完成的核心。」")
    print("「它記錄了火的資格，卻還沒有承載力量。現在啟用，只會把印記燒毀。」")
    print()
    print("賽恩用封蠟與灰白布帶暫時封住碎片的共鳴，又把它們交還給你。")
    print("「去神殿後側的聖物調查台吧。那裡能讓碎片承接成真正的火之聖印。」")
    print()
    print("已確認：未完成的火之印記核心。")
    print("下一步：前往聖物調查台合成並安置火之聖印。聖印被動效果尚未開放。")
    state["flags"][FIRE_MARK_CHURCH_LOOKUP_FLAG] = True
    print()


def parent_job(job: str) -> str:
    return {
        "元素騎士": "劍士",
        "星詠者": "法師",
        "影行者": "盜賊",
        "聖印使": "牧師"
    }.get(job, job)


def temple(state: dict, region_id: str = "border_fire") -> None:
    from data import PROMOTIONS, SKILLS

    facility_name = get_facility_display_name(region_id, "temple")
    welcome_msg = get_dialogue(region_id, "temple", "welcome")
    title(facility_name)
    print(welcome_msg)
    if should_show_fire_mark_church_bridge(state):
        fire_mark_church_bridge(state)
    elif should_show_fire_mark_church_lookup(state):
        fire_mark_church_lookup(state)
    if state["flags"].get("boss_glen_defeated"):
        print("賽恩看著你手中的火之印記碎片：")
        print("「這還不是完整的印記。但神殿記得它的溫度。若你找到更多線索，再回來找我。」")
    print()

    # 檢查是否已選轉職
    promotion_id = state.get("promotion_id")
    if promotion_id:
        promo = PROMOTIONS.get(promotion_id)
        if promo:
            print(f"目前職業：{state['job']}／{promo['name']}")
            print(f"稱號摘要：{promo['summary']}")
            print("您已宣誓晉升，力量已與印記融合。")
            print()
    else:
        print(f"目前職業：{state['job']} (尚未轉職)")
        # 獲取該基礎職業對應的正式轉職
        choices = [
            (promo_id, promo)
            for promo_id, promo in PROMOTIONS.items()
            if promo.get("source_job") == state["job"] and promo.get("status") == "formal"
        ]
        if not choices:
            print("目前尚無可供晉升的正式轉職路線。")
        else:
            print("可晉升轉職路線：")
            for promo_id, promo in choices:
                print("\n────────────────────────────────────────")
                print(f"【{promo['name']}】")
                print(f"描述：{promo['summary']}")
                active_name = SKILLS.get(promo["active_skill_id"], {}).get("name", promo["active_skill_id"])
                active_desc = SKILLS.get(promo["active_skill_id"], {}).get("desc", "")
                passive_name = SKILLS.get(promo["passive_skill_id"], {}).get("name", promo["passive_skill_id"])
                passive_desc = SKILLS.get(promo["passive_skill_id"], {}).get("desc", "")
                print(f" └─ 新主動技能：[{active_name}] - {active_desc}")
                print(f" └─ 新被動技能：[{passive_name}] - {passive_desc}")
            print("────────────────────────────────────────\n")

            # 檢查晉升條件
            lv_satisfied = state.get("level", 1) >= 18
            quest_satisfied = "quest_ice_return_handoff" in state.get("completed_quests", [])

            print("晉升要求狀態：")
            print(f"- [{'已達成' if lv_satisfied else '未達成'}] 角色等級達 Lv18 (目前: Lv{state.get('level', 1)})")
            print(f"- [{'已達成' if quest_satisfied else '未達成'}] 完成任務「寒冰歸來手尾」")

            if lv_satisfied and quest_satisfied:
                print("\n[可轉職] 賽恩微笑著看著你：「你已經證明了自己。是否要繼承力量，進行職業晉升？」")
                menu_options = [f"晉升為 {promo['name']}" for promo_id, promo in choices] + ["我再想想"]
                choice = action_menu_panel(
                    "選擇晉升方向",
                    menu_options,
                    facility_name,
                    border_style="yellow"
                )
                if 1 <= choice <= len(choices):
                    chosen_id, chosen_promo = choices[choice - 1]
                    confirm = input(f"\n【警告】轉職是一次性且不可逆的決定，你確定要轉職為「{chosen_promo['name']}」嗎？(y/n) > ").strip().lower()
                    if confirm in ("y", "yes"):
                        state["promotion_id"] = chosen_id
                        # 學習主動與被動技能
                        learned = state.setdefault("learned_skills", [])
                        if chosen_promo["active_skill_id"] not in learned:
                            learned.append(chosen_promo["active_skill_id"])
                        if chosen_promo["passive_skill_id"] not in learned:
                            learned.append(chosen_promo["passive_skill_id"])

                        print(f"\n【系統】晉升成功！你已正式成為 {chosen_promo['name']}！")
                        print(f"解鎖主動技能 [{SKILLS.get(chosen_promo['active_skill_id'], {}).get('name')}]！")
                        print(f"解鎖被動技能 [{SKILLS.get(chosen_promo['passive_skill_id'], {}).get('name')}]！")
                        pause()
                        return
                    else:
                        print("\n你決定再考慮一下。")
                        pause()
    print("\n神殿聖印選項：")
    if any(state.get("flags", {}).get(flag) for flag in ("fire_seal_enshrined", "ice_seal_enshrined", "earth_seal_enshrined", "thunder_seal_enshrined")):
        choice = action_menu_panel(
            "聖印被動",
            ["選擇／免費改選已安置聖印的被動效果", "離開神殿"],
            facility_name,
            header_lines=["每枚已安置聖印可保留一個被動選擇。"],
            allow_back=True,
            border_style="yellow",
        )
        if choice == 1:
            relic_passive_menu(state)
        else:
            return
    else:
        pause()


def town_menu(state: dict, region_id: str = "border_fire") -> None:
    region_id = check_and_normalize_region(state, region_id)
    while True:
        region = REGIONS.get(region_id, REGIONS["border_fire"])
        options = [
            f"{get_facility_display_name(region_id, 'guild')} - 委託、素材收購與火印線索",
            f"{get_facility_display_name(region_id, 'weapon_workshop')} - 武器購買與強化",
            f"{get_facility_display_name(region_id, 'armor_workshop')} - 防具購買與強化",
            f"{get_facility_display_name(region_id, 'shop')} - 補給與特殊道具",
            f"{get_facility_display_name(region_id, 'synthesis')} - 把素材轉成裝備與戰術道具",
            f"{get_facility_display_name(region_id, 'magic_shop')} - 學習永久技能",
            f"{get_facility_display_name(region_id, 'temple')} - 轉職、火印與未來方向預覽",
            f"{get_facility_display_name(region_id, 'relic')} - 預覽未開放聖物線索",
            f"{get_facility_display_name(region_id, 'storage')} - 存放與取出非關鍵物品",
            f"{get_facility_display_name(region_id, 'inn')}休息 30G - 回復 HP/MP",
        ]
        choice = action_menu_panel(
            "你要去哪裡",
            options,
            region["town_name"],
            header_lines=player_resource_lines(state)[:2],
            hint_lines=town_hint_lines(state),
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        if choice == 1:
            guild_menu(state, region_id)
        elif choice == 2:
            iron_workshop(state, region_id)
        elif choice == 3:
            armor_workshop(state, region_id)
        elif choice == 4:
            travel_shop(state, region_id)
        elif choice == 5:
            if not is_unlocked(state, "shop_synthesis_01"):
                mira_name = get_npc_display_name(region_id, "mira")
                print(f"{mira_name}的店門半掩著。先完成工會任務「洞窟採集」吧。")
                pause()
            else:
                craft_menu(
                    state,
                    get_facility_display_name(region_id, "synthesis"),
                    [r_id for r_id, r in RECIPES.items() if r.get("region", "border_fire") == region_id and (not r.get("base_item") or EQUIPMENT.get(list(r["output"].keys())[0], {}).get("slot") == "accessory")], region_id,
                )
        elif choice == 6:
            magic_shop(state, region_id)
        elif choice == 7:
            temple(state, region_id)
        elif choice == 8:
            relic_preview_menu(state, region_id)
        elif choice == 9:
            storage_menu(state, region_id)
        elif choice == 10:
            rest_inn(state, region_id)


def iron_workshop(state: dict, region_id: str = "border_fire") -> None:
    region_id = check_and_normalize_region(state, region_id)
    title_text = get_facility_display_name(region_id, "weapon_workshop")
    ambiance = get_dialogue(region_id, "weapon_workshop", "ambiance")
    quote = get_dialogue(region_id, "weapon_workshop", "quote")
    workshop_catalog(
        state,
        title_text,
        "購買武器",
        "強化武器",
        SHOP_INVENTORY["weapon"],
        [r_id for r_id, r in RECIPES.items() if r.get("region", "border_fire") == region_id and r.get("base_item") and EQUIPMENT.get(list(r["output"].keys())[0], {}).get("slot") == "weapon"],
        [ambiance, quote],
        ["武器升級能縮短戰鬥回合；購買後仍需到背包/裝備中替換。"],
        "yellow",
    )


def armor_workshop(state: dict, region_id: str = "border_fire") -> None:
    region_id = check_and_normalize_region(state, region_id)
    title_text = get_facility_display_name(region_id, "armor_workshop")
    ambiance = get_dialogue(region_id, "armor_workshop", "ambiance")
    quote = get_dialogue(region_id, "armor_workshop", "quote")
    workshop_catalog(
        state,
        title_text,
        "購買防具",
        "強化防具",
        SHOP_INVENTORY["armor"],
        [r_id for r_id, r in RECIPES.items() if r.get("region", "border_fire") == region_id and r.get("base_item") and EQUIPMENT.get(list(r["output"].keys())[0], {}).get("slot") not in ("weapon", "accessory")],
        [ambiance, quote],
        ["防具與抗性裝能提高長探索容錯；購買後仍需到背包/裝備中替換。"],
        "green",
    )
