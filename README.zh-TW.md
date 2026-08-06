# Element Maze（元素迷宮）

這是可遊玩的 Element Maze RPG 專案入口。主要入口為即時 GUI，另保留
CLI 文字核心版；詳細決策與專門契約位於 `01_content/`。

[English README](README.md)

## 目前階段：依使用者回饋進行維護

目前可玩的內容範圍已穩定。除非另有明確決定，不主動開啟新擴充內容或
正式發行流程；先收集、排序並處理真實使用者回饋，改善既有遊戲體驗。

可處理的維護範圍包括：

- 音效品質、時機、音量與靜音行為；
- 繁體中文文案、翻譯、術語與編碼問題；
- GUI 排版、可讀性、互動回饋與畫面呈現問題；
- 會影響正常遊玩的可重現遊戲邏輯或 runtime 問題。

每一項回饋都應作為一個連貫的維護任務處理。遊戲規則仍以 Python 與
`04_data/data/` 為準；不可因回饋自行推論或新增內容、系統或發行範圍。

## 歷史驗證紀錄

- Batch A--C 的已驗證整合候選版為
  `codex/s6-wave3-integration` 上的
  `02aa179ef8f9259b56369e3998cb7d91ee81ea3d`；它已通過 runtime、劇情、
  SFX、發行資產、portable package 與 localhost/browser 驗證。
- 歷史紀錄中的 `main` 與 `origin/main` 為
  `46efeb93a0e98da12bde6c60769af2d303aeeb26`。候選版未因此自動提升為
  `main`，也不代表已正式發行。
- GUI 是主要產品入口；次要 CLI 名稱為 **文字核心版 Text Core**。
- Python 與 `04_data/data/` 是遊戲規則的唯一權威。瀏覽器 JavaScript、
  靜態 fixtures、portable launcher 與 release builder 不得自行定義遊戲規則。

## 已落地的候選內容摘要

- 可玩範圍封存為 Fire、Ice、Earth、Thunder、Final 五個區段、四個基礎職業、
  八條正式轉職路線、四個元素封印與 Final Boss。
- `story_beat` 選用呈現資料固定六個欄位：`id`、`kind`、`title`、`lines`、
  `dismiss_label`、`tone`。`kind` 可為 `prologue`、`region_transition`、
  `boss_before`、`boss_after`、`ending`；`tone` 可為 `neutral`、`warning`、
  `victory`、`ending`。
- GUI 會安全忽略無效劇情 payload，並呈現序章、區域轉換、Boss 前後劇情與結局。
  戰鬥完成順序維持：`result close -> boss_after -> ending -> navigation`。
- 目前有五種可切換的程序式微型 SFX，沒有 BGM、二進位音檔或自動播放。
  啟用狀態使用 `element_maze.sfx_enabled`，預設為開啟；舊版
  `element_maze.sfx_muted` 會一次性遷移。不受信任的 synthetic click 不得建立或
  恢復 `AudioContext`。
- 僅供發行使用的圖片 builder 會將參照圖片寫入
  `dist/assets-overlay/app/<repository-relative-path>`，並將 format 1 manifest
  寫入 `dist/manifests/assets-manifest.json`。已驗證候選版包含 196 張圖片、排除
  47 張 `OLD` 圖與 6 張未參照圖片，且不覆寫 repository 原始檔。
- Windows portable builder 會分開保留 `app/` 與 `assets-overlay/app/`，啟動既有的
  live GUI/runtime bridge，也能開啟 **文字核心版 Text Core**。本機驗證 ZIP 已通過
  搬移檢查，但不屬於正式發行。
- 正式發行目前仍受 `release_ready:false` 阻擋：runtime 尚未確認可再散布、
  runtime／相依授權尚未彙整，且已驗證的本機 runtime 缺少 `rich` 相依套件。

## 執行方式

同步的 `.venv` 若不健康，請勿依賴它；請為目前 worktree 明確指定 Python：

```powershell
$mazePython = 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
```

主要即時 GUI：

```powershell
& $mazePython -B .\06_tools\gui_runtime_bridge.py
```

開啟 `http://127.0.0.1:8010/start_screen/index.html?mode=live`。請使用 localhost，
不要使用 `file://`。

次要 CLI（**文字核心版 Text Core**）：

```powershell
& $mazePython .\element_maze.py
```

當本機 Python 環境正常時，`run-game.bat` 仍可作為 CLI 便利入口。`save.json` 是
runtime 輸出，不應手動編輯。

