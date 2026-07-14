from __future__ import annotations

from typing import Any
from . import game
from .gui_presentation import resource_strip


ELEMENT_ORDER = {
    "fire": 0,
    "ice": 1,
    "earth": 2,
    "thunder": 3,
}


def _relic_slot(state: dict[str, Any], relic_id: str, relic: dict[str, Any]) -> dict[str, Any]:
    required = game.relic_source_required(relic)
    enshrined = game.relic_enshrined(state, relic)
    ready = game.relic_ready_to_enshrine(state, relic)
    selected_passive = game.selected_relic_passive(state, relic_id, relic)
    passive_choices = [
        {
            "choice_id": choice["id"],
            "label": choice["label"],
            "summary": choice["summary"],
            "selected": choice["id"] == (selected_passive or {}).get("id"),
        }
        for choice in game.relic_passive_choices(relic)
    ]
    collected = required if enshrined else min(game.relic_source_count(state, relic), required)
    ancient_text = relic["complete_text"] if enshrined else (relic["ready_text"] if ready else relic["locked_text"])
    status_label = ("已安置，已選被動" if selected_passive else "已安置，待選被動") if enshrined else ("可安置" if ready else "待調查")

    return {
        "relic_id": relic_id,
        "element_id": relic.get("element_id", "unknown"),
        "label": relic.get("label", relic.get("name", "")),
        "relic_name": relic.get("name", ""),
        "collected": collected,
        "required": required,
        "unlocked": ready or enshrined,
        "ready": ready,
        "enshrined": enshrined,
        "active": selected_passive is not None,
        "selected_passive_id": (selected_passive or {}).get("id"),
        "selected_passive_label": (selected_passive or {}).get("label"),
        "passive_choices": passive_choices,
        "passive_enabled": enshrined,
        "passive_disabled_reason": None if enshrined else "需先安置此聖印。",
        "ancient_text": ancient_text,
        "source": relic.get("source", ""),
        "summary": relic.get("summary", ""),
        "effect_preview": relic.get("effect_preview", ""),
        "source_item_id": relic.get("source_item_id"),
        "seal_item_id": relic.get("seal_item_id"),
        "action_label": relic.get("action_label", "安置聖印"),
        "disabled_reason": None if ready or enshrined else game.relic_disabled_reason(state, relic),
        "status_label": status_label,
    }


def relic_preview_screen_model(state: dict[str, Any]) -> dict[str, Any]:
    game.ensure_state_defaults(state)

    strip = resource_strip(state)

    relic_entries = sorted(
        game.preview_relic_entries(),
        key=lambda entry: ELEMENT_ORDER.get(entry[1].get("element_id", ""), 99),
    )
    slots = [_relic_slot(state, relic_id, relic) for relic_id, relic in relic_entries]

    return {
        "screen_id": "relic_preview_screen",
        "title": "聖物調查台 (Relic Preview)",
        "subtitle": "合成並安置 Fire / Ice / Earth / Thunder 四元素聖印；已安置聖印可於轉職神殿免費選擇被動。",
        "resource_strip": strip,
        "slots": slots
    }
