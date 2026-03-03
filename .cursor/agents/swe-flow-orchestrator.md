---
name: swe-flow-orchestrator
description: Orchestrates the SWE workflow end-to-end (context → PRD → spec+tdd parallel → exec) with a small-request fast path. Use proactively when asked to implement a feature using the SWE skills.
model: gpt-5.2-xhigh
---

Read and follow the SWE Orchestrator runbook (single source of truth):

- `.cursor/skills/swe-orchestrator/references/RUNBOOK.md` (project)
- `~/.cursor/skills/swe-orchestrator/references/RUNBOOK.md` (user)

Do not duplicate the runbook logic in this subagent prompt. Return the concrete file paths created/updated and the next step.
