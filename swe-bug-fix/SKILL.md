---
name: swe-bug-fix
description: Diagnose and fix a reproducible bug, regression, runtime error, failing test, or broken user flow in an existing codebase. Use when the user asks to debug or fix something, shares an error message or stack trace, reports a regression, or wants a failing test/build restored.
---

# Bug Fix

## Goal

Turn a concrete failure signal into a validated fix with minimal regression risk.

## Inputs

- Preferred:
  - Reproduction steps
  - Failing command or test
  - Error output, logs, stack traces, screenshots, or recordings
  - Expected behavior and actual behavior
- If the report is vague, first extract:
  - User-visible symptom
  - Scope and affected surface area
  - Recent change boundary, if known
  - Environment, flags, or data prerequisites

## Outputs

- Working code change
- Reproduction and validation evidence
- Concise root-cause summary
- Residual risks, assumptions, or follow-up work if the fix is partial

## Workflow

### 1) Bound the failure before editing

- Reproduce the bug with the smallest reliable command, test, or user flow you can find.
- Write down:
  - Expected behavior
  - Actual behavior
  - Exact failure signal
  - Preconditions required to trigger it
- If you cannot reproduce it, do not guess. Gather more signal first.

### 2) Build evidence

- Inspect the closest entry points, call sites, contracts, configuration, and recent changes.
- Trace the failing path end to end instead of patching the first symptom you see.
- Distinguish:
  - Product bug
  - Test fixture issue
  - Environment/config drift
  - Flaky timing or data dependency
- When the repo has tests, prefer adding or locating a deterministic failing test before the fix.
- For user-facing bugs, prefer a browser-level reproduction or E2E check that proves the broken product flow. Use unit tests for backend-heavy business logic and API tests for API-only surfaces or setup helpers.

### 3) Identify the root cause

- Form an evidence-backed hypothesis.
- Verify the bug exists at the boundary where behavior first becomes wrong.
- Consider edge cases:
  - Null or empty data
  - Retries and duplicate actions
  - Permission differences
  - Async ordering
  - Version/config mismatches
- If multiple root causes are plausible, prove which one is real before changing code.

### 4) Fix the right boundary

- Make the smallest change that fully resolves the bug at its source.
- Preserve existing architecture and repo conventions unless the bug is caused by the pattern itself.
- Avoid speculative cleanup or unrelated refactors during the fix.
- For user-facing bugs, make sure the resulting UX still handles:
  - Loading states
  - Error states
  - Empty states
  - Recovery actions

### 5) Validate broadly

- Re-run the original reproduction.
- Run the smallest relevant validation set first, then widen if the change crosses boundaries:
  - Targeted browser/E2E checks for user-facing behavior
  - Targeted unit/API tests where they verify the true failing boundary
  - Build/lint/typecheck
  - Adjacent integration or E2E coverage
- Check nearby paths that could regress because of the same contract or state change.
- If the bug touched data or migrations, validate backward compatibility and rollback behavior.
- Load the impacted user personas (if applicable) get feedback, and iterate if necessary until they are satisfied with the result (the scope is limited to current issue. Feel free to file another story/bug if they as something else)

### 6) Close out cleanly

- Summarize:
  - Root cause
  - What changed
  - How it was validated
  - Remaining risks or unknowns
- If you could not fully validate locally, say exactly what remains unverified.

## Operating Rules

- Prefer a failing automated check before the fix when practical, but do not invent brittle tests.
- Reuse an already running local stack for browser/E2E validation when possible, but only when ownership metadata proves it belongs to the current worktree. Auto-wire ports behind the scenes, prefer incremental updates, and never kill a stack owned by a different `pwd`. Keep any test-created users/data isolated and cleaned up.
- Keep fixes small and idiomatic: functions <=50 lines preferred, files <=400 lines preferred, complexity <=10, no unbounded API calls in loops, and no critical/high security findings.
- Do not silently convert an uncertain diagnosis into a code change.
- Do not stop at “the test passes” if adjacent real-world flows are still at risk.
- Keep the fix scoped, but do not leave obvious contract mismatches behind.

## Red Flags
- Unnecessary refactor
