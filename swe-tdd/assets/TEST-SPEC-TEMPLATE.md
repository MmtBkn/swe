# Test Specification Document (Template)

---

## Metadata (Front Matter)

- **Title:** [Test Spec for <Feature Name>]
- **Author(s):** [Name(s)]
- **Owner:** [Team/role responsible]
- **Status:** [Draft / In Review / Approved / Executing / Done]
- **Last Updated:** [YYYY-MM-DD]
- **Related Links:** [PRD, Tech Spec, Epics, dashboards, runbooks]

### Version History

| Version | Date       | Author | Notes         |
| ------- | ---------- | ------ | ------------- |
| 0.1     | YYYY-MM-DD | [Name] | Initial Draft |

---

## 1. Executive Summary

- **Feature / Change:** [1–2 sentences]
- **Primary user value:** [1–2 bullets]
- **Key risks:** [Top 3 testing risks]
- **In scope:** [Major areas]
- **Out of scope:** [Explicit exclusions]

---

## 2. Source of Truth

- **PRD:** [path/link]
- **Tech Spec (if any):** [path/link]
- **Epics (if any):** [path/link]
- **Stories (if any):** [path/link]

---

## 3. Personas & Access Model

### 3.1 Personas

| Persona | Description | Entry Points | Notes |
| ------ | ----------- | ------------ | ----- |
| Admin  |             |              |       |
| Member |             |              |       |
| Viewer |             |              |       |

### 3.2 Permissions / Capabilities

| Persona | Capability | Allowed? (Y/N/Read-only) | Notes |
| ------- | ---------- | ------------------------ | ----- |
| Admin   |            |                          |       |

---

## 4. Feature Areas (Epic-Aligned)

If epics exist, use epic titles as feature areas. Otherwise, derive feature areas from PRD sections and user journeys.

| Feature Area | Epic ID/Title (if any) | Primary Journeys | Dependencies | Risk |
| ------------ | ---------------------- | ---------------- | ------------ | ---- |
| Area A       | EPIC-00X               |                  |              |      |

---

## 5. Persona × Feature Matrix (Coverage)

Keep this as an actual matrix when feasible. If there are too many features, keep the matrix for P0/P1 areas and add a detailed access table below.

### 5.1 Matrix

Legend: **A**=Allowed, **R**=Read-only, **D**=Denied, **N/A**=Not applicable

| Persona \\ Feature Area | Area A | Area B | Area C |
| ----------------------- | ------ | ------ | ------ |
| Admin                   | A      | A      | A      |
| Member                  | A      | R      | D      |
| Viewer                  | R      | D      | D      |

### 5.2 Access & Coverage Table (scales better than a wide matrix)

| Persona | Feature Area | Access | Must-Validate Scenarios | Priority |
| ------- | ------------ | ------ | ----------------------- | -------- |
| Admin   | Area A       | A      |                         | P0       |

---

## 6. User Stories (Derived From PRD)

These are **test-driven** user stories to help validate implementation completeness later (even if `.swe/stories/` doesn’t exist yet).

| ID | Persona | User Story | Feature Area | Priority (P0/P1/P2) | Acceptance Criteria (testable) | Notes |
| -- | ------- | ---------- | ------------ | ------------------- | ------------------------------ | ----- |
| US-001 | Admin | As an Admin, I want… | Area A | P0 | Given/When/Then… | |

---

## 7. Requirements Traceability (PRD → Stories → Tests)

| PRD Requirement / AC | User Story IDs | Epic/Story (optional) | Test Case IDs | Notes |
| -------------------- | -------------- | --------------------- | ------------- | ----- |
|                      |                |                       |               |       |

---

## 8. Test Strategy

### 8.1 E2E Approach (Primary)

This test spec focuses on **end-to-end user flows and outcomes**:

- Run against a running environment (local/CI/staging) with a real browser.
- Validate **user-visible outcomes** (UI state, navigation, notifications, permission outcomes).
- Use preconditions/fixtures/APIs only to set up state; keep assertions user-centric.
- Prefer stable locators (e.g., roles/labels/test-ids) over brittle CSS selectors.
- Unit tests are supporting checks for backend-heavy business logic, not substitutes for user-facing E2E acceptance.
- API tests are acceptable for API-only user surfaces or setup helpers, but browser E2E remains the default for product behavior.

