from __future__ import annotations

from data import EQUIPMENT, ITEMS, MATERIALS
from .equipment_refs import resolve_equipment_ref


def format_affix_view(affix: dict | None) -> str:
    """Format a detached resolver affix view for the CLI without mutation."""
    if not affix or affix.get("status") == "none":
        return "無"
    if affix.get("status") != "valid":
        return f"異常詞綴 ({affix.get('id', 'unknown')})"
    stat_parts = []
    for stat_key, value in affix.get("stats", {}).items():
        suffix = "%" if stat_key in {"effect_accuracy", "crit", "fire_resist", "ice_resist", "earth_resist", "thunder_resist", "trap_evasion", "rare_drop"} else ""
        stat_parts.append(f"{stat_key} {value:+}{suffix}")
    return f"{affix['name']} ({'、'.join(stat_parts)})"


def equipment_affix_summary(affixes: dict | None) -> str:
    affixes = affixes or {}
    return f"主詞綴：{format_affix_view(affixes.get('major'))}／次詞綴：{format_affix_view(affixes.get('minor'))}"


def item_name(item_id: str, state: dict | None = None) -> str:
    if item_id in ITEMS:
        return ITEMS[item_id]["name"]
    if item_id in EQUIPMENT:
        return EQUIPMENT[item_id]["name"]
    if state:
        resolved = resolve_equipment_ref(state, item_id)
        if resolved:
            return resolved["base"]["name"]
    if item_id in MATERIALS:
        return MATERIALS[item_id]
    return item_id


def format_items(cost: dict) -> str:
    if not cost:
        return "無"
    parts = []
    for item_id, qty in cost.items():
        if item_id.startswith("flag:"):
            flag = item_id.split(":", 1)[1]
            flag_names = {
                "ash_guardian_defeated": "擊敗灰燼守衛",
                "boss_glen_defeated": "擊敗山寨頭目葛倫",
                "cinder_seal_sentinel_defeated": "擊敗燼印鎮衛",
                "fire_mark_church_bridge_done": "完成火印神殿接橋",
                "fire_mark_church_lookup_done": "完成火印教會查閱",
                "fire_mark_guild_inquiry_done": "完成火印工會詢問",
            }
            parts.append(flag_names.get(flag, flag))
        else:
            parts.append(f"{item_name(item_id)} x{qty}")
    return "、".join(parts)


def equipment_summary(item_id: str, state: dict | None = None) -> str:
    resolved = resolve_equipment_ref(state or {}, item_id)
    eq = resolved["base"] if resolved else EQUIPMENT[item_id]
    stat_values = resolved["effective_stats"] if resolved else eq.get("stats", {})
    stats = []
    for key, label in [
        ("attack", "攻擊"),
        ("magic_attack", "魔攻"),
        ("defense", "防禦"),
        ("agility", "敏捷"),
        ("effect_accuracy", "效果命中"),
        ("magic_defense", "魔防"),
        ("crit", "暴擊"),
        ("fire_resist", "火抗"),
        ("trap_evasion", "陷阱迴避"),
        ("rare_drop", "稀有掉落"),
    ]:
        if key in stat_values:
            value = stat_values[key]
            suffix = "%" if key in {"effect_accuracy", "crit", "fire_resist", "ice_resist", "earth_resist", "thunder_resist", "trap_evasion", "rare_drop"} else ""
            stats.append(f"{label} {value:+}{suffix}")
    return "，".join(stats) if stats else eq.get("desc", "")


def monster_drop_names(monster: dict) -> str:
    drops = [item_name(item_id) for item_id, _chance, _qty in monster["drops"]]
    return "、".join(drops) if drops else "無"
