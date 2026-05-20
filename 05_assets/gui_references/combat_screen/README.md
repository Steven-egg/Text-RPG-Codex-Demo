# Combat Screen GUI References

Purpose: preserve user-provided combat screen mockups as visual references for static prototype planning.

## Files

```text
combat_screen_visual_reference_v1_user_mockup_command.png
```

## Reference Notes

### `combat_screen_visual_reference_v1_user_mockup_command.png`

- Source: user-provided mockup.
- Screen: Combat Screen.
- State: active battle command screen with player status, enemy status, battle log, and command buttons.
- Intended use: guide the combat static prototype layout, battle HUD proportions, command bar placement, enemy focus area, player status panel, and battle log behavior.

## Accepted Direction

- Combat screen should keep the battlefield as the main visual stage.
- Enemy name, HP, weakness, round count, player HP/MP, command labels, and battle log text should be rendered by the prototype layer.
- Bottom command actions should represent UIAction choices such as attack, skill, item, defend, and flee.
- Combat log should be readable without covering the main command controls.
- This reference can guide visual hierarchy, but not combat formulas or runtime behavior.

## Boundaries

- This file is a reference image only.
- Do not treat it as a runtime asset.
- Do not import it into `03_engine`.
- Do not connect it to runtime data, schema, save data, or combat formulas.
- Do not start a formal asset pipeline from this file.
- Do not use this image as the static prototype's actual battle background unless a later asset-pipeline decision explicitly approves it.
