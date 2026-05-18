# Codex Session 接續快照

用途：提供新 session 在需要歷史脈絡時的精簡接續快照。本檔不再承擔完整流水帳；日常接續請先讀 `01_content/codex-handoff-short.md`、`README.md` 與 `01_content/gui-planning-index.md`。

狀態日期：2026-05-18

## 1. 最短閱讀順序

一般接續：

1. `01_content/codex-handoff-short.md`
2. `README.md`
3. `01_content/gui-planning-index.md`
4. 依任務加讀對應文件

GUI planning 接續：

1. `01_content/gui-planning-index.md`
2. `01_content/gui-ui-direction-brief.md`
3. `01_content/gui-screen-map.md`
4. `01_content/ui-flow-blueprint.md`

Guild Screen 接續：

1. `01_content/gui-guild-screen-visual-baseline.md`
2. `01_content/gui-guild-screen-model-draft.md`
3. `01_content/gui-guild-screen-review-checklist.md`
4. `01_content/gui-facility-screen-template.md`
5. `01_content/gui-asset-registry-draft.md`

Facility / Synthesis 接續：

1. `01_content/gui-facility-screen-template.md`
2. `01_content/gui-asset-request-schema.md`
3. `01_content/gui-asset-registry-draft.md`

## 2. 目前專案穩定狀態

- 專案是 Python CLI 文字冒險 RPG《元素迷宮：邊境冒險者》。
- v1 第一幕可通關；第二幕火系 demo 已進 runtime。
- Act 2 火系 demo 已包含灰燼裂谷、灰燼守衛、補給線升級、燼印深窟、燼印鎮衛 Boss MVP、第 3 枚火之印記碎片來源、三碎片後工會詢問、神殿接橋與教會查閱結果。
- 三枚碎片目前被確認為「未完成的火之印記核心」。
- 火之印記目前不是正式聖物，不提供裝備、啟用、升級、戰鬥效果或正式聖物效果。
- 正式轉職、正式聖物、正式職業特化、八元素 runtime、完整屬性克制、通用 Boss framework、Act 3 runtime 內容都尚未開放。
- `06_tools/content_inventory_report.py` 是 read-only 內容盤點工具，不是 SSOT，也不是 validation 替代品。
- 目前沒有已批准的下一個 runtime 施工目標。

## 3. CLI UI 已落地狀態

目前 CLI UI 仍只是顯示層薄包裝，不是正式 GUI framework。

已完成的 CLI / Rich display layer 範圍：

- Start Screen MVP。
- 核心循環 Rich `Panel` thin layer。
- Travel Shop Catalog MVP。
- Workshop Catalog MVP。
- Magic Shop Catalog MVP。
- Synthesis Catalog MVP。
- Combat UI Log Separation MVP。
- 城鎮設施開始整理成專屬 facility panel。

這些成果可作為 GUI playable reference，但不等於最終 GUI 架構。後續 GUI 應抽象為 ScreenModel / UIAction，再接不同 render layer。

## 4. GUI planning 目前結論

GUI 仍處於 planning / reference / mockup 階段。

- 尚未實作 GUI。
- 尚未選定 pygame / HTML / Unity / WebView 或其他 GUI 技術。
- 尚未啟動正式 asset pipeline。
- 尚未建立正式 prompt builder、style bible 或 production asset registry。
- 目前不應把 CLI `input()` / `print()` menu 視為最終架構。
- 三階段策略仍是 UI-1 文字式 UI、UI-2 CLI / Rich wireframe、UI-3 最終 GUI 視覺版。
- 三階段應共用 Screen Map、ScreenModel 與 UIAction；差異只在 render layer。

GUI 文件入口：

- `01_content/gui-planning-index.md`：唯一 GUI 文件入口與閱讀順序。
- `01_content/gui-ui-direction-brief.md`：整體 GUI 方向與視覺語彙。
- `01_content/gui-screen-map.md`：Screen Map、UIAction、ScreenModel 草案。
- `01_content/ui-flow-blueprint.md`：目前 CLI thin layer 與 GUI flow 的銜接。
- `01_content/gui-guild-screen-model-draft.md`：Guild Screen 的 ScreenModel、row model 與 UIAction 草案。
- `01_content/gui-guild-screen-review-checklist.md`：Guild Screen baseline、mockup、wireframe 或 implementation 的審查清單。

