# Element Maze 封版維護收斂 v1

日期：2026-07-27

用途：記錄封版後可維護性、資料契約、驗證方式與剩餘風險。runtime data 仍以 `04_data/data/` 為 SSOT；本文件不取代程式資料表。

## 1. 封版範圍

- 已完成範圍：Fire、Ice、Earth、Thunder、Final 五區主線，四個核心職業、正式轉職、四元素封印、最終 Boss、Python CLI 主體；GUI 保留 static prototype，部分畫面已有既定 live bridge。
- 不做事項：不新增 gameplay、任務、設施、職業、資產或 GUI bridge；不開容量升級；不改存檔格式；不因報表數字不漂亮而改職業、怪物、補給或裝備數值；不先拆高風險的 `combat.py`。
- 平衡狀態：已封版。只有可重現、且影響正常通關或職業體驗的玩家問題，才可另開最小維護修正；回合數、耗材、品質比較與傷害比例一律只是診斷證據。
- S10 最終量測維持 40 情境、200/200 勝利，全部 Boss 都在 10--15 回合。普通怪保留既有診斷：Fire Rogue 2/3/3、Ice Rogue 5/5/6、Thunder Rogue 6/6/6、Thunder Cleric 5/6/6、Final Cleric 8/8/8；這些數字不授權重新調整平衡。

## 2. 現行玩家契約

### 四職業與轉職

- 核心職業是劍士、法師、盜賊、牧師。
- `04_data/data/promotions.py` 目前有八條 `formal` 轉職路線，每個核心職業兩條；共同門檻是完成 `quest_ice_return_handoff` 且達 Lv18。轉職技能與效果由 data、engine 與 `06_tools/test_promotion_contracts.py` 共同驗證。
- 職業成長 SSOT 是 `04_data/data/jobs.py` 的 `growth_points`；細節與節點表在 `01_content/proposed-job-growth-points-v1.md`。

### 出發補給

- 共用 state contract 定義五格：續航 HP、緊急 HP、MP、投擲、逃脫。未使用物品留在一般背包，只有實際使用才扣除。
- live GUI 的世界地圖出發整備會把五格 payload 交給 Python `configure_run_supplies()` 驗證；遊戲規則不由 JavaScript 決定。
- CLI 目前的 `configure_cli_run_supplies()` 只提供前四格，未提供逃脫格選擇；這是已知 CLI/live GUI 對齊風險，不在本次文件收斂中擴功能修正。

### 倉庫 live GUI

- 解鎖費用 500G；容量是 10 種非關鍵物品，而不是 10 個物品。
- 已有解鎖、存入、取出；重複種類可繼續存入，關鍵物品不可存入。
- 容量升級沒有開放，也不列為封版前待辦。

### 怪物種族與 live combat GUI

- 六種族資料與特性規則以 `04_data/data/monsters.py` 的 `MONSTER_RACE_RULES` 為 SSOT；`game.py` 是真實戰鬥 consumer，前端不重建種族規則。
- live combat ScreenModel 明確提供敵人種族顯示名稱、特性顯示名稱與可讀狀態；構裝／靈體的一次性直接傷害護盾顯示「剩餘 1 次／0 次」，其餘一次性特性顯示「待機／已觸發」。
- Combat Screen 只渲染 ScreenModel。舊 static fixtures 未提供種族／特性欄位時，仍維持既有屬性／狀態 fallback，不會成為 gameplay SSOT。

## 3. 劍士 13.50 點例外

最終決定：劍士 `growth_points.attack = 1.5`，每級總和 13.50 點，是刻意的職業例外，不是文件或資料漏填。不得為了讓 uniform validator 通過而補回 3.0，也不得以此為理由調整其他職業或怪物。

同步方式：

- `04_data/data/jobs.py` 保留劍士 1.5；不改 gameplay 數值。
- `06_tools/validate_data.py` 使用逐職業封版總額：劍士 13.50，法師／盜賊／牧師各 15.00；未知職業沒有封版總額時直接報錯。
- `06_tools/test_job_growth_points.py` 驗證同一組逐職業總額與里程碑除以 3 的公式。
- `01_content/proposed-job-growth-points-v1.md` 的總額、里程碑與 Warrior 節點表同步為 13.50 點版本。

## 4. `game.py` / `dungeon.py` read-only 結論

### Live code 判定

原先交接假設「下一步才抽出 `dungeon.py`」，但 live repository 顯示抽取已在既有歷史中完成：`03_engine/engine/dungeon.py` 已存在，`game.py` 已從該模組匯入並 re-export 迷宮 API。因此本次不再搬程式；以下是現況稽核與後續邊界。

