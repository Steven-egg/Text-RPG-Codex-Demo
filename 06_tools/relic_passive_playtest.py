from __future__ import annotations

"""Disposable CLI playtest for Relic Passive v1.

This tool creates an in-memory state only.  It deliberately does not import or
call the save/load entry points and discards the state when the process exits.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from data import JOBS, MONSTERS  # noqa: E402
from engine.display import menu  # noqa: E402
from engine.facilities import temple  # noqa: E402
from engine.game import combat, show_status  # noqa: E402
from engine.state import add_item, clamp_vitals, create_state, get_stats  # noqa: E402

JOB_ALIASES = {
    "warrior": "劍士",
    "mage": "法師",
    "rogue": "盜賊",
    "cleric": "牧師",
}
SEAL_FLAGS = (
    "fire_seal_enshrined",
    "ice_seal_enshrined",
    "earth_seal_enshrined",
    "thunder_seal_enshrined",
)
TRAINING_ENCOUNTERS = (
    ("Fire normal: 青苔鼠", "mon_moss_rat", False),
    ("Ice normal: 冰原外圍守衛", "mon_ice_outer_guard", False),
    ("Earth normal: 苔根拾荒者", "mon_earth_rootling_scavenger", False),
    ("Thunder normal: 靜電蜥蜴", "mon_thunder_static_lizard", False),
    ("Fire Boss: 格倫", "boss_glen", True),
    ("Ice Boss: 冰封聖印領主", "boss_ice_final_seal_lord", True),
    ("Earth Boss: 深層地脈領主", "boss_earth_deep_leyline_lord", True),
)


def normalize_job(value: str) -> str:
    job = JOB_ALIASES.get(value.lower(), value)
    if job not in JOBS:
        supported = ", ".join(JOB_ALIASES)
        raise ValueError(f"未知職業：{value}（可用：{supported}）")
    return job


def build_playtest_state(job: str = "cleric", level: int = 25) -> dict:
    job_key = normalize_job(job)
    if level < 1 or level > 99:
        raise ValueError("等級必須介於 1 到 99。")
    state = create_state("Relic Playtester", job_key)
    state["level"] = level
    state["gold"] = 9_999
    state["flags"].update({flag: True for flag in SEAL_FLAGS})
    for item_id, quantity in {
        "item_potion_s": 10,
        "item_potion_m": 10,
        "item_focus_drop": 5,
        "item_herb_antidote": 5,
        "item_armor_piercer": 5,
    }.items():
        add_item(state, item_id, quantity)
    stats = get_stats(state)
    state["current_hp"] = stats["max_hp"]
    state["current_mp"] = stats["max_mp"]
    return state


def choose_training_encounter(state: dict) -> None:
    options = [entry[0] for entry in TRAINING_ENCOUNTERS]
    choice = menu("選擇訓練戰", options, allow_back=True)
    if choice == 0:
        return
    _label, enemy_id, boss = TRAINING_ENCOUNTERS[choice - 1]
    if enemy_id not in MONSTERS:
        raise RuntimeError(f"訓練戰資料不存在：{enemy_id}")
    combat(state, enemy_id, boss=boss)
    clamp_vitals(state)


def playtest_loop(state: dict) -> None:
    while True:
        choice = menu(
            "Relic Passive v1 Playtest（本次測試不會存檔）",
            [
                "前往轉職神殿選擇／免費改選聖印被動",
                "查看角色狀態",
                "開始訓練戰",
                "結束並丟棄測試角色",
            ],
            allow_back=False,
        )
        if choice == 1:
            temple(state)
        elif choice == 2:
            show_status(state)
        elif choice == 3:
            choose_training_encounter(state)
        else:
            print("測試角色已丟棄；未讀寫任何存檔。")
            return


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="不寫存檔的 Relic Passive v1 CLI playtest")
    parser.add_argument("--job", default="cleric", help="warrior / mage / rogue / cleric，或中文職業名")
    parser.add_argument("--level", default=25, type=int, help="測試等級，1 到 99")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    state = build_playtest_state(args.job, args.level)
    print(f"已建立 {state['job']} Lv{state['level']} 的四聖印測試角色。")
    playtest_loop(state)


if __name__ == "__main__":
    main()
