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
    RELICS,
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
    "mat_ice_salt": 32,
    "mat_ice_saltcloth": 36,
    "mat_ice_wreck_plank": 38,
    "mat_ice_frostroot": 40,
    "mat_ice_blue_stone": 44,
    "mat_ice_frostiron": 52,
    "mat_ice_seal_dust": 58,
    "mat_ice_deep_core": 72,
    "mat_earth_moss_loam": 76,
    "mat_earth_rootfiber": 82,
    "mat_earth_spore_cap": 84,
    "mat_earth_quarry_stone": 90,
    "mat_earth_petrified_bark": 96,
    "mat_earth_leyline_shard": 108,
    "mat_earth_seal_clay": 116,
    "mat_earth_deep_core": 132,
    "mat_thunder_charge_sand": 140,
    "mat_thunder_copper_vein": 148,
    "mat_thunder_stormglass": 154,
    "mat_thunder_sky_stone": 164,
    "mat_thunder_conductor_rod": 172,
    "mat_thunder_cloud_essence": 188,
    "mat_thunder_seal_spark": 202,
    "mat_thunder_deep_core": 226,
    "mat_final_echo_ash": 240,
    "mat_final_frost_memory": 248,
    "mat_final_root_stone": 256,
    "mat_final_storm_glass": 264,
    "mat_final_void_shard": 280,
    "mat_final_seal_core": 310,
    "mat_final_demon_core": 340,
    "mat_final_deep_essence": 360,
}

STORAGE_UNLOCK_COST = 500
STORAGE_CAPACITY = 10
SLEEVE_BLADE_FOLLOWUP_MULTIPLIER = 0.35
MAX_COMBAT_SUMMARY_LINES = 3
TRAVEL_SHOP_CATEGORIES = ["全部", "補給品", "戰術道具", "飾品"]
MAGIC_SHOP_CATEGORIES = ["全部", "攻擊魔法", "恢復魔法", "輔助魔法", "特殊魔法"]
SYNTHESIS_CATEGORIES = ["全部", "裝備", "戰術道具"]
FIRE_MARK_GUILD_INQUIRY_FLAG = "fire_mark_guild_inquiry_done"
FIRE_MARK_CHURCH_BRIDGE_FLAG = "fire_mark_church_bridge_done"
FIRE_MARK_CHURCH_LOOKUP_FLAG = "fire_mark_church_lookup_done"
BOSS_GLEN_SIGHTED_FLAG = "boss_glen_sighted"
BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG = "boss_glen_investigation_accepted"
FIRE_MARK_SHARD_ID = "key_fire_mark_shard"
ICE_REGION_UNLOCK = "unlock_ice_region"
ICE_PHASE_2_DUNGEON_ID = "dungeon_ice_main_phase_2"
EARTH_REGION_UNLOCK = "unlock_earth_region_preview"
EARTH_PHASE_2_DUNGEON_ID = "dungeon_earth_main_phase_2"
THUNDER_REGION_UNLOCK = "unlock_thunder_region_preview"
THUNDER_PHASE_2_DUNGEON_ID = "dungeon_thunder_main_phase_2"
FINAL_REGION_UNLOCK = "unlock_final_region_preview"
FINAL_PHASE_2_DUNGEON_ID = "dungeon_final_main_phase_2"
FINAL_PHASE_3_DUNGEON_ID = "dungeon_final_main_phase_3"
FINAL_QUEST_ID = "quest_final_demon_king"
MAIN_STORY_CLEARED_FLAG = "main_story_cleared"
ELEMENTAL_SEAL_FLAGS = (
    "fire_seal_enshrined",
    "ice_seal_enshrined",
    "earth_seal_enshrined",
    "thunder_seal_enshrined",
)

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

@dataclass
class CombatActionResult:
    damage: int = 0
    events: list[str] = field(default_factory=list)
    summary: list[str] = field(default_factory=list)
    outcome: str | None = None

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

def boss_clear_flag(boss_id: str | None) -> str | None:
    if not boss_id:
        return None
    return BOSS_CLEAR_FLAGS.get(boss_id)

def boss_defeated(state: dict, boss_id: str | None) -> bool:
    flag = boss_clear_flag(boss_id)
    return bool(flag and state.get("flags", {}).get(flag))

def player_facing_dungeon_ids(state: dict, region_id: str | None = None) -> list[str]:
    dungeon_ids = []
    allowed_dungeon_ids = None
    if region_id is not None and region_id in REGIONS:
        allowed_dungeon_ids = set(REGIONS[region_id]["dungeon_ids"])
    ice_phase_2_unlocked = is_unlocked(state, ICE_PHASE_2_DUNGEON_ID)
    earth_phase_2_unlocked = is_unlocked(state, EARTH_PHASE_2_DUNGEON_ID)
    thunder_phase_2_unlocked = is_unlocked(state, THUNDER_PHASE_2_DUNGEON_ID)
    final_phase_2_unlocked = is_unlocked(state, FINAL_PHASE_2_DUNGEON_ID)
    final_phase_3_unlocked = is_unlocked(state, FINAL_PHASE_3_DUNGEON_ID)
    for dungeon_id, dungeon in DUNGEONS.items():
        if allowed_dungeon_ids is not None and dungeon_id not in allowed_dungeon_ids:
            continue
        if dungeon_id == "dungeon_ice_main_phase_1" and ice_phase_2_unlocked:
            continue
        if dungeon_id == "dungeon_earth_main_phase_1" and earth_phase_2_unlocked:
            continue
        if dungeon_id == "dungeon_thunder_main_phase_1" and thunder_phase_2_unlocked:
            continue
        if dungeon_id == "dungeon_final_main_phase_1" and (final_phase_2_unlocked or final_phase_3_unlocked):
            continue
        if dungeon_id == "dungeon_final_main_phase_2" and final_phase_3_unlocked:
            continue
        if is_unlocked(state, dungeon.get("unlock")):
            dungeon_ids.append(dungeon_id)
    return dungeon_ids

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
    if state.get("flags", {}).get(MAIN_STORY_CLEARED_FLAG):
        return "Main story cleared. Save if you want to keep this clear file, or start a new run from the title screen."
    if can_ask_fire_mark_guild_inquiry(state):
        return "三枚火之印記碎片正在共鳴，回冒險者工會詢問諾亞。"
    if should_show_fire_mark_church_lookup(state):
        return "回轉職神殿詢問賽恩的查閱結果。"
    if should_show_fire_mark_church_bridge(state):
        return "帶著三枚火之印記碎片前往轉職神殿。"
    if ready_relic_names(state):
        return f"前往聖物調查台安置聖印：{ready_relic_names(state)[0]}。"
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
    if "quest_ice_main_phase_2" in state["completed_quests"] and "quest_ice_return_handoff" not in state["completed_quests"]:
        return "Return to the Guild and file the Ice seal handoff report."
    if "quest_earth_main_phase_2" in state["completed_quests"] and "quest_earth_return_handoff" not in state["completed_quests"]:
        return "Return to the Guild and file the Earth seal handoff report."
    if "quest_thunder_main_phase_2" in state["completed_quests"] and "quest_thunder_return_handoff" not in state["completed_quests"]:
        return "Return to the Guild and file the Thunder seal handoff report."
    if "quest_final_main_phase_2" in state["completed_quests"] and FINAL_QUEST_ID not in state["completed_quests"]:
        return "The Demon King's throne route is open. Enter the final phase and finish Q5."
    if "quest_final_main_phase_1" in state["completed_quests"] and "quest_final_main_phase_2" not in state["completed_quests"]:
        return "The final seal core is open. Defeat the Seal Core for Q4."
    if "quest_final_minor_b" in state["completed_quests"] and "quest_final_main_phase_1" not in state["completed_quests"]:
        return "The Demon King's Gate is open. Break the Elemental Echo Gate for Q3."
    if "quest_final_minor_a" in state["completed_quests"] and "quest_final_minor_b" not in state["completed_quests"]:
        return "Broken Seal Ruins is open. Gather final approach samples for Q2."
    if is_unlocked(state, FINAL_REGION_UNLOCK) and "quest_final_minor_a" not in state["completed_quests"]:
        return "Final region is open. Start with Echoing Frontline and prepare for the Demon King."
    if "quest_thunder_return_handoff" in state["completed_quests"] and not is_unlocked(state, FINAL_REGION_UNLOCK):
        return "四元素路線已回報。將四聖印安置到聖物調查台後，魔王城前線才會穩定開啟。"
    if "quest_thunder_main_phase_1" in state["completed_quests"] and "quest_thunder_main_phase_2" not in state["completed_quests"]:
        return "Lightning Tower crown route is open. Push to the Crown Array seal."
    if "quest_thunder_minor_b" in state["completed_quests"] and "quest_thunder_main_phase_1" not in state["completed_quests"]:
        return "Lightning Tower lower array is open. Defeat the Warden for Q3."
    if "quest_thunder_minor_a" in state["completed_quests"] and "quest_thunder_minor_b" not in state["completed_quests"]:
        return "Conductive Channel is open. Gather the anomaly samples for Q2."
    if is_unlocked(state, THUNDER_REGION_UNLOCK) and "quest_thunder_minor_a" not in state["completed_quests"]:
        return "Thunder route is open. Start with Stormbreak Plateau and report Q1 samples."
    if "quest_earth_main_phase_1" in state["completed_quests"] and "quest_earth_main_phase_2" not in state["completed_quests"]:
        return "Leyline Grove deeper route is open. Push to the Deep Heart seal."
    if "quest_earth_minor_b" in state["completed_quests"] and "quest_earth_main_phase_1" not in state["completed_quests"]:
        return "Leyline Grove outer ring is open. Defeat the Grovekeeper for Q3."
    if "quest_earth_minor_a" in state["completed_quests"] and "quest_earth_minor_b" not in state["completed_quests"]:
        return "Old Quarry Vein is open. Gather the anomaly samples for Q2."
    if is_unlocked(state, EARTH_REGION_UNLOCK) and "quest_earth_minor_a" not in state["completed_quests"]:
        return "Earth route is open. Start with Rootfall Wildwood and report Q1 samples."
    if "quest_ice_main_phase_1" in state["completed_quests"] and "quest_ice_main_phase_2" not in state["completed_quests"]:
        return "霜鐵古城 deeper route is open. Push to the inner palace seal."
    if "quest_ice_minor_b" in state["completed_quests"] and "quest_ice_main_phase_1" not in state["completed_quests"]:
        return "霜鐵古城 outer city is open. Defeat the Gatewarden for Q3."
    if "quest_ice_minor_a" in state["completed_quests"] and "quest_ice_minor_b" not in state["completed_quests"]:
        return "霜根岩窟 is open. Gather the anomaly samples for Q2."
    if is_unlocked(state, ICE_REGION_UNLOCK) and "quest_ice_minor_a" not in state["completed_quests"]:
        return "Ice route is open. Start with 幽帆沉船 and report Q1 samples."
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

