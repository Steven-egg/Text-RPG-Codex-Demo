# GUI Facility Image Generation Standard v0.1

Purpose: working standard for future GUI static prototype facility background
generation and review. This document defines prompt structure, visual scale,
placement, reference priority, comparison workflow, and metadata capture for
facility images used by `07_gui_prototype/`.

This is planning and review guidance only. It does not approve image generation,
formal asset-pipeline work, runtime changes, data changes, schema changes,
manual `save.json` work, GUI bridge work, or combat/formula changes.

## 1. Basic Rules

- Target canvas for current facility backgrounds: `1672x941`.
- Default GUI image destination after owner approval:
  `07_gui_prototype/<screen>/assets/`.
- `05_assets/` is a historical mockup / reference archive, not the current GUI
  asset pipeline. The owner may manually organize it; agents should not delete,
  move, or archive it by default.
- `07_gui_prototype/start_screen/assets/Alternate/` is an owner-created
  alternate folder. Do not process it unless explicitly requested.
- Facility images must not contain UI, captions, signs with readable text,
  runtime IDs, or gameplay claims.
- Display Name is the visual SSOT. Do not let runtime IDs override the display
  name's visual meaning.
- Existing Fire / current facility backgrounds are the primary scale and
  composition references. Ice candidates are problem-comparison references, not
  acceptance baselines.
- Temple is a special case: its NPC may be larger and more ceremonial than
  ordinary facility NPCs.

## 2. Detailed Visual Rules

### Canvas And Composition

- Use a wide facility composition matching the current GUI background grammar:
  right foreground NPC or main object, center work surface, and readable left /
  middle background depth.
- Preserve the mature fantasy GUI texture already present in Fire facilities:
  dark wood, metal detail, warm lamps, working surfaces, shelves, banners,
  counters, tools, and readable interior depth.
- The background should still read after CSS `cover` cropping and panel overlays.
- Avoid overly empty rooms, pure scenic landscapes, or close-up portraits with no
  facility context.

### UI Safety

Current facility screens commonly place information panels over the left and
middle areas, with a bottom action / feedback bar. The image must survive those
overlays.

- Keep the NPC face and core expression out of the bottom action area.
- Do not place the NPC face under the left list / catalog area or central detail
  panel.
- The right foreground is the preferred NPC zone, but the face should not touch
  the right crop edge.
- For ordinary NPC facilities, a useful draft target is:
  - face center: roughly `x 62%-86%`, `y 14%-42%`
  - shoulders / upper torso: right half to lower middle
  - hands / tools / counter: center-right lower third, allowed to be partly
    hidden by GUI panels
- Background focal props may sit center-left, but should remain recognizable
  when darkened or partially covered.

### NPC Size And Camera Distance

- Ordinary facility NPCs should feel like the existing guild / workshop / inn /
  magic shop / synthesis images: medium-close half-body or head-and-torso
  framing, not distant full-body shots.
- Avoid camera distance that makes the NPC much smaller than current Fire
  facility NPCs after GUI placement.
- Temple is exempt from the ordinary scale rule and may use a larger devotional
  figure.
- Male NPCs must avoid same-face / same-body drift. Give each man a distinct
  age, build, face shape, hair, posture, clothing silhouette, tool use, and
  expression.

### NPC Placement

- Right foreground is the default for NPC facilities.
- Keep the head inside the frame with breathing room above and to the right.
- Hands and profession props should be visible when possible, especially for
  workshop, shop, synthesis, magic shop, and guild reception roles.
- If the facility has no NPC, the focal object replaces the NPC: investigation
  table, warehouse shelves, sealed device, maps, crates, ropes, relic stand, or
  other screen-relevant props.

### Ice Visual Identity

Ice is not a pure glacier or empty snow cave. It should read as frost-tide coast:

- cold sea, fog harbor, salt frost, wet wood, ropes, ship silhouettes, lighthouse
  hints, misted windows, brass lanterns, damp paper, frost-blue ambient light
- cold blue environment plus warm yellow lamps, copper / brass, hearth fire, or
  forge glow
- dark wood and metal remain important so Ice shares the same mature GUI fantasy
  language as the Fire facilities
- avoid all-white snowfields, sterile ice caves, or outdoor-only scenes unless
  the specific facility requires it

## 3. Reference Read List

Primary current GUI references:

- `07_gui_prototype/guild_screen/assets/guild-background.jpg`
- `07_gui_prototype/workshop_screen/assets/workshop-background.jpg`
- `07_gui_prototype/workshop_screen/assets/workshop-background-02.jpg`
- `07_gui_prototype/inn_screen/assets/inn-background.jpg`
- `07_gui_prototype/magic_shop_screen/assets/magic-shop-background.jpg`
- `07_gui_prototype/synthesis_screen/assets/synthesis-background.jpg`
- `07_gui_prototype/temple_screen/assets/temple-background.jpg`
- `07_gui_prototype/storage_screen/assets/storage-background.jpg`

Problem-comparison references only:

- `07_gui_prototype/guild_screen/assets/ice-guild-background-with-noah-candidate-v02.png`
- `07_gui_prototype/workshop_screen/assets/ice-weapon-workshop-with-gray-candidate-v01.png`

Naming / visual SSOT references, read-only:

- `01_content/asset-production-inventory-v0.1.md` Ice facility rows
- `04_data/data/display_names.py` display names and NPC names

