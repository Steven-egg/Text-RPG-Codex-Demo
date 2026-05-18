# Town Hub UI-2 Wireframe Plan

用途：規劃 Town Hub 後續 UI-2 / Rich wireframe 或 visual mockup 補強時要驗證的 layout、資訊層與狀態案例。此文件只做規劃，不生成新圖、不選平台、不改 runtime。

## 0. Inputs

已確認輸入：

- `01_content/gui-town-hub-screen-model-draft.md`
- `01_content/gui-town-hub-review-checklist.md`
- `01_content/gui-town-hub-mockup-review-v1.md`
- `01_content/gui-screen-map.md`
- `05_assets/gui_references/town_hub/town_hub_visual_reference_v1_user_mockup.png`

目前 mockup review 結論：

```text
result: pass_with_notes
```

可保留：

- 場景式 Town Hub identity。
- facility 建築入口。
- 上方 title / subtitle。
- 左下返回世界地圖入口。

需補強：

- `resource_strip`
- `town_guidance`
- 少量 high-value `facility_badges`
- `magic_shop`、`temple`、`storage` 的入口策略

## 1. Boundary

- 不修改 runtime、data、schema、save 或 combat formula。
- 不重構 `03_engine/engine/game.py`。
- 不選定 pygame / HTML / Unity / WebView。
- 不生成新圖。
- 不啟動正式 asset pipeline。
- 不把 Town Hub 擴成自由行走城鎮。
- 不把 facility 內部流程塞進 Town Hub。
- 不建立完整通知系統。
- 不把 mockup 圖內文字當成資料來源。

## 2. Wireframe Goal

UI-2 wireframe 只驗證 Town Hub 的畫面結構與資訊層：

- 玩家一眼知道目前在艾爾姆城鎮。
- 玩家看得到目前狀態與下一步方向。
- 玩家能選擇 facility node。
- 少量 badge 能提示真正該處理的事情。
- 返回 World Map 清楚。
- 未呈現在第一張 mockup 中的 runtime facility 入口有安排策略。

不驗證：

- 正式背景圖品質。
- 正式 icon set。
- 動畫、hover 特效或聲音。
- 各 facility 內部 list-detail-confirm 流程。
- runtime builder 或 render adapter。

## 3. Layout Zones

建議 UI-2 wireframe 分成五個 zone。

```text
┌────────────────────────────────────────────────────────────┐
│ Header: title / subtitle                      resource_strip │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Scene / facility_nodes                                     │
│                                                            │
│   [Inn]        [Guild]        [Workshop]                   │
│                                                            │
│   [Shop]       [Relic]        [Synthesis]                  │
│                                                            │
│        [Magic Shop / Temple / Storage strategy]            │
│                                                            │
├────────────────────────────────────────────────────────────┤
│ open_world_map       town_guidance          global_actions │
└────────────────────────────────────────────────────────────┘
```

### Header

用途：

- 顯示 `title` / `subtitle`。
- 容納輕量 `resource_strip`。

建議：

- title/subtitle 保留在上方中央。
- `resource_strip` 可放上方右側或 header 下方細列。
- 不放完整角色狀態頁。

### Scene / Facility Nodes

用途：

- 保留城鎮場景與建築入口。
- 以 `facility_nodes` 承接互動。

建議：

- facility node 使用 icon + label + short description。
- selected / hover / focus 狀態要清楚。
- `disabled_reason` 應可透過 node 狀態或 guidance 顯示。
- node label 由 render layer 動態輸出。

### Town Guidance

用途：

- 顯示 1-2 行下一步提示。

建議：

- 放在底部中央或下方資訊條。
- 優先顯示 `next_step_hint(state)`。
- 補充提示來自 `town_hint_lines(state)`。
- 不變成完整 quest tracker。

### World Map Entry

用途：

- 清楚提供 `open_world_map`。

建議：

- 保留左下角。
- 與 facility node 視覺層級不同，避免誤認為一般設施。

### Global Actions

用途：

- 現階段主 hub 相容入口：`open_character`、`open_inventory`。

建議：

- 可放右下角或 resource strip 附近。
- 明確註記：最終是否屬於全域導航，待 navigation model 再定。
- 不應搶過 facility node 與 World Map entry。

## 4. Facility Node Strategy

