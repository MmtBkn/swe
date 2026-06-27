---
name: swe-tdd
description: Break down a PRD/proposal into a comprehensive, E2E-first Test Specification Document (test plan) with persona coverage, a persona × feature matrix, feature-area breakdown, explicit UX edge cases (happy/error/empty/crash/recovery), and a PRD → user stories → E2E tests traceability map. Designed to run early as an independent pass for `swe-spec` or directly when the user asks to “write a test spec”, “create a QA test plan”, “derive tests from this PRD”, “create acceptance/validation test cases”, or wants Playwright/Selenium-style end-to-end user-flow validation.
---

# SWE TDD (PRD → Test Specification Document)

## Goal

Turn a PRD into a high-quality **Test Specification Document** that can drive implementation, QA, and release readiness, including:

- Persona definitions and access model
- **Persona × feature matrix** (coverage + permissions)
- Derived **user stories** (PRD → stories) for later verification
- Feature-area test breakdown (epic-aligned when available)
- Explicit UX-first edge cases (happy paths, error paths, empty/null states + CTAs, crash/recovery)
- Users and data required to test, created on the fly with isolated namespaces, no reliance on existing data, and cleanup after each run
- A per-worktree shared-stack, parallel-safe E2E execution strategy that avoids expensive environment spin-up per test worker
- Requirements traceability (PRD → stories → **E2E tests**), with assumptions clearly labeled
- A PRD-coverage iteration loop to surface ambiguities early (without writing the spec)

## Inputs

- **Primary**: PRD/proposal file path (preferred) or pasted PRD text.
  - Typical locations: `proposals/`, `.swe/proposals/`.
- **Optional (often missing on first run — do not block)**:
  - Technical spec: `.swe/specs/TSD-00X-<feature-slug>.md`
  - Epics: `.swe/epics/<feature-slug>/`
  - Stories (for finer-grain mapping): `.swe/stories/<feature-slug>/`
  - Repo standards/context: `.swe/context/**`, `docs/`, `README*`, `ARCHITECTURE*`, `adr/`, `decisions/`, `rfcs/`
  - Existing E2E test stack/config (discover from repo): `playwright.config.*`, `cypress.config.*`, Selenium/WebDriver setup, etc.

## Output

Create/update:

- Test spec: `.swe/specs/TST-00X-<feature-slug>.md`

Where:

- `<feature-slug>` is kebab-case derived from PRD title (or filename if needed).
- `TST-00X` is a 3-digit increment (e.g., `TST-001`). Choose the next number by scanning existing files matching `TST-\\d{3}` in `.swe/specs/`.

If the repo already stores test specs elsewhere, keep the *content* and structure from this skill, but follow the repo’s convention for paths.

## Workflow

### 1) Resolve the PRD (source of truth)

- If the user gave a PRD path, read it.
- If the user pasted PRD text, treat it as the PRD source of truth.
- If no PRD is provided, ask for it (offer likely locations), or ask the user to paste it.

### 2) Load related `.swe` artifacts (if present)

- Prefer to load in this order:
  1) Matching proposal in `.swe/proposals/`
  2) Latest technical spec `.swe/specs/TSD-00X-<feature-slug>.md` (highest `00X`)
  3) Related epics under `.swe/epics/<feature-slug>/`
  4) (Optional) Related Stories under `.swe/stories/<feature-slug>/`
- Use these artifacts to refine test scope and coverage, but do not contradict the PRD. If there’s a mismatch, call it out explicitly.
- It’s normal for these to be missing when running in parallel with `swe-spec`; proceed with PRD-only.

### 3) Load standards and templates

- Read `assets/TEST-SPEC-BEST-PRACTICES.md` and use it as your checklist/quality bar.
- Read `assets/TEST-SPEC-TEMPLATE.md` and use it as the starting structure.

### 4) E2E-first constraint (non-negotiable)

- This test spec is for **end-to-end user flows and outcomes**, not business-logic unit tests.
- Every test case should be automatable in an E2E framework (prefer Playwright; otherwise Selenium/Cypress per repo).
- If verifying an outcome requires hooks (seed data, APIs, feature flags), capture them as **preconditions**, but keep the assertions user-facing.
- Unit tests are acceptable only for backend-heavy business logic that cannot be validated efficiently through the browser. API tests are acceptable for API-only products or setup helpers, but they do not replace E2E acceptance for user-facing product behavior.
- Prefer fewer, high-signal E2E tests over broad low-value permutations. Use risk and user impact to decide P0/P1/P2 coverage.

### 4.1) Scalable E2E execution model

- Specify how to build once, start the application stack once per worktree, and reuse the same base URL across smoke, impacted, and full-regression E2E runs.
- Do not require a fresh environment per test file, worker, retry, story, or commit. Use one owned shared stack per worktree unless the repo architecture makes shared-stack isolation impossible.
- Do not hardcode ports or ask the user to choose ports. Auto-wire ports behind the scenes by discovering free ports or using repo-supported env vars, then pass the resolved base URL to tests.
- Define stack ownership metadata:
  - absolute worktree root from `pwd`
  - stack start timestamp
  - base URL and dynamically assigned ports
  - process/container IDs or labels
  - command used to start the stack
