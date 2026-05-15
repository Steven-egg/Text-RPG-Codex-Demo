from __future__ import annotations

import json
import math
import random
import sys
from copy import deepcopy
from pathlib import Path

from .bestiary import monster_locations
from .display import (
    action_menu_panel,
    clear_screen,
    main_menu_panel,
    menu,
    pause,
    render_panel,
    save_prompt_panel,
    setup_console,
    title,
)
from .formatting import equipment_summary, format_items, item_name, monster_drop_names
from .previews import get_preview_promotions_for_job, get_preview_relics, show_job_specialization_preview
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
    SHOP_INVENTORY,
    SKILLS,
)

ROOT = Path(__file__).resolve().parents[2]
SAVE_PATH = ROOT / "save.json"

GUILD_MATERIAL_BUY_PRICES = {
    "mat_moss_fiber": 6,
    "mat_cracked_stone": 6,
    "mat_small_crystal": 14,
    "mat_fire_stone": 18,
    "mat_scorched_iron": 22,
    "mat_lava_shard": 30,
    "mat_ravine_ash": 28,
    "mat_charred_iron": 32,
    "mat_flame_stone_refined": 45,
}

STORAGE_UNLOCK_COST = 500
STORAGE_CAPACITY = 10
SLEEVE_BLADE_FOLLOWUP_MULTIPLIER = 0.35
FIRE_MARK_GUILD_INQUIRY_FLAG = "fire_mark_guild_inquiry_done"
FIRE_MARK_CHURCH_BRIDGE_FLAG = "fire_mark_church_bridge_done"
FIRE_MARK_CHURCH_LOOKUP_FLAG = "fire_mark_church_lookup_done"
FIRE_MARK_SHARD_ID = "key_fire_mark_shard"

def is_key_item(item_id: str) -> bool:
    return item_id.startswith("key_")

def exp_to_next(level: int) -> int:
    return 70 + (level - 1) * 70

def create_state(name: str, job: str) -> dict:
    base = JOBS[job]["base"]
    state = {
        "name": name,
        "job": job,
        "level": 1,
        "exp": 0,
        "gold": 120,
        "guild_points": 0,
        "current_hp": base["max_hp"],
        "current_mp": base["max_mp"],
        "inventory": {},
        "equipment": {"weapon": None, "head": None, "body": None, "accessory": None, "special": None},
        "learned_skills": list(JOBS[job]["base_skills"]),
        "completed_quests": ["quest_register"],
        "unlocked": ["dungeon_moss_cave"],
        "cleared_dungeons": [],
        "flags": {},
        "storage_unlocked": False,
        "storage": {},
        "bestiary": [],
    }
    for item_id, qty in QUESTS["quest_register"]["reward"]["items"].items():
        add_item(state, item_id, qty)
    equip_item(state, "special_trial_badge", quiet=True)
    return state

def ensure_state_defaults(state: dict) -> dict:
    if not isinstance(state.get("flags"), dict):
        state["flags"] = {}
    state.setdefault("storage_unlocked", False)
    if not isinstance(state.get("storage"), dict):
        state["storage"] = {}
    else:
        for item_id, qty in list(state["storage"].items()):
            if not isinstance(qty, int) or qty <= 0:
                del state["storage"][item_id]
    if not isinstance(state.get("bestiary"), list):
        state["bestiary"] = []
    else:
        clean_bestiary = []
        seen = set()
        for monster_id in state["bestiary"]:
            if monster_id in MONSTERS and monster_id not in seen:
                clean_bestiary.append(monster_id)
                seen.add(monster_id)
        state["bestiary"] = clean_bestiary
    return state

def add_item(state: dict, item_id: str, qty: int = 1) -> None:
    if qty <= 0:
        return
    state["inventory"][item_id] = state["inventory"].get(item_id, 0) + qty

def remove_item(state: dict, item_id: str, qty: int = 1) -> bool:
    if qty <= 0:
        return True
    if state["inventory"].get(item_id, 0) < qty:
        return False
    state["inventory"][item_id] -= qty
    if state["inventory"][item_id] <= 0:
        del state["inventory"][item_id]
    return True

def add_storage_item(state: dict, item_id: str, qty: int = 1) -> None:
    if qty <= 0:
        return
    state["storage"][item_id] = state["storage"].get(item_id, 0) + qty

def remove_storage_item(state: dict, item_id: str, qty: int = 1) -> bool:
    if qty <= 0:
        return True
    if state["storage"].get(item_id, 0) < qty:
        return False
    state["storage"][item_id] -= qty
    if state["storage"][item_id] <= 0:
        del state["storage"][item_id]
    return True

def owns_item_or_equipped(state: dict, item_id: str) -> bool:
    if state["inventory"].get(item_id, 0) > 0:
        return True
    return item_id in state["equipment"].values()

def consume_item_or_equipped(state: dict, item_id: str) -> bool:
    if remove_item(state, item_id, 1):
        return True
    for slot, equipped in state["equipment"].items():
        if equipped == item_id:
            state["equipment"][slot] = None
            return True
    return False

def unlock(state: dict, key: str) -> None:
    if key not in state["unlocked"]:
        state["unlocked"].append(key)

def is_unlocked(state: dict, key: str | None) -> bool:
    if not key:
        return True
    return key in state["unlocked"] or key in state["completed_quests"]

def get_stats(state: dict, buffs: dict | None = None) -> dict:
    job = JOBS[state["job"]]
    stats = deepcopy(job["base"])
    level_bonus = state["level"] - 1
    for key, value in job["growth"].items():
        stats[key] += value * level_bonus
    extra_count = (state["level"] - 1) // 3
    for key, value in job["extra_every_3"].items():
        stats[key] = stats.get(key, 0) + value * extra_count

    stats["magic_attack"] = 0
    stats["fire_resist"] = 0
    stats["trap_evasion"] = 0
    stats["rare_drop"] = 0

    for item_id in state["equipment"].values():
        if not item_id:
            continue
        for key, value in EQUIPMENT[item_id].get("stats", {}).items():
            stats[key] = stats.get(key, 0) + value

    if buffs:
        if buffs.get("defense_up", 0) > 0:
            stats["defense"] = math.ceil(stats["defense"] * 1.2)
        if buffs.get("defense_down", 0) > 0:
            stats["defense"] = max(1, math.floor(stats["defense"] * 0.8))
        if buffs.get("quickstep", 0) > 0:
            stats["agility"] = math.ceil(stats["agility"] * 1.25)

    stats["fire_resist"] = min(stats.get("fire_resist", 0), 75)
    return stats

def clamp_vitals(state: dict) -> None:
    stats = get_stats(state)
    state["current_hp"] = max(0, min(state["current_hp"], stats["max_hp"]))
    state["current_mp"] = max(0, min(state["current_mp"], stats["max_mp"]))

def player_summary_line(state: dict) -> str:
    clamp_vitals(state)
    stats = get_stats(state)
    return (
        f"{state['name']} / {state['job']} Lv{state['level']} / "
        f"HP {state['current_hp']}/{stats['max_hp']} / "
        f"MP {state['current_mp']}/{stats['max_mp']} / {state['gold']}G"
    )

def player_resource_lines(state: dict) -> list[str]:
    stats = get_stats(state)
    return [
        player_summary_line(state),
        f"工會積分 {state['guild_points']} / 經驗 {state['exp']}/{exp_to_next(state['level'])}",
        (
            f"攻擊 {stats['attack']} / 魔攻 {stats['magic_attack']} / 防禦 {stats['defense']} / "
            f"敏捷 {stats['agility']} / 暴擊 {stats['crit']}% / 火抗 {stats['fire_resist']}%"
        ),
    ]

def run_loot_summary(run_log: dict) -> str:
    item_lines = [f"{item_name(item_id)} x{qty}" for item_id, qty in sorted(run_log.get("items", {}).items())]
    item_text = "、".join(item_lines) if item_lines else "無"
    return f"本趟收益：{run_log.get('gold', 0)}G / 物品：{item_text}"

def ready_quest_titles(state: dict) -> list[str]:
    return [
        QUESTS[quest_id]["title"]
        for quest_id in QUESTS
        if quest_unlocked(state, quest_id) and quest_ready(state, quest_id)
    ]

def next_step_hint(state: dict) -> str:
    if can_ask_fire_mark_guild_inquiry(state):
        return "三枚火之印記碎片正在共鳴，回冒險者工會詢問諾亞。"
    if should_show_fire_mark_church_lookup(state):
        return "回轉職神殿詢問賽恩的查閱結果。"
    if should_show_fire_mark_church_bridge(state):
        return "帶著三枚火之印記碎片前往轉職神殿。"
    if "quest_cinder_depths_scout" in state["completed_quests"] and not state["flags"].get("cinder_seal_sentinel_defeated"):
        return "前往燼印深窟終點，挑戰燼印鎮衛。"
    if "quest_supply_upgrade" in state["completed_quests"] and "quest_cinder_depths_scout" not in state["completed_quests"]:
        return "探索燼印深窟並完成工會偵查委託。"
    if state["flags"].get("ash_guardian_defeated") and "quest_supply_upgrade" not in state["completed_quests"]:
        return "收集深窟素材，完成補給線升級。"
    if "quest_ash_ravine_scout" in state["completed_quests"] and not state["flags"].get("ash_guardian_defeated"):
        return "前往灰燼裂谷終點，挑戰灰燼守衛。"
    if "quest_boss_glen" in state["completed_quests"] and "quest_ash_ravine_scout" not in state["completed_quests"]:
        return "前往灰燼裂谷，帶回偵查素材。"
    ready_titles = ready_quest_titles(state)
    if ready_titles:
        return f"工會有可交付委託：{ready_titles[0]}。"
    return "整備補給與裝備後，選擇下一座迷宮探索。"

