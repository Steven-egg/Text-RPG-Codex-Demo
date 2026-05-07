# monster.schema

## 資料來源

- `04_data/data/monsters.py`
- Runtime 常數：`MONSTERS`

## 目前資料結構

```python
MONSTERS = {
    monster_id: {
        "name": str,
        "level": int,
        "hp": int,
        "attack": int,
        "defense": int,
        "agility": int,
        "accuracy": int,
        "crit": int,
        "element": str,
        "exp": int,
        "gold": tuple[int, int],
        "drops": list[tuple[item_or_material_id, chance_float, qty_int]],
        "boss": bool,  # optional
    }
}
```

## 必填欄位

- `name`
- `level`
- `hp`
- `attack`
- `defense`
- `agility`
- `accuracy`
- `crit`
- `element`
- `exp`
- `gold`
- `drops`

## 選填欄位

- `boss`

## 引用規則

- `drops` 的 id 必須存在於 `ITEMS`、`EQUIPMENT` 或 `MATERIALS`。
- `gold` 必須是 `(min, max)`，且 `min <= max`。
- `chance` 是 0 到 1 的 float。
- `DUNGEONS.monsters` 與 `DUNGEONS.boss` 可引用 monster id。

## 未來注意事項

特殊 AI 目前寫在 `monster_action()` 與 `boss_glen_action()`。未來新增特殊怪物時，建議加入：

```python
"behavior": "normal" | "lava_imp" | "scorched_guard" | "boss_glen"
```

再由 behavior registry 對應 engine 函式。
