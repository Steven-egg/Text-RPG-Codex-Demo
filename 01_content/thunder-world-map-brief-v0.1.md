# Thunder World Map Brief v0.1

Purpose: record the selected Thunder region world-map direction for future
visual candidate generation. This brief is planning only. It does not approve
image generation, GUI implementation, runtime data edits, quest text edits,
schema changes, save changes, combat changes, asset-pipeline work, staging, or
commits.

Use this file with:

- `01_content/world-content-skeleton-v0.1.md`
- `01_content/ui-art-prep-brief-v0.1.md`
- `01_content/naming-lexicon-v0.1.md`

## Selected Direction

Thunder region world map display direction:

- Region: `鳴雷天原`
- Town hub: `雲港塔城`
- Minor dungeon A: `裂雷高原`
- Minor dungeon B: `導雷水道`
- Main dungeon: `雷光塔`
- Main phase 1: `下層陣列`
- Main phase 2: `冠頂陣列`

The Thunder world map should feel like a storm plateau and sky-road region, not
only a lightning tower. It includes highland cliffs, storm clouds, floating
stone paths, conductive waterways, copper-toned rails or conduits, sky bridges,
and a central tower route rising into the clouds.

## World Map Composition

Match the broad readability of the Ice world map visual reference:

- High-angle fantasy world-map view, not a parchment map.
- Clear routes and node readability from the town hub to each major location.
- `雷光塔` sits near the center as the main visual endpoint.
- `雲港塔城` sits to the side on a high cliff, still large enough to read as the
  regional town hub.
- `裂雷高原` appears on the ground-level or near-side route as a storm-cut
  plateau.
- `導雷水道` appears as a visible side route with conductive channels, wet stone,
  copper rails, or charged water control structures.
- Routes should show an upward progression from plateau paths to sky roads,
  then into `雷光塔` and its `下層陣列` / `冠頂陣列` climb.

Do not put readable text labels inside the image. Region and location names
belong in UI, documents, or candidate tables, not in the generated map image.

## Visual Mood

Target mood:

- Grand, charged, and readable.
- Storm clouds opening with dramatic broken light.
- The central tower, side hub city, sky roads, floating stones, conductive
  channels, and highland rock surfaces all remain visually legible.
- Thunder should remain the core identity; water appears as conductive terrain
  and weather support, not as the dominant element.

Use `雲光銅石分層` for visual variety:

- Broken cloud light and gray-white storm clouds.
- Blue-white lightning around the tower and array structures.
- Copper-toned rails, conduits, or channel edges.
- Floating stones and highland rock surfaces.
- Warm hub lights from the side cliff city.

## Decorative Landmarks

These landmarks are world-map visual vocabulary only. They are not quest
requirements, unlock keys, runtime locations, or mandatory quest-description
text.

- `天路雷橋`
- `導雷雲渠`
- `浮石環`
- `破雲冠環`

## Image Brief Draft

Create a high-angle fantasy world map of `鳴雷天原`, a Thunder-element storm
plateau and sky-road region. The map centers on `雷光塔`, a cloud-piercing
lightning tower with visible lower array structures and a crown array near the
cloud break. The route should read as an ascent: ground-level highland paths,
storm-cut plateau roads, conductive waterways, floating stone paths, sky
bridges, and finally the tower climb.

Place `雲港塔城` to the side on a high cliff, large enough to read as a real
regional hub. It should have air-harbor platforms, towers, docks or landing
decks, air bridges, roads connected to the plateau, warm city lights, and a
clear relationship to the sky-road network. In the near or ground route, show
`裂雷高原` as a wide storm-broken plateau. On a side route, show `導雷水道` as
charged water channels, wet stone, copper rails, and conductive control
structures.

Lighting should show storm clouds breaking open with dramatic light. Use
blue-white lightning, gray-white cloud layers, copper rails, floating stones,
highland rock, and warm hub lights so the scene does not become a one-note blue
or purple thunderstorm. The image should have no text labels, no watermarks, no
UI overlay, and no unreadable generated writing.

## Negative Constraints

Avoid:

- Text labels or map lettering inside the image.
- A tiny side hub that looks smaller than a later-region town should be.
- A single tower-only composition with no readable regional route.
- A water-dominant map where Thunder no longer feels like the main identity.
- Snowfield, icy coast, lava, desert, forest-only, or Final-region siege
  identity.
- A one-note blue or purple storm palette with no rock, copper, cloud, or city
  light separation.

## Acceptance Criteria

- The image reads as Thunder at first glance, distinct from Fire, Ice, Earth,
  and Final.
- `雷光塔` reads as the central destination and has a visible lower-to-crown
  route.
- `雲港塔城` reads as a later-region town hub even though it is placed to the
  side.
- The route structure is legible: plateau to conductive waterway, sky roads,
  lower tower array, and crown array.
- Floating stones, conductive channels, copper-toned conduits, storm clouds,
  broken cloud light, highland rock, and air-harbor city elements are present
  without making the scene visually cluttered.
- No visible text labels, watermarks, UI overlays, snowfield theme, desert
  theme, lava theme, or one-note thunderstorm treatment.

## Boundaries

This brief does not approve:

- Generating an image.
- Adding image files under `05_assets/`.
- Editing `07_gui_prototype/`.
- Editing runtime data, quest text, schema, save data, combat, or registry.
- Starting a formal asset pipeline.

Before any future image generation or placement work, get explicit approval for
the exact surface and whether the output is a reference candidate, a GUI
prototype placeholder, or a formal asset-pipeline target.
