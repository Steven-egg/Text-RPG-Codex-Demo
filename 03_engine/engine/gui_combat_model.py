from __future__ import annotations

from typing import Any
from data import ITEMS, SKILLS
from . import game
from .formatting import item_name
from .gui_presentation_helpers import percent


def combat_enemy_trait_status(enemy: dict[str, Any], enemy_buffs: dict[str, Any]) -> str:
    """Return a GUI-readable status without duplicating the race rule table."""
    trait = game.monster_race_trait(enemy)
    trait_name = trait.get("display_name", "")
    summary = game.monster_race_trait_summary(enemy, enemy_buffs)
    if not trait_name or summary == "無":
        return "無"

    status = summary.removeprefix(trait_name).strip()
    if status in {"0", "1"}:
        return f"剩餘 {status} 次"
    if status.startswith("（") and status.endswith("）"):
        return status[1:-1]
    return status or "待機"


def combat_item_rows(state: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for item_id in game.COMBAT_ITEM_IDS:
        qty = game.combat_item_quantity(state, item_id)
        if qty <= 0:
            continue
        item = ITEMS.get(item_id, {})
        rows.append(
            {
                "action_id": "use_item",
                "label": item.get("name", item_name(item_id)),
                "meta": f"x{qty}",
                "description": item.get("desc", ""),
                "enabled": True,
                "disabled_reason": None,
                "payload": {"item_id": item_id},
            }
        )
    return rows


def get_learned_elements(state: dict[str, Any]) -> list[str]:
    elements = []
    for skill_id in state.get("learned_skills", []):
        skill = SKILLS.get(skill_id)
        if skill and skill.get("element") in {"火", "冰", "自然", "雷"}:
            elem = skill["element"]
            if elem not in elements:
                elements.append(elem)
    return elements


def combat_skill_rows(state: dict[str, Any], combat: dict[str, Any] | None, resolved: bool) -> list[dict[str, Any]]:
    rows = []
    learned_skills = state.get("learned_skills", [])
    for skill_id in learned_skills:
        skill = SKILLS.get(skill_id)
        if not skill:
            continue

        if skill_id in {"skill_star_fracture", "skill_sigil_mage"}:
            learned_elements = get_learned_elements(state)
            if not learned_elements:
                mp_cost = skill.get("mp", 0)
                rows.append({
                    "action_id": "use_skill",
                    "label": f"{skill.get('name')} (無可用元素)",
                    "meta": f"MP {mp_cost}",
                    "description": "尚未學會火、冰、自然、雷中任何一項元素魔法，無法使用此技能。",
                    "enabled": False,
                    "disabled_reason": "未學會任何元素魔法。",
                    "payload": {"skill_id": skill_id}
                })
                continue

            for elem in learned_elements:
                mp_cost = skill.get("mp", 0)
                has_enough_mp = state.get("current_mp", 0) >= mp_cost
                enabled = not resolved and has_enough_mp
                disabled_reason = None
                if resolved:
                    disabled_reason = "戰鬥已結束。"
                elif not has_enough_mp:
                    disabled_reason = "MP 不足。"

                payload = {"skill_id": skill_id, "element": elem}
                if combat and "enemy_id" in combat:
                    payload["enemy_id"] = combat["enemy_id"]

                if skill_id == "skill_star_fracture":
                    label = f"星裂術：{elem}"
                    desc = f"消耗 12 MP。對敵人造成大額【{elem}】屬性魔法傷害。"
                else:
                    label = f"印紋術：{elem}"
                    desc = f"消耗 6 MP。對目標施加【{elem}】之印紋（持續 5 回合）。"

                rows.append({
                    "action_id": "use_skill",
                    "label": label,
                    "meta": f"MP {mp_cost}",
                    "description": desc,
                    "enabled": enabled,
                    "disabled_reason": disabled_reason,
                    "payload": payload,
                })
            continue

        mp_cost = skill.get("mp", 0)
        has_enough_mp = state.get("current_mp", 0) >= mp_cost
        enabled = not resolved and has_enough_mp
        disabled_reason = None
        if resolved:
            disabled_reason = "戰鬥已結束。"
        elif not has_enough_mp:
            disabled_reason = "MP 不足。"

        payload = {"skill_id": skill_id}
        kind = skill.get("kind")
        if kind in ("damage", "debuff") and combat and "enemy_id" in combat:
            payload["enemy_id"] = combat["enemy_id"]

        rows.append(
            {
                "action_id": "use_skill",
                "label": skill.get("name", skill_id),
                "meta": f"MP {mp_cost}",
                "description": skill.get("desc", ""),
                "enabled": enabled,
                "disabled_reason": disabled_reason,
                "payload": payload,
            }
        )
    return rows


def result_overlay_model(outcome: str, title: str, status: str, summary: str, rows: list[str]) -> dict[str, Any]:
    if outcome in ("victory", "retreat"):
        next_action = {
            "action_id": "back_to_exploration",
            "label": "返回探索",
            "description": "回到探索畫面繼續前進。",
            "payload": {"from": f"combat_result_{outcome}"},
            "feedback_message": "正在返回探索...",
            "navigate_to": "../dungeon_exploration/index.html?mode=live",
        }
    else:
        next_action = {
            "action_id": "back_to_town_hub",
            "label": "回到城鎮",
            "description": "返回城鎮廣場進行休整。",
            "payload": {"from": f"combat_result_{outcome}"},
            "feedback_message": "正在返回城鎮...",
            "navigate_to": "../town_hub/index.html?mode=live",
        }
    return {
        "outcome": outcome,
        "label": "戰鬥結束",
        "title": title,
        "status_summary": status,
        "battle_summary": summary,
        "reward_title": "結算",
        "rows": [
            {"label": f"{index}.", "value": row, "tone": "danger" if outcome == "defeat" and index == 1 else "neutral"}
            for index, row in enumerate(rows, start=1)
        ],
        "next_action": next_action,
    }


def combat_screen_model(session: Any) -> dict[str, Any]:
    state = session.require_state()
    combat = session.require_combat()
    enemy = combat["enemy"]
    stats = game.get_stats(state, combat["player_buffs"])
    enemy_hp = max(0, combat["enemy_hp"])
    resolved = combat.get("outcome") is not None
    boss = bool(combat.get("boss"))
    usable_items = combat_item_rows(state)
    usable_skills = combat_skill_rows(state, combat, resolved)
    enemy_trait = game.monster_race_trait(enemy)
    return {
        "screen_id": "combat_screen",
        "title": "戰鬥",
        "subtitle": "迎擊眼前的強敵，取得勝利以推進探索。",
        "resource_strip": [{"label": f"第 {combat['turn']} 回合", "tone": "neutral"}],
        "player": {
            "name": state.get("name", ""),
            "class_label": state.get("job", ""),
            "level_label": f"Lv{state.get('level', 1)}",
            "hp_label": f"{state['current_hp']} / {stats['max_hp']}",
            "mp_label": f"{state['current_mp']} / {stats['max_mp']}",
            "status_label": game.buff_summary(combat["player_buffs"]),
            "stance_label": "戰鬥結束" if resolved else "可行動",
        },
        "enemy": {
            "enemy_id": combat["enemy_id"],
            "name": enemy["name"],
            "hp_label": f"HP {enemy_hp} / {enemy['hp']}",
            "hp_percent": percent(enemy_hp, enemy["hp"]),
            "attribute": enemy["element"],
            "race_label": game.monster_race_display_name(enemy),
            "trait_label": enemy_trait.get("display_name", "無"),
            "trait_status_label": combat_enemy_trait_status(enemy, combat["enemy_buffs"]),
            "status_label": game.buff_summary(combat["enemy_buffs"]),
        },
        "command_message": combat.get("last_action_summary", ""),
        "skill_menu": {
            "label": "技能選擇",
            "title": "技能",
            "summary": f"目前 MP {state['current_mp']}/{stats['max_mp']}。目標：{enemy['name']} / 屬性 {enemy['element']} / 狀態 {game.buff_summary(combat['enemy_buffs'])}。再次按技能可收回。",
            "empty_message": "尚無可用技能。" if state.get("learned_skills", []) else "沒有學會任何技能。",
            "items": usable_skills,
        },
        "item_menu": {
            "label": "道具選擇",
            "title": "道具",
            "summary": f"目標：{enemy['name']} / 狀態 {game.buff_summary(combat['enemy_buffs'])}。",
            "empty_message": "沒有可用道具。",
            "items": usable_items,
        },
        "battle_log": combat.get("battle_log", []),
        "result_overlay": combat.get("result_overlay"),
        "actions": [
            {
                "action_id": "basic_attack",
                "label": "攻擊",
                "description": "進行普通攻擊。",
                "enabled": not resolved,
                "disabled_reason": None if not resolved else "戰鬥已結束。",
                "primary": True,
                "payload": {"enemy_id": combat["enemy_id"]},
            },
            {
                "action_id": "open_skill_menu",
                "label": "技能",
                "description": "職業特殊技能。",
                "enabled": not resolved and bool(state.get("learned_skills", [])),
                "disabled_reason": (
                    "戰鬥已結束。" if resolved else (
                        "你尚未學會任何技能。" if not state.get("learned_skills", []) else None
                    )
                ),
                "primary": False,
                "payload": {"source": "combat_screen"},
            },
            {
                "action_id": "open_item_menu",
                "label": "道具",
                "description": "使用攜帶的戰鬥道具。",
                "enabled": not resolved and bool(usable_items),
                "disabled_reason": None if usable_items else "沒有可用道具。",
                "primary": False,
                "payload": {"source": "combat_screen"},
            },
            {
                "action_id": "defend",
                "label": "防禦",
                "description": "採取防禦姿態降低下回合所受傷害。",
                "enabled": not resolved,
                "disabled_reason": None if not resolved else "戰鬥已結束。",
                "primary": False,
                "payload": {},
            },
            {
                "action_id": "retreat",
                "label": "逃跑",
                "description": "嘗試逃離當前戰鬥。",
                "enabled": not resolved and not boss,
                "disabled_reason": (
                    "戰鬥已結束。" if resolved else (
                        "Boss 戰不可逃跑。" if boss else None
                    )
                ),
                "primary": False,
                "payload": {"enemy_id": combat["enemy_id"]},
            },
        ],
    }