def travel_shop_category(item_id: str) -> str:
    if item_id in EQUIPMENT:
        return "飾品"
    kind = ITEMS.get(item_id, {}).get("kind")
    if kind == "consumable":
        return "補給品"
    if kind in {"battle", "special"}:
        return "戰術道具"
    return "其他"

def travel_shop_owned_count(state: dict, item_id: str) -> int:
    owned = state["inventory"].get(item_id, 0)
    if item_id in EQUIPMENT and item_id in state["equipment"].values():
        owned += 1
    return owned

def travel_shop_available_items(state: dict, category: str = "全部") -> list[str]:
    available = [item_id for item_id in SHOP_INVENTORY["travel"] if is_shop_item_available(state, item_id)]
    if category == "全部":
        return available
    return [item_id for item_id in available if travel_shop_category(item_id) == category]

def travel_shop_item_detail(item_id: str) -> str:
    data = ITEMS.get(item_id) or EQUIPMENT[item_id]
    if item_id in EQUIPMENT:
        return equipment_summary(item_id)
    return data.get("desc", "")

def travel_shop_item_line(state: dict, item_id: str) -> str:
    data = ITEMS.get(item_id) or EQUIPMENT[item_id]
    return (
        f"{item_name(item_id)} / {travel_shop_category(item_id)} / "
        f"持有 x{travel_shop_owned_count(state, item_id)} / {data['price']}G / "
        f"{travel_shop_item_detail(item_id)}"
    )

def travel_shop_detail_lines(state: dict, item_id: str) -> list[str]:
    data = ITEMS.get(item_id) or EQUIPMENT[item_id]
    lines = [
        f"商品：{item_name(item_id)}",
        f"分類：{travel_shop_category(item_id)}",
        f"持有：x{travel_shop_owned_count(state, item_id)}",
        f"價格：{data['price']}G",
        f"效果：{travel_shop_item_detail(item_id)}",
        f"目前金幣：{state['gold']}G",
    ]
    if item_id in EQUIPMENT:
        lines.append(f"可用職業：{','.join(EQUIPMENT[item_id]['jobs'])}")
        lines.append("購買後會放入背包；仍需到背包/裝備中替換。")
    return lines

def buy_travel_shop_item(state: dict, item_id: str) -> str:
    data = ITEMS.get(item_id) or EQUIPMENT[item_id]
    price = data["price"]
    if state["gold"] < price:
        return "金幣不足。"
    if item_id in EQUIPMENT and state["job"] not in EQUIPMENT[item_id]["jobs"]:
        return f"{state['job']}無法使用這件裝備，先別買比較好。"
    state["gold"] -= price
    add_item(state, item_id, 1)
    return f"購買了 {item_name(item_id)}。"

