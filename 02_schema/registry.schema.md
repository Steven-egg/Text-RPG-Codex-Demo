# registry.schema

## 目的

registry 是資料總目錄與引用驗證依據，不承擔 gameplay 邏輯。

## Schema registry

本文件定義所有 id 類型、來源檔案、引用關係、unlock key 與 flag 命名規則。

## Data registry

程式位置：

```text
04_data/data/registry.py
```

用途：

- 匯總所有 data tables。
- 提供 id set helper。
- 支援 `06_tools/validate_data.py`。
- 未來可供 engine 做查詢，但不放複雜遊戲規則。

## Id 類型與來源

| 類型 | 來源 |
|---|---|
| job id | `JOBS` key |
| material id | `MATERIALS` key |
| item id | `ITEMS` key |
| equipment id | `EQUIPMENT` key |
| skill id | `SKILLS` key |
| magic book id | `MAGIC_BOOKS` key |
| recipe id | `RECIPES` key |
| promotion id | `PROMOTIONS` key |
| monster id | `MONSTERS` key |
| dungeon id | `DUNGEONS` key |
| quest id | `QUESTS` key |
| shop inventory key | `SHOP_INVENTORY` key |

## Unlock key

`state["unlocked"]` 可包含：

- dungeon id
- quest id
- recipe id
- item/equipment 的 `unlock`
- shop unlock key
- story/system key

目前允許的 story/system key：

- `shop_synthesis_01`
- `second_act_preview`
- `unlock_act_2`
- `unlock_ash_ravine`
- `dungeon_moss_cave`

目前允許的 runtime event unlock：

- `item_armor_piercer`
- `recipe_piercing_bundle`
- `recipe_heat_charm`

## Flag key

flag 使用短字串，存於 `state["flags"]`。任務 turn-in 引用時使用：

```text
flag:boss_glen_defeated
```

目前允許 flag：

- `boss_glen_defeated`

## Promotion preview

`PROMOTIONS` 是 preview-only 的轉職預告資料表，供轉職神殿顯示未來職業方向與條件狀態。

目前不新增 save 欄位、不修改 `state["job"]`、不把轉職後名稱加入 `JOBS`，也不影響戰鬥能力。Validation 只檢查 `source_job`、顯示欄位、status 與 requirements 的跨表引用。

## Validation

工具位置：

```text
06_tools/validate_data.py
```

validation 應檢查跨表引用、基礎欄位與 unlock key 合理性。通過時印出：

```text
data validation ok
```
