---
description: Produce an E2E-first test specification by delegating to the canonical swe-tdd skill.
argument-hint: [PRD path or test spec request]
disable-model-invocation: true
---

Read `.llm/references/SKILL-PROXY-RULES.md` or `~/.llm/references/SKILL-PROXY-RULES.md`, using the first one that exists, and use it to execute the canonical skill named `swe-tdd`.

Primary repo path: `swe-tdd/SKILL.md`

If arguments are present, treat them as the user's test-spec request:

`$ARGUMENTS`
