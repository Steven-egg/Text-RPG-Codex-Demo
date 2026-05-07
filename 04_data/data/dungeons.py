from __future__ import annotations



DUNGEONS = {
    "dungeon_moss_cave": {
        "name": "青苔洞窟",
        "recommended": "Lv1-3",
        "steps": 12,
        "element": "自然/無",
        "unlock": "dungeon_moss_cave",
        "materials": ["mat_moss_fiber", "mat_cracked_stone", "mat_small_crystal"],
        "monsters": ["mon_moss_rat", "mon_cave_slug", "mon_cracked_golem"],
        "gold_range": (20, 60),
        "clear_guild": 30,
        "boss": None,
    },
    "dungeon_scorched_mine": {
        "name": "焦石礦坑",
        "recommended": "Lv4-6",
        "steps": 18,
        "element": "火",
        "unlock": "dungeon_scorched_mine",
        "materials": ["mat_fire_stone", "mat_scorched_iron", "mat_lava_shard"],
        "monsters": ["mon_cinder_bat", "mon_lava_imp", "mon_scorched_guard"],
        "gold_range": (60, 110),
        "clear_guild": 100,
        "boss": "boss_glen",
    },
    "dungeon_ash_ravine": {
        "name": "灰燼裂谷",
        "recommended": "Lv7-9",
        "steps": 18,
        "element": "火",
        "unlock": "unlock_ash_ravine",
        "materials": ["mat_ravine_ash", "mat_charred_iron", "mat_flame_stone_refined"],
        "monsters": ["mon_ash_imp", "mon_lava_bat", "mon_cinder_soldier"],
        "gold_range": (90, 150),
        "clear_guild": 80,
        "boss": None,
    },
}



EVENT_WEIGHTS = [
    ("battle", 45),
    ("material", 20),
    ("treasure", 10),
    ("trap", 10),
    ("empty", 10),
    ("special", 5),
]
