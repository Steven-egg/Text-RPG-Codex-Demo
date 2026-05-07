# shop.schema

## 資料來源

- `04_data/data/shops.py`
- Runtime 常數：`SHOP_INVENTORY`

## 目前資料結構

```python
SHOP_INVENTORY = {
    inventory_key: list[item_or_equipment_id],
}
```

目前 inventory key 包含：

- `weapon`
- `armor`
- `travel`

## 必填欄位

每個 inventory key 對應一個商品 id list。

## 選填欄位

目前無選填欄位。

## 引用規則

- 商品 id 必須存在於 `ITEMS` 或 `EQUIPMENT`。
- 商品是否顯示由 item/equipment 自身的 `unlock` 控制。

## 現況說明

商店 metadata 尚未資料化。店名、NPC、解鎖條件目前主要寫在 README、設計文件與 engine 流程中。

## 未來注意事項

未來可新增：

```python
SHOPS = {
    "shop_weapon_01": {
        "name": "鐵刃工坊",
        "npc": "葛雷",
        "unlock": None,
        "inventory_key": "weapon",
    }
}
```

目前不強制實作，避免過早架構化。
