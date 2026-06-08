/**
 * storage_skinning_lab — Fixture Data Capsule
 * Auto-generated from official static prototype fixtures.
 */

window.STORAGE_LOCKED_FIXTURE = {
  "screen_id": "storage_screen",
  "facility_id": "storage",
  "title": "工會倉庫",
  "subtitle": "存放與取出非關鍵物品，保障行囊空間",
  "selected_mode": "deposit",
  "selected_item_id": null,
  "storage_state": {
    "unlocked": false,
    "unlock_cost": 500,
    "can_unlock": false,
    "disabled_reason": "金幣不足以支付開啟費用"
  },
  "resource_strip": [
    {
      "id": "player_name",
      "label": "米菈的小隊",
      "tone": "neutral"
    },
    {
      "id": "player_gold",
      "label": "金幣：420G",
      "tone": "warning"
    },
    {
      "id": "storage_status",
      "label": "倉庫狀態：未開啟",
      "tone": "danger"
    },
    {
      "id": "storage_capacity",
      "label": "容量：0 / 10 種物品",
      "tone": "neutral"
    }
  ],
  "npc": {
    "name": "諾亞",
    "role": "冒險者工會會長",
    "portrait_placeholder": "Noah",
    "avatar_text": "「普通素材可以寄放在這裡，貴重物品請隨身保管。」",
    "dialog_locked": "花費 500G 金幣可為米菈小隊解鎖工會專屬的無限期保管箱。"
  },
  "category_tabs": [
    {
      "id": "all",
      "label": "全部",
      "count": 2,
      "enabled": true
    },
    {
      "id": "materials",
      "label": "材料",
      "count": 1,
      "enabled": true
    },
    {
      "id": "consumables",
      "label": "消耗品",
      "count": 1,
      "enabled": true
    },
    {
      "id": "equipment",
      "label": "裝備",
      "count": 0,
      "enabled": true
    },
    {
      "id": "valuables",
      "label": "貴重物",
      "count": 0,
      "enabled": true
    }
  ],
  "inventory_rows": [
    {
      "item_id": "mat_iron_ore",
      "title": "鐵礦石",
      "category": "materials",
      "short_title": "鐵礦",
      "summary": "普通金屬素材 / 持有：5",
      "owned_count": 5,
      "enabled": false,
      "disabled_reason": "倉庫未開啟"
    },
    {
      "item_id": "item_potion_s",
      "title": "微效生命藥水",
      "category": "consumables",
      "short_title": "小生命",
      "summary": "消耗品 / 持有：3",
      "owned_count": 3,
      "enabled": false,
      "disabled_reason": "倉庫未開啟"
    }
  ],
  "storage_rows": [],
  "item_details": {
    "mat_iron_ore": {
      "item_id": "mat_iron_ore",
      "title": "鐵礦石",
      "category_label": "普通素材",
      "description": "散發微弱金屬光澤的粗糙礦石，常用於裝備的鍛造與強化。",
      "effect_summary": "無直接效果",
      "use_context": "工坊強化、合成材料"
    },
    "item_potion_s": {
      "item_id": "item_potion_s",
      "title": "微效生命藥水",
      "category_label": "消耗性道具",
      "description": "工會配發的微效藥水，能回復少許生命值。",
      "effect_summary": "戰鬥中或探索中回復 20 點生命值",
      "use_context": "生存與恢復"
    }
  },
  "primary_actions": {
    "unlock_storage": {
      "action_id": "unlock_storage",
      "label": "解鎖倉庫 (500G)",
      "enabled": false,
      "disabled_reason": "金幣不足，需要 500G",
      "payload": {
        "cost": 500
      }
    }
  },
  "requirement_rows": {
    "unlock_storage": [
      {
        "id": "req_gold",
        "label": "金幣需求",
        "required_value": "500G",
        "current_value": "420G",
        "status": "unmet",
        "disabled_reason": "金幣不足"
      }
    ]
  }
};

