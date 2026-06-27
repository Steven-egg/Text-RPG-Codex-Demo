# GUI Family Classification & Visual Token Audit V0.1

Status: Active baseline; first Dialogue / Service normalization sprint
implemented

Scope: GUI static prototype visual classification, token planning, and drift
audit only

## 1. Purpose

This audit defines a reusable visual reference for the current 14 GUI static
prototype screens and future facility additions.

It separates three levels of consistency:

1. Global Visual Tokens
2. Screen Family Shells
3. Screen Exceptions

The goal is to avoid deciding typography roles, title scales, panel material,
shell gutters, and action semantics from scratch for every new screen while
preserving layouts that serve genuinely different tasks.

This document is a planning baseline. It is not:

- a shared CSS implementation;
- a component library or GUI framework;
- approval to force all screens into one geometry;
- approval to modify runtime, data, schema, save, combat, fixtures, or
  JavaScript;
- authority to treat static fixture values as gameplay SSOT.

## 2. Evidence And Boundaries

Evidence labels used in this audit:

- **Observed CSS**: directly verified in current `07_gui_prototype/*/styles.css`.
- **Observed HTML reference**: directly verified in each screen's stylesheet or
  font-link section.
- **Existing planning baseline**: already stated in current GUI Task Zone docs.
- **Proposed V0.1 token**: reusable documentation target, not yet a shared CSS
  API.
- **Needs visual review**: CSS evidence is insufficient to classify the
  difference as accepted or drift.

Files reviewed:

- `01_content/gui-planning-index.md`
- `01_content/blueprints/gui-facility-shell-baseline-v0.1.md`
- `01_content/blueprints/facilities-visual-integration-spec-v0.1.md`
- `01_content/archive/gui-ui-direction-brief.md`
- all 14 `07_gui_prototype/*/styles.css` files
- stylesheet and font-link sections from all 14 screen `index.html` files

Files intentionally not loaded:

- full `01_content/gui-html-static-prototype-progress-v1.md`
- Cold Zone documents
- runtime bridge plan
- JavaScript, fixtures, runtime, data, schema, combat, or `save.json`

## 3. Three-Level Consistency Model

### 3.1 Global Visual Tokens

Global tokens describe roles and semantics that remain useful across screen
families:

- font roles and fallback stacks;
- typography roles and size ranges;
- spacing rhythm;
- shell gutter vocabulary;
- panel material vocabulary;
- primary, secondary, disabled, selected, focus, and debug semantics.

Global tokens do not require identical selector names or a shared stylesheet.

### 3.2 Screen Family Shells

Family shells describe geometry and responsive behavior only for screens with
the same primary interaction task.

A family shell may define:

- desktop shell width and gutter;
- panel or slot arrangement;
- action-region placement;
- family title range;
- breakpoint and stacking behavior.

A family shell must not be used merely because two screens are both facilities.

### 3.3 Screen Exceptions

Screen exceptions preserve identity and task-specific needs:

- background composition and accent palette;
- NPC, facility-object, or environment focus;
- resource-strip visibility;
- modal or dialogue-choice placement;
- spatial node maps;
- exploration and combat presentation;
- Start Screen cover composition.

An exception should be documented before it is normalized away.

## 4. Formal Screen Family Classification

| Family | Current members | Classification reason |
| --- | --- | --- |
| Spatial Navigation | Town Hub, World Map | The primary interaction is selecting a place in a spatial composition. Both use floating HUD treatment and location selection, but each owns different node and drawer geometry. |
| Catalog / Transaction | Shop, Magic Shop, Synthesis | The primary interaction is scanning a selectable catalog, reading selected detail and requirements, then performing one primary transaction-like action. |
| Catalog Variants | Workshop, Guild | Both retain catalog/task scanning and detail/action grammar, but their task models require independent variants. Workshop is multi-mode equipment work; Guild is a task and material board. |
| Dialogue / Service | Inn, Temple | The scene and NPC remain prominent while a compact dialogue/service footer carries the main actions. |
| Operation Workspace | Storage | The primary task is two-way item transfer with quantity, capacity, and state visibility. It is operation-first rather than showcase-first. |
| Object Showcase | Relic Preview | The primary task is inspecting a central facility object with supporting slots, translation, and one main action. |
| Expedition | Dungeon Exploration, Combat | Both belong to the expedition loop and share resource/action semantics, but they require separate Exploration and Combat shell variants. |
| Unique Entry | Start Screen | The screen is a cover-led entry composition with a unique title and login/action stack. |

