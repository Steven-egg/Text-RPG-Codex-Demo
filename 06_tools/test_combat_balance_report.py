from __future__ import annotations

"""Focused measurement-semantics checks for ``test_combat_balance.py``.

These checks validate the QA tool, not the game's balance.  Passing this file
does not mean that the benchmark targets are met.
"""

import csv
import importlib.util
import io
import json
import math
import random
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "06_tools" / "test_combat_balance.py"
SPEC = importlib.util.spec_from_file_location("combat_balance", MODULE_PATH)
assert SPEC and SPEC.loader
balance = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = balance
SPEC.loader.exec_module(balance)


EXPECTED_TARGETS = {
    "fire": {"normal_actions": (2, 5), "boss_actions": (6, 10), "boss_min_final_hp_ratio": 0.25},
    "ice": {"normal_actions": (2, 5), "boss_actions": (7, 12), "boss_min_final_hp_ratio": 0.25},
    "earth": {"normal_actions": (3, 6), "boss_actions": (8, 14), "boss_min_final_hp_ratio": 0.20},
    "thunder": {"normal_actions": (3, 6), "boss_actions": (9, 16), "boss_min_final_hp_ratio": 0.15},
    "final": {"normal_actions": (4, 7), "boss_actions": (12, 20), "boss_min_final_hp_ratio": 0.10},
}


def _assert_schema(records: list[dict]) -> None:
    assert records
    assert set(records[0]) == set(balance.RECORD_FIELDS)
    for record in records:
        assert set(record) == set(balance.RECORD_FIELDS)
        assert record["schema_version"] == balance.SCHEMA_VERSION
        assert record["rng_stream_id"] == balance._comparison_seed(
            record["region"], record["job"], record["target_type"], record["seed"],
        )
        assert record["result"] in {"victory", "player_death", "timeout"}
        assert record["final_mp"] >= 0
        assert record["enemy_actions"] <= record["player_actions"]
        assert record["enemy_hp_remaining_at_end"] >= 0
        shares = record["direct_damage_share"] + record["dot_damage_share"] + record["item_damage_share"]
        has_damage = record["direct_damage"] + record["dot_damage"] + record["item_damage"]
        assert abs(shares - (1.0 if has_damage else 0.0)) <= 0.001

        if record["result"] == "victory":
            assert record["final_hp"] > 0
            assert record["death_turn"] is None
            assert record["enemy_hp_remaining_on_death"] is None
            assert record["enemy_hp_remaining_at_end"] == 0
        elif record["result"] == "player_death":
            assert record["final_hp"] == 0
            assert record["death_turn"] is not None
            assert record["enemy_hp_remaining_on_death"] == record["enemy_hp_remaining_at_end"]
        else:
            assert record["death_turn"] is None
            assert record["enemy_hp_remaining_on_death"] is None
            assert record["enemy_hp_remaining_at_end"] > 0

        # Effective damage cannot consume more HP than the player had available,
        # including effective healing received earlier in the fight.
        assert record["incoming_damage"] <= record["initial_hp"] + record["healing"]
        assert record["final_hp"] == record["initial_hp"] - record["incoming_damage"] + record["healing"]
        assert balance.MONSTERS[record["enemy_id"]]["hp"] == (
            record["direct_damage"]
            + record["dot_damage"]
            + record["item_damage"]
            + record["enemy_hp_remaining_at_end"]
        )

        equipment_profile = "naked" if record["layer"] == "B0" else ("weapon_only" if record["layer"] == "B1" else "full")
        loadout, _complete, _carry = balance._loadout_status(record["region"], record["job"], equipment_profile)
        assert record["gear_grind_equivalent"] == balance._gear_grind_equivalent(loadout, record["region"])

        assert record["equipment_total_power"] == round(record["equipment_base_power"] + record["affix_budget_spent"], 2)
        if record["layer"] == "B6":
            assert record["affix_budget_spent"] <= record["quality_budget_cap"] + 0.001
            assert isinstance(record["quality_saturated"], bool)


