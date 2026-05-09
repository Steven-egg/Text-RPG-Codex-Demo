# Codex Session 接續快照

用途：給下一個 Codex session 在接手此專案時快速恢復上下文。  
狀態日期：2026-05-09
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
Act 2 Slice 1 已完成：灰燼裂谷偵查版已進入 runtime data。Act 2 Entry Balance & Guidance Patch 也已完成，修正葛倫壓力、小魔晶掉落、破甲釘負回饋與灰燼裂谷入口引導。集中藥袋 special 裝備語意 bug 也已修正。近期已完成工會收購 MVP、倉庫 MVP、倉庫入口顯示位置修正、怪物圖鑑 MVP、轉職資料結構 MVP、聖物資料結構 preview MVP 與職業特化 MVP preview-only。重點仍不是直接完成第二幕，而是逐步以單一節點 MVP 驗證 engine、save、schema、data、registry、validation 與必要文件同步。

## 2. 已完成項目

### 可玩遊戲原型

- `element_maze.py` 作為入口。
- `run-game.bat` 可啟動遊戲。
- 四個初始職業：劍士、法師、盜賊、牧師。
- 城鎮：工會、鐵刃工坊、堅甲工坊、旅人小鋪、米菈合成屋、星燈魔法商店、轉職神殿。
- 迷宮：青苔洞窟、焦石礦坑、灰燼裂谷偵查版。
- Boss：山寨頭目葛倫。灰燼裂谷目前沒有 Boss。
- 基礎戰鬥、掉落、合成、商店、任務、魔法書、存檔、工會素材收購、LV1 倉庫、怪物圖鑑 MVP、轉職 preview、聖物 preview、職業特化 preview。
- 玩家普通攻擊與傷害技能目前為 100% 命中。

### Act 2 Slice 1 runtime data

- 完成 `quest_boss_glen` 後會解鎖 `second_act_preview`、`unlock_act_2`、`unlock_ash_ravine`。
- `dungeon_ash_ravine` 已新增，定位為灰燼裂谷偵查版。
- 灰燼裂谷偵查版目前有 3 個普通怪：灰燼小鬼、熔岩蝙蝠、燼火兵。
- 灰燼裂谷偵查版目前有 3 個素材：裂谷灰、焦黑鐵片、精煉火焰石。
- 灰燼裂谷目前為 18 步，`boss` 為 `None`。
- 已新增最小偵查任務 `quest_ash_ravine_scout`，完成「血跡地圖」後可見。
- 灰燼守衛、完整火之印記、第二幕完整任務鏈、轉職神殿後續仍未實作。

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
- 後續若要調整灰燼裂谷難度，需以 Lv7-9、低裝或無抗火斗篷狀態另行測試。

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
│     └─ game.py
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

位置：`03_engine/engine/game.py`

負責：

- 主流程、選單與輸入。
- 城鎮、背包、商店、合成、任務、迷宮、戰鬥。
- 存檔與讀檔。
- 傷害、狀態、掉落、任務交付等 runtime 規則。

目前 `game.py` 仍是較大的單檔 engine，但不要大重構。

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
- 破甲釘即時傷害補丁。
- 集中藥袋 special 裝備語意修正。
- 轉職資料結構 MVP。
- 聖物資料結構 preview MVP。
- 職業特化 MVP preview-only。

目前尚未實作：

- 灰燼守衛 Boss。
- 第二幕完整任務鏈。
- 情報屋或鍊金攤。
- 完整火之印記流程。
- 轉職試煉入口 runtime 行為。
- 正式轉職系統。
- 正式職業特化選擇與效果。
- 完整聖物系統、聖物取得狀態與聖物效果。

第二幕第一個最小施工切片「灰燼裂谷偵查版」已完成；後續仍不應直接擴成完整第二幕。

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
- 不要修改 `03_engine/engine/game.py`。
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
2. 下一個新 session 再規劃下一個單一節點，例如聖物取得狀態 MVP、職業特化正式設計前只讀檢查、README / runtime 說明檢查或 engine 拆分前檢查；仍需先做單一節點規劃與實作前檢查，不直接實作完整系統。
3. 在使用者明確要求下，提出 schema / registry / validation / save schema 的最小修改理由與範圍。

下一個候選節點可評估：

1. 聖物取得狀態 MVP。
2. 職業特化正式設計前只讀檢查。
3. README / runtime 說明檢查。
4. engine 拆分前檢查。

下一輪仍應先做單一節點規劃與實作前檢查，不要直接實作完整系統。

若進入下一個新系統節點，第一步仍應是架構盤點，不要直接改檔：

```text
確認節點目標與不做項
→ 檢查現有 engine / save / schema / data / registry 形狀
→ 確認是否需要新增 save 欄位或 schema 文件
→ 回報修改範圍與風險
→ 使用者確認後，下一輪才實作
```

不要在同一輪做灰燼守衛、完整火之印記、第二幕完整任務鏈、轉職試煉、情報屋、鍊金攤、聖物完整系統、轉職完整系統、怪物圖鑑完整系統、第二個元素迷宮、Act 3、倉庫升級完整版或經濟平衡調整。

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

可回貼舊 session 驗證是否 drift：

