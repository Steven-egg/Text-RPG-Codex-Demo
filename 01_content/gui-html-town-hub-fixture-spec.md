# HTML Town Hub Fixture Spec

用途：定義 HTML Town Hub static prototype 的 fixture 內容。此文件只做 markdown-only fixture specification，不建立 `07_gui_prototype/`，不寫 HTML / CSS / JS，不接 runtime。

## 0. Status

```text
fixture_scope: town_hub_static_html_prototype
spec_date: 2026-05-19
status: fixture_spec_only
implementation_status: not_started
runtime_adapter_status: not_started
asset_pipeline_status: not_started
```

參考：

- `01_content/gui-html-town-hub-prototype-plan.md`
- `01_content/gui-town-hub-screen-model-draft.md`
- `01_content/gui-town-hub-programmatic-layout-plan-v1.md`
- `01_content/gui-town-hub-facility-node-mapping-v1.md`

## 1. Boundary

- 不修改 runtime、data、schema、save 或 combat formula。
- 不讀取或改動 `03_engine/engine/game.py`。
- 不建立 prototype 目錄。
- 不寫 HTML / CSS / JS。
- 不讀寫 `save.json`。
- 不讓 JS 複製 Python gameplay logic。
- 不把 fixture 視為資料 SSOT。
- 不啟動正式 asset pipeline。

## 2. Fixture Files

未來若建立 HTML prototype，建議先放兩個 fixture：

```text
07_gui_prototype/town_hub/fixtures/town-hub-default.json
07_gui_prototype/town_hub/fixtures/town-hub-alerts.json
```

兩份 fixture 都是 static display data，只用來驗證 render layer。

## 3. Shared Schema

```text
TownHubScreenModelFixture
- screen_id
- title
- subtitle
- resource_strip[]
- town_guidance[]
- selected_facility_id
- facility_nodes[]
- navigation_actions[]
- global_actions[]
- debug_notes[]
```

### `resource_strip[]`

```text
ResourceItem
- id
- label
- tone
```

`tone` 只給 prototype style 使用，不是 gameplay。

### `facility_nodes[]`

```text
TownFacilityNode
- facility_id
- label
- description
- visual_group
- visual_anchor
- icon_role
- enabled
- disabled_reason
- badges[]
- primary_action
- payload
```

### `badges[]`

```text
FacilityBadge
- badge_id
- label
- kind
- priority
```

### `navigation_actions[]` / `global_actions[]`

```text
UIActionItem
- action_id
- label
- description
- enabled
- disabled_reason
- payload
```

## 4. `town-hub-default.json`

用途：

- 驗證沒有 urgent alert 時的基本可讀性。
- 驗證所有 facility nodes 都能掃讀。
- 驗證 Town Hub 不是按鈕牆，而是場景式 facility hub。

