# Inn Screen GUI References

Purpose: preserve user-provided inn screen mockups as visual references for static prototype planning.

## Files

- [inn_screen_visual_reference_v1_user_mockup_cli.png](file:///c:/Users/User/OneDrive/文字冒險遊戲/05_assets/gui_references/facility_inn_screen/inn_screen_visual_reference_v1_user_mockup_cli.png)
- [inn_screen_visual_reference_v1_user_mockup_main.jpg](file:///c:/Users/User/OneDrive/文字冒險遊戲/05_assets/gui_references/facility_inn_screen/inn_screen_visual_reference_v1_user_mockup_main.jpg)

## Reference Notes

### `inn_screen_visual_reference_v1_user_mockup_cli.png`

- Source: user-provided CLI mockup.
- Screen: Inn Screen (微光旅店).
- State: CLI Rich panel displaying room service cost (30G), current gold (620G), HP/MP (156/156, 29/29), rest prompt, and post-rest health recovery message.
- Intended use: represent the target gameplay functionality and dialogue text for the Inn Rest option.

### `inn_screen_visual_reference_v1_user_mockup_main.jpg`

- Source: user-provided GUI mockup.
- Screen: Inn Screen (金鹿旅店).
- State: classic JRPG immersive layout featuring NPC Lily, a dialogue frame, and an action menu.
- Intended use: guide the inn static prototype toward a visual-novel dialogue interface, replacing the complex 3-column layout.

## Accepted Direction

- The screen shifts from multiple card panels to a unified JRPG dialogue shell.
- Top status bar integrates location title, HP, MP, and gold displays.
- Bottom actions are simplified to core gameplay choices: `休息` (rest at inn) and `返回城鎮` (back to town).
- The "聊聊" (Talk/Rumors) option is removed to keep the demo content focused and avoid bloat.

## Boundaries

- Reference images only; do not use as runtime backgrounds or runtime assets.
- These files are reference-only mockups, not formal asset pipeline outputs.
- Static prototype only; do not connect the Python runtime or read/write `save.json`.
- No drift to gameplay data, data schemas, save state schema, or combat formula.
- Keep detailed visual rationale here rather than in README or the Hot Zone handoff.
