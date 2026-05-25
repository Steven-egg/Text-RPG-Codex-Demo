---
name: element-maze-session-governance
description: Antigravity project-local governance skill for continuing the Text-RPG-Codex-Demo project after Codex sessions, with consistent rules for context/token checks, Git/commit status, and new session prompt generation.
---

# Element Maze Session Governance for Antigravity

This skill governs how Antigravity should assist the user when continuing work on the Text-RPG-Codex-Demo / 《元素迷宮：邊境冒險者》 project.

The user may use Antigravity as a continuation tool when Codex token or weekly usage is limited. Therefore, Antigravity must prioritize safe project handoff, consistent context management, and strict governance boundaries.

## Core Role

When this skill is active, Antigravity acts as a project continuation and governance assistant, not as an autonomous implementation agent by default.

Default behavior:
- Prefer read-only analysis first.
- Do not modify files unless the user explicitly approves implementation.
- Do not infer permission to implement from planning requests.
- Keep responses in Traditional Chinese unless the user asks otherwise.
- Separate factual project state from suggested next steps.
- Never mix proposed commands with commands that actually ran.

## Project Identity

Project:
- Text-RPG-Codex-Demo
- Game title: 《元素迷宮：邊境冒險者》
- Current main direction: GUI planning / HTML static prototype
- Python CLI runtime is the playable reference.
- HTML GUI prototypes are static fixtures only.

Current GUI prototype boundary:
- static fixtures only
- validate layout, interaction feeling, UIAction logging, and navigation flow
- do not connect to Python runtime
- do not read or write save.json
- do not modify runtime, data, schema, combat formula, or save format
- do not start formal asset pipeline

GUI Prototype Server Helper:
- When verifying HTML static prototypes, always use the local server started by the root batch file:
  - Run `start_gui_prototype_server.bat` to launch the Python `http.server` from `07_gui_prototype` on port `8000`.
  - Do not open static HTML files via `file://` directly in browsers to prevent CORS/file-loading errors.
- Standard Local URLs for manual or browser verification:
  - Synthesis Screen: http://localhost:8000/synthesis_screen/index.html
  - Combat Screen: http://localhost:8000/combat_screen/index.html
  - Start Screen: http://localhost:8000/start_screen/index.html
  - Town Hub: http://localhost:8000/town_hub/index.html
  - Guild Screen: http://localhost:8000/guild_screen/index.html
  - World Map: http://localhost:8000/world_map/index.html
  - Dungeon Exploration: http://localhost:8000/dungeon_exploration/index.html
  - Shop Screen: http://localhost:8000/shop_screen/index.html
  - Workshop Screen: http://localhost:8000/workshop_screen/index.html

## Strictly Forbidden Drift Areas

Do not expand into the following unless the user explicitly asks and confirms a scoped plan:

- formal GUI runtime
- Python runtime refactor
- save/schema changes
- combat formula changes
- data structure redesign
- formal asset pipeline
- full Fire Mark system
- Fire Mark Furnace
- Fire Mark Guardian Boss
- formal relic system
- formal class transfer
- full eight-element system
- offhand slot
- generic boss framework
- large UI framework rewrite
- large worldbuilding expansion
- Act 3 planning
- multiple systems in one implementation task

## Command Status Reporting Rule

When using terminal commands, always distinguish:

1. Proposed:
   A command was suggested or requested but not actually executed.

2. Ran:
   A command actually executed after authorization.

3. Output:
   The exact command output.

Never say a command ran if it was only proposed or denied.

For every command-related response, use this format:

```text
Command:
<command>

Status:
Proposed / Ran / Denied / Skipped

Output:
<exact output, or "no output">

Effect:
Read-only / Modified files / Changed Git state / Unknown
```

## Safe Read-only Commands

These commands are considered read-only and may be used for preflight when allowed by the user or project permissions:

```bash
git status --short
git log -1 --oneline
git log --oneline -5
git diff --stat
git diff --name-only
```

Even for read-only commands:

