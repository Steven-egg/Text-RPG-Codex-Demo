from __future__ import annotations

from typing import Any
from data import EQUIPMENT, ITEMS
from . import game
from .formatting import item_name

STORAGE_UNLOCK_COST = game.STORAGE_UNLOCK_COST
STORAGE_CAPACITY = game.STORAGE_CAPACITY


def get_storage_item_category(item_id: str) -> str:
    if item_id in EQUIPMENT:
        return "equipment"
    if item_id.startswith("key_") or item_id == "special_trial_badge":
        return "valuables"
    if item_id.startswith("mat_"):
        return "materials"
    if item_id in ITEMS:
        kind = ITEMS[item_id].get("kind")
        if kind == "consumable":
            return "consumables"
        if kind in {"battle", "special"}:
            return "valuables"
    return "materials"


def get_item_category_label(item_id: str, is_storage: bool = False) -> str:
    suffix = " (倉庫)" if is_storage else " (背包)"
    if item_id in EQUIPMENT:
        slot = EQUIPMENT[item_id].get("slot", "")
        slot_labels = {"weapon": "武器", "head": "頭部防具", "body": "身體防具", "accessory": "飾品", "special": "特殊裝備"}
        return slot_labels.get(slot, "裝備") + suffix
    if item_id.startswith("key_"):
        return "關鍵道具" + suffix
    if item_id.startswith("mat_"):
        return "普通素材" + suffix
    if item_id in ITEMS:
        kind = ITEMS[item_id].get("kind")
        if kind == "consumable":
            return "消耗性道具" + suffix
        if kind == "battle":
            return "戰術道具" + suffix
    return "道具" + suffix