若只處理靜態 GUI，請先讀
`.codex/skills/element-maze-gui-static-prototype/SKILL.md`，啟動
`start_gui_prototype_server.bat`，並保留 fixture fallback 與 UIAction logging。

## 驗證路徑

遊戲／runtime 基線：

```powershell
& $mazePython 06_tools\validate_data.py
& $mazePython element_maze.py --smoke-test
& $mazePython 06_tools\test_job_growth_points.py
& $mazePython 06_tools\test_promotion_contracts.py
& $mazePython 06_tools\test_dungeon_defeat_contract.py
& $mazePython 06_tools\smoke_test_combat_bridge.py
& $mazePython 06_tools\test_combat_balance_report.py
```

劇情與 GUI SFX：

```powershell
& $mazePython 06_tools\test_story_beats.py
node 06_tools/test_gui_story_beats.mjs
node 06_tools/test_gui_sfx.mjs
```

僅供發行的參照資產：

```powershell
& $mazePython 06_tools\test_release_assets.py
& $mazePython 06_tools\build_release_assets.py --dry-run
& $mazePython 06_tools\build_release_assets.py --output dist\assets-overlay --manifest dist\manifests\assets-manifest.json
& $mazePython 06_tools\build_release_assets.py --verify --output dist\assets-overlay --manifest dist\manifests\assets-manifest.json
```

Windows portable 驗證：

```powershell
& $mazePython 06_tools\test_windows_portable.py
```

文件與變更基本檢查：

```powershell
git diff --check
```

完整的 build／verify 指令、runtime 要求與正式發行條件定義於
`01_content/windows-portable-release-v1.md`。若未帶 `--redistributable-runtime`
而提供機器本機 runtime，產出的只是被忽略的本機驗證結果，且
`release_ready:false`；不得發布或宣稱為可正式發行。

戰鬥平衡的 phase-0 報告僅供診斷，不授權據此調整數值：

```powershell
& $mazePython 06_tools\test_combat_balance.py --phase0
```

## 專案結構

- `element_maze.py`：文字核心版入口。
- `01_content/`：現行決策、交接、計畫與封存歷史。
- `02_schema/`：資料契約。
- `03_engine/engine/game.py`：CLI 生命週期、戰鬥、主迴圈與相容性 re-export。
- `03_engine/engine/facilities.py`：城鎮設施的 CLI 領域邏輯。
- `03_engine/engine/dungeon.py`：地下城選單、探索、事件、Boss gate、通關交接與
  戰敗處理。
- `03_engine/engine/state.py`：可持久化預設值與共用 state helper。
- `04_data/data/`：runtime 資料的 SSOT。
- `06_tools/`：bridge、validator、聚焦測試與 release builder。
- `07_gui_prototype/`：靜態 fallback 畫面與即時 GUI render layer。

## 文件入口

- GUI live bridge：`01_content/gui-runtime-bridge-plan-v1.md`
- GUI 靜態現況：`01_content/gui-static-current-state-v1.md`
- 發行資產契約：`01_content/release-asset-policy-v1.md`
- Windows portable 契約：`01_content/windows-portable-release-v1.md`
- 現行資產清單：`01_content/asset-production-inventory-v0.1.md`
- 歷史 handoff、已結案決策與驗證紀錄：`01_content/archive/`
- 尚未核准的未來設計：`01_content/blueprints/`

## 固定邊界

- 不得把 HTML fixture、JavaScript、portable launcher 或 release output 視為
  遊戲規則 SSOT，也不得將 Python 遊戲規則複製到這些層。
- 平衡已封存。只有可重現、影響正常通關或職業遊玩體驗的問題，才可進行最小維護修正。
- 成長數值 SSOT 是 `04_data/data/jobs.py`。Warrior 是固定例外，每級 13.50 點
  （`attack = 1.5`）；Mage、Rogue 與 Cleric 均為 15.00。
- 不主動擴充儲存容量、設施、職業、存檔、獎勵、解鎖或遊戲內容範圍；為處理使用者
  回饋而需要的目標性資產替換或調整，則可直接進行。
- GUI bridge 與工具仍透過 `game.*` 匯入時，必須保留 `game.py` 的相容性 re-export。
- 維護期間依使用者回饋與可重現問題選擇聚焦修正。未來如要正式發行或提升分支，需
  另行取得 Owner 批准並訂定驗收標準。
