# GUI Planning Index

用途：作為 GUI 規劃文件的唯一入口、閱讀順序與治理索引，避免 `01_content/` 隨著 reference、mockup、prompt 與候選文件增加後失去脈絡。

## 0. 預設閱讀順序

新 session 若只是接續 GUI planning，不需要掃過全部 GUI 文件。預設只讀：

1. `01_content/codex-handoff-short.md`
2. `README.md`
3. `01_content/gui-planning-index.md`
4. `01_content/gui-ui-direction-brief.md`

接著依任務加讀：

| 任務 | 加讀文件 |
|---|---|
| Screen flow / UIAction / ScreenModel | `01_content/gui-screen-map.md`、`01_content/ui-flow-blueprint.md` |
| Town Hub Screen model | `01_content/gui-town-hub-screen-model-draft.md`、`01_content/gui-screen-map.md`、`01_content/ui-flow-blueprint.md`、`01_content/gui-ui-direction-brief.md` |
| Town Hub Screen review | `01_content/gui-town-hub-review-checklist.md`、`01_content/gui-town-hub-screen-model-draft.md`、`01_content/gui-ui-direction-brief.md` |
| Town Hub mockup review record | `01_content/gui-town-hub-mockup-review-v1.md`、`01_content/gui-town-hub-review-checklist.md`、`01_content/gui-town-hub-screen-model-draft.md` |
| Town Hub UI-2 wireframe planning | `01_content/gui-town-hub-wireframe-plan.md`、`01_content/gui-town-hub-screen-model-draft.md`、`01_content/gui-town-hub-mockup-review-v1.md` |
| Town Hub UI-2 wireframe draft | `01_content/gui-town-hub-ui2-wireframe-draft.md`、`01_content/gui-town-hub-wireframe-plan.md`、`01_content/gui-town-hub-review-checklist.md` |
| Town Hub UI-2 wireframe review | `01_content/gui-town-hub-ui2-wireframe-review-v1.md`、`01_content/gui-town-hub-ui2-wireframe-draft.md`、`01_content/gui-town-hub-review-checklist.md` |
| Facility template | `01_content/gui-facility-screen-template.md` |
| Guild Screen model | `01_content/gui-guild-screen-model-draft.md`、`01_content/gui-guild-screen-visual-baseline.md`、`01_content/gui-facility-screen-template.md`、`01_content/gui-asset-registry-draft.md` |
| Guild Screen review | `01_content/gui-guild-screen-review-checklist.md`、`01_content/gui-guild-screen-model-draft.md`、`01_content/gui-guild-screen-visual-baseline.md` |
| Mockup / reference 評估 | `01_content/gui-asset-request-schema.md`、`01_content/gui-asset-registry-draft.md`、對應 screen baseline / template |
| 歷史追溯 | `01_content/codex-session-snapshot.md`，只在真的需要歷史決策時讀 |

不要預設閱讀：

- `01_content/gui-facility-synthesis-mockup-request.md`
- `01_content/gui-facility-synthesis-prompt-draft.md`
- `01_content/gui-facility-synthesis-v2-prompt-draft.md`
- 完整 `01_content/codex-session-snapshot.md`

以上文件是歷史、候選或條件式文件，不是主要入口。

## 1. 目前 GUI 狀態

GUI 仍處於 planning / reference / mockup 階段。

- 尚未實作 GUI。
- 尚未選定 pygame / HTML / Unity / WebView 或其他 GUI 技術。
- 尚未啟動正式 asset pipeline。
- 目前 CLI / Rich panel 只作為 playable reference，不等於最終 GUI 架構。
- GUI 規劃應先整理 Screen Map、ScreenModel 與 UIAction，再考慮 render layer。
- reference image、candidate mockup 與 prompt draft 都不等於 runtime asset。
- runtime、data、schema、save、combat formula 都不可因 GUI 規劃而修改。
- 不重構 `03_engine/engine/game.py`，除非未來另開明確小切片並先 read-only 評估。

## 2. 文件生命週期