def _assert_exact_coverage(records: list[dict]) -> None:
    assert len(records) == 2_320
    ids = [record["scenario_id"] for record in records]
    assert len(ids) == len(set(ids))

    counts = Counter(
        (record["layer"], record["region"], record["job"], record["target_type"], record["seed"])
        for record in records
    )
    for layer in balance.LAYERS:
        for region in balance.REGIONS:
            for job in balance.JOBS:
                for target in ("normal", "boss"):
                    for seed in balance.DEFAULT_SEEDS:
                        expected = 4 if layer == "B6" else (1 if layer != "B5" or region == "fire" else 3)
                        assert counts[(layer, region, job, target, seed)] == expected

    layer_counts = Counter(record["layer"] for record in records)
    assert layer_counts == {"B0": 200, "B1": 200, "B2": 200, "B3": 200, "B4": 200, "B5": 520, "B6": 800}
    assert {record["promotion_profile"] for record in records if record["layer"] == "B5"} == {
        "none", "promotion_branch_a", "promotion_branch_b",
    }
    assert {record["equipment_profile_id"] for record in records if record["layer"] == "B6"} == {
        "gear_floor", "gear_median", "gear_ceiling", "gear_legendary_sensitivity",
    }


def _assert_rendering(records: list[dict]) -> None:
    csv_rows = list(csv.DictReader(io.StringIO(balance.render_records(records, "csv"))))
    json_rows = json.loads(balance.render_records(records, "json"))
    assert len(csv_rows) == len(records) == len(json_rows)
    assert list(csv_rows[0]) == list(balance.RECORD_FIELDS)


def _global_snapshots() -> dict[str, object]:
    return {
        "equipment": deepcopy(balance.EQUIPMENT),
        "monsters": deepcopy(balance.MONSTERS),
        "skills": deepcopy(balance.SKILLS),
        "relics": deepcopy(balance.RELICS),
        "loadouts": deepcopy(balance.FULL_LOADOUTS),
    }


def _assert_globals_unchanged(before: dict[str, object]) -> None:
    assert balance.EQUIPMENT == before["equipment"]
    assert balance.MONSTERS == before["monsters"]
    assert balance.SKILLS == before["skills"]
    assert balance.RELICS == before["relics"]
    assert balance.FULL_LOADOUTS == before["loadouts"]


def _assert_determinism_and_state(first_records: list[dict], before: dict[str, object], rng_before: object) -> None:
    first = balance.render_records(first_records, "json")
    _assert_globals_unchanged(before)
    assert random.getstate() == rng_before
    second = balance.render_records(balance.build_records(balance.LAYERS, balance.DEFAULT_SEEDS), "json")
    assert first == second
    _assert_globals_unchanged(before)
    assert random.getstate() == rng_before

    item_id = "weapon_iron_sword"
    original_stats = deepcopy(balance.EQUIPMENT[item_id]["stats"])
    with balance._temporary_equipment_stats({item_id: {"attack": 1}}):
        assert balance.EQUIPMENT[item_id]["stats"]["attack"] == original_stats["attack"] + 1
    assert balance.EQUIPMENT[item_id]["stats"] == original_stats
    try:
        with balance._temporary_equipment_stats({item_id: {"attack": 1}}):
            raise RuntimeError("restore probe")
    except RuntimeError:
        pass
    assert balance.EQUIPMENT[item_id]["stats"] == original_stats


def _assert_comparative_rng() -> None:
    key = balance._comparison_seed("ice", "rogue", "boss", balance.DEFAULT_SEEDS[0])
    assert "B3" not in key and "promotion" not in key and "gear" not in key
    original = random.getstate()
    with balance._common_random_stream("ice", "rogue", "boss", balance.DEFAULT_SEEDS[0]):
        first = [random.random() for _ in range(8)]
    with balance._common_random_stream("ice", "rogue", "boss", balance.DEFAULT_SEEDS[0]):
        second = [random.random() for _ in range(8)]
    assert first == second
    assert random.getstate() == original


