from __future__ import annotations



JOBS = {
    "劍士": {
        "base": {
            "max_hp": 120,
            "max_mp": 20,
            "attack": 17,
            "magic_attack": 3,
            "defense": 13,
            "magic_defense": 7,
            "agility": 8,
            "effect_accuracy": 0,
            "crit": 5,
        },
        "growth": {"max_hp": 12, "max_mp": 3, "attack": 4, "magic_attack": 1, "defense": 3, "magic_defense": 1, "agility": 1},
        "extra_every_3": {"attack": 2},
        "base_skills": ["skill_power_slash"],
    },
    "法師": {
        "base": {
            "max_hp": 80,
            "max_mp": 55,
            "attack": 8,
            "magic_attack": 15,
            "defense": 5,
            "magic_defense": 10,
            "agility": 9,
            "effect_accuracy": 0,
            "crit": 4,
        },
        "growth": {"max_hp": 7, "max_mp": 8, "attack": 1, "magic_attack": 5, "defense": 1, "magic_defense": 2, "agility": 2},
        "extra_every_3": {"max_mp": 5},
        "base_skills": ["skill_arcane_bolt"],
    },
    "盜賊": {
        "base": {
            "max_hp": 92,
            "max_mp": 28,
            "attack": 13,
            "magic_attack": 4,
            "defense": 7,
            "magic_defense": 7,
            "agility": 15,
            "effect_accuracy": 12,
            "crit": 10,
        },
        "growth": {"max_hp": 9, "max_mp": 4, "attack": 3, "magic_attack": 1, "defense": 2, "magic_defense": 1, "agility": 4, "effect_accuracy": 1},
        "extra_every_3": {"crit": 1},
        "base_skills": ["skill_backstab", "skill_toxic_edge"],
    },
    "牧師": {
        "base": {
            "max_hp": 130,
            "max_mp": 42,
            "attack": 8,
            "magic_attack": 12,
            "defense": 8,
            "magic_defense": 12,
            "agility": 8,
            "effect_accuracy": 0,
            "crit": 4,
        },
        "growth": {"max_hp": 12, "max_mp": 7, "attack": 1, "magic_attack": 4, "defense": 1, "magic_defense": 3, "agility": 1},
        "extra_every_3": {"defense": 2},
        "base_skills": ["skill_blessed_touch", "skill_sanctified_decay", "skill_regeneration"],
    },
}
