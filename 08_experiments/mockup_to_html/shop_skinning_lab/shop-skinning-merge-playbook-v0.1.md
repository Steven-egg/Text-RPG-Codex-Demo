# Shop Skinning Lab Merge Playbook (商店視覺優化合併指南) v0.1

本指南記錄將實驗室版本（`08_experiments/mockup_to_html/shop_skinning_lab/`）合併回正式商店靜態原型（`07_gui_prototype/shop_screen/`）的最小實作路徑、已知風險以及可重複使用的合併流程。

---

## 1. 合併目的

* **驗證可行性**：本輪合併並非正式定版，其核心目的在於驗證從獨立實驗室（isolated lab）回推至正式靜態原型（`07_gui_prototype`）的 merge-back 路線可行，且能在過程中不損壞 Live Bridge 通訊。
* **建立參考範本**：記錄本次成功合併的最小實作路徑，作為後續 Magic Shop (魔法商店)、Workshop (鐵匠鋪)、Synthesis (合成屋) 等城鎮設施畫面進行視覺整合與 Lab merge-back 的技術參考。

---

## 2. 檔案對照映射 (Source -> Target Mapping)

| 來源 Lab 檔案 (Source) | 目標正式檔案 (Target) | 合併處理策略 |
| :--- | :--- | :--- |
| `index.html` | [07_gui_prototype/shop_screen/index.html](file:///C:/Users/user/OneDrive/文字冒險遊戲/07_gui_prototype/shop_screen/index.html) | **結構重整**。調整 `<aside>` 層級並引入字體，保留 ESM 模組引用與開發用 DOM 節點。 |
| `shop_skinning_lab.css` | [07_gui_prototype/shop_screen/styles.css](file:///C:/Users/user/OneDrive/文字冒險遊戲/07_gui_prototype/shop_screen/styles.css) | **直接替換**。整合 Obsidian Dark & Gold 主題、三欄式 grid 佈局與響應式規則。 |
| `fixtures.js` 內變數 | [07_gui_prototype/shop_screen/fixtures/](file:///C:/Users/user/OneDrive/文字冒險遊戲/07_gui_prototype/shop_screen/fixtures/) | **格式轉寫**。將 JS 全域變數物件轉換為對應的 JSON 檔案（`shop-default.json` 與 `shop-constrained.json`）。 |
| `bg-npc.jpg` | `07_gui_prototype/shop_screen/bg-npc.jpg` | **拷貝資源**。拷貝作為 CSS 局部調用的背景立繪圖資源。 |
| `shop_skinning_lab.js` | [07_gui_prototype/shop_screen/shop-screen.js](file:///C:/Users/user/OneDrive/文字冒險遊戲/07_gui_prototype/shop_screen/shop-screen.js) | **邏輯整合（不可覆蓋）**。只作渲染對齊參考，完整保留正式版的 Live Mode 通訊機制。 |

---

## 3. 實作步驟紀錄

### Step 1. 資源拷貝 (Assets)
* 將實驗室的立繪背景圖 `bg-npc.jpg` 複製至目標資料夾 `07_gui_prototype/shop_screen/bg-npc.jpg`。

### Step 2. CSS 視覺整合 (Styles)
* 將 `shop_skinning_lab.css` 寫入 `styles.css`，用以帶入：
  * Obsidian Panel、細金線與角落星芒 `✦` 裝飾。
  * 琥珀金選中高光（`--amber-glow`）與狀態徽章樣式。
  * 三欄式主佈局（catalog / detail / npc stage）與 1220px 媒體查詢。

### Step 3. HTML 結構對齊 (DOM Structure)
* 編輯 `index.html`，在 `<head>` 中載入 `Noto Serif TC` 和 `Outfit` 字體連結。
* 將 `<aside class="shopkeeper-side">` 移動至 `<main class="shop-layout">` 元素外部，使其在 Grid 中與 Header/Footer 平級，以配合新 CSS 佈局。
* **保留**底部的 `<script type="module" src="./shop-screen.js"></script>` ESM 引腳，不可改為 Lab 版的普通腳本。
* **保留** DOM 中的 `#screen-subtitle`、`.screen-label`、`.fixture-switcher` 等開發用節點，僅透過 CSS 將其隱藏，防止 JS 查詢回傳 Null。

### Step 4. Fixture JSON 同步 (Data Sync)
* 使用 Python 腳本（`convert_fixtures.py`）清洗 `fixtures.js` 中的 `SHOP_DEFAULT_FIXTURE` 與 `SHOP_CONSTRAINED_FIXTURE` 物件，剔除 JS 全域宣告，輸出為純 JSON，覆蓋寫入：
  * `fixtures/shop-default.json`
  * `fixtures/shop-constrained.json`

### Step 5. 保留正式 Live Bridge 行為 (JavaScript Preservation)
* 完整保留 `shop-screen.js` 的 ES Module 結構、`runtimeClient` 呼叫、Live Mode 下 `dispatchAction` 與靜態模式下 `fetch` 的邏輯。經比對，正式版 JS 渲染方法與 Lab 一致，本次不改動正式 JS 以避免風險。

### Step 6. CSS-Only Layout Tuning (佈局微調)
* **增寬商品面板**：調整 `--catalog-col` 為 `clamp(460px, 28vw, 540px)`，加寬左側商品卡片，解除分類 Tab 及名稱/持有量/狀態 Badge 的擠壓狀況。
* **預防佈局溢出**：微調 `--npc-col` 下限至 `minmax(300px, 1fr)`，確保寬度收縮至 `1220px` 臨界點時三欄能緊密貼合，無水平滾動條產生。

---

## 4. 成功條件與驗證 (Verification Plan)

合併完成後，必須依序執行以下驗證：

1. **JS 語法基本檢查**（因本機環境 global node command 缺失，此項可在具備 Node 環境下執行）：
   ```powershell
   node --check 07_gui_prototype/shop_screen/shop-screen.js
   ```
2. **Live Bridge 冒煙測試**：
   ```powershell
   python 06_tools/smoke_test_shop_bridge.py
   ```
   * *指標*：終端機輸出 `Shop Travel Inventory bridge smoke test successfully completed all checks!` 且回報 `PASS`。
3. **全遊戲主流程與資料校驗**：
   ```powershell
   python element_maze.py --smoke-test
   python 06_tools/validate_data.py
   ```
   * *指標*：回報 `smoke test ok` 與 `data validation ok`。
4. **瀏覽器視覺檢查 (Visual QA)**：
   * 在 Live 模式或 Fixture 模式下造訪 `07_gui_prototype/shop_screen/index.html`。
   * 確認商品列表寬度充足、詳細面板及 NPC 區塊無錯位。
   * 切換縮放比例（100%、90%、67%），確認右下角購買按鈕可正常點擊且無邊界裁切。

---

## 5. 已知風險與禁止事項 (Guardrails)

* **禁止 JS 直接覆蓋**：嚴禁以 `shop_skinning_lab.js` 直接覆蓋 `shop-screen.js`，否則會斷開與 Python 後端的即時連線。
* **禁止 Fixtures 升格**：不可將 JSON 測試假資料視為 gameplay 規則的權威來源（gameplay SSOT 依然是 Python 原始碼與資料表）。
* **禁止修改 Runtime 核心**：在進行設施畫面視覺合併時，禁止修改 Python runtime、data、schema、save.json 或戰鬥機制。
* **禁止建立正式 Asset Pipeline**：背景圖等實驗資源僅限於 `shop_screen/` 本地調用，嚴禁在 `05_assets/` 或其他全域目錄建立複雜的構建或轉檔管線。
* **禁止盲目推論**：Shop 的成功 merge-back 不代表 Magic Shop、Workshop 等其他設施可以免除演練直接合併。每個 Screen 在合併前均需單獨進行 read-only rehearsal。

---

## 6. 後續設施 Merge 操作計畫 (Reusable Workflow)

未來其他設施畫面（如 Magic Shop, Workshop）合併時，應遵循以下標準作業程序（SOP）：

```
[1. Read-Only Rehearsal] ──> [2. 建立測試分支] ──> [3. 拷貝新資源 (bg/image)]
                                                        │
[6. 視覺與佈局微調] <── [5. 整合渲染 HTML/CSS] <── [4. 轉寫 JSON Fixtures]
         │
[7. 雙軌驗證 (Smoke & Visual)] ──> [8. 撰寫與更新 Playbook/Handoff]
```

1. **第一階段：唯讀評估 (Rehearsal)**
   * 列出該設施畫面 Source 與 Target 的檔案對照。
   * 檢查 HTML 節點變動與 JS live mode 通訊相依性。
2. **第二階段：環境準備 (Branching)**
   * 確認 git status 乾淨。建議建立獨立測試分支（如 `feat-gui-merge-<facility>`）。
3. **第三階段：資源與資料轉寫 (Assets & Data)**
   * 拷貝該設施所需的圖像/背景至其 prototype 目錄。
   * 將該實驗室的靜態數據轉寫為對應目錄下的 `.json` fixtures。
4. **第四階段：HTML 與 CSS 整合 (Visual Integration)**
   * 移動必要的 DOM 節點以配合 CSS 佈局，引入字體。
   * 覆蓋或整合 `styles.css`，優先保證 ESM 腳本結構不受破壞。
5. **第五階段：微調與驗證 (Tuning & Smoke Test)**
   * 啟動瀏覽器進行不同解析度與縮放比的 Layout QA，進行必要的 CSS 變數微調。
   * 執行該設施的 Live Bridge 冒煙測試與遊戲本體 smoke test，確保 `PASS`。
   * 記錄 diff 與待優化項目。

---

## 7. 下一輪候選任務 (Deferred Candidate Backlog)

> [!NOTE]
> 以下僅列出後續規劃候選，本次不進行任何實體開發。

* **設施畫面視覺品質與響應式 QA (Browser/Responsive Visual QA)**
  * 在不同作業系統（Windows / macOS）及不同瀏覽器內核下，針對 Shop 合併後的邊界縮放與毛玻璃（backdrop-filter）支援度進行全面視覺核對。
* **Magic Shop / Workshop 合併前唯讀對照**
  * 比對 `08_experiments/` 內 Magic Shop 與 Workshop 的實驗室版，與 `07_gui_prototype/` 正式版之間的 DOM 及 JS 差異，產出 Source -> Target Mapping 對照表。
* **設施類 shared CSS 提取計畫 (Family-Level Shared CSS Planning)**
  * 評估是否將黑曜石面板（Obsidian Panel）、金線裝飾（Gold Ornaments）、JRPG 頁籤等通用樣式提取為 shared CSS（例如 `07_gui_prototype/shared/facility-common.css`），以減少重複代碼，但前提是**不進行全域樣式庫的強制重構**。
