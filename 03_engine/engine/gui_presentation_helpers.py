from __future__ import annotations

from typing import Any
from pathlib import Path
from data import JOBS, ITEMS, EQUIPMENT, MONSTERS
from .state import ensure_state_defaults, get_stats
from .formatting import item_name

SAVE_PATH = Path(__file__).resolve().parents[2] / "save.json"

JOB_IDS = ["warrior", "mage", "rogue", "cleric"]
JOB_ID_TO_KEY = dict(zip(JOB_IDS, JOBS.keys()))
JOB_KEY_TO_ID = {value: key for key, value in JOB_ID_TO_KEY.items()}


def save_exists() -> bool:
    return SAVE_PATH.exists()


def percent(current: int, maximum: int) -> int:
    if maximum <= 0:
        return 0
    return max(0, min(100, round(current / maximum * 100)))


def state_summary(state: dict[str, Any] | None) -> dict[str, Any] | None:
    if state is None:
        return None
    ensure_state_defaults(state)
    stats = get_stats(state)
    job_key = state.get("job")
    return {
        "name": state.get("name", ""),
        "job_id": JOB_KEY_TO_ID.get(job_key, str(job_key)),
        "job_label": str(job_key),
        "level": state.get("level", 1),
        "exp": state.get("exp", 0),
        "gold": state.get("gold", 0),
        "guild_points": state.get("guild_points", 0),
        "hp": {"current": state.get("current_hp", stats["max_hp"]), "max": stats["max_hp"]},
        "mp": {"current": state.get("current_mp", stats["max_mp"]), "max": stats["max_mp"]},
        "save_exists": save_exists(),
    }


def player_model(state: dict[str, Any]) -> dict[str, Any]:
    summary = state_summary(state) or {}
    hp = summary["hp"]
    mp = summary["mp"]
    return {
        "name": summary["name"],
        "class_label": summary["job_label"],
        "level_label": f"Lv{summary['level']}",
        "hp": {"label": f"HP {hp['current']}/{hp['max']}", "percent": percent(hp["current"], hp["max"])},
        "mp": {"label": f"MP {mp['current']}/{mp['max']}", "percent": percent(mp["current"], mp["max"])},
        "gold_label": f"{summary['gold']}G",
    }


def normalize_job_id(job_id: str | None) -> str:
    from .gui_actions import GuiActionError
    job_id = str(job_id or "").strip().lower()
    if job_id in JOB_ID_TO_KEY:
        return JOB_ID_TO_KEY[str(job_id)]
    if job_id in JOBS:
        return str(job_id)
    raise GuiActionError("Unknown job id.", status=400)


def run_reward_rows(run_log: dict[str, Any]) -> list[dict[str, str]]:
    rows = []
    gold = int(run_log.get("gold", 0) or 0)
    if gold:
        rows.append({"label": "金幣", "value": f"{gold}G"})
    for item_id, qty in run_log.get("items", {}).items():
        rows.append({"label": item_name(item_id), "value": f"x{qty}"})
    return rows


def boss_label(boss_id: str | None) -> str:
    if not boss_id:
        return "-"
    monster = MONSTERS.get(boss_id)
    return monster["name"] if monster else boss_id

