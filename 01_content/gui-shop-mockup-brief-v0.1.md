# GUI Shop Mockup Brief V0.1

Purpose: define one bounded visual mockup candidate for the Shop
Mockup-to-HTML Skinning Lab while preserving the current Shop prototype shell.

Status: `retired_historical_after_experiment_completion`.

This early Shop single-screen mockup route is a historical record. The owner
retired and removed `08_experiments/` after facility skinning exploration
completed. Do not generate another Shop candidate or implement this brief as an
active route.

This document is a markdown-only brief. It does not generate an image, approve
image generation, create a runtime asset, start an asset pipeline, or authorize
HTML/CSS/JavaScript implementation.

## 0. Status

```yaml
brief_id: gui_shop_mockup_brief_v0_1
screen_id: facility_shop_screen
prototype_path: 07_gui_prototype/shop_screen/
shell_family: transaction_list_detail_npc
status: retired_historical_after_experiment_completion
candidate_count: 1
generation_status: one_preview_candidate_generated_outside_repository
implementation_status: accepted_results_live_in_formal_prototype
runtime_usage_allowed: false
asset_pipeline_status: not_started
```

Primary planning references:

- `01_content/gui-facility-shell-baseline-v0.1.md`
- `01_content/gui-shop-skinning-lab-readiness-checklist-v0.1.md`
- `07_gui_prototype/shop_screen/index.html`
- `07_gui_prototype/shop_screen/styles.css`

## 1. Mockup Goal

Create one visual mockup candidate that demonstrates how a warm frontier supply
shop atmosphere and a recognizable merchant presence could support the current
Shop HTML shell.

The candidate should validate:

- whether the existing three-column Shop layout can carry a stronger visual
  identity without becoming harder to read;
- whether a merchant half-body visual can occupy the current right column
  without competing with item browsing and purchase decisions;
- whether subtle full-shell atmosphere can sit behind translucent HTML/CSS
  panels;
- whether the current header, footer feedback, and action hierarchy remain
  visually clear.

The candidate should not validate:

- a redesigned Shop layout;
- new Shop functions or gameplay;
- final production artwork;
- facility-family-wide styling;
- mobile redesign;
- a formal asset pipeline or Design System.

## 2. Candidate Direction

### 2.1 Recommended Visual Direction

```text
Warm frontier traveling-supply shop
with a practical merchant counter atmosphere,
restrained fantasy decoration,
and a right-column merchant half-body focal visual.
```

The Shop should feel:

- practical and welcoming rather than luxurious;
- stocked for dungeon expeditions rather than general city commerce;
- warm, worn, and functional;
- connected to a frontier adventurer town;
- visually distinct from the arcane Magic Shop and craft-focused Synthesis
  facility.

Suggested atmosphere:

- warm amber lantern light;
- dark wood shelving and travel crates;
- rolled maps, rope, leather packs, bottles, and supply bundles;
- subtle brass fittings and worn signboard shapes;
- restrained teal or green accents that support the current Shop identity;
- a merchant who reads as experienced, approachable, and commercially alert.

Avoid:

- modern convenience-store styling;
- luxury boutique presentation;
- dense marketplace crowds;
- bright gacha-shop styling;
- generic medieval tavern imagery;
- an illustration so detailed that it competes with Shop information.

### 2.2 Merchant Format

Recommended V0.1 candidate:

```text
right-column half-body merchant
```

The merchant should:

- remain primarily inside the existing right-side visual region;
- face slightly toward the center item-detail area;
- keep the face and upper-body silhouette readable;
- leave a quiet lower region for HTML-rendered NPC name and role;
- remain safely croppable when the responsive layout stacks;
- avoid holding objects that resemble functional Shop buttons or item-row icons.

This candidate does not decide the merchant's final character design.

### 2.3 Atmosphere Containment

Recommended V0.1 candidate:

```text
merchant focal art contained in the right column
+ low-detail Shop atmosphere allowed behind the full shell
```

The full-shell atmosphere must remain quiet behind the left and center columns.
It should create material and lighting context, not become a second information
layer.