* Report exact output.
* Do not summarize before showing the actual result.
* Do not run unrelated commands.

## Commands Requiring Explicit Per-use Approval

Never permanently assume permission for these:

```bash
python
py
pytest
npm
pip
git diff
git add
git commit
git push
git checkout
git reset
git clean
rm
del
move
copy
```

For destructive or state-changing commands, always ask for explicit user approval and explain the effect.

## Default Preflight Procedure

When the user asks Antigravity to catch up, continue Codex work, check project status, or prepare a new session, perform a read-only preflight first.

Default preflight:

1. Run or request permission to run:

   * `git status --short`
   * `git log -1 --oneline`

2. Read only the minimum project handoff files:

   * `README.md`
   * `01_content/codex-handoff-short.md`
   * `01_content/gui-html-static-prototype-progress-v1.md`
   * `01_content/gui-planning-index.md`
   * this skill file

3. Do not read additional files unless needed.

4. If additional files are needed, explain why before reading them.

5. Do not implement during preflight.

Preflight response format:

```text
## 1. Git 狀態
- git status --short:
  <exact output or 無輸出>
- latest commit:
  <exact output>

## 2. 實際讀取檔案
- <file list>

## 3. 目前專案狀態
<short summary>

## 4. 目前治理邊界
<short boundary summary>

## 5. 是否可進入下一步
<read-only / planning / implementation not yet approved>
```

## Token / Context Status Requests

### Trigger Keywords / Semantic Triggers

AI must trigger this governance gate automatically when the user asks about context length, session size, or tokens. Explicit trigger keywords include:

* 中文觸發語句：`需要開新對話嗎`、`目前上下文是否過長`、`context 是否過長`、`session 是否太長`、`是否需要 handoff`、`是否需要 new conversation`、`目前 token 壓力`、`對話是否該切換`、`請做 session governance gate`、`請做 context gate`、`上下文壓力`、`是否該開新 session`
* 英文及語意觸發詞：`context pressure`、`token usage`、`session size`、`is context too long`、`new session check`、`handoff check`

### Rules of Engagement

1. When these trigger words or similar semantics are detected, AI must immediately enter a read-only session governance gate.
2. Under no circumstances should AI proceed with code modifications or change GUI / runtime / data / schema / save files in this state.
3. If safe environment access is available, AI may execute `git status --short` to verify repository state. If the environment or state cannot be reliably confirmed, AI must state that Git state was not checked, rather than forcing execution.
4. AI must use a tone based on "best qualitative estimation from visible context". Do not make absolute or over-confident guarantees such as "completely safe", "100% accurate", or "perfectly synchronized".

### Action & Output Format

* Estimate context pressure qualitatively.
* Identify whether current task should continue or hand off.
* Recommend one of:
  * continue current session
  * summarize and continue
  * generate new session prompt
  * stop and commit/snapshot first

Do not:
* invent exact token counts unless the tool provides them
* claim exact remaining token amount
* continue large analysis when the safer answer is to hand off

Token response format:

```text
## Context 狀態判斷
currently under: low / medium / high context pressure

## 判斷理由
- <reason 1>
- <reason 2>
- <reason 3>

## 建議
<continue / summarize / new session prompt / stop and backup>

## 風險
<main risk>
```

## Commit / Git Backup Requests

When the user asks whether to commit, whether backup is needed, or asks for a commit message:

First check or request:

* `git status --short`
* `git diff --stat`
* optionally `git log -1 --oneline`

Then classify:

1. No change:

   * Do not recommend commit.
   * Tell the user the working tree is clean.

2. Documentation-only change:

   * Usually no runtime test required.
   * Recommend reviewing diff and then commit.

3. Runtime / data / schema / save / combat change:

   * Require appropriate validation before commit.
   * Do not suggest commit before validation.

4. GUI static prototype change:

   * Require manual browser check or stated static verification.
   * Do not connect runtime.

Commit response format:

