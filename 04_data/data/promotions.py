from __future__ import annotations


PROMOTIONS = {
    "promotion_element_knight": {
        "source_job": "劍士",
        "name": "元素騎士",
        "summary": "物理攻擊搭配元素附魔與抗性姿態。",
        "requirements": [
            {"kind": "level", "value": 12, "label": "角色等級達 Lv12"},
            {"kind": "item", "key": "key_fire_mark_shard", "label": "持有火之印記碎片"},
        ],
        "status": "preview",
    },
    "promotion_star_singer": {
        "source_job": "法師",
        "name": "星詠者",
        "summary": "高 MP、多元素連鎖與弱點爆發。",
        "requirements": [
            {"kind": "level", "value": 12, "label": "角色等級達 Lv12"},
            {"kind": "quest", "key": "quest_magic_crystal", "label": "完成魔晶研究"},
            {"kind": "unlock", "key": "unlock_ash_ravine", "label": "發現灰燼裂谷"},
        ],
        "status": "preview",
    },
    "promotion_shadow_walker": {
        "source_job": "盜賊",
        "name": "影行者",
        "summary": "先手、陷阱應對、暴擊與資源偷取。",
        "requirements": [
            {"kind": "level", "value": 12, "label": "角色等級達 Lv12"},
            {"kind": "quest", "key": "quest_mine_scout", "label": "完成焦石偵查"},
            {"kind": "unlock", "key": "unlock_ash_ravine", "label": "發現灰燼裂谷"},
        ],
        "status": "preview",
    },
    "promotion_holy_seal": {
        "source_job": "牧師",
        "name": "聖印使",
        "summary": "治療、防禦結界與印記淨化。",
        "requirements": [
            {"kind": "level", "value": 12, "label": "角色等級達 Lv12"},
            {"kind": "quest", "key": "quest_cave_gathering", "label": "完成洞窟採集"},
            {"kind": "unlock", "key": "unlock_ash_ravine", "label": "發現灰燼裂谷"},
        ],
        "status": "preview",
    },
}
