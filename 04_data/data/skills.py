from __future__ import annotations



SKILLS = {
    "skill_power_slash": {
        "name": "重斬",
        "mp": 4,
        "kind": "damage",
        "stat": "attack",
        "element": "物理",
        "multiplier": 1.3125,
        "charge_bonus_per_stack": 0.08,
        "desc": "物理傷害，倍率 1.25。",
    },
    "skill_arcane_bolt": {
        "name": "秘光彈",
        "mp": 4,
        "kind": "damage",
        "stat": "magic",
        "element": "無",
        "multiplier": 0.564,
        "desc": "無屬性魔法傷害，倍率 1.2。",
    },
    "skill_backstab": {
        "name": "背刺",
        "mp": 4,
        "kind": "damage",
        "stat": "attack",
        "element": "物理",
        "multiplier": 1.15,
        "crit_bonus": 10,
        "on_hit": {"status": "bleed", "duration": 3, "chance": 70, "multiplier": 0.45, "damage_type": "physical"},
        "desc": "高命中物理傷害，暴擊 +10%；命中後可附加流血，每回合造成自身攻擊力 ×45% 的物理狀態傷害，持續 3 回合。",
    },
    "skill_blessed_touch": {
        "name": "祝禱",
        "mp": 5,
        "kind": "heal",
        "amount": 30,
        "multiplier": 1.5,
        "desc": "回復 HP 30。",
    },
    "skill_toxic_edge": {
        "name": "毒刃",
        "mp": 5,
        "kind": "damage",
        "stat": "attack",
        "element": "物理",
        "multiplier": 0.9,
        "on_hit": {"status": "poison", "duration": 5, "chance": 65, "multiplier": 0.35, "damage_type": "physical"},
        "desc": "造成物理傷害，並有機率附加中毒；每回合造成自身攻擊力 ×35% 的物理狀態傷害，持續 5 回合。",
    },
    "skill_sanctified_decay": {
        "name": "聖蝕",
        "mp": 7,
        "kind": "dot",
        "stat": "magic",
        "element": "無",
        "duration": 5,
        "multiplier": 0.55,
        "desc": "必定施加持續魔法傷害 5 回合。",
    },
    "skill_regeneration": {
        "name": "再生祈禱",
        "mp": 8,
        "kind": "regen",
        "duration": 5,
        "amount": 6,
        "multiplier": 0.45,
        "desc": "必定施加持續回復 5 回合。",
    },
    "skill_spark": {
        "name": "火花術",
        "mp": 5,
        "kind": "damage",
        "stat": "magic",
        "element": "火",
        "multiplier": 0.588,
        "desc": "火屬性小傷害。",
    },
    "skill_ice_needle": {
        "name": "冰針術",
        "mp": 6,
        "kind": "damage",
        "stat": "magic",
        "element": "冰",
        "multiplier": 0.635,
        "desc": "冰屬性小傷害，對火屬敵人有效。",
    },
    "skill_minor_heal": {
        "name": "小治癒術",
        "mp": 7,
        "kind": "heal",
        "amount": 45,
        "desc": "回復 HP 45。",
    },
    "skill_quickstep": {
        "name": "迅步術",
        "mp": 0,
        "kind": "passive",
        "passive_triggers": [
            {
                "job": "劍士",
                "event": "physical_charge_reaches",
                "requires": {"stacks": 3},
                "effect": {"kind": "charge_skill_bonus", "state_key": "warrior_quickstep_ready", "damage_percent": 25},
            },
            {
                "job": "盜賊",
                "event": "physical_status_applied",
                "requires": {"statuses": ["bleed", "poison"]},
                "replacement_group": "rogue_pursuit",
                "priority": 1,
                "effect": {"kind": "extra_normal_followup", "state_key": "rogue_pursuit", "uses": 1, "followup_multiplier": 1.0},
            },
        ],
        "desc": "被動：劍士滿層蓄力後強化下一次蓄力技能；盜賊成功附加流血或中毒後獲得一次追擊。",
    },
    "skill_cinder_mark": {
        "name": "燼印術",
        "mp": 9,
        "kind": "debuff",
        "debuff": "cinder_mark",
        "duration": 5,
        "damage_percent": 50,
        "damage_scope": "elemental_magic",
        "desc": "5 回合使敵人受到的直接元素魔法傷害 +50%。",
    },
    # === Ice Region Skills ===
    "skill_ice_01": {
        "name": "冰刃術",
        "mp": 7,
        "kind": "damage",
        "stat": "magic",
        "element": "冰",
        "multiplier": 0.658,
        "desc": "冰屬性魔法傷害。",
    },
    "skill_ice_02": {
        "name": "冰療術",
        "mp": 8,
        "kind": "heal",
        "amount": 60,
        "desc": "回復 HP 60。",
    },
    "skill_ice_04": {
        "name": "冰斬術",
        "mp": 6,
        "kind": "damage",
        "stat": "attack",
        "element": "冰",
        "multiplier": 1.3,
        "charge_bonus_per_stack": 0.10,
        "desc": "冰屬性物理傷害。",
    },
    "skill_ice_05": {
        "name": "霜速術",
        "mp": 0,
        "kind": "passive",
        "passive_triggers": [
            {
                "job": "盜賊",
                "event": "physical_status_applied",
                "requires": {"statuses": ["bleed", "poison"]},
                "replacement_group": "rogue_pursuit",
                "priority": 2,
                "effect": {"kind": "extra_normal_followup", "state_key": "rogue_pursuit", "uses": 1, "followup_multiplier": 1.5},
            },
        ],
        "desc": "被動：取代迅步追擊；成功附加流血或中毒後，下一次普通攻擊追加更強追擊。",
    },
    # === Earth Region Skills ===
    "skill_earth_01": {
        "name": "落石術",
        "mp": 8,
        "kind": "damage",
        "stat": "magic",
        "element": "自然",
        "multiplier": 0.495,
        "desc": "土屬性魔法傷害。",
    },
    "skill_earth_02": {
        "name": "地沙術",
        "mp": 9,
        "kind": "damage",
        "stat": "magic",
        "element": "自然",
        "multiplier": 0.528,
        "desc": "土屬性重度魔法傷害。",
    },
    "skill_earth_03": {
        "name": "大地療育",
        "mp": 10,
        "kind": "heal",
        "amount": 80,
        "desc": "回復 HP 80。",
    },
    "skill_earth_05": {
        "name": "石裂斬",
        "mp": 8,
        "kind": "damage",
        "stat": "attack",
        "element": "自然",
        "multiplier": 1.45,
        "charge_bonus_per_stack": 0.12,
        "desc": "土屬性物理傷害。",
    },
    "skill_earth_06": {
        "name": "深根毒刺",
        "mp": 9,
        "kind": "damage",
        "stat": "attack",
        "element": "自然",
        "multiplier": 1.35,
        "desc": "土屬性物理傷害，附帶劇毒效果。",
    },
    # === Thunder Region Skills ===
    "skill_thunder_01": {
        "name": "電弧術",
        "mp": 10,
        "kind": "damage",
        "stat": "magic",
        "element": "雷",
        "multiplier": 0.752,
        "desc": "雷屬性魔法傷害。",
    },
    "skill_thunder_02": {
        "name": "狂雷術",
        "mp": 12,
        "kind": "damage",
        "stat": "magic",
        "element": "雷",
        "multiplier": 0.87,
        "desc": "雷屬性高階魔法傷害。",
    },
    "skill_thunder_03": {
        "name": "閃電之光",
        "mp": 12,
        "kind": "heal",
        "amount": 110,
        "desc": "高階神聖回復 HP 110。",
    },
    "skill_thunder_05": {
        "name": "迅雷斬",
        "mp": 10,
        "kind": "damage",
        "stat": "attack",
        "element": "雷",
        "multiplier": 2.08,
        "charge_bonus_per_stack": 0.14,
        "desc": "雷屬性物理斬擊傷害。",
    },
    "skill_thunder_06": {
        "name": "雷閃步",
        "mp": 10,
        "kind": "buff",
        "buff": "quickstep",
        "duration": 3,
        "desc": "3 回合敏捷 +30%。",
    },
    # === Final Region Skills ===
    "skill_final_01": {
        "name": "虛空衝擊",
        "mp": 15,
        "kind": "damage",
        "stat": "magic",
        "element": "無",
        "multiplier": 0.893,
        "desc": "虛空屬性高階魔法傷害。",
    },
    "skill_final_02": {
        "name": "深淵黑洞",
        "mp": 20,
        "kind": "damage",
        "stat": "magic",
        "element": "無",
        "multiplier": 1.081,
        "desc": "深淵禁忌魔法，大範圍高階魔法傷害。",
    },
    "skill_final_03": {
        "name": "聖暗雙重",
        "mp": 16,
        "kind": "heal",
        "amount": 160,
        "desc": "終極神聖回復 HP 160。",
    },
    "skill_final_05": {
        "name": "深淵霸斬",
        "mp": 15,
        "kind": "damage",
        "stat": "attack",
        "element": "物理",
        "multiplier": 3.6,
        "charge_bonus_per_stack": 0.16,
        "desc": "深淵物理霸斬傷害。",
    },
    "skill_final_06": {
        "name": "虛空瞬步",
        "mp": 14,
        "kind": "buff",
        "buff": "quickstep",
        "duration": 4,
        "desc": "4 回合敏捷 +30%。",
    },
}



