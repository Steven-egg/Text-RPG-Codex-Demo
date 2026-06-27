# GUI Facility Shell Baseline V0.1

Purpose: define the facility-family composition and responsibility baseline for
current formal prototypes and future visual review.

This baseline separates AI-generated facility hero imagery, HTML/CSS/JS
presentation, runtime authority, and lab-only prototype markers. It describes
responsibility boundaries and current facility layouts. It is not a Shop
skinning plan, a single-screen visual mockup brief, a Design System, a GUI
framework, or an asset pipeline.

## 0. Corrected Mockup-to-HTML Model

The current reference model is:

```text
AI facility hero image
-> HTML/CSS/JS overlay
-> runtime-backed state and action semantics
```

Lab-only controls and placeholders remain outside the intended final
presentation:

```text
fixture switcher / UIAction Log / placeholder portrait / construction marker
```

Interpretation:

- Current formal facility backgrounds demonstrate the **AI facility hero image
  layer**. A single image
  may contain the facility interior, NPC, lighting, atmosphere, props, and
  composition. It does not contain UI panels, text, values, controls, lists, or
  gameplay state.
- Current formal facility prototypes demonstrate the **HTML/CSS/JS overlay
  layer**. Cut-corner
  panels, translucent materials, masks, blur, gradients, typography, form or
  list controls, hover states, buttons, toast messages, and interactive feedback
  can all be rendered above a background image.
- AI reference imagery must not be treated as a fantasy UI atlas that HTML must
  reproduce one-to-one.
- A facility hero image may support the full screen, not only a current NPC
  placeholder rectangle. Its composition must still preserve overlay-safe
  reading and interaction zones.

## 0.1 Retired Experiment Route And Current Adjustment Route

The owner retired and removed `08_experiments/` after facility skinning
exploration completed. The experiment route established useful responsibility
boundaries, but parallel copies and later source-to-target transfer are not the
default path for future minor visual work.

When visual adjustment resumes:

1. Start with read-only review and exact-scope owner approval.
2. Modify the formal `07_gui_prototype/<screen>/` path directly.
3. Use a short-lived feature branch for uncertain or multi-file work.
4. Keep static prototype and runtime authority boundaries unchanged.
5. Verify only the touched surface with fitting syntax, bridge, and browser
   checks.

Create a separate experiment copy only when an explicit isolation need cannot be
served by a feature branch.

## 1. Scope And Boundaries

Observed facility prototype screens:

- `guild_screen`
- `inn_screen`
- `shop_screen`
- `workshop_screen`
- `magic_shop_screen`
- `synthesis_screen`
- `storage_screen`
- `temple_screen`
- `relic_preview_screen`

No Academy prototype currently exists under `07_gui_prototype/`. Academy remains
`not observed`; this baseline does not invent its layout or assign it to a shell
family.

This baseline may be used to:

- classify existing facility shell families;
- identify the intended responsibility of each visual or functional region;
- plan facility hero-image composition without embedding UI;
- preserve HTML/CSS overlay and runtime-authority boundaries;
- identify lab-only placeholders that should not drive final visual decisions.

This baseline does not authorize:

- image generation or a single-screen visual candidate;
- HTML, CSS, JavaScript, ScreenModel, UIAction, runtime, data, schema, save, or
  combat changes;
- importing reference images into runtime;
- a formal component library, Design System, GUI framework, or asset pipeline;
- pixel-perfect measurements or forced unification of every facility.

## 2. Four-Layer Responsibility Model

### 2.1 AI Facility Hero Image Support Layer

Responsible for:

- facility interior or exterior scene;
- NPC or facility-object presence;
- lighting, atmosphere, depth, and environmental storytelling;
- non-functional props and composition;
- visual focus and negative space that support overlays.

Not responsible for:

- UI panels, lists, tabs, detail cards, forms, buttons, or toast messages;
- readable title, dialogue, labels, prices, values, requirements, or feedback;
- selected, disabled, completed, affordable, learned, or other gameplay states;
- runtime data or action semantics.

### 2.2 HTML/CSS/JS Overlay Layer

Responsible for:

- screen identity, title, subtitle, and dynamic labels;
- panels, cut-corner frames, translucent materials, masks, blur, gradients, and
  decorative CSS treatment;
- lists, tabs, details, requirements, rewards, status badges, and resource
  summaries;
- NPC name, role, dialogue, hints, feedback, and result messages;
- navigation, buttons, hover, focus, selected, disabled, modal, and toast states;
- responsive layout and accessibility behavior;
- dispatching UIAction payloads and rendering returned ScreenModels.

Not responsible for:

- deciding gameplay eligibility, cost, reward, mutation, or persistence;
- copying gameplay rules into presentation JavaScript;
- treating fixture values as gameplay authority.

### 2.3 Runtime Authority Layer

Runtime authority is not a visible screen region. It is the source of truth that
supplies or validates overlay content and actions.

Responsible for:

- player resources and persistent state;
- available items, recipes, books, tasks, services, rewards, and requirements;
- eligibility, disabled reasons, costs, quantities, and results;
- action validation and state mutation;
- ScreenModel values and UIAction outcomes in approved live slices.

In static prototype mode, fixtures imitate runtime-shaped display data only.
They do not become runtime authority.

### 2.4 Lab-Only Placeholder / Marker Layer

Responsible for prototype construction, verification, and layout diagnosis:

- fixture switchers and fixture state labels;
- UIAction Log and debug controls;
- generic `設施畫面` labels;
- loading, fixture-failure, static-prototype, and debug wording;
- NPC initials, emoji silhouettes, empty portrait plates, and temporary visual
  stand-ins;
- blank reserve areas and construction copy used to test placement.

Lab-only elements must not be mistaken for required final UI. They may still
remain available during prototype verification.

## 3. Facility Shell Families

### 3.1 List-Detail-Service Family

Current members:

- Shop
- Magic Shop
- Synthesis
- Workshop, as an independent hybrid variant
- Guild, as a task-oriented variant

Shared overlay grammar:

```text
screen identity / optional resource summary
-> selectable list or task board
-> selected detail and requirement / reward / condition region
-> action and feedback region
```

The AI hero image supplies facility scene and NPC presence behind or around this
overlay grammar. It does not need to reproduce the current three-column panel
geometry inside the image.

### 3.2 Hero-Dialogue-Service Family

Current members:

- Inn
- Temple

Shared overlay grammar:

```text
screen identity / optional resources
-> large scene and NPC hero-image support
-> dialogue / feedback overlay
-> small service or navigation action menu
-> optional screen-specific modal
```

This family most directly demonstrates the `bg-npc.png` model: a full facility
scene and NPC image can sit behind independently rendered dialogue and service
overlays.

### 3.3 Specialized Workspace / Showcase Family

Current members:

- Storage
- Relic Preview

Storage prioritizes a dual-list transfer workspace. Relic Preview prioritizes a
central facility-object showcase. Both may use AI facility atmosphere, but their
hero images must not weaken operation-first or focus-first overlays.

### 3.4 Unclassified / Not Observed

- Academy: no current prototype; do not infer a classroom, NPC, list, service,
  skill, or training layout from the name alone.

## 4. Facility Four-Layer Configuration Specification

