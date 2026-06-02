# 《元素迷宮：邊境冒險者》終端機版

## 最新完成：GUI Runtime Bridge Combat Skill Button Live MVP（local live mode）

最近 GUI live bridge 基準 commit：`4acd04d [antig] feat(gui): add combat skill button live bridge`。

`07_gui_prototype/` 目前仍以 HTML static prototype 為預設模式；另外已落地一條明確受限的 local runtime-connected live slice，用來驗證 browser UIAction → Python bridge → runtime ScreenModel 的最小閉環。

Blessed live slice 已包含：

- Start Screen：`start_new_game`、`restart_game`、`load_game`；live 入口 copy / no-save / has-save 狀態已對齊 static Start Screen，`load_demo_seed` 保留為 backend smoke/helper，不再顯示為 live Start Screen 主要入口。
- Town Hub：live resource strip、facility nodes、`open_world_map`，並可進入 Guild live screen；Town Hub 不再顯示 `save_game`。
- Inn Screen：`rest_at_inn` 扣 30G 並由 Python runtime 回滿 HP/MP。
- World Map：沿用 static shell 顯示 runtime-backed location / route ScreenModel；主選單保留 `save_game` 與 shell-only `open_settings`，移除主選單 `back_to_town_hub`，返回城鎮只透過城鎮節點 / detail action。
- Guild Screen：live bridge 會顯示 runtime 已解鎖迷宮的通關 / 回報狀態；當玩家流程滿足工會任務狀態、解鎖條件與通關條件，且尚未回報時，可登記探索回報。

Combat Loop Completion Slice v0 已完成受限 live loop 收斂：

- World Map → Dungeon Exploration → Combat → victory / retreat / defeat routing 維持穩定；victory 與 successful retreat 回 Dungeon Exploration，defeat 回 Town Hub，Dungeon Exploration 的離開動作回 World Map。
- Combat victory result overlay 已補強 EXP、Gold、drops、bestiary 與 level up 顯示；level up 會提示 HP/MP 回滿。
- route clear / resolved state 已完成最小呈現；走到 `12 / 12` 這類終點狀態後，`advance_step` 會停用，原撤退 action 改為「離開迷宮」並返回 World Map。
- 本 slice 只修改 `03_engine/engine/gui_actions.py`；未修改 `03_engine/engine/game.py`、`04_data/`、`02_schema/`、`save.json` 或 combat formula。

Combat Skill Button Live MVP 已完成受限 live bridge 收斂，並已以盜賊／刺客路線完成一輪 E2E 手測：

- GUI live bridge 已新增 `use_skill` routing；Combat ScreenModel 會依照 `state["learned_skills"]` 與既有 `SKILLS` 產生 `skill_menu`。
- 技能按鈕會依目前 MP、已學技能與戰鬥是否結束計算 enabled / disabled_reason。
- gameplay 判斷在 Python server-side：檢查 `skill_id` 是否已學、技能是否存在於既有 `SKILLS`、MP 是否足夠；MP 不足回 409 blocked，MP 扣減也在 server-side。
- damage / heal / buff / debuff 沿用既有 runtime 行為與資料；前端 JavaScript 只 dispatch UIAction 並 render ScreenModel，不握 gameplay 決定權。
- 使用者手測確認：Combat Skill Button Live MVP 已以盜賊／刺客路線完成一輪 E2E 手測；可進入 live bridge 與戰鬥、盜賊／刺客技能可使用並消耗 MP、MP 耗盡後技能無法再使用、技能戰鬥可取得 EXP、level up 會觸發 HP/MP 回滿，戰鬥後可返回 Dungeon Exploration，後續可回 World Map / Town Hub / Guild / Inn / Save，未發現明顯 routing regression；劍士、法師、牧師與其他職業技能分支仍待後續補測。
- 本 MVP 不新增正式 skill system、skill framework、target selection、技能重平衡或大型 combat 重構；未修改 `03_engine/engine/game.py`、`04_data/`、`02_schema/`、`save.json` 或 combat formula。

Guild Report / Dungeon Clear Reward MVP 已完成受限 live bridge 收斂：

- Guild report 只設定 `state.flags["guild_reported_<dungeon_id>"] = True`，用於登記 / 顯示回報狀態。
- 首次通關 reward 仍在 route clear 當下發放；Guild report 不重複發放 clear reward，也不搬移 route clear reward 的發放時間點。
- 手測流程確認：一開始進 Guild 時若任務 / 解鎖條件尚未滿足，不能直接完成回報；打一輪 dungeon 後回 Guild，任務 / 回報狀態解鎖並可成功回報。
- static fixture fallback 保留；story hint 目前只保留 hidden placeholder，不啟用 fire mark / Noah / story hint active bridge。
- 本 MVP 不代表完整 guild system、正式 quest framework、reputation、achievement 或正式任務系統完成。

手測已通過：`start_gui_runtime_bridge_server.bat` 可正常啟動；重新開啟 bat 後，使用者確認新狀態重新開始、在 World Map 主選單存檔、回到標題後繼續遊戲，runtime 狀態可保留，且無 traceback 或 fatal error。Python runtime 仍是 gameplay authority；GUI live mode 只 dispatch UIAction 並 render ScreenModel。

