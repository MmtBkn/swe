---
name: swe-ux-ui
description: Create or evolve UI designs in Google Stitch for the current repo by resolving a repo-scoped Stitch project from the root `package.json`, continuing existing product designs from screenshots when appropriate, and generating or editing screens with the strongest available Gemini model while balancing persona needs and developer intent. Use when a user asks to design a new screen or flow, continue an existing UI, create mockups, edit Stitch screens, create/apply a design system, or manage Stitch-based UX/UI work for the current project.
---

# SWE UX UI

## Goal

Turn product intent into usable, implementation-aware UI designs in Google Stitch (or other tools you have access to such as Figma AI), then validate the outcome with persona review before considering the design work complete.

## Inputs

- Design request
  - new screen, new flow, screen edits, variants, uploaded mockups, design system work
- Optional Stitch identifiers
  - `projectId`, project resource name, screen IDs, design system asset ID
- Optional product context
  - PRD/spec/story paths
  - persona file paths
  - screenshots or mockups
  - device targets
  - developer constraints such as component library, brand, accessibility, responsiveness, or implementation preferences

## Tool Map

- Project resolution: `list_projects`, `get_project`, `create_project`
- Screen inventory: `list_screens`, `get_screen`
- New design: `generate_screen_from_text`
- Edit existing design: `edit_screens`
- Import existing mockups: `upload_screens_from_images`
- Explore options: `generate_variants`
- Design system: `list_design_systems`, `create_design_system`, `update_design_system`, `apply_design_system`

## Workflow

### 1) Build the design brief

- Read the user request carefully.
- If the request points to a PRD, spec, story, or bug, read that first.
- If the request references personas, read the persona file(s).
- Extract:
  - target user and jobs-to-be-done
  - primary task flow
  - trust, accessibility, and density needs
  - device target
  - developer intent and implementation constraints
- If the request is ambiguous about which screen or flow to design, ask one concise question.

### 2) Determine greenfield versus existing product

- Classify the work before touching Stitch:
  - greenfield: no meaningful existing UI to preserve
  - existing product: there is already a shipped, staged, or locally running UI that this work extends or revises
- Treat the work as existing product when any of these are true:
  - the request mentions redesign, refresh, polish, refactor, bug fix, or continue
  - the repo already contains the feature
  - screenshots, mockups, or a running app are available
- For existing-product work, prefer continuing from the current design rather than replacing it blindly.

### 3) Resolve the Stitch project

- If the user gave a `projectId` or resource name, use it.
- Otherwise:
  - read the root `package.json`
  - derive the canonical project title from `package.json.name`
  - if `package.json.name` is missing, fall back to the repo folder name
- Prefer a local cache when present:
  - `.swe/context/design/stitch-project.json`
- If that cache exists, verify it with `get_project`.
- If no valid cached project exists:
  - call `list_projects` for owned projects
  - match on normalized title first
  - if the user explicitly mentions a shared project, also inspect shared projects
- If no matching project exists, call `create_project` with the derived title.
- After resolving a project, write or update `.swe/context/design/stitch-project.json` with:
  - `projectId`
  - `projectName`
  - `title`
  - `sourcePackageName`

### 4) Inventory current UI work before changing anything

- Call `list_screens` for the resolved project.
- Summarize existing screens before creating new ones.
- If a requested screen already exists or is close, prefer editing or variant generation instead of creating duplicates.
- Use `get_screen` when you need details, screenshots, HTML, or export references for a specific screen.

### 5) Continue existing products from screenshots when possible

- For existing-product work, gather visual source material first.
- Prefer this order:
  - existing Stitch screens in the resolved project
  - user-provided screenshots or mockups
  - screenshots captured from the current app or local dev server
- If the current UI exists outside Stitch, import screenshots with `upload_screens_from_images` before editing so the new work starts from the real baseline.
- Treat uploaded or edited screens as the continuation path for future iterations.

### 6) Resolve or create the design system

- Call `list_design_systems` for the project.
- If a relevant design system exists, reuse it.
- If none exists and the task is more than a one-off mockup, create one before generating screens.
- Build the design system from the strongest available evidence:
  - existing product branding
  - repo design tokens or CSS variables when the user points to them
  - component library constraints
  - persona needs
  - explicit user direction
