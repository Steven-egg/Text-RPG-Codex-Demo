from __future__ import annotations

from typing import Any
from . import game
from .gui_presentation import resource_strip
from .story_beats import take_story_beat


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
    selected_passive = None
    passive_choices = []
    collected = required if enshrined else min(game.relic_source_count(state, relic), required)
    ancient_text = relic["complete_text"] if enshrined else (relic["ready_text"] if ready else relic["locked_text"])
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
        "passive_enabled": False,
        "passive_disabled_reason": "聖印效果仍在前瞻階段，尚未實裝。",
        "ancient_text": ancient_text,
        "source": relic.get("source", ""),
        "summary": relic.get("summary", ""),
        "effect_preview": relic.get("effect_preview", ""),
        "source_item_id": relic.get("source_item_id"),
        "seal_item_id": relic.get("seal_item_id"),
        "action_label": "主線前瞻（效果未實裝）",
        "disabled_reason": "聖印效果仍在前瞻階段，尚未實裝。",
        "status_label": "主線進度前瞻",
    }


def relic_preview_screen_model(state: dict[str, Any]) -> dict[str, Any]:
    game.ensure_state_defaults(state)
    preview_beat = take_story_beat(state, "guidance.relic_preview")

    strip = resource_strip(state)

    relic_entries = sorted(
        game.preview_relic_entries(),
        key=lambda entry: ELEMENT_ORDER.get(entry[1].get("element_id", ""), 99),
    )
    slots = [_relic_slot(state, relic_id, relic) for relic_id, relic in relic_entries]

    return {
        "screen_id": "relic_preview_screen",
        "title": "聖物調查台 (Relic Preview)",
        "subtitle": "Fire / Ice / Earth / Thunder 聖印用於主線進度前瞻；效果尚未實裝。",
        "resource_strip": strip,
        "slots": slots,
        "story_beat": preview_beat,
    }
