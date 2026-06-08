/**
 * magic_shop_skinning_lab — Fixture Data Capsule
 * Auto-generated from official static prototype fixtures.
 */

window.MAGIC_SHOP_DEFAULT_FIXTURE = {
  "screen_id": "facility_magic_shop_screen",
  "facility_id": "magic_shop",
  "title": "星燈魔法商店",
  "subtitle": "願星辰指引你的靈魂，冒險者。在這裡可以購買並學習永久的戰鬥魔法與輔助技能。",
  "npc": {
    "id": "eve",
    "name": "伊芙",
    "role": "星燈魔法商店的館長，專注於古老星辰與元素術式的研究。",
    "guidance": "伊芙輕輕敲了敲書脊：「願星辰指引你的靈魂，冒險者。今天想要解讀哪一本古老術式？」",
    "portrait_placeholder": "EV"
  },
  "player_summary": {
    "name": "米菈",
    "level": 4,
    "job": "法師",
    "gold": 500
  },
  "category_tabs": [
    {
      "id": "all",
      "label": "全部魔法",
      "count": 6,
      "enabled": true
    },
    {
      "id": "damage",
      "label": "攻擊魔法",
      "count": 3,
      "enabled": true
    },
    {
      "id": "heal",
      "label": "恢復魔法",
      "count": 1,
      "enabled": true
    },
    {
      "id": "buff",
      "label": "輔助魔法",
      "count": 2,
      "enabled": true
    }
  ],
  "selected_category_id": "all",
  "selected_book_id": "book_spark",
  "list_rows": [
    {
      "id": "row_book_spark",
      "book_id": "book_spark",
      "title": "《火花術書》",
      "category": "damage",
      "summary": "學會火花術。火屬性小傷害魔法。",
      "price": 180,
      "mp": 5,
      "req_level": 2,
      "jobs": [
        "法師",
        "牧師"
      ],
      "status": "learnable",
      "enabled": true,
      "disabled_reason": null,
      "badges": [
        {
          "badge_id": "hot",
          "label": "熱門",
          "kind": "info"
        }
      ]
    },
    {
      "id": "row_book_ice_needle",
      "book_id": "book_ice_needle",
      "title": "《冰針術書》",
      "category": "damage",
      "summary": "學會冰針術。冰屬性小傷害魔法，克制火屬性敵人。",
      "price": 220,
      "mp": 6,
      "req_level": 3,
      "jobs": [
        "法師"
      ],
      "status": "learnable",
      "enabled": true,
      "disabled_reason": null,
      "badges": []
    },
    {
      "id": "row_book_minor_heal",
      "book_id": "book_minor_heal",
      "title": "《小治癒術書》",
      "category": "heal",
      "summary": "學會小治癒術。回復我方 HP 45 點。",
      "price": 200,
      "mp": 7,
      "req_level": 2,
      "jobs": [
        "牧師"
      ],
      "status": "job_restricted",
      "enabled": false,
      "disabled_reason": "職業不符",
      "badges": []
    },
    {
      "id": "row_book_guardian_rune",
      "book_id": "book_guardian_rune",
      "title": "《守護符文書》",
      "category": "buff",
      "summary": "學會守護符文。3 回合內提高防禦力 20%。",
      "price": 300,
      "mp": 8,
      "req_level": 4,
      "jobs": [
        "劍士",
        "牧師"
      ],
      "status": "job_restricted",
      "enabled": false,
      "disabled_reason": "職業不符",
      "badges": []
    },
    {
      "id": "row_book_quickstep",
      "book_id": "book_quickstep",
      "title": "《迅步術書》",
      "category": "buff",
      "summary": "學會迅步術。3 回合內提高敏捷 25%。",
      "price": 240,
      "mp": 6,
      "req_level": 3,
      "jobs": [
        "盜賊",
        "劍士"
      ],
      "status": "job_restricted",
      "enabled": false,
      "disabled_reason": "職業不符",
      "badges": []
    },
    {
      "id": "row_book_cinder_mark",
      "book_id": "book_cinder_mark",
      "title": "《燼印術書》",
      "category": "damage",
      "summary": "學會燼印術。使敵人更容易受到火屬性傷害。",
      "price": 360,
      "mp": 9,
      "req_level": 5,
      "jobs": [
        "法師",
        "牧師"
      ],
      "status": "level_restricted",
      "enabled": false,
      "disabled_reason": "等級不足 Lv5",
      "badges": [
        {
          "badge_id": "rare",
          "label": "高階",
          "kind": "warning"
        }
      ]
    }
  ],
  "book_details": {
    "book_spark": {
      "book_id": "book_spark",
      "title": "《火花術書》",
      "category_label": "攻擊魔法",
      "skill_name": "火花術",
      "mp_cost": 5,
      "description": "凝聚精純的初階火元素術式，從法杖前端射出燃燒的火花。是法師探險時最可靠的基礎進攻魔法。",
      "effect_summary": "造成火屬性小傷害 (基礎倍率 1.25)",
      "jobs": [
        "法師",
        "牧師"
      ],
      "req_level": 2,
      "price": 180,
      "status": "learnable",
      "disabled_reason": null
    },
    "book_ice_needle": {
      "book_id": "book_ice_needle",
      "title": "《冰針術書》",
      "category_label": "攻擊魔法",
      "skill_name": "冰針術",
      "mp_cost": 6,
      "description": "凝聚周遭的水元素並凝結成銳利的冰針，能有效穿透敌人的防線。對付焦石礦坑與燼印深窟的火系魔物效果卓越。",
      "effect_summary": "造成冰屬性小傷害 (基礎倍率 1.35)，火系敵人剋星",
      "jobs": [
        "法師"
      ],
      "req_level": 3,
      "price": 220,
      "status": "learnable",
      "disabled_reason": null
    },
    "book_minor_heal": {
      "book_id": "book_minor_heal",
      "title": "《小治癒術書》",
      "category_label": "恢復魔法",
      "skill_name": "小治癒術",
      "mp_cost": 7,
      "description": "吟唱光之神聖禱詞，降下溫和的魔法微光撫平傷口。牧師最基礎的治療法術。",
      "effect_summary": "回復 HP 45 點",
      "jobs": [
        "牧師"
      ],
      "req_level": 2,
      "price": 200,
      "status": "job_restricted",
      "disabled_reason": "職業不符"
    },
    "book_guardian_rune": {
      "book_id": "book_guardian_rune",
      "title": "《守護符文書》",
      "category_label": "輔助魔法",
      "skill_name": "守護符文",
      "mp_cost": 8,
      "description": "以魔力在前方空域構築虛擬的幾何土盾，暫時提升受術者的防禦耐性。",
      "effect_summary": "3 回合內防禦 +20%",
      "jobs": [
        "劍士",
        "牧師"
      ],
      "req_level": 4,
      "price": 300,
      "status": "job_restricted",
      "disabled_reason": "職業不符"
    },
    "book_quickstep": {
      "book_id": "book_quickstep",
      "title": "《迅步術書》",
      "category_label": "輔助魔法",
      "skill_name": "迅步術",
      "mp_cost": 6,
      "description": "為雙足加持微弱風行之術，能更容易閃避敵人攻擊，或在戰場上搶先做出應對。",
      "effect_summary": "3 回合內敏捷 +25%",
      "jobs": [
        "盜賊",
        "劍士"
      ],
      "req_level": 3,
      "price": 240,
      "status": "job_restricted",
      "disabled_reason": "職業不符"
    },
    "book_cinder_mark": {
      "book_id": "book_cinder_mark",
      "title": "《燼印術書》",
      "category_label": "攻擊魔法",
      "skill_name": "燼印術",
      "mp_cost": 9,
      "description": "釋放火山微粒覆蓋於敵方目標身上，留下容易被高熱點燃的隱密標記。火花術的絕佳增傷搭配。",
      "effect_summary": "3 回合內降低火抗性，使敵人更容易受到火屬性傷害",
      "jobs": [
        "法師",
        "牧師"
      ],
      "req_level": 5,
      "price": 360,
      "status": "level_restricted",
      "disabled_reason": "等級不足"
    }
  },
  "requirement_rows": {
    "book_spark": [
      {
        "id": "gold",
        "label": "金幣需求",
        "required_value": "180G",
        "current_value": "500G",
        "status": "met",
        "disabled_reason": null
      },
      {
        "id": "mat_small_crystal",
        "label": "小魔晶",
        "required_value": "1 個",
        "current_value": "2 個",
        "status": "met",
        "disabled_reason": null
      }
    ],
    "book_ice_needle": [
      {
        "id": "gold",
        "label": "金幣需求",
        "required_value": "220G",
        "current_value": "500G",
        "status": "met",
        "disabled_reason": null
      },
      {
        "id": "mat_small_crystal",
        "label": "小魔晶",
        "required_value": "2 個",
        "current_value": "2 個",
        "status": "met",
        "disabled_reason": null
      }
    ]
  },
  "primary_actions": {
    "book_spark": {
      "action_id": "learn_magic_book",
      "label": "學習火花術 (180G)",
      "enabled": true,
      "disabled_reason": null,
      "payload": {
        "book_id": "book_spark",
        "price": 180
      },
      "result_message": "你成功研讀了《火花術書》！扣除金幣 180G 與小魔晶 x1，已永久學會法術「火花術」！"
    },
    "book_ice_needle": {
      "action_id": "learn_magic_book",
      "label": "學習冰針術 (220G)",
      "enabled": true,
      "disabled_reason": null,
      "payload": {
        "book_id": "book_ice_needle",
        "price": 220
      },
      "result_message": "你成功研讀了《冰針術書》！扣除金幣 220G 與小魔晶 x2，已永久學會法術「冰針術」！"
    }
  },
  "debug_notes": [
    "Default Magic Shop fixture is static display data only.",
    "Learning magic book logs UIAction and does not change player learned_skills array."
  ]
};

