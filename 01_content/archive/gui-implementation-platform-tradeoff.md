# GUI Implementation Platform Tradeoff

用途：評估第一個可操作 Programmatic GUI prototype 應優先使用 pygame 或 HTML。此文件只做 markdown-only decision note，不代表已開始 GUI 實作，也不啟動正式 asset pipeline。

## 0. Status

```text
decision_scope: first_programmatic_gui_prototype
decision_date: 2026-05-19
status: tradeoff_note_only
implementation_status: not_started
asset_pipeline_status: not_started
```

參考：

- `01_content/gui-ui-direction-brief.md`
- `01_content/gui-screen-map.md`
- `01_content/ui-flow-blueprint.md`
- `01_content/gui-town-hub-programmatic-layout-plan-v1.md`

## 1. Boundary

- 不修改 runtime、data、schema、save 或 combat formula。
- 不讀取或改動 `03_engine/engine/game.py`。
- 不啟動正式 asset pipeline。
- 不把 mockup candidate 當 runtime asset。
- 不選 Unity 作為第一個 prototype。
- 不追求 UI-3 最終視覺。
- 不把平台選型和正式 implementation 混在同一步。

## 2. Decision Goal

目前要決定的不是最終 GUI 技術，而是第一個能驗證 Programmatic GUI 的 prototype path。

第一個 prototype 應優先驗證：

- ScreenModel / UIAction 是否能承接 CLI flow。
- Town Hub 是否能用 `facility_nodes` 可操作。
- dynamic text 是否能穩定由 render layer 輸出。
- focus / hover / disabled / badge 是否能由程式狀態控制。
- 不依賴正式 asset pipeline 也能測操作感。

## 3. Option A: pygame

### 優點

- 與目前 Python 專案語言一致。
- 初期可直接在本機執行，不需要 web server。
- 適合做 game-like input：keyboard、controller、mouse focus。
- 可用程式畫 panel、button、badge、focus outline。
- 對未來單機桌面遊戲包裝較直覺。
- 較容易保持「runtime 仍在 Python」的心智模型。

### 代價

- 文字排版、中文字型、換行、tooltip、scroll list 都要自己處理更多。
- UI layout 若手寫，容易變成低階座標管理。
- Rich text、responsive layout、debug inspector 不如 browser 方便。
- 若之後要做大量 UI 狀態與表單，開發速度可能較慢。
- 美術與 layout hot reload 需要額外工具或自訂工作流。

### 適合驗證

- Town Hub focus order。
- keyboard / controller 操作感。
- game-loop style render layer。
- placeholder panel / icon / badge rendering。

### 風險

- 過早陷入字型、座標與自製 UI toolkit。
- 若沒有先定 ScreenModel，容易把 runtime state 和 render code 混在一起。

## 4. Option B: HTML

### 優點

- 文字排版、中文換行、scroll、tooltip、responsive layout 較成熟。
- CSS 很適合快速驗證 resource strip、cards、badges、focus state。
- DOM 結構天然適合 ScreenModel → render layer。
- browser devtools 方便檢查 layout 與互動狀態。
- 容易做 mockup-like programmatic GUI，而不需要正式圖片。
- 若未來要做 WebView 或網頁版，轉換成本低。

### 代價

- 需要決定 Python runtime 與 HTML UI 的溝通方式。
- 若用 local web server，會多一層 dev server / API / bridge 複雜度。
- 若為了快而把 gameplay 邏輯搬進 JS，會造成 SSOT drift。
- 打包成桌面遊戲時，可能要再評估 Electron / WebView / local bridge。
- 較不像傳統 Python game loop，輸入與狀態流需要明確切邊界。

### 適合驗證

- ScreenModel driven layout。
- dynamic text safety。
- Town Hub programmatic layout zones。
- Facility list-detail-confirm UI。
- badge、disabled reason、guidance、scroll list。

### 風險

- 過早建立 API / server / bridge。
- 讓 UI prototype 誘導 gameplay logic 分裂到前端。

## 5. Unity 暫不建議

Unity 現階段不適合作為第一個 prototype path。

原因：

