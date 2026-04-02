---
description: Run the SWE workflow through shared orchestration rules and Claude subagents.
argument-hint: [feature request or bug report]
disable-model-invocation: true
context: fork
agent: swe-flow-orchestrator
---

Read `.llm/references/SWE-ORCHESTRATOR-RUNBOOK.md` or `~/.llm/references/SWE-ORCHESTRATOR-RUNBOOK.md`, using the first one that exists, and follow it exactly.

Use the project subagents in `.claude/agents/` when the runbook delegates work.

If arguments are present, treat them as the user's request:

`$ARGUMENTS`
