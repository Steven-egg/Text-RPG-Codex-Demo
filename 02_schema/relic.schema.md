# relic.schema

## 資料來源

- `04_data/data/relics.py`
- Runtime 常數：`RELICS`

## 目前定位

`RELICS` 目前是 preview-only 的聖物資料表，只用來讓玩家看見未來聖物系統的線索與效果預告。

本階段不代表玩家已取得聖物，不新增 save 欄位，不影響角色能力，也不接入任何戰鬥公式。

## 目前資料結構

```python
RELICS = {
    relic_id: {
        "name": str,
        "summary": str,
        "source": str,
        "unlock": {
            "kind": "unlock" | "quest" | "flag" | "item" | "level",
            "key": str,       # level 以外需要
            "value": int,     # level 需要
            "label": str,
        },
        "effect_preview": str,
        "status": "preview",
    }
}
```

## 必填欄位

- `name`
- `summary`
- `source`
- `effect_preview`
- `status`

## 選填欄位

- `unlock`

## 型別與規則

- `status` 目前只支援 `"preview"`。
- `unlock.kind` 目前支援 `unlock`、`quest`、`flag`、`item`、`level`。
- `unlock.label` 是 UI 顯示用文字。
- `unlock` 只代表 preview 顯示條件或提示，不代表取得條件已實作。

## 引用規則

- `unlock.kind == "unlock"` 時，`key` 必須能由既有 unlock producer 產生。
- `unlock.kind == "quest"` 時，`key` 必須存在於 `QUESTS`。
- `unlock.kind == "flag"` 時，`key` 必須存在於已知 flag key。
- `unlock.kind == "item"` 時，`key` 必須存在於 `ITEMS`、`EQUIPMENT` 或 `MATERIALS`。
- `unlock.kind == "level"` 時，需使用正整數 `value`。

## 未來注意事項

- 若要實作取得狀態，才評估新增 `state["relics"]` 與 save migration。
- 若要實作聖物效果，才評估接入 `get_stats()` 或戰鬥傷害計算。
- 本階段不得讓聖物改變裝備 stats、戰鬥數值、陷阱傷害或元素倍率。