## 5. 已採納 / 未採納 visual direction

### Guild Screen

Guild Screen 已採用使用者提供圖作為 visual baseline。

```text
05_assets/gui_references/guild_screen/guild_screen_visual_baseline_v1_user_reference.png
```

對應文件：

- `01_content/gui-guild-screen-visual-baseline.md`
- `01_content/gui-guild-screen-model-draft.md`
- `01_content/gui-guild-screen-review-checklist.md`
- `01_content/gui-asset-registry-draft.md`

定位：

- Adventurers' Guild / Quest Board。
- 左側任務列表。
- 中央任務詳情。
- 報酬摘要。
- 任務達成 / 回報條件檢查表。
- 底部 NPC guidance / feedback bar。
- 右下單一主要 action。

此圖是 visual baseline / reference，不是 runtime asset，也不代表正式 asset pipeline 已開始。

### Facility / Synthesis

Facility / Synthesis 目前有 v0 / v2 candidate，但不視為正式 baseline。

候選圖位置：

```text
05_assets/gui_references/facility_synthesis_screen/
```

狀態：

- v0 可作為溫暖工坊、羊皮紙、木框、黃銅、柔和燈光、NPC 存在感的方向參考。
- v2 保留為探索歷史與比較參考。
- 後續 Facility direction 應回到 `01_content/gui-facility-screen-template.md` 與中文動態文字安全區規則。

## 6. Asset / reference 邊界

- reference image 不等於 runtime asset。
- `.codex/generated_images` 只是生成暫存，不是專案內正式資料來源。
- `05_assets/gui_references` 是專案內 reference / candidate 暫存區，不是正式 runtime asset path。
- 不要把候選圖直接引用進 `03_engine` 或 runtime。
- 所有物品、任務、價格、數值、狀態、action label、Battle Log、NPC 提示與任何可能由 data / save / localization 改變的文字，都必須由 render layer 動態輸出，不可畫死在圖片裡。
- 若未來要正式使用任何圖片，需另行決定正式 asset path、命名規則、授權 / 來源紀錄與替換策略。

## 7. 明確禁止事項

除非使用者另開明確小切片並批准，否則不要做：

- 不修改 runtime、data、schema、save、combat formula。
- 不重構 `03_engine/engine/game.py`。
- 不實作 GUI。
- 不啟動 dev server。
- 不生成新圖片。
- 不移動圖片。
- 不選定 pygame / HTML / Unity / WebView。
- 不建立正式 asset pipeline。
- 不把 Synthesis v0 / v2 candidate 當正式 baseline。
- 不把 Guild baseline 當 runtime asset。
- 不把 mockup 或 reference image 反推 gameplay。
- 不新增 Act 3 文件或 runtime 內容。
- 不做完整火之印記、火印熔爐、正式聖物、正式轉職、八元素或通用 Boss framework。

## 8. 下一步建議

目前最適合的下一步仍是 markdown-only 小切片：

- Guild Screen：read-only 對照目前 `guild_menu()` 與任務資料來源，列出未來 `build_guild_screen_model(...)` 可能需要的資料。
- Facility Template：補強 `FacilityScreenModel` 與 Shop / Forge / Magic / Synthesis 的欄位差異。
- Mockup 評估：建立單一 screen 的 review checklist，不生成新圖。

若下一步要碰 runtime，必須先做 read-only 評估，明確列出會碰到的檔案、風險、驗證方式與不碰範圍，再等使用者批准。

## 9. Snapshot 精簡紀錄

本檔已於 2026-05-18 精簡為接續快照，移除舊 session 的長流水帳、已完成過程細節、過期 UI 狀態與重複驗證紀錄。

需要完整歷史時，優先查：

- `README.md`
- `01_content/codex-handoff-short.md`
- 對應專門文件，例如 `01_content/act-2-content-plan.md`、`01_content/game-design.md`、`01_content/gui-asset-registry-draft.md`
- git history