def town_hint_lines(state: dict) -> list[str]:
    hints = []
    main_hint = next_step_hint(state)
    if main_hint != "整備補給與裝備後，選擇下一座迷宮探索。":
        hints.append(main_hint)
    ready_titles = ready_quest_titles(state)
    if ready_titles and not main_hint.startswith("工會有可交付委託"):
        hints.append(f"工會有可交付委託：{'、'.join(ready_titles[:2])}。")
    stats = get_stats(state)
    if state["current_hp"] < stats["max_hp"] or state["current_mp"] < stats["max_mp"]:
        hints.append("旅館可回復 HP/MP，適合在長探索或 Boss 前使用。")
    if state["inventory"].get("item_potion_s", 0) + state["inventory"].get("item_potion_m", 0) == 0:
        hints.append("背包沒有藥水，旅人小鋪可補充探索容錯。")
    if not hints:
        hints.append("把探索收益轉成任務、裝備、技能或補給後再出發。")
    return hints

def guild_hint_lines(state: dict) -> list[str]:
    hints = []
    ready_titles = ready_quest_titles(state)
    if ready_titles:
        hints.append(f"可交付委託：{'、'.join(ready_titles[:2])}。")

    in_progress = []
    for quest_id, quest in QUESTS.items():
        if quest_unlocked(state, quest_id) and quest_id not in state["completed_quests"] and not quest_ready(state, quest_id):
            in_progress.append(f"{quest['title']} 需要 {format_items(quest['turn_in'])}")
    if in_progress:
        hints.append(f"進行中：{in_progress[0]}。")

    if "quest_ash_ravine_scout" in state["completed_quests"] and not state["flags"].get("ash_guardian_defeated"):
        hints.append("灰燼裂谷偵查已完成；灰燼守衛已可在裂谷終點挑戰。")
    elif state["flags"].get("ash_guardian_defeated") and "quest_supply_upgrade" not in state["completed_quests"]:
        hints.append("灰燼守衛已擊敗；補給線升級委託已開放。")
    elif "quest_cinder_depths_scout" in state["completed_quests"] and not state["flags"].get("cinder_seal_sentinel_defeated"):
        hints.append("燼印深窟偵查已完成；燼印鎮衛已可在深窟終點挑戰。")

    if not hints:
        hints.append(next_step_hint(state))
    return hints

def recommended_level_note(recommended: str, level: int) -> str:
    raw = recommended.replace("Lv", "")
    parts = raw.split("-")
    try:
        low = int(parts[0])
        high = int(parts[-1])
    except (ValueError, IndexError):
        return "等級參考"
    if level < low:
        return "等級偏低"
    if level > high + 2:
        return "可穩定回收"
    return "適合探索"

def dungeon_gate_hint(state: dict, dungeon_id: str) -> str:
    dungeon = DUNGEONS[dungeon_id]
    boss_id = dungeon.get("boss")
    if not boss_id:
        return "終點 Boss：無。"
    boss_name = MONSTERS[boss_id]["name"]
    if boss_available_at_dungeon_end(state, dungeon_id, boss_id):
        return f"終點可能遭遇 {boss_name}，出發前確認 HP、藥水與火抗。"
    if state["flags"].get("boss_glen_defeated") and boss_id == "boss_glen":
        return f"{boss_name} 已擊敗。"
    if state["flags"].get("ash_guardian_defeated") and boss_id == "boss_ash_guardian":
        return f"{boss_name} 已擊敗。"
    if state["flags"].get("cinder_seal_sentinel_defeated") and boss_id == "boss_cinder_seal_sentinel":
        return f"{boss_name} 已擊敗。"
    return f"{boss_name} 尚未滿足挑戰條件，先處理工會委託線索。"

def dungeon_boss_status(state: dict, dungeon_id: str) -> str:
    dungeon = DUNGEONS[dungeon_id]
    boss_id = dungeon.get("boss")
    if not boss_id:
        return "Boss 無"
    boss_name = MONSTERS[boss_id]["name"]
    if boss_available_at_dungeon_end(state, dungeon_id, boss_id):
        return f"Boss {boss_name}: 可挑戰"
    if state["flags"].get("boss_glen_defeated") and boss_id == "boss_glen":
        return f"Boss {boss_name}: 已擊敗"
    if state["flags"].get("ash_guardian_defeated") and boss_id == "boss_ash_guardian":
        return f"Boss {boss_name}: 已擊敗"
    if state["flags"].get("cinder_seal_sentinel_defeated") and boss_id == "boss_cinder_seal_sentinel":
        return f"Boss {boss_name}: 已擊敗"
    return f"Boss {boss_name}: 需任務線索"

def dungeon_option_line(state: dict, dungeon_id: str) -> str:
    dungeon = DUNGEONS[dungeon_id]
    clear = "已通關" if dungeon_id in state["cleared_dungeons"] else "未通關"
    level_note = recommended_level_note(dungeon["recommended"], state["level"])
    return (
        f"{dungeon['name']} / 推薦 {dungeon['recommended']} / {dungeon['steps']} 步 / "
        f"{dungeon['element']} / {clear} / {level_note} / {dungeon_boss_status(state, dungeon_id)}"
    )

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
) -> list[str]:
    stats = get_stats(state, player_buffs)
    return [
        f"回合 {turn}",
        f"{state['name']} HP {state['current_hp']}/{stats['max_hp']} / MP {state['current_mp']}/{stats['max_mp']} / 狀態 {buff_summary(player_buffs)}",
        f"{enemy['name']} HP {enemy_hp}/{enemy['hp']} / 屬性 {enemy['element']} / 狀態 {buff_summary(enemy_buffs)}",
    ]

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

def add_gold(state: dict, amount: int, run_log: dict | None = None) -> None:
    if amount <= 0:
        return
    state["gold"] += amount
    if run_log is not None:
        run_log["gold"] += amount

def add_loot(state: dict, item_id: str, qty: int, run_log: dict | None = None) -> None:
    add_item(state, item_id, qty)
    if run_log is not None:
        run_log["items"][item_id] = run_log["items"].get(item_id, 0) + qty

def can_pay_items(state: dict, cost: dict) -> bool:
    for item_id, qty in cost.items():
        if item_id.startswith("flag:"):
            flag = item_id.split(":", 1)[1]
            if not state["flags"].get(flag):
                return False
            continue
        if state["inventory"].get(item_id, 0) < qty:
            return False
    return True

def pay_items(state: dict, cost: dict) -> None:
    for item_id, qty in cost.items():
        if item_id.startswith("flag:"):
            continue
        remove_item(state, item_id, qty)

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

def equip_item(state: dict, item_id: str, quiet: bool = False) -> bool:
    if item_id not in EQUIPMENT:
        return False
    eq = EQUIPMENT[item_id]
    if state["job"] not in eq["jobs"]:
        if not quiet:
            print(f"{state['job']}無法裝備 {eq['name']}。")
        return False
    if state["inventory"].get(item_id, 0) <= 0:
        if not quiet:
            print("背包中沒有這件裝備。")
        return False
    slot = eq["slot"]
    old = state["equipment"].get(slot)
    remove_item(state, item_id, 1)
    if old:
        add_item(state, old, 1)
    state["equipment"][slot] = item_id
    clamp_vitals(state)
    if not quiet:
        print(f"已裝備 {eq['name']}。")
    return True

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

def is_shop_item_available(state: dict, item_id: str) -> bool:
    data = ITEMS.get(item_id) or EQUIPMENT.get(item_id)
    if not data:
        return False
    return is_unlocked(state, data.get("unlock"))

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

def magic_book_price(state: dict, book_id: str) -> int:
    price = MAGIC_BOOKS[book_id]["price"]
    if book_id == "book_spark" and "quest_magic_crystal" in state["completed_quests"]:
        price = max(0, price - 50)
    return price

