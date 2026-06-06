from __future__ import annotations

from typing import Any
from data import MAGIC_BOOKS, SKILLS
from . import game
from .formatting import item_name


def get_magic_book_category(book_id: str) -> tuple[str, str]:
    cli_cat = game.magic_shop_category(book_id)
    if cli_cat == "攻擊魔法":
        return "damage", "攻擊魔法"
    if cli_cat == "恢復魔法":
        return "heal", "恢復魔法"
    if cli_cat == "輔助魔法":
        return "buff", "輔助魔法"
    return "special", "特殊魔法"


def get_magic_book_status_key(state: dict, book_id: str) -> str:
    book = MAGIC_BOOKS[book_id]
    skill_id = book["skill"]
    if skill_id in state.get("learned_skills", []):
        return "learned"
    if state.get("job") not in book["jobs"]:
        return "job_restricted"
    if state.get("level", 1) < book["level"]:
        return "level_restricted"
    return "learnable"


def get_magic_book_description(book_id: str, name: str, skill_desc: str) -> str:
    descs = {
        "book_spark": "凝聚精純的初階火元素術式，從法杖前端射出燃燒的火花。是法師探險時最可靠的基礎進攻魔法。",
        "book_ice_needle": "凝聚周遭的水元素並凝結成銳利的冰針，能有效穿透敌人的防線。對付焦石礦坑與燼印深窟的火系魔物效果卓越。",
        "book_minor_heal": "吟唱光之神聖禱詞，降下溫和的魔法微光撫平傷口。牧師最基礎的治療法術。",
        "book_guardian_rune": "以魔力在前方空域構築虛擬的幾何土盾，暫時提升受術者的防禦耐性。",
        "book_quickstep": "為雙足加持微弱風行之術，能更容易閃避敵人攻擊，或在戰場上搶先做出應對。",
        "book_cinder_mark": "釋放火山微粒覆蓋於敵方目標身上，留下容易被高熱點燃的隱密標記。火花術的絕佳增傷搭配。"
    }
    return descs.get(book_id, f"記載著{name}術式的古老魔法書。")


