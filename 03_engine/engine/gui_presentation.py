from __future__ import annotations

from typing import Any
from . import game


def resource_strip(state: dict[str, Any]) -> list[dict[str, str]]:
    game.ensure_state_defaults(state)
    stats = game.get_stats(state)
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
        {"id": "hp", "label": f"HP {current_hp}/{max_hp}", "tone": "healthy"},
        {"id": "mp", "label": f"MP {current_mp}/{max_mp}", "tone": "mana"},
        {"id": "gold", "label": f"{gold}G", "tone": "gold"},
        {"id": "guild_points", "label": f"Guild {guild_points}", "tone": "neutral"},
    ]
