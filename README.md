# 《元素迷宮：邊境冒險者》終端機版

## 1. 專案定位

這是一個 Python CLI 文字冒險 RPG 的 v1 playable vertical slice。核心體驗是「進入迷宮探索 → 戰鬥 → 取得素材與金幣 → 回城整備 → 商店、合成、工會、魔法書強化 → 挑戰更高階迷宮」。

目前目標不是大型內容擴張，而是讓既有最小垂直切片具備可維護、可擴張、可驗證的資料與文件基礎。第二幕已開始以最小切片方式進入 runtime data，目前完成「灰燼裂谷偵查版」與「灰燼守衛 Boss MVP」。

## 2. 目前版本狀態

目前版本已可遊玩，第一幕主線可通關，包含：

- 單人職業：劍士、法師、盜賊、牧師
- 城鎮：工會、鐵刃工坊、堅甲工坊、旅人小鋪、米菈合成屋、星燈魔法商店、轉職神殿
- 商店：武器、防具、飾品、補給、特殊道具
- 魔法書：購買後永久學習技能
- 迷宮：青苔洞窟、焦石礦坑、灰燼裂谷偵查版
- 戰鬥：攻擊、防禦、技能、道具、逃跑
- 掉落：金幣、素材、藥水、關鍵道具
- 合成：抗火斗篷、鐵劍 +1、皮甲 +1、集中藥袋、暖石墜改、破甲釘組
- 工會任務：冒險者登記、洞窟採集、魔晶研究、焦石偵查、血跡地圖、灰燼裂谷偵查
- 工會收購 MVP：工會可收購白名單素材，只給金幣；第一版不收消耗品、裝備或關鍵道具
- 倉庫 MVP：可花費 500G 開啟 LV1 倉庫，存取最多 10 種非 key item 背包物品
- 怪物圖鑑 MVP：擊敗怪物後 100% 登錄，可從主選單查看已登錄怪物的基礎資訊
- 轉職 preview-only MVP：轉職神殿顯示 `PROMOTIONS` 預覽方向與條件，正式轉職尚未開放
- 聖物 preview-only MVP：城鎮「聖物調查」顯示 `RELICS` 預覽，聖物取得與效果尚未開放
- 職業特化 preview-only MVP：角色狀態頁顯示 `JOB_SPECIALIZATIONS` 預覽，目前尚未生效
- 盜賊 head-slot 副武器 data-only MVP：新增盜賊限定 `head` slot 副武器語意裝備，未新增 `offhand`
- Boss：山寨頭目葛倫、灰燼守衛
- 存檔：主選單可存檔，會建立 `save.json`

第二幕目前已實作的 runtime data 包含 Act 2 Slice 1 與灰燼守衛 Boss MVP：

- 完成 `quest_boss_glen` 後會解鎖 `second_act_preview`、`unlock_act_2`、`unlock_ash_ravine`。
- `dungeon_ash_ravine` 已存在，定位為灰燼裂谷偵查版，目前為 18 步。
- 灰燼裂谷目前有 3 個普通怪與 3 個素材。
- 完成「血跡地圖」後，工會會提示玩家前往灰燼裂谷，並顯示最小偵查任務「灰燼裂谷偵查」。
- 灰燼裂谷 `boss` 已指向 `boss_ash_guardian`。
- 灰燼守衛只會在完成 `quest_ash_ravine_scout` 後於灰燼裂谷終點出現。
- 擊敗灰燼守衛會設定 `ash_guardian_defeated`，並取得第 2 枚 `key_fire_mark_shard`；防重複領取已由手測確認。
- 目前火之印記碎片最多可取得 2 枚。
- 完整火之印記、火印熔爐、火印爐衛、第二幕完整任務鏈、轉職神殿後續仍未實作。

最近一次入口平衡修正：