### 4.1 Classification Corrections

- Storage and Relic Preview are separate formal families. Their current
  documentation grouping remains useful as a responsibility category, but it
  must not imply shared panel geometry.
- Town Hub and World Map are Spatial Navigation screens. They must not be placed
  into a facility three-column shell.
- Dungeon Exploration and Combat belong to one workflow family but must not
  share panel geometry.
- Workshop and Guild remain catalog variants rather than reference members of
  the base Catalog / Transaction shell.

## 5. Current CSS Comparison Matrix

Values in this section describe current CSS. They are not automatically
recommended standards.

### 5.1 Typography, Shell, And Geometry

| Screen | Body font | Main title | Desktop shell and gutter | Main panel columns or slots |
| --- | --- | --- | --- | --- |
| Start Screen | UI sans: `Inter`, `Noto Sans TC`, system sans fallbacks | Hero title `clamp(3rem, 5.4vw, 5.9rem)` | Shell capped at `1760px x 960px`; body gutter `12px` | Single cover stage with entry/action stack |
| Town Hub | UI sans | Initial title rule reaches `clamp(2rem, 4vw, 4.7rem)`; fullscreen override uses `clamp(1.5rem, 2vw, 1.85rem)` | Base shell `1500px`, `16px` gutter; desktop presentation becomes spatial fullscreen with fixed HUD | Facility nodes, fixed title/resources, footer `1fr / 240px` |
| World Map | UI sans | No single persistent page-title token; detail title `2rem`, menu heading `2.25rem` | Fullscreen `100% x 100%`, no outer gutter | Spatial nodes plus independent detail, menu, utility, and debug drawers |
| Shop | Facility UI: `Outfit`, `Noto Serif TC`, serif fallback | `clamp(2rem, 3.2vw, 3rem)` | `1880px`, `12px` gutter | Catalog `clamp(460px, 28vw, 540px)`, detail `460px`, NPC `minmax(300px, 1fr)` |
| Magic Shop | Facility UI | `clamp(2rem, 3.2vw, 3rem)` | `1880px`, `12px` gutter | Catalog `clamp(450px, 28vw, 520px)`, detail `520px`, NPC `minmax(400px, 1fr)` |
| Synthesis | Facility UI | `clamp(2.2rem, 4.1vw, 4.65rem)` | `1540px`, `16px` gutter | `460px / minmax(460px, 1.1fr) / minmax(450px, 1.2fr)` |
| Workshop | Facility UI; final root size `18px` after an earlier `19.5px` rule | Final override `clamp(2.5rem, 4.4vw, 4.55rem)` | Final game container `1540px`, `16px` gutter | `minmax(420px, .95fr) / minmax(460px, 1.08fr) / minmax(430px, 1.15fr)` |
| Guild | Facility UI | `clamp(2rem, 3.2vw, 3rem)` | `1500px`, `16px` gutter | `minmax(320px, .72fr) / minmax(380px, .8fr) / minmax(360px, .92fr)` |
| Inn | Facility UI | `clamp(1.8rem, 2.8vw, 2.5rem)` | `1880px`, `12px` gutter | Full-width hero stage plus footer `clamp(260px, 20vw, 320px) / 1fr / clamp(260px, 20vw, 320px)` |
| Temple | Facility UI | `clamp(1.8rem, 2.8vw, 2.5rem)` | `1880px`, `12px` gutter | Same base hero/footer geometry as Inn, plus screen modal and dialogue choices |
| Storage | Facility UI; root size `19.5px` | `clamp(1.8rem, 2.8vw, 2.5rem)` | Viewport shell capped at `1440px x 900px`; no standard outer gutter | Transfer workspace `32% / 36% / 32%` |
| Relic Preview | Facility UI | `clamp(1.8rem, 3vw, 2.8rem)` | Full viewport minus `20px` internal padding on each side | Showcase `1fr / 1.2fr / 1fr` |
| Dungeon Exploration | UI sans | Base `clamp(1.65rem, 2.4vw, 2.8rem)`; desktop fullscreen hides generic title copy | Base `1540px`, `16px` gutter; desktop override becomes fullscreen | Floating HUD and footer `clamp(140px, 15vw, 180px) / 1fr / clamp(280px, 25vw, 360px)` |
| Combat | UI sans | Compact debug/header title `clamp(1.1rem, 1.5vw, 1.8rem)` | Fullscreen combat stage, capped base width `1600px` | Stage overlays plus five-column bottom command row |