window.STORAGE_EMPTY_FIXTURE = {
  "screen_id": "storage_screen",
  "facility_id": "storage",
  "title": "工會倉庫",
  "subtitle": "存放與取出非關鍵物品，保障行囊空間",
  "selected_mode": "deposit",
  "selected_item_id": null,
  "storage_state": {
    "unlocked": true,
    "unlock_cost": 0,
    "can_unlock": false,
    "disabled_reason": ""
  },
  "resource_strip": [
    {
      "id": "player_name",
      "label": "米菈的小隊",
      "tone": "neutral"
    },
    {
      "id": "player_gold",
      "label": "金幣：1250G",
      "tone": "neutral"
    },
    {
      "id": "storage_status",
      "label": "倉庫狀態：已解鎖",
      "tone": "success"
    },
    {
      "id": "storage_capacity",
      "label": "容量：0 / 10 種物品",
      "tone": "success"
    }
  ],
  "npc": {
    "name": "諾亞",
    "role": "冒險者工會會長",
    "portrait_placeholder": "Noah",
    "avatar_text": "「普通素材可以寄放在這裡，貴重物品請隨身保管。」",
    "dialog_locked": "選擇背包的格子物品，即可直接存入工會倉庫中。"
  },
  "category_tabs": [
    {
      "id": "all",
      "label": "全部",
      "count": 2,
      "enabled": true
    },
    {
      "id": "materials",
      "label": "材料",
      "count": 1,
      "enabled": true
    },
    {
      "id": "consumables",
      "label": "消耗品",
      "count": 1,
      "enabled": true
    },
    {
      "id": "equipment",
      "label": "裝備",
      "count": 0,
      "enabled": true
    },
    {
      "id": "valuables",
      "label": "貴重物",
      "count": 0,
      "enabled": true
    }
  ],
  "inventory_rows": [
    {
      "item_id": "mat_iron_ore",
      "title": "鐵礦石",
      "category": "materials",
      "short_title": "鐵礦",
      "summary": "普通金屬素材 / 持有：5",
      "owned_count": 5,
      "enabled": true,
      "disabled_reason": ""
    },
    {
      "item_id": "item_potion_s",
      "title": "微效生命藥水",
      "category": "consumables",
      "short_title": "小生命",
      "summary": "消耗品 / 持有：3",
      "owned_count": 3,
      "enabled": true,
      "disabled_reason": ""
    }
  ],
  "storage_rows": [],
  "item_details": {
    "mat_iron_ore": {
      "item_id": "mat_iron_ore",
      "title": "鐵礦石",
      "category_label": "普通素材",
      "description": "散發微弱金屬光澤的粗糙礦石，常用於裝備的鍛造與強化。",
      "effect_summary": "無直接效果",
      "use_context": "工坊強化、合成材料"
    },
    "item_potion_s": {
      "item_id": "item_potion_s",
      "title": "微效生命藥水",
      "category_label": "消耗性道具",
      "description": "工會配發的微效藥水，能回復少許生命值。",
      "effect_summary": "戰鬥中或探索中回復 20 點生命值",
      "use_context": "生存與恢復"
    }
  },
  "primary_actions": {
    "upgrade_storage": {
      "action_id": "upgrade_storage",
      "label": "升級倉庫容量 (未開放)",
      "enabled": false,
      "disabled_reason": "工會目前尚未開放更高級別的擴充服務",
      "payload": {}
    },
    "mat_iron_ore": {
      "action_id": "deposit_item",
      "label": "確認存入",
      "enabled": true,
      "disabled_reason": "",
      "payload": {
        "item_id": "mat_iron_ore",
        "quantity": 1
      }
    },
    "item_potion_s": {
      "action_id": "deposit_item",
      "label": "確認存入",
      "enabled": true,
      "disabled_reason": "",
      "payload": {
        "item_id": "item_potion_s",
        "quantity": 1
      }
    }
  },
  "requirement_rows": {
    "mat_iron_ore": [
      {
        "id": "req_ownership",
        "label": "背包持有量",
        "required_value": ">= 1",
        "current_value": "5 個",
        "status": "met",
        "disabled_reason": ""
      },
      {
        "id": "req_storage_cap",
        "label": "倉庫可用容量",
        "required_value": "< 10 種",
        "current_value": "0 種已用",
        "status": "met",
        "disabled_reason": ""
      }
    ],
    "item_potion_s": [
      {
        "id": "req_ownership",
        "label": "背包持有量",
        "required_value": ">= 1",
        "current_value": "3 個",
        "status": "met",
        "disabled_reason": ""
      },
      {
        "id": "req_storage_cap",
        "label": "倉庫可用容量",
        "required_value": "< 10 種",
        "current_value": "0 種已用",
        "status": "met",
        "disabled_reason": ""
      }
    ]
  }
};

