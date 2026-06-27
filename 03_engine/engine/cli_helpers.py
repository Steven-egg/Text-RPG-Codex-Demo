from __future__ import annotations

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

REGION_LOCKED_REASONS = {
    "ice": "Ice Region unlocks after the Fire Seal route is complete.",
    "earth": "Earth Region unlocks after completing Ice Region quests.",
    "thunder": "Thunder Region unlocks after completing Earth Region quests.",
    "final": "Final Region requires all four enshrined elemental seals.",
}

def get_region_locked_reason(region_id: str) -> str:
    return REGION_LOCKED_REASONS.get(region_id, "This region is locked.")


BOSS_CLEAR_DATA = {
    "boss_glen": {
        "defeated_flag": "boss_glen_defeated",
        "loot": [
            ("key_blood_map", 1),
            ("key_fire_mark_shard", 1),
            ("mat_lava_shard", 2),
        ],
        "messages": [
            "葛倫倒下時，懷裡掉出一張染血地圖。",
            "取得 血跡地圖 x1、火之印記碎片 x1、熔岩碎片 x2。"
        ]
    },
    "boss_ash_guardian": {
        "defeated_flag": "ash_guardian_defeated",
        "unlocks": ["dungeon_cinder_seal_depths"],
        "loot": [
            ("key_fire_mark_shard", 1),
        ],
        "messages": [
            "灰燼守衛的爐心逐漸熄滅，一枚赤紅碎片從灰殼中落下。",
            "取得 火之印記碎片 x1。"
        ]
    },
    "boss_cinder_seal_sentinel": {
        "defeated_flag": "cinder_seal_sentinel_defeated",
        "loot": [
            ("key_fire_mark_shard", 1),
        ],
        "messages": [
            "燼印鎮衛碎裂時，胸口的赤紅刻印凝成第三枚碎片。",
            "取得 火之印記碎片 x1。",
            "三枚碎片短暫共鳴，像有一個尚未說出口的名字在灰燼裡亮起。回城後先向工會與神殿確認。"
        ]
    },
    "boss_ice_wreck_captain": {
        "defeated_flag": "ice_wreck_captain_defeated",
        "loot": [
            ("key_ice_wreck_captain_log", 1),
            ("mat_ice_saltcloth", 2),
        ],
        "messages": [
            "Wreck Captain defeated. Key proof recovered: Wreck Captain Log x1."
        ]
    },
    "boss_ice_frostroot_keeper": {
        "defeated_flag": "ice_frostroot_keeper_defeated",
        "loot": [
            ("key_ice_frostroot_core", 1),
            ("mat_ice_frostroot", 2),
        ],
        "messages": [
            "Frostroot Keeper defeated. Key proof recovered: Frostroot Core x1."
        ]
    },
    "boss_ice_outer_gatewarden": {
        "defeated_flag": "ice_outer_gatewarden_defeated",
        "loot": [
            ("key_ice_outer_gate_sigils", 1),
            ("mat_ice_frostiron", 2),
        ],
        "messages": [
            "Outer Gatewarden defeated. Q3 can now be reported at the Guild."
        ]
    },
    "boss_ice_final_seal_lord": {
        "defeated_flag": "ice_final_boss_defeated",
        "extra_flags": {
            "ice_relic_marker_resolved": True,
        },
        "loot": [
            ("key_ice_relic_marker_source", 1),
            ("mat_ice_deep_core", 2),
        ],
        "messages": [
            "Final Seal Lord defeated. Ice relic marker source recovered; no relic effect is active."
        ]
    },
    "boss_earth_rootwarden": {
        "defeated_flag": "earth_rootwarden_defeated",
        "loot": [
            ("key_earth_rootwarden_seed", 1),
            ("mat_earth_rootfiber", 2),
        ],
        "messages": [
            "Rootwarden defeated. Key proof recovered: Rootwarden Seed x1."
        ]
    },
    "boss_earth_quarry_colossus": {
        "defeated_flag": "earth_quarry_colossus_defeated",
        "loot": [
            ("key_earth_quarry_core", 1),
            ("mat_earth_quarry_stone", 2),
        ],
        "messages": [
            "Quarry Colossus defeated. Key proof recovered: Quarry Colossus Core x1."
        ]
    },
    "boss_earth_outer_grovekeeper": {
        "defeated_flag": "earth_outer_grovekeeper_defeated",
        "loot": [
            ("key_earth_outer_grove_sigils", 1),
            ("mat_earth_leyline_shard", 2),
        ],
        "messages": [
            "Outer Grovekeeper defeated. Q3 can now be reported at the Guild."
        ]
    },
    "boss_earth_deep_leyline_lord": {
        "defeated_flag": "earth_final_boss_defeated",
        "extra_flags": {
            "earth_relic_marker_resolved": True,
        },
        "loot": [
            ("key_earth_relic_marker_source", 1),
            ("mat_earth_deep_core", 2),
        ],
        "messages": [
            "Deep Leyline Lord defeated. Earth relic marker source recovered; no relic effect is active."
        ]
    },
    "boss_thunder_plateau_beacon": {
        "defeated_flag": "thunder_plateau_beacon_defeated",
        "loot": [
            ("key_thunder_plateau_beacon", 1),
            ("mat_thunder_copper_vein", 2),
        ],
        "messages": [
            "Plateau Beacon defeated. Key proof recovered: Plateau Beacon x1."
        ]
    },
    "boss_thunder_channel_keeper": {
        "defeated_flag": "thunder_channel_keeper_defeated",
        "loot": [
            ("key_thunder_channel_core", 1),
            ("mat_thunder_sky_stone", 2),
        ],
        "messages": [
            "Channel Keeper defeated. Key proof recovered: Channel Core x1."
        ]
    },
    "boss_thunder_lower_array_warden": {
        "defeated_flag": "thunder_lower_array_warden_defeated",
        "loot": [
            ("key_thunder_lower_array_sigils", 1),
            ("mat_thunder_cloud_essence", 2),
        ],
        "messages": [
            "Lower Array Warden defeated. Q3 can now be reported at the Guild."
        ]
    },
    "boss_thunder_crown_storm_lord": {
        "defeated_flag": "thunder_final_boss_defeated",
        "extra_flags": {
            "thunder_relic_marker_resolved": True,
        },
        "loot": [
            ("key_thunder_relic_marker_source", 1),
            ("mat_thunder_deep_core", 2),
        ],
        "messages": [
            "Crown Storm Lord defeated. Thunder relic marker source recovered; no relic effect is active."
        ]
    },
    "boss_final_echo_vanguard": {
        "defeated_flag": "final_echo_vanguard_defeated",
        "loot": [
            ("key_final_vanguard_proof", 1),
            ("mat_final_echo_ash", 2),
        ],
        "messages": [
            "Final Echo Vanguard defeated. Key proof recovered: Final Vanguard Proof x1."
        ]
    },
    "boss_final_ruin_jailer": {
        "defeated_flag": "final_ruin_jailer_defeated",
        "loot": [
            ("key_final_ruin_jailer_core", 1),
            ("mat_final_root_stone", 2),
        ],
        "messages": [
            "Ruin Jailer defeated. Key proof recovered: Ruin Jailer Core x1."
        ]
    },
    "boss_final_echo_warden": {
        "defeated_flag": "final_echo_warden_defeated",
        "loot": [
            ("key_final_echo_warden_sigils", 1),
            ("mat_final_seal_core", 2),
        ],
        "messages": [
            "Echo Warden defeated. Q3 can now be reported at the Guild."
        ]
    },
    "boss_final_seal_core": {
        "defeated_flag": "final_seal_core_defeated",
        "loot": [
            ("key_final_seal_core_sigils", 1),
            ("mat_final_demon_core", 2),
        ],
        "messages": [
            "Final Seal Core broken. Q4 can now be reported at the Guild."
        ]
    },
    "boss_final_demon_king": {
        "defeated_flag": "final_demon_king_defeated",
        "loot": [
            ("key_final_demon_king_mark", 1),
            ("mat_final_demon_core", 2),
        ],
        "messages": [
            "Demon King defeated. The main story ending is ready."
        ],
        "special_action": "demon_king_ending"
    }
}