| Node | Wireframe strategy | Notes |
|---|---|---|
| `guild` | 中央或最高優先建築入口 | 可承接 `可回報`、`火印線索` badge。 |
| `inn` | 左側或補給區入口 | 預設不加 badge；低 HP/MP 放 town guidance。 |
| `travel_shop` | 市集 / 商店入口 | 缺藥水優先放 town guidance，不急著加 badge。 |
| `workshop` visual group | 單一工坊建築或相鄰雙入口 | model 仍保留 `iron_workshop` / `armor_workshop`。 |
| `synthesis` | 米菈合成屋入口 | 可顯示 `未解鎖` status badge。 |
| `magic_shop` | 星燈 / 魔法塔 / 小型招牌入口 | 第一張 mockup 未明確呈現，wireframe 需補位置。 |
| `temple` | 神殿 / 教會 / spire 類入口 | 可承接火印橋接或查閱提示。 |
| `relic_preview` | 聖物調查入口 | 可保留現 mockup 的聖物調查所語意。 |
| `storage` | 工會旁倉庫 / 小木屋 / 次級入口 | 可顯示 `未開啟` status badge。 |
| `world_map` | 左下 navigation | navigation，不是 facility node。 |

工坊策略：

- 視覺上可維持一棟工坊建築。
- UI-2 wireframe 需測試兩種呈現：
  - 一個 `workshop` node，選取後顯示 `鐵刃工坊 / 堅甲工坊` 二級選擇。
  - 同一建築上放兩個相鄰 node label。
- 不應因視覺合併而改 runtime facility。

## 5. Badge Strategy

badge 只放在 facility node 上，不放滿整張城鎮。

優先級：

1. `guild` / `火印線索`
2. `guild` / `可回報`
3. `synthesis` / `未解鎖`
4. `temple` / `可查閱`
5. `storage` / `未開啟`

顯示規則：

- 每個 node 預設最多 1 個 badge。
- 若同 node 有多個 badge，選 priority 較高者顯示，其他可在 selected detail 或 town guidance 中補充。
- badge 分為 `notification` 與 `status`。
- badge 需搭配文字，不只靠顏色或 icon。

不做：

- 不顯示完整通知列表。
- 不記錄已讀。
- 不顯示每個商品 / 配方 / 魔法書的可處理狀態。
- 不用 badge 取代 facility 內部 screen。

## 6. State Scenarios To Test

UI-2 wireframe 至少應測以下狀態。

### Scenario A: Default Town

目的：確認畫面在沒有 urgent badge 時仍可讀。

應看到：

- title / subtitle。
- resource strip。
- facility nodes。
- `open_world_map`。
- town guidance 顯示一般整備提示。

### Scenario B: Guild Ready To Submit

來源：

- `ready_quest_titles(state)` 非空。

應看到：

- `guild` node 顯示 `可回報`。
- town guidance 可顯示工會有可交付委託。

### Scenario C: Fire Mark Guild Inquiry

來源：

- `can_ask_fire_mark_guild_inquiry(state)` 為 true。

應看到：

- `guild` node 顯示 `火印線索`。
- town guidance 提示回冒險者工會詢問諾亞。
- 不進入 Guild Screen story hint card 細節。

### Scenario D: Synthesis Locked

來源：

- `is_unlocked(state, "shop_synthesis_01")` 為 false。

應看到：

- `synthesis` node 可顯示 `未解鎖`。
- selected detail 或 disabled reason 說明需先完成工會任務。

### Scenario E: Low HP / No Potion

來源：

- HP/MP 未滿。
- 背包沒有小藥水或中藥水。

應看到：

- town guidance 提醒旅館或旅人小鋪。
- 不一定在 inn / shop node 上加 badge。

### Scenario F: Missing Facility Entrances

目的：確認 mockup 未明確呈現的 `magic_shop`、`temple`、`storage` 在 wireframe 中有入口策略。

應看到：

- 入口位置或次級入口規則。
- 不刪除 runtime facility。

## 7. Dynamic Text Rules

UI-2 wireframe 必須保留可動態輸出的文字位置。

不可烘進圖片或固定背景的內容：

- title / subtitle。
- facility label / description。
- badge label。
- resource values。
- town guidance。
- disabled reason。
- action labels。

可以作為視覺 placeholder：

- 建築符號。
- icon role。
- 無語意依賴的招牌形狀。
- 背景道路、旗幟、燈光、材質。

## 8. Acceptance Criteria

Wireframe 可進入下一步時，應滿足：

- 場景式 hub 仍清楚。
- `resource_strip` 有位置且不壓迫場景。
- `town_guidance` 可讀且不變成 quest tracker。
- facility nodes 可辨識、可 focus、可 disabled。
- badge 數量受控。
- `magic_shop`、`temple`、`storage` 有入口策略。
- `open_world_map` 清楚。
- `open_character` / `open_inventory` 只作為現階段主 hub 相容入口。
- 沒有要求 runtime / data / schema / save 改動。

## 9. Recommended Next Step

下一步建議二選一：

1. 先做 markdown-only UI-2 wireframe 草圖，使用文字框線描述 zones 與 state variants。
2. 若要補 visual mockup prompt，先只寫 prompt draft，不生成新圖，並明確要求 dynamic text safe areas。

建議優先選 1，因為它能先驗證資訊層，不會過早進入圖像生成與 asset 管理。