### 5.2 Actions, Breakpoints, And Resource Visibility

| Screen | Action height and placement | Breakpoints | Resource strip |
| --- | --- | --- | --- |
| Start Screen | Entry stack; actions `58px` minimum | `980px`, `560px`, desktop height `760px` | Not used |
| Town Hub | Fixed bottom-right World Map action, `44px` minimum | `1180px`, `820px`, `560px` | Visible floating HUD |
| World Map | Detail actions `54px`; menu actions `72px`, compact height `60px` | `1180px`, `760px`, viewport height `760px` | Visible inside player strip |
| Shop | Three-slot footer; primary and secondary actions `70px` | `1220px`, `720px` | Intentionally hidden |
| Magic Shop | Three-slot footer; primary and secondary actions `70px` | `1220px`, `720px` | Visible |
| Synthesis | Three-slot footer; actions `58px` minimum | `1220px`, `720px` | Intentionally hidden |
| Workshop | Three-slot footer; final action rules reach `58px` minimum after multiple overrides | `1220px`; an older `768px` block also remains | Player/resource information hidden |
| Guild | Three-slot footer; actions `58px` minimum | `1220px`, `720px` | Forced hidden |
| Inn | Fixed dialogue/service footer; actions `70px`, mobile `50px` | `900px` | Visible |
| Temple | Fixed dialogue/service footer; actions `70px`, mobile `50px` | `900px` | Hidden |
| Storage | Content-sized transfer and footer actions | `1024px` | Visible |
| Relic Preview | Primary `60px` minimum, back `50px` minimum | `900px` | Forced hidden |
| Dungeon Exploration | Bottom exploration actions `72px` | `1180px`, `820px`, `560px`; desktop fullscreen override from `821px` | Visible floating HUD |
| Combat | Bottom command actions `108px` | `1180px`, `860px`, `560px`; desktop fullscreen override from `1181px` | Visible compact HUD |

### 5.3 Font Loading Observation

- Facility screens generally load `Outfit` and `Noto Serif TC` from Google
  Fonts through HTML or CSS import.
- Town Hub, World Map, Dungeon Exploration, Combat, and Start Screen use an
  unlinked UI-sans stack beginning with `Inter` and `Noto Sans TC`, so actual
  rendering depends on locally available fonts.
- Debug/action logs commonly use `Cascadia Mono`, `Consolas`, or generic
  monospace and commonly settle around `0.78rem`.
- Storage imports `Outfit` without `Noto Serif TC` in CSS but also links both
  families in HTML.
- Workshop imports fonts in CSS and also links them in HTML.

## 6. Proposed Global Visual Tokens V0.1

These tokens are documentation roles first. Do not create a shared stylesheet
until a later exact-scope implementation gate approves it.

### 6.1 Font Roles

