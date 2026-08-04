from __future__ import annotations

from typing import Any
from data import EQUIPMENT, ITEMS, RECIPES, MATERIALS
from . import game
from .equipment_refs import equipment_base_id
from .gui_presentation import resource_strip


def synthesis_screen_model(state: dict[str, Any], selected_region_id: str | None = None) -> dict[str, Any]:
    gold = state.get("gold", 0)
    from data.regions import REGIONS, _is_unlocked
    region_id = selected_region_id or "border_fire"
    if region_id not in REGIONS or not _is_unlocked(state, REGIONS[region_id].get("unlock_key")):
        region_id = "border_fire"
    mira_recipes = game.synthesis_recipe_ids(region_id)

    recipe_rows = []
    recipe_details = {}
    requirement_rows = {}

    equipment_count = 0
    battle_count = 0

    icon_labels = {
        "gold": "G",
        "mat_scorched_iron": "鐵",
        "mat_cracked_stone": "石",
        "mat_moss_fiber": "纖",
        "mat_small_crystal": "晶",
        "mat_fire_stone": "火",
        "mat_lava_shard": "岩",
    }

    # First, scan recipes to get counts
    for r_id in mira_recipes:
        cat_str = game.synthesis_recipe_category(r_id)
        if cat_str == "裝備":
            equipment_count += 1
        else:
            battle_count += 1

    # Default selection to the first recipe routed to this region's synthesis shop.
    default_recipe_id = mira_recipes[0] if mira_recipes else ""

    for r_id in mira_recipes:
        recipe = RECIPES[r_id]
        unlocked = game.is_unlocked(state, recipe.get("unlock"))
        job_compatible = game.recipe_job_compatible(state, r_id)
        unavailable_reason = game.recipe_unavailable_reason(state, r_id)
        has_enough_gold = gold >= recipe["gold"]
        has_enough_mats = game.can_pay_items(state, recipe["materials"])

        base_item = recipe.get("base_item")
        has_base_item = True
        if base_item:
            has_base_item = game.owns_item_or_equipped(state, base_item)

        # Categorize
        cat_str = game.synthesis_recipe_category(r_id)
        category = "equipment" if cat_str == "裝備" else "battle"
        category_label = cat_str

        # Get output item info
        out_item_id, out_qty = list(recipe["output"].items())[0]
        out_name = game.item_name(out_item_id)
        output_summary = f"{out_name} x{out_qty}"

        if out_item_id in EQUIPMENT:
            owned_count = game.equipment_owned_count(state, out_item_id)
            owned_summary = f"{owned_count} 件"
        else:
            owned_count = state.get("inventory", {}).get(out_item_id, 0)
            owned_summary = f"{owned_count} 個"

        # Determine craft limit count
        craft_limit = game.max_synthesis_count(state, r_id)

        # Determine status
        if not job_compatible:
            status = "missing"
            status_label = "職業不符"
            action_enabled = False
            action_disabled_reason = unavailable_reason
            feedback_text = unavailable_reason
            feedback_tone = "warning"
        elif not unlocked:
            status = "missing"
            status_label = "尚未解鎖"
            action_enabled = False
            action_disabled_reason = game.recipe_locked_reason(state, r_id)
            feedback_text = action_disabled_reason
            feedback_tone = "warning"
        elif not has_enough_gold:
            status = "missing"
            status_label = "金幣不足"
            action_enabled = False
            action_disabled_reason = f"需要 {recipe['gold']}G，目前 {gold}G。"
            feedback_text = "素材與基底齊了，但工錢不夠。"
            feedback_tone = "warning"
        elif not has_base_item:
            status = "missing"
            status_label = "缺少基底"
            action_enabled = False
            action_disabled_reason = f"需要基底 {game.item_name(base_item)}。"
            feedback_text = f"缺少必要的基底裝備 {game.item_name(base_item)}。"
            feedback_tone = "warning"
        elif not has_enough_mats:
            status = "missing"
            status_label = "素材不足"
            action_enabled = False
            mats_desc_list = []
            for m_id, m_qty in recipe["materials"].items():
                mats_desc_list.append(f"{game.item_name(m_id)} x{m_qty} (目前 x{state.get('inventory', {}).get(m_id, 0)})")
            action_disabled_reason = "需要 " + "、".join(mats_desc_list) + "。"
            feedback_text = "製作材料還不夠，先去迷宮搜集一下吧。"
            feedback_tone = "warning"
        else:
            # For base_item recipes, status can be 'limited' if base item has limited count
            if base_item:
                status = "limited"
                status_label = "基底有限"
            else:
                status = "craftable"
                status_label = "可製作"
            action_enabled = True
            action_disabled_reason = None
            feedback_text = f"米菈微笑道：「看來你的材料與基底都齊了，隨時可以製作 {recipe['name']}。」"
            feedback_tone = "success"

        recipe_rows.append({
            "recipe_id": r_id,
            "title": recipe["name"],
            "category": category,
            "category_label": category_label,
            "status": status,
            "status_label": status_label,
            "output_summary": output_summary,
            "owned_summary": owned_summary,
            "max_count": craft_limit,
            "gold": recipe["gold"],
            "disabled_reason": action_disabled_reason,
        })

        # Build detailed result message for synthesis confirmation
        mats_used = "、".join([f"{game.item_name(m_id)} x{m_qty}" for m_id, m_qty in recipe["materials"].items()])
        base_used = f"與{game.item_name(base_item)}" if base_item else ""
        result_msg = f"成功合成{recipe['name']}！扣除金幣 {recipe['gold']}G，消耗{mats_used}{base_used}。"

        recipe_details[r_id] = {
            "title": recipe["name"],
            "description": recipe.get("desc", f"取得 {output_summary}。"),
            "effect": recipe.get("desc", f"取得 {output_summary}。"),
            "base_note": f"基底：需要 {game.item_name(base_item)} x1，可消耗背包或已裝備物。" if base_item else "基底：不需要基底裝備。",
            "notes": "合成會消耗素材與金幣。",
            "outputs": [
                { "item_id": out_item_id, "label": out_name, "quantity": out_qty }
            ],
            "primary_action": {
                "action_id": "craft_recipe",
                "label": f"合成{recipe['name']}",
                "enabled": action_enabled,
                "disabled_reason": action_disabled_reason,
                "payload": { "recipe_id": r_id },
                "result_message": result_msg if action_enabled else f"無法合成：{action_disabled_reason}"
            },
            "ready_feedback": {
                "tone": feedback_tone,
                "speaker": "米菈",
                "text": feedback_text
            },
            "blocked_feedback": {
                "tone": feedback_tone,
                "speaker": "米菈",
                "text": feedback_text
            },
        }

        # Build requirement rows
        r_rows = [
            {
                "id": "recipe_access",
                "icon_label": "方",
                "label": "配方取得條件",
                "required_value": game.recipe_unlock_condition(r_id),
                "current_value": "已取得" if unlocked else "未取得",
                "status": "met" if unlocked else "missing",
                "status_label": "已滿足" if unlocked else "未滿足",
                "disabled_reason": None if unlocked else game.recipe_locked_reason(state, r_id),
            },
            {
                "id": "gold",
                "icon_label": "G",
                "label": "金幣",
                "required_value": f"{recipe['gold']}G",
                "current_value": f"{gold}G",
                "status": "met" if has_enough_gold else "missing",
                "status_label": "已滿足" if has_enough_gold else "不足",
                "disabled_reason": None if has_enough_gold else f"需要 {recipe['gold']}G，目前 {gold}G。"
            }
        ]

        if base_item:
            owned_base_qty = game.recipe_base_owned_count(state, recipe)
            is_equipped = any(
                equipment_base_id(state, reference_id) == base_item
                for reference_id in state.get("equipment", {}).values()
            )
            if is_equipped:
                curr_val_str = f"x{owned_base_qty}（已裝備）"
            else:
                curr_val_str = f"x{owned_base_qty}"

            r_rows.append({
                "id": f"base_{base_item}",
                "icon_label": "基",
                "label": f"基底裝備：{game.item_name(base_item)}",
                "required_value": "x1",
                "current_value": curr_val_str,
                "status": "limited" if has_base_item else "missing",
                "status_label": "可消耗" if has_base_item else "不足",
                "disabled_reason": None if has_base_item else f"需要基底 {game.item_name(base_item)}。"
            })

        for m_id, m_qty in recipe["materials"].items():
            owned_qty = state.get("inventory", {}).get(m_id, 0)
            met = owned_qty >= m_qty
            r_rows.append({
                "id": m_id,
                "icon_label": icon_labels.get(m_id, game.item_name(m_id)[0] if m_id in ITEMS or m_id in EQUIPMENT or m_id in MATERIALS else "物"),
                "label": game.item_name(m_id),
                "required_value": f"x{m_qty}",
                "current_value": f"x{owned_qty}",
                "status": "met" if met else "missing",
                "status_label": "已滿足" if met else "不足",
                "disabled_reason": None if met else f"需要 {game.item_name(m_id)} x{m_qty}，目前 x{owned_qty}。"
            })

        requirement_rows[r_id] = r_rows

    category_tabs = [
        { "id": "all", "label": "全部", "count": len(mira_recipes), "selected": True, "enabled": True },
        { "id": "equipment", "label": "裝備", "count": equipment_count, "selected": False, "enabled": equipment_count > 0 },
        { "id": "battle", "label": "戰術道具", "count": battle_count, "selected": False, "enabled": battle_count > 0 }
    ]

    return {
        "screen_id": "facility_synthesis_screen",
        "facility_id": "synthesis",
        "title": "米菈合成屋 (Live)",
        "subtitle": "角色資源狀態、素材消耗與配方製作皆由 Python 遊戲引擎同步。",
        "npc": {
            "id": "mira",
            "name": "米菈",
            "role": "合成屋主人，擅長把素材、基底裝備與金幣整理成可執行的配方。"
        },
        "resource_strip": resource_strip(state),
        "category_tabs": category_tabs,
        "selected_category_id": "all",
        "selected_recipe_id": default_recipe_id,
        "recipe_rows": recipe_rows,
        "recipe_details": recipe_details,
        "requirement_rows": requirement_rows,
        "feedback_message": {
            "tone": "info",
            "speaker": "米菈",
            "text": "選一張配方，右側會顯示金幣、素材與基底裝備狀態。"
        },
        "empty_state": {
            "message": "目前沒有符合分類的可用配方。"
        }
    }