MAGIC_BOOKS = {
    "book_spark": {
        "name": "火花術書",
        "jobs": ["法師", "牧師"],
        "level": 2,
        "price": 180,
        "materials": {"mat_small_crystal": 1},
        "skill": "skill_spark",
    },
    "book_ice_needle": {
        "name": "冰針術書",
        "jobs": ["法師"],
        "level": 3,
        "price": 220,
        "materials": {"mat_small_crystal": 2},
        "skill": "skill_ice_needle",
    },
    "book_minor_heal": {
        "name": "小治癒術書",
        "jobs": ["牧師"],
        "level": 2,
        "price": 200,
        "materials": {"mat_moss_fiber": 2},
        "skill": "skill_minor_heal",
    },
    "book_quickstep": {
        "name": "迅步術書",
        "jobs": ["盜賊", "劍士"],
        "level": 3,
        "price": 240,
        "materials": {"mat_moss_fiber": 2},
        "skill": "skill_quickstep",
    },
    "book_cinder_mark": {
        "name": "燼印術書",
        "jobs": ["法師"],
        "level": 6,
        "price": 460,
        "materials": {"mat_ice_blue_stone": 2},
        "skill": "skill_cinder_mark",
        "region": "ice",
    },
    # === Ice Region Magic Books ===
    "book_ice_01": {
        "name": "冰刃術書",
        "jobs": ["法師"],
        "level": 6,
        "price": 400,
        "materials": {"mat_ice_salt": 3},
        "skill": "skill_ice_01",
        "region": "ice",
    },
    "book_ice_02": {
        "name": "冰療術書",
        "jobs": ["牧師"],
        "level": 6,
        "price": 420,
        "materials": {"mat_ice_saltcloth": 2},
        "skill": "skill_ice_02",
        "region": "ice",
    },
    "book_ice_04": {
        "name": "冰斬術書",
        "jobs": ["劍士"],
        "level": 7,
        "price": 450,
        "materials": {"mat_ice_frostroot": 2},
        "skill": "skill_ice_04",
        "region": "ice",
    },
    "book_ice_05": {
        "name": "霜速術書",
        "jobs": ["盜賊"],
        "level": 7,
        "price": 460,
        "materials": {"mat_ice_blue_stone": 2},
        "skill": "skill_ice_05",
        "region": "ice",
    },
    # === Earth Region Magic Books ===
    "book_earth_01": {
        "name": "落石術書",
        "jobs": ["法師"],
        "level": 11,
        "price": 600,
        "materials": {"mat_earth_moss_loam": 3},
        "skill": "skill_earth_01",
        "region": "earth",
    },
    "book_earth_02": {
        "name": "地沙術書",
        "jobs": ["法師"],
        "level": 12,
        "price": 620,
        "materials": {"mat_earth_rootfiber": 2},
        "skill": "skill_earth_02",
        "region": "earth",
    },
    "book_earth_03": {
        "name": "大地療育書",
        "jobs": ["牧師"],
        "level": 11,
        "price": 650,
        "materials": {"mat_earth_spore_cap": 2},
        "skill": "skill_earth_03",
        "region": "earth",
    },
    "book_earth_05": {
        "name": "石裂斬術書",
        "jobs": ["劍士"],
        "level": 12,
        "price": 700,
        "materials": {"mat_earth_petrified_bark": 2},
        "skill": "skill_earth_05",
        "region": "earth",
    },
    "book_earth_06": {
        "name": "深根毒刺書",
        "jobs": ["盜賊"],
        "level": 12,
        "price": 720,
        "materials": {"mat_earth_leyline_shard": 2},
        "skill": "skill_earth_06",
        "region": "earth",
    },
    # === Thunder Region Magic Books ===
    "book_thunder_01": {
        "name": "電弧術書",
        "jobs": ["法師"],
        "level": 16,
        "price": 900,
        "materials": {"mat_thunder_charge_sand": 3},
        "skill": "skill_thunder_01",
        "region": "thunder",
    },
    "book_thunder_02": {
        "name": "狂雷術書",
        "jobs": ["法師"],
        "level": 17,
        "price": 950,
        "materials": {"mat_thunder_copper_vein": 2},
        "skill": "skill_thunder_02",
        "region": "thunder",
    },
    "book_thunder_03": {
        "name": "閃電之光書",
        "jobs": ["牧師"],
        "level": 16,
        "price": 980,
        "materials": {"mat_thunder_stormglass": 2},
        "skill": "skill_thunder_03",
        "region": "thunder",
    },
    "book_thunder_05": {
        "name": "迅雷斬術書",
        "jobs": ["劍士"],
        "level": 17,
        "price": 1050,
        "materials": {"mat_thunder_conductor_rod": 2},
        "skill": "skill_thunder_05",
        "region": "thunder",
    },
    "book_thunder_06": {
        "name": "雷閃步術書",
        "jobs": ["盜賊"],
        "level": 17,
        "price": 1080,
        "materials": {"mat_thunder_cloud_essence": 2},
        "skill": "skill_thunder_06",
        "region": "thunder",
    },
    # === Final Region Magic Books ===
    "book_final_01": {
        "name": "虛空衝擊書",
        "jobs": ["法師"],
        "level": 21,
        "price": 1500,
        "materials": {"mat_final_echo_ash": 3},
        "skill": "skill_final_01",
        "region": "final",
    },
    "book_final_02": {
        "name": "深淵黑洞書",
        "jobs": ["法師"],
        "level": 23,
        "price": 1600,
        "materials": {"mat_final_frost_memory": 2},
        "skill": "skill_final_02",
        "region": "final",
    },
    "book_final_03": {
        "name": "聖暗雙重書",
        "jobs": ["牧師"],
        "level": 21,
        "price": 1550,
        "materials": {"mat_final_root_stone": 2},
        "skill": "skill_final_03",
        "region": "final",
    },
    "book_final_05": {
        "name": "深淵霸斬書",
        "jobs": ["劍士"],
        "level": 23,
    },
    # === Ice Region Magic Books ===
    "book_ice_01": {
        "name": "冰刃術書",
        "jobs": ["法師"],
        "level": 6,
        "price": 400,
        "materials": {"mat_ice_salt": 3},
        "skill": "skill_ice_01",
        "region": "ice",
    },
    "book_ice_02": {
        "name": "冰療術書",
        "jobs": ["牧師"],
        "level": 6,
        "price": 420,
        "materials": {"mat_ice_saltcloth": 2},
        "skill": "skill_ice_02",
        "region": "ice",
    },
    "book_ice_04": {
        "name": "冰斬術書",
        "jobs": ["劍士"],
        "level": 7,
        "price": 450,
        "materials": {"mat_ice_frostroot": 2},
        "skill": "skill_ice_04",
        "region": "ice",
    },
    "book_ice_05": {
        "name": "霜速術書",
        "jobs": ["盜賊"],
        "level": 7,
        "price": 460,
        "materials": {"mat_ice_blue_stone": 2},
        "skill": "skill_ice_05",
        "region": "ice",
    },
    # === Earth Region Magic Books ===
    "book_earth_01": {
        "name": "落石術書",
        "jobs": ["法師"],
        "level": 11,
        "price": 600,
        "materials": {"mat_earth_moss_loam": 3},
        "skill": "skill_earth_01",
        "region": "earth",
    },
    "book_earth_02": {
        "name": "地沙術書",
        "jobs": ["法師"],
        "level": 12,
        "price": 620,
        "materials": {"mat_earth_rootfiber": 2},
        "skill": "skill_earth_02",
        "region": "earth",
    },
    "book_earth_03": {
        "name": "大地療育書",
        "jobs": ["牧師"],
        "level": 11,
        "price": 650,
        "materials": {"mat_earth_spore_cap": 2},
        "skill": "skill_earth_03",
        "region": "earth",
    },
    "book_earth_05": {
        "name": "石裂斬術書",
        "jobs": ["劍士"],
        "level": 12,
        "price": 700,
        "materials": {"mat_earth_petrified_bark": 2},
        "skill": "skill_earth_05",
        "region": "earth",
    },
    "book_earth_06": {
        "name": "深根毒刺書",
        "jobs": ["盜賊"],
        "level": 12,
        "price": 720,
        "materials": {"mat_earth_leyline_shard": 2},
        "skill": "skill_earth_06",
        "region": "earth",
    },
    # === Thunder Region Magic Books ===
    "book_thunder_01": {
        "name": "電弧術書",
        "jobs": ["法師"],
        "level": 16,
        "price": 900,
        "materials": {"mat_thunder_charge_sand": 3},
        "skill": "skill_thunder_01",
        "region": "thunder",
    },
    "book_thunder_02": {
        "name": "狂雷術書",
        "jobs": ["法師"],
        "level": 17,
        "price": 950,
        "materials": {"mat_thunder_copper_vein": 2},
        "skill": "skill_thunder_02",
        "region": "thunder",
    },
    "book_thunder_03": {
        "name": "閃電之光書",
        "jobs": ["牧師"],
        "level": 16,
        "price": 980,
        "materials": {"mat_thunder_stormglass": 2},
        "skill": "skill_thunder_03",
        "region": "thunder",
    },
    "book_thunder_05": {
        "name": "迅雷斬術書",
        "jobs": ["劍士"],
        "level": 17,
        "price": 1050,
        "materials": {"mat_thunder_conductor_rod": 2},
        "skill": "skill_thunder_05",
        "region": "thunder",
    },
    "book_thunder_06": {
        "name": "雷閃步術書",
        "jobs": ["盜賊"],
        "level": 17,
        "price": 1080,
        "materials": {"mat_thunder_cloud_essence": 2},
        "skill": "skill_thunder_06",
        "region": "thunder",
    },
    # === Final Region Magic Books ===
    "book_final_01": {
        "name": "虛空衝擊書",
        "jobs": ["法師"],
        "level": 21,
        "price": 1500,
        "materials": {"mat_final_echo_ash": 3},
        "skill": "skill_final_01",
        "region": "final",
    },
    "book_final_02": {
        "name": "深淵黑洞書",
        "jobs": ["法師"],
        "level": 23,
        "price": 1600,
        "materials": {"mat_final_frost_memory": 2},
        "skill": "skill_final_02",
        "region": "final",
    },
    "book_final_03": {
        "name": "聖暗雙重書",
        "jobs": ["牧師"],
        "level": 21,
        "price": 1550,
        "materials": {"mat_final_root_stone": 2},
        "skill": "skill_final_03",
        "region": "final",
    },
    "book_final_05": {
        "name": "深淵霸斬書",
        "jobs": ["劍士"],
        "level": 23,
        "price": 1800,
        "materials": {"mat_final_void_shard": 2},
        "skill": "skill_final_05",
        "region": "final",
    },
    "book_final_06": {
        "name": "虛空瞬步書",
        "jobs": ["盜賊"],
        "level": 23,
        "price": 1850,
        "materials": {"mat_final_seal_core": 2},
        "skill": "skill_final_06",
        "region": "final",
    },
}


