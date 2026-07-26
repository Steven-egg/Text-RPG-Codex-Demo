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

# Quality-system affixes.  These are the numerical SSOT; the lexicon remains
# name-only and is never consulted for gameplay values.
AFFIXES.update({
    "major_edge": {"name": "銳刃", "tier": "major", "family": "edge", "slots": ("weapon", "head"), "stats": {"attack": 1}},
    "major_tempo": {"name": "疾行", "tier": "major", "family": "tempo", "slots": ("weapon", "head"), "stats": {"agility": 1}},
    "major_guard": {"name": "守護", "tier": "major", "family": "guard", "slots": ("head", "body", "accessory"), "stats": {"defense": 1}},
    "major_magic_guard": {"name": "祈護", "tier": "major", "family": "magic_guard", "slots": ("head", "body", "accessory"), "stats": {"magic_defense": 1}},
    "major_status_guard": {"name": "清醒", "tier": "major", "family": "status_guard", "slots": ("head", "body", "accessory"), "stats": {"effect_accuracy": 1}},
    "minor_precision": {"name": "精準", "tier": "minor", "family": "precision", "slots": ("weapon", "head"), "stats": {"effect_accuracy": 1}},
    "minor_element_ward": {"name": "護符", "tier": "minor", "family": "element_ward", "slots": ("head", "body", "accessory"), "stats": {"fire_resist": 1}},
    "minor_status_guard": {"name": "定心", "tier": "minor", "family": "status_minor", "slots": ("head", "body", "accessory"), "stats": {"magic_defense": 1}},
    "minor_guard": {"name": "堅固", "tier": "minor", "family": "guard_minor", "slots": ("head", "body", "accessory"), "stats": {"defense": 1}},
})

AFFIXES["minor_crit"] = {
    "name": "致命",
    "tier": "minor",
    "family": "crit",
    "slots": ("weapon", "accessory"),
    "stats": {"crit": 8},
}

# Warrior/Mage quality affixes.  The generic resolver exposes these values as
# effective equipment stats; combat consumes the three runtime-only keys.
AFFIXES.update({
    "major_charge_skill_bonus": {
        "name": "蓄鋒", "tier": "major", "family": "charge_skill_bonus",
        "slots": ("weapon",), "stats": {"physical_charge_skill_bonus": 4},
    },
    "minor_charge_cap": {
        "name": "極蓄", "tier": "minor", "family": "charge_cap",
        "slots": ("weapon",), "stats": {"physical_charge_cap": 1},
    },
    "minor_charge_gain": {
        "name": "疾蓄", "tier": "minor", "family": "charge_gain",
        "slots": ("weapon",), "stats": {"physical_charge_gain_chance": 25},
    },
    "minor_elemental_magic_direct": {
        "name": "奧能", "tier": "minor", "family": "elemental_magic_direct",
        "slots": ("weapon",), "stats": {"elemental_magic_direct_percent": 6},
    },
    "minor_magic_guard_weapon": {
        "name": "法幕", "tier": "minor", "family": "magic_guard_weapon",
        "slots": ("weapon",), "stats": {"magic_defense": 1},
    },
    "minor_quality_fire_ward": {
        "name": "火焰護符", "tier": "minor", "family": "quality_fire_ward",
        "slots": ("head", "body", "accessory"), "stats": {"fire_resist": 5},
    },
    "minor_quality_ice_ward": {
        "name": "冰霜護符", "tier": "minor", "family": "quality_ice_ward",
        "slots": ("head", "body", "accessory"), "stats": {"ice_resist": 5},
    },
    "minor_quality_earth_ward": {
        "name": "地脈護符", "tier": "minor", "family": "quality_earth_ward",
        "slots": ("head", "body", "accessory"), "stats": {"earth_resist": 5},
    },
    "minor_quality_thunder_ward": {
        "name": "雷鳴護符", "tier": "minor", "family": "quality_thunder_ward",
        "slots": ("head", "body", "accessory"), "stats": {"thunder_resist": 5},
    },
    "minor_quality_final_ward": {
        "name": "深淵護符", "tier": "minor", "family": "quality_final_ward",
        "slots": ("head", "body", "accessory"),
        "stats": {"fire_resist": 2, "ice_resist": 2, "earth_resist": 2, "thunder_resist": 2},
    },
})