Live bootstrap log naming cleanup 已完成：Start、Town Hub、Inn、World Map 在 live 成功載入時會記錄 `live_screen_loaded` / `live_loader`，並帶 `mode: "live"` 與 `screen_id`；static fixture load 與 live fallback 仍保留 `fixture_loaded`，fallback 仍會另外記 `live_bridge_unavailable`。

目前仍不提升 Guild Report MVP 之外的 Shop、Workshop、Synthesis、Storage、Magic Shop、Temple、Relic Preview 到正式 bridge contract。Guild 只完成受限 clear report 登記；Dungeon / Combat 僅完成已批准的 traversal / combat loop 小切片與 Combat Skill Button Live MVP。Combat skill button 只沿用既有 `SKILLS` / `learned_skills` / runtime combat flow，不代表完整 dungeon framework、boss framework、正式 skill system、skill framework、target selection、inventory / equipment interaction、facility family、完整 guild system 或正式 quest framework 已開放。

已知後續對齊點：

- Live bridge 已收斂到 Start Screen / Town Hub / Inn / World Map、受限 Dungeon / Combat loop、Guild Report MVP 與 Combat Skill Button Live MVP 的最小可測 GUI shell；後續仍需以單一小切片另行批准，不自動擴張其他 live bridge surface。
- 若未來要讓 `open_settings` 變成真正設定面板，需另開單一小切片；目前只是 GUI shell 入口，不 dispatch 到 Python runtime。
- `save.gui-backup-*.json` 是 bridge save 前安全備份產物，已列入 `.gitignore`；不要手動讀寫 `save.json`。

## 仍然有效：GUI HTML Static Prototype（static fixtures）

此層工作是 `07_gui_prototype/` 的 HTML static prototype。它只驗證 GUI render layer、layout、互動與 UIAction logging，不接 Python runtime，不讀寫 `save.json`，不修改 runtime / data / schema / combat formula，也不啟動正式 asset pipeline。

- 已建立 Start Screen、Town Hub、Guild Screen、Synthesis Screen、World Map、Dungeon Exploration、Combat Screen、Shop Screen、Workshop Screen、Storage Screen、Magic Shop Screen、Inn Screen、Temple Screen、Relic Preview Screen 十四個 static prototype。
- Start Screen 已有 no-save / has-save fixtures、開始 / 讀取 / 重新開始入口，以及只寫 UIAction 的冒險者登錄 modal。
- World Map 可用靜態 fixture 導向 Dungeon Exploration；Dungeon Exploration 的 `Fixed Encounter Preview` 可導向 Combat Screen。
- Combat Screen 已有 5 個底部指令、技能 / 道具 floating popover、右側 Battle Log、Victory / Defeat / Retreat result preview fixtures。
- Combat Result 已整合為 Combat Screen 內的中央 terminal overlay，不再新增獨立 Combat Result Screen。
- Result overlay 開啟後 command bar 停用；勝利 / 撤退下一步回 Dungeon Exploration，戰敗下一步回 Town Hub。
- Combat Screen 第一輪 mockup-alignment layout tuning pass 已完成；若後續還有調整，應視為使用者 review 後的小幅微調。
- Synthesis Screen 已完成基礎版面定案；Shop Screen、Workshop Screen、Storage Screen、Magic Shop Screen static prototype v1 皆已完成；旅店 (Inn Screen)、轉職神殿 (Temple Screen) 與遺物展示台 (Relic Preview Screen) 目前也停在 static prototype 階段。
- Inn Screen 與 Temple Screen 已完成 JRPG dialogue/menu static prototype 調整；mockup reference 只存放於 `05_assets/gui_references/facility_inn_screen/` 與 `05_assets/gui_references/facility_temple_screen/`，不作 runtime asset。
- 下一步若是 static prototype 工作，仍須維持 static prototype 邊界；若是 live bridge 工作，必須限制在已批准的 blessed slice cleanup 或另開 read-only planning gate。
- 詳細狀態與驗證紀錄見 `01_content/gui-html-static-prototype-progress-v1.md`。

## 最新 runtime 收尾：v0.2-2 技能系統最小版

Python CLI runtime 已完成 v0.2-2 技能系統最小版收尾；Final Smoke Test：PASS。

- 背包選單已整併。
- 初始背包已正式化。
- 寶箱技能書已 MVP 化。
- 技能書使用、技能學習、戰鬥施放與 MP 消耗正常。
- 「Element Decay 引擎」不是正式專案術語，不納入正式紀錄。

## 前一輪 runtime 完成：Synthesis Catalog MVP

最新 UI 變更仍只做 CLI 顯示層優化，範圍限定米菈合成屋：

- 米菈合成屋改為專屬分類 catalog 流程：全部、裝備、戰術道具。
- 配方清單顯示分類、可製作狀態、產出、持有 / 裝備狀態、最多可製作次數、費用與素材持有狀態。
- 配方詳情顯示可製作狀態、基底裝備、素材需求、最多可製作次數、金幣、效果與合成確認。
- 原本的配方解鎖、金幣、素材、基底裝備消耗與產出規則維持不變。
- 本輪不碰工會、倉庫、背包 / 裝備管理、資料表或新增配方。

## 前一輪完成：Magic Shop Catalog MVP

最新 UI 變更仍只做 CLI 顯示層優化，範圍限定星燈魔法商店：