### 迷宮域函式與進入點

| 責任 | 現行函式 | 主要進入點 |
|---|---|---|
| 選單與顯示 | `dungeon_menu`、`dungeon_option_line`、`dungeon_gate_hint`、`dungeon_boss_status`、`recommended_level_note`、`run_loot_summary` | `game.main_loop()`；GUI model 經 `game.*` re-export |
| 出發整備 | `configure_cli_run_supplies` | CLI `dungeon_menu()`；live GUI 直接呼叫共用 state helper |
| 探索循環 | `explore_dungeon`、`choose_weighted_event` | CLI `dungeon_menu()` |
| 加權事件 | `dungeon_material_event`、`dungeon_treasure_event`、`dungeon_trap_event`、`dungeon_special_event` | CLI `explore_dungeon()` |
| Boss gate / clear handoff | `record_boss_glen_sighting`、`boss_available_at_dungeon_end`、`boss_challenge_prompt`、`clear_dungeon_boss` | CLI 探索；`gui_exploration_model.py`、`gui_actions.py` 經 `game.*` |
| 敗北與結局 | `handle_defeat`、`complete_final_quest_from_boss`、`show_main_story_ending` | CLI 探索／戰鬥結算；Boss clear handoff |

### 依賴與 state mutation

- Data：`DUNGEONS`、`MONSTERS`、`EVENT_WEIGHTS`、`QUESTS`、`EQUIPMENT` 與 dialogue `say()`。
- 共用規則：`state.py` 的 unlock、quest、stats、補給、loot、gold、裝備品質與 inventory helpers；`cli_helpers.py` 的 treasure／trap／special／Boss clear config；`facilities.py` 的 Glen／主線 flags 與 `next_step_hint()`。
- CLI：`display.py` 的 panel、menu、pause；`formatting.py` 的物品顯示。
- Combat seam：`explore_dungeon()` 以函式內 lazy import 呼叫 `game.combat()`，避免模組載入時的循環失敗。這是現有相依，不在本次改成 `combat.py`。
- 直接或 helper-based mutation 包含：`run_supplies`、`current_hp/current_mp`、背包與本趟 loot／gold、`cleared_dungeons`、`guild_points`、Boss／主線 flags、unlock、品質裝備 instance、完成任務、`_ending_pending` 與 `_return_to_title`。

### CLI / GUI bridge 相容邊界

- `game.py` 保持 CLI lifecycle 與 high-level orchestrator；迷宮函式由 `dungeon.py` 擁有。
- 現有 `game.py` re-export 必須保留，直到 `gui_actions.py`、`gui_exploration_model.py` 與工具的 `game.*` 相依在另一個明確 slice 中完成遷移與 bridge smoke。
- live GUI 自己維護 session exploration step 與事件結算，只共用部分 Python helper；不能假設 CLI `explore_dungeon()` 是 GUI 的直接執行路徑。任何未來修改都要防止兩條流程語意漂移。
- 抽取或清理時不得改文字、亂數權重、獎勵、Boss gate、敗北損失、補給、存檔 shape 或 GUI action／ScreenModel 行為。

### Gate 結論

`game.py → dungeon.py` 的主要抽取已落地，本次沒有新的解耦 implementation 可執行，也沒有批准 `combat.py`。若要再做維護，只應另批一個精確 hardening slice，例如補 bridge/re-export 契約測試或處理 CLI/live GUI 探索漂移；不要重複搬移同一批函式。

本次稽核另發現 `handle_defeat()` 缺少 `is_key_item` 與 `EQUIPMENT` import，可在一般敗北且本趟有物品時重現 `NameError`。這符合「有證據才修」規則，已用最小 import 修正，沒有改敗北公式或資料。

## 5. 封版驗證清單

不要使用目前損壞的 `.venv`。PowerShell 共用執行器：

```powershell
$mazePython = 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
```

