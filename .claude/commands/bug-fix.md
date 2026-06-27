---
description: Diagnose and fix a bounded bug or regression by delegating to the canonical swe-bug-fix skill.
argument-hint: [bug description, failing command, or repro]
disable-model-invocation: true
---

Read `.llm/references/SKILL-PROXY-RULES.md` or `~/.llm/references/SKILL-PROXY-RULES.md`, using the first one that exists, and use it to execute the canonical skill named `swe-bug-fix`.

Primary repo path: `swe-bug-fix/SKILL.md`

If arguments are present, treat them as the user's explicit bug report or reproduction context:

`$ARGUMENTS`
