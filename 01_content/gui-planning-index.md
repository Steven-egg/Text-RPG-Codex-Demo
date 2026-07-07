# GUI Planning Index

Purpose: Task Zone index for GUI planning, document lifecycle, and archive
candidate routing. This file is opened only for GUI planning, drift audit, task
routing, or archive/lifecycle work. It is not part of ordinary Hot Zone startup.

## 0. Default Reading

New sessions first follow `01_content/agent-startup-reading-list.md`.

For GUI Task Zone work, start with the smallest matching route:

| Task | Read |
|---|---|
| Static prototype screen work | Current agent GUI static prototype skill, then only the relevant `07_gui_prototype/<screen>/` files. |
| Static prototype handoff / screen verification | Targeted sections of `01_content/gui-html-static-prototype-progress-v1.md`. |
| GUI planning / drift audit / document routing | This file. |
| Facility-family responsibility planning | `01_content/blueprints/gui-facility-shell-baseline-v0.1.md`. |
| Facility visual comparison | `01_content/blueprints/facilities-visual-integration-spec-v0.1.md`; currently paused and not implementation approval. |
| Screen flow / UIAction / ScreenModel mapping | `01_content/blueprints/gui-screen-map.md`, `01_content/blueprints/ui-flow-blueprint.md`. |
| Runtime-connected GUI planning | `01_content/gui-runtime-bridge-plan-v1.md`, then stop at a read-only planning gate. |
| Runtime bridge contract audit | `01_content/blueprints/gui-bridge-vertical-slice-contract-audit-v1.md`. |
| Runtime bridge preflight | `01_content/blueprints/gui-runtime-bridge-preflight-v1.md`. |
| Historical decision trace | `01_content/archive/codex-session-snapshot.md` or named historical docs only when truly needed. |

Do not full-load `01_content/gui-html-static-prototype-progress-v1.md` or broad
historical GUI docs during ordinary startup.

## 1. Current GUI State

Default GUI mode remains HTML static prototype:

- Static prototype root: `07_gui_prototype/`
- Static prototypes currently exist for 14 screens: Start Screen, Town Hub,
  Guild Screen, Synthesis Screen, World Map, Dungeon Exploration, Combat Screen,
  Shop Screen, Workshop Screen, Storage Screen, Magic Shop Screen, Inn Screen,
  Temple Screen, and Relic Preview Screen.
- Static prototypes validate render layer, layout, fixture shape, navigation,
  interaction, and UIAction logging only.
- Static fixtures are not gameplay SSOT and must not copy gameplay rules into
  JavaScript.
- Shop + Magic Shop GUI Layout Normalization V0.5 first CSS-only checkpoint is
  complete through `c7729df`.
- Current facility planning is family-level Mockup-to-HTML responsibility
  mapping. AI facility hero images provide scene / NPC / atmosphere;
  HTML/CSS/JS provides UI and interaction; runtime remains gameplay authority.
- Facility skinning exploration is complete. The owner retired and removed
  `08_experiments/`; accepted visual results now live in the formal
  `07_gui_prototype/` screens.
- Future minor visual changes should target formal prototype files directly
  after exact-scope approval. Use a short-lived feature branch for uncertain or
  multi-file changes rather than recreating a parallel experiment copy.
- Facilities visual integration review is paused at
  `01_content/blueprints/facilities-visual-integration-spec-v0.1.md`.

Local runtime-connected live bridge exists only for explicit blessed slices:

- Start / load / restart.
- Town Hub / Inn / World Map local live shell.
- Approved Dungeon / Combat loop and Combat Skill Button MVP.
- Guild clear report registration MVP.
- Shop Buy Consumable MVP.
- Magic Shop Learn Magic Book MVP.
- Workshop Buy Weapon MVP and Workshop Weapon Equip MVP.

Current newest live bridge state:

- Workshop can buy existing weapon-shop weapons without auto-equipping.
- Workshop can equip inventory-held weapon-slot items into `equipment.weapon`.
- Python runtime remains gameplay authority through server-side validation and
  existing runtime helpers.
- This does not open full inventory / equipment management or broader facility
  framework work.

