---
name: swe-spec
description: Translate an existing PRD/proposal into a principal-architect-level technical specification and implementation epics, aligned to repo/company standards and best practices. Use when a user asks to “write a tech spec”, “create a technical design/spec”, “turn this PRD into a technical spec”, or “derive epics” for a feature.
---

# SWE Spec

## Goal

Turn a PRD into:

- A high-quality technical specification document (architecture + detailed design + rollout/testing).
- A set of implementation epics with clear scope and acceptance criteria.

## Inputs

- A PRD/proposal file path (preferred) or pasted PRD text.
  - Typical locations: `proposals/`, `.swe/proposals/`.
- Repo context and standards (when available):
  - `.swe/context/**` (company/product briefs, personas, etc.)
  - `docs/`, `README*`, `ARCHITECTURE*`, `CONTRIBUTING*`, `adr/`, `decisions/`, `rfcs/`, `.github/`

## Outputs

Create/update the following files:

- Tech spec: `.swe/specs/TSD-00X-<feature-slug>.md`
- Epics: `.swe/epics/<feature-slug>/EPIC-00X-<epic-slug>.md`
- Stories: `.swe/stories/<feature-slug>/STORY-00X-<story-slug>.md`

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

### 3) Load skill assets

- Read `assets/TECH-SPEC-BEST-PRACTICES.md` and use it as your quality bar and checklist.
- Read `assets/TECH-SPEC-TEMPLATE.md` and use it as the starting structure for the spec.

### 4) Plan integration points
4. Create a deep codebase analysis plan (before Tech Spec)
   • Produce a deep analysis plan (15–30 bullets) that explains how you will understand:
      •	the current product behavior,
      •	the actual codebase architecture, and
      •	the exact integration points required for the upcoming Tech Spec.
      •	Ingest product context and historical decisions
      •	Read anything under .swe/context/ (if present).
      •	Read anything under .swe/proposals/ (if present), prioritizing the most recent proposals to learn prior tradeoffs and constraints.
      •	If .swe/proposals/ does not exist, proceed without failing.
      •	Map the repo topology and ownership boundaries
      •	Determine if this is a monorepo vs multi-repo vs single app, and list major packages/services.
      •	Identify frontend/backend/services, shared libraries, internal SDKs, and “glue” layers.
      •	Identify bounded contexts / domains (e.g., billing, auth, chat, search, documents) and where each lives in code.
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
      •	Create a short artifact under: .swe-cache/tech-analysis/ANALYSIS-00X-<Short-Slug>.md containing:
      •	Architecture snapshot (components + responsibilities)
      •	Integration inventory (APIs, events, jobs, external deps)
      •	Dependency graph (at least high-level)
      •	Key flows (sequence-style bullets)
      •	Data model touchpoints (tables/collections/indexes)
      •	Risk list + unknowns (with planned validation steps)
      • Tests that neds to be created/updated
      • Integration points with existing APIs/Components
      •	This artifact becomes the source of truth for the upcoming Tech Spec.
      •	Hard requirement: reflect analysis in the Tech Spec
    •	When writing the Tech Spec, you must:
      •	explicitly reference the discovered integration points,
      •	name the impacted modules/services,
      •	describe relationship boundaries,
      •	and ensure proposed design aligns with existing patterns found in the repo.
      •	If evidence is missing, clearly label assumptions and add a “Validation Plan” section.
      •	Suggested files/folders to inspect (when present)
      •	README*, docs/, package.json, go.mod, pyproject.toml, requirements.txt, Cargo.toml
      •	Dockerfile, docker-compose.yml, .github/workflows/
      •	k8s/, helm/, terraform/, infra/, .env*
      •	plus: src/, apps/, services/, packages/, libs/, cmd/, internal/, api/, migrations/ (if they exist)

