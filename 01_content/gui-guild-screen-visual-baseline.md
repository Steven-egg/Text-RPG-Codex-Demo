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

這張圖不是商店、合成屋或完整工會管理後台，而是：

- 左側選任務。
- 中央看任務詳情。
- 中央中段看報酬。
- 中央下方看達成 / 回報條件。
- 底部看 NPC 提示與操作 feedback。
- 右下執行唯一主要 action。

GUI 第一版 demo 最適合做「工會任務列表 / 委託板」，不要先擴成完整工會管理系統。

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
- Guild Screen 第一版重點是任務選取、任務詳情、報酬與回報條件。
- 額外資源摘要容易讓畫面變成管理型 UI，也會削弱委託板語意。

### C. 左側頁籤列

建議分類：

- 可接任務
- 進行中任務
- 可回報 / 已完成
- 主線線索 / 特殊委託

注意：
- 圖示可以存在，但 tab label 必須動態輸出。
- 第一版可先只實作其中 2-3 種狀態，視目前任務流程而定。

### D. 左側任務列表

用途：
- 快速掃描任務，不承載完整任務描述。

每列建議欄位：

- 任務名稱
- 任務地點
- 建議等級
- 任務狀態 icon

狀態 icon 建議先限制為：

- 可接
- 進行中
- 可回報
- 鎖定

限制：
- 不放任務長描述。
- 不放完整報酬。
- 不放完整完成條件。
- 若中文資訊變多，允許加高 row、減少同屏列數，透過滾動解決密度。

### E. 中央上方任務詳情區

用途：
- 放選中任務的完整詳情。

建議內容：

- 任務名稱
- 任務類型
- 任務地點
- 建議等級
- 任務描述

文字容量：
- 第一版以 2-4 行中文描述為主。
- 若描述較長，預留內部 scroll behavior。
- 不把任務描述塞進左側列表。

### F. 中央詳情區下方小框

定稿定位：

```text
任務報酬摘要
```

建議內容：

- 金幣
- 工會積分 / 聲望
- 道具報酬
- 解鎖內容

限制：
- 不與任務完成條件混用。
- 不放長敘事。
- 不放 NPC feedback。

### G. 中央下方表格區

定稿定位：

```text
任務達成條件 / 回報條件檢查表
```

建議 row 結構：

```text
條件類型 icon
→ 條件名稱
→ 需求數量 / 目前持有數
→ 狀態：綠勾 / 紅叉
```

可支援內容：

- 所需素材名稱
- 需求數量 / 目前持有數
- 討伐數
- 探索完成度
- 是否已回報前置任務

限制：
- 不做大規模管理表格。
- 第一版最多 3-5 條條件較穩。
- 欄位不可過多，避免失去 RPG 感。

### H. 底部中央深色訊息區

定稿定位：

```text
NPC 說明與操作 feedback bar
```

建議內容：

- 工會接待員提示
- 任務提示
- 條件不足原因
- 接取成功訊息
- 回報成功訊息

此區可作為 Guild / Facility 類畫面的共用 feedback bar，但 Guild Screen 應保留接待員語氣。

### I. 右下主要操作按鈕

用途：
- 單一主要 action。

依任務狀態動態切換：

- 接受任務
- 回報任務
- 確認
- 不可操作狀態

限制：
- 第一版只保留一個主要操作按鈕。
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
- 中央表格的綠勾 / 紅叉狀態語彙。

避免：

- 合成屋 / 商店道具感過重。
- 額外資源槽與語意不明的黑色資訊框。
- 任務列表 row 放過多描述。
- 中央表格變成後台管理 UI。
- 同時出現多個主要 action。
- 把固定中文或數字畫死在圖片中。

## 4. 與 Facility 共用模板的關係

Guild Screen 可沿用 Facility Screen 的大骨架：

```text
category / tab
→ list
→ selected detail
→ requirement / status
→ confirm
→ feedback
```

但 Guild Screen 必須保留自己的語意：

- list 是任務列表，不是商品或配方列表。
- detail 是任務詳情，不是商品詳情。
- requirement 是任務達成 / 回報條件，不是購買或合成素材而已。
- feedback 是接待員提示與任務狀態，不是交易結果而已。

## 5. 第一版 Demo 建議範圍

第一版 Guild Screen demo 最小可做：

- 顯示任務列表。
- 選中任務。
- 顯示任務詳情。
- 顯示報酬摘要。
- 顯示達成 / 回報條件檢查。
- 底部顯示接待員提示。
- 右下依狀態顯示接受 / 回報 / 不可用。

暫不做：

- 完整工會積分系統。
- 完整任務歷史。
- 多層工會子頁。
- 複雜篩選與排序。
- 批量回報。
- 任務地圖自由導航。

## 6. 後續文件建議

若後續要繼續文件化，可新增：

- `01_content/gui-guild-screen-prompt-draft.md`：以此 baseline 轉成正式 prompt 草案。
- `01_content/gui-guild-screen-model-draft.md`：定義 GuildScreenModel / GuildTaskRow / GuildConditionRow。
