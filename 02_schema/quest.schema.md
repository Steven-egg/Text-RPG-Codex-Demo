# quest.schema

## 資料來源

- `04_data/data/quests.py`
- Runtime 常數：`QUESTS`

## 目前資料結構

```python
QUESTS = {
    quest_id: {
        "title": str,
        "giver": str,
        "turn_in": dict[item_id_or_flag, qty],
        "reward": {
            "gold": int,
            "items": dict[item_id, qty],
            "guild": int,
        },
        "unlocks": list[unlock_key],
        "desc": str,
    }
}
```

## 必填欄位

- `title`
- `giver`
- `turn_in`
- `reward.gold`
- `reward.items`
- `reward.guild`
- `unlocks`
- `desc`

## 選填欄位

目前無選填欄位。

## 引用規則

- `turn_in` 可引用 `ITEMS`、`EQUIPMENT`、`MATERIALS`，或 `flag:xxx`。
- `reward.items` 可引用 `ITEMS`、`EQUIPMENT`、`MATERIALS`。
- `unlocks` 可解鎖 dungeon、shop、item、recipe、quest 或 story preview。

## 現況說明

目前部分 quest 會把自己的 quest id 放進 `unlocks`，作為任務顯示與完成邏輯的簡化設計。這是目前允許的。

## 未來注意事項

- 若任務解鎖規則變多，建議把 `quest_unlocked()` 的硬寫邏輯資料化。
- 新增 `flag:` turn-in 時，需確認 engine 中有對應事件會設定該 flag。
