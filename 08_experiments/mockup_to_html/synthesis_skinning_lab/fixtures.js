/**
 * synthesis_skinning_lab — Fixture Data Capsule
 * Auto-generated from official static prototype fixtures.
 */

window.SYNTHESIS_DEFAULT_FIXTURE = {
  "screen_id": "facility_synthesis_screen",
  "facility_id": "synthesis",
  "title": "米菈合成屋",
  "subtitle": "把迷宮素材整理成裝備與戰術道具。這裡只呈現 Synthesis Screen 的 static fixture。",
  "npc": {
    "id": "mira",
    "name": "米菈",
    "role": "合成屋主人，擅長把素材、基底裝備與金幣整理成可執行的配方。"
  },
  "resource_strip": [
    {
      "id": "hero",
      "label": "艾琳 / 盜賊 Lv8",
      "tone": "primary"
    },
    {
      "id": "hp",
      "label": "HP 86/86",
      "tone": "healthy"
    },
    {
      "id": "mp",
      "label": "MP 34/40",
      "tone": "mana"
    },
    {
      "id": "gold",
      "label": "420G",
      "tone": "gold"
    },
    {
      "id": "recipes",
      "label": "可用配方 4",
      "tone": "neutral"
    }
  ],
  "category_tabs": [
    {
      "id": "all",
      "label": "全部",
      "count": 4,
      "selected": true,
      "enabled": true
    },
    {
      "id": "equipment",
      "label": "裝備",
      "count": 3,
      "selected": false,
      "enabled": true
    },
    {
      "id": "battle",
      "label": "戰術道具",
      "count": 1,
      "selected": false,
      "enabled": true
    }
  ],
  "selected_category_id": "all",
  "selected_recipe_id": "recipe_fire_cloak",
  "recipe_rows": [
    {
      "recipe_id": "recipe_fire_cloak",
      "title": "抗火斗篷",
      "category": "equipment",
      "category_label": "裝備",
      "status": "craftable",
      "status_label": "可製作",
      "output_summary": "抗火斗篷 x1",
      "owned_summary": "0 件",
      "max_count": 1,
      "gold": 300
    },
    {
      "recipe_id": "recipe_focus_pouch",
      "title": "集中藥袋",
      "category": "equipment",
      "category_label": "裝備",
      "status": "craftable",
      "status_label": "可製作",
      "output_summary": "集中藥袋 x1",
      "owned_summary": "0 件",
      "max_count": 2,
      "gold": 140
    },
    {
      "recipe_id": "recipe_heat_charm",
      "title": "暖石墜改",
      "category": "equipment",
      "category_label": "裝備",
      "status": "limited",
      "status_label": "基底有限",
      "output_summary": "暖石墜改 x1",
      "owned_summary": "0 件",
      "max_count": 1,
      "gold": 260
    },
    {
      "recipe_id": "recipe_piercing_bundle",
      "title": "破甲釘組",
      "category": "battle",
      "category_label": "戰術道具",
      "status": "craftable",
      "status_label": "可製作",
      "output_summary": "破甲釘 x3",
      "owned_summary": "1 個",
      "max_count": 1,
      "gold": 120
    }
  ],
  "recipe_details": {
    "recipe_fire_cloak": {
      "title": "抗火斗篷",
      "description": "以火焰石與焦黑鐵礦縫入斗篷內襯，降低焦石礦坑與火系迷宮的壓力。",
      "effect": "火傷害 -25%。",
      "base_note": "基底：不需要基底裝備。",
      "notes": "合成會消耗素材與金幣；此 prototype 只記錄 UIAction。",
      "outputs": [
        {
          "item_id": "acc_fire_cloak",
          "label": "抗火斗篷",
          "quantity": 1
        }
      ],
      "primary_action": {
        "action_id": "craft_recipe",
        "label": "合成抗火斗篷",
        "enabled": true,
        "disabled_reason": null,
        "payload": {
          "recipe_id": "recipe_fire_cloak"
        },
        "result_message": "已送出合成 UIAction；static prototype 不會扣除素材、金幣或產出裝備。"
      },
      "ready_feedback": {
        "tone": "success",
        "speaker": "米菈",
        "text": "材料齊了。這張配方可以驗證確認與結果提示。"
      }
    },
    "recipe_focus_pouch": {
      "title": "集中藥袋",
      "description": "把青苔纖維與小魔晶縫成小袋，進入迷宮前可整理集中滴露。",
      "effect": "每次進入迷宮時取得集中滴露 x1。",
      "base_note": "基底：不需要基底裝備。",
      "notes": "此處只展示配方狀態，不進入 runtime。",
      "outputs": [
        {
          "item_id": "special_focus_pouch",
          "label": "集中藥袋",
          "quantity": 1
        }
      ],
      "primary_action": {
        "action_id": "craft_recipe",
        "label": "合成集中藥袋",
        "enabled": true,
        "disabled_reason": null,
        "payload": {
          "recipe_id": "recipe_focus_pouch"
        },
        "result_message": "已送出合成 UIAction；static prototype 不會修改持有數。"
      },
      "ready_feedback": {
        "tone": "success",
        "speaker": "米菈",
        "text": "這張配方適合檢查裝備類輸出與材料列。"
      }
    },
    "recipe_heat_charm": {
      "title": "暖石墜改",
      "description": "把暖石墜重新封入熔岩碎片，換取更穩定的火抗與些微敏捷。",
      "effect": "火傷害 -18%，敏捷 +1。",
      "base_note": "基底：暖石墜 x1，可消耗背包或已裝備物。",
      "notes": "基底裝備列用來驗證 Requirement row 的非素材條件。",
      "outputs": [
        {
          "item_id": "acc_warm_stone_plus",
          "label": "暖石墜改",
          "quantity": 1
        }
      ],
      "primary_action": {
        "action_id": "craft_recipe",
        "label": "合成暖石墜改",
        "enabled": true,
        "disabled_reason": null,
        "payload": {
          "recipe_id": "recipe_heat_charm"
        },
        "result_message": "已送出合成 UIAction；static prototype 不會消耗暖石墜。"
      },
      "ready_feedback": {
        "tone": "info",
        "speaker": "米菈",
        "text": "有基底裝備的配方也可以走同一套確認流程。"
      }
    },
    "recipe_piercing_bundle": {
      "title": "破甲釘組",
      "description": "把焦黑鐵礦與破裂石片磨成簡易釘組，方便在戰鬥中削弱敵方防禦。",
      "effect": "取得破甲釘 x3。",
      "base_note": "基底：不需要基底裝備。",
      "notes": "戰術道具分類用來驗證 category tab 過濾。",
      "outputs": [
        {
          "item_id": "item_armor_piercer",
          "label": "破甲釘",
          "quantity": 3
        }
      ],
      "primary_action": {
        "action_id": "craft_recipe",
        "label": "合成破甲釘組",
        "enabled": true,
        "disabled_reason": null,
        "payload": {
          "recipe_id": "recipe_piercing_bundle"
        },
        "result_message": "已送出合成 UIAction；static prototype 不會新增破甲釘。"
      },
      "ready_feedback": {
        "tone": "success",
        "speaker": "米菈",
        "text": "切到戰術道具分類時，列表應只剩這類配方。"
      }
    }
  },
  "requirement_rows": {
    "recipe_fire_cloak": [
      {
        "id": "gold",
        "icon_label": "G",
        "label": "金幣",
        "required_value": "300G",
        "current_value": "420G",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      },
      {
        "id": "mat_fire_stone",
        "icon_label": "火",
        "label": "火焰石",
        "required_value": "x3",
        "current_value": "x4",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      },
      {
        "id": "mat_scorched_iron",
        "icon_label": "鐵",
        "label": "焦黑鐵礦",
        "required_value": "x2",
        "current_value": "x2",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      }
    ],
    "recipe_focus_pouch": [
      {
        "id": "gold",
        "icon_label": "G",
        "label": "金幣",
        "required_value": "140G",
        "current_value": "420G",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      },
      {
        "id": "mat_moss_fiber",
        "icon_label": "苔",
        "label": "青苔纖維",
        "required_value": "x3",
        "current_value": "x8",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      },
      {
        "id": "mat_small_crystal",
        "icon_label": "晶",
        "label": "小魔晶",
        "required_value": "x2",
        "current_value": "x5",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      }
    ],
    "recipe_heat_charm": [
      {
        "id": "gold",
        "icon_label": "G",
        "label": "金幣",
        "required_value": "260G",
        "current_value": "420G",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      },
      {
        "id": "base_acc_warm_stone",
        "icon_label": "基",
        "label": "基底裝備：暖石墜",
        "required_value": "x1",
        "current_value": "x1（已裝備）",
        "status": "limited",
        "status_label": "可消耗",
        "disabled_reason": null
      },
      {
        "id": "mat_lava_shard",
        "icon_label": "熔",
        "label": "熔岩碎片",
        "required_value": "x1",
        "current_value": "x1",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      }
    ],
    "recipe_piercing_bundle": [
      {
        "id": "gold",
        "icon_label": "G",
        "label": "金幣",
        "required_value": "120G",
        "current_value": "420G",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      },
      {
        "id": "mat_scorched_iron",
        "icon_label": "鐵",
        "label": "焦黑鐵礦",
        "required_value": "x2",
        "current_value": "x2",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      },
      {
        "id": "mat_cracked_stone",
        "icon_label": "石",
        "label": "破裂石片",
        "required_value": "x3",
        "current_value": "x6",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      }
    ]
  },
  "feedback_message": {
    "tone": "info",
    "speaker": "米菈",
    "text": "選一張配方，右側會顯示金幣、素材與基底裝備狀態。"
  },
  "empty_state": {
    "message": "目前沒有符合分類的可用配方。"
  },
  "debug_notes": [
    "Default Synthesis fixture is static display data only.",
    "Craft action logs UIAction only and does not change inventory, gold, or equipment.",
    "Fixture values mirror current runtime recipes for readability but are not gameplay SSOT."
  ]
};

