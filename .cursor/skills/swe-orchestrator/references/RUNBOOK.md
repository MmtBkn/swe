# SWE Orchestrator Runbook (Cursor)

This file is the **single source of truth** for Cursor SWE orchestration behavior.

All of the following should **only reference this runbook** (do not duplicate workflow logic elsewhere):

- Skill: `swe-orchestrator`
- Subagent: `swe-flow-orchestrator`
- Runner subagents: `swe-context-builder`, `swe-prd-runner`, `swe-spec-runner`, `swe-tdd-runner`, `swe-exec-runner`

## Orchestration requirements

- Orchestration must run via the `swe-flow-orchestrator` subagent (its model is configured in `.cursor/agents/swe-flow-orchestrator.md`).
- If the request is classified as **small**, implementation must be performed by `swe-flow-orchestrator`. Do **not** run `swe-exec-runner` for small requests.

## Canonical instructions live in SWE skill files

For each step, the canonical how-to instructions live in the corresponding SWE skill’s `SKILL.md`:

- `swe-init`
- `swe-prd`
- `swe-spec`
- `swe-tdd`
- `swe-exec`

Runner subagents must **read the relevant `SKILL.md` and follow it** (no re-implementation of those instructions in subagent prompts).

### Where to find the skill `SKILL.md` files

Prefer the first match that exists:

1. `.cursor/skills/<skill-name>/SKILL.md`
2. `.agents/skills/<skill-name>/SKILL.md`
3. `.codex/skills/<skill-name>/SKILL.md`
4. `~/.cursor/skills/<skill-name>/SKILL.md`
5. `~/.codex/skills/<skill-name>/SKILL.md`

If none exist for a required skill, stop and report the missing paths (do not guess).

## Global orchestration rules (non-negotiable)

- If `.swe/context/` exists and is non-empty: **do not recreate, refresh, or rewrite it**. Use it as-is.
- Never invent facts. Missing detail becomes **Open Questions** and/or explicitly labeled **Assumptions**.
- Always report the concrete file paths created/updated so downstream steps can reference them.

## Step 0: classify the request

### Small request (single-story) criteria

Treat the request as **small** when all are true:

- Clear, concrete ask (no major open questions).
- Likely ≤ 1 story (no multi-epic breakdown needed).
- No schema migrations / major API surface area changes / multi-service rollout.
- Low coordination risk (no cross-cutting auth/billing/compliance redesign).

If unclear, ask the user to choose: small one-story change vs full feature workflow.

### Small request flow (standalone story + implement now)

When the request is small:

1. Create a standalone story folder under `.swe/stories/one-off/`.
2. Create `.swe/stories/one-off/001-<story-slug>.md` with:
   - Goal / Non-goals
   - Acceptance criteria (testable)
   - Validation steps (commands/tests to run)
3. Implement the ask immediately using the `swe-flow-orchestrator` subagent.
4. Run the smallest validating command(s) available.
5. Rename the story file to `001-<story-slug>-done.md` after validation and note results in `.swe/stories/<oneoff-slug>/.next.md`.

Do **not** run: PRD, spec, TDD, or exec flows for this path.

## Full feature workflow (PRD → spec+tdd parallel → exec)

### 1) Context (conditional)

- If `.swe/context/` exists and is non-empty: skip (read-only).
- If `.swe/context/` does not exist: delegate to `swe-context-builder`.

### 2) PRD

- Delegate to `swe-prd-runner` and wait for a PRD under `.swe/proposals/PROPOSAL-00X-*.md`.
- Capture the PRD path; it is the source of truth for the next steps.

### 3) Spec + TDD (parallel)

- Launch `swe-spec-runner` and `swe-tdd-runner` in parallel with the same PRD path.
- IMPORTANT constraint: `swe-spec-runner` must **skip any step** that produces a Test Spec (`.swe/specs/TST-*.md`). Test Spec ownership belongs to `swe-tdd-runner`.
- Reconcile mismatches (slug, scope, acceptance criteria, rollout/testing) before coding.

### 4) Execution (gated)

- Ask the user for an explicit go/no-go to implement.
- Delegate to `swe-exec-runner` with the story folder path and constraints.

## Role playbooks (for subagents)

### Role: `swe-flow-orchestrator`

- Read this runbook and execute either the small-request flow or the full feature workflow.
- Delegate to runner subagents as needed.
- Return a concise summary with concrete file paths.

### Role: `swe-context-builder`

- Read the canonical `swe-init` skill `SKILL.md` (using the location order above).
- Follow it exactly.
- Return the file paths created/updated + a short TL;DR + open questions.

### Role: `swe-prd-runner`

- Read the canonical `swe-prd` skill `SKILL.md` (using the location order above).
- Follow it exactly.
- Return the PRD path + short summary + open questions.

### Role: `swe-spec-runner`

- Read the canonical `swe-spec` skill `SKILL.md` (using the location order above).
- Follow it exactly **except**: do not generate `.swe/specs/TST-*.md` (see constraint above).
- Return the tech spec/epic/story paths + top risks + open questions.

### Role: `swe-tdd-runner`

- Read the canonical `swe-tdd` skill `SKILL.md` (using the location order above).
- Follow it exactly.
- Return the test spec path + coverage summary + PRD gaps.

### Role: `swe-exec-runner`

- Read the canonical `swe-exec` skill `SKILL.md` (using the location order above).
- Follow it exactly.
- Return what changed + what was validated + what’s next.
