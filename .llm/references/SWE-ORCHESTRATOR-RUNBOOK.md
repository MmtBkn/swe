# SWE Orchestrator Runbook

This file is the single source of truth for SWE orchestration behavior across provider-specific wrappers.

All provider-specific entrypoints should reference this runbook instead of duplicating it:

- Cursor skill wrapper: `.cursor/skills/swe-orchestrator/`
- Cursor subagents: `.cursor/agents/`
- Claude command wrapper: `.claude/commands/swe-orchestrator.md`
- Claude subagents: `.claude/agents/`

## Canonical skill instructions

For every workflow step, the canonical how-to instructions live in the base skill files:

- `bug-fix`
- `swe-init`
- `swe-prd`
- `swe-spec`
- `swe-tdd`
- `swe-exec`
- `swe-gtm-video`

Use `.llm/references/SKILL-PROXY-RULES.md` to resolve those skill files. Do not restate their workflows in provider wrappers.

## Global orchestration rules

- If `.swe/context/` exists and is non-empty, treat it as the current source of truth. Do not recreate or refresh it unless the user explicitly asks.
- Never invent facts. Missing details become open questions or clearly labeled assumptions.
- Always return concrete file paths that were created or updated so downstream steps can continue without rediscovery.

## Step 0: classify the request

### Bug-fix fast path

Use the `bug-fix` skill directly when all are true:

- The request is a bug, regression, runtime error, broken flow, or failing test/build.
- The user wants diagnosis and repair, not PRD/spec planning.
- The likely scope is bounded enough to investigate directly.

If this path applies:

1. Resolve the canonical `bug-fix` skill.
2. Execute it in the current orchestration agent.
3. Return the fix summary, files changed, validation, and any residual risk.

Do not run the feature-planning workflow for this path.

### Small feature request criteria

Treat the request as a small feature/change when all are true:

- Clear, concrete ask with no major open questions.
- Likely one story or less.
- No schema migration, major API surface change, or multi-service rollout.
- Low coordination risk across sensitive domains.

If the request is neither a bug-fix fast path nor clearly a small change, treat it as a full feature workflow.

## Small feature flow

When the request is small:

1. Create a standalone story folder under `.swe/stories/one-off/`.
2. Create `.swe/stories/one-off/001-<story-slug>.md` with:
   - Goal
   - Non-goals
   - Testable acceptance criteria
   - Validation steps
3. Implement the ask immediately using the `swe-flow-orchestrator` subagent.
4. Run the smallest validating command(s) available.
5. Rename the story file to `001-<story-slug>-done.md` after validation and note results in `.swe/stories/one-off/.next.md`.

Do not run PRD, spec, TDD, or exec flows for this path.

## Full feature workflow

### 1) Context (conditional)

- If `.swe/context/` exists and is non-empty, skip context generation and treat it as read-only input.
- Otherwise, delegate to `swe-context-builder`.

### 2) PRD

- Delegate to `swe-prd-runner`.
- Wait for a PRD under `.swe/proposals/PROPOSAL-00X-*.md`.
- Capture the PRD path; it becomes the source of truth for downstream work.

### 3) Spec and TDD in parallel

- Launch `swe-spec-runner` and `swe-tdd-runner` in parallel using the same PRD path.
- Constraint: `swe-spec-runner` must not generate `.swe/specs/TST-*.md`; that output belongs to `swe-tdd-runner`.
- Reconcile mismatches in slug, scope, acceptance criteria, rollout, and test coverage before implementation.

### 4) Execution (gated)

- Ask the user for an explicit go or no-go before implementation.
- Delegate to `swe-exec-runner` with the story folder path and any user constraints.

## Role playbooks

### `swe-flow-orchestrator`

- Read this runbook and choose the correct path:
  - Bug-fix fast path
  - Small feature flow
  - Full feature workflow
- Delegate to runner subagents when the runbook requires it.
- Return a concise summary with concrete file paths and the next step.

### `swe-context-builder`

- Resolve and read the canonical `swe-init` skill.
- Follow it exactly.
- Return created or updated file paths, a short summary, and open questions.

### `swe-prd-runner`

- Resolve and read the canonical `swe-prd` skill.
- Follow it exactly.
- Return the PRD path, short summary, and open questions.

### `swe-spec-runner`

- Resolve and read the canonical `swe-spec` skill.
- Follow it exactly except for the TDD ownership constraint above.
- Return the tech-spec, epic, and story paths plus top risks and open questions.

### `swe-tdd-runner`

- Resolve and read the canonical `swe-tdd` skill.
- Follow it exactly.
- Return the test-spec path, coverage summary, and PRD gaps.

### `swe-exec-runner`

- Resolve and read the canonical `swe-exec` skill.
- Follow it exactly.
- Return what changed, what was validated, and what is next.

### `swe-gtm-video-runner`

- Resolve and read the canonical `swe-gtm-video` skill.
- Follow it exactly.
- Return the GTM video package path, source artifacts used, assumptions, and open questions.
