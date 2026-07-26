from __future__ import annotations

from typing import Any
from . import game
from .gui_presentation import resource_strip
from data import PROMOTIONS, SKILLS


def temple_screen_model(state: dict[str, Any]) -> dict[str, Any]:
    game.ensure_state_defaults(state)

    strip = resource_strip(state)

    # Check if player has at least 30G
    has_gold = state.get("gold", 0) >= 30
    moon_well = {
        "label": "月神之井",
        "description": "汲取蘊藏魔力的露水進行祈福，可隨機獲得全隊屬性微幅抗性加成。",
        "cost": 30,
        "enabled": has_gold,
        "payload": { "altar_action": "pray", "cost": 30 }
    }

    choices = [
        (promo_id, promo)
        for promo_id, promo in PROMOTIONS.items()
        if promo.get("source_job") == state.get("job") and promo.get("status") == "formal"
    ]

    current_promo_id = state.get("promotion_id")
    promotions = []
    for promo_id, promo in choices:
        reqs = []
        for req in promo.get("requirements", []):
            satisfied = game.promotion_requirement_met(state, req)
            kind = req.get("kind")
            if kind == "level":
                current_str = f"目前 Lv{state.get('level', 1)} / 達 Lv{req.get('value', 12)}"
            elif kind == "unlock":
                unlocked = game.is_unlocked(state, req.get("key"))
                current_str = "已探索" if unlocked else "未探索"
            elif kind == "quest":
                completed = req.get("key") in state.get("completed_quests", [])
                current_str = "已完成" if completed else "未完成"
            elif kind == "item":
                owned = state.get("inventory", {}).get(req.get("key"), 0)
                current_str = "已取得" if owned > 0 else "未持有"
            else:
                current_str = "已達成" if satisfied else "未達成"

            reqs.append({
                "name": req.get("label", ""),
                "current": current_str,
                "satisfied": satisfied
            })

        # 主被動技能預覽
        active_skill = SKILLS.get(promo["active_skill_id"], {})
        passive_skill = SKILLS.get(promo["passive_skill_id"], {})
        description = (
            f"{promo.get('summary', '')} "
            f"| 主動技能：[{active_skill.get('name')}] - {active_skill.get('desc')} "
            f"| 被動技能：[{passive_skill.get('name')}] - {passive_skill.get('desc')}"
        )

        # 檢查轉職按鈕狀態
        if current_promo_id:
            if current_promo_id == promo_id:
                enabled = False
                label = f"{promo.get('name')} (已晉升)"
                disabled_reason = "您已晉升此職業。"
            else:
                enabled = False
                label = promo.get("name")
                disabled_reason = "您已宣誓晉升為其他職業。"
        else:
            # 檢查條件是否全數達成
            all_satisfied = all(game.promotion_requirement_met(state, req) for req in promo.get("requirements", []))
            enabled = all_satisfied
            label = promo.get("name")
            disabled_reason = None if all_satisfied else "未達成所有晉升要求條件。"

        promotions.append({
            "class_id": promo_id,
            "label": label,
            "description": description,
            "requirements": reqs,
            "enabled": enabled,
            "disabled_reason": disabled_reason
        })

    inquiries = []
    if game.should_show_fire_mark_church_bridge(state):
        inquiries.append({
            "inquiry_id": "fire_mark_church_bridge",
            "action_id": "fire_mark_church_bridge",
            "label": "向賽恩展示印記碎片",
            "description": "向賽恩大祭司展示獲得的三枚火焰碎片，以尋求線索。",
            "enabled": True,
            "payload": {},
            "response_text": "賽恩凝視著碎片，輕聲說道：『工會看不懂它，是因為這不是委託紀錄裡的東西。它不普通，但我還不能斷言它是什麼。我要花點時間查閱舊文獻。先把碎片收好。等我整理出線索，再回神殿找我。』"
        })
    elif game.should_show_fire_mark_church_lookup(state):
        inquiries.append({
            "inquiry_id": "fire_mark_church_lookup",
            "action_id": "fire_mark_church_lookup",
            "label": "詢問火之印記核心",
            "description": "向賽恩大祭司詢問古代文獻查閱結果與火之印記核心的事。",
            "enabled": True,
            "payload": {},
            "response_text": "賽恩指著舊文獻，輕聲說道：『查到了。這三枚碎片不是完整的火之印記，而是它尚未完成的核心。去神殿後側的聖物調查台吧。那裡能讓碎片承接成真正的火之聖印。』"
        })
    elif state.get("flags", {}).get("boss_glen_defeated"):
        inquiries.append({
            "inquiry_id": "fire_mark_sayn_comment",
            "action_id": "fire_mark_sayn_comment",
            "label": "詢問火之印記",
            "description": "向賽恩大祭司詢問關於火之印記與碎片的來歷。",
            "enabled": False,
            "payload": {},
            "response_text": "賽恩看著你手中的火之印記碎片：『這還不是完整的印記。但神殿記得它的溫度。若你找到更多線索，再回來找我。』"
        })

    return {
        "screen_id": "temple_screen",
        "title": "轉職神殿 (Live)",
        "subtitle": "在此沐浴月神光華，進行職業晉升宣誓或查閱古代碑文。",
        "resource_strip": strip,
        "moon_well": moon_well,
        "promotions": promotions,
        "inquiries": inquiries
    }
