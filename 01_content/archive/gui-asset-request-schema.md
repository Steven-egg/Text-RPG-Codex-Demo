# GUI Asset Request Schema 草案

用途：定義未來若要提出 GUI 素材需求時，應如何描述 request。此文件是規劃草案，不代表已啟動 asset pipeline，也不要求現在生成圖片、選平台或建立 registry。

## 0. 當前邊界

- 不生成圖片。
- 不建立正式 asset registry。
- 不建立 prompt builder。
- 不選定 pygame / HTML / Unity 或其他 GUI 技術。
- 不修改 runtime、data、schema、save、combat formula。
- 不重構 `03_engine/engine/game.py`。
- 不把目前 CLI `input()` / `print()` menu 視為最終架構。
- 所有素材 request 都必須服務 ScreenModel / UIAction，而不是反過來用圖片決定 gameplay。

## 1. Schema 目標

Asset request schema 的目的，是讓未來每一個素材需求都能回答：

- 這個素材用在哪個 screen？
- 它服務哪個 UI 職責？
- 它是否承載動態文字？
- 它是背景、角色、icon、面板、按鈕 skin，還是完整 mockup？
- 它需要哪些尺寸、比例、透明度或狀態變體？
- 它需要符合哪些視覺方向？
- 它明確不能包含什麼？
- 它如何被驗收？

此 schema 只描述需求，不產出素材、不保證執行順序，也不取代未來 asset registry。

## 2. Request Object

建議每個素材需求以單一 request object 表示。格式可先用 Markdown + YAML-like block 記錄；未來若要工具化，再轉成 JSON / YAML。

```yaml
request_id: gui_asset_synthesis_bg_v0
status: draft
screen_id: facility_synthesis_screen
flow_id: flow_a_town_facility
asset_type: background
asset_role: location_atmosphere
priority: low
owner_context: ui_planning

purpose: >
  Support the Synthesis Screen atmosphere without carrying any dynamic UI text.

screen_model_links:
  - screen_id
  - title
  - sections
  - actions

ui_action_links:
  - select_category
  - select_item
  - craft_recipe
  - confirm
  - back

content_brief: >
  A warm frontier alchemy workshop interior for Mila's synthesis house.

style_keywords:
  - warm wood
  - brass tools
  - parchment labels without readable words
  - small crystals
  - practical workshop

color_material_direction:
  - warm wood
  - brass
  - parchment
  - soft lamplight

dimensions:
  target_ratio: "16:9"
  responsive_safe_area: "center and right side must remain calm enough for UI panels"
  transparency: false

dynamic_text_policy:
  baked_text_allowed: false
  decorative_glyphs_allowed: true
  render_layer_text_required: true

variants:
  required: false
  states: []

forbidden:
  - readable text inside image
  - modern sci-fi dashboard
  - neon gacha style
  - clutter behind item list area
  - UI buttons baked into the image

acceptance_checks:
  - Works behind dynamic UI panels.
  - Does not contain readable text.
  - Does not imply new gameplay systems.
  - Matches GUI direction brief visual tone.
```

## 3. Required Fields

每個正式 request 至少應包含：

| Field | 用途 |
|---|---|
| `request_id` | 穩定 id。建議格式：`gui_asset_{screen_or_domain}_{role}_v0`。 |
| `status` | 需求狀態。初期只用 `draft`、`proposed`、`approved_for_experiment`。 |
| `screen_id` | 使用在哪個 screen。 |
| `flow_id` | 屬於 Flow A 或 Flow B，或跨 flow 共用。 |
| `asset_type` | 素材類型，例如 background、icon、panel_skin。 |
| `asset_role` | 素材在畫面中的職責，例如 location_atmosphere、status_symbol。 |
| `priority` | `low`、`medium`、`high`。第一階段通常只允許少量 high。 |
| `purpose` | 為什麼需要這個素材。 |
| `content_brief` | 素材應畫什麼。 |
| `dynamic_text_policy` | 是否允許圖片內文字；預設不允許。 |
| `forbidden` | 明確禁止內容。 |
| `acceptance_checks` | 驗收條件。 |

## 4. Optional Fields