- 星燈魔法商店改為專屬 catalog 流程：全部、攻擊魔法、恢復魔法、輔助魔法、特殊魔法。
- 魔法書清單顯示分類、學習狀態、可用職業、等級需求、MP、價格與技能效果。
- 魔法書詳情顯示對應技能、職業條件、等級條件、金幣、素材持有狀態與永久學習提示。
- 原本的職業限制、等級限制、素材需求、火花術書折扣與永久學習規則維持不變。
- 本輪不碰旅人小鋪、鐵刃 / 堅甲工坊、合成屋、工會收購或資料表。

## 前一輪完成：Workshop Catalog MVP

最新 UI 變更仍只做 CLI 顯示層優化，範圍限定鐵刃工坊與堅甲工坊：

- 鐵刃工坊改為專屬 catalog 流程：購買武器、強化武器、我的裝備。
- 堅甲工坊改為專屬 catalog 流程：購買防具、強化防具、我的裝備。
- 裝備清單顯示目前職業可用性、背包 / 已裝備狀態、價格與能力摘要。
- 裝備詳情顯示欄位、類型、可用職業、價格、能力與說明。
- 強化詳情顯示完成品、基底裝備狀態、素材持有狀態、費用與效果。
- 原本價格、可用職業、基底裝備消耗、素材消耗與強化結果維持不變。
- 本輪不碰旅人小鋪、魔法商店、合成屋、工會收購或資料表。

## 前一輪完成：Travel Shop Catalog MVP

最新 UI 變更仍只做 CLI 顯示層優化，範圍限定旅人小鋪：

- 旅人小鋪改為專屬分類商店流程：全部、補給品、戰術道具、飾品。
- 商品清單顯示持有數、價格與效果摘要。
- 選中商品後進入商品詳情 panel，再確認購買 1 個。
- 原本的價格、解鎖條件、背包加入與裝備替換規則維持不變。
- 鐵刃工坊、堅甲工坊、魔法商店、合成屋、工會收購與其他商店流程不在本輪範圍內。
- 本輪不做商品圖示、NPC 圖、批量購買、賣出功能或新 UI framework。

## 前一輪完成：Start Screen MVP

最新 UI 變更仍只做 CLI 顯示層優化，依照使用者提供的開始畫面範本取其架構，不取圖像風格：

- 啟動時先顯示 `《元素迷宮：邊境冒險者》` 開始畫面。
- 若偵測到 `save.json`，開始畫面提供「重新開始」與「載入進度」。
- 若未偵測到存檔，開始畫面只提供「開始新冒險」。
- 保留原本角色建立、讀檔與主選單流程；不改 save schema、不改 gameplay flow。
- Rich 不可用時仍退回純文字標題與數字選單。
- 本輪不加入背景圖、不做全螢幕場景、不建立 UI framework、Unity 或 HTML UI。

## 前一輪完成：Combat UI Log Separation MVP

最新 UI 變更仍只做 CLI 顯示層優化，並把戰鬥主畫面與完整過程紀錄拆開：

- 戰鬥動作現在先產出事件文字，再由 `combat()` 統一渲染回合摘要與 Battle Log。
- 戰鬥主畫面聚焦當前決策：回合數、玩家 HP/MP/狀態、敵人 HP/屬性/狀態、上一動短摘要與戰鬥指令。
- 攻擊、防禦、技能、道具、逃跑、敵人行動與灼傷 tick 會整理成每回合 1-3 行「戰鬥結果摘要」。
- 完整過程保留在戰鬥結束或脫離時的 `Battle Log` panel，方便測試、debug 與戰後回顧。
- 技能與道具選擇沿用既有 Rich panel 薄層，仍維持數字輸入與返回邏輯。
- 本輪不新增玩法內容，不改 data/schema/save/combat formula，也不建立 UI framework、Unity 或 HTML UI。

前一輪核心循環 UI panel 化狀態：

- `display.py` 新增薄層 `render_panel()` 與 `action_menu_panel()`，讓畫面能分成狀態、提示、行動與結算區。
- 主選單補上 HP/MP 與下一步提示，維持原本主選單行動列表。
- 城鎮整備、迷宮選擇、迷宮探索、戰鬥指令、探索/失敗結算已接入 Rich `Panel` 顯示。
- 角色狀態頁拆成角色狀態、裝備、技能 panel。
- 依手動測試回饋修正迷宮 Boss/gate 提示：Boss 狀態改放在各迷宮選項中，避免不同迷宮提示混在一起；葛倫已擊敗後會正確顯示已擊敗。
- 背包顯示補上物品描述、任務、配方與工會收購用途；城鎮倉庫入口已簡化為純倉庫功能。
- 旅館、冒險者工會、工坊、商店、魔法書、合成與倉庫開始改為專屬設施 panel。
- 米菈合成屋已從單層配方清單改為分類 catalog，顯示可製作狀態、產出、持有狀態、素材、基底裝備、最多可製作次數與合成確認。
- 工會內部補上可交付、進行中委託與 Boss 挑戰狀態提示，避免重要線索只出現在主選單或迷宮選擇。
- 數字輸入、返回邏輯、save/schema/data/combat formula 與 gameplay flow 維持原樣。
- Rich 不可用時會退回原本的文字輸出，不影響啟動與 smoke test。
- 本輪不建立 UI framework，不擴張成 Unity / HTML UI。
- 使用者本機已補裝 `.venv` 並回報 `python element_maze.py --smoke-test` 成功；Codex 端另以 bundled Python 驗證 smoke test、data validation 與 content inventory report。

