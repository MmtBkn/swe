---
description: Review artifacts, designs, or live features from one or more user personas using a fresh-context reviewer agent.
argument-hint: [persona file path + target path or URL]
disable-model-invocation: true
context: fork
agent: swe-user-persona-reviewer
---

Read `.llm/references/SKILL-PROXY-RULES.md` or `~/.llm/references/SKILL-PROXY-RULES.md`, using the first one that exists, and use it to execute the canonical skill named `swe-user-persona-review`.

Primary repo path: `swe-user-persona-review/SKILL.md`

If arguments are present, treat them as the user's review target and persona-review request:

`$ARGUMENTS`