# Balance adjustment for fluid combat (Warrior/Mage/Rogue/Cleric buffs)
SKILLS["skill_power_slash"]["charge_bonus_per_stack"] = 0.15
SKILLS["skill_ice_04"]["charge_bonus_per_stack"] = 0.20
SKILLS["skill_earth_05"]["charge_bonus_per_stack"] = 0.25
SKILLS["skill_thunder_05"]["charge_bonus_per_stack"] = 0.30
SKILLS["skill_final_05"]["charge_bonus_per_stack"] = 0.35

SKILLS["skill_arcane_bolt"]["mp"] = 3
SKILLS["skill_spark"]["mp"] = 4
SKILLS["skill_ice_needle"]["mp"] = 4
SKILLS["skill_ice_01"]["mp"] = 5
SKILLS["skill_earth_01"]["mp"] = 6
SKILLS["skill_earth_02"]["mp"] = 7
SKILLS["skill_thunder_01"]["mp"] = 8
SKILLS["skill_thunder_02"]["mp"] = 10
SKILLS["skill_final_01"]["mp"] = 12
SKILLS["skill_final_02"]["mp"] = 15

SKILLS["skill_backstab"]["on_hit"]["multiplier"] = 0.60
SKILLS["skill_toxic_edge"]["on_hit"]["multiplier"] = 0.50

