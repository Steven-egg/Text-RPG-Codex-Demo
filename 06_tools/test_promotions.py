import sys
import random
import math
from pathlib import Path
from copy import deepcopy

# 加入路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "03_engine"))
sys.path.insert(0, str(Path(__file__).parent.parent / "04_data"))

from engine.state import create_state, get_stats, add_item, equip_item
from engine import game
from data import PROMOTIONS, SKILLS, MONSTERS

# 標準裝備配置
BEST_GEAR = {
    "earth": {
        "warrior": {"weapon": "weapon_earth_warrior_01", "head": "armor_earth_head_01", "body": "armor_earth_body_01", "accessory": "acc_earth_accessory_01"},
        "mage": {"weapon": "weapon_earth_mage_01", "head": "armor_earth_head_01", "body": "armor_traveler_cloth", "accessory": "acc_earth_accessory_01"},
        "rogue": {"weapon": "weapon_earth_rogue_01", "head": "armor_rogue_sleeve_blade", "body": "armor_earth_rogue_body_01", "accessory": "acc_earth_accessory_01"},
        "cleric": {"weapon": "weapon_earth_priest_01", "head": "armor_earth_head_01", "body": "armor_earth_body_01", "accessory": "acc_earth_accessory_01"},
    },
    "thunder": {
        "warrior": {"weapon": "weapon_thunder_warrior_01", "head": "armor_thunder_head_01", "body": "armor_thunder_body_01", "accessory": "acc_thunder_accessory_01"},
        "mage": {"weapon": "weapon_thunder_mage_01", "head": "armor_thunder_head_01", "body": "armor_traveler_cloth", "accessory": "acc_thunder_accessory_01"},
        "rogue": {"weapon": "weapon_thunder_rogue_01", "head": "armor_rogue_sleeve_blade", "body": "armor_thunder_rogue_body_01", "accessory": "acc_thunder_accessory_01"},
        "cleric": {"weapon": "weapon_thunder_priest_01", "head": "armor_thunder_head_01", "body": "armor_thunder_body_01", "accessory": "acc_thunder_accessory_01"},
    },
    "final": {
        "warrior": {"weapon": "weapon_final_warrior_01", "head": "armor_final_head_01", "body": "armor_final_body_01", "accessory": "acc_final_accessory_01"},
        "mage": {"weapon": "weapon_final_mage_01", "head": "armor_final_head_01", "body": "armor_traveler_cloth", "accessory": "acc_final_accessory_01"},
        "rogue": {"weapon": "weapon_final_rogue_01", "head": "armor_rogue_sleeve_blade", "body": "armor_final_rogue_body_01", "accessory": "acc_final_accessory_01"},
        "cleric": {"weapon": "weapon_final_priest_01", "head": "armor_final_head_01", "body": "armor_final_body_01", "accessory": "acc_final_accessory_01"},
    },
}

# 為每個職業建立合適的 Player State
def build_promoted_state(promo_id: str, region: str) -> dict:
    promo = PROMOTIONS[promo_id]
    base_job = promo["source_job"]
    
    # 建立等級 18 的基礎角色
    state = create_state("TestHero", base_job)
    state["level"] = 18
    state["promotion_id"] = promo_id
    
    # 學習新技能與基礎技能
    state["learned_skills"].extend([promo["active_skill_id"], promo["passive_skill_id"]])
    state["learned_skills"] = list(set(state["learned_skills"]))
    
    # 設定好裝備
    job_key = {
        "劍士": "warrior",
        "法師": "mage",
        "盜賊": "rogue",
        "牧師": "cleric"
    }[base_job]
    
    gear_set = BEST_GEAR[region][job_key]
    for slot, item_id in gear_set.items():
        state["equipment"][slot] = item_id
        
    # 重置 HP/MP 至滿值
    stats = get_stats(state)
    state["current_hp"] = stats["max_hp"]
    state["current_mp"] = stats["max_mp"]
    
    # 給予聖瓶 (如果是聖蝕司祭)
    if promo_id == "promotion_holy_eclipse":
        add_item(state, "item_sanctified_ash_vial", 5)
        
    return state