# 3rd Slimming Slice Data

QUEST_COMPLETE_DIALOGUES = {
    "quest_cave_gathering": [
        "米菈合成屋開放了。拉比也開始販售逃脫卷軸。"
    ],
    "quest_magic_crystal": [
        "伊芙記下小魔晶的光色。火花術書現在折價 50G。"
    ],
    "quest_mine_scout": [
        "拉比壓低聲音：焦石礦坑深處很熱，抗火斗篷的配方已交給米菈。"
    ],
    "quest_boss_glen": [
        "諾亞看著血跡地圖，表情第一次變得猶豫。第二幕的元素迷宮露出了入口。",
        "下一步很明確：前往「迷宮探索」中的灰燼裂谷，先帶回少量裂谷素材完成偵查。"
    ],
    "quest_ash_ravine_scout": [
        "諾亞收起裂谷灰與焦黑鐵片：這些足夠證明灰燼裂谷值得深入調查，但現在還不是挑戰守衛的時候。"
    ],
    "quest_supply_upgrade": [
        "諾亞點頭：旅人小鋪已能販售中藥水。接下來的長戰鬥，記得把補給準備好。"
    ],
    "quest_cinder_depths_scout": [
        "諾亞攤開偵查圖：深窟最底層有一座燼印鎮衛。若要第三枚火之印記碎片，只能親自擊敗它。"
    ]
}

DUNGEON_EVENT_TEMPLATES = {
    "material": "你找到 {item_name} x{qty}。",
    "treasure_gold": "你打開一只舊木箱，取得 {gold}G。",
    "treasure_item": "你找到 {item_name} x1。",
    "trap_dodge": "你察覺地面異樣，及時避開了陷阱。",
}

DUNGEON_TREASURE_CONFIG = {
    "gold_chance": 0.65,
    "fallback_items": ["item_potion_s", "item_focus_drop"],
}

DUNGEON_TRAP_CONFIG = {
    "max_dodge_chance": 65,
    "fire_base_damage": 14,
    "default_damage": 8,
    "fire_msg": "熱風從裂縫噴出，你受到 {damage} 點火傷害。",
    "default_msg": "碎石從腳邊滑落，你受到 {damage} 點傷害。"
}

DUNGEON_SPECIAL_CONFIG = {
    "dungeon_moss_cave": {
        "loot_item": "mat_small_crystal",
        "loot_qty": 1,
        "chance": 1.0,
        "msg_main": "牆上刻著舊工會標記：別把小魔晶賣掉。你取得小魔晶 x1。",
        "msg_loot": None
    },
    "default": {
        "loot_item": "mat_lava_shard",
        "loot_qty": 1,
        "chance": 0.4,
        "msg_main": "你發現有人故意遮住通往深處的舊路標。拉比的情報看來沒錯。",
        "msg_loot": "路標後方還卡著熔岩碎片 x1。"
    }
}