`06_tools/content_inventory_report.py` 是 read-only 內容盤點工具，不是 gameplay 功能，也不是 validation 的替代品。

UI 完成後要回頭處理的 demo 遊玩體驗、平衡、任務引導與內容節奏 polish，統一記錄在 `01_content/demo-playtest-notes.md`；它不是目前 runtime 施工清單。

## 目前 GUI prototype 方向：ScreenModel / UIAction

目前 CLI / Rich panel 已足以作為 playable reference；HTML static prototype 已用 static fixtures 驗證第一批 GUI screen 的 layout 與互動。正式 runtime 仍是 Python CLI，HTML prototype 不是正式遊戲入口；local runtime bridge 只作為受限的開發測試通道。

GUI 升級目前分三層，另有一條受限 local bridge slice：

- Phase UI-1：CLI / Rich playable reference。已完成核心循環與設施 catalog 的顯示層整理。
- Phase UI-2：HTML static fixture prototype。已建立 Start Screen、Town Hub、Guild、Synthesis、World Map、Dungeon Exploration、Combat、Shop、Workshop、Storage、Magic Shop、Inn、Temple、Relic Preview；預設仍只用 fixture，不接 runtime。
- Phase UI-2.5：local runtime bridge blessed slice。已驗證 Start / Town Hub / Inn / World Map 的 UIAction dispatch 與 ScreenModel render，並完成受限 Dungeon / Combat loop：戰鬥結算 overlay、返回探索、route clear / resolved state 與離開迷宮回 World Map；Guild 目前只完成 clear report 狀態顯示與回報登記 MVP。其他設施與更完整的 guild / quest / skill / boss / inventory / equipment / dungeon framework 仍需另開 planning gate。
- Phase UI-3：最終 GUI 視覺版本。使用正式背景圖、角色圖、icon、UI skin，並需要 asset request schema、prompt builder、asset registry 與 style bible；此階段尚未開始。

三層應共用同一套 Screen Map、ScreenModel 與 UIAction；CLI 數字輸入、Rich wireframe 選取與未來 GUI 點擊 / 觸控都只應映射到同一批遊戲語意 action。

正式 UI flow 暫定為：

- Flow A：Start Screen → World Map Screen → Town Hub Screen → Facility Screens（Guild / Shop / Forge / Synthesis / Inn / Storage）。
- Flow B：Start Screen → World Map Screen → Exploration Screen → Combat Screen → Result → 回到 Exploration 或 World Map / Town。

下一步建議維持小切片邊界：static prototype 仍只做 fixture/render/UIAction logging；live bridge cleanup 只限 blessed slice 對齊項。不要讀寫 save、不要把 gameplay logic 複製到 JavaScript、不要把 reference/mockup 圖當 runtime asset。

## 近期完成：火之印記三碎片後的工會、神殿與教會查閱 MVP

最新 runtime 已完成三個很小的劇情接橋：
- 玩家持有 `key_fire_mark_shard x3`，且尚未觸發過事件時，冒險者工會會新增「詢問三枚印記碎片的事情」。
- 工會詢問完成後會設定 `fire_mark_guild_inquiry_done`，諾亞會說明三枚碎片反應明顯，但工會無法判讀真正用途，建議前往教堂／教會側詢問。
- 玩家完成工會詢問、仍持有三枚碎片，且尚未觸發教堂／神殿接橋時，第一次進入轉職神殿會觸發賽恩的一次性對話。
- 神殿接橋完成後會設定 `fire_mark_church_bridge_done`。
- 玩家完成神殿接橋後，可觸發教會查閱結果；教會確認三枚碎片是「未完成的火之印記核心」，完成後設定 `fire_mark_church_lookup_done`。

這些事件只做「查閱、確認與交還／封存」的劇情收束，不合成火之印記、不消耗三枚碎片、不開正式火印流程，也不啟用正式聖物或正式轉職。

## 目前 Act 2 火系 demo 最新狀態

- `dungeon_cinder_seal_depths`「燼印深窟」已進 runtime。
- 深窟普通怪目前為 `mon_ember_stalker`、`mon_molten_shell`、`mon_cinder_brand_wisp`。
- `boss_cinder_seal_sentinel` 已進 runtime，現名「燼印鎮衛」。
- 第 3 枚 `key_fire_mark_shard` 已可由擊敗燼印鎮衛取得，並以 `cinder_seal_sentinel_defeated` 防重複領取。
- Boss gate 使用 `quest_cinder_depths_scout`；未完成該任務時，深窟通關只顯示回工會詢問諾亞的暗示。
- `quest_supply_upgrade`「補給線升級」已素材化，需要 `mat_flame_stone_refined x3` 與 `mat_lava_shard x2`。
- 完成 `quest_supply_upgrade` 後維持既有效果：取得 `item_potion_m x2`，並解鎖旅人小鋪販售中藥水。
- 火之印記碎片目前最多可取得 3 枚；三碎片後的工會詢問事件已完成，使用 `fire_mark_guild_inquiry_done` 防重複觸發。
- 工會 → 教堂／神殿接橋事件已完成，使用 `fire_mark_church_bridge_done` 防重複觸發。
- 教會查閱結果已完成，使用 `fire_mark_church_lookup_done` 防重複觸發；結論是三枚碎片為「未完成的火之印記核心」。
- 測試結果：燼印鎮衛調高一階難度後，Lv10-Lv12 盜賊可通過；中藥水在 Boss 後期連續使用兩次，確認有實戰價值；目前不再調 Boss 數值。