| 文件 | 狀態 | 角色 | 預設讀取 |
|---|---|---|---|
| `01_content/gui-planning-index.md` | core | GUI 文件入口、閱讀順序、治理規則 | 是 |
| `01_content/gui-ui-direction-brief.md` | core | GUI 整體方向、視覺語彙、禁止方向 | 是 |
| `01_content/gui-screen-map.md` | core | Screen Map、UIAction、ScreenModel 草案 | 視任務 |
| `01_content/ui-flow-blueprint.md` | core | CLI thin layer 到 GUI flow 的承接說明 | 視任務 |
| `01_content/gui-town-hub-screen-model-draft.md` | core | Town Hub 的場景式 facility node、badge 與 UIAction 草案 | Town Hub 任務必讀 |
| `01_content/gui-town-hub-review-checklist.md` | conditional | Town Hub reference、mockup、wireframe 或 implementation 的審查清單 | Town Hub review 任務必讀 |
| `01_content/gui-town-hub-mockup-review-v1.md` | conditional | Town Hub V1 user mockup 的正式 review 記錄 | Town Hub mockup review 時讀 |
| `01_content/gui-town-hub-wireframe-plan.md` | conditional | Town Hub UI-2 / Rich wireframe 與視覺補強規劃 | Town Hub wireframe 任務必讀 |
| `01_content/gui-town-hub-ui2-wireframe-draft.md` | conditional | Town Hub UI-2 markdown wireframe 草圖與狀態變體 | Town Hub wireframe 任務必讀 |
| `01_content/gui-town-hub-ui2-wireframe-review-v1.md` | conditional | Town Hub UI-2 markdown wireframe 的正式 review 記錄 | Town Hub wireframe review 時讀 |
| `01_content/gui-facility-screen-template.md` | core | Facility 類畫面共用模板 | 視任務 |
| `01_content/gui-guild-screen-visual-baseline.md` | core | Guild Screen 已採納 visual baseline | Guild 任務必讀 |
| `01_content/gui-guild-screen-model-draft.md` | core | Guild Screen 的 ScreenModel、row model 與 UIAction 草案 | Guild 任務必讀 |
| `01_content/gui-guild-screen-review-checklist.md` | conditional | Guild Screen baseline、mockup、wireframe 或 implementation 的審查清單 | Guild review 任務必讀 |
| `01_content/gui-asset-registry-draft.md` | core | reference / candidate / baseline 狀態登記 | mockup 或 baseline 任務必讀 |
| `01_content/gui-asset-request-schema.md` | conditional | 未來素材需求描述 schema | 只在 mockup / asset request 任務讀 |
| `01_content/gui-facility-synthesis-mockup-request.md` | historical | Synthesis v0 mockup request 過程紀錄 | 否 |
| `01_content/gui-facility-synthesis-prompt-draft.md` | historical | Synthesis v0 prompt 與 V2 notes | 否 |
| `01_content/gui-facility-synthesis-v2-prompt-draft.md` | historical | Synthesis V2 prompt 草案 | 只有明確要生成 / 評估 V2 時讀 |
| `01_content/codex-session-snapshot.md` | compact snapshot | 接續快照，不再作長歷史流水帳 | 需要歷史時讀 |

文件狀態定義：

- `core`：仍會持續被新 session 使用，應保持精簡、準確、可導覽。
- `conditional`：只在特定任務中讀取，不是新 session 入口。
- `historical`：保留過程與候選資訊，但不再作為規劃入口。
- `compact snapshot`：只保留接續需要的穩定結論，不承擔完整歷史紀錄。

## 3. 文件分層導覽

### A. 新 session 必讀入口

- `01_content/codex-handoff-short.md`：目前專案穩定狀態、禁止事項與下一步邊界。
- `README.md`：project-level SSOT，包含目前 runtime 狀態、資料夾職責、驗證方式與 roadmap。
- `01_content/gui-planning-index.md`：GUI 文件入口與治理索引。
- `01_content/gui-ui-direction-brief.md`：GUI vertical slice 的整體方向、視覺語彙、禁止方向與三階段策略。

