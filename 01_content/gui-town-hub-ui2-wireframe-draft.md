# Town Hub UI-2 Wireframe Draft

用途：以 markdown-only 草圖描述 Town Hub UI-2 / Rich wireframe 的版面與狀態變體。此文件只驗證畫面結構，不生成新圖、不選平台、不改 runtime。

## 0. Inputs

- `01_content/gui-town-hub-screen-model-draft.md`
- `01_content/gui-town-hub-review-checklist.md`
- `01_content/gui-town-hub-mockup-review-v1.md`
- `01_content/gui-town-hub-wireframe-plan.md`
- `05_assets/gui_references/town_hub/town_hub_visual_reference_v1_user_mockup.png`

## 1. Boundary

- 不修改 runtime、data、schema、save 或 combat formula。
- 不重構 `03_engine/engine/game.py`。
- 不選定 pygame / HTML / Unity / WebView。
- 不生成新圖。
- 不啟動正式 asset pipeline。
- 不把 Town Hub 擴成自由行走城鎮。
- 不把 facility 內部流程塞進 Town Hub。
- 不建立完整通知系統。
- `open_character` / `open_inventory` 僅作為現階段主 hub 相容入口；最終是否屬於全域導航，後續再定。

## 2. Wireframe Language

本草圖使用文字框線表達 UI-2 layout，不代表最終像素位置。

標記：

```text
[NODE]        facility node / building entry
[NAV]         navigation entry
[GLOBAL]      current hub compatibility action
[BADGE]       high-value badge
[DISABLED]    disabled / locked state
{dynamic}     render layer 動態文字
```

所有 `{dynamic}` 內容都不可烘在圖片裡。

## 3. Base Layout

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ {艾爾姆城鎮}                         {name/job/lv} {HP/MP} {gold}        │
│ {冒險者的據點與補給中心}              {guild_points / exp optional}       │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│        [NODE inn]                 [NODE guild]              [NODE workshop]│
│        旅館                       工會委託所                工坊           │
│        休息恢復 HP/MP             接受與回報任務            裝備強化與製造 │
│                                                                            │
│                                                                            │
│ [NODE travel_shop]              [NODE relic_preview]       [NODE synthesis]│
│ 商店                            聖物調查所                 米菈合成屋     │
│ 購買與販賣物品                  聖物調查與知識             素材合成與轉換 │
│                                                                            │
│            [NODE magic_shop]   [NODE temple]   [NODE storage]              │
│            星燈魔法商店        轉職神殿       倉庫                         │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│ [NAV open_world_map] {返回世界地圖}                                         │
│ {town_guidance: 1-2 行主線 / 補給 / 可回報提示}           [GLOBAL actions] │
│                                                            角色  背包       │
└────────────────────────────────────────────────────────────────────────────┘
```

版面意圖：

- 主要場景保留建築入口感，不把 Town Hub 變成按鈕牆。
- `resource_strip` 放 header 右側或 header 次列，保持輕量。
- `town_guidance` 放底部，避免遮住建築入口。
- `open_world_map` 保留左下 navigation。
- `magic_shop`、`temple`、`storage` 先以次級 facility node rail 補足 runtime 入口；未來 visual mockup 可改成場景建築。

## 4. Facility Node Draft

```text
TownFacilityNode visual draft
- icon slot
- label
- short description
- optional badge
- selected / hover / focus state
- disabled reason hook
```

單一 node 文字結構：

```text
┌────────────────────┐
│ {icon} {label}      │
│ {short_description} │
│ {badge?}            │
└────────────────────┘
```

約束：

- label 與 description 都由 render layer 輸出。
- badge 最多顯示一個；多個狀態時選最高優先級。
- disabled reason 不一定常駐，可在 selected node detail 或 town guidance 顯示。
- icon 只輔助，不可取代文字。

## 5. State Variant A: Default Town

目的：確認沒有 urgent badge 時，場景仍可讀。

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ 艾爾姆城鎮                              莉亞 / 盜賊 Lv8 / HP 86/86 / 420G │
│ 冒險者的據點與補給中心                  工會積分 12 / EXP 40/630          │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│        [旅館]                    [工會委託所]              [工坊]          │
│        休息恢復 HP/MP             接受與回報任務            裝備強化與製造 │
│                                                                            │
│ [商店]                         [聖物調查所]               [米菈合成屋]    │
│ 購買與販賣物品                  聖物調查與知識             素材合成與轉換 │
│                                                                            │
│            [星燈魔法商店]      [轉職神殿]      [倉庫]                      │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│ 返回世界地圖                                                               │
│ 把探索收益轉成任務、裝備、技能或補給後再出發。             角色  背包     │
└────────────────────────────────────────────────────────────────────────────┘
```

