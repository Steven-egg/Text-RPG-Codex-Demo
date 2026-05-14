from __future__ import annotations

from data import EQUIPMENT, ITEMS, MATERIALS


def item_name(item_id: str) -> str:
    if item_id in ITEMS:
        return ITEMS[item_id]["name"]
    if item_id in EQUIPMENT:
        return EQUIPMENT[item_id]["name"]
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


def equipment_summary(item_id: str) -> str:
    eq = EQUIPMENT[item_id]
    stats = []
    for key, label in [
        ("attack", "攻擊"),
        ("magic_attack", "魔攻"),
        ("defense", "防禦"),
        ("agility", "敏捷"),
        ("accuracy", "命中"),
        ("crit", "暴擊"),
        ("fire_resist", "火抗"),
        ("trap_evasion", "陷阱迴避"),
        ("rare_drop", "稀有掉落"),
    ]:
        if key in eq.get("stats", {}):
            value = eq["stats"][key]
            suffix = "%" if key in {"accuracy", "crit", "fire_resist", "trap_evasion", "rare_drop"} else ""
            stats.append(f"{label} {value:+}{suffix}")
    return "，".join(stats) if stats else eq.get("desc", "")


def monster_drop_names(monster: dict) -> str:
    drops = [item_name(item_id) for item_id, _chance, _qty in monster["drops"]]
    return "、".join(drops) if drops else "無"
