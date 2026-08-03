from __future__ import annotations

import json
import math
import random
import sys
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path

from .bestiary import monster_locations
from .display import (
    action_menu_panel,
    clear_screen,
    main_menu_panel,
    menu,
    pause,
    render_panel,
    setup_console,
    start_screen_panel,
    title,
)
from .story_beats import region_story_beat_id, show_story_beat, take_story_beat
from .formatting import equipment_summary, format_items, item_name, monster_drop_names
from .equipment_refs import equipment_ref_count
from .previews import get_preview_promotions_for_job, show_job_specialization_preview
from .state import (
    is_key_item,
    exp_to_next,
    create_state,
    ensure_state_defaults,
    add_item,
    remove_item,
    add_storage_item,
    remove_storage_item,
    owns_item_or_equipped,
    consume_item_or_equipped,
    unlock,
    is_unlocked,
    boss_clear_flag,
    boss_defeated,
    player_facing_dungeon_ids,
    get_stats,
    equipment_comparison,
    clamp_vitals,
    equip_item,
    ICE_REGION_UNLOCK,
    EARTH_REGION_UNLOCK,
    THUNDER_REGION_UNLOCK,
    ICE_PHASE_2_DUNGEON_ID,
    EARTH_PHASE_2_DUNGEON_ID,
    THUNDER_PHASE_2_DUNGEON_ID,
    FINAL_PHASE_2_DUNGEON_ID,
    FINAL_PHASE_3_DUNGEON_ID,
    FINAL_REGION_UNLOCK,
    FINAL_QUEST_ID,
    BOSS_CLEAR_FLAGS,
    check_and_normalize_region,
    can_pay_items,
    pay_items,
    quest_unlocked,
    quest_ready,
    player_summary_line,
    player_resource_lines,
    add_gold,
    add_loot,
    run_supply_item_quantity,
    item_job_allowed,
    consume_run_supply_item,
    configure_run_supplies,
)
from .relic import (
    relic_enshrined,
    relic_ready_to_enshrine,
    relic_source_count,
    relic_source_required,
    relic_disabled_reason,
    relic_passive_choices,
    selected_relic_passive,
    select_relic_passive,
    preview_relic_entries,
    enshrine_relic,
    relic_preview_menu,
    ready_relic_names,
    active_relic_passive_effects,
)
from data import (
    DUNGEONS,
    EQUIPMENT,
    EVENT_WEIGHTS,
    ITEMS,
    JOBS,
    MAGIC_BOOKS,
    MONSTERS,
    MONSTER_RACE_RULES,
    PHYSICAL_STATUS_EFFECTIVENESS_MULTIPLIERS,
    QUESTS,
    RECIPES,
    REGIONS,
    SHOP_INVENTORY,
    SKILLS,
    get_facility_display_name,
    get_facility_short_description,
    get_npc_display_name,
    get_region_by_dungeon,
    get_region_by_quest,
    get_unlocked_regions,
    get_dialogue,
)
from .cli_helpers import (
    GUILD_MATERIAL_BUY_PRICES,
    get_region_locked_reason,
    DUNGEON_TREASURE_CONFIG,
    DUNGEON_TRAP_CONFIG,
    DUNGEON_SPECIAL_CONFIG,
)
from .facilities import (
    STORAGE_UNLOCK_COST,
    STORAGE_CAPACITY,
    TRAVEL_SHOP_CATEGORIES,
    MAGIC_SHOP_CATEGORIES,
    SYNTHESIS_CATEGORIES,
    FIRE_MARK_GUILD_INQUIRY_FLAG,
    FIRE_MARK_CHURCH_BRIDGE_FLAG,
    FIRE_MARK_CHURCH_LOOKUP_FLAG,
    FIRE_MARK_SHARD_ID,
    BOSS_GLEN_SIGHTED_FLAG,
    BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG,
    MAIN_STORY_CLEARED_FLAG,
    next_step_hint,
    ready_quest_titles,
    town_hint_lines,
    guild_hint_lines,
    is_shop_item_available,
    travel_shop_category,
    travel_shop_owned_count,
    travel_shop_available_items,
    travel_shop_item_detail,
    travel_shop_item_line,
    travel_shop_detail_lines,
    buy_travel_shop_item,
    travel_shop_item_menu,
    travel_shop,
    equipment_owned_count,
    equipment_status_line,
    equipment_job_status,
    workshop_item_line,
    workshop_item_detail_lines,
    buy_workshop_item,
    workshop_buy_menu,
    recipe_base_status,
    recipe_material_status,
    recipe_output_summary,
    workshop_recipe_line,
    workshop_recipe_detail_lines,
    craft_recipe_message,
    workshop_upgrade_menu,
    workshop_equipment_lines,
    workshop_catalog,
    magic_book_price,
    magic_shop_category,
    magic_book_status,
    magic_shop_book_ids,
    magic_material_status,
    magic_book_line,
    magic_book_detail_lines,
    learn_magic_book_message,
    magic_shop_book_menu,
    magic_shop,
    recipe_available,
    synthesis_recipe_category,
    synthesis_available_recipes,
    recipe_output_owned_status,
    recipe_base_owned_count,
    synthesis_recipe_status,
    max_synthesis_count,
    synthesis_recipe_line,
    synthesis_recipe_detail_lines,
    craft_recipe,
    craft_recipe_list_menu,
    craft_menu,
    rest_inn,
    storage_kind_count,
    storage_has_room_for,
    prompt_quantity,
    show_storage,
    storage_deposit_menu,
    storage_withdraw_menu,
    storage_menu,
    can_accept_boss_glen_investigation,
    accept_boss_glen_investigation,
    boss_glen_investigation,
    fire_mark_guild_inquiry,
    can_ask_fire_mark_guild_inquiry,
    guild_quest_menu,
    guild_material_buy_menu,
    show_or_complete_quest,
    guild_menu,
    iron_workshop,
    armor_workshop,
    promotion_requirement_met,
    promotion_requirement_line,
    should_show_fire_mark_church_bridge,
    fire_mark_church_bridge,
    should_show_fire_mark_church_lookup,
    fire_mark_church_lookup,
    temple,
    town_menu,
)


ROOT = Path(__file__).resolve().parents[2]
SAVE_PATH = ROOT / "save.json"



MAX_COMBAT_SUMMARY_LINES = 3


BOSS_CLEAR_FLAGS = {
    "boss_glen": "boss_glen_defeated",
    "boss_ash_guardian": "ash_guardian_defeated",
    "boss_cinder_seal_sentinel": "cinder_seal_sentinel_defeated",
    "boss_ice_wreck_captain": "ice_wreck_captain_defeated",
    "boss_ice_frostroot_keeper": "ice_frostroot_keeper_defeated",
    "boss_ice_outer_gatewarden": "ice_outer_gatewarden_defeated",
    "boss_ice_final_seal_lord": "ice_final_boss_defeated",
    "boss_earth_rootwarden": "earth_rootwarden_defeated",
    "boss_earth_quarry_colossus": "earth_quarry_colossus_defeated",
    "boss_earth_outer_grovekeeper": "earth_outer_grovekeeper_defeated",
    "boss_earth_deep_leyline_lord": "earth_final_boss_defeated",
    "boss_thunder_plateau_beacon": "thunder_plateau_beacon_defeated",
    "boss_thunder_channel_keeper": "thunder_channel_keeper_defeated",
    "boss_thunder_lower_array_warden": "thunder_lower_array_warden_defeated",
    "boss_thunder_crown_storm_lord": "thunder_final_boss_defeated",
    "boss_final_echo_vanguard": "final_echo_vanguard_defeated",
    "boss_final_ruin_jailer": "final_ruin_jailer_defeated",
    "boss_final_echo_warden": "final_echo_warden_defeated",
    "boss_final_seal_core": "final_seal_core_defeated",
    "boss_final_demon_king": "final_demon_king_defeated",
}

# Compatibility imports and re-exports for extracted dungeon domain
from .dungeon import (
    BOSS_REQUIRED_QUESTS,
    BOSS_FREE_CHALLENGE,
    run_loot_summary,
    recommended_level_note,
    dungeon_gate_hint,
    dungeon_boss_status,
    dungeon_option_line,
    record_boss_glen_sighting,
    activate_boss_glen_investigation,
    choose_weighted_event,
    dungeon_menu,
    boss_available_at_dungeon_end,
    boss_challenge_prompt,
    clear_dungeon_boss,
    explore_dungeon,
    dungeon_material_event,
    dungeon_treasure_event,
    dungeon_trap_event,
    dungeon_special_event,
    handle_defeat,
    complete_final_quest_from_boss,
    show_main_story_ending,
)


@dataclass
class CombatActionResult:
    damage: int = 0
    events: list[str] = field(default_factory=list)
    summary: list[str] = field(default_factory=list)
    outcome: str | None = None
    free_action: bool = False


def combat_item_quantity(state: dict, item_id: str) -> int:
    """Return the amount legal for the current expedition."""
    if not item_job_allowed(state, item_id):
        return 0
    if item_id == "item_herb_antidote":
        return state.get("inventory", {}).get(item_id, 0)
    return min(state.get("inventory", {}).get(item_id, 0), run_supply_item_quantity(state, item_id))


def consume_combat_item(state: dict, item_id: str) -> bool:
    if item_id == "item_herb_antidote":
        return remove_item(state, item_id, 1)
    return consume_run_supply_item(state, item_id)


COMBAT_HP_RECOVERY = {
    "item_potion_s": (35, 0.30),
    "item_ice_potion_01": (70, 0.35),
    "item_earth_potion_01": (120, 0.40),
    "item_thunder_potion_01": (180, 0.48),
    "item_final_potion_01": (260, 0.55),
}
COMBAT_MP_RECOVERY = {
    "item_focus_drop": (12, 0.25),
    "item_ice_potion_02": (30, 0.30),
    "item_earth_potion_02": (40, 0.35),
    "item_thunder_potion_02": (60, 0.40),
    "item_final_potion_02": (90, 0.45),
}
COMBAT_THROWABLE_IDS = tuple(item_id for item_id, item in ITEMS.items() if item.get("kind") == "battle")
COMBAT_ITEM_IDS = (*COMBAT_HP_RECOVERY, *COMBAT_MP_RECOVERY, "item_herb_antidote", *COMBAT_THROWABLE_IDS, "item_escape_scroll")


def combat_recovery_amount(state: dict, item_id: str) -> int:
    """Return the configured fixed-or-percent recovery before the resource cap."""
    stats = get_stats(state)
    if item_id in COMBAT_HP_RECOVERY:
        fixed, ratio = COMBAT_HP_RECOVERY[item_id]
        return max(fixed, math.ceil(stats["max_hp"] * ratio))
    if item_id in COMBAT_MP_RECOVERY:
        fixed, ratio = COMBAT_MP_RECOVERY[item_id]
        return max(fixed, math.ceil(stats["max_mp"] * ratio))
    raise ValueError(f"Unsupported recovery item: {item_id}")


def combat_throwable_damage(item_id: str, enemy: dict, enemy_buffs: dict) -> tuple[int, int]:
    """Resolve a fixed battle-item hit without player-stat or critical scaling."""
    effect = ITEMS.get(item_id, {}).get("battle_effect")
    if not isinstance(effect, dict):
        raise ValueError(f"Unsupported throwable item: {item_id}")
    power = effect["power"]
    if effect["damage_type"] == "physical":
        damage = max(1, math.ceil(power - adjusted_defense(enemy, enemy_buffs, "physical") * 0.6))
    elif effect["damage_type"] == "elemental":
        damage = max(1, math.ceil(power * element_multiplier(effect["element"], enemy.get("element", ""), enemy_buffs)))
    else:
        damage = power
    return damage, effect.get("defense_down_turns", 0)


def use_combat_throwable(state: dict, item_id: str, enemy: dict, enemy_buffs: dict) -> CombatActionResult:
    """Apply a battle item once for both CLI and live GUI combat paths."""
    effect = ITEMS[item_id]["battle_effect"]
    damage, defense_down_turns = combat_throwable_damage(item_id, enemy, enemy_buffs)
    consume_combat_item(state, item_id)
    detail = []
    if defense_down_turns:
        enemy_buffs["defense_down"] = max(enemy_buffs.get("defense_down", 0), defense_down_turns)
        detail.append("敵方防禦下降")
    dot = effect.get("dot")
    if dot:
        apply_dot(
            enemy_buffs,
            dot["status"],
            dot["duration"],
            0,
            dot["damage_type"],
            "none",
            fixed_power=dot["power"],
        )
        detail.append(f"{status_display_name(dot['status'])}持續 {dot['duration']} 回合")
    suffix = f"，{'；'.join(detail)}。" if detail else "。"
    line = f"{item_name(item_id)}命中敵人，造成 {damage} 傷害{suffix}"
    return CombatActionResult(damage=damage, events=[line], summary=[line])





