# GUI Guild Screen Visual Baseline

用途：依據使用者提供的 Guild Screen UI 參考圖，定稿第一版工會畫面的視覺基準與資訊配置。此文件只做 GUI 規劃，不代表已進 runtime、不啟動正式 asset pipeline。

## 0. 參考圖

```yaml
baseline_id: gui_guild_screen_visual_baseline_v1
status: accepted_visual_baseline
screen_id: facility_guild_screen
flow_id: flow_a_town_facility
source_image_path: 05_assets/gui_references/guild_screen/guild_screen_visual_baseline_v1_user_reference.png
runtime_usage_allowed: false
copied_into_project_assets: false
copied_into_project_references: true
```

此圖作為 Guild Screen 第一版 GUI 視覺方向基準；目前已放入 `05_assets/gui_references` 作為 reference，但不是正式 runtime asset，也不直接引用進遊戲。

## 1. 畫面定位

最終定位：

```text
Adventurers' Guild / Quest Board
冒險者工會 / 委託板
```

Guild Screen V1 忠於目前 runtime，定位為：

- 已解鎖委託瀏覽。
- 任務需求與報酬查看。
- 條件滿足時提交 / 回報任務。
- 三枚火印碎片後的諾亞詢問入口。

這張圖不是商店、合成屋、完整工會管理後台，也不是接任務系統。GUI 第一版 demo 不新增 `active_quests`，不處理「接取任務」，也不把工會素材收購放進主視覺。

## 2. 定稿區塊配置

### A. 左上大橫幅

用途：
- Guild Screen 標題區。

推薦動態文字：
- `冒險者工會 / 委託板`
- 或 `冒險者工會` + `委託板`

限制：
- 不放玩家身份資訊。
- 不放雜項資源。
- 不把文字畫死在圖片裡。

### B. 頂部小資訊槽與右上資訊框

定稿決策：
- 刪除語意不明的左上三個小資訊槽。
- 刪除右上黑色資訊框。
- 不硬塞非核心資訊。

原因：
- Guild Screen V1 重點是任務選取、任務詳情、報酬與回報條件。
- 額外資源摘要容易讓畫面變成管理型 UI，也會削弱委託板語意。

### C. 任務篩選列

V1 可保留任務篩選列，但它只作為 UI-only filter，不代表 gameplay state，也不寫入 save/state/schema。

建議 filter：

- 全部委託。
- 可回報。
- 已完成。

限制：

- 不顯示「可接任務」。
- 不顯示「進行中任務」。
- 不顯示可接 / 接取 / active 類任務狀態。
- 不使用 `category_tabs` 命名。
- 不新增 `active_quests` 或任務接取流程。

V1 也不需要 `sections` / `selected_section_id`。三枚火印碎片後的諾亞詢問入口優先以 `story_hint_card` 顯示；若 layout 受限，可降級為任務列表附近的特殊互動列。

### D. 左側任務列表

用途：
- 快速掃描套用 filter 後的已解鎖委託。

每列建議欄位：

- 任務名稱。
- 委託人。
- 任務狀態 marker。

狀態 marker 建議先限制為：

- 可回報。
- 條件不足。
- 已完成。

V1 延後：

- 任務地點。
- 建議等級。
- 任務類型。

限制：
- 不放任務長描述。
- 不放完整報酬。
- 不放完整完成條件。
- 不顯示「可接」或「進行中」這類暗示接任務流程的狀態。
- 若中文資訊變多，允許加高 row、減少同屏列數，透過滾動解決密度。

### D-1. Story Hint Card

用途：
- 顯示三枚火印碎片後的諾亞詢問入口。

顯示條件：
- 玩家持有 `key_fire_mark_shard x3`。
- 尚未完成 `fire_mark_guild_inquiry_done`。

限制：
- 不做成 tab。
- 不計入任務 filter 數量。
- 不寫入 `QUESTS`。
- 若 layout 受限，可降級為左側列表附近的特殊互動列。

### E. 中央上方任務詳情區

用途：
- 放選中任務的完整詳情，或選中 story hint 時的主線詢問說明。

V1 建議內容：

- 任務名稱。
- 委託人。
- 任務描述。
- 目前狀態。

V1 延後：

- 任務類型。
- 任務地點。
- 建議等級。
- 由迷宮 / Boss 推導出的風險提示。

文字容量：
- 第一版以 2-4 行中文描述為主。
- 若描述較長，預留內部 scroll behavior。
- 不把任務描述塞進左側列表。

### F. 中央詳情區下方小框

定稿定位：

```text
任務報酬摘要
```

V1 建議內容：

- 金幣。
- 工會積分。
- 道具報酬。
- 解鎖內容摘要。

