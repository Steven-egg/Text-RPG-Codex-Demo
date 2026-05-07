# promotion.schema

## 資料來源

- `04_data/data/promotions.py`
- Runtime 常數：`PROMOTIONS`

## 目前用途

`PROMOTIONS` 目前是 preview-only 的轉職預告資料表，只供轉職神殿顯示未來職業方向與條件狀態。

本階段不代表角色可以真正轉職：

- 不新增 save 欄位。
- 不修改 `state["job"]`。
- 不影響 `get_stats()`。
- 不影響戰鬥能力、技能、裝備限制或等級成長。
- 未來真正轉職時，才評估是否新增 `state` 欄位或正式職業資料。

## 目前資料結構

```python
PROMOTIONS = {
    promotion_id: {
        "source_job": job_id,
        "name": str,
        "summary": str,
        "requirements": list[requirement],
        "status": "preview",
    }
}
```

### requirement

```python
{"kind": "level", "value": int, "label": str}
{"kind": "unlock", "key": unlock_key, "label": str}
{"kind": "quest", "key": quest_id, "label": str}
{"kind": "flag", "key": flag_key, "label": str}
{"kind": "item", "key": item_id | equipment_id | material_id, "label": str}
```

## 必填欄位

- `source_job`
- `name`
- `summary`
- `requirements`
- `status`

## 選填欄位

目前無選填欄位。

## 引用規則

- `source_job` 必須存在於 `JOBS`。
- `requirements.kind == "unlock"` 時，`key` 必須是已知 unlock producer。
- `requirements.kind == "quest"` 時，`key` 必須存在於 `QUESTS`。
- `requirements.kind == "flag"` 時，`key` 必須存在於 registry 的 known flag。
- `requirements.kind == "item"` 時，`key` 必須存在於 `ITEMS`、`EQUIPMENT` 或 `MATERIALS`。
- 不要求轉職後名稱存在於 `JOBS`，避免誤導成已可真正轉職。

## 維護規則

- `status` 目前只支援 `"preview"`。
- 轉職神殿只能讀取並顯示條件，不提供確認轉職選項。
- 新增 requirement kind 時，需同步更新 `temple()` 顯示 helper、`06_tools/validate_data.py` 與本 schema。