def buff_summary(buffs: dict) -> str:
    labels = {
        "burn": "灼傷",
        "defense_up": "防禦上升",
        "defense_down": "防禦下降",
        "quickstep": "迅步",
        "cinder_mark": "燼印",
        "bleed": "流血",
        "poison": "中毒",
        "regeneration": "再生",
    }
    active = [f"{labels.get(key, key)} {turns}" for key, turns in buffs.items() if not key.startswith("_") and isinstance(turns, int) and turns > 0]
    if buffs.get("_physical_charge", 0) > 0:
        active.append(f"Physical Charge {physical_charge(buffs)}")
    if buffs.get("_warrior_quickstep_ready"):
        active.append("迅步預備")
    if buffs.get("_rogue_pursuit"):
        active.append(f"{buffs['_rogue_pursuit']['skill_name']}追擊")
    return "、".join(active) if active else "無"


PHYSICAL_CHARGE_KEY = "_physical_charge"
MAX_PHYSICAL_CHARGE = 3
RACE_TRAIT_STATE_KEY = "_race_trait_state"
STATUS_DISPLAY_NAMES = {
    "bleed": "流血", "poison": "中毒", "burn": "灼傷",
    "sanctified_erosion": "聖蝕", "rending_wound": "裂創",
}


def status_display_name(status: str) -> str:
    return STATUS_DISPLAY_NAMES.get(status, status)


def monster_race_rule(enemy: dict) -> dict:
    return MONSTER_RACE_RULES.get(enemy.get("race"), {})


def monster_race_display_name(enemy: dict) -> str:
    return monster_race_rule(enemy).get("display_name", enemy.get("race", "未知"))


def monster_race_trait(enemy: dict) -> dict:
    return monster_race_rule(enemy).get("trait", {})


def monster_race_trait_summary(enemy: dict, enemy_buffs: dict | None = None) -> str:
    trait = monster_race_trait(enemy)
    if not trait:
        return "無"
    state = (enemy_buffs or {}).get(RACE_TRAIT_STATE_KEY, {})
    effect_kind = trait.get("effect", {}).get("kind")
    if effect_kind == "first_direct_damage_reduction":
        status = "0" if state.get("triggered") else "1"
        return f"{trait['display_name']} {status}"
    return f"{trait['display_name']}（{'已觸發' if state.get('triggered') else '待機'}）"


def _monster_race_trait_state(enemy_buffs: dict) -> dict:
    return enemy_buffs.setdefault(RACE_TRAIT_STATE_KEY, {})


def apply_monster_race_direct_damage_trait(
    enemy: dict,
    enemy_buffs: dict,
    damage: int,
    damage_type: str,
) -> tuple[int, list[str]]:
    """Consume a visible one-shot race ward on a matching direct hit."""
    trait = monster_race_trait(enemy)
    effect = trait.get("effect", {})
    state = _monster_race_trait_state(enemy_buffs)
    if (
        damage <= 0
        or state.get("triggered")
        or effect.get("kind") != "first_direct_damage_reduction"
        or effect.get("damage_type") != damage_type
    ):
        return damage, []
    reduced_damage = max(1, math.ceil(damage * (1 - effect["ratio"])))
    prevented = max(0, damage - reduced_damage)
    state.update({
        "trait_id": trait["id"],
        "triggered": True,
        "proc_count": state.get("proc_count", 0) + 1,
        "damage_prevented": state.get("damage_prevented", 0) + prevented,
    })
    label = "物理" if damage_type == "physical" else "魔法"
    return reduced_damage, [
        f"種族特性【{trait['display_name']}】吸收 {prevented} 點直接{label}傷害，效果隨即消失。"
    ]


def apply_monster_race_threshold_recovery(
    enemy: dict,
    enemy_hp: int,
    damage: int,
    enemy_buffs: dict,
) -> tuple[int, list[str]]:
    """Resolve the Plant one-shot heal as net damage on the triggering hit."""
    trait = monster_race_trait(enemy)
    trigger = trait.get("trigger", {})
    effect = trait.get("effect", {})
    state = _monster_race_trait_state(enemy_buffs)
    projected_hp = enemy_hp - damage
    if (
        damage <= 0
        or state.get("triggered")
        or trigger.get("kind") != "hp_below"
        or effect.get("kind") != "heal_max_hp"
        or projected_hp <= 0
        or projected_hp > enemy["hp"] * trigger["ratio"]
    ):
        return damage, []
    requested = math.ceil(enemy["hp"] * effect["ratio"])
    healed = min(requested, damage, max(0, enemy["hp"] - projected_hp))
    if healed <= 0:
        return damage, []
    state.update({
        "trait_id": trait["id"],
        "triggered": True,
        "proc_count": state.get("proc_count", 0) + 1,
        "healing": state.get("healing", 0) + healed,
    })
    return damage - healed, [f"種族特性【{trait['display_name']}】發動，回復 {healed} HP。"]


def prepare_monster_race_enemy_turn(
    enemy: dict,
    enemy_hp: int,
    enemy_buffs: dict,
) -> list[str]:
    """Arm or resolve deterministic one-shot race traits before an enemy turn."""
    trait = monster_race_trait(enemy)
    if not trait:
        return []
    trigger = trait.get("trigger", {})
    effect = trait.get("effect", {})
    state = _monster_race_trait_state(enemy_buffs)
    state["enemy_actions"] = state.get("enemy_actions", 0) + 1
    if state.get("triggered"):
        return []

    trigger_kind = trigger.get("kind")
    should_trigger = (
        trigger_kind == "hp_below" and enemy_hp <= enemy["hp"] * trigger["ratio"]
    ) or (
        trigger_kind == "enemy_action_count" and state["enemy_actions"] == trigger["count"]
    )
    if not should_trigger:
        return []

    state.update({
        "trait_id": trait["id"],
        "triggered": True,
        "proc_count": state.get("proc_count", 0) + 1,
    })
    if effect.get("kind") == "next_attack_multiplier":
        enemy["_race_next_attack_multiplier"] = effect["value"]
        return [f"種族特性【{trait['display_name']}】發動，下一次攻擊傷害提升。"]
    if effect.get("kind") == "buff":
        buff = effect["buff"]
        enemy_buffs[buff] = max(enemy_buffs.get(buff, 0), effect["turns"])
        return [f"種族特性【{trait['display_name']}】發動，防禦上升。"]
    return []


def parent_job(job: str) -> str:
    return {
        "元素騎士": "劍士",
        "星詠者": "法師",
        "影行者": "盜賊",
        "聖印使": "牧師"
    }.get(job, job)


def physical_charge_cap(state: dict | None = None) -> int:
    """Return the live Warrior Charge cap, including a quality weapon bonus.

    The affix value is intentionally floored after quality scaling so the
    integer stack contract remains stable across the non-normal quality bands.
    """
    if not state:
        return MAX_PHYSICAL_CHARGE
    return MAX_PHYSICAL_CHARGE + max(0, math.floor(get_stats(state).get("physical_charge_cap", 0)))


def physical_charge(player_buffs: dict, state: dict | None = None) -> int:
    return max(0, min(physical_charge_cap(state), int(player_buffs.get(PHYSICAL_CHARGE_KEY, 0))))


def gain_physical_charge(state: dict, player_buffs: dict) -> int:
    if parent_job(state.get("job", "")) != "劍士":
        return physical_charge(player_buffs, state)
    cap = physical_charge_cap(state)
    stacks = min(cap, physical_charge(player_buffs, state) + 1)
    chance = max(0, min(100, get_stats(state).get("physical_charge_gain_chance", 0)))
    if stacks < cap and random.random() * 100 < chance:
        stacks = min(cap, stacks + 1)
    player_buffs[PHYSICAL_CHARGE_KEY] = stacks
    return stacks


def consume_physical_charge(player_buffs: dict, state: dict | None = None) -> int:
    stacks = physical_charge(player_buffs, state)
    player_buffs.pop(PHYSICAL_CHARGE_KEY, None)
    player_buffs.pop("_warrior_quickstep_ready", None)
    return stacks


def passive_triggers_for_event(state: dict, event: str, **context: object) -> list[dict]:
    """Return learned passive triggers, resolving replacement groups once."""
    candidates: list[dict] = []
    for skill_id in state.get("learned_skills", []):
        skill = SKILLS.get(skill_id, {})
        if skill.get("kind") != "passive":
            continue
        for trigger in skill.get("passive_triggers", []):
            requires = trigger.get("requires", {})
            if trigger.get("job") != state.get("job") or trigger.get("event") != event:
                continue
            if event == "physical_charge_reaches" and context.get("stacks") != requires.get("stacks"):
                continue
            if event == "physical_status_applied" and context.get("status") not in requires.get("statuses", []):
                continue
            candidates.append({**trigger, "skill_id": skill_id, "skill_name": skill["name"]})
    resolved: dict[str, dict] = {}
    ungrouped: list[dict] = []
    for trigger in candidates:
        group = trigger.get("replacement_group")
        if not group:
            ungrouped.append(trigger)
        elif group not in resolved or trigger.get("priority", 0) > resolved[group].get("priority", 0):
            resolved[group] = trigger
    return [*ungrouped, *resolved.values()]


def activate_passives(state: dict, player_buffs: dict, event: str, **context: object) -> list[str]:
    events = []
    for trigger in passive_triggers_for_event(state, event, **context):
        effect = trigger["effect"]
        player_buffs[f"_{effect['state_key']}"] = {**effect, "skill_id": trigger["skill_id"], "skill_name": trigger["skill_name"]}
        if effect["kind"] == "charge_skill_bonus":
            events.append(f"{trigger['skill_name']}預備完成：下一次消耗 Physical Charge 的物理技能傷害 +{effect['damage_percent']}%。")
        else:
            events.append(f"{trigger['skill_name']}追擊窗口開啟：下一次普通攻擊追加一次追擊。")
    return events


def physical_status_effectiveness(enemy: dict, status: str) -> str:
    return monster_race_rule(enemy).get("physical_status", {}).get(status, "ineffective")


def physical_status_damage_multiplier(enemy: dict, status: str) -> float:
    if status not in {"bleed", "poison"}:
        return 1.0
    return PHYSICAL_STATUS_EFFECTIVENESS_MULTIPLIERS[physical_status_effectiveness(enemy, status)]


def calc_physical_status_damage(power: int, multiplier: float) -> int:
    """Status damage is deterministic and intentionally ignores defense."""
    return max(1, math.ceil(power * multiplier))

def combat_panel_lines(
    state: dict,
    enemy: dict,
    enemy_hp: int,
    turn: int,
    player_buffs: dict,
    enemy_buffs: dict,
    last_action_summary: str,
) -> list[str]:
    stats = get_stats(state, player_buffs)
    return [
        f"回合 {turn}",
        f"{state['name']} HP {state['current_hp']}/{stats['max_hp']} / MP {state['current_mp']}/{stats['max_mp']} / 狀態 {buff_summary(player_buffs)}",
        (
            f"{enemy['name']} HP {enemy_hp}/{enemy['hp']} / 屬性 {enemy['element']} / "
            f"種族 {monster_race_display_name(enemy)} / 特性 {monster_race_trait_summary(enemy, enemy_buffs)} / "
            f"狀態 {buff_summary(enemy_buffs)}"
        ),
        f"上一動：{last_action_summary}",
    ]

def record_battle_events(battle_log: list[str], turn: int, events: list[str]) -> None:
    for event in events:
        battle_log.append(f"回合 {turn}: {event}")

def combat_summary_lines(*groups: list[str]) -> list[str]:
    lines: list[str] = []
    for group in groups:
        for line in group:
            if line:
                lines.append(line)
            if len(lines) >= MAX_COMBAT_SUMMARY_LINES:
                return lines
    return lines

def render_combat_summary(lines: list[str], boss: bool) -> None:
    if not lines:
        return
    render_panel(
        "戰鬥結果摘要",
        lines[:MAX_COMBAT_SUMMARY_LINES],
        border_style="red" if boss else "yellow",
    )

def render_battle_log(battle_log: list[str], boss: bool) -> None:
    render_panel(
        "Battle Log",
        battle_log if battle_log else ["本場戰鬥沒有紀錄。"],
        border_style="red" if boss else "cyan",
    )

def exp_reward_for_dungeon(state: dict, amount: int, dungeon_id: str | None = None) -> dict:
    """Calculate the shared dungeon EXP reward used by CLI and GUI."""
    reward = {"base_exp": amount, "awarded_exp": amount, "multiplier": 1.0, "reason": None}
    dungeon = DUNGEONS.get(dungeon_id or "")
    if not dungeon:
        return reward
    try:
        recommended_max = int(dungeon["recommended"].replace("Lv", "").split("-")[-1])
    except (AttributeError, ValueError, IndexError):
        return reward
    if state.get("level", 1) > recommended_max + 2:
        reward.update(
            awarded_exp=math.floor(amount * 0.2),
            multiplier=0.2,
            reason=f"目前 Lv{state['level']} 高於此地圖推薦上限 Lv{recommended_max} 兩級以上",
        )
    return reward


def gain_exp(state: dict, amount: int, dungeon_id: str | None = None) -> dict:
    reward = exp_reward_for_dungeon(state, amount, dungeon_id)
    awarded_exp = reward["awarded_exp"]
    print(f"獲得經驗 {awarded_exp}。")
    if reward["reason"]:
        print(f"經驗衰減：{reward['reason']}，本次僅獲得 20%（原始 {amount} EXP）。")
    state["exp"] += awarded_exp
    while state["exp"] >= exp_to_next(state["level"]):
        state["exp"] -= exp_to_next(state["level"])
        state["level"] += 1
        stats = get_stats(state)
        state["current_hp"] = stats["max_hp"]
        state["current_mp"] = stats["max_mp"]
        print(f"等級提升！現在是 Lv{state['level']}，HP/MP 已回滿。")

    return reward