| Proposed role | Intended use | Current reference |
| --- | --- | --- |
| `font-ui-spatial` | Spatial Navigation, Expedition, and entry UI | `Inter`, `Noto Sans TC`, `Microsoft JhengHei`, `PingFang TC`, Arial, sans-serif |
| `font-ui-facility` | Facility body, values, metadata, and controls | `Outfit`, `Noto Serif TC`, serif fallback |
| `font-display-serif` | Facility titles, major detail names, dialogue emphasis, and selected primary actions | `Noto Serif TC`, serif |
| `font-debug-mono` | UIAction logs, diagnostics, and prototype output | `Cascadia Mono`, Consolas, monospace |

Fallback requirement:

- every role must remain readable when remote Google Fonts fail;
- font loading must not determine layout correctness;
- new facilities should select a role rather than invent a new stack.

### 6.2 Typography Roles

| Proposed role | V0.1 range | Guidance |
| --- | --- | --- |
| `type-panel-label` | `0.72rem` | Uppercase or tracked labels, screen labels, and compact panel identity |
| `type-debug` | `0.78rem` | Debug logs and prototype diagnostics |
| `type-meta` | `0.82rem` | Secondary values, descriptions, and compact state |
| `type-body-compact` | `0.85rem` to `0.88rem` | Dense catalog and operation workspace copy |
| `type-body` | `0.92rem` to `1rem` | Standard body, dialogue, and button copy |
| `type-subtitle` | `0.92rem` to `1.18rem` | Family-dependent supporting copy |
| `type-title-sm` | `1.5rem` to `1.85rem` | Compact spatial HUD title |
| `type-title-md` | `1.8rem` to `2.5rem` | Dialogue, workspace, and service title |
| `type-title-lg` | `2rem` to `3rem` | Catalog / Transaction reference title |
| `type-title-xl` | `2.2rem` to `4.65rem` | Large-title exception range requiring visual review |
| `type-title-hero` | `3rem` to `5.9rem` | Unique entry or cover title |

Title ranges are selected by family. They are not one universal title token.

### 6.3 Spacing Rhythm

Primary documented rhythm:

```text
4 / 8 / 12 / 16 / 20 / 24 / 32px
```

Rules:

- `12px` is the current dominant internal shell and panel gap.
- `16px` is the dominant standard desktop outer gutter.
- `8px` is the dominant compact control and metadata gap.
- `20px`, `24px`, and `32px` are reserved for large visual separation.
- `10px`, `14px`, and `18px` may remain as optical padding values, but should
  not become new spacing families.

### 6.4 Shell Gutter Vocabulary

| Proposed role | Current reference | Intended use |
| --- | --- | --- |
| `shell-gutter-compact` | `12px` outer gutter | Wide desktop facility scenes such as Shop, Magic Shop, Inn, and Temple |
| `shell-gutter-standard` | `16px` outer gutter | Bounded desktop shells such as Guild, Synthesis, Workshop, and base Exploration |
| `shell-gutter-mobile` | `6px` to `10px` | Family-specific stacked layouts |
| `shell-gutter-fullscreen` | `0px` | World Map, Combat, and accepted fullscreen presentation variants |

Shell width remains a family-shell decision, not a global token.

### 6.5 Panel Material

Global material description:

```text
dark translucent surface
+ thin family or facility accent border
+ inset or drop shadow
+ optional 8px title blur
+ typical 12px to 14px content-panel blur
```

Panel geometry remains family-specific:

- `4px` radius suits antique facility controls and compact service panels;
- `8px` radius suits spatial, expedition, and larger modern panels;
- `6px` may remain a spatial-HUD optical exception;
- opacity and blur must be reviewed against each background image.

### 6.6 Action Semantics

| State | Required semantic treatment |
| --- | --- |
| Primary | Stronger accent border or gradient, highest action emphasis, stronger hover glow |
| Secondary | Quieter neutral surface, lower visual emphasis, accent only on hover or focus |
| Disabled | Muted text, reduced opacity near current `.45`, no glow, blocked cursor, visible disabled reason nearby |
| Selected / Active | Accent border plus subtle fill or inset emphasis; must remain distinct from hover |
| Focus-visible | Visible outline or equivalent focus treatment independent of hover |
| Debug / Quiet | Low-emphasis control reserved for prototype or supporting actions |

