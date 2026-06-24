# item.schema

## 資料來源

- `04_data/data/items.py`
- Runtime 常數：`ITEMS`

## 目前資料結構

```python
ITEMS = {
    item_id: {
        "name": str,
        "kind": str,
        "price": int,
        "desc": str,
        "unlock": str,  # optional
    }
}
```

## 必填欄位

- `name`
- `kind`
- `price`
- `desc`

## 選填欄位

- `unlock`
- `region`

## 型別與規則

- `kind` 目前支援 `consumable`、`special`、`battle`。
- `price` 是商店售價，必須為 `int >= 0`。
- `unlock` 若存在，必須能由任務、怪物事件或劇情流程加入 `state["unlocked"]`。
- `region` 若存在，必須為合法的區域 ID（例如 `border_fire`、`ice`、`earth`、`thunder`、`final` 之一）。

## 引用規則

- `SHOP_INVENTORY` 可引用 item id。
- `QUESTS.reward.items` 可引用 item id。
- `RECIPES.output` 與 `RECIPES.base_item` 可引用 item id。
- `MONSTERS.drops` 可引用 item id。

## 未來注意事項

目前 item effect 多數硬寫在 engine，例如小藥水、集中滴露、破甲釘、逃脫卷軸。未來若道具效果增加，建議逐步資料化：

```python
"effect": {
    "type": "heal_hp" | "heal_mp" | "clear_status" | "apply_debuff" | "escape",
    "amount": int,
    "status": str,
    "duration": int,
}
```
