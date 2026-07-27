"""Deterministic data, migration, and Live temple contracts for Formal Promotion v1."""
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "03_engine", ROOT / "04_data"):
    if str(module_root) not in sys.path:
        sys.path.insert(0, str(module_root))

from data import PROMOTIONS, SKILLS
from engine import game
from engine.gui_actions import GuiActionError, GuiRuntimeSession
from engine.gui_temple_model import temple_screen_model
from engine.state import add_item, create_state, ensure_state_defaults, player_summary_line


FORMAL_PROMOTION_IDS = {
    "promotion_blood_blade",
    "promotion_blood_armor",
    "promotion_star_fracture",
    "promotion_sigil_mage",
    "promotion_shadow_slayer",
    "promotion_miasma_hunter",
    "promotion_holy_veil",
    "promotion_holy_eclipse",
}


def qualified_state(job: str) -> dict:
    state = create_state("promotion-contract", job)
    state["level"] = 18
    state["completed_quests"].append("quest_ice_return_handoff")
    return state


def run() -> None:
    assert set(PROMOTIONS) == FORMAL_PROMOTION_IDS
    assert {promo["source_job"] for promo in PROMOTIONS.values()} == {"劍士", "法師", "盜賊", "牧師"}

    for promotion_id, promotion in PROMOTIONS.items():
        assert promotion["status"] == "formal", promotion_id
        assert promotion["active_skill_id"] in SKILLS, promotion_id
        assert promotion["passive_skill_id"] in SKILLS, promotion_id
        assert SKILLS[promotion["active_skill_id"]]["kind"] != "passive", promotion_id
        assert SKILLS[promotion["passive_skill_id"]]["kind"] == "passive", promotion_id
        requirements = {(item["kind"], item.get("key", item.get("value"))) for item in promotion["requirements"]}
        assert ("level", 18) in requirements, promotion_id
        assert ("quest", "quest_ice_return_handoff") in requirements, promotion_id

    for legacy_job, base_job in {
        "元素騎士": "劍士",
        "星詠者": "法師",
        "影行者": "盜賊",
        "聖印使": "牧師",
    }.items():
        migrated = ensure_state_defaults({"job": legacy_job, "inventory": {}})
        assert migrated["job"] == base_job
        assert migrated["promotion_id"] is None

    promoted = qualified_state("劍士")
    promoted["promotion_id"] = "promotion_blood_blade"
    assert "劍士／血鋒鬥士" in player_summary_line(promoted)

    eligible_model = temple_screen_model(qualified_state("法師"))
    assert len(eligible_model["promotions"]) == 2
    assert all(option["enabled"] for option in eligible_model["promotions"])

    locked_model = temple_screen_model(create_state("promotion-contract", "法師"))
    assert all(not option["enabled"] for option in locked_model["promotions"])

    claimed_state = qualified_state("法師")
    claimed_state["promotion_id"] = "promotion_star_fracture"
    claimed_model = temple_screen_model(claimed_state)
    assert all(not option["enabled"] for option in claimed_model["promotions"])
    assert next(option for option in claimed_model["promotions"] if option["class_id"] == "promotion_star_fracture")["label"].endswith("(已晉升)")

    live_session = GuiRuntimeSession()
    live_session.new_game(name="promotion-contract", job_id="mage")
    live_state = live_session.require_state()
    live_state["level"] = 18
    live_state["completed_quests"].append("quest_ice_return_handoff")
    try:
        live_session.dispatch("claim_promotion", {"class_id": "promotion_star_fracture"}, screen_id="temple_screen")
    except GuiActionError as error:
        assert error.status == 409
    else:
        raise AssertionError("promotion claim should require an explicit confirmation")
    assert live_state["promotion_id"] is None
    confirmed = live_session.dispatch("claim_promotion", {"class_id": "promotion_star_fracture", "confirmed": True}, screen_id="temple_screen")
    assert confirmed["ok"] is True
    assert live_state["promotion_id"] == "promotion_star_fracture"

    enemy = {"hp": 100, "current_hp": 100, "element": "冰", "defense": 0, "magic_defense": 0, "agility": 0}
    original_roll = game.direct_damage_roll
    game.direct_damage_roll = lambda agility: 1.0
    try:
        star = qualified_state("法師")
        star["promotion_id"] = "promotion_star_fracture"
        star["learned_skills"].extend(["skill_star_fracture", "skill_star_fracture_passive"])
        mp_before = star["current_mp"]
        star_result = game.execute_skill(star, enemy, "skill_star_fracture", {**SKILLS["skill_star_fracture"], "element": "雷"}, {}, {})
        assert star_result.damage > 0
        assert star["current_mp"] == mp_before + 6

        sigil = qualified_state("法師")
        sigil["promotion_id"] = "promotion_sigil_mage"
        sigil_buffs: dict = {}
        sigil_enemy_buffs: dict = {}
        game.execute_skill(sigil, enemy, "skill_sigil_mage", {**SKILLS["skill_sigil_mage"], "element": "火"}, sigil_buffs, sigil_enemy_buffs)
        detonation = game.player_attack(
            sigil, enemy, enemy["hp"], {"name": "測試火術", "kind": "damage", "stat": "magic", "multiplier": 1.0, "element": "火"}, sigil_buffs, sigil_enemy_buffs,
        )
        assert "sigil_mage_mark" not in sigil_enemy_buffs
        assert any("印紋引爆" in event for event in detonation.events)

        shadow = qualified_state("盜賊")
        shadow["promotion_id"] = "promotion_shadow_slayer"
        execute_skill = SKILLS["skill_shadow_slayer_execute"]
        high_hp = game.execute_skill(shadow, {**enemy, "current_hp": 50}, "skill_shadow_slayer_execute", execute_skill, {}, {})
        low_hp = game.execute_skill(shadow, {**enemy, "current_hp": 39}, "skill_shadow_slayer_execute", execute_skill, {}, {})
        assert low_hp.damage > high_hp.damage

        miasma = qualified_state("盜賊")
        miasma["promotion_id"] = "promotion_miasma_hunter"
        plain = game.execute_skill(miasma, enemy, "skill_miasma_strike", SKILLS["skill_miasma_strike"], {}, {})
        afflicted = game.execute_skill(miasma, enemy, "skill_miasma_strike", SKILLS["skill_miasma_strike"], {}, {"bleed": 3, "poison": 3})
        assert afflicted.damage > plain.damage

        blood_blade = qualified_state("劍士")
        charge_skill = {"name": "測試蓄力斬", "kind": "damage", "charge_bonus_per_stack": 0.3}
        base_charge_damage, _ = game.calc_player_damage(blood_blade, enemy, charge_skill, {"physical_charge": 2}, {})
        blood_blade["promotion_id"] = "promotion_blood_blade"
        blood_charge_damage, _ = game.calc_player_damage(
            blood_blade, enemy, charge_skill, {"physical_charge": 2, "blood_blade_active": 3}, {},
        )
        assert blood_charge_damage > base_charge_damage

        eclipse = qualified_state("牧師")
        eclipse["promotion_id"] = "promotion_holy_eclipse"
        no_vial = game.execute_skill(eclipse, enemy, "skill_holy_eclipse_cast", SKILLS["skill_holy_eclipse_cast"], {}, {})
        assert no_vial.outcome == "cancel"
        add_item(eclipse, "item_sanctified_ash_vial")
        eclipse_buffs: dict = {}
        eclipse_result = game.execute_skill(eclipse, enemy, "skill_holy_eclipse_cast", SKILLS["skill_holy_eclipse_cast"], eclipse_buffs, {})
        assert eclipse_result.outcome is None
        assert eclipse["inventory"].get("item_sanctified_ash_vial", 0) == 0
        assert eclipse_buffs["_holy_eclipse_vial_marked"] is True
    finally:
        game.direct_damage_roll = original_roll


if __name__ == "__main__":
    run()
    print("promotion contracts passed")
