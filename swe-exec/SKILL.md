---
name: swe-exec
description: Execute and implement a story, feature, epic, or PRD end-to-end by loading `.swe` planning artifacts (stories, epics, tech spec, proposal), maintaining a `.next.md` execution log, implementing stories sequentially, and marking completed artifacts with a `-done` filename suffix. Use when a user points to a story file under `.swe/stories/<feature-slug>/` or asks you to “implement/execute” a feature defined in `.swe`.
---

# SWE Exec

## Objective

Turn `.swe` planning artifacts into working code by:

- Rebuilding context from `.swe` files whenever needed.
- Implementing `.swe/stories/<feature-slug>/` in numeric order as small, reviewable vertical slices.
- Keeping the proposal branch locally green with story-level validation and commits.
- Tracking decisions/status in `.swe/stories/<feature-slug>/.next.md`.
- Renaming completed artifacts with `-done` in the filename.

## Inputs and path conventions

- Stories live under: `.swe/stories/<feature-slug>/`
  - Story files are numbered: `.swe/stories/<feature-slug>/001-<story>.md`
  - When finished, rename to: `.swe/stories/<feature-slug>/001-<story>-done.md`
- Tech specs live under: `.swe/specs/`
  - Match: `.swe/specs/TSD-00X-<feature-slug>.md` (if multiple, prefer highest `00X`)
  - When done (after user verification), rename to: `.swe/specs/TSD-00X-<feature-slug>-done.md`
- Test specs live under: `.swe/specs/`
  - Match: `.swe/specs/TST-00X-<feature-slug>.md` (if multiple, prefer highest `00X`)
  - Read before implementation so story acceptance maps to E2E test IDs and data isolation requirements.
- Epics live under: `.swe/epics/<feature-slug>/` (read all)
- Proposals/PRDs:
  - If present, read the matching proposal under `.swe/proposals/PROPOSAL-00X-<Short-Slug>.md`.
  - If `.swe/proposals/` doesn’t exist, also check `.swe/proposals/` (common alternative).
  - When done (after user verification), rename to: `PROPOSAL-00X-<Short-Slug>-done.md`
- Company/Product Context live under: `.swe/context/` (read all, including sub folders/files)

## Workflow

Read repo-local standards first (don't skip, full file):
- AGENTS.md, CLAUDE.md, DESIGN.md, .github/copilot-instructions.md
- Coding/contribution standards (if present)

0. Prepare the branch and validation model
   - Run `git status --short` and identify the current branch before editing.
   - Work on one proposal/feature branch per proposal. If no suitable branch exists, create a branch named from the proposal or feature slug before implementation.
   - If the worktree has unrelated uncommitted changes, do not move or rewrite them. Continue only when you can avoid touching them, or ask the user how to proceed.
   - Keep the branch locally green. Do not push or open a PR until build, lint/typecheck, and the required E2E tier pass locally.
   - Commit each completed story independently after its validation gate passes. Use the proposal branch as the integration branch for those story commits.

1. Resolve what to execute
   - Prefer a concrete input like a story path: `.swe/stories/<feature-slug>/00N-<story>.md`.
   - If the user provides only an epic/PRD, locate the corresponding `<feature-slug>` by searching `.swe/stories/` and asking for confirmation.
   - Extract `<feature-slug>` from the story path (the directory name under `.swe/stories/`).

2. Rebuild the execution context (do this at the start and whenever context is compacted)
   - Read, in this order (when they exist):
     1) Proposal (matching `PROPOSAL-00X-<Short-Slug>.md`)
     2) Tech spec: `.swe/specs/TSD-00X-<feature-slug>.md`
     3) Test spec: `.swe/specs/TST-00X-<feature-slug>.md`
     4) All epics: every file under `.swe/epics/<feature-slug>/`
     5) Existing decision log: `.swe/stories/<feature-slug>/.next.md` (if present)
     6) Current story being implemented
   - If any of these are missing, note the gap in `.next.md` and proceed if possible.
   - If the TST is missing for feature work, create or request an independent `swe-tdd` pass before implementing user-facing stories.