def _assert_comparative_monotonicity(records: list[dict]) -> None:
    lookup = {
        (
            record["layer"], record["region"], record["job"], record["target_type"], record["seed"],
            record["promotion_profile"], record["equipment_profile_id"],
        ): record
        for record in records
    }

    def assert_not_worse(lower: dict, higher: dict) -> None:
        if lower["result"] == "victory":
            assert higher["result"] == "victory"
            assert higher["player_actions"] <= lower["player_actions"]

    for region in balance.REGIONS:
        for job in balance.JOBS:
            for target in ("normal", "boss"):
                for seed in balance.DEFAULT_SEEDS:
                    b3 = lookup[("B3", region, job, target, seed, "none", "full")]
                    b4 = lookup[("B4", region, job, target, seed, "none", "full")]
                    assert b3["rng_stream_id"] == b4["rng_stream_id"]
                    assert_not_worse(b3, b4)
                    if region != "fire":
                        none = lookup[("B5", region, job, target, seed, "none", "full")]
                        branch_a = lookup[("B5", region, job, target, seed, "promotion_branch_a", "full")]
                        branch_b = lookup[("B5", region, job, target, seed, "promotion_branch_b", "full")]
                        assert len({none["rng_stream_id"], branch_a["rng_stream_id"], branch_b["rng_stream_id"]}) == 1
                        assert_not_worse(none, branch_a)
                        assert_not_worse(branch_a, branch_b)
                    floor = lookup[("B6", region, job, target, seed, "none", "gear_floor")]
                    median = lookup[("B6", region, job, target, seed, "none", "gear_median")]
                    ceiling = lookup[("B6", region, job, target, seed, "none", "gear_ceiling")]
                    legendary = lookup[("B6", region, job, target, seed, "none", "gear_legendary_sensitivity")]
                    assert len({floor["rng_stream_id"], median["rng_stream_id"], ceiling["rng_stream_id"], legendary["rng_stream_id"]}) == 1
                    assert_not_worse(floor, median)
                    assert_not_worse(median, ceiling)
                    assert_not_worse(ceiling, legendary)


def _assert_runtime_tick_and_effective_vitals(records: list[dict]) -> None:
    assert not [record for record in records if record["result"] == "victory" and record["final_hp"] == 0]
    assert balance._effective_hp_loss(10, -999, 100) == 10
    assert balance._effective_hp_loss(10, 7, 100) == 3

    state, _loadout, _complete, _carry, _relics = balance._build_state("warrior", "fire", "full", False, False)
    state["current_hp"] = 1
    buffs = {"burn": 1}
    balance.game.tick_effects(state, buffs, {})
    assert state["current_hp"] <= 0
    assert balance._round_outcome(state["current_hp"], 10) == "player_death"
    assert balance._round_outcome(0, 0) == "player_death"
    assert balance._round_outcome(1, 0) == "victory"

    regen_state, _loadout, _complete, _carry, _relics = balance._build_state("cleric", "fire", "full", False, False)
    regen_state["current_hp"] = 1
    regen = balance.SKILLS["skill_regeneration"]
    regen_buffs = {
        "burn": 1,
        "regeneration": 1,
        "_regen_data": {"amount": regen["amount"], "multiplier": regen["multiplier"]},
    }
    balance.game.tick_effects(regen_state, regen_buffs, {})
    assert regen_state["current_hp"] > 0
    assert balance._round_outcome(regen_state["current_hp"], 10) is None


def _assert_timeout_semantics() -> None:
    original = balance.MAX_PLAYER_ACTIONS
    balance.MAX_PLAYER_ACTIONS = 1
    try:
        record = balance.measure_scenario(
            layer="B0", region_id="fire", job_key="warrior", target_type="normal",
            seed=balance.DEFAULT_SEEDS[0], equipment_profile="naked", rotation=False, relics=False,
        )
    finally:
        balance.MAX_PLAYER_ACTIONS = original
    assert record["result"] == "timeout"
    assert record["death_turn"] is None
    assert record["enemy_hp_remaining_on_death"] is None
    assert record["enemy_hp_remaining_at_end"] > 0

    json_record = json.loads(balance.render_records([record], "json"))[0]
    assert json_record["death_turn"] is None
    assert json_record["enemy_hp_remaining_on_death"] is None
    assert json_record["enemy_hp_remaining_at_end"] == record["enemy_hp_remaining_at_end"]

    csv_record = next(csv.DictReader(io.StringIO(balance.render_records([record], "csv"))))
    assert csv_record["death_turn"] == ""
    assert csv_record["enemy_hp_remaining_on_death"] == ""
    assert csv_record["enemy_hp_remaining_at_end"] == str(record["enemy_hp_remaining_at_end"])


