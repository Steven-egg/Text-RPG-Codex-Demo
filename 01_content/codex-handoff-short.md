# Codex Handoff Short

- `README.md` 是 project-level SSOT；專案採分層 SSOT，不是所有細節都塞在 README。
- 目前版本：Python CLI v1 playable vertical slice，可玩核心循環已完成；第二幕 Act 2 Slice 1 已進 runtime data。
- 目前專案階段：v1 第一幕完成，第二幕進入最小施工切片迭代。
- 目前已新增幕次總綱：`01_content/full-act-structure.md`。
- 目前已新增第二幕規劃：`01_content/act-2-content-plan.md`。
- 第二幕目前已完成 Act 2 Slice 1：灰燼裂谷偵查版已進 runtime data。
- 完成 `quest_boss_glen` 後會解鎖 `second_act_preview`、`unlock_act_2`、`unlock_ash_ravine`。
- 已新增 `dungeon_ash_ravine`、3 個普通怪與 3 個素材。
- Act 2 Entry Balance & Guidance Patch 已完成：葛倫小幅降壓、小魔晶掉落率提高、破甲釘新增即時傷害、灰燼裂谷改為 18 步、完成血跡地圖後會引導玩家接「灰燼裂谷偵查」。
- 玩家短測確認：破甲釘可造成傷害並正常觸發擊殺、經驗與金幣結算；小藥水、集中滴露、逃脫卷軸未觀察到被破甲釘補丁波及。
- 集中藥袋 special 裝備語意 bug 已修正：只有 `state["equipment"].get("special") == "special_focus_pouch"` 時，進入迷宮才會取得集中滴露並顯示訊息；見習徽章與其他 special 裝備不受影響。
- 灰燼裂谷難度暫不調整：玩家短測角色 Lv10、火抗 25%、裝備抗火斗篷，已高於推薦 Lv7-9；後續需以 Lv7-9、低裝或無抗火斗篷狀態另行測試。
- 灰燼裂谷目前沒有 Boss，`boss` 為 `None`。
- 灰燼守衛、完整火之印記、第二幕完整任務鏈、轉職神殿後續仍未實作。
- 下一步若沒有使用者明確改變方向，只允許做「第二幕下一個最小施工切片評估」或 `01_content/` 文件同步。
- 下一步優先做 Lv7-9 低裝或無抗火斗篷灰燼裂谷短測；若節奏正常，下一個建議施工切片仍應偏小：灰燼裂谷素材出口或最小火抗對策配方，不做完整第二幕。
- 不得實作整個第二幕。
- 不得修改 `03_engine/engine/game.py`，除非使用者明確要求且範圍極小；最近一次只為破甲釘即時傷害與偵查任務顯示做過小補丁。
- 不得修改 `04_data/data/*.py`，除非進入已批准的最小施工切片；目前文件同步輪不得修改 runtime data。
- 不得修改 `02_schema/*.schema.md`，除非先提出理由與最小修改範圍並獲得明確要求。
- 不得修改 `04_data/data/registry.py` 或 `06_tools/validate_data.py`，除非進入明確批准的 registry/validation 準備切片。
- 不得新增 `01_content/act-3-content-plan.md`；雖然灰燼裂谷偵查版已完成，仍需等灰燼守衛或完整火之印記流程完成最小驗證後再產生。
- 不得新增 act-3 runtime 內容。
- 不得處理 Element Decay。
- 不得重構 engine、不得遷移 Python dict 到 JSON/YAML。
- 不得把 `save.json` 當資料來源。

Drift check 可回貼：

```text
目前專案是《元素迷宮：邊境冒險者》Python CLI v1 playable vertical slice。README.md 是 project-level SSOT；01_content 是內容與架構規劃；full-act-structure.md 是五幕總綱；act-2-content-plan.md 是第二幕灰燼裂谷規劃；02_schema 是資料契約；04_data/data 是 runtime data；registry.py 是資料索引與 unlock/helper；engine/game.py 是 runtime 流程。v1 第一幕已完成且主線可通關；第二幕 Act 2 Slice 1 已完成，灰燼裂谷偵查版已進 runtime data，完成 quest_boss_glen 後會解鎖 unlock_act_2 與 unlock_ash_ravine，並可接「灰燼裂谷偵查」。入口平衡補丁已完成：葛倫小幅降壓、小魔晶較易取得、破甲釘有即時傷害、灰燼裂谷為 18 步；破甲釘短測已確認可正常觸發擊殺、經驗與金幣結算。集中藥袋已修正為 special 欄裝備時才生效。灰燼裂谷目前沒有 Boss；灰燼守衛、完整火之印記、第二幕完整任務鏈、轉職神殿後續仍未實作。下一步優先以 Lv7-9 低裝或無抗火斗篷狀態短測灰燼裂谷；若節奏正常，再評估素材出口或最小火抗對策配方。不得直接改 engine/schema，不得處理 Element Decay，不得新增 act-3-content-plan.md。
```

新 session 建議優先讀：

1. `01_content/codex-handoff-short.md`
2. `README.md`
3. `01_content/full-act-structure.md`
4. `01_content/act-2-content-plan.md`
5. `01_content/game-architecture.md`
6. `01_content/game-design.md`
7. 需要施工前評估時，再讀 `02_schema/`、`04_data/data/registry.py`、`06_tools/validate_data.py`