def magic_shop(state: dict) -> None:
    while True:
        book_ids = list(MAGIC_BOOKS.keys())
        options = []
        for book_id in book_ids:
            book = MAGIC_BOOKS[book_id]
            skill = SKILLS[book["skill"]]
            learned = book["skill"] in state["learned_skills"]
            price = magic_book_price(state, book_id)
            status = "已學會" if learned else f"{price}G，需求 {format_items(book['materials'])}"
            options.append(
                f"{book['name']} / {status} / {','.join(book['jobs'])} Lv{book['level']} / {skill['desc']}"
            )
        choice = action_menu_panel(
            "選擇要學習的魔法書",
            options,
            "星燈魔法商店",
            header_lines=[
                "伊芙輕輕敲了敲書脊：「願星辰指引你的靈魂，冒險者。」",
                f"持有金幣：{state['gold']}G",
            ],
            hint_lines=["魔法書學會後會永久加入戰鬥技能。"],
            allow_back=True,
            border_style="magenta",
        )
        if choice == 0:
            return
        book_id = book_ids[choice - 1]
        book = MAGIC_BOOKS[book_id]
        skill_id = book["skill"]
        price = magic_book_price(state, book_id)
        if skill_id in state["learned_skills"]:
            print("你已經學會這本書的技能。")
        elif state["job"] not in book["jobs"]:
            print(f"{state['job']}無法理解這本魔法書的核心術式。")
        elif state["level"] < book["level"]:
            print(f"等級不足，需要 Lv{book['level']}。")
        elif state["gold"] < price:
            print("金幣不足。")
        elif not can_pay_items(state, book["materials"]):
            print("素材不足。")
        else:
            state["gold"] -= price
            pay_items(state, book["materials"])
            state["learned_skills"].append(skill_id)
            print(f"你學會了 {SKILLS[skill_id]['name']}。")
        pause()

def recipe_available(state: dict, recipe_id: str) -> bool:
    recipe = RECIPES[recipe_id]
    return is_unlocked(state, recipe.get("unlock"))