## 3. Existing Shell To Preserve

### 3.1 Large-Screen Composition

```text
header
three-column main content
footer
collapsed UIAction Log
```

Visible shell rows remain:

1. Shop header.
2. Shop main content.
3. Shop footer.
4. Collapsed UIAction Log.

The Shop resource strip remains hidden and must not appear in the mockup.

### 3.2 Main Content Columns

| Column | Current role | Mockup treatment |
|---|---|---|
| Left | Category tabs and item list | Quietest functional panel; prioritize scanning and row-state readability |
| Center | Item detail and purchase requirements | Main decision panel; reserve the strongest text-safe area |
| Right | Merchant portrait, name, and role | Primary visual focal region; keep HTML copy-safe space |

### 3.3 Footer

| Footer area | Current role | Mockup treatment |
|---|---|---|
| Left | Return to Town | Clearly secondary navigation |
| Center | Feedback, disabled reason, and result | Wide readable message region |
| Right | Primary purchase action | Strongest interactive emphasis |

The footer must remain visually distinct from the background atmosphere.

## 4. Screen Identity Decision For V0.1

For this candidate:

- keep the dynamic Shop title and subtitle in the existing header region;
- treat the header as a lighter atmospheric overlay rather than a large
  illustrated signboard;
- omit the generic `設施畫面` label from mockup evaluation;
- omit fixture controls and UIAction Log from the polished candidate view;
- keep the underlying prototype controls conceptually available for later
  verification;
- keep merchant name and role as HTML-rendered copy;
- treat the `行商` category label as optional and not required in the candidate.

These choices are V0.1 mockup assumptions, not final Shop UI decisions.

## 5. Dynamic HTML Overlay Contract

All required interface information remains dynamic HTML-rendered content.

Must remain HTML-rendered:

- Shop title and subtitle;
- category labels;
- item titles, summaries, prices, ownership, and statuses;
- selected item detail;
- effect and use-context text;
- requirement labels, values, and states;
- merchant name and role;
- feedback speaker and message;
- back and purchase action labels;
- disabled reasons and result messages.

The mockup image may contain:

- merchant character art;
- shelves, counter, crates, bottles, packs, maps, ropes, and other atmospheric
  supply-shop objects;
- decorative unreadable marks or abstract sign shapes;
- lighting, surface texture, and restrained ornamental framing.

The mockup image must not contain readable UI text, numbers, prices, labels,
buttons, status badges, or gameplay information.

## 6. Text-Safe And Visual-Safe Zones

| Zone | Required safety | Candidate guidance |
|---|---|---|
| Header | Dynamic title plus one short subtitle | Low-detail band with stable contrast; no bright shelf light behind title |
| Left item browser | Dense Chinese row text and category tabs | Darkest and quietest area; avoid merchant limbs, shelves with strong horizontal labels, or bright objects |
| Center item detail | Several lines of description and metadata | Broad text-safe surface with restrained edge decoration |
| Center requirements | Multiple rows and semantic states | Neutral background; avoid decorative red/green signals |
| Right merchant face | Safe focal crop | Keep face away from likely narrow-layout crop edges |
| Right merchant copy | NPC name and role | Quiet lower or side zone with no detailed props behind copy |
| Footer feedback | One to two lines of dynamic text | Stable, readable strip independent of background image |
| Footer actions | Secondary and primary controls | Avoid decorative frames that resemble extra buttons |

## 7. Panel And Overlay Treatment

The mockup should test a translucent HTML/CSS overlay approach:

- dark translucent functional panels;
- restrained blur or softened background beneath text-heavy regions;
- slightly stronger opacity in the item browser, detail, requirements, and
  feedback areas;
- lighter framing around the merchant region;
- clear selected and disabled states that do not rely on the image;
- decorative corners or edge accents only where they do not reduce text-safe
  space.

The mockup should not imply that every panel must become fully transparent.
Readability has priority over revealing more background art.

## 8. Candidate Review Frame

Primary mockup review frame:

```yaml
viewport_width: 1440px
layout_state: three_column
shop_resource_strip: hidden
fixture_state: default_shop
selected_item_state: purchasable
lab_only_markers_visible: false
```