def save_game(state: dict) -> None:
    SAVE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已存檔：{SAVE_PATH}")

def load_game() -> dict | None:
    if not SAVE_PATH.exists():
        return None
    try:
        return ensure_state_defaults(json.loads(SAVE_PATH.read_text(encoding="utf-8")))
    except Exception:
        print("存檔讀取失敗，請重新開始。")
        return None

def new_game() -> dict:
    title("元素迷宮：邊境冒險者")
    name = input("請輸入冒險者名字 > ").strip() or "見習冒險者"
    jobs = list(JOBS.keys())
    choice = menu("選擇初始職業", jobs, allow_back=False)
    job = jobs[choice - 1]
    state = create_state(name, job)
    show_story_beat(
        take_story_beat(
            state,
            "prologue.new_game",
            context={"player": name, "job": job},
        )
    )
    return state

def show_status(state: dict) -> None:
    clamp_vitals(state)
    render_panel("角色狀態", player_resource_lines(state), border_style="cyan")

    slot_names = {"weapon": "武器", "head": "頭部", "body": "身體", "accessory": "飾品", "special": "特殊"}
    equipment_lines = []
    for slot, label in slot_names.items():
        item_id = state["equipment"].get(slot)
        equipment_lines.append(f"{label}: {item_name(item_id, state) if item_id else '無'}")
    render_panel("裝備", equipment_lines, border_style="green")

    skill_lines = []
    for skill_id in state["learned_skills"]:
        skill = SKILLS[skill_id]
        skill_lines.append(f"{skill['name']} / MP {skill['mp']}: {skill['desc']}")
    render_panel("技能", skill_lines, border_style="magenta")

    show_job_specialization_preview(state["job"])

def show_inventory(state: dict) -> None:
    if not state["inventory"]:
        render_panel("背包與素材", ["背包目前是空的。"], border_style="green")
        return
    lines = []
    for item_id, qty in sorted(state["inventory"].items(), key=lambda pair: item_name(pair[0])):
        lines.append(f"{item_name(item_id, state)} x{qty} / {item_usage_summary(item_id, state)}")
    render_panel("背包與素材", lines, border_style="green")

def item_usage_summary(item_id: str, state: dict | None = None) -> str:
    data = ITEMS.get(item_id) or EQUIPMENT.get(item_id)
    desc = data.get("desc", "") if data else ""
    usage = []
    from .equipment_refs import is_equipment_ref
    if item_id in EQUIPMENT or (state and is_equipment_ref(state, item_id)):
        usage.append("可裝備")
    if item_id in {"item_potion_s", "item_potion_m", "item_focus_drop", "item_herb_antidote", "item_armor_piercer", "item_escape_scroll"}:
        usage.append("戰鬥可用")
    if is_key_item(item_id):
        usage.append("關鍵道具")
    quest_titles = [
        quest["title"]
        for quest in QUESTS.values()
        if item_id in quest.get("turn_in", {})
    ]
    if quest_titles:
        usage.append(f"任務：{'、'.join(quest_titles[:2])}")
    recipe_names = [
        recipe["name"]
        for recipe in RECIPES.values()
        if item_id in recipe.get("materials", {}) or recipe.get("base_item") == item_id
    ]
    if recipe_names:
        usage.append(f"配方：{'、'.join(recipe_names[:2])}")
    if item_id in GUILD_MATERIAL_BUY_PRICES:
        usage.append(f"工會收購 {GUILD_MATERIAL_BUY_PRICES[item_id]}G")
    if usage:
        return f"{desc} 用途：{'；'.join(usage)}。"
    return desc or "目前沒有額外用途提示。"