window.SYNTHESIS_CONSTRAINED_FIXTURE = {
  "screen_id": "facility_synthesis_screen",
  "facility_id": "synthesis",
  "title": "米菈合成屋",
  "subtitle": "條件不足測試狀態：確認缺金幣、缺素材與缺基底時仍能清楚顯示原因。",
  "npc": {
    "id": "mira",
    "name": "米菈",
    "role": "合成屋主人，會先指出缺口，再讓玩家決定下一步準備。"
  },
  "resource_strip": [
    {
      "id": "hero",
      "label": "艾琳 / 盜賊 Lv8",
      "tone": "primary"
    },
    {
      "id": "hp",
      "label": "HP 41/86",
      "tone": "healthy"
    },
    {
      "id": "mp",
      "label": "MP 18/40",
      "tone": "mana"
    },
    {
      "id": "gold",
      "label": "90G",
      "tone": "gold"
    },
    {
      "id": "recipes",
      "label": "可用配方 4",
      "tone": "neutral"
    }
  ],
  "category_tabs": [
    {
      "id": "all",
      "label": "全部",
      "count": 4,
      "selected": true,
      "enabled": true
    },
    {
      "id": "equipment",
      "label": "裝備",
      "count": 3,
      "selected": false,
      "enabled": true
    },
    {
      "id": "battle",
      "label": "戰術道具",
      "count": 1,
      "selected": false,
      "enabled": true
    }
  ],
  "selected_category_id": "all",
  "selected_recipe_id": "recipe_heat_charm",
  "recipe_rows": [
    {
      "recipe_id": "recipe_fire_cloak",
      "title": "抗火斗篷",
      "category": "equipment",
      "category_label": "裝備",
      "status": "missing",
      "status_label": "素材不足",
      "output_summary": "抗火斗篷 x1",
      "owned_summary": "0 件",
      "max_count": 0,
      "gold": 300
    },
    {
      "recipe_id": "recipe_focus_pouch",
      "title": "集中藥袋",
      "category": "equipment",
      "category_label": "裝備",
      "status": "missing",
      "status_label": "金幣不足",
      "output_summary": "集中藥袋 x1",
      "owned_summary": "0 件",
      "max_count": 0,
      "gold": 140
    },
    {
      "recipe_id": "recipe_heat_charm",
      "title": "暖石墜改",
      "category": "equipment",
      "category_label": "裝備",
      "status": "missing",
      "status_label": "基底不足",
      "output_summary": "暖石墜改 x1",
      "owned_summary": "0 件",
      "max_count": 0,
      "gold": 260
    },
    {
      "recipe_id": "recipe_piercing_bundle",
      "title": "破甲釘組",
      "category": "battle",
      "category_label": "戰術道具",
      "status": "missing",
      "status_label": "金幣不足",
      "output_summary": "破甲釘 x3",
      "owned_summary": "0 個",
      "max_count": 0,
      "gold": 120
    }
  ],
  "recipe_details": {
    "recipe_fire_cloak": {
      "title": "抗火斗篷",
      "description": "火系迷宮對策裝。這個 constrained fixture 用來呈現金幣與素材同時不足時的 readable rows。",
      "effect": "火傷害 -25%。",
      "base_note": "基底：不需要基底裝備。",
      "notes": "不可用 action 仍會寫 blocked UIAction，不會修改任何資料。",
      "outputs": [
        {
          "item_id": "acc_fire_cloak",
          "label": "抗火斗篷",
          "quantity": 1
        }
      ],
      "primary_action": {
        "action_id": "craft_recipe",
        "label": "素材不足",
        "enabled": false,
        "disabled_reason": "需要 300G、火焰石 x3、焦黑鐵礦 x2；目前 90G、火焰石 x1、焦黑鐵礦 x0。",
        "payload": {
          "recipe_id": "recipe_fire_cloak"
        }
      },
      "blocked_feedback": {
        "tone": "warning",
        "speaker": "米菈",
        "text": "這張配方缺金幣和素材。先去補給或探索會比較穩。"
      }
    },
    "recipe_focus_pouch": {
      "title": "集中藥袋",
      "description": "每趟迷宮前整理集中滴露的輔助裝備。這裡示範只缺金幣的狀態。",
      "effect": "每次進入迷宮時取得集中滴露 x1。",
      "base_note": "基底：不需要基底裝備。",
      "notes": "金幣不足時 primary action disabled。",
      "outputs": [
        {
          "item_id": "special_focus_pouch",
          "label": "集中藥袋",
          "quantity": 1
        }
      ],
      "primary_action": {
        "action_id": "craft_recipe",
        "label": "金幣不足",
        "enabled": false,
        "disabled_reason": "需要 140G，目前 90G。",
        "payload": {
          "recipe_id": "recipe_focus_pouch"
        }
      },
      "blocked_feedback": {
        "tone": "warning",
        "speaker": "米菈",
        "text": "素材齊了，但工錢不夠。"
      }
    },
    "recipe_heat_charm": {
      "title": "暖石墜改",
      "description": "把暖石墜重新封入熔岩碎片，換取更穩定的火抗與些微敏捷。",
      "effect": "火傷害 -18%，敏捷 +1。",
      "base_note": "基底：需要暖石墜 x1；目前背包與裝備都沒有。",
      "notes": "此 fixture 的預設選取配方用來驗證基底不足。",
      "outputs": [
        {
          "item_id": "acc_warm_stone_plus",
          "label": "暖石墜改",
          "quantity": 1
        }
      ],
      "primary_action": {
        "action_id": "craft_recipe",
        "label": "基底不足",
        "enabled": false,
        "disabled_reason": "需要暖石墜 x1，目前沒有可消耗的基底裝備。",
        "payload": {
          "recipe_id": "recipe_heat_charm"
        }
      },
      "blocked_feedback": {
        "tone": "warning",
        "speaker": "米菈",
        "text": "這不是從零做起的配方。先準備暖石墜，再來改造。"
      }
    },
    "recipe_piercing_bundle": {
      "title": "破甲釘組",
      "description": "把焦黑鐵礦與破裂石片磨成簡易釘組，方便在戰鬥中削弱敵方防禦。",
      "effect": "取得破甲釘 x3。",
      "base_note": "基底：不需要基底裝備。",
      "notes": "戰術道具分類在 constrained 狀態也可被過濾檢查。",
      "outputs": [
        {
          "item_id": "item_armor_piercer",
          "label": "破甲釘",
          "quantity": 3
        }
      ],
      "primary_action": {
        "action_id": "craft_recipe",
        "label": "金幣不足",
        "enabled": false,
        "disabled_reason": "需要 120G，目前 90G。",
        "payload": {
          "recipe_id": "recipe_piercing_bundle"
        }
      },
      "blocked_feedback": {
        "tone": "warning",
        "speaker": "米菈",
        "text": "破甲釘不難做，但至少要付得起材料處理費。"
      }
    }
  },
  "requirement_rows": {
    "recipe_fire_cloak": [
      {
        "id": "gold",
        "icon_label": "G",
        "label": "金幣",
        "required_value": "300G",
        "current_value": "90G",
        "status": "missing",
        "status_label": "不足",
        "disabled_reason": "需要 300G，目前 90G。"
      },
      {
        "id": "mat_fire_stone",
        "icon_label": "火",
        "label": "火焰石",
        "required_value": "x3",
        "current_value": "x1",
        "status": "missing",
        "status_label": "不足",
        "disabled_reason": "需要火焰石 x3，目前 x1。"
      },
      {
        "id": "mat_scorched_iron",
        "icon_label": "鐵",
        "label": "焦黑鐵礦",
        "required_value": "x2",
        "current_value": "x0",
        "status": "missing",
        "status_label": "不足",
        "disabled_reason": "需要焦黑鐵礦 x2，目前 x0。"
      }
    ],
    "recipe_focus_pouch": [
      {
        "id": "gold",
        "icon_label": "G",
        "label": "金幣",
        "required_value": "140G",
        "current_value": "90G",
        "status": "missing",
        "status_label": "不足",
        "disabled_reason": "需要 140G，目前 90G。"
      },
      {
        "id": "mat_moss_fiber",
        "icon_label": "苔",
        "label": "青苔纖維",
        "required_value": "x3",
        "current_value": "x4",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      },
      {
        "id": "mat_small_crystal",
        "icon_label": "晶",
        "label": "小魔晶",
        "required_value": "x2",
        "current_value": "x2",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      }
    ],
    "recipe_heat_charm": [
      {
        "id": "gold",
        "icon_label": "G",
        "label": "金幣",
        "required_value": "260G",
        "current_value": "90G",
        "status": "missing",
        "status_label": "不足",
        "disabled_reason": "需要 260G，目前 90G。"
      },
      {
        "id": "base_acc_warm_stone",
        "icon_label": "基",
        "label": "基底裝備：暖石墜",
        "required_value": "x1",
        "current_value": "x0",
        "status": "missing",
        "status_label": "不足",
        "disabled_reason": "需要暖石墜 x1，目前沒有可消耗的基底裝備。"
      },
      {
        "id": "mat_lava_shard",
        "icon_label": "熔",
        "label": "熔岩碎片",
        "required_value": "x1",
        "current_value": "x2",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      }
    ],
    "recipe_piercing_bundle": [
      {
        "id": "gold",
        "icon_label": "G",
        "label": "金幣",
        "required_value": "120G",
        "current_value": "90G",
        "status": "missing",
        "status_label": "不足",
        "disabled_reason": "需要 120G，目前 90G。"
      },
      {
        "id": "mat_scorched_iron",
        "icon_label": "鐵",
        "label": "焦黑鐵礦",
        "required_value": "x2",
        "current_value": "x2",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      },
      {
        "id": "mat_cracked_stone",
        "icon_label": "石",
        "label": "破裂石片",
        "required_value": "x3",
        "current_value": "x4",
        "status": "met",
        "status_label": "已滿足",
        "disabled_reason": null
      }
    ]
  },
  "feedback_message": {
    "tone": "warning",
    "speaker": "米菈",
    "text": "這個測試狀態會保留缺口，不會嘗試替你自動補材料。"
  },
  "empty_state": {
    "message": "目前沒有符合分類的可用配方。"
  },
  "debug_notes": [
    "Constrained Synthesis fixture is static display data only.",
    "Blocked craft action logs UIAction and shows disabled_reason.",
    "No runtime synthesis, inventory mutation, gold mutation, or save writes are performed."
  ]
};
