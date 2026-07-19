# equipment.schema

## Phase 4A Affix Instance Contract

`EQUIPMENT` remains static base data. It must never store a rolled affix or be
mutated to represent one player's copy. A future runtime resolver combines a
base entry with its persisted instance record:

```python
equipment_instance = {
    "base_item_id": equipment_id,       # must exist in EQUIPMENT
    "generation_version": 0 | 1,
    "roll_index": int,                  # non-negative, unique in one state
    "major_affix_id": str | None,
    "minor_affix_id": str | None,
}
```

`generation_version: 0` denotes a legacy-migrated, unaffixed copy. Version 1
is reserved for the first deterministic runtime generator. The instance may
have at most one major and one minor affix; neither may change its base slot,
job list, price, or `normal_attack_followup` data.

Affix definitions are planned as static data with an id, tier (`major` or
`minor`), eligible base slots, stat increment, and family. A family may occur
at most once per instance. The first runtime slice excludes `special`,
head-slot pseudo-offhand behavior changes, and elemental infusion. Elemental
infusion remains a later contract extension and must not override a skill's
declared element.

Per-item and loadout caps apply only to the sum of affix increments. They do
not retroactively invalidate deterministic base stats that exceed legacy QA
caps.

## 資料來源

- `04_data/data/items.py`
- Runtime 常數：`EQUIPMENT`

## 目前資料結構

```python
EQUIPMENT = {
    equipment_id: {
        "name": str,
        "slot": "weapon" | "head" | "body" | "accessory" | "special",
        "subtype": str,
        "price": int,
        "jobs": list[job_id],
        "stats": dict[stat_key, int],
        "desc": str,
        "unlock": str,  # optional
        "normal_attack_followup": {  # optional; head-slot pseudo-offhands only
            "multiplier": float,
            "element": str,
            "on_hit": {"status": str, "duration": int, "chance": int, "multiplier": float, "damage_type": str},  # optional
        },
    }
}
```

## 必填欄位

- `name`
- `slot`
- `subtype`
- `price`
- `jobs`
- `stats`
- `desc`

## 選填欄位

- `unlock`
- `region`
- `normal_attack_followup`

`normal_attack_followup` is valid only on `head` equipment. It triggers after a
normal attack that does not defeat the target. Its optional `on_hit` uses the
existing physical-status accuracy, race-effectiveness, duration, and damage rules.

## 型別與規則

- `slot` 必須符合 `state["equipment"]` 支援欄位。
- `jobs` 內的 job id 必須存在於 `JOBS`。
- `price` 可為 `0`，通常代表任務、合成或關鍵裝備。
- `stats` key 目前支援：`attack`、`magic_attack`、`defense`、`magic_defense`、`agility`、`effect_accuracy`、`crit`、`fire_resist`、`ice_resist`、`earth_resist`、`thunder_resist`、`trap_evasion`、`rare_drop`。
- `region` 若存在，必須為合法的區域 ID（例如 `border_fire`、`ice`、`earth`、`thunder`、`final` 之一）。

## 引用規則

- `SHOP_INVENTORY` 可引用 equipment id。
- `RECIPES.output` 與 `RECIPES.base_item` 可引用 equipment id。
- `QUESTS.reward.items`、`MONSTERS.drops`、`state.inventory`、`state.equipment` 可引用 equipment id。

## 未來注意事項

- 合成消耗基礎裝備由 `RECIPES[recipe_id]["base_item"]` 管理，不寫在 equipment 裡。
- 新增 stat key 時，需同步更新 `get_stats()`、`equipment_summary()`、validation 與此 schema。
