# state.schema

## 資料來源

- Runtime 建立：`03_engine/engine/game.py:create_state()`
- Runtime 存檔：`save.json`

`save.json` 是玩家進度，不是設計資料 SSOT。

## 目前資料結構

```python
{
    "name": str,
    "job": str,
    "level": int,
    "exp": int,
    "gold": int,
    "guild_points": int,
    "current_hp": int,
    "current_mp": int,
    "inventory": dict[item_id, qty],
    "storage_unlocked": bool,
    "storage": dict[item_id, qty],
    "bestiary": list[monster_id],
    "equipment": {
        "weapon": item_id | None,
        "head": item_id | None,
        "body": item_id | None,
        "accessory": item_id | None,
        "special": item_id | None,
    },
    "learned_skills": list[skill_id],
    "completed_quests": list[quest_id],
    "unlocked": list[unlock_key],
    "cleared_dungeons": list[dungeon_id],
    "flags": dict[flag_key, bool],
}
```

## 必填欄位

所有上列欄位皆為目前必填。讀取舊存檔時若缺欄位，未來應提供 migration 或預設補值。

## 引用規則

- `job` 必須存在於 `JOBS`；目前中文職業名稱即為 job id。
- `inventory` key 必須存在於 `ITEMS`、`EQUIPMENT` 或 `MATERIALS`。
- `storage_unlocked` 表示 LV1 倉庫是否已開啟；第一版沒有 `storage_level`。
- `storage` key 必須存在於 `ITEMS`、`EQUIPMENT` 或 `MATERIALS`，且目前 runtime 不允許存入 `key_` 開頭的 key item。
- `bestiary` 內的 monster id 必須存在於 `MONSTERS`；第一版只記錄已登錄怪物，不記錄擊殺數、遭遇數或完成率。
- `equipment` value 若非 `None`，必須存在於 `EQUIPMENT`。
- `learned_skills` 必須存在於 `SKILLS`。
- `completed_quests` 必須存在於 `QUESTS`。
- `cleared_dungeons` 必須存在於 `DUNGEONS`。
- `unlocked` 可包含 dungeon id、quest id、recipe id、item unlock key、shop unlock key、story/system key。
- `flags` 用於事件狀態，例如 `boss_glen_sighted`、`boss_glen_investigation_accepted`、`boss_glen_defeated`。

## 未來注意事項

- 不要手動把 `save.json` 當資料表改。
- 讀取舊存檔時，runtime 需以 `ensure_state_defaults()` 補上 `flags={}`、`storage_unlocked=False`、`storage={}` 與 `bestiary=[]`。
- 若 data id 改名，需處理舊存檔相容性。
- 若新增裝備 slot，需同步更新 `equipment.schema.md` 與 `create_state()`。