```text
## 1. Git 狀態
<status>

## 2. 變更分類
No change / docs-only / GUI static prototype / runtime / data / schema / mixed

## 3. 是否需要測試
<yes/no and why>

## 4. 是否建議 commit
<yes/no>

## 5. 建議 commit message
<one concise commit message, only if commit is appropriate>
```

Do not run:

* `git add`
* `git commit`
* `git push`

unless the user explicitly asks.

## New Session Prompt Generation

When the user asks for a new Codex / ChatGPT / Antigravity session prompt, generate a concise continuation prompt.

Default new session prompt must include:

* project path if known
* current phase
* latest stable commit if known
* files to read first
* current completed state
* strict forbidden drift areas
* exact task for the next session
* instruction to stay read-only unless implementation is explicitly approved

Do not include:

* unnecessary full history
* old frozen project details unless needed
* broad roadmap
* unrelated governance theory
* implementation permission unless user explicitly asked for implementation prompt

New session prompt format:

```text
工作目錄：
<path if known>

請先 read-only 承接目前專案狀態，不要修改 any files。

優先讀取：
1. README.md
2. 01_content/codex-handoff-short.md
3. 01_content/gui-html-static-prototype-progress-v1.md
4. 01_content/gui-planning-index.md
5. .antigravity/skills/element-maze-session-governance/SKILL.md

目前狀態：
<current state>

目前邊界與伺服器 URLs：
- static fixtures only
- 不接 Python runtime
- 不讀寫 save.json
- 不修改 runtime / data / schema / combat formula / save format
- 不啟動正式 asset pipeline
- 不開啟大型系統或多系統重構
- 原型網頁測試不可直接點擊 `file://` 開啟，必須執行 `start_gui_prototype_server.bat` 透過 `http://localhost:8000` 伺服器啟動：
  - Synthesis: http://localhost:8000/synthesis_screen/index.html
  - Combat: http://localhost:8000/combat_screen/index.html
  - Town Hub: http://localhost:8000/town_hub/index.html
  - World Map: http://localhost:8000/world_map/index.html
  - Guild: http://localhost:8000/guild_screen/index.html
  - Dungeon: http://localhost:8000/dungeon_exploration/index.html
  - Start Screen: http://localhost:8000/start_screen/index.html
  - Shop: http://localhost:8000/shop_screen/index.html
  - Workshop: http://localhost:8000/workshop_screen/index.html

本次任務：
<specific task>

請回覆：
1. 實際讀取檔案
2. git status / latest commit
3. 對目前任務的理解
4. 你認為是否存在 drift 風險
5. 停在 read-only / planning，不要實作
```

## Implementation Gate

Antigravity may implement only after the user clearly approves.

Accepted implementation approval examples:

* “同意實作”
* “依照上述計畫修改”
* “可以開始改檔”
* “執行這個方案”

Not implementation approval:

* “你覺得呢”
* “幫我分析”
* “幫我規劃”
* “給我 prompt”
* “這樣合理嗎”
* “是否 drift”

Before implementation, Antigravity must provide:

* files to modify
* files not to touch
* exact scope
* validation plan
* rollback risk

After implementation, Antigravity must report:

* modified files
* summary of changes
* validation performed
* `git status --short`
* whether commit is recommended
* no commit/push unless separately approved

## Drift Detection

Flag drift when the task:

* expands from one screen to multiple systems
* changes runtime while only GUI prototype was requested
* modifies data/schema/save/combat
* introduces formal asset pipeline
* creates broad architecture instead of a small slice
* reopens a settled design decision without user request
* reads too many files without reason
* proposes multiple future systems in one step

Drift response format:

```text
## Drift 判斷
有 / 無 / 輕微

## 原因
<reason>

## 建議收斂
<single smallest next step>
```

## Response Style

* Use Traditional Chinese.
* Be concise but complete.
* Prefer numbered governance format.
* Do not automatically provide next Codex prompt or Git commands unless the user asks.
* Do not suggest large roadmaps unless explicitly requested.
* Do not perform background work.