通過條件：

- 沒有 badge 時不顯得空。
- resource strip 不干擾 title。
- town guidance 不像完整 quest tracker。

## 6. State Variant B: Guild Ready / Fire Mark Priority

目的：確認工會高價值通知可突出，但不膨脹成通知系統。

優先顯示順序：

1. `火印線索`
2. `可回報`

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ 艾爾姆城鎮                              莉亞 / 盜賊 Lv12 / HP 96/96 / 760G│
│ 冒險者的據點與補給中心                  工會積分 28 / EXP 120/840         │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│        [旅館]                    [工會委託所]              [工坊]          │
│        休息恢復 HP/MP             接受與回報任務            裝備強化與製造 │
│                                  [BADGE 火印線索]                          │
│                                                                            │
│ [商店]                         [聖物調查所]               [米菈合成屋]    │
│ 購買與販賣物品                  聖物調查與知識             素材合成與轉換 │
│                                                                            │
│            [星燈魔法商店]      [轉職神殿]      [倉庫]                      │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│ 返回世界地圖                                                               │
│ 三枚火之印記碎片正在共鳴，回冒險者工會詢問諾亞。           角色  背包     │
└────────────────────────────────────────────────────────────────────────────┘
```

通過條件：

- `guild` node 可見 badge。
- town guidance 與 badge 不互相搶戲。
- 不顯示 Guild Screen 內部 `story_hint_card`。
- 不出現 `submit_quest` 作為 Town Hub action。

## 7. State Variant C: Synthesis Locked

目的：確認 disabled node 與 disabled reason 的呈現。

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ 艾爾姆城鎮                              新手 / 劍士 Lv1 / HP 90/90 / 120G │
│ 冒險者的據點與補給中心                  工會積分 0 / EXP 0/70             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│        [旅館]                    [工會委託所]              [工坊]          │
│        休息恢復 HP/MP             接受與回報任務            裝備強化與製造 │
│                                                                            │
│ [商店]                         [聖物調查所]               [米菈合成屋]    │
│ 購買與販賣物品                  聖物調查與知識             素材合成與轉換 │
│                                                           [DISABLED 未解鎖]│
│            [星燈魔法商店]      [轉職神殿]      [倉庫]                      │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│ 返回世界地圖                                                               │
│ 米菈的店門半掩著。先完成工會任務「洞窟採集」吧。           角色  背包     │
└────────────────────────────────────────────────────────────────────────────┘
```

通過條件：

- `未解鎖` 是 status badge，不是通知。
- disabled reason 可在 town guidance 或 selected node detail 顯示。
- 不因 locked node 修改 unlock rule。

## 8. State Variant D: Low HP / No Potion

