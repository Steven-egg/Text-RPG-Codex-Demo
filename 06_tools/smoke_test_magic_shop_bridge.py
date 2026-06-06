from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from engine.gui_actions import GuiRuntimeSession, GuiActionError
from data import MAGIC_BOOKS, SKILLS


def run_smoke_test():
    print("Starting Magic Shop Learn Magic Book Live MVP bridge smoke test...")

    # 1. Happy Path: Mage (Lv2) learning book_spark
    session = GuiRuntimeSession()
    session.new_game(name="星燈法師", job_id="mage")
    state = session.require_state()

    # Set Lv 2 and give enough gold + materials
    state["level"] = 2
    state["gold"] = 250
    state["inventory"]["mat_small_crystal"] = 2

    print(f"Initial State: job={state['job']}, level={state['level']}, gold={state['gold']}, inventory={dict(state['inventory'])}, learned_skills={state.get('learned_skills')}")

    # Perform learning
    response = session.dispatch("learn_magic_book", {"book_id": "book_spark"}, screen_id="magic_shop_screen")
    assert response["ok"] is True
    assert "skill_spark" in state["learned_skills"]
    assert state["gold"] == 70  # 250 - 180 = 70G
    assert state["inventory"]["mat_small_crystal"] == 1  # 2 - 1 = 1

    print("Happy Path verified: Gold deducted, materials paid, skill added.")

    # 2. Blocked Path: Learning already learned spell
    try:
        session.dispatch("learn_magic_book", {"book_id": "book_spark"}, screen_id="magic_shop_screen")
        raise AssertionError("Expected learning already learned spell to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "已學會此法術"
        print("Blocked Path (Already learned) verified.")

    # 3. Blocked Path: Class restricted (Warrior trying to learn spark)
    session2 = GuiRuntimeSession()
    session2.new_game(name="大劍士", job_id="warrior")
    state2 = session2.require_state()
    state2["level"] = 2
    state2["gold"] = 300
    state2["inventory"]["mat_small_crystal"] = 2

    try:
        session2.dispatch("learn_magic_book", {"book_id": "book_spark"}, screen_id="magic_shop_screen")
        raise AssertionError("Expected class mismatch to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert err.blocked_reason == "職業不符"
        print("Blocked Path (Class restricted) verified.")

    # 4. Blocked Path: Level restricted (Mage Lv1 trying to learn spark)
    session3 = GuiRuntimeSession()
    session3.new_game(name="見習法師", job_id="mage")
    state3 = session3.require_state()
    state3["level"] = 1
    state3["gold"] = 300
    state3["inventory"]["mat_small_crystal"] = 2

    try:
        session3.dispatch("learn_magic_book", {"book_id": "book_spark"}, screen_id="magic_shop_screen")
        raise AssertionError("Expected level mismatch to fail, but it succeeded.")
    except GuiActionError as err:
        assert err.status == 409
        assert "等級不足" in err.blocked_reason
        print("Blocked Path (Level restricted) verified.")

    # 5. Screen Model Coverage Verification
    model = session.screen_model("magic_shop_screen")
    assert model["screen_id"] == "facility_magic_shop_screen"

    # Verify we cover all MAGIC_BOOKS
    rows = model["list_rows"]
    row_book_ids = {row["book_id"] for row in rows}
    assert row_book_ids == set(MAGIC_BOOKS.keys())
    assert len(row_book_ids) == 6
    print("All MAGIC_BOOKS covered in model rows.")

    # Verify category counts (Damage=2, Heal=1, Buff=2, Special=1, All=6)
    category_tabs = {tab["id"]: tab for tab in model["category_tabs"]}
    assert category_tabs["all"]["count"] == 6
    assert category_tabs["damage"]["count"] == 2
    assert category_tabs["heal"]["count"] == 1
    assert category_tabs["buff"]["count"] == 2
    assert category_tabs["special"]["count"] == 1
    print("Category counts verified.")

    # Verify book_cinder_mark is debuff/特殊魔法
    cinder_mark_row = next(row for row in rows if row["book_id"] == "book_cinder_mark")
    assert cinder_mark_row["category"] == "special"

    cinder_mark_details = model["book_details"]["book_cinder_mark"]
    assert cinder_mark_details["category_label"] == "特殊魔法"
    print("book_cinder_mark special/特殊魔法 category verified.")

    # Verify details, actions and requirements are present for all books
    for b_id in MAGIC_BOOKS:
        assert b_id in model["book_details"]
        assert b_id in model["requirement_rows"]
        assert b_id in model["primary_actions"]
    print("All books details, requirements, actions verified.")

    print("Magic Shop bridge smoke test ok")


if __name__ == "__main__":
    run_smoke_test()