The candidate should visually represent:

- a populated item list;
- one selected purchasable item;
- readable item detail;
- readable purchase requirements;
- merchant presence;
- readable feedback;
- clear back and purchase actions.

The candidate must not invent specific new products or render readable product
names. Abstract text blocks or the existing HTML screenshot composition may be
used to represent dynamic content during visual planning.

Secondary responsive review remains required later at:

- `1221px`
- `1220px`
- `720px`

The single visual mockup candidate itself only needs to establish the `1440px`
direction. It must not claim responsive validation before HTML/CSS testing.

## 9. Generation-Ready Content Brief

Use the following content brief only after separate approval to create one Shop
visual mockup candidate:

```text
Create one polished visual mockup reference for a fantasy RPG frontier supply
shop screen, designed to skin an existing HTML interface rather than redesign
its layout.

Preserve the existing composition:
- a light header overlay for dynamic Shop title and subtitle;
- a quiet left column for category tabs and a scrollable item list;
- a broad center column for selected item detail and purchase requirements;
- a right column containing an approachable, experienced traveling merchant as
  a half-body focal character;
- a bottom footer with secondary navigation on the left, a wide feedback area
  in the center, and a primary purchase action on the right.

Visual atmosphere:
- warm frontier adventurer supply shop;
- amber lantern light, dark wood shelves, travel crates, rolled maps, rope,
  leather packs, bottles, and practical expedition supplies;
- restrained teal or green accents;
- worn but welcoming, practical rather than luxurious;
- the merchant faces slightly toward the center detail area.

Overlay safety:
- keep the left item-list and center detail areas dark, quiet, and low-detail;
- preserve a broad text-safe area for Chinese descriptions and requirement rows;
- preserve a quiet lower area in the merchant column for dynamic NPC name and
  role;
- keep the footer clearly readable;
- background decorations must not resemble buttons, item rows, badges, or
  semantic status indicators.

Dynamic text policy:
- do not include readable Chinese, English, numbers, prices, labels, item names,
  buttons, feedback, resource values, or status text in the image;
- all UI text and controls will remain HTML-rendered overlays.

Do not add:
- a visible resource strip;
- Shop sell mode, quantity controls, equipment management, or new gameplay;
- a crowd scene, luxury boutique, tavern, modern shop, or gacha-store styling;
- a new layout or additional interface regions.

Output intent:
- one 1440px-direction visual mockup candidate for review;
- visual reference only, not a runtime asset;
- suitable for later bounded HTML/CSS skinning-lab review.
```

## 10. Candidate Acceptance Checklist

- [ ] Reads as a frontier adventurer supply shop.
- [ ] Preserves the existing header, three-column content, and footer hierarchy.
- [ ] Does not show a resource strip.
- [ ] Keeps the left and center columns quiet enough for dense dynamic HTML text.
- [ ] Gives the merchant a clear right-column focal presence.
- [ ] Preserves an HTML copy-safe region for merchant name and role.
- [ ] Keeps footer feedback and actions visually distinct.
- [ ] Contains no readable UI text, prices, values, labels, or buttons in the
      image layer.
- [ ] Does not imply new Shop functions or gameplay.
- [ ] Does not present itself as a runtime asset or facility-family-wide final
      style.
- [ ] Can plausibly degrade to a readable Shop when the visual image is removed.

## 11. Stop Conditions

Return to a read-only review if a mockup direction:

- changes the three-column information hierarchy;
- adds a visible resource strip;
- removes or hides purchase requirements;
- turns feedback into image-baked dialogue;
- places the merchant across left or center text-heavy regions;
- requires item, price, or action text to be embedded in artwork;
- introduces new Shop functions or gameplay;
- becomes a full-screen illustration with decorative UI pasted over it;
- claims responsive readiness without HTML/CSS verification;
- requires propagation to another facility before Shop is reviewed.

## 12. Next Approval Gate

This brief is retained for historical context only. It does not define a next
action or authorize renewed Shop mockup, experiment, or implementation work.
