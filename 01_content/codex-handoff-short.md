# Codex Handoff Short

用途：新 session 優先讀取的短交接。只放目前穩定狀態、禁止事項與下一步邊界；詳細歷史請需要時再讀 `01_content/codex-session-snapshot.md`。

## 最新穩定狀態

- 專案是 Python CLI 文字冒險 RPG《元素迷宮：邊境冒險者》。
- 最近 live bridge 基準 commit 是 `4acd04d [antig] feat(gui): add combat skill button live bridge`。
- v1 第一幕可通關；第二幕火系 demo 已進 runtime。
- 灰燼裂谷、灰燼守衛 Boss MVP、補給線升級、燼印深窟、燼印鎮衛 Boss MVP 已完成。
- `quest_supply_upgrade` 已素材化：需要 `mat_flame_stone_refined x3` 與 `mat_lava_shard x2`，完成後取得 `item_potion_m x2`，並解鎖旅人小鋪販售中藥水。
- 中藥水已在燼印鎮衛 Boss 戰中確認有實戰價值；目前不再調 Boss 數值。
- CLI UI MVP 已推進到核心循環 Rich `Panel` 薄層：主選單、角色狀態、城鎮整備、迷宮選擇、迷宮探索、戰鬥指令與結算都已整理出狀態 / 提示 / 行動區；不改 gameplay flow、data、schema、save 或 combat formula。
- Combat UI Log Separation MVP 已完成：戰鬥動作改為產出事件文字，由 `combat()` 統一渲染 1-3 行回合摘要與戰後 `Battle Log`，主畫面只保留當前決策所需狀態與上一動短摘要。
- Start Screen MVP 已完成：啟動時顯示標題與最小進入選項；有存檔時提供「重新開始 / 載入進度」，無存檔時提供「開始新冒險」；只取 UI 範本架構，不做背景圖或新 UI framework。
- Travel Shop Catalog MVP 已完成：旅人小鋪改為專屬分類商店流程，顯示分類、持有數、價格、商品詳情與購買確認；其他商店仍維持原流程。
- Workshop Catalog MVP 已完成：鐵刃工坊與堅甲工坊改為專屬 catalog 流程，分成購買、強化與我的裝備；顯示職業可用性、裝備狀態、強化基底與素材狀態；其他商店不變。
- Magic Shop Catalog MVP 已完成：星燈魔法商店改為專屬 catalog 流程，依魔法功能分類，顯示學習狀態、職業 / 等級 / 素材條件、MP、價格與技能效果；其他商店不變。
- Synthesis Catalog MVP 已完成：米菈合成屋改為專屬 catalog 流程，分成全部、裝備與戰術道具；顯示可製作狀態、產出、持有 / 裝備狀態、基底裝備、素材狀態、最多可製作次數、金幣與合成確認；不新增配方或改變合成規則。
- v0.2-2 技能系統最小版已完成收尾，Final Smoke Test：PASS；完成背包選單整併、初始背包正式化、寶箱技能書 MVP 化、技能書使用、技能學習、戰鬥施放與 MP 消耗正常。
- 「Element Decay 引擎」不是正式專案術語，不納入正式紀錄。
- GUI HTML static prototype 已進入可互動驗證階段，位置在 `07_gui_prototype/`；目前包含 Start Screen、Town Hub、Guild Screen、Synthesis Screen、World Map、Dungeon Exploration、Combat Screen、Shop Screen、Workshop Screen、Storage Screen、Magic Shop Screen、Inn Screen、Temple Screen、Relic Preview Screen 十四個畫面。
- static prototype 只使用 fixtures 驗證 render layer、layout、互動與 UIAction logging；不接 Python runtime、不讀寫 `save.json`、不修改 runtime / data / schema / combat formula、不啟動正式 asset pipeline。
- GUI runtime bridge blessed live slice 已落地並手測通過，範圍目前包含 Start Screen、Town Hub、Inn Screen、World Map、受限 Dungeon / Combat loop、World Map utility preview、Guild Report MVP 與 Combat Skill Button Live MVP；其中 `back_to_town_hub` 只保留在城鎮節點 / detail action，不在 World Map 主選單。
- Combat Loop Completion Slice v0 已完成並提交於 `be6b06c [antig] feat(gui): complete live combat loop feedback`：Combat victory result overlay 會顯示 EXP、Gold、drops、bestiary 與 level up；victory 後可回 Dungeon Exploration；route clear / resolved state 已有最小呈現；終點狀態停用 `advance_step`，並以「離開迷宮」返回 World Map。
- 本輪 Combat Loop Completion 只修改 `03_engine/engine/gui_actions.py`；未修改 `03_engine/engine/game.py`、`04_data/`、`02_schema/`、`save.json` 或 combat formula。defeat / retreat routing 未回歸。
- Guild Report / Dungeon Clear Reward MVP 已完成並提交於 `c2052d4 [antig] feat(gui): add guild clear report live bridge`：Live Town Hub 可進入 Guild；Guild Screen live bridge 顯示 runtime 已解鎖迷宮的通關 / 回報狀態；當玩家流程滿足工會任務狀態、解鎖條件與通關條件，且尚未回報時，可執行回報登記。
- Guild report 只設定 `state.flags["guild_reported_<dungeon_id>"] = True`，用於登記 / 顯示回報狀態；首次通關 reward 仍在 route clear 當下發放，Guild report 不重複發 clear reward，也不搬移 reward 發放時間點。
- Guild MVP 保留 static fixture fallback；後續 follow-up 已移除 fire mark / Noah / story_hint active bridge 殘影，只保留 hidden placeholder。這不代表完整 guild system、正式 quest framework、reputation、achievement 或正式任務系統已完成。
- Combat Skill Button Live MVP 已完成並提交於 `4acd04d [antig] feat(gui): add combat skill button live bridge`：GUI live bridge 新增 `use_skill` routing；Combat ScreenModel 依照 `state["learned_skills"]` 與既有 `SKILLS` 產生 `skill_menu`；技能按鈕依目前 MP、已學技能與戰鬥是否結束計算 enabled / disabled_reason。
- Combat Skill Button Live MVP 的 gameplay 判斷在 Python server-side：檢查 `skill_id` 是否已學、技能是否存在於既有 `SKILLS`、MP 是否足夠；MP 不足回 409 blocked，MP 扣減也在 server-side。damage / heal / buff / debuff 沿用既有 runtime 行為與資料，前端 JavaScript 不握 gameplay 決定權。
- Combat Skill Button Live MVP 只修改 `03_engine/engine/gui_actions.py`；未修改 `03_engine/engine/game.py`、`04_data/`、`02_schema/`、`save.json` 或 combat formula；不新增正式 skill system、skill framework、target selection、技能重平衡或大型 combat 重構。
- `load_demo_seed` 保留為 backend smoke/helper，不再顯示為 live Start Screen 主要入口；live Start Screen copy / no-save / has-save 狀態已對齊 static Start Screen。
- Town Hub live 不再顯示 `save_game`；World Map 主選單保留 `save_game`，新增 shell-only `open_settings`，移除主選單 `back_to_town_hub`。
- `start_gui_runtime_bridge_server.bat` 可啟動 local live test server；使用者手測重新開啟 bat 後，新狀態重新開始、在 World Map 主選單存檔、回到標題後繼續遊戲，runtime 狀態可保留，無 traceback 或 fatal error。
- Blessed live slice 仍以 Python runtime 為 gameplay authority；GUI JavaScript 只 dispatch UIAction 並 render ScreenModel。Guild 目前只完成 clear report MVP；Dungeon / Combat 目前只完成已批准的 traversal / combat loop 小切片與 Combat Skill Button Live MVP，不代表完整 guild system、quest framework、skill system、skill framework、target selection、boss framework、inventory / equipment interaction、facility family 或完整 dungeon framework 已開放。
- Live bootstrap log naming cleanup 已完成：Start、Town Hub、Inn、World Map 在 live 成功載入時記錄 `live_screen_loaded` / `live_loader`，payload 帶 `mode: "live"` 與 `screen_id`；static fixture load 與 live fallback 仍保留 `fixture_loaded`，fallback 仍會另外記 `live_bridge_unavailable`。
- 手測後已完成本輪 live Start Screen copy / entry state 與 Town Hub / World Map 主選單 placement 對齊；本 slice 不再有必做 follow-up。
- `save.gui-backup-*.json` 是 bridge save 前安全備份產物，已加入 `.gitignore`；不要手動讀寫 `save.json`。
- Inn Screen 與 Temple Screen 已完成 JRPG dialogue/menu static prototype 調整；mockup reference 只放在 `05_assets/gui_references/facility_inn_screen/` 與 `05_assets/gui_references/facility_temple_screen/`，不作 runtime asset。
- Start Screen alignment review 已通過；no-save / has-save fixtures、開始 / 讀取 / 重新開始入口、冒險者登錄 modal 與前往 World Map 的 static navigation 都維持 static-only 邊界。
- Combat Screen static prototype 已有底部 5 指令、技能 / 道具 floating popover、右側 Battle Log、Victory / Defeat / Retreat result preview fixtures，以及整合在 Combat Screen 內的中央 Combat Result overlay。
- Combat Result overlay 不新增獨立 Combat Result Screen；勝利 / 撤退下一步回 Dungeon Exploration，戰敗下一步回 Town Hub。Combat Screen 第一輪 mockup-alignment layout tuning pass 已完成，不再是目前下一步主線。
- Dynamic Traversal Continuity v1 方向已討論並同意，規格記錄在 `01_content/gui-dynamic-traversal-continuity-v1-spec.md`：GUI live mode 應以 CLI traversal semantics 與 static UX shell 為準；combat victory / successful combat retreat 回同一個 `dungeon_exploration`，combat defeat 回 `town_hub`，`dungeon_exploration` retreat 回 `world_map`；玩家主 UI 改中文 RPG 語氣，工程字眼只留 log/debug。此規格不是 runtime 施工批准。
- Synthesis Screen static prototype 已建立並完成基礎版面定案：左側分類 / 配方列表、中央配方詳情與需求缺口決策流、右側米菈視覺區、底部提示與合成 action；未來正式 bridge 或 UI 圖片 / portrait 貼入時若出現問題再調整。
- Shop Screen static prototype v1 已建立：使用 static fixtures 驗證商品分類、商品詳情、價格 / 持有數 / 庫存顯示、`buy_item`、blocked state、`back_to_town_hub` 與 UIAction logging；不消耗金幣、不改背包、不接 runtime。
- Workshop Screen static prototype v1 已建立：使用 static fixtures 驗證購買 / 強化 tab、裝備詳情、職業 / 金幣 / 材料限制、`buy_equipment`、`upgrade_equipment`、blocked state、`back_to_town_hub` 與 UIAction logging；不消耗素材、不改裝備、不接 runtime。
- UI 下一階段仍共用 Screen Map、ScreenModel 與 UIAction；CLI / Rich、HTML static prototype 與未來正式 GUI 的差異只在 render layer。
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

