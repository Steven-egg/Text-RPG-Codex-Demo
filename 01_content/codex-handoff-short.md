# Codex Handoff Short

## 最新 handoff：燼印深窟 Boss / 第 3 碎片 read-only plan

- 本輪只做文件同步；不改 runtime / engine / data / schema / save/state。
- `dungeon_cinder_seal_depths`「燼印深窟」skeleton 已進 runtime，並由使用者人工測試通過。
- 目前 `dungeon_cinder_seal_depths["boss"]` 仍為 `None`。
- 燼印深窟由 `quest_supply_upgrade` 完成後解鎖，`unlock` 直接使用 `dungeon_cinder_seal_depths`。
- 燼印深窟目前只有兩隻普通怪：`mon_ember_stalker`、`mon_molten_shell`。
- `mon_cinder_acolyte` 暫不新增，避免引出施法、debuff 或特殊 AI。
- 第 3 枚 `key_fire_mark_shard` 尚未開放；目前火之印記碎片最多仍可取得 2 枚。

下一輪 Boss MVP 預設：
- 新 Boss id：`boss_cinder_seal_sentinel`。
- Boss 名稱：「燼印哨衛」。
- Boss 所屬地城：`dungeon_cinder_seal_depths`。
- 第 3 枚 `key_fire_mark_shard` 只由擊敗 `boss_cinder_seal_sentinel` 後取得。
- 工會不補發第 3 枚碎片，只負責提示玩家前往燼印深窟，以及 Boss 後提示玩家可去教會詢問碎片或火之印記。
- Boss gate 預設新增一個最小偵查或討伐任務，例如 `quest_cinder_depths_scout`。
- 完成該任務後，才讓燼印深窟終點可挑戰 `boss_cinder_seal_sentinel`。
- 不新增 registry story key；能用 quest completion 或既有 id 就不用新增 unlock key。
- Boss reward 預設設定 `cinder_seal_sentinel_defeated` flag、給 `key_fire_mark_shard x1`，並防重複領取。
- Boss 後只提示「可去教會詢問火之印記」，不開正式火印流程。
- Boss 行為可用單一 hardcoded Boss handler；不做通用 Boss framework。

下一輪 runtime 最小範圍預設：
- `04_data/data/monsters.py`
- `04_data/data/dungeons.py`
- `04_data/data/quests.py`
- 必要時才改 `03_engine/engine/game.py` 加入單一 Boss gate / clear handler。

明確限制：
- 不新增或實作完整火之印記。
- 不新增火印熔爐。
- 不新增火印爐衛。
- 不新增正式轉職。
- 不新增正式聖物。
- 不新增八元素。
- 不新增完整屬性克制。
- 不新增通用 Boss framework。
- 不改 save/schema。
- 不改 combat formula。
- 不新增 Act 3 規劃文件。

## 最新 handoff：補給藥水升級任務 MVP 已完成

- 本輪已完成 `quest_supply_upgrade`「補給線升級」。
- 新增 `item_potion_m`「中藥水」，可回復 HP 70。
- 灰燼守衛擊敗後，工會會出現補給升級任務。
- 任務完成後取得 `item_potion_m x2`，並解鎖旅人小鋪販售中藥水。
- 本輪暫不實作素材交付需求；不綁定 `mat_ravine_ash`、`mat_flame_stone_refined` 或任何新材料。
- 素材交付需求待新的 dungeon / materials / monsters 系統完成後再回補。
- 本輪未修改 schema / save / state / combat formula。
- 本輪未修改 Boss AI、dungeon / monster data、materials / drops / refinement，也未新增鍊金、製藥或配方系統。

最新實機驗證：
- 火系第一章 vertical slice 已完整跑通：葛倫 Boss 戰、`血跡地圖`、`灰燼裂谷偵查`、`灰燼守衛`、`補給線升級`、中藥水解鎖。
- `quest_supply_upgrade` gate 正常：灰燼守衛未擊敗前不出現，擊敗後出現，完成後不可重複完成。
- 商店解鎖狀態正常保存；任務完成後旅人小鋪販售中藥水。
- 葛倫、灰燼裂谷怪物、灼傷、防禦下降、Boss buff/debuff、掉落、圖鑑、等級提升、首次通關獎勵正常。
- 舊道具功能正常，未被中藥水系統破壞：小藥水、集中滴露、解毒草、破甲釘、逃脫卷軸均可正常使用。
- 中藥水戰鬥中可正常使用；HP 不足時回復 70，接近滿血時不超過 max HP。

## 最新 handoff：第 3 枚火之印記碎片與燼印深窟規劃

