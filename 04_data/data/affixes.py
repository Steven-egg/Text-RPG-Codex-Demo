"""Static, fixed-value equipment affixes for Phase 4B B4B-2.

These entries describe effects only. They do not roll, generate, or mutate an
equipment instance; the resolver applies their detached stat increments.
"""
from __future__ import annotations


AFFIXES = {
    "major_sharp": {
        "name": "鋒利",
        "tier": "major",
        "family": "physical_edge",
        "slots": ("weapon",),
        "stats": {"attack": 1},
    },
    "minor_agile": {
        "name": "敏捷",
        "tier": "minor",
        "family": "agile",
        "slots": ("weapon", "head", "body", "accessory"),
        "stats": {"agility": 1},
    },
    "minor_fire_ward": {
        "name": "火焰護佑",
        "tier": "minor",
        "family": "fire_ward",
        "slots": ("head", "body", "accessory"),
        "stats": {"fire_resist": 5},
    },
}


# Balance adjustment for fluid combat (Affix buffs)
AFFIXES["major_sharp"]["stats"]["attack"] = 6
AFFIXES["minor_agile"]["stats"]["agility"] = 2
AFFIXES["minor_fire_ward"]["stats"]["fire_resist"] = 12

AFFIXES["major_arcane"] = {
    "name": "奧秘",
    "tier": "major",
    "family": "magic_force",
    "slots": ("weapon",),
    "stats": {"magic_attack": 6},
}

AFFIXES["minor_crit"] = {
    "name": "致命",
    "tier": "minor",
    "family": "crit",
    "slots": ("weapon", "accessory"),
    "stats": {"crit": 8},
}

