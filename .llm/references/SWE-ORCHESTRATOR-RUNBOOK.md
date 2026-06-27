# SWE Orchestrator Runbook

This file is the single source of truth for SWE orchestration behavior across provider-specific wrappers.

All provider-specific entrypoints should reference this runbook instead of duplicating it:

- Cursor skill wrapper: `.cursor/skills/swe-orchestrator/`
- Cursor subagents: `.cursor/agents/`
- Claude command wrapper: `.claude/commands/swe-orchestrator.md`
- Claude subagents: `.claude/agents/`

## Canonical skill instructions

For every workflow step, the canonical how-to instructions live in the base skill files:

- `swe-bug-fix`
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
- Prefer one proposal/feature branch per proposal. Keep story work as sequential, independently validated commits on that branch.
- Do not open or push a PR until the branch is locally green, unless the user explicitly asks for a failing draft and the failure is documented.
- Default validation is E2E-first for user-facing behavior. Unit tests are supporting checks for backend-heavy business logic; API tests are supporting checks for API-only surfaces or setup helpers.
- Favor a shared-stack E2E model per worktree: build once, start the stack once, reuse the same base URL across smoke, impacted, and full-regression suites.
- Do not hardcode ports or ask users to choose them. Auto-wire ports behind the scenes with free-port discovery or repo-supported env vars, and pass resolved base URLs into tests.
- Runtime cleanup must be ownership-safe: record absolute `pwd`, stack start timestamp, ports, base URL, and process/container IDs; never interact with a stack owned by a different worktree.
- E2E tests must create isolated data per worktree/branch/commit/worker/test and clean up their own users, orgs, groups, credentials, and domain resources.
- Implementation must stay within repo coding standards and avoid giant generated files: functions <=50 lines preferred, files <=400 lines preferred, complexity <=10, no unbounded API calls in loops, and no critical/high security findings.

## Step 0: classify the request

### swe-bug-fix fast path

Use the `swe-bug-fix` skill directly when all are true:

- The request is a bug, regression, runtime error, broken flow, or failing test/build.
- The user wants diagnosis and repair, not PRD/spec planning.
- The likely scope is bounded enough to investigate directly.

If this path applies:

1. Resolve the canonical `swe-bug-fix` skill.
2. Execute it in the current orchestration agent.
3. Return the fix summary, files changed, validation, and any residual risk.

Do not run the feature-planning workflow for this path.

### Small feature request criteria

Treat the request as a small feature/change when all are true:

- Clear, concrete ask with no major open questions.
- Likely one story or less.
- No schema migration, major API surface change, or multi-service rollout.
- Low coordination risk across sensitive domains.

If the request is neither a swe-bug-fix fast path nor clearly a small change, treat it as a full feature workflow.

## Small feature flow

When the request is small:

1. Create a standalone story folder under `.swe/stories/one-off/`.
2. Create `.swe/stories/one-off/001-<story-slug>.md` with:
   - Goal
   - Non-goals
   - Testable acceptance criteria
   - Validation steps
3. Implement the ask immediately using the `swe-flow-orchestrator` subagent.
4. Work on a dedicated branch unless the user already placed you on the intended branch.
5. Run the story validation gate: build/lint/typecheck where available plus smoke or impacted E2E for user-facing behavior.
6. Rename the story file to `001-<story-slug>-done.md` after validation and note results in `.swe/stories/one-off/.next.md`.
7. Commit the code, tests, `.next.md`, and story rename to the branch.

Do not run PRD, spec, TDD, or exec flows for this path.

## Full feature workflow

### 1) Context (conditional)

- If `.swe/context/` exists and is non-empty, skip context generation and treat it as read-only input.
- Otherwise, delegate to `swe-context-builder`.

### 2) PRD

- Delegate to `swe-prd-runner`.
- Wait for a PRD under `.swe/proposals/PROPOSAL-00X-*.md`.
- Capture the PRD path; it becomes the source of truth for downstream work.

### 3) Spec with independent TDD pass

- Delegate to `swe-spec-runner` with the PRD path.
- `swe-spec-runner` must ensure `.swe/specs/TST-*.md` exists by spawning an independent `swe-tdd` pass when subagents/runners are available.
- If the orchestrator directly launches `swe-tdd-runner`, treat that as the independent pass for `swe-spec-runner`; do not create duplicate TST files.
- Reconcile mismatches in slug, scope, acceptance criteria, rollout, and test coverage before implementation.
- Ensure the TDD output defines smoke, impacted, and full-regression tiers, per-worktree shared-stack E2E execution, agent-wired ports, runtime ownership metadata, parallel-safe data namespaces, and cleanup expectations.
- Ensure the spec output creates fine-grained vertical stories that can be implemented, validated, and committed independently. Do not collapse scope to minimize story count.

### 4) Execution (gated)

- Ask the user for an explicit go or no-go before implementation.
- Delegate to `swe-exec-runner` with the story folder path, proposal branch expectation, TST path, and any user constraints.
- Require `swe-exec-runner` to validate and commit each story before marking it `-done`.
- Require final branch validation before PR: build/lint/typecheck, impacted E2E, and full regression when required by risk or scope.

## Role playbooks

### `swe-flow-orchestrator`

- Read this runbook and choose the correct path:
  - swe-bug-fix fast path
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
- Follow it exactly, including its independent `swe-tdd` pass.
- Return the tech-spec, test-spec, epic, and story paths plus top risks and open questions.

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
