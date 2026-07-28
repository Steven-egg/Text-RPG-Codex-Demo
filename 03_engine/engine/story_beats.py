from __future__ import annotations

from typing import Any, Mapping

from data.dialogues import DEFAULT_CONTEXT, STORY_BEATS, render_template

from .display import render_panel


STORY_BEAT_KINDS = {"prologue", "region_transition", "boss_before", "boss_after", "ending"}
STORY_BEAT_TONES = {"neutral", "warning", "victory", "ending"}
STORY_BEAT_KEYS = {"id", "kind", "title", "lines", "dismiss_label", "tone"}
MAIN_STORY_BOSS_IDS = {
    "boss_cinder_seal_sentinel",
    "boss_ice_final_seal_lord",
    "boss_earth_deep_leyline_lord",
    "boss_thunder_crown_storm_lord",
    "boss_final_demon_king",
}
REGION_STORY_BEAT_IDS = {
    "ice": "region.enter.ice",
    "earth": "region.enter.earth",
    "thunder": "region.enter.thunder",
    "final": "region.enter.final",
}


def story_seen_flag(beat_id: str) -> str:
    return f"story_seen.{beat_id}"


def region_story_beat_id(region_id: str) -> str | None:
    return REGION_STORY_BEAT_IDS.get(region_id)


def boss_story_beat_id(boss_id: str, timing: str) -> str | None:
    if boss_id not in MAIN_STORY_BOSS_IDS or timing not in {"before", "after"}:
        return None
    return f"boss.{timing}.{boss_id}"


def build_story_beat(beat_id: str, context: Mapping[str, Any] | None = None) -> dict[str, Any] | None:
    template = STORY_BEATS.get(beat_id)
    if template is None:
        return None

    render_context = {**DEFAULT_CONTEXT, **(context or {})}
    lines = render_template(template["lines"], render_context)
    beat = {
        "id": beat_id,
        "kind": template["kind"],
        "title": render_template(template["title"], render_context),
        "lines": lines,
        "dismiss_label": render_template(template["dismiss_label"], render_context),
        "tone": template["tone"],
    }
    _validate_story_beat(beat)
    return beat


def take_story_beat(
    state: dict[str, Any],
    beat_id: str | None,
    *,
    context: Mapping[str, Any] | None = None,
) -> dict[str, Any] | None:
    if beat_id is None:
        return None
    flags = state.get("flags")
    if not isinstance(flags, dict):
        flags = {}
        state["flags"] = flags
    seen_flag = story_seen_flag(beat_id)
    if flags.get(seen_flag):
        return None
    beat = build_story_beat(beat_id, context)
    if beat is None:
        return None
    flags[seen_flag] = True
    return beat


def show_story_beat(beat: dict[str, Any] | None) -> None:
    if beat is None:
        return
    border_style = {
        "neutral": "cyan",
        "warning": "yellow",
        "victory": "green",
        "ending": "magenta",
    }[beat["tone"]]
    render_panel(beat["title"], beat["lines"], border_style=border_style)


def _validate_story_beat(beat: dict[str, Any]) -> None:
    if set(beat) != STORY_BEAT_KEYS:
        raise ValueError(f"Invalid story beat keys: {beat.get('id', '<unknown>')}")
    if beat["kind"] not in STORY_BEAT_KINDS:
        raise ValueError(f"Invalid story beat kind: {beat['kind']}")
    if beat["tone"] not in STORY_BEAT_TONES:
        raise ValueError(f"Invalid story beat tone: {beat['tone']}")
    if not isinstance(beat["title"], str) or not beat["title"]:
        raise ValueError("Story beat title must be non-empty text.")
    if not isinstance(beat["dismiss_label"], str) or not beat["dismiss_label"]:
        raise ValueError("Story beat dismiss_label must be non-empty text.")
    lines = beat["lines"]
    if not isinstance(lines, list) or not 2 <= len(lines) <= 5:
        raise ValueError("Story beat lines must contain two to five entries.")
    if any(not isinstance(line, str) or not line or "\n" in line or "<" in line or ">" in line for line in lines):
        raise ValueError("Story beat lines must contain plain, non-empty single-line text.")
