from __future__ import annotations

import json
import math
import os
import random
import sys
from copy import deepcopy
from pathlib import Path

from data import (
    DUNGEONS,
    EQUIPMENT,
    EVENT_WEIGHTS,
    ITEMS,
    JOBS,
    MAGIC_BOOKS,
    MATERIALS,
    MONSTERS,
    PROMOTIONS,
    QUESTS,
    RECIPES,
    RELICS,
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

def setup_console() -> None:
    if os.name == "nt":
        os.system("chcp 65001 > nul")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    except Exception:
        pass

def item_name(item_id: str) -> str:
    if item_id in ITEMS:
        return ITEMS[item_id]["name"]
    if item_id in EQUIPMENT:
        return EQUIPMENT[item_id]["name"]
    if item_id in MATERIALS:
        return MATERIALS[item_id]
    return item_id

def is_key_item(item_id: str) -> bool:
    return item_id.startswith("key_")

def pause() -> None:
    input("\n按 Enter 繼續...")

def title(text: str) -> None:
    print("\n" + "=" * 56)
    print(text)
    print("=" * 56)

def menu(prompt: str, options: list[str], allow_back: bool = True) -> int:
    print()
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    if allow_back:
        print("0. 返回")
    while True:
        raw = input(f"{prompt} > ").strip()
        if allow_back and raw == "0":
            return 0
        if raw.isdigit():
            choice = int(raw)
            if 1 <= choice <= len(options):
                return choice
        print("請輸入列表中的數字。")

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

def format_items(cost: dict) -> str:
    if not cost:
        return "無"
    parts = []
    for item_id, qty in cost.items():
        if item_id.startswith("flag:"):
            flag = item_id.split(":", 1)[1]
            flag_names = {"boss_glen_defeated": "擊敗山寨頭目葛倫"}
            parts.append(flag_names.get(flag, flag))
        else:
            parts.append(f"{item_name(item_id)} x{qty}")
    return "、".join(parts)

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
    stats = get_stats(state)
    title(f"{state['name']} / {state['job']} Lv{state['level']}")
    print(f"HP {state['current_hp']}/{stats['max_hp']}  MP {state['current_mp']}/{stats['max_mp']}")
    print(f"金幣 {state['gold']}G  工會積分 {state['guild_points']}")
    print(
        f"攻擊 {stats['attack']}  魔攻 {stats['magic_attack']}  防禦 {stats['defense']}  "
        f"敏捷 {stats['agility']}  命中 100%  暴擊 {stats['crit']}%  火抗 {stats['fire_resist']}%"
    )
    print(f"經驗 {state['exp']}/{exp_to_next(state['level'])}")
    print("\n裝備")
    slot_names = {"weapon": "武器", "head": "頭部", "body": "身體", "accessory": "飾品", "special": "特殊"}
    for slot, label in slot_names.items():
        item_id = state["equipment"].get(slot)
        print(f"- {label}: {item_name(item_id) if item_id else '無'}")
    print("\n技能")
    for skill_id in state["learned_skills"]:
        skill = SKILLS[skill_id]
        print(f"- {skill['name']} / MP {skill['mp']}: {skill['desc']}")

def show_inventory(state: dict) -> None:
    title("背包與素材")
    if not state["inventory"]:
        print("背包目前是空的。")
        return
    for item_id, qty in sorted(state["inventory"].items(), key=lambda pair: item_name(pair[0])):
        print(f"- {item_name(item_id)} x{qty}")

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
        title("裝備管理")
        for slot, item_id in state["equipment"].items():
            print(f"{slot}: {item_name(item_id) if item_id else '無'}")
        if not equippables:
            print("\n背包裡沒有可裝備物品。")
            pause()
            return
        options = [f"{item_name(item_id)} - {equipment_summary(item_id)}" for item_id in equippables]
        choice = menu("選擇要裝備的物品", options)
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
        title(shop_name)
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
            print("目前沒有可購買商品。")
            pause()
            return
        print(f"持有金幣：{state['gold']}G")
        choice = menu("選擇商品", options)
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
        title("星燈魔法商店")
        print("伊芙輕輕敲了敲書脊：「買下的不是紙，是你以後能做出的選擇。」")
        print(f"持有金幣：{state['gold']}G")
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
        choice = menu("選擇要學習的魔法書", options)
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
        title(title_text)
        available = [recipe_id for recipe_id in recipe_ids if recipe_available(state, recipe_id)]
        if not available:
            print("目前沒有可用配方。")
            pause()
            return
        print(f"持有金幣：{state['gold']}G")
        options = []
        for recipe_id in available:
            recipe = RECIPES[recipe_id]
            base = f"，消耗 {item_name(recipe['base_item'])}" if recipe.get("base_item") else ""
            options.append(
                f"{recipe['name']} / {recipe['gold']}G / {format_items(recipe['materials'])}{base} / {recipe['desc']}"
            )
        choice = menu("選擇配方", options)
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
    previews = [
        relic
        for relic in RELICS.values()
        if relic.get("status") == "preview"
    ]
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
        title("邊境城鎮艾爾姆")
        options = [
            "冒險者工會",
            "鐵刃工坊",
            "堅甲工坊",
            "旅人小鋪",
            "米菈合成屋",
            "星燈魔法商店",
            "轉職神殿",
            "聖物調查",
            "倉庫/背包",
            "旅館休息 30G",
        ]
        choice = menu("你要去哪裡", options)
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
            backpack_menu(state, allow_storage=True)
        elif choice == 10:
            rest_inn(state)

def iron_workshop(state: dict) -> None:
    while True:
        title("鐵刃工坊")
        print("葛雷抬眼看你：「好武器不能替你冒險，但能讓怪物少活幾回合。」")
        choice = menu("鐵刃工坊", ["購買武器", "強化武器"])
        if choice == 0:
            return
        if choice == 1:
            buy_menu(state, "鐵刃工坊 - 武器", SHOP_INVENTORY["weapon"])
        elif choice == 2:
            craft_menu(state, "鐵刃工坊 - 強化", ["recipe_iron_sword_plus_1"])

def armor_workshop(state: dict) -> None:
    while True:
        title("堅甲工坊")
        print("布琳把皮甲翻到內側：「能活著回來，才有下一次委託。」")
        choice = menu("堅甲工坊", ["購買防具", "強化防具"])
        if choice == 0:
            return
        if choice == 1:
            buy_menu(state, "堅甲工坊 - 防具", SHOP_INVENTORY["armor"])
        elif choice == 2:
            craft_menu(state, "堅甲工坊 - 強化", ["recipe_leather_armor_plus_1"])

def rest_inn(state: dict) -> None:
    stats = get_stats(state)
    if state["gold"] < 30:
        print("旅館老闆搖搖頭：「先去工會看看有沒有簡單委託吧。」")
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
        title("倉庫")
        print(f"工會旁的小倉庫還沒整理好。開啟 LV1 倉庫需要 {STORAGE_UNLOCK_COST}G。")
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
        title("倉庫 LV1")
        print(f"容量：{storage_kind_count(state)}/{STORAGE_CAPACITY} 種物品。")
        choice = menu("選擇動作", ["查看倉庫", "存入物品", "取出物品"])
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
    title("倉庫內容")
    if not state["storage"]:
        print("倉庫目前是空的。")
        return
    for item_id, qty in state["storage"].items():
        print(f"- {item_name(item_id)} x{qty}")

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

    choice = menu("選擇要存入的物品", options)
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
    choice = menu("選擇要取出的物品", options)
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

def monster_locations(monster_id: str) -> list[str]:
    locations = []
    for dungeon in DUNGEONS.values():
        if monster_id in dungeon.get("monsters", []) or dungeon.get("boss") == monster_id:
            locations.append(dungeon["name"])
    return locations

def monster_drop_names(monster: dict) -> str:
    drops = [item_name(item_id) for item_id, _chance, _qty in monster["drops"]]
    return "、".join(drops) if drops else "無"

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
        title("倉庫/背包")
        options = ["查看背包", "裝備管理"]
        if allow_storage:
            options.append("倉庫")
        options.append("查看狀態")
        choice = menu("選擇動作", options)
        if choice == 0:
            return
        if choice == 1:
            show_inventory(state)
            pause()
        elif choice == 2:
            equipment_menu(state)
        elif allow_storage and choice == 3:
            storage_menu(state)
        elif choice == len(options):
            show_status(state)
            pause()

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
    return False

def quest_ready(state: dict, quest_id: str) -> bool:
    if quest_id in state["completed_quests"]:
        return False
    return can_pay_items(state, QUESTS[quest_id]["turn_in"])

def guild_menu(state: dict) -> None:
    while True:
        title("冒險者工會")
        print("諾亞翻開任務冊：「今天也讓背包比出門時重一點吧。」")
        choice = menu("選擇服務", ["查看委託任務", "收購素材"])
        if choice == 0:
            return
        if choice == 1:
            guild_quest_menu(state)
        elif choice == 2:
            guild_material_buy_menu(state)

def guild_quest_menu(state: dict) -> None:
    while True:
        title("冒險者工會")
        print("諾亞翻開任務冊：「今天也讓背包比出門時重一點吧。」")
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
        choice = menu("選擇任務", options)
        if choice == 0:
            return
        quest_id = quest_ids[choice - 1]
        show_or_complete_quest(state, quest_id)
        pause()

def guild_material_buy_menu(state: dict) -> None:
    while True:
        title("工會收購素材")
        print("諾亞推來一只木箱：「只收登記過的可重複素材，劇情物品我可不敢碰。」")
        buyable_ids = [
            item_id
            for item_id in GUILD_MATERIAL_BUY_PRICES
            if state["inventory"].get(item_id, 0) > 0
        ]
        if not buyable_ids:
            print("背包裡沒有工會目前收購的素材。")
            pause()
            return

        options = []
        for item_id in buyable_ids:
            qty = state["inventory"][item_id]
            price = GUILD_MATERIAL_BUY_PRICES[item_id]
            options.append(f"{item_name(item_id)} x{qty} / 單價 {price}G")

        choice = menu("選擇要出售的素材", options)
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


def temple(state: dict) -> None:
    title("轉職神殿")
    print("賽恩站在門前，像一塊懂得呼吸的石碑。")
    if state["flags"].get("boss_glen_defeated"):
        print("賽恩看著你手中的火之印記碎片：")
        print("「這還不是完整的印記。但神殿記得它的溫度。等你集齊三枚元素核心，再回來敲這扇門。」")
    print()
    print(f"目前職業：{state['job']}")
    previews = [
        promotion
        for promotion in PROMOTIONS.values()
        if promotion.get("source_job") == state["job"] and promotion.get("status") == "preview"
    ]
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
    unlocked_dungeons = [dungeon_id for dungeon_id, d in DUNGEONS.items() if is_unlocked(state, d["unlock"])]
    if not unlocked_dungeons:
        print("目前沒有可探索的迷宮。")
        pause()
        return
    title("迷宮探索")
    options = []
    for dungeon_id in unlocked_dungeons:
        dungeon = DUNGEONS[dungeon_id]
        clear = "已通關" if dungeon_id in state["cleared_dungeons"] else "未通關"
        options.append(f"{dungeon['name']} / 推薦 {dungeon['recommended']} / {dungeon['steps']} 步 / {clear}")
    choice = menu("選擇迷宮", options)
    if choice == 0:
        return
    explore_dungeon(state, unlocked_dungeons[choice - 1])

def explore_dungeon(state: dict, dungeon_id: str) -> None:
    dungeon = DUNGEONS[dungeon_id]
    run_log = {"gold": 0, "items": {}}
    title(dungeon["name"])
    print(f"推薦等級：{dungeon['recommended']}  主要屬性：{dungeon['element']}")
    if state["equipment"].get("special") == "special_focus_pouch":
        add_loot(state, "item_focus_drop", 1, run_log)
        print("集中藥袋發出微光，你在出發前多整理出一瓶集中滴露。")
    for step in range(1, dungeon["steps"] + 1):
        clamp_vitals(state)
        stats = get_stats(state)
        if state["current_hp"] <= 0:
            handle_defeat(state, run_log)
            return
        print(f"\n第 {step}/{dungeon['steps']} 步  HP {state['current_hp']}/{stats['max_hp']}  MP {state['current_mp']}/{stats['max_mp']}")
        raw = input("按 Enter 前進，輸入 r 撤退 > ").strip().lower()
        if raw == "r":
            print("你帶著本趟收穫返回城鎮。")
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
    if boss_id and not state["flags"].get("boss_glen_defeated"):
        raw = input("礦坑深處傳來粗暴的笑聲。要挑戰 Boss 嗎？(y/n) > ").strip().lower()
        if raw == "y":
            result = combat(state, boss_id, boss=True, run_log=run_log)
            if result is False:
                handle_defeat(state, run_log)
                return
            if result is True:
                clear_boss_glen(state, run_log)
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
    title("戰鬥失敗")
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
    print("工會救援隊把你帶回艾爾姆。")
    print(f"失去本趟金幣 {lost_gold}G。")
    if lost_items:
        print("散落素材：" + "、".join(lost_items))
    else:
        print("素材大致都保住了。")
    pause()

def clear_boss_glen(state: dict, run_log: dict) -> None:
    state["flags"]["boss_glen_defeated"] = True
    add_loot(state, "key_blood_map", 1, run_log)
    add_loot(state, "key_fire_mark_shard", 1, run_log)
    add_loot(state, "mat_lava_shard", 2, run_log)
    print("\n葛倫倒下時，懷裡掉出一張染血地圖。")
    print("取得 血跡地圖 x1、火之印記碎片 x1、熔岩碎片 x2。")

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
    summoned = False
    title(f"遭遇 {enemy['name']}")
    while enemy_hp > 0 and state["current_hp"] > 0:
        clamp_vitals(state)
        stats = get_stats(state, player_buffs)
        print(f"\n回合 {turn}")
        print(f"{state['name']} HP {state['current_hp']}/{stats['max_hp']} MP {state['current_mp']}/{stats['max_mp']}")
        print(f"{enemy['name']} HP {enemy_hp}/{enemy['hp']}")

        options = ["攻擊", "防禦", "技能", "道具"]
        if not boss:
            options.append("逃跑")
        choice = menu("戰鬥指令", options, allow_back=False)
        defending = False
        escaped = False

        if choice == 1:
            escaped = player_attack(state, enemy, enemy_hp, None, player_buffs, enemy_buffs)
            if isinstance(escaped, int):
                enemy_hp -= escaped
        elif choice == 2:
            defending = True
            if player_buffs.get("defense_up", 0) > 0:
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
            summoned = boss_glen_action(enemy, enemy_hp, state, player_buffs, enemy_buffs, defending, turn, summoned)
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
        for item_id in ["item_potion_s", "item_focus_drop", "item_herb_antidote", "item_armor_piercer", "item_escape_scroll"]
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

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def main_loop(state: dict) -> None:
    while True:
        clamp_vitals(state)
        title("主選單")
        print(f"{state['name']} / {state['job']} Lv{state['level']} / {state['gold']}G")
        choice = menu("選擇行動", ["查看狀態", "返回城鎮整備", "進入迷宮探索", "怪物圖鑑", "背包/裝備", "存檔", "離開遊戲"], allow_back=False)
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
        title("找到存檔")
        choice = menu("要讀取舊存檔嗎", ["讀取存檔", "重新開始"], allow_back=False)
        if choice == 1:
            state = load_game()
    if state is None:
        state = new_game()
    main_loop(state)