明確仍未開放：
- 完整火之印記的正式合成與啟用。
- 火印熔爐。
- 具名火印守護 Boss（「火印爐衛」較適合作為稱號／怪物類型，不作為第一章收束 Boss 正式名稱）。
- 正式教會火印流程。
- 正式轉職與正式聖物。
- 八元素或完整屬性克制。
- 通用 Boss framework。
- save/schema/combat formula 改動。
- Act 3 文件與 Act 3 runtime 內容。

目前設計共識：
- demo 第一章火印線的收束不是「玩家掌握完整火印力量」。
- demo 第一章火印線的收束應定位為「玩家確認三枚碎片的真相，取得／確認未完成的火之印記核心」。
- 火之印記目前不是正式聖物，暫定為未來正式聖物的零組件／核心材料與劇情上的重要印記。
- 目前不提供火印裝備、啟用、升級、戰鬥效果或正式聖物效果。
- 正式聖物、正式轉職、完整屬性系統暫不開放。

## 1. 專案定位

這是一個 Python CLI 文字冒險 RPG 的 v1 playable vertical slice。核心體驗是「進入迷宮探索 → 戰鬥 → 取得素材與金幣 → 回城整備 → 商店、合成、工會、魔法書強化 → 挑戰更高階迷宮」。

目前目標不是大型內容擴張，而是讓既有最小垂直切片具備可維護、可擴張、可驗證的資料與文件基礎。第二幕已開始以最小切片方式進入 runtime data，目前完成灰燼裂谷、灰燼守衛、補給線升級、燼印深窟、燼印鎮衛 Boss MVP 與深窟未接 Boss 任務時的通關提示 UX。

## 2. 目前版本狀態

目前版本已可遊玩，第一幕主線可通關，包含：

- 單人職業：劍士、法師、盜賊、牧師
- 城鎮：工會、鐵刃工坊、堅甲工坊、旅人小鋪、米菈合成屋、星燈魔法商店、轉職神殿
- 商店：武器、防具、飾品、補給、特殊道具
- 魔法書：購買後永久學習技能
- 迷宮：青苔洞窟、焦石礦坑、灰燼裂谷、燼印深窟
- 戰鬥：攻擊、防禦、技能、道具、逃跑
- 掉落：金幣、素材、藥水、關鍵道具
- 合成：抗火斗篷、鐵劍 +1、皮甲 +1、集中藥袋、暖石墜改、破甲釘組
- 工會任務：冒險者登記、洞窟採集、魔晶研究、焦石偵查、血跡地圖、灰燼裂谷偵查、補給線升級、燼印深窟偵查
- 工會收購 MVP：工會可收購白名單素材，只給金幣；第一版不收消耗品、裝備或關鍵道具
- 倉庫 MVP：可花費 500G 開啟 LV1 倉庫，存取最多 10 種非 key item 背包物品
- 怪物圖鑑 MVP：擊敗怪物後 100% 登錄，可從主選單查看已登錄怪物的基礎資訊
- CLI UI MVP：核心循環已以 Rich `Panel` 薄層整理，涵蓋開始畫面、主選單、角色狀態、城鎮整備、工坊 catalog、旅人小鋪分類商店、星燈魔法商店 catalog、米菈合成屋 catalog、迷宮選擇、迷宮探索、戰鬥指令與結算；戰鬥已完成主畫面 / Battle Log 分流；輸入、資料、存檔與戰鬥規則維持原樣
- GUI HTML static prototype：`07_gui_prototype/` 目前包含 Start Screen、Town Hub、Guild Screen、Synthesis Screen、World Map、Dungeon Exploration、Combat Screen、Shop Screen、Workshop Screen、Storage Screen、Magic Shop Screen、Inn Screen、Temple Screen、Relic Preview Screen；預設只用 fixtures 驗證 GUI layout / interaction，不是正式 runtime UI
- GUI runtime bridge live slice：local-only bridge 已可手測 Start / Town Hub / Inn / World Map 的最小 live flow，並完成受限 Dungeon / Combat loop 的勝利結算、返回探索、route clear / resolved state 與離開迷宮回 World Map；Guild Report MVP 只登記 / 顯示已解鎖且符合流程條件的迷宮回報狀態，不重發 clear reward；Combat Skill Button Live MVP 只沿用既有 `SKILLS` / `learned_skills` / runtime combat flow，技能合法性與 MP 扣減由 Python server-side 判斷；Python runtime 仍是 gameplay authority，其他設施與完整 guild / quest / skill framework / target selection / boss / inventory / equipment / dungeon framework 仍不在正式 bridge contract 內
- 轉職 preview-only MVP：轉職神殿顯示 `PROMOTIONS` 預覽方向與條件，正式轉職尚未開放
- 聖物 preview-only MVP：城鎮「聖物調查」顯示 `RELICS` 預覽，聖物取得與效果尚未開放
- 職業特化 preview-only MVP：角色狀態頁顯示 `JOB_SPECIALIZATIONS` 預覽，目前尚未生效
- 盜賊 head-slot 副武器 data-only MVP：新增盜賊限定 `head` slot 副武器語意裝備，未新增 `offhand`
- Boss：山寨頭目葛倫、灰燼守衛、燼印鎮衛
- 存檔：主選單可存檔，會建立 `save.json`