以 `01_content/agent-startup-reading-list.md` 的 Hot Zone / Task Zone / Cold Zone 規則為準。

Hot Zone 啟動必讀：

1. `AGENTS.md`
2. `01_content/agent-startup-reading-list.md`
3. 專案內目前有效的 `SKILL.md`（Codex 讀 `.codex/skills/element-maze-session-ops/SKILL.md`，Antigravity 讀 `.antigravity/skills/element-maze-session-governance/SKILL.md`）
4. `README.md`
5. `01_content/codex-handoff-short.md`

GUI static prototype 任務需再讀目前 agent 對應的 GUI skill。`01_content/gui-html-static-prototype-progress-v1.md` 只在需要 GUI screen 細節或驗證紀錄時讀取相關段落，不列入 Hot Zone 啟動必讀。

Task Zone 只在任務需要時選讀，例如 GUI planning、drift audit 或 task routing 才讀 `01_content/gui-planning-index.md`；需要流程或畫面地圖時才讀 `01_content/ui-flow-blueprint.md`、`01_content/gui-screen-map.md` 或對應 `07_gui_prototype/<screen>/`。

Cold Zone 不在新 session 啟動時主動大量讀取；需要詳細歷史、第二幕規劃、長期幕次、demo polish 或架構背景時，才依使用者明確指示讀取對應文件。

