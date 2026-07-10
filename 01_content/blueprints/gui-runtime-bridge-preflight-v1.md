# GUI Runtime Bridge Preflight V1

Purpose: short preflight gate for an explicitly approved runtime-connected GUI
slice. This is not a static GUI task checklist. The former detailed endpoint,
action, and first-slice record is archived at
`../archive/gui-runtime-bridge-preflight-v1.md`.

## Required Before Implementation

- Read `01_content/gui-runtime-bridge-plan-v1.md`.
- Confirm explicit approval for the exact runtime-connected slice.
- Name the screen, UIActions, runtime functions, files, server entry point, and
  validation commands.
- Confirm that Python remains gameplay authority and JavaScript remains a
  dispatcher / renderer.
- Confirm that `save.json` is accessed only through existing runtime behavior.

## Scope Gate

Allowed only when named in the approval:

- local bridge server or smoke helper under `06_tools/`;
- small runtime adapter work under `03_engine/engine/`;
- live-mode client or render integration under `07_gui_prototype/`.

Do not expand into new gameplay systems, schema, data, save migration, combat
formula, or generic inventory/equipment work.

## Validation Gate

- Use the approved bridge server and confirm it is alive before navigating.
- Validate only the named screen and one narrow happy / blocked path where useful.
- Keep static fixture fallback intact.
- Stop after the first server or Browser failure and report before retrying.
- Close the server and clean up the process after validation.

## History

For the former first-slice endpoint and action contract, read only when historical
bridge context is specifically required:

`../archive/gui-runtime-bridge-preflight-v1.md`
