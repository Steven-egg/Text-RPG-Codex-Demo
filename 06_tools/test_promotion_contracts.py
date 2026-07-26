"""Deterministic data, migration, and Live temple contracts for Formal Promotion v1."""
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "03_engine", ROOT / "04_data"):
    if str(module_root) not in sys.path:
        sys.path.insert(0, str(module_root))

from data import PROMOTIONS, SKILLS
from engine.gui_temple_model import temple_screen_model
from engine.state import create_state, ensure_state_defaults, player_summary_line


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


if __name__ == "__main__":
    run()
    print("promotion contracts passed")