Current selector forms remain valid according to screen behavior:

- native `:disabled`;
- `[aria-disabled="true"]`;
- `[data-disabled="true"]`.

Do not unify selector forms without reviewing HTML and render behavior.

## 7. Screen Family Shell Contracts

### 7.1 Spatial Navigation

Members: Town Hub, World Map

May share:

- UI-sans typography role;
- floating player/resource HUD material;
- location selected, locked, disabled, and focus semantics;
- fullscreen or near-fullscreen spatial stage;
- responsive move from spatial overlay toward stacked fallback.

Must preserve:

- Town Hub facility-node positioning and fixed bottom guidance/action treatment;
- World Map route nodes, detail drawer, menu drawer, and utility drawer;
- independent title treatment;
- no facility three-column template.

### 7.2 Catalog / Transaction

Members: Shop, Magic Shop, Synthesis

May share:

- facility font roles;
- catalog, selected detail, requirements, NPC/support, and footer grammar;
- title-copy material;
- selected row, disabled reason, feedback, and action semantics;
- desktop-to-single-column stacking concept.

Must preserve:

- transaction verb and detail content;
- resource-strip visibility;
- family member column widths until owner visual review;
- Synthesis large-title exception until reviewed;
- individual accent palette and background composition.

### 7.3 Catalog Variants

Members: Workshop, Guild

May share:

- catalog/task scanning hierarchy;
- detail/condition region;
- three-slot feedback/action footer grammar;
- facility font and action semantics.

Must preserve:

- Workshop mode-specific equipment presentation, background variants, and
  operation controls;
- Guild task/material modes, story hint, filters, and task-board density;
- independent geometry from the base Catalog / Transaction members.

### 7.4 Dialogue / Service

Members: Inn, Temple

May share:

- `1880px` compact-gutter shell;
- hero stage and bottom `135px` dialogue/service footer;
- footer three-slot geometry;
- `70px` desktop and `50px` stacked action heights;
- title range and panel material;
- `900px` stacking breakpoint.

Must preserve:

- Inn resource visibility and confirmation/dialogue behavior;
- Temple hidden resources, promotions modal, and inquiry choices;
- background, NPC, copy, and service semantics.

### 7.5 Operation Workspace

Member: Storage

May share with future operation workspaces:

- persistent operation state visibility;
- two-way source/destination scanning;
- quantity, capacity, and transfer feedback;
- operation-first responsive stacking.

Must preserve:

- transfer geometry;
- content-sized operation actions;
- visible resource/status strip;
- no forced large NPC or object showcase.

### 7.6 Object Showcase

Member: Relic Preview

May share with future showcase screens:

- central focus-object hierarchy;
- supporting slots and explanation panels;
- single strong primary action;
- object-first atmosphere.

Must preserve:

- `1 / 1.2 / 1` showcase geometry;
- relic altar/object emphasis;
- preview and attune semantics;
- no Storage transfer geometry.

### 7.7 Expedition

Members: Dungeon Exploration, Combat

May share:

- UI-sans font role;
- compact resource HUD;
- primary, disabled, and escape/retreat action semantics;
- fullscreen desktop presentation;
- debug-only action-log treatment.

Must preserve:

- Exploration event, route-state, progress, and footer action layout;
- Combat stage, player/enemy presentation, submenu, command row, and result
  overlay;
- separate responsive shell contracts.

### 7.8 Unique Entry

Member: Start Screen

May share:

- global action semantics;
- focus-visible and debug semantics;
- global spacing and typography role vocabulary.

Must preserve:

- cover-led composition;
- hero-title scale;
- entry/login action stack;
- unique responsive behavior.

## 8. New Facility Classification Checklist

Use this checklist before creating a facility shell:

