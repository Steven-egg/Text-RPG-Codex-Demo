/**
 * inn_skinning_lab — Fixture Data Capsule
 * Auto-generated from official static prototype fixtures.
 */

window.INN_DEFAULT_FIXTURE = {
  "screen_id": "inn_screen",
  "title": "旅店 (Ember Inn)",
  "subtitle": "提供體力與魔力回復，並可在此聆聽各路傳聞。",
  "resource_strip": [
    {
      "id": "hp",
      "label": "HP 120/192",
      "tone": "warning"
    },
    {
      "id": "mp",
      "label": "MP 15/38",
      "tone": "mp"
    },
    {
      "id": "gold",
      "label": "1957G",
      "tone": "gold"
    }
  ],
  "service": {
    "service_id": "overnight_rest",
    "label": "過夜休息 (Overnight Rest)",
    "cost": 30,
    "description": "花費 30 金幣在客房中休息一晚，將當前 HP 與 MP 完全恢復至最大值。",
    "enabled": true,
    "disabled_reason": null,
    "payload": {
      "service_id": "overnight_rest",
      "cost": 30
    }
  },
  "npc": {
    "name": "莉莉 (Lily)",
    "description": "旅店老闆娘。性格溫柔且熱心，用熱騰騰的燉湯與乾淨的床鋪迎接疲憊的旅人。",
    "avatar_token": "LY",
    "prompt": "辛苦了，年輕的冒險者。喝碗熱騰騰的濃湯，然後好好睡一覺吧！"
  },
  "rumors": [
    {
      "title": "【流言】裂谷的巨石守衛",
      "content": "工會偵察員回報，灰燼裂谷深處沉睡著由熔岩構成的巨石守衛，極度危險..."
    },
    {
      "title": "【傳聞】火之印記碎片",
      "content": "古老的火之印記被震裂成三片，唯有擊敗最強大的守護魔物才能回收並查明真相..."
    }
  ]
};