| Field | 用途 |
|---|---|
| `screen_model_links` | 這個素材支援哪些 ScreenModel 欄位。 |
| `ui_action_links` | 這個素材支援哪些 UIAction。 |
| `style_keywords` | 風格關鍵詞。 |
| `color_material_direction` | 色彩與材質方向。 |
| `dimensions` | 比例、尺寸、透明度、安全區。 |
| `variants` | 狀態變體，例如 normal、hover、disabled、selected。 |
| `layout_constraints` | 不可遮擋區域、可裁切區、安全邊界。 |
| `reuse_targets` | 可重用於哪些 screen。 |
| `dependencies` | 是否依賴已定義的 UI layout、mockup 或 icon set。 |
| `notes` | 暫存設計備註。 |

## 5. Controlled Values 草案

### `status`

- `draft`：只是草案。
- `proposed`：已可拿來討論是否做實驗。
- `approved_for_experiment`：已批准可做一個 mockup / prompt 實驗。
- `generated_candidate`：未來若產出候選素材才使用。
- `accepted`：未來若素材被採用才使用。
- `rejected`：未來若素材不採用才使用。
- `archived`：已過期或被取代。

目前階段只應使用 `draft` 或 `proposed`。

### `flow_id`

- `flow_a_town_facility`
- `flow_b_exploration_combat`
- `shared_core`

### `screen_id`

- `start_screen`
- `world_map_screen`
- `town_hub_screen`
- `facility_screen`
- `facility_synthesis_screen`
- `facility_shop_screen`
- `facility_forge_screen`
- `facility_magic_screen`
- `facility_guild_screen`
- `facility_inn_screen`
- `facility_storage_screen`
- `exploration_screen`
- `combat_screen`
- `result_reward_screen`

第一階段優先：
- `start_screen`
- `world_map_screen`
- `town_hub_screen`
- `facility_synthesis_screen`
- `facility_shop_screen`
- `exploration_screen`
- `combat_screen`
- `result_reward_screen`

### `asset_type`

- `background`：場景或氛圍背景。
- `location_illustration`：地點插圖，可局部用於 hub 或 facility。
- `character_portrait`：NPC 或角色圖。
- `icon`：語意 icon。
- `status_badge`：狀態標記，例如可製作、缺素材、Boss gate。
- `map_node`：World Map 地點節點。
- `panel_skin`：面板框、底板、分隔線材質。
- `button_skin`：按鈕或 action bar skin。
- `item_thumbnail`：物品、素材、裝備縮圖。
- `screen_mockup`：完整 screen 視覺 mockup，只可用於單一 screen 實驗。

### `asset_role`

- `location_atmosphere`
- `navigation_anchor`
- `facility_identity`
- `category_symbol`
- `item_identity`
- `resource_symbol`
- `status_symbol`
- `danger_signal`
- `reward_signal`
- `ui_frame`
- `interaction_state`
- `mockup_validation`

### `priority`

- `low`：可延後，沒有它也能驗證 UI。
- `medium`：有助於 mockup，但不是必需。
- `high`：第一個 screen mockup 必須要有。

第一階段不應同時出現大量 `high` request。

## 6. Dynamic Text Policy

預設規則：所有會因 data、save、角色狀態、語系、平衡或操作狀態改變的文字，都必須由 render layer 輸出，不可畫死在圖片裡。

```yaml
dynamic_text_policy:
  baked_text_allowed: false
  decorative_glyphs_allowed: true
  render_layer_text_required: true
```

### 不可畫死在圖片裡

- screen title、subtitle、地點名稱。
- button、tab、action label。
- 物品、裝備、技能、配方、任務、迷宮、怪物、NPC 名稱。
- 價格、持有數、素材需求、最多可製作次數。
- HP、MP、EXP、金幣、等級、推薦等級、步數。
- 可用 / 不可用原因、gate 條件、Boss 狀態。
- 任務描述、戰鬥摘要、Battle Log、探索事件文字、獎勵文字。
- 錯誤提示、確認提示、返回提示。

### 可以存在於圖片裡

- 無語意依賴的紋理。
- 不可讀或無實際語意的裝飾符號。
- 邊框、印記、材質、光影。
- 不承載 gameplay 狀態的場景物件。

