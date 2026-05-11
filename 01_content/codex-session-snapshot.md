# Codex Session 接續快照

## 最新快照：火之印記三碎片後工會詢問與神殿接橋已進 runtime

目前 runtime 已完成三枚 `key_fire_mark_shard` 收集後的兩個最小劇情接橋：

完成內容：
- 玩家持有 `key_fire_mark_shard x3`，且尚未觸發過事件時，冒險者工會會新增「詢問三枚印記碎片的事情」。
- 工會詢問完成後設定 `fire_mark_guild_inquiry_done`；諾亞會提示三枚碎片反應明顯，但工會無法判讀真正用途，建議前往教堂／教會側詢問。
- 玩家完成工會詢問、仍持有三枚碎片，且尚未觸發神殿接橋時，第一次進入轉職神殿會觸發賽恩的一次性對話。
- 神殿接橋完成後設定 `fire_mark_church_bridge_done`。
- 這兩個事件只做查閱方向與劇情接橋：不合成火之印記、不消耗三枚碎片、不開正式火印流程、不啟用正式聖物或正式轉職。
- 本輪文件同步為 markdown-only；不改 runtime / data / schema / save / combat formula。

目前 runtime 最新狀態：
- `dungeon_cinder_seal_depths`「燼印深窟」已進 runtime，普通怪為 `mon_ember_stalker`、`mon_molten_shell`、`mon_cinder_brand_wisp`。
- `boss_cinder_seal_sentinel` 已進 runtime，現名「燼印鎮衛」；擊敗後取得第 3 枚 `key_fire_mark_shard`，並設定 `cinder_seal_sentinel_defeated` 防重複領取。
- `quest_supply_upgrade` 已素材化，需要 `mat_flame_stone_refined x3` 與 `mat_lava_shard x2`；完成後取得 `item_potion_m x2` 並解鎖旅人小鋪販售中藥水。
- 三碎片後的工會詢問事件已完成，使用 `fire_mark_guild_inquiry_done` 防重複觸發。
- 工會 → 教堂／神殿接橋事件已完成，使用 `fire_mark_church_bridge_done` 防重複觸發。
- 火之印記目前不是正式聖物，暫定為未來正式聖物的零組件／核心材料與第一章主線成果物。
- demo 第一章目標是完成「發現火印真相」，不是讓玩家掌握火印力量。
- 燼印鎮衛調高一階難度後，Lv10-Lv12 盜賊測試可通過；中藥水在 Boss 後期連續使用兩次，確認具有實戰價值；目前不再調 Boss 數值。
- 未實作：完整火之印記正式合成／啟用、火印熔爐、具名火印守護 Boss、正式教會火印流程、正式聖物、正式轉職、完整屬性系統、通用 Boss framework、save/schema/combat formula 改動。

## 歷史快照：中藥水任務素材化 MVP

本輪記錄使用者測試結果，並將補給線升級改成素材交付型任務。

- 燼印深窟 Boss `boss_cinder_seal_sentinel` 調高一階難度後，Lv10-Lv12 盜賊測試可通過。
- 中藥水在 Boss 後期連續使用兩次，確認具有實戰價值。
- 目前不再調 Boss 數值。
- 本輪不做完整火之印記、火印熔爐、火印爐衛、工會三碎片詢問選項、教會事件、通用 Boss framework、save/schema/combat formula。

## 歷史快照：燼印深窟 dungeon skeleton MVP 與 Boss read-only plan

本輪完成文件同步，記錄「燼印深窟」最新狀態與下一輪 Boss MVP 邊界。本輪不修改 runtime / engine / data / schema / save/state。

已完成狀態：
- `dungeon_cinder_seal_depths`「燼印深窟」skeleton 已進 runtime。
- 使用者已完成人工測試，確認沒有問題。
- 歷史註記：當時 `dungeon_cinder_seal_depths["boss"]` 仍為 `None`；目前已指向 `boss_cinder_seal_sentinel`。
- 燼印深窟由 `quest_supply_upgrade` 完成後解鎖，`unlock` 直接使用 `dungeon_cinder_seal_depths`。
- 燼印深窟目前只有兩隻普通怪：`mon_ember_stalker`、`mon_molten_shell`。
- `mon_cinder_acolyte` 暫不新增，避免引出施法、debuff 或特殊 AI。
- 本輪未新增新素材、新商店、新配方或新道具。
- 歷史註記：當時火之印記碎片最多可取得 2 枚；目前第 3 枚已可由燼印鎮衛取得。

下一輪 Boss MVP 預設：
- 新 Boss id：`boss_cinder_seal_sentinel`。
- Boss 名稱：「燼印哨衛」。
- Boss 所屬地城：`dungeon_cinder_seal_depths`。
- 第 3 枚 `key_fire_mark_shard` 只由擊敗 `boss_cinder_seal_sentinel` 後取得。
- 工會不補發第 3 枚碎片，只負責提示玩家前往燼印深窟，以及 Boss 後提示玩家可去教會詢問碎片或火之印記。
- Boss gate 預設使用最小偵查或討伐任務，例如 `quest_cinder_depths_scout`。
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

明確未做：
- 未新增或實作完整火之印記。
- 未新增火印熔爐。
- 未新增火印爐衛。
- 未新增正式轉職。
- 未新增正式聖物。
- 未新增八元素。
- 未新增完整屬性克制。
- 未新增通用 Boss framework。
- 未改 save/schema。
- 未改 combat formula。
- 未新增 Act 3 規劃文件。

## 補給藥水升級任務 MVP 完成紀錄

本輪完成補給藥水升級任務 MVP，範圍只包含補給任務、商店解鎖與戰鬥中使用中藥水。

完成內容：
- 新增 `item_potion_m`「中藥水」，`kind` 為 `consumable`，價格 80G，效果文案為回復 HP 70。
- `item_potion_m` 已加入旅人小鋪 `SHOP_INVENTORY["travel"]`，未解鎖前不顯示。
- 新增 `quest_supply_upgrade`「補給線升級」。
- `quest_supply_upgrade` 在 `ash_guardian_defeated` 為 true 後出現。
- 任務完成後獎勵 `item_potion_m x2`，並 unlock `item_potion_m`，讓旅人小鋪開始販售中藥水。
- 戰鬥道具選單已支援 `item_potion_m`，使用後回復最多 70 HP，且不超過 max HP。

本輪刻意暫緩：
- 不實作素材交付需求。
- 不綁定 `mat_ravine_ash`、`mat_flame_stone_refined` 或任何新材料。
- 素材交付需求待新的 dungeon / materials / monsters 系統完成後再回補。

未修改：
- schema / save / state。
- combat formula。
- Boss AI。
- dungeon / monster data。
- materials / drops / refinement。
- 鍊金、製藥、配方、正式轉職、正式聖物、八元素、offhand、完整火印、火印熔爐、火印爐衛。

實機驗證結果：
- 已完整驗證火系第一章 vertical slice：葛倫 Boss 戰、`血跡地圖`、`灰燼裂谷偵查`、`灰燼守衛`、`補給線升級` 與中藥水解鎖。
- quest flag 與前置條件正常：灰燼守衛未擊敗前不會出現「補給線升級」，擊敗後任務正常解鎖，任務完成後不會重複完成。
- 商店解鎖狀態正常保存，任務完成後旅人小鋪會販售中藥水。
- 葛倫與灰燼裂谷怪物正常運作，Boss 系統未出現回歸問題。
- 灼傷、防禦下降、Boss buff/debuff 正常。
- 掉落、圖鑑、等級提升、首次通關獎勵正常。
- 舊道具回歸功能已確認：小藥水、集中滴露、解毒草、破甲釘、逃脫卷軸均可正常使用，未被中藥水系統破壞。
- 新中藥水系統已確認：戰鬥中可正常使用，HP 不足時回復 70，接近滿血時不會超過 max HP。

## 第 3 枚火之印記碎片 read-only 規劃結論

本輪只做 markdown-only 收尾與備份；未實作 gameplay，也不修改 runtime / engine / data / schema / save/state。

最新規劃方向已修正：第 3 枚 `key_fire_mark_shard` 不做成工會任務補發，而是來自燼印深窟後續 Boss。工會只負責灰燼守衛後提供新地點線索，以及 Boss 後提示玩家可去教會詢問火之印記。

