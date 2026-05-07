# dungeon.schema

## 資料來源

- `04_data/data/dungeons.py`
- Runtime 常數：`DUNGEONS`、`EVENT_WEIGHTS`

## 目前資料結構

```python
DUNGEONS = {
    dungeon_id: {
        "name": str,
        "recommended": str,
        "steps": int,
        "element": str,
        "unlock": str,
        "materials": list[material_id],
        "monsters": list[monster_id],
        "gold_range": tuple[int, int],
        "clear_guild": int,
        "boss": monster_id | None,
    }
}
```

## 必填欄位

- `name`
- `recommended`
- `steps`
- `element`
- `unlock`
- `materials`
- `monsters`
- `gold_range`
- `clear_guild`
- `boss`

## 選填欄位

目前無選填欄位。

## 引用規則

- `unlock` 必須能出現在 `state["unlocked"]` 或初始解鎖規則中。
- `materials` 必須存在於 `MATERIALS`。
- `monsters` 必須存在於 `MONSTERS`。
- `boss` 若非 `None`，必須存在於 `MONSTERS`。
- `gold_range` 必須是 `(min, max)`，且 `min <= max`。

## 事件權重

`EVENT_WEIGHTS` 目前是全域事件機率：

```python
list[tuple[event_key, weight_int]]
```

## 未來注意事項

若不同迷宮需要不同事件權重，可改成 dungeon 內部欄位：

```python
"event_weights": [("battle", 45), ("material", 20)]
```

目前不重構，先維持全域權重。
