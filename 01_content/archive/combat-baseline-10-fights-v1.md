# 五區域十情境戰鬥基準 v1

S10 是獨立、stdout-only 的平衡量測層。它不修改怪物、角色成長、技能、
裝備、聖物、存檔或 GUI；既有 B4 仍是目前遊戲基線。

## 測量範圍

每個區域有兩個情境：入口的代表普通怪，以及終盤 Boss。每個情境使用四
職業與五個固定種子，總計 `10 × 4 × 5 = 200` 筆記錄。

| 測點 | 裝備／聖物時點 | 補給 | 共同目標 |
|---|---|---|---|
| 入口普通怪 | Fire 使用起始配置；其餘區域使用前一區終盤裝備與已取得聖物 | 不攜帶 | 3–5 玩家行動 |
| 終盤 Boss | 使用本區 Boss 前可取得的後期裝備與聖物 | 五格 Boss 標準補給 | 10–15 玩家行動 |

所有職業都採用同一個目標區間；勝利且行動數位於區間內才算該筆通過。
這是共同節奏目標，並不取代 B4 原有的職業差異化診斷。

## S10 配置與可選項

- 機器可讀 SSOT：[s10_baseline_config.py](../06_tools/s10_baseline_config.py)
- 人工審閱與挑選表：[s10-baseline-selection-v1.md](s10-baseline-selection-v1.md)

配置目前以 B4 的各職業區域裝備與聖物選項為預設。若要調整，僅在
`S10_SCENARIOS` 對應情境的 `loadout_overrides[job]` 填入既有裝備 ID；
S10 驗證會拒絕不相容槽位、職業不相容裝備、Boss 後裝備時點與非法補給。

Boss 標準補給固定為：續航 HP 中藥水 ×1、緊急 HP 中藥水 ×1、MP 集中滴
露 ×1、投擲破甲釘 ×1、逃脫不攜帶。量測必經 `configure_run_supplies`，不
會以一般背包數量繞過五格規則。

## 執行

```powershell
# 200 筆情境／職業／種子紀錄
& '<bundled-python>' 06_tools/test_combat_balance.py --s10 --format csv

# 40 筆情境／職業摘要：五種子範圍、中位數與通過結果
& '<bundled-python>' 06_tools/test_combat_balance.py --s10-summary --format csv
```

兩個入口只輸出到標準輸出，不建立 repository artifact。首次完整 S10 結果
僅用於定位差距；任何數值調整須另以小範圍決策進行。