### B. Screen map / flow

- `01_content/gui-screen-map.md`：主要 screen、flow、UIAction、ScreenModel 草案。
- `01_content/ui-flow-blueprint.md`：目前 CLI thin display layer 與未來 GUI flow 的銜接。

這一層用來回答：

- 有哪些 screen。
- screen 之間怎麼流動。
- CLI 數字輸入、Rich wireframe 與未來 GUI 點擊如何映射到同一批 UIAction。

### C. Town Hub Screen model

- `01_content/gui-town-hub-screen-model-draft.md`：Town Hub 的場景式 facility node、badge 與 UIAction 草案。
- `01_content/gui-town-hub-review-checklist.md`：Town Hub reference、mockup、wireframe 或未來 implementation 的審查清單。
- `01_content/gui-town-hub-mockup-review-v1.md`：目前 Town Hub user mockup 的正式 review 記錄，結論為 `pass_with_notes`。
- `01_content/gui-town-hub-wireframe-plan.md`：Town Hub UI-2 / Rich wireframe 與視覺補強規劃。
- `01_content/gui-town-hub-ui2-wireframe-draft.md`：Town Hub UI-2 markdown wireframe 草圖與狀態變體。
- `01_content/gui-town-hub-ui2-wireframe-review-v1.md`：Town Hub UI-2 markdown wireframe 的正式 review 記錄，結論為 `pass_with_notes`。
- `05_assets/gui_references/town_hub/town_hub_visual_reference_v1_user_mockup.png`：Town Hub visual reference / user mockup。

Town Hub 目前採用「艾爾姆城鎮場景式 hub」方向：

- facility 以建築或場景熱點呈現，不是純列表。
- `facility_nodes` 承接工會、旅館、工坊、商店、合成屋、魔法商店、轉職神殿、聖物調查與倉庫等入口。
- badge 只保留少量高價值提示，例如工會可回報、火印線索、合成屋未解鎖。
- 不處理各 facility 內部流程，不新增 runtime gameplay。

### D. Facility template

- `01_content/gui-facility-screen-template.md`：Shop、Forge、Magic Shop、Synthesis 等設施畫面共用模板。

共用核心流程：

```text
category
→ item / recipe / service list
→ selected detail
→ requirement / status
→ confirm
→ result feedback
```

這是 Facility 類 screen 的共用語法，不要求所有設施長得完全一樣。

### E. Guild Screen baseline

- `01_content/gui-guild-screen-visual-baseline.md`
- `01_content/gui-guild-screen-model-draft.md`
- `01_content/gui-guild-screen-review-checklist.md`
- `05_assets/gui_references/guild_screen/guild_screen_visual_baseline_v1_user_reference.png`

Guild Screen 目前採納方向是「冒險者工會 / 委託板」：

- 左側任務列表。
- 中央任務詳情。
- 報酬摘要。
- 任務達成 / 回報條件檢查表。
- 底部 NPC guidance / feedback bar。
- 右下單一主要 action。

`gui-guild-screen-model-draft.md` 將此 baseline 轉成 `GuildScreenModel`、`GuildTaskRow`、`GuildConditionRow`、`GuildRewardSummary` 與 Guild-specific UIAction，仍不代表 runtime 已實作。

`gui-guild-screen-review-checklist.md` 用於評估 Guild baseline、mockup、wireframe 或未來 implementation 是否符合 model、dynamic text safety、asset governance 與 gameplay safety。

### F. Asset / reference 管理

- `01_content/gui-asset-request-schema.md`：素材需求描述 schema 草案。
- `01_content/gui-asset-registry-draft.md`：reference / candidate / baseline 登記草案。
- `05_assets/gui_references/README.md`：專案內 GUI reference 暫存區的邊界與命名規則。
- `05_assets/gui_references/town_hub/`：Town Hub visual reference / user mockup 暫存區。
- `05_assets/gui_references/guild_screen/README.md`：Guild Screen reference baseline 資料夾說明。
- `05_assets/gui_references/facility_synthesis_screen/README.md`：Synthesis Screen candidate mockup 資料夾說明。