```text
目前專案是《元素迷宮：邊境冒險者》Python CLI v1 playable vertical slice。README.md 是 project-level SSOT；01_content 是內容與架構規劃；game-design.md 是 v1 設計；game-architecture.md 是擴大架構；full-act-structure.md 是五幕總綱；act-2-content-plan.md 是第二幕灰燼裂谷規劃。02_schema 是資料契約；04_data/data 是 runtime data；registry.py 只做資料索引與 id/unlock helper；validate_data.py 做跨表引用驗證；engine/game.py 是 runtime 流程。v1 第一幕已完成且主線可通關；第二幕 Act 2 Slice 1 已完成，灰燼裂谷偵查版已進 runtime data，完成 quest_boss_glen 後會解鎖 unlock_act_2 與 unlock_ash_ravine，並可接「灰燼裂谷偵查」。入口平衡補丁、集中藥袋 special 裝備語意修正、工會收購 MVP、倉庫 MVP、倉庫入口 UX 修正、怪物圖鑑 MVP、轉職資料結構 MVP、聖物資料結構 preview MVP 與職業特化 MVP preview-only 皆已完成。轉職資料目前只做 `PROMOTIONS` preview-only 骨架與神殿條件顯示，正式轉職尚未開放。聖物資料目前只做 `RELICS` preview-only 骨架與城鎮「聖物調查」顯示，聖物效果尚未開放。職業特化目前只做 `JOB_SPECIALIZATIONS` preview-only 骨架與角色狀態頁顯示，四個基礎職業 preview 為劍士「守勢突破」、法師「元素共鳴」、盜賊「影步偵查」、牧師「聖印守護」，UI 明確標註目前尚未生效。職業特化 MVP 未新增 save 欄位，未修改 `state.schema.md`，未新增 `state["job_specialization"]` 或其他特化狀態，未修改 `get_stats()`、戰鬥、技能、裝備限制或魔法書限制，也未混入轉職神殿；轉職神殿仍只顯示 `PROMOTIONS` preview。目前已新增 `run_checks.bat` 作為 Windows 本機標準驗證入口，使用者本機執行已通過 `data validation ok`、`smoke test ok`、`all checks ok`；前一輪 Codex 環境找不到 Python runtime，後續驗證以本機 `run_checks.bat` 結果為準，可另開節點檢查 README / runtime 說明。灰燼裂谷目前沒有 Boss；灰燼守衛、完整火之印記、第二幕完整任務鏈、正式轉職系統、聖物取得狀態與聖物效果、正式職業特化選擇與效果仍未實作。本 session 到此收尾；下一個新 session 可評估聖物取得狀態 MVP、職業特化正式設計前只讀檢查、README / runtime 說明檢查或 engine 拆分前檢查，仍需先做單一節點規劃與實作前檢查，不直接實作完整系統。不得處理 Element Decay，不得新增 act-3-content-plan.md。
```

## 12. 給下一個 Codex 的一句話

目前專案已完成 v1 可玩原型、第二幕內容規劃、五幕總綱、灰燼裂谷偵查版 runtime data、入口平衡引導補丁、集中藥袋 special 裝備語意修正、工會收購 MVP、倉庫 MVP、倉庫入口 UX 修正、怪物圖鑑 MVP、轉職資料結構 MVP、聖物資料結構 preview MVP 與職業特化 MVP preview-only。轉職資料目前只做 `PROMOTIONS` preview-only 骨架與神殿條件顯示，正式轉職尚未開放，也沒有新增 save 欄位或改變 `state["job"]`。聖物資料目前只做 `RELICS` preview-only 骨架與城鎮「聖物調查」顯示，聖物效果尚未開放，也沒有新增 `state["relics"]` 或任何 save 欄位。職業特化目前只做 `JOB_SPECIALIZATIONS` preview-only 骨架與角色狀態頁顯示，UI 明確標註目前尚未生效，也沒有新增 save 欄位、特化狀態欄位、數值效果或任何戰鬥/技能/裝備/魔法書限制變更。Windows 本機標準驗證入口是專案根目錄的 `run_checks.bat`；Codex 若遇到 Python runtime / sandbox 存取限制，不視為 gameplay 錯誤。本 session 到此收尾；下一個新 session 可評估聖物取得狀態 MVP、職業特化正式設計前只讀檢查、README / runtime 說明檢查或 engine 拆分前檢查，但仍要先做單一節點規劃與實作前檢查，不直接實作完整系統；不要急著把灰燼守衛、完整火之印記、完整任務鏈、完整轉職、完整聖物、完整職業特化、完整圖鑑或後續幕次塞進 runtime。

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

1. 聖物取得狀態 MVP。
2. 職業特化正式設計前只讀檢查。
3. README / runtime 說明檢查。
4. engine 拆分前檢查。

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

1. 聖物取得狀態 MVP。
2. 職業特化正式設計前只讀檢查。
3. README / runtime 說明檢查。
4. engine 拆分前檢查。

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

1. 聖物取得狀態 MVP。
2. 職業特化正式設計前只讀檢查。
3. README / runtime 說明檢查。
4. engine 拆分前檢查。

下一輪仍應先做單一節點規劃與實作前檢查，不要直接實作完整系統。
