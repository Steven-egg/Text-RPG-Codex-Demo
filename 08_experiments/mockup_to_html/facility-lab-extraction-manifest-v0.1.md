# Facility Lab Extraction Manifest V0.1

This manifest summarizes the results of the batch extraction of official facility screens into isolated, fixture-only visual labs.

## Extraction Summary

- **Source Root**: `07_gui_prototype/`
- **Target Root**: `08_experiments/mockup_to_html/`
- **Status**: All 8 screens successfully extracted. No official prototype code modified. No forbidden keywords remain in the lab files.

---

## 1. Guild Screen (`guild_skinning_lab`)

- **Source -> Lab**: `07_gui_prototype/guild_screen/` -> `08_experiments/mockup_to_html/guild_skinning_lab/`
- **Fixture Scenarios**:
  - `default`: Default Board (`guild-default.json`)
  - `quest-ready`: Quest Ready / Fire Mark (`guild-quest-ready.json`)
- **Extraction Adjustments**:
  - Removed ESM `import` of `runtimeClient`.
  - Removed `loadLiveScreen`, `loadStaticFallback`, and `handleBackToTown` functions.
  - Intercepted back button click listener to only log the action locally instead of navigating.
  - Stripped `runtimeClient.isLiveMode()` checks and live branches in loader and primary actions.
- **Retained Interactions**:
  - Mode Tabs switching (委託任務 / 素材收購).
  - Task board category filters and task row selection.
  - Story Hint card visibility and details display.
  - Details panel rendering rewards, condition check list, and NPC dialog feedback.
  - Simulation of reporting quest (UIAction Log recording).
- **Validation**: PASS. Contains no forbidden keywords. Syntax is correct.
- **Visual Skinning Readiness**: Ready.

---

## 2. Inn Screen (`inn_skinning_lab`)

- **Source -> Lab**: `07_gui_prototype/inn_screen/` -> `08_experiments/mockup_to_html/inn_skinning_lab/`
- **Fixture Scenarios**:
  - `default`: Default Inn (`inn-default.json`)
- **Extraction Adjustments**:
  - Removed ESM `import` of `runtimeClient`.
  - Removed `loadLiveScreen`, `loadStaticFallback`, and `handleBackToTown` functions.
  - Intercepted back button click listener to only log the action.
  - Stripped `runtimeClient.isLiveMode()` checks and live rest action dispatching.
- **Retained Interactions**:
  -rumor list rendering.
  - JRPG dialogue selection flow (Y/N key listener, Yes/No buttons).
  - Stepper rest confirmation dialogues with NPC Lily.
  - Rest recovery animation simulation (front-end resource bar回滿 representation).
  - UIAction Log recording of rest event.
- **Validation**: PASS. Contains no forbidden keywords. Syntax is correct.
- **Visual Skinning Readiness**: Ready.

---

## 3. Workshop Screen (`workshop_skinning_lab`)

- **Source -> Lab**: `07_gui_prototype/workshop_screen/` -> `08_experiments/mockup_to_html/workshop_skinning_lab/`
- **Fixture Scenarios**:
  - `default`: Default Forge (`workshop-default.json`)
  - `constrained`: Constrained Forge (`workshop-constrained.json`)
- **Extraction Adjustments**:
  - Removed ESM `import` of `runtimeClient`.
  - Removed `loadLiveScreen` and `loadStaticFallback` functions.
  - Intercepted back button click listener to log only.
  - Stripped `runtimeClient.isLiveMode()` checks and live branches in `handlePrimaryAction()`.
- **Retained Interactions**:
  - Category tabs switching (Weapon, Armor, Upgrade, Owned).
  - Dynamic NPC theme switcher (葛雷/布琳 custom dialogues and layouts).
  - Requirements checks (materials quantity, gold cost, job compatibility, base item checks).
  - Buy, Upgrade, and Equip action logging.
- **Validation**: PASS. Contains no forbidden keywords. Syntax is correct.
- **Visual Skinning Readiness**: Ready.

---

## 4. Magic Shop Screen (`magic_shop_skinning_lab`)

- **Source -> Lab**: `07_gui_prototype/magic_shop_screen/` -> `08_experiments/mockup_to_html/magic_shop_skinning_lab/`
- **Fixture Scenarios**:
  - `default`: Default Magic Shop (`magic-shop-default.json`)
  - `constrained`: Constrained Magic Shop (`magic-shop-constrained.json`)
  - `discount`: Discount Magic Shop (`magic-shop-discount.json`)
  - `learned`: Learned Magic Shop (`magic-shop-learned.json`)
- **Extraction Adjustments**:
  - Removed ESM `import` of `runtimeClient`.
  - Removed `loadLiveScreen`, `loadStaticFallback`, and `handleBackToTown` functions.
  - Intercepted back button click listener to log only.
  - Stripped `runtimeClient.isLiveMode()` checks and live learn branches in `executeLearnAction()`.
- **Retained Interactions**:
  - Spellbook category tabs and rows listing.
  - Details panel rendering requirements, pricing, and NPC guidance dialogue.
  - Learn magic book action logging.