1. What is the player's primary task?
   - scan and select a catalog;
   - converse and choose a service;
   - transfer or manipulate objects;
   - inspect a central object;
   - select a spatial destination;
   - perform a unique entry or transition.
2. Does the screen require a persistent list and selected detail?
   - yes: start with Catalog / Transaction;
   - task board or multi-mode equipment work: use a Catalog Variant.
3. Is quantity, capacity, source, and destination the core loop?
   - yes: use Operation Workspace.
4. Is NPC dialogue and a small service set the core loop?
   - yes: use Dialogue / Service.
5. Is one object the visual and informational focus?
   - yes: use Object Showcase.
6. Does the screen depend on node position or spatial relationships?
   - yes: use Spatial Navigation, not a facility catalog shell.
7. Select global font, title, spacing, material, and action roles.
8. Select the closest family shell.
9. Document required exceptions:
   - resource visibility;
   - title range;
   - background and safe areas;
   - NPC or object focus;
   - modal or special action placement.
10. If the screen cannot fit the family without changing the family's primary
    task, define a new variant rather than modifying every family member.

## 9. Drift Register

### 9.1 Clear Normalization Candidates

These items have enough CSS evidence to document as shared roles:

- font-role vocabulary and fallback responsibility;
- panel label size around `0.72rem`;
- debug/log size around `0.78rem` and mono role;
- spacing rhythm centered on `8px`, `12px`, and `16px`;
- primary, secondary, disabled, selected, and focus semantics;
- title-copy material as a facility-family pattern;
- family breakpoint and shell-gutter naming;
- explicit separation of Storage and Relic Preview geometry;
- explicit separation of Town Hub / World Map from facility catalog geometry.

### 9.2 Needs Browser Or Owner Visual Review

- whether Synthesis and Workshop large titles are accepted exceptions or drift;
- whether Storage root `19.5px` and Workshop final root `18px` are intentional;
- whether Shop and Magic Shop column-width differences are necessary;
- whether Guild action radius `8px` should remain a task-board variant;
- whether panel opacity and blur are balanced against every current background;
- whether all background safe areas remain readable at required viewports;
- whether Town Hub and World Map title hierarchies are correctly balanced;
- whether differing breakpoint values are task-driven or historical;
- whether remote font failure produces acceptable typography and wrapping.

### 9.3 Screen Exceptions To Preserve

- resource-strip visibility remains screen-specific;
- Town Hub and World Map spatial layouts;
- Storage transfer geometry;
- Relic Preview showcase geometry;
- Temple promotions modal and dialogue choices;
- Inn dialogue/service flow;
- Dungeon Exploration route/event/footer presentation;
- Combat stage and command layout;
- Start Screen cover and hero composition;
- background, accent, NPC, facility-object, and environment focus.

## 10. First Minimum CSS-Only Normalization Sprint

Recommended first family: Inn and Temple

Reason:

- Shop and Magic Shop already completed an earlier layout-normalization
  checkpoint and retain intentional resource and column-width differences.
- Inn and Temple have the strongest current family-shell parity.
- Their base geometry, title range, footer, actions, and breakpoint already
  match closely, allowing a low-risk documentation-to-CSS alignment pass.

### 10.1 Exact Touched Files

- `07_gui_prototype/inn_screen/styles.css`
- `07_gui_prototype/temple_screen/styles.css`

### 10.2 Allowed Change

CSS only:

- add screen-local Dialogue / Service family token aliases;
- replace matching literal shell, footer, action, title, radius, blur, and
  breakpoint-adjacent values with those aliases where the cascade remains
  behaviorally identical;
- preserve all screen-specific rules.

No shared stylesheet is created in this sprint.

### 10.3 Expected Result

- visual no-op at accepted viewports;
- clear reusable Dialogue / Service family contract inside both stylesheets;
- easier future comparison without creating a component library;
- no change to HTML, JavaScript, fixtures, runtime behavior, or resource
  visibility.

### 10.4 Risks

