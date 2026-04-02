---
description: Execute a story, epic, or PRD end-to-end by delegating to the canonical swe-exec skill.
argument-hint: [story path, epic path, or feature request]
disable-model-invocation: true
---

Read `.llm/references/SKILL-PROXY-RULES.md` or `~/.llm/references/SKILL-PROXY-RULES.md`, using the first one that exists, and use it to execute the canonical skill named `swe-exec`.

Primary repo path: `swe-exec/SKILL.md`

If arguments are present, treat them as the execution target or request:

`$ARGUMENTS`