- 本輪是 markdown-only 收尾與備份；未實作 gameplay，未修改 runtime / engine / data / schema / save/state。
- 最新方向已從「工會任務補發第 3 枚火之印記碎片」修正為「燼印深窟 + Boss 掉落」。
- 新 dungeon `dungeon_cinder_seal_depths`「燼印深窟」已完成 skeleton MVP，Boss 仍未實作。
- 已實作普通怪：`mon_ember_stalker`、`mon_molten_shell`。
- `mon_cinder_acolyte` 暫不新增，避免引出施法、debuff 或特殊 AI。
- 新 Boss 候選：`boss_cinder_seal_sentinel`，名稱「燼印哨衛」。
- 第 3 枚 `key_fire_mark_shard` 不由工會補發，而是由 `boss_cinder_seal_sentinel` 擊敗後掉落。
- 工會只負責兩段提示：灰燼守衛後提供新地點線索；燼印哨衛後提示玩家可去教會詢問碎片或火之印記。
- 暫不實作完整火之印記、火印熔爐、火印爐衛。

後續節奏暫定三個追加任務：
- 任務 A：開啟新火系 dungeon 的引子。
- 任務 B：開放進階補給藥水的引子。
- 任務 C：Boss 討伐任務兼第 3 枚火之印記碎片取得與教會引導。

補給藥水升級任務 MVP：
- 已作為燼印深窟前置節點完成；`quest_supply_upgrade` 完成後會解鎖燼印深窟 skeleton。
- 目的：讓玩家能更順地度過第二章 demo 的 Boss，同時 Boss 難度不必過度下修。
- 只做補給任務，不做鍊金系統、不做製藥系統、不新增配方系統、不修改 combat formula。

最新限制：
- 暫不新增完整火之印記、火印熔爐、火印爐衛。
- 暫不新增正式轉職、正式聖物、八元素完整系統、`offhand` slot。
- 暫不修改 schema / save/state / combat formula。
- 暫不做通用 Boss framework。
- 暫不展開完整第二幕。

- `README.md` 是 project-level SSOT；專案採分層 SSOT，不是所有細節都塞在 README。
- 目前版本：Python CLI v1 playable vertical slice，可玩核心循環已完成；第二幕 Act 2 Slice 1 已進 runtime data。
- 目前專案階段：v1 第一幕完成，第二幕進入最小施工切片迭代；灰燼守衛 Boss MVP 已完成，下一個 runtime 候選節點需先 read-only 規劃。
- 目前已新增幕次總綱：`01_content/full-act-structure.md`。
- 目前已新增第二幕規劃：`01_content/act-2-content-plan.md`。
- 第二幕目前已完成 Act 2 Slice 1：灰燼裂谷偵查版已進 runtime data。
- 完成 `quest_boss_glen` 後會解鎖 `second_act_preview`、`unlock_act_2`、`unlock_ash_ravine`。
- 已新增 `dungeon_ash_ravine`、3 個普通怪、3 個素材與最小偵查任務「灰燼裂谷偵查」。
- Act 2 Entry Balance & Guidance Patch 已完成：葛倫小幅降壓、小魔晶掉落率提高、破甲釘新增即時傷害、灰燼裂谷改為 18 步、完成血跡地圖後會引導玩家接「灰燼裂谷偵查」。
- 灰燼裂谷普通怪 HP 平衡 MVP 已完成：`mon_ash_imp` 92 -> 104、`mon_lava_bat` 84 -> 96、`mon_cinder_soldier` 118 -> 132；本機 `run_checks.bat` 已通過。
- Lv7 → Lv8 盜賊實測確認目前灰燼裂谷難度合理；暫不建議繼續提高 HP，也不建議修改 combat formula、EXP/gold、升級全回復或新增怪物技能。
- 灰燼守衛 Boss MVP 已完成：新增 `boss_ash_guardian`，`dungeon_ash_ravine["boss"]` 指向灰燼守衛，新增 `ash_guardian_defeated`。
- 灰燼守衛只在 `quest_ash_ravine_scout` 完成後於灰燼裂谷終點出現；擊敗後取得第 2 枚 `key_fire_mark_shard`，且防重複領取正常。
- 灰燼守衛 MVP 驗證已完成：本機 `run_checks.bat` 通過；手動測試確認葛倫流程未回歸、灰燼裂谷偵查 gate 正常、灰燼守衛只觸發一次、第 2 枚碎片取得正常。
- 集中藥袋 special 裝備語意 bug 已修正：只有 `state["equipment"].get("special") == "special_focus_pouch"` 時，進入迷宮才會取得集中滴露並顯示訊息。
- 工會收購 MVP、倉庫 MVP、怪物圖鑑 MVP、轉職 preview-only MVP、聖物 preview-only MVP、職業特化 preview-only MVP 皆已完成。
- 盜賊 head-slot 副武器 data-only MVP 已完成：新增 `armor_rogue_sleeve_blade`（影袖副刃），使用既有 `head` slot 與 `attack`、`agility`、`crit`，未新增 `offhand`。
- 副武器效果下一步優先做分類設計：魔法類型偏元素持續傷害，物理效果類型偏流血、破甲、標記、中毒；目前不直接做 combat 實作或職業特化。
- 新增 `01_content/combat-growth-layering-plan.md`：本輪確認「職業玩法定位先行，屬性系統暫緩」，火/冰只作為局部特色，不新增八元素、完整屬性克制或精神屬性。
- 盜賊影袖副刃普通攻擊低倍率追擊 MVP 已完成並經使用者手測成功：只影響盜賊、只限裝備 `armor_rogue_sleeve_blade`、只限普通攻擊；技能不觸發，擊殺/EXP/gold/掉落維持一次結算。
- `03_engine/engine/` 目前已包含 `game.py`、`display.py`、`formatting.py`、`bestiary.py`、`previews.py`；不建議繼續為拆而拆。
- 灰燼裂谷目前已有灰燼守衛 Boss MVP。
- 目前火之印記碎片最多可取得 2 枚；完整火之印記、火印熔爐、火印爐衛、第二幕完整任務鏈、正式轉職系統、聖物取得狀態與效果、正式職業特化選擇與效果仍未實作。
- 目前已有暖石墜改與抗火斗篷兩件火抗裝備；不要再把餘燼護符或新火抗 accessory 當主要下一步，避免裝備定位重疊。
- 下一個 runtime 候選節點應先 read-only 規劃，不要直接施工；候選方向可暫列為火印熔爐 skeleton、第 3 枚碎片來源、完整火之印記 preview/event。
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
- 下一階段建議暫停橫向擴張大型系統，改做 read-only 規劃「火之印記第一章可玩閉環 demo MVP」剩餘節點：火印熔爐 skeleton、第 3 枚碎片來源、完整火之印記 preview/event。
- 暫不做八元素、完整屬性克制、精神屬性、正式轉職、正式聖物、多城鎮、大型 UI 框架、通用 Boss framework 或 combat/schema/save 大改。

