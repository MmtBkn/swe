---
name: swe-spec
description: Translate an existing PRD/proposal into a principal-architect-level technical specification, independent E2E-first test spec, and implementation epics/stories aligned to repo/company standards and best practices. Use when a user asks to “write a tech spec”, “create a technical design/spec”, “turn this PRD into a technical spec”, “derive epics”, or prepare a feature for implementation.
---

# SWE Spec

## Goal

Turn a PRD into:

- A high-quality technical specification document (architecture + detailed design + rollout/testing).
- An independent E2E-first test specification generated through `swe-tdd`.
- A set of fine-grained implementation epics/stories with clear scope and acceptance criteria.

## Inputs

- A PRD/proposal file path (preferred) or pasted PRD text.
  - Typical locations: `proposals/`, `.swe/proposals/`.
- Repo context and standards (when available):
  - `.swe/context/**` (company/product briefs, personas, etc.)
  - `docs/`, `README*`, `ARCHITECTURE*`, `CONTRIBUTING*`, `adr/`, `decisions/`, `rfcs/`, `.github/`
- Mocks, user may provide

## Outputs

Create/update the following files:

- Tech spec: `.swe/specs/TSD-00X-<feature-slug>.md`
- Test spec: `.swe/specs/TST-00X-<feature-slug>.md`
- Epics: `.swe/epics/<feature-slug>/EPIC-00X-<epic-slug>.md`
- Stories: `.swe/stories/<feature-slug>/STORY-00X-<story-slug>.md`

This skill must ensure the TST exists even when the user only runs `swe-spec -> swe-exec`. Generate the TST by delegating to an independent `swe-tdd` pass; do not let the same spec-writing perspective silently invent the test plan.

Where:

- `<feature-slug>` is kebab-case derived from the PRD title (or filename if needed).
- `EPIC-00X` and `STORY-00X` is a 3-digit increment (e.g., `EPIC-001`).
- Use filesystem-safe names. If you want a colon in the *title* (e.g., `EPIC-001: Payments API`), keep it in the H1, not the filename.

## Workflow

### 1) Resolve the PRD

- If the user gave a PRD path, read it (if remote url, use your tools to read it).
- If not, ask for the PRD path (offer likely locations: `proposals/`, `.swe/proposals/`).
- If the user pasted PRD text, treat it as the PRD source of truth.
- Do not invent requirements; stick with the PRD, and make your best judgement for edge cases.

### 2) Load standards and constraints

