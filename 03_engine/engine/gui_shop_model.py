from __future__ import annotations

from typing import Any
from data import ITEMS, EQUIPMENT, SHOP_INVENTORY
from . import game


def get_consumable_description(item_id: str, name: str) -> str:
    descs = {
        "item_potion_s": "星燈鎮藥劑師調配的基礎恢復藥水，輕便好攜帶，是初階冒險者的必備補給。",
        "item_potion_m": "含有更多星燈草提取物的高階恢復藥水，能快速癒合較深的傷口。",
        "item_herb_antidote": "採集自森林邊緣的天然藥草，能有效中和毒素；在 v1 中也可用於緩解輕微灼傷。",
        "item_focus_drop": "蒸餾自魔力花露的澄澈液體，能微幅活化精神力與法力迴路。",
    }
    return descs.get(item_id, f"旅行所需的{name}。")


def get_consumable_effect_summary(item_id: str) -> str:
    effects = {
        "item_potion_s": "回復 HP 35 點",
        "item_potion_m": "回復 HP 70 點",
        "item_herb_antidote": "解除中毒狀態；v1 中亦可消除灼傷 buff",
        "item_focus_drop": "回復 MP 12 點",
    }
    return effects.get(item_id, "")


def shop_screen_model(state: dict[str, Any], selected_region_id: str | None = None) -> dict[str, Any]:
    gold = state.get("gold", 0)
    from data.regions import REGIONS, _is_unlocked
    region_id = selected_region_id or "border_fire"
    if region_id not in REGIONS or not _is_unlocked(state, REGIONS[region_id].get("unlock_key")):
        region_id = "border_fire"
    travel_items = [
        item_id for item_id in SHOP_INVENTORY["travel"]
        if (ITEMS.get(item_id) or EQUIPMENT.get(item_id, {})).get("region", "border_fire") == region_id
    ]

    list_rows = []
    item_details = {}
    requirement_rows = {}
    primary_actions = {}

    category_counts = {
        "all": 0,
        "consumables": 0,
        "tactical": 0,
        "accessories": 0
    }

    for item_id in travel_items:
        item = ITEMS.get(item_id) or EQUIPMENT.get(item_id)
        if not item:
            continue
        price = item["price"]
        owned_count = game.travel_shop_owned_count(state, item_id)
        unlocked = game.is_shop_item_available(state, item_id)
        has_enough_gold = gold >= price

        category_name = game.travel_shop_category(item_id)
        if category_name == "補給品":
            category = "consumables"
            category_label = "補給品"
        elif category_name == "戰術道具":
            category = "tactical"
            category_label = "戰術道具"
        elif category_name == "飾品":
            category = "accessories"
            category_label = "飾品"
        else:
            category = "consumables"
            category_label = "補給品"

        category_counts["all"] += 1
        category_counts[category] += 1

        job_ok = True
        if item_id in EQUIPMENT:
            job_ok = state.get("job") in item["jobs"]

        if not unlocked:
            row_enabled = False
            disabled_reason = "尚未解鎖"
            status = "missing"
            stock_label = "尚未解鎖"
        elif not job_ok:
            row_enabled = False
            disabled_reason = "職業不符"
            status = "blocked"
            stock_label = "無限庫存"
        elif not has_enough_gold:
            row_enabled = False
            disabled_reason = "金幣不足"
            status = "blocked"
            stock_label = "無限庫存"
        else:
            row_enabled = True
            disabled_reason = None
            status = "purchasable"
            stock_label = "無限庫存"

        badges = []
        if item_id == "item_potion_s":
            badges.append({ "badge_id": "hot", "label": "熱銷", "kind": "info" })

        list_rows.append({
            "id": f"row_{item_id.split('_', 1)[1]}",
            "item_id": item_id,
            "title": item["name"],
            "category": category,
            "summary": game.travel_shop_item_detail(item_id),
            "price": price,
            "owned_count": owned_count,
            "stock_label": stock_label,
            "status": status,
            "enabled": row_enabled,
            "disabled_reason": disabled_reason,
            "badges": badges
        })

        item_details[item_id] = {
            "item_id": item_id,
            "title": item["name"],
            "category_label": category_label,
            "description": get_consumable_description(item_id, item["name"]) if category == "consumables" else item.get("desc", ""),
            "effect_summary": get_consumable_effect_summary(item_id) if category == "consumables" else game.travel_shop_item_detail(item_id),
            "use_context": "購買後放入背包；需另行裝備。" if item_id in EQUIPMENT else "可在戰鬥中或非戰鬥狀態下使用。",
            "price": price,
            "owned_count": owned_count,
            "status": status,
            "disabled_reason": disabled_reason
        }

        reqs = []
        # Gold requirement
        gold_status = "met" if has_enough_gold else "missing"
        gold_disabled = None if has_enough_gold else "金幣不足"
        if not unlocked:
            gold_status = "missing"
            gold_disabled = "尚未解鎖"
        reqs.append({
            "id": "gold",
            "label": "金幣需求",
            "required_value": f"{price}G",
            "current_value": f"{gold}G",
            "status": gold_status,
            "disabled_reason": gold_disabled
        })

        # Job restriction if equipment
        if item_id in EQUIPMENT:
            job_status = "met" if job_ok else "missing"
            job_disabled = None if job_ok else "職業不符"
            reqs.append({
                "id": "job",
                "label": "職業限制",
                "required_value": ",".join(item["jobs"]),
                "current_value": state.get("job", ""),
                "status": job_status,
                "disabled_reason": job_disabled
            })

        requirement_rows[item_id] = reqs

        action_enabled = unlocked and has_enough_gold and job_ok
        action_disabled_reason = None
        if not unlocked:
            action_disabled_reason = "尚未解鎖"
        elif not job_ok:
            action_disabled_reason = "職業不符"
        elif not has_enough_gold:
            action_disabled_reason = "金幣不足"

        result_msg = ""
        if action_enabled:
            result_msg = f"成功購買 {item['name']}！獲得 {item['name']} x1，扣除金幣 {price}G。"
        else:
            result_msg = f"無法購買 {item['name']}：{action_disabled_reason}。"

        primary_actions[item_id] = {
            "action_id": "buy_item",
            "label": f"購買 {item['name']}",
            "enabled": action_enabled,
            "disabled_reason": action_disabled_reason,
            "payload": { "item_id": item_id },
            "result_message": result_msg
        }

    category_tabs = [
        { "id": "all", "label": "全部商品", "count": category_counts["all"], "enabled": True },
        { "id": "consumables", "label": "補給品", "count": category_counts["consumables"], "enabled": True },
        { "id": "tactical", "label": "戰術道具", "count": category_counts["tactical"], "enabled": True },
        { "id": "accessories", "label": "飾品", "count": category_counts["accessories"], "enabled": True }
    ]

    if gold >= 30:
        feedback_text = "「挑選想要的物品，右側會顯示購買所需的條件與持有狀況。」"
        feedback_tone = "info"
    else:
        feedback_text = "「金幣不太夠呢，或者有些高等級物資公會還沒放行。去北邊礦坑賺點金幣再來吧？」"
        feedback_tone = "warning"

    feedback_message = {
        "tone": feedback_tone,
        "speaker": "特里",
        "text": feedback_text
    }

    return {
        "screen_id": "facility_shop_screen",
        "facility_id": "travel_shop",
        "title": "星燈行商鋪 (Live)",
        "subtitle": "與遊戲核心同步的商品交易服務，僅限補給品與旅行裝備購買。",
        "npc": {
            "id": "terry",
            "name": "特里",
            "role": "行商特里，常年往返於迷宮城鎮之間，販售各種實用的補給品與旅行裝備。",
            "guidance": "「歡迎光臨！今天的貨色都很齊全喔！特別是生命補給藥水，剛從公會那裡進了一批新鮮的！」",
            "portrait_placeholder": "TR"
        },
        "player_summary": {
            "name": state.get("name", ""),
            "level": state.get("level", 1),
            "job": state.get("job", ""),
            "gold": gold
        },
        "category_tabs": category_tabs,
        "selected_category_id": "all",
        "selected_item_id": "item_potion_s",
        "list_rows": list_rows,
        "item_details": item_details,
        "requirement_rows": requirement_rows,
        "primary_actions": primary_actions,
        "feedback_message": feedback_message,
        "navigation_actions": [
            {
                "action_id": "back_to_town_hub",
                "label": "返回城鎮",
                "description": "離開商鋪返回城鎮廣場。",
                "enabled": True,
                "payload": {}
            }
        ]
    }
