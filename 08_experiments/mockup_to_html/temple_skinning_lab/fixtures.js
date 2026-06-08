/**
 * temple_skinning_lab — Fixture Data Capsule
 * Auto-generated from official static prototype fixtures.
 */

window.TEMPLE_DEFAULT_FIXTURE = {
  "screen_id": "temple_screen",
  "title": "轉職神殿 (Temple & Church)",
  "subtitle": "在此沐浴月神光華，進行職業晉升宣誓或查閱古代碑文。",
  "resource_strip": [
    {
      "id": "hp",
      "label": "HP 183/192",
      "tone": "primary"
    },
    {
      "id": "mp",
      "label": "MP 38/38",
      "tone": "mp"
    },
    {
      "id": "gold",
      "label": "1957G",
      "tone": "gold"
    }
  ],
  "moon_well": {
    "label": "月神之井",
    "description": "汲取蘊藏魔力的露水進行祈福，可隨機獲得全隊屬性微幅抗性加成。",
    "cost": 30,
    "enabled": true,
    "payload": {
      "altar_action": "pray",
      "cost": 30
    }
  },
  "promotions": [
    {
      "class_id": "paladin",
      "label": "聖騎士 (Paladin)",
      "description": "二階防禦型戰士。掌握基礎光之奇蹟，獲得強大護甲與治癒恩賜。",
      "requirements": [
        {
          "name": "冒險者等級 10 級",
          "current": "Lv7 / Lv10",
          "satisfied": false
        },
        {
          "name": "轉職黃金 1000G",
          "current": "1957G / 1000G",
          "satisfied": true
        }
      ],
      "enabled": false,
      "disabled_reason": "等級不足，請先提升實力。"
    },
    {
      "class_id": "berserker",
      "label": "狂戰士 (Berserker)",
      "description": "二階攻擊型戰士。捨棄盾牌，以怒氣與生命為代價換取極限破壞力。",
      "requirements": [
        {
          "name": "冒險者等級 10 級",
          "current": "Lv7 / Lv10",
          "satisfied": false
        },
        {
          "name": "轉職黃金 1000G",
          "current": "1957G / 1000G",
          "satisfied": true
        }
      ],
      "enabled": false,
      "disabled_reason": "等級不足，請先提升實力。"
    }
  ],
  "inquiries": [
    {
      "inquiry_id": "fire_mark_inquiry",
      "label": "詢問火之印記碎片",
      "description": "向賽恩大祭司展示獲得的火焰碎片，以解譯古代文字。",
      "enabled": true,
      "payload": {
        "inquiry_id": "fire_mark_lore"
      },
      "response_text": "大祭司賽恩凝視著碎片，輕聲說道：『這碎片殘留著熾熱的古老氣息，其上的刻印早已殘缺不全。也許在邊境更深處的熔岩流動中，能尋得它原本的來歷...』"
    }
  ]
};