def equipment_menu(state: dict) -> None:
    while True:
        from .equipment_refs import inventory_equipment_refs
        equippables = inventory_equipment_refs(state)
        slot_names = {"weapon": "武器", "head": "頭部", "body": "身體", "accessory": "飾品", "special": "特殊"}
        current_lines = [
            f"{slot_names.get(slot, slot)}: {item_name(item_id, state) if item_id else '無'}"
            for slot, item_id in state["equipment"].items()
        ]
        render_panel("目前裝備", current_lines, border_style="green")
        if not equippables:
            print("\n背包裡沒有可裝備物品。")
            pause()
            return
        options = [f"{item_name(item_id, state)} - {equipment_summary(item_id, state)}" for item_id in equippables]
        choice = action_menu_panel(
            "選擇要裝備的物品",
            options,
            "裝備管理",
            header_lines=["選擇物品後會替換同欄位目前裝備。"],
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        item_id = equippables[choice - 1]
        comparison = equipment_comparison(state, item_id)
        candidate = comparison["candidate"]
        equipped = comparison["equipped"]
        comparison_lines = [
            f"候選：{candidate['name']} / 普通 / +0",
            f"目前：{equipped['name'] if equipped else '無'} / 普通 / +0" if equipped else "目前：無",
        ]
        for stat, values in comparison["stats"].items():
            if values["delta"]:
                comparison_lines.append(f"{stat}: {values['before']} → {values['after']} ({values['delta']:+})")
        comparison_lines.append("詞綴：無 → 無")
        render_panel("裝備比較", comparison_lines, border_style="cyan")
        if comparison["compatible"] and action_menu_panel(
            "確認替換", ["裝備此物品"], "裝備比較", allow_back=True, border_style="green"
        ) == 1:
            equip_item(state, item_id)
        pause()



def buy_menu(state: dict, shop_name: str, item_ids: list[str]) -> None:
    while True:
        available = [item_id for item_id in item_ids if is_shop_item_available(state, item_id)]
        options = []
        for item_id in available:
            data = ITEMS.get(item_id) or EQUIPMENT[item_id]
            if item_id in EQUIPMENT:
                detail = equipment_summary(item_id)
            else:
                detail = data.get("desc", "")
            options.append(f"{item_name(item_id)} / {data['price']}G / {detail}")
        if not options:
            render_panel(shop_name, ["目前沒有可購買商品。"], border_style="green")
            pause()
            return
        choice = action_menu_panel(
            "選擇商品",
            options,
            shop_name,
            header_lines=[f"持有金幣：{state['gold']}G"],
            hint_lines=["購買後會放入背包；裝備仍需到背包/裝備中替換。"],
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        item_id = available[choice - 1]
        data = ITEMS.get(item_id) or EQUIPMENT[item_id]
        price = data["price"]
        if state["gold"] < price:
            print("金幣不足。")
        elif item_id in EQUIPMENT and state["job"] not in EQUIPMENT[item_id]["jobs"]:
            print(f"{state['job']}無法使用這件裝備，先別買比較好。")
        else:
            state["gold"] -= price
            add_item(state, item_id, 1)
            print(f"購買了 {item_name(item_id)}。")
        pause()


def try_register_bestiary(state: dict, monster_id: str) -> bool:
    ensure_state_defaults(state)
    if monster_id not in MONSTERS or monster_id in state["bestiary"]:
        return False
    state["bestiary"].append(monster_id)
    print(f"怪物圖鑑新增：{MONSTERS[monster_id]['name']}。")
    return True

def bestiary_menu(state: dict) -> None:
    ensure_state_defaults(state)
    while True:
        registered_ids = [monster_id for monster_id in MONSTERS if monster_id in state["bestiary"]]
        title("怪物圖鑑")
        if not registered_ids:
            print("尚未登錄任何怪物。擊敗怪物後，圖鑑會自動記錄。")
            pause()
            return

        options = [MONSTERS[monster_id]["name"] for monster_id in registered_ids]
        choice = menu("選擇怪物", options)
        if choice == 0:
            return

        monster_id = registered_ids[choice - 1]
        monster = MONSTERS[monster_id]
        locations = monster_locations(monster_id)
        gold_min, gold_max = monster["gold"]
        gold_text = f"{gold_min}G" if gold_min == gold_max else f"{gold_min}-{gold_max}G"

        title(monster["name"])
        print(f"屬性：{monster['element']}")
        print(f"HP：{monster['hp']}")
        print(f"攻擊：{monster['attack']}")
        print(f"經驗值：{monster['exp']}")
        print(f"金錢：{gold_text}")
        print(f"出現地點：{'、'.join(locations) if locations else '未知'}")
        print(f"掉落物：{monster_drop_names(monster)}")
        pause()

def backpack_menu(state: dict, allow_storage: bool = False) -> None:
    while True:
        options = ["查看背包與素材用途", "裝備管理"]
        if allow_storage:
            options.append("倉庫")
        choice = action_menu_panel(
            "選擇動作",
            options,
            "背包 / 裝備",
            header_lines=player_resource_lines(state)[:2],
            hint_lines=["背包會顯示描述、任務、配方與收購用途；裝備管理用來實際替換裝備。"],
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        if choice == 1:
            show_inventory(state)
            pause()
        elif choice == 2:
            equipment_menu(state)
        elif allow_storage and choice == 3:
            storage_menu(state)
ELEMENT_ALIASES = {
    "fire": "fire", "Fire": "fire", "火": "fire",
    "ice": "ice", "Ice": "ice", "冰": "ice",
    "earth": "earth", "Earth": "earth", "地": "earth", "自然": "earth",
    "thunder": "thunder", "Thunder": "thunder", "雷": "thunder",
    "physical": "physical", "物理": "physical", "none": "none", "無": "none", "Final": "final",
}
ELEMENT_COUNTERS = {"ice": "fire", "fire": "earth", "earth": "thunder", "thunder": "ice"}
ELEMENT_RESIST_KEYS = {"fire": "fire_resist", "ice": "ice_resist", "earth": "earth_resist", "thunder": "thunder_resist"}


def normalized_element(element: str | None) -> str:
    return ELEMENT_ALIASES.get(element or "", element or "none")


def element_multiplier(attack_element: str, target_element: str, enemy_buffs: dict | None = None) -> float:
    attack = normalized_element(attack_element)
    target = normalized_element(target_element)
    multiplier = 1.25 if ELEMENT_COUNTERS.get(attack) == target else 0.80 if ELEMENT_COUNTERS.get(target) == attack else 1.0
    return multiplier


def elemental_resistance(target: dict, attack_element: str) -> int:
    return max(0, min(75, target.get(ELEMENT_RESIST_KEYS.get(normalized_element(attack_element), ""), 0)))


def direct_damage_roll(agility: int) -> float:
    agility = max(0, agility)
    high_damage_chance = min(30.0, agility * 0.15)
    if random.random() * 100 < high_damage_chance:
        return random.uniform(1.15, 1.45)
    return random.uniform(0.80, 1.10)


def adjusted_defense(target: dict, buffs: dict, damage_type: str) -> int:
    key = "magic_defense" if damage_type == "magic" else "defense"
    defense = target.get(key, target.get("defense", 0))
    if damage_type == "physical":
        if buffs.get("defense_up", 0) > 0:
            defense = math.ceil(defense * 1.15)
        if buffs.get("defense_down", 0) > 0:
            defense = max(1, math.floor(defense * 0.8))
    return defense


def calc_typed_damage(power: int, multiplier: float, target: dict, target_buffs: dict, damage_type: str, element: str, *, agility: int = 0, crit_chance: int = 0, crit_damage_percent: int = 0, direct: bool = False) -> tuple[int, bool]:
    defense = adjusted_defense(target, target_buffs, damage_type)
    base = max(1, power * multiplier - defense * 0.6)
    base *= element_multiplier(element, target.get("element", ""), target_buffs)
    base *= 1 - elemental_resistance(target, element) / 100
    is_crit = False
    if direct:
        base *= direct_damage_roll(agility)
        is_crit = random.randint(1, 100) <= max(0, crit_chance)
        if is_crit:
            base *= 1.5 * (1 + crit_damage_percent / 100)
    return max(1, math.ceil(base)), is_crit


def calc_player_damage(state: dict, enemy: dict, skill: dict | None, player_buffs: dict, enemy_buffs: dict) -> tuple[int, bool]:
    stats = get_stats(state, player_buffs)
    is_magic = bool(skill and skill.get("stat") == "magic")
    power = stats["magic_attack"] if is_magic else stats["attack"]
    multiplier = skill.get("multiplier", 1.0) if skill else 1.0
    promotion_id = state.get("promotion_id")
    promotion_config = {}
    if promotion_id:
        from data import PROMOTIONS
        promotion_config = PROMOTIONS.get(promotion_id, {}).get("config", {})
    relic_effects = active_relic_passive_effects(state)
    direct_bonus = relic_effects.get("direct_damage_percent", 0)
    direct_bonus += relic_effects.get("direct_magic_damage_percent" if is_magic else "direct_physical_damage_percent", 0)
    attack_element = skill.get("element", "物理") if skill else "物理"
    if is_magic and normalized_element(attack_element) in ELEMENT_RESIST_KEYS:
        direct_bonus += stats.get("elemental_magic_direct_percent", 0)
    multiplier *= 1 + direct_bonus / 100
    if skill and skill.get("charge_bonus_per_stack"):
        per_stack_bonus = skill["charge_bonus_per_stack"] + stats.get("physical_charge_skill_bonus", 0) / 100
        multiplier += physical_charge(player_buffs, state) * per_stack_bonus
        ready = player_buffs.get("_warrior_quickstep_ready", {})
        if ready.get("kind") == "charge_skill_bonus":
            multiplier *= 1 + ready["damage_percent"] / 100
    if skill and skill.get("charge_bonus_per_stack") and promotion_id == "promotion_blood_blade":
        multiplier += player_buffs.get("blood_blade_active", 0) * promotion_config.get("charge_bonus_per_stack", 0)
    if promotion_id == "promotion_miasma_hunter":
        afflicted = sum(enemy_buffs.get(status, 0) > 0 for status in ("bleed", "poison"))
        if afflicted:
            multiplier *= 1 + promotion_config.get("passive_damage_bonus_percent", 0) / 100
    mark_data = enemy_buffs.get("_debuff_data", {}).get("cinder_mark", {})
    if (
        is_magic
        and normalized_element(attack_element) in ELEMENT_RESIST_KEYS
        and mark_data.get("damage_scope") == "elemental_magic"
    ):
        multiplier *= 1 + mark_data["damage_percent"] / 100
    crit_chance = stats["crit"] + (skill.get("crit_bonus", 0) if skill else 0)
    crit_damage_percent = relic_effects.get("crit_damage_percent", 0) + (skill.get("crit_damage_percent", 0) if skill else 0)
    return calc_typed_damage(
        power, multiplier, enemy, enemy_buffs, "magic" if is_magic else "physical", attack_element,
        agility=stats["agility"], crit_chance=crit_chance,
        crit_damage_percent=crit_damage_percent, direct=True,
    )

def normal_attack_followup(state: dict, skill: dict | None) -> tuple[dict, dict] | None:
    if skill is not None:
        return None
    head_id = state["equipment"].get("head")
    head = EQUIPMENT.get(head_id, {})
    followup = head.get("normal_attack_followup")
    if not followup:
        return None
    return head, followup


def calc_normal_attack_followup_damage(state: dict, enemy: dict, player_buffs: dict, enemy_buffs: dict, followup: dict, bonus_multiplier: float = 1.0) -> int:
    stats = get_stats(state, player_buffs)
    relic_effects = active_relic_passive_effects(state)
    multiplier = followup["multiplier"] * bonus_multiplier * (1 + (relic_effects.get("direct_damage_percent", 0) + relic_effects.get("direct_physical_damage_percent", 0)) / 100)
    damage, _ = calc_typed_damage(stats["attack"], multiplier, enemy, enemy_buffs, "physical", followup["element"])
    return damage

def calc_enemy_damage(enemy: dict, state: dict, multiplier: float, element: str, player_buffs: dict, defending: bool) -> int:
    stats = get_stats(state, player_buffs)
    is_magic = normalized_element(element) in ELEMENT_RESIST_KEYS
    power = enemy.get("magic_attack", enemy["attack"]) if is_magic else enemy["attack"]
    multiplier *= enemy.pop("_race_next_attack_multiplier", 1.0)
    damage, _ = calc_typed_damage(power, multiplier, stats, {}, "magic" if is_magic else "physical", element)
    if defending:
        damage = max(1, math.ceil(damage * 0.6))

    # 聖幕司祭護盾吸收邏輯
    if player_buffs.get("holy_veil_shield", 0) > 0 and player_buffs.get("_holy_veil_shield_value", 0) > 0:
        shield = player_buffs["_holy_veil_shield_value"]
        absorbed = min(damage, shield)
        damage -= absorbed
        player_buffs["_holy_veil_shield_value"] -= absorbed
        player_buffs.setdefault("_shield_absorb_logs", []).append(f"聖幕結界吸收了 {absorbed} 點傷害。")

        # 觸發反震：每敵方行動最多一次
        if not player_buffs.get("_holy_veil_reflected_this_action"):
            player_buffs["_holy_veil_reflected_this_action"] = True
            from data import PROMOTIONS
            promo = PROMOTIONS.get(state.get("promotion_id", ""))
            reflect_mult = promo["config"].get("reflect_multiplier", 0.8) if promo else 0.8
            reflect_damage = max(1, math.ceil(stats["magic_attack"] * reflect_mult))
            player_buffs["_reflect_damage_queue"] = player_buffs.get("_reflect_damage_queue", 0) + reflect_damage
            player_buffs.setdefault("_shield_absorb_logs", []).append(f"聖幕結界反震，對敵人造成 {reflect_damage} 點神聖傷害。")

        if player_buffs["_holy_veil_shield_value"] <= 0:
            player_buffs.pop("holy_veil_shield", None)
            player_buffs.pop("_holy_veil_shield_value", None)

    return damage

def combat(state: dict, enemy_id: str, boss: bool = False, run_log: dict | None = None):
    enemy = deepcopy(MONSTERS[enemy_id])
    enemy_hp = enemy["hp"]
    player_buffs = {}
    enemy_buffs = {}
    # 聖蝕聖瓶初始計數
    initial_vials = state.get("inventory", {}).get("item_sanctified_ash_vial", 0)
    if state.get("job") == "影行者":
        player_buffs["_rogue_pursuit"] = {"skill_name": "影行者身法", "followup_multiplier": 1.8}
    turn = 1
    boss_marker = False
    last_action_summary = "尚未行動。"
    race_name = monster_race_display_name(enemy)
    trait_name = monster_race_trait(enemy).get("display_name", "無")
    battle_log = [
        f"遭遇 {enemy['name']}。敵人屬性：{enemy['element']} / 種族：{race_name} / 特性：{trait_name} / HP {enemy_hp}/{enemy['hp']}。"
    ]
    render_panel(
        f"遭遇 {enemy['name']}",
        [
            f"敵人屬性：{enemy['element']} / 種族：{race_name} / HP {enemy_hp}/{enemy['hp']}",
            f"種族特性：{trait_name}",
            "觀察敵我狀態後選擇攻擊、防禦、技能或道具。",
        ],
        border_style="red" if boss else "yellow",
    )
    while enemy_hp > 0 and state["current_hp"] > 0:
        clamp_vitals(state)
        enemy["current_hp"] = enemy_hp

        options = ["攻擊", "防禦", "技能", "道具"]
        if not boss:
            options.append("逃跑")
        choice = action_menu_panel(
            "戰鬥指令",
            options,
            "戰鬥狀態",
            header_lines=combat_panel_lines(state, enemy, enemy_hp, turn, player_buffs, enemy_buffs, last_action_summary),
            hint_lines=["Boss 戰不可逃跑。" if boss else "逃跑失敗時敵人仍會行動。"],
            allow_back=False,
            border_style="red" if boss else "yellow",
        )
        defending = False
        action_result = CombatActionResult()

        if choice == 1:
            action_result = player_attack(state, enemy, enemy_hp, None, player_buffs, enemy_buffs)
            enemy_hp -= action_result.damage
        elif choice == 2:
            defending = True
            events = []
            if player_buffs.get("defense_up", 0) > 0:
                stats = get_stats(state, player_buffs)
                state["current_mp"] = min(stats["max_mp"], state["current_mp"] + 2)
                events.append("你穩住姿勢，符文讓你回復 MP 2。")
            events.append("你採取防禦姿態。")
            action_result = CombatActionResult(events=events, summary=["你採取防禦姿態。"])
        elif choice == 3:
            result = skill_menu(state, enemy, player_buffs, enemy_buffs)
            if result.outcome == "cancel":
                render_combat_summary(result.summary, boss)
                if result.summary:
                    last_action_summary = result.summary[0]
                continue
            action_result = result
            enemy_hp -= action_result.damage
        elif choice == 4:
            result = combat_item_menu(state, boss, enemy_buffs, enemy, player_buffs.get("_mp_item_used", False))
            if result.outcome == "cancel":
                render_combat_summary(result.summary, boss)
                if result.summary:
                    last_action_summary = result.summary[0]
                continue
            action_result = result
            if action_result.outcome == "escaped":
                record_battle_events(battle_log, turn, action_result.events)
                summary = combat_summary_lines(action_result.summary)
                render_combat_summary(summary, boss)
                render_battle_log(battle_log, boss)
                return "fled"
            enemy_hp -= action_result.damage
            if action_result.free_action:
                player_buffs["_mp_item_used"] = True
                record_battle_events(battle_log, turn, action_result.events)
                render_combat_summary(action_result.summary, boss)
                if action_result.summary:
                    last_action_summary = action_result.summary[0]
                continue
        elif not boss and choice == 5:
            if try_escape(state, enemy):
                action_result = CombatActionResult(
                    events=["你成功脫離戰鬥。"],
                    summary=["你成功脫離戰鬥。"],
                    outcome="fled",
                )
                record_battle_events(battle_log, turn, action_result.events)
                render_combat_summary(action_result.summary, boss)
                render_battle_log(battle_log, boss)
                return "fled"
            action_result = CombatActionResult(events=["逃跑失敗。"], summary=["逃跑失敗。"])

        turn_events = list(action_result.events)
        if enemy_hp <= 0:
            turn_events.append(f"{enemy['name']}倒下。")
            record_battle_events(battle_log, turn, turn_events)
            summary = combat_summary_lines(action_result.summary, [f"{enemy['name']}倒下。"])
            render_combat_summary(summary, boss)
            if summary:
                last_action_summary = summary[0]
            break

        # 同步當前 HP 至 enemy 字典以利低生命/被動判定
        enemy["current_hp"] = enemy_hp

        # 重置反震限制
        player_buffs.pop("_holy_veil_reflected_this_action", None)

        boss_marker, enemy_events = dispatch_enemy_turn(
            enemy_id,
            enemy,
            enemy_hp,
            state,
            player_buffs,
            enemy_buffs,
            defending,
            turn,
            boss_marker,
        )

        # 收集護盾吸收日誌
        absorb_logs = player_buffs.pop("_shield_absorb_logs", [])
        for log in absorb_logs:
            enemy_events.append(log)

        # 扣減反震傷害
        reflect_damage = player_buffs.pop("_reflect_damage_queue", 0)
        if reflect_damage > 0:
            enemy_hp = max(0, enemy_hp - reflect_damage)

        # 星裂術 MP 回復被動與印記引爆 log 收集
        sigil_logs = player_buffs.pop("_sigil_detonate_logs", [])
        for d in sigil_logs:
            enemy_events.append(f"【被動】印紋引爆！追加造成 {d} 點魔法傷害，並清除了印記。")

        effect_result = tick_effects(state, player_buffs, enemy_buffs, enemy)
        player_buffs.pop("_mp_item_used", None)
        effect_events, dot_damage = effect_result
        enemy_hp -= dot_damage
        turn_events.extend(enemy_events)
        turn_events.extend(effect_events)
        record_battle_events(battle_log, turn, turn_events)
        summary = combat_summary_lines(action_result.summary, enemy_events, effect_events)
        render_combat_summary(summary, boss)
        if summary:
            last_action_summary = " / ".join(summary[:2])
        turn += 1

    if state["current_hp"] <= 0:
        battle_log.append("戰鬥結束：你倒下了。")
        render_combat_summary(["你倒下了。"], boss)
        render_battle_log(battle_log, boss)
        return False

    print(f"\n擊敗 {enemy['name']}！")
    # 聖蝕司祭返還聖瓶邏輯
    if state.get("promotion_id") == "promotion_holy_eclipse" and player_buffs.get("_holy_eclipse_vial_marked"):
        current_vials = state.get("inventory", {}).get("item_sanctified_ash_vial", 0)
        if current_vials < initial_vials:
            add_item(state, "item_sanctified_ash_vial", 1)
            print("【被動】聖蝕司祭淨化儀式：戰鬥勝利，返還本戰消耗的聖蝕聖瓶 x1。")
    try_register_bestiary(state, enemy_id)
    gain_exp(state, enemy["exp"], (run_log or {}).get("dungeon_id"))
    gold = random.randint(*enemy["gold"])
    add_gold(state, gold, run_log)
    print(f"獲得 {gold}G。")
    for item_id, chance, qty in enemy["drops"]:
        stats = get_stats(state)
        final_chance = chance + stats.get("rare_drop", 0) / 100
        if random.random() <= final_chance:
            add_loot(state, item_id, qty, run_log)
            print(f"取得 {item_name(item_id)} x{qty}。")
    if enemy_id == "mon_scorched_guard":
        unlock(state, "item_armor_piercer")
        unlock(state, "recipe_piercing_bundle")
        print("你摸清了斥候的護甲結構，旅人小鋪開始販售破甲釘，米菈也能製作破甲釘組。")
    if enemy_id == "mon_lava_imp":
        unlock(state, "recipe_heat_charm")
    result_lines = [f"擊敗 {enemy['name']}。", f"目前 {player_summary_line(state)}"]
    if run_log is not None:
        result_lines.append(run_loot_summary(run_log))
    result_lines.append("Boss 結果將在迷宮結算中處理。" if boss else next_step_hint(state))
    render_panel("戰鬥結算", result_lines, border_style="red" if boss else "green")
    render_battle_log(battle_log, boss)
    return True

def player_attack(state: dict, enemy: dict, enemy_hp: int, skill: dict | None, player_buffs: dict, enemy_buffs: dict):
    damage, is_crit = calc_player_damage(state, enemy, skill, player_buffs, enemy_buffs)
    is_magic = bool(skill and skill.get("stat") == "magic")
    damage, race_events = apply_monster_race_direct_damage_trait(
        enemy, enemy_buffs, damage, "magic" if is_magic else "physical",
    )
    label = skill["name"] if skill else "普通攻擊"
    crit_text = " 暴擊！" if is_crit else ""
    events = [f"你使用{label}，造成 {damage} 傷害。{crit_text}"]
    summary = [f"你使用{label}，造成 {damage} 傷害。{crit_text}"]
    events.extend(race_events)
    summary.extend(race_events)
    pursuit = player_buffs.pop("_rogue_pursuit", None) if skill is None else None
    if skill and skill.get("charge_bonus_per_stack"):
        consumed = consume_physical_charge(player_buffs, state)
        if consumed:
            charge_line = f"消耗 Physical Charge {consumed} 層。"
            events.append(charge_line)
            summary.append(charge_line)
    elif skill is None and parent_job(state.get("job")) == "劍士":
        stacks = gain_physical_charge(state, player_buffs)
        charge_line = f"Physical Charge 增加至 {stacks}/{physical_charge_cap(state)}。"
        events.append(charge_line)
        summary.append(charge_line)
        passive_events = activate_passives(state, player_buffs, "physical_charge_reaches", stacks=min(stacks, MAX_PHYSICAL_CHARGE))
        events.extend(passive_events)
        summary.extend(passive_events)
        if state.get("job") == "元素騎士":
            stats = get_stats(state, player_buffs)
            elemental_bonus = max(1, int(stats["attack"] * 0.15))
            damage += elemental_bonus
            element = random.choice(["火", "冰", "自然", "雷"])
            events.append(f"元素騎士的劍刃激盪出{element}元素傷害，追加 {elemental_bonus} 傷害。")
            summary.append(f"元素追擊 {elemental_bonus} 傷害。")
    followup_data = normal_attack_followup(state, skill)
    if followup_data and enemy_hp - damage > 0:
        followup_equipment, followup = followup_data
        followup_damage = calc_normal_attack_followup_damage(state, enemy, player_buffs, enemy_buffs, followup)
        followup_damage, race_events = apply_monster_race_direct_damage_trait(
            enemy, enemy_buffs, followup_damage, "physical",
        )
        damage += followup_damage
        events.append(f"{followup_equipment['name']}順勢劃出追擊，造成 {followup_damage} 傷害。")
        summary.append(f"{followup_equipment['name']}追擊 {followup_damage} 傷害。")
        events.extend(race_events)
        summary.extend(race_events)
        if followup.get("on_hit"):
            effect_events, applied_status = apply_weapon_effect(state, enemy, followup["on_hit"], enemy_buffs)
            events.extend(effect_events)
            summary.extend(effect_events)
            if applied_status:
                passive_events = activate_passives(state, player_buffs, "physical_status_applied", status=applied_status)
                events.extend(passive_events)
                summary.extend(passive_events)
    if pursuit and followup_data and enemy_hp - damage > 0:
        followup_equipment, followup = followup_data
        pursuit_damage = calc_normal_attack_followup_damage(
            state, enemy, player_buffs, enemy_buffs, followup, pursuit["followup_multiplier"],
        )
        pursuit_damage, race_events = apply_monster_race_direct_damage_trait(
            enemy, enemy_buffs, pursuit_damage, "physical",
        )
        damage += pursuit_damage
        pursuit_line = f"{pursuit['skill_name']}追擊發動，{followup_equipment['name']}追加造成 {pursuit_damage} 傷害。"
        events.append(pursuit_line)
        summary.append(pursuit_line)
        events.extend(race_events)
        summary.extend(race_events)
    if skill and skill.get("on_hit"):
        effect_events, applied_status = apply_weapon_effect(state, enemy, skill["on_hit"], enemy_buffs)
        events.extend(effect_events)
        summary.extend(effect_events)
        if applied_status:
            passive_events = activate_passives(state, player_buffs, "physical_status_applied", status=applied_status)
            events.extend(passive_events)
            summary.extend(passive_events)
    if skill and skill.get("stat") == "magic" and enemy_buffs.get("sigil_mage_mark", 0) > 0:
        marked_element = enemy_buffs.get("_sigil_element")
        if normalized_element(marked_element) == normalized_element(skill.get("element")):
            from data import PROMOTIONS
            config = PROMOTIONS["promotion_sigil_mage"]["config"]
            detonation, _ = calc_typed_damage(
                get_stats(state, player_buffs)["magic_attack"], config["detonate_multiplier"],
                enemy, enemy_buffs, "magic", "none",
            )
            detonation, race_events = apply_monster_race_direct_damage_trait(
                enemy, enemy_buffs, detonation, "magic",
            )
            damage += detonation
            enemy_buffs.pop("sigil_mage_mark", None)
            enemy_buffs.pop("_sigil_element", None)
            events.append(f"印紋引爆，追加造成 {detonation} 點魔法傷害。")
            summary.append(f"印紋引爆 +{detonation} 傷害。")
            events.extend(race_events)
            summary.extend(race_events)
    if skill and skill.get("_skill_id") == "skill_star_fracture":
        if element_multiplier(skill.get("element", "none"), enemy.get("element", "")) > 1:
            from data import PROMOTIONS
            refund = PROMOTIONS["promotion_star_fracture"]["config"].get("weakness_mp_refund", 0)
            state["current_mp"] = min(get_stats(state)["max_mp"], state["current_mp"] + refund)
            events.append(f"星裂契合弱點，回復 {refund} MP。")
            summary.append(f"弱點回復 {refund} MP。")
    if is_magic and is_crit and state.get("job") == "星詠者":
        state["current_mp"] = min(get_stats(state)["max_mp"], state["current_mp"] + 3)
        events.append("星詠者的星光引導，暴擊回復 3 MP。")
        summary.append("星光回復 3 MP。")
    damage, race_events = apply_monster_race_threshold_recovery(enemy, enemy_hp, damage, enemy_buffs)
    events.extend(race_events)
    summary.extend(race_events)
    lifesteal_percent = active_relic_passive_effects(state).get("physical_lifesteal_percent", 0)
    if not is_magic and lifesteal_percent:
        stats = get_stats(state, player_buffs)
        healed = min(math.floor(damage * lifesteal_percent / 100), max(0, stats["max_hp"] - state["current_hp"]))
        if healed:
            state["current_hp"] += healed
            line = f"火之聖印汲取 {healed} HP。"
            events.append(line)
            summary.append(line)
    return CombatActionResult(damage=damage, events=events, summary=summary)



def apply_dot(
    enemy_buffs: dict,
    status: str,
    duration: int,
    multiplier: float,
    damage_type: str,
    element: str,
    *,
    fixed_power: int | None = None,
) -> None:
    enemy_buffs[status] = duration
    enemy_buffs.setdefault("_dot_data", {})[status] = {
        "multiplier": multiplier,
        "damage_type": damage_type,
        "element": element,
    }
    if fixed_power is not None:
        enemy_buffs["_dot_data"][status]["fixed_power"] = fixed_power


def apply_weapon_effect(state: dict, enemy: dict, effect: dict, enemy_buffs: dict) -> tuple[list[str], str | None]:
    stats = get_stats(state)
    chance = max(35, min(95, effect.get("chance", 0) + stats.get("effect_accuracy", 0) - enemy.get("physical_status_resist", 0)))
    status = effect["status"]
    if status in {"bleed", "poison"} and physical_status_effectiveness(enemy, status) == "ineffective":
        return [f"{enemy['name']} 的種族不受{status_display_name(status)}影響。"], None
    if random.randint(1, 100) > chance:
        return [f"{status_display_name(status)}附加失敗。"], None
    if status == "defense_down":
        enemy_buffs[status] = effect["duration"]
        return [f"{status_display_name(status)}附加成功。"], status
    apply_dot(enemy_buffs, status, effect["duration"], effect["multiplier"], effect.get("damage_type", "physical"), effect.get("element", "物理"))
    return [f"{status_display_name(status)}附加成功，持續 {effect['duration']} 回合。"], status

def execute_skill(state: dict, enemy: dict, skill_id: str, skill: dict, player_buffs: dict, enemy_buffs: dict) -> CombatActionResult:
    stats = get_stats(state, player_buffs)
    skill = {**skill, "_skill_id": skill_id}
    from data import PROMOTIONS

    # 1. 扣 HP 的技能（血鋒/血鎧）
    if skill_id in {"skill_blood_blade_strike", "skill_blood_armor_shield"}:
        max_hp = stats["max_hp"]
        hp_cost = int(max_hp * 0.15)
        if state["current_hp"] <= hp_cost:
            return CombatActionResult(events=["HP 不足，無法安全支付生命代價。"], summary=["HP 不足，無法安全支付生命代價。"], outcome="cancel")
        state["current_hp"] -= hp_cost

    # 2. 處理元素選擇技能的 element 賦予
    if skill_id in {"skill_star_fracture", "skill_sigil_mage"} and not skill.get("element"):
        learned_elements = []
        for sk_id in state.get("learned_skills", []):
            sk = SKILLS.get(sk_id)
            if sk and sk.get("element") in {"火", "冰", "自然", "雷"}:
                elem = sk["element"]
                if elem not in learned_elements:
                    learned_elements.append(elem)
        if not learned_elements:
            return CombatActionResult(events=["尚未學會火、冰、自然、雷中任何一項元素魔法。"], summary=["無可用元素魔法。"], outcome="cancel")

        if len(learned_elements) == 1:
            chosen_element = learned_elements[0]
        else:
            choice = action_menu_panel(
                "選擇施放元素",
                learned_elements,
                "元素選擇",
                hint_lines=["此技能必須以學會的元素施放。"],
                allow_back=False,
                border_style="magenta"
            )
            chosen_element = learned_elements[choice - 1]

        skill = {**skill, "element": chosen_element}

    if skill_id == "skill_star_fracture":
        config = PROMOTIONS["promotion_star_fracture"]["config"]
        multiplier = config["multiplier"]
        if element_multiplier(skill["element"], enemy.get("element", "")) > 1:
            multiplier *= 1 + config.get("weakness_multiplier_bonus", 0)
        skill = {**skill, "stat": "magic", "multiplier": multiplier}
    elif skill_id == "skill_shadow_slayer_execute":
        config = PROMOTIONS["promotion_shadow_slayer"]["config"]
        low_hp = enemy.get("current_hp", enemy.get("hp", 1)) / max(1, enemy.get("hp", 1)) < config["threshold_hp_percent"] / 100
        skill = {
            **skill,
            "multiplier": config["execute_multiplier"] if low_hp else config["base_multiplier"],
            "crit_bonus": config["passive_crit_bonus"] if low_hp else 0,
            "crit_damage_percent": config["passive_crit_damage_percent"] if low_hp else 0,
        }
    elif skill_id == "skill_miasma_strike":
        config = PROMOTIONS["promotion_miasma_hunter"]["config"]
        status_count = sum(enemy_buffs.get(status, 0) > 0 for status in ("bleed", "poison"))
        skill = {**skill, "multiplier": config["base_multiplier"] + status_count * config["multiplier_bonus_per_status"]}

    # 3. 按技能種類執行
    if skill["kind"] == "damage":
        return player_attack(state, enemy, enemy.get("current_hp", enemy.get("hp", 100)), skill, player_buffs, enemy_buffs)

    elif skill["kind"] == "heal":
        before = state["current_hp"]
        amount = skill["amount"] + math.floor(stats["magic_attack"] * skill.get("multiplier", 0))
        amount = math.ceil(amount * (1 + active_relic_passive_effects(state).get("healing_regen_percent", 0) / 100))
        state["current_hp"] = min(stats["max_hp"], state["current_hp"] + amount)
        healed = state["current_hp"] - before
        line = f"你使用{skill['name']}，回復 {healed} HP。"
        return CombatActionResult(events=[line], summary=[line])

    elif skill["kind"] == "buff":
        buff_key = skill["buff"]
        if buff_key in {"blood_blade_active", "blood_armor_active"}:
            max_stk = 3
            if buff_key == "blood_armor_active":
                max_stk = 4 if "skill_blood_armor_passive" in state.get("learned_skills", []) else 3
            player_buffs[buff_key] = min(max_stk, player_buffs.get(buff_key, 0) + 1)
            line = f"你使用{skill['name']}。目前【{status_display_name(buff_key)}】堆疊至 {player_buffs[buff_key]}/{max_stk} 層。"
        elif buff_key == "holy_veil_shield":
            shield_base = 40
            shield_mult = 1.5
            from data import PROMOTIONS
            promo = PROMOTIONS.get("promotion_holy_veil", {})
            cfg = promo.get("config", {})
            if cfg:
                shield_base = cfg.get("shield_base", 40)
                shield_mult = cfg.get("shield_multiplier", 1.5)
            shield_cap = stats["magic_attack"] * shield_mult + shield_base
            if "skill_holy_veil_passive" in state.get("learned_skills", []):
                shield_cap *= (1.0 + cfg.get("passive_capacity_bonus_percent", 25) / 100.0)
            shield_cap = int(shield_cap)
            player_buffs["holy_veil_shield"] = 99
            player_buffs["_holy_veil_shield_value"] = shield_cap
            line = f"你使用{skill['name']}。建立容量 {shield_cap} 的聖幕護盾。"
        elif buff_key == "holy_eclipse_active":
            from data import PROMOTIONS
            promo = PROMOTIONS.get("promotion_holy_eclipse", {})
            cfg = promo.get("config", {})
            dur = cfg.get("duration", 5)
            regen_amt = cfg.get("regen_amount", 6)
            regen_mult = cfg.get("regen_multiplier", 0.45)
            dot_mult = cfg.get("dot_multiplier", 0.6)
            vial_id = "item_sanctified_ash_vial"
            if not remove_item(state, vial_id):
                return CombatActionResult(events=["缺少聖蝕聖瓶，無法施展聖蝕祈禱。"], summary=["缺少聖蝕聖瓶。"], outcome="cancel")

            player_buffs["regeneration"] = dur
            player_buffs["_regen_data"] = {"amount": regen_amt, "multiplier": regen_mult}
            apply_dot(enemy_buffs, "聖蝕", dur, dot_mult, "magic", "無")
            player_buffs["_holy_eclipse_vial_marked"] = True
            line = f"你使用{skill['name']}。自身進入再生狀態，且對敵人施加聖蝕持續魔法傷害，持續 {dur} 回合。"
        else:
            player_buffs[buff_key] = skill["duration"]
            if skill.get("buff_stats"):
                player_buffs.setdefault("_buff_stat_data", {})[buff_key] = dict(skill["buff_stats"])
            line = f"你使用{skill['name']}。{skill['desc']}"
        return CombatActionResult(events=[line], summary=[line])

    elif skill["kind"] == "debuff":
        debuff_key = skill["debuff"]
        if debuff_key == "sigil_mage_mark":
            elem = skill.get("element", "物理")
            enemy_buffs["sigil_mage_mark"] = skill["duration"]
            enemy_buffs["_sigil_element"] = elem
            line = f"你使用{skill['name']}。施加【{elem}】之印記，持續 {skill['duration']} 回合。"
        else:
            enemy_buffs[debuff_key] = skill["duration"]
            if skill.get("damage_percent") is not None:
                enemy_buffs.setdefault("_debuff_data", {})[debuff_key] = {
                    "damage_percent": skill["damage_percent"],
                    "damage_scope": skill.get("damage_scope"),
                }
            line = f"你使用{skill['name']}。{skill['desc']}"
        return CombatActionResult(events=[line], summary=[line])

    elif skill["kind"] == "dot":
        apply_dot(enemy_buffs, skill["name"], skill["duration"], skill["multiplier"], "magic", skill.get("element", "無"))
        line = f"{skill['name']} 必定附加，持續 {skill['duration']} 回合。"
        return CombatActionResult(events=[line], summary=[line])

    elif skill["kind"] == "regen":
        player_buffs["regeneration"] = skill["duration"]
        player_buffs["_regen_data"] = {"amount": skill["amount"], "multiplier": skill["multiplier"]}
        line = f"{skill['name']} 必定附加，持續 {skill['duration']} 回合。"
        return CombatActionResult(events=[line], summary=[line])

    return CombatActionResult()


def skill_menu(state: dict, enemy: dict, player_buffs: dict, enemy_buffs: dict):
    skills = [skill_id for skill_id in state["learned_skills"] if SKILLS[skill_id].get("kind") != "passive"]
    if not skills:
        return CombatActionResult(events=["沒有可施放的主動技能。"], summary=["沒有可施放的主動技能。"], outcome="cancel")
    options = []
    for skill_id in skills:
        skill = SKILLS[skill_id]
        options.append(f"{skill['name']} / MP {skill['mp']} / {skill['desc']}")
    stats = get_stats(state, player_buffs)
    choice = action_menu_panel(
        "選擇技能",
        options,
        "技能選擇",
        header_lines=[
            f"目前 MP {state['current_mp']}/{stats['max_mp']}",
            f"目標：{enemy['name']} / 屬性 {enemy['element']} / 狀態 {buff_summary(enemy_buffs)}",
        ],
        hint_lines=["返回不消耗本回合。"],
        border_style="magenta",
    )
    if choice == 0:
        return CombatActionResult(outcome="cancel")
    skill_id = skills[choice - 1]
    skill = SKILLS[skill_id]
    if state["current_mp"] < skill["mp"]:
        return CombatActionResult(events=["MP 不足。"], summary=["MP 不足。"], outcome="cancel")

    # 執行技能
    res = execute_skill(state, enemy, skill_id, skill, player_buffs, enemy_buffs)
    if res.outcome == "cancel":
        return res
    state["current_mp"] -= skill["mp"]
    return res

def combat_item_menu(state: dict, boss: bool, enemy_buffs: dict, enemy: dict, mp_item_used: bool = False):
    usable_ids = [
        item_id
        for item_id in COMBAT_ITEM_IDS
        if combat_item_quantity(state, item_id) > 0
    ]
    if not usable_ids:
        return CombatActionResult(events=["沒有可用道具。"], summary=["沒有可用道具。"], outcome="cancel")
    options = [f"{item_name(item_id)} x{combat_item_quantity(state, item_id)} / {ITEMS[item_id]['desc']}" for item_id in usable_ids]
    choice = action_menu_panel(
        "選擇道具",
        options,
        "道具選擇",
        header_lines=[f"目標：{enemy['name']} / 狀態 {buff_summary(enemy_buffs)}"],
        hint_lines=["返回不消耗本回合。"],
        border_style="green",
    )
    if choice == 0:
        return CombatActionResult(outcome="cancel")
    item_id = usable_ids[choice - 1]
    if item_id in COMBAT_MP_RECOVERY and mp_item_used:
        return CombatActionResult(events=["本回合已使用 MP 藥水。"], summary=["本回合已使用 MP 藥水。"], outcome="cancel")
    if item_id in COMBAT_HP_RECOVERY:
        stats = get_stats(state)
        before = state["current_hp"]
        state["current_hp"] = min(stats["max_hp"], state["current_hp"] + combat_recovery_amount(state, item_id))
        consume_combat_item(state, item_id)
        line = f"使用{item_name(item_id)}，回復 {state['current_hp'] - before} HP。"
        return CombatActionResult(events=[line], summary=[line])
    elif item_id in COMBAT_MP_RECOVERY:
        stats = get_stats(state)
        before = state["current_mp"]
        state["current_mp"] = min(stats["max_mp"], state["current_mp"] + combat_recovery_amount(state, item_id))
        consume_combat_item(state, item_id)
        line = f"使用{item_name(item_id)}，回復 {state['current_mp'] - before} MP。"
        return CombatActionResult(events=[line], summary=[line], free_action=True)
    elif item_id == "item_herb_antidote":
        consume_combat_item(state, item_id)
        state.setdefault("_clear_burn", True)
        line = "你嚼下解毒草，灼熱感稍微退去。"
        return CombatActionResult(events=[line], summary=[line])
    elif item_id in COMBAT_THROWABLE_IDS:
        return use_combat_throwable(state, item_id, enemy, enemy_buffs)
    elif item_id == "item_escape_scroll":
        if boss:
            return CombatActionResult(events=["Boss 戰中無法使用逃脫卷軸。"], summary=["Boss 戰中無法使用逃脫卷軸。"], outcome="cancel")
        consume_combat_item(state, item_id)
        return CombatActionResult(events=["卷軸化成白光，你撤回迷宮入口。"], summary=["卷軸化成白光，你撤回迷宮入口。"], outcome="escaped")
    return CombatActionResult()

def try_escape(state: dict, enemy: dict) -> bool:
    stats = get_stats(state)
    chance = 45 + (stats["agility"] - enemy["agility"]) * 3
    chance = max(25, min(85, chance))
    return random.randint(1, 100) <= chance

def monster_action(enemy_id: str, enemy: dict, state: dict, player_buffs: dict, defending: bool) -> list[str]:
    if enemy_id == "mon_lava_imp" and random.random() < 0.35:
        damage = calc_enemy_damage(enemy, state, 1.1, "火", player_buffs, defending)
        state["current_hp"] -= damage
        events = [f"{enemy['name']}丟出小火球，造成 {damage} 火傷害。"]
        if random.random() < 0.2:
            player_buffs["burn"] = 3
            events.append("你陷入灼傷。")
        return events
    if enemy_id == "mon_scorched_guard" and random.random() < 0.3:
        damage = calc_enemy_damage(enemy, state, 1.0, "物理", player_buffs, defending)
        state["current_hp"] -= damage
        player_buffs["defense_down"] = 2
        return [f"{enemy['name']}使用破甲斬，造成 {damage} 傷害，你的防禦下降。"]
    element = "火" if enemy_id == "mon_cinder_bat" else "物理"
    damage = calc_enemy_damage(enemy, state, 1.0, element, player_buffs, defending)
    state["current_hp"] -= damage
    return [f"{enemy['name']}攻擊，造成 {damage} 傷害。"]

def boss_glen_action(
    enemy: dict,
    enemy_hp: int,
    state: dict,
    player_buffs: dict,
    enemy_buffs: dict,
    defending: bool,
    turn: int,
    summoned: bool,
) -> tuple[bool, list[str]]:
    if not summoned and enemy_hp <= enemy["hp"] * 0.6:
        enemy_buffs["defense_up"] = 3
        return True, ["葛倫吹響口哨，山寨手下在遠處吶喊。他的防禦上升。"]
    if enemy_hp <= enemy["hp"] * 0.35:
        damage = calc_enemy_damage(enemy, state, 1.35, "物理", player_buffs, defending)
        state["current_hp"] -= damage
        player_buffs["defense_down"] = 2
        return summoned, [f"葛倫使出破甲重擊，造成 {damage} 傷害，你的防禦下降。"]
    if turn % 3 == 0:
        damage = calc_enemy_damage(enemy, state, 1.15, "火", player_buffs, defending)
        state["current_hp"] -= damage
        events = [f"葛倫砸出火油瓶，造成 {damage} 火傷害。"]
        if random.random() < 0.25:
            player_buffs["burn"] = 3
            events.append("你陷入灼傷。")
        return summoned, events
    damage = calc_enemy_damage(enemy, state, 1.0, "物理", player_buffs, defending)
    state["current_hp"] -= damage
    return summoned, [f"葛倫粗暴斬擊，造成 {damage} 傷害。"]

def boss_ash_guardian_action(
    enemy: dict,
    enemy_hp: int,
    state: dict,
    player_buffs: dict,
    enemy_buffs: dict,
    defending: bool,
    turn: int,
    charged: bool,
) -> tuple[bool, list[str]]:
    if charged:
        damage = calc_enemy_damage(enemy, state, 1.35, "火", player_buffs, defending)
        state["current_hp"] -= damage
        events = [f"{enemy['name']}釋放爐心蓄熱，熔火爆裂造成 {damage} 火傷害。"]
        if random.random() < 0.2:
            player_buffs["burn"] = 3
            events.append("你陷入灼傷。")
        return False, events
    if enemy_hp <= enemy["hp"] * 0.45 and turn % 3 == 1:
        return True, [f"{enemy['name']}胸口的爐心開始發亮，下一擊會很危險。"]
    if turn % 4 == 0:
        enemy_buffs["defense_up"] = 2
        return charged, [f"{enemy['name']}收攏灰燼甲片，防禦上升。"]
    if turn % 2 == 0:
        damage = calc_enemy_damage(enemy, state, 1.1, "火", player_buffs, defending)
        state["current_hp"] -= damage
        return charged, [f"{enemy['name']}揮出火舌掃擊，造成 {damage} 火傷害。"]
    damage = calc_enemy_damage(enemy, state, 1.0, "物理", player_buffs, defending)
    state["current_hp"] -= damage
    return charged, [f"{enemy['name']}以沉重石臂砸下，造成 {damage} 傷害。"]

def boss_cinder_seal_sentinel_action(
    enemy: dict,
    enemy_hp: int,
    state: dict,
    player_buffs: dict,
    enemy_buffs: dict,
    defending: bool,
    turn: int,
    charged: bool,
) -> tuple[bool, list[str]]:
    if charged:
        damage = calc_enemy_damage(enemy, state, 1.4, "火", player_buffs, defending)
        state["current_hp"] -= damage
        events = [f"{enemy['name']}將燼印壓入地面，赤焰衝擊造成 {damage} 火傷害。"]
        if random.random() < 0.25:
            player_buffs["burn"] = 3
            events.append("你陷入灼傷。")
        return False, events
    if enemy_hp <= enemy["hp"] * 0.5 and turn % 3 == 1:
        return True, [f"{enemy['name']}胸口的燼印亮起，下一擊正在蓄勢。"]
    if turn % 4 == 0:
        enemy_buffs["defense_up"] = 2
        return charged, [f"{enemy['name']}收束熔殼，防禦上升。"]
    if turn % 2 == 0:
        damage = calc_enemy_damage(enemy, state, 1.05, "物理", player_buffs, defending)
        state["current_hp"] -= damage
        player_buffs["defense_down"] = 2
        return charged, [f"{enemy['name']}以刻印長槍貫擊，造成 {damage} 傷害，你的防禦下降。"]
    damage = calc_enemy_damage(enemy, state, 1.1, "火", player_buffs, defending)
    state["current_hp"] -= damage
    return charged, [f"{enemy['name']}揮出燼火斬，造成 {damage} 火傷害。"]

def dispatch_enemy_turn(
    enemy_id: str,
    enemy: dict,
    enemy_hp: int,
    state: dict,
    player_buffs: dict,
    enemy_buffs: dict,
    defending: bool,
    turn: int,
    boss_marker: bool,
) -> tuple[bool, list[str]]:
    race_events = prepare_monster_race_enemy_turn(enemy, enemy_hp, enemy_buffs)
    if enemy_id == "boss_glen":
        boss_marker, events = boss_glen_action(
            enemy,
            enemy_hp,
            state,
            player_buffs,
            enemy_buffs,
            defending,
            turn,
            boss_marker,
        )
    elif enemy_id == "boss_ash_guardian":
        boss_marker, events = boss_ash_guardian_action(
            enemy,
            enemy_hp,
            state,
            player_buffs,
            enemy_buffs,
            defending,
            turn,
            boss_marker,
        )
    elif enemy_id == "boss_cinder_seal_sentinel":
        boss_marker, events = boss_cinder_seal_sentinel_action(
            enemy,
            enemy_hp,
            state,
            player_buffs,
            enemy_buffs,
            defending,
            turn,
            boss_marker,
        )
    else:
        events = monster_action(enemy_id, enemy, state, player_buffs, defending)
    return boss_marker, [*race_events, *events]

def tick_effects(state: dict, player_buffs: dict, enemy_buffs: dict, enemy: dict | None = None):
    events = []
    enemy_dot_damage = 0
    if state.pop("_clear_burn", False):
        player_buffs.pop("burn", None)
    if player_buffs.get("burn", 0) > 0:
        damage = max(1, math.ceil(get_stats(state)["max_hp"] * 0.05))
        state["current_hp"] -= damage
        events.append(f"灼傷造成 {damage} 傷害。")
    if player_buffs.get("regeneration", 0) > 0:
        regen = player_buffs.get("_regen_data", {})
        stats = get_stats(state)
        amount = regen.get("amount", 0) + math.floor(stats["magic_attack"] * regen.get("multiplier", 0))
        amount = math.ceil(amount * (1 + active_relic_passive_effects(state).get("healing_regen_percent", 0) / 100))
        if state.get("job") == "聖印使":
            amount = math.ceil(amount * 1.20)
        healed = min(amount, stats["max_hp"] - state["current_hp"])

        state["current_hp"] += max(0, healed)
        events.append(f"再生回復 {max(0, healed)} HP。")
    if enemy is not None:
        for status, dot in list(enemy_buffs.get("_dot_data", {}).items()):
            if enemy_buffs.get(status, 0) <= 0:
                continue
            if "fixed_power" in dot:
                damage = dot["fixed_power"]
            else:
                stats = get_stats(state)
                power = stats["magic_attack"] if dot["damage_type"] == "magic" else stats["attack"]
                if dot["damage_type"] == "physical":
                    race_multiplier = physical_status_damage_multiplier(enemy, status)
                    damage = (
                        calc_physical_status_damage(power, dot["multiplier"] * race_multiplier)
                        if race_multiplier > 0
                        else 0
                    )
                else:
                    damage, _ = calc_typed_damage(
                        power, dot["multiplier"], enemy, enemy_buffs, dot["damage_type"], dot["element"],
                    )
            if "fixed_power" not in dot:
                damage = math.ceil(damage * (1 + active_relic_passive_effects(state).get("dot_damage_percent", 0) / 100))

            # 聖蝕司祭被動：再生與聖蝕並存時傷害提升 30%
            if status == "聖蝕" and player_buffs.get("regeneration", 0) > 0 and "skill_holy_eclipse_passive" in state.get("learned_skills", []):
                from data import PROMOTIONS
                promo = PROMOTIONS.get("promotion_holy_eclipse", {})
                cfg = promo.get("config", {})
                damage = math.ceil(damage * (1.0 + cfg.get("passive_dot_boost_percent", cfg.get("passive_dot_damage_bonus_percent", 30)) / 100.0))

            enemy_dot_damage += damage
            events.append(f"{status_display_name(status)}造成 {damage} 傷害。")
    for buffs in (player_buffs, enemy_buffs):
        expired = []
        for key in list(buffs.keys()):
            if key.startswith("_"):
                continue
            buffs[key] -= 1
            if buffs[key] <= 0:
                expired.append(key)
        for key in expired:
            del buffs[key]
            if buffs is enemy_buffs:
                buffs.get("_dot_data", {}).pop(key, None)
                buffs.get("_debuff_data", {}).pop(key, None)
                if key == "sigil_mage_mark":
                    buffs.pop("_sigil_element", None)
            if buffs is player_buffs and key == "regeneration":
                buffs.pop("_regen_data", None)
            if buffs is player_buffs:
                buffs.get("_buff_stat_data", {}).pop(key, None)
    return (events, enemy_dot_damage) if enemy is not None else events

CLI_REGION_ORDER = ["border_fire", "ice", "earth", "thunder", "final"]
CLI_REGION_ROUTE_ENABLED = {"border_fire", "ice", "earth", "thunder", "final"}


def cli_region_label(region_id: str) -> str:
    region = REGIONS.get(region_id, {})
    return region.get("name") or region.get("town_name") or region_id


def cli_region_route_enabled(state: dict, region_id: str) -> bool:
    return region_id in CLI_REGION_ROUTE_ENABLED and region_id in get_unlocked_regions(state)


def cli_region_locked_reason(region_id: str) -> str:
    return get_region_locked_reason(region_id)


def region_travel_menu(state: dict, current_region_id: str) -> str:
    options = []
    for region_id in CLI_REGION_ORDER:
        status = "current" if region_id == current_region_id else ("open" if cli_region_route_enabled(state, region_id) else "locked")
        options.append(f"{cli_region_label(region_id)} / {status}")
    choice = action_menu_panel(
        "Travel to new region",
        options,
        "Region Gate",
        header_lines=["Travel through the region gate to other unlocked regions."],
        allow_back=True,
        border_style="blue",
    )
    if choice == 0:
        return current_region_id
    region_id = CLI_REGION_ORDER[choice - 1]
    if not cli_region_route_enabled(state, region_id):
        print(cli_region_locked_reason(region_id))
        pause()
        return current_region_id
    print(f"Traveling to {cli_region_label(region_id)}.")
    if region_id != current_region_id:
        show_story_beat(take_story_beat(state, region_story_beat_id(region_id)))
    pause()
    return region_id


def main_loop(state: dict) -> str | None:
    current_region_id = state.get("flags", {}).get("current_region_id") or "border_fire"
    while True:
        clamp_vitals(state)
        main_options = [
            "查看狀態",
            "返回城鎮整備",
            "進入迷宮探索",
            "怪物圖鑑",
            "背包/裝備",
            "存檔",
            "離開遊戲",
        ]
        main_options.insert(3, "前往新區域 / 前往新大陸")
        choice = main_menu_panel(
            "選擇行動",
            main_options,
            player_summary_line(state),
            allow_back=False,
            hint_lines=[next_step_hint(state)],
        )
        if choice == 1:
            show_status(state)
            pause()
        elif choice == 2:
            town_menu(state, current_region_id)
        elif choice == 3:
            dungeon_menu(state, current_region_id)
            if state.pop("_return_to_title", False):
                return "title"
        elif choice == 4:
            current_region_id = region_travel_menu(state, current_region_id)
            if "flags" not in state:
                state["flags"] = {}
            state["flags"]["current_region_id"] = current_region_id
        elif choice == 5:
            bestiary_menu(state)
        elif choice == 6:
            backpack_menu(state, allow_storage=False)
        elif choice == 7:
            save_game(state)
            pause()
        elif choice == 8:
            raw = input("離開前要存檔嗎？(y/n) > ").strip().lower()
            if raw == "y":
                save_game(state)
            print("下次再回艾爾姆。")
            return

def smoke_test() -> None:
    # Boss routes are intentionally gated to the v1 Rogue/Cleric quality path.
    quality_smoke_job = "盜賊"
    state = create_state("測試者", "劍士")
    assert state["inventory"].get("item_potion_s") == 2
    assert state["equipment"].get("special") == "special_trial_badge"
    assert "special_trial_badge" not in state["inventory"]
    assert state["current_hp"] == 120
    assert state["storage_unlocked"] is False
    assert state["storage"] == {}
    assert state["bestiary"] == []
    assert get_region_by_dungeon("dungeon_ice_minor_a") == "ice"
    assert get_region_by_quest("quest_final_demon_king") == "final"
    assert get_unlocked_regions(state) == ["border_fire"]
    assert get_npc_display_name("ice", "innkeeper")
    assert get_facility_display_name("final", "guild")
    assert get_facility_short_description("thunder", "shop")
    # Dialogue helper checks
    assert get_dialogue("ice", "guild", "welcome") == "「霜潮港隨時需要人手，看看今天的委託吧。」"
    # Fallback to border_fire check
    assert get_dialogue("invalid_region", "guild", "welcome") == "「歡迎回來。想挑戰新目標，還是要交付已完成的委託？」"
    assert "dungeon_moss_cave" in player_facing_dungeon_ids(state)
    assert "dungeon_moss_cave" in player_facing_dungeon_ids(state, "border_fire")
    assert "dungeon_ice_minor_a" not in player_facing_dungeon_ids(state, "border_fire")
    legacy_state = {"inventory": {}}
    ensure_state_defaults(legacy_state)
    assert legacy_state["flags"] == {}
    assert legacy_state["storage_unlocked"] is False
    assert legacy_state["storage"] == {}
    assert legacy_state["bestiary"] == []
    glen_state = create_state("格倫規則測試", quality_smoke_job)
    glen_state["completed_quests"].append("quest_mine_scout")
    assert not quest_unlocked(glen_state, "quest_boss_glen")
    assert not boss_available_at_dungeon_end(glen_state, "dungeon_scorched_mine", "boss_glen")
    assert record_boss_glen_sighting(glen_state)
    assert not record_boss_glen_sighting(glen_state)
    assert can_accept_boss_glen_investigation(glen_state)
    assert accept_boss_glen_investigation(glen_state)
    assert not accept_boss_glen_investigation(glen_state)
    assert quest_unlocked(glen_state, "quest_boss_glen")
    assert boss_available_at_dungeon_end(glen_state, "dungeon_scorched_mine", "boss_glen")
    legacy_glen_state = create_state("舊格倫進度測試", quality_smoke_job)
    legacy_glen_state["completed_quests"].append("quest_mine_scout")
    legacy_glen_state["flags"]["boss_glen_defeated"] = True
    assert quest_unlocked(legacy_glen_state, "quest_boss_glen")
    assert not can_accept_boss_glen_investigation(legacy_glen_state)
    assert not boss_available_at_dungeon_end(legacy_glen_state, "dungeon_scorched_mine", "boss_glen")
    ice_state = create_state("Ice route smoke", quality_smoke_job)
    ice_state["flags"]["cinder_seal_sentinel_defeated"] = True
    ice_state["flags"][FIRE_MARK_CHURCH_LOOKUP_FLAG] = True
    ice_state["inventory"][FIRE_MARK_SHARD_ID] = 3
    assert not is_unlocked(ice_state, ICE_REGION_UNLOCK)
    fire_relic_result = enshrine_relic(ice_state, "relic_fire_seal")
    assert fire_relic_result["changed"] is True
    assert ice_state["flags"]["fire_seal_enshrined"]
    assert ice_state["inventory"].get(FIRE_MARK_SHARD_ID, 0) == 0
    assert ice_state["inventory"].get("key_fire_seal", 0) == 1
    assert is_unlocked(ice_state, ICE_REGION_UNLOCK)
    assert "ice" in get_unlocked_regions(ice_state)
    assert quest_unlocked(ice_state, "quest_ice_minor_a")
    assert "dungeon_ice_minor_a" in player_facing_dungeon_ids(ice_state)
    assert "dungeon_ice_minor_a" in player_facing_dungeon_ids(ice_state, "ice")
    assert "dungeon_moss_cave" not in player_facing_dungeon_ids(ice_state, "ice")
    assert boss_available_at_dungeon_end(ice_state, "dungeon_ice_minor_a", "boss_ice_wreck_captain")
    ice_state["completed_quests"].append("quest_ice_minor_a")
    unlock(ice_state, "dungeon_ice_minor_b")
    assert quest_unlocked(ice_state, "quest_ice_minor_b")
    assert boss_available_at_dungeon_end(ice_state, "dungeon_ice_minor_b", "boss_ice_frostroot_keeper")
    ice_state["completed_quests"].append("quest_ice_minor_b")
    unlock(ice_state, "dungeon_ice_main_phase_1")
    assert quest_unlocked(ice_state, "quest_ice_main_phase_1")
    assert boss_available_at_dungeon_end(ice_state, "dungeon_ice_main_phase_1", "boss_ice_outer_gatewarden")
    ice_state["flags"]["ice_outer_gatewarden_defeated"] = True
    assert quest_ready(ice_state, "quest_ice_main_phase_1")
    ice_state["completed_quests"].append("quest_ice_main_phase_1")
    unlock(ice_state, "dungeon_ice_main_phase_2")
    assert "dungeon_ice_main_phase_1" not in player_facing_dungeon_ids(ice_state)
    assert "dungeon_ice_main_phase_2" in player_facing_dungeon_ids(ice_state)
    assert quest_unlocked(ice_state, "quest_ice_main_phase_2")
    assert boss_available_at_dungeon_end(ice_state, "dungeon_ice_main_phase_2", "boss_ice_final_seal_lord")
    ice_state["flags"]["ice_final_boss_defeated"] = True
    ice_state["flags"]["ice_relic_marker_resolved"] = True
    assert quest_ready(ice_state, "quest_ice_main_phase_2")
    ice_state["completed_quests"].append("quest_ice_main_phase_2")
    assert quest_unlocked(ice_state, "quest_ice_return_handoff")
    assert quest_ready(ice_state, "quest_ice_return_handoff")
    earth_state = create_state("Earth route smoke", quality_smoke_job)
    unlock(earth_state, EARTH_REGION_UNLOCK)
    assert quest_unlocked(earth_state, "quest_earth_minor_a")
    assert "dungeon_earth_minor_a" in player_facing_dungeon_ids(earth_state)
    assert boss_available_at_dungeon_end(earth_state, "dungeon_earth_minor_a", "boss_earth_rootwarden")
    earth_state["completed_quests"].append("quest_earth_minor_a")
    unlock(earth_state, "dungeon_earth_minor_b")
    assert quest_unlocked(earth_state, "quest_earth_minor_b")
    assert boss_available_at_dungeon_end(earth_state, "dungeon_earth_minor_b", "boss_earth_quarry_colossus")
    earth_state["completed_quests"].append("quest_earth_minor_b")
    unlock(earth_state, "dungeon_earth_main_phase_1")
    assert quest_unlocked(earth_state, "quest_earth_main_phase_1")
    assert boss_available_at_dungeon_end(earth_state, "dungeon_earth_main_phase_1", "boss_earth_outer_grovekeeper")
    earth_state["flags"]["earth_outer_grovekeeper_defeated"] = True
    assert quest_ready(earth_state, "quest_earth_main_phase_1")
    earth_state["completed_quests"].append("quest_earth_main_phase_1")
    unlock(earth_state, "dungeon_earth_main_phase_2")
    assert "dungeon_earth_main_phase_1" not in player_facing_dungeon_ids(earth_state)
    assert "dungeon_earth_main_phase_2" in player_facing_dungeon_ids(earth_state)
    assert quest_unlocked(earth_state, "quest_earth_main_phase_2")
    assert boss_available_at_dungeon_end(earth_state, "dungeon_earth_main_phase_2", "boss_earth_deep_leyline_lord")
    earth_state["flags"]["earth_final_boss_defeated"] = True
    earth_state["flags"]["earth_relic_marker_resolved"] = True
    assert quest_ready(earth_state, "quest_earth_main_phase_2")
    earth_state["completed_quests"].append("quest_earth_main_phase_2")
    assert quest_unlocked(earth_state, "quest_earth_return_handoff")
    assert quest_ready(earth_state, "quest_earth_return_handoff")
    thunder_state = create_state("Thunder route smoke", quality_smoke_job)
    unlock(thunder_state, THUNDER_REGION_UNLOCK)
    assert quest_unlocked(thunder_state, "quest_thunder_minor_a")
    assert "dungeon_thunder_minor_a" in player_facing_dungeon_ids(thunder_state)
    assert boss_available_at_dungeon_end(thunder_state, "dungeon_thunder_minor_a", "boss_thunder_plateau_beacon")
    thunder_state["completed_quests"].append("quest_thunder_minor_a")
    unlock(thunder_state, "dungeon_thunder_minor_b")
    assert quest_unlocked(thunder_state, "quest_thunder_minor_b")
    assert boss_available_at_dungeon_end(thunder_state, "dungeon_thunder_minor_b", "boss_thunder_channel_keeper")
    thunder_state["completed_quests"].append("quest_thunder_minor_b")
    unlock(thunder_state, "dungeon_thunder_main_phase_1")
    assert quest_unlocked(thunder_state, "quest_thunder_main_phase_1")
    assert boss_available_at_dungeon_end(thunder_state, "dungeon_thunder_main_phase_1", "boss_thunder_lower_array_warden")
    thunder_state["flags"]["thunder_lower_array_warden_defeated"] = True
    assert quest_ready(thunder_state, "quest_thunder_main_phase_1")
    thunder_state["completed_quests"].append("quest_thunder_main_phase_1")
    unlock(thunder_state, "dungeon_thunder_main_phase_2")
    assert "dungeon_thunder_main_phase_1" not in player_facing_dungeon_ids(thunder_state)
    assert "dungeon_thunder_main_phase_2" in player_facing_dungeon_ids(thunder_state)
    assert quest_unlocked(thunder_state, "quest_thunder_main_phase_2")
    assert boss_available_at_dungeon_end(thunder_state, "dungeon_thunder_main_phase_2", "boss_thunder_crown_storm_lord")
    thunder_state["flags"]["thunder_final_boss_defeated"] = True
    thunder_state["flags"]["thunder_relic_marker_resolved"] = True
    assert quest_ready(thunder_state, "quest_thunder_main_phase_2")
    thunder_state["completed_quests"].append("quest_thunder_main_phase_2")
    assert quest_unlocked(thunder_state, "quest_thunder_return_handoff")
    assert quest_ready(thunder_state, "quest_thunder_return_handoff")
    for key in QUESTS["quest_thunder_return_handoff"]["unlocks"]:
        unlock(thunder_state, key)
    assert not is_unlocked(thunder_state, FINAL_REGION_UNLOCK)
    final_gate_state = create_state("Final gate smoke", quality_smoke_job)
    final_gate_state["flags"]["fire_seal_enshrined"] = True
    final_gate_state["flags"]["ice_seal_enshrined"] = True
    final_gate_state["flags"]["earth_seal_enshrined"] = True
    final_gate_state["flags"]["thunder_relic_marker_resolved"] = True
    final_gate_state["inventory"]["key_thunder_relic_marker_source"] = 1
    assert not is_unlocked(final_gate_state, FINAL_REGION_UNLOCK)
    thunder_relic_result = enshrine_relic(final_gate_state, "relic_thunder_marker_source")
    assert thunder_relic_result["changed"] is True
    assert final_gate_state["flags"]["thunder_seal_enshrined"]
    assert final_gate_state["inventory"].get("key_thunder_seal", 0) == 1
    assert is_unlocked(final_gate_state, FINAL_REGION_UNLOCK)
    final_state = create_state("Final route smoke", quality_smoke_job)
    unlock(final_state, FINAL_REGION_UNLOCK)
    assert quest_unlocked(final_state, "quest_final_minor_a")
    assert "dungeon_final_minor_a" in player_facing_dungeon_ids(final_state)
    assert boss_available_at_dungeon_end(final_state, "dungeon_final_minor_a", "boss_final_echo_vanguard")
    final_state["completed_quests"].append("quest_final_minor_a")
    unlock(final_state, "dungeon_final_minor_b")
    assert quest_unlocked(final_state, "quest_final_minor_b")
    assert boss_available_at_dungeon_end(final_state, "dungeon_final_minor_b", "boss_final_ruin_jailer")
    final_state["completed_quests"].append("quest_final_minor_b")
    unlock(final_state, "dungeon_final_main_phase_1")
    assert quest_unlocked(final_state, "quest_final_main_phase_1")
    assert boss_available_at_dungeon_end(final_state, "dungeon_final_main_phase_1", "boss_final_echo_warden")
    final_state["flags"]["final_echo_warden_defeated"] = True
    assert quest_ready(final_state, "quest_final_main_phase_1")
    final_state["completed_quests"].append("quest_final_main_phase_1")
    unlock(final_state, FINAL_PHASE_2_DUNGEON_ID)
    assert "dungeon_final_main_phase_1" not in player_facing_dungeon_ids(final_state)
    assert "dungeon_final_main_phase_2" in player_facing_dungeon_ids(final_state)
    assert quest_unlocked(final_state, "quest_final_main_phase_2")
    assert boss_available_at_dungeon_end(final_state, "dungeon_final_main_phase_2", "boss_final_seal_core")
    final_state["flags"]["final_seal_core_defeated"] = True
    assert quest_ready(final_state, "quest_final_main_phase_2")
    final_state["completed_quests"].append("quest_final_main_phase_2")
    unlock(final_state, FINAL_PHASE_3_DUNGEON_ID)
    assert "dungeon_final_main_phase_1" not in player_facing_dungeon_ids(final_state)
    assert "dungeon_final_main_phase_2" not in player_facing_dungeon_ids(final_state)
    assert "dungeon_final_main_phase_3" in player_facing_dungeon_ids(final_state)
    assert quest_unlocked(final_state, FINAL_QUEST_ID)
    assert not quest_ready(final_state, FINAL_QUEST_ID)
    assert boss_available_at_dungeon_end(final_state, "dungeon_final_main_phase_3", "boss_final_demon_king")
    clear_dungeon_boss(final_state, "boss_final_demon_king", {"gold": 0, "items": {}})
    assert final_state["flags"]["final_demon_king_defeated"]
    assert final_state["flags"][MAIN_STORY_CLEARED_FLAG]
    assert FINAL_QUEST_ID in final_state["completed_quests"]
    assert final_state.pop("_ending_pending", False)
    assert try_register_bestiary(state, "mon_moss_rat")
    assert state["bestiary"] == ["mon_moss_rat"]
    assert not try_register_bestiary(state, "mon_moss_rat")
    state["bestiary"] = []
    add_item(state, "mat_moss_fiber", 3)
    add_item(state, "mat_cracked_stone", 2)
    state["storage_unlocked"] = True
    assert storage_has_room_for(state, "mat_moss_fiber")
    remove_item(state, "mat_moss_fiber", 1)
    add_storage_item(state, "mat_moss_fiber", 1)
    assert state["inventory"]["mat_moss_fiber"] == 2
    assert state["storage"]["mat_moss_fiber"] == 1
    remove_storage_item(state, "mat_moss_fiber", 1)
    add_item(state, "mat_moss_fiber", 1)
    assert "mat_moss_fiber" not in state["storage"]
    assert state["inventory"]["mat_moss_fiber"] == 3
    assert quest_ready(state, "quest_cave_gathering")
    state["completed_quests"].append("quest_cave_gathering")
    unlock(state, "shop_synthesis_01")
    unlock(state, "dungeon_scorched_mine")
    add_item(state, "weapon_iron_sword", 1)
    add_item(state, "mat_cracked_stone", 5)
    add_item(state, "mat_scorched_iron", 1)
    state["gold"] = 999
    craft_recipe(state, "recipe_iron_sword_plus_1")
    assert equipment_ref_count(state, "weapon_iron_sword_plus_1") == 1
    damage, _ = calc_player_damage(state, MONSTERS["mon_moss_rat"], None, {}, {})
    assert damage > 0

    # 測試漸進式 CLI 路由與區域正規化
    cli_state = create_state("CLI Route Test", "劍士")
    assert cli_region_route_enabled(cli_state, "border_fire")
    assert not cli_region_route_enabled(cli_state, "ice")
    assert not cli_region_route_enabled(cli_state, "earth")
    assert check_and_normalize_region(cli_state, "earth") == "border_fire"
    assert check_and_normalize_region(cli_state, "thunder") == "border_fire"
    assert check_and_normalize_region(cli_state, "final") == "border_fire"

    unlock(cli_state, "unlock_ice_region")
    assert cli_region_route_enabled(cli_state, "ice")
    assert not cli_region_route_enabled(cli_state, "earth")
    assert check_and_normalize_region(cli_state, "ice") == "ice"
    assert check_and_normalize_region(cli_state, "earth") == "border_fire"

    unlock(cli_state, "unlock_earth_region_preview")
    assert cli_region_route_enabled(cli_state, "earth")
    assert check_and_normalize_region(cli_state, "earth") == "earth"
    assert check_and_normalize_region(cli_state, "thunder") == "border_fire"

    unlock(cli_state, "unlock_thunder_region_preview")
    assert cli_region_route_enabled(cli_state, "thunder")
    assert check_and_normalize_region(cli_state, "thunder") == "thunder"
    assert check_and_normalize_region(cli_state, "final") == "border_fire"

    unlock(cli_state, "unlock_final_region_preview")
    assert cli_region_route_enabled(cli_state, "final")
    assert check_and_normalize_region(cli_state, "final") == "final"

    print("smoke test ok")

def main() -> None:
    setup_console()
    if "--smoke-test" in sys.argv:
        smoke_test()
        return

    while True:
        state = None
        has_save = SAVE_PATH.exists()
        choice = start_screen_panel(has_save)
        if has_save and choice == 2:
            state = load_game()
        if state is None:
            state = new_game()
        if main_loop(state) != "title":
            return