window.STORAGE_FILLED_FIXTURE = {
  "screen_id": "storage_screen",
  "facility_id": "storage",
  "title": "工會倉庫",
  "subtitle": "存放與取出非關鍵物品，保障行囊空間",
  "selected_mode": "deposit",
  "selected_item_id": null,
  "storage_state": {
    "unlocked": true,
    "unlock_cost": 0,
    "can_unlock": false,
    "disabled_reason": ""
  },
  "resource_strip": [
    {
      "id": "player_name",
      "label": "米菈的小隊",
      "tone": "neutral"
    },
    {
      "id": "player_gold",
      "label": "金幣：1250G",
      "tone": "neutral"
    },
    {
      "id": "storage_status",
      "label": "倉庫狀態：已解鎖",
      "tone": "success"
    },
    {
      "id": "storage_capacity",
      "label": "容量：2 / 10 種物品",
      "tone": "neutral"
    }
  ],
  "npc": {
    "name": "諾亞",
    "role": "冒險者工會會長",
    "portrait_placeholder": "Noah",
    "avatar_text": "「普通素材可以寄放在這裡，貴重物品請隨身保管。」",
    "dialog_locked": "點選背包格子以存入，點選倉庫格子以取出物品。"
  },
  "category_tabs": [
    {
      "id": "all",
      "label": "全部",
      "count": 2,
      "enabled": true
    },
    {
      "id": "materials",
      "label": "材料",
      "count": 1,
      "enabled": true
    },
    {
      "id": "consumables",
      "label": "消耗品",
      "count": 1,
      "enabled": true
    },
    {
      "id": "equipment",
      "label": "裝備",
      "count": 0,
      "enabled": true
    },
    {
      "id": "valuables",
      "label": "貴重物",
      "count": 0,
      "enabled": true
    }
  ],
  "inventory_rows": [
    {
      "item_id": "mat_iron_ore",
      "title": "鐵礦石",
      "category": "materials",
      "short_title": "鐵礦",
      "summary": "普通金屬素材 / 持有：5",
      "owned_count": 5,
      "enabled": true,
      "disabled_reason": ""
    },
    {
      "item_id": "item_potion_s",
      "title": "微效生命藥水",
      "category": "consumables",
      "short_title": "小生命",
      "summary": "消耗品 / 持有：3",
      "owned_count": 3,
      "enabled": true,
      "disabled_reason": ""
    }
  ],
  "storage_rows": [
    {
      "item_id": "mat_copper_powder",
      "title": "銅精粉",
      "category": "materials",
      "short_title": "銅粉",
      "summary": "精煉金屬粉末 / 倉庫：12",
      "owned_count": 12,
      "enabled": true,
      "disabled_reason": ""
    },
    {
      "item_id": "mat_cloth",
      "title": "普通布料",
      "category": "materials",
      "short_title": "布料",
      "summary": "日常編織素材 / 倉庫：8",
      "owned_count": 8,
      "enabled": true,
      "disabled_reason": ""
    }
  ],
  "item_details": {
    "mat_iron_ore": {
      "item_id": "mat_iron_ore",
      "title": "鐵礦石",
      "category_label": "普通素材 (背包)",
      "description": "散發微弱金屬光澤的粗糙礦石，常用於裝備的鍛造與強化。",
      "effect_summary": "無直接效果",
      "use_context": "工坊強化、合成材料"
    },
    "item_potion_s": {
      "item_id": "item_potion_s",
      "title": "微效生命藥水",
      "category_label": "消耗性道具 (背包)",
      "description": "工會配發的微效藥水，能回復少許生命值值。",
      "effect_summary": "戰鬥中或探索中回復 20 點生命值值",
      "use_context": "生存與恢復"
    },
    "mat_copper_powder": {
      "item_id": "mat_copper_powder",
      "title": "銅精粉",
      "category_label": "精煉素材 (倉庫)",
      "description": "經工會研磨篩選的高純度銅粉，常用於製作飾品與精密道具。",
      "effect_summary": "無直接效果",
      "use_context": "米菈合成屋材料"
    },
    "mat_cloth": {
      "item_id": "mat_cloth",
      "title": "普通布料",
      "category_label": "編織素材 (倉庫)",
      "description": "質地堅韌的白棉布，是製造防具與特殊藥袋的良好基底。",
      "effect_summary": "無直接效果",
      "use_context": "防具強化、配方合成"
    }
  },
  "primary_actions": {
    "upgrade_storage": {
      "action_id": "upgrade_storage",
      "label": "升級倉庫容量 (未開放)",
      "enabled": false,
      "disabled_reason": "工會目前尚未開放更高級別的擴充服務",
      "payload": {}
    },
    "mat_iron_ore": {
      "action_id": "deposit_item",
      "label": "確認存入",
      "enabled": true,
      "disabled_reason": "",
      "payload": {
        "item_id": "mat_iron_ore",
        "quantity": 1
      }
    },
    "item_potion_s": {
      "action_id": "deposit_item",
      "label": "確認存入",
      "enabled": true,
      "disabled_reason": "",
      "payload": {
        "item_id": "item_potion_s",
        "quantity": 1
      }
    },
    "mat_copper_powder": {
      "action_id": "withdraw_item",
      "label": "確認取出",
      "enabled": true,
      "disabled_reason": "",
      "payload": {
        "item_id": "mat_copper_powder",
        "quantity": 1
      }
    },
    "mat_cloth": {
      "action_id": "withdraw_item",
      "label": "確認取出",
      "enabled": true,
      "disabled_reason": "",
      "payload": {
        "item_id": "mat_cloth",
        "quantity": 1
      }
    }
  },
  "requirement_rows": {
    "mat_iron_ore": [
      {
        "id": "req_ownership",
        "label": "背包持有量",
        "required_value": ">= 1",
        "current_value": "5 個",
        "status": "met",
        "disabled_reason": ""
      },
      {
        "id": "req_storage_cap",
        "label": "倉庫可用容量",
        "required_value": "< 10 種",
        "current_value": "2 種已用",
        "status": "met",
        "disabled_reason": ""
      }
    ],
    "item_potion_s": [
      {
        "id": "req_ownership",
        "label": "背包持有量",
        "required_value": ">= 1",
        "current_value": "3 個",
        "status": "met",
        "disabled_reason": ""
      },
      {
        "id": "req_storage_cap",
        "label": "倉庫可用容量",
        "required_value": "< 10 種",
        "current_value": "2 種已用",
        "status": "met",
        "disabled_reason": ""
      }
    ],
    "mat_copper_powder": [
      {
        "id": "req_storage_count",
        "label": "倉庫儲存量",
        "required_value": ">= 1",
        "current_value": "12 個",
        "status": "met",
        "disabled_reason": ""
      }
    ],
    "mat_cloth": [
      {
        "id": "req_storage_count",
        "label": "倉庫儲存量",
        "required_value": ">= 1",
        "current_value": "8 個",
        "status": "met",
        "disabled_reason": ""
      }
    ]
  }
};

