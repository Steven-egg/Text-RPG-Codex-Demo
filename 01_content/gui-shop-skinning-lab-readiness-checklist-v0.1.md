# GUI Shop Skinning Lab Readiness Checklist V0.1

Purpose: define the minimum readiness gate for using the current Shop Screen as
the first representative GUI Mockup-to-HTML Skinning Lab.

Status: `paused_by_owner`.

This Shop single-screen route is paused. The active planning baseline has
returned to facility-family Mockup-to-HTML responsibility mapping in
`01_content/gui-facility-shell-baseline-v0.1.md`. Do not resume this checklist,
generate another Shop candidate, or implement Shop skinning without new explicit
owner approval.

This checklist is documentation-only. It does not approve mockup generation,
image generation, asset import, HTML/CSS/JavaScript edits, runtime bridge work,
or expansion to other facility screens.

## 0. Lab Objective

The Shop Skinning Lab should answer one bounded question:

> Can a facility-atmosphere and merchant-presence skin be placed behind the
> current Shop HTML interface without weakening its existing layout,
> readability, responsive behavior, or action feedback?

The lab is not intended to:

- redesign Shop interaction or information architecture;
- define the final visual direction for every facility;
- create a formal asset pipeline, Design System, component library, or GUI
  framework;
- modify runtime, ScreenModel, UIAction, fixture semantics, data, schema, save,
  economy, or gameplay behavior;
- automatically propagate Shop styling to Magic Shop or Synthesis.

## 1. Representative Screen And Current Shell

Representative screen:

```text
07_gui_prototype/shop_screen/
```

Shell family:

```text
Transaction / List-Detail-NPC Shell
```

Current large-screen row structure:

```text
Shop header
-> three-column Shop content
-> Shop footer
-> collapsed UIAction Log
```

The Shop resource strip remains hidden. The current Shop shell therefore keeps
four visible shell rows. A skinning lab must not reintroduce a visible resource
row without a separate owner decision.

Current three-column content structure:

```text
left: category tabs + item list
center: item detail + purchase requirements
right: merchant portrait + identity
```

Current footer structure:

```text
left: return to Town
center: feedback / disabled reason / result
right: primary purchase action
```

At `1220px` and below, the Shop main content and footer stack into a single
column. The lab must preserve this existing responsive boundary.

## 2. Retained Functional Layout

All items below must remain present and readable during any future skinning lab.

### 2.1 Screen Identity

- Dynamic facility title.
- Dynamic short subtitle.
- Clear separation between facility identity and functional content.

### 2.2 Item Browser

- Category tabs.
- Scrollable item list.
- Selected, enabled, and disabled row states.
- Item title, summary, price, ownership, or status information currently
  provided by the render layer.

### 2.3 Item Detail And Requirements

- Selected item title and description.
- Category, ownership, effect, or use-context information.
- Detail status badge.
- Purchase requirement rows.
- Required and current values.
- Met, blocked, or unavailable status communication.

### 2.4 Merchant Presence

- A preserved right-side visual region for merchant presence.
- HTML-rendered NPC name and role.
- Enough visual separation between merchant art and functional panels.

### 2.5 Footer Actions And Feedback

- Back to Town control.
- Feedback speaker and message.
- Primary purchase action.
- Disabled reason and result feedback.
- Clear distinction between navigation, feedback, and primary action.

## 3. Element Classification For Visual Review

### 3.1 Final-UI Candidates

These elements should be visible when judging whether a skin works:

- dynamic Shop title and subtitle;
- category tabs and item rows;
- item detail and requirement information;
- status badges and disabled states;
- merchant name and role;
- feedback message;
- back and primary action controls.

Their exact colors, decoration, typography, and panel treatment are not approved
by this checklist.

### 3.2 Lab-Only Markers

These elements support prototype testing and should be excluded from final-style
evaluation. They may be temporarily hidden only within an explicitly approved
skinning lab:

- generic `設施畫面` label;
- fixture switcher and `測試狀態` label;
- fixture option names;
- UIAction Log and its clear control;
- loading, fixture-failure, static-prototype, and debug wording.

Hiding a lab-only marker for a visual review does not authorize deleting it from
the prototype or removing its verification role.

### 3.3 Placeholder / Replaceable Visual Candidates

These establish layout position but are not approved as final art:

- current NPC portrait placeholder;
- portrait initials or generated placeholder tokens;
- current decorative panel backgrounds;
- temporary merchant description or construction copy when it is used only to
  establish space;
- empty or low-detail visual space inside the merchant region.

### 3.4 Needs Owner Decision

Confirm these before any image or CSS implementation:

- whether the Shop title and subtitle remain in the current header or move into
  a lighter overlay treatment;
- whether `行商` remains a visible NPC-category label;
- whether merchant-role copy is final content, temporary guidance, or shortened
  skinning-lab copy;
- whether the lab uses a merchant portrait, half-body character, or a broader
  facility scene with the merchant placed inside it;
- whether the future image is confined to the merchant column or may extend
  behind the full shell as a low-detail background.

## 4. Hero Image Safe Area

### 4.1 Required Safe Area

The primary hero image safe area is the current right-side merchant region.

It should support:

- a clearly readable merchant face or focal subject;
- merchant identity without embedding the NPC name or role into the image;
- enough lower-area quiet space for the existing HTML-rendered NPC copy;
- responsive cropping that does not remove the face or primary silhouette.

### 4.2 Optional Atmosphere Extension

A future lab may test a low-detail facility atmosphere extending behind the
full Shop shell, but only if:

- left and center reading areas remain visually quiet;
- panel text contrast remains stable;
- background details do not resemble buttons, badges, rows, or status markers;
- the merchant remains the main visual focal point;
- removing the image still leaves a fully readable and usable Shop.

### 4.3 Image Content Restrictions

Do not bake any of the following into a hero or background image:

- facility title or subtitle;
- merchant name or role;
- category labels;
- item names, icons intended as functional identifiers, prices, or owned counts;
- requirement text or status;
- buttons, feedback, disabled reasons, or result messages;
- Gold or player resource values;
- fixture, debug, or UIAction information.

## 5. HTML/CSS Overlay Safe Areas

| Area | Overlay requirement | Background guidance |
|---|---|---|
| Header / screen identity | Must support dynamic title and one short subtitle | Keep low-detail and avoid a bright focal point directly behind text |
| Left item browser | Must support tabs, scrolling rows, status, price, and ownership text | Use the quietest background region; avoid character silhouettes and strong edges |
| Center detail card | Must support several lines of Chinese description and item state | Keep contrast stable and decoration outside the main reading block |
| Center requirement panel | Must support multiple requirement rows and blocked states | Avoid red/green decorative cues that could conflict with semantic states |
| Right merchant region | Must support HTML NPC name and role over or below visual art | Preserve face-safe and copy-safe zones |
| Footer feedback | Must support one to two lines of result or disabled-reason text | Keep readable independently from the hero image |
| Footer actions | Must keep back and purchase actions visually distinct | Avoid background shapes that resemble interactive controls |

Required interface information remains HTML-rendered. The skin may support the
interface but must not become the interface.

## 6. Existing Shop Exceptions To Preserve

- Shop resource strip remains hidden.
- Shop keeps four visible shell rows.
- Main content remains three columns above the existing responsive boundary.
- At `1220px` and below, content and footer stack to one column.
- The merchant region remains a layout-safe visual reserve even before final
  artwork exists.
- Feedback remains a dedicated footer region rather than being hidden inside
  merchant dialogue or background art.
- Primary purchase action remains separate from item-row selection.
- Fixture switching and UIAction logging remain available for prototype
  verification, even if temporarily hidden during an approved visual capture.

## 7. Mockup Brief Inputs Required

Before creating a Shop mockup candidate, record:

- intended Shop atmosphere and visual mood;
- merchant visual format: portrait, half-body, or facility scene;
- hero image containment: merchant column only or low-detail full-shell
  background;
- protected text-safe zones from Section 5;
- final-candidate elements that must be shown in the mockup;
- lab-only markers that should be omitted from the mockup;
- the target review viewport;
- explicit statement that all visible text and controls will remain HTML-rendered.

The mockup brief must not invent gameplay, products, Shop services, sell modes,
quantity controls, equipment management, or economy changes.

## 8. Review Viewports And Acceptance Criteria

Required review viewports:

- `1440px`: full three-column shell and merchant visual balance.
- `1221px`: final width immediately above the stacking breakpoint.
- `1220px`: first stacked-layout width.
- `720px`: narrow-screen readability and safe cropping.

The lab is ready to pass only when all applicable criteria are true:

- [ ] The retained functional layout from Section 2 is still recognizable.
- [ ] Shop resource strip remains hidden.
- [ ] No required text, value, state, or action is baked into an image.
- [ ] Item list and detail text remain readable over the skin.
- [ ] Requirement states remain distinguishable without relying on the
      background image.
- [ ] Merchant focal art does not compete with list, detail, requirements, or
      actions.
- [ ] NPC name and role remain HTML-rendered and readable.
- [ ] Back, feedback, and primary action remain distinct.
- [ ] Disabled and result feedback remain readable.
- [ ] `1440px`, `1221px`, `1220px`, and `720px` show no horizontal overflow,
      overlap, clipped critical text, or unsafe merchant cropping.
- [ ] The Shop remains readable and usable when the skin image is removed.
- [ ] Fixture switching and UIAction logging still remain available for
      verification.

## 9. Stop Conditions

Stop the lab and return to a read-only review if a proposed direction requires:

- changing Shop information architecture or interaction flow;
- showing the resource strip;
- moving or removing the dedicated feedback region;
- changing ScreenModel or UIAction behavior;
- adding products, services, sell modes, quantity selection, or gameplay;
- replacing dynamic HTML text with image-baked text;
- creating a shared asset pipeline, Design System, or facility framework;
- applying the result to Magic Shop, Synthesis, Workshop, Guild, or other
  facilities without a separate review;
- broad responsive-layout restructuring rather than skinning the existing shell.

## 10. Approval Gate

This checklist establishes readiness criteria only.

Before any next action, obtain separate owner approval for exactly one of:

1. A markdown-only Shop mockup brief.
2. One Shop visual mockup candidate.
3. One bounded Shop HTML/CSS skinning lab.

Approval for one option does not imply approval for the others, and does not
approve propagation to the broader facility family.
