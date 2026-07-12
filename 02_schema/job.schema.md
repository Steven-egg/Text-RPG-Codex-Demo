# job.schema

## 資料來源

- `04_data/data/jobs.py`
- Runtime 常數：`JOBS`

## 目前資料結構

```python
JOBS = {
    job_id: {
        "base": dict[stat_key, int],
        "growth": dict[stat_key, int],
        "extra_every_3": dict[stat_key, int],
        "base_skills": list[skill_id],
    }
}
```

目前 `job_id` 直接使用中文職業名稱，例如 `劍士`、`法師`。

## 必填欄位

- `base.max_hp`
- `base.max_mp`
- `base.attack`
- `base.defense`
- `base.agility`
- `base.magic_attack`
- `base.magic_defense`
- `base.effect_accuracy`
- `base.crit`
- `growth.max_hp`
- `growth.max_mp`
- `growth.attack`
- `growth.defense`
- `growth.agility`
- `extra_every_3`
- `base_skills`

## 選填欄位

目前無選填欄位。

## 型別與規則

- 所有 stat 數值皆為 `int`。
- `effect_accuracy`、`crit` 是百分比數字；效果命中僅用於物理附加狀態，直接攻擊與魔法效果皆為必中。
- `base_skills` 內的 skill id 必須存在於 `SKILLS`。

## 未來注意事項

- 中長期建議改成 stable id，例如 `job_warrior`、`job_mage`，再用 `name` 存顯示文字。
- 新增職業時，需同步檢查裝備 `jobs`、魔法書 `jobs`、初始技能與 README。
