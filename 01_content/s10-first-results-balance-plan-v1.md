# S10 首次結果平衡數據規劃 v1

目的：把 S10 `entry/endgame` 的第一次 200 筆結果轉為可執行、可驗收的窄範圍資料調整順序。本文件是規劃與決策記錄，不授權直接修改 runtime、怪物、角色、技能、裝備、聖物或存檔資料。

## 決策與邊界

- B4 仍是既有遊戲基線與職業差異診斷；S10 是跨五區共同節奏比較層。S10 未通過不等同於 B4 失效，也不等同於批准調整任何數值。
- S10 SSOT 維持 `06_tools/s10_baseline_config.py`。十個情境、五個固定種子、stdout-only，以及 Boss `configure_run_supplies` 的五格規則均不改變。
- 共同節奏門檻只判斷「五種子全部勝利，且每筆玩家行動都在範圍內」：普通怪 3–5、Boss 10–15。
- 下列「差距」以中位數減去目標下限表示；負值代表偏短。範圍一律是五種子的 min/median/max。

## 首次量測快照

執行日期：2026-07-22。指令：

```powershell
C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe 06_tools/test_combat_balance.py --s10 --format csv
C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe 06_tools/test_combat_balance.py --s10-summary --format csv
```

共 200/200 勝利；40 個「情境 × 職業」格中，6 格符合共同節奏：五區入口的 Cleric 與 Final Boss 的 Cleric。其餘 34 格皆因過短未達標，沒有敗北或超過上限的格子。

縮寫：`W` Warrior、`M` Mage、`R` Rogue、`C` Cleric；每格為 `min/median/max（差距）`。

| 區域／測點／代表敵人 | 共同目標 | W | M | R | C | 判定與主要偏差 |
|---|---:|---:|---:|---:|---:|---|
| Fire entry / `mon_ember_stalker` | 3–5 | 2/2/2 (-1) | 1/1/1 (-2) | 1/1/2 (-2) | 3/3/3 (0) | 普通怪過短；Mage/Rogue 特別短 |
| Fire endgame / `boss_cinder_seal_sentinel` | 10–15 | 4/5/5 (-5) | 3/4/4 (-6) | 6/6/6 (-4) | 8/9/9 (-1) | Boss 過短；W/M/R 特別短 |
| Ice entry / `mon_ice_outer_guard` | 3–5 | 2/2/2 (-1) | 1/2/2 (-1) | 2/2/2 (-1) | 3/3/3 (0) | 普通怪過短 |
| Ice endgame / `boss_ice_final_seal_lord` | 10–15 | 4/4/4 (-6) | 3/4/4 (-6) | 4/5/6 (-5) | 7/8/8 (-2) | Boss 過短；W/M 特別短 |
| Earth entry / `mon_earth_leyline_guard` | 3–5 | 2/2/2 (-1) | 1/1/1 (-2) | 1/2/2 (-1) | 3/3/3 (0) | 普通怪過短；Mage/Rogue 特別短 |
| Earth endgame / `boss_earth_deep_leyline_lord` | 10–15 | 4/4/4 (-6) | 2/3/3 (-7) | 3/3/3 (-7) | 7/7/7 (-3) | Boss 過短；M/R 特別短 |
| Thunder entry / `mon_thunder_array_guard` | 3–5 | 2/2/2 (-1) | 1/1/1 (-2) | 2/2/3 (-1) | 3/3/3 (0) | 普通怪過短；Mage 特別短 |
| Thunder endgame / `boss_thunder_crown_storm_lord` | 10–15 | 3/4/4 (-6) | 2/2/2 (-8) | 2/2/2 (-8) | 6/6/6 (-4) | 最嚴重 Boss 過短；M/R 特別短 |
| Final entry / `mon_final_core_guard` | 3–5 | 2/2/2 (-1) | 1/1/1 (-2) | 1/2/2 (-1) | 4/4/4 (0) | 普通怪過短；Mage/Rogue 特別短 |
| Final endgame / `boss_final_demon_king` | 10–15 | 4/4/4 (-6) | 2/3/3 (-7) | 3/3/4 (-7) | 10/10/10 (0) | Boss 過短；M/R 特別短 |

## 補給與量測解讀

所有 Boss 情境均配置同一五格 `boss_standard`：兩格 HP、MP、戰術投擲、逃跑（空）。`configure_run_supplies` 已在 S10 建置與設定驗證時呼叫。

- HP 補給與 MP 補給：20 個 Boss × 5 種子均為 0 次使用。
- 戰術投擲：僅 Cleric 在 Earth、Thunder、Final Boss 各 5/5 次使用；其餘職業與 Fire/Ice Cleric 均為 0 次。
- 因此「補給未實際使用」是結果的一部分：多數 Boss 在策略到達補給條件之前已結束。不得以增加補給數量、強度或改動五格規則來修正本次短戰鬥。
- 現有 S10 CSV 不輸出 item-use 欄位；本次以同一 S10 參數從量測回傳值讀取使用計數。後續若需把補給採用率作為正式 gate，應先另立 stdout-only 的小型報表欄位規劃，不能在本數值 slice 夾帶調整。

## 共同節奏與 B4 職業診斷：必須分開