```json
{
  "screen_id": "town_hub",
  "title": "艾爾姆城鎮",
  "subtitle": "冒險者的據點與補給中心",
  "resource_strip": [
    { "id": "hero", "label": "莉亞 / 盜賊 Lv8", "tone": "primary" },
    { "id": "hp", "label": "HP 86/86", "tone": "healthy" },
    { "id": "mp", "label": "MP 34/40", "tone": "mana" },
    { "id": "gold", "label": "420G", "tone": "gold" },
    { "id": "guild_points", "label": "工會積分 12", "tone": "neutral" }
  ],
  "town_guidance": [
    "把探索收益轉成任務、裝備、技能或補給後再出發。"
  ],
  "selected_facility_id": "guild",
  "facility_nodes": [
    {
      "facility_id": "guild",
      "label": "工會委託所",
      "description": "接受與回報任務",
      "visual_group": "guild",
      "visual_anchor": "top_center_guild_hall",
      "icon_role": "guild",
      "enabled": true,
      "disabled_reason": null,
      "badges": [
        {
          "badge_id": "quest_ready",
          "label": "可回報",
          "kind": "notification",
          "priority": 80
        }
      ],
      "primary_action": "open_facility",
      "payload": { "facility_id": "guild" }
    },
    {
      "facility_id": "inn",
      "label": "旅館",
      "description": "休息恢復 HP/MP",
      "visual_group": "rest",
      "visual_anchor": "left_inn",
      "icon_role": "bed",
      "enabled": true,
      "disabled_reason": null,
      "badges": [],
      "primary_action": "open_facility",
      "payload": { "facility_id": "inn" }
    },
    {
      "facility_id": "travel_shop",
      "label": "旅人小鋪",
      "description": "購買補給與戰術道具",
      "visual_group": "shop",
      "visual_anchor": "mid_left_market",
      "icon_role": "shop",
      "enabled": true,
      "disabled_reason": null,
      "badges": [],
      "primary_action": "open_facility",
      "payload": { "facility_id": "travel_shop" }
    },
    {
      "facility_id": "workshop",
      "label": "工坊",
      "description": "武器與防具的購買、強化",
      "visual_group": "workshop",
      "visual_anchor": "right_workshop_group",
      "icon_role": "hammer",
      "enabled": true,
      "disabled_reason": null,
      "badges": [],
      "primary_action": "open_facility",
      "payload": { "facility_id": "workshop" }
    },
    {
      "facility_id": "synthesis",
      "label": "米菈合成屋",
      "description": "素材合成與道具轉換",
      "visual_group": "alchemy",
      "visual_anchor": "bottom_left_alchemy",
      "icon_role": "alchemy",
      "enabled": true,
      "disabled_reason": null,
      "badges": [],
      "primary_action": "open_facility",
      "payload": { "facility_id": "synthesis" }
    },
    {
      "facility_id": "magic_shop",
      "label": "星燈魔法商店",
      "description": "學習永久技能與魔法",
      "visual_group": "magic",
      "visual_anchor": "right_arcane_shop",
      "icon_role": "magic",
      "enabled": true,
      "disabled_reason": null,
      "badges": [],
      "primary_action": "open_facility",
      "payload": { "facility_id": "magic_shop" }
    },
    {
      "facility_id": "temple",
      "label": "轉職神殿",
      "description": "轉職與火印查閱",
      "visual_group": "temple",
      "visual_anchor": "bottom_center_temple",
      "icon_role": "temple",
      "enabled": true,
      "disabled_reason": null,
      "badges": [],
      "primary_action": "open_facility",
      "payload": { "facility_id": "temple" }
    },
    {
      "facility_id": "relic_preview",
      "label": "聖物調查所",
      "description": "查看未開放的聖物線索",
      "visual_group": "archive",
      "visual_anchor": "bottom_right_archive",
      "icon_role": "relic",
      "enabled": true,
      "disabled_reason": null,
      "badges": [],
      "primary_action": "open_facility",
      "payload": { "facility_id": "relic_preview" }
    },
    {
      "facility_id": "storage",
      "label": "倉庫",
      "description": "存取非關鍵物品",
      "visual_group": "storage",
      "visual_anchor": "far_bottom_right_depot",
      "icon_role": "storage",
      "enabled": true,
      "disabled_reason": null,
      "badges": [],
      "primary_action": "open_facility",
      "payload": { "facility_id": "storage" }
    }
  ],
  "navigation_actions": [
    {
      "action_id": "open_world_map",
      "label": "返回世界地圖",
      "description": "回到目的地選擇",
      "enabled": true,
      "disabled_reason": null,
      "payload": {}
    }
  ],
  "global_actions": [
    {
      "action_id": "open_character",
      "label": "角色",
      "description": "查看角色狀態",
      "enabled": true,
      "disabled_reason": null,
      "payload": {}
    },
    {
      "action_id": "open_inventory",
      "label": "背包",
      "description": "查看持有物品",
      "enabled": true,
      "disabled_reason": null,
      "payload": {}
    }
  ],
  "debug_notes": [
    "Default fixture is static display data only.",
    "Do not treat fixture values as gameplay SSOT.",
    "World map is navigation, not facility node."
  ]
}
```