# 戰鬥模擬 AI 選擇行為
def choose_combat_action(state: dict, enemy: dict, enemy_hp: int, turn: int, player_buffs: dict, enemy_buffs: dict) -> tuple[str, dict | None]:
    promo_id = state.get("promotion_id")
    stats = get_stats(state, player_buffs)
    
    if promo_id == "promotion_blood_blade":
        # 血鋒鬥士：有蓄力就放蓄力斬，沒蓄力且 HP 足夠就放主動 buff
        hp_cost = int(stats["max_hp"] * 0.15)
        has_charge = player_buffs.get("physical_charge", 0) > 0
        if has_charge:
            return "use_skill", SKILLS["skill_earth_05"] # 標準物理蓄力斬
        elif state["current_hp"] > hp_cost and player_buffs.get("blood_blade_active", 0) < 3:
            return "use_skill", SKILLS["skill_blood_blade_strike"]
            
    elif promo_id == "promotion_blood_armor":
        # 血鎧守衛：主動 buff 未滿且 HP 足夠就放主動 buff
        hp_cost = int(stats["max_hp"] * 0.15)
        max_stk = 4 if "skill_blood_armor_passive" in state["learned_skills"] else 3
        if state["current_hp"] > hp_cost and player_buffs.get("blood_armor_active", 0) < max_stk:
            return "use_skill", SKILLS["skill_blood_armor_shield"]
            
    elif promo_id == "promotion_star_fracture":
        # 星裂術士：若有 MP 且敵人有弱點，放星裂術，否則普攻
        # 決定星裂術屬性
        element = "火" if enemy["element"] == "冰" else "冰"
        if state["current_mp"] >= 12:
            skill = {**SKILLS["skill_star_fracture"], "element": element}
            return "use_skill", skill
            
    elif promo_id == "promotion_sigil_mage":
        # 印紋術士：若目標沒有印紋，放印紋術；否則放與印紋同元素的傷害魔法觸發引爆
        if not enemy_buffs.get("sigil_mage_mark") and state["current_mp"] >= 6:
            skill = {**SKILLS["skill_sigil_mage"], "element": "火"}
            return "use_skill", skill
        elif enemy_buffs.get("sigil_mage_mark") and state["current_mp"] >= 6:
            # 放火球術引爆
            return "use_skill", SKILLS["skill_arcane_bolt"]
            
    elif promo_id == "promotion_shadow_slayer":
        # 斷影刺客：敵方生命低於 40% 時，放斷影處決；否則普攻
        enemy_ratio = enemy_hp / enemy["hp"]
        if enemy_ratio < 0.40 and state["current_mp"] >= 6:
            return "use_skill", SKILLS["skill_shadow_slayer_execute"]
            
    elif promo_id == "promotion_miasma_hunter":
        # 瘴痕獵手：若目標有 bleed/poison 放瘴痕打擊，否則進行普攻以施加狀態
        enemy_has_status = enemy_buffs.get("bleed", 0) > 0 or enemy_buffs.get("poison", 0) > 0
        if enemy_has_status and state["current_mp"] >= 6:
            return "use_skill", SKILLS["skill_miasma_strike"]
            
    elif promo_id == "promotion_holy_veil":
        # 聖幕司祭：護盾消失了就建立護盾，否則普攻
        if not player_buffs.get("holy_veil_shield") and state["current_mp"] >= 6:
            return "use_skill", SKILLS["skill_holy_veil_barrier"]
            
    elif promo_id == "promotion_holy_eclipse":
        # 聖蝕司祭：再生和聖蝕 DoT 沒了就放主動，否則普攻
        if not player_buffs.get("regeneration") and state["current_mp"] >= 10:
            return "use_skill", SKILLS["skill_holy_eclipse_cast"]

    # 預設普攻
    return "attack", None

