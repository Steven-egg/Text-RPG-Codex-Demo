# material.schema

## 資料來源

- `04_data/data/materials.py`
- Runtime 常數：`MATERIALS`

## 目前資料結構

```python
MATERIALS = {
    material_id: display_name,
}
```

## 必填欄位

每筆資料是一組 `str -> str`：

- key：material id
- value：顯示名稱

## 選填欄位

目前無選填欄位。

## 引用規則

material id 可被以下資料引用：

- `MONSTERS.drops`
- `DUNGEONS.materials`
- `QUESTS.turn_in`
- `QUESTS.reward.items`
- `RECIPES.materials`
- `MAGIC_BOOKS.materials`
- `state.inventory`

## 現況說明

目前關鍵道具也放在 `MATERIALS`，例如 `key_blood_map`、`key_fire_mark_shard`。

## 未來注意事項

若 key item 數量增加，建議拆成：

- `MATERIALS`
- `KEY_ITEMS`

目前先保留現況，避免不必要重構。
