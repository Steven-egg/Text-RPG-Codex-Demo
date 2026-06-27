# Facility Synthesis Screen Mockup Request 草案

用途：依據 `gui-ui-direction-brief.md`、`gui-screen-map.md`、`gui-asset-request-schema.md`，整理一份單一 `facility_synthesis_screen` mockup request 草案。此文件只描述未來可審查的 UI-3 visual concept 素材需求，不生成圖片、不啟動 asset pipeline、不選定 GUI 技術。

## 0. 邊界

- 狀態是 `draft`，不是已批准生成。
- 定位偏 UI-3 visual concept，作為未來正式 GUI 視覺概念稿的需求草案。
- 不生成圖片、不呼叫 image tool、不建立 asset registry。
- 不修改 runtime、data、schema、save、combat formula。
- 不重構 `03_engine/engine/game.py`。
- 不新增配方、素材、商品、價格或合成規則。
- 不把目前 CLI 數字選單直接視為最終 GUI。
- 所有文字、數值、配方資訊與 action label 都必須由 render layer 動態輸出。

## 1. Request Object

```yaml
request_id: gui_asset_facility_synthesis_screen_mockup_v0
status: draft
screen_id: facility_synthesis_screen
flow_id: flow_a_town_facility
asset_type: screen_mockup
asset_role: mockup_validation
priority: medium
owner_context: ui_planning

source_documents:
  - 01_content/gui-ui-direction-brief.md
  - 01_content/gui-screen-map.md
  - 01_content/gui-asset-request-schema.md

purpose: >
  Validate the first UI-3 visual concept direction for Mila's synthesis house while
  still preserving the Facility Screen structure. The mockup should test category
  tabs, recipe list, recipe detail, material and gold requirements, craft availability,
  NPC interaction presence, confirm action, and result feedback while keeping all
  gameplay text dynamic.

screen_model_links:
  - screen_id
  - title
  - subtitle
  - player_summary
  - objective
  - sections
  - selected_id
  - actions
  - result_message

ui_action_links:
  - select_category
  - select_item
  - open_detail
  - close_detail
  - craft_recipe
  - confirm
  - cancel
  - back

content_brief: >
  A single 16:9 GUI mockup for the Synthesis Screen inside Mila's synthesis house.
  The scene should feel like a warm frontier alchemy and crafting workshop: wood,
  brass tools, parchment surfaces, small crystals, bottles, recipe materials, and
  soft lamplight. The layout should clearly show a category area, a recipe list,
  a selected recipe detail area, requirement/status rows, and a bottom action bar.
  Reserve a visible portrait or character-presence area for Mila / the facility NPC
  so the screen retains a sense of character interaction. Use placeholder blocks or
  abstract markings for text regions; do not include readable UI text in the image.

layout_intent:
  top_region:
    role: screen_identity_and_player_summary
    should_show:
      - dynamic screen title area
      - dynamic player resource summary area
      - dynamic objective or facility hint area
  npc_region:
    role: facility_character_presence
    should_show:
      - Mila / NPC portrait or bust area
      - optional non-readable speech or hint panel area
      - enough separation from functional recipe detail text
  left_region:
    role: category_and_recipe_navigation
    should_show:
      - category tabs or segmented controls
      - recipe list rows
      - selected row state
      - disabled or unavailable row state
  right_region:
    role: selected_recipe_detail
    should_show:
      - recipe output area
      - effect or description area
      - base equipment requirement area
      - material requirement area
      - gold requirement area
      - maximum craft count or availability area
  bottom_region:
    role: actions_and_feedback
    should_show:
      - primary craft or confirm action area
      - back/cancel action area
      - result or disabled reason message area

style_keywords:
  - warm frontier workshop
  - practical alchemy bench
  - parchment panels
  - brass and iron fittings
  - soft lamplight
  - small crystals and bottles
  - readable list-detail interface
  - restrained fantasy RPG UI

color_material_direction:
  - warm wood
  - parchment
  - brass
  - iron gray
  - soft amber light
  - small star-lamp blue accents
  - limited green/gold availability accents
  - muted red/gray unavailable accents

dimensions:
  target_ratio: "16:9"
  secondary_ratio: "not required"
  transparency: false
  responsive_safe_area: "desktop 16:9 only for this draft"
  crop_policy: "may crop decorative workshop edges; never crop core UI regions"

dynamic_text_policy:
  baked_text_allowed: false
  decorative_glyphs_allowed: true
  render_layer_text_required: true

variants:
  required: false
  states: []

layout_constraints:
  - The mockup must preserve enough quiet panel space for dynamic Chinese UI text.
  - Decorative clutter must stay outside recipe list and detail reading areas.
  - Category, list, detail, requirement, action, and result regions must be visually distinct.
  - The Mila / NPC portrait area must support character interaction without covering core recipe controls.
  - Availability should be distinguishable by shape/value treatment, not color alone.
  - The mockup must not imply drag-and-drop crafting or new crafting mechanics.
  - This draft only targets desktop 16:9 and should not attempt mobile or narrow layout solutions.

reuse_targets:
  - facility_shop_screen
  - facility_forge_screen
  - facility_magic_screen

dependencies:
  - ScreenModel / UIAction definitions remain conceptual at this stage.
  - No asset registry exists yet.
  - No render platform has been selected.

forbidden:
  - readable Chinese or English text baked into the image
  - readable NPC dialogue baked into the image
  - recipe names baked into the image
  - material names or item stats baked into the image
  - prices, counts, HP/MP, gold, or quantities baked into the image
  - UI buttons with fixed labels baked into the image
  - new recipes, new materials, or new crafting rules
  - batch crafting or selling flow
  - drag-and-drop crafting implication
  - modern sci-fi dashboard styling
  - neon gacha styling
  - photorealistic modern shop counter
  - full-screen decorative illustration with no usable list-detail layout
  - portrait placement that blocks category, list, detail, requirement, action, or result regions
  - clutter behind text-heavy regions

acceptance_checks:
  - Uses `facility_synthesis_screen` and Flow A concepts correctly.
  - Reads as a UI-3 visual concept request, not a pure UI-2 wireframe request.
  - Communicates the `category -> recipe list -> detail -> confirm -> result` pattern.
  - Reserves a clear Mila / NPC portrait or character-presence region.
  - Leaves all gameplay text, labels, numbers, names, and messages dynamic.
  - Provides clear regions for category tabs, list rows, selected recipe detail, requirements, actions, and result feedback.
  - Targets desktop 16:9 only.
  - Works as a mockup request without requiring pygame, HTML, Unity, or any specific GUI framework.
  - Does not imply runtime, data, schema, save, or combat changes.
  - Could later inform Shop / Forge / Magic facility layouts without forcing them to be identical.
```

