from __future__ import annotations

import random
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from data import MONSTERS  # noqa: E402
from engine.game import calc_player_damage, player_attack, tick_effects  # noqa: E402
from engine.relic import select_relic_passive  # noqa: E402
from engine.state import create_state, ensure_state_defaults, get_stats  # noqa: E402


RELIC_IDS = (
    "relic_fire_seal",
    "relic_ice_marker_source",
    "relic_earth_marker_source",
    "relic_thunder_marker_source",
)


def enshrined_state(job: str = "劍士") -> dict:
    state = create_state("Relic Tester", job)
    for relic_id, flag in zip(
        RELIC_IDS,
        ("fire_seal_enshrined", "ice_seal_enshrined", "earth_seal_enshrined", "thunder_seal_enshrined"),
        strict=True,
    ):
        state["flags"][flag] = True
    return state


def choose(state: dict, relic_id: str, choice_id: str) -> None:
    result = select_relic_passive(state, relic_id, choice_id)
    assert result["status"] == "selected", result


def test_state_compatibility() -> None:
    state = create_state("Legacy", "劍士")
    state.pop("relic_passives")
    ensure_state_defaults(state)
    assert state["relic_passives"] == {}
    state["flags"]["fire_seal_enshrined"] = True
    state["relic_passives"] = {"relic_fire_seal": "fire_direct_damage", "relic_ice_marker_source": "ice_max_mp", "bad": "choice"}
    ensure_state_defaults(state)
    assert state["relic_passives"] == {"relic_fire_seal": "fire_direct_damage"}
    assert select_relic_passive(state, "relic_ice_marker_source", "ice_max_mp")["status"] == "blocked"


def test_selection_and_stats() -> None:
    state = enshrined_state()
    choose(state, "relic_fire_seal", "fire_all_resist")
    choose(state, "relic_ice_marker_source", "ice_all_resist")
    choose(state, "relic_earth_marker_source", "earth_all_resist")
    choose(state, "relic_thunder_marker_source", "thunder_all_resist")
    stats = get_stats(state)
    assert all(stats[key] == 20 for key in ("fire_resist", "ice_resist", "earth_resist", "thunder_resist"))

    state = enshrined_state()
    base = get_stats(state)
    choose(state, "relic_ice_marker_source", "ice_max_mp")
    choose(state, "relic_earth_marker_source", "earth_max_hp")
    choose(state, "relic_thunder_marker_source", "thunder_crit")
    stats = get_stats(state)
    assert stats["max_hp"] > base["max_hp"]
    assert stats["max_mp"] > base["max_mp"]
    assert stats["crit"] == base["crit"] + 8
    choose(state, "relic_thunder_marker_source", "thunder_effect_accuracy")
    assert get_stats(state)["effect_accuracy"] == base["effect_accuracy"] + 15


def test_damage_sustain_and_dot() -> None:
    enemy = deepcopy(MONSTERS["mon_moss_rat"])
    baseline = enshrined_state()
    boosted = enshrined_state()
    choose(boosted, "relic_fire_seal", "fire_direct_damage")
    choose(boosted, "relic_thunder_marker_source", "thunder_direct_physical_damage")
    random.seed(20260713)
    normal, _ = calc_player_damage(baseline, enemy, None, {}, {})
    random.seed(20260713)
    enhanced, _ = calc_player_damage(boosted, enemy, None, {}, {})
    assert enhanced > normal

    lifesteal = enshrined_state()
    choose(lifesteal, "relic_fire_seal", "fire_physical_lifesteal")
    lifesteal["current_hp"] = 1
    before = lifesteal["current_hp"]
    result = player_attack(lifesteal, enemy, enemy["hp"], None, {}, {})
    assert result.damage > 0
    assert lifesteal["current_hp"] >= before

    dot_state = enshrined_state("盜賊")
    choose(dot_state, "relic_earth_marker_source", "earth_dot_damage")
    buffs = {"bleed": 1, "_dot_data": {"bleed": {"multiplier": 0.45, "damage_type": "physical", "element": "physical"}}}
    _, boosted_dot = tick_effects(dot_state, {}, buffs, enemy)
    base_state = enshrined_state("盜賊")
    buffs = {"bleed": 1, "_dot_data": {"bleed": {"multiplier": 0.45, "damage_type": "physical", "element": "physical"}}}
    _, base_dot = tick_effects(base_state, {}, buffs, enemy)
    assert boosted_dot > base_dot

    regen_state = enshrined_state("牧師")
    choose(regen_state, "relic_earth_marker_source", "earth_healing_regen")
    regen_state["current_hp"] = 1
    tick_effects(regen_state, {"regeneration": 1, "_regen_data": {"amount": 10, "multiplier": 0}}, {})
    assert regen_state["current_hp"] == 13


def main() -> None:
    test_state_compatibility()
    test_selection_and_stats()
    test_damage_sustain_and_dot()
    print("Relic Passive v1 deterministic tests ok!")


if __name__ == "__main__":
    main()