S10 的共同門檻刻意對四職業相同：它回答「這個入口代表怪／本區 Boss 是否提供足以形成基本戰鬥節奏的長度」。它不要求四職業的行動數相同，也不能單靠行動數判斷職業強弱。

B4 則保留角色身分與角色差異的診斷用途：Warrior 的蓄力爆發、Mage 的元素爆發、Rogue 的持續物理／狀態輸出、Cleric 的長戰鬥 DoT、再生與道具。後續每個 S10 slice 都必須同時重跑 B4 報告，但 B4 只做護欄：不可引入新失敗、不可消除既有職業機制、不可把角色差異強制壓成同一行動數。除非獨立 read-only 規劃證明怪物窄調無法達標，禁止把 S10 偏短轉成職業成長、技能、裝備或聖物調整。

## 偏差分類與優先順序

| 優先 | 範圍 | 主要偏差 | 可接受的候選調整面 | 這一階段不做 |
|---:|---|---|---|---|
| P0 | Thunder Boss | 全職業 Boss 過短，M/R -8 | 單一 Boss 資料列的 HP、物防、魔防；每次只測一個候選組合 | 補給、職業、技能、聖物、Boss 行為 |
| P0 | Earth、Final Boss | Boss 過短，M/R -7 | 各自單一 Boss 資料列的 HP、物防、魔防 | 跨區共用公式或全域倍率 |
| P1 | Fire、Ice Boss | Boss 過短，且 Fire Cleric 僅 -1 | 各自單一 Boss 資料列的 HP、物防、魔防 | 以 Cleric 為理由削弱其 DoT／再生 |
| P1 | 五區入口普通怪 | 普通怪整體過短，Mage 常 -2 | 各自單一代表普通怪資料列的 HP、物防、魔防 | 更換 S10 代表敵人、調整前區裝備或聖物時序 |
| P2 | 補給採用率可觀測性 | 配置存在但多數未使用；不是數值失衡本身 | 先規劃 stdout-only 報表延伸，納入各類 item use | 更改 `boss_standard`、五格規則或策略閾值 |

P0 表示影響最大，但不要求跨區合併實作。為降低混雜因素，實際執行順序以下一節的 Fire 校準 slice 為起點；它成功後才以同一方法處理 P0 的嚴重 Boss。

## 第一個可執行的窄範圍 balance slice

**選定 slice：Fire endgame 的 `boss_cinder_seal_sentinel`，只做此 Boss 資料列的 HP／物理防禦／魔法防禦候選網格，最後只落地一組。**

選擇理由：它不含前置聖物、情境最單純；四職業全勝但全數低於 Boss 節奏，且補給完全未被使用；同時 Cleric 僅差一回合，能及早暴露「只加 HP」是否會壓壞角色差異。此 slice 不修改 S10 config、敵人技能／行為、玩家端資料或任何跨區共用值。

執行決策：

1. 先記錄此 Boss 現行 HP、defense、magic_defense；只在工作副本做小步候選網格（每個欄位相對現值不超過 10%，最多三輪）。
2. 先測 HP-only；若 W/M/R 仍未同時進入 10–15，再測 HP + 單一相應防禦欄位。不得同時以傷害、攻擊、行為、狀態或補給補償。
3. 每個候選完整重跑 S10 與 B4；只保留第一個通過下列 S10 gate 且 B4 沒有新失敗的候選。若三輪沒有候選，停止，不擴張範圍，產出 read-only 原因記錄後請求新的決策。

### Fire slice 的 S10 驗收條件

- `--s10 --format csv` 的 Fire endgame 20 筆全部 victory，且每筆 player_actions 在 10–15。
- `--s10-summary --format csv` 的 Fire endgame 四職業皆 `target_met=True`；其餘九個 S10 情境不得由此 slice 變差（它們的資料不應被觸及）。
- Boss supply profile 仍為 `boss_standard`，五格結構與 `configure_run_supplies` 呼叫不變。
- B4 既有測試／報告中沒有新增失敗；不以讓四職業同回合數作為條件。
- `git diff --check` 無空白錯誤，且 diff 只涉及批准的單一 Boss 資料列（實作時）與必要的測試快照／規劃紀錄。

## 後續 slice 的固定驗收模板

每次只處理一個代表敵人資料列。普通怪 slice 的 gate 是四職業五種子全勝且 3–5；Boss slice 是 10–15。除此之外，每次都必須：保留 S10 SSOT 與五格補給規則、重跑 B4 護欄、保留所有不在 slice 內的資料列、並用 `git diff --check` 確認範圍。

## 明確不調整項目

- runtime、戰鬥公式、敵人 AI／行為、`configure_run_supplies` 與 S10 stdout-only 行為。
- 角色基礎／成長／每三級成長、轉職、技能與 MP 成本、裝備與詞綴、Rogue 偽副手、聖物被動。
- HP／耐力跨系統重做、戰中換裝、GUI、bridge、存檔／schema。
- S10 情境代表敵人、前區裝備／已取得聖物時序、固定種子、共同目標或 Boss 五格補給規則。

本文件本身不改動任何 runtime 或遊戲資料，也不構成提交 Git 的要求。
