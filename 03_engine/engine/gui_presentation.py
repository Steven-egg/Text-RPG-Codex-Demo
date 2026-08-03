from __future__ import annotations

from typing import Any
from .state import ensure_state_defaults, get_stats


def display_resource(value: object) -> str:
    """Render resource values without leaking fractional implementation detail."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    return str(int(number)) if number.is_integer() else f"{number:.2f}".rstrip("0").rstrip(".")


def resource_strip(state: dict[str, Any]) -> list[dict[str, str]]:
    ensure_state_defaults(state)
    stats = get_stats(state)
    name = state.get("name", "")
    job_key = state.get("job")
    job_label = str(job_key)
    level = state.get("level", 1)

    current_hp = state.get("current_hp", stats["max_hp"])
    max_hp = stats["max_hp"]

    current_mp = state.get("current_mp", stats["max_mp"])
    max_mp = stats["max_mp"]

    gold = state.get("gold", 0)
    guild_points = state.get("guild_points", 0)

    return [
        {"id": "hero", "label": f"{name} / {job_label} Lv{level}", "tone": "primary"},
        {"id": "hp", "label": f"HP {display_resource(current_hp)}/{display_resource(max_hp)}", "tone": "healthy"},
        {"id": "mp", "label": f"MP {display_resource(current_mp)}/{display_resource(max_mp)}", "tone": "mana"},
        {"id": "gold", "label": f"{gold}G", "tone": "gold"},
        {"id": "guild_points", "label": f"Guild {guild_points}", "tone": "neutral"},
    ]