目前已完成與尚未實作的切分：
- 新 dungeon `dungeon_cinder_seal_depths`「燼印深窟」已完成 skeleton MVP。
- 已實作普通怪：`mon_ember_stalker`、`mon_molten_shell`。
- `mon_cinder_acolyte` 暫不新增，避免引出施法、debuff 或特殊 AI。
- 新 Boss 候選：`boss_cinder_seal_sentinel`，名稱「燼印哨衛」，尚未實作。
- 擊敗 `boss_cinder_seal_sentinel` 後才取得第 3 枚 `key_fire_mark_shard`。
- 擊敗 Boss 並回報後，工會提示玩家可去教會詢問碎片或火之印記相關資訊。

後續任務節奏暫定為三個追加任務：
- 任務 A：開啟新火系 dungeon 的引子。
- 任務 B：開放進階補給藥水的引子。
- 任務 C：Boss 討伐任務兼第 3 枚火之印記碎片取得與教會引導。

補給藥水升級任務 MVP 已作為燼印深窟前置節點完成：`quest_supply_upgrade` 完成後會解鎖燼印深窟 skeleton。目的不是開鍊金或製藥系統，而是讓玩家能更順地度過第二章 demo 的 Boss，同時 Boss 難度不必過度下修。

明確限制：
- 暫不新增完整火之印記。
- 暫不新增火印熔爐。
- 暫不新增火印爐衛。
- 暫不新增正式轉職。
- 暫不新增正式聖物。
- 暫不新增八元素完整系統。
- 暫不新增 `offhand` slot。
- 暫不修改 schema / save/state。
- 暫不修改 combat formula。
- 暫不做通用 Boss framework。
- 暫不展開完整第二幕。

用途：給下一個 Codex session 在接手此專案時快速恢復上下文。  
狀態日期：2026-05-10
專案：`C:\Users\user\OneDrive\文字冒險遊戲`

## 1. 目前版本與目標

目前版本是 Python CLI 文字冒險 RPG《元素迷宮：邊境冒險者》的 v1 playable vertical slice。

目前已可遊玩，核心循環為：

```text
進入迷宮探索
→ 戰鬥
→ 取得素材、金幣、經驗
→ 回城整備
→ 商店、合成、工會、魔法書強化
→ 挑戰更高階迷宮
```

目前專案已從「可玩原型」進入「第二幕最小施工切片迭代」與核心系統 MVP 拆點階段。  
Act 2 火系 demo 已包含灰燼裂谷、灰燼守衛、補給線升級、燼印深窟、燼印鎮衛 Boss MVP 與第 3 枚火之印記碎片來源。最新完成的最小 UX 補點是：玩家走完燼印深窟但尚未滿足 Boss gate 時，會提示深處仍有守護者氣息，並引導回冒險者工會詢問諾亞。重點仍不是直接完成第二幕，而是逐步以單一節點 MVP 驗證 engine、save、schema、data、registry、validation 與必要文件同步。

## 2. 已完成項目

### 可玩遊戲原型

- `element_maze.py` 作為入口。
- `run-game.bat` 可啟動遊戲。
- 四個初始職業：劍士、法師、盜賊、牧師。
- 城鎮：工會、鐵刃工坊、堅甲工坊、旅人小鋪、米菈合成屋、星燈魔法商店、轉職神殿。
- 迷宮：青苔洞窟、焦石礦坑、灰燼裂谷、燼印深窟。
- Boss：山寨頭目葛倫、灰燼守衛、燼印鎮衛。
- 基礎戰鬥、掉落、合成、商店、任務、魔法書、存檔、工會素材收購、LV1 倉庫、怪物圖鑑 MVP、轉職 preview、聖物 preview、職業特化 preview、盜賊 head-slot 副武器 data-only MVP。
- 玩家普通攻擊與傷害技能目前為 100% 命中。

### Act 2 runtime data

- 完成 `quest_boss_glen` 後會解鎖 `second_act_preview`、`unlock_act_2`、`unlock_ash_ravine`。
- `dungeon_ash_ravine` 已新增，定位為灰燼裂谷偵查版。
- 灰燼裂谷偵查版目前有 3 個普通怪：灰燼小鬼、熔岩蝙蝠、燼火兵。
- 灰燼裂谷偵查版目前有 3 個素材：裂谷灰、焦黑鐵片、精煉火焰石。
- 灰燼裂谷目前為 18 步，`boss` 為 `boss_ash_guardian`。
- 已新增最小偵查任務 `quest_ash_ravine_scout`，完成「血跡地圖」後可見。
- 灰燼守衛只在 `quest_ash_ravine_scout` 完成後出現；擊敗後設定 `ash_guardian_defeated` 並取得第 2 枚 `key_fire_mark_shard`。
- 灰燼守衛後會開放燼印深窟探索；`quest_supply_upgrade` 已素材化並解鎖中藥水販售。
- 燼印深窟目前有 3 個普通怪：餘燼潛獵者、熔殼岩獸、燼印火靈。
- 燼印鎮衛只在 `quest_cinder_depths_scout` 完成後出現；擊敗後設定 `cinder_seal_sentinel_defeated` 並取得第 3 枚 `key_fire_mark_shard`。
- 目前火之印記碎片最多可取得 3 枚；玩家持有三枚碎片後，可在工會觸發三碎片詢問並設定 `fire_mark_guild_inquiry_done`。
- 完成工會詢問後，首次進入轉職神殿會觸發工會 → 教堂／神殿接橋並設定 `fire_mark_church_bridge_done`。
- 火之印記目前不是正式聖物，暫定為未來正式聖物的零組件／核心材料；demo 第一章目標是「發現火印真相」，不是「掌握火印力量」。
- 完整火之印記正式合成／啟用、火印熔爐、具名火印守護 Boss、第二幕完整任務鏈、正式轉職與正式聖物仍未實作。

### Act 2 Entry Balance & Guidance Patch

- `boss_glen` 小幅降壓：HP 260 -> 240、attack 25 -> 23、crit 6 -> 5。
- `mat_small_crystal` 掉落率提高：洞窟黏蟲 10% -> 18%，裂石小魔像 12% -> 20%。
- `item_armor_piercer` 仍降防 3 回合，並新增立即造成少量比例傷害。
- `dungeon_ash_ravine` 步數 8 -> 18。
- `quest_boss_glen` 完成訊息會指向灰燼裂谷偵查；`quest_ash_ravine_scout` 以少量裂谷素材作為交付目標。
- 玩家短測確認：破甲釘可造成傷害並正常觸發擊殺、經驗與金幣結算。
- 玩家短測未觀察到小藥水、集中滴露、逃脫卷軸被破甲釘補丁波及。

### 集中藥袋 special 裝備語意修正

- 原本使用背包與裝備共用的擁有判定，導致集中藥袋沒有遵守 special 裝備語意。
- 目前已改為 `state["equipment"].get("special") == "special_focus_pouch"`。
- 只有 special 欄實際裝備集中藥袋時，進入迷宮才會取得集中滴露並顯示訊息。
- 見習徽章與其他 special 裝備不受影響。

### 灰燼裂谷難度註記

- 玩家目前短測角色 Lv10、火抗 25%、裝備抗火斗篷，已高於灰燼裂谷推薦 Lv7-9。
- 灰燼裂谷體感偏輕鬆暫不視為怪物數值 bug。
- 後續若要調整灰燼裂谷難度，需先整理 Lv6-7、低裝或無抗火斗篷狀態的實測資料。

### 核心系統 MVP 節點

- 工會收購 MVP 已完成：
  - 採白名單制，只允許指定素材被工會收購。
  - 不使用「非 key item」作為可賣判斷。
  - 第一版只給金幣，不給工會積分，不做工會等級，不調整經濟系統。
  - 不修改 save schema，不新增 save 欄位。
- 倉庫 MVP 已完成：
  - 新增 `storage_unlocked: bool`。
  - 新增 `storage: dict[item_id, qty]`。
  - 新增 `ensure_state_defaults(state)`，讀取舊存檔後補 `storage_unlocked=False` 與 `storage={}`。
  - 開倉費固定 500G，第一版只開啟 LV1，不做升級系統。
  - 容量為 10 種物品，以物品種類數計算；既有種類可繼續堆疊。
  - key item 不可存；目前以 `is_key_item(item_id)` helper 集中判斷。
  - 存入/取出共用既有 inventory add/remove 邏輯，不直接操作已裝備物品。