限制：
- 使用 `guild_points` / 工會積分語意，不使用 reputation / 聲望暗示新系統。
- 不與任務完成條件混用。
- 不放長敘事。
- 不放 NPC feedback。

### G. 中央下方表格區

定稿定位：

```text
任務達成條件 / 回報條件檢查表
```

V1 row 結構：

```text
條件類型 icon
→ 條件名稱
→ 需求數量 / 目前持有數或目前狀態
→ 狀態：已滿足 / 未滿足
```

V1 支援內容：

- 所需素材、物品或裝備名稱。
- 需求數量 / 目前持有數。
- `flag:xxx` 條件是否已成立。
- 無需求任務的 readable empty state。

V1 延後：

- 討伐數。
- 探索完成度。
- 前置任務鏈表格。
- 大型管理表格。

限制：
- 第一版最多 3-5 條條件較穩。
- 欄位不可過多，避免失去 RPG 感。
- 不只靠紅綠色判斷條件狀態。

### H. 底部中央深色訊息區

定稿定位：

```text
NPC 說明與操作 feedback bar
```

建議內容：

- 工會接待員提示。
- 任務提示。
- 條件不足原因。
- 回報成功訊息。
- 任務已完成提示。
- 三枚火印碎片後的諾亞詢問提示。

不顯示：

- 接取成功訊息。
- 素材收購結果。

此區可作為 Guild / Facility 類畫面的共用 feedback bar，但 Guild Screen 應保留接待員語氣。

### I. 右下主要操作按鈕

用途：
- 單一主要 action。

V1 依選中 row 狀態動態切換：

- `submit_quest`：回報任務。
- `open_story_hint`：查看 / 觸發諾亞主線詢問。
- `unavailable`：條件不足、已完成或無選取。

限制：
- 不顯示「接受任務」。
- 不增加多個並列主 action。
- 按鈕文字必須動態渲染。

### J. 左下返回區

定稿定位：

```text
返回 Town Hub / 離開工會
```

screen flow：

```text
Town Hub Screen
→ Guild Screen
→ Town Hub Screen
```

第一版不做工會內多層返回。

## 3. 視覺定稿要點

保留：

- 工會接待員與角色互動感。
- 委託板 / 接待櫃台氛圍。
- 羊皮紙、木材、黃銅、藍色工會旗幟、指南針 / 冒險者徽記。
- 左側任務列表 + 中央詳情 + 條件檢查 + 底部 feedback + 右下 action 的清楚層級。
- 中央表格的狀態語彙。

避免：

- 合成屋 / 商店道具感過重。
- 額外資源槽與語意不明的黑色資訊框。
- 任務列表 row 放過多描述。
- 中央表格變成後台管理 UI。
- 同時出現多個主要 action。
- 把固定中文或數字畫死在圖片中。
- 視覺上暗示接任務、任務接取狀態或 `active_quests`。

## 4. 與 Facility 共用模板的關係

Guild Screen 可沿用 Facility Screen 的大骨架：

```text
list
→ task filter
→ selected detail
→ requirement / status
→ primary action
→ feedback
```

但 Guild Screen V1 必須保留自己的語意：

- list 是套用 task filter 後的已解鎖任務，不是商品或配方列表。
- story hint 是特殊提示卡；layout 受限時才降級為特殊互動列。
- detail 是任務詳情，不是商品詳情。
- requirement 是任務達成 / 回報條件，不是購買或合成素材而已。
- feedback 是接待員提示與任務狀態，不是交易結果而已。
- 素材收購不納入 Guild Screen V1；未來應另作 Guild Buyback / Exchange 類型畫面。

## 5. 第一版 Demo 建議範圍

第一版 Guild Screen demo 最小可做：

- 顯示已解鎖任務列表。
- 顯示 UI-only task filters：全部委託、可回報、已完成。
- 顯示三枚火印碎片後的諾亞詢問 `story_hint_card`。
- 選中任務。
- 顯示任務詳情。
- 顯示報酬摘要。
- 顯示達成 / 回報條件檢查。
- 底部顯示接待員提示。
- 右下依狀態顯示回報 / 查看線索 / 不可用。

暫不做：

- 接任務系統。
- `active_quests`。
- `category_tabs` / sections。
- 可接任務 / 進行中任務這類生命週期 tab。
- 任務地點、任務類型、建議等級。
- 工會素材收購。
- 完整工會積分系統。
- 完整任務歷史。
- 多層工會子頁。
- 複雜篩選與排序。
- 批量回報。
- 任務地圖自由導航。

## 6. 後續文件建議

若後續要繼續文件化，可新增：

- `01_content/gui-guild-screen-prompt-draft.md`：以此 baseline 轉成正式 prompt 草案。
- Guild Buyback / Exchange 類型畫面草案：若未來要處理素材收購 GUI，應獨立於 Guild Screen V1。