def craft_menu(state: dict, title_text: str, recipe_ids: list[str]) -> None:
    while True:
        available = [recipe_id for recipe_id in recipe_ids if recipe_available(state, recipe_id)]
        if not available:
            render_panel(title_text, ["目前沒有可用配方。"], border_style="green")
            pause()
            return
        options = []
        for recipe_id in available:
            recipe = RECIPES[recipe_id]
            base = f"，消耗 {item_name(recipe['base_item'])}" if recipe.get("base_item") else ""
            options.append(
                f"{recipe['name']} / {recipe['gold']}G / {format_items(recipe['materials'])}{base} / {recipe['desc']}"
            )
        choice = action_menu_panel(
            "選擇配方",
            options,
            title_text,
            header_lines=[f"持有金幣：{state['gold']}G"],
            hint_lines=["製作會消耗素材；若配方需要基底裝備，已裝備物也可被消耗。"],
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        recipe_id = available[choice - 1]
        craft_recipe(state, recipe_id)
        pause()

def craft_recipe(state: dict, recipe_id: str) -> None:
    recipe = RECIPES[recipe_id]
    if state["gold"] < recipe["gold"]:
        print("金幣不足。")
        return
    if not can_pay_items(state, recipe["materials"]):
        print("素材不足。")
        return
    base_item = recipe.get("base_item")
    if base_item and not owns_item_or_equipped(state, base_item):
        print(f"需要 {item_name(base_item)}。")
        return
    state["gold"] -= recipe["gold"]
    pay_items(state, recipe["materials"])
    if base_item:
        consume_item_or_equipped(state, base_item)
    for item_id, qty in recipe["output"].items():
        add_item(state, item_id, qty)
    print(f"完成：{recipe['name']}。")

def relic_unlock_met(state: dict, unlock_data: dict | None) -> bool:
    if not unlock_data:
        return True
    kind = unlock_data.get("kind")
    if kind == "level":
        return state.get("level", 0) >= unlock_data.get("value", 0)
    if kind == "unlock":
        return is_unlocked(state, unlock_data.get("key"))
    if kind == "quest":
        return unlock_data.get("key") in state.get("completed_quests", [])
    if kind == "flag":
        return bool(state.get("flags", {}).get(unlock_data.get("key")))
    if kind == "item":
        return state.get("inventory", {}).get(unlock_data.get("key"), 0) > 0
    return False

def relic_unlock_line(state: dict, unlock_data: dict | None) -> str:
    if not unlock_data:
        return "解鎖提示：目前無額外提示。"
    status = "已達成" if relic_unlock_met(state, unlock_data) else "未達成"
    return f"解鎖提示：{unlock_data['label']}（{status}）"

def relic_preview_menu(state: dict) -> None:
    title("聖物調查")
    previews = get_preview_relics()
    if not previews:
        print("目前沒有可預覽的聖物線索。")
        pause()
        return

    print("目前僅為預覽，聖物效果尚未開放。")
    for relic in previews:
        print(f"\n{relic['name']}")
        print(relic["summary"])
        print(f"來源：{relic['source']}")
        print(relic_unlock_line(state, relic.get("unlock")))
        print(f"效果預告：{relic['effect_preview']}")
        print(f"狀態：{relic['status']}")
    print("\n這裡不會取得、裝備、啟用或強化聖物。")
    pause()

def town_menu(state: dict) -> None:
    while True:
        options = [
            "冒險者工會 - 委託、素材收購與火印線索",
            "鐵刃工坊 - 武器購買與強化",
            "堅甲工坊 - 防具購買與強化",
            "旅人小鋪 - 補給與特殊道具",
            "米菈合成屋 - 把素材轉成裝備與戰術道具",
            "星燈魔法商店 - 學習永久技能",
            "轉職神殿 - 轉職、火印與未來方向預覽",
            "聖物調查 - 預覽未開放聖物線索",
            "倉庫 - 存放與取出非關鍵物品",
            "旅館休息 30G - 回復 HP/MP",
        ]
        choice = action_menu_panel(
            "你要去哪裡",
            options,
            "邊境城鎮艾爾姆",
            header_lines=player_resource_lines(state)[:2],
            hint_lines=town_hint_lines(state),
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        if choice == 1:
            guild_menu(state)
        elif choice == 2:
            iron_workshop(state)
        elif choice == 3:
            armor_workshop(state)
        elif choice == 4:
            buy_menu(state, "旅人小鋪 - 拉比", SHOP_INVENTORY["travel"])
        elif choice == 5:
            if not is_unlocked(state, "shop_synthesis_01"):
                print("米菈的店門半掩著。先完成工會任務「洞窟採集」吧。")
                pause()
            else:
                craft_menu(
                    state,
                    "米菈合成屋",
                    ["recipe_fire_cloak", "recipe_focus_pouch", "recipe_heat_charm", "recipe_piercing_bundle"],
                )
        elif choice == 6:
            magic_shop(state)
        elif choice == 7:
            temple(state)
        elif choice == 8:
            relic_preview_menu(state)
        elif choice == 9:
            storage_menu(state)
        elif choice == 10:
            rest_inn(state)

def iron_workshop(state: dict) -> None:
    while True:
        choice = action_menu_panel(
            "鐵刃工坊",
            ["購買武器", "強化武器"],
            "鐵刃工坊",
            header_lines=[
                "伴隨著鐵錘敲擊砧台的節奏，這裡充滿了金屬與汗水的硬派氣息。",
                "葛雷抹了一把汗：「最好的防禦就是進攻。」",
            ],
            hint_lines=["武器升級能縮短戰鬥回合；購買後仍需到裝備管理替換。"],
            allow_back=True,
            border_style="yellow",
        )
        if choice == 0:
            return
        if choice == 1:
            buy_menu(state, "鐵刃工坊 - 武器", SHOP_INVENTORY["weapon"])
        elif choice == 2:
            craft_menu(state, "鐵刃工坊 - 強化", ["recipe_iron_sword_plus_1"])

def armor_workshop(state: dict) -> None:
    while True:
        choice = action_menu_panel(
            "堅甲工坊",
            ["購買防具", "強化防具"],
            "堅甲工坊",
            header_lines=[
                "布琳的手指滑過一排整齊的甲冑。",
                "「耐用、實惠，品質無可挑剔。每一件都經得起實戰檢驗。」",
            ],
            hint_lines=["防具與抗性裝能提高長探索容錯；購買後仍需到裝備管理替換。"],
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        if choice == 1:
            buy_menu(state, "堅甲工坊 - 防具", SHOP_INVENTORY["armor"])
        elif choice == 2:
            craft_menu(state, "堅甲工坊 - 強化", ["recipe_leather_armor_plus_1"])

def rest_inn(state: dict) -> None:
    stats = get_stats(state)
    render_panel(
        "微光旅店",
        [
            "旅店老闆擦亮櫃台上的銅鈴：「睡一晚，明天的路會比較像路。」",
            f"費用：30G / 目前金幣：{state['gold']}G",
            f"目前 HP {state['current_hp']}/{stats['max_hp']} / MP {state['current_mp']}/{stats['max_mp']}",
        ],
        border_style="green",
    )
    if state["gold"] < 30:
        print("旅館老闆搖搖頭：「先去工會看看有沒有簡單委託吧。」")
        pause()
        return
    raw = input("要休息一晚嗎？(y/n) > ").strip().lower()
    if raw != "y":
        print("暫不休息。")
    else:
        state["gold"] -= 30
        state["current_hp"] = stats["max_hp"]
        state["current_mp"] = stats["max_mp"]
        print("你在旅館休息了一晚，HP/MP 回滿。")
    pause()

def storage_kind_count(state: dict) -> int:
    ensure_state_defaults(state)
    return len(state["storage"])

def storage_has_room_for(state: dict, item_id: str) -> bool:
    ensure_state_defaults(state)
    return item_id in state["storage"] or storage_kind_count(state) < STORAGE_CAPACITY

def prompt_quantity(action: str, item_id: str, available: int) -> int | None:
    raw = input(f"要{action}幾個 {item_name(item_id)}？目前有 {available} 個，輸入 0 取消 > ").strip()
    try:
        qty = int(raw)
    except ValueError:
        print("請輸入數字。")
        return None
    if qty == 0:
        print("取消。")
        return None
    if qty < 0:
        print("數量不能小於 0。")
        return None
    if qty > available:
        print("數量超過目前持有數量。")
        return None
    return qty

def storage_menu(state: dict) -> None:
    ensure_state_defaults(state)
    if not state["storage_unlocked"]:
        render_panel(
            "工會倉庫",
            [
                "工會旁的小倉庫還沒整理好，木箱上還掛著新的銅鎖。",
                f"開啟 LV1 倉庫需要 {STORAGE_UNLOCK_COST}G。",
                f"目前金幣：{state['gold']}G / 容量：{STORAGE_CAPACITY} 種非關鍵物品。",
            ],
            border_style="green",
        )
        if state["gold"] < STORAGE_UNLOCK_COST:
            print("金幣不足，暫時無法開啟倉庫。")
            pause()
            return
        raw = input(f"要花費 {STORAGE_UNLOCK_COST}G 開啟倉庫嗎？(y/n) > ").strip().lower()
        if raw == "y":
            state["gold"] -= STORAGE_UNLOCK_COST
            state["storage_unlocked"] = True
            print(f"倉庫已開啟。容量：{STORAGE_CAPACITY} 種物品。")
        else:
            print("暫不開啟倉庫。")
        pause()
        return

    while True:
        choice = action_menu_panel(
            "選擇動作",
            ["查看倉庫", "存入物品", "取出物品"],
            "倉庫 LV1",
            header_lines=[
                f"容量：{storage_kind_count(state)}/{STORAGE_CAPACITY} 種物品。",
                "關鍵道具不會存入倉庫。",
            ],
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        if choice == 1:
            show_storage(state)
            pause()
        elif choice == 2:
            storage_deposit_menu(state)
        elif choice == 3:
            storage_withdraw_menu(state)

def show_storage(state: dict) -> None:
    ensure_state_defaults(state)
    if not state["storage"]:
        render_panel("倉庫內容", ["倉庫目前是空的。"], border_style="green")
        return
    lines = [f"{item_name(item_id)} x{qty}" for item_id, qty in state["storage"].items()]
    render_panel("倉庫內容", lines, border_style="green")

def storage_deposit_menu(state: dict) -> None:
    ensure_state_defaults(state)
    if not state["storage_unlocked"]:
        print("倉庫尚未開啟。")
        pause()
        return

    depositable_ids = [
        item_id
        for item_id, qty in state["inventory"].items()
        if qty > 0 and not is_key_item(item_id)
    ]
    if not depositable_ids:
        print("背包裡沒有可存入倉庫的物品。")
        pause()
        return

    options = []
    for item_id in depositable_ids:
        room_note = ""
        if item_id not in state["storage"] and storage_kind_count(state) >= STORAGE_CAPACITY:
            room_note = " / 倉庫已滿，無法新增種類"
        options.append(f"{item_name(item_id)} x{state['inventory'][item_id]}{room_note}")

    choice = action_menu_panel(
        "選擇要存入的物品",
        options,
        "倉庫存入",
        header_lines=[f"容量：{storage_kind_count(state)}/{STORAGE_CAPACITY} 種物品。"],
        allow_back=True,
        border_style="green",
    )
    if choice == 0:
        return

    item_id = depositable_ids[choice - 1]
    if not storage_has_room_for(state, item_id):
        print("倉庫已滿，無法存入新的物品種類。")
        pause()
        return

    qty = prompt_quantity("存入", item_id, state["inventory"].get(item_id, 0))
    if qty is None:
        pause()
        return

    if remove_item(state, item_id, qty):
        add_storage_item(state, item_id, qty)
        print(f"已存入 {item_name(item_id)} x{qty}。")
    else:
        print("背包中的物品數量不足。")
    pause()

def storage_withdraw_menu(state: dict) -> None:
    ensure_state_defaults(state)
    if not state["storage_unlocked"]:
        print("倉庫尚未開啟。")
        pause()
        return
    if not state["storage"]:
        print("倉庫目前是空的。")
        pause()
        return

    item_ids = list(state["storage"].keys())
    options = [f"{item_name(item_id)} x{state['storage'][item_id]}" for item_id in item_ids]
    choice = action_menu_panel(
        "選擇要取出的物品",
        options,
        "倉庫取出",
        header_lines=[f"容量：{storage_kind_count(state)}/{STORAGE_CAPACITY} 種物品。"],
        allow_back=True,
        border_style="green",
    )
    if choice == 0:
        return

    item_id = item_ids[choice - 1]
    qty = prompt_quantity("取出", item_id, state["storage"].get(item_id, 0))
    if qty is None:
        pause()
        return

    if remove_storage_item(state, item_id, qty):
        add_item(state, item_id, qty)
        print(f"已取出 {item_name(item_id)} x{qty}。")
    else:
        print("倉庫中的物品數量不足。")
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

def quest_unlocked(state: dict, quest_id: str) -> bool:
    if quest_id == "quest_register":
        return True
    if quest_id in {"quest_cave_gathering", "quest_magic_crystal"}:
        return "quest_register" in state["completed_quests"]
    if quest_id == "quest_mine_scout":
        return "quest_cave_gathering" in state["completed_quests"]
    if quest_id == "quest_boss_glen":
        return "quest_mine_scout" in state["completed_quests"]
    if quest_id == "quest_ash_ravine_scout":
        return "quest_boss_glen" in state["completed_quests"]
    if quest_id == "quest_supply_upgrade":
        return state["flags"].get("ash_guardian_defeated", False)
    if quest_id == "quest_cinder_depths_scout":
        return "quest_supply_upgrade" in state["completed_quests"]
    return False

def quest_ready(state: dict, quest_id: str) -> bool:
    if quest_id in state["completed_quests"]:
        return False
    return can_pay_items(state, QUESTS[quest_id]["turn_in"])

def can_ask_fire_mark_guild_inquiry(state: dict) -> bool:
    return (
        state["inventory"].get(FIRE_MARK_SHARD_ID, 0) >= 3
        and not state["flags"].get(FIRE_MARK_GUILD_INQUIRY_FLAG)
    )

def fire_mark_guild_inquiry(state: dict) -> None:
    title("詢問三枚印記碎片的事情")
    print("你把三枚火之印記碎片放在諾亞面前。")
    print("碎片彼此靠近時，裂紋裡浮起微弱的紅光，像在回應同一個呼吸。")
    print()
    print("諾亞仔細翻過工會的舊紀錄，最後搖了搖頭：")
    print("「三枚碎片的反應已經很明顯，但工會沒有足夠資料判讀它真正的用途。」")
    print("「去教堂問問吧。教會保存的舊文獻，也許能解釋這些印記碎片代表什麼。」")
    print()
    print("正式火之印記流程尚未開放；你已記下下一步該詢問教會。")
    state["flags"][FIRE_MARK_GUILD_INQUIRY_FLAG] = True

def guild_menu(state: dict) -> None:
    while True:
        options = ["查看委託任務", "收購素材"]
        inquiry_option = can_ask_fire_mark_guild_inquiry(state)
        if inquiry_option:
            options.append("詢問三枚印記碎片的事情")
        choice = action_menu_panel(
            "選擇服務",
            options,
            "冒險者工會",
            header_lines=[
                "諾亞從一堆文件中抬頭，對你點了點頭。",
                "「歡迎回來。想挑戰新目標，還是要交付已完成的委託？」",
            ],
            hint_lines=guild_hint_lines(state),
            allow_back=True,
            border_style="cyan",
        )
        if choice == 0:
            return
        if choice == 1:
            guild_quest_menu(state)
        elif choice == 2:
            guild_material_buy_menu(state)
        elif inquiry_option and choice == 3:
            fire_mark_guild_inquiry(state)
            pause()

def guild_quest_menu(state: dict) -> None:
    while True:
        quest_ids = [qid for qid in QUESTS if quest_unlocked(state, qid)]
        options = []
        for quest_id in quest_ids:
            quest = QUESTS[quest_id]
            if quest_id in state["completed_quests"]:
                status = "已完成"
            elif quest_ready(state, quest_id):
                status = "可交付"
            else:
                status = f"進行中，需求 {format_items(quest['turn_in'])}"
            options.append(f"{quest['title']} / {status}")
        choice = action_menu_panel(
            "選擇任務",
            options,
            "工會委託",
            header_lines=["委託清單會保留已完成任務，方便確認目前進度。"],
            hint_lines=guild_hint_lines(state),
            allow_back=True,
            border_style="cyan",
        )
        if choice == 0:
            return
        quest_id = quest_ids[choice - 1]
        show_or_complete_quest(state, quest_id)
        pause()

def guild_material_buy_menu(state: dict) -> None:
    while True:
        buyable_ids = [
            item_id
            for item_id in GUILD_MATERIAL_BUY_PRICES
            if state["inventory"].get(item_id, 0) > 0
        ]
        if not buyable_ids:
            render_panel(
                "工會收購素材",
                [
                    "諾亞推來一只木箱：「只收登記過的可重複素材，劇情物品我可不敢碰。」",
                    "背包裡沒有工會目前收購的素材。",
                ],
                border_style="cyan",
            )
            pause()
            return

        options = []
        for item_id in buyable_ids:
            qty = state["inventory"][item_id]
            price = GUILD_MATERIAL_BUY_PRICES[item_id]
            options.append(f"{item_name(item_id)} x{qty} / 單價 {price}G")

        choice = action_menu_panel(
            "選擇要出售的素材",
            options,
            "工會收購素材",
            header_lines=["諾亞推來一只木箱：「只收登記過的可重複素材，劇情物品我可不敢碰。」"],
            allow_back=True,
            border_style="cyan",
        )
        if choice == 0:
            return

        item_id = buyable_ids[choice - 1]
        owned = state["inventory"].get(item_id, 0)
        price = GUILD_MATERIAL_BUY_PRICES[item_id]
        raw = input(f"要出售幾個 {item_name(item_id)}？目前有 {owned} 個，輸入 0 取消 > ").strip()
        try:
            qty = int(raw)
        except ValueError:
            print("請輸入數字。")
            pause()
            continue

        if qty == 0:
            print("取消出售。")
            pause()
            continue
        if qty < 0:
            print("數量不能小於 0。")
            pause()
            continue
        if qty > owned:
            print("背包中的素材數量不足。")
            pause()
            continue

        total = qty * price
        print(f"收購價格：{item_name(item_id)} x{qty} = {total}G。")
        confirm = input("確定出售嗎？(y/n) > ").strip().lower()
        if confirm != "y":
            print("取消出售。")
            pause()
            continue

        remove_item(state, item_id, qty)
        state["gold"] += total
        print(f"已出售 {item_name(item_id)} x{qty}，獲得 {total}G。")
        pause()

def show_or_complete_quest(state: dict, quest_id: str) -> None:
    quest = QUESTS[quest_id]
    title(quest["title"])
    print(f"委託人：{quest['giver']}")
    print(quest["desc"])
    if quest_id in state["completed_quests"]:
        print("這個任務已完成。")
        return
    print(f"交付需求：{format_items(quest['turn_in'])}")
    if not quest_ready(state, quest_id):
        print("目前還不能交付。")
        return
    raw = input("要交付任務嗎？(y/n) > ").strip().lower()
    if raw != "y":
        return
    pay_items(state, quest["turn_in"])
    reward = quest["reward"]
    state["gold"] += reward.get("gold", 0)
    guild_gain = reward.get("guild", 0)
    if state["equipment"].get("special") == "special_trial_badge":
        guild_gain = math.ceil(guild_gain * 1.05)
    state["guild_points"] += guild_gain
    for item_id, qty in reward.get("items", {}).items():
        add_item(state, item_id, qty)
    for key in quest.get("unlocks", []):
        unlock(state, key)
    state["completed_quests"].append(quest_id)
    print(f"任務完成。獲得 {reward.get('gold', 0)}G、工會積分 +{guild_gain}。")
    if quest_id == "quest_cave_gathering":
        print("米菈合成屋開放了。拉比也開始販售逃脫卷軸。")
    elif quest_id == "quest_magic_crystal":
        print("伊芙記下小魔晶的光色。火花術書現在折價 50G。")
    elif quest_id == "quest_mine_scout":
        print("拉比壓低聲音：焦石礦坑深處很熱，抗火斗篷的配方已交給米菈。")
    elif quest_id == "quest_boss_glen":
        print("諾亞看著血跡地圖，表情第一次變得猶豫。第二幕的元素迷宮露出了入口。")
        print("下一步很明確：前往「迷宮探索」中的灰燼裂谷，先帶回少量裂谷素材完成偵查。")
    elif quest_id == "quest_ash_ravine_scout":
        print("諾亞收起裂谷灰與焦黑鐵片：這些足夠證明灰燼裂谷值得深入調查，但現在還不是挑戰守衛的時候。")
    elif quest_id == "quest_supply_upgrade":
        print("諾亞點頭：旅人小鋪已能販售中藥水。接下來的長戰鬥，記得把補給準備好。")
    elif quest_id == "quest_cinder_depths_scout":
        print("諾亞攤開偵查圖：深窟最底層有一座燼印鎮衛。若要第三枚火之印記碎片，只能親自擊敗它。")

def promotion_requirement_met(state: dict, requirement: dict) -> bool:
    kind = requirement.get("kind")
    if kind == "level":
        return state.get("level", 0) >= requirement.get("value", 0)
    if kind == "unlock":
        return is_unlocked(state, requirement.get("key"))
    if kind == "quest":
        return requirement.get("key") in state.get("completed_quests", [])
    if kind == "flag":
        return bool(state.get("flags", {}).get(requirement.get("key")))
    if kind == "item":
        return state.get("inventory", {}).get(requirement.get("key"), 0) > 0
    return False


def promotion_requirement_line(state: dict, requirement: dict) -> str:
    status = "已達成" if promotion_requirement_met(state, requirement) else "未達成"
    return f"- [{status}] {requirement['label']}"


def should_show_fire_mark_church_bridge(state: dict) -> bool:
    return (
        state["flags"].get(FIRE_MARK_GUILD_INQUIRY_FLAG, False)
        and state["inventory"].get(FIRE_MARK_SHARD_ID, 0) >= 3
        and not state["flags"].get(FIRE_MARK_CHURCH_BRIDGE_FLAG)
    )


def fire_mark_church_bridge(state: dict) -> None:
    print("賽恩聽完諾亞的轉介，視線落在三枚火之印記碎片上。")
    print("碎片的紅光在神殿石階間一明一滅，像是在尋找尚未打開的門。")
    print("「工會看不懂它，是因為這不是委託紀錄裡的東西。」賽恩低聲說。")
    print("「它不普通，但我還不能斷言它是什麼。我要花點時間查閱舊文獻。」")
    print("「先把碎片收好。等我整理出線索，再回神殿找我。」")
    print()
    print("你記下賽恩的囑咐：先保管碎片，稍後再回神殿詢問查閱結果。")
    state["flags"][FIRE_MARK_CHURCH_BRIDGE_FLAG] = True
    print()


def should_show_fire_mark_church_lookup(state: dict) -> bool:
    return (
        state["flags"].get(FIRE_MARK_CHURCH_BRIDGE_FLAG, False)
        and state["inventory"].get(FIRE_MARK_SHARD_ID, 0) >= 3
        and not state["flags"].get(FIRE_MARK_CHURCH_LOOKUP_FLAG)
    )


def fire_mark_church_lookup(state: dict) -> None:
    print("賽恩把翻開的舊文獻推到石桌中央，頁面上畫著三道分裂的火印。")
    print("「查到了。這三枚碎片不是完整的火之印記，而是它尚未完成的核心。」")
    print("「它記錄了火的資格，卻還沒有承載力量。現在啟用，只會把印記燒毀。」")
    print()
    print("賽恩用封蠟與灰白布帶暫時封住碎片的共鳴，又把它們交還給你。")
    print("「先保管好。等找到真正的熔印之地，再談合成與承載。」")
    print()
    print("已確認：未完成的火之印記核心。")
    print("正式火之印記合成、啟用與聖物效果尚未開放。")
    state["flags"][FIRE_MARK_CHURCH_LOOKUP_FLAG] = True
    print()


def temple(state: dict) -> None:
    title("轉職神殿")
    print("賽恩站在門前，像一塊懂得呼吸的石碑。")
    if should_show_fire_mark_church_bridge(state):
        fire_mark_church_bridge(state)
    elif should_show_fire_mark_church_lookup(state):
        fire_mark_church_lookup(state)
    if state["flags"].get("boss_glen_defeated"):
        print("賽恩看著你手中的火之印記碎片：")
        print("「這還不是完整的印記。但神殿記得它的溫度。若你找到更多線索，再回來找我。」")
    print()
    print(f"目前職業：{state['job']}")
    previews = get_preview_promotions_for_job(state["job"])
    if not previews:
        print("目前尚無可預覽轉職方向。")
    else:
        print("可預覽轉職方向：")
        for promotion in previews:
            print(f"\n{state['job']} → {promotion['name']}")
            print(promotion["summary"])
            print("條件狀態：")
            for requirement in promotion["requirements"]:
                print(promotion_requirement_line(state, requirement))
    print("\n正式轉職尚未開放。")
    print("神殿目前只顯示未來方向，不會改變你的職業或能力。")
    pause()

def choose_weighted_event() -> str:
    total = sum(weight for _, weight in EVENT_WEIGHTS)
    roll = random.randint(1, total)
    current = 0
    for event, weight in EVENT_WEIGHTS:
        current += weight
        if roll <= current:
            return event
    return "empty"

def dungeon_menu(state: dict) -> None:
    if state["flags"].get("ash_guardian_defeated") and not is_unlocked(state, "dungeon_cinder_seal_depths"):
        unlock(state, "dungeon_cinder_seal_depths")
    unlocked_dungeons = [dungeon_id for dungeon_id, d in DUNGEONS.items() if is_unlocked(state, d["unlock"])]
    if not unlocked_dungeons:
        print("目前沒有可探索的迷宮。")
        pause()
        return
    options = [dungeon_option_line(state, dungeon_id) for dungeon_id in unlocked_dungeons]
    hint_lines = [next_step_hint(state)]
    if any(DUNGEONS[dungeon_id]["element"] == "火" for dungeon_id in unlocked_dungeons):
        hint_lines.append(f"目前火抗 {get_stats(state)['fire_resist']}%，火系迷宮前建議檢查補給。")
    choice = action_menu_panel(
        "選擇迷宮",
        options,
        "迷宮探索",
        header_lines=[player_summary_line(state)],
        hint_lines=hint_lines,
        allow_back=True,
        border_style="yellow",
    )
    if choice == 0:
        return
    explore_dungeon(state, unlocked_dungeons[choice - 1])

def boss_available_at_dungeon_end(state: dict, dungeon_id: str, boss_id: str | None) -> bool:
    if boss_id == "boss_glen":
        return not state["flags"].get("boss_glen_defeated")
    if boss_id == "boss_ash_guardian":
        return (
            dungeon_id == "dungeon_ash_ravine"
            and "quest_ash_ravine_scout" in state["completed_quests"]
            and not state["flags"].get("ash_guardian_defeated")
        )
    if boss_id == "boss_cinder_seal_sentinel":
        return (
            dungeon_id == "dungeon_cinder_seal_depths"
            and "quest_cinder_depths_scout" in state["completed_quests"]
            and not state["flags"].get("cinder_seal_sentinel_defeated")
        )
    return False

def boss_challenge_prompt(boss_id: str) -> str:
    if boss_id == "boss_ash_guardian":
        return "裂谷深處的灰燼凝成古老守衛。要挑戰灰燼守衛嗎？(y/n) > "
    if boss_id == "boss_cinder_seal_sentinel":
        return "燼印深窟的最底層浮現赤紅刻印。要挑戰燼印鎮衛嗎？(y/n) > "
    return "礦坑深處傳來粗暴的笑聲。要挑戰 Boss 嗎？(y/n) > "

def clear_dungeon_boss(state: dict, boss_id: str, run_log: dict) -> None:
    if boss_id == "boss_glen":
        clear_boss_glen(state, run_log)
    elif boss_id == "boss_ash_guardian":
        clear_ash_guardian(state, run_log)
    elif boss_id == "boss_cinder_seal_sentinel":
        clear_cinder_seal_sentinel(state, run_log)

def explore_dungeon(state: dict, dungeon_id: str) -> None:
    dungeon = DUNGEONS[dungeon_id]
    run_log = {"gold": 0, "items": {}}
    render_panel(
        dungeon["name"],
        [
            f"推薦等級：{dungeon['recommended']} / 目前 {state['job']} Lv{state['level']} ({recommended_level_note(dungeon['recommended'], state['level'])})",
            f"主要屬性：{dungeon['element']} / 路線長度：{dungeon['steps']} 步",
            dungeon_gate_hint(state, dungeon_id),
            "按 Enter 前進；輸入 r 可帶著本趟收穫撤退。",
        ],
        border_style="yellow",
    )
    if state["equipment"].get("special") == "special_focus_pouch":
        add_loot(state, "item_focus_drop", 1, run_log)
        print("集中藥袋發出微光，你在出發前多整理出一瓶集中滴露。")
    for step in range(1, dungeon["steps"] + 1):
        clamp_vitals(state)
        stats = get_stats(state)
        if state["current_hp"] <= 0:
            handle_defeat(state, run_log)
            return
        render_panel(
            "探索狀態",
            [
                f"{dungeon['name']} / 第 {step}/{dungeon['steps']} 步",
                f"HP {state['current_hp']}/{stats['max_hp']} / MP {state['current_mp']}/{stats['max_mp']}",
                run_loot_summary(run_log),
            ],
            border_style="green",
        )
        raw = input("按 Enter 前進，輸入 r 撤退 > ").strip().lower()
        if raw == "r":
            print("你帶著本趟收穫返回城鎮。")
            render_panel("探索結算", ["撤退成功。", run_loot_summary(run_log)], border_style="green")
            pause()
            return
        event = choose_weighted_event()
        if event == "battle":
            monster_id = random.choice(dungeon["monsters"])
            result = combat(state, monster_id, boss=False, run_log=run_log)
            if result is False:
                handle_defeat(state, run_log)
                return
        elif event == "material":
            dungeon_material_event(state, dungeon, run_log)
        elif event == "treasure":
            dungeon_treasure_event(state, dungeon, run_log)
        elif event == "trap":
            dungeon_trap_event(state, dungeon)
        elif event == "special":
            dungeon_special_event(state, dungeon_id, run_log)
        else:
            print(random.choice([
                "你聽見遠處有水滴聲，除此之外什麼也沒有。",
                "地上的舊腳印很快被灰塵蓋住。",
                "這一段路安靜得像在等你先開口。",
            ]))

    print(f"\n你走完了 {dungeon['name']} 的探索路線。")
    if dungeon_id not in state["cleared_dungeons"]:
        state["cleared_dungeons"].append(dungeon_id)
        state["guild_points"] += dungeon["clear_guild"]
        print(f"首次通關探索路線，工會積分 +{dungeon['clear_guild']}。")

    boss_id = dungeon.get("boss")
    if boss_available_at_dungeon_end(state, dungeon_id, boss_id):
        raw = input(boss_challenge_prompt(boss_id)).strip().lower()
        if raw == "y":
            result = combat(state, boss_id, boss=True, run_log=run_log)
            if result is False:
                handle_defeat(state, run_log)
                return
            if result is True:
                clear_dungeon_boss(state, boss_id, run_log)
    elif (
        dungeon_id == "dungeon_cinder_seal_depths"
        and boss_id == "boss_cinder_seal_sentinel"
        and not state["flags"].get("cinder_seal_sentinel_defeated")
    ):
        print("\n深窟深處仍殘留著某種守護者的氣息。")
        print("這裡似乎還有未解開的事情。或許可以回冒險者工會詢問諾亞。")
    render_panel(
        "探索結算",
        [
            f"完成路線：{dungeon['name']}",
            run_loot_summary(run_log),
            next_step_hint(state),
        ],
        border_style="green",
    )
    pause()

def dungeon_material_event(state: dict, dungeon: dict, run_log: dict) -> None:
    item_id = random.choice(dungeon["materials"])
    qty = 2 if random.random() < 0.2 else 1
    add_loot(state, item_id, qty, run_log)
    print(f"你找到 {item_name(item_id)} x{qty}。")

def dungeon_treasure_event(state: dict, dungeon: dict, run_log: dict) -> None:
    if random.random() < 0.65:
        gold = random.randint(*dungeon["gold_range"])
        add_gold(state, gold, run_log)
        print(f"你打開一只舊木箱，取得 {gold}G。")
    else:
        item_id = random.choice(["item_potion_s", "item_focus_drop"])
        add_loot(state, item_id, 1, run_log)
        print(f"你找到 {item_name(item_id)} x1。")

def dungeon_trap_event(state: dict, dungeon: dict) -> None:
    stats = get_stats(state)
    dodge = min(65, stats["agility"] * 2 + stats.get("trap_evasion", 0))
    if random.randint(1, 100) <= dodge:
        print("你察覺地面異樣，及時避開了陷阱。")
        return
    if dungeon["element"] == "火":
        damage = math.ceil(14 * (1 - stats["fire_resist"] / 100))
        state["current_hp"] -= damage
        print(f"熱風從裂縫噴出，你受到 {damage} 點火傷害。")
    else:
        damage = 8
        state["current_hp"] -= damage
        print(f"碎石從腳邊滑落，你受到 {damage} 點傷害。")

def dungeon_special_event(state: dict, dungeon_id: str, run_log: dict) -> None:
    if dungeon_id == "dungeon_moss_cave":
        add_loot(state, "mat_small_crystal", 1, run_log)
        print("牆上刻著舊工會標記：別把小魔晶賣掉。你取得小魔晶 x1。")
    else:
        print("你發現有人故意遮住通往深處的舊路標。拉比的情報看來沒錯。")
        if random.random() < 0.4:
            add_loot(state, "mat_lava_shard", 1, run_log)
            print("路標後方還卡著熔岩碎片 x1。")

def handle_defeat(state: dict, run_log: dict) -> None:
    lost_gold = math.floor(run_log.get("gold", 0) * 0.3)
    state["gold"] = max(0, state["gold"] - lost_gold)
    lost_items = []
    for item_id, qty in run_log.get("items", {}).items():
        lose_qty = math.floor(qty * 0.3)
        if lose_qty > 0 and state["inventory"].get(item_id, 0) > 0:
            actual = min(lose_qty, state["inventory"].get(item_id, 0))
            remove_item(state, item_id, actual)
            lost_items.append(f"{item_name(item_id)} x{actual}")
    stats = get_stats(state)
    state["current_hp"] = max(1, stats["max_hp"] // 2)
    state["current_mp"] = max(0, stats["max_mp"] // 2)
    result_lines = [
        "工會救援隊把你帶回艾爾姆。",
        f"失去本趟金幣 {lost_gold}G。",
        "散落素材：" + "、".join(lost_items) if lost_items else "素材大致都保住了。",
        f"回城後 HP {state['current_hp']}/{stats['max_hp']} / MP {state['current_mp']}/{stats['max_mp']}",
        next_step_hint(state),
    ]
    render_panel("戰鬥失敗 / 回城結算", result_lines, border_style="red")
    pause()

def clear_boss_glen(state: dict, run_log: dict) -> None:
    state["flags"]["boss_glen_defeated"] = True
    add_loot(state, "key_blood_map", 1, run_log)
    add_loot(state, "key_fire_mark_shard", 1, run_log)
    add_loot(state, "mat_lava_shard", 2, run_log)
    print("\n葛倫倒下時，懷裡掉出一張染血地圖。")
    print("取得 血跡地圖 x1、火之印記碎片 x1、熔岩碎片 x2。")

def clear_ash_guardian(state: dict, run_log: dict) -> None:
    if state["flags"].get("ash_guardian_defeated"):
        return
    state["flags"]["ash_guardian_defeated"] = True
    unlock(state, "dungeon_cinder_seal_depths")
    add_loot(state, "key_fire_mark_shard", 1, run_log)
    print("\n灰燼守衛的爐心逐漸熄滅，一枚赤紅碎片從灰殼中落下。")
    print("取得 火之印記碎片 x1。")

def clear_cinder_seal_sentinel(state: dict, run_log: dict) -> None:
    if state["flags"].get("cinder_seal_sentinel_defeated"):
        return
    state["flags"]["cinder_seal_sentinel_defeated"] = True
    add_loot(state, "key_fire_mark_shard", 1, run_log)
    print("\n燼印鎮衛碎裂時，胸口的赤紅刻印凝成第三枚碎片。")
    print("取得 火之印記碎片 x1。")
    print("三枚碎片短暫共鳴，像有一個尚未說出口的名字在灰燼裡亮起。")

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
            header_lines=combat_panel_lines(state, enemy, enemy_hp, turn, player_buffs, enemy_buffs),
            hint_lines=["Boss 戰不可逃跑。" if boss else "逃跑失敗時敵人仍會行動。"],
            allow_back=False,
            border_style="red" if boss else "yellow",
        )
        defending = False
        escaped = False

        if choice == 1:
            escaped = player_attack(state, enemy, enemy_hp, None, player_buffs, enemy_buffs)
            if isinstance(escaped, int):
                enemy_hp -= escaped
        elif choice == 2:
            defending = True
            if player_buffs.get("defense_up", 0) > 0:
                stats = get_stats(state, player_buffs)
                state["current_mp"] = min(stats["max_mp"], state["current_mp"] + 2)
                print("你穩住姿勢，符文讓你回復 MP 2。")
            print("你採取防禦姿態。")
        elif choice == 3:
            result = skill_menu(state, enemy, player_buffs, enemy_buffs)
            if result == "cancel":
                continue
            if isinstance(result, int):
                enemy_hp -= result
        elif choice == 4:
            result = combat_item_menu(state, boss, enemy_buffs, enemy)
            if result == "cancel":
                continue
            if result == "escaped":
                return "fled"
            if isinstance(result, int):
                enemy_hp -= result
        elif not boss and choice == 5:
            if try_escape(state, enemy):
                print("你成功脫離戰鬥。")
                return "fled"
            print("逃跑失敗。")

        if enemy_hp <= 0:
            break

        if boss and enemy_id == "boss_glen":
            boss_marker = boss_glen_action(enemy, enemy_hp, state, player_buffs, enemy_buffs, defending, turn, boss_marker)
        elif boss and enemy_id == "boss_ash_guardian":
            boss_marker = boss_ash_guardian_action(enemy, enemy_hp, state, player_buffs, enemy_buffs, defending, turn, boss_marker)
        elif boss and enemy_id == "boss_cinder_seal_sentinel":
            boss_marker = boss_cinder_seal_sentinel_action(enemy, enemy_hp, state, player_buffs, enemy_buffs, defending, turn, boss_marker)
        else:
            monster_action(enemy_id, enemy, state, player_buffs, defending)

        tick_effects(state, player_buffs, enemy_buffs)
        turn += 1

    if state["current_hp"] <= 0:
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
    return True

def player_attack(state: dict, enemy: dict, enemy_hp: int, skill: dict | None, player_buffs: dict, enemy_buffs: dict):
    stats = get_stats(state, player_buffs)
    skill_bonus = skill.get("accuracy", 0) if skill else 0
    if not hit_roll(stats["accuracy"], enemy["agility"], skill_bonus):
        print("攻擊落空。")
        return 0
    damage, is_crit = calc_player_damage(state, enemy, skill, player_buffs, enemy_buffs)
    label = skill["name"] if skill else "普通攻擊"
    crit_text = " 暴擊！" if is_crit else ""
    print(f"你使用{label}，造成 {damage} 傷害。{crit_text}")
    if can_sleeve_blade_followup(state, skill) and enemy_hp - damage > 0:
        followup_damage = calc_sleeve_blade_followup_damage(state, enemy, player_buffs, enemy_buffs)
        damage += followup_damage
        print(f"影袖副刃順勢劃出追擊，造成 {followup_damage} 傷害。")
    return damage

def skill_menu(state: dict, enemy: dict, player_buffs: dict, enemy_buffs: dict):
    skills = state["learned_skills"]
    options = []
    for skill_id in skills:
        skill = SKILLS[skill_id]
        options.append(f"{skill['name']} / MP {skill['mp']} / {skill['desc']}")
    choice = menu("選擇技能", options)
    if choice == 0:
        return "cancel"
    skill_id = skills[choice - 1]
    skill = SKILLS[skill_id]
    if state["current_mp"] < skill["mp"]:
        print("MP 不足。")
        return "cancel"
    state["current_mp"] -= skill["mp"]
    if skill["kind"] == "damage":
        return player_attack(state, enemy, enemy["hp"], skill, player_buffs, enemy_buffs)
    if skill["kind"] == "heal":
        stats = get_stats(state, player_buffs)
        before = state["current_hp"]
        state["current_hp"] = min(stats["max_hp"], state["current_hp"] + skill["amount"])
        print(f"你使用{skill['name']}，回復 {state['current_hp'] - before} HP。")
        return None
    if skill["kind"] == "buff":
        player_buffs[skill["buff"]] = skill["duration"]
        print(f"你使用{skill['name']}。{skill['desc']}")
        return None
    if skill["kind"] == "debuff":
        enemy_buffs[skill["debuff"]] = skill["duration"]
        print(f"你使用{skill['name']}。{skill['desc']}")
        return None
    return None

def combat_item_menu(state: dict, boss: bool, enemy_buffs: dict, enemy: dict):
    usable_ids = [
        item_id
        for item_id in ["item_potion_s", "item_potion_m", "item_focus_drop", "item_herb_antidote", "item_armor_piercer", "item_escape_scroll"]
        if state["inventory"].get(item_id, 0) > 0
    ]
    if not usable_ids:
        print("沒有可用道具。")
        return "cancel"
    options = [f"{item_name(item_id)} x{state['inventory'][item_id]} / {ITEMS[item_id]['desc']}" for item_id in usable_ids]
    choice = menu("選擇道具", options)
    if choice == 0:
        return "cancel"
    item_id = usable_ids[choice - 1]
    if item_id == "item_potion_s":
        stats = get_stats(state)
        before = state["current_hp"]
        state["current_hp"] = min(stats["max_hp"], state["current_hp"] + 35)
        remove_item(state, item_id, 1)
        print(f"使用小藥水，回復 {state['current_hp'] - before} HP。")
    elif item_id == "item_potion_m":
        stats = get_stats(state)
        before = state["current_hp"]
        state["current_hp"] = min(stats["max_hp"], state["current_hp"] + 70)
        remove_item(state, item_id, 1)
        print(f"使用中藥水，回復 {state['current_hp'] - before} HP。")
    elif item_id == "item_focus_drop":
        stats = get_stats(state)
        before = state["current_mp"]
        state["current_mp"] = min(stats["max_mp"], state["current_mp"] + 12)
        remove_item(state, item_id, 1)
        print(f"使用集中滴露，回復 {state['current_mp'] - before} MP。")
    elif item_id == "item_herb_antidote":
        remove_item(state, item_id, 1)
        state.setdefault("_clear_burn", True)
        print("你嚼下解毒草，灼熱感稍微退去。")
    elif item_id == "item_armor_piercer":
        remove_item(state, item_id, 1)
        enemy_buffs["defense_down"] = max(enemy_buffs.get("defense_down", 0), 3)
        damage = max(8, math.ceil(enemy["hp"] * 0.08))
        print(f"破甲釘命中敵人的護具縫隙，造成 {damage} 傷害，敵方防禦下降。")
        return damage
    elif item_id == "item_escape_scroll":
        if boss:
            print("Boss 戰中無法使用逃脫卷軸。")
            return "cancel"
        remove_item(state, item_id, 1)
        print("卷軸化成白光，你撤回迷宮入口。")
        return "escaped"
    return None

def try_escape(state: dict, enemy: dict) -> bool:
    stats = get_stats(state)
    chance = 45 + (stats["agility"] - enemy["agility"]) * 3
    chance = max(25, min(85, chance))
    return random.randint(1, 100) <= chance

def monster_action(enemy_id: str, enemy: dict, state: dict, player_buffs: dict, defending: bool) -> None:
    if enemy_id == "mon_lava_imp" and random.random() < 0.35:
        damage = calc_enemy_damage(enemy, state, 1.1, "火", player_buffs, defending)
        state["current_hp"] -= damage
        print(f"{enemy['name']}丟出小火球，造成 {damage} 火傷害。")
        if random.random() < 0.2:
            player_buffs["burn"] = 3
            print("你陷入灼傷。")
        return
    if enemy_id == "mon_scorched_guard" and random.random() < 0.3:
        damage = calc_enemy_damage(enemy, state, 1.0, "物理", player_buffs, defending)
        state["current_hp"] -= damage
        player_buffs["defense_down"] = 2
        print(f"{enemy['name']}使用破甲斬，造成 {damage} 傷害，你的防禦下降。")
        return
    element = "火" if enemy_id == "mon_cinder_bat" else "物理"
    damage = calc_enemy_damage(enemy, state, 1.0, element, player_buffs, defending)
    state["current_hp"] -= damage
    print(f"{enemy['name']}攻擊，造成 {damage} 傷害。")

def boss_glen_action(
    enemy: dict,
    enemy_hp: int,
    state: dict,
    player_buffs: dict,
    enemy_buffs: dict,
    defending: bool,
    turn: int,
    summoned: bool,
) -> bool:
    if not summoned and enemy_hp <= enemy["hp"] * 0.6:
        enemy_buffs["defense_up"] = 3
        print("葛倫吹響口哨，山寨手下在遠處吶喊。他的防禦上升。")
        return True
    if enemy_hp <= enemy["hp"] * 0.35:
        damage = calc_enemy_damage(enemy, state, 1.35, "物理", player_buffs, defending)
        state["current_hp"] -= damage
        player_buffs["defense_down"] = 2
        print(f"葛倫使出破甲重擊，造成 {damage} 傷害，你的防禦下降。")
        return summoned
    if turn % 3 == 0:
        damage = calc_enemy_damage(enemy, state, 1.15, "火", player_buffs, defending)
        state["current_hp"] -= damage
        print(f"葛倫砸出火油瓶，造成 {damage} 火傷害。")
        if random.random() < 0.25:
            player_buffs["burn"] = 3
            print("你陷入灼傷。")
        return summoned
    damage = calc_enemy_damage(enemy, state, 1.0, "物理", player_buffs, defending)
    state["current_hp"] -= damage
    print(f"葛倫粗暴斬擊，造成 {damage} 傷害。")
    return summoned

def boss_ash_guardian_action(
    enemy: dict,
    enemy_hp: int,
    state: dict,
    player_buffs: dict,
    enemy_buffs: dict,
    defending: bool,
    turn: int,
    charged: bool,
) -> bool:
    if charged:
        damage = calc_enemy_damage(enemy, state, 1.35, "火", player_buffs, defending)
        state["current_hp"] -= damage
        print(f"{enemy['name']}釋放爐心蓄熱，熔火爆裂造成 {damage} 火傷害。")
        if random.random() < 0.2:
            player_buffs["burn"] = 3
            print("你陷入灼傷。")
        return False
    if enemy_hp <= enemy["hp"] * 0.45 and turn % 3 == 1:
        print(f"{enemy['name']}胸口的爐心開始發亮，下一擊會很危險。")
        return True
    if turn % 4 == 0:
        enemy_buffs["defense_up"] = 2
        print(f"{enemy['name']}收攏灰燼甲片，防禦上升。")
        return charged
    if turn % 2 == 0:
        damage = calc_enemy_damage(enemy, state, 1.1, "火", player_buffs, defending)
        state["current_hp"] -= damage
        print(f"{enemy['name']}揮出火舌掃擊，造成 {damage} 火傷害。")
        return charged
    damage = calc_enemy_damage(enemy, state, 1.0, "物理", player_buffs, defending)
    state["current_hp"] -= damage
    print(f"{enemy['name']}以沉重石臂砸下，造成 {damage} 傷害。")
    return charged

def boss_cinder_seal_sentinel_action(
    enemy: dict,
    enemy_hp: int,
    state: dict,
    player_buffs: dict,
    enemy_buffs: dict,
    defending: bool,
    turn: int,
    charged: bool,
) -> bool:
    if charged:
        damage = calc_enemy_damage(enemy, state, 1.4, "火", player_buffs, defending)
        state["current_hp"] -= damage
        print(f"{enemy['name']}將燼印壓入地面，赤焰衝擊造成 {damage} 火傷害。")
        if random.random() < 0.25:
            player_buffs["burn"] = 3
            print("你陷入灼傷。")
        return False
    if enemy_hp <= enemy["hp"] * 0.5 and turn % 3 == 1:
        print(f"{enemy['name']}胸口的燼印亮起，下一擊正在蓄勢。")
        return True
    if turn % 4 == 0:
        enemy_buffs["defense_up"] = 2
        print(f"{enemy['name']}收束熔殼，防禦上升。")
        return charged
    if turn % 2 == 0:
        damage = calc_enemy_damage(enemy, state, 1.05, "物理", player_buffs, defending)
        state["current_hp"] -= damage
        player_buffs["defense_down"] = 2
        print(f"{enemy['name']}以刻印長槍貫擊，造成 {damage} 傷害，你的防禦下降。")
        return charged
    damage = calc_enemy_damage(enemy, state, 1.1, "火", player_buffs, defending)
    state["current_hp"] -= damage
    print(f"{enemy['name']}揮出燼火斬，造成 {damage} 火傷害。")
    return charged

def tick_effects(state: dict, player_buffs: dict, enemy_buffs: dict) -> None:
    if state.pop("_clear_burn", False):
        player_buffs.pop("burn", None)
    if player_buffs.get("burn", 0) > 0:
        damage = max(1, math.ceil(get_stats(state)["max_hp"] * 0.05))
        state["current_hp"] -= damage
        print(f"灼傷造成 {damage} 傷害。")
    for buffs in (player_buffs, enemy_buffs):
        expired = []
        for key in list(buffs.keys()):
            buffs[key] -= 1
            if buffs[key] <= 0:
                expired.append(key)
        for key in expired:
            del buffs[key]

def main_loop(state: dict) -> None:
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
            town_menu(state)
        elif choice == 3:
            dungeon_menu(state)
        elif choice == 4:
            bestiary_menu(state)
        elif choice == 5:
            backpack_menu(state, allow_storage=False)
        elif choice == 6:
            save_game(state)
            pause()
        elif choice == 7:
            raw = input("離開前要存檔嗎？(y/n) > ").strip().lower()
            if raw == "y":
                save_game(state)
            print("下次再回艾爾姆。")
            return

def smoke_test() -> None:
    state = create_state("測試者", "劍士")
    assert state["current_hp"] == 120
    assert state["storage_unlocked"] is False
    assert state["storage"] == {}
    assert state["bestiary"] == []
    legacy_state = {"inventory": {}}
    ensure_state_defaults(legacy_state)
    assert legacy_state["flags"] == {}
    assert legacy_state["storage_unlocked"] is False
    assert legacy_state["storage"] == {}
    assert legacy_state["bestiary"] == []
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
    print("smoke test ok")

def main() -> None:
    setup_console()
    if "--smoke-test" in sys.argv:
        smoke_test()
        return

    state = None
    if SAVE_PATH.exists():
        choice = save_prompt_panel()
        if choice == 1:
            state = load_game()
    if state is None:
        state = new_game()
    main_loop(state)