- 山寨頭目葛倫小幅降壓，保留 Boss 定位但降低過度補血循環。
- 洞窟黏蟲與裂石小魔像的小魔晶掉落率提高。
- 破甲釘現在會造成少量即時傷害，並維持 3 回合降低敵方防禦。
- 玩家短測確認：破甲釘可造成傷害並正常觸發擊殺、經驗與金幣結算；小藥水、集中滴露、逃脫卷軸未觀察到被破甲釘補丁波及。
- 集中藥袋已修正為 special 欄實際裝備時才生效；只放在背包中不會在進入迷宮時取得集中滴露。
- 灰燼裂谷普通怪 HP 平衡 MVP 已完成：三隻普通怪小幅提高 HP，`run_checks.bat` 已通過。
- Lv7 → Lv8 盜賊實測確認目前灰燼裂谷難度合理；暫不建議繼續提高 HP，也不建議修改 combat formula、EXP/gold、升級全回復或新增怪物技能。
- 灰燼守衛 Boss MVP 已完成：新增 `boss_ash_guardian`、新增 `ash_guardian_defeated`、灰燼裂谷 boss 指向灰燼守衛；本機 `run_checks.bat` 通過，手動測試確認葛倫流程未回歸、灰燼裂谷偵查 gate 正常、灰燼守衛只觸發一次且第 2 枚火之印記碎片取得正常。

## 3. 啟動方式

最簡單的方式：

1. 在資料夾中執行 `run-game.bat`
2. 建立角色
3. 從主選單進入城鎮或迷宮

如果要用指令啟動：

```powershell
C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\element_maze.py
```

### 驗證方式

Windows 本機可在專案根目錄執行標準檢查入口：

```powershell
.\run_checks.bat
```

`run_checks.bat` 會依序執行：

```powershell
python 06_tools\validate_data.py
python element_maze.py --smoke-test
```

若 Codex 環境因 runtime 或 sandbox 限制無法執行 Python，請由使用者在本機 PowerShell 執行 `run_checks.bat`，再將結果回貼到 Codex session。

煙霧測試：

```powershell
C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\element_maze.py --smoke-test
```

資料驗證：

```powershell
C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\06_tools\validate_data.py
```

## 4. 專案資料夾職責

- `element_maze.py`：遊戲入口，負責載入 `04_data` 與 `03_engine`，再執行 `engine.game.main()`。
- `01_content/`：內容設計文件與玩法規劃。
- `02_schema/`：資料契約文件，定義欄位、型別、引用規則與維護規則。
- `03_engine/engine/`：遊戲流程與規則；目前包含主流程 `game.py`，以及低風險 helper modules：`display.py`、`formatting.py`、`bestiary.py`、`previews.py`。
- `04_data/data/`：runtime 實際讀取的資料表。
- `05_assets/`：未來素材資源預留。
- `06_tools/`：開發與驗證工具。

## 5. SSOT 分層規則

- `README.md`：project-level SSOT，說明版本狀態、啟動方式、資料夾職責、治理規則與 roadmap。
- `01_content/game-design.md`：content-design SSOT，說明玩法循環、世界觀、職業定位、迷宮、商店、任務節奏與平衡基準。
- `02_schema/*.schema.md`：data-contract SSOT，定義每類 data 的欄位、型別、必要性、引用關係與維護規則。
- `04_data/data/*.py`：runtime data SSOT，遊戲實際讀取的資料表。
- `04_data/data/registry.py`：資料索引與引用總目錄，供 validation 與未來查詢使用。
- `06_tools/validate_data.py`：資料驗證工具，檢查跨表引用與基本欄位一致性。
- `save.json`：runtime 存檔，不是 SSOT，不應作為設計資料來源。

## 6. Data 擴張規則

新增職業時，至少同步檢查：

- `04_data/data/jobs.py`
- `04_data/data/skills.py`
- 裝備與魔法書的可用職業
- `02_schema/job.schema.md`
- validation 與 smoke test

新增道具時，至少同步檢查：

- `04_data/data/items.py`
- `04_data/data/shops.py`
- 若有新效果，檢查 `03_engine/engine/game.py`
- `02_schema/item.schema.md`
- validation

新增裝備時，至少同步檢查：

- `04_data/data/items.py` 的 `EQUIPMENT`
- `04_data/data/shops.py`
- `04_data/data/crafting.py`
- `02_schema/equipment.schema.md`
- validation

新增技能或魔法書時，至少同步檢查：

