# Codex Handoff Short

用途：新 session 優先讀取的短交接。只放目前穩定狀態、禁止事項與下一步邊界；詳細歷史請需要時再讀 `01_content/codex-session-snapshot.md`。

## 最新穩定狀態

- 專案是 Python CLI 文字冒險 RPG《元素迷宮：邊境冒險者》。
- v1 第一幕可通關；第二幕火系 demo 已進 runtime。
- 灰燼裂谷、灰燼守衛 Boss MVP、補給線升級、燼印深窟、燼印鎮衛 Boss MVP 已完成。
- `quest_supply_upgrade` 已素材化：需要 `mat_flame_stone_refined x3` 與 `mat_lava_shard x2`，完成後取得 `item_potion_m x2`，並解鎖旅人小鋪販售中藥水。
- 中藥水已在燼印鎮衛 Boss 戰中確認有實戰價值；目前不再調 Boss 數值。

## 火印第一章前置閉環

- 第 1 枚 `key_fire_mark_shard` 來自葛倫線。
- 第 2 枚來自灰燼守衛，使用 `ash_guardian_defeated` 防重複領取。
- 第 3 枚來自燼印鎮衛，使用 `cinder_seal_sentinel_defeated` 防重複領取。
- 玩家持有 3 枚碎片後，可在冒險者工會詢問諾亞，完成後設定 `fire_mark_guild_inquiry_done`。
- 完成工會詢問、仍持有 3 枚碎片且尚未觸發神殿接橋時，第一次進入轉職神殿會觸發賽恩一次性對話，完成後設定 `fire_mark_church_bridge_done`。
- 完成神殿接橋後，可取得教會查閱結果，完成後設定 `fire_mark_church_lookup_done`。
- 教會查閱結果確認：三枚碎片是「未完成的火之印記核心」。

## 火印定位

- demo 第一章火印線的收束不是「玩家掌握完整火印力量」。
- demo 第一章火印線的收束是：玩家取得三枚碎片，經工會與神殿確認，得知其真相為「未完成的火之印記核心」。
- 火之印記目前不是正式聖物。
- 火之印記目前定位為第一章主線成果物、未來正式聖物的零組件／核心材料，以及劇情上的重要印記。
- 目前不提供火印裝備、啟用、升級、戰鬥效果或正式聖物效果。
- 教會目前只做查閱、確認與交還／封存，不做正式合成與啟用。

## 明確仍未開放

- 完整火之印記。
- 火印熔爐 dungeon。
- 具名火印守護 Boss / 火印爐衛 Boss。
- 正式合成／啟用火之印記。
- 正式教會火印流程。
- 正式聖物取得、裝備、效果、升級。
- 正式轉職與正式職業特化效果。
- 八元素 runtime 與完整屬性克制。
- `offhand` slot。
- 通用 Boss framework。
- save/schema 改動。
- combat formula 改動。
- Act 3 文件或 runtime 內容。

## 新 Session 讀檔順序

1. `01_content/codex-handoff-short.md`
2. `README.md`
3. 需要詳細歷史時再讀 `01_content/codex-session-snapshot.md`
4. 需要第二幕規劃脈絡時再讀 `01_content/act-2-content-plan.md`
5. 需要長期幕次脈絡時再讀 `01_content/full-act-structure.md`
6. 需要架構或玩法背景時再讀 `01_content/game-architecture.md`、`01_content/game-design.md`、`01_content/combat-growth-layering-plan.md`

## 下一步邊界

- 目前沒有已批准的下一個 runtime 施工目標。
- 教會查閱結果 MVP 已完成，不要再列為待做。
- 火印熔爐、完整火印、火印守護 Boss、正式聖物、正式轉職、八元素、Act 3 都只能視為未來願景；不是當前下一步。
- 若未來要繼續 gameplay，仍需先做單一小切片 read-only 邊界確認，再由使用者明確批准施工範圍。
- 文件同步輪只改 markdown，不改 runtime / data / schema / save / combat formula。

## 最新驗證

- `run_checks.bat` 仍可能因 PATH 找不到 `python` 失敗。
- 已用 bundled Python 補跑：
  - `06_tools/validate_data.py`：`data validation ok`
  - `element_maze.py --smoke-test`：`smoke test ok`

建議穩定節點 commit message：`Complete fire mark church inquiry flow`