這一層只管理 reference 與候選圖，不代表正式 asset pipeline 已開始。

### G. Synthesis mockup 探索歷史

- `01_content/gui-facility-synthesis-mockup-request.md`
- `01_content/gui-facility-synthesis-prompt-draft.md`
- `01_content/gui-facility-synthesis-v2-prompt-draft.md`
- `05_assets/gui_references/facility_synthesis_screen/`

注意：Synthesis v0 / v2 目前是 visual concept / reference history，不是正式採納 baseline，也不是 runtime asset。

### H. Historical / optional 背景文件

- `01_content/codex-session-snapshot.md`：精簡後的接續快照。
- `01_content/game-design.md`：玩法與內容設計背景。
- `01_content/game-architecture.md`：專案架構背景。
- `01_content/full-act-structure.md`：長期幕次規劃。
- `01_content/act-2-content-plan.md`：第二幕規劃脈絡。
- `01_content/demo-playtest-notes.md`：UI 完成後才回頭處理的 demo 體驗 / 平衡 / 任務引導 backlog。
- `01_content/combat-growth-layering-plan.md`：戰鬥與成長層級規劃背景。

這些文件可補脈絡，但不應在 GUI planning session 中自然導向 runtime 施工。

## 4. 已採納視覺方向

### Town Hub Screen

Town Hub Screen 採用使用者提供圖作為 visual reference / user mockup，不視為最終 layout，也不是 runtime asset。

```text
05_assets/gui_references/town_hub/town_hub_visual_reference_v1_user_mockup.png
```

目前採納方向：

- Screen 定位是艾爾姆城鎮的設施入口 hub。
- 主畫面是城鎮場景，facility 以建築或場景熱點呈現。
- 上方保留城鎮 title / subtitle，左下保留返回世界地圖入口。
- 玩家資源、下一步提示與 facility badge 必須由 render layer 動態輸出。
- badge 只做少量高價值提示，不擴張成完整通知系統。

### Guild Screen

Guild Screen 採用使用者提供圖作為 visual baseline。

```text
05_assets/gui_references/guild_screen/guild_screen_visual_baseline_v1_user_reference.png
```

目前定稿方向：

- Screen 定位是 Adventurers' Guild / Quest Board。
- 保留接待員與工會互動感。
- 以任務列表、任務詳情、報酬摘要、條件檢查、底部 feedback 與單一主要 action 為核心。
- 所有文字、數值、任務名稱、條件與 action label 都必須由 render layer 動態輸出，不可畫死在圖片裡。

### Facility / Synthesis

Facility / Synthesis 目前有 v0 / v2 candidate，但不視為正式 baseline。

候選圖位置：

```text
05_assets/gui_references/facility_synthesis_screen/
```

目前定位：

- v0 可保留作為「溫暖工坊、羊皮紙、木框、黃銅、柔和燈光、NPC 存在感」方向參考。
- v2 保留為探索歷史與比較參考。
- 後續 Facility direction 應回到 `gui-facility-screen-template.md` 與可讀性規則，而不是直接把任一 candidate 當最終 UI。

## 5. 任務型閱讀建議

### 若要做 Town Hub Screen model

優先讀：

1. `01_content/gui-planning-index.md`
2. `01_content/codex-handoff-short.md`
3. `README.md`
4. `01_content/gui-ui-direction-brief.md`
5. `01_content/gui-screen-map.md`
6. `01_content/ui-flow-blueprint.md`
7. `01_content/gui-town-hub-screen-model-draft.md`

目標應是文件化 `TownHubScreenModel`、`facility_nodes`、少量高價值 badge 與 Town Hub-specific UIAction，不要直接改 runtime。

### 若要 review Town Hub Screen mockup / wireframe

優先讀：