def magic_shop_screen_model(state: dict[str, Any]) -> dict[str, Any]:
    gold = state.get("gold", 0)
    level = state.get("level", 1)
    job = state.get("job", "")

    categories_counts = {"all": 0, "damage": 0, "heal": 0, "buff": 0, "special": 0}
    for b_id in MAGIC_BOOKS:
        categories_counts["all"] += 1
        cat_id, _ = get_magic_book_category(b_id)
        if cat_id in categories_counts:
            categories_counts[cat_id] += 1

    category_tabs = [
        { "id": "all", "label": "全部魔法", "count": categories_counts["all"], "enabled": True },
        { "id": "damage", "label": "攻擊魔法", "count": categories_counts["damage"], "enabled": True },
        { "id": "heal", "label": "恢復魔法", "count": categories_counts["heal"], "enabled": True },
        { "id": "buff", "label": "輔助魔法", "count": categories_counts["buff"], "enabled": True },
        { "id": "special", "label": "特殊魔法", "count": categories_counts["special"], "enabled": True }
    ]

    list_rows = []
    book_details = {}
    requirement_rows = {}
    primary_actions = {}

    book_ids = list(MAGIC_BOOKS.keys())
    for b_id in book_ids:
        if b_id not in MAGIC_BOOKS:
            continue
        book = MAGIC_BOOKS[b_id]
        skill_id = book["skill"]
        skill = SKILLS.get(skill_id, {})

        price = game.magic_book_price(state, b_id)
        cat_id, cat_label = get_magic_book_category(b_id)
        status_key = get_magic_book_status_key(state, b_id)

        row_enabled = (status_key == "learnable")
        disabled_reason = None
        if status_key == "learned":
            disabled_reason = "已學會"
        elif status_key == "job_restricted":
            disabled_reason = "職業不符"
        elif status_key == "level_restricted":
            disabled_reason = f"等級不足 Lv{book['level']}"

        badges = []
        if b_id == "book_spark":
            badges.append({ "badge_id": "hot", "label": "熱門", "kind": "info" })
        elif b_id == "book_cinder_mark":
            badges.append({ "badge_id": "rare", "label": "高階", "kind": "warning" })

        list_rows.append({
            "id": f"row_{b_id}",
            "book_id": b_id,
            "title": f"《{book['name']}》",
            "category": cat_id,
            "summary": f"學會{skill.get('name', '')}。{skill.get('desc', '')}",
            "price": price,
            "mp": skill.get("mp", 0),
            "req_level": book["level"],
            "jobs": book["jobs"],
            "status": status_key,
            "enabled": row_enabled,
            "disabled_reason": disabled_reason,
            "badges": badges
        })

        description = get_magic_book_description(b_id, book["name"], skill.get("desc", ""))

        book_details[b_id] = {
            "book_id": b_id,
            "title": f"《{book['name']}》",
            "category_label": cat_label,
            "skill_name": skill.get("name", ""),
            "mp_cost": skill.get("mp", 0),
            "description": description,
            "effect_summary": skill.get("desc", ""),
            "jobs": book["jobs"],
            "req_level": book["level"],
            "price": price,
            "status": status_key,
            "disabled_reason": disabled_reason
        }

        reqs = []
        gold_status = "met" if gold >= price else "unmet"
        gold_disabled = None if gold >= price else "金幣不足"
        reqs.append({
            "id": "gold",
            "label": "金幣需求",
            "required_value": f"{price}G",
            "current_value": f"{gold}G",
            "status": gold_status,
            "disabled_reason": gold_disabled
        })

        level_status = "met" if level >= book["level"] else "unmet"
        level_disabled = None if level >= book["level"] else "等級限制"
        reqs.append({
            "id": "level",
            "label": "等級限制",
            "required_value": f"Lv {book['level']}",
            "current_value": f"Lv {level}",
            "status": level_status,
            "disabled_reason": level_disabled
        })

        for mat_id, req_qty in book["materials"].items():
            owned_qty = state.get("inventory", {}).get(mat_id, 0)
            mat_status = "met" if owned_qty >= req_qty else "unmet"
            mat_disabled = None if owned_qty >= req_qty else "素材不足"
            reqs.append({
                "id": mat_id,
                "label": item_name(mat_id),
                "required_value": f"{req_qty} 個",
                "current_value": f"{owned_qty} 個",
                "status": mat_status,
                "disabled_reason": mat_disabled
            })

        requirement_rows[b_id] = reqs

        has_enough_gold = gold >= price
        has_enough_mats = game.can_pay_items(state, book["materials"])
        action_enabled = (status_key == "learnable") and has_enough_gold and has_enough_mats

        action_label = f"學習{skill.get('name', '')} ({price}G)"
        action_disabled_reason = None
        if status_key == "learned":
            action_label = "已學會此法術"
            action_disabled_reason = "已學會"
        elif status_key == "job_restricted":
            action_label = "職業不符"
            action_disabled_reason = "職業不符"
        elif status_key == "level_restricted":
            action_label = "等級不足"
            action_disabled_reason = f"等級不足 Lv{book['level']}"
        elif not has_enough_gold:
            action_label = "金幣不足"
            action_disabled_reason = "金幣不足"
        elif not has_enough_mats:
            action_label = "素材不足"
            action_disabled_reason = "素材不足"

        result_message = None
        if action_enabled:
            result_message = f"你成功研讀了《{book['name']}》！扣除金幣 {price}G 與素材，已永久學會法術「{skill.get('name', '')}」！"

        primary_actions[b_id] = {
            "action_id": "learn_magic_book",
            "label": action_label,
            "enabled": action_enabled,
            "disabled_reason": action_disabled_reason,
            "payload": { "book_id": b_id, "price": price },
            "result_message": result_message
        }

    feedback_text = "「願星辰指引你的靈魂，冒險者。選中魔法書可開始研讀。」"
    feedback_tone = "info"
    if gold < 100:
        feedback_text = "「金幣似乎不太夠呢，在星燈下可以多積累一些歷練再來研讀。」"
        feedback_tone = "warning"

    feedback_message = {
        "tone": feedback_tone,
        "speaker": "伊芙",
        "text": feedback_text
    }

    selected_book_id = "book_spark"
    learnable_books = [r["book_id"] for r in list_rows if r["status"] == "learnable"]
    if learnable_books:
        selected_book_id = learnable_books[0]
    elif list_rows:
        selected_book_id = list_rows[0]["book_id"]

    return {
        "screen_id": "facility_magic_shop_screen",
        "facility_id": "magic_shop",
        "title": "星燈魔法商店 (Live)",
        "subtitle": "願星辰指引你的靈魂，冒險者。在這裡可以購買並學習永久的戰鬥魔法與輔助技能。",
        "npc": {
            "id": "eve",
            "name": "伊芙",
            "role": "星燈魔法商店的館長，專注於古老星辰與元素術式的研究。",
            "guidance": "伊芙輕輕敲了敲書脊：「願星辰指引你的靈魂，冒險者。今天想要解讀哪一本古老術式？」",
            "portrait_placeholder": "EV"
        },
        "player_summary": {
            "name": state.get("name", ""),
            "level": level,
            "job": job,
            "gold": gold
        },
        "category_tabs": category_tabs,
        "selected_category_id": "all",
        "selected_book_id": selected_book_id,
        "list_rows": list_rows,
        "book_details": book_details,
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
