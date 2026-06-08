# Shop Skinning Lab v0.2.2 — isolated visual baseline

## 核心說明

- **本資料夾定位**：一個完全獨立 (isolated)、僅使用靜態資料 (fixture-only) 的介面外觀修補實驗室 (skinning lab)。
- **非正式產物**：本資料夾內的所有程式碼皆非正式 Shop runtime 的原始碼，亦不具備任何 gameplay 決策權限 (not gameplay authority)。
- **目前視覺基線**：目前 live lab 狀態為 v0.2.2 layout refinement，已形成可供後續 lab-only skinning 對照的 player-facing visual baseline。
- **來源階段**：v0.1.1 為 extraction repair 起點；v0.2.2 是在該基礎上完成欄寬、Footer、debug panel 隱藏、NPC visual stage 與 zoom clipping 修正後的目前基線。
- **無 runtime／API 依賴**：本 lab 不涉及任何 runtime-client、API calls、fetch 或 live mode。
- **禁止直接合併**：不可直接將此處的 fixtures、fake behaviors 或 lab-only 測試控制項 merge 回正式 Shop。
- **雙向同步限制**：無論是從正式 Shop 進行 resync 或是將本 lab merge-back，都必須通過新的 owner-approved read-only planning gate。

---

## 一、Local Task Capsule (本地任務膠囊)

本 lab 的設計宗旨之一為大幅降低未來 Antigravity 進行 isolated skinning iteration 時的 token／context 消耗。

未來進行一般 **lab-only skinning** 工作時，您**僅需要**閱讀：
1. Repository-required Hot Zone startup reads (依專案治理規則，如 `AGENTS.md` 等)。
2. 本 `README.md`。
3. 本資料夾內的檔案 (`index.html`、`shop_skinning_lab.css`、`shop_skinning_lab.js`、`fixtures.js`)。

未來一般 lab-only skinning **絕對不應**重新閱讀：
- 正式 Shop prototype 原始碼。
- GUI runtime bridge plan。
- Python runtime 與 ScreenModel 實作。
- 專案 data、schema、save.json 或 combat 相關文件。
- 大型歷史 progress 紀錄文件。

---

## 二、Source Snapshot (來源快照記錄)

本 lab 最初的 v0.1.1 extraction repair 係參考以下正式 Shop 檔案做為視覺 extraction source：
- `07_gui_prototype/shop_screen/index.html`
- `07_gui_prototype/shop_screen/styles.css`
- `07_gui_prototype/shop_screen/shop-screen.js`
- `07_gui_prototype/shop_screen/fixtures/shop-default.json`
- `07_gui_prototype/shop_screen/fixtures/shop-constrained.json`

此快照資訊僅供備查，未來普通 skinning iteration 不應自動重新載入或同步這些檔案。

目前 v0.2.2 的版面決策、隱藏項目與 Footer / NPC 安全區修正，請以 `shop-skinning-process-note-v1.md` 為接續依據。

---

## 三、Retained Visual Baseline (保留之正式 Shop 視覺結構)

為確保本 lab 能夠與正式 Shop runtime-shaped prototype 進行肉眼對照，本 lab 重建並保留了以下視覺結構：
- **Shop resource strip**：結構保留但預設隱藏，不顯示 lab 自創的資源列，符合正式 Shop 現狀。
- **Header**：包含動態商店標題與副標題，以及 fixture scenario selector。
- **Category Tabs**：提供完整的分類頁籤切換（❖ 全部、🧪 補給品、⚔ 戰術道具、💍 飾品）與商品計數。
- **Complete Item List**：提供完整的 9 項商品列，支援 hover、selected 與 disabled 狀態。
- **Detail Panel**：顯示所選商品的細節資訊，包含分類、持有數、描述、效果摘要與使用用途。
- **Requirements Panel**：展示購買限制列表（金幣或聲望等），標示已滿足 (`met`)、金幣不足 (`blocked`/`missing`) 或售罄 (`missing`) 等狀態。
- **NPC Safe Area**：保留右側 NPC 莉娜／特里的視覺安全區、NPC 姓名與角色稱號。
- **Footer Actions**：提供獨立的返回按鈕（左）、提示回饋欄（中）與主要購買按鈕（右）。
- **UIAction Log**：摺疊式 (`<details>`) 的 test action 記錄面版，用以驗證使用者操作事件的派發模擬。

### 響應式佈局基準 (Responsive Baseline)
- **1440px**：標準三欄式桌面佈局 (item browser / item detail / NPC column)。
- **1220px 及以下**：切換為垂直單欄式堆疊佈局 (stacked layout)。
- **720px**：窄螢幕極簡佈局，不隱藏 NPC 區。

---

## 四、何時需要重啟 Broader Reading

若在未來的 lab-only skinning 遇到以下狀況，請**立即停止**工作，並取得新的 read-only planning gate：
- 需要從正式 Shop 檔案進行 resync。
- 需要評估或執行 merge-back 回正式 prototype。
- 需要修改 ScreenModel 或 UIAction contract 假設。
- 企圖連接 Python runtime、實體 API 或 live bridge。
- 需要修改本 lab 資料夾以外的任何檔案。
- 建立正式的 asset pipeline 或 Design System。
- 擴大到其他設施畫面（如 Magic Shop, Synthesis 等）。
