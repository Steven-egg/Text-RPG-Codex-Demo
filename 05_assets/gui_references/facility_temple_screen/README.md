# Temple Screen GUI References

Purpose: preserve user-provided temple/church mockups as visual references for static prototype planning.

## Files

- [temple_screen_visual_reference_v1_user_mockup_main.jpg](file:///c:/Users/User/OneDrive/文字冒險遊戲/05_assets/gui_references/facility_temple_screen/temple_screen_visual_reference_v1_user_mockup_main.jpg)

## Reference Notes

### `temple_screen_visual_reference_v1_user_mockup_main.jpg`

- Source: user-provided GUI mockup.
- Screen: Temple Screen (聖光教會).
- State: classic JRPG immersive layout featuring NPC Sister Elisia, a dialogue frame, and an action menu.
- Intended use: guide the temple static prototype toward a visual-novel dialogue interface, replacing the complex 3-column layout.

## Accepted Direction

- The screen shifts from multiple card panels (moon well, altar, inquiry) to a unified JRPG dialogue shell.
- Top status bar integrates location title, HP, MP, and gold displays.
- Bottom actions are simplified to: `詢問關於主線與聖痕` (story inquiries) and `轉職預覽與引導` (promotion preview modal), and `返回城鎮` (back to town).
- The "祈禱與祝福 / 汲取月露" option is removed from the visible static prototype to keep the screen focused and avoid pre-flight chores.

## Boundaries

- Reference image only; do not use as a runtime background or runtime asset.
- This file is a reference-only mockup, not a formal asset pipeline output.
- Static prototype only; do not connect the Python runtime or read/write `save.json`.
- No drift to gameplay data, data schemas, save state schema, or combat formula.
- Keep detailed visual rationale here rather than in README or the Hot Zone handoff.
