# GUI References

用途：暫存 GUI 視覺概念圖、使用者提供的參考圖、候選 mockup 與人工審查用圖片。

## 邊界

- 這裡的圖片是 reference / candidate，不是正式 runtime asset。
- 不代表已啟動正式 asset pipeline。
- 不代表圖片已可直接進遊戲。
- 不應被 `03_engine` 或 runtime 直接引用。
- 若未來要正式使用，需另行整理到正式 asset path，並補命名、來源、版本、授權 / 生成紀錄與替換策略。

## 建議命名

```text
guild_screen_visual_baseline_v1_user_reference.png
facility_synthesis_screen_mockup_v0_candidate_001.png
facility_synthesis_screen_mockup_v2_candidate_001.png
world_map_visual_reference_v1_user_mockup_menu_open.png
world_map_visual_reference_v1_user_mockup_detail_drawer.png
```

## 建議子資料夾

```text
05_assets/gui_references/town_hub/
05_assets/gui_references/guild_screen/
05_assets/gui_references/facility_synthesis_screen/
05_assets/gui_references/world_map/
```

## World Map references

- `world_map/world_map_visual_reference_v1_user_mockup_menu_open.png`: World Map user mockup showing the top-left menu opened as a left-side drawer.
- `world_map/world_map_visual_reference_v1_user_mockup_detail_drawer.png`: World Map user mockup showing a selected map point with the right-side information drawer open.

These World Map files are reference-only images. They should guide the static prototype layout, drawer behavior, and visual direction, but they are not runtime assets and should not be imported into the engine or used as gameplay data.

## Regional Placeholder Candidates - 2026-06-21

These generated images are visual references only. They are not runtime assets,
gameplay data, schema inputs, save data, or formal asset-pipeline outputs. Do
not import them into `03_engine`, `04_data`, `02_schema`, `save.json`, or GUI
runtime bridge code without a later exact-scope approval.

Current regional world map candidates:

- `ice-world-map-placeholder-candidate-v01.png`: existing Ice world map visual reference.
- `earth-world-map-placeholder-candidate-v01.png`: Earth world map placeholder candidate.
- `thunder-world-map-placeholder-candidate-v01.png`: Thunder world map placeholder candidate; accepted as the current Thunder map reference.
- `final-world-map-placeholder-candidate-v01.png`: Final world map placeholder candidate; accepted as the current Final map reference.

Current regional town hub candidates:

- `ice-town-hub-placeholder-candidate-v01.png`: existing Ice town hub visual reference.
- `earth-town-hub-placeholder-candidate-v01.png`: Earth town hub placeholder candidate.
- `thunder-town-hub-placeholder-candidate-v01.png`: Thunder town hub placeholder candidate; accepted as the current Thunder hub reference.
- `thunder-town-hub-facility-layout-candidate-v01.png`: numbered Thunder hub layout reference; point 6 is the Relic / central plaza reference.
- `final-town-hub-placeholder-candidate-v01.png`: superseded Final hub draft; retained for history, but too character-heavy and less clear in facility color separation.
- `final-town-hub-placeholder-candidate-v02.png`: accepted as the current Final hub reference; cleaner no-people composition with more identifiable facility color zones.

Final town hub v02 facility layout reference:

1. Guild / command hall.
2. Workshop.
3. Synthesis / alchemy.
4. Storage / logistics.
5. Magic Shop / magic support.
6. Temple / healer pavilion.
7. Inn / rest area.
8. Shop / market supplies.
9. Relic / memorial plaza.

This numbered layout is a visual planning reference only. It does not define
runtime facility IDs, screen navigation, data entries, quest behavior, unlock
rules, or GUI bridge behavior.

## 目前 reference / candidate

- `town_hub/town_hub_visual_reference_v1_user_mockup.png`：Town Hub 使用者參考圖。
- `town_hub/town_hub_visual_mockup_candidate_v1_001.png`：Town Hub generated visual mockup candidate，僅作 reference。
- `guild_screen/guild_screen_visual_baseline_v1_user_reference.png`：Guild Screen visual baseline。
- `facility_synthesis_screen/`：Synthesis Screen historical mockup candidates。