window.MAGIC_SHOP_CONSTRAINED_FIXTURE = {
  "screen_id": "facility_magic_shop_screen",
  "facility_id": "magic_shop",
  "title": "星燈魔法商店 (受限展示版)",
  "subtitle": "願星辰指引你的靈魂，冒險者。在這裡可以購買並學習永久的戰鬥魔法與輔助技能。",
  "npc": {
    "id": "eve",
    "name": "伊芙",
    "role": "星燈魔法商店的館長，專注於古老星辰與元素術式的研究。",
    "guidance": "伊芙微微皺起眉頭：「嗯... 你的魔力波動有些奇特，似乎並不符合這些術式的需求。」",
    "portrait_placeholder": "EV"
  },
  "player_summary": {
    "name": "艾琳",
    "level": 1,
    "job": "盜賊",
    "gold": 50
  },
  "category_tabs": [
    {
      "id": "all",
      "label": "全部魔法",
      "count": 6,
      "enabled": true
    },
    {
      "id": "damage",
      "label": "攻擊魔法",
      "count": 3,
      "enabled": true
    },
    {
      "id": "heal",
      "label": "恢復魔法",
      "count": 1,
      "enabled": true
    },
    {
      "id": "buff",
      "label": "輔助魔法",
      "count": 2,
      "enabled": true
    }
  ],
  "selected_category_id": "all",
  "selected_book_id": "book_quickstep",
  "list_rows": [
    {
      "id": "row_book_spark",
      "book_id": "book_spark",
      "title": "《火花術書》",
      "category": "damage",
      "summary": "學會火花術。火屬性小傷害魔法。",
      "price": 180,
      "mp": 5,
      "req_level": 2,
      "jobs": [
        "法師",
        "牧師"
      ],
      "status": "job_restricted",
      "enabled": false,
      "disabled_reason": "職業不符",
      "badges": []
    },
    {
      "id": "row_book_ice_needle",
      "book_id": "book_ice_needle",
      "title": "《冰針術書》",
      "category": "damage",
      "summary": "學會冰針術。冰屬性小傷害魔法，克制火屬性敵人。",
      "price": 220,
      "mp": 6,
      "req_level": 3,
      "jobs": [
        "法師"
      ],
      "status": "job_restricted",
      "enabled": false,
      "disabled_reason": "職業不符",
      "badges": []
    },
    {
      "id": "row_book_minor_heal",
      "book_id": "book_minor_heal",
      "title": "《小治癒術書》",
      "category": "heal",
      "summary": "學會小治癒術。回復我方 HP 45 點。",
      "price": 200,
      "mp": 7,
      "req_level": 2,
      "jobs": [
        "牧師"
      ],
      "status": "job_restricted",
      "enabled": false,
      "disabled_reason": "職業不符",
      "badges": []
    },
    {
      "id": "row_book_guardian_rune",
      "book_id": "book_guardian_rune",
      "title": "《守護符文書》",
      "category": "buff",
      "summary": "學會守護符文。3 回合內提高防禦力 20%。",
      "price": 300,
      "mp": 8,
      "req_level": 4,
      "jobs": [
        "劍士",
        "牧師"
      ],
      "status": "job_restricted",
      "enabled": false,
      "disabled_reason": "職業不符",
      "badges": []
    },
    {
      "id": "row_book_quickstep",
      "book_id": "book_quickstep",
      "title": "《迅步術書》",
      "category": "buff",
      "summary": "學會迅步術。3 回合內提高敏捷 25%。",
      "price": 240,
      "mp": 6,
      "req_level": 3,
      "jobs": [
        "盜賊",
        "劍士"
      ],
      "status": "level_restricted",
      "enabled": false,
      "disabled_reason": "等級不足 Lv3",
      "badges": []
    },
    {
      "id": "row_book_cinder_mark",
      "book_id": "book_cinder_mark",
      "title": "《燼印術書》",
      "category": "damage",
      "summary": "學會燼印術。使敵人更容易受到火屬性傷害。",
      "price": 360,
      "mp": 9,
      "req_level": 5,
      "jobs": [
        "法師",
        "牧師"
      ],
      "status": "job_restricted",
      "enabled": false,
      "disabled_reason": "職業不符",
      "badges": []
    }
  ],
  "book_details": {
    "book_quickstep": {
      "book_id": "book_quickstep",
      "title": "《迅步術書》",
      "category_label": "輔助魔法",
      "skill_name": "迅步術",
      "mp_cost": 6,
      "description": "為雙足加持微弱風行之術，能更容易閃避敵人攻擊，或在戰場上搶先做出應對。此法術完美契合盜賊的靈活身手，但你的等階尚低，難以掌握其風軌流動。",
      "effect_summary": "3 回合內敏捷 +25%",
      "jobs": [
        "盜賊",
        "劍士"
      ],
      "req_level": 3,
      "price": 240,
      "status": "level_restricted",
      "disabled_reason": "等級不足 Lv3"
    },
    "book_spark": {
      "book_id": "book_spark",
      "title": "《火花術書》",
      "category_label": "攻擊魔法",
      "skill_name": "火花術",
      "mp_cost": 5,
      "description": "凝聚精純的初階火元素術式，從法杖前端射出燃燒的火花。非編織魔網的純粹武力職業無法解讀其符文奧秘。",
      "effect_summary": "造成火屬性小傷害 (基礎倍率 1.25)",
      "jobs": [
        "法師",
        "牧師"
      ],
      "req_level": 2,
      "price": 180,
      "status": "job_restricted",
      "disabled_reason": "職業不符"
    }
  },
  "requirement_rows": {
    "book_quickstep": [
      {
        "id": "gold",
        "label": "金幣需求",
        "required_value": "240G",
        "current_value": "50G",
        "status": "unmet",
        "disabled_reason": "金幣不足"
      },
      {
        "id": "level",
        "label": "等級限制",
        "required_value": "Lv 3",
        "current_value": "Lv 1",
        "status": "unmet",
        "disabled_reason": "等級不足"
      },
      {
        "id": "mat_moss_fiber",
        "label": "苔蘚纖維",
        "required_value": "2 個",
        "current_value": "0 個",
        "status": "unmet",
        "disabled_reason": "素材不足"
      }
    ]
  },
  "primary_actions": {
    "book_quickstep": {
      "action_id": "learn_magic_book",
      "label": "等級不足",
      "enabled": false,
      "disabled_reason": "等級不足 Lv3",
      "payload": {
        "book_id": "book_quickstep",
        "price": 240
      },
      "result_message": null
    }
  },
  "debug_notes": [
    "Thief level 1 constrained display.",
    "Quickstep requires Level 3, sufficient gold, and moss fiber."
  ]
};

