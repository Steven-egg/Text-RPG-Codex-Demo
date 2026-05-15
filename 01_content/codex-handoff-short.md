# Codex Handoff Short

用途：新 session 優先讀取的短交接。只放目前穩定狀態、禁止事項與下一步邊界；詳細歷史請需要時再讀 `01_content/codex-session-snapshot.md`。

## 最新穩定狀態

- 專案是 Python CLI 文字冒險 RPG《元素迷宮：邊境冒險者》。
- v1 第一幕可通關；第二幕火系 demo 已進 runtime。
- 灰燼裂谷、灰燼守衛 Boss MVP、補給線升級、燼印深窟、燼印鎮衛 Boss MVP 已完成。
- `quest_supply_upgrade` 已素材化：需要 `mat_flame_stone_refined x3` 與 `mat_lava_shard x2`，完成後取得 `item_potion_m x2`，並解鎖旅人小鋪販售中藥水。
- 中藥水已在燼印鎮衛 Boss 戰中確認有實戰價值；目前不再調 Boss 數值。
- CLI UI MVP 已推進到核心循環 Rich `Panel` 薄層：主選單、角色狀態、城鎮整備、迷宮選擇、迷宮探索、戰鬥指令與結算都已整理出狀態 / 提示 / 行動區；不改 gameplay flow、data、schema、save 或 combat formula。
- 手動測試回饋後已修正迷宮 Boss/gate 提示混雜問題，Boss 狀態現在放在各迷宮選項；背包補上用途提示，旅館改為專屬 panel。
- 第二輪手動回饋後，城鎮第 9 項已簡化為純倉庫入口；工會、工坊、商店、魔法書、合成與倉庫開始比照旅館走專屬設施 panel。工會內部已補可交付、進行中委託與 Boss 挑戰狀態提示。
- UI 完成後再處理的 demo 遊玩體驗、平衡、任務引導與內容節奏 polish，已集中記錄在 `01_content/demo-playtest-notes.md`；它不是目前 runtime 施工清單。
- `06_tools/content_inventory_report.py` 已作為 read-only 內容盤點工具納入 README 說明，不是 validation 替代品。

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
6. 需要 UI 完成後的 demo polish backlog 時再讀 `01_content/demo-playtest-notes.md`
7. 需要架構或玩法背景時再讀 `01_content/game-architecture.md`、`01_content/game-design.md`、`01_content/combat-growth-layering-plan.md`

## 下一步邊界

- 目前沒有已批准的下一個 runtime 施工目標。
- 教會查閱結果 MVP 已完成，不要再列為待做。
- 火印熔爐、完整火印、火印守護 Boss、正式聖物、正式轉職、八元素、Act 3 都只能視為未來願景；不是當前下一步。
- UI 目前只允許 CLI 顯示層薄包裝；可延續 `render_panel()` / `action_menu_panel()` 做小步 panel 化，不要擴張成 UI framework、Unity 或 HTML UI。
- `content_inventory_report.py` 只做 read-only 盤點；不要把 report 輸出當成 SSOT 或 gameplay 變更依據。
- 若未來要繼續 gameplay，仍需先做單一小切片 read-only 邊界確認，再由使用者明確批准施工範圍。
- 若使用者指定文件同步輪，只改 markdown，不改 runtime / data / schema / save / combat formula。

## 最新驗證

- 使用者本機已補裝 `.venv`，並回報 `python element_maze.py --smoke-test` 成功。
- Codex 端直接使用 `.venv` 時遇到 WindowsApps Python stub 路徑限制；這是 Codex 沙盒環境問題，不視為 gameplay 錯誤。
- Codex 已用 bundled Python 補跑：
  - `06_tools/validate_data.py`：`data validation ok`
  - `element_maze.py --smoke-test`：`smoke test ok`
  - `06_tools/content_inventory_report.py --json`：成功輸出 report

建議穩定節點 commit message：`Panelize core CLI loop screens`
