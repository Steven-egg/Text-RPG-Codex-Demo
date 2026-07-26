"""Focused non-S10 regression checks for Warrior/Mage quality equipment."""
from __future__ import annotations

import random
from math import isclose
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "03_engine", ROOT / "04_data"):
    if str(module_root) not in sys.path:
        sys.path.insert(0, str(module_root))

from data import EQUIPMENT
from engine.dungeon import boss_available_at_dungeon_end
from engine.equipment_quality import QUALITY_AFFIX_MULTIPLIERS, pattern_for, supports_quality_job
from engine.equipment_refs import resolve_equipment_ref
from engine.game import calc_player_damage, gain_physical_charge, physical_charge_cap
from engine.state import create_state, equip_item, grant_quality_equipment, get_stats, quality_equipment_candidates


def equip_quality(state: dict, base_item_id: str, major: str, minor: str | None) -> str:
    reference_id = grant_quality_equipment(state, base_item_id, "epic")
    instance = state["equipment_instances"][reference_id]
    instance["major_affix_id"] = major
    instance["minor_affix_id"] = minor
    assert equip_item(state, reference_id, quiet=True)
    return reference_id


def run() -> None:
    assert all(supports_quality_job(job) for job in ("劍士", "法師", "盜賊", "牧師"))
    for job in ("劍士", "法師", "盜賊", "牧師"):
        state = create_state(f"{job}-candidates", job)
        assert quality_equipment_candidates(state, "border_fire")
        assert quality_equipment_candidates(state, "ice")

    warrior = create_state("quality-warrior", "劍士")
    cap_ref = equip_quality(warrior, "weapon_ice_warrior_01", "major_charge_skill_bonus", "minor_charge_cap")
    cap_view = resolve_equipment_ref(warrior, cap_ref)
    assert cap_view and isclose(cap_view["affix_stats"]["physical_charge_cap"], 1.35)
    assert physical_charge_cap(warrior) == 4
    buffs = {"_physical_charge": 2}
    assert gain_physical_charge(warrior, buffs) == 3
    assert isclose(get_stats(warrior)["physical_charge_skill_bonus"], 5.4)

    gain_ref = equip_quality(warrior, "weapon_ice_warrior_01", "major_charge_skill_bonus", "minor_charge_gain")
    gain_view = resolve_equipment_ref(warrior, gain_ref)
    assert gain_view and isclose(gain_view["affix_stats"]["physical_charge_gain_chance"], 33.75)
    random.seed(1)
    assert gain_physical_charge(warrior, {"_physical_charge": 0}) == 2

    mage = create_state("quality-mage", "法師")
    mage_ref = equip_quality(mage, "weapon_ice_mage_01", "major_arcane", "minor_elemental_magic_direct")
    mage_view = resolve_equipment_ref(mage, mage_ref)
    assert mage_view and isclose(mage_view["affix_stats"]["elemental_magic_direct_percent"], 8.1)
    assert get_stats(mage)["magic_attack"] >= EQUIPMENT["weapon_ice_mage_01"]["stats"]["magic_attack"] + 6 * 1.35

    enemy = {"defense": 0, "magic_defense": 0, "agility": 0, "ice_resist": 0}
    elemental_skill = {"stat": "magic", "multiplier": 1.0, "element": "冰"}
    neutral_skill = {"stat": "magic", "multiplier": 1.0, "element": "無"}
    random.seed(11)
    elemental_damage, _ = calc_player_damage(mage, enemy, elemental_skill, {}, {})
    mage["equipment_instances"][mage_ref]["minor_affix_id"] = "minor_magic_guard_weapon"
    random.seed(11)
    unboosted_elemental_damage, _ = calc_player_damage(mage, enemy, elemental_skill, {}, {})
    assert elemental_damage > unboosted_elemental_damage
    random.seed(11)
    unboosted_neutral_damage, _ = calc_player_damage(mage, enemy, neutral_skill, {}, {})
    mage["equipment_instances"][mage_ref]["minor_affix_id"] = "minor_elemental_magic_direct"
    random.seed(11)
    neutral_damage, _ = calc_player_damage(mage, enemy, neutral_skill, {}, {})
    assert neutral_damage == unboosted_neutral_damage

    for region, expected_minor in (
        ("ice", "minor_quality_ice_ward"),
        ("earth", "minor_quality_earth_ward"),
        ("thunder", "minor_quality_thunder_ward"),
        ("final", "minor_quality_final_ward"),
    ):
        base = {"slot": "head", "region": region}
        selected = {pattern_for(base, "法師", "epic", random.Random(seed))[2] for seed in range(20)}
        assert expected_minor in selected

    fine_to_legendary = []
    for quality in ("fine", "rare", "epic", "legendary"):
        ref = grant_quality_equipment(mage, "weapon_ice_mage_01", quality)
        mage["equipment_instances"][ref]["major_affix_id"] = "major_arcane"
        mage["equipment_instances"][ref]["minor_affix_id"] = None
        fine_to_legendary.append(resolve_equipment_ref(mage, ref)["affix_stats"]["magic_attack"])
    assert fine_to_legendary == [6 * QUALITY_AFFIX_MULTIPLIERS[quality] for quality in ("fine", "rare", "epic", "legendary")]

    warrior["flags"]["ice_wreck_captain_defeated"] = False
    mage["flags"]["ice_wreck_captain_defeated"] = False
    assert boss_available_at_dungeon_end(warrior, "dungeon_ice_minor_a", "boss_ice_wreck_captain")
    assert boss_available_at_dungeon_end(mage, "dungeon_ice_minor_a", "boss_ice_wreck_captain")


if __name__ == "__main__":
    run()
    print("Warrior/Mage quality checks passed")
