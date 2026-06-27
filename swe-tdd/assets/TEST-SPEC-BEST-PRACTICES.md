# Test Specification Best Practices (Checklist)

Use this as a quality bar when turning a PRD into a Test Specification Document.

## 1) Core principles

- **Traceability over volume:** Every PRD requirement should map to at least one test (or an explicit “not testable yet” note).
- **Stay out of the spec:** This document is about *testable outcomes and UX*, not architecture/endpoints. If a design decision is required, capture it as an **Open Question**.
- **Be explicit about uncertainty:** Missing PRD detail becomes **Assumptions** + **Open Questions**, not hidden guesses.
- **Risk-based prioritization:** Clearly label **P0/P1/P2** (or Must/Should/Could) and justify P0 by user impact + likelihood.
- **Persona completeness:** If access control exists, test coverage is incomplete without persona-based validation.
- **Feature-area ownership:** Structure the test spec by feature area (preferably aligned to epics) so execution can parallelize.
- **UX-first bias:** Always cover happy paths *and* error/empty/null/crash/recovery paths with user-friendly expectations (copy + CTAs).
- **Shared stack over repeated spin-up:** Build and start the application stack once per worktree, then reuse the same base URL across E2E suites whenever possible.
- **Agent-wired ports:** Do not hardcode ports or ask users to choose them. Discover free ports or use repo-supported env vars behind the scenes and pass the resolved base URL to tests.
- **Owned runtime only:** Record absolute `pwd`, stack start timestamp, base URL, ports, and process/container IDs. Never interact with or kill a stack owned by a different worktree.
- **Incremental updates first:** Prefer hot reload, targeted service restart, migration apply, Hasura metadata apply, schema refresh, or cache clear before killing/recreating the stack.
- **Parallel-safe by design:** Every test run needs isolated users, orgs, groups, credentials, browser state, and domain data. The same test should be safe to run concurrently on different worktrees or branches.
- **Cleanup is part of correctness:** Tests must delete/archive test-owned resources or tag them for TTL cleanup after crashes.

## 2) Required sections (definition of done)

- Personas & access model
- Persona × feature matrix
- Derived user stories (PRD → stories)
- Feature-area breakdown (epic-aligned when possible)
- Requirements traceability (PRD → stories → tests; optionally epic/story)
- Edge cases (cross-cutting + per feature area)
- Test strategy (E2E approach + tooling)
- Shared-stack execution model
- Worktree stack ownership metadata and ghost cleanup rules
- Parallel data isolation and cleanup strategy
- Suite tiers (smoke, impacted, full regression)
- Release readiness / exit criteria

## 3) Edge case coverage (minimum bar)

For every **feature area**, include explicit tests for:

- **Permissions:** allowed vs denied vs read-only; “same UI, different access” scenarios
- **Validation:** boundary values, invalid formats, empty states + CTAs
- **Error UX:** actionable errors, retry, recovery, support paths
- **State transitions:** create/update/delete/restore; retries; idempotency where relevant
- **Failure modes:** timeouts, partial failures, external dependency failures
- **Concurrency:** double submit, simultaneous edits, out-of-order events
- **Crash scenarios:** never strand the user (error boundaries, safe fallbacks)
- **Observability:** “did we log/metric/audit the right thing” for critical actions

## 4) E2E guidance (this doc’s scope)

- Every test case should be runnable in an E2E framework (Playwright preferred; Selenium/Cypress per repo).
- Define tests in terms of **user actions** and **user-visible outcomes**.
- Prefer fewer, higher-signal tests (smoke + critical paths + high-risk error/empty/crash cases).
- Include user-perceived NFR checks where feasible in E2E (no infinite loading, reasonable latency, basic a11y checks). Defer true load/stress testing to a separate plan.
- Prefer resilient selectors (roles/labels/test-ids) and deterministic waits; avoid sleeps.
- Unit tests are fine for backend-heavy business logic, and API tests are fine for API-only products or setup helpers, but they do not replace browser E2E for user-facing behavior.
- Use smoke and impacted suites for story-level feedback. Reserve full regression for PR/release gates or broad, risky changes.

## 5) Making tests actually runnable

- Avoid time-based sleeps; use deterministic waits (events, network assertions, polling with timeouts).
- Define test data seeding/reset strategy.
- Define a namespace format using worktree hash, branch, commit, worker index, test file/name, and a timestamp or random suffix.
- Create required users, super-admin credentials, orgs, groups, feature flags, and domain data inside that namespace.
- Keep browser contexts and auth/storage state worker-scoped.
- Pass `E2E_WORKTREE_ROOT`, `E2E_STACK_STARTED_AT`, `E2E_RUN_ID`, and `BASE_URL` into E2E runs so ownership and cleanup are deterministic.
- Document cleanup hooks and a fallback TTL cleanup strategy for crashed or interrupted runs.
- Call out where feature flags/config are required to exercise paths.
- Identify flake risks and mitigations (async, eventual consistency, third parties).

## 6) Closing PRD gaps responsibly

When the PRD is missing detail, do this:

1. Add a small set of **Open Questions** (prioritized, actionable).
2. Write **Assumptions** that unblock drafting tests.
3. Mark assumption-dependent test cases clearly (e.g., `Blocked: needs PM confirmation`).
4. Provide a “default expected behavior” only when it’s a safe, common pattern, and label it as an assumption.
