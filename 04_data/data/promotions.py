from __future__ import annotations

PROMOTIONS = {
    # 劍士 -> 血鋒鬥士
    "promotion_blood_blade": {
        "source_job": "劍士",
        "name": "血鋒鬥士",
        "summary": "扣除最大 HP 比例獲得血戰層數，大幅強化 Physical Charge 爆發的極端進攻路線。",
        "active_skill_id": "skill_blood_blade_strike",
        "passive_skill_id": "skill_blood_blade_passive",
        "requirements": [
            {"kind": "quest", "key": "quest_ice_return_handoff", "label": "完成任務「寒冰歸來手尾」"},
            {"kind": "level", "value": 18, "label": "角色等級達 Lv18"},
        ],
        "status": "formal",
        "config": {
            "hp_cost_percent": 15,
            "max_stacks": 3,
            "charge_bonus_per_stack": 0.12,  # 每層血戰使 Charge 傷害加乘額外提升 12%
        }
    },
    # 劍士 -> 血鎧守衛
    "promotion_blood_armor": {
        "source_job": "劍士",
        "name": "血鎧守衛",
        "summary": "扣除最大 HP 比例獲得血鎧，獲得極高物理與魔法防禦的防守路線。",
        "active_skill_id": "skill_blood_armor_shield",
        "passive_skill_id": "skill_blood_armor_passive",
        "requirements": [
            {"kind": "quest", "key": "quest_ice_return_handoff", "label": "完成任務「寒冰歸來手尾」"},
            {"kind": "level", "value": 18, "label": "角色等級達 Lv18"},
        ],
        "status": "formal",
        "config": {
            "hp_cost_percent": 15,
            "max_stacks_base": 3,
            "max_stacks_with_passive": 4,
            "defense_percent_per_stack_base": 20,
            "defense_percent_per_stack_passive": 25,
        }
    },
    # 法師 -> 星裂術士
    "promotion_star_fracture": {
        "source_job": "法師",
        "name": "星裂術士",
        "summary": "選定已學元素進行高 MP 消耗的單次大爆發傷害，極限放大元素弱點乘數。",
        "active_skill_id": "skill_star_fracture",
        "passive_skill_id": "skill_star_fracture_passive",
        "requirements": [
            {"kind": "quest", "key": "quest_ice_return_handoff", "label": "完成任務「寒冰歸來手尾」"},
            {"kind": "level", "value": 18, "label": "角色等級達 Lv18"},
        ],
        "status": "formal",
        "config": {
            "mp_cost": 12,
            "multiplier": 2.2,
            "weakness_multiplier_bonus": 0.25,  # 契合弱點時傷害提升 25%
            "weakness_mp_refund": 6,          # 契合弱點時回復 6 MP
        }
    },
    # 法師 -> 印紋術士
    "promotion_sigil_mage": {
        "source_job": "法師",
        "name": "印紋術士",
        "summary": "在目標身上標記元素印記，再次以同元素技能命中時引爆額外無屬性魔法傷害。",
        "active_skill_id": "skill_sigil_mage",
        "passive_skill_id": "skill_sigil_mage_passive",
        "requirements": [
            {"kind": "quest", "key": "quest_ice_return_handoff", "label": "完成任務「寒冰歸來手尾」"},
            {"kind": "level", "value": 18, "label": "角色等級達 Lv18"},
        ],
        "status": "formal",
        "config": {
            "mp_cost": 6,
            "duration": 5,
            "detonate_multiplier": 1.2,  # 引爆時造成 1.2 * 魔攻的額外傷害
        }
    },
    # 盜賊 -> 斷影刺客
    "promotion_shadow_slayer": {
        "source_job": "盜賊",
        "name": "斷影刺客",
        "summary": "針對低生命目標進行致命處決，並在目標低生命時獲得高暴擊與暴擊傷害提升。",
        "active_skill_id": "skill_shadow_slayer_execute",
        "passive_skill_id": "skill_shadow_slayer_passive",
        "requirements": [
            {"kind": "quest", "key": "quest_ice_return_handoff", "label": "完成任務「寒冰歸來手尾」"},
            {"kind": "level", "value": 18, "label": "角色等級達 Lv18"},
        ],
        "status": "formal",
        "config": {
            "mp_cost": 6,
            "base_multiplier": 1.4,
            "execute_multiplier": 2.8,
            "threshold_hp_percent": 40,
            "passive_crit_bonus": 25,
            "passive_crit_damage_percent": 50,
        }
    },
    # 盜賊 -> 瘴痕獵手
    "promotion_miasma_hunter": {
        "source_job": "盜賊",
        "name": "瘴痕獵手",
        "summary": "利用敵人已有的流血或中毒狀態，不消耗或刷新狀態，造成額外追擊與常駐增增傷。",
        "active_skill_id": "skill_miasma_strike",
        "passive_skill_id": "skill_miasma_hunter_passive",
        "requirements": [
            {"kind": "quest", "key": "quest_ice_return_handoff", "label": "完成任務「寒冰歸來手尾」"},
            {"kind": "level", "value": 18, "label": "角色等級達 Lv18"},
        ],
        "status": "formal",
        "config": {
            "mp_cost": 6,
            "base_multiplier": 1.2,
            "multiplier_bonus_per_status": 0.6,
            "passive_damage_bonus_percent": 15,
        }
    },
    # 牧師 -> 聖幕司祭
    "promotion_holy_veil": {
        "source_job": "牧師",
        "name": "聖幕司祭",
        "summary": "主動建立能吸收直接傷害的護盾，並在護盾實際吸收傷害時對攻擊者進行神聖反震。",
        "active_skill_id": "skill_holy_veil_barrier",
        "passive_skill_id": "skill_holy_veil_passive",
        "requirements": [
            {"kind": "quest", "key": "quest_ice_return_handoff", "label": "完成任務「寒冰歸來手尾」"},
            {"kind": "level", "value": 18, "label": "角色等級達 Lv18"},
        ],
        "status": "formal",
        "config": {
            "mp_cost": 8,
            "shield_base": 40,
            "shield_multiplier": 1.5,
            "passive_capacity_bonus_percent": 25,
            "reflect_multiplier": 0.8,
        }
    },
    # 牧師 -> 聖蝕司祭
    "promotion_holy_eclipse": {
        "source_job": "牧師",
        "name": "聖蝕司祭",
        "summary": "一回合同時建立或刷新聖蝕持續傷害與再生，並在勝利後返還消耗的聖蝕聖瓶。",
        "active_skill_id": "skill_holy_eclipse_cast",
        "passive_skill_id": "skill_holy_eclipse_passive",
        "requirements": [
            {"kind": "quest", "key": "quest_ice_return_handoff", "label": "完成任務「寒冰歸來手尾」"},
            {"kind": "level", "value": 18, "label": "角色等級達 Lv18"},
        ],
        "status": "formal",
        "config": {
            "mp_cost": 10,
            "duration": 5,
            "dot_multiplier": 0.6,
            "regen_amount": 6,
            "regen_multiplier": 0.45,
            "passive_dot_boost_percent": 30,
        }
    },
}