## 5. `town-hub-alerts.json`

用途：

- 驗證 high-value badge。
- 驗證 disabled node。
- 驗證低 HP / 無藥水或火印提示的 `town_guidance`。

```json
{
  "screen_id": "town_hub",
  "title": "艾爾姆城鎮",
  "subtitle": "冒險者的據點與補給中心",
  "resource_strip": [
    { "id": "hero", "label": "莉亞 / 盜賊 Lv12", "tone": "primary" },
    { "id": "hp", "label": "HP 24/96", "tone": "danger" },
    { "id": "mp", "label": "MP 18/44", "tone": "mana" },
    { "id": "gold", "label": "760G", "tone": "gold" },
    { "id": "guild_points", "label": "工會積分 28", "tone": "neutral" }
  ],
  "town_guidance": [
    "三枚火之印記碎片正在共鳴，回冒險者工會詢問諾亞。",
    "HP 偏低，出發前可考慮旅館或補給。"
  ],
  "selected_facility_id": "synthesis",
  "facility_nodes": [
    {
      "facility_id": "guild",
      "label": "工會委託所",
      "description": "接受與回報任務",
      "visual_group": "guild",
      "visual_anchor": "top_center_guild_hall",
      "icon_role": "guild",
      "enabled": true,
      "disabled_reason": null,
      "badges": [
        {
          "badge_id": "fire_mark_hint",
          "label": "火印線索",
          "kind": "notification",
          "priority": 100
        }
      ],
      "primary_action": "open_facility",
      "payload": { "facility_id": "guild" }
    },
    {
      "facility_id": "inn",
      "label": "旅館",
      "description": "休息恢復 HP/MP",
      "visual_group": "rest",
      "visual_anchor": "left_inn",
      "icon_role": "bed",
      "enabled": true,
      "disabled_reason": null,
      "badges": [],
      "primary_action": "open_facility",
      "payload": { "facility_id": "inn" }
    },
    {
      "facility_id": "travel_shop",
      "label": "旅人小鋪",
      "description": "購買補給與戰術道具",
      "visual_group": "shop",
      "visual_anchor": "mid_left_market",
      "icon_role": "shop",
      "enabled": true,
      "disabled_reason": null,
      "badges": [],
      "primary_action": "open_facility",
      "payload": { "facility_id": "travel_shop" }
    },
    {
      "facility_id": "workshop",
      "label": "工坊",
      "description": "武器與防具的購買、強化",
      "visual_group": "workshop",
      "visual_anchor": "right_workshop_group",
      "icon_role": "hammer",
      "enabled": true,
      "disabled_reason": null,
      "badges": [],
      "primary_action": "open_facility",
      "payload": { "facility_id": "workshop" }
    },
    {
      "facility_id": "synthesis",
      "label": "米菈合成屋",
      "description": "素材合成與道具轉換",
      "visual_group": "alchemy",
      "visual_anchor": "bottom_left_alchemy",
      "icon_role": "alchemy",
      "enabled": false,
      "disabled_reason": "完成工會任務「洞窟採集」後開放。",
      "badges": [
        {
          "badge_id": "locked",
          "label": "未解鎖",
          "kind": "status",
          "priority": 70
        }
      ],
      "primary_action": "open_facility",
      "payload": { "facility_id": "synthesis" }
    },
    {
      "facility_id": "magic_shop",
      "label": "星燈魔法商店",
      "description": "學習永久技能與魔法",
      "visual_group": "magic",
      "visual_anchor": "right_arcane_shop",
      "icon_role": "magic",
      "enabled": true,
      "disabled_reason": null,
      "badges": [],
      "primary_action": "open_facility",
      "payload": { "facility_id": "magic_shop" }
    },
    {
      "facility_id": "temple",
      "label": "轉職神殿",
      "description": "轉職與火印查閱",
      "visual_group": "temple",
      "visual_anchor": "bottom_center_temple",
      "icon_role": "temple",
      "enabled": true,
      "disabled_reason": null,
      "badges": [
        {
          "badge_id": "fire_mark_lookup",
          "label": "可查閱",
          "kind": "notification",
          "priority": 60
        }
      ],
      "primary_action": "open_facility",
      "payload": { "facility_id": "temple" }
    },
    {
      "facility_id": "relic_preview",
      "label": "聖物調查所",
      "description": "查看未開放的聖物線索",
      "visual_group": "archive",
      "visual_anchor": "bottom_right_archive",
      "icon_role": "relic",
      "enabled": true,
      "disabled_reason": null,
      "badges": [],
      "primary_action": "open_facility",
      "payload": { "facility_id": "relic_preview" }
    },
    {
      "facility_id": "storage",
      "label": "倉庫",
      "description": "存取非關鍵物品",
      "visual_group": "storage",
      "visual_anchor": "far_bottom_right_depot",
      "icon_role": "storage",
      "enabled": false,
      "disabled_reason": "倉庫功能尚未開啟。",
      "badges": [
        {
          "badge_id": "storage_closed",
          "label": "未開啟",
          "kind": "status",
          "priority": 50
        }
      ],
      "primary_action": "open_facility",
      "payload": { "facility_id": "storage" }
    }
  ],
  "navigation_actions": [
    {
      "action_id": "open_world_map",
      "label": "返回世界地圖",
      "description": "回到目的地選擇",
      "enabled": true,
      "disabled_reason": null,
      "payload": {}
    }
  ],
  "global_actions": [
    {
      "action_id": "open_character",
      "label": "角色",
      "description": "查看角色狀態",
      "enabled": true,
      "disabled_reason": null,
      "payload": {}
    },
    {
      "action_id": "open_inventory",
      "label": "背包",
      "description": "查看持有物品",
      "enabled": true,
      "disabled_reason": null,
      "payload": {}
    }
  ],
  "debug_notes": [
    "Alerts fixture is static display data only.",
    "Disabled nodes should be focusable but should not dispatch open_facility.",
    "Low HP guidance should not force inn or shop badges."
  ]
}
```

