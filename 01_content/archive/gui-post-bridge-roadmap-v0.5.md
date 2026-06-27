# GUI Post-Bridge Roadmap V0.5

> Purpose: This document records the post-bridge direction after the main GUI live bridge families are mostly complete. It is a planning reference before detailed implementation, not an implementation task, not a formal design system, not a full UI framework, and not a formal asset pipeline.

## 1. Current Position

The current Element Maze / 元素迷宮 project position is:

- The CLI demo remains the gameplay authority.
- The GUI prototype is a screen shell and interaction-feel prototype, not gameplay authority.
- The GUI live bridge connects existing CLI runtime / state / action behavior to GUI ScreenModel / UIAction.
- The current target is an expandable playable demo, not a closed demo.
- Narrow MVP is a current-slice risk control method. It does not mean future extension points are closed.
- Bridge families that have already been proven should move toward CLI coverage / bridge coverage cleanup.
- System families that have not been proven should still use small MVP gates.

This document exists to prevent the project from losing the overall direction after bridge completion and over-focusing on local polish, micro-refactors, or isolated UI details.

## 2. Post-Bridge Roadmap

Recommended order after the main GUI live bridge work is mostly complete:

1. Bridge Closeout / Coverage Cleanup
2. God File / Maintainability Checkpoint
3. GUI Layout Normalization V0.5
4. Render-layer Polish Slice
5. UI Skinning Vertical Slice V0.5
6. Gameplay / Data Expansion
7. Formal Design System / Asset Pipeline, deferred until later

This roadmap is directional. It does not authorize broad refactors, full UI framework work, formal design system work, or large asset pipeline work.

## 3. Bridge Closeout / Coverage Cleanup

The first post-bridge step is to confirm whether the main bridge families are actually complete enough to move forward.

Suitable work:

- Confirm which GUI live bridge families have landed.
- Confirm which screens are bridge-complete, coverage-incomplete, shell-only, or intentionally deferred.
- Add missing bridge coverage only when the CLI runtime / data / action already exists.
- Add or update smoke tests when they directly support the completed bridge family.
- Update concise documentation only when the project state has changed.

Not suitable work:

- New gameplay systems.
- New formal runtime contracts.
- New save/schema migrations unless explicitly planned.
- Treating Temple / Relic / Settings as bridge defects when they are currently outside the bridge closeout scope.

Current boundary notes:

- Temple / Relic are currently at the CLI demo boundary. Fire Mark / church / relic content may remain preview-only or shell-like by design.
- Settings is not currently a CLI gameplay system and should be deferred to GUI polish or full-game expansion.

## 4. God File / Maintainability Checkpoint

After bridge closeout, the project should check whether major runtime or GUI bridge files are becoming god files.

Typical candidates:

- `game.py`
- `gui_actions.py`
- large ScreenModel builder sections
- repeated UIAction routing helpers
- runtime helpers that mix gameplay, state mutation, display shaping, and bridge response formatting

The purpose of this checkpoint is not aesthetic cleanup. The purpose is:

- Improve AI-agent施工 boundaries.
- Reduce accidental cross-layer edits.
- Prepare for future schema / ScreenModel / UIAction constraints.
- Make smoke tests easier to write and target.
- Keep CLI and GUI connected to the same gameplay authority.
- Reduce diff noise and review burden.
- Prevent runtime god files from causing documentation god files.

### 4.1 Bounded Slice, Not Endless Micro-slice

Refactor and maintainability work should use bounded slices, not endless micro-slices.

The goal is to reduce risk and improve reviewability, not to split every small change into separate sessions. Low-risk changes that share the same purpose, layer, and affected family may be grouped into one implementation slice. Read-only planning is required mainly when the work crosses runtime/schema/save/data/combat boundaries, changes shared contracts, or risks becoming a broad refactor.

Recommended principle:

> High-risk work should be sliced smaller. Low-risk same-layer work may be grouped. A slice must have a clear boundary, but should not be so small that it blocks progress.

In short:

> 大風險小切，低風險合併；切片要有邊界，但不要微切到阻塞進度。

### 4.2 Proven Pattern Confidence

After the first successful bridge or layout pattern in a family has landed and passed verification, follow-up work in the same family may use a larger bounded slice. The goal is to benefit from the proven pattern instead of treating every similar screen as a new unknown system.

For example, once one facility bridge pattern has been validated, related facility screens may follow the same ScreenModel / UIAction / render-layer approach for coverage cleanup. They do not require the same level of read-only planning as the first sample, unless they cross runtime/schema/save/data/combat boundaries or introduce a new contract.

Recommended principle:

> 首例嚴控，後續比照；已驗證 pattern 應轉化為施工效率，而不是繼續微切片。

Construction analogy:

> The first sample room should be checked carefully. After the sample is accepted, similar rooms should follow the proven method. They should not each be treated as a brand-new design and inspection process unless they have special conditions.

### 4.3 When to Be Strict

Use stricter slicing and read-only planning when work may affect:

- `save.json` or save migration.
- `04_data` or schema.
- combat formula.
- shared runtime contract.
- CLI gameplay and GUI bridge at the same time.
- new formal systems such as relic, class, settings, or full asset pipeline.
- multiple unrelated screen families.
- large diffs that are difficult to review.

### 4.4 When to Allow Grouping

