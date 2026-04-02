---
description: Create a concise plan by delegating to the canonical create-plan skill.
argument-hint: [request to plan]
disable-model-invocation: true
---

Read `.llm/references/SKILL-PROXY-RULES.md` or `~/.llm/references/SKILL-PROXY-RULES.md`, using the first one that exists, and use it to execute the canonical skill named `create-plan`.

Primary repo path: `create-plan/SKILL.md`

If arguments are present, treat them as the user's planning request:

`$ARGUMENTS`
