---
description: Create a PRD or proposal by delegating to the canonical swe-prd skill.
argument-hint: [feature request or PRD path]
disable-model-invocation: true
---

Read `.llm/references/SKILL-PROXY-RULES.md` or `~/.llm/references/SKILL-PROXY-RULES.md`, using the first one that exists, and use it to execute the canonical skill named `swe-prd`.

Primary repo path: `swe-prd/SKILL.md`

If arguments are present, treat them as the user's PRD request:

`$ARGUMENTS`
