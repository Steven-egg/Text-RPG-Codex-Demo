# recipe.schema

## 資料來源

- `04_data/data/crafting.py`
- Runtime 常數：`RECIPES`

## 目前資料結構

```python
RECIPES = {
    recipe_id: {
        "name": str,
        "output": dict[item_id, qty],
        "materials": dict[material_id, qty],
        "gold": int,
        "unlock": str,
        "desc": str,
        "base_item": item_id,  # optional
    }
}
```

## 必填欄位

- `name`
- `output`
- `materials`
- `gold`
- `unlock`
- `desc`

## 選填欄位

- `base_item`
- `region`

## 引用規則

- `output` 的 id 必須存在於 `ITEMS` 或 `EQUIPMENT`。
- `materials` 必須存在於 `MATERIALS`。
- `base_item` 若存在，必須存在於 `ITEMS` 或 `EQUIPMENT`。
- `unlock` 必須能由任務、怪物事件、初始狀態或其他流程加入 `state["unlocked"]`，或可被 `is_unlocked()` 透過 completed quest 判斷。
- `region` 若存在，必須為合法的區域 ID（例如 `border_fire`、`ice`、`earth`、`thunder`、`final` 之一）。

## 合成流程

目前 engine 合成順序：

1. 檢查 gold
2. 檢查 materials
3. 檢查 base_item
4. 扣 gold
5. 扣 materials
6. 扣 base_item
7. 加入 output

## 未來注意事項

- 若 recipes 數量增加，建議依裝備、道具、關鍵物品拆分資料檔。
- 若 unlock rule 變複雜，建議資料化而不是繼續使用字串約定。
