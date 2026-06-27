# GUI Bridge Vertical Slice Contract Audit v1

狀態：docs-only contract audit。此文件不是 implementation status，也不是 runtime bridge 施工批准。

目的：把既有 GUI runtime bridge 雛形整理成一條可被批准的最小 vertical slice，避免後續 bridge 擴張時把 static prototype、mockup/reference、CLI runtime 與 live bridge 的責任混在一起。

本文件只固定 contract-level / interaction-level 規格，不固定 pixel layout、設計系統或 UI polish。

---

## 1. Boundary

本 audit 的 blessed vertical slice 只包含：

```text
start_screen
-> start_new_game / restart_game / load_demo_seed / load_game
-> town_hub
-> open_world_map
-> world_map
-> save_game
-> back_to_town_hub
-> town_hub
-> inn_screen
-> rest_at_inn
-> inn_screen or town_hub returned ScreenModel
```

明確排除在正式 bridge contract 外：

- Guild
- Shop
- Workshop
- Synthesis
- Storage
- Magic Shop
- Temple
- Relic Preview
- Dungeon Exploration
- Combat

目前 repo 內已存在 Dungeon / Combat live bridge 雛形，但在本 audit 中標記為 experimental / off-contract。後續若要讓 Dungeon / Combat 成為正式 live slice，需另開 read-only planning gate。

---

## 2. Current Bridge Inventory

目前 live bridge 雛形分成三層：

| Layer | Path | Current responsibility |
|---|---|---|
| Bridge server | `06_tools/gui_runtime_bridge.py` | 提供 local HTTP server、static prototype file serving、`/api/*` bridge endpoints |
| Runtime adapter | `03_engine/engine/gui_actions.py` | 維護 in-memory `GuiRuntimeSession`，把 GUI action dispatch 到 Python runtime helper |
| Frontend client | `07_gui_prototype/shared/runtime-client.js` | 在 `?mode=live` 下呼叫 bridge API，static mode 維持 fixtures |

目前 bridge API 雛形：

| Endpoint | Contract role |
|---|---|
| `GET /api/session` | 回傳 bridge health、save 狀態、目前 state summary |
| `POST /api/session/new` | 建立 in-memory runtime state |
| `POST /api/session/load` | 透過 runtime `load_game()` 載入既有 save |
| `POST /api/session/demo-seed` | 建立 dev-only demo seed state，不應視為正式 gameplay action |
| `POST /api/save` | 透過 runtime `save_game()` 寫入 save |
| `GET /api/screen/<screen_id>` | 回傳目前 live ScreenModel |
| `POST /api/action` | 派送白名單 UIAction 並回傳 result / ScreenModel / navigation outcome |

這份 inventory 只描述現有行為能力，不等同於 code review，也不代表所有已存在 live behavior 都進入正式 contract。

---

## 3. Blessed Screen Contract

ScreenModel base fields：

```text
screen_id
layout_family
title
subtitle
resource_strip or player_summary
actions / menu_actions / navigation_actions
selected_* when applicable
feedback_message or message when applicable
```

`layout_family` 是 bridge contract 的語意分類，不是 CSS class，不要求 static prototype 立刻已有同名欄位。

| screen_id | layout_family | Required fields | Optional fields | Navigation outcome |
|---|---|---|---|---|
| `start_screen` | `entry` | `screen_id`, `title`, `actions`, `registration` | `hero_kicker`, `hero_title`, `hero_copy`, `screen_label` | successful start/load -> `town_hub` |
| `town_hub` | `hub` | `screen_id`, `title`, `resource_strip`, `facility_nodes`, `navigation_actions` | `town_guidance`, `selected_facility_id`, `badges` | `open_world_map` -> `world_map`; `rest_at_inn` may return `town_hub` or route to `inn_screen` depending client flow |
| `world_map` | `navigation_map` | `screen_id`, `title`, `player`, `menu_actions`, `locations` | `selected_location_id`, `current_location_id`, `route_segments` | `back_to_town_hub` -> `town_hub`; `save_game` same screen unless response chooses otherwise |
| `inn_screen` | `dialogue_node` | `screen_id`, `title`, `resource_strip`, `service` | `npc`, `rumors`, `feedback_message` | `rest_at_inn` returns updated `inn_screen` or `town_hub` ScreenModel |

Runtime remains the gameplay authority. Static fixture `enabled` flags may guide rendering, but every live action must be validated by Python runtime at dispatch time.

---

## 4. Blessed UIAction Contract

Canonical blessed action list:

| action_id | Payload schema | Success response | Blocked/error response | Screen behavior |
|---|---|---|---|---|
| `start_new_game` | `{ name: string, job_id: string }` | creates in-memory state, returns `town_hub` model / route | invalid job -> error | next screen |
| `restart_game` | `{ name: string, job_id: string }` | same runtime behavior as new game, action id preserved | invalid job -> error | next screen |
| `load_demo_seed` | `{}` | creates in-memory dev seed, returns `town_hub` | adapter error -> error | next screen |
| `load_game` | `{}` | loads existing runtime save, returns `town_hub` | no valid save -> blocked/error | next screen |
| `save_game` | `{}` | writes via runtime `save_game()`, returns state summary and current/specified screen model | no loaded state -> blocked/error | same screen |
| `open_world_map` | `{}` | returns `world_map` model / route | no loaded state -> blocked/error | next screen |
| `back_to_town_hub` | `{}` or `{ from: string }` | clears active live run and returns `town_hub` model / route | no loaded state -> blocked/error | next screen |
| `rest_at_inn` | `{ service_id: "overnight_rest", cost: 30 }` | deducts 30G, restores HP/MP, returns updated model | unknown service, cost mismatch, insufficient gold -> blocked/error | same screen or returned screen |