- 倉庫入口顯示位置修正已完成：
  - `backpack_menu(state, allow_storage=False)`。
  - 城鎮選單呼叫 `backpack_menu(state, allow_storage=True)`，會顯示倉庫。
  - 主選單「背包/裝備」呼叫 `backpack_menu(state, allow_storage=False)`，不顯示倉庫。
  - 未修改 save schema、倉庫資料結構或倉庫核心存取邏輯。
- 怪物圖鑑 MVP 已完成：
  - 新增 `bestiary: list[monster_id]` save 欄位。
  - `create_state()` 新角色包含 `bestiary=[]`。
  - `ensure_state_defaults(state)` 會補舊存檔 `bestiary=[]`。
  - `combat()` 勝利後 100% 登錄怪物；普通怪與 Boss 皆適用。
  - 逃跑、戰敗、單純遭遇不登錄。
  - 已登錄怪物不重複加入、不重複提示。
  - 主選單新增「怪物圖鑑」獨立入口，不放城鎮或背包。
  - 圖鑑只顯示已登錄怪物。
  - 顯示名稱、屬性、HP、攻擊、經驗值、金錢、出現地點、掉落物名稱。
  - `monster_locations(monster_id)` 從 `DUNGEONS` 反查出現地點。
  - 掉落物用 `item_name()` 顯示名稱，不直接印 id。
  - 本輪未做 20% 機率登錄、掉落率顯示、擊殺數、遭遇數、`???` 未登錄清單、圖鑑完成率、圖鑑獎勵、成就系統、大型 UI 重構或 engine 大拆分。
- 轉職資料結構 MVP 已完成：
  - 新增 `04_data/data/promotions.py`，建立 `PROMOTIONS` preview-only 轉職資料。
  - 城鎮「轉職神殿」已改為讀取 `PROMOTIONS`，顯示目前職業、未來轉職方向、summary 與條件達成狀態。
  - 神殿明確顯示正式轉職尚未開放。
  - 沒有新增 save 欄位、沒有修改 `state["job"]`、沒有修改 `get_stats()` 或戰鬥公式。
- 聖物資料結構 preview MVP 已完成：
  - 新增 `04_data/data/relics.py`，建立 `RELICS`。
  - 第一個 preview-only 聖物是 `relic_ash_charm`，名稱為「灰燼護符」。
  - `RELICS` 已匯出並納入 registry。
  - `06_tools/validate_data.py` 已加入 relic validation。
  - 新增 `02_schema/relic.schema.md`，並更新 schema README 與 registry schema。
  - 城鎮已新增「聖物調查」入口。
  - 「聖物調查」目前只顯示 preview，不提供取得、裝備、啟用、升級或強化。
  - 畫面會明確顯示「目前僅為預覽，聖物效果尚未開放」。
  - 沒有新增 save 欄位、沒有新增 `state["relics"]`、沒有修改 `state.schema.md`。
  - 沒有修改 `create_state()`、`ensure_state_defaults()`、`get_stats()`、`calc_enemy_damage()`、`element_multiplier()`、陷阱傷害公式或裝備 stats。
  - 沒有實作聖物取得、裝備、啟用、效果、升級、掉落、任務鏈、圖鑑或成就。
- 職業特化 MVP preview-only 已完成：
  - 新增 `04_data/data/job_specializations.py`，建立 `JOB_SPECIALIZATIONS` preview-only。
  - 四個基礎職業各有一筆職業特化 preview：
    - 劍士：守勢突破。
    - 法師：元素共鳴。
    - 盜賊：影步偵查。
    - 牧師：聖印守護。
  - `JOB_SPECIALIZATIONS` 已匯出並納入 registry。
  - `06_tools/validate_data.py` 已加入 job specialization validation。
  - 新增 `02_schema/job_specialization.schema.md`，並更新 schema README 與 registry schema。
  - 角色狀態頁 `show_status()` 會顯示目前 `state["job"]` 對應的「職業特化預覽」。
  - UI 明確標註「目前尚未生效」。
  - 沒有新增 save 欄位、沒有修改 `state.schema.md`。
  - 沒有新增 `state["job_specialization"]` 或其他特化狀態。
  - 沒有修改 `get_stats()`、戰鬥、技能、裝備限制或魔法書限制。
  - 沒有混入轉職神殿；轉職神殿仍只顯示 `PROMOTIONS` preview。
- 盜賊 head-slot 副武器 data-only MVP 已完成：
  - 新增 `armor_rogue_sleeve_blade`（影袖副刃）。
  - 使用既有 `head` slot，`subtype` 為「副武器」。
  - `jobs` 只允許 `["盜賊"]`。
  - stats 只使用既有 key：`attack`、`agility`、`crit`。
  - 已加入既有防具商店。
  - 沒有新增 `offhand` slot，沒有修改 engine、combat、save/state 或 schema/validation。

### 專案治理與文件

- `README.md` 是 project-level SSOT。
- `02_schema/` 已建立 Markdown schema 文件。
- `04_data/data/registry.py` 已建立 data registry。
- `06_tools/validate_data.py` 已建立 validation 工具。
- `01_content/game-design.md` 是 v1 content-design SSOT。
- `01_content/game-architecture.md` 是擴大版 architecture SSOT。
- `01_content/act-2-content-plan.md` 已建立第二幕灰燼裂谷內容計畫。
- `01_content/full-act-structure.md` 已建立五幕總體骨架，作為幕次總綱。
- `01_content/codex-handoff-short.md` 已更新為短交接摘要。

### 已驗證過

早前已驗證：

- 編譯檢查通過。
- `element_maze.py --smoke-test` 通過。
- `06_tools/validate_data.py` 通過並輸出 `data validation ok`。

注意：前一輪 Codex 環境找不到全域 `python`、`py`，README 中的 bundled Python 路徑也無法存取。使用者本機可用 Python 路徑為：

```powershell
C:\Users\User\AppData\Local\Programs\Python\Python311\python.exe
```

若 Codex 環境仍無法存取該路徑，不應判定程式錯誤；後續驗證以使用者本機結果為準，並可另開節點檢查 README / runtime 說明。

最近一次入口平衡與引導修正已通過 validation、compile check 與 smoke test。
最近一次集中藥袋 special 裝備語意修正也已通過 validation、compile check 與 smoke test。
最近一次工會收購 MVP 已通過 validation、smoke test、工會入口檢查與素材收購流程模擬。
最近一次倉庫 MVP 已通過 validation、smoke test、舊存檔補欄位、開倉、存入/取出、容量、key item 排除與非法輸入等流程測試。
最近一次倉庫入口 UX 修正已通過 validation、smoke test 與 `allow_storage` 選單可見性測試。
最近一次怪物圖鑑 MVP 已通過 validation、smoke test、普通怪勝利登錄、Boss 勝利登錄、重複登錄不重複加入、逃跑 / 戰敗不登錄、圖鑑 UI、主選單入口、工會收購與倉庫 helper 回歸檢查。
怪物圖鑑 MVP 實機短測全部通過：
- 主選單有「怪物圖鑑」。
- 新遊戲或舊存檔進入圖鑑不會報錯。
- 尚未擊敗怪物時有空狀態提示。
- 擊敗普通怪後會出現在圖鑑。
- 圖鑑顯示內容可接受，沒有過度干擾。
- 已登錄怪物不重複提示。
- 主選單、城鎮、背包、倉庫入口沒有混亂。
最近一次轉職資料結構 MVP 已通過 validation 與 smoke test。
最近一次聖物資料結構 preview MVP 已通過 validation 與 smoke test：
- bundled Python 執行 `06_tools\validate_data.py` → `data validation ok`
- bundled Python 執行 `element_maze.py --smoke-test` → `smoke test ok`
最近一次職業特化 MVP preview-only 已由使用者在本機專案根目錄補跑並通過：
- `python 06_tools\validate_data.py` → `data validation ok`
- `python element_maze.py --smoke-test` → `怪物圖鑑新增：青苔鼠。`、`完成：鐵劍 +1。`、`smoke test ok`
目前已新增 `run_checks.bat` 作為 Windows 本機標準驗證入口，會依序執行 `python 06_tools\validate_data.py` 與 `python element_maze.py --smoke-test`。
使用者已在本機專案根目錄手動執行 `run_checks.bat` 並通過：
- `data validation ok`
- `smoke test ok`
- `all checks ok`
若 Codex 環境遇到 Python runtime / sandbox 存取限制，不視為 gameplay 錯誤；以使用者本機 PowerShell 執行 `run_checks.bat` 的回貼結果為準。

## 3. 目前檔案結構

忽略 `__pycache__` 後，目前主要結構如下：

