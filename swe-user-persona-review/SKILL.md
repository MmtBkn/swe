---
name: swe-user-persona-review
description: Review a PRD, technical spec, story, design artifact, live feature, or bug fix from one or more user personas defined in a persona file. Use when a user wants persona-based feedback, asks you to "act like" a target user, wants design critique based on screenshots instead of code, or wants live browser validation of a local feature or fix as impacted personas. When multiple personas or auth states are involved, run isolated fresh-context reviews in parallel so browser state does not leak across personas.
---

# SWE User Persona Review

## Goal

Produce grounded feedback from the perspective of real users, not just implementers.

This skill is for:

- Artifact review: PRD, proposal, tech spec, epic, story, bug ticket
- Design review: screenshots, mockups, exported frames, recordings
- Live review: running feature, local dev server, staging/prod URL, swe-bug-fix validation

## Inputs

- Persona file path or paths
  - Prefer repo-local sources such as `.swe/context/user-personas.md`, `.swe/context/personas/**`, `docs/personas/**`
- Review target
  - Path to a PRD/spec/story/design artifact, or a URL / local app to review
- Optional context
  - Credentials, seed accounts, feature flags, device constraints, known risks, expected flows

## Operating Rules

### 1) Fresh context by default

- If the platform supports subagents, run this review in a fresh-context reviewer agent.
- Pass only the minimum needed context:
  - persona file path
  - target path or URL
  - review goal
  - environment constraints
  - credentials or flags if required
- Do not preload your own conclusions. The reviewer should form an independent judgment.

### 2) Isolate personas and sessions

- If multiple personas are requested, run one isolated review per persona.
- If the same persona needs multiple auth states or environments, isolate those too.
- When Chrome DevTools MCP is available, create a separate isolated browser context or page per persona or account.
- Never share cookies, local storage, or login state across personas unless the test explicitly requires shared state.
- If parallel execution is available, run persona reviews in parallel.

### 3) Evidence over opinion

- Tie every finding back to the persona's goals, constraints, and workflow.
- For live reviews, validate in the browser before concluding.
- For design reviews, use screenshots or recordings as the source of truth. Do not inspect code unless the user explicitly asks for code review.
- For swe-bug-fix validation, treat the fix as unverified until you reproduce and retest it against the live app.

### 4) Findings-first output

- Default to a reviewer mindset.
- Present findings first, ordered by severity.
- For each finding, include:
  - affected persona
  - why it matters
  - concrete evidence
  - suggested change

## Workflow

### 1) Resolve the persona set

- Read the provided persona file completely.
- Extract, per persona:
  - goals and jobs-to-be-done
  - key workflows
  - domain fluency
  - permissions and constraints
  - device expectations
  - trust, accessibility, or support needs
- If the file contains many personas, include only the personas materially impacted by the target.
- State which personas were reviewed and which were excluded.
- If no persona file was provided:
  - search likely repo locations first
  - if none exist, ask for one concise clarification or proceed with clearly labeled minimal assumptions only when the user asked for best-effort review

### 2) Classify the target

Pick one primary mode:

- Artifact review
- Design review
- Live experience review

Use secondary checks only when needed.

### 3) Artifact review mode

- Read the target fully.
- Review it first as the persona:
  - Does the workflow make sense to this user?
  - Are prerequisites and permissions realistic?
  - Are copy, labels, and CTAs understandable?
  - Are failure, empty, and recovery states covered?
  - Would this persona trust the experience?
- Then do a delivery-aware pass:
  - missing acceptance criteria
  - missing persona or permission coverage
  - hidden assumptions
  - risky rollout, dependency, or migration gaps
  - unclear success metrics or observability gaps
- If the target is a PRD/spec/story, cite the relevant section or heading for each finding.

### 4) Design review mode

- Review the design from screenshots, exported frames, or recordings only.
- Do not grade the implementation code.
- Focus on the experience the persona would actually perceive:
  - visual hierarchy
  - clarity of primary action
  - information scent
  - trust and credibility
  - cognitive load and density
  - visible accessibility concerns
  - consistency across screens and states
  - whether the next step is obvious
- If multiple screens are provided, evaluate the flow between them.
- If critical states are missing from the design set, call that out explicitly.

### 5) Live experience review mode

- Prefer Chrome DevTools MCP for interactive validation.
- If Chrome MCP is unavailable or not appropriate, use Playwright or another available browser/emulator tool and say what you used.
- When reviewing multiple personas in Chrome, use separate isolated browser contexts or pages so login state cannot bleed across reviews.
- For local work:
  - discover the target URL from the user, repo docs, or the running environment
  - if the dev server is not running, start the safest repo-native command you can justify
  - if several commands are plausible, ask one concise question instead of guessing
- Validate as the persona:
  - entering the flow
  - navigation clarity
  - success path
  - failure path
  - empty or null states
  - permission behavior
  - recovery after invalid input or interruption
  - responsiveness and device fit
- Inspect screenshots, not just DOM text.
- Capture concrete evidence:
  - URLs visited
  - steps taken
  - screenshots
  - visible errors
  - console or network issues when relevant

### 6) Device coverage

- Match device coverage to the persona and target:
  - desktop web
  - mobile web
  - tablet
  - large-screen / TV-like experience
- Use the best available emulator or device emulation.
- State clearly what was actually emulated versus what is inferred.
- Do not claim native-device validation if you only used browser emulation.

### 7) swe-bug-fix validation mode

- Recreate the original bug path if it is known.
- Validate:
  - the original failure no longer occurs
  - the intended success path works
  - adjacent persona-sensitive flows did not regress
  - copy, trust, and recovery behavior are still acceptable
- If the original repro is incomplete, derive the smallest defensible repro and label the assumption.

### 8) Synthesize the review

For each persona reviewed, provide:

- top findings
- why they matter to that persona
- evidence: section, screen, URL, screenshot, or repro step
- recommended changes
- open questions or assumption-dependent concerns

Then provide a cross-persona summary:

- shared issues
- persona conflicts
- highest-leverage fixes

## Output Expectations

Use this default structure:

1. Findings
2. Open questions / assumptions
3. Evidence and coverage
4. Recommended changes

For live reviews, always include:

- personas reviewed
- device or browser contexts used
- whether session isolation was maintained
- URLs visited
- screenshots taken
- anything you could not validate

If no issues are found, say that explicitly and still note coverage gaps or untested risk areas.

## Red Flags

- Reviewing a design by reading code instead of screenshots
- Reusing the same logged-in session across personas
- Giving generic UX advice not tied to persona goals
- Skipping error, empty, or recovery states
- Claiming a bug fix works without live validation
- Letting one persona dominate the review when others are materially affected
