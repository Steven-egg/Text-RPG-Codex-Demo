# GUI Asset Registry Draft

用途：記錄目前 GUI 視覺概念素材的候選狀態、來源、用途、審查結果與後續動作。此文件是 registry 草案，不代表已啟動正式 asset pipeline，也不代表素材已進 runtime。

## 0. 邊界

- 此文件只做候選素材盤點。
- 不修改 runtime、data、schema、save、combat formula。
- 不重構 `03_engine/engine/game.py`。
- 不建立正式 asset pipeline。
- 不選定 pygame / HTML / Unity 或其他 GUI 技術。
- 不把候選圖視為正式可用 asset。
- 不把候選圖直接引用進遊戲。
- 若未來要正式使用任何圖片，必須先另行決定 project asset path、命名規則、授權 / 來源紀錄與替換策略。

## 1. Registry 狀態

```yaml
registry_id: gui_asset_registry_draft
status: draft
scope: gui_visual_concept_candidates
current_focus_screen: facility_synthesis_screen
formal_pipeline_started: false
runtime_usage_allowed: false
```

## 2. Status Values 草案

| Status | 意義 |
|---|---|
| `generated_candidate` | 已生成候選圖，但尚未正式採用。 |
| `user_reference` | 使用者提供的參考圖。 |
| `reference_only` | 僅保留作歷史或比較參考，不作為目前採納基準。 |
| `reviewed_candidate` | 已人工審查，可作為方向參考。 |
| `needs_v2` | 已知需要第二版微調。 |
| `accepted_direction` | 可作為視覺方向基準，但不代表可直接進 runtime。 |
| `accepted_visual_baseline` | 已定為某 screen 的視覺基準，但仍不代表可直接進 runtime。 |
| `rejected` | 不採用。 |
| `archived` | 被更新版本或決策取代。 |

## 3. Candidate Entries

### `gui_asset_facility_synthesis_screen_mockup_v0_candidate_001`

```yaml
asset_id: gui_asset_facility_synthesis_screen_mockup_v0_candidate_001
status:
  - generated_candidate
  - reviewed_candidate
  - accepted_direction
  - needs_v2

screen_id: facility_synthesis_screen
flow_id: flow_a_town_facility
asset_type: screen_mockup
asset_role: ui3_visual_concept
version: v0
candidate_number: 001

project_asset_path: null
project_reference_path: 05_assets/gui_references/facility_synthesis_screen/facility_synthesis_screen_mockup_v0_candidate_001.png
source_generated_path: C:\Users\user\.codex\generated_images\019e35b5-5f6f-7e62-b550-11d7009b116c\ig_0fe2a899f30af140016a09b731ab808191aaf9352e03d706a1.png

linked_documents:
  request: 01_content/gui-facility-synthesis-mockup-request.md
  prompt: 01_content/gui-facility-synthesis-prompt-draft.md
  direction_brief: 01_content/gui-ui-direction-brief.md
  asset_request_schema: 01_content/gui-asset-request-schema.md

generation_scope:
  generated_count: 1
  expanded_to_other_screens: false
  generated_as_final_asset: false
  copied_into_project_assets: false

intended_use:
  - First UI-3 visual concept candidate for Mila's synthesis house.
  - Validate warm workshop visual direction.
  - Validate list-detail-confirm-result facility layout.
  - Preserve NPC interaction presence through Mila / facility portrait.

not_intended_for:
  - Runtime use.
  - Final GUI implementation.
  - Direct import into 05_assets.
  - Full asset pipeline kickoff.
  - Shop / Forge / Magic screen final layout.

accepted_direction_notes:
  - Warm frontier workshop direction works.
  - Parchment, wood, brass, soft lamplight, and subtle blue crystal accents fit the project tone.
  - The screen reads as a synthesis / crafting facility.
  - Mila / NPC portrait has strong and useful facility interaction presence.
  - The main layout communicates category, recipe list, detail, requirements, actions, and result regions.
  - Left list scroll language is acceptable; row height can be adjusted later instead of treating the list as a layout failure.

known_issues:
  - Central detail text-safe zones need to be clearer for dynamic Chinese text.
  - Material / requirement rows should support icon + material name + required count + owned count, not icon-only.
  - Bottom result message region should better support one to two lines of Chinese feedback.

v2_refinement_focus:
  - Improve central detail panel Chinese text-safe zones.
  - Widen and structure material / requirement rows.
  - Preserve one to two lines of bottom result feedback text.
  - Keep Mila / NPC portrait at strong size.
  - If necessary, shift portrait only slightly right without cropping face.
  - Keep left recipe list scrollable; allow fewer, taller rows.

dynamic_text_policy:
  baked_text_allowed: false
  render_layer_text_required: true
  candidate_contains_intentional_text: false

approval_notes:
  user_confirmed:
    - UI-3 visual concept direction.
    - Keep Mila / NPC portrait presence.
    - Desktop 16:9 only.
    - Left list is acceptable because it has scroll language.
    - V2 focus should be central detail, material requirements, and bottom result text.
```

### `gui_asset_facility_synthesis_screen_mockup_v2_candidate_001`