- 專案目前是 Python CLI RPG，Unity 會讓語言、runtime、data flow 全部重切。
- 還沒建立 ScreenModel / UIAction adapter，不適合直接跳到大型 engine。
- 對目前的 Programmatic GUI 驗證而言成本太高。
- 容易過早變成 Asset-driven / scene-driven，而不是先驗證 UI model。

Unity 可留待更後期，等遊戲要轉成完整 commercial client 或需要大量動畫 / 場景系統時再評估。

## 6. Criteria Comparison

| Criteria | pygame | HTML |
|---|---|---|
| Python runtime 接合 | 高 | 中 |
| 快速排版與中文文字 | 中 | 高 |
| focus / keyboard / controller | 高 | 中 |
| mouse / hover / tooltip | 中 | 高 |
| list-detail-confirm layout | 中 | 高 |
| game-like render loop | 高 | 中 |
| debug layout | 中 | 高 |
| 避免 gameplay drift | 高，只要留在 Python | 中，需要防止 JS 複製邏輯 |
| asset pipeline 延後 | 高 | 高 |
| 第一個 Town Hub prototype | 高 | 高 |
| 第一個 Facility prototype | 中 | 高 |

## 7. Recommended First Path

建議第一個可操作 prototype 優先採：

```text
HTML programmatic GUI prototype
```

理由：

- 目前最需要驗證的是 ScreenModel / dynamic text / layout / badges / disabled reasons，而 HTML 的排版與文字處理成本最低。
- Town Hub 與 Facility Screen 都有大量中文動態文字與區塊 layout，HTML 能更快暴露可讀性問題。
- 可先用 static JSON-like ScreenModel fixture 驗證 render layer，不必立即接 runtime。
- 能維持 Programmatic GUI → Asset-driven 原則：先用 CSS / DOM / placeholder icons 畫可操作 UI，再決定正式 asset。

但這不是最終平台定案。若後續更重視 controller / single executable / Python-only loop，可再把已穩定的 ScreenModel 移植到 pygame render layer。

## 8. Safe Prototype Shape

若走 HTML，第一步應是 prototype，不是正式 app。

建議形狀：

```text
prototype/
- static TownHubScreenModel fixture
- render Town Hub layout zones
- render facility nodes
- support focus / hover / selected state
- dispatch UIAction as logged events
- no runtime mutation
- no save
- no gameplay logic in JS
```

可驗證：

- title / subtitle。
- resource strip。
- facility node label / description。
- disabled status。
- one badge per node。
- selected node guidance。
- open_world_map / open_facility action payload。

不可做：

- 不直接讀寫 save。
- 不複製 Python gameplay logic。
- 不建立正式 server API。
- 不把 generated mockup 當背景進 runtime。
- 不接正式 asset pipeline。

## 9. If Choosing pygame Instead

若使用者更偏好 Python-only 或 game loop prototype，pygame 也合理，但應先控制 scope：

```text
pygame prototype:
- fixed 16:9 window
- draw panels / buttons / node boxes programmatically
- load no formal background asset
- use placeholder icons or simple symbols
- render Chinese text from model
- keyboard + mouse focus
- dispatch UIAction as logged events
```

pygame path 的第一個風險是 UI toolkit 成本，因此不應一開始就做 animation、pixel-perfect mockup 或完整 facility screen。

## 10. Guardrails

無論選 HTML 或 pygame，都必須維持：

- Runtime remains source of gameplay truth.
- ScreenModel is the bridge.
- UIAction is the interaction contract.
- Render layer owns layout and visual states.
- Dynamic text is rendered by UI, never baked into assets.
- Assets remain optional until programmatic prototype feels right.

避免：

- 一邊選平台一邊改 runtime。
- 讓 mockup 圖決定 gameplay。
- 讓 HTML / JS 複製 Python 規則。
- 讓 pygame render code 直接抓一堆 runtime internals。
- 在第一個 prototype 就做正式 asset pipeline。

## 11. Recommended Next Step

建議下一步：

1. 先確認是否接受 `HTML programmatic GUI prototype` 作為第一個 prototype path。
2. 若接受，下一份文件應寫 `gui-html-town-hub-prototype-plan.md`。
3. 該 plan 仍先使用 static `TownHubScreenModel` fixture，不接 runtime。
4. 等 HTML prototype 的 layout 與 action contract 穩定後，再評估 runtime adapter。