def _assert_benchmark_targets(records: list[dict]) -> None:
    assert balance.BENCHMARK_TARGETS == EXPECTED_TARGETS
    for region, target in EXPECTED_TARGETS.items():
        for target_type, key in (("normal", "normal_actions"), ("boss", "boss_actions")):
            low, high = target[key]
            sample = {
                "region": region,
                "target_type": target_type,
                "result": "victory",
                "player_actions": low,
                "final_hp_ratio": target["boss_min_final_hp_ratio"],
            }
            assert balance.evaluate_benchmark_record(sample)["action_target_met"]
            sample["player_actions"] = high
            assert balance.evaluate_benchmark_record(sample)["action_target_met"]
            sample["player_actions"] = high + 1
            assert not balance.evaluate_benchmark_record(sample)["action_target_met"]

    # Directly evaluate the actual pre-promotion comparison layers.  The QA
    # check validates target semantics and keeps B5 overlays out of baseline
    # pass/fail; it intentionally does not assert that the game meets targets.
    baseline = [record for record in records if record["layer"] in {"B0", "B1", "B2", "B3", "B4"}]
    assert len(baseline) == 1_000
    evaluations = [balance.evaluate_benchmark_record(record) for record in baseline]
    assert len(evaluations) == len(baseline)
    assert all(set(result) == {"action_target_met", "boss_hp_target_met"} for result in evaluations)


def _rotation_choice(job: str, region: str, enemy: dict, state: dict, player_buffs: dict, enemy_buffs: dict, turn: int, boss: bool, counts: dict) -> tuple[str, str | None]:
    return balance._choose_rotation_action(job, region, enemy, state, player_buffs, enemy_buffs, turn, boss, counts)


def _assert_canonical_rotation() -> None:
    counts = {"hp": 0, "mp": 0, "battle": 0}
    mage_fire, *_ = balance._build_state("mage", "fire", "full", False, False)
    assert _rotation_choice("mage", "fire", balance.MONSTERS[balance.REGIONS["fire"]["normal"]], mage_fire, {}, {}, 1, False, counts) == ("skill", "skill_ice_needle")
    mage_thunder, *_ = balance._build_state("mage", "thunder", "full", False, False)
    assert _rotation_choice("mage", "thunder", balance.MONSTERS[balance.REGIONS["thunder"]["normal"]], mage_thunder, {}, {}, 1, False, counts) == ("skill", "skill_earth_01")

    rogue, *_ = balance._build_state("rogue", "ice", "full", False, False)
    assert _rotation_choice("rogue", "ice", {"race": "beast"}, rogue, {}, {}, 1, False, counts) == ("skill", "skill_backstab")
    assert _rotation_choice("rogue", "ice", {"race": "plant"}, rogue, {}, {}, 1, False, counts) == ("skill", "skill_toxic_edge")
    assert _rotation_choice("rogue", "ice", {"race": "construct"}, rogue, {}, {}, 1, False, counts) == ("normal", None)

    warrior, *_ = balance._build_state("warrior", "earth", "full", False, False)
    assert _rotation_choice("warrior", "earth", balance.MONSTERS[balance.REGIONS["earth"]["normal"]], warrior, {}, {}, 1, False, counts) == ("normal", None)
    assert _rotation_choice("warrior", "earth", balance.MONSTERS[balance.REGIONS["earth"]["normal"]], warrior, {"_physical_charge": 3}, {}, 4, False, counts) == ("skill", "skill_earth_05")

    cleric, *_ = balance._build_state("cleric", "thunder", "full", False, True)
    enemy = balance.MONSTERS[balance.REGIONS["thunder"]["boss"]]
    assert _rotation_choice("cleric", "thunder", enemy, cleric, {}, {}, 1, True, counts) == ("skill", "skill_sanctified_decay")
    cleric["current_hp"] = 1
    dot = {balance.SKILLS["skill_sanctified_decay"]["name"]: 3}
    assert _rotation_choice("cleric", "thunder", enemy, cleric, {}, dot, 2, True, counts) == ("skill", "skill_regeneration")
    cleric["current_hp"] = balance.get_stats(cleric)["max_hp"]
    assert _rotation_choice("cleric", "thunder", enemy, cleric, {"regeneration": 3}, dot, 3, True, counts) == ("item", "item_armor_piercer")


