# HTML Town Hub Prototype Plan

用途：規劃第一個 HTML Programmatic GUI prototype，先以 static `TownHubScreenModel` fixture 驗證 Town Hub layout、dynamic text、focus / hover / disabled / badge 與 UIAction contract。此文件只做 implementation planning，不代表已開始寫 GUI，也不接 runtime。

## 0. Status

```text
prototype_scope: town_hub_html_static_fixture
plan_date: 2026-05-19
status: prototype_plan_only
implementation_status: not_started
runtime_adapter_status: not_started
asset_pipeline_status: not_started
```

參考：

- `01_content/gui-implementation-platform-tradeoff.md`
- `01_content/gui-town-hub-programmatic-layout-plan-v1.md`
- `01_content/gui-town-hub-facility-node-mapping-v1.md`
- `01_content/gui-town-hub-screen-model-draft.md`
- `01_content/gui-screen-map.md`
- `01_content/ui-flow-blueprint.md`

## 1. Boundary

- 不修改 runtime、data、schema、save 或 combat formula。
- 不讀取或改動 `03_engine/engine/game.py`。
- 不建立正式 server API。
- 不讓 JS 複製 Python gameplay logic。
- 不讀寫 `save.json`。
- 不把 candidate mockup 當 runtime background。
- 不啟動正式 asset pipeline。
- 不做 Facility 內部流程。
- 不把 HTML prototype 視為最終平台定案。

## 2. Prototype Goal

第一個 HTML prototype 只驗證 Programmatic GUI 是否成立。

必須驗證：

- `TownHubScreenModel` 可以驅動畫面。
- `facility_nodes` 可以以建築 / hotspot 卡片方式操作。
- 所有文字由 render layer 動態輸出。
- focus / hover / selected state 可用。
- disabled state 與 disabled reason 可讀。
- badge 可以少量、高價值、由 model 控制。
- `open_facility` / `open_world_map` / global actions 能 dispatch 成 UIAction log。

不驗證：

- 真實 runtime state。
- 真實 save / load。
- 真實商店、工坊、合成、工會流程。
- 正式背景圖、正式 icon set、動畫或 sound。

## 3. Suggested Prototype Location

建議未來若實作，可先放在獨立 prototype 目錄，避免混入 runtime：

```text
07_gui_prototype/
- town_hub/
  - index.html
  - styles.css
  - town-hub.js
  - fixtures/
    - town-hub-default.json
    - town-hub-alerts.json
```

此路徑只是提案。正式建立前可再確認 repo 結構命名。

## 4. Static Fixture Shape

第一版 fixture 應是 JSON-like `TownHubScreenModel`，不從 Python runtime 讀取。

```json
{
  "screen_id": "town_hub",
  "title": "艾爾姆城鎮",
  "subtitle": "冒險者的據點與補給中心",
  "resource_strip": [
    { "id": "hero", "label": "莉亞 / 盜賊 Lv8" },
    { "id": "hp", "label": "HP 86/86" },
    { "id": "mp", "label": "MP 34/40" },
    { "id": "gold", "label": "420G" },
    { "id": "guild_points", "label": "工會積分 12" }
  ],
  "town_guidance": [
    "把探索收益轉成任務、裝備、技能或補給後再出發。"
  ],
  "selected_facility_id": "guild",
  "facility_nodes": [],
  "global_actions": []
}
```

注意：

- 文字可以在 fixture 中作為測試資料，但未來 runtime 版本必須由 Python ScreenModel 產生。
- HTML render layer 不可硬寫任何 gameplay text。
- fixture 只測 display，不作資料 SSOT。

## 5. Facility Node Fixture

單一 node 建議形狀：

```json
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
  "payload": {
    "facility_id": "guild"
  }
}
```

V1 fixture nodes：

- `guild`
- `inn`
- `travel_shop`
- `workshop`
- `synthesis`
- `magic_shop`
- `temple`
- `relic_preview`
- `storage`

`world_map` 不放在 `facility_nodes`，而是 navigation action。

## 6. Layout Zones

HTML prototype 應直接對應 programmatic layout zones：

```text
page.town-hub
- header.title-area
- header.resource-strip
- main.scene-facility-node-area
- footer.world-map-nav-area
- footer.town-guidance-area
- footer.global-actions-area
```