The following may be grouped into one bounded slice when they share the same purpose and layer:

- Follow-up work using an already proven bridge family pattern.
- Same-family layout cleanup.
- Same-type button / modal / overlay alignment.
- Same bridge family coverage cleanup.
- Small helper extraction within the same file or family when behavior is preserved.
- Small smoke test updates that directly verify the same change.
- Small documentation sync that records the same landed state.

This is especially important for facility-family work such as Shop / Magic Shop / Workshop / Synthesis / Storage / Guild when a related bridge pattern has already been proven.

## 5. GUI Layout Normalization V0.5

GUI Layout Normalization V0.5 is the recommended next UI-facing step after bridge closeout and maintainability checkpointing.

This is not formal UI design work. It is a layout consistency pass before UI skinning.

Suitable scope:

- Panel size ranges.
- Button size ranges.
- Spacing / gap conventions.
- Back button placement.
- Confirm / cancel / close placement.
- Modal / overlay size categories.
- Facility-family common structure.
- Hub / dungeon / combat family differences.
- Identifying where visual differences are intentional and should not be forced into one layout.

Not suitable scope:

- Pixel-perfect layout rules.
- Formal component library.
- Full CSS / JS framework refactor.
- Full UI framework.
- Formal design tokens.
- Formal asset pipeline.
- Rebuilding all screens.
- Hard-unifying every screen family.

Recommended framing:

> GUI Layout Normalization V0.5 organizes minimum viable consistency across existing GUI prototype / live bridge screens before UI skinning. It is not a formal design system and does not authorize broad frontend refactors.

## 6. Render-layer Polish Slice

After layout normalization rules are agreed, choose one or two screen families for focused render-layer polish.

Suitable work:

- Scroll behavior.
- Overlay stacking.
- Button alignment.
- Panel balance.
- Text wrapping.
- Result modal readability.
- Facility list layout.
- Consistent close / back behavior.

Unsuitable work:

- Gameplay changes.
- Data/schema/save changes.
- Formal asset import pipeline.
- Rewriting shared UI architecture.
- Full-screen redesign across all families.

Recommended first candidates:

- Facility family: Shop / Magic Shop / Workshop / Synthesis / Storage / Guild.
- Navigation family: Town Hub / World Map.
- Adventure family: Dungeon Exploration / Combat.

The first polish slice should be small enough to review, but not artificially split into one button or one CSS property per session.

## 7. UI Skinning Vertical Slice V0.5

UI skinning should begin only after the layout structure is reasonably stable.

Recommended approach:

- Pick one representative flow.
- Apply visual style to that flow only.
- Use it as a future reference, not a formal asset pipeline.

Possible vertical slice:

Start Screen → Town Hub → Guild → World Map → Dungeon Exploration → Combat → Result → Town Hub

Suitable work:

- Color direction.
- JRPG mood.
- Panel decoration.
- Background treatment.
- Icon usage.
- Typography hierarchy.
- NPC / facility atmosphere.

Not suitable work:

- Full art production pipeline.
- Complete design system.
- Global asset naming/import/loading system.
- Mandatory visual rules for every future screen.

## 8. Gameplay / Data Expansion

Gameplay and data expansion should be discussed after the bridge and GUI foundation are stable enough.

Possible future directions:

- New dungeon.
- New boss.
- New quest line.
- Fire Mark formalization.
- Relic formalization.
- Class / specialization expansion.
- Temple expansion.
- Settings / save management.
- Full-game progression planning.

These should not be mixed into layout normalization, bridge closeout, or render-layer polish tasks unless explicitly scoped.

## 9. Explicit Deferrals

The following should remain deferred unless explicitly approved in a future planning session:

- Full UI framework.
- Formal Design System.
- Formal asset pipeline.
- Large runtime refactor.
- Complete engine re-architecture.
- Full schema migration.
- Save migration.
- Combat formula rewrite.
- Complete Temple / Relic formalization.
- Settings as a formal system.
- Multi-family frontend rewrite.
- Rebuilding all prototype screens.

## 10. How to Use This Document

This document is a direction guide, not an implementation order.

Codex may use it for:

- Read-only planning.
- Determining whether a proposed task belongs to bridge closeout, maintainability, layout normalization, render polish, UI skinning, or gameplay expansion.
- Checking whether a task is becoming too broad.
- Identifying whether an existing pattern is already proven and can be reused efficiently.

Antigravity should not use this document alone as authorization to implement broad changes. Implementation still needs a specific bounded task.

Future planning should check this document when:

- A task starts to expand into full UI framework work.
- A small cleanup becomes endless micro-slicing.
- A proven pattern is being treated as a brand-new unknown system.
- A god file starts absorbing too many unrelated responsibilities.
- UI polish starts mixing with gameplay/data/schema/save changes.

## 11. One-line Principles

- CLI remains gameplay authority.
- GUI bridge connects existing runtime; it should not reinvent gameplay.
- Bridge-complete families should gain coverage efficiency from proven patterns.
- Layout normalization is not a formal design system.
- Refactor work should improve governance and reviewability, not create endless micro-slices.
- High-risk work should be sliced smaller; low-risk same-layer work may be grouped.
- First sample strict, follow-up by proven pattern.
- Do not let local polish make the project forget the post-bridge roadmap.