```text
文字冒險遊戲/
├─ README.md
├─ element_maze.py
├─ run-game.bat
├─ run_checks.bat
├─ save.json
├─ .gitignore
├─ 01_content/
│  ├─ game-design.md
│  ├─ game-architecture.md
│  ├─ act-2-content-plan.md
│  ├─ full-act-structure.md
│  ├─ codex-handoff-short.md
│  └─ codex-session-snapshot.md
├─ 02_schema/
│  ├─ README.md
│  ├─ state.schema.md
│  ├─ job.schema.md
│  ├─ job_specialization.schema.md
│  ├─ promotion.schema.md
│  ├─ relic.schema.md
│  ├─ item.schema.md
│  ├─ equipment.schema.md
│  ├─ skill.schema.md
│  ├─ magic_book.schema.md
│  ├─ material.schema.md
│  ├─ monster.schema.md
│  ├─ dungeon.schema.md
│  ├─ quest.schema.md
│  ├─ shop.schema.md
│  ├─ recipe.schema.md
│  └─ registry.schema.md
├─ 03_engine/
│  └─ engine/
│     ├─ __init__.py
│     ├─ bestiary.py
│     ├─ display.py
│     ├─ formatting.py
│     ├─ game.py
│     └─ previews.py
├─ 04_data/
│  └─ data/
│     ├─ __init__.py
│     ├─ jobs.py
│     ├─ job_specializations.py
│     ├─ materials.py
│     ├─ items.py
│     ├─ skills.py
│     ├─ crafting.py
│     ├─ monsters.py
│     ├─ dungeons.py
│     ├─ quests.py
│     ├─ shops.py
│     ├─ promotions.py
│     ├─ relics.py
│     └─ registry.py
├─ 05_assets/
└─ 06_tools/
   └─ validate_data.py
```

## 4. SSOT 分層

- `README.md`：project-level SSOT，說明版本狀態、啟動方式、資料夾職責、治理規則與 roadmap。
- `01_content/game-design.md`：content-design SSOT，說明 v1 玩法、系統、內容表與平衡基準。
- `01_content/game-architecture.md`：architecture SSOT，說明擴大遊戲架構、系統邊界、內容階層與未來資料化順序。
- `01_content/full-act-structure.md`：五幕總綱，銜接 README、v1 設計、擴大架構與第二幕內容計畫。
- `01_content/act-2-content-plan.md`：第二幕內容規劃，聚焦灰燼裂谷與元素迷宮擴張驗證。
- `02_schema/*.schema.md`：data-contract SSOT，定義欄位、型別、引用規則與維護規則。
- `04_data/data/*.py`：runtime data SSOT，遊戲實際讀取的資料表。
- `04_data/data/registry.py`：data registry 與 id/unlock helper。
- `06_tools/validate_data.py`：資料驗證工具。
- `save.json`：runtime 存檔，不是 SSOT。

## 5. Schema / Engine / Data / Registry 分工

### schema

位置：`02_schema/`

負責：

- 定義資料契約。
- 說明欄位、型別、必要性與選填欄位。
- 說明跨表引用規則。
- 記錄未來擴張注意事項。

不負責 runtime 邏輯、實際遊戲資料或玩家存檔。

### engine

位置：`03_engine/engine/`

負責：

- `game.py`：主流程、城鎮、背包、商店、合成、任務、迷宮、戰鬥、存檔與讀檔。
- `display.py`：CLI / display primitives。
- `formatting.py`：名稱查詢與格式化 helper。
- `bestiary.py`：怪物圖鑑查詢 helper。
- `previews.py`：preview-only 顯示與資料查詢 helper。

目前 `game.py` 仍是 runtime 核心且職責較集中，但已有低風險 helper modules。不要繼續為拆而拆，也不要在功能輪順手重構 engine。

### data

位置：`04_data/data/`

負責：

- `jobs.py`：職業。
- `job_specializations.py`：preview-only 職業特化預告資料。
- `materials.py`：素材與關鍵道具名稱。
- `items.py`：一般道具與裝備。
- `skills.py`：技能與魔法書。
- `crafting.py`：合成配方。
- `monsters.py`：怪物與 Boss。
- `dungeons.py`：迷宮與事件權重。
- `quests.py`：任務。
- `shops.py`：商店商品清單。
- `promotions.py`：preview-only 轉職預告資料。
- `relics.py`：preview-only 聖物預告資料。

data 檔只放資料表，不放互動流程或 gameplay 邏輯。

### registry

位置：`04_data/data/registry.py`

負責：

- 彙整所有 data table。
- 提供 id set helper。
- 集中記錄初始、事件、劇情、系統 unlock key。
- 支援 validation。

不負責戰鬥邏輯、任務流程、迷宮事件處理或玩家輸入。

## 6. 第二幕目前狀態

`01_content/act-2-content-plan.md` 已存在，且目前已標註 Act 2 Slice 1 的已實作狀態。未標註已實作的段落仍是規劃或候選內容。

第二幕第一輪主軸：

```text
血跡地圖解讀
→ 灰燼裂谷線索
→ 城鎮新增準備需求
→ 灰燼裂谷探索
→ 灰燼守衛 Boss
→ 完整火之印記
→ 轉職試煉入口預告
```

目前已實作：

- 灰燼裂谷偵查版 runtime data。
- `dungeon_ash_ravine`。
- 3 個普通怪。
- 3 個素材。
- `unlock_act_2` 與 `unlock_ash_ravine`。
- `quest_ash_ravine_scout` 最小偵查任務。
- 灰燼守衛 Boss MVP：`boss_ash_guardian`、`ash_guardian_defeated`、灰燼裂谷 boss 指向灰燼守衛。
- 灰燼守衛 gate：完成 `quest_ash_ravine_scout` 後才會在灰燼裂谷終點出現。
- 灰燼守衛擊敗獎勵：第 2 枚 `key_fire_mark_shard`，且防重複領取正常。
- 燼印鎮衛 Boss MVP 與第 3 枚 `key_fire_mark_shard` 來源。
- 三碎片後工會詢問事件：設定 `fire_mark_guild_inquiry_done`。
- 工會 → 教堂／神殿接橋事件：設定 `fire_mark_church_bridge_done`。
- 破甲釘即時傷害補丁。
- 集中藥袋 special 裝備語意修正。
- 轉職資料結構 MVP。
- 聖物資料結構 preview MVP。
- 職業特化 MVP preview-only。

目前尚未實作：

- 第二幕完整任務鏈。
- 情報屋或鍊金攤。
- 完整火之印記正式合成／啟用。
- 火印熔爐。
- 具名火印守護 Boss。
- 正式教會火印流程。
- 轉職試煉入口 runtime 行為。
- 正式轉職系統。
- 正式職業特化選擇與效果。
- 完整聖物系統、聖物取得狀態與聖物效果。

目前火之印記不是正式聖物，暫定為未來正式聖物的零組件／核心材料；demo 第一章收束目標是「發現火印真相」，不是讓玩家掌握完整火印力量。

第二幕第一個最小施工切片「灰燼裂谷偵查版」與灰燼守衛 Boss MVP 已完成；後續仍不應直接擴成完整第二幕。

## 7. 五幕總綱目前狀態

`01_content/full-act-structure.md` 已建立五幕制骨架：

1. 第一幕：v1 MVP 垂直切片，已完成。
2. 第二幕：灰燼裂谷與元素迷宮擴張驗證。
3. 第三幕：轉職與第二元素路線成形。
4. 第四幕：中後期複合系統整合。
5. 第五幕：終局迷宮與最終 Boss 封版。

此文件明確規定：

- 不提前新增 `act-3-content-plan.md`。
- 不提前實作第三幕、第四幕、第五幕內容。
- 每一輪施工都應先確認幕次、最小切片與允許修改檔案。

## 8. 明確禁止事項

除非使用者在新 session 明確改變方向，否則禁止：

