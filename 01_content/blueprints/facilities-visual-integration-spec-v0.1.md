# Facilities Visual Integration Spec V0.1

Status: Draft comparison reference, paused by owner after experiment retirement

Scope: GUI skinning and visual integration only

## 1. Purpose

This document records the emerging visual grammar across the current facility
screens. It supports comparison, visual review, and narrow follow-up planning
before later screen families are skinned.

This document is not:

- an implementation order;
- a runtime, bridge, gameplay, save/load, or data plan;
- a formal design system, component library, schema, or asset pipeline;
- authority to make CSS, HTML, JavaScript, asset, or documentation changes.

Current posture:

- facility skinning exploration is complete and `08_experiments/` is retired;
- accepted results live in the formal `07_gui_prototype/` screens;
- this comparison reference is paused and has no active implementation slice.

Use the following evidence labels when extending this document:

- **Observed CSS**: directly verified in the current stylesheet.
- **Observed structure**: directly verified in current prototype files or the
  facility shell baseline.
- **Owner accepted**: explicitly accepted through visual review.
- **Proposed**: a candidate that still needs comparison or screenshots.
- **TBD**: insufficient evidence.

Do not promote **Proposed** or **TBD** statements into shared standards without
visual review.

## 2. Relationship To Existing Guidance

Read this document after:

- `01_content/blueprints/gui-facility-shell-baseline-v0.1.md`
- `01_content/archive/gui-facility-screen-template.md`

The facility shell baseline owns the responsibility split:

```text
AI facility hero image
-> HTML/CSS/JS overlay
-> runtime-backed state and action semantics
```

This document adds a comparison layer over current facility CSS. It does not
replace `AGENTS.md`, the current agent's skills, the GUI static sprint rules, or
screen-level progress records.

## 3. Boundaries

In scope:

- facility-family visual comparison;
- CSS and layout grammar;
- title, panel, button, disabled-state, feedback, and readability review;
- background and NPC composition guidance;
- comparison tables and narrow visual candidates.

Out of scope:

- runtime, bridge, `ScreenModel`, or `UIAction` behavior changes;
- gameplay, data, schema, save/load, economy, balance, or combat changes;
- direct CSS, HTML, JavaScript, fixture, or asset implementation;
- formal JSON/YAML schemas or an asset registry;
- forcing every facility into one layout.

## 4. Observed Facility Families

| Family | Current members | Shared visual priority |
| --- | --- | --- |
| List-Detail-Service | Shop, Magic Shop, Synthesis, Guild; Workshop as a hybrid | list scanning, selected detail, requirements, action availability, feedback |
| Hero-Dialogue-Service | Inn, Temple | scene and NPC presence, dialogue readability, compact service choices |
| Specialized Workspace / Showcase | Storage, Relic Preview | operation clarity or object focus, stable state and action presentation |

Facility families are comparison groups, not mandatory layout templates.

## 5. Observed Shared Visual Grammar

The following patterns are directly visible in current facility stylesheets:

- facility backgrounds are loaded through CSS images;
- dark translucent panels use accent borders, shadows, and frequent blur;
- most title blocks use a left accent border and a horizontal dark-to-transparent
  gradient;
- facility titles use `Noto Serif TC`, heavy weight, letter spacing, and layered
  text shadow;
- primary actions use dark accent gradients and stronger hover glow;
- disabled actions use muted color, reduced opacity, no glow, and
  `cursor: not-allowed`;
- accent palettes vary by facility while preserving the same broad material
  language;
- fixture controls and UIAction logs are hidden in current visual skinning
  styles;
- functional UI remains HTML/CSS/JS overlay content rather than image-baked UI.

This is an emerging grammar, not a formal shared CSS API.

## 6. Current CSS Comparison

This table was filled from the current facility `styles.css` files. Values
describe the current CSS only; they are not recommended standards.