若 request 需要任何可讀文字，必須特別標記為例外並說明原因；第一階段原則上不接受例外。

## 7. Dimensions 草案

目前不選平台，因此 dimensions 只描述設計約束，不定死引擎尺寸。

```yaml
dimensions:
  target_ratio: "16:9"
  secondary_ratio: "4:3 optional"
  transparency: false
  responsive_safe_area: "UI panels must remain readable on center/right area"
  crop_policy: "may crop edges, never crop important subject"
```

常見值：
- `target_ratio`: `16:9`、`4:3`、`1:1`、`free`
- `transparency`: `true` / `false`
- `crop_policy`: `may_crop_edges`、`must_show_full_subject`、`tileable`

icon 或 badge 可先使用：

```yaml
dimensions:
  target_ratio: "1:1"
  transparency: true
  min_readable_size: "small UI icon"
```

## 8. Variants 草案

只有 UI skin、button、badge、map node 等互動素材需要 variants。

```yaml
variants:
  required: true
  states:
    - normal
    - hover
    - selected
    - disabled
```

常見 state：
- `normal`
- `hover`
- `selected`
- `disabled`
- `locked`
- `available`
- `completed`
- `danger`
- `new`

背景圖、角色圖與 screen mockup 通常不應要求大量 variants。

## 9. Screen-Specific Guidance

### Start Screen

優先素材：
- `background` 或 `screen_mockup`
- `panel_skin`

注意：
- 標題文字不可烘在圖裡。
- 不要做成正式影片或動畫需求。
- 可用邊境入口、迷宮遠景、燈火、旅行裝備建立氣氛。

### World Map Screen

優先素材：
- `map_node`
- `status_badge`
- `background` 或簡化地圖底圖

注意：
- 地點名稱、推薦等級、Boss 狀態必須動態渲染。
- 節點 icon 可表達城鎮、洞窟、礦坑、裂谷、深窟。
- 不做自由拖曳大世界地圖。

### Town Hub Screen

優先素材：
- `location_illustration`
- `facility_identity`
- `status_badge`

注意：
- 設施名稱、可交付狀態、價格提示都不可烘在圖裡。
- Hub 要服務重複操作，不要太像一次性劇情插圖。

### Facility Synthesis Screen

優先素材：
- `background` 或 `location_illustration`
- `icon` for recipe categories
- `panel_skin`
- `status_badge`

注意：
- 配方名稱、素材、價格、最多可製作次數、可製作狀態都必須由 render layer 輸出。
- 第一個 mockup 實驗若要選 screen，建議選這個。
- 不新增配方，不改合成規則。

### Facility Shop Screen

優先素材：
- `background` 或 `location_illustration`
- `icon` for item categories
- `item_thumbnail` only if needed

注意：
- 商品名稱、價格、持有數、解鎖狀態不可烘在圖裡。
- 不做批量購買或賣出規則。

### Exploration Screen

優先素材：
- `background`
- `status_badge`
- `icon` for material / encounter / retreat

注意：
- 迷宮名稱、步數、事件文字、本趟收益必須動態渲染。
- 不暗示格子移動或即時探索。

### Combat Screen

優先素材：
- `panel_skin`
- `status_badge`
- `icon` for attack / defend / skill / item / flee
- `background` only if it does not reduce readability

注意：
- HP/MP、狀態、敵名、回合數與 Battle Log 必須動態渲染。
- 主畫面服務決策，不做完整戰鬥紀錄長卷軸。
- 不暗示新 combat formula 或多目標重做。

### Result / Reward Screen

優先素材：
- `reward_signal`
- `status_badge`
- `panel_skin`

注意：
- EXP、金幣、掉落、unlock、結果文字必須動態渲染。
- 不先做成就、抽卡或大量獎勵動畫風格。

## 10. Request Examples

以下是填寫範例，不是已批准的生成需求。

### Example A：Synthesis Screen Mockup

