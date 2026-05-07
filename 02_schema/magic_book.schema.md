# magic_book.schema

## 資料來源

- `04_data/data/skills.py`
- Runtime 常數：`MAGIC_BOOKS`

## 目前資料結構

```python
MAGIC_BOOKS = {
    book_id: {
        "name": str,
        "jobs": list[job_id],
        "level": int,
        "price": int,
        "materials": dict[material_id, qty],
        "skill": skill_id,
    }
}
```

## 必填欄位

- `name`
- `jobs`
- `level`
- `price`
- `materials`
- `skill`

## 選填欄位

目前無選填欄位。

## 引用規則

- `jobs` 內的 job id 必須存在於 `JOBS`。
- `materials` key 必須存在於 `MATERIALS`。
- `skill` 必須存在於 `SKILLS`。
- 同一個 skill 原則上不應由多本魔法書重複教學，除非明確設計成不同版本。

## 未來注意事項

- 折扣邏輯目前寫在 `magic_book_price()`，例如 `book_spark` 完成 `quest_magic_crystal` 後折價。
- 未來折扣規則增加時，建議資料化，不要在 engine 裡大量硬寫 book id。