- Prefer updating one project design system over creating many overlapping ones.
- Apply the chosen design system to edited or generated screens when consistency matters.

### 7) Pick the right Stitch action

- New screen or new flow: `generate_screen_from_text`
- Modify existing screens or imported baselines: `edit_screens`
- Import screenshots or wireframes first: `upload_screens_from_images`, then `edit_screens` if needed
- Generate alternative approaches: `generate_variants`
- Restyle to a shared look and feel: `apply_design_system`

### 8) Build a strong prompt

- Be concrete. Avoid vague prompts like "make it modern" or "clean it up".
- Include:
  - screen purpose
  - primary persona and any secondary personas
  - top tasks and success criteria
  - required sections and CTAs
  - empty, loading, error, and recovery states when relevant
  - trust or compliance cues
  - device target
  - visual direction and brand constraints
  - implementation constraints developers care about
- If persona needs and developer desires conflict, surface the tradeoff and bias toward user success unless the user explicitly prioritizes another constraint.

### 9) Model and device selection

- Prefer the strongest quality model exposed by the Stitch tools.
- Default to `GEMINI_3_PRO` for primary generation and substantial edits.
- Use a newer stronger model only if the tool explicitly exposes it.
- Use `GEMINI_3_FLASH` only for lower-cost, faster iteration when quality risk is acceptable.
- Set `deviceType` deliberately:
  - `MOBILE` for phone-first flows
  - `DESKTOP` for desktop-first work
  - `TABLET` when explicitly needed
  - `AGNOSTIC` only when the design is intentionally cross-device

### 10) Start small and expand deliberately

- Do not try to generate an entire product in one pass.
- If Stitch supports multiple-screen generation, start with the smallest coherent batch that proves the direction.
- Default approach:
  - start with 1 focal screen when refining an existing screen
  - start with 2 screens for a new flow when two connected states materially improve quality
  - add more screens only after inspecting the first output
- Expand in steps until the full ask is covered.

### 11) Treat edits as additive outputs

- Do not assume `edit_screens` mutates screens in place.
- Track original screen IDs and any newly returned screen IDs separately.
- When an edit creates new screens, treat the new screens as the latest revision set and keep the lineage clear in your summary.
- Avoid repeated edits against stale screen IDs.

### 12) Handle long-running generation safely

- `generate_screen_from_text`, `edit_screens`, and `generate_variants` can take a few minutes.
- Do not retry just because the connection fails or times out.
- After waiting, inspect the result with `get_screen` or `list_screens`.
- If Stitch returns suggestions in output components, show the suggestions to the user and, if accepted, use the suggestion as the next prompt.

### 13) Run persona review before calling the work complete

- After the design direction is produced, run `swe-user-persona-review`.
- Provide the reviewer:
  - persona file path(s)
  - the design request
  - generated or edited screen references
  - screenshots or exports when available
  - relevant PRD/spec/story links
- If the persona review finds material issues, iterate in Stitch and review again.
- Do not stop after the first generation if the end-to-end ask is not actually satisfied.

### 14) Validate end to end before returning

- Confirm:
  - the resolved Stitch project is correct
  - the generated or edited screens cover the user’s ask
  - the design system is aligned or intentionally omitted
  - persona-review feedback has been addressed or clearly left open
  - there are no obvious missing states for the requested scope

### 15) Close out with concrete artifacts

- Return:
  - resolved or created Stitch project
  - existing screens inventoried
  - screens uploaded, created, edited, or variant-generated
  - design system created, updated, or applied
  - prompt summary used
  - persona-review outcome
  - next recommended design actions

## Output Expectations

- Always report the Stitch project used.
- For edits or new screens, include the screen resource names or IDs and call out which are latest revisions.
- If you could not resolve a project or design system confidently, say exactly why.
- If Stitch MCP is unavailable in the environment, stop and report that instead of pretending the integration exists.

## Guardrails

- Never call `delete_project` unless the user explicitly asks and confirms.
- Do not create duplicate projects for the same repo when a matching project already exists.
- Do not create duplicate screens when a targeted edit, upload, or variant is sufficient.
- Do not ignore persona needs just because a developer preference was mentioned.
- Do not ignore developer constraints when they materially affect feasibility or consistency.
