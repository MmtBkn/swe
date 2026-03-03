---
name: swe-orchestrator
description: Orchestrate swe-init → swe-prd → (swe-spec + swe-tdd in parallel) → swe-exec using Cursor subagents and the SWE skills.
disable-model-invocation: true
---

# SWE Orchestrator (Cursor)

Use this skill when you want a clean, end-to-end workflow from idea → shipped code while keeping the main chat focused.

## Model requirement (important)

This workflow is intended to be orchestrated by a subagent pinned to **GPT-5.2 xhigh**.

1. Launch the `swe-flow-orchestrator` subagent in the foreground and hand it:
   - The user’s request
   - The repo/workspace path
   - Any constraints (security/compliance, timelines, do-not-touch areas)
2. If `swe-flow-orchestrator` is not available, proceed in the main agent, but you should switch the main model to **GPT-5.2 xhigh** first.

## Prerequisites

### Skills

The following skills should be available to Agent:

- `swe-init`
- `swe-prd`
- `swe-spec`
- `swe-tdd`
- `swe-exec`

Cursor discovers skills from `.agents/skills/`, `.cursor/skills/`, `~/.cursor/skills/`, and also `.codex/skills/` / `~/.codex/skills/` for compatibility.

### Subagents

This workflow expects the following custom subagents to exist (typically in `.cursor/agents/`):

- `swe-flow-orchestrator` (GPT-5.2 xhigh)
- `swe-context-builder` (GPT-5.2 high)
- `swe-prd-runner` (GPT-5.2 xhigh)
- `swe-spec-runner` (GPT-5.2 xhigh)
- `swe-tdd-runner` (GPT-5.2 xhigh)
- `swe-exec-runner` (GPT-5.3 Codex xhigh)

If any of these subagents are missing, fall back to running the corresponding `swe-*` skill in the main agent (still follow the same ordering and file conventions).

## Operating rules

- Keep the main conversation small: delegate heavy exploration/writing to subagents.
- Never invent business/system facts. Missing detail becomes **Open Questions** and/or explicitly labeled **Assumptions**.
- Always report the concrete file paths created/updated so downstream steps can be wired correctly.

## Orchestration

### 0) Resolve the feature request

If the user hasn’t provided a concrete feature, ask for:

- Title + 1–2 sentence intent
- Primary user/persona
- Constraints (security/compliance, timeline, target platforms, deployment environment)
- Any “do-not-touch” areas

### 0.1) Decide: small request vs full feature

If the user request is **small** (single localized change) you must **not** run PRD/spec/TDD/exec flows.

Treat it as **small** when all are true:

- Clear, concrete ask (no major open questions).
- Likely ≤ 1 story (no multi-epic breakdown needed).
- No schema migrations / major API surface area changes / multi-service rollout.
- Low coordination risk (no cross-cutting auth/billing/compliance redesign).

If it’s small:

1. Create a standalone story folder under `.swe/stories/<oneoff-slug>/` (derive from the ask; ensure it’s unique).
2. Create `.swe/stories/<oneoff-slug>/001-<story-slug>.md` with:
   - Goal, non-goals
   - Acceptance criteria (testable)
   - Validation steps (commands/tests to run)
3. Do **not** launch `swe-prd-runner`, `swe-spec-runner`, `swe-tdd-runner`, or `swe-exec-runner`.
4. Implement the ask immediately **using GPT-5.2 xhigh** (no PRD/spec/test-plan generation for this path).
5. Run the smallest validating command(s) available.
6. Rename the story file to `001-<story-slug>-done.md` after validation and note results in `.swe/stories/<oneoff-slug>/.next.md`.

### 1) Context (conditional)

1. Check whether `.swe/context/` exists and is non-empty.
2. If it exists, **do not recreate or refresh it**. Use it as-is.
3. If it does not exist, launch the `swe-context-builder` subagent with:
   - Company/product names (ask the user if unknown)
   - Any relevant links (docs, website, internal wikis if available)
   - The current workspace/repo path
3. When it completes, confirm these exist (or are intentionally skipped with justification):
   - `.swe/context/companies/*.md`
   - `.swe/context/products/*.md`
   - `.swe/context/user-personas.md`
   - `.swe/context/architecture.md`

### 2) PRD

1. Launch `swe-prd-runner` with the user’s feature request and constraints.
2. Wait for it to produce a PRD under `.swe/proposals/PROPOSAL-00X-*.md`.
3. Capture and repeat back the PRD path (this is the source of truth for the next steps).

### 3) Spec + TDD (parallel)

1. In a **single** message, launch **both** `swe-spec-runner` and `swe-tdd-runner` in parallel.
2. Provide both subagents the same PRD path and instruct them to:
   - Derive a consistent `<feature-slug>` from the PRD title/filename
   - Keep assumptions/open questions explicit
3. When both complete, verify expected artifacts exist:
   - Tech spec: `.swe/specs/TSD-00X-<feature-slug>.md`
   - Epics: `.swe/epics/<feature-slug>/EPIC-00X-*.md`
   - Stories: `.swe/stories/<feature-slug>/STORY-00X-*.md`
   - Test spec: `.swe/specs/TST-00X-<feature-slug>.md`
4. Reconcile any mismatches (slug, scope, acceptance criteria, rollout/testing) before coding.

### 4) Execution

1. Ask the user for an explicit go/no-go: **“Proceed to implement the stories now?”**
2. Launch `swe-exec-runner` with:
   - The story folder path `.swe/stories/<feature-slug>/`
   - Any constraints (release strategy, flags, do-not-touch)
3. Ensure it:
   - Implements stories sequentially
   - Maintains `.swe/stories/<feature-slug>/.next.md`
   - Runs the smallest validating command(s) per story
   - Renames completed artifacts with `-done` only after verification

### 5) Finalization

- Ensure all stories are implemented and verified against the test spec.
- Summarize what changed, how to verify, and what remains (if anything).
