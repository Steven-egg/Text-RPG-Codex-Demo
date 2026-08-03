from __future__ import annotations

import math
import random
from typing import Any

from data import (
    DUNGEONS,
    EQUIPMENT,
    MONSTERS,
    EVENT_WEIGHTS,
    QUESTS,
    say,
)
from .formatting import item_name
from .display import action_menu_panel, render_panel, pause
from .story_beats import boss_story_beat_id, show_story_beat, take_story_beat
from .state import (
    is_key_item,
    is_unlocked,
    unlock,
    player_facing_dungeon_ids,
    get_stats,
    clamp_vitals,
    player_summary_line,
    remove_item,
    add_item,
    quest_unlocked,
    boss_defeated,
    FINAL_QUEST_ID,
    add_gold,
    add_loot,
    configure_run_supplies,
    RUN_SUPPLY_THROW_ITEMS,
    item_job_allowed,
    grant_quality_equipment,
    quality_equipment_candidates,
)
from .equipment_quality import BOSS_QUALITY, QUALITY_LABELS, supports_quality_job
from .facilities import (
    BOSS_GLEN_SIGHTED_FLAG,
    BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG,
    MAIN_STORY_CLEARED_FLAG,
    next_step_hint,
)
from .cli_helpers import (
    DUNGEON_TREASURE_CONFIG,
    DUNGEON_TRAP_CONFIG,
    DUNGEON_SPECIAL_CONFIG,
)

BOSS_REQUIRED_QUESTS = {
    "boss_ice_outer_gatewarden": "quest_ice_main_phase_1",
    "boss_ice_final_seal_lord": "quest_ice_main_phase_2",
    "boss_earth_outer_grovekeeper": "quest_earth_main_phase_1",
    "boss_earth_deep_leyline_lord": "quest_earth_main_phase_2",
    "boss_thunder_lower_array_warden": "quest_thunder_main_phase_1",
    "boss_thunder_crown_storm_lord": "quest_thunder_main_phase_2",
    "boss_final_echo_warden": "quest_final_main_phase_1",
    "boss_final_seal_core": "quest_final_main_phase_2",
    "boss_final_demon_king": FINAL_QUEST_ID,
}

BOSS_FREE_CHALLENGE = {
    "boss_ice_wreck_captain",
    "boss_ice_frostroot_keeper",
    "boss_earth_rootwarden",
    "boss_earth_quarry_colossus",
    "boss_thunder_plateau_beacon",
    "boss_thunder_channel_keeper",
    "boss_final_echo_vanguard",
    "boss_final_ruin_jailer",
}


def run_loot_summary(run_log: dict) -> str:
    item_lines = [f"{item_name(item_id)} x{qty}" for item_id, qty in sorted(run_log.get("items", {}).items())]
    item_text = "、".join(item_lines) if item_lines else "無"
    return f"本趟收益：{run_log.get('gold', 0)}G / 物品：{item_text}"


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


def record_boss_glen_sighting(state: dict) -> bool:
    flags = state.setdefault("flags", {})
    if flags.get("boss_glen_defeated") or flags.get(BOSS_GLEN_SIGHTED_FLAG):
        return False
    flags[BOSS_GLEN_SIGHTED_FLAG] = True
    return True


def activate_boss_glen_investigation(state: dict) -> bool:
    """Auto-accept Glen's investigation at the mine endpoint.

    This also upgrades legacy saves which have only the former sighting flag.
    """
    flags = state.setdefault("flags", {})
    if flags.get("boss_glen_defeated"):
        return False
    flags[BOSS_GLEN_SIGHTED_FLAG] = True
    if flags.get(BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG):
        return False
    flags[BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG] = True
    return True


def choose_weighted_event() -> str:
    total = sum(weight for _, weight in EVENT_WEIGHTS)
    roll = random.randint(1, total)
    current = 0
    for event, weight in EVENT_WEIGHTS:
        current += weight
        if roll <= current:
            return event
    return "empty"


def dungeon_menu(state: dict, region_id: str = "border_fire") -> None:
    unlocked_dungeons = player_facing_dungeon_ids(state, region_id)
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
    if not configure_cli_run_supplies(state):
        return
    explore_dungeon(state, unlocked_dungeons[choice - 1])


