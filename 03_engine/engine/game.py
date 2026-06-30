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
from .formatting import equipment_summary, format_items, item_name, monster_drop_names
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
)
from .relic import (
    relic_enshrined,
    relic_ready_to_enshrine,
    relic_source_count,
    relic_source_required,
    relic_disabled_reason,
    preview_relic_entries,
    enshrine_relic,
    relic_preview_menu,
    ready_relic_names,
)
from data import (
    DUNGEONS,
    EQUIPMENT,
    EVENT_WEIGHTS,
    ITEMS,
    JOBS,
    MAGIC_BOOKS,
    MONSTERS,
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



SLEEVE_BLADE_FOLLOWUP_MULTIPLIER = 0.35
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





def buff_summary(buffs: dict) -> str:
    labels = {
        "burn": "灼傷",
        "defense_up": "防禦上升",
        "defense_down": "防禦下降",
        "quickstep": "迅步",
        "cinder_mark": "燼印",
    }
    active = [f"{labels.get(key, key)} {turns}" for key, turns in buffs.items() if turns > 0]
    return "、".join(active) if active else "無"

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
        f"{enemy['name']} HP {enemy_hp}/{enemy['hp']} / 屬性 {enemy['element']} / 狀態 {buff_summary(enemy_buffs)}",
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

def gain_exp(state: dict, amount: int) -> None:
    print(f"獲得經驗 {amount}。")
    state["exp"] += amount
    while state["exp"] >= exp_to_next(state["level"]):
        state["exp"] -= exp_to_next(state["level"])
        state["level"] += 1
        stats = get_stats(state)
        state["current_hp"] = stats["max_hp"]
        state["current_mp"] = stats["max_mp"]
        print(f"等級提升！現在是 Lv{state['level']}，HP/MP 已回滿。")





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
    print(f"\n諾亞替你別上見習徽章：「歡迎來到艾爾姆，{name}。今天開始，你就是{job}了。」")
    return state

def show_status(state: dict) -> None:
    clamp_vitals(state)
    render_panel("角色狀態", player_resource_lines(state), border_style="cyan")

    slot_names = {"weapon": "武器", "head": "頭部", "body": "身體", "accessory": "飾品", "special": "特殊"}
    equipment_lines = []
    for slot, label in slot_names.items():
        item_id = state["equipment"].get(slot)
        equipment_lines.append(f"{label}: {item_name(item_id) if item_id else '無'}")
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
        lines.append(f"{item_name(item_id)} x{qty} / {item_usage_summary(item_id)}")
    render_panel("背包與素材", lines, border_style="green")

def item_usage_summary(item_id: str) -> str:
    data = ITEMS.get(item_id) or EQUIPMENT.get(item_id)
    desc = data.get("desc", "") if data else ""
    usage = []
    if item_id in EQUIPMENT:
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
        equippables = [item_id for item_id in state["inventory"] if item_id in EQUIPMENT]
        slot_names = {"weapon": "武器", "head": "頭部", "body": "身體", "accessory": "飾品", "special": "特殊"}
        current_lines = [
            f"{slot_names.get(slot, slot)}: {item_name(item_id) if item_id else '無'}"
            for slot, item_id in state["equipment"].items()
        ]
        render_panel("目前裝備", current_lines, border_style="green")
        if not equippables:
            print("\n背包裡沒有可裝備物品。")
            pause()
            return
        options = [f"{item_name(item_id)} - {equipment_summary(item_id)}" for item_id in equippables]
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
        equip_item(state, equippables[choice - 1])
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
def element_multiplier(attack_element: str, target_element: str, enemy_buffs: dict | None = None) -> float:
    multiplier = 1.0
    if attack_element == "冰" and target_element == "火":
        multiplier = 1.2
    elif attack_element == "火" and target_element == "自然":
        multiplier = 1.1
    elif attack_element == "火" and target_element == "火":
        multiplier = 0.75
    if enemy_buffs and enemy_buffs.get("cinder_mark", 0) > 0 and attack_element == "火":
        multiplier *= 1.15
    return multiplier

def hit_roll(attacker_accuracy: int, target_agility: int, skill_bonus: int = 0) -> bool:
    return True

def calc_player_damage(state: dict, enemy: dict, skill: dict | None, player_buffs: dict, enemy_buffs: dict) -> tuple[int, bool]:
    stats = get_stats(state, player_buffs)
    if skill and skill.get("stat") == "magic":
        power = stats["attack"] + stats["magic_attack"]
    else:
        power = stats["attack"]
    multiplier = skill.get("multiplier", 1.0) if skill else 1.0
    enemy_defense = enemy["defense"]
    if enemy_buffs.get("defense_up", 0) > 0:
        enemy_defense = math.ceil(enemy_defense * 1.15)
    if enemy_buffs.get("defense_down", 0) > 0:
        enemy_defense = max(1, math.floor(enemy_defense * 0.8))
    base = max(1, power * multiplier - enemy_defense * 0.6)
    attack_element = skill.get("element", "物理") if skill else "物理"
    base *= element_multiplier(attack_element, enemy["element"], enemy_buffs)
    crit_chance = stats["crit"] + (skill.get("crit_bonus", 0) if skill else 0)
    is_crit = random.randint(1, 100) <= crit_chance
    if is_crit:
        base *= 1.5
    return max(1, math.ceil(base)), is_crit

def can_sleeve_blade_followup(state: dict, skill: dict | None) -> bool:
    return (
        skill is None
        and state["job"] == "盜賊"
        and state["equipment"].get("head") == "armor_rogue_sleeve_blade"
    )

def calc_sleeve_blade_followup_damage(state: dict, enemy: dict, player_buffs: dict, enemy_buffs: dict) -> int:
    stats = get_stats(state, player_buffs)
    enemy_defense = enemy["defense"]
    if enemy_buffs.get("defense_up", 0) > 0:
        enemy_defense = math.ceil(enemy_defense * 1.15)
    if enemy_buffs.get("defense_down", 0) > 0:
        enemy_defense = max(1, math.floor(enemy_defense * 0.8))
    base = max(1, stats["attack"] * SLEEVE_BLADE_FOLLOWUP_MULTIPLIER - enemy_defense * 0.6)
    return max(1, math.ceil(base))

def calc_enemy_damage(enemy: dict, state: dict, multiplier: float, element: str, player_buffs: dict, defending: bool) -> int:
    stats = get_stats(state, player_buffs)
    base = max(1, enemy["attack"] * multiplier - stats["defense"] * 0.6)
    if element == "火":
        base *= 1 - stats["fire_resist"] / 100
    if defending:
        base *= 0.6
    return max(1, math.ceil(base))

def combat(state: dict, enemy_id: str, boss: bool = False, run_log: dict | None = None):
    enemy = deepcopy(MONSTERS[enemy_id])
    enemy_hp = enemy["hp"]
    player_buffs = {}
    enemy_buffs = {}
    turn = 1
    boss_marker = False
    last_action_summary = "尚未行動。"
    battle_log = [f"遭遇 {enemy['name']}。敵人屬性：{enemy['element']} / HP {enemy_hp}/{enemy['hp']}。"]
    render_panel(
        f"遭遇 {enemy['name']}",
        [
            f"敵人屬性：{enemy['element']} / HP {enemy_hp}/{enemy['hp']}",
            "觀察敵我狀態後選擇攻擊、防禦、技能或道具。",
        ],
        border_style="red" if boss else "yellow",
    )
    while enemy_hp > 0 and state["current_hp"] > 0:
        clamp_vitals(state)

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
            result = combat_item_menu(state, boss, enemy_buffs, enemy)
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

        effect_events = tick_effects(state, player_buffs, enemy_buffs)
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
    try_register_bestiary(state, enemy_id)
    gain_exp(state, enemy["exp"])
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
    stats = get_stats(state, player_buffs)
    skill_bonus = skill.get("accuracy", 0) if skill else 0
    if not hit_roll(stats["accuracy"], enemy["agility"], skill_bonus):
        return CombatActionResult(events=["攻擊落空。"], summary=["攻擊落空。"])
    damage, is_crit = calc_player_damage(state, enemy, skill, player_buffs, enemy_buffs)
    label = skill["name"] if skill else "普通攻擊"
    crit_text = " 暴擊！" if is_crit else ""
    events = [f"你使用{label}，造成 {damage} 傷害。{crit_text}"]
    summary = [f"你使用{label}，造成 {damage} 傷害。{crit_text}"]
    if can_sleeve_blade_followup(state, skill) and enemy_hp - damage > 0:
        followup_damage = calc_sleeve_blade_followup_damage(state, enemy, player_buffs, enemy_buffs)
        damage += followup_damage
        events.append(f"影袖副刃順勢劃出追擊，造成 {followup_damage} 傷害。")
        summary.append(f"影袖副刃追擊 {followup_damage} 傷害。")
    return CombatActionResult(damage=damage, events=events, summary=summary)

def skill_menu(state: dict, enemy: dict, player_buffs: dict, enemy_buffs: dict):
    skills = state["learned_skills"]
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
    state["current_mp"] -= skill["mp"]
    if skill["kind"] == "damage":
        return player_attack(state, enemy, enemy["hp"], skill, player_buffs, enemy_buffs)
    if skill["kind"] == "heal":
        before = state["current_hp"]
        state["current_hp"] = min(stats["max_hp"], state["current_hp"] + skill["amount"])
        healed = state["current_hp"] - before
        line = f"你使用{skill['name']}，回復 {healed} HP。"
        return CombatActionResult(events=[line], summary=[line])
    if skill["kind"] == "buff":
        player_buffs[skill["buff"]] = skill["duration"]
        line = f"你使用{skill['name']}。{skill['desc']}"
        return CombatActionResult(events=[line], summary=[line])
    if skill["kind"] == "debuff":
        enemy_buffs[skill["debuff"]] = skill["duration"]
        line = f"你使用{skill['name']}。{skill['desc']}"
        return CombatActionResult(events=[line], summary=[line])
    return CombatActionResult()

def combat_item_menu(state: dict, boss: bool, enemy_buffs: dict, enemy: dict):
    usable_ids = [
        item_id
        for item_id in ["item_potion_s", "item_potion_m", "item_focus_drop", "item_herb_antidote", "item_armor_piercer", "item_escape_scroll"]
        if state["inventory"].get(item_id, 0) > 0
    ]
    if not usable_ids:
        return CombatActionResult(events=["沒有可用道具。"], summary=["沒有可用道具。"], outcome="cancel")
    options = [f"{item_name(item_id)} x{state['inventory'][item_id]} / {ITEMS[item_id]['desc']}" for item_id in usable_ids]
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
    if item_id == "item_potion_s":
        stats = get_stats(state)
        before = state["current_hp"]
        state["current_hp"] = min(stats["max_hp"], state["current_hp"] + 35)
        remove_item(state, item_id, 1)
        line = f"使用小藥水，回復 {state['current_hp'] - before} HP。"
        return CombatActionResult(events=[line], summary=[line])
    elif item_id == "item_potion_m":
        stats = get_stats(state)
        before = state["current_hp"]
        state["current_hp"] = min(stats["max_hp"], state["current_hp"] + 70)
        remove_item(state, item_id, 1)
        line = f"使用中藥水，回復 {state['current_hp'] - before} HP。"
        return CombatActionResult(events=[line], summary=[line])
    elif item_id == "item_focus_drop":
        stats = get_stats(state)
        before = state["current_mp"]
        state["current_mp"] = min(stats["max_mp"], state["current_mp"] + 12)
        remove_item(state, item_id, 1)
        line = f"使用集中滴露，回復 {state['current_mp'] - before} MP。"
        return CombatActionResult(events=[line], summary=[line])
    elif item_id == "item_herb_antidote":
        remove_item(state, item_id, 1)
        state.setdefault("_clear_burn", True)
        line = "你嚼下解毒草，灼熱感稍微退去。"
        return CombatActionResult(events=[line], summary=[line])
    elif item_id == "item_armor_piercer":
        remove_item(state, item_id, 1)
        enemy_buffs["defense_down"] = max(enemy_buffs.get("defense_down", 0), 3)
        damage = max(8, math.ceil(enemy["hp"] * 0.08))
        line = f"破甲釘命中敵人的護具縫隙，造成 {damage} 傷害，敵方防禦下降。"
        return CombatActionResult(damage=damage, events=[line], summary=[line])
    elif item_id == "item_escape_scroll":
        if boss:
            return CombatActionResult(events=["Boss 戰中無法使用逃脫卷軸。"], summary=["Boss 戰中無法使用逃脫卷軸。"], outcome="cancel")
        remove_item(state, item_id, 1)
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
    if enemy_id == "boss_glen":
        return boss_glen_action(
            enemy,
            enemy_hp,
            state,
            player_buffs,
            enemy_buffs,
            defending,
            turn,
            boss_marker,
        )
    if enemy_id == "boss_ash_guardian":
        return boss_ash_guardian_action(
            enemy,
            enemy_hp,
            state,
            player_buffs,
            enemy_buffs,
            defending,
            turn,
            boss_marker,
        )
    if enemy_id == "boss_cinder_seal_sentinel":
        return boss_cinder_seal_sentinel_action(
            enemy,
            enemy_hp,
            state,
            player_buffs,
            enemy_buffs,
            defending,
            turn,
            boss_marker,
        )
    return boss_marker, monster_action(enemy_id, enemy, state, player_buffs, defending)

def tick_effects(state: dict, player_buffs: dict, enemy_buffs: dict) -> list[str]:
    events = []
    if state.pop("_clear_burn", False):
        player_buffs.pop("burn", None)
    if player_buffs.get("burn", 0) > 0:
        damage = max(1, math.ceil(get_stats(state)["max_hp"] * 0.05))
        state["current_hp"] -= damage
        events.append(f"灼傷造成 {damage} 傷害。")
    for buffs in (player_buffs, enemy_buffs):
        expired = []
        for key in list(buffs.keys()):
            buffs[key] -= 1
            if buffs[key] <= 0:
                expired.append(key)
        for key in expired:
            del buffs[key]
    return events

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
    glen_state = create_state("格倫規則測試", "劍士")
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
    legacy_glen_state = create_state("舊格倫進度測試", "劍士")
    legacy_glen_state["completed_quests"].append("quest_mine_scout")
    legacy_glen_state["flags"]["boss_glen_defeated"] = True
    assert quest_unlocked(legacy_glen_state, "quest_boss_glen")
    assert not can_accept_boss_glen_investigation(legacy_glen_state)
    assert not boss_available_at_dungeon_end(legacy_glen_state, "dungeon_scorched_mine", "boss_glen")
    ice_state = create_state("Ice route smoke", next(iter(JOBS)))
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
    earth_state = create_state("Earth route smoke", next(iter(JOBS)))
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
    thunder_state = create_state("Thunder route smoke", next(iter(JOBS)))
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
    final_gate_state = create_state("Final gate smoke", next(iter(JOBS)))
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
    final_state = create_state("Final route smoke", next(iter(JOBS)))
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
    assert state["inventory"].get("weapon_iron_sword_plus_1", 0) == 1
    state["level"] = 4
    add_item(state, "mat_cracked_stone", 3)
    state["gold"] = 999
    book = MAGIC_BOOKS["book_guardian_rune"]
    assert state["job"] in book["jobs"]
    assert can_pay_items(state, book["materials"])
    pay_items(state, book["materials"])
    state["learned_skills"].append(book["skill"])
    assert "skill_guardian_rune" in state["learned_skills"]
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