CSS 初版可採固定 16:9 desktop layout，先不做 mobile。

建議：

- `scene-facility-node-area` 用 CSS grid / absolute anchors 二選一。
- 初版若要貼近 mockup，可用 CSS grid areas 命名 anchor。
- 不使用 candidate image 當背景。
- 可用 gradient / simple panel / placeholder shape 表達城鎮區域。

## 7. Interaction Scope

第一版互動只需要：

- Mouse hover node。
- Click node -> set selected node -> log `open_facility` candidate action 或顯示 selected detail。
- Keyboard arrow / Tab focus。
- Enter / Space dispatch selected action。
- Disabled node 可 focus，但 Enter 顯示 disabled reason，不 dispatch facility action。
- World map button dispatch `open_world_map` log。
- Character / Inventory dispatch global action log。

Action log 範例：

```json
{
  "action_id": "open_facility",
  "payload": {
    "facility_id": "guild"
  }
}
```

此 log 只顯示在 prototype debug panel，不連接 runtime。

## 8. State Variants

建議至少準備兩個 fixture：

### Default Town

用途：

- 確認沒有 urgent badge 時，layout 仍可讀。
- 確認所有 facility nodes 都可掃讀。

狀態：

- `guild` 無 badge 或只顯示 `可回報`。
- `synthesis` enabled。
- `storage` enabled 或 status normal。
- town guidance 是一般整備提示。

### Alert / Locked Town

用途：

- 確認 badge、disabled、guidance 是否清楚。

狀態：

- `guild` 顯示 `火印線索`。
- `synthesis` disabled，顯示 `未解鎖`。
- `storage` disabled 或顯示 `未開啟`。
- town guidance 顯示火印或補給提醒。

## 9. Rendering Rules

HTML render layer 必須遵守：

- 所有文字都從 fixture / model 讀取。
- facility label 不硬寫在 HTML template。
- badge label 不硬寫在 CSS。
- disabled reason 由 node 提供。
- focus state 由 DOM state / CSS class 控制。
- icon 可先用 emoji-free simple symbol、CSS shape、文字代碼或 data attribute，但不能成為唯一資訊來源。

避免：

- 把 mockup 圖切成背景。
- 把 generated candidate 的 icon 直接裁成 runtime icons。
- 用 JS 寫死 `guild` 的特殊邏輯。
- 在 prototype 中加入購買、合成、任務交付等 facility 內部 action。

## 10. Visual Style For Prototype

初版 prototype 應是 usable wireframe，不是 final art。

可用：

- 暖木、石路、黃銅、羊皮紙色塊。
- 深色半透明面板。
- CSS border / shadow / outline 表達 focus。
- simple icon role text，例如 `guild`, `inn`, `shop`，或抽象符號。

暫不用：

- 正式背景圖。
- 正式 icon set。
- 動畫特效。
- NPC portrait。
- generated candidate as background。

## 11. Acceptance Criteria

HTML prototype 計畫完成後，未來實作應符合：

- 不接 runtime 也能載入 static fixture。
- 能切換至少兩個 Town Hub fixture。
- 能 render title / subtitle / resource strip / town guidance。
- 能 render 9 個 facility nodes。
- 能顯示 selected / hover / keyboard focus。
- 能顯示 badge，且每 node 最多一個主要 badge。
- 能顯示 disabled reason。
- 能 dispatch UIAction log。
- 不含 gameplay calculation。
- 不讀寫 save。
- 不需要正式 assets。

## 12. Future Runtime Adapter Boundary

等 static prototype 穩定後，才評估 runtime adapter。

未來 adapter 應做：

- Python runtime state -> `TownHubScreenModel`
- `UIAction` -> Python command / screen transition

adapter 不應做：

- 改 gameplay 規則。
- 在 JS 重算商店、合成、工坊、任務條件。
- 直接讀寫 save。
- 把 UI state 寫入 gameplay state。

## 13. Recommended Next Step

建議下一步是二選一：

1. 若仍要文件化：先寫 HTML prototype fixture spec，列出完整 `town-hub-default.json` 與 `town-hub-alerts.json`。
2. 若要開始實作：建立 `07_gui_prototype/town_hub/`，放入 `index.html`、`styles.css`、`town-hub.js` 與 static fixture，但仍不接 runtime。