第二幕目前已實作的 runtime data 包含灰燼裂谷、灰燼守衛、燼印深窟與燼印鎮衛 Boss MVP：

- 完成 `quest_boss_glen` 後會解鎖 `second_act_preview`、`unlock_act_2`、`unlock_ash_ravine`。
- `dungeon_ash_ravine` 已存在，定位為灰燼裂谷偵查版，目前為 18 步。
- 灰燼裂谷目前有 3 個普通怪與 3 個素材。
- 完成「血跡地圖」後，工會會提示玩家前往灰燼裂谷，並顯示最小偵查任務「灰燼裂谷偵查」。
- 灰燼裂谷 `boss` 已指向 `boss_ash_guardian`。
- 灰燼守衛只會在完成 `quest_ash_ravine_scout` 後於灰燼裂谷終點出現。
- 擊敗灰燼守衛會設定 `ash_guardian_defeated`，並取得第 2 枚 `key_fire_mark_shard`；防重複領取已由手測確認。
- 灰燼守衛擊敗後會開放燼印深窟探索，並讓 `quest_supply_upgrade` 出現。
- `quest_supply_upgrade` 已素材化，需要 `mat_flame_stone_refined x3` 與 `mat_lava_shard x2`；完成後取得 `item_potion_m x2` 並解鎖旅人小鋪販售中藥水。
- 燼印深窟目前有 3 個普通怪：餘燼潛獵者、熔殼岩獸、燼印火靈。
- 燼印深窟 `boss` 已指向 `boss_cinder_seal_sentinel`（燼印鎮衛）。
- 燼印鎮衛只會在完成 `quest_cinder_depths_scout` 後於燼印深窟終點出現；未滿足 Boss gate 時，深窟通關會提示玩家回工會詢問諾亞。
- 擊敗燼印鎮衛會設定 `cinder_seal_sentinel_defeated`，並取得第 3 枚 `key_fire_mark_shard`。
- 目前火之印記碎片最多可取得 3 枚；三碎片後可在工會詢問諾亞，完成後設定 `fire_mark_guild_inquiry_done`。
- 完成工會詢問後，玩家首次進入轉職神殿會觸發工會 → 教堂／神殿接橋，完成後設定 `fire_mark_church_bridge_done`。
- 完成神殿接橋後，可取得教會查閱結果，完成後設定 `fire_mark_church_lookup_done`；三枚碎片被確認為「未完成的火之印記核心」。
- 火之印記目前不是正式聖物，暫定為未來正式聖物的零組件／核心材料；demo 第一章目標是「發現火印真相」，不是「掌握火印力量」。
- 完整火之印記正式合成／啟用、火印熔爐、具名火印守護 Boss、第二幕完整任務鏈、正式轉職、正式聖物與正式教會火印流程仍未實作。

最近一次入口平衡修正：

- 山寨頭目葛倫小幅降壓，保留 Boss 定位但降低過度補血循環。
- 洞窟黏蟲與裂石小魔像的小魔晶掉落率提高。
- 破甲釘現在會造成少量即時傷害，並維持 3 回合降低敵方防禦。
- 玩家短測確認：破甲釘可造成傷害並正常觸發擊殺、經驗與金幣結算；小藥水、集中滴露、逃脫卷軸未觀察到被破甲釘補丁波及。
- 集中藥袋已修正為 special 欄實際裝備時才生效；只放在背包中不會在進入迷宮時取得集中滴露。
- 灰燼裂谷普通怪 HP 平衡 MVP 已完成：三隻普通怪小幅提高 HP，`run_checks.bat` 已通過。
- Lv7 → Lv8 盜賊實測確認目前灰燼裂谷難度合理；暫不建議繼續提高 HP，也不建議修改 combat formula、EXP/gold、升級全回復或新增怪物技能。
- 灰燼守衛 Boss MVP 已完成：新增 `boss_ash_guardian`、新增 `ash_guardian_defeated`、灰燼裂谷 boss 指向灰燼守衛；本機 `run_checks.bat` 通過，手動測試確認葛倫流程未回歸、灰燼裂谷偵查 gate 正常、灰燼守衛只觸發一次且第 2 枚火之印記碎片取得正常。

## 3. 啟動方式

最簡單的方式：

1. 在資料夾中執行 `run-game.bat`
2. 建立角色
3. 從主選單進入城鎮或迷宮

如果要用指令啟動：

```powershell
C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\element_maze.py
```

若使用本機 `.venv`，可先啟用 venv 後用一般 `python` 指令：

```powershell
.\.venv\Scripts\Activate.ps1
python .\element_maze.py
```

`.venv/` 已列入 `.gitignore`，只作為本機執行環境，不是專案資料來源。

### 驗證方式

Windows 本機可在專案根目錄執行標準檢查入口：

```powershell
.\run_checks.bat
```

`run_checks.bat` 會依序執行：

```powershell
python 06_tools\validate_data.py
python element_maze.py --smoke-test
```

若 Codex 環境因 runtime 或 sandbox 限制無法執行 Python，請由使用者在本機 PowerShell 執行 `run_checks.bat`，再將結果回貼到 Codex session。

若本機已啟用 `.venv` 或 PATH 中有可用 Python，也可直接執行：

```powershell
python element_maze.py --smoke-test
```

煙霧測試：

```powershell
C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\element_maze.py --smoke-test
```

資料驗證：

```powershell
C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\06_tools\validate_data.py
```