### 5) Write the technical specification (principal architect mode)
- Read `.swe-cache/tech-analysis/ANALYSIS-00X-<Short-Slug>.md`, all of it.
- Create `.swe/specs/` if needed.
- Create/update `.swe/specs/TSD-00X-<feature-slug>.md` using the template.
- Requirements traceability:
  - Map each PRD requirement/acceptance criterion to concrete design elements (APIs, jobs, data changes, UI).
  - Call out open questions explicitly (do not hide uncertainty).
- Architecture quality:
  - Include at least one diagram when helpful (Mermaid is preferred).
  - Present 1–3 viable options when meaningful; pick one and justify trade-offs.
  - Cover security/privacy, performance, observability, migrations, rollout/rollback, and testing.
- Style:
  - Act like a principal engineer
  - Be crisp, concrete, and decisive.
  - Prefer tables/checklists for scannability.
  - Avoid hand-wavy phrases (“just”, “simply”, “etc.”).

### 6) Spec quality pass

- Act like another Principal Engineer, and review the tech spec against `assets/TECH-SPEC-BEST-PRACTICES.md`, and against the original PRD and fix gaps.
- Do another round of pass against the original PRD and fix gaps
- Ensure outputs are created exactly under `.swe/specs/`.

### 5) Create a test SPEC
- Act like a Principal Software Engineer in Test
- Write a Test Spec Similar to the Tech Spec you just wrote
- Include real life user usecases, and important business logic, primarily tested in Playwright, run against the running server

### 5) Create epics from the spec

- Create `.swe/epics/<feature-slug>/` if needed.
- Derive a set of epics (usually 1–20 depending on the size, and edge cases) that cover end-to-end delivery.
- For each epic:
  - Choose the next incremental `EPIC-00X` by scanning existing epic files in the folder.
  - Create `EPIC-00X-<epic-slug>.md` and break down the PRD/Tech Spec section
- Create test Epics testing the delivery

### 7) Epic quality pass

- Review the spec against `assets/TECH-SPEC-BEST-PRACTICES.md`, the original PRD and fix gaps.
- Do another round of pass against the original PRD and fix gaps by creating more epics, or updating existing epics
- Ensure outputs are created exactly under `.swe/epics/<feature-slug>/`.

### 8) Create stories from the spec, and epics

- Create `.swe/stories/<feature-slug>/` if needed.
- Derive a set of stories (usually 1–20 depending on the size, and edge cases) that cover end-to-end delivery.
- For each story:
  - Choose the next incremental `STORY-00X` by scanning existing epic files in the folder.
  - Create `STORY-00X-<epic-slug>.md`
  - Act like a principal TPM, and break down the PRD/Epic section to story using storywriting best practices
- Continue until all of the epics are broken down

### 9) Story quality pass
- Compact your context
- Read everything under `.swe/context`, `.swe/epics/<feature-slug>/` It's long, but It's important to build the context. 
- Start from the first story, and do this for each story; Review the story against the PRD/Epic, and fix gaps by updating the story, or creating a new story.
- Do final pass, and make sure stories are coverting everything under the PRD, Tech Spec, and the Epic that is part of
- Ensure outputs are created exactly under `.swe/stories/<feature-slug>/`

### 10) Implementation quality pass
- Read everything under `.swe/context`, `.swe/epics/<feature-slug>/`, `.swe/stories/<feature-slug>/`, `.swe/specs/TSD-00X-<feature-slug>.md`, `.swe-cache/tech-analysis/ANALYSIS-00X-<Short-Slug>.md` It's long, but It's important to build the context.
- Identify integration risks, potetial things that we broke during the integration, and fix them
- If UI is involved Do final pass testing using your browser mcp skills like Chrome MCP to bring the app up, take screenshots, and test it, and make sure stories are coverting everything under the PRD, Tech Spec, and the Epic that is part of, and none of the existing features are broken by this change

Notes:
This is a full feature execution. It's a big task, and It will take time. You have the time, and resources. You are smart, use your best jugment to unblock yourself when you feel like there is a blocker. Continue non stop until all of the stories are executed.