def _assert_promotion_overlay() -> None:
    assert balance._promotion_multiplier("none", "skill") == 1.0
    assert balance._promotion_multiplier("promotion_branch_a", "skill") == 1.05
    assert balance._promotion_multiplier("promotion_branch_b", "normal") == 1.05
    assert balance._promotion_multiplier("promotion_branch_b", "skill") == 1.10
    assert balance._promotion_multiplier("promotion_branch_b", "dot") == 1.10
    assert balance._promotion_multiplier("promotion_branch_b", "skill") <= 1.10


def _direct_item_use(state: dict, boss: bool, enemy_buffs: dict, enemy: dict):
    with balance._menu_choice(1):
        return balance.game.combat_item_menu(state, boss, enemy_buffs, enemy)


def _assert_item_adapter_parity() -> None:
    enemy = deepcopy(balance.MONSTERS["boss_thunder_crown_storm_lord"])
    for item_id in ("item_potion_m", "item_focus_drop", "item_armor_piercer"):
        base, _loadout, _complete, _carry, _relics = balance._build_state("cleric", "thunder", "full", False, True)
        base["inventory"] = {item_id: 2}
        if item_id == "item_potion_m":
            base["current_hp"] = 1
        elif item_id == "item_focus_drop":
            base["current_mp"] = 0
        adapter_state = deepcopy(base)
        direct_state = deepcopy(base)
        adapter_buffs: dict = {}
        direct_buffs: dict = {}
        adapter_result = balance.use_tool_item_adapter(adapter_state, True, adapter_buffs, enemy, item_id)
        direct_result = _direct_item_use(direct_state, True, direct_buffs, enemy)
        assert adapter_state == direct_state
        assert adapter_buffs == direct_buffs
        assert adapter_result.damage == direct_result.damage
        assert adapter_result.events == direct_result.events
        assert adapter_result.summary == direct_result.summary
        assert adapter_state["inventory"].get(item_id, 0) == 1
        if item_id == "item_potion_m":
            assert adapter_state["current_hp"] > base["current_hp"] and adapter_result.damage == 0
        elif item_id == "item_focus_drop":
            assert adapter_state["current_mp"] == 12 and adapter_result.damage == 0
        else:
            assert adapter_result.damage == max(8, math.ceil(enemy["hp"] * 0.08))
            assert adapter_buffs["defense_down"] == 3


def _assert_audit_categories() -> None:
    assert "SLOT_ILLEGAL" in balance._classify_equipment("bad_slot", {"slot": "hand", "stats": {"attack": 1}})
    assert "SANDBOX_ONLY_STAT" in balance._classify_equipment("sandbox", {"slot": "head", "stats": {"accuracy": 1}})
    attack_body = {"slot": "body", "stats": {"attack": 1}}
    resist_weapon = {"slot": "weapon", "stats": {"fire_resist": 1}}
    assert "SLOT_ILLEGAL" in balance._classify_equipment("attack_body", attack_body)
    assert "SLOT_ILLEGAL" in balance._classify_equipment("resist_weapon", resist_weapon)
    capped = {"slot": "accessory", "stats": {"crit": balance.PER_ITEM_STAT_CAPS["crit"] + 1}}
    assert "STACKING_ILLEGAL" in balance._classify_equipment("capped", capped)
    stacking = {"slot": "body", "stats": {}, "normal_attack_followup": {"multiplier": 0.2, "on_hit": {"status": "bleed"}}}
    assert "STACKING_ILLEGAL" in balance._classify_equipment("stacking", stacking)
    assert "MANUAL_EFFECT_BUDGET" in balance._classify_equipment("stacking", stacking)
    assert "OVER_BUDGET" in balance._classify_equipment("budget", {"slot": "weapon", "stats": {}}, 11, 10)
    assert "crit" in balance._classify_loadout(balance.FULL_LOADOUTS["ice"]["rogue"])

    leather = balance.EQUIPMENT["armor_leather_armor"]
    expected = sum(max(0, value) * balance.POWER_WEIGHTS.get(stat, 0.0) for stat, value in leather["stats"].items())
    assert balance._equipment_power(["armor_leather_armor"]) == round(expected, 2)

    audit = balance.audit_equipment()
    assert audit["manual_effect_head_slot_isolate"]
    assert all(entry["other_slots_equal"] for entry in audit["manual_effect_head_slot_isolate"].values())