| 分類 | 指令／方法 | 判定範圍 |
|---|---|---|
| 阻擋型 | `& $mazePython 06_tools\validate_data.py` | data cross-table contract；逐職業成長總額包含劍士 13.50 例外 |
| 阻擋型 | `& $mazePython element_maze.py --smoke-test` | 主程式 import、基礎流程與既有 smoke contract |
| 阻擋型 | `& $mazePython 06_tools\test_job_growth_points.py` | 成長表、節點公式、敏捷傷害 contract |
| 阻擋型 | `& $mazePython 06_tools\test_promotion_contracts.py` | 八條正式轉職的資料／engine contract |
| 阻擋型 | `& $mazePython 06_tools\test_dungeon_defeat_contract.py` | 一般敗北的金幣／loot 損失與 HP／MP 回城回復；覆蓋缺 import 回歸 |
| 阻擋型 | `& $mazePython 06_tools\smoke_test_combat_bridge.py` | CLI/live GUI 戰鬥 bridge contract |
| 阻擋型（GUI render） | `node 06_tools\test_combat_gui_render.mjs` 與 `node --check 07_gui_prototype\combat_screen\combat-screen.js` | live race/trait meta mapping、舊 fixture fallback 與 JavaScript syntax |
| 阻擋型（工具契約） | `& $mazePython 06_tools\test_combat_balance_report.py` | 報表欄位、配對、重現性與工具可執行性；報表數值仍是診斷，不是平衡 gate |
| 診斷型 | `& $mazePython 06_tools\test_combat_balance.py --phase0` | 回合數、耗材、品質比較、傷害比例；成功執行與輸出可留存，但數值不得自行觸發調整 |
| 阻擋型（GUI 有改時） | 讀 `.codex/skills/element-maze-gui-static-prototype/SKILL.md`，以 localhost `?mode=live` 驗證 live 畫面與不帶 mode 的 static fixture | 不使用 `file://`；runtime bridge 仍由 Python 掌握 gameplay |
| 阻擋型 | `git diff --check` | whitespace／patch integrity |

本次實際結果：

- Data validation：通過；撤回 Warrior 3.0 後的原始基線曾只報 15 點總額錯誤，改成逐職業封版契約後輸出 `data validation ok`。
- Main smoke：通過，輸出 `smoke test ok`。
- Growth／promotion／defeat regression：全部通過。
- Combat bridge：通過，輸出 `Combat Bridge Boss Rule Parity smoke test passed.`；新增 regression 證明構裝護盾在真實 live 普攻後由「剩餘 1 次」更新為「剩餘 0 次」。
- Combat GUI render：Node regression 與 JavaScript syntax checks 通過；Playwright 以 `?mode=live` 實測種族／特性／護盾次數隨攻擊更新，並以不帶 mode 的頁面確認舊 fixture fallback。唯一 console error 是既有 `favicon.ico` 404，與本次模組及 render 無關。
- Balance report contract：通過，明示 `no balance verdict`。
- Phase 0 diagnostics：exit 0；只確認工具可執行，不以 1,901 行 CSV 的數值開平衡。
- 額外嘗試的既有 `06_tools/test_supply_quality_v1.py` 在到達本次敗北回歸前，就因舊 `item_potion_m` migration 假設找不到 `item_potion_s` 而失敗。本次未修改該補給／save contract；此漂移列入剩餘風險，不宣稱整個 repository 全綠。

## 6. 使用工具與文件路由

- 使用工具：`git status`／`git diff`（唯讀工作區稽核）、`rg`（函式與 consumer 盤點）、指定 Python runtime（驗證）、`apply_patch`（最小文件／contract 修正）。
- 穩定入口：`README.md`。
- 短交接：`01_content/codex-handoff-short.md`。
- 本次封版結論與詳細清單：本文件。
- 成長數值決定：`01_content/proposed-job-growth-points-v1.md`。
- 歷史拆分方向：`01_content/archive/task.md`、`01_content/archive/game-architecture.md`，只供背景，不是現行批准。

## 7. 剩餘風險

- 工作區仍含 engine、data、tools、Temple GUI 與量測文件的既有未提交 WIP；本次沒有 stage、commit、push 或重設。
- `dungeon.py` 對 `game.combat()` 的 lazy import 與 `game.py` re-export 是有意保留的相容 seam，但仍增加循環相依與測試理解成本。
- live GUI 探索流程與 CLI 探索循環不是同一執行路徑；Boss helper 已共用，但加權事件與 step orchestration 仍可能漂移。
- CLI 出發整備沒有逃脫格，和五格 state/live GUI contract 不完全一致；本次不擴補給功能。
- `06_tools/test_supply_quality_v1.py` 的舊補給 migration 假設與 live state 不一致；需先釐清舊存檔相容需求，不能為了讓測試變綠而猜測 migration 規則。
- 現有 smoke 不是五區、四職業的完整人工通關；未來只有真實玩家問題可觸發針對性重現與修正。
- balance 工具能證明報表契約與重現性，不能證明所有數值「正確」或授權新一輪平衡。
