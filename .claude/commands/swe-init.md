---
description: Build reusable company, product, persona, and architecture context by delegating to the canonical swe-init skill.
argument-hint: [company/product context request]
disable-model-invocation: true
---

Read `.llm/references/SKILL-PROXY-RULES.md` or `~/.llm/references/SKILL-PROXY-RULES.md`, using the first one that exists, and use it to execute the canonical skill named `swe-init`.

Primary repo path: `swe-init/SKILL.md`

If arguments are present, treat them as the user's context-building request:

`$ARGUMENTS`