## 下一步邊界

- Blessed GUI runtime bridge live slice 已完成 normalization、Start Screen / entry state 對齊、Town Hub / World Map 主選單 placement cleanup、World Map utility read-only preview、Combat Loop Completion Slice v0、Guild Report / Dungeon Clear Reward MVP，以及 Combat Skill Button Live MVP；下一步仍需由使用者指定單一小切片，不自動擴張 runtime bridge。
- 教會查閱結果 MVP 已完成，不要再列為待做。
- 火印熔爐、完整火印、火印守護 Boss、正式聖物、正式轉職、八元素、Act 3 都只能視為未來願景；不是當前下一步。
- runtime UI 仍以 CLI / Rich 行為語意為準；GUI live mode 若後續施工，應沿用 static UX shell 並透過 Python bridge 注入 ScreenModel，不要重構 `game.py`。
- Combat Skill Button Live MVP 已完成，不再列為待評估或待施工項；若未來要超出按鈕 live MVP，仍需另開單一小切片與 read-only planning gate。
- HTML static prototype 只允許在 `07_gui_prototype/` 內用 fixtures 小步調整，不讀寫 save、不接 Python、不複製 gameplay logic 到 JS。
- Synthesis Screen、Shop Screen、Workshop Screen、Storage Screen、Magic Shop Screen、Inn Screen、Temple Screen、Relic Preview Screen static prototype v1 目前都已完成，不再作為未完成候選；Inn Screen 與 Temple Screen 已完成 JRPG dialogue/menu static prototype 調整。
- 下一個 UI 任務需由使用者指定單一小切片。不得把 Guild Report MVP 擴張成完整 guild system、正式 quest framework、reputation 或 achievement；不得把 Combat Skill Button MVP 擴張成正式 skill system、skill framework、target selection、技能重平衡或大型 combat 重構；不得擴張 Shop、Workshop、Synthesis、Storage、Magic Shop、Temple、Relic、完整 boss / inventory / equipment / dungeon framework；不讀寫 `save.json`、不修改 data / schema / combat formula、不啟動 formal asset pipeline，也不要把 reference/mockup 圖當 runtime asset。
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