| Screen | AI facility hero image support area | HTML/CSS/JS overlay area | Runtime authority | Lab-only placeholder / marker |
|---|---|---|---|---|
| Guild | Full guild-hall atmosphere, quest-board setting, receptionist or guild NPC, lighting and props; composition should leave task-reading zones usable | Header, resource strip, task/material modes, filters, story hint, task or material list, detail, rewards, conditions, confirmation, footer feedback, back and primary action | Unlocked tasks, completion/readiness, rewards, conditions, story-hint visibility, sellable materials, quantities, prices, disabled reasons, submit/sell results | Fixture switcher, UIAction Log, generic `設施畫面`, current empty NPC portrait, fixture-only and static-prototype copy |
| Inn | Full inn interior, fireplace, innkeeper, lighting, atmosphere, non-functional room props | HUD title, resource summary, dialogue box, NPC name, service prompt, confirmation choices, feedback, action menu, navigation | HP/MP/Gold, rest cost, service availability, disabled reason, rest result, navigation result | Fixture switcher, UIAction Log, `LY` avatar token, emoji silhouette, temporary hidden fields, construction feedback |
| Shop | Full supply-shop interior and merchant presence; scene may support the whole screen and is not limited to the current right column | Header, title/subtitle, category tabs, item list, item detail, requirements, NPC name/role, feedback, back and purchase action, all masks/blur/panel styling | Available inventory, prices, owned counts, item detail, requirements, affordability, disabled reasons, buy validation and result | Fixture switcher, UIAction Log, generic `設施畫面`, current portrait placeholder, static-fixture result wording; resource strip remains intentionally hidden |
| Workshop | Forge/armory scene, equipment workspace, relevant craftsperson presence, lighting and material atmosphere; visual variant may need to respond to weapon/armor mode later | Header/player chips, tabs, item list, equipment detail, requirements, NPC name/role/dialogue, feedback, back and buy/equip/upgrade action | Player resources/equipment, available equipment and upgrades, stats, job compatibility, materials, costs, eligibility, validation and result | Fixture selector, debug/UIAction panel, current silhouettes, default construction dialogue, `ELM FORGE` and other hard-coded identity text pending owner classification |
| Magic Shop | Full arcane shop/library scene, Eve or relevant NPC, magical lighting and props without functional spellbook labels | Header, visible resource strip, category tabs, spellbook list, spell detail, price, requirements, NPC name/role/guidance, feedback, back and learn action | Available books, prices, learned state, discounts, level/job/material requirements, disabled reasons, learn validation and result | Fixture switcher, UIAction Log, generic `設施畫面`, `EV` portrait placeholder, fixture-state wording |
| Synthesis | Full synthesis workshop, Mira or relevant NPC, alchemy/crafting atmosphere, materials and tools as non-functional scene props | Header, category tabs, recipe list, output detail, requirement/material-gap rows, NPC name/role, feedback, back and craft action, panel effects | Available recipes, output, materials, Gold, eligibility, disabled reasons, crafting validation and result | Fixture switcher, UIAction Log, generic `設施畫面`, current portrait placeholder, static-prototype wording; resource strip remains intentionally hidden |
| Temple | Full temple/church interior and priestess/NPC, stained glass, altar, light, atmosphere; strongest current reference for the full-screen hero-image model | HUD title, dialogue, NPC name, feedback, inquiry/service menu, promotions modal, modal controls, navigation, masks/blur/effects | Resources when shown, prayer/service cost and eligibility, inquiries, promotion requirements, disabled reasons, action validation and results | Fixture switcher, UIAction Log, current initials/emoji silhouette, hidden temporary containers, preview-only or construction wording; current resource strip is hidden |
| Storage | Subtle warehouse or guild-depot atmosphere; no required large NPC focal image; keep two-way scanning clear | Header, visible resource/status strip, backpack list, storage list, capacity, selected-item detail, quantity controls, requirements, feedback, back and transfer/unlock action | Unlock state/cost, capacity, inventory/storage contents, transferable quantity, requirements, validation and transfer result | Fixture switcher, UIAction Log, generic `設施畫面`, placeholder empty states and construction guidance |
| Relic Preview | Relic altar, chamber atmosphere, central relic/object focus, lighting and non-functional inscriptions | Title/subtitle, resource strip, element slot list, focus detail, translation/effect panel, feedback, attune action, navigation | Registered relics, collection/unlock state, requirements, preview detail, action availability/result | Fixture switcher, UIAction Log, current orb placeholder, preview-only disclaimer, duplicate static altar label pending classification |
| Academy | Not observed; no hero-image composition may be assigned yet | Not observed; no overlay configuration may be assigned yet | Not observed; no training/skill/service authority may be inferred | The word `Academy` itself is only a requested candidate until a prototype or approved scope exists |

## 5. Common Region Responsibility Map

