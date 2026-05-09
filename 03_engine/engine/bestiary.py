from __future__ import annotations

from data import DUNGEONS


def monster_locations(monster_id: str) -> list[str]:
    locations = []
    for dungeon in DUNGEONS.values():
        if monster_id in dungeon.get("monsters", []) or dungeon.get("boss") == monster_id:
            locations.append(dungeon["name"])
    return locations
