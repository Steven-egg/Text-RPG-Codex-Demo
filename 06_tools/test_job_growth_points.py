from __future__ import annotations

"""Focused checks for the unified four-job point-growth contract."""

import math
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from data import EQUIPMENT, JOBS, SKILLS  # noqa: E402
from data.jobs import GROWTH_POINT_RATES, per_three_level_points  # noqa: E402
from engine.game import apply_weapon_effect, direct_damage_roll  # noqa: E402
from engine.state import create_state, get_stats  # noqa: E402


LEVELS = (8, 16, 24, 32, 40)
EXPECTED_POINTS = {
    "warrior": {"max_hp": 4.05, "max_mp": 0.75, "attack": 3.0, "magic_attack": 0.0, "defense": 3.3, "magic_defense": 0.75, "agility": 0.15, "crit": 3.0, "effect_accuracy": 0.0},
    "mage": {"max_hp": 2.0, "max_mp": 5.0, "attack": 0.0, "magic_attack": 5.0, "defense": 0.75, "magic_defense": 2.25, "agility": 0.0, "crit": 0.0, "effect_accuracy": 0.0},
    "rogue": {"max_hp": 3.0, "max_mp": 0.0, "attack": 1.95, "magic_attack": 0.0, "defense": 2.7, "magic_defense": 0.75, "agility": 1.5, "crit": 2.85, "effect_accuracy": 2.25},
    "cleric": {"max_hp": 3.4, "max_mp": 2.25, "attack": 2.25, "magic_attack": 2.3, "defense": 1.5, "magic_defense": 3.0, "agility": 0.3, "crit": 0.0, "effect_accuracy": 0.0},
}


def _job_name(job_key: str) -> str:
    # Stable table order is the runtime's four core-job order.
    return tuple(JOBS)[("warrior", "mage", "rogue", "cleric").index(job_key)]


def test_point_tables_and_milestones() -> None:
    for job_key, expected in EXPECTED_POINTS.items():
        job = JOBS[_job_name(job_key)]
        assert "growth" not in job and "extra_every_3" not in job
        assert job["growth_points"] == expected
        assert math.isclose(sum(job["growth_points"].values()), 15.0, abs_tol=1e-12)
        milestone = per_three_level_points(job["growth_points"])
        assert all(math.isclose(milestone[key], value / 3, abs_tol=1e-12) for key, value in expected.items())
        assert math.isclose(sum(milestone.values()), 5.0, abs_tol=1e-12)


def test_bare_stats_follow_point_formula_at_required_levels() -> None:
    for job_key, points in EXPECTED_POINTS.items():
        job = JOBS[_job_name(job_key)]
        for level in LEVELS:
            state = create_state("Growth QA", _job_name(job_key))
            state["level"] = level
            state["equipment"] = {slot: None for slot in state["equipment"]}
            stats = get_stats(state)
            milestones = (level - 1) // 3
            for stat, rate in GROWTH_POINT_RATES.items():
                expected = job["base"].get(stat, 0) + rate * points[stat] * (level - 1 + milestones / 3)
                assert math.isclose(stats[stat], expected, abs_tol=1e-9), (job_key, level, stat, stats[stat], expected)


def test_effect_accuracy_is_limited_to_physical_on_hit_statuses() -> None:
    source = Path(ROOT / "03_engine" / "engine" / "game.py").read_text(encoding="utf-8")
    function_source = source[source.index("def apply_weapon_effect"):source.index("def skill_menu")]
    assert "effect_accuracy" in function_source
    assert "effect_accuracy" not in source[source.index("def apply_dot"):source.index("def apply_weapon_effect")]
    on_hit_skills = [skill for skill in SKILLS.values() if skill.get("on_hit")]
    on_hit_followups = [equipment["normal_attack_followup"] for equipment in EQUIPMENT.values() if equipment.get("normal_attack_followup", {}).get("on_hit")]
    assert on_hit_skills and on_hit_followups
    assert all(skill.get("stat") == "attack" and skill["on_hit"].get("damage_type") == "physical" for skill in on_hit_skills)
    assert all(followup["on_hit"].get("damage_type") == "physical" for followup in on_hit_followups)
    rogue = create_state("Growth QA", _job_name("rogue"))
    rogue["equipment"] = {slot: None for slot in rogue["equipment"]}
    rogue["level"] = 40
    events, status = apply_weapon_effect(
        rogue,
        {"name": "QA target", "race": "beast", "physical_status_resist": 0},
        SKILLS["skill_backstab"]["on_hit"],
        {},
    )
    assert events and status in {None, "bleed"}


def test_direct_damage_agility_formula_and_cap() -> None:
    expected_chances = {0: 0.0, 30: 4.5, 100: 15.0, 200: 30.0}
    for agility, chance in expected_chances.items():
        # A roll exactly above the high-damage chance must use the normal band.
        with patch("engine.game.random.random", return_value=(chance + 0.01) / 100), patch("engine.game.random.uniform", return_value=0.91) as uniform:
            assert direct_damage_roll(agility) == 0.91
            uniform.assert_called_once_with(0.80, 1.10)
        # A roll below any non-zero chance must use the agile high-damage band.
        if chance:
            with patch("engine.game.random.random", return_value=0.0), patch("engine.game.random.uniform", return_value=1.23) as uniform:
                assert direct_damage_roll(agility) == 1.23
                uniform.assert_called_once_with(1.15, 1.45)
    assert min(30.0, 500 * 0.15) == 30.0


def main() -> None:
    test_point_tables_and_milestones()
    test_bare_stats_follow_point_formula_at_required_levels()
    test_effect_accuracy_is_limited_to_physical_on_hit_statuses()
    test_direct_damage_agility_formula_and_cap()
    print("job growth point checks ok")


if __name__ == "__main__":
    main()
