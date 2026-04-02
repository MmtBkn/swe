---
description: Install curated or GitHub-hosted skills by delegating to the canonical skill-installer skill.
argument-hint: [skill name or GitHub path]
disable-model-invocation: true
---

Read `.llm/references/SKILL-PROXY-RULES.md` or `~/.llm/references/SKILL-PROXY-RULES.md`, using the first one that exists, and use it to execute the canonical skill named `skill-installer`.

Primary repo path: `.system/skill-installer/SKILL.md`

If arguments are present, treat them as the user's installation request:

`$ARGUMENTS`
