# World Map GUI References

Purpose: preserve user-provided World Map mockups as visual references for static prototype planning.

## Files

```text
world_map_visual_reference_v1_user_mockup_menu_open.png
world_map_visual_reference_v1_user_mockup_detail_drawer.png
```

## Reference Notes

### `world_map_visual_reference_v1_user_mockup_menu_open.png`

- Source: user-provided mockup.
- Screen: World Map.
- State: top-left main menu button opened as a left-side drawer.
- Intended use: guide the World Map static prototype menu behavior, top player/resource strip, map-first composition, and left drawer proportions.

### `world_map_visual_reference_v1_user_mockup_detail_drawer.png`

- Source: user-provided mockup.
- Screen: World Map.
- State: map location selected, with a right-side information drawer visible.
- Intended use: guide the World Map static prototype location selection behavior, right detail drawer, location metadata rows, and confirm-travel CTA placement.

## Accepted Direction

- The World Map should use the map as the main full-width stage.
- The top-left menu button opens a left-side main menu drawer.
- Clicking a map location opens or updates a right-side location information drawer.
- The right detail drawer is not shown by default.
- Location names, status, rewards, levels, and action text should be rendered by the prototype layer, not baked into the reference image.

## Boundaries

- These files are reference images only.
- Do not treat them as runtime assets.
- Do not import them into `03_engine`.
- Do not connect them to runtime data, schema, save data, or combat formulas.
- Do not start a formal asset pipeline from these files.
- Do not use these images as the static prototype's actual map background unless a later asset-pipeline decision explicitly approves it.
