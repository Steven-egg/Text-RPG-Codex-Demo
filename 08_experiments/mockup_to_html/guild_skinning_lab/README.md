# Guild Screen Skinning Lab v0.1.0 — isolated visual baseline

## 核心說明

- **本資料夾定位**：一個完全獨立 (isolated)、僅使用靜態資料 (fixture-only) 的介面外觀修補實驗室 (skinning lab)。
- **非正式產物**：本資料夾內的所有程式碼皆非正式 Guild Screen runtime 的原始碼，亦不具備任何 gameplay 決策權限 (not gameplay authority)。
- **無 runtime／API 依賴**：本 lab 不涉及任何 runtime-client、API calls、fetch 或 live mode。
- **禁止直接合併**：不可直接將此處的 fixtures、fake behaviors 或 lab-only 測試控制項 merge 回正式 screen。

## 檔案說明

- `index.html`：從正式 prototype 抽取的 DOM 結構，已改為引用本地樣式與腳本。
- `guild_skinning_lab.css`：複製自正式 prototype 現有樣式。
- `guild_skinning_lab.js`：靜態行為控制器，移除了與 runtime 連接的 ESM 模組與 API 呼叫。
- `fixtures.js`：由原 json 檔轉換而來的靜態場景數據。