- 不要直接完成整個第二幕。
- 不要修改 `03_engine/engine/*.py`。
- 不要修改 `04_data/data/*.py`。
- 不要修改 `02_schema/*.schema.md`，除非先提出理由與最小修改範圍且使用者明確要求。
- 不要修改 `04_data/data/registry.py` 或 `06_tools/validate_data.py`，除非進入明確批准的 registry/validation 準備切片。
- 不要新增 gameplay 內容到 runtime data。
- 不要新增 `01_content/act-3-content-plan.md`。
- 不要新增 act-3 runtime 內容。
- 不要大重構 engine。
- 不要把 Python dict 全部改成 JSON/YAML。
- 不要把 `save.json` 當資料來源。
- 不要刪除或覆蓋既有可玩版本。
- 不要新增 data 後不跑 validation。
- 不要讓 README、schema、data、registry、validation 與內容文件互相矛盾。
- 不要處理 Element Decay。
- 不要調整工會收購價格或擴充經濟系統，除非使用者明確要求進入平衡輪。
- 不要擴充倉庫升級、分類、搜尋、排序或與工會收購聯動，除非使用者明確要求。
- 不要擴充怪物圖鑑完整系統、圖鑑獎勵、完成率、擊殺數、遭遇數、掉落率百科或成就系統，除非使用者明確要求。
- 不要擴充聖物取得、裝備、啟用、效果、升級、掉落、任務鏈、圖鑑或成就，除非使用者明確要求。
- 不要擴充職業特化選擇、特化狀態、被動效果、技能效果或數值加成，除非使用者明確要求。

## 9. 下一步只允許做什麼

目前下一步只允許以下之一：

1. 做 `01_content/` 文件同步或 drift check，並將本 session 作為恢復點收尾。
2. 下一個新 session 再規劃下一個單一節點，例如火印熔爐 skeleton read-only 規劃、第 3 枚碎片來源 read-only 規劃、完整火之印記 preview/event read-only 規劃、數值平衡 read-only 檢查；仍需先做單一節點規劃與實作前檢查，不直接實作完整系統。
3. 在使用者明確要求下，提出 schema / registry / validation / save schema 的最小修改理由與範圍。

下一個候選節點可評估：

1. 火印熔爐 skeleton read-only 規劃。
2. 第 3 枚碎片來源 read-only 規劃。
3. 完整火之印記 preview/event read-only 規劃。
4. 數值平衡 read-only 檢查。

下一輪仍應先做單一節點規劃與實作前檢查，不要直接實作完整系統。

若進入下一個新系統節點，第一步仍應是架構盤點，不要直接改檔：

```text
確認節點目標與不做項
→ 檢查現有 engine / save / schema / data / registry 形狀
→ 確認是否需要新增 save 欄位或 schema 文件
→ 回報修改範圍與風險
→ 使用者確認後，下一輪才實作
```

不要在同一輪做火印熔爐、火印爐衛、完整火之印記、第二幕完整任務鏈、轉職試煉、情報屋、鍊金攤、聖物完整系統、轉職完整系統、怪物圖鑑完整系統、第二個元素迷宮、Act 3、倉庫升級完整版、經濟平衡調整、火抗配方、`offhand` slot、通用 Boss framework 或 combat formula 調整。

## 10. 新 session 先檢查哪些檔案

新 session 開始時，建議依序讀：

1. `01_content/codex-handoff-short.md`
2. `README.md`
3. `01_content/full-act-structure.md`
4. `01_content/act-2-content-plan.md`
5. `01_content/game-architecture.md`
6. `01_content/game-design.md`

如果任務進入第二幕施工前評估，再讀：

7. `02_schema/README.md`
8. `02_schema/registry.schema.md`
9. `02_schema/dungeon.schema.md`
10. `02_schema/monster.schema.md`
11. `02_schema/quest.schema.md`
12. `02_schema/recipe.schema.md`
13. `02_schema/item.schema.md`
14. `02_schema/equipment.schema.md`
15. `04_data/data/registry.py`
16. `06_tools/validate_data.py`

只有需要理解 runtime 行為時才讀：

17. `03_engine/engine/game.py`

下一步文件規劃不應修改 engine。

## 11. Drift check 摘要

可回貼最新 session 驗證是否 drift：

```text
目前專案是《元素迷宮：邊境冒險者》Python CLI v1 playable vertical slice。README.md 是 project-level SSOT；01_content 是內容與架構規劃；game-design.md 是 v1 設計；game-architecture.md 是擴大架構；full-act-structure.md 是五幕總綱；act-2-content-plan.md 是第二幕規劃。02_schema 是資料契約；04_data/data 是 runtime data；registry.py 只做資料索引與 id/unlock helper；validate_data.py 做跨表引用驗證；03_engine/engine 目前包含 game.py、display.py、formatting.py、bestiary.py、previews.py。v1 第一幕已完成且主線可通關；第二幕火系 demo 已進 runtime，包含灰燼裂谷、灰燼守衛、補給線升級、燼印深窟、燼印鎮衛 Boss MVP 與第 3 枚 key_fire_mark_shard 來源。灰燼守衛只在 quest_ash_ravine_scout 完成後於灰燼裂谷終點出現，擊敗後設定 ash_guardian_defeated 並取得第 2 枚碎片；灰燼守衛後會開放燼印深窟探索。quest_supply_upgrade 已素材化，需要 mat_flame_stone_refined x3 與 mat_lava_shard x2，完成後取得 item_potion_m x2 並解鎖旅人小鋪販售中藥水。燼印深窟目前有 mon_ember_stalker、mon_molten_shell、mon_cinder_brand_wisp；boss_cinder_seal_sentinel 現名「燼印鎮衛」，只在 quest_cinder_depths_scout 完成後於深窟終點出現，擊敗後設定 cinder_seal_sentinel_defeated 並取得第 3 枚碎片。若玩家通關深窟但尚未滿足 Boss gate，會顯示守護者氣息與回工會詢問諾亞的提示。玩家持有三枚碎片後，可在工會觸發三碎片詢問並設定 fire_mark_guild_inquiry_done；完成工會詢問後，首次進入轉職神殿會觸發工會 → 教堂／神殿接橋並設定 fire_mark_church_bridge_done。火之印記目前不是正式聖物，暫定為未來正式聖物的零組件／核心材料；demo 第一章目標是發現火印真相，不是掌握火印力量。轉職、聖物與職業特化目前皆為 preview-only，未新增正式狀態或效果；盜賊副武器使用既有 head slot，未新增 offhand。完整火之印記正式合成／啟用、火印熔爐、具名火印守護 Boss、第二幕完整任務鏈、正式轉職、正式聖物、正式職業特化仍未實作。不得處理 Element Decay，不得新增 act-3-content-plan.md，不得新增火抗配方、offhand slot、通用 Boss framework 或完整屬性克制，不得修改 combat formula。
```

## 12. 給下一個 Codex 的一句話

目前專案已完成 v1 可玩原型、第二幕內容規劃、五幕總綱、灰燼裂谷 runtime data、灰燼守衛 Boss MVP、補給線升級素材化、燼印深窟、燼印鎮衛 Boss MVP、第 3 枚火之印記碎片來源、未接 Boss 任務時的深窟通關提示 UX、三碎片後工會詢問事件，以及工會 → 教堂／神殿接橋事件。轉職、聖物與職業特化目前皆為 preview-only，未新增正式狀態、save 欄位或數值效果。盜賊副武器使用既有 `head` slot，沒有新增 `offhand`。火之印記目前不是正式聖物，暫定為未來正式聖物的零組件／核心材料；完整火之印記正式合成／啟用、火印熔爐、具名火印守護 Boss、正式教會火印流程仍未實作。`03_engine/engine` 已拆出 display、formatting、bestiary、previews 等 helper modules，但不要繼續為拆而拆。Windows 本機標準驗證入口是專案根目錄的 `run_checks.bat`；Codex 若遇到 Python runtime / sandbox 存取限制，不視為 gameplay 錯誤。下一個 runtime 候選節點仍應維持單一小切片，不要急著把完整任務鏈、完整轉職、完整聖物、完整職業特化、完整圖鑑、通用 Boss framework 或後續幕次塞進 runtime。

## 13. 轉職資料結構 MVP 收尾摘要

本輪「轉職資料結構 MVP」已完成，範圍是資料化神殿預告與條件顯示，不是完整轉職系統。

完成內容：

- 新增 `04_data/data/promotions.py`，建立 `PROMOTIONS` preview-only 轉職資料。
- 已建立四個 preview-only 轉職方向：
  - 劍士 → 元素騎士
  - 法師 → 星詠者
  - 盜賊 → 影行者
  - 牧師 → 聖印使
- 目前轉職等級條件採 Lv12。
- `PROMOTIONS` 已匯出並納入 registry。
- `06_tools/validate_data.py` 已加入 promotion validation。
- 新增 `02_schema/promotion.schema.md`，並更新 `02_schema/README.md` 與 `02_schema/registry.schema.md`。
- 城鎮「轉職神殿」已改為讀取 `PROMOTIONS`，顯示目前職業、未來轉職方向、summary 與條件達成狀態。
- 神殿會明確顯示「正式轉職尚未開放」。

