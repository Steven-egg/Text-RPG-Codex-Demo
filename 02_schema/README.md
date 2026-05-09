# 02_schema 資料契約

本資料夾是《元素迷宮：邊境冒險者》的 data-contract SSOT。這裡描述資料欄位、型別、必要性、跨表引用與維護規則；實際 runtime 讀取的資料仍以 `04_data/data/*.py` 為準。

目前 schema 以 Markdown 維護，不是 JSON Schema。未來若資料量增加，可依這些文件轉成 `.json` schema 或 validation script。

## 文件索引

- `state.schema.md`：`save.json` 與 runtime player state。
- `job.schema.md`：職業資料 `JOBS`。
- `job_specialization.schema.md`：preview-only 職業特化預告資料 `JOB_SPECIALIZATIONS`。
- `promotion.schema.md`：preview-only 轉職預告資料 `PROMOTIONS`。
- `relic.schema.md`：preview-only 聖物預告資料 `RELICS`。
- `item.schema.md`：一般道具 `ITEMS`。
- `equipment.schema.md`：裝備 `EQUIPMENT`。
- `skill.schema.md`：技能 `SKILLS`。
- `magic_book.schema.md`：魔法書 `MAGIC_BOOKS`。
- `material.schema.md`：素材與關鍵道具 `MATERIALS`。
- `monster.schema.md`：怪物與 Boss `MONSTERS`。
- `dungeon.schema.md`：迷宮 `DUNGEONS` 與事件權重。
- `quest.schema.md`：任務 `QUESTS`。
- `shop.schema.md`：商店商品清單 `SHOP_INVENTORY`。
- `recipe.schema.md`：合成配方 `RECIPES`。
- `registry.schema.md`：id registry、unlock key 與 validation 規則。

## 維護規則

- 修改 `04_data/data/*.py` 後，請同步檢查相關 schema。
- 新增跨表 id 引用後，請執行 `06_tools/validate_data.py`。
- `save.json` 是 runtime 存檔，不是設計資料來源。