Notes:

- `load_demo_seed` is dev-only bridge support. It is useful for browser smoke tests but is not formal gameplay.
- `rest_at_inn` is the bridge canonical action name. Older CLI wording such as `rest_inn` is a runtime function/menu reference, not the bridge action id.
- `back_to_town_hub` is the canonical Town Hub return action for this blessed slice. Similar names such as `return_to_town_hub` remain future normalization work.

---

## 5. Bridge Response Contract

Successful response minimum shape:

```text
ok: true
action_id
message
state_summary
screen_model
next_route or next_screen_id
```

Blocked/error response minimum shape:

```text
ok: false
error
```

Recommended future-compatible fields:

```text
status: success | blocked | error
blocked_reason
next_screen_id
```

Current implementation primarily uses HTTP status plus `{ ok: false, error }`. That is acceptable for the current blessed slice, but any future contract expansion should avoid requiring frontend code to infer gameplay legality from static fixtures.

---

## 6. Prototype-Only And Non-Contract Inputs

Mockup/reference images:

- may be used for GUI imagination, prototype generation reference, operation feel exploration, and UX gap discovery;
- may suggest container needs such as modal, drawer, popover, tab, detail panel, feedback region, or blocked state;
- must not become runtime assets;
- must not become gameplay authority;
- must not directly define bridge payloads or runtime rules.

Static prototype fixtures:

- may be used as ScreenModel shape reference;
- may validate render layer, layout, interaction, navigation feel, and UIAction logging;
- must not be treated as gameplay SSOT.

Explicitly excluded from bridge contract:

- button size
- card width/height
- grid ratio
- three-column ratio
- portrait exact position
- hover animation
- color palette
- letter spacing
- background image
- mockup layer position
- CSS-only layout details

Inn static mode currently includes frontend HP/MP/gold rest simulation. For bridge purposes, that behavior is UX preview only. Live mode must rely on runtime response from `rest_at_inn`; GUI must not independently deduct gold, restore HP/MP, or decide legality.

---

## 7. Normalization Gaps

These are known contract gaps or future cleanup items. They are not approved implementation tasks in this audit.

| Gap | Impact | v1 decision |
|---|---|---|
| `workshop_screen` fixtures currently lack `screen_id` | Contract shape drift for a future facility slice | Record only; Workshop is outside blessed slice |
| `back_to_town_hub` and `return_to_town_hub` both appear in prototype/action vocabulary | Future route/action ambiguity | Use `back_to_town_hub` for blessed slice |
| CLI/runtime function naming such as `rest_inn` differs from bridge action `rest_at_inn` | Potential action naming drift | Use `rest_at_inn` as bridge canonical |
| `load_demo_seed` exists in live bridge | Could be mistaken for formal gameplay | Mark dev-only |
| Dungeon / Combat live bridge code exists | High-risk stateful gameplay surface | Mark experimental/off-contract |
| `layout_family` is not yet emitted in all ScreenModels | Useful contract field absent from current models | Treat as contract audit recommendation, not required before docs approval |

---

## 8. Acceptance Scenarios

These scenarios define what the blessed vertical slice must prove before broader bridge work.

1. Start new game
   - User submits name and job from Start Screen.
   - Runtime creates an in-memory state through Python.
   - Response returns `town_hub` ScreenModel or route.

2. Demo seed
   - User loads demo seed.
   - Runtime creates an in-memory test state.
   - `save.json` is not written by this action.
   - Response returns `town_hub` ScreenModel or route.

3. Load save
   - If a valid save exists, runtime loads it and returns `town_hub`.
   - If no valid save exists, bridge returns blocked/error.

4. Save game
   - User dispatches `save_game`.
   - Bridge calls Python runtime save behavior.
   - GUI does not manually read or write `save.json`.

5. Inn rest success
   - State has at least 30G.
   - User dispatches `rest_at_inn` with `{ service_id: "overnight_rest", cost: 30 }`.
   - Runtime deducts 30G and restores HP/MP to current max.
   - Response returns updated `state_summary` and ScreenModel.

6. Inn rest blocked
   - State has less than 30G.
   - Runtime rejects `rest_at_inn`.
   - GUI displays blocked/error result.
   - GUI does not deduct gold or restore HP/MP locally.

---

## 9. Next Gate

After this audit is accepted, the next implementation slice should be limited to contract-gap cleanup for the blessed slice only.

Allowed next implementation category, if separately approved:

- make blessed slice response shape more explicit;
- add or normalize `layout_family` for blessed live ScreenModels;
- align Start / Town Hub / World Map / Inn live-mode rendering with returned ScreenModel shape;
- add bridge smoke checks for the blessed acceptance scenarios.

Still requires separate planning gate:

- Dungeon / Combat live bridge promotion from experimental to contract;
- Shop / Workshop / Synthesis / Storage / Magic Shop live mutations;
- Guild quest turn-in, material selling, or story flag mutations;
- Temple story actions or Relic gameplay effects;
- save schema, data schema, combat formula, economy, or runtime refactor work.

