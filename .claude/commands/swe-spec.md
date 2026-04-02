---
description: Produce a technical specification, epics, and stories by delegating to the canonical swe-spec skill.
argument-hint: [PRD path or technical design request]
disable-model-invocation: true
---

Read `.llm/references/SKILL-PROXY-RULES.md` or `~/.llm/references/SKILL-PROXY-RULES.md`, using the first one that exists, and use it to execute the canonical skill named `swe-spec`.

Primary repo path: `swe-spec/SKILL.md`

If arguments are present, treat them as the user's spec request:

`$ARGUMENTS`