本輪 blessed GUI runtime bridge live slice cleanup 已確認：
- `python -m py_compile 03_engine/engine/gui_actions.py`：PASS
- live model smoke：Town Hub navigation 只剩 `open_world_map`；World Map 主選單含 `save_game` / `open_settings` 並移除 `back_to_town_hub`；Start Screen no-save / has-save 入口對齊 static；新遊戲 fallback 名稱為 `見習冒險者`：PASS
- `node --check 07_gui_prototype/start_screen/start-screen.js`：PASS
- `node --check 07_gui_prototype/world_map/world-map.js`：PASS
- `06_tools/validate_data.py`：PASS
- `element_maze.py --smoke-test`：PASS
- bridge HTTP smoke：PASS
- `git diff --check`：PASS，僅 CRLF warning
- 使用者手測重新開啟 bat、新狀態重新開始、在 World Map 主選單存檔、回到標題後繼續遊戲：PASS，runtime 狀態可保留，無 traceback 或 fatal error

本輪 Combat Loop Completion Slice v0 已確認：
- `python -m py_compile 03_engine/engine/gui_actions.py`：PASS
- `python 06_tools/validate_data.py`：PASS
- `python element_maze.py --smoke-test`：PASS
- `git diff --check`：PASS，僅 CRLF warning
- 使用者手測 World Map → Dungeon Exploration → Combat → victory result overlay → 返回探索 → route clear / resolved state → 離開迷宮回 World Map：PASS
- 使用者手測 victory overlay 顯示金幣、經驗、掉落物、圖鑑提示與 level up：PASS
- defeat / retreat routing 未回歸；本輪只修改 `03_engine/engine/gui_actions.py`，未修改 `game.py`、`04_data/`、`02_schema/`、`save.json` 或 combat formula

本輪 Guild Report / Dungeon Clear Reward MVP 已確認：
- `python -m py_compile 03_engine/engine/gui_actions.py`：PASS
- `node --check 07_gui_prototype/guild_screen/guild-screen.js`：PASS
- `git diff --check`：PASS，僅 CRLF warning
- `python 06_tools/validate_data.py`：PASS
- `python element_maze.py --smoke-test`：PASS
- 使用者手測：初次進 Guild 時因任務 / 解鎖條件尚未滿足，不能直接完成回報；打一輪 dungeon 後回 Guild，任務 / 回報狀態解鎖並成功完成回報流程
- 語意確認：Guild report 只登記 `guild_reported_<dungeon_id>` 狀態；首次通關 reward 仍在 route clear 當下發放，不由 Guild report 重複發放