window.MAGIC_SHOP_DISCOUNT_FIXTURE = {
  "screen_id": "facility_magic_shop_screen",
  "facility_id": "magic_shop",
  "title": "星燈魔法商店 (魔晶折扣版)",
  "subtitle": "願星辰指引你的靈魂，冒險者。在這裡可以購買並學習永久的戰鬥魔法與輔助技能。",
  "npc": {
    "id": "eve",
    "name": "伊芙",
    "role": "星燈魔法商店的館長，專注於古老星辰與元素術式的研究。",
    "guidance": "伊芙眼睛一亮：「啊，多虧你幫忙收集的魔晶，關於低階元素的研究有了很大突破！火花術書現在為你永久折價 50G！」",
    "portrait_placeholder": "EV"
  },
  "player_summary": {
    "name": "米菈",
    "level": 4,
    "job": "法師",
    "gold": 350
  },
  "category_tabs": [
    {
      "id": "all",
      "label": "全部魔法",
      "count": 6,
      "enabled": true
    },
    {
      "id": "damage",
      "label": "攻擊魔法",
      "count": 3,
      "enabled": true
    },
    {
      "id": "heal",
      "label": "恢復魔法",
      "count": 1,
      "enabled": true
    },
    {
      "id": "buff",
      "label": "輔助魔法",
      "count": 2,
      "enabled": true
    }
  ],
  "selected_category_id": "all",
  "selected_book_id": "book_spark",
  "list_rows": [
    {
      "id": "row_book_spark",
      "book_id": "book_spark",
      "title": "《火花術書》",
      "category": "damage",
      "summary": "學會火花術。火屬性小傷害魔法。[魔晶研究已折價 50G]",
      "price": 130,
      "mp": 5,
      "req_level": 2,
      "jobs": [
        "法師",
        "牧師"
      ],
      "status": "learnable",
      "enabled": true,
      "disabled_reason": null,
      "badges": [
        {
          "badge_id": "discount",
          "label": "折價 50G",
          "kind": "warning"
        }
      ]
    },
    {
      "id": "row_book_ice_needle",
      "book_id": "book_ice_needle",
      "title": "《冰針術書》",
      "category": "damage",
      "summary": "學會冰針術。冰屬性小傷害魔法，克制火屬性敵人。",
      "price": 220,
      "mp": 6,
      "req_level": 3,
      "jobs": [
        "法師"
      ],
      "status": "learnable",
      "enabled": true,
      "disabled_reason": null,
      "badges": []
    },
    {
      "id": "row_book_minor_heal",
      "book_id": "book_minor_heal",
      "title": "《小治癒術書》",
      "category": "heal",
      "summary": "學會小治癒術。回復我方 HP 45 點。",
      "price": 200,
      "mp": 7,
      "req_level": 2,
      "jobs": [
        "牧師"
      ],
      "status": "job_restricted",
      "enabled": false,
      "disabled_reason": "職業不符",
      "badges": []
    },
    {
      "id": "row_book_guardian_rune",
      "book_id": "book_guardian_rune",
      "title": "《守護符文書》",
      "category": "buff",
      "summary": "學會守護符文。3 回合內提高防禦力 20%。",
      "price": 300,
      "mp": 8,
      "req_level": 4,
      "jobs": [
        "劍士",
        "牧師"
      ],
      "status": "job_restricted",
      "enabled": false,
      "disabled_reason": "職業不符",
      "badges": []
    },
    {
      "id": "row_book_quickstep",
      "book_id": "book_quickstep",
      "title": "《迅步術書》",
      "category": "buff",
      "summary": "學會迅步術。3 回合內提高敏捷 25%。",
      "price": 240,
      "mp": 6,
      "req_level": 3,
      "jobs": [
        "盜賊",
        "劍士"
      ],
      "status": "job_restricted",
      "enabled": false,
      "disabled_reason": "職業不符",
      "badges": []
    },
    {
      "id": "row_book_cinder_mark",
      "book_id": "book_cinder_mark",
      "title": "《燼印術書》",
      "category": "damage",
      "summary": "學會燼印術。使敵人更容易受到火屬性傷害。",
      "price": 360,
      "mp": 9,
      "req_level": 5,
      "jobs": [
        "法師",
        "牧師"
      ],
      "status": "level_restricted",
      "enabled": false,
      "disabled_reason": "等級不足 Lv5",
      "badges": [
        {
          "badge_id": "rare",
          "label": "高階",
          "kind": "warning"
        }
      ]
    }
  ],
  "book_details": {
    "book_spark": {
      "book_id": "book_spark",
      "title": "《火花術書》",
      "category_label": "攻擊魔法",
      "skill_name": "火花術",
      "mp_cost": 5,
      "description": "凝聚精純的初階火元素術式，從法杖前端射出燃燒的火花。因已完成工會「魔晶研究」委託，伊芙為你提供了特惠折扣！",
      "effect_summary": "造成火屬性小傷害 (基礎倍率 1.25)",
      "jobs": [
        "法師",
        "牧師"
      ],
      "req_level": 2,
      "price": 130,
      "status": "learnable",
      "disabled_reason": null
    },
    "book_ice_needle": {
      "book_id": "book_ice_needle",
      "title": "《冰針術書》",
      "category_label": "攻擊魔法",
      "skill_name": "冰針術",
      "mp_cost": 6,
      "description": "凝聚周遭的水元素並凝結成銳利的冰針，能有效穿透敌人的防線。對付焦石礦坑與燼印深窟的火系魔物效果卓越。",
      "effect_summary": "造成冰屬性小傷害 (基礎倍率 1.35)，火系敵人剋星",
      "jobs": [
        "法師"
      ],
      "req_level": 3,
      "price": 220,
      "status": "learnable",
      "disabled_reason": null
    }
  },
  "requirement_rows": {
    "book_spark": [
      {
        "id": "gold",
        "label": "金幣需求",
        "required_value": "130G",
        "current_value": "350G",
        "status": "met",
        "disabled_reason": null
      },
      {
        "id": "mat_small_crystal",
        "label": "小魔晶",
        "required_value": "1 個",
        "current_value": "1 個",
        "status": "met",
        "disabled_reason": null
      }
    ],
    "book_ice_needle": [
      {
        "id": "gold",
        "label": "金幣需求",
        "required_value": "220G",
        "current_value": "350G",
        "status": "met",
        "disabled_reason": null
      },
      {
        "id": "mat_small_crystal",
        "label": "小魔晶",
        "required_value": "2 個",
        "current_value": "1 個",
        "status": "unmet",
        "disabled_reason": "素材不足"
      }
    ]
  },
  "primary_actions": {
    "book_spark": {
      "action_id": "learn_magic_book",
      "label": "學習火花術 (130G)",
      "enabled": true,
      "disabled_reason": null,
      "payload": {
        "book_id": "book_spark",
        "price": 130
      },
      "result_message": "你成功研讀了《火花術書》！扣除金幣 130G 與小魔晶 x1，已永久學會法術「火花術」！"
    },
    "book_ice_needle": {
      "action_id": "learn_magic_book",
      "label": "學習冰針術 (220G)",
      "enabled": false,
      "disabled_reason": "素材不足",
      "payload": {
        "book_id": "book_ice_needle",
        "price": 220
      },
      "result_message": null
    }
  },
  "debug_notes": [
    "Discount Magic Shop fixture covers magic crystal quest completion.",
    "Spark book is discounted to 130G."
  ]
};