def _flatten(adjustments: dict[str, dict[str, int]]) -> dict[tuple[str, str], int]:
    return {(item_id, stat): value for item_id, stats in adjustments.items() for stat, value in stats.items()}


def _assert_quality_affix_semantics() -> None:
    assert balance.QUALITY_ENVELOPES == {"normal": 0.00, "fine": 0.05, "rare": 0.10, "epic": 0.15, "legendary": 0.20}
    profile_ids = ("gear_floor", "gear_median", "gear_ceiling", "gear_legendary_sensitivity")
    expected_qualities = ("normal", "rare", "epic", "legendary")
    for region, loadouts in balance.FULL_LOADOUTS.items():
        for job, loadout in loadouts.items():
            profiles = [balance._affix_profile(job, loadout, profile) for profile in profile_ids]
            assert tuple(profile[1] for profile in profiles) == expected_qualities, (region, job)
            spent = [profile[4] for profile in profiles]
            assert spent == sorted(spent), (region, job, spent)
            for profile in profiles:
                cap = round(profile[3] * balance.QUALITY_ENVELOPES[profile[1]], 2)
                assert profile[4] <= cap + 0.001, (region, job, profile[1], profile[4], cap)
            for previous, current in zip(profiles, profiles[1:]):
                previous_adjustments = _flatten(previous[0])
                current_adjustments = _flatten(current[0])
                assert all(
                    current_adjustments.get(key, 0) >= value
                    for key, value in previous_adjustments.items()
                ), (region, job, previous[1], current[1], previous_adjustments, current_adjustments)
            if profiles[-1][0] == profiles[-2][0]:
                assert profiles[-1][5], (region, job)
            assert profiles[-1][2] == "legendary_sensitivity_not_baseline", (region, job)

    # Session 5 exposed three concrete allocation regressions when each
    # quality tier restarted the round-robin order.  Lock the repaired
    # cumulative path so those item/stat pairs cannot disappear behind a new
    # monotonic-but-different allocation.
    fire_warrior = balance.FULL_LOADOUTS["fire"]["warrior"]
    warrior_rare = _flatten(balance._affix_profile("warrior", fire_warrior, "gear_median")[0])
    warrior_epic = _flatten(balance._affix_profile("warrior", fire_warrior, "gear_ceiling")[0])
    warrior_legendary = _flatten(balance._affix_profile("warrior", fire_warrior, "gear_legendary_sensitivity")[0])
    warrior_body_defense = ("armor_leather_armor", "defense")
    warrior_weapon_attack = ("weapon_iron_sword", "attack")
    assert (
        warrior_rare[warrior_body_defense],
        warrior_epic[warrior_body_defense],
        warrior_legendary[warrior_body_defense],
    ) == (2, 2, 2)
    assert (
        warrior_epic[warrior_weapon_attack],
        warrior_legendary[warrior_weapon_attack],
    ) == (1, 1)

    fire_cleric = balance.FULL_LOADOUTS["fire"]["cleric"]
    cleric_epic = _flatten(balance._affix_profile("cleric", fire_cleric, "gear_ceiling")[0])
    cleric_legendary = _flatten(balance._affix_profile("cleric", fire_cleric, "gear_legendary_sensitivity")[0])
    cleric_body_defense = ("armor_leather_armor", "defense")
    assert (
        cleric_epic[cleric_body_defense],
        cleric_legendary[cleric_body_defense],
    ) == (2, 3)


def main() -> None:
    balance.check_runtime_contracts()
    before = _global_snapshots()
    rng_before = random.getstate()
    records = balance.build_records(balance.LAYERS, balance.DEFAULT_SEEDS)
    _assert_schema(records)
    _assert_exact_coverage(records)
    _assert_rendering(records)
    _assert_determinism_and_state(records, before, rng_before)
    _assert_comparative_rng()
    _assert_comparative_monotonicity(records)
    _assert_runtime_tick_and_effective_vitals(records)
    _assert_timeout_semantics()
    _assert_benchmark_targets(records)
    _assert_canonical_rotation()
    _assert_promotion_overlay()
    _assert_item_adapter_parity()
    _assert_audit_categories()
    _assert_quality_affix_semantics()
    print("Balance Architecture v2 measurement-semantics checks ok (no balance verdict).")


if __name__ == "__main__":
    main()
