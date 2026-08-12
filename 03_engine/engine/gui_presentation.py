from __future__ import annotations

import math
from typing import Any
from .equipment_quality import QUALITY_LABELS
from .equipment_refs import resolve_equipment_ref
from .state import ensure_state_defaults, get_stats


EQUIPMENT_STAT_LABELS = {
    "attack": "物理攻擊力",
    "magic_attack": "魔法攻擊力",
    "defense": "物理防禦力",
    "magic_defense": "魔法防禦力",
    "agility": "敏捷",
    "crit": "暴擊率",
    "accuracy": "命中率",
    "effect_accuracy": "效果命中",
    "fire_resist": "火屬性抗性",
    "ice_resist": "冰屬性抗性",
    "earth_resist": "地屬性抗性",
    "lightning_resist": "雷屬性抗性",
    "rare_drop": "稀有掉落率",
    "physical_charge_skill_bonus": "蓄力技能傷害",
}
EQUIPMENT_PERCENT_STATS = {
    "crit", "accuracy", "fire_resist", "ice_resist", "earth_resist",
    "lightning_resist", "rare_drop", "physical_charge_skill_bonus",
}
GUI_HIDDEN_EQUIPMENT_STATS = {"trap_evasion"}
EQUIPMENT_SLOT_LABELS = {
    "weapon": "武器",
    "offhand": "副手",
    "head": "頭部",
    "body": "身體",
    "accessory": "飾品",
    "special": "特殊裝備",
}


def equipment_stat_rows(stats: dict[str, Any] | None) -> list[dict[str, Any]]:
    rows = []
    for key, value in (stats or {}).items():
        if key in GUI_HIDDEN_EQUIPMENT_STATS:
            continue
        suffix = "%" if key in EQUIPMENT_PERCENT_STATS else ""
        sign = "+" if isinstance(value, (int, float)) and value > 0 else ""
        rows.append({
            "key": key,
            "label": EQUIPMENT_STAT_LABELS.get(key, key),
            "value": value,
            "display_value": f"{sign}{display_resource(value)}{suffix}",
            "suffix": suffix,
        })
    return rows


def equipment_affix_names(resolved: dict[str, Any] | None) -> list[str]:
    if not resolved:
        return []
    return [
        str(view["name"])
        for view in resolved.get("affixes", {}).values()
        if view.get("status") == "valid" and view.get("name")
    ]


def equipment_slot_comparison(state: dict[str, Any], candidate_ref: str) -> dict[str, Any] | None:
    candidate = resolve_equipment_ref(state, candidate_ref)
    if not candidate:
        return None
    slot = candidate["base"]["slot"]
    current_ref = state.get("equipment", {}).get(slot)
    current = resolve_equipment_ref(state, current_ref)
    candidate_stats = candidate.get("effective_stats", {})
    current_stats = current.get("effective_stats", {}) if current else {}
    keys = list(dict.fromkeys([*candidate_stats, *current_stats]))
    rows = []
    for key in keys:
        before = current_stats.get(key, 0)
        after = candidate_stats.get(key, 0)
        rows.append({
            "key": key,
            "label": EQUIPMENT_STAT_LABELS.get(key, key),
            "current": before,
            "candidate": after,
            "delta": after - before,
            "suffix": "%" if key in EQUIPMENT_PERCENT_STATS else "",
        })
    return {
        "slot": slot,
        "slot_label": EQUIPMENT_SLOT_LABELS.get(slot, slot),
        "candidate_name": candidate["base"]["name"],
        "candidate_quality_label": QUALITY_LABELS.get(candidate["quality"], "普通"),
        "current_name": current["base"]["name"] if current else None,
        "current_quality_label": QUALITY_LABELS.get(current["quality"], "普通") if current else None,
        "current_affix_names": equipment_affix_names(current),
        "same_base": bool(current and current["base_item_id"] == candidate["base_item_id"]),
        "stat_rows": rows,
    }


def display_resource(value: object) -> str:
    """Render resource values without leaking fractional implementation detail."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    return str(int(number)) if number.is_integer() else f"{number:.2f}".rstrip("0").rstrip(".")


def display_hit_points(value: object) -> str:
    """Present HP as a whole number while the combat model retains precision."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    return str(max(0, math.floor(number + 0.5)))


def display_mana_points(value: object) -> str:
    """Present MP as a whole number while the runtime retains precision."""
    return display_hit_points(value)


def resource_strip(state: dict[str, Any]) -> list[dict[str, str]]:
    ensure_state_defaults(state)
    stats = get_stats(state)
    name = state.get("name", "")
    job_key = state.get("job")
    job_label = str(job_key)
    level = state.get("level", 1)

    current_hp = state.get("current_hp", stats["max_hp"])
    max_hp = stats["max_hp"]

    current_mp = state.get("current_mp", stats["max_mp"])
    max_mp = stats["max_mp"]

    gold = state.get("gold", 0)
    guild_points = state.get("guild_points", 0)

    return [
        {"id": "hero", "label": f"{name} / {job_label} Lv{level}", "tone": "primary"},
        {"id": "hp", "label": f"HP {display_hit_points(current_hp)}/{display_hit_points(max_hp)}", "tone": "healthy"},
        {"id": "mp", "label": f"MP {display_mana_points(current_mp)}/{display_mana_points(max_mp)}", "tone": "mana"},
        {"id": "gold", "label": f"{gold}G", "tone": "gold"},
        {"id": "guild_points", "label": f"Guild {guild_points}", "tone": "neutral"},
    ]
