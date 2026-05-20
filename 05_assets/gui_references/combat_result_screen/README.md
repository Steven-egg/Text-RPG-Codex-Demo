# Combat Result Screen GUI References

Purpose: preserve user-provided combat result mockups as visual references for static prototype planning.

## Files

```text
combat_result_visual_reference_v1_user_mockup_victory.png
```

## Reference Notes

### `combat_result_visual_reference_v1_user_mockup_victory.png`

- Source: user-provided mockup.
- Screen: Combat Result Screen.
- State: victory/result screen with rewards, level-up feedback, loot, battle log, narrative summary, and continue actions.
- Intended use: guide the combat result static prototype layout, reward summary hierarchy, post-battle narrative region, battle log placement, and continue-exploration CTA.

## Accepted Direction

- Combat result should clearly separate victory status, reward summary, loot, narrative result text, and battle log.
- Gold, EXP, level changes, obtained items, battle log lines, and action labels should be rendered by the prototype layer.
- Primary action should support returning to dungeon exploration after the result screen.
- Secondary actions can support viewing items and status.
- This reference can guide result presentation, but not reward calculation or runtime state updates.

## Boundaries

- This file is a reference image only.
- Do not treat it as a runtime asset.
- Do not import it into `03_engine`.
- Do not connect it to runtime data, schema, save data, or combat formulas.
- Do not start a formal asset pipeline from this file.
- Do not use this image as the static prototype's actual result background unless a later asset-pipeline decision explicitly approves it.