- Pass ownership metadata to E2E runs, for example `E2E_WORKTREE_ROOT`, `E2E_STACK_STARTED_AT`, `E2E_RUN_ID`, and `BASE_URL`.
- Tests and cleanup scripts must not interact with a stack whose recorded worktree root differs from their current `pwd`.
- If the worktree root matches but the stack timestamp differs, treat the older timestamp as stale. Reuse the newest healthy stack for that worktree; kill only processes/containers proven to belong to the same worktree and an older ghost timestamp.
- Prefer incremental runtime updates over full restarts: hot reload, targeted service restart, migration apply, Hasura metadata apply, schema refresh, or cache clear. Kill and recreate the stack only when incremental repair fails or the change requires it.
- If multiple local or remote runners need access to the same stack, document a tunnel option such as Cloudflare Tunnel or ngrok, plus the expected base URL variable.
- Define suite tiers:
  - Smoke: fastest health/login/critical-path coverage.
  - Impacted: tests mapped to the current story, changed routes, changed API contracts, and risk areas.
  - Full regression: run before PR/release or for broad/sensitive changes, not after every small edit.
- Define parallel execution requirements:
  - worker-scoped browser contexts and auth/storage state
  - no shared mutable accounts or orgs
  - unique test namespace per worktree/branch/commit/worker/test
  - cleanup and TTL fallback for crashed runs

### 5) Derive personas and access model

- If personas already exist in `.swe/context/**` or the PRD, reuse them.
- If personas are missing, infer **minimal reasonable personas** from the PRD and product shape (e.g., Admin / Member / Viewer / Anonymous), and clearly label them as **assumptions**.
- Define permissions per persona at the feature-area level (what they can see/do).

### 6) Break down the PRD by feature area (epic-aligned)

- If epics exist, use epic titles as the primary “feature areas”.
- If epics do not exist, create feature areas from PRD sections and user journeys (UI, API, data model, notifications, integrations, admin tooling, migration, etc.).
- For each feature area, identify:
  - User journeys (happy paths)
  - Empty/null states + user-friendly CTAs (what can the user do next?)
  - Error paths + recovery (retry, support, fallback)
  - Loading/intermediate states (spinners, skeletons, disabled buttons, progress)
  - Crash scenarios and graceful degradation (never strand the user)
  - Business rules
  - State transitions
  - Data changes
  - Integrations and async behavior
  - NFRs (performance, reliability, security, accessibility)

### 7) Derive user stories (required)

- Produce a concise set of user stories covering the PRD end-to-end:
  - Format: “As a <persona>, I want <capability>, so that <value>”
  - Include acceptance criteria that are **testable** and user-visible
  - Assign each story to a feature area and priority (P0/P1/P2)
- These stories are primarily for **later validation** (did the spec/epics/stories/implementation cover what users asked for?).

### 8) Create the Persona × Feature matrix (required)

- Build a matrix that maps each persona to each feature area:
  - Access/permissions (Allowed / Read-only / Denied)
  - Primary scenarios to validate
  - Test priority (P0/P1/P2)
  - Notes on risk/complexity

### 9) Produce detailed E2E test scenarios per feature area

- For each feature area, include:
  - **Smoke** scenarios (minimum viable validation)
  - **Happy path** scenarios (primary flows)
  - **Negative** scenarios (validation, errors, permissions)
  - **Edge cases** (explicit, enumerated; include empty states, null/undefined values, and crash/recovery)
  - **Observability checks** (logs/metrics/audits where relevant)
  - **Data Prep** prepare ephemeral users/data for non-conflicting, highly parallelized testing
  - **Cleanup** remove or expire test-owned resources so clutter does not break future runs
  - **Automation guidance** (Playwright preferred; otherwise Selenium/Cypress per repo)
- Prefer a consistent test case format with stable IDs (e.g., `TS-AREA1-001`) and **explicit user steps + expected user-visible outcomes**.

### 10) Requirements traceability (PRD → stories → E2E tests)

- Create a traceability table mapping PRD requirements/acceptance criteria → user story IDs → E2E test case IDs.
- If stories exist, optionally include story IDs in the mapping.
- If a PRD requirement is not testable as written, mark it and propose a concrete testable rewrite as a **suggestion**.

### 11) Catch ambiguities and close reasonable gaps (without writing the spec)

- Do **not** invent new features or design the architecture.
- When details are missing:
  - Add an **Assumptions** section (clearly labeled).
  - Add an **Open Questions** section (prioritized; what must be decided in the spec).
  - Still write “default” test scenarios that validate the most common expected behaviors, but mark them as **Assumption-dependent** (blocked until confirmed).
  - Explicitly call out **UX ambiguity** (copy, error messaging, empty state CTAs, recovery behavior).

### 12) Iterate with the PRD until coverage is complete

- Do a coverage loop (repeat until done):
  1) Scan the PRD section-by-section and list any requirement/AC not yet mapped.
  2) Add missing user stories and E2E tests.
  3) Add/refresh assumptions + open questions for ambiguous items.
  4) Re-run traceability to confirm **no PRD orphan requirements** remain.
- Stop condition: every PRD requirement/AC is mapped to at least one user story and one E2E test case (or explicitly marked “blocked: needs decision”).

### 13) Quality pass (Principal SDET)

- Re-read the PRD and ensure all sections are represented in the test spec.
- Re-check:
  - Persona coverage (matrix complete)
  - Feature-area coverage (no orphan requirements)
  - Edge cases present (cross-cutting + per area)
  - Clear priorities (P0/P1/P2) and E2E executability
  - No hidden uncertainty: assumptions and open questions are explicit
  - Do not rely on existing data
  - Instructions to clean up after every test
  - Shared-stack execution is defined so E2E does not repeatedly rebuild or restart the environment
  - Parallel worker/resource isolation is explicit enough that the same test can run concurrently on different worktrees or branches without collision