# Rogue passive followup multipliers
for trigger in SKILLS["skill_quickstep"]["passive_triggers"]:
    if trigger.get("job") == "盜賊":
        trigger["effect"]["followup_multiplier"] = 1.2
for trigger in SKILLS["skill_ice_05"]["passive_triggers"]:
    if trigger.get("job") == "盜賊":
        trigger["effect"]["followup_multiplier"] = 1.8

# Cleric adjustments
SKILLS["skill_sanctified_decay"]["multiplier"] = 0.70
SKILLS["skill_regeneration"]["amount"] = 10


# === Formal Promotion v1 Skills ===
SKILLS.update({
    # 劍士 - 血鋒鬥士
    "skill_blood_blade_strike": {
        "name": "血鋒本戰",
        "mp": 0,
        "kind": "buff",
        "buff": "blood_blade_active",
        "duration": 99,
        "desc": "消耗 15% 最大 HP 獲得 1 層血戰狀態，提升 Physical Charge 爆發傷害（上限 3 層）。不可自殺。"
    },
    "skill_blood_blade_passive": {
        "name": "血鋒本能",
        "mp": 0,
        "kind": "passive",
        "desc": "被動：擁有血戰層數時，每層使蓄力技能傷害倍率額外提升 12%。"
    },
    # 劍士 - 血鎧守衛
    "skill_blood_armor_shield": {
        "name": "血鎧護衛",
        "mp": 0,
        "kind": "buff",
        "buff": "blood_armor_active",
        "duration": 99,
        "desc": "消耗 15% 最大 HP 獲得 1 層血鎧狀態，提升防禦力（上限 3/4 層）。不可自殺。"
    },
    "skill_blood_armor_passive": {
        "name": "堅毅血鎧",
        "mp": 0,
        "kind": "passive",
        "desc": "被動：血鎧最大上限 +1 且每層提升的防禦力提高。"
    },
    # 法師 - 星裂術士
    "skill_star_fracture": {
        "name": "星裂術",
        "mp": 12,
        "kind": "damage",
        "desc": "消耗高 MP 施放已學元素的單次大爆發傷害。"
    },
    "skill_star_fracture_passive": {
        "name": "星裂回報",
        "mp": 0,
        "kind": "passive",
        "desc": "被動：若星裂術契合敵方弱點元素，傷害提升 25% 且回復 6 MP。"
    },
    # 法師 - 印紋術士
    "skill_sigil_mage": {
        "name": "印紋術",
        "mp": 6,
        "kind": "debuff",
        "debuff": "sigil_mage_mark",
        "duration": 5,
        "desc": "對目標施加已學元素的印記，同元素再次命中時引爆大額額外傷害並清除印記。"
    },
    "skill_sigil_mage_passive": {
        "name": "印紋引爆",
        "mp": 0,
        "kind": "passive",
        "desc": "被動：同元素技能命中印記目標時引爆額外無屬性傷害，並清除印記。"
    },
    # 盜賊 - 斷影刺客
    "skill_shadow_slayer_execute": {
        "name": "斷影處決",
        "mp": 6,
        "kind": "damage",
        "desc": "物理傷害，對低生命（<40% HP）目標造成雙倍處決傷害。"
    },
    "skill_shadow_slayer_passive": {
        "name": "收尾狂熱",
        "mp": 0,
        "kind": "passive",
        "desc": "被動：對低生命（<40% HP）目標，自身暴擊率提升 25% 且暴擊傷害提升 50%。"
    },
    # 盜賊 - 瘴痕獵手
    "skill_miasma_strike": {
        "name": "瘴痕打擊",
        "mp": 6,
        "kind": "damage",
        "desc": "物理傷害，目標每有流血或中毒狀態，傷害倍率增加 0.6。"
    },
    "skill_miasma_hunter_passive": {
        "name": "瘴痕狩獵",
        "mp": 0,
        "kind": "passive",
        "desc": "被動：目標每有流血或中毒狀態，自身造成的攻擊與技能傷害提升 15%。"
    },
    # 牧師 - 聖幕司祭
    "skill_holy_veil_barrier": {
        "name": "聖幕結界",
        "mp": 8,
        "kind": "buff",
        "buff": "holy_veil_shield",
        "duration": 99,
        "desc": "主動建立能吸收直接傷害的護盾，吸收時對攻擊者進行神聖反震。"
    },
    "skill_holy_veil_passive": {
        "name": "聖幕屏障",
        "mp": 0,
        "kind": "passive",
        "desc": "被動：最大護盾容量提升 25%。"
    },
    # 牧師 - 聖蝕司祭
    "skill_holy_eclipse_cast": {
        "name": "聖蝕儀式",
        "mp": 10,
        "kind": "buff",
        "buff": "holy_eclipse_active",
        "duration": 5,
        "desc": "同時施加自身聖蝕 DoT 與再生狀態 5 回合。勝利後若使用過聖蝕聖瓶則返還一瓶。"
    },
    "skill_holy_eclipse_passive": {
        "name": "聖蝕交融",
        "mp": 0,
        "kind": "passive",
        "desc": "被動：再生與自身聖蝕 DoT 並存時強化 DoT 傷害，並於戰後返還第一瓶聖蝕聖瓶。"
    }
})
