# AGENTS.md

Shared entry point for agents working in this repository. Read live files
relevant to the task; this file is not a project-status record. Use Traditional
Chinese unless the user asks otherwise.

## Autonomy and safety

- Make routine technical decisions from repository conventions, tests, prior
  implementations, and authoritative documentation. Do not ask the user to
  decide what can be reasonably inferred.
- Proceed autonomously with scoped, reversible, and verifiable local work.
  Preserve unrelated changes; run fitting non-destructive checks; reassess if
  evidence contradicts the approach or scope expands materially.
- Ask only when product intent, unavailable information, external
  authorization, irreversible/destructive actions, meaningful cost, security,
  or permission risk requires a decision. Recommend a default and ask for the
  minimum decision needed.
- Require explicit confirmation before production deployment, external
  messages, purchases, credential or permission changes, Git history changes,
  or destructive actions outside clearly approved targets.

## Routing and boundaries

- Start with the smallest useful reads. Treat code, tests, schemas, and live
  data as evidence; do not duplicate changing status into this file.
- Planning, review, architecture, runtime, data, schema, save, and combat work
  are read-only unless the user explicitly requests implementation.
- Do not read, write, or manually edit `save.json`; do not change runtime,
  data, schema, save, or combat behavior without explicit scoped approval.
- Current GUI work lives in `07_gui_prototype/`. Read
  `07_gui_prototype/AGENTS.md` before work there.
- Runtime-connected GUI work needs explicit approval; first read
  `01_content/gui-runtime-bridge-plan-v1.md` and stop at a read-only planning
  gate before implementation.
