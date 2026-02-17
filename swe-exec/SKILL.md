---
name: swe-exec
description: Execute and implement a story, feature, epic, or PRD end-to-end by loading `.swe` planning artifacts (stories, epics, tech spec, proposal), maintaining a `.next.md` execution log, implementing stories sequentially, and marking completed artifacts with a `-done` filename suffix. Use when a user points to a story file under `.swe/stories/<feature-slug>/` or asks you to “implement/execute” a feature defined in `.swe`.
---

# SWE Exec

## Objective

Turn `.swe` planning artifacts into working code by:

- Rebuilding context from `.swe` files whenever needed.
- Implementing `.swe/stories/<feature-slug>/` in numeric order.
- Tracking decisions/status in `.swe/stories/<feature-slug>/.next.md`.
- Renaming completed artifacts with `-done` in the filename.

## Inputs and path conventions

- Stories live under: `.swe/stories/<feature-slug>/`
  - Story files are numbered: `.swe/stories/<feature-slug>/001-<story>.md`
  - When finished, rename to: `.swe/stories/<feature-slug>/001-<story>-done.md`
- Tech specs live under: `.swe/specs/`
  - Match: `.swe/specs/TSD-00X-<feature-slug>.md` (if multiple, prefer highest `00X`)
  - When done (after user verification), rename to: `.swe/specs/TSD-00X-<feature-slug>-done.md`
- Epics live under: `.swe/epics/<feature-slug>/` (read all)
- Proposals/PRDs:
  - If present, read the matching proposal under `.swe/proposals/PROPOSAL-00X-<Short-Slug>.md`.
  - If `.swe/proposals/` doesn’t exist, also check `.swe/proposals/` (common alternative).
  - When done (after user verification), rename to: `PROPOSAL-00X-<Short-Slug>-done.md`
- Company/Product Context live under: `.swe/context/` (read all, including sub folders/files)

## Workflow

1. Resolve what to execute
   - Prefer a concrete input like a story path: `.swe/stories/<feature-slug>/00N-<story>.md`.
   - If the user provides only an epic/PRD, locate the corresponding `<feature-slug>` by searching `.swe/stories/` and asking for confirmation.
   - Extract `<feature-slug>` from the story path (the directory name under `.swe/stories/`).

2. Rebuild the execution context (do this at the start and whenever context is compacted)
   - Read, in this order (when they exist):
     1) Proposal (matching `PROPOSAL-00X-<Short-Slug>.md`)
     2) Tech spec: `.swe/specs/TSD-00X-<feature-slug>.md`
     3) All epics: every file under `.swe/epics/<feature-slug>/`
     4) Existing decision log: `.swe/stories/<feature-slug>/.next.md` (if present)
     5) Current story being implemented
   - If any of these are missing, note the gap in `.next.md` and proceed if possible.

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
   - Start at `001-...`. Act like a FAANG Principal Engineer implement one story at a time until all stories are done.
   - Skip any story already suffixed `-done`.
   - For each story:
     - Re-read the story and capture acceptance criteria in `.next.md`.
     - Act like a FAANG Principal Engineer, and implement the code changes needed to satisfy the story.
     - Run the smallest validating command(s) available (tests/build/lint or other commands like kubectl deploy or `npx nx serve segments --configuration=online`) and fix failures caused by your changes.
     - When the validation is complete, Rename the story file to include `-done` in the filename.
     - Update `.next.md` with what changed and what story is next.
   - Continue non stop until all of the stories are implemented

5. Finalize after all stories are implemented
   - Run stack locally, use your browser skills and verify all of the changes.
   - Make sure PRD, and Spec is fully implemented. 
   - Only after verification:
     - Rename the tech spec to add `-done`.
     - Rename the proposal/PRD to add `-done`.
   - Record the verification and final status in `.next.md`.

6. When you are done, test all of the implementation against to the .swe/specs/TST-00X-<feature-slug>.md
   - Write and run playwright/selennium or other e2e tests to test end to end user flows and business value in real user environment 
   - Identify gaps
   - Close gaps

## Operating rules

- Use your best judgement for missing requirements.
- Prefer small, reviewable diffs per story; keep changes scoped to the current story.
- Use repository-native scripts/commands for build/test/lint when available.
- For renames in a git repo, prefer `git mv` (or an equivalent safe rename) so history is preserved.