明確未做：

- 沒有新增 save 欄位。
- 沒有新增 `state["promotion"]`、`state["specialization"]`、`state["completed_promotions"]`。
- 沒有修改 `state["job"]`。
- 沒有修改 `get_stats()`。
- 沒有修改戰鬥公式、技能效果、裝備限制或等級成長。
- 沒有把轉職後職業加入 `JOBS`。

驗證結果：

- `...\python.exe 06_tools/validate_data.py` → `data validation ok`
- `...\python.exe element_maze.py --smoke-test` → `smoke test ok`

下一個候選節點可評估：

1. 數值平衡 read-only 檢查。
2. 灰燼裂谷 Lv6-7 實測資料整理。
3. 檢查怪物成長是否跟不上角色成長、裝備整備與升級全回復。

下一輪仍應先做單一節點規劃與實作前檢查，不要直接實作完整系統。

## 14. 聖物資料結構 preview MVP 收尾摘要

本輪「聖物資料結構 preview MVP」已完成，範圍是資料骨架與玩家可見 preview，不是完整聖物系統。

完成內容：

- 新增 `04_data/data/relics.py`，建立 `RELICS`。
- 目前第一個 preview-only 聖物為 `relic_ash_charm`。
- `relic_ash_charm` 名稱為「灰燼護符」。
- `RELICS` 已匯出並納入 registry。
- `06_tools/validate_data.py` 已加入 relic validation。
- 新增 `02_schema/relic.schema.md`。
- 已更新 `02_schema/README.md` 與 `02_schema/registry.schema.md`。
- 城鎮已新增「聖物調查」入口。
- 「聖物調查」會顯示聖物名稱、summary、來源、解鎖提示、effect_preview 與 status。
- 「聖物調查」目前只顯示 preview，不提供取得、裝備、啟用、升級或強化。
- 畫面會明確顯示「目前僅為預覽，聖物效果尚未開放」。

明確未做：

- 沒有新增 save 欄位。
- 沒有新增 `state["relics"]`。
- 沒有修改 `state.schema.md`。
- 沒有修改 `create_state()`。
- 沒有修改 `ensure_state_defaults()`。
- 沒有修改 `get_stats()`。
- 沒有修改 `calc_enemy_damage()`、`element_multiplier()`、陷阱傷害公式或裝備 stats。
- 沒有實作聖物取得、裝備、啟用、效果、升級、掉落、任務鏈、圖鑑或成就。

驗證結果：

- bundled Python 執行 `06_tools\validate_data.py` → `data validation ok`
- bundled Python 執行 `element_maze.py --smoke-test` → `smoke test ok`

下一個候選節點可評估：

1. 數值平衡 read-only 檢查。
2. 灰燼裂谷 Lv6-7 實測資料整理。
3. 檢查怪物成長是否跟不上角色成長、裝備整備與升級全回復。

下一輪仍應先做單一節點規劃與實作前檢查，不要直接實作完整系統。

## 15. 職業特化 MVP preview-only 收尾摘要

本輪「職業特化 MVP preview-only」已完成，範圍是資料骨架與角色狀態頁 preview，不是正式職業特化系統。

完成內容：

- 新增 `04_data/data/job_specializations.py`，建立 `JOB_SPECIALIZATIONS` preview-only。
- 四個基礎職業各有一筆職業特化 preview：
  - 劍士：守勢突破。
  - 法師：元素共鳴。
  - 盜賊：影步偵查。
  - 牧師：聖印守護。
- 已新增 `02_schema/job_specialization.schema.md`。
- 已更新 `04_data/data/__init__.py` 匯出。
- 已更新 `04_data/data/registry.py` 與 `DATA_REGISTRY`。
- 已更新 `06_tools/validate_data.py`，新增 `check_job_specializations()`。
- 角色狀態頁 `show_status()` 會顯示目前職業對應的「職業特化預覽」。
- UI 明確標註「目前尚未生效」。

明確未做：

- 沒有新增 save 欄位。
- 沒有修改 `state.schema.md`。
- 沒有新增 `state["job_specialization"]` 或其他特化狀態。
- 沒有修改 `get_stats()`。
- 沒有修改戰鬥、技能、裝備限制或魔法書限制。
- 沒有混入轉職神殿；轉職神殿仍只顯示 `PROMOTIONS` preview。

驗證結果：

- 使用者本機執行 `python 06_tools\validate_data.py` → `data validation ok`
- 使用者本機執行 `python element_maze.py --smoke-test` → `怪物圖鑑新增：青苔鼠。`、`完成：鐵劍 +1。`、`smoke test ok`

環境註記：

- 前一輪 Codex 環境找不到 `python`、`py` 與 README 中的 bundled Python runtime。
- 使用者本機已補跑通過；後續驗證以本機結果為準。
- 可另開節點檢查 README / runtime 說明，但不應在功能輪把 runtime 缺失判定為程式錯誤。

下一個候選節點可評估：

1. 數值平衡 read-only 檢查。
2. 灰燼裂谷 Lv6-7 實測資料整理。
3. 檢查怪物成長是否跟不上角色成長、裝備整備與升級全回復。

下一輪仍應先做單一節點規劃與實作前檢查，不要直接實作完整系統。

## 16. engine/data 結構整理前檢查結論

本輪「engine/data 結構整理前檢查」已完成，範圍是 read-only 架構盤點，未修改檔案。

結論：

- 不建議現在整理 `03_engine/engine` 與 `04_data/data` 的巢狀結構。
- 目前真正風險不是資料夾層級，而是 `03_engine/engine/game.py` 職責集中；`game.py` 同時承擔 state/defaults、inventory/equipment、storage、bestiary、guild/quest、shop/crafting、preview UI、dungeon、combat、save/load 與 smoke test。
- `save/state`、`combat/dungeon`、`import/package path`、`registry/validation` 屬高風險區；未來重構前需獨立盤點，不應在功能輪順手修改。
- 若未來拆分 engine，建議先從低風險邊界開始，例如 display / lookup helpers 或 town menu 子功能；不要一開始碰 save/state、combat/dungeon 或大型搬檔。
- 目前不應直接做 engine 拆分、搬移檔案、修改 import、修改 save schema、修改 `state.schema.md` 或大型重構。

此方向目前不作為下一步；若未來明確要延續，仍需先做「engine 拆分前規劃表」並列出候選切點、import 影響、驗證清單與 rollback 範圍，不要直接實作。

## 17. CLI / display primitives 拆分完成紀錄

本輪完成第一個最小 engine 拆分 MVP：只拆出 CLI / display primitives，未擴大到其他 engine 區域。

本輪新增檔案：
- `03_engine/engine/display.py`

本輪修改檔案：
- `03_engine/engine/game.py`

已搬移 helper：
- `setup_console`
- `pause`
- `title`
- `menu`
- `clear_screen`

import 方向：
- `game.py` 單向 import `display.py`
- `display.py` 不 import `game.py`
- 目前沒有 circular import

未修改範圍：
- save/state
- combat/dungeon
- data
- schema
- registry/validation
- `run_checks.bat`
- `element_maze.py`
- README
- gameplay 數值與規則

驗證結果：
- 原始 `python` 指令因 PATH 找不到 python 失敗，不視為 gameplay 錯誤
- 使用本機 Python 絕對路徑補跑：
  - `data validation ok`
  - `smoke test ok`

下一步建議：
- 使用者本機跑 `run_checks.bat`
- 通過後 Git commit / push
- 下一個 engine 拆分節點需另行規劃，不要直接連續拆分

## formatting / lookup helpers 拆分完成紀錄

本輪完成第二個最小 engine helper 拆分節點：只拆出 formatting / lookup helpers，未擴大到其他 engine 區域。

本輪新增檔案：
- `03_engine/engine/formatting.py`

本輪修改檔案：
- `03_engine/engine/game.py`

已搬移 helper：
- `item_name`
- `format_items`
- `equipment_summary`
- `monster_drop_names`

import 方向：
- `game.py -> formatting.py -> data`
- `formatting.py` 不 import `game.py`
- 目前沒有 circular import

未修改範圍：
- save/state
- combat/dungeon
- data
- schema
- registry/validation
- `run_checks.bat`
- `element_maze.py`
- `display.py`
- README
- gameplay 數值與規則