## 6. Rendering Expectations

HTML prototype should:

- Render all text from fixture.
- Render all nodes from `facility_nodes`.
- Render `navigation_actions` separately from facility nodes.
- Render `global_actions` separately from facility nodes.
- Sort badges by `priority` and show only the highest-priority badge per node.
- Allow disabled nodes to be selected / focused.
- Show disabled reason in selected detail or guidance area.
- Log action payloads rather than calling runtime.

HTML prototype should not:

- Hard-code any facility label in HTML.
- Hard-code badge text in CSS.
- Calculate unlock rules.
- Read or write save.
- Import runtime modules.
- Use generated mockup candidate as background.

## 7. Prototype Fixture Acceptance

Fixture spec is acceptable when future implementation can:

- Load both fixtures.
- Switch fixture state without code changes.
- Render all 9 facility nodes.
- Render at least one notification badge.
- Render at least one status badge.
- Render at least one disabled node.
- Render two-line town guidance.
- Dispatch `open_facility`, `open_world_map`, `open_character`, and `open_inventory` as logs.

## 8. Recommended Next Session Start

下一個 session 若要開始實作，建議最小讀取：

1. `01_content/gui-planning-index.md`
2. `01_content/gui-implementation-platform-tradeoff.md`
3. `01_content/gui-html-town-hub-prototype-plan.md`
4. `01_content/gui-html-town-hub-fixture-spec.md`

然後建立：

```text
07_gui_prototype/town_hub/
- index.html
- styles.css
- town-hub.js
- fixtures/town-hub-default.json
- fixtures/town-hub-alerts.json
```

仍不接 runtime、不讀寫 save、不啟動正式 asset pipeline。

