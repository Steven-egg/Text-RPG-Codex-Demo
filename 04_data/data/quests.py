from __future__ import annotations



QUESTS = {
    "quest_register": {
        "title": "冒險者登記",
        "giver": "諾亞",
        "turn_in": {},
        "reward": {"gold": 0, "items": {"item_potion_s": 2, "special_trial_badge": 1}, "guild": 0},
        "unlocks": ["dungeon_moss_cave"],
        "desc": "選擇職業並領取見習徽章。",
    },
    "quest_cave_gathering": {
        "title": "洞窟採集",
        "giver": "諾亞",
        "turn_in": {"mat_moss_fiber": 3, "mat_cracked_stone": 2},
        "reward": {"gold": 120, "items": {}, "guild": 30},
        "unlocks": ["shop_synthesis_01", "item_escape_scroll", "dungeon_scorched_mine", "quest_cave_gathering"],
        "desc": "交付青苔纖維 x3、破裂石片 x2。",
    },
    "quest_magic_crystal": {
        "title": "魔晶研究",
        "giver": "伊芙",
        "turn_in": {"mat_small_crystal": 2},
        "reward": {"gold": 0, "items": {}, "guild": 20},
        "unlocks": ["recipe_focus_pouch", "quest_magic_crystal"],
        "desc": "交付小魔晶 x2，火花術書折價 50G。",
    },
    "quest_mine_scout": {
        "title": "焦石偵查",
        "giver": "拉比",
        "turn_in": {"mat_fire_stone": 2},
        "reward": {"gold": 0, "items": {}, "guild": 40},
        "unlocks": ["item_warm_stone", "recipe_fire_cloak", "quest_mine_scout"],
        "desc": "進入焦石礦坑並帶回火焰石 x2。",
    },
    "quest_boss_glen": {
        "title": "血跡地圖",
        "giver": "諾亞",
        "turn_in": {"flag:boss_glen_defeated": 1},
        "reward": {"gold": 300, "items": {}, "guild": 100},
        "unlocks": ["second_act_preview", "unlock_act_2", "unlock_ash_ravine", "quest_boss_glen"],
        "desc": "擊敗山寨頭目葛倫。交回血跡地圖後，工會會指示下一步偵查灰燼裂谷。",
    },
    "quest_ash_ravine_scout": {
        "title": "灰燼裂谷偵查",
        "giver": "諾亞",
        "turn_in": {"mat_ravine_ash": 2, "mat_charred_iron": 1},
        "reward": {"gold": 180, "items": {"item_potion_s": 2}, "guild": 70},
        "unlocks": ["quest_ash_ravine_scout"],
        "desc": "前往新解鎖的灰燼裂谷偵查，帶回裂谷灰 x2、焦黑鐵片 x1。這不是討伐任務，遇到壓力就先撤回城鎮。",
    },
    "quest_supply_upgrade": {
        "title": "補給線升級",
        "giver": "諾亞",
        "turn_in": {"mat_flame_stone_refined": 3, "mat_lava_shard": 2},
        "reward": {"gold": 0, "items": {"item_potion_m": 2}, "guild": 0},
        "unlocks": ["item_potion_m", "dungeon_cinder_seal_depths", "quest_supply_upgrade"],
        "desc": "灰燼守衛已倒下，工會開始整理更深入火系迷宮的補給路線。交付精煉火石 x3、熔岩碎片 x2，用來穩定中藥水的耐熱瓶封。",
    },
    "quest_cinder_depths_scout": {
        "title": "燼印深窟偵查",
        "giver": "諾亞",
        "turn_in": {"mat_flame_stone_refined": 2, "mat_lava_shard": 1},
        "reward": {"gold": 220, "items": {"item_potion_m": 1}, "guild": 80},
        "unlocks": ["quest_cinder_depths_scout"],
        "desc": "補給線穩定後，前往燼印深窟記錄燼印反應。帶回精煉火石 x2、熔岩碎片 x1；工會只需要偵查資料，不會補發火之印記碎片。",
    },
}