1. `01_content/gui-planning-index.md`
2. `01_content/gui-ui-direction-brief.md`
3. `01_content/gui-screen-map.md`
4. `01_content/ui-flow-blueprint.md`
5. `01_content/gui-town-hub-screen-model-draft.md`
6. `01_content/gui-town-hub-review-checklist.md`
7. 若需要查看既有 review 結論，再讀 `01_content/gui-town-hub-mockup-review-v1.md`

目標應是評估場景式 hub、dynamic text safety、facility node 可讀性、badge 節制與 gameplay safety，不要生成新圖或直接改 runtime。

### 若要做 Town Hub UI-2 / Rich wireframe planning

優先讀：

1. `01_content/gui-planning-index.md`
2. `01_content/gui-ui-direction-brief.md`
3. `01_content/gui-screen-map.md`
4. `01_content/gui-town-hub-screen-model-draft.md`
5. `01_content/gui-town-hub-mockup-review-v1.md`
6. `01_content/gui-town-hub-wireframe-plan.md`

目標應是驗證 resource strip、town guidance、facility nodes、少量 badge 與缺漏 facility 入口策略，不要生成新圖、不選平台、不改 runtime。

### 若要 review 或延續 Town Hub UI-2 markdown wireframe

優先讀：

1. `01_content/gui-planning-index.md`
2. `01_content/gui-town-hub-screen-model-draft.md`
3. `01_content/gui-town-hub-review-checklist.md`
4. `01_content/gui-town-hub-wireframe-plan.md`
5. `01_content/gui-town-hub-ui2-wireframe-draft.md`
6. 若需要查看既有 review 結論，再讀 `01_content/gui-town-hub-ui2-wireframe-review-v1.md`

目標應是檢查 wireframe 是否滿足場景式 hub、resource strip、town guidance、facility node、badge discipline 與 dynamic text safety，不要生成新圖。

### 若要做 Guild Screen model

優先讀：

1. `01_content/gui-planning-index.md`
2. `01_content/codex-handoff-short.md`
3. `README.md`
4. `01_content/gui-ui-direction-brief.md`
5. `01_content/gui-screen-map.md`
6. `01_content/ui-flow-blueprint.md`
7. `01_content/gui-facility-screen-template.md`
8. `01_content/gui-guild-screen-visual-baseline.md`
9. `01_content/gui-guild-screen-model-draft.md`
10. `01_content/gui-guild-screen-review-checklist.md`
11. `01_content/gui-asset-registry-draft.md`

目標應是文件化 `GuildScreenModel`、`GuildTaskRow`、`GuildConditionRow` 與 Guild-specific UIAction，不要直接改 runtime。

### 若要做 Facility template

優先讀：

1. `01_content/gui-planning-index.md`
2. `01_content/gui-ui-direction-brief.md`
3. `01_content/gui-screen-map.md`
4. `01_content/ui-flow-blueprint.md`
5. `01_content/gui-facility-screen-template.md`
6. `01_content/gui-asset-request-schema.md`
7. `01_content/gui-asset-registry-draft.md`

若聚焦 Synthesis，再視需要讀 Synthesis mockup historical 文件。

### 若要生成或評估 mockup

優先讀：

1. `01_content/gui-planning-index.md`
2. `01_content/gui-ui-direction-brief.md`
3. `01_content/gui-asset-request-schema.md`
4. `01_content/gui-asset-registry-draft.md`
5. 對應 screen 文件：
   - Town Hub：`01_content/gui-town-hub-screen-model-draft.md`
   - Town Hub review：`01_content/gui-town-hub-review-checklist.md`
   - Town Hub mockup review record：`01_content/gui-town-hub-mockup-review-v1.md`
   - Town Hub wireframe planning：`01_content/gui-town-hub-wireframe-plan.md`
   - Town Hub UI-2 wireframe draft：`01_content/gui-town-hub-ui2-wireframe-draft.md`
   - Town Hub UI-2 wireframe review：`01_content/gui-town-hub-ui2-wireframe-review-v1.md`
   - Guild：`01_content/gui-guild-screen-visual-baseline.md`
   - Facility / Synthesis：`01_content/gui-facility-screen-template.md`
