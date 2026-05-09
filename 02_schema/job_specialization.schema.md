# job_specialization.schema

## 資料來源

- `04_data/data/job_specializations.py`
- Runtime 常數：`JOB_SPECIALIZATIONS`

## 目前用途

`JOB_SPECIALIZATIONS` 目前是 preview-only 的職業特化預告資料表，只供角色狀態頁顯示目前基礎職業的未來特化方向。

本階段不代表職業特化能力已啟用：

- 不新增 save 欄位。
- 不新增 `state["job_specialization"]` 或其他特化狀態欄位。
- 不修改 `state["job"]`。
- 不開放玩家選擇職業特化。
- 不影響 `get_stats()`。
- 不影響戰鬥能力、技能效果、裝備限制、魔法書限制或等級成長。

## 目前資料結構

```python
JOB_SPECIALIZATIONS = {
    specialization_id: {
        "source_job": job_id,
        "name": str,
        "summary": str,
        "identity": str,
        "effect_preview": str,
        "status": "preview",
    }
}
```

## 必填欄位

- `source_job`
- `name`
- `summary`
- `identity`
- `effect_preview`
- `status`

## 選填欄位

目前無選填欄位。

## 引用規則

- `source_job` 必須存在於 `JOBS`。
- `status` 目前只支援 `"preview"`。
- `effect_preview` 只能描述未來可能方向，不代表已實作或已生效能力。

## 維護規則

- 角色狀態頁顯示時必須明確標註「職業特化預覽」與「目前尚未生效」。
- 不得在轉職神殿顯示職業特化，避免與 `PROMOTIONS` 混淆。
- 新增正式特化機制前，不得讓本資料表影響 save schema、角色數值、戰鬥公式、技能、裝備限制或魔法書限制。
