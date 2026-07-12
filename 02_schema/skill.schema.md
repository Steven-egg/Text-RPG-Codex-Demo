# skill.schema

## 資料來源

- `04_data/data/skills.py`
- Runtime 常數：`SKILLS`

## 目前資料結構

### damage

```python
{
    "name": str,
    "mp": int,
    "kind": "damage",
    "stat": "attack" | "magic",
    "element": str,
    "multiplier": float,
    "crit_bonus": int,  # optional
    "desc": str,
}
```

### dot

```python
{
    "name": str,
    "mp": int,
    "kind": "dot",
    "stat": "magic",
    "element": str,
    "duration": int,
    "multiplier": float,
    "desc": str,
}
```

### regen

```python
{
    "name": str,
    "mp": int,
    "kind": "regen",
    "duration": int,
    "amount": int,
    "multiplier": float,
    "desc": str,
}
```

### heal

```python
{
    "name": str,
    "mp": int,
    "kind": "heal",
    "amount": int,
    "desc": str,
}
```

### buff

```python
{
    "name": str,
    "mp": int,
    "kind": "buff",
    "buff": str,
    "duration": int,
    "desc": str,
}
```

### debuff

```python
{
    "name": str,
    "mp": int,
    "kind": "debuff",
    "debuff": str,
    "duration": int,
    "desc": str,
}
```

## 必填欄位

- 全類型共通：`name`、`mp`、`kind`、`desc`
- `damage`：`stat`、`element`、`multiplier`；可選 `on_hit` 用於物理附加效果。
- `heal`：`amount`
- `buff`：`buff`、`duration`
- `debuff`：`debuff`、`duration`

## 選填欄位

- `damage.crit_bonus`

## 引用規則

- `JOBS.base_skills` 必須引用 `SKILLS`。
- `MAGIC_BOOKS.skill` 必須引用 `SKILLS`。
- `state.learned_skills` 必須引用 `SKILLS`。

## 維護規則

- `kind` 決定 engine 走哪種處理流程。
- 目前支援的 buff/debuff key：`defense_up`、`defense_down`、`quickstep`、`cinder_mark`、`burn`。
- 新增 buff/debuff 時，需同步更新 `get_stats()`、`tick_effects()`、傷害計算、validation 與此 schema。

## 未來注意事項

目前直接攻擊與魔法效果皆為 100% 命中；物理附加效果使用角色 `effect_accuracy` 與目標 `physical_status_resist` 判定。