本輪 Combat Skill Button Live MVP 已確認：
- `python -m py_compile 03_engine/engine/gui_actions.py`：PASS
- `python 06_tools/validate_data.py`：PASS
- `python element_maze.py --smoke-test`：PASS
- `node --check 07_gui_prototype/combat_screen/combat-screen.js`：PASS
- Codex bundled `node.exe --check 07_gui_prototype/combat_screen/combat-screen.js`：PASS
- `git diff --check`：PASS
- 使用者手測：Combat Skill Button Live MVP 已以盜賊／刺客路線完成一輪 E2E 手測；可進入 live bridge 流程與戰鬥；盜賊／刺客技能可使用並消耗 MP；MP 消耗完後技能無法再使用；可透過技能戰鬥取得 EXP；level up 會觸發 HP/MP 回滿；戰鬥後可返回 Dungeon Exploration，後續可回 World Map / Town Hub / Guild / Inn / Save，未發現明顯 routing regression；劍士、法師、牧師與其他職業技能分支仍待後續補測
- 語意確認：`use_skill` gameplay authority 在 Python server-side；沿用既有 `SKILLS` / `learned_skills` / runtime combat flow；未新增正式 skill system、skill framework、target selection，也未修改 `game.py`、data、schema、save 或 combat formula

本輪 live bootstrap log naming cleanup 已確認：
- Start / Town Hub / Inn / World Map live 成功載入 log 改為 `live_screen_loaded`：PASS
- Live 成功路徑不再誤顯示 `fixture_loaded` 或 `live_bridge_unavailable`：PASS
- Static-server fallback 仍保留 `fixture_loaded` 並正確顯示 `live_bridge_unavailable`：PASS
- 4 個 blessed screen JavaScript syntax checks：PASS
- `git diff --check`：PASS，僅 CRLF warning

本輪 Magic Shop Catalog MVP 已確認：
- Python 語法編譯
- `06_tools/validate_data.py`
- `element_maze.py --smoke-test`
- `git diff --check`
- 額外魔法商店探針：分類、詳情、學習魔法書、金幣 / 素材 / 已學技能更新正常

本輪 Synthesis Catalog MVP 已確認：
- Python 語法編譯
- `06_tools/validate_data.py`
- `element_maze.py --smoke-test`
- `git diff --check`
- 額外合成屋探針：分類、詳情、可製作狀態、最多可製作次數、合成配方、金幣 / 素材 / 基底裝備 / 產出更新正常

本輪 GUI HTML static prototype 已確認：
- Start Screen / Town Hub / Guild / Synthesis / World Map / Dungeon Exploration / Combat Screen / Shop Screen / Workshop Screen / Storage Screen / Magic Shop Screen 皆只用 static fixtures。
- Start Screen alignment review 已通過；Synthesis / Shop / Workshop / Storage / Magic Shop static prototype v1 已落地，目前不應回到已定案畫面做無指名重工。
- Dungeon Exploration 的 `Fixed Encounter Preview` 可導向 Combat Screen static prototype。
- Combat Screen skill / item popover、Battle Log、Victory / Defeat / Retreat result overlay 與 result next navigation 已完成互動驗證。
- Combat Screen 第一輪 mockup-alignment layout tuning pass 已完成；後續若有調整，應視為使用者 review 後的小幅微調。
- 最近機器檢查：Combat Screen JS syntax OK；Combat Screen JSON fixtures parse OK。

本輪 Workshop Catalog MVP 已確認：
- Python 語法編譯
- `06_tools/validate_data.py`
- `element_maze.py --smoke-test`
- `git diff --check`
- 額外工坊探針：購買武器、強化武器、購買防具、強化防具的金幣 / 背包更新正常

本輪 Travel Shop Catalog MVP 已確認：
- Python 語法編譯
- `06_tools/validate_data.py`
- `element_maze.py --smoke-test`
- `git diff --check`
- 額外旅人小鋪探針：分類、詳情、購買 1 個與金幣 / 持有數更新正常

本輪 Start Screen MVP 已確認：
- Python 語法編譯
- `06_tools/validate_data.py`
- `element_maze.py --smoke-test`
- `git diff --check`
- 額外入口探針：無存檔時可選「開始新冒險」，有存檔時可選「載入進度」

前一輪 Combat UI Log Separation MVP 已確認：
- Python 語法編譯
- `06_tools/validate_data.py`
- `element_maze.py --smoke-test`
- `git diff --check`
- 額外非互動戰鬥探針：普通攻擊戰可跑完，回合摘要與 Battle Log 正常輸出

建議下一個穩定節點 commit message：`docs(gui): sync combat skill bridge handoff`