HTML static prototype 檢查目前以 fixture / syntax / browser 手測為主，不接 runtime：

```powershell
C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe --check .\07_gui_prototype\combat_screen\combat-screen.js
```

Combat Screen fixtures 可用 PowerShell JSON parser 檢查；這只驗證 static display data，不代表 gameplay 結算：

```powershell
Get-ChildItem .\07_gui_prototype\combat_screen\fixtures -Filter *.json |
  ForEach-Object { Get-Content -Raw -Encoding UTF8 $_.FullName | ConvertFrom-Json | Out-Null }
```

內容盤點工具：

```powershell
python .\06_tools\content_inventory_report.py
python .\06_tools\content_inventory_report.py --json
```

`content_inventory_report.py` 是 read-only 工具，用於盤點資料數量、runtime / preview-only tables、資料分組、迷宮 / Boss / 任務、unlock drift、火印相關 id、命名與治理提醒，以及 engine 中硬寫 id 的參照位置。它不修改資料，也不取代 `validate_data.py`。

## 4. 專案資料夾職責

- `element_maze.py`：遊戲入口，負責載入 `04_data` 與 `03_engine`，再執行 `engine.game.main()`。
- `01_content/`：內容設計文件與玩法規劃。
- `02_schema/`：資料契約文件，定義欄位、型別、引用規則與維護規則。
- `03_engine/engine/`：遊戲流程與規則；目前包含主流程 `game.py`，以及低風險 helper modules：`display.py`、`formatting.py`、`bestiary.py`、`previews.py`。
- `04_data/data/`：runtime 實際讀取的資料表。
- `05_assets/`：未來素材資源預留。
- `06_tools/`：開發、驗證與 read-only 盤點工具；目前包含 `validate_data.py` 與 `content_inventory_report.py`。
- `07_gui_prototype/`：HTML static prototype；只用 fixture 驗證 GUI layout / interaction / UIAction logging，不是正式 runtime UI。

## 5. SSOT 分層規則

- `README.md`：project-level SSOT，說明版本狀態、啟動方式、資料夾職責、治理規則與 roadmap。
- `01_content/game-design.md`：content-design SSOT，說明玩法循環、世界觀、職業定位、迷宮、商店、任務節奏與平衡基準。
- `02_schema/*.schema.md`：data-contract SSOT，定義每類 data 的欄位、型別、必要性、引用關係與維護規則。
- `04_data/data/*.py`：runtime data SSOT，遊戲實際讀取的資料表。
- `04_data/data/registry.py`：資料索引與引用總目錄，供 validation 與未來查詢使用。
- `06_tools/validate_data.py`：資料驗證工具，檢查跨表引用與基本欄位一致性。
- `06_tools/content_inventory_report.py`：read-only 內容盤點與 drift 檢查輔助工具，不是 SSOT。
- `save.json`：runtime 存檔，不是 SSOT，不應作為設計資料來源。

## 6. Data 擴張規則

新增職業時，至少同步檢查：

- `04_data/data/jobs.py`
- `04_data/data/skills.py`
- 裝備與魔法書的可用職業
- `02_schema/job.schema.md`
- validation 與 smoke test

新增道具時，至少同步檢查：

- `04_data/data/items.py`
- `04_data/data/shops.py`
- 若有新效果，檢查 `03_engine/engine/game.py`
- `02_schema/item.schema.md`
- validation

新增裝備時，至少同步檢查：

- `04_data/data/items.py` 的 `EQUIPMENT`
- `04_data/data/shops.py`
- `04_data/data/crafting.py`
- `02_schema/equipment.schema.md`
- validation

新增技能或魔法書時，至少同步檢查：

- `04_data/data/skills.py`
- `04_data/data/jobs.py`
- 若是新 `kind` 或新 buff/debuff，檢查 engine 處理流程
- `02_schema/skill.schema.md`
- `02_schema/magic_book.schema.md`
- validation

新增怪物、迷宮、任務或配方時，至少同步檢查：

- 對應的 `04_data/data/*.py`
- 被引用的素材、怪物、任務、解鎖 key 是否存在
- 對應 schema
- `06_tools/validate_data.py`

## 7. Registry 與 Validation

`04_data/data/registry.py` 只做資料彙整與 id set helper，不放複雜 gameplay 邏輯。它目前提供：

- `DATA_REGISTRY`
- item-like id、sellable id、skill id、job id、monster id、dungeon id、recipe id、quest id helper
- 初始、事件、系統、劇情 unlock key 的集中定義

`06_tools/validate_data.py` 會檢查主要跨表引用：

- job 初始技能是否存在
- equipment jobs 是否存在
- magic book 的 job、material、skill 是否存在
- recipe output、material、base item、unlock 是否有效
- dungeon material、monster、boss、unlock 是否有效
- monster drops 是否有效
- quest turn-in、reward、unlock 是否有效
- shop 商品是否存在
- event weights 與基本欄位是否合理

通過時會印出：

```text
data validation ok
```

`06_tools/content_inventory_report.py` 會輸出 read-only 內容盤點：

- runtime 與 preview-only 資料表數量
- item / equipment / skill 分組
- dungeon、boss、quest 與 preview content 摘要
- unlock producer / consumer drift
- 火印相關 id 清單
- 命名與治理提醒
- engine hardcoded id 參照位置

## 8. 不要做的事