Known Ice facility NPC allocation:

| Facility Display Name | NPC |
|---|---|
| 霜潮工會聯絡所 | 諾亞, female |
| 霜鐵工坊 | 格雷, male |
| 霜碑神殿 | 賽恩, male; temple scale exception |
| 霜潮旅店 | 霜潮旅店掌櫃, male |
| 鹽霧護具鋪 | 布琳, female |
| 寒港補給鋪 | 拉比, female |
| 霜潮合成台 | 米菈, female |
| 冰燈魔法商店 | 伊芙, female |
| 冰印調查台 | no NPC |
| 港口倉庫 | no NPC |

Naming note: `格雷` is canonical in CLI/data. Some GUI text may still show
`葛雷`; generated images should not contain text.

## 4. Prompt Templates

### Ordinary NPC Facility

```text
[Facility Display Name], mature fantasy JRPG facility background for GUI static
prototype, 1672x941 wide canvas, right foreground [NPC name, gender, profession,
age/build/face/hair/gesture], medium-close half-body, face in the upper-right
safe zone, hands and working surface visible, readable left and middle interior
depth, [facility-specific props], frost-tide coast identity, cold blue ambient
light plus warm brass lantern/firelight, dark wood and metal details, rich but
not cluttered, no text, no UI.
```

Fill-in fields:

- `Facility Display Name`
- `NPC name / gender / role`
- `age/build/face/hair/gesture`
- `facility-specific props`
- `regional material details`

### No-NPC Facility

```text
[Facility Display Name], mature fantasy JRPG facility background for GUI static
prototype, 1672x941 wide canvas, no character, primary visual focus on
[investigation table / warehouse shelves / sealed device / maps / cargo],
center-right midground, readable left-side background depth, frost-tide coast
identity, cold blue ambient light plus warm brass lantern/firelight, dark wood,
metal, rope, salt frost, no text, no UI.
```

### Temple Exception

```text
[Facility Display Name], sacred frost temple interior, 1672x941 wide canvas,
[NPC name, gender, role] as a closer ceremonial foreground figure, larger than
ordinary facility NPCs, centered-right but not edge-cropped, solemn ritual
posture, frost stone tablet, altar, pillars, soft divine light, cold blue and
warm candle contrast, no text, no UI.
```

### Negative Prompt / Avoid List

```text
text, captions, logo, UI panels, signs with readable words, runtime IDs,
cropped face, face at image edge, tiny distant NPC, full-body far shot,
duplicate male face, same body type, same pose, plain white snowfield, empty ice
cave, modern objects, extra fingers, broken hands, warped tools, unreadable
clutter, overexposed pure white ice, image with no usable left/middle background
depth.
```

## 5. Review And Overlay Pipeline

Manual owner workflow currently compares candidates by temporarily replacing the
GUI asset, taking screenshots, restoring the original, then overlaying candidate
and current screenshots at about `50%-60%` opacity.

Preferred future agent-assisted workflow, if separately approved:

- Use a non-destructive preview manifest instead of moving or replacing files by
  hand.
- Record original asset path, candidate path, hashes, dimensions, screen route,
  screenshot output paths, and restore status.
- Preview candidate images by temporary CSS override or generated preview page,
  not by permanently swapping source assets.
- Produce a before / after / overlay / contact-sheet package.
- Report only paths and compact metrics unless the owner asks to inspect images.
- Abort if expected files are missing, dimensions mismatch, hashes changed, or a
  restore step cannot be proven.

This standard does not approve implementation of that tool. It only defines the
desired safety shape.

## 6. File Format And Metadata

- Production candidates may use PNG while art is still being reviewed.
- Do not knowingly create new long-term files where PNG bytes are disguised with
  a `.jpg` extension.
- Final destructive compression and format unification can wait until later
  polish.
- Existing files may already have extension/content drift; do not rewrite them
  unless the owner approves that exact asset surface.

Prompt and seed extraction:

- PIL / PieXif or similar tools may read PNG text chunks or EXIF from some
  generated images.
- Metadata availability depends on the generator and export path; many tools
  strip prompt or seed data.
- If Codex image generation or another tool does not expose a reliable seed,
  record `unknown`; do not claim reproducibility.

Recommended sidecar metadata:

```json
{
  "image_id": "",
  "display_name": "",
  "region": "ice",
  "facility": "",
  "intended_gui_path": "",
  "canvas": "1672x941",
  "npc": {
    "name": "",
    "gender": "",
    "role": "",
    "scale_rule": "ordinary | temple_exception | none"
  },
  "prompt": "",
  "negative_prompt": "",
  "reference_images": [],
  "date": "",
  "tool": "",
  "model": "",
  "seed": "unknown",
  "review_status": "candidate | accepted | rejected",
  "owner_notes": "",
  "accepted_or_rejected_reason": "",
  "comparison_outputs": {
    "before": "",
    "after": "",
    "overlay": "",
    "contact_sheet": ""
  }
}
```

Sidecar naming options:

- `<image>.meta.json` for structured metadata
- `<image>.prompt.md` for human-readable prompt review

## 7. Minimum Next Step

Owner should confirm or adjust this standard before any next phase:

- create or refine a non-destructive preview / overlay helper
- regenerate guild or workshop candidates
- generate the next Ice facility image
- update GUI image references or screen assets

Any of those follow-up phases needs separate exact-surface approval.