```yaml
asset_id: gui_asset_facility_synthesis_screen_mockup_v2_candidate_001
status:
  - generated_candidate
  - reviewed_candidate
  - reference_only

screen_id: facility_synthesis_screen
flow_id: flow_a_town_facility
asset_type: screen_mockup
asset_role: ui3_visual_concept_v2
version: v2
candidate_number: 001

project_asset_path: null
project_reference_path: 05_assets/gui_references/facility_synthesis_screen/facility_synthesis_screen_mockup_v2_candidate_001.png
source_generated_path: C:\Users\user\.codex\generated_images\019e35b5-5f6f-7e62-b550-11d7009b116c\ig_0fe2a899f30af140016a09cf47b51c8191964d2ff640642760.png

linked_documents:
  prompt: 01_content/gui-facility-synthesis-v2-prompt-draft.md
  facility_template: 01_content/gui-facility-screen-template.md
  registry: 01_content/gui-asset-registry-draft.md

generation_scope:
  generated_count: 1
  copied_into_project_assets: false
  copied_into_project_references: true
  runtime_usage_allowed: false

intended_use:
  - Preserve V2 synthesis visual exploration history.
  - Compare against v0 and later facility template decisions.

not_intended_for:
  - Runtime use.
  - Current accepted synthesis baseline.
  - Direct import into 05_assets as formal runtime asset.

review_notes:
  - Kept as a project reference image only.
  - Not currently marked as the accepted synthesis visual baseline.
  - Later facility synthesis direction should still be judged against text-safe detail zones, material requirement rows, bottom feedback space, and NPC presence.

dynamic_text_policy:
  baked_text_allowed: false
  render_layer_text_required: true
```

## 4. Human Review Summary

目前此候選圖適合作為第一版合成屋 UI 視覺方向參考，但不適合作為最終 asset 直接使用。

可保留：

- 整體溫暖工坊氣氛。
- 羊皮紙、木材、黃銅、柔和燈火與少量藍色晶體點綴。
- 米菈 / NPC 的存在感。
- 左側分類與可滾動列表語彙。
- 中央詳情與底部 action / feedback 的大方向。

需要 V2 微調：

- 中央詳情區需要更清楚的中文文字安全區。
- 素材需求區需要能放素材名稱與數量。
- 底部結果訊息區需要穩定容納 1-2 行中文提示。

### `gui_asset_guild_screen_visual_baseline_v1_user_reference`

```yaml
asset_id: gui_asset_guild_screen_visual_baseline_v1_user_reference
status:
  - user_reference
  - reviewed_candidate
  - accepted_direction
  - accepted_visual_baseline

screen_id: facility_guild_screen
flow_id: flow_a_town_facility
asset_type: screen_mockup
asset_role: guild_visual_baseline
version: v1
candidate_number: user_reference_001

project_asset_path: null
project_reference_path: 05_assets/gui_references/guild_screen/guild_screen_visual_baseline_v1_user_reference.png
source_user_path: 05_assets/gui_references/guild_screen/guild_screen_visual_baseline_v1_user_reference.png

linked_documents:
  visual_baseline: 01_content/gui-guild-screen-visual-baseline.md
  facility_template: 01_content/gui-facility-screen-template.md
  direction_brief: 01_content/gui-ui-direction-brief.md

generation_scope:
  generated_by_current_session: false
  user_provided_reference: true
  copied_into_project_assets: false
  copied_into_project_references: true
  runtime_usage_allowed: false

intended_use:
  - First accepted visual baseline for Guild Screen.
  - Define Adventurers' Guild / Quest Board layout.
  - Preserve receptionist character interaction.
  - Clarify quest list, quest details, reward summary, condition checklist, feedback, and primary action regions.

not_intended_for:
  - Runtime use.
  - Direct import into 05_assets.
  - Final GUI implementation without further layout/model work.
  - Full guild management system.

accepted_direction_notes:
  - Best positioned as Adventurers' Guild / Quest Board.
  - Keep one clear Guild title area.
  - Remove ambiguous top resource slots and top-right black info box.
  - Left list is for quest scanning only: task name, location, recommended level, status icon.
  - Central main panel is for quest name, type, location, recommended level, and description.
  - Reward summary is separate from completion / turn-in requirements.
  - Lower table is a task condition / turn-in checklist.
  - Bottom dark bar is NPC guidance and operation feedback.
  - Bottom-right remains a single dynamic primary action.

dynamic_text_policy:
  baked_text_allowed: false
  render_layer_text_required: true

approval_notes:
  user_confirmed:
    - This version matches the intended Guild Screen direction.
    - Use it as the baseline for Guild Screen planning.
```

## 5. Future Registry Fields 草案

若未來建立正式 registry，可考慮欄位：

```yaml
asset_id:
screen_id:
asset_type:
asset_role:
version:
status:
project_asset_path:
source_generated_path:
source_prompt_path:
source_request_path:
created_date:
reviewed_date:
approved_by:
usage_allowed:
runtime_reference_allowed:
dynamic_text_safe:
known_issues:
replacement_of:
replaced_by:
notes:
```

## 6. 下一步建議

建議下一步仍不要直接啟動正式 asset pipeline。較合理的後續是二選一：

1. 依照 `gui-facility-synthesis-prompt-draft.md` 的 V2 refinement notes，準備第二版 prompt 草案，但暫不生成。
2. 若要生成第二張候選圖，需先明確批准「只生成一張 V2 `facility_synthesis_screen` UI-3 visual concept」，且仍不擴到其他 screen。