- `04_data/data/skills.py`
- `04_data/data/jobs.py`
- 若是新 `kind` 或新 buff/debuff，檢查 engine 處理流程
- `02_schema/skill.schema.md`
- `02_schema/magic_book.schema.md`
- validation

新增怪物、迷宮、任務或配方時，至少同步檢查：

- 對應的 `04_data/data/*.py`
- 被引用的素材、怪物、任務、解鎖 key 是否存在
- 對應 schema
- `06_tools/validate_data.py`

## 7. Registry 與 Validation

`04_data/data/registry.py` 只做資料彙整與 id set helper，不放複雜 gameplay 邏輯。它目前提供：

- `DATA_REGISTRY`
- item-like id、sellable id、skill id、job id、monster id、dungeon id、recipe id、quest id helper
- 初始、事件、系統、劇情 unlock key 的集中定義

`06_tools/validate_data.py` 會檢查主要跨表引用：

- job 初始技能是否存在
- equipment jobs 是否存在
- magic book 的 job、material、skill 是否存在
- recipe output、material、base item、unlock 是否有效
- dungeon material、monster、boss、unlock 是否有效
- monster drops 是否有效
- quest turn-in、reward、unlock 是否有效
- shop 商品是否存在
- event weights 與基本欄位是否合理

通過時會印出：

```text
data validation ok
```

## 8. 不要做的事

- 不要把 `save.json` 當資料表或設計來源。
- 不要新增 data 後不跑 validation。
- 不要直接在 engine 裡大量硬寫新的 id；若必須硬寫，請在 schema 或 registry 記錄原因。
- 不要一次重構整個 `03_engine/engine/game.py`。
- 不要把 Python dict 全部改成 JSON/YAML，除非另有明確任務。
- 不要讓 README、schema 與實際 data 狀態不同步。

## 9. 下一步 Roadmap

短期：

- 維持 schema 文件。
- 修改 data 後固定跑 validation。
- 重要 gameplay 修改後固定跑 smoke test。
- 下一輪若要繼續評估灰燼裂谷，優先改測法師、劍士、牧師或不同裝備狀態，不直接施工。
- 暫不繼續提高灰燼裂谷普通怪 HP，暫不修改 combat formula、EXP/gold、升級全回復或新增怪物技能。
- 灰燼裂谷目前已具備偵查版與灰燼守衛 Boss MVP；後續測試結論需避免用單次隨機遭遇過度外推。
- 暫不把餘燼護符或新火抗 accessory 當主要下一步；目前已有暖石墜改與抗火斗篷，新增同質火抗飾品容易定位重疊。
- 暫不建議直接做火印熔爐、火印爐衛、完整火之印記、正式轉職、正式聖物、倉庫升級完整版、完整圖鑑系統、火抗配方或 Act 3。
- 下一個 runtime 候選節點應先 read-only 規劃，不直接施工；候選方向包含火印熔爐 skeleton、第 3 枚碎片來源、完整火之印記 preview/event。

中期：

- 若未來有明確低風險邊界，再評估 `03_engine/engine/game.py` 拆分；目前不要為拆而拆。
- 將 item effect、monster behavior、unlock rule 部分資料化。
- 為 validation 增加更細的欄位型別與平衡範圍檢查。

長期：

- 評估 data 是否繼續使用 Python dict，或遷移為 JSON/YAML。
- 建立 save migration，處理 id 改名與版本升級。
- 補更多自動測試，覆蓋商店、合成、任務、迷宮與 Boss 流程。

## 10. 遊玩提示

- 先刷青苔洞窟，交付「洞窟採集」解鎖合成屋與焦石礦坑。
- 小魔晶不要急著賣掉，它能用來學魔法書或完成任務。
- 焦石礦坑的火傷害很痛，抗火斗篷、暖石墜、守護符文和補給都很有用。
- 擊敗山寨頭目葛倫後，把任務「血跡地圖」交回工會，會看到第二幕預告並解鎖灰燼裂谷偵查版；下一步是接「灰燼裂谷偵查」並帶回少量裂谷素材。
- 完成「灰燼裂谷偵查」後，灰燼裂谷終點會出現灰燼守衛；擊敗後可取得第 2 枚火之印記碎片。目前完整火之印記尚未開放。