驗證結果：
- 本機 `run_checks.bat` 通過
- `smoke test ok`
- `all checks ok`

GitHub 備份：
- commit `8582872`
- message `Extract formatting lookup helpers`
- 已 push 到 `main`

下一步提醒：
- 下一個 engine 拆分節點需另行 read-only 檢查
- 不要直接連續拆 town、storage、guild、combat、dungeon 或 save/state
- 若繼續拆分，優先考慮低風險 helper 或 preview-only UI，但需先規劃

## bestiary lookup helper 拆分完成紀錄

本輪完成第三個最小 engine helper 拆分節點：只拆出 bestiary lookup helper，未擴大到圖鑑 UI 或登錄流程。

本輪新增檔案：
- `03_engine/engine/bestiary.py`

本輪修改檔案：
- `03_engine/engine/game.py`

已搬移 helper：
- `monster_locations` 已由 `game.py` 搬至 `bestiary.py`

import 方向：
- `game.py -> bestiary.py -> data`
- `bestiary.py` 目前只 import `from data import DUNGEONS`

明確未搬移：
- `bestiary_menu`
- `try_register_bestiary`
- `monster_drop_names`
- `ensure_state_defaults`

未修改範圍：
- save/state
- combat/dungeon
- storage
- guild/quest
- shop/crafting
- data
- schema
- registry/validation
- README
- gameplay 數值與規則

驗證結果：
- 本機 `run_checks.bat` 已通過
- `smoke test ok`
- `all checks ok`

下一步提醒：
- 下一個 engine 拆分節點仍需先做 read-only 檢查
- 不要直接連續拆 engine

## job specialization preview helper 拆分完成紀錄

本輪完成第四個最小 engine helper 拆分節點：只抽出 job specialization preview helper，未擴大到其他 preview 或 gameplay 區域。

本輪新增檔案：
- `03_engine/engine/previews.py`

本輪修改檔案：
- `03_engine/engine/game.py`

已抽出 helper：
- `show_job_specialization_preview(job: str) -> None`

原本來源：
- `show_status` 內的職業特化 preview 顯示區塊

import 方向：
- `game.py -> previews.py -> data`
- `previews.py` 目前只 import `from data import JOB_SPECIALIZATIONS`

明確未搬移：
- `show_status` 本體

未修改範圍：
- relic
- promotion
- bestiary
- save/state
- combat/dungeon
- data
- schema
- registry/validation
- gameplay 數值與規則

驗證結果：
- 本機 `run_checks.bat` 已通過
- `smoke test ok`
- `all checks ok`

下一步提醒：
- 下一個 engine 拆分節點仍需先做 read-only 檢查
- 不要直接連續拆 engine

## relic preview query helper 拆分完成紀錄

本輪完成第五個最小 engine helper 拆分節點：只抽出 relic preview data query helper，未搬移聖物選單本體或解鎖文字 helper。

本輪修改檔案：
- `03_engine/engine/previews.py`
- `03_engine/engine/game.py`

已新增 helper：
- `get_preview_relics() -> list[dict]`

原本來源：
- `relic_preview_menu` 內的 `RELICS.values()` 與 `status == "preview"` 篩選區塊

import 方向：
- `game.py -> previews.py -> data`
- `previews.py` 目前 import `JOB_SPECIALIZATIONS` 與 `RELICS`
- `previews.py` 不 import `game.py`

明確未搬移：
- `relic_preview_menu`
- `relic_unlock_met`
- `relic_unlock_line`
- temple
- promotion requirement helper

未修改範圍：
- save/state
- combat/dungeon
- town/guild/storage/shop/crafting
- data
- schema
- registry/validation
- README
- gameplay 數值與規則

驗證提醒：
- 本輪建議執行本機 `run_checks.bat`
- 若通過，建議 commit message：`Extract relic preview query helper`

## promotion preview query helper 拆分完成紀錄

本輪完成第六個最小 engine helper 拆分節點：只抽出 promotion preview data query helper，未搬移 temple 本體或 promotion requirement helper。

本輪修改檔案：
- `03_engine/engine/previews.py`
- `03_engine/engine/game.py`

已新增 helper：
- `get_preview_promotions_for_job(job: str) -> list[dict]`

原本來源：
- `temple` 內的 `PROMOTIONS.values()`、`source_job == state["job"]` 與 `status == "preview"` 篩選區塊

import 方向：
- `game.py -> previews.py -> data`
- `previews.py` 目前 import `JOB_SPECIALIZATIONS`、`PROMOTIONS` 與 `RELICS`
- `previews.py` 不 import `game.py`

明確未搬移：
- `temple`
- `promotion_requirement_met`
- `promotion_requirement_line`
- relic preview helper
- job specialization preview helper

未修改範圍：
- save/state
- combat/dungeon
- town/guild/storage/shop/crafting
- data
- schema
- registry/validation
- README
- gameplay 數值與規則

驗證提醒：
- 本輪建議執行本機 `run_checks.bat`
- 若通過，建議 commit message：`Extract promotion preview query helper`

## 職業特色與刺客副武器 MVP 規劃紀錄

本輪沒有實作，只做 read-only 規劃。

本輪先暫停「餘燼護符」方案，原因是目前已有暖石墜改與抗火斗篷兩件火抗 accessory，再新增同質火抗 accessory 會造成裝備定位重疊。

本輪改為評估「職業特色 / 刺客副武器 / 敏捷戰鬥價值」。

目前 equipment slot 固定為：
- `weapon`
- `head`
- `body`
- `accessory`
- `special`

短期不建議新增 `offhand` slot，因為會牽涉 state、schema、validation、UI、save/defaults 與裝備流程。

第一版刺客特色 MVP 建議採用 data-only 方式：沿用既有 `head` slot，新增盜賊限定「副武器」語意裝備。

此 MVP 的限制是 UI 仍可能顯示為「頭部/head」，但可接受為短期語意不完美。

刺客副武器建議使用既有 stats，例如 `attack`、`agility`、`crit`，不新增新 stat。

敏捷目前用於 `quickstep`、陷阱迴避與逃跑機率，但未真正成為核心輸出屬性。

未來可考慮讓 `agility` 影響傷害浮動區間，例如 85%~125%，敏捷相對怪物越高，越容易落在高傷害區間。

敏捷傷害浮動屬於 combat rule MVP，會碰 `calc_player_damage()`，不應與刺客副武器 data-only MVP 同輪實作。

此候選已於後續完成，完成狀態見下一節。原建議範圍如下：
- 只新增盜賊限定 head-slot 副武器裝備
- 取得方式優先放既有商店
- 不新增 `offhand` slot
- 不修改 engine
- 不修改 combat
- 不修改 save/state
- 不修改 schema/validation

實作後需要本機跑 `run_checks.bat`，通過後再 Git commit / push。

## 盜賊 head-slot 副武器 MVP 完成紀錄

本輪完成 data-only MVP，只新增盜賊限定 head-slot 副武器裝備 `armor_rogue_sleeve_blade`（影袖副刃），並將取得方式放入既有防具商店。

本輪未新增 `offhand` slot，未修改 engine，未修改 combat，未修改 save/state，也未修改 schema/validation。

敏捷傷害浮動仍保留為後續 combat rule MVP；本輪不處理 `calc_player_damage()` 或任何敏捷戰鬥公式。

## 文件 / handoff drift sync MVP 完成紀錄

本輪只做文件同步，更新 README、短交接與 snapshot，反映目前已完成 v1 playable slice、灰燼裂谷偵查版、工會收購 MVP、倉庫 MVP、怪物圖鑑 MVP、轉職 preview-only MVP、聖物 preview-only MVP、職業特化 preview-only MVP，以及盜賊 head-slot 副武器 data-only MVP。

本輪修正 snapshot 前段檔案樹，補上目前 engine helper modules：`game.py`、`display.py`、`formatting.py`、`bestiary.py`、`previews.py`。

本輪將下一步方向記錄為 read-only 數值平衡檢查、灰燼裂谷 Lv6-7 實測資料整理，以及怪物成長是否跟不上角色成長、裝備整備與升級全回復的檢查。

本輪未修改 gameplay、data、schema、engine、validation、`run_checks.bat` 或 `save.json`；未新增功能、未新增 `offhand` slot、未修改 combat formula、未新增火抗配方。

## 灰燼裂谷 Lv7 → Lv8 盜賊實測紀錄