- 不要把 `save.json` 當資料表或設計來源。
- 不要新增 data 後不跑 validation。
- 不要直接在 engine 裡大量硬寫新的 id；若必須硬寫，請在 schema 或 registry 記錄原因。
- 不要一次重構整個 `03_engine/engine/game.py`。
- 不要把 Python dict 全部改成 JSON/YAML，除非另有明確任務。
- 不要讓 README、schema 與實際 data 狀態不同步。

## 9. 下一步 Roadmap

短期：

- 維持 schema 文件。
- 修改 data 後固定跑 validation。
- 重要 gameplay 修改後固定跑 smoke test。
- CLI UI 目前只做顯示層包裝；開始畫面、工坊 catalog、旅人小鋪分類商店、星燈魔法商店 catalog、米菈合成屋 catalog 與戰鬥主畫面 / Battle Log 分流已落地。
- HTML static prototype 預設只允許在 `07_gui_prototype/` 內用 static fixtures 驗證畫面，不接 Python runtime、不讀寫 `save.json`、不啟動正式 asset pipeline；reference/mockup 圖只作設計參考，不作 runtime asset。
- Synthesis Screen 已完成基礎版面定案；Shop Screen、Workshop Screen、Storage Screen、Magic Shop Screen、Inn Screen、Temple Screen、Relic Preview Screen static prototype v1 目前皆已完成。Inn Screen 與 Temple Screen 已完成 JRPG dialogue/menu static prototype 調整，reference-only mockup 位置為 `05_assets/gui_references/facility_inn_screen/` 與 `05_assets/gui_references/facility_temple_screen/`。
- 下一步 UI 工作需先 read-only 確認單一小切片。已落地的 runtime bridge 只限 blessed live slice、World Map utility preview、受限 Dungeon / Combat loop、Guild Report MVP 與 Combat Skill Button Live MVP；不得把 Guild Report MVP 擴張成完整 guild system、正式 quest framework、reputation 或 achievement，不得把 Combat Skill Button MVP 擴張成正式 skill system、skill framework、target selection、技能重平衡或大型 combat 重構，也不得擴張 Shop、Workshop、Synthesis、Storage、Magic Shop、Temple、Relic、完整 boss / inventory / equipment / dungeon framework，或為 reference/mockup 圖啟動 formal asset pipeline。
- 下一輪若要繼續評估灰燼裂谷，優先改測法師、劍士、牧師或不同裝備狀態，不直接施工。
- 暫不繼續提高灰燼裂谷普通怪 HP，暫不修改 combat formula、EXP/gold、升級全回復或新增怪物技能。
- 灰燼裂谷目前已具備偵查版與灰燼守衛 Boss MVP；後續測試結論需避免用單次隨機遭遇過度外推。
- 暫不把餘燼護符或新火抗 accessory 當主要下一步；目前已有暖石墜改與抗火斗篷，新增同質火抗飾品容易定位重疊。
- 暫不建議直接做火印熔爐、具名火印守護 Boss、完整火之印記正式合成／啟用、正式教會火印流程、正式轉職、正式聖物、倉庫升級完整版、完整圖鑑系統、火抗配方或 Act 3。
- 教會查閱結果 MVP 已完成；不要再把它列為下一輪施工目標。
- 下一個 runtime 候選節點尚未指定；若未來要繼續，仍應先做單一小切片的 read-only 邊界確認，不直接施工火印熔爐、完整火印、正式聖物、正式轉職或大型系統。

中期：

- 若未來有明確低風險邊界，再評估 `03_engine/engine/game.py` 拆分；目前不要為拆而拆。
- 將 item effect、monster behavior、unlock rule 部分資料化。
- 為 validation 增加更細的欄位型別與平衡範圍檢查。

長期：

- 評估 data 是否繼續使用 Python dict，或遷移為 JSON/YAML。
- 建立 save migration，處理 id 改名與版本升級。
- 補更多自動測試，覆蓋商店、合成、任務、迷宮與 Boss 流程。

## 10. 遊玩提示

- 先刷青苔洞窟，交付「洞窟採集」解鎖合成屋與焦石礦坑。
- 小魔晶不要急著賣掉，它能用來學魔法書或完成任務。
- 焦石礦坑的火傷害很痛，抗火斗篷、暖石墜、守護符文和補給都很有用。
- 擊敗山寨頭目葛倫後，把任務「血跡地圖」交回工會，會看到第二幕預告並解鎖灰燼裂谷偵查版；下一步是接「灰燼裂谷偵查」並帶回少量裂谷素材。
- 完成「灰燼裂谷偵查」後，灰燼裂谷終點會出現灰燼守衛；擊敗後可取得第 2 枚火之印記碎片，並開放燼印深窟探索。
- 完成「補給線升級」後，中藥水會進入旅人小鋪販售；補給線升級需要從燼印深窟取得精煉火石與熔岩碎片。
- 完成「燼印深窟偵查」後，燼印深窟終點會出現燼印鎮衛；擊敗後可取得第 3 枚火之印記碎片。
- 持有三枚火之印記碎片後，可回工會詢問諾亞；完成工會詢問後，再進轉職神殿會觸發教堂／教會側接橋。
- 完成神殿接橋後，可取得教會查閱結果；目前三枚碎片會被確認為「未完成的火之印記核心」。
- 目前火之印記只作為第一章主線成果物與未來正式聖物的核心材料，不提供裝備、啟用、升級或戰鬥效果。