# 模擬單場戰鬥
def simulate_battle(state: dict, enemy_id: str) -> bool:
    enemy = deepcopy(MONSTERS[enemy_id])
    enemy_hp = enemy["hp"]
    player_buffs = {}
    enemy_buffs = {}
    
    # 聖蝕聖瓶初始計數
    initial_vials = state.get("inventory", {}).get("item_sanctified_ash_vial", 0)
    
    turn = 1
    max_turns = 100
    
    while state["current_hp"] > 0 and enemy_hp > 0 and turn <= max_turns:
        # 同步敵人當前 HP
        enemy["current_hp"] = enemy_hp
        
        # 玩家行動
        act_type, skill = choose_combat_action(state, enemy, enemy_hp, turn, player_buffs, enemy_buffs)
        
        if act_type == "use_skill" and skill:
            # 扣 MP
            state["current_mp"] -= skill["mp"]
            # 執行技能
            res = game.execute_skill(state, enemy, skill.get("id", ""), skill, player_buffs, enemy_buffs)
            
            # 若為傷害技能，扣減敵人 HP
            # 在 execute_skill 內部呼叫 player_attack 時會產生 damage
            # 我們可以藉由模擬 player_attack 產生的 action_result 來扣減 enemy_hp
            # 為了讓模擬完全走通，我們可以攔截 player_attack：
            # player_attack 會在 res.events 或 buffs 裡，但它對敵人的傷害可以直接由我們在模擬中計算：
            if skill["kind"] == "damage":
                damage, _ = game.calc_player_damage(state, enemy, skill, player_buffs, enemy_buffs)
                enemy_hp -= damage
        else:
            # 普攻
            damage, _ = game.calc_player_damage(state, enemy, None, player_buffs, enemy_buffs)
            enemy_hp -= damage
            
        if enemy_hp <= 0:
            break
            
        # 敵方行動
        # 重置反震限制
        player_buffs.pop("_holy_veil_reflected_this_action", None)
        
        # 敵方傷害
        damage = game.calc_enemy_damage(enemy, state, 1.0, enemy["element"], player_buffs, False)
        state["current_hp"] -= damage
        
        # 反震傷害
        reflect_damage = player_buffs.pop("_reflect_damage_queue", 0)
        if reflect_damage > 0:
            enemy_hp -= reflect_damage
            
        if enemy_hp <= 0:
            break
            
        # 狀態 tick
        res_events, dot_damage = game.tick_effects(state, player_buffs, enemy_buffs, enemy)
        enemy_hp -= dot_damage
        
        turn += 1
        
    won = state["current_hp"] > 0 and enemy_hp <= 0
    
    # 聖瓶返還
    if won and state.get("promotion_id") == "promotion_holy_eclipse" and player_buffs.get("_holy_eclipse_vial_marked"):
        current_vials = state.get("inventory", {}).get("item_sanctified_ash_vial", 0)
        if current_vials < initial_vials:
            add_item(state, "item_sanctified_ash_vial", 1)
            
    return won

# 量測與 Focused Tests 執行
def run_measurements():
    # 固定隨機種子以確保 determinism
    random.seed(42)
    
    regions = ["earth", "thunder", "final"]
    monsters_by_region = {
        "earth": ["mon_earth_rootling_scavenger", "boss_earth_rootwarden"],
        "thunder": ["mon_thunder_static_lizard", "boss_thunder_plateau_beacon"],
        "final": ["mon_final_ash_echo", "boss_final_echo_vanguard"]
    }
    
    print("======================================================================")
    print("           正式轉職 v1 戰鬥平衡與量測報告 (Focused Tests)")
    print("======================================================================")
    
    for region in regions:
        print(f"\n【區域：{region.upper()}】")
        for promo_id, promo in PROMOTIONS.items():
            for monster_id in monsters_by_region[region]:
                wins = 0
                sim_count = 50
                
                # 執行 50 次模擬以計算勝率
                for _ in range(sim_count):
                    state = build_promoted_state(promo_id, region)
                    if simulate_battle(state, monster_id):
                        wins += 1
                        
                win_rate = (wins / sim_count) * 100
                print(f" - 晉升: {promo['name']:<8} vs {monster_id:<18} -> 勝率: {win_rate:>5.1f}%")

if __name__ == "__main__":
    run_measurements()