| Facility | Family | Title selector and size | Title block | Resource summary | Primary action sizing | Disabled selector | Background | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Shop | List-Detail-Service | `h1`; `clamp(2rem, 3.2vw, 3rem)` | `.title-copy`; gold left border and gradient | hidden in accepted layout through `[hidden]` | `70px` | `[aria-disabled="true"]` | `url('./bg-npc.jpg')` | Reference member of the normalized Shop family |
| Guild | List-Detail-Service task variant | `h1`; `clamp(2rem, 3.2vw, 3rem)` | `.title-copy`; gold left border and gradient | forced hidden | `min-height: 58px` | `[aria-disabled="true"]` | `var(--facility-background-image)` | Uses larger `8px` action radius than Shop |
| Magic Shop | List-Detail-Service | `h1`; `clamp(2rem, 3.2vw, 3rem)` | `.title-copy`; magenta left border and gradient | visible | `70px` | `[aria-disabled="true"]` | `var(--facility-background-image)` | Closely matches Shop geometry with arcane accents |
| Synthesis | List-Detail-Service | `h1`; `clamp(2.2rem, 4.1vw, 4.65rem)` | `.title-copy`; warm gold left border and gradient | hidden in accepted layout through `[hidden]` | `min-height: 58px` | `[aria-disabled="true"]` | `var(--facility-background-image)` | Large-title exception; keep pending screenshot review |
| Workshop | List-Detail-Service hybrid | `.title-zone .main-title`; final override reaches `clamp(2.5rem, 4.4vw, 4.55rem)` | `.title-zone`; related gradient treatment | shared player/resource strip not used; player info hidden | multiple action rule blocks; `70px` and later `min-height: 58px` appear | `:disabled` | `var(--facility-background-image)` | Multiple later overrides make screenshot review necessary before normalization |
| Inn | Hero-Dialogue-Service | `.hud-location-name`; `clamp(1.8rem, 2.8vw, 2.5rem)` | `.title-copy`; warm gold left border and gradient | visible HUD resources | `.action-btn` is `70px` | `:disabled` | `url('./assets/inn-background.jpg')` | Dialogue and service choice hierarchy is family-specific |
| Temple | Hero-Dialogue-Service | `.hud-location-name`; `clamp(1.8rem, 2.8vw, 2.5rem)` | `.title-copy`; gold left border and gradient | hidden | `.action-btn` is `70px` | `:disabled` | `url('./assets/temple-background.jpg')` | Closely matches Inn structure with sacred atmosphere |
| Storage | Specialized Workspace | `.title-copy h1`; `clamp(1.8rem, 2.8vw, 2.5rem)` | `.title-copy`; gold left border and gradient | visible | content-sized | `[aria-disabled="true"]` | `var(--facility-background-image)` | Operation-first layout; no large NPC is required |
| Relic Preview | Specialized Showcase | `.title-copy h1`; `clamp(1.8rem, 3vw, 2.8rem)` | `.title-copy`; purple-accent gradient | forced hidden | `min-height: 60px` | `:disabled` | `var(--facility-background-image)` | Object-first showcase; separate comparison target |

### 6.1 Verified Convergence

Observed CSS supports these conclusions:

- Shop, Guild, and Magic Shop share the same title size, weight, spacing, and
  broad title-block structure.
- Inn, Temple, and Storage share a smaller title range suited to their denser or
  dialogue-oriented layouts.
- Synthesis and Workshop are current large-title exceptions.
- Primary-action visual behavior has converged more than selector naming or
  sizing has.
- Disabled action semantics are visually similar, but implementation uses both
  `[aria-disabled="true"]` and `:disabled`.
- Resource-summary visibility is intentionally facility-specific.

### 6.2 Evidence Still Needed

CSS alone cannot decide:

- whether Synthesis and Workshop large titles are visually successful;
- whether a current difference is owner-accepted or merely historical drift;
- whether background safe areas remain readable at required viewport sizes;
- whether panel opacity and blur are balanced against each facility image;
- whether a shared rule causes regressions in Chinese text wrapping or action
  placement.

These questions require screenshots or browser review.

## 7. Visual Integration Candidates

Candidates are ordered by current evidence and risk. They are not implementation
approval.

### Candidate A: Title Typography Classification

First review target.

Current evidence suggests three title ranges:

```text
Shop-family list/detail:
  clamp(2rem, 3.2vw, 3rem)

Dialogue / workspace:
  approximately clamp(1.8rem, 2.8vw, 2.5rem)

Large-title exceptions:
  Synthesis and Workshop
```

Recommended review:

- preserve the matching Shop / Guild / Magic Shop range;
- visually review Synthesis and Workshop before changing them;
- treat the result as a family range, not one universal title token.

### Candidate B: Primary And Disabled Action Semantics

Second review target.

Potential shared documentation rule:

