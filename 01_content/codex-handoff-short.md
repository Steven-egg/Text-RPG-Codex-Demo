# Codex Handoff Short

- `README.md` 是 project-level SSOT；專案採分層 SSOT，不是所有細節都塞在 README。
- 目前版本：Python CLI v1 playable vertical slice，可玩核心循環已完成；第二幕 Act 2 Slice 1 已進 runtime data。
- 目前專案階段：v1 第一幕完成，第二幕進入最小施工切片迭代與 read-only 數值檢查準備。
- 目前已新增幕次總綱：`01_content/full-act-structure.md`。
- 目前已新增第二幕規劃：`01_content/act-2-content-plan.md`。
- 第二幕目前已完成 Act 2 Slice 1：灰燼裂谷偵查版已進 runtime data。
- 完成 `quest_boss_glen` 後會解鎖 `second_act_preview`、`unlock_act_2`、`unlock_ash_ravine`。
- 已新增 `dungeon_ash_ravine`、3 個普通怪、3 個素材與最小偵查任務「灰燼裂谷偵查」。
- Act 2 Entry Balance & Guidance Patch 已完成：葛倫小幅降壓、小魔晶掉落率提高、破甲釘新增即時傷害、灰燼裂谷改為 18 步、完成血跡地圖後會引導玩家接「灰燼裂谷偵查」。
- 灰燼裂谷普通怪 HP 平衡 MVP 已完成：`mon_ash_imp` 92 -> 104、`mon_lava_bat` 84 -> 96、`mon_cinder_soldier` 118 -> 132；本機 `run_checks.bat` 已通過。
- Lv7 → Lv8 盜賊實測確認目前灰燼裂谷難度合理；暫不建議繼續提高 HP，也不建議修改 combat formula、EXP/gold、升級全回復或新增怪物技能。
- 集中藥袋 special 裝備語意 bug 已修正：只有 `state["equipment"].get("special") == "special_focus_pouch"` 時，進入迷宮才會取得集中滴露並顯示訊息。
- 工會收購 MVP、倉庫 MVP、怪物圖鑑 MVP、轉職 preview-only MVP、聖物 preview-only MVP、職業特化 preview-only MVP 皆已完成。
- 盜賊 head-slot 副武器 data-only MVP 已完成：新增 `armor_rogue_sleeve_blade`（影袖副刃），使用既有 `head` slot 與 `attack`、`agility`、`crit`，未新增 `offhand`。
- 副武器效果下一步優先做分類設計：魔法類型偏元素持續傷害，物理效果類型偏流血、破甲、標記、中毒；目前不直接做 combat 實作或職業特化。
- 新增 `01_content/combat-growth-layering-plan.md`：本輪確認「職業玩法定位先行，屬性系統暫緩」，火/冰只作為局部特色，不新增八元素、完整屬性克制或精神屬性。
- `03_engine/engine/` 目前已包含 `game.py`、`display.py`、`formatting.py`、`bestiary.py`、`previews.py`；不建議繼續為拆而拆。
- 灰燼裂谷目前沒有 Boss，`boss` 為 `None`。
- 灰燼守衛、完整火之印記、第二幕完整任務鏈、正式轉職系統、聖物取得狀態與效果、正式職業特化選擇與效果仍未實作。
- 目前已有暖石墜改與抗火斗篷兩件火抗裝備；不要再把餘燼護符或新火抗 accessory 當主要下一步，避免裝備定位重疊。
- 下一步若要繼續評估灰燼裂谷，建議改測法師、劍士、牧師或不同裝備狀態；不要直接繼續調 HP 或施工。
- 不得實作整個第二幕。
- 不得新增 `offhand` slot。
- 不得修改 combat formula，不得修改敏捷、暴擊、命中、閃避等戰鬥規則。
- 不得修改 save/state。
- 不得修改 `02_schema/*.schema.md`，除非先提出理由與最小修改範圍並獲得明確要求。
- 不得修改 `04_data/data/*.py`，除非進入已批准的最小施工切片；文件同步輪不得修改 runtime data。
- 不得修改 `03_engine/engine/*.py`，除非使用者明確要求且範圍極小。
- 不得修改 `04_data/data/registry.py` 或 `06_tools/validate_data.py`，除非進入明確批准的 registry/validation 準備切片。
- 不得新增 `01_content/act-3-content-plan.md`。
- 不得新增 act-3 runtime 內容。
- 不得處理 Element Decay。
- 不得新增火抗配方，不得把 Python dict 遷移到 JSON/YAML，不得把 `save.json` 當資料來源。

Drift check 可回貼：

```text
目前專案是《元素迷宮：邊境冒險者》Python CLI v1 playable vertical slice。README.md 是 project-level SSOT；01_content 是內容與架構規劃；full-act-structure.md 是五幕總綱；act-2-content-plan.md 是第二幕灰燼裂谷規劃；combat-growth-layering-plan.md 記錄「職業玩法定位先行，屬性系統暫緩」。02_schema 是資料契約；04_data/data 是 runtime data；registry.py 是資料索引與 unlock/helper；06_tools/validate_data.py 做跨表引用驗證；03_engine/engine 目前包含 game.py、display.py、formatting.py、bestiary.py、previews.py。v1 第一幕已完成且主線可通關；第二幕 Act 2 Slice 1 已完成，灰燼裂谷偵查版已進 runtime data，完成 quest_boss_glen 後會解鎖 unlock_act_2 與 unlock_ash_ravine，並可接「灰燼裂谷偵查」。入口平衡補丁、灰燼裂谷普通怪 HP 平衡 MVP、集中藥袋 special 裝備語意修正、工會收購 MVP、倉庫 MVP、倉庫入口 UX 修正、怪物圖鑑 MVP、轉職 preview-only MVP、聖物 preview-only MVP、職業特化 preview-only MVP 與盜賊 head-slot 副武器 data-only MVP 皆已完成。灰燼裂谷 Lv7 → Lv8 盜賊實測確認目前難度合理；暫不建議繼續提高 HP，也不建議修改 combat formula、EXP/gold、升級全回復或新增怪物技能。轉職、聖物與職業特化目前皆為 preview-only，未新增正式狀態或效果。火、冰目前只作為局部特色，不新增八元素、完整屬性克制、完整抗性表或精神屬性。盜賊副武器使用既有 head slot，未新增 offhand。副武器效果下一步優先維持分類設計：魔法類型偏元素持續傷害，物理效果類型偏流血、破甲、標記、中毒；目前不直接做 combat 實作或職業特化。灰燼裂谷目前沒有 Boss；灰燼守衛、完整火之印記、第二幕完整任務鏈、正式轉職、正式聖物、正式職業特化仍未實作。下一輪適合回到盜賊影袖副刃普通攻擊追擊最小 MVP，但不得新增 offhand、精神屬性、完整特化、完整轉職、完整聖物或大改 combat formula。
```

新 session 建議優先讀：

1. `01_content/codex-handoff-short.md`
2. `README.md`
3. `01_content/codex-session-snapshot.md`
4. `01_content/full-act-structure.md`
5. `01_content/act-2-content-plan.md`
6. `01_content/combat-growth-layering-plan.md`
7. `01_content/game-architecture.md`
8. `01_content/game-design.md`
9. 需要施工前評估時，再讀 `02_schema/`、`04_data/data/registry.py`、`06_tools/validate_data.py`
