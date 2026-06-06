from __future__ import annotations

from typing import Any
from . import game
from .gui_presentation import resource_strip
from .previews import get_preview_relics


def relic_preview_screen_model(state: dict[str, Any]) -> dict[str, Any]:
    game.ensure_state_defaults(state)

    strip = resource_strip(state)

    relics = get_preview_relics()
    slots = []

    ash_relic = next((r for r in relics if r.get("source") == "灰燼裂谷調查線索" or r.get("name") == "灰燼護符"), None)

    if ash_relic:
        unlocked = game.relic_unlock_met(state, ash_relic.get("unlock"))
        slots.append({
            "element_id": "fire",
            "label": "🔥 火之印記碎片",
            "relic_name": ash_relic["name"],
            "collected": 3 if unlocked else 0,
            "required": 3,
            "unlocked": unlocked,
            "active": unlocked,
            "ancient_text": f"「當三碎聚首，薪火重燃，深谷之衛方可安息...」三個散落的火焰碎片在此相聚，流動著溫熱的餘溫魔能。被動效果（預期）：{ash_relic['effect_preview']}"
        })
    else:
        slots.append({
            "element_id": "fire",
            "label": "🔥 火之印記碎片",
            "relic_name": "未完成的火印核心",
            "collected": 3 if state.get("inventory", {}).get("key_fire_mark_shard", 0) >= 3 else state.get("inventory", {}).get("key_fire_mark_shard", 0),
            "required": 3,
            "unlocked": state.get("inventory", {}).get("key_fire_mark_shard", 0) >= 3,
            "active": state.get("inventory", {}).get("key_fire_mark_shard", 0) >= 3,
            "ancient_text": "「當三碎聚首，薪火重燃...」三個散落的火焰碎片在此相聚，流動著溫熱 Genes / 餘溫魔能。被動效果（預估）：火屬性抗性 +15% (實際套用依 CLI runtime 為準)。"
        })

    slots.append({
        "element_id": "water",
        "label": "💧 潮汐之淚",
        "relic_name": "海神淚滴",
        "collected": 0,
        "required": 1,
        "unlocked": False,
        "active": False,
        "ancient_text": "「深海之瞳，凝視深淵...」尚未解鎖。碎片可能掉落於沉沒遺跡或海岸巢穴中。正式聖物玩法尚未開放。"
    })
    slots.append({
        "element_id": "wind",
        "label": "🌪️ 風暴之羽",
        "relic_name": "天羽核心",
        "collected": 0,
        "required": 1,
        "unlocked": False,
        "active": False,
        "ancient_text": "「狂嵐不息，撕裂天穹...」尚未解鎖。需要在北方高原的峭壁鳥巢中尋得風羽線索。正式聖物玩法尚未開放。"
    })

    return {
        "screen_id": "relic_preview_screen",
        "title": "古代遺物展示台 (Relic Altar)",
        "subtitle": "檢視與解讀冒險中取得的古代元素聖物與碎片印記。",
        "resource_strip": strip,
        "slots": slots
    }