- Read repo-local standards first (don't skip, full file):
  - `.swe/context/**` (if present)
  - Architecture docs/ADRs (if present)
  - AGENTS.md, CLAUDE.md, .github/copilot-instructions.md
  - Coding/contribution standards (if present)
- If company standards conflict with generic best practices, follow company standards and document the rationale.
- If no standards exist, follow `assets/TECH-SPEC-BEST-PRACTICES.md`.

### 3) Load related mockups
- Read mockup files
  - Read DESIGN.md file if present
  - If local, identify, and read local mockup files
  - If remote read it (use your tools to donwload or read it)
    - prefer fetching html/react version where exist

### 4) Load skill assets

- Read `assets/TECH-SPEC-BEST-PRACTICES.md` and use it as your quality bar and checklist.
- Read `assets/TECH-SPEC-TEMPLATE.md` and use it as the starting structure for the spec.

### 4.1) Start the independent TDD pass

- Start an independent `swe-tdd` pass as early as possible after resolving the PRD and standards.
- If subagents/runners are available, spawn a separate agent with the canonical `swe-tdd` skill, passing only:
  - PRD/proposal path or pasted PRD text
  - repo/context pointers needed to understand personas and product behavior
  - requested TST output path
  - instruction to avoid reading your draft TSD until its first TST draft is complete
- If subagents are not available, run the `swe-tdd` workflow yourself in a deliberately separate pass before finalizing epics/stories, and label in the TST that no separate agent was available.
- The independent TDD pass must create/update `.swe/specs/TST-00X-<feature-slug>.md`.
- Reconcile TST gaps back into the TSD, epics, and stories before implementation. Do not proceed to `swe-exec` with only a TSD.

### 5) Plan integration points
4. Create a deep codebase analysis plan (before Tech Spec)
   • Produce a deep analysis plan (15–30 bullets) that explains how you will understand:
      •	the current product behavior,
      •	the actual codebase architecture, and
      •	the exact integration points required for the upcoming Tech Spec.
      •	Ingest product context and historical decisions
      •	Read anything under .swe/context/ (if present).
      •	Read related proposals under .swe/proposals/ (if present), prioritizing the most recent proposals to learn prior tradeoffs and constraints.
      •	If .swe/proposals/ does not exist, proceed without failing.
      •	Map the repo topology and ownership boundaries
      •	Determine if this is a monorepo vs multi-repo vs single app, and list major packages/services.
      •	Identify frontend/backend/services, shared libraries, internal SDKs, and “glue” layers.
      •	Identify bounded contexts / domains (e.g., billing, auth, chat, search, documents) and where each lives in code.
      • Identify API, and UI patterns
      •	Understand runtime + delivery shape (how it actually runs)
      •	Identify entrypoints and bootstrapping code for each deployable (servers, workers, CLIs).
      •	Identify build system(s), packaging, and dependency graph (workspaces, modules, Bazel, Gradle, etc.).
      •	Inspect CI/CD pipelines and environments (dev/stage/prod), plus deployment assets (Docker/K8s/Helm/Terraform).
      •	Note environment variables, secrets strategy, config layering, and runtime flags.
      •	Find integration points the Tech Spec must reference
      •	Identify public interfaces: HTTP routes, RPC, GraphQL, message topics/queues, cron jobs, webhooks.
      •	Identify consumers/providers: who calls whom, where retries/timeouts happen, and where contracts are defined.
      •	Identify cross-cutting infrastructure: authn/authz, telemetry, caching, rate limiting, feature flags, localization, search indexing, background jobs.
      •	Pinpoint data & state relationships
      •	Identify data stores (SQL/NoSQL/vector/blob), schemas/migrations, ORMs, repositories/DAOs.
      •	Trace key entities and lifecycle: where created, read, updated, deleted; and any state machines.
      •	Identify data ownership boundaries and duplication risks.
      •	Trace request flows end-to-end
      •	For 1–3 representative user journeys relevant to the feature, trace:
      •	UI → API → service → datastore (and back), or worker flows if async.
      •	Record key modules involved, contract boundaries, and failure points.
      •	Audit extension mechanisms + feature enablement
      •	Identify feature flag/config system usage and standard patterns.
      •	Identify plugin/adapter patterns, dependency injection boundaries, and interface abstractions you should extend instead of bypass.
      •	Catalog “must-touch” modules and “do-not-touch” constraints
      •	List the most likely modules/files/packages impacted by the feature.
      •	List sensitive areas (security, auth, billing, compliance) and constraints from prior proposals/context.
    •	Produce a “Tech Spec Integration Map” artifact
      •	Create a short artifact under: .swe/.cache/tech-analysis/ANALYSIS-00X-<Short-Slug>.md containing:
      •	Architecture snapshot (components + responsibilities)
      •	Integration inventory (APIs, events, jobs, external deps)
      •	Dependency graph (at least high-level)
      •	Key flows (sequence-style bullets)
      •	Data model touchpoints (tables/collections/indexes)
      •	Risk list + unknowns (with planned validation steps)
      • Tests that need to be created/updated
      • E2E suite tier expectations (smoke, impacted, full regression)
      • Shared-stack, parallel-safe test data requirements
      • Integration points with existing APIs/Components
      •	This artifact becomes the source of truth for the upcoming Tech Spec.
      •	Hard requirement: reflect analysis in the Tech Spec
      • If we are operating a monorepo like nx;
        • Idetify modularization opportunuties for long term maintenance, and scalibiliy
        • npm packages, microfrontends, python packages, docker containers, nx projects, microservices, whatever we can modularize to build, test whatever is changed, so we can build and deploy large scale projects
        • Identify modules where functionality has a distinct responsibility, ownership, dependencies, reuse potential, testing/build requirements, or when the existing module is becoming difficult to understand and maintain.
   •	When writing the Tech Spec, you must:
      •	explicitly reference the discovered integration points,
      •	name the impacted modules/services,
      • point to related mockups (where applicable)
      •	describe relationship boundaries,
      •	and ensure proposed design aligns with existing patterns found in the repo.
      •	If evidence is missing, clearly label assumptions and add a “Validation Plan” section.
      •	Suggested files/folders to inspect (when present)
      •	README*, docs/, package.json, go.mod, pyproject.toml, requirements.txt, Cargo.toml
      •	Dockerfile, docker-compose.yml, .github/workflows/
      •	k8s/, helm/, terraform/, infra/, .env*
      •	plus: src/, apps/, services/, packages/, libs/, cmd/, internal/, api/, migrations/ (if they exist)

### 6) Write the technical specification (principal architect mode)
- Read `.swe/.cache/tech-analysis/ANALYSIS-00X-<Short-Slug>.md`, all of it.
- Create `.swe/specs/` if needed.
- Create/update `.swe/specs/TSD-00X-<feature-slug>.md` using the template.
- Requirements traceability:
  - Map each PRD requirement/acceptance criterion to concrete design elements (APIs, jobs, data changes, UI).
  - Call out open questions explicitly (do not hide uncertainty).
- Architecture quality:
  - Include at least one diagram when helpful (Mermaid is preferred).
  - Introduce new modules/microfrontends/microservices where functionality has a distinct responsibility, ownership, dependencies, reuse potential, testing/build requirements, or when the existing module is becoming difficult to understand and maintain
  - Present 1–3 viable options when meaningful; pick one and justify trade-offs.
  - Cover security/privacy, performance, observability, migrations, rollout/rollback, and testing.
- Style:
  - Act like a principal engineer
  - Be crisp, concrete, and decisive.
  - Prefer tables/checklists for scannability.
  - Avoid hand-wavy phrases (“just”, “simply”, “etc.”).

### 7) Spec quality pass

- Act like another Principal Engineer, and review the tech spec against `assets/TECH-SPEC-BEST-PRACTICES.md`, and against the original PRD and fix gaps.
- Do another round of pass against the original PRD and fix gaps
- Ensure outputs are created exactly under `.swe/specs/`.

### 8) Reconcile validation with the independent E2E test spec
- Read `.swe/specs/TST-00X-<feature-slug>.md` and align epics/stories with its personas, feature areas, and E2E test IDs.
- If the TST is missing, stop and create it through the independent `swe-tdd` pass before creating final epics/stories.
- Treat TST findings as a second perspective. If the TST identifies missing UX states, permissions, edge cases, or data cleanup requirements, update the TSD and implementation stories.
- In the tech spec, define validation requirements at the design level:
  - preferred E2E framework and repo-native commands when discoverable
  - story done gate: build/lint/typecheck plus smoke or impacted E2E
  - PR gate: build/lint/typecheck plus impacted E2E and full regression when required
  - shared-stack execution: one owned stack per worktree, ports auto-wired behind the scenes, incremental updates where possible
  - parallel-safe data: unique test namespace, per-worker users/orgs/groups, cleanup and TTL fallback
- Keep assertions user-facing. Use unit/API tests only as supporting coverage for backend-heavy business logic or API-only products.

### 9) Create epics from the spec

- Create `.swe/epics/<feature-slug>/` if needed.
- Derive a set of epics (usually 1–20 depending on the size, and edge cases) that cover end-to-end delivery.
- For each epic:
  - Choose the next incremental `EPIC-00X` by scanning existing epic files in the folder.
  - Create `EPIC-00X-<epic-slug>.md` and break down the PRD/Tech Spec section
  - Write the epic like you are writing for junior engineer, don't leave any detail out
  - Prefer vertical user-value epics over purely component-layer epics. Component-only epics are acceptable only for platform prerequisites, migrations, or cross-cutting infrastructure.
  - Use the design system that project is following for the Web/UI changes. Pick, and use material design (likely with material-ui), or fluent UI if not defined.
  - Make sure happy paths, loading paths, error paths, null states are explicitly covered with call to actions (create, retry etc.) 
- Include validation expectations and related TST IDs in each epic.

### 10) Epic quality pass

- Review the spec against `assets/TECH-SPEC-BEST-PRACTICES.md`, the original PRD and fix gaps.
- Do another round of pass against the original PRD and fix gaps by creating more epics, or updating existing epics
- Ensure outputs are created exactly under `.swe/epics/<feature-slug>/`.

### 11) Create stories from the spec, and epics

- Create `.swe/stories/<feature-slug>/` if needed.
- For each epic:
  - Choose the next incremental `STORY-00X` by scanning existing epic files in the folder.
  - Create `STORY-00X-<epic-slug>-<story-slug>.md`
  - Derive as many fine-grained stories as needed to make scope, dependencies, and acceptance criteria unambiguous. Do not optimize for fewer stories. If a feature genuinely needs 100 detailed stories, create 100 detailed stories.
    - Act like a principal TPM, and break down the PRD/Epic section to story using story writing best practices
    - Write the story like you are writing it for a junior engineer, so provide clear guidence, and direction, and don't leave any detail out
    - Prefer fine-grained vertical implementation stories that include the minimum frontend, backend, data, and test work needed to deliver one user-visible outcome.
    - Split stories by user role, route/screen, state transition, integration boundary, migration step, permission model, error/recovery state, and independently testable acceptance criteria.
    - Avoid overloaded stories with multiple unrelated outcomes. Avoid vague placeholder stories that cannot be validated independently.
    - Create separate component-layer stories only when the work cannot be safely shipped as a vertical slice, such as foundational migrations, shared SDKs, auth primitives, or infrastructure.
    - Make setup/boilerplate tasks small and explicit. Do not let setup stories become a dumping ground for unrelated implementation.
      - For front end tasks, act like a principal user experience designer. Detail user experience, and designs. Include links to related mockups where applicable
      - When you are handling CRUD screens, separate list/view, and edit views (edits are usually popup, or dedicated page unless instructed otherwise)
    - Documentation tasks are added under .swe/docs (separate stories .swe/docs/support for customer support team, .swe/docs/gtm for go to market team, .swe/docs/ops for Ops team (manual configs etc.), .swe/docs/devops for DevOps team (flags etc, where applicable),  and other options where applicable)
    - Security review for each epic
    - Every story must include:
      - expected branch/commit scope
      - instructions to run build/lint/typecheck/e2e commands where applicable
      - smoke or impacted E2E test IDs from the TST when known
      - required isolated test data and cleanup expectations
      - code-quality constraints: functions <=50 lines preferred, files <=400 lines preferred, cyclomatic complexity <=10, no hardcoded values, no duplicated code, no unbounded API loops
      - user-visible acceptance criteria
      - non functional requirements
- Continue until all epics are covered with enough detail for a junior engineer to implement safely. The goal is complete, fine-grained, independently testable scope, not artificial ticket minimization.

### 12) Story quality pass
- Compact your context
- Read everything under `.swe/context`, `.swe/epics/<feature-slug>/`, and all the files under `STORY-00X-<epic-slug>` It's long, but It's important to build the context. 
- Start from the first story, and do this for each story; Review the story against the PRD/Epic, and fix gaps by updating the story, or creating a new story.
- Do final pass, and make sure stories are covering everything under the PRD, Tech Spec, and the Epic that is part of
- Ensure outputs are created exactly under `.swe/stories/<feature-slug>/`

### 13) Implementation quality pass
- Read everything under `.swe/context`, `.swe/epics/<feature-slug>/`, `.swe/stories/<feature-slug>/`, `.swe/specs/TSD-00X-<feature-slug>.md`, `.swe/.cache/tech-analysis/ANALYSIS-00X-<Short-Slug>.md` It's long, but It's important to build the context.
- Identify integration risks, potential things that we would break during the integration (product, build, infra, anything), and create extra stories to mitigate them
- If UI is involved instruct stories to do final pass testing using AIs browser mcp skills like Chrome MCP to bring the full app up, take screenshots, and test it, and make sure stories are covering the PRD requirements, Tech Spec, and the Epic that is part of, and none of the existing features are broken by this change
- Verify every story is small and specific enough to implement, validate, and commit independently on the proposal branch.
- Verify every story has explicit E2E-first validation and parallel-safe test data instructions.
- Verify the full feature can be validated with one owned running stack per worktree instead of spinning up a new environment per test worker.
- Verify implementation guidance rejects giant generated files, god objects, deep nesting, missing error/null/recovery states, and critical/high security findings.

Notes:
This is full feature planning. Complete the task without cutting corners, and do not be lazy about decomposition. Optimize for detailed, fine-grained, reviewable artifacts that lead to small green story commits. Include happy paths, null states, error paths, and recovery paths. Use best judgment to unblock reasonable gaps with explicit assumptions, and stop to surface only truly blocking decisions. Stories should read as if written by a principal TPM for implementation by a junior engineer.

Red flags;
- Specs/Epics/Stories written short, and not covering the PRD comprehensively
- Missing error state (including no retry action option), null state, live browser (where applicable) validation
- A design system, theming solution, or component library is not used (when we touch UIs)