def configure_cli_run_supplies(state: dict) -> bool:
    """Small CLI preparation step; unused inventory remains untouched."""
    inventory = state.get("inventory", {})
    def choose(label: str, allowed: tuple[str, ...], cap: int) -> dict:
        available = [item_id for item_id in allowed if inventory.get(item_id, 0) > 0]
        if not available or cap == 0:
            return {}
        print(f"{label}：" + " / ".join(f"{item_name(item_id)} x{inventory[item_id]}" for item_id in available))
        if len(available) > 1:
            raw_item = input("輸入 1 選第一項、2 選第二項（留白不帶）> ").strip()
            if raw_item not in {"1", "2"}:
                return {}
            item_id = available[int(raw_item) - 1]
        else:
            item_id = available[0]
        raw = input(f"輸入數量 0-{min(cap, inventory[item_id])}（0 不帶）> ").strip()
        try:
            quantity = int(raw or "0")
        except ValueError:
            print("數量格式錯誤。")
            return {}
        if quantity <= 0:
            return {}
        return {"item_id": item_id, "quantity": quantity}
    selections = {
        "sustain_hp": choose("續航 HP 格", ("item_potion_s",), 3),
        "emergency_hp": choose("保險 HP 格", ("item_potion_s", "item_ice_potion_01", "item_earth_potion_01", "item_thunder_potion_01", "item_final_potion_01"), 1),
        "mp": choose("MP 格", ("item_focus_drop", "item_ice_potion_02", "item_earth_potion_02", "item_thunder_potion_02", "item_final_potion_02"), 1 if state.get("job") in {"戰士", "盜賊"} else 2),
        "throwable": choose(
            "投擲格",
            tuple(item_id for item_id in RUN_SUPPLY_THROW_ITEMS if item_job_allowed(state, item_id)),
            2,
        ),
    }
    try:
        configure_run_supplies(state, selections)
    except ValueError as error:
        print(f"補給配置失敗：{error}")
        pause()
        return False
    return True


def boss_available_at_dungeon_end(state: dict, dungeon_id: str, boss_id: str | None) -> bool:
    if boss_id == "boss_glen":
        return (
            dungeon_id == "dungeon_scorched_mine"
            and state["flags"].get(BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG, False)
            and not state["flags"].get("boss_glen_defeated")
        )
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
    if boss_id in BOSS_FREE_CHALLENGE:
        return not boss_defeated(state, boss_id)
    required_quest = BOSS_REQUIRED_QUESTS.get(boss_id)
    if required_quest:
        return (
            quest_unlocked(state, required_quest)
            and not boss_defeated(state, boss_id)
        )
    return False


def boss_challenge_prompt(boss_id: str) -> str:
    if boss_id == "boss_ash_guardian":
        return "裂谷深處的灰燼凝成古老守衛。要挑戰灰燼守衛嗎？(y/n) > "
    if boss_id == "boss_cinder_seal_sentinel":
        return "燼印深窟的最底層浮現赤紅刻印。要挑戰燼印鎮衛嗎？(y/n) > "
    return "礦坑深處傳來粗暴的笑聲。要挑戰 Boss 嗎？(y/n) > "


def clear_dungeon_boss(state: dict, boss_id: str, run_log: dict) -> dict[str, Any] | None:
    from .cli_helpers import BOSS_CLEAR_DATA
    if boss_id not in BOSS_CLEAR_DATA:
        return None

    data = BOSS_CLEAR_DATA[boss_id]
    defeated_flag = data["defeated_flag"]
    if state["flags"].get(defeated_flag):
        return None

    state["flags"][defeated_flag] = True

    # Extra Flags
    for flag_key, flag_val in data.get("extra_flags", {}).items():
        state["flags"][flag_key] = flag_val

    # Unlocks
    for dungeon_to_unlock in data.get("unlocks", []):
        unlock(state, dungeon_to_unlock)

    # Loot
    for item_id, qty in data.get("loot", []):
        add_loot(state, item_id, qty, run_log)

    quality = BOSS_QUALITY.get(boss_id)
    if quality:
        region_id = (
            "border_fire" if boss_id in {"boss_glen", "boss_ash_guardian", "boss_cinder_seal_sentinel"}
            else "final" if boss_id.startswith("boss_final_")
            else boss_id.split("_")[1]
        )
        candidates = quality_equipment_candidates(state, region_id)
        if candidates:
            reference_id = grant_quality_equipment(state, random.choice(candidates), quality)
            state.setdefault("_quality_reward_messages", []).append(
                f"獲得 {QUALITY_LABELS[quality]}品質裝備（{reference_id}）。"
            )

    # Special Action
    if data.get("special_action") == "demon_king_ending":
        state["flags"][MAIN_STORY_CLEARED_FLAG] = True
        complete_final_quest_from_boss(state)
        state["_ending_pending"] = True

    # Messages
    messages = data.get("messages", [])
    if messages:
        print(f"\n{messages[0]}")
        for msg in messages[1:]:
            print(msg)
    return take_story_beat(state, boss_story_beat_id(boss_id, "after"))


def explore_dungeon(state: dict, dungeon_id: str) -> None:
    from .game import combat
    dungeon = DUNGEONS[dungeon_id]
    run_log = {"gold": 0, "items": {}, "dungeon_id": dungeon_id}
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
    if dungeon_id == "dungeon_scorched_mine" and boss_id == "boss_glen":
        if activate_boss_glen_investigation(state):
            print(f"\n你在{dungeon['name']}深處發現了{MONSTERS[boss_id]['name']}。調查已自動承接，可立刻挑戰。")
            show_story_beat(take_story_beat(state, "boss.before.boss_glen"))
    if boss_available_at_dungeon_end(state, dungeon_id, boss_id):
        show_story_beat(take_story_beat(state, boss_story_beat_id(boss_id, "before")))
        raw = input(boss_challenge_prompt(boss_id)).strip().lower()
        if raw == "y":
            result = combat(state, boss_id, boss=True, run_log=run_log)
            if result is False:
                handle_defeat(state, run_log)
                return
            if result is True:
                show_story_beat(clear_dungeon_boss(state, boss_id, run_log))
                if state.pop("_ending_pending", False):
                    show_main_story_ending(state)
                    state["_return_to_title"] = True
                    return
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
    print(say("dungeon.event.material", item_name=item_name(item_id), qty=qty))