3. Create/update the decision log: `.swe/stories/<feature-slug>/.next.md`
   - Ensure `.swe/stories/<feature-slug>/.next.md` exists.
   - Keep it short and current; update it after every meaningful change.
   - Recommended sections:
     - `# <feature-slug> — Execution Log`
     - `## Status` (what’s in progress, what’s blocked)
     - `## Decisions` (what you chose and why)
     - `## Implementation Notes` (key files changed, migrations, flags)
     - `## Next` (the next concrete step)
     - `## Done` (completed stories list)

4. Implement stories sequentially
   - List story files under `.swe/stories/<feature-slug>/` and sort by numeric prefix (`001`, `002`, …).
   - Create a checklist plan with each story name, and create a plan to implement it
   - Start at `001-...`. Act like a FAANG Principal Engineer implement one story at a time until all stories are done.
   - Skip any story already suffixed `-done`.
   - For each story:
     - Re-read the story and capture acceptance criteria in `.next.md`.
     - Confirm the story is a vertical, independently reviewable slice. If it is too large to validate and commit cleanly, split it before implementation and update `.next.md`.
     - For UI tasks, imagine the experience you are going to build, and the detailed UI layout, and flows
     - Act like a FAANG Principal Engineer, and update plan to include sub plan for this story. (# Plan Story 001XXX Subtask 001-001XXX)
     - Act like a FAANG Principal Engineer, and implement the code changes needed to satisfy the story.
     - Prefer user-facing E2E tests for acceptance. Use unit tests only for backend-heavy business logic where a browser cannot exercise the behavior directly, and API tests only for API-only user surfaces.
     - Run the story validation gate: format if repo-standard, lint, typecheck/build, and the smallest E2E tier that proves the acceptance criteria against a running app.
     - Fix failures caused by your changes before continuing to the next story.
     - Record the exact validation commands and results in `.next.md`.
     - When validation is complete, rename the story file to include `-done` in the filename.
     - Update `.next.md` with what changed and what story is next.
     - Commit the story's code, test, artifact, `.next.md`, and story rename changes to the proposal branch after validation passes.
   - Continue sequentially only while each story remains small, independently validated, and committed. Do not accumulate many uncommitted stories.

5. Finalize after all stories are implemented
   - Reuse the same owned stack for the current worktree when possible, use your browser skills, and verify all of the changes.
   - Run full branch validation before PR: build, lint/typecheck, targeted impacted E2E, and full regression E2E only when the change crosses sensitive or broad product boundaries.
   - Make sure PRD, and Spec is fully implemented. 
   - Only after verification:
     - Rename the tech spec to add `-done`.
     - Rename the proposal/PRD to add `-done`.
   - Record the verification and final status in `.next.md`.

6. Check if there are stories left unimplemented for given folder
   - Create a plan to implement remaining stories as independently green commits on the proposal branch.
   - Continue only while each story can be validated, committed, and kept small. If scope or validation risk would create a large unreviewable batch, stop and report the risk before proceeding.

7. When you are done, test all the implementation against to the .swe/specs/TST-00X-<feature-slug>.md
   - Write and run Playwright/Selenium/Cypress or other E2E tests to test end-to-end user flows and business value in a real user environment.
   - Use test tiers:
     - Smoke: login/health and one critical path for fast confidence.
     - Impacted: E2E tests mapped to the current story and changed surfaces.
     - Full regression: run before PR or for broad/sensitive changes; do not run after every tiny edit unless required.
   - Identify gaps
   - Close gaps

## E2E Runtime and Data Rules

- Build once and start the stack once for the current worktree when feasible; reuse the same base URL for all story E2E tiers.
- Do not hardcode ports or ask the user to choose ports. Wire ports behind the scenes by discovering free ports or using repo-supported env vars, then pass the resolved base URL to tests.
- Record stack ownership metadata when starting or reusing a local stack:
  - absolute worktree root from `pwd`
  - stack start timestamp
  - base URL and dynamically assigned ports
  - process/container IDs or labels
  - start command and readiness check
- Pass ownership metadata to every E2E run, for example `E2E_WORKTREE_ROOT`, `E2E_STACK_STARTED_AT`, `E2E_RUN_ID`, and `BASE_URL`.
- Do not restart the environment per test file, worker, retry, story, or commit unless the repo architecture requires it.
- Prefer incremental updates before restart: hot reload, targeted service restart, migration apply, Hasura metadata apply, schema refresh, or cache clear.
- Kill/recreate only when incremental repair fails, ownership metadata proves the stack belongs to the same worktree, or the change explicitly requires a clean runtime.
- If recorded stack `pwd` differs from the current worktree root, do not interact with or kill it.
- If recorded `pwd` matches and timestamp matches, reuse it.
- If recorded `pwd` matches but a newer healthy stack timestamp exists, treat older runs as ghosts and clean up only processes/containers proven to belong to the same worktree and older timestamp.
- If parallel agents or runners need external access, expose the one shared local stack with a tunnel such as Cloudflare Tunnel or ngrok, but keep test data isolated by namespace.
- Every E2E run must create its own resources: users, super-admin credentials, orgs, groups, projects, feature flags, and domain data required by the scenario.
- Generate a unique namespace from worktree hash, branch, commit, worker index, test file, and a timestamp/random suffix. Apply it to emails, org names, slugs, external IDs, and cleanup tags.
- Never share mutable credentials, browser storage state, orgs, groups, or seeded records across parallel workers unless the test explicitly validates collaboration.
- Clean up test-owned resources in `afterEach`/`afterAll` or the repo's equivalent. Add a TTL/fallback cleanup path for crashed test runs.
- Parallel workers must use isolated browser contexts and worker-scoped auth/storage state.
- Prefer deterministic waits, roles/labels/test IDs, and explicit user-visible assertions. Avoid sleeps and brittle CSS selectors.

## Code Quality Gate

- Follow repo coding standards and existing architecture. Do not generate massive files or code dumps.
- Keep functions <=50 lines preferred; >100 requires refactor discussion. Keep cyclomatic complexity <=10; >15 requires justification.
- Keep files <=400 lines preferred; >800 requires an ownership/refactor plan. Split components/services/helpers before files become god objects.
- Reject big-ball-of-mud, golden-hammer, magic, tight-coupling, premature-optimization, and not-invented-here designs.
- Avoid deep nesting >4 levels, duplicated code, hardcoded values, missing error/retry handling, performance bottlenecks, and API calls in unbounded loops.
- For UI changes, include null/empty/error states with recovery CTA, plus stable `data-testid` and `data-pendo` tags for test and analytics surfaces.
- Do not merge or mark done with critical/high security findings.

## Operating rules

- Use your best judgment for missing requirements.
- Prefer small, reviewable diffs per story; keep changes scoped to the current story.
- Use repository-native scripts/commands for build/test/lint when available.
- For renames in a git repo, prefer `git mv` (or an equivalent safe rename) so history is preserved.
- When you are done with a task, for example 001, check the next one in the sequence, 002, and there is next task in the sequence, continue with the execution of the next story
- Never mark a story `-done` without local validation evidence in `.next.md`.
- Never open a PR for a branch that is not locally green unless the user explicitly asks for a failing draft and the failure is documented.

For user interfaces;
Viewport budget:

- If the first screen includes a sticky/fixed header, that header counts against the hero. The combined header + hero content must fit within the initial viewport at common desktop and mobile sizes.
- When using `100vh`/`100svh` heroes, subtract persistent UI chrome (`calc(100svh - header-height)`) or overlay the header instead of stacking it in normal flow.

## Apps

Default to Linear-style restraint:

- calm surface hierarchy
- strong typography and spacing
- few colors
- dense but readable information
- minimal chrome
- cards only when the card is the interaction

For app UI, organize around:

- primary workspace
- navigation
- secondary context or inspector
- one clear accent for action or state

Avoid:

- dashboard-card mosaics
- thick borders on every region
- decorative gradients behind routine product UI
- multiple competing accent colors
- ornamental icons that do not improve scanning

If a panel can become plain layout without losing meaning, remove the card treatment.

## Imagery

Imagery must do narrative work.

- Use at least one strong, real-looking image for brands, venues, editorial pages, and lifestyle products.
- Prefer in-situ photography over abstract gradients or fake 3D objects.
- Choose or crop images with a stable tonal area for text.
- Do not use images with embedded signage, logos, or typographic clutter fighting the UI.
- Do not generate images with built-in UI frames, splits, cards, or panels.
- If multiple moments are needed, use multiple images, not one collage.

The first viewport needs a real visual anchor. Decorative texture is not enough.

## Copy

- Write in product language, not design commentary.
- Let the headline carry the meaning.
- Supporting copy should usually be one short sentence.
- Cut repetition between sections.
- do not include prompt language or design commentary into the UI
- Give every section one responsibility: explain, prove, deepen, or convert.

If deleting 30 percent of the copy improves the page, keep deleting.

## Utility Copy For Product UI

When the work is a dashboard, app surface, admin tool, or operational workspace, default to utility copy over marketing copy.

- Prioritize orientation, status, and action over promise, mood, or brand voice.
- Start with the working surface itself: KPIs, charts, filters, tables, status, or task context. Do not introduce a hero section unless the user explicitly asks for one.
- Section headings should say what the area is or what the user can do there.
- Good: "Selected KPIs", "Plan status", "Search metrics", "Top segments", "Last sync".
- Avoid aspirational hero lines, metaphors, campaign-style language, and executive-summary banners on product surfaces unless specifically requested.
- Supporting text should explain scope, behavior, freshness, or decision value in one sentence.
- If a sentence could appear in a homepage hero or ad, rewrite it until it sounds like product UI.
- If a section does not help someone operate, monitor, or decide, remove it.
- Litmus check: if an operator scans only headings, labels, and numbers, can they understand the page immediately?

## Motion

Use motion to create presence and hierarchy, not noise.

Ship at least 2-3 intentional motions for visually led work:

- one entrance sequence in the hero
- one scroll-linked, sticky, or depth effect
- one hover, reveal, or layout transition that sharpens affordance

Prefer Framer Motion when available for:

- section reveals
- shared layout transitions
- scroll-linked opacity, translate, or scale shifts
- sticky storytelling
- carousels that advance narrative, not just fill space
- menus, drawers, and modal presence effects

Motion rules:

- noticeable in a quick recording
- smooth on mobile
- fast and restrained
- consistent across the page
- removed if ornamental only

## Hard Rules

- No cards by default.
- No hero cards by default.
- No boxed or center-column hero when the brief calls for full bleed.
- No more than one dominant idea per section.
- No section should need many tiny UI devices to explain itself.
- No headline should overpower the brand on branded pages.
- No filler copy.
- No split-screen hero unless text sits on a calm, unified side.
- No more than two typefaces without a clear reason.
- No more than one accent color unless the product already has a strong system.

## Reject These Failures

- Generic SaaS card grid as the first impression
- Beautiful image with weak brand presence
- Strong headline with no clear action
- Busy imagery behind text
- Sections that repeat the same mood statement
- Carousel with no narrative purpose
- App UI made of stacked cards instead of layout

Overall Red Flags
- There are stories left under the folder unimplemented
- There are gaps in the implementation
- You broke different features
- Not good user experience
- Not good Interface design
- Broken layouts
- Responsiveness issues
- You haven't tested Ui related changes your headless browser skill (where skill exists)
- Error messages caused by poor UX implementation
- Missing url routing
- No motion (motion.dev or similar) or other elements to please the user.