- CSS cascade differences between the two files;
- Temple modal and dialogue-choice overlays;
- desktop footer clipping;
- the exact `900px` stack transition;
- remote font rendering and Chinese text wrapping;
- accidental change to Inn resources or Temple hidden resources.

### 10.5 Browser Verification Plan

For both screens:

- desktop reference: `1440 x 900`;
- breakpoint edge: `901px` and `899px` viewport widths;
- compact/mobile: `560px` viewport width;
- default state and disabled-action state;
- footer alignment and action heights;
- title, dialogue, feedback, and long-text wrapping.

Inn-specific:

- resource HUD remains visible;
- dialogue choices and confirmation remain usable.

Temple-specific:

- resource HUD remains hidden;
- inquiry choices remain aligned;
- promotions modal opens, scrolls, and closes without overlap.

### 10.6 Implementation Result

Implemented on June 15, 2026.

Completed CSS-only changes:

- added the same 13 screen-local `--dialogue-service-*` family aliases to Inn
  and Temple;
- replaced matching shell, title, panel, footer, and action literals with the
  aliases;
- preserved screen-specific resources, dialogue choices, modal, backgrounds,
  copy, and interaction rules;
- did not create shared CSS or modify HTML, JavaScript, fixtures, runtime, data,
  schema, save, or combat.

Static verification:

- `git diff --check`: PASS;
- Inn and Temple family alias maps: identical;
- required alias usage: complete;
- CSS brace structure: balanced;
- each screen uses the family aliases 21 times.

Initial browser review found two owner-approved follow-up items:

- at the `901px` review width, the desktop shell still used fixed base columns
  that widened the footer beyond the visible shell;
- Temple static loading fetched `default` instead of an existing fixture JSON,
  causing a `Fixture request failed: 404` state.

Follow-up implemented on June 16, 2026 (Asia/Taipei session):

- added matching Inn and Temple narrow-desktop bridge rules for `901px` through
  `1287px`, preserving desktop footer grammar while allowing shell columns to
  fit the viewport;
- removed Inn's narrow-desktop resource strip scale so the visible resource HUD
  stays inside the review viewport;
- changed Temple's fixture option to `./fixtures/temple-default.json`;
- preserved the existing `900px` stacked breakpoint behavior and did not expand
  normalization to other screen families.

Browser verification completed after the follow-up:

- Inn and Temple loaded with `data-load-state="ready"` at `1440 x 900`,
  `901 x 900`, `899 x 900`, and `560 x 900`;
- no body, shell, or footer horizontal overflow at the tested viewports;
- Inn resource HUD remained visible;
- Temple resource HUD remained hidden;
- desktop action height remained `70px`;
- stacked action height remained `50px`;
- Inn confirmation choices opened and disabled the hidden action buttons;
- Temple guide choices opened, and the promotions modal opened without overlap
  or page overflow.

Codex desktop loading note:

- use the Browser plugin with the in-app browser for GUI verification;
- start the temporary static server inside the same persistent browser-control
  environment so it remains alive during navigation;
- serve the repository path `07_gui_prototype/` as the server root;
- use `http://127.0.0.1:8000/<screen_folder>/index.html` for screen URLs;
- do not use `file://`, because fixture `fetch()` calls may fail;
- prefer `127.0.0.1` over `localhost` when checking this environment, because
  it avoids IPv6/localhost ambiguity;
- if the shell `py -3` route fails because the Windows launcher points to an
  unusable Store Python, use the bundled Codex runtime or the in-browser
  temporary server route instead;
- reset the temporary viewport and close the server after verification.

## 11. Implementation Gate

This audit establishes the classification and planning baseline. The first
Dialogue / Service CSS-only alias sprint and its owner-approved browser follow-up
are implemented and browser-verified for Inn and Temple.

Further implementation is not approved by this audit. It does not approve:

- a shared visual CSS file;
- a formal token package or component library;
- HTML, JavaScript, fixture, asset, runtime, data, schema, save, or combat
  changes;
- normalization of Synthesis or Workshop large titles;
- cross-family geometry unification.