6. 對應 reference 資料夾 README：
   - `05_assets/gui_references/README.md`
   - `05_assets/gui_references/town_hub/`
   - `05_assets/gui_references/guild_screen/README.md`
   - `05_assets/gui_references/facility_synthesis_screen/README.md`

mockup 評估重點：

- 是否保留中文動態文字安全區。
- 是否符合 ScreenModel / UIAction，而不是新增 gameplay。
- 是否能清楚呈現 list、detail、requirements、feedback、primary action。
- 是否維持 reference / candidate 狀態，不誤升為 runtime asset。

### 若要碰 runtime

必須另開明確小切片，且先做 read-only 評估。

最低要求：

- 先說明要碰哪個 runtime 範圍。
- 先 read-only 對照 `README.md`、`codex-handoff-short.md` 與相關 runtime 檔案。
- 明確確認不修改 data、schema、save、combat formula，除非使用者另行批准。
- 不因 GUI mockup 或 reference image 直接改 gameplay。
- 不重構整個 `03_engine/engine/game.py`。

## 6. 文件治理規則

- 新增任何 GUI markdown 文件時，必須同步更新本 index。
- 新文件必須標記生命週期：`core`、`conditional`、`historical` 或 `archive candidate`。
- 不要再平鋪增加一堆未分類 `.md`。
- 新文件應先放進本索引的其中一層：入口、screen map / flow、facility template、screen baseline、asset / reference、mockup exploration、historical / optional。
- reference image 不等於 runtime asset。
- `.codex/generated_images` 只是生成暫存，不是專案內正式資料來源。
- `05_assets/gui_references` 是專案內 reference / candidate 暫存區，不是正式 runtime asset path。
- 正式 asset pipeline 尚未開始。
- 不要把候選圖直接引用進 `03_engine` 或 runtime。
- 不要把圖片內文字當成資料來源；動態文字必須由 render layer 輸出。
- GUI 規劃文件可以描述未來方向，但不可暗示 pygame / HTML / Unity 已被選定。
- GUI 規劃文件不可把 runtime / data / schema / save / combat formula 變更包進同一輪。

## 7. Snapshot 精簡規則

`01_content/codex-session-snapshot.md` 不再承擔完整歷史流水帳。它只保留：

- 目前專案可接續狀態。
- 當前 GUI planning 結論。
- 已採納 / 未採納 visual baseline。
- 明確禁止事項。
- 新 session 的最短閱讀順序。

已完成過程、舊 prompt、舊 mockup、已落地 runtime MVP 的長細節，不應反覆塞回 snapshot。

## 8. 建議下一步

最適合的下一步是選一個小而清楚的文件化切片：

- Town Hub Screen：可延續 `gui-town-hub-screen-model-draft.md`，補強場景式 `facility_nodes`、badge 優先級與 World Map / Facility Screen 銜接。
- Town Hub mockup review 已完成：`gui-town-hub-mockup-review-v1.md` 結論為 `pass_with_notes`；下一步可小幅同步 `gui-screen-map.md`。
- Town Hub UI-2 planning 已建立：`gui-town-hub-wireframe-plan.md`；下一步可做 markdown-only wireframe 草圖，不生成新圖。
- Town Hub UI-2 wireframe draft 已建立：`gui-town-hub-ui2-wireframe-draft.md`；下一步可用 Town Hub review checklist 審查草圖。
- Town Hub UI-2 wireframe review 已完成：`gui-town-hub-ui2-wireframe-review-v1.md` 結論為 `pass_with_notes`；下一步可寫 visual mockup prompt draft，但先不生成新圖。
- Guild Screen：下一步可 read-only 對照 `guild_menu()` 與任務資料來源，列出未來 `build_guild_screen_model(...)` 可能需要的資料。
- Facility Template：補強 `FacilityScreenModel` 與不同 facility variant 的欄位差異。
- Mockup 評估：建立一份單一 screen 的 review checklist，不生成新圖。

若任何下一步需要 runtime，請另開 read-only 小切片再決定。