Drift check 可回貼：

```text
目前專案是《元素迷宮：邊境冒險者》Python CLI v1 playable vertical slice。README.md 是 project-level SSOT；01_content 是內容與架構規劃；full-act-structure.md 是五幕總綱；act-2-content-plan.md 是第二幕灰燼裂谷規劃；combat-growth-layering-plan.md 記錄「職業玩法定位先行，屬性系統暫緩」。02_schema 是資料契約；04_data/data 是 runtime data；registry.py 是資料索引與 unlock/helper；06_tools/validate_data.py 做跨表引用驗證；03_engine/engine 目前包含 game.py、display.py、formatting.py、bestiary.py、previews.py。v1 第一幕已完成且主線可通關；第二幕 Act 2 Slice 1 已完成，灰燼裂谷偵查版已進 runtime data，完成 quest_boss_glen 後會解鎖 unlock_act_2 與 unlock_ash_ravine，並可接「灰燼裂谷偵查」。入口平衡補丁、灰燼裂谷普通怪 HP 平衡 MVP、灰燼守衛 Boss MVP、集中藥袋 special 裝備語意修正、工會收購 MVP、倉庫 MVP、倉庫入口 UX 修正、怪物圖鑑 MVP、轉職 preview-only MVP、聖物 preview-only MVP、職業特化 preview-only MVP 與盜賊 head-slot 副武器 data-only MVP 皆已完成。灰燼守衛只在 quest_ash_ravine_scout 完成後於灰燼裂谷終點出現；擊敗後設定 ash_guardian_defeated 並取得第 2 枚 key_fire_mark_shard；本機 run_checks.bat 與手動測試皆通過。盜賊影袖副刃普通攻擊低倍率追擊 MVP 已完成並由使用者手測成功，定位為裝備/副武器效果層的最小玩法實例；它只影響盜賊、只限裝備 armor_rogue_sleeve_blade、只限普通攻擊，技能攻擊不觸發，擊殺/EXP/gold/掉落維持一次結算。轉職、聖物與職業特化目前皆為 preview-only，未新增正式狀態或效果。火、冰目前只作為局部特色，不新增八元素、完整屬性克制、完整抗性表或精神屬性。盜賊副武器使用既有 head slot，未新增 offhand。目前火之印記碎片最多可取得 2 枚；完整火之印記、火印熔爐、火印爐衛、第二幕完整任務鏈、正式轉職、正式聖物、正式職業特化仍未實作。下一階段建議暫停橫向擴張大型系統，轉向 read-only 規劃火印熔爐 skeleton、第 3 枚碎片來源、完整火之印記 preview/event；暫不做八元素、完整屬性克制、精神屬性、正式轉職、正式聖物、多城鎮、大型 UI 框架、通用 Boss framework 或 combat/schema/save 大改。
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