- primary action uses an accent gradient and stronger hover emphasis;
- secondary action remains visually quieter;
- disabled action has muted text, reduced opacity, no glow, and blocked cursor;
- disabled reason remains visible in nearby text or feedback;
- both native `:disabled` and `[aria-disabled="true"]` remain valid according to
  current render behavior.

Do not unify selectors until the relevant HTML and render behavior are reviewed.

### Candidate C: Panel Material Description

Third review target.

Describe the common material at a family level:

```text
dark translucent surface
+ thin facility accent border
+ inset or drop shadow
+ optional blur
+ family-specific radius, opacity, and geometry
```

Do not force identical panel dimensions, radius, blur, or opacity.

### Candidate D: Background Safe-Area Checklist

Suitable as an immediate documentation rule because it protects future image
work without changing implementation.

## 8. Allowed Facility Differences

Keep these differences unless visual review identifies unwanted drift:

- family layout and column ratios;
- resource-summary visibility;
- accent palette;
- panel geometry and density;
- NPC presence, scale, and position;
- background brightness and detail density;
- dialogue and feedback scale;
- operation-first Storage layout;
- object-first Relic Preview layout.

Shared grammar should preserve facility identity rather than flatten it.

## 9. Background And NPC Image Guidance

Recommended baseline:

```text
16:9 facility hero image
no readable UI text
no prices, values, labels, dialogue, or requirements
no fake functional panels, buttons, list rows, badges, or notifications
no gameplay state baked into the image
```

Composition rules:

- preserve overlay-safe reading and interaction regions;
- avoid bright, high-detail clutter behind text-heavy areas;
- allow CSS masks, gradients, and dimming to protect readability;
- keep NPCs clear of primary lists, details, and actions;
- use ranges and safe zones rather than fixed NPC coordinates;
- allow Storage to remain atmosphere-first without a large NPC;
- keep Relic Preview object-first.

An accepted reference set should contain:

```text
accepted image or screenshot
+ short reason it passed
+ safe-area and NPC-scale notes
+ known mistakes to avoid
```

Do not rely on prompt wording alone as a visual schema.

## 10. Visual Review Checklist

### Overlay Responsibility

- [ ] Functional text and controls are rendered by HTML/CSS/JS.
- [ ] No gameplay values or state are baked into the background.
- [ ] Removing or replacing the hero image does not remove required information.

### Readability And Layout

- [ ] Main list, detail, requirements, dialogue, and feedback remain readable.
- [ ] Long Chinese text can wrap or scroll without breaking the screen.
- [ ] Primary actions and disabled reasons remain visible.
- [ ] Background detail does not compete with interaction regions.
- [ ] Responsive layout does not hide or overlap required actions.

### Interaction States

- [ ] Primary, secondary, hover/focus, selected, and disabled states are clear.
- [ ] Disabled state is not communicated by color alone.
- [ ] Focus-visible treatment remains usable.
- [ ] Fixture controls and UIAction logs remain debug-only.

### Facility Identity

- [ ] Facility identity remains clear through scene, palette, props, NPC, object,
  or layout.
- [ ] Shared visual grammar does not erase family-specific needs.

## 11. Usage Workflow

This specification is a comparison reference, not automatic approval.

Preferred sequence:

```text
read current screen and relevant CSS
-> compare against this document
-> separate observed behavior from proposed interpretation
-> choose one smallest candidate
-> obtain exact-scope approval
-> implement only that slice
-> review screenshots or browser result
-> update documentation only if the result is accepted
```

Follow `AGENTS.md` and the current agent's GUI static prototype skill for planning
gates, allowed surfaces, implementation, and verification. This document does
not duplicate agent-specific prompts or command policies.

When a future visual adjustment is approved, prefer direct edits to the formal
`07_gui_prototype/<screen>/` path on a short-lived feature branch for uncertain
or multi-file work. Do not recreate a parallel experiment copy unless an
explicit isolation need cannot be served by a branch.

## 12. Next Recommended Slice

Paused. No visual review or CSS unification slice is currently approved.

When the owner explicitly resumes this work, begin with:

```text
Review current screenshots or browser renders for title typography only:
Shop, Guild, Magic Shop, Synthesis, Workshop, Inn, Temple, Storage, and Relic Preview.
```

Classify each title as:

```text
accepted family baseline
accepted intentional exception
probable drift
needs more visual evidence
```

After that review, propose at most one CSS-only title adjustment. Do not combine
it with panel, button, background, runtime, bridge, or asset changes.
