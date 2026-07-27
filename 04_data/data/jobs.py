from __future__ import annotations

# Growth allocations are authored in points. Keep the conversion here so the
# job table remains the single source of truth for both level cadences.
GROWTH_POINT_RATES = {
    "max_hp": 2.0,
    "max_mp": 1.0,
    "attack": 1.0,
    "magic_attack": 1.0,
    "defense": 1.0,
    "magic_defense": 1.0,
    "agility": 1.0,
    "crit": 0.1,
    "effect_accuracy": 0.1,
}


def per_three_level_points(per_level_points: dict[str, float]) -> dict[str, float]:
    """Derive the milestone allocation from the frozen per-level table."""
    return {stat: points / 3 for stat, points in per_level_points.items()}



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
        "growth_points": {"max_hp": 4.05, "max_mp": 0.75, "attack": 1.5, "magic_attack": 0.0, "defense": 3.3, "magic_defense": 0.75, "agility": 0.15, "crit": 3.0, "effect_accuracy": 0.0},
        "base_skills": ["skill_power_slash"],
    },
    "法師": {
        "base": {
            "max_hp": 110,
            "max_mp": 55,
            "attack": 8,
            "magic_attack": 15,
            "defense": 12,
            "magic_defense": 10,
            "agility": 9,
            "effect_accuracy": 0,
            "crit": 4,
        },
        "growth_points": {"max_hp": 2.0, "max_mp": 5.0, "attack": 0.0, "magic_attack": 5.0, "defense": 0.75, "magic_defense": 2.25, "agility": 0.0, "crit": 0.0, "effect_accuracy": 0.0},
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
        "growth_points": {"max_hp": 3.0, "max_mp": 0.0, "attack": 1.95, "magic_attack": 0.0, "defense": 2.7, "magic_defense": 0.75, "agility": 1.5, "crit": 2.85, "effect_accuracy": 2.25},
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
        "growth_points": {"max_hp": 3.4, "max_mp": 2.25, "attack": 2.25, "magic_attack": 2.3, "defense": 1.5, "magic_defense": 3.0, "agility": 0.3, "crit": 0.0, "effect_accuracy": 0.0},
        "base_skills": ["skill_blessed_touch", "skill_sanctified_decay", "skill_regeneration"],
    },
}