前一輪完成灰燼裂谷普通怪 HP 平衡 MVP，只調整 `04_data/data/monsters.py` 中三隻灰燼裂谷普通怪 HP：
- `mon_ash_imp`：HP 92 -> 104
- `mon_lava_bat`：HP 84 -> 96
- `mon_cinder_soldier`：HP 118 -> 132

本機 `run_checks.bat` 已通過：
- `smoke test ok`
- `all checks ok`

本次實測條件：
- 職業：盜賊
- 等級：Lv7 進場，途中升至 Lv8
- 裝備：獵人短匕、影袖副刃、旅人衣、抗火斗篷、見習徽章
- 進場 HP / MP：149 / 52
- 未攜帶藥水
- 迷宮長度：18 步

實測結果：
- 共 7 場戰鬥
- 燼火兵 6 場、灰燼小鬼 1 場
- 中途升級至 Lv8，HP/MP 全回復
- 最終通關狀態：HP 43 / MP 12
- 未死亡，未逃跑，未使用藥水

判斷：
- 目前灰燼裂谷難度合理
- 不建議繼續提高 HP
- 不建議修改 combat formula、EXP/gold、升級全回復或新增怪物技能
- 若後續仍要評估，應改測法師、劍士、牧師或不同裝備狀態

## 副武器效果分類設計文件 MVP

本輪只做 markdown-only 設計同步，未修改 runtime data、engine、schema、save/state、registry 或 validation。

使用者偏好確認：副武器不應只是第二把主武器，也不應讓普通攻擊直接變成 2 倍輸出。中後期副武器應作為效果載體，讓盜賊或未來刺客路線依敵人、迷宮與資源狀態選擇不同副武器。

本輪在 `01_content/game-design.md` 補上「副武器效果方向」：
- 魔法類型副武器：以元素持續傷害或元素追擊為主，例如火焰灼燒、冰霜凍傷、毒素侵蝕。
- 物理效果副武器：以戰術狀態或短期弱化為主，例如流血、破甲、標記、中毒。

設計邊界：
- 短期仍不新增 `offhand` slot。
- 可沿用既有 `head` slot 的「副武器」語意做原型，例如 `armor_rogue_sleeve_blade`。
- 不定義最終資料欄位名稱，不提前修改 schema 或 save/state。
- 不直接做 combat 實作，不新增正式職業特化系統。

風險紀錄：
- 此方向未來可能導致衍生屬性與狀態類別增加。
- 第一個可施工原型應只選單一副武器與單一低風險效果，不一次做完整狀態系統。
- 魔法類型副武器應等元素與持續傷害框架更清楚後再做。

## 職業玩法定位先行，屬性系統暫緩

本輪只做 markdown-only 規劃同步，新增 `01_content/combat-growth-layering-plan.md`，未修改 Python、runtime data、schema、save/state、engine、registry 或 validation。

核心結論：
- 先穩定四職業玩法語言，再討論屬性、轉職、聖物等大型成長系統。
- 火、冰目前只作為局部特色：火服務焦石礦坑、灰燼裂谷、火傷、火抗裝備與火之印記；冰主要服務冰針術與個別技能語意。
- 暫不新增八元素、完整屬性抗性表、精神屬性或完整屬性克制。
- 魔法/世界觀屬性與物理/戰術效果分層處理；流血、破甲、標記、中毒不應直接混成元素矩陣。

四職業暫定方向：
- 法師：高 MP、魔法技能、魔攻裝備與未來元素適性，暫不要求完整元素系統。
- 盜賊：物理、先手、暴擊、副武器與戰術狀態形成特色，魔法面主要靠裝備或武器效果補足。
- 戰士：穩定物理、防禦姿態、破甲、反擊、盾/武器特效與站場穩定度，不只靠高倍率傷害。
- 牧師：續戰型魔法職，偏治療、護盾、淨化、持續魔法傷害與未來聖屬性方向。

系統優先順序：
1. 職業玩法定位文件。
2. 盜賊影袖副刃普通攻擊追擊 MVP。
3. 職業特化 preview 文案同步。
4. 屬性世界觀架構 markdown-only MVP。
5. 完整八元素與屬性克制系統。

施工邊界：
- 盜賊影袖副刃普通攻擊追擊歸類為裝備/副武器效果層，也可作為職業特化 preview 的玩法實例。
- 它不是正式職業特化系統，不需要 `offhand`、save/state 或 schema 擴充作為前置。
- 下一輪適合回到「盜賊影袖副刃普通攻擊追擊最小 MVP」。
- 下一輪若施工，必須先鎖定低倍率、只限普通攻擊、只限裝備 `armor_rogue_sleeve_blade`，且不得重複擊殺、經驗、金幣或掉落結算。

## 盜賊影袖副刃普通攻擊低倍率追擊 MVP 完成紀錄

本輪完成「盜賊影袖副刃普通攻擊低倍率追擊 MVP」，範圍是最小裝備效果，不是完整 `offhand` 系統，也不是正式職業特化系統。

已知驗證結果：
- 使用者已手測成功，確認盜賊裝備 `armor_rogue_sleeve_blade` 後，普通攻擊可形成兩次攻擊效果。
- 實作後由 Codex 以本機 Python 執行資料驗證與 smoke test，結果通過：
  - `data validation ok`
  - `smoke test ok`
- Codex 另做函式層級檢查，確認裝備觸發、未裝備不觸發、技能不觸發、其他職業不觸發、主攻擊已擊殺不額外追擊。

功能邊界：
- 只影響職業「盜賊」。
- 只影響裝備 `armor_rogue_sleeve_blade`。
- 只影響普通攻擊；技能攻擊不觸發追擊。
- 追擊是低倍率物理追擊，不暴擊、不套元素、不新增狀態。
- 擊殺、EXP、gold、掉落仍維持一次結算。
- 不新增 `offhand` slot。
- 不修改 schema、save/state、runtime data、registry 或 validation。
- 不修改主傷害公式，不開完整職業特化系統。

系統定位：
- 本功能屬於「裝備 / 副武器效果層」的最小玩法實例。
- 它證明影袖副刃可以先用既有 `head` slot 承載副武器語意，不需要立刻新增正式副手欄位。
- 後續不應立刻橫向擴張更多副武器、完整狀態系統或大型職業特化系統。

下一階段方向：
- 暫停繼續橫向擴張大型系統。
- 下一輪建議轉向 read-only / markdown-only 規劃「火之印記第一章可玩閉環 demo MVP」。
- 火之印記閉環方向包含：第三關 Boss、新火系 dungeon skeleton、三個火之印記碎片、火之印記合成 preview/event、2～3 個任務支撐，等級節奏約 Lv8～Lv12。
- 暫不做八元素、完整屬性克制、精神屬性、正式轉職、正式聖物、多城鎮、大型 UI 框架，或 combat/schema/save 大改。

## 灰燼守衛 Boss MVP 完成紀錄

本輪完成「灰燼守衛 Boss MVP」，範圍只是在既有灰燼裂谷加入第二幕第一個守門 Boss，不是完整火之印記閉環。

完成內容：
- 新增 `boss_ash_guardian`。
- `dungeon_ash_ravine["boss"]` 已指向 `boss_ash_guardian`。
- 新增 `ash_guardian_defeated` flag。
- 灰燼守衛只在 `quest_ash_ravine_scout` 完成後於灰燼裂谷終點出現。
- 擊敗灰燼守衛後取得第 2 枚 `key_fire_mark_shard`。
- 防重複領取正常；再次走完灰燼裂谷不會重複觸發灰燼守衛或取得第 2 枚碎片。

驗證結果：
- 使用者本機 `run_checks.bat` 已通過。
- 手動測試確認葛倫流程未回歸。
- 手動測試確認灰燼裂谷偵查 gate 正常。
- 手動測試確認灰燼守衛只觸發一次。
- 手動測試確認第 2 枚火之印記碎片取得正常。

歷史邊界（灰燼守衛 MVP 完成當時）：
- 當時火之印記碎片最多可取得 2 枚；目前第 3 枚已可由燼印鎮衛取得。
- 完整火之印記尚未實作。
- 火印熔爐與火印爐衛尚未實作。
- 正式轉職、正式聖物、八元素、`offhand` slot、完整屬性克制與通用 Boss framework 仍未開放。

歷史下一步建議（灰燼守衛 MVP 完成當時）：
- 火印熔爐 skeleton read-only 規劃。
- 第 3 枚碎片來源 read-only 規劃（目前已完成為燼印鎮衛掉落）。
- 完整火之印記 preview/event read-only 規劃。