### 8.1.1 Suite Tiers

| Tier | Purpose | When to Run | Expected Duration Target | Required Coverage |
| ---- | ------- | ----------- | ------------------------ | ----------------- |
| Smoke | Fast confidence in environment + critical path | Every story before `-done`; before PR | [target] | Health/login + one critical path |
| Impacted | Validate changed surfaces and mapped requirements | Every story before `-done`; before PR | [target] | Tests linked to changed routes/APIs/personas |
| Full Regression | Broad confidence before merge/release | Before PR, release, or broad/sensitive changes | [target] | P0/P1 cross-feature flows |

### 8.2 Tooling (align to repo)

- **E2E:** [Playwright preferred / Selenium / Cypress / other]
- **Auth helpers:** [storage state, test users, SSO bypass, etc]
- **Test data helpers:** [seed scripts, API helpers, DB reset]

### 8.3 Shared Stack Execution

- **Build once:** [command]
- **Start stack once per worktree:** [command]
- **Base URL:** [local URL or tunnel URL env var]
- **Port wiring:** Agent auto-discovers free ports or uses repo-supported env vars behind the scenes; no user port selection and no hardcoded ports.
- **Readiness check:** [health endpoint/UI signal]
- **Reuse rule:** Reuse the same owned running stack for the current worktree across smoke, impacted, and full-regression suites. Do not restart per test file/worker/retry/story unless isolation requires it.
- **Incremental update strategy:** [hot reload, targeted service restart, migration apply, Hasura metadata apply, schema refresh, cache clear]
- **Full restart criteria:** [only when incremental repair fails or the change requires it]
- **Tunnel option:** [Cloudflare Tunnel/ngrok command and URL variable, if parallel remote runners need access]

#### 8.3.1 Stack Ownership Metadata

| Field | Value / Source | Required Use |
| ----- | -------------- | ------------ |
| Worktree root | absolute `pwd` | Prevent cross-worktree interaction |
| Stack start timestamp | generated when stack starts | Detect stale/ghost stacks |
| Base URL | resolved at startup | Passed to E2E as `BASE_URL` |
| Ports | dynamically assigned or repo env vars | Avoid hardcoded collisions |
| Process/container IDs or labels | startup output/runtime labels | Safe cleanup/restart targeting |
| Start command | repo-native command | Reproduce and debug |

Pass to E2E runs:
- `E2E_WORKTREE_ROOT`
- `E2E_STACK_STARTED_AT`
- `E2E_RUN_ID`
- `BASE_URL`

Ownership rules:
- If recorded worktree root differs from current `pwd`, do not interact with or kill that stack.
- If worktree root matches and timestamp matches, reuse that stack.
- If worktree root matches but a newer healthy stack timestamp exists, treat older runs as ghosts and clean up only resources proven to belong to the same worktree and older timestamp.

### 8.4 Environments

- **Local:** [how to run shared stack]
- **CI:** [pipeline and worker parallelism]
- **Staging:** [required flags/seed data]

### 8.5 Test Data, Isolation & Cleanup

- **Namespace format:** `[worktree-hash]-[branch]-[commit]-[worker]-[test]-[random or timestamp]`
- **Required fixtures:** [created per run/test]
- **Required accounts/roles:** [created per worker/test, including super-admin if needed]
- **Required orgs/groups/resources:** [created per worker/test]
- **Isolation rules:** no shared mutable users, orgs, groups, browser storage state, or seeded records across parallel workers
- **Cleanup strategy:** delete/archive test-owned resources in `afterEach`/`afterAll`; tag resources for TTL/fallback cleanup after crashed runs
- **Data reset strategy:** [only if needed beyond per-test cleanup]

---

### 8.6 UX & Recovery Expectations (Global)

Use this to drive UX-first test cases. Prefer “no dead ends”.