def dungeon_treasure_event(state: dict, dungeon: dict, run_log: dict) -> None:
    if random.random() < DUNGEON_TREASURE_CONFIG["gold_chance"]:
        gold = random.randint(*dungeon["gold_range"])
        add_gold(state, gold, run_log)
        print(say("dungeon.event.treasure_gold", gold=gold))
    else:
        item_id = random.choice(DUNGEON_TREASURE_CONFIG["fallback_items"])
        add_loot(state, item_id, 1, run_log)
        print(say("dungeon.event.treasure_item", item_name=item_name(item_id)))


def dungeon_trap_event(state: dict, dungeon: dict) -> None:
    stats = get_stats(state)
    dodge = min(DUNGEON_TRAP_CONFIG["max_dodge_chance"], stats["agility"] * 2 + stats.get("trap_evasion", 0))
    if random.randint(1, 100) <= dodge:
        print(say("dungeon.event.trap_dodge"))
        return
    if dungeon["element"] == "火":
        damage = math.ceil(DUNGEON_TRAP_CONFIG["fire_base_damage"] * (1 - stats["fire_resist"] / 100))
        state["current_hp"] -= damage
        print(say(DUNGEON_TRAP_CONFIG["fire_msg_key"], damage=damage))
    else:
        damage = DUNGEON_TRAP_CONFIG["default_damage"]
        state["current_hp"] -= damage
        print(say(DUNGEON_TRAP_CONFIG["default_msg_key"], damage=damage))


def dungeon_special_event(state: dict, dungeon_id: str, run_log: dict) -> None:
    cfg = DUNGEON_SPECIAL_CONFIG.get(dungeon_id, DUNGEON_SPECIAL_CONFIG["default"])
    print(say(cfg["msg_main_key"]))
    if cfg["chance"] >= 1.0:
        add_loot(state, cfg["loot_item"], cfg["loot_qty"], run_log)
        if cfg["msg_loot_key"]:
            print(say(cfg["msg_loot_key"]))
    else:
        if random.random() < cfg["chance"]:
            add_loot(state, cfg["loot_item"], cfg["loot_qty"], run_log)
            if cfg["msg_loot_key"]:
                print(say(cfg["msg_loot_key"]))


def handle_defeat(state: dict, run_log: dict) -> None:
    lost_gold = math.ceil(run_log.get("gold", 0) * 0.5)
    state["gold"] = max(0, state["gold"] - lost_gold)
    lost_items = []
    for item_id, qty in run_log.get("items", {}).items():
        if is_key_item(item_id) or item_id in EQUIPMENT:
            continue
        lose_qty = math.ceil(qty * 0.5)
        if lose_qty > 0 and state["inventory"].get(item_id, 0) > 0:
            actual = min(lose_qty, state["inventory"].get(item_id, 0))
            remove_item(state, item_id, actual)
            lost_items.append(f"{item_name(item_id)} x{actual}")
    stats = get_stats(state)
    state["current_hp"] = max(1, math.ceil(stats["max_hp"] * 0.25))
    state["current_mp"] = math.ceil(stats["max_mp"] * 0.25)
    result_lines = [
        "工會救援隊把你帶回艾爾姆。",
        f"失去本趟金幣 {lost_gold}G。",
        "散落素材：" + "、".join(lost_items) if lost_items else "素材大致都保住了。",
        f"回城後 HP {state['current_hp']}/{stats['max_hp']} / MP {state['current_mp']}/{stats['max_mp']}",
        next_step_hint(state),
    ]
    render_panel("戰鬥失敗 / 回城結算", result_lines, border_style="red")
    pause()


def complete_final_quest_from_boss(state: dict) -> None:
    if FINAL_QUEST_ID in state["completed_quests"]:
        return
    quest = QUESTS[FINAL_QUEST_ID]
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
    state["completed_quests"].append(FINAL_QUEST_ID)
    print(f"Final Q5 completed. Guild reputation +{guild_gain}.")


def show_main_story_ending(state: dict) -> None:
    show_story_beat(
        take_story_beat(
            state,
            "ending.main_story_clear",
            context={"player": state.get("name", "見習冒險者")},
        )
    )
    pause()
    render_panel(
        "MAIN STORY CLEAR",
        [
            f"Clear adventurer: {state['name']} / {state['job']} Lv{state['level']}",
            f"Guild reputation: {state['guild_points']}",
            "This clear state is not saved automatically.",
            "Returning to title screen.",
        ],
        border_style="green",
    )
    pause()
