# Dungeon Exploration Screen GUI References

Purpose: preserve user-provided dungeon exploration mockups as visual references for static prototype planning.

## Files

```text
dungeon_exploration_visual_reference_v1_user_mockup_main.png
```

## Reference Notes

### `dungeon_exploration_visual_reference_v1_user_mockup_main.png`

- Source: user-provided mockup.
- Screen: Dungeon Exploration Screen.
- State: dungeon route/exploration step view with location summary, exploration status, narrative text, and bottom actions.
- Intended use: guide the dungeon exploration static prototype layout, location information panel, current run status panel, narrative message region, and exploration action buttons.

## Accepted Direction

- Dungeon exploration should use the dungeon scene as the main visual stage.
- Location name, recommended level, player level, element, route length, current step, HP/MP, run rewards, and item summary should be rendered by the prototype layer.
- Bottom actions should represent UIAction choices such as advance, retreat, view items, and status.
- The central message region should support short exploration narration without pushing the command bar off-screen.
- This reference can guide exploration flow presentation, but not runtime dungeon generation or combat formulas.

## Boundaries

- This file is a reference image only.
- Do not treat it as a runtime asset.
- Do not import it into `03_engine`.
- Do not connect it to runtime data, schema, save data, or combat formulas.
- Do not start a formal asset pipeline from this file.
- Do not use this image as the static prototype's actual dungeon background unless a later asset-pipeline decision explicitly approves it.