window.MAGIC_SHOP_LEARNED_FIXTURE = {
  "screen_id": "facility_magic_shop_screen",
  "facility_id": "magic_shop",
  "title": "星燈魔法商店 (術式飽和版)",
  "subtitle": "願星辰指引你的靈魂，冒險者。在這裡可以購買並學習永久的戰鬥魔法與輔助技能。",
  "npc": {
    "id": "eve",
    "name": "伊芙",
    "role": "星燈魔法商店的館長，專注於古老星辰與元素術式的研究。",
    "guidance": "伊芙微笑著合上書本：「不愧是智慧超群的學者，我這裡能傳授你的魔法奧秘，已然盡數鐫刻於你的法術書中了。」",
    "portrait_placeholder": "EV"
  },
  "player_summary": {
    "name": "米菈",
    "level": 5,
    "job": "法師",
    "gold": 1500
  },
  "category_tabs": [
    {
      "id": "all",
      "label": "全部魔法",
      "count": 6,
      "enabled": true
    },
    {
      "id": "damage",
      "label": "攻擊魔法",
      "count": 3,
      "enabled": true
    },
    {
      "id": "heal",
      "label": "恢復魔法",
      "count": 1,
      "enabled": true
    },
    {
      "id": "buff",
      "label": "輔助魔法",
      "count": 2,
      "enabled": true
    }
  ],
  "selected_category_id": "all",
  "selected_book_id": "book_spark",
  "list_rows": [
    {
      "id": "row_book_spark",
      "book_id": "book_spark",
      "title": "《火花術書》",
      "category": "damage",
      "summary": "學會火花術。火屬性小傷害魔法。",
      "price": 180,
      "mp": 5,
      "req_level": 2,
      "jobs": [
        "法師",
        "牧師"
      ],
      "status": "learned",
      "enabled": false,
      "disabled_reason": "已學會",
      "badges": [
        {
          "badge_id": "learned",
          "label": "已學會",
          "kind": "success"
        }
      ]
    },
    {
      "id": "row_book_ice_needle",
      "book_id": "book_ice_needle",
      "title": "《冰針術書》",
      "category": "damage",
      "summary": "學會冰針術。冰屬性小傷害魔法，克制火屬性敵人。",
      "price": 220,
      "mp": 6,
      "req_level": 3,
      "jobs": [
        "法師"
      ],
      "status": "learned",
      "enabled": false,
      "disabled_reason": "已學會",
      "badges": [
        {
          "badge_id": "learned",
          "label": "已學會",
          "kind": "success"
        }
      ]
    },
    {
      "id": "row_book_minor_heal",
      "book_id": "book_minor_heal",
      "title": "《小治癒術書》",
      "category": "heal",
      "summary": "學會小治癒術。回復我方 HP 45 點。",
      "price": 200,
      "mp": 7,
      "req_level": 2,
      "jobs": [
        "牧師"
      ],
      "status": "job_restricted",
      "enabled": false,
      "disabled_reason": "職業不符",
      "badges": []
    },
    {
      "id": "row_book_guardian_rune",
      "book_id": "book_guardian_rune",
      "title": "《守護符文書》",
      "category": "buff",
      "summary": "學會守護符文。3 回合內提高防禦力 20%。",
      "price": 300,
      "mp": 8,
      "req_level": 4,
      "jobs": [
        "劍士",
        "牧師"
      ],
      "status": "job_restricted",
      "enabled": false,
      "disabled_reason": "職業不符",
      "badges": []
    },
    {
      "id": "row_book_quickstep",
      "book_id": "book_quickstep",
      "title": "《迅步術書》",
      "category": "buff",
      "summary": "學會迅步術。3 回合內提高敏捷 25%。",
      "price": 240,
      "mp": 6,
      "req_level": 3,
      "jobs": [
        "盜賊",
        "劍士"
      ],
      "status": "job_restricted",
      "enabled": false,
      "disabled_reason": "職業不符",
      "badges": []
    },
    {
      "id": "row_book_cinder_mark",
      "book_id": "book_cinder_mark",
      "title": "《燼印術書》",
      "category": "damage",
      "summary": "學會燼印術。使敵人更容易受到火屬性傷害。",
      "price": 360,
      "mp": 9,
      "req_level": 5,
      "jobs": [
        "法師",
        "牧師"
      ],
      "status": "learned",
      "enabled": false,
      "disabled_reason": "已學會",
      "badges": [
        {
          "badge_id": "learned",
          "label": "已學會",
          "kind": "success"
        }
      ]
    }
  ],
  "book_details": {
    "book_spark": {
      "book_id": "book_spark",
      "title": "《火花術書》",
      "category_label": "攻擊魔法",
      "skill_name": "火花術",
      "mp_cost": 5,
      "description": "凝聚精純的初階火元素術式，從法杖前端射出燃燒的火花。米菈法杖頂端長燃的微光見證了對此術式的精確掌握。",
      "effect_summary": "造成火屬性小傷害 (基礎倍率 1.25)",
      "jobs": [
        "法師",
        "牧師"
      ],
      "req_level": 2,
      "price": 180,
      "status": "learned",
      "disabled_reason": "已學會"
    },
    "book_cinder_mark": {
      "book_id": "book_cinder_mark",
      "title": "《燼印術書》",
      "category_label": "攻擊魔法",
      "skill_name": "燼印術",
      "mp_cost": 9,
      "description": "釋放火山微粒覆蓋於敵方目標身上，留下容易被高熱點燃的隱密標記。火花術的絕佳增傷搭配。",
      "effect_summary": "3 回合內降低火抗性，使敵人更容易受到火屬性傷害",
      "jobs": [
        "法師",
        "牧師"
      ],
      "req_level": 5,
      "price": 360,
      "status": "learned",
      "disabled_reason": "已學會"
    }
  },
  "requirement_rows": {
    "book_spark": [
      {
        "id": "gold",
        "label": "金幣需求",
        "required_value": "180G",
        "current_value": "1500G",
        "status": "met",
        "disabled_reason": null
      },
      {
        "id": "learned",
        "label": "學習狀態",
        "required_value": "未學習",
        "current_value": "已學習",
        "status": "unmet",
        "disabled_reason": "已學會"
      }
    ],
    "book_cinder_mark": [
      {
        "id": "gold",
        "label": "金幣需求",
        "required_value": "360G",
        "current_value": "1500G",
        "status": "met",
        "disabled_reason": null
      },
      {
        "id": "learned",
        "label": "學習狀態",
        "required_value": "未學習",
        "current_value": "已學習",
        "status": "unmet",
        "disabled_reason": "已學會"
      }
    ]
  },
  "primary_actions": {
    "book_spark": {
      "action_id": "learn_magic_book",
      "label": "已學會此法術",
      "enabled": false,
      "disabled_reason": "已學會",
      "payload": {
        "book_id": "book_spark",
        "price": 180
      },
      "result_message": null
    },
    "book_cinder_mark": {
      "action_id": "learn_magic_book",
      "label": "已學會此法術",
      "enabled": false,
      "disabled_reason": "已學會",
      "payload": {
        "book_id": "book_cinder_mark",
        "price": 360
      },
      "result_message": null
    }
  },
  "debug_notes": [
    "Full-learn state Mage level 5.",
    "All eligible magic books are already learned."
  ]
};