- **Validation**: PASS. Contains no forbidden keywords. Syntax is correct.
- **Visual Skinning Readiness**: Ready.

---

## 5. Synthesis Screen (`synthesis_skinning_lab`)

- **Source -> Lab**: `07_gui_prototype/synthesis_screen/` -> `08_experiments/mockup_to_html/synthesis_skinning_lab/`
- **Fixture Scenarios**:
  - `default`: Default Synthesis (`synthesis-default.json`)
  - `constrained`: Constrained Synthesis (`synthesis-constrained.json`)
- **Extraction Adjustments**:
  - Removed ESM `import` of `runtimeClient`.
  - Removed `loadLiveScreen`, `loadStaticFallback`, and `dispatchRuntimeAction` functions.
  - Intercepted back button click listener to log only.
  - Stripped `runtimeClient.isLiveMode()` checks and live alchemical branches in `activatePrimaryAction()`.
- **Retained Interactions**:
  - Alchemical category tabs and recipe rows listing.
  - Output summary pills display.
  - Requirement details rendering and craft action logging.
- **Validation**: PASS. Contains no forbidden keywords. Syntax is correct.
- **Visual Skinning Readiness**: Ready.

---

## 6. Storage Screen (`storage_skinning_lab`)

- **Source -> Lab**: `07_gui_prototype/storage_screen/` -> `08_experiments/mockup_to_html/storage_skinning_lab/`
- **Fixture Scenarios**:
  - `locked`: Locked Storage (`storage-locked.json`)
  - `empty`: Empty Storage (`storage-empty.json`)
  - `filled`: Filled Storage (`storage-filled.json`)
  - `blocked`: Blocked Storage (`storage-blocked.json`)
- **Extraction Adjustments**:
  - Removed ESM `import` of `runtimeClient`.
  - Removed `loadLiveScreen`, `loadStaticFallback`, `handleBackToTown`, `handleLiveTransferAction`, and `handleLivePrimaryAction` functions.
  - Intercepted back button click listener to log only.
  - Stripped `runtimeClient.isLiveMode()` checks.
- **Retained Interactions**:
  - Backpack list and storage slots list (renders exactly 10 JRPG-style rows, showing empty/locked placeholders).
  - Transfer details card (deposit/withdraw directions and metadata).
  - Stepper controls (+/- adjustment, max button, bounds constraint).
  - Unlock warehouse and Transfer confirmation simulation logging.
- **Validation**: PASS. Contains no forbidden keywords. Syntax is correct.
- **Visual Skinning Readiness**: Ready.

---

## 7. Temple Screen (`temple_skinning_lab`)

- **Source -> Lab**: `07_gui_prototype/temple_screen/` -> `08_experiments/mockup_to_html/temple_skinning_lab/`
- **Fixture Scenarios**:
  - `default`: Default Temple (`temple-default.json`)
- **Extraction Adjustments**:
  - Removed ESM `import` of `runtimeClient`.
  - Removed `loadLiveScreen`, `loadStaticFallback`, and `handleBackToTown` functions.
  - Intercepted back button click listener to log only.
  - Stripped `runtimeClient.isLiveMode()` checks and live branches in `handlePray()` and `handleInquiry()`.
- **Retained Interactions**:
  - Promotions list and requirements checked list.
  - Moon well pray button and feedback display.
  - Inquiries selection and priestess Sian's dialogue bubble updates.
  - Promotions modal opening and backdrop closing.
- **Validation**: PASS. Contains no forbidden keywords. Syntax is correct.
- **Visual Skinning Readiness**: Ready.

---

## 8. Relic Preview Screen (`relic_preview_skinning_lab`)

- **Source -> Lab**: `07_gui_prototype/relic_preview_screen/` -> `08_experiments/mockup_to_html/relic_preview_skinning_lab/`
- **Fixture Scenarios**:
  - `default`: Default Relic preview (`relic-preview-default.json`)
- **Extraction Adjustments**:
  - Removed ESM `import` of `runtimeClient`.
  - Removed `loadLiveScreen`, `loadStaticFallback`, and `handleBackToTown` functions.
  - Intercepted back button click listener to log only.
  - Stripped `runtimeClient.isLiveMode()` checks and live attune branches in `handleAttune()`.
- **Retained Interactions**:
  - Relic slots listing with element icons.
  - Focus relic translation texts and attune status buttons.
  - Orb visual state animation trigger.
  - Attunement simulation logging.
- **Validation**: PASS. Contains no forbidden keywords. Syntax is correct.
- **Visual Skinning Readiness**: Ready.

---

## Next Steps Recommendation

All 8 extracted labs are fully functional fixture-only mockups and contain zero runtime dependencies.
The following labs are best suited to prioritize for visual skinning:
1. **Temple Screen (`temple_skinning_lab`)**: Has the strongest existing full-screen visual composition, making it a great candidate for applying obsidian dark and gold themes.
2. **Storage Screen (`storage_skinning_lab`)**: The transfer stepper and grid lists are excellent candidates for responsive visual spacing QA.