- **Empty states:** Clear explanation + primary CTA (create/import/invite/learn more).
- **Errors:** Actionable messaging (what happened, why, what to do next) + retry when safe.
- **Loading:** Avoid infinite spinners; timeouts and escape hatches; disable duplicate submits.
- **Crash resilience:** Error boundaries / graceful degradation; users can recover or get support.

---

## 9. Feature-Area Test Scenarios (Required)

For each feature area, include happy paths, negative paths, permissions, and explicit edge cases.

### 9.A Feature Area: [Area A]

**Scope:**
- 

**Key journeys:**
- 

**Empty/null states + CTAs (UX-first):**
- [What happens with no data? What should the user do next?]

**Error paths + recovery (UX-first):**
- [Validation errors, permission denied, timeouts, retries]

**Crash / degraded-mode expectations (UX-first):**
- [Never strand the user; provide fallback/retry/support path]

**Assumptions / Open questions (if any):**
- 

#### 9.A.1 Test Cases

| ID | Tier | Scenario | Persona(s) | Priority (P0/P1/P2) | Preconditions / Isolated Data | Cleanup | Steps (User Actions) | Expected User Outcome |
| -- | ---- | -------- | ---------- | ------------------- | ----------------------------- | ------- | -------------------- | --------------------- |
| TS-A-001 | Smoke/Impacted/Regression | | | P0 | | | | |

#### 9.A.2 Edge Cases (Explicit)

- [Edge case 1]
- [Edge case 2]

---

## 10. Cross-Cutting Edge Case Catalog (Required)

Capture edge cases that cut across multiple feature areas.

### 10.1 Auth & Permissions

- Role downgrade/upgrade while session active
- Access revoked mid-flow
- Expired/invalid tokens; logout/session timeout handling

### 10.2 Validation & Data Integrity

- Boundary values (min/max), empty/whitespace-only, invalid formats
- Duplicate submissions / idempotency
- Partial failures and rollback behavior

### 10.3 Concurrency & Ordering

- Double-click / multi-submit
- Simultaneous edits
- Out-of-order async events

### 10.4 Time / Locale / i18n

- Time zones, DST transitions, locale-specific formatting

### 10.5 Reliability / Network

- Retries, timeouts, offline/slow network, eventual consistency

### 10.6 Pagination / Sorting / Filtering (if applicable)

- Empty states, large pages, cursor invalidation

### 10.7 Security Basics

- Authorization bypass attempts, insecure direct object references (IDOR)
- Input sanitization / injection risk surfaces

### 10.8 Accessibility (if UI)

- Keyboard-only flows
- Screen reader labels for critical controls
- Focus management on navigation/modals/errors

### 10.9 Empty States & Calls to Action (if UI)

- No results / no data states with a clear next action (create/import/invite/learn more)
- First-run experience (FTUE) and guidance copy
- Permission-limited empty states (user lacks access; explain why + what to do)

### 10.10 Crash Scenarios & Recovery

- UI render crashes (blank screen) → error boundary + recovery path
- API/worker crashes → user gets actionable error + retry
- “Stuck” states (infinite loading, disabled UI) → timeouts and escape hatches

---

## 11. Non-Functional Testing

### 11.1 Performance

- User-perceived performance budgets (if defined): page load, action latency, spinners.
- Validate with E2E-friendly checks where possible (timings, “no infinite loading”, responsiveness).
- If deeper load/stress testing is required, note it as a follow-up outside this E2E-focused test spec.

### 11.2 Observability / Auditing

- Expected logs/metrics/traces for key actions
- Audit events for security-sensitive actions

### 11.3 Backward Compatibility / Migration

- Upgrade/downgrade considerations
- Data migration verification (if any)

---

## 12. Release Readiness & Exit Criteria

- **P0 pass criteria:** [what must pass]
- **Story done gate:** [build/lint/typecheck + smoke/impacted E2E commands]
- **PR gate:** [build/lint/typecheck + impacted E2E + full regression criteria]
- **Known risks accepted:** [list]
- **Monitoring plan:** [dashboards/alerts]
- **Rollback triggers:** [what conditions cause rollback]