def travel_shop_item_menu(state: dict, category: str, region_id: str = "border_fire") -> None:
    while True:
        item_ids = travel_shop_available_items(state, category)
        facility_name = get_facility_display_name(region_id, "shop")
        if not item_ids:
            render_panel(
                f"{facility_name} - 商品清單",
                [f"分類：{category}", "目前此分類沒有可購買商品。"],
                border_style="green",
            )
            pause()
            return
        choice = action_menu_panel(
            "選擇商品",
            [travel_shop_item_line(state, item_id) for item_id in item_ids],
            f"{facility_name} - 商品清單",
            header_lines=[
                f"持有金幣：{state['gold']}G",
                f"分類：{category} / 可購買商品 {len(item_ids)} 種",
            ],
            hint_lines=["選擇商品可查看效果、持有數與購買確認。"],
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        item_id = item_ids[choice - 1]
        action = action_menu_panel(
            "商品操作",
            ["購買 1 個"],
            f"{facility_name} - 商品詳情",
            header_lines=travel_shop_detail_lines(state, item_id),
            allow_back=True,
            border_style="green",
        )
        if action == 0:
            continue
        result = buy_travel_shop_item(state, item_id)
        render_panel(
            f"{facility_name} - 購買結果",
            [result, f"目前金幣：{state['gold']}G", f"{item_name(item_id)} 持有：x{travel_shop_owned_count(state, item_id)}"],
            border_style="green",
        )
        pause()

def travel_shop(state: dict, region_id: str = "border_fire") -> None:
    while True:
        available = travel_shop_available_items(state)
        category_options = []
        for category in TRAVEL_SHOP_CATEGORIES:
            count = len(travel_shop_available_items(state, category))
            category_options.append(f"{category} / {count} 種商品")
        shop_title = f"{get_facility_display_name(region_id, 'shop')} - {get_npc_display_name(region_id, 'rabi')}"
        choice = action_menu_panel(
            "選擇分類",
            category_options,
            shop_title,
            header_lines=[
                get_dialogue(region_id, "shop", "welcome"),
                f"持有金幣：{state['gold']}G",
                f"可購買商品：{len(available)} 種",
            ],
            hint_lines=["補給品提高探索容錯；戰術道具能處理長戰鬥；飾品需購買後手動裝備。"],
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        travel_shop_item_menu(state, TRAVEL_SHOP_CATEGORIES[choice - 1], region_id)

def equipment_owned_count(state: dict, item_id: str) -> int:
    owned = state["inventory"].get(item_id, 0)
    if item_id in state["equipment"].values():
        owned += 1
    return owned

def equipment_status_line(state: dict, item_id: str) -> str:
    if item_id in state["equipment"].values():
        return "已裝備"
    if state["inventory"].get(item_id, 0) > 0:
        return f"背包 x{state['inventory'][item_id]}"
    return "未持有"

def equipment_job_status(state: dict, item_id: str) -> str:
    return "可用" if state["job"] in EQUIPMENT[item_id]["jobs"] else "目前職業不可用"

def workshop_item_line(state: dict, item_id: str) -> str:
    eq = EQUIPMENT[item_id]
    return (
        f"{eq['name']} / {equipment_job_status(state, item_id)} / "
        f"{equipment_status_line(state, item_id)} / {eq['price']}G / {equipment_summary(item_id)}"
    )

def workshop_item_detail_lines(state: dict, item_id: str) -> list[str]:
    eq = EQUIPMENT[item_id]
    slot_names = {"weapon": "武器", "head": "頭部", "body": "身體", "accessory": "飾品", "special": "特殊"}
    lines = [
        f"裝備：{eq['name']}",
        f"欄位：{slot_names.get(eq['slot'], eq['slot'])} / {eq['subtype']}",
        f"狀態：{equipment_status_line(state, item_id)}",
        f"可用職業：{','.join(eq['jobs'])}",
        f"目前職業：{state['job']}（{equipment_job_status(state, item_id)}）",
        f"價格：{eq['price']}G / 目前金幣：{state['gold']}G",
        f"能力：{equipment_summary(item_id)}",
        f"說明：{eq['desc']}",
        "購買後會放入背包；仍需到背包/裝備中替換。",
    ]
    return lines

def buy_workshop_item(state: dict, item_id: str) -> str:
    eq = EQUIPMENT[item_id]
    if state["gold"] < eq["price"]:
        return "金幣不足。"
    if state["job"] not in eq["jobs"]:
        return f"{state['job']}無法使用這件裝備，先別買比較好。"
    state["gold"] -= eq["price"]
    add_item(state, item_id, 1)
    return f"購買了 {eq['name']}。"

def workshop_buy_menu(state: dict, title_text: str, item_ids: list[str], border_style: str) -> None:
    while True:
        available = [item_id for item_id in item_ids if is_shop_item_available(state, item_id)]
        if not available:
            render_panel(title_text, ["目前沒有可購買裝備。"], border_style=border_style)
            pause()
            return
        choice = action_menu_panel(
            "選擇裝備",
            [workshop_item_line(state, item_id) for item_id in available],
            title_text,
            header_lines=[
                f"持有金幣：{state['gold']}G",
                f"目前職業：{state['job']} / 商品 {len(available)} 種",
            ],
            hint_lines=["選擇裝備可查看完整能力、可用職業與購買確認。"],
            allow_back=True,
            border_style=border_style,
        )
        if choice == 0:
            return
        item_id = available[choice - 1]
        action = action_menu_panel(
            "裝備操作",
            ["購買 1 件"],
            f"{title_text} - 裝備詳情",
            header_lines=workshop_item_detail_lines(state, item_id),
            allow_back=True,
            border_style=border_style,
        )
        if action == 0:
            continue
        result = buy_workshop_item(state, item_id)
        render_panel(
            f"{title_text} - 購買結果",
            [
                result,
                f"目前金幣：{state['gold']}G",
                f"{item_name(item_id)} 狀態：{equipment_status_line(state, item_id)}",
            ],
            border_style=border_style,
        )
        pause()

def recipe_base_status(state: dict, recipe: dict) -> str:
    base_item = recipe.get("base_item")
    if not base_item:
        return "無"
    status = "足夠" if owns_item_or_equipped(state, base_item) else "不足"
    return f"{item_name(base_item)}（{status}）"

def recipe_material_status(state: dict, materials: dict) -> str:
    parts = []
    for item_id, qty in materials.items():
        owned = state["inventory"].get(item_id, 0)
        status = "足夠" if owned >= qty else "不足"
        parts.append(f"{item_name(item_id)} {owned}/{qty} {status}")
    return "、".join(parts) if parts else "無"

def recipe_output_summary(recipe: dict) -> str:
    return format_items(recipe["output"])

def workshop_recipe_line(state: dict, recipe_id: str) -> str:
    recipe = RECIPES[recipe_id]
    return (
        f"{recipe['name']} / {recipe['gold']}G / "
        f"基底：{recipe_base_status(state, recipe)} / "
        f"素材：{format_items(recipe['materials'])} / {recipe['desc']}"
    )

def workshop_recipe_detail_lines(state: dict, recipe_id: str) -> list[str]:
    recipe = RECIPES[recipe_id]
    return [
        f"強化：{recipe['name']}",
        f"完成品：{recipe_output_summary(recipe)}",
        f"基底裝備：{recipe_base_status(state, recipe)}",
        f"素材需求：{recipe_material_status(state, recipe['materials'])}",
        f"費用：{recipe['gold']}G / 目前金幣：{state['gold']}G",
        f"效果：{recipe['desc']}",
        "強化會消耗素材；若需要基底裝備，已裝備物也可被消耗。",
    ]

def craft_recipe_message(state: dict, recipe_id: str) -> str:
    recipe = RECIPES[recipe_id]
    if state["gold"] < recipe["gold"]:
        return "金幣不足。"
    if not can_pay_items(state, recipe["materials"]):
        return "素材不足。"
    base_item = recipe.get("base_item")
    if base_item and not owns_item_or_equipped(state, base_item):
        return f"需要 {item_name(base_item)}。"
    state["gold"] -= recipe["gold"]
    pay_items(state, recipe["materials"])
    if base_item:
        consume_item_or_equipped(state, base_item)
    for item_id, qty in recipe["output"].items():
        add_item(state, item_id, qty)
    return f"完成：{recipe['name']}。"

def workshop_upgrade_menu(state: dict, title_text: str, recipe_ids: list[str], border_style: str) -> None:
    while True:
        available = [recipe_id for recipe_id in recipe_ids if recipe_available(state, recipe_id)]
        if not available:
            render_panel(title_text, ["目前沒有可用強化配方。"], border_style=border_style)
            pause()
            return
        choice = action_menu_panel(
            "選擇強化",
            [workshop_recipe_line(state, recipe_id) for recipe_id in available],
            title_text,
            header_lines=[f"持有金幣：{state['gold']}G"],
            hint_lines=["選擇強化可查看基底裝備、素材狀態與完成品。"],
            allow_back=True,
            border_style=border_style,
        )
        if choice == 0:
            return
        recipe_id = available[choice - 1]
        action = action_menu_panel(
            "強化操作",
            ["進行強化"],
            f"{title_text} - 強化詳情",
            header_lines=workshop_recipe_detail_lines(state, recipe_id),
            allow_back=True,
            border_style=border_style,
        )
        if action == 0:
            continue
        result = craft_recipe_message(state, recipe_id)
        render_panel(
            f"{title_text} - 強化結果",
            [result, f"目前金幣：{state['gold']}G"],
            border_style=border_style,
        )
        pause()

def workshop_equipment_lines(state: dict, item_ids: list[str]) -> list[str]:
    slot_names = {"weapon": "武器", "head": "頭部", "body": "身體", "accessory": "飾品", "special": "特殊"}
    relevant_slots = []
    for item_id in item_ids:
        slot = EQUIPMENT[item_id]["slot"]
        if slot not in relevant_slots:
            relevant_slots.append(slot)
    lines = ["目前裝備："]
    for slot in relevant_slots:
        equipped = state["equipment"].get(slot)
        lines.append(f"{slot_names.get(slot, slot)}：{item_name(equipped) if equipped else '無'}")
    owned = [
        f"{item_name(item_id)} x{state['inventory'][item_id]} / {equipment_summary(item_id)}"
        for item_id in item_ids
        if state["inventory"].get(item_id, 0) > 0
    ]
    lines.append("")
    lines.append("背包中的本店裝備：")
    lines.extend(owned if owned else ["目前沒有本店裝備在背包中。"])
    return lines

def workshop_catalog(
    state: dict,
    title_text: str,
    option_buy: str,
    option_upgrade: str,
    item_ids: list[str],
    recipe_ids: list[str],
    intro_lines: list[str],
    hint_lines: list[str],
    border_style: str,
) -> None:
    while True:
        choice = action_menu_panel(
            title_text,
            [option_buy, option_upgrade, "我的裝備"],
            title_text,
            header_lines=[*intro_lines, f"持有金幣：{state['gold']}G"],
            hint_lines=hint_lines,
            allow_back=True,
            border_style=border_style,
        )
        if choice == 0:
            return
        if choice == 1:
            workshop_buy_menu(state, f"{title_text} - {option_buy}", item_ids, border_style)
        elif choice == 2:
            workshop_upgrade_menu(state, f"{title_text} - {option_upgrade}", recipe_ids, border_style)
        elif choice == 3:
            render_panel(f"{title_text} - 我的裝備", workshop_equipment_lines(state, item_ids), border_style=border_style)
            pause()

def magic_book_price(state: dict, book_id: str) -> int:
    price = MAGIC_BOOKS[book_id]["price"]
    if book_id == "book_spark" and "quest_magic_crystal" in state["completed_quests"]:
        price = max(0, price - 50)
    return price

def magic_shop_category(book_id: str) -> str:
    skill = SKILLS[MAGIC_BOOKS[book_id]["skill"]]
    kind = skill["kind"]
    if kind == "damage":
        return "攻擊魔法"
    if kind == "heal":
        return "恢復魔法"
    if kind == "buff":
        return "輔助魔法"
    if kind == "debuff":
        return "特殊魔法"
    return "特殊魔法"

def magic_book_status(state: dict, book_id: str) -> str:
    book = MAGIC_BOOKS[book_id]
    skill_id = book["skill"]
    price = magic_book_price(state, book_id)
    if skill_id in state["learned_skills"]:
        return "已學會"
    if state["job"] not in book["jobs"]:
        return "職業不符"
    if state["level"] < book["level"]:
        return f"等級不足 Lv{book['level']}"
    if state["gold"] < price:
        return "金幣不足"
    if not can_pay_items(state, book["materials"]):
        return "素材不足"
    return "可學習"

def magic_shop_book_ids(category: str = "全部") -> list[str]:
    book_ids = list(MAGIC_BOOKS.keys())
    if category == "全部":
        return book_ids
    return [book_id for book_id in book_ids if magic_shop_category(book_id) == category]

def magic_material_status(state: dict, materials: dict) -> str:
    if not materials:
        return "無"
    parts = []
    for item_id, qty in materials.items():
        owned = state["inventory"].get(item_id, 0)
        status = "足夠" if owned >= qty else "不足"
        parts.append(f"{item_name(item_id)} {owned}/{qty} {status}")
    return "、".join(parts)

def magic_book_line(state: dict, book_id: str) -> str:
    book = MAGIC_BOOKS[book_id]
    skill = SKILLS[book["skill"]]
    price = magic_book_price(state, book_id)
    return (
        f"{book['name']} / {magic_shop_category(book_id)} / {magic_book_status(state, book_id)} / "
        f"{','.join(book['jobs'])} Lv{book['level']} / MP {skill['mp']} / {price}G / {skill['desc']}"
    )

def magic_book_detail_lines(state: dict, book_id: str) -> list[str]:
    book = MAGIC_BOOKS[book_id]
    skill = SKILLS[book["skill"]]
    price = magic_book_price(state, book_id)
    lines = [
        f"魔法書：{book['name']}",
        f"分類：{magic_shop_category(book_id)}",
        f"狀態：{magic_book_status(state, book_id)}",
        f"學會技能：{skill['name']} / MP {skill['mp']}",
        f"技能效果：{skill['desc']}",
        f"可用職業：{','.join(book['jobs'])}",
        f"目前職業：{state['job']}（{'可學' if state['job'] in book['jobs'] else '不可學'}）",
        f"等級需求：Lv{book['level']} / 目前 Lv{state['level']}",
        f"費用：{price}G / 目前金幣：{state['gold']}G",
        f"需求素材：{magic_material_status(state, book['materials'])}",
        "魔法書學會後會永久加入戰鬥技能。",
    ]
    if book_id == "book_spark" and "quest_magic_crystal" in state["completed_quests"]:
        lines.append("魔晶研究已完成，火花術書價格已折扣。")
    return lines

def learn_magic_book_message(state: dict, book_id: str) -> str:
    book = MAGIC_BOOKS[book_id]
    skill_id = book["skill"]
    price = magic_book_price(state, book_id)
    if skill_id in state["learned_skills"]:
        return "你已經學會這本書的技能。"
    if state["job"] not in book["jobs"]:
        return f"{state['job']}無法理解這本魔法書的核心術式。"
    if state["level"] < book["level"]:
        return f"等級不足，需要 Lv{book['level']}。"
    if state["gold"] < price:
        return "金幣不足。"
    if not can_pay_items(state, book["materials"]):
        return "素材不足。"
    state["gold"] -= price
    pay_items(state, book["materials"])
    state["learned_skills"].append(skill_id)
    return f"你學會了 {SKILLS[skill_id]['name']}。"

def magic_shop(state: dict, region_id: str = "border_fire") -> None:
    while True:
        category_options = []
        for category in MAGIC_SHOP_CATEGORIES:
            count = len(magic_shop_book_ids(category))
            category_options.append(f"{category} / {count} 本魔法書")
        facility_name = get_facility_display_name(region_id, "magic_shop")
        welcome_text = get_dialogue(region_id, "magic_shop", "welcome")
        choice = action_menu_panel(
            "選擇分類",
            category_options,
            facility_name,
            header_lines=[
                welcome_text,
                f"持有金幣：{state['gold']}G",
            ],
            hint_lines=["依魔法功能分類瀏覽；選中魔法書後可查看職業、等級、素材與技能效果。"],
            allow_back=True,
            border_style="magenta",
        )
        if choice == 0:
            return
        magic_shop_book_menu(state, MAGIC_SHOP_CATEGORIES[choice - 1], region_id)

def magic_shop_book_menu(state: dict, category: str, region_id: str = "border_fire") -> None:
    while True:
        book_ids = magic_shop_book_ids(category)
        facility_name = get_facility_display_name(region_id, "magic_shop")
        if not book_ids:
            render_panel(
                f"{facility_name} - 魔法書列表",
                [f"分類：{category}", "目前此分類沒有魔法書。"],
                border_style="magenta",
            )
            pause()
            return
        choice = action_menu_panel(
            "選擇魔法書",
            [magic_book_line(state, book_id) for book_id in book_ids],
            f"{facility_name} - 魔法書列表",
            header_lines=[
                f"持有金幣：{state['gold']}G",
                f"分類：{category} / 魔法書 {len(book_ids)} 本",
            ],
            hint_lines=["選擇魔法書可查看技能、條件、素材狀態與學習確認。"],
            allow_back=True,
            border_style="magenta",
        )
        if choice == 0:
            return
        book_id = book_ids[choice - 1]
        action = action_menu_panel(
            "魔法書操作",
            ["學習魔法"],
            "星燈魔法商店 - 魔法書詳情",
            header_lines=magic_book_detail_lines(state, book_id),
            allow_back=True,
            border_style="magenta",
        )
        if action == 0:
            continue
        result = learn_magic_book_message(state, book_id)
        render_panel(
            "星燈魔法商店 - 學習結果",
            [
                result,
                f"目前金幣：{state['gold']}G",
                f"狀態：{magic_book_status(state, book_id)}",
            ],
            border_style="magenta",
        )
        pause()

def recipe_available(state: dict, recipe_id: str) -> bool:
    recipe = RECIPES[recipe_id]
    return is_unlocked(state, recipe.get("unlock"))

def synthesis_recipe_category(recipe_id: str) -> str:
    recipe = RECIPES[recipe_id]
    for item_id in recipe["output"]:
        if item_id in ITEMS and ITEMS[item_id].get("kind") == "battle":
            return "戰術道具"
    return "裝備"

def synthesis_available_recipes(state: dict, recipe_ids: list[str], category: str = "全部") -> list[str]:
    available = [recipe_id for recipe_id in recipe_ids if recipe_available(state, recipe_id)]
    if category == "全部":
        return available
    return [recipe_id for recipe_id in available if synthesis_recipe_category(recipe_id) == category]

def recipe_output_owned_status(state: dict, recipe: dict) -> str:
    parts = []
    for item_id in recipe["output"]:
        if item_id in EQUIPMENT:
            parts.append(f"{item_name(item_id)} x{equipment_owned_count(state, item_id)}（{equipment_status_line(state, item_id)}）")
        else:
            parts.append(f"{item_name(item_id)} x{state['inventory'].get(item_id, 0)}")
    return "、".join(parts) if parts else "無"

def recipe_base_owned_count(state: dict, recipe: dict) -> int:
    base_item = recipe.get("base_item")
    if not base_item:
        return 0
    return state["inventory"].get(base_item, 0) + (1 if base_item in state["equipment"].values() else 0)

def synthesis_recipe_status(state: dict, recipe_id: str) -> str:
    recipe = RECIPES[recipe_id]
    if state["gold"] < recipe["gold"]:
        return "金幣不足"
    if not can_pay_items(state, recipe["materials"]):
        return "素材不足"
    base_item = recipe.get("base_item")
    if base_item and not owns_item_or_equipped(state, base_item):
        return "基底不足"
    return "可製作"

def max_synthesis_count(state: dict, recipe_id: str) -> int:
    recipe = RECIPES[recipe_id]
    limits = []
    if recipe["gold"] > 0:
        limits.append(state["gold"] // recipe["gold"])
    for item_id, qty in recipe["materials"].items():
        limits.append(state["inventory"].get(item_id, 0) // qty)
    if recipe.get("base_item"):
        limits.append(recipe_base_owned_count(state, recipe))
    return min(limits) if limits else 0

def synthesis_recipe_line(state: dict, recipe_id: str) -> str:
    recipe = RECIPES[recipe_id]
    return (
        f"{recipe['name']} / {synthesis_recipe_category(recipe_id)} / "
        f"{synthesis_recipe_status(state, recipe_id)} / "
        f"產出：{recipe_output_summary(recipe)} / "
        f"持有：{recipe_output_owned_status(state, recipe)} / "
        f"最多 {max_synthesis_count(state, recipe_id)} 次 / "
        f"{recipe['gold']}G / 素材：{recipe_material_status(state, recipe['materials'])}"
    )

def synthesis_recipe_detail_lines(state: dict, recipe_id: str) -> list[str]:
    recipe = RECIPES[recipe_id]
    return [
        f"配方：{recipe['name']}",
        f"分類：{synthesis_recipe_category(recipe_id)}",
        f"狀態：{synthesis_recipe_status(state, recipe_id)}",
        f"產出：{recipe_output_summary(recipe)}",
        f"持有：{recipe_output_owned_status(state, recipe)}",
        f"基底：{recipe_base_status(state, recipe)}",
        f"素材需求：{recipe_material_status(state, recipe['materials'])}",
        f"最多可製作：{max_synthesis_count(state, recipe_id)} 次",
        f"費用：{recipe['gold']}G / 目前金幣：{state['gold']}G",
        f"效果：{recipe['desc']}",
        "合成會消耗素材；若需要基底裝備，已裝備物也可被消耗。",
    ]

def craft_menu(state: dict, title_text: str, recipe_ids: list[str], region_id: str = "border_fire") -> None:
    title_text = get_facility_display_name(region_id, "synthesis")
    while True:
        available = synthesis_available_recipes(state, recipe_ids)
        if not available:
            render_panel(title_text, ["目前沒有可用配方。"], border_style="green")
            pause()
            return
        choice = action_menu_panel(
            "選擇分類",
            [
                f"{category} / {len(synthesis_available_recipes(state, recipe_ids, category))} 張配方"
                for category in SYNTHESIS_CATEGORIES
            ],
            title_text,
            header_lines=[
                get_dialogue(region_id, "synthesis", "welcome"),
                f"持有金幣：{state['gold']}G",
            ],
            hint_lines=["分類瀏覽可用配方；選中配方後會顯示產出、持有數、基底與素材狀態。"],
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        craft_recipe_list_menu(state, title_text, recipe_ids, SYNTHESIS_CATEGORIES[choice - 1])

def craft_recipe_list_menu(state: dict, title_text: str, recipe_ids: list[str], category: str) -> None:
    while True:
        available = synthesis_available_recipes(state, recipe_ids, category)
        if not available:
            render_panel(
                f"{title_text} - 配方列表",
                [f"分類：{category}", "目前此分類沒有可用配方。"],
                border_style="green",
            )
            pause()
            return
        choice = action_menu_panel(
            "選擇配方",
            [synthesis_recipe_line(state, recipe_id) for recipe_id in available],
            f"{title_text} - 配方列表",
            header_lines=[
                f"持有金幣：{state['gold']}G",
                f"分類：{category} / 配方 {len(available)} 張",
            ],
            hint_lines=["選擇配方可查看完整材料狀態與合成確認。"],
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        recipe_id = available[choice - 1]
        action = action_menu_panel(
            "合成操作",
            ["進行合成"],
            f"{title_text} - 配方詳情",
            header_lines=synthesis_recipe_detail_lines(state, recipe_id),
            allow_back=True,
            border_style="green",
        )
        if action == 0:
            continue
        result = craft_recipe_message(state, recipe_id)
        recipe = RECIPES[recipe_id]
        render_panel(
            f"{title_text} - 合成結果",
            [
                result,
                f"目前金幣：{state['gold']}G",
                f"持有：{recipe_output_owned_status(state, recipe)}",
            ],
            border_style="green",
        )
        pause()

def craft_recipe(state: dict, recipe_id: str) -> None:
    print(craft_recipe_message(state, recipe_id))

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


def preview_relic_entries() -> list[tuple[str, dict]]:
    return [
        (relic_id, relic)
        for relic_id, relic in RELICS.items()
        if relic.get("status") == "preview"
    ]


def find_preview_relic(identifier: str | None) -> tuple[str, dict] | None:
    if not identifier:
        return None
    for relic_id, relic in preview_relic_entries():
        if identifier in {relic_id, relic.get("name"), relic.get("seal_item_id"), relic.get("element_id")}:
            return relic_id, relic
    return None


def relic_source_required(relic: dict) -> int:
    required = relic.get("source_required", 1)
    return required if isinstance(required, int) and required > 0 else 1


def relic_source_count(state: dict, relic: dict) -> int:
    return state.get("inventory", {}).get(relic.get("source_item_id"), 0)


def relic_enshrined(state: dict, relic: dict) -> bool:
    return bool(state.get("flags", {}).get(relic.get("complete_flag")))


def relic_ready_to_enshrine(state: dict, relic: dict) -> bool:
    return (
        not relic_enshrined(state, relic)
        and relic_unlock_met(state, relic.get("unlock"))
        and relic_source_count(state, relic) >= relic_source_required(relic)
    )


def relic_disabled_reason(state: dict, relic: dict) -> str | None:
    if relic_enshrined(state, relic):
        return "聖印已安置。"
    if not relic_unlock_met(state, relic.get("unlock")):
        unlock_data = relic.get("unlock") or {}
        return f"尚未達成：{unlock_data.get('label', '前置條件')}。"
    source_item_id = relic.get("source_item_id", "")
    required = relic_source_required(relic)
    current = relic_source_count(state, relic)
    if current < required:
        return f"需要 {item_name(source_item_id)} x{required}（目前 {current}）。"
    return None


def ready_relic_names(state: dict) -> list[str]:
    return [
        relic["name"]
        for _relic_id, relic in preview_relic_entries()
        if relic_ready_to_enshrine(state, relic)
    ]


def all_elemental_seals_enshrined(state: dict) -> bool:
    flags = state.get("flags", {})
    return all(flags.get(flag) for flag in ELEMENTAL_SEAL_FLAGS)


def unlock_final_region_from_relics(state: dict) -> bool:
    if not all_elemental_seals_enshrined(state):
        return False
    if is_unlocked(state, FINAL_REGION_UNLOCK):
        return False
    unlock(state, FINAL_REGION_UNLOCK)
    return True


def enshrine_relic(state: dict, identifier: str | None) -> dict:
    found = find_preview_relic(identifier)
    if not found:
        return {
            "status": "blocked",
            "changed": False,
            "message": "找不到指定的聖印資料。",
        }

    relic_id, relic = found
    if relic_enshrined(state, relic):
        return {
            "status": "complete",
            "changed": False,
            "relic_id": relic_id,
            "message": relic["complete_text"],
        }

    disabled_reason = relic_disabled_reason(state, relic)
    if disabled_reason:
        return {
            "status": "blocked",
            "changed": False,
            "relic_id": relic_id,
            "message": disabled_reason,
        }

    source_item_id = relic["source_item_id"]
    required = relic_source_required(relic)
    if not remove_item(state, source_item_id, required):
        return {
            "status": "blocked",
            "changed": False,
            "relic_id": relic_id,
            "message": f"需要 {item_name(source_item_id)} x{required}。",
        }

    seal_item_id = relic["seal_item_id"]
    add_item(state, seal_item_id, 1)
    state.setdefault("flags", {})[relic["complete_flag"]] = True

    unlocked_lines = []
    if relic.get("element_id") == "fire" and not is_unlocked(state, ICE_REGION_UNLOCK):
        unlock(state, ICE_REGION_UNLOCK)
        unlocked_lines.append("極寒區域路線已開放。")
    if unlock_final_region_from_relics(state):
        unlocked_lines.append("四聖印已安置，魔王城前線路線已開放。")

    message_lines = [
        relic["ready_text"],
        f"取得並安置：{item_name(seal_item_id)} x1。",
        "聖印被動效果尚未開放。",
    ]
    message_lines.extend(unlocked_lines)
    return {
        "status": "enshrined",
        "changed": True,
        "relic_id": relic_id,
        "message": "\n".join(message_lines),
    }


def relic_preview_menu(state: dict, region_id: str = "border_fire") -> None:
    facility_name = get_facility_display_name(region_id, "relic")
    title(facility_name)
    previews = [relic for _relic_id, relic in preview_relic_entries()]
    if not previews:
        print("目前沒有可預覽的聖物線索。")
        pause()
        return

    print("四元素聖印可在此合成或安置；聖印被動效果尚未開放。")
    for relic in previews:
        complete = relic_enshrined(state, relic)
        ready = relic_ready_to_enshrine(state, relic)
        print(f"\n{relic['name']}")
        print(relic["summary"])
        print(f"來源：{relic['source']}")
        print(relic_unlock_line(state, relic.get("unlock")))
        print(f"源證：{item_name(relic['source_item_id'])} {relic_source_count(state, relic)}/{relic_source_required(relic)}")
        print("狀態：" + ("已安置" if complete else ("可安置" if ready else "待調查")))
        print(f"效果預告：{relic['effect_preview']}")
    ready_entries = [
        (relic_id, relic)
        for relic_id, relic in preview_relic_entries()
        if relic_ready_to_enshrine(state, relic)
    ]
    if ready_entries:
        options = [relic["action_label"] for _relic_id, relic in ready_entries]
        choice = action_menu_panel(
            "聖印安置",
            options,
            facility_name,
            header_lines=["選擇可安置的聖印。此操作不會啟用任何戰鬥效果。"],
            allow_back=True,
            border_style="yellow",
        )
        if choice:
            relic_id, _relic = ready_entries[choice - 1]
            result = enshrine_relic(state, relic_id)
            render_panel("聖印安置結果", result["message"].splitlines(), border_style="yellow")
    else:
        print("\n目前沒有可安置的聖印。")
    print("\n這裡不會裝備、啟用、強化聖物，也不會提供戰鬥加成。")
    pause()

def town_menu(state: dict, region_id: str = "border_fire") -> None:
    while True:
        region = REGIONS.get(region_id, REGIONS["border_fire"])
        options = [
            f"{get_facility_display_name(region_id, 'guild')} - 委託、素材收購與火印線索",
            f"{get_facility_display_name(region_id, 'weapon_workshop')} - 武器購買與強化",
            f"{get_facility_display_name(region_id, 'armor_workshop')} - 防具購買與強化",
            f"{get_facility_display_name(region_id, 'shop')} - 補給與特殊道具",
            f"{get_facility_display_name(region_id, 'synthesis')} - 把素材轉成裝備與戰術道具",
            f"{get_facility_display_name(region_id, 'magic_shop')} - 學習永久技能",
            f"{get_facility_display_name(region_id, 'temple')} - 轉職、火印與未來方向預覽",
            f"{get_facility_display_name(region_id, 'relic')} - 預覽未開放聖物線索",
            f"{get_facility_display_name(region_id, 'storage')} - 存放與取出非關鍵物品",
            f"{get_facility_display_name(region_id, 'inn')}休息 30G - 回復 HP/MP",
        ]
        choice = action_menu_panel(
            "你要去哪裡",
            options,
            region["town_name"],
            header_lines=player_resource_lines(state)[:2],
            hint_lines=town_hint_lines(state),
            allow_back=True,
            border_style="green",
        )
        if choice == 0:
            return
        if choice == 1:
            guild_menu(state, region_id)
        elif choice == 2:
            iron_workshop(state, region_id)
        elif choice == 3:
            armor_workshop(state, region_id)
        elif choice == 4:
            travel_shop(state, region_id)
        elif choice == 5:
            if not is_unlocked(state, "shop_synthesis_01"):
                mira_name = get_npc_display_name(region_id, "mira")
                print(f"{mira_name}的店門半掩著。先完成工會任務「洞窟採集」吧。")
                pause()
            else:
                craft_menu(
                    state,
                    get_facility_display_name(region_id, "synthesis"),
                    ["recipe_fire_cloak", "recipe_focus_pouch", "recipe_heat_charm", "recipe_piercing_bundle"], region_id,
                )
        elif choice == 6:
            magic_shop(state, region_id)
        elif choice == 7:
            temple(state, region_id)
        elif choice == 8:
            relic_preview_menu(state, region_id)
        elif choice == 9:
            storage_menu(state, region_id)
        elif choice == 10:
            rest_inn(state, region_id)

def iron_workshop(state: dict, region_id: str = "border_fire") -> None:
    title_text = get_facility_display_name(region_id, "weapon_workshop")
    ambiance = get_dialogue(region_id, "weapon_workshop", "ambiance")
    quote = get_dialogue(region_id, "weapon_workshop", "quote")
    workshop_catalog(
        state,
        title_text,
        "購買武器",
        "強化武器",
        SHOP_INVENTORY["weapon"],
        ["recipe_iron_sword_plus_1"],
        [ambiance, quote],
        ["武器升級能縮短戰鬥回合；購買後仍需到背包/裝備中替換。"],
        "yellow",
    )

def armor_workshop(state: dict, region_id: str = "border_fire") -> None:
    title_text = get_facility_display_name(region_id, "armor_workshop")
    ambiance = get_dialogue(region_id, "armor_workshop", "ambiance")
    quote = get_dialogue(region_id, "armor_workshop", "quote")
    workshop_catalog(
        state,
        title_text,
        "購買防具",
        "強化防具",
        SHOP_INVENTORY["armor"],
        ["recipe_leather_armor_plus_1"],
        [ambiance, quote],
        ["防具與抗性裝能提高長探索容錯；購買後仍需到背包/裝備中替換。"],
        "green",
    )

def rest_inn(state: dict, region_id: str = "border_fire") -> None:
    stats = get_stats(state)
    title_text = get_facility_display_name(region_id, "inn")
    welcome_text = get_dialogue(region_id, "inn", "welcome")
    reject_text = get_dialogue(region_id, "inn", "reject")
    render_panel(
        title_text,
        [
            welcome_text,
            f"費用：30G / 目前金幣：{state['gold']}G",
            f"目前 HP {state['current_hp']}/{stats['max_hp']} / MP {state['current_mp']}/{stats['max_mp']}",
        ],
        border_style="green",
    )
    if state["gold"] < 30:
        print(reject_text)
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

def storage_menu(state: dict, region_id: str = "border_fire") -> None:
    ensure_state_defaults(state)
    facility_name = get_facility_display_name(region_id, "storage")
    if not state["storage_unlocked"]:
        locked_msg = get_dialogue(region_id, "storage", "locked")
        render_panel(
            facility_name,
            [
                locked_msg,
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
        unlocked_msg = get_dialogue(region_id, "storage", "unlocked")
        choice = action_menu_panel(
            "選擇動作",
            ["查看倉庫", "存入物品", "取出物品"],
            f"{facility_name} LV1",
            header_lines=[
                unlocked_msg,
                f"容量：{storage_kind_count(state)}/{STORAGE_CAPACITY} 種物品。",
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
        return (
            "quest_mine_scout" in state["completed_quests"]
            and (
                state["flags"].get(BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG, False)
                or state["flags"].get("boss_glen_defeated", False)
                or quest_id in state["completed_quests"]
            )
        )
    if quest_id == "quest_ash_ravine_scout":
        return "quest_boss_glen" in state["completed_quests"]
    if quest_id == "quest_supply_upgrade":
        return state["flags"].get("ash_guardian_defeated", False)
    if quest_id == "quest_cinder_depths_scout":
        return "quest_supply_upgrade" in state["completed_quests"]
    if quest_id == "quest_ice_minor_a":
        return is_unlocked(state, ICE_REGION_UNLOCK)
    if quest_id == "quest_ice_minor_b":
        return "quest_ice_minor_a" in state["completed_quests"]
    if quest_id == "quest_ice_main_phase_1":
        return "quest_ice_minor_b" in state["completed_quests"]
    if quest_id == "quest_ice_main_phase_2":
        return "quest_ice_main_phase_1" in state["completed_quests"]
    if quest_id == "quest_ice_return_handoff":
        return "quest_ice_main_phase_2" in state["completed_quests"]
    if quest_id == "quest_earth_minor_a":
        return is_unlocked(state, EARTH_REGION_UNLOCK)
    if quest_id == "quest_earth_minor_b":
        return "quest_earth_minor_a" in state["completed_quests"]
    if quest_id == "quest_earth_main_phase_1":
        return "quest_earth_minor_b" in state["completed_quests"]
    if quest_id == "quest_earth_main_phase_2":
        return "quest_earth_main_phase_1" in state["completed_quests"]
    if quest_id == "quest_earth_return_handoff":
        return "quest_earth_main_phase_2" in state["completed_quests"]
    if quest_id == "quest_thunder_minor_a":
        return is_unlocked(state, THUNDER_REGION_UNLOCK)
    if quest_id == "quest_thunder_minor_b":
        return "quest_thunder_minor_a" in state["completed_quests"]
    if quest_id == "quest_thunder_main_phase_1":
        return "quest_thunder_minor_b" in state["completed_quests"]
    if quest_id == "quest_thunder_main_phase_2":
        return "quest_thunder_main_phase_1" in state["completed_quests"]
    if quest_id == "quest_thunder_return_handoff":
        return "quest_thunder_main_phase_2" in state["completed_quests"]
    if quest_id == "quest_final_minor_a":
        return is_unlocked(state, FINAL_REGION_UNLOCK)
    if quest_id == "quest_final_minor_b":
        return "quest_final_minor_a" in state["completed_quests"]
    if quest_id == "quest_final_main_phase_1":
        return "quest_final_minor_b" in state["completed_quests"]
    if quest_id == "quest_final_main_phase_2":
        return "quest_final_main_phase_1" in state["completed_quests"]
    if quest_id == FINAL_QUEST_ID:
        return "quest_final_main_phase_2" in state["completed_quests"]
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

def record_boss_glen_sighting(state: dict) -> bool:
    flags = state.setdefault("flags", {})
    if flags.get("boss_glen_defeated") or flags.get(BOSS_GLEN_SIGHTED_FLAG):
        return False
    flags[BOSS_GLEN_SIGHTED_FLAG] = True
    return True

def can_accept_boss_glen_investigation(state: dict) -> bool:
    flags = state.setdefault("flags", {})
    return (
        flags.get(BOSS_GLEN_SIGHTED_FLAG, False)
        and not flags.get(BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG, False)
        and not flags.get("boss_glen_defeated", False)
    )

def accept_boss_glen_investigation(state: dict) -> bool:
    if not can_accept_boss_glen_investigation(state):
        return False
    state["flags"][BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG] = True
    return True

def boss_glen_investigation(state: dict) -> None:
    dungeon_name = DUNGEONS["dungeon_scorched_mine"]["name"]
    boss_name = MONSTERS["boss_glen"]["name"]
    title(f"{dungeon_name}異常調查")
    print(f"你向冒險者公會回報了{dungeon_name}深處的強敵。")
    print(f"公會正式委託你調查並討伐{boss_name}。")
    accept_boss_glen_investigation(state)

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

def guild_menu(state: dict, region_id: str = "border_fire") -> None:
    while True:
        options = ["查看委託任務", "收購素材"]
        glen_investigation_option = can_accept_boss_glen_investigation(state)
        if glen_investigation_option:
            options.append(f"接受{DUNGEONS['dungeon_scorched_mine']['name']}異常調查")
        inquiry_option = can_ask_fire_mark_guild_inquiry(state)
        if inquiry_option:
            options.append("詢問三枚印記碎片的事情")
        facility_name = get_facility_display_name(region_id, "guild")
        greeting = get_dialogue(region_id, "guild", "greeting")
        welcome = get_dialogue(region_id, "guild", "welcome")
        choice = action_menu_panel(
            "選擇服務",
            options,
            facility_name,
            header_lines=[
                greeting,
                welcome,
            ],
            hint_lines=guild_hint_lines(state),
            allow_back=True,
            border_style="cyan",
        )
        if choice == 0:
            return
        if choice == 1:
            guild_quest_menu(state, region_id)
        elif choice == 2:
            guild_material_buy_menu(state)
        elif glen_investigation_option and choice == 3:
            boss_glen_investigation(state)
            pause()
        elif inquiry_option and choice == 3 + int(glen_investigation_option):
            fire_mark_guild_inquiry(state)
            pause()

def guild_quest_menu(state: dict, region_id: str = "border_fire") -> None:
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
    print("「去神殿後側的聖物調查台吧。那裡能讓碎片承接成真正的火之聖印。」")
    print()
    print("已確認：未完成的火之印記核心。")
    print("下一步：前往聖物調查台合成並安置火之聖印。聖印被動效果尚未開放。")
    state["flags"][FIRE_MARK_CHURCH_LOOKUP_FLAG] = True
    print()


def temple(state: dict, region_id: str = "border_fire") -> None:
    facility_name = get_facility_display_name(region_id, "temple")
    welcome_msg = get_dialogue(region_id, "temple", "welcome")
    title(facility_name)
    print(welcome_msg)
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

def dungeon_menu(state: dict, region_id: str = "border_fire") -> None:
    if state["flags"].get("ash_guardian_defeated") and not is_unlocked(state, "dungeon_cinder_seal_depths"):
        unlock(state, "dungeon_cinder_seal_depths")
    unlocked_dungeons = player_facing_dungeon_ids(state)
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

def clear_dungeon_boss(state: dict, boss_id: str, run_log: dict) -> None:
    if boss_id == "boss_glen":
        clear_boss_glen(state, run_log)
    elif boss_id == "boss_ash_guardian":
        clear_ash_guardian(state, run_log)
    elif boss_id == "boss_cinder_seal_sentinel":
        clear_cinder_seal_sentinel(state, run_log)
    elif boss_id == "boss_ice_wreck_captain":
        clear_ice_wreck_captain(state, run_log)
    elif boss_id == "boss_ice_frostroot_keeper":
        clear_ice_frostroot_keeper(state, run_log)
    elif boss_id == "boss_ice_outer_gatewarden":
        clear_ice_outer_gatewarden(state, run_log)
    elif boss_id == "boss_ice_final_seal_lord":
        clear_ice_final_seal_lord(state, run_log)
    elif boss_id == "boss_earth_rootwarden":
        clear_earth_rootwarden(state, run_log)
    elif boss_id == "boss_earth_quarry_colossus":
        clear_earth_quarry_colossus(state, run_log)
    elif boss_id == "boss_earth_outer_grovekeeper":
        clear_earth_outer_grovekeeper(state, run_log)
    elif boss_id == "boss_earth_deep_leyline_lord":
        clear_earth_deep_leyline_lord(state, run_log)
    elif boss_id == "boss_thunder_plateau_beacon":
        clear_thunder_plateau_beacon(state, run_log)
    elif boss_id == "boss_thunder_channel_keeper":
        clear_thunder_channel_keeper(state, run_log)
    elif boss_id == "boss_thunder_lower_array_warden":
        clear_thunder_lower_array_warden(state, run_log)
    elif boss_id == "boss_thunder_crown_storm_lord":
        clear_thunder_crown_storm_lord(state, run_log)
    elif boss_id == "boss_final_echo_vanguard":
        clear_final_echo_vanguard(state, run_log)
    elif boss_id == "boss_final_ruin_jailer":
        clear_final_ruin_jailer(state, run_log)
    elif boss_id == "boss_final_echo_warden":
        clear_final_echo_warden(state, run_log)
    elif boss_id == "boss_final_seal_core":
        clear_final_seal_core(state, run_log)
    elif boss_id == "boss_final_demon_king":
        clear_final_demon_king(state, run_log)

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
    if dungeon_id == "dungeon_scorched_mine" and boss_id == "boss_glen":
        first_sighting = record_boss_glen_sighting(state)
        if first_sighting:
            print(f"\n你在{dungeon['name']}深處發現了{MONSTERS[boss_id]['name']}，但目前情報不足。")
        if (
            not state["flags"].get(BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG)
            and not state["flags"].get("boss_glen_defeated")
        ):
            print(f"請先返回冒險者公會回報，接受{dungeon['name']}異常調查後再來挑戰。")
    if boss_available_at_dungeon_end(state, dungeon_id, boss_id):
        raw = input(boss_challenge_prompt(boss_id)).strip().lower()
        if raw == "y":
            result = combat(state, boss_id, boss=True, run_log=run_log)
            if result is False:
                handle_defeat(state, run_log)
                return
            if result is True:
                clear_dungeon_boss(state, boss_id, run_log)
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
    print("三枚碎片短暫共鳴，像有一個尚未說出口的名字在灰燼裡亮起。回城後先向工會與神殿確認。")

def clear_ice_wreck_captain(state: dict, run_log: dict) -> None:
    if state["flags"].get("ice_wreck_captain_defeated"):
        return
    state["flags"]["ice_wreck_captain_defeated"] = True
    add_loot(state, "key_ice_wreck_captain_log", 1, run_log)
    add_loot(state, "mat_ice_saltcloth", 2, run_log)
    print("\nWreck Captain defeated. Key proof recovered: Wreck Captain Log x1.")

def clear_ice_frostroot_keeper(state: dict, run_log: dict) -> None:
    if state["flags"].get("ice_frostroot_keeper_defeated"):
        return
    state["flags"]["ice_frostroot_keeper_defeated"] = True
    add_loot(state, "key_ice_frostroot_core", 1, run_log)
    add_loot(state, "mat_ice_frostroot", 2, run_log)
    print("\nFrostroot Keeper defeated. Key proof recovered: Frostroot Core x1.")

def clear_ice_outer_gatewarden(state: dict, run_log: dict) -> None:
    if state["flags"].get("ice_outer_gatewarden_defeated"):
        return
    state["flags"]["ice_outer_gatewarden_defeated"] = True
    add_loot(state, "key_ice_outer_gate_sigils", 1, run_log)
    add_loot(state, "mat_ice_frostiron", 2, run_log)
    print("\nOuter Gatewarden defeated. Q3 can now be reported at the Guild.")

def clear_ice_final_seal_lord(state: dict, run_log: dict) -> None:
    if state["flags"].get("ice_final_boss_defeated"):
        return
    state["flags"]["ice_final_boss_defeated"] = True
    state["flags"]["ice_relic_marker_resolved"] = True
    add_loot(state, "key_ice_relic_marker_source", 1, run_log)
    add_loot(state, "mat_ice_deep_core", 2, run_log)
    print("\nFinal Seal Lord defeated. Ice relic marker source recovered; no relic effect is active.")

def clear_earth_rootwarden(state: dict, run_log: dict) -> None:
    if state["flags"].get("earth_rootwarden_defeated"):
        return
    state["flags"]["earth_rootwarden_defeated"] = True
    add_loot(state, "key_earth_rootwarden_seed", 1, run_log)
    add_loot(state, "mat_earth_rootfiber", 2, run_log)
    print("\nRootwarden defeated. Key proof recovered: Rootwarden Seed x1.")

def clear_earth_quarry_colossus(state: dict, run_log: dict) -> None:
    if state["flags"].get("earth_quarry_colossus_defeated"):
        return
    state["flags"]["earth_quarry_colossus_defeated"] = True
    add_loot(state, "key_earth_quarry_core", 1, run_log)
    add_loot(state, "mat_earth_quarry_stone", 2, run_log)
    print("\nQuarry Colossus defeated. Key proof recovered: Quarry Colossus Core x1.")

def clear_earth_outer_grovekeeper(state: dict, run_log: dict) -> None:
    if state["flags"].get("earth_outer_grovekeeper_defeated"):
        return
    state["flags"]["earth_outer_grovekeeper_defeated"] = True
    add_loot(state, "key_earth_outer_grove_sigils", 1, run_log)
    add_loot(state, "mat_earth_leyline_shard", 2, run_log)
    print("\nOuter Grovekeeper defeated. Q3 can now be reported at the Guild.")

def clear_earth_deep_leyline_lord(state: dict, run_log: dict) -> None:
    if state["flags"].get("earth_final_boss_defeated"):
        return
    state["flags"]["earth_final_boss_defeated"] = True
    state["flags"]["earth_relic_marker_resolved"] = True
    add_loot(state, "key_earth_relic_marker_source", 1, run_log)
    add_loot(state, "mat_earth_deep_core", 2, run_log)
    print("\nDeep Leyline Lord defeated. Earth relic marker source recovered; no relic effect is active.")

def clear_thunder_plateau_beacon(state: dict, run_log: dict) -> None:
    if state["flags"].get("thunder_plateau_beacon_defeated"):
        return
    state["flags"]["thunder_plateau_beacon_defeated"] = True
    add_loot(state, "key_thunder_plateau_beacon", 1, run_log)
    add_loot(state, "mat_thunder_copper_vein", 2, run_log)
    print("\nPlateau Beacon defeated. Key proof recovered: Plateau Beacon x1.")

def clear_thunder_channel_keeper(state: dict, run_log: dict) -> None:
    if state["flags"].get("thunder_channel_keeper_defeated"):
        return
    state["flags"]["thunder_channel_keeper_defeated"] = True
    add_loot(state, "key_thunder_channel_core", 1, run_log)
    add_loot(state, "mat_thunder_sky_stone", 2, run_log)
    print("\nChannel Keeper defeated. Key proof recovered: Channel Core x1.")

def clear_thunder_lower_array_warden(state: dict, run_log: dict) -> None:
    if state["flags"].get("thunder_lower_array_warden_defeated"):
        return
    state["flags"]["thunder_lower_array_warden_defeated"] = True
    add_loot(state, "key_thunder_lower_array_sigils", 1, run_log)
    add_loot(state, "mat_thunder_cloud_essence", 2, run_log)
    print("\nLower Array Warden defeated. Q3 can now be reported at the Guild.")

def clear_thunder_crown_storm_lord(state: dict, run_log: dict) -> None:
    if state["flags"].get("thunder_final_boss_defeated"):
        return
    state["flags"]["thunder_final_boss_defeated"] = True
    state["flags"]["thunder_relic_marker_resolved"] = True
    add_loot(state, "key_thunder_relic_marker_source", 1, run_log)
    add_loot(state, "mat_thunder_deep_core", 2, run_log)
    print("\nCrown Storm Lord defeated. Thunder relic marker source recovered; no relic effect is active.")

def clear_final_echo_vanguard(state: dict, run_log: dict) -> None:
    if state["flags"].get("final_echo_vanguard_defeated"):
        return
    state["flags"]["final_echo_vanguard_defeated"] = True
    add_loot(state, "key_final_vanguard_proof", 1, run_log)
    add_loot(state, "mat_final_echo_ash", 2, run_log)
    print("\nFinal Echo Vanguard defeated. Key proof recovered: Final Vanguard Proof x1.")

def clear_final_ruin_jailer(state: dict, run_log: dict) -> None:
    if state["flags"].get("final_ruin_jailer_defeated"):
        return
    state["flags"]["final_ruin_jailer_defeated"] = True
    add_loot(state, "key_final_ruin_jailer_core", 1, run_log)
    add_loot(state, "mat_final_root_stone", 2, run_log)
    print("\nRuin Jailer defeated. Key proof recovered: Ruin Jailer Core x1.")

def clear_final_echo_warden(state: dict, run_log: dict) -> None:
    if state["flags"].get("final_echo_warden_defeated"):
        return
    state["flags"]["final_echo_warden_defeated"] = True
    add_loot(state, "key_final_echo_warden_sigils", 1, run_log)
    add_loot(state, "mat_final_seal_core", 2, run_log)
    print("\nEcho Warden defeated. Q3 can now be reported at the Guild.")

def clear_final_seal_core(state: dict, run_log: dict) -> None:
    if state["flags"].get("final_seal_core_defeated"):
        return
    state["flags"]["final_seal_core_defeated"] = True
    add_loot(state, "key_final_seal_core_sigils", 1, run_log)
    add_loot(state, "mat_final_demon_core", 2, run_log)
    print("\nFinal Seal Core broken. Q4 can now be reported at the Guild.")

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

def clear_final_demon_king(state: dict, run_log: dict) -> None:
    if state["flags"].get("final_demon_king_defeated"):
        return
    state["flags"]["final_demon_king_defeated"] = True
    state["flags"][MAIN_STORY_CLEARED_FLAG] = True
    add_loot(state, "key_final_demon_king_mark", 1, run_log)
    add_loot(state, "mat_final_demon_core", 2, run_log)
    complete_final_quest_from_boss(state)
    state["_ending_pending"] = True
    print("\nDemon King defeated. The main story ending is ready.")

def show_main_story_ending(state: dict) -> None:
    render_panel(
        "Ending",
        [
            "The Demon King's throne falls silent.",
            "The four elemental marks answer one another: ash, frost, root, and thunder.",
            "The maze does not vanish, but its hunger loosens. Roads that once twisted shut begin to breathe again.",
            f"{state['name']} returns to the Guild as the first adventurer to close the Element Maze's main seal.",
        ],
        border_style="yellow",
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

def main_loop(state: dict) -> str | None:
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
            if state.pop("_return_to_title", False):
                return "title"
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
    clear_final_demon_king(final_state, {"gold": 0, "items": {}})
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
