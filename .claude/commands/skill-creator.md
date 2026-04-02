---
description: Create or update a skill by delegating to the canonical skill-creator skill.
argument-hint: [skill creation request]
disable-model-invocation: true
---

Read `.llm/references/SKILL-PROXY-RULES.md` or `~/.llm/references/SKILL-PROXY-RULES.md`, using the first one that exists, and use it to execute the canonical skill named `skill-creator`.

Primary repo path: `.system/skill-creator/SKILL.md`

If arguments are present, treat them as the user's skill-creation request:

`$ARGUMENTS`