def storage_screen_model(state: dict[str, Any]) -> dict[str, Any]:
    unlocked = state.get("storage_unlocked", False)
    gold = state.get("gold", 0)

    resource_strip = [
        { "id": "player_name", "label": f"{state.get('name', '米菈')}的小隊", "tone": "neutral" },
        { "id": "player_gold", "label": f"金幣：{gold}G", "tone": "warning" if (gold < STORAGE_UNLOCK_COST and not unlocked) else "neutral" },
        { "id": "storage_status", "label": "倉庫狀態：已解鎖" if unlocked else "倉庫狀態：未開啟", "tone": "success" if unlocked else "danger" },
        { "id": "storage_capacity", "label": f"容量：{len(state.get('storage', {}))} / {STORAGE_CAPACITY} 種物品", "tone": "success" if unlocked else "neutral" }
    ]

    inventory_rows = []
    item_details = {}

    for item_id, qty in state.get("inventory", {}).items():
        if qty <= 0:
            continue

        category = get_storage_item_category(item_id)
        name = item_name(item_id)

        enabled = False
        disabled_reason = "倉庫未開啟"
        if unlocked:
            if item_id.startswith("key_"):
                disabled_reason = "貴重物無法存入倉庫"
            elif not game.storage_has_room_for(state, item_id):
                disabled_reason = "倉庫容量已滿，無法新增種類"
            else:
                enabled = True
                disabled_reason = None

        inventory_rows.append({
            "item_id": item_id,
            "title": name,
            "category": category,
            "short_title": name[:3] if len(name) > 3 else name,
            "summary": f"普通素材 / 持有：{qty}" if category == "materials" else f"消耗品 / 持有：{qty}",
            "owned_count": qty,
            "enabled": enabled,
            "disabled_reason": disabled_reason
        })

    storage_rows = []
    if unlocked:
        for item_id, qty in state.get("storage", {}).items():
            if qty <= 0:
                continue

            category = get_storage_item_category(item_id)
            name = item_name(item_id)

            storage_rows.append({
                "item_id": item_id,
                "title": name,
                "category": category,
                "short_title": name[:3] if len(name) > 3 else name,
                "summary": f"普通素材 / 倉庫：{qty}" if category == "materials" else f"消耗品 / 倉庫：{qty}",
                "owned_count": qty,
                "enabled": True,
                "disabled_reason": None
            })

    all_item_ids = set(state.get("inventory", {}).keys()) | set(state.get("storage", {}).keys())
    for item_id in all_item_ids:
        in_inv = state.get("inventory", {}).get(item_id, 0) > 0
        in_st = state.get("storage", {}).get(item_id, 0) > 0
        if not (in_inv or in_st):
            continue

        name = item_name(item_id)
        cat_label = get_item_category_label(item_id, is_storage=in_st and not in_inv)

        desc = ""
        effect = ""
        use_context = ""

        if item_id in EQUIPMENT:
            eq = EQUIPMENT[item_id]
            desc = eq.get("desc", "")
            effect = f"提供屬性加成：攻擊+{eq.get('stats', {}).get('attack', 0)}" if eq.get('stats') else "提供裝備屬性"
            use_context = f"可裝備於：{eq.get('slot')}"
        elif item_id in ITEMS:
            it = ITEMS[item_id]
            desc = it.get("desc", "")
            effect = "戰鬥中或探索中回復生命值" if it.get("kind") == "consumable" else "無直接效果"
            use_context = "生存與恢復" if it.get("kind") == "consumable" else "工坊強化、合成材料"

        item_details[item_id] = {
            "item_id": item_id,
            "title": name,
            "category_label": cat_label,
            "description": desc,
            "effect_summary": effect,
            "use_context": use_context
        }

    category_counts = {"all": 0, "materials": 0, "consumables": 0, "equipment": 0, "valuables": 0}
    for row in inventory_rows:
        category_counts["all"] += 1
        cat = row["category"]
        if cat in category_counts:
            category_counts[cat] += 1

    category_tabs = [
        { "id": "all", "label": "全部", "count": category_counts["all"], "enabled": True },
        { "id": "materials", "label": "材料", "count": category_counts["materials"], "enabled": True },
        { "id": "consumables", "label": "消耗品", "count": category_counts["consumables"], "enabled": True },
        { "id": "equipment", "label": "裝備", "count": category_counts["equipment"], "enabled": True },
        { "id": "valuables", "label": "貴重物", "count": category_counts["valuables"], "enabled": True }
    ]

    primary_actions = {}
    requirement_rows = {}

    if not unlocked:
        can_unlock = gold >= STORAGE_UNLOCK_COST
        disabled_reason = "" if can_unlock else f"金幣不足，需要 {STORAGE_UNLOCK_COST}G"
        primary_actions["unlock_storage"] = {
            "action_id": "unlock_storage",
            "label": f"解鎖倉庫 ({STORAGE_UNLOCK_COST}G)",
            "enabled": can_unlock,
            "disabled_reason": disabled_reason,
            "payload": { "cost": STORAGE_UNLOCK_COST }
        }
        requirement_rows["unlock_storage"] = [
            {
                "id": "req_gold",
                "label": "金幣需求",
                "required_value": f"{STORAGE_UNLOCK_COST}G",
                "current_value": f"{gold}G",
                "status": "met" if can_unlock else "unmet",
                "disabled_reason": None if can_unlock else "金幣不足"
            }
        ]
    else:
        primary_actions["upgrade_storage"] = {
            "action_id": "upgrade_storage",
            "label": "升級倉庫容量 (未開放)",
            "enabled": False,
            "disabled_reason": "工會目前尚未開放更高級別的擴充服務",
            "payload": {}
        }

        for row in inventory_rows:
            primary_actions[row["item_id"]] = {
                "action_id": "deposit_item",
                "label": "確認存入",
                "enabled": row["enabled"],
                "disabled_reason": row["disabled_reason"],
                "payload": { "item_id": row["item_id"], "quantity": 1 }
            }
            requirement_rows[row["item_id"]] = []
            if not row["enabled"]:
                requirement_rows[row["item_id"]].append({
                    "id": "req_mvp_disabled",
                    "label": "轉移服務限制",
                    "required_value": "可存入",
                    "current_value": "限制中",
                    "status": "unmet",
                    "disabled_reason": row["disabled_reason"]
                })
        for row in storage_rows:
            primary_actions[row["item_id"]] = {
                "action_id": "withdraw_item",
                "label": "確認取出",
                "enabled": True,
                "disabled_reason": None,
                "payload": { "item_id": row["item_id"], "quantity": 1 }
            }
            requirement_rows[row["item_id"]] = []

    return {
        "screen_id": "storage_screen",
        "facility_id": "storage",
        "title": "工會倉庫 (Live)",
        "subtitle": "與遊戲核心同步的保管箱存取服務。",
        "selected_mode": "deposit",
        "selected_item_id": None,
        "storage_state": {
            "unlocked": unlocked,
            "unlock_cost": 0 if unlocked else STORAGE_UNLOCK_COST,
            "can_unlock": (gold >= STORAGE_UNLOCK_COST) if not unlocked else False,
            "disabled_reason": "" if (unlocked or gold >= STORAGE_UNLOCK_COST) else "金幣不足以支付開啟費用"
        },
        "resource_strip": resource_strip,
        "npc": {
            "name": "諾亞",
            "role": "冒險者工會會長",
            "portrait_placeholder": "Noah",
            "avatar_text": "「目前先幫你開啟與檢視保管箱；寄存與取出服務還在準備中。」",
            "dialog_locked": "本輪 Live MVP 僅提供倉庫解鎖與檢視；寄存與取出尚未開放。" if unlocked else f"花費 {STORAGE_UNLOCK_COST}G 金幣可為米菈小隊解鎖工會專屬的無限期保管箱。"
        },
        "category_tabs": category_tabs,
        "inventory_rows": inventory_rows,
        "storage_rows": storage_rows,
        "item_details": item_details,
        "primary_actions": primary_actions,
        "requirement_rows": requirement_rows,
        "empty_state": {
            "title": "沒有物品",
            "message": "目前沒有符合篩選條件的物品。",
            "suggested_action": "切換其他篩選。"
        }
    }