| Region | Primary layer | Supporting layer | Rule |
|---|---|---|---|
| Facility environment | AI facility hero image | CSS masks, blur, gradients, dimming | May include scene and NPC; must not include functional UI |
| NPC visual presence | AI facility hero image | HTML NPC name, role, dialogue, focus treatment | NPC art and NPC text remain separate responsibilities |
| Screen title / identity | HTML/CSS overlay | Runtime/fixture-supplied text | Never bake readable title into hero image |
| Resource summary | HTML/CSS overlay | Runtime authority | Visibility is facility-specific; do not force one rule across all facilities |
| Lists / task boards / tabs | HTML/CSS/JS overlay | Runtime authority | Hero image must leave these regions readable |
| Detail / requirements / rewards | HTML/CSS/JS overlay | Runtime authority | Values, state, and disabled reasons remain dynamic |
| Dialogue / feedback / toast | HTML/CSS/JS overlay | Runtime result/message | May visually float over the hero image; never image-baked |
| Buttons / navigation / modal | HTML/CSS/JS overlay | UIAction and runtime validation | Hover, focus, disabled, and result states remain interactive HTML |
| Fixture switcher / UIAction Log | Lab-only marker | Static prototype verification | Do not use as final-UI visual requirements |

## 6. Facility Hero Image Composition Baseline

An AI facility hero image may contain:

- a complete facility scene;
- one or more visually relevant NPCs when approved by that facility's scope;
- lighting, atmosphere, architecture, furniture, tools, and non-functional props;
- quiet or darkened regions designed to support overlays;
- depth and visual focus that guide attention without creating fake controls.

An AI facility hero image must not contain:

- readable UI text, values, labels, dialogue, prices, requirements, or feedback;
- panels that the HTML layer must reproduce one-to-one;
- functional-looking buttons, list rows, status badges, tabs, or notifications;
- gameplay eligibility, selected state, completion state, or resource state;
- visual implications of unapproved gameplay or services.

The hero image and overlay may overlap spatially. Responsibility is determined by
function, not by whether an element appears on the left, center, right, top, or
bottom.

## 7. HTML/CSS Overlay Baseline

The overlay layer may freely use presentation techniques such as:

- translucent panels and material effects;
- cut corners, borders, gradients, shadows, and decorative CSS;
- localized dimming, blur, and masks to protect text-safe regions;
- typography hierarchy and dynamic labels;
- hover, focus, active, selected, disabled, modal, and toast states;
- responsive repositioning and stacking.

The overlay layer must remain independently usable:

- removing the hero image must not remove required information or actions;
- changing the hero image must not change gameplay semantics;
- interactive states must not depend on image-baked cues;
- overlay text must remain readable across required facility states.

## 8. Runtime Authority Boundary

For every facility:

```text
runtime or runtime-shaped fixture
-> ScreenModel values
-> HTML/CSS/JS overlay rendering
-> UIAction payload
-> runtime validation and result
```

The AI hero image does not participate in this flow.

Static fixtures may demonstrate:

- default, constrained, learned, completed, locked, or other display states;
- layout capacity and text wrapping;
- selected and disabled presentation;
- feedback and action rendering.

Static fixtures must not:

- become gameplay SSOT;
- define new items, recipes, tasks, services, prices, or requirements;
- authorize JavaScript gameplay logic.

## 9. Known Exceptions And Open Decisions

- Shop and Synthesis keep their resource strips hidden; Magic Shop keeps its
  resource strip visible. This remains an intentional current difference.
- Temple's current resource strip is hidden.
- Workshop uses a fixed-size independent shell and hard-coded identity text;
  their final classification remains unresolved.
- Guild, Shop, Magic Shop, Synthesis, and Workshop currently reserve explicit NPC
  regions, but future hero imagery may support the full screen rather than being
  cropped only into those regions.
- Storage remains operation-first and does not require a large NPC focal image.
- Relic Preview remains facility-object-first rather than NPC-first.
- Academy cannot be classified until a prototype or exact approved scope exists.
- The retired Shop readiness checklist and Shop mockup brief must not be treated
  as active routes.

## 10. Recommended Next Gate

No visual implementation or additional planning candidate is currently
approved. The paused comparison reference is
`01_content/blueprints/facilities-visual-integration-spec-v0.1.md`.
