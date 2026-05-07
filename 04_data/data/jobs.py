from __future__ import annotations



JOBS = {
    "劍士": {
        "base": {
            "max_hp": 120,
            "max_mp": 20,
            "attack": 17,
            "defense": 11,
            "agility": 8,
            "accuracy": 90,
            "crit": 5,
        },
        "growth": {"max_hp": 12, "max_mp": 3, "attack": 4, "defense": 3, "agility": 1},
        "extra_every_3": {"attack": 2},
        "base_skills": ["skill_power_slash"],
    },
    "法師": {
        "base": {
            "max_hp": 80,
            "max_mp": 55,
            "attack": 9,
            "defense": 6,
            "agility": 9,
            "accuracy": 88,
            "crit": 4,
        },
        "growth": {"max_hp": 7, "max_mp": 8, "attack": 2, "defense": 1, "agility": 2},
        "extra_every_3": {"max_mp": 5},
        "base_skills": ["skill_arcane_bolt"],
    },
    "盜賊": {
        "base": {
            "max_hp": 95,
            "max_mp": 28,
            "attack": 13,
            "defense": 7,
            "agility": 15,
            "accuracy": 93,
            "crit": 10,
        },
        "growth": {"max_hp": 9, "max_mp": 4, "attack": 3, "defense": 2, "agility": 4},
        "extra_every_3": {"crit": 1},
        "base_skills": ["skill_backstab"],
    },
    "牧師": {
        "base": {
            "max_hp": 105,
            "max_mp": 42,
            "attack": 10,
            "defense": 9,
            "agility": 8,
            "accuracy": 90,
            "crit": 4,
        },
        "growth": {"max_hp": 10, "max_mp": 6, "attack": 2, "defense": 2, "agility": 1},
        "extra_every_3": {"defense": 2},
        "base_skills": ["skill_blessed_touch"],
    },
}