Detailed live bridge notes live in `01_content/gui-runtime-bridge-plan-v1.md`.
Screen-level static verification lives in
`01_content/gui-html-static-prototype-progress-v1.md`.

## 2. Document Lifecycle

Lifecycle labels:

- `entry`: short routing / startup docs.
- `core`: current Task Zone docs that remain active.
- `conditional`: read only for the named task.
- `paused`: owner-paused route; read or resume only when explicitly reopened.
- `superseded`: replaced by a newer active route; read only for historical
  context or comparison.
- `historical`: old planning or decision trace.
- `archive candidate`: logically stale candidate / prompt / draft docs; do not
  move physically without explicit approval.

### Entry / Hot Zone Pointers

| File | Lifecycle | Role |
|---|---|---|
| `AGENTS.md` | entry | Shared Codex / Antigravity governance route. |
| `01_content/agent-startup-reading-list.md` | entry | Loading-zone and startup read order. |
| `README.md` | entry | Compact project entry and current stable capsule. |
| `01_content/codex-handoff-short.md` | entry | Short new-session handoff and next-step boundary. |

### Active GUI Task Zone

| File | Lifecycle | Role |
|---|---|---|
| `01_content/gui-planning-index.md` | core | This GUI routing and lifecycle index. |
| `01_content/gui-facility-image-generation-standard-v0.1.md` | conditional | Facility background image generation and review standard; not image-generation or asset-pipeline approval by itself. |
| `01_content/blueprints/gui-facility-shell-baseline-v0.1.md` | core | Facility-family Mockup-to-HTML four-layer responsibility and configuration baseline. |
| `01_content/blueprints/gui-family-classification-visual-token-audit-v0.1.md` | core | Formal 14-screen family classification, Global Visual Tokens V0.1 planning baseline, drift register, and normalization gate. |
| `01_content/blueprints/facilities-visual-integration-spec-v0.1.md` | conditional | Paused Draft facility CSS and visual comparison reference; not implementation approval. |
| `01_content/gui-html-static-prototype-progress-v1.md` | core | Static prototype handoff, built screens, and targeted verification notes. |
| `01_content/gui-runtime-bridge-plan-v1.md` | core | Runtime bridge plan, approved surfaces, and landed live-slice status notes. |
| `01_content/blueprints/gui-screen-map.md` | core | Screen, flow, UIAction, and ScreenModel map. |
| `01_content/blueprints/ui-flow-blueprint.md` | core | CLI thin-layer to GUI flow mapping. |
| `01_content/blueprints/gui-runtime-bridge-preflight-v1.md` | conditional | Runtime bridge preflight; read only for bridge planning. |
| `01_content/blueprints/gui-bridge-vertical-slice-contract-audit-v1.md` | conditional | Bridge contract audit. |
| `01_content/blueprints/gui-dynamic-traversal-continuity-v1-spec.md` | conditional | Traversal continuity semantics; not implementation approval by itself. |

### Screen / Facility Planning Docs

| File | Lifecycle | Role |
|---|---|---|
| `01_content/archive/gui-facility-screen-template.md` | conditional | Facility screen model template. |
| `01_content/archive/gui-guild-screen-visual-baseline.md` | conditional | Guild visual baseline. |
| `01_content/archive/gui-guild-screen-model-draft.md` | conditional | Guild ScreenModel draft. |
| `01_content/archive/gui-guild-screen-review-checklist.md` | conditional | Guild review checklist. |
| `01_content/archive/gui-town-hub-screen-model-draft.md` | conditional | Town Hub ScreenModel draft. |
| `01_content/archive/gui-town-hub-review-checklist.md` | conditional | Town Hub review checklist. |
| `01_content/archive/gui-town-hub-facility-node-mapping-v1.md` | conditional | Town Hub facility node mapping. |
| `01_content/archive/gui-town-hub-programmatic-layout-plan-v1.md` | conditional | Town Hub programmatic layout plan. |
| `01_content/archive/gui-shop-skinning-lab-readiness-checklist-v0.1.md` | historical | Retired Shop lab readiness record; do not use as a current route. |
| `01_content/archive/gui-shop-mockup-brief-v0.1.md` | historical | Retired Shop mockup brief; do not generate or implement from it. |

