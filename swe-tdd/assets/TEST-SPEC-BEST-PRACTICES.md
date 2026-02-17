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

## 2) Required sections (definition of done)

- Personas & access model
- Persona × feature matrix
- Derived user stories (PRD → stories)
- Feature-area breakdown (epic-aligned when possible)
- Requirements traceability (PRD → stories → tests; optionally epic/story)
- Edge cases (cross-cutting + per feature area)
- Test strategy (E2E approach + tooling)
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

## 5) Making tests actually runnable

- Avoid time-based sleeps; use deterministic waits (events, network assertions, polling with timeouts).
- Define test data seeding/reset strategy.
- Call out where feature flags/config are required to exercise paths.
- Identify flake risks and mitigations (async, eventual consistency, third parties).

## 6) Closing PRD gaps responsibly

When the PRD is missing detail, do this:

1. Add a small set of **Open Questions** (prioritized, actionable).
2. Write **Assumptions** that unblock drafting tests.
3. Mark assumption-dependent test cases clearly (e.g., `Blocked: needs PM confirmation`).
4. Provide a “default expected behavior” only when it’s a safe, common pattern, and label it as an assumption.
