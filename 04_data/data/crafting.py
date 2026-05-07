from __future__ import annotations



RECIPES = {
    "recipe_fire_cloak": {
        "name": "抗火斗篷",
        "output": {"acc_fire_cloak": 1},
        "materials": {"mat_fire_stone": 3, "mat_scorched_iron": 2},
        "gold": 300,
        "unlock": "recipe_fire_cloak",
        "desc": "火傷害 -25%。",
    },
    "recipe_iron_sword_plus_1": {
        "name": "鐵劍 +1",
        "output": {"weapon_iron_sword_plus_1": 1},
        "base_item": "weapon_iron_sword",
        "materials": {"mat_cracked_stone": 5, "mat_scorched_iron": 1},
        "gold": 180,
        "unlock": "quest_cave_gathering",
        "desc": "消耗鐵劍，製作攻擊 +18 的鐵劍 +1。",
    },
    "recipe_leather_armor_plus_1": {
        "name": "皮甲 +1",
        "output": {"armor_leather_armor_plus_1": 1},
        "base_item": "armor_leather_armor",
        "materials": {"mat_moss_fiber": 4, "mat_cracked_stone": 3},
        "gold": 160,
        "unlock": "quest_cave_gathering",
        "desc": "消耗皮甲，製作防禦 +15 的皮甲 +1。",
    },
    "recipe_focus_pouch": {
        "name": "集中藥袋",
        "output": {"special_focus_pouch": 1},
        "materials": {"mat_moss_fiber": 3, "mat_small_crystal": 2},
        "gold": 140,
        "unlock": "recipe_focus_pouch",
        "desc": "每次進入迷宮時取得集中滴露 x1。",
    },
    "recipe_heat_charm": {
        "name": "暖石墜改",
        "output": {"acc_warm_stone_plus": 1},
        "base_item": "acc_warm_stone",
        "materials": {"mat_fire_stone": 2, "mat_lava_shard": 1},
        "gold": 260,
        "unlock": "recipe_heat_charm",
        "desc": "火傷害 -18%，敏捷 +1。",
    },
    "recipe_piercing_bundle": {
        "name": "破甲釘組",
        "output": {"item_armor_piercer": 3},
        "materials": {"mat_scorched_iron": 2, "mat_cracked_stone": 3},
        "gold": 120,
        "unlock": "recipe_piercing_bundle",
        "desc": "取得破甲釘 x3。",
    },
}