### Historical / Optional Background

| File | Lifecycle | Role |
|---|---|---|
| `01_content/archive/gui-implementation-platform-tradeoff.md` | historical | Platform tradeoff background; not a startup doc. |
| `01_content/archive/codex-session-snapshot.md` | historical | Compact historical snapshot only when decision trace is needed. |
| `01_content/archive/gui-ui-direction-brief.md` | archive candidate | Old GUI direction background; not a current entry doc. |

## 3. Archive Candidate Index

These docs are logical archive candidates. Keep them out of Hot Zone startup.
Do not move or delete them without explicit owner approval for that exact archive
operation.

- `01_content/archive/gui-asset-registry-draft.md`
- `01_content/archive/gui-asset-request-schema.md`
- `01_content/archive/gui-facility-screen-template.md`
- `01_content/archive/gui-facility-synthesis-mockup-request.md`
- `01_content/archive/gui-facility-synthesis-prompt-draft.md`
- `01_content/archive/gui-facility-synthesis-v2-prompt-draft.md`
- `01_content/archive/gui-guild-screen-model-draft.md`
- `01_content/archive/gui-guild-screen-review-checklist.md`
- `01_content/archive/gui-guild-screen-visual-baseline.md`
- `01_content/archive/gui-html-town-hub-fixture-spec.md`
- `01_content/archive/gui-html-town-hub-prototype-plan.md`
- `01_content/archive/gui-town-hub-facility-node-mapping-v1.md`
- `01_content/archive/gui-town-hub-mockup-review-v1.md`
- `01_content/archive/gui-town-hub-programmatic-layout-plan-v1.md`
- `01_content/archive/gui-town-hub-review-checklist.md`
- `01_content/archive/gui-town-hub-screen-model-draft.md`
- `01_content/archive/gui-town-hub-ui2-wireframe-draft.md`
- `01_content/archive/gui-town-hub-ui2-wireframe-review-v1.md`
- `01_content/archive/gui-town-hub-visual-mockup-candidate-review-v1.md`
- `01_content/archive/gui-town-hub-visual-mockup-prompt-draft.md`
- `01_content/archive/gui-town-hub-visual-mockup-prompt-review-v1.md`
- `01_content/archive/gui-town-hub-wireframe-plan.md`
- `01_content/archive/gui-ui-direction-brief.md`

Some archive candidates are still conditionally useful for a named screen review
or drift audit. Their archive-candidate status means "do not read by default",
not "delete".

## 4. Task Routing Notes

Static prototype work:

- Stay inside `07_gui_prototype/<screen>/` and static fixtures unless a different
  exact scope is approved.
- Preserve fixture fallback and UIAction logging.
- Do not connect Python runtime.

Runtime-connected prototype work:

- First read `01_content/gui-runtime-bridge-plan-v1.md`.
- Stop at a read-only planning gate before implementation.
- Do not manually read or edit `save.json`.
- Do not modify runtime/data/schema/combat formula unless separately approved.

Docs cleanup:

- Keep `README.md` and `01_content/codex-handoff-short.md` compact.
- Move detailed verification and historical MVP notes into Task Zone docs.
- Do not create new docs unless existing Task Zone docs cannot carry the
  information.

## 5. Governance

- New GUI markdown docs must be added to this index with a lifecycle label.
- Do not add unclassified `.md` files to `01_content/`.
- Reference images and generated mockups are design references, not runtime
  assets.
- `05_assets/gui_references/` is reference storage, not a formal asset pipeline.
- `08_experiments/` was retired and removed by the owner after facility
  skinning exploration completed. Do not recreate it as a default work route.
- GUI planning must not imply that HTML, pygame, Unity, or another platform is
  the final app unless that choice is separately approved.
- GUI planning must not bundle runtime, data, schema, save, or combat formula
  changes into the same task.

## 6. Recommended Next Step

No GUI visual implementation or additional planning candidate is currently
approved. Facilities visual integration review remains paused at
`01_content/blueprints/facilities-visual-integration-spec-v0.1.md`.
