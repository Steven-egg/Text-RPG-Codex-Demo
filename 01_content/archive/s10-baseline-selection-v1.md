# S10 入口／終盤基準選擇表 v1

這是 `06_tools/s10_baseline_config.py` 的可讀審閱表。Python 設定是量測
SSOT；要覆寫裝備時，在對應情境的 `loadout_overrides[job]` 填入既有裝備
ID，然後執行 S10 驗證。此表不代表世界地圖換裝功能。

## 固定規則

| 項目 | 設定 |
|---|---|
| 職業 | 戰士、法師、盜賊、牧師全部測量 |
| 種子 | `20260712`、`20260713`、`20260714`、`20260715`、`20260716` |
| 行動策略 | B4 `canonical_v2` 固定輪替與既有補給門檻 |
| 普通怪目標 | 3–5 玩家行動；不攜帶補給 |
| Boss 目標 | 10–15 玩家行動；固定 Boss 補給 |
| Boss 補給 | 續航 HP：中藥水 ×1；緊急 HP：中藥水 ×1；MP：集中滴露 ×1；投擲：破甲釘 ×1；逃脫：不攜帶 |

## 十個情境

| 配置 ID 尾碼 | 區域／測點 | 敵人 ID | 等級 | 裝備來源 | 聖物數量 | 補給 |
|---|---|---|---:|---|---:|---|
| `fire:entry` | Fire 入口普通怪 | `mon_ember_stalker` | 10 | Fire 起始／B4 Fire | 0 | 無 |
| `fire:endgame` | Fire 終盤 Boss | `boss_cinder_seal_sentinel` | 10 | Fire Boss 前／B4 Fire | 0 | Boss 標準 |
| `ice:entry` | Ice 入口普通怪 | `mon_ice_outer_guard` | 18 | Fire 終盤／B4 Fire | 0 | 無 |
| `ice:endgame` | Ice 終盤 Boss | `boss_ice_final_seal_lord` | 18 | Ice Boss 前／B4 Ice | 1 | Boss 標準 |
| `earth:entry` | Earth 入口普通怪 | `mon_earth_leyline_guard` | 25 | Ice 終盤／B4 Ice | 1 | 無 |
| `earth:endgame` | Earth 終盤 Boss | `boss_earth_deep_leyline_lord` | 25 | Earth Boss 前／B4 Earth | 2 | Boss 標準 |
| `thunder:entry` | Thunder 入口普通怪 | `mon_thunder_array_guard` | 32 | Earth 終盤／B4 Earth | 2 | 無 |
| `thunder:endgame` | Thunder 終盤 Boss | `boss_thunder_crown_storm_lord` | 32 | Thunder Boss 前／B4 Thunder | 3 | Boss 標準 |
| `final:entry` | Final 入口普通怪 | `mon_final_core_guard` | 40 | Thunder 終盤／B4 Thunder | 3 | 無 |
| `final:endgame` | Final 終盤 Boss | `boss_final_demon_king` | 40 | Final Boss 前／B4 Final | 4 | Boss 標準 |

## 執行

```powershell
& '<bundled-python>' 06_tools/test_combat_balance.py --s10 --format csv

# 每個情境／職業的五種子範圍與中位數
& '<bundled-python>' 06_tools/test_combat_balance.py --s10-summary --format csv
```

輸出只寫到標準輸出；每筆包含配置 ID、職業、種子、回合數、勝敗與目標
判定。所有數值調整都必須等待這份首次完整結果後另行決定。
