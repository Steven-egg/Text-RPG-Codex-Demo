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

## 目前 reference / candidate

- `town_hub/town_hub_visual_reference_v1_user_mockup.png`：Town Hub 使用者參考圖。
- `town_hub/town_hub_visual_mockup_candidate_v1_001.png`：Town Hub generated visual mockup candidate，僅作 reference。
- `guild_screen/guild_screen_visual_baseline_v1_user_reference.png`：Guild Screen visual baseline。
- `facility_synthesis_screen/`：Synthesis Screen historical mockup candidates。