```yaml
request_id: gui_asset_synthesis_mockup_v0
status: draft
screen_id: facility_synthesis_screen
flow_id: flow_a_town_facility
asset_type: screen_mockup
asset_role: mockup_validation
priority: medium

purpose: >
  Validate the visual hierarchy for category tabs, recipe list, recipe detail,
  material requirements, confirm action, and result feedback.

content_brief: >
  A GUI mockup for Mila's synthesis house. Warm workshop mood. Left side category
  and recipe list, right side recipe details, bottom action bar. No readable text
  baked into the image; use placeholder blocks only.

style_keywords:
  - frontier alchemy workshop
  - warm wood and brass
  - parchment panels
  - clear list-detail layout

dimensions:
  target_ratio: "16:9"
  transparency: false
  responsive_safe_area: "important UI groups should remain inside central safe area"

dynamic_text_policy:
  baked_text_allowed: false
  decorative_glyphs_allowed: true
  render_layer_text_required: true

variants:
  required: false
  states: []

forbidden:
  - readable Chinese or English text
  - final logo treatment
  - new recipe names
  - new gameplay mechanics
  - cluttered background behind details panel

acceptance_checks:
  - Shows category, list, detail, condition, confirm, and result regions.
  - Dynamic text can be overlaid later.
  - Does not require a specific GUI framework.
```

### Example B：World Map Node Icon

```yaml
request_id: gui_asset_world_map_dungeon_node_v0
status: draft
screen_id: world_map_screen
flow_id: shared_core
asset_type: map_node
asset_role: navigation_anchor
priority: low

purpose: >
  Represent dungeon destinations on the World Map without embedding destination names.

content_brief: >
  Small fantasy map node icon for a dungeon entrance. Readable at small size,
  transparent background, no text.

style_keywords:
  - simple fantasy map symbol
  - cave entrance
  - readable silhouette
  - warm dark outline

dimensions:
  target_ratio: "1:1"
  transparency: true
  min_readable_size: "small UI map node"

dynamic_text_policy:
  baked_text_allowed: false
  decorative_glyphs_allowed: false
  render_layer_text_required: true

variants:
  required: true
  states:
    - normal
    - selected
    - locked
    - completed

forbidden:
  - location name text
  - level number text
  - boss status text
  - highly detailed illustration that fails at small size

acceptance_checks:
  - Works as a map node, not a full scene.
  - Can pair with dynamic labels and gate badges.
```

### Example C：Status Badge Set

```yaml
request_id: gui_asset_status_badge_availability_v0
status: draft
screen_id: shared_core
flow_id: shared_core
asset_type: status_badge
asset_role: status_symbol
priority: low

purpose: >
  Provide reusable visual states for available, unavailable, completed, and danger.

content_brief: >
  Small badge shapes that can sit next to dynamic text. No words or numbers.

style_keywords:
  - parchment and brass UI
  - simple state shapes
  - readable at small size

dimensions:
  target_ratio: "1:1"
  transparency: true

dynamic_text_policy:
  baked_text_allowed: false
  decorative_glyphs_allowed: true
  render_layer_text_required: true

variants:
  required: true
  states:
    - available
    - disabled
    - completed
    - danger
    - new

forbidden:
  - checkmark with embedded text
  - red/green only distinction without shape change
  - modern app badge style

acceptance_checks:
  - States are distinguishable by shape and value, not color alone.
  - Works beside dynamic labels.
```

## 11. Review Checklist

建立或審查素材 request 時，至少確認：

- 是否引用正確 `screen_id` 與 `flow_id`？
- 是否能說清楚素材服務哪個 UI 職責？
- 是否沒有把動態文字畫死在圖片裡？
- 是否沒有暗示未批准的新 gameplay？
- 是否沒有要求一次生成大量素材？
- 是否沒有提前指定 pygame / HTML / Unity？
- 是否有明確 forbidden 清單？
- 是否有 acceptance checks？
- 是否能支援 ScreenModel / UIAction，而不是繞過它們？

## 12. 下一步建議

下一個 session 若繼續 UI 規劃，建議只做其中一件：

1. 以此 schema 草案填一份 `facility_synthesis_screen` 的單一 mockup request。
2. 對照 `01_content/gui-ui-direction-brief.md`，整理第一批必要 `asset_type` 與 `asset_role` 是否過多。
3. 設計未來 asset registry 欄位草案，但仍不生成圖片。