## 2. Mockup 應驗證的畫面問題

這份 request 只應驗證 UI 結構，不驗證美術量產：

- Synthesis Screen 是否適合用「左側分類與配方列表、右側詳情、底部 action」的結構。
- 可製作 / 不可製作 / 缺素材 / 缺金幣 / 缺基底裝備是否能被清楚區分。
- 詳情區是否能容納產出、效果、基底裝備、素材、金幣與最多可製作次數。
- 結果訊息是否能在不跳出新大畫面的情況下被玩家看見。
- 這個 Facility layout 是否有機會延伸到 Shop、Forge、Magic Book。

## 3. 不應驗證的內容

- 不驗證正式美術風格最終定稿。
- 不驗證 image generation prompt 品質。
- 不驗證正式 icon set。
- 不驗證素材命名與 registry。
- 不驗證 GUI 技術選型。
- 不驗證合成規則、配方平衡、素材經濟或 runtime 行為。
- 不驗證 mobile / narrow layout。

## 4. 可合理判斷的欄位

目前可由三份文件合理判斷：

- `screen_id`：`facility_synthesis_screen`
- `flow_id`：`flow_a_town_facility`
- `asset_type`：`screen_mockup`
- `asset_role`：`mockup_validation`
- `status`：`draft`
- `dynamic_text_policy.baked_text_allowed`：`false`
- 主要互動模式：`category -> recipe list -> detail -> confirm -> result`
- 主要 action：`select_category`、`select_item`、`craft_recipe`、`confirm`、`back`
- 視覺方向：溫暖邊境工坊、羊皮紙、木材、黃銅、柔和燈火、少量星燈藍點綴
- visual concept 定位：偏 UI-3，不是純 UI-2 wireframe
- 角色互動感：保留米菈 / NPC portrait 或 character-presence 區域
- 尺寸範圍：目前只做桌面 16:9，不先處理 mobile / narrow layout

## 5. 已確認決策

以下決策已由使用者確認，後續 request review 應以此為準：

1. 第一張 mockup 偏 UI-3 visual concept，作為未來正式 GUI 視覺概念稿的需求草案。
2. 保留米菈 / NPC portrait 位置，讓設施畫面維持角色互動感。
3. 目前只做桌面 16:9，不先處理 mobile / narrow layout。