目的：確認補給提醒優先用 town guidance，而不是每個相關設施都加 badge。

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ 艾爾姆城鎮                              莉亞 / 盜賊 Lv8 / HP 22/86 / 310G │
│ 冒險者的據點與補給中心                  工會積分 12 / EXP 40/630          │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│        [旅館]                    [工會委託所]              [工坊]          │
│        休息恢復 HP/MP             接受與回報任務            裝備強化與製造 │
│                                                                            │
│ [商店]                         [聖物調查所]               [米菈合成屋]    │
│ 購買與販賣物品                  聖物調查與知識             素材合成與轉換 │
│                                                                            │
│            [星燈魔法商店]      [轉職神殿]      [倉庫]                      │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│ 返回世界地圖                                                               │
│ 旅館可回復 HP/MP；背包沒有藥水，旅人小鋪可補充探索容錯。   角色  背包     │
└────────────────────────────────────────────────────────────────────────────┘
```

通過條件：

- 不為旅館與商店同時加 badge。
- guidance 足以幫玩家決策。
- 資源列讓低 HP 狀態一眼可見。

## 9. State Variant E: Selected Node Focus

目的：確認 keyboard / controller / mouse hover 都可映射 `selected_facility_id`。

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ 艾爾姆城鎮                              莉亞 / 法師 Lv6 / HP 62/62 / 500G │
│ 冒險者的據點與補給中心                  工會積分 8 / EXP 10/420           │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│        [旅館]                 >  [工會委託所]  <           [工坊]          │
│        休息恢復 HP/MP             接受與回報任務            裝備強化與製造 │
│                                  [BADGE 可回報]                            │
│                                                                            │
│ [商店]                         [聖物調查所]               [米菈合成屋]    │
│ 購買與販賣物品                  聖物調查與知識             素材合成與轉換 │
│                                                                            │
│            [星燈魔法商店]      [轉職神殿]      [倉庫]                      │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│ 返回世界地圖                                                               │
│ 工會有可交付委託。確認可進入工會查看與回報。               角色  背包     │
└────────────────────────────────────────────────────────────────────────────┘
```

通過條件：

- selected node 明確，但不改 save。
- guidance 可顯示 selected node 的 disabled reason 或提示。
- selected state 不等於進入 facility。

## 10. Missing Facility Entrance Strategy

目前 mockup 未明確呈現 `magic_shop`、`temple`、`storage`。UI-2 草圖採「次級 facility rail」補足。

```text
            [星燈魔法商店]      [轉職神殿]      [倉庫]
```

後續 visual mockup 可採三種策略之一：

1. 加入小型建築或招牌，整合進城鎮場景。
2. 放在場景邊緣作次級入口，但仍是 `facility_nodes`。
3. 若空間不足，放入 `更多設施` 展開區，但不得隱藏重要主線提示。

目前建議：

- `magic_shop` 使用星燈 / 魔法招牌。
- `temple` 使用神殿尖塔 / 教會入口。
- `storage` 使用工會旁倉庫 / 小木屋。

## 11. Open Questions

- 工坊在 visual mockup 中是否維持單一建築，並在選取後提供 `鐵刃工坊 / 堅甲工坊` 二級選擇？
- `open_character` / `open_inventory` 最終會留在 Town Hub，還是移到全域 navigation？
- `storage` 是否應是獨立建築，或依附在工會旁的小入口？
- `temple` 與 `relic_preview` 是否需要視覺上相鄰，以暗示兩者同屬未來成長 / 聖物資訊區？

## 12. Acceptance Criteria

- 場景式 hub 清楚。
- `facility_nodes` 可辨識、可 focus、可 disabled。
- `resource_strip` 可讀且不壓迫場景。
- `town_guidance` 可讀且不變成 quest tracker。
- badge 少量且高價值。
- `magic_shop`、`temple`、`storage` 有入口策略。
- `open_world_map` 清楚且不是 facility。
- `open_character` / `open_inventory` 只作為現階段主 hub 相容入口。
- 不需要 runtime、data、schema、save 改動。

## 13. Recommended Next Step

建議下一步：

1. 用 `01_content/gui-town-hub-review-checklist.md` review 本 wireframe draft。
2. 若通過，才考慮寫一份 visual mockup prompt draft。
3. visual prompt draft 仍不生成新圖，先確認 dynamic text safe areas 與缺漏 facility 入口策略。