window.STORAGE_BLOCKED_FIXTURE = {
  "screen_id": "storage_screen",
  "facility_id": "storage",
  "title": "工會倉庫",
  "subtitle": "存放與取出非關鍵物品，保障行囊空間",
  "selected_mode": "deposit",
  "selected_item_id": null,
  "storage_state": {
    "unlocked": true,
    "unlock_cost": 0,
    "can_unlock": false,
    "disabled_reason": ""
  },
  "resource_strip": [
    {
      "id": "player_name",
      "label": "米菈的小隊",
      "tone": "neutral"
    },
    {
      "id": "player_gold",
      "label": "金幣：1250G",
      "tone": "neutral"
    },
    {
      "id": "storage_status",
      "label": "倉庫狀態：已解鎖",
      "tone": "success"
    },
    {
      "id": "storage_capacity",
      "label": "容量：10 / 10 種物品",
      "tone": "danger"
    }
  ],
  "npc": {
    "name": "諾亞",
    "role": "冒險者工會會長",
    "portrait_placeholder": "Noah",
    "avatar_text": "「普通素材可以寄放在這裡，貴重物品請隨身保管。」",
    "dialog_locked": "此物品無法寄放，請確認種類（貴重劇情物不可存放）或倉庫剩餘容量。"
  },
  "category_tabs": [
    {
      "id": "all",
      "label": "全部",
      "count": 2,
      "enabled": true
    },
    {
      "id": "materials",
      "label": "材料",
      "count": 1,
      "enabled": true
    },
    {
      "id": "consumables",
      "label": "消耗品",
      "count": 0,
      "enabled": true
    },
    {
      "id": "equipment",
      "label": "裝備",
      "count": 0,
      "enabled": true
    },
    {
      "id": "valuables",
      "label": "貴重物",
      "count": 1,
      "enabled": true
    }
  ],
  "inventory_rows": [
    {
      "item_id": "key_fire_mark_shard",
      "title": "火之印記碎片",
      "category": "valuables",
      "short_title": "火印碎片",
      "summary": "關鍵劇情道具 / 持有：3",
      "owned_count": 3,
      "enabled": false,
      "disabled_reason": "關鍵物品禁止存放"
    },
    {
      "item_id": "mat_iron_ore",
      "title": "鐵礦石",
      "category": "materials",
      "short_title": "鐵礦",
      "summary": "新金屬素材 / 持有：5",
      "owned_count": 5,
      "enabled": false,
      "disabled_reason": "倉庫容量已滿"
    }
  ],
  "storage_rows": [
    {
      "item_id": "mat_copper_powder",
      "title": "銅精粉",
      "category": "materials",
      "short_title": "銅粉",
      "summary": "精煉金屬粉末 / 倉庫：12",
      "owned_count": 12,
      "enabled": true,
      "disabled_reason": ""
    }
  ],
  "item_details": {
    "key_fire_mark_shard": {
      "item_id": "key_fire_mark_shard",
      "title": "火之印記碎片",
      "category_label": "關鍵道具 (貴重物)",
      "description": "古老火之印記分裂出的碎片，蘊藏溫熱的元素共鳴。事關重大，必須隨身攜帶。",
      "effect_summary": "無直接戰鬥效果",
      "use_context": "劇情關鍵任務與查閱"
    },
    "mat_iron_ore": {
      "item_id": "mat_iron_ore",
      "title": "鐵礦石",
      "category_label": "普通素材 (材料)",
      "description": "散發微弱金屬光澤的粗糙礦石，常用於裝備的鍛造與強化。",
      "effect_summary": "無直接效果",
      "use_context": "工坊強化、合成材料"
    },
    "mat_copper_powder": {
      "item_id": "mat_copper_powder",
      "title": "銅精粉",
      "category_label": "精煉素材 (倉庫)",
      "description": "經工會研磨篩選的高純度銅粉，常用於製作飾品與精密道具。",
      "effect_summary": "無直接效果",
      "use_context": "米菈合成屋材料"
    }
  },
  "primary_actions": {
    "upgrade_storage": {
      "action_id": "upgrade_storage",
      "label": "升級倉庫容量 (未開放)",
      "enabled": false,
      "disabled_reason": "工會目前尚未開放更高級別的擴充服務",
      "payload": {}
    },
    "key_fire_mark_shard": {
      "action_id": "blocked_action",
      "label": "禁止存放",
      "enabled": false,
      "disabled_reason": "關鍵劇情道具禁止存放",
      "payload": {
        "item_id": "key_fire_mark_shard"
      }
    },
    "mat_iron_ore": {
      "action_id": "blocked_action",
      "label": "倉庫已滿",
      "enabled": false,
      "disabled_reason": "倉庫容量已達 10/10，無法存入新物品種類",
      "payload": {
        "item_id": "mat_iron_ore"
      }
    },
    "mat_copper_powder": {
      "action_id": "withdraw_item",
      "label": "確認取出",
      "enabled": true,
      "disabled_reason": "",
      "payload": {
        "item_id": "mat_copper_powder",
        "quantity": 1
      }
    }
  },
  "requirement_rows": {
    "key_fire_mark_shard": [
      {
        "id": "req_key_item",
        "label": "物品類型限制",
        "required_value": "非關鍵道具",
        "current_value": "關鍵道具",
        "status": "unmet",
        "disabled_reason": "禁止存放"
      }
    ],
    "mat_iron_ore": [
      {
        "id": "req_ownership",
        "label": "背包持有量",
        "required_value": ">= 1",
        "current_value": "5 個",
        "status": "met",
        "disabled_reason": ""
      },
      {
        "id": "req_storage_cap",
        "label": "倉庫可用容量",
        "required_value": "< 10 種",
        "current_value": "10 種 (已滿)",
        "status": "unmet",
        "disabled_reason": "容量已達上限"
      }
    ],
    "mat_copper_powder": [
      {
        "id": "req_storage_count",
        "label": "倉庫儲存量",
        "required_value": ">= 1",
        "current_value": "12 個",
        "status": "met",
        "disabled_reason": ""
      }
    ]
  }
};
