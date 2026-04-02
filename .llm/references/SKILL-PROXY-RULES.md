# Skill Proxy Rules

This file is the provider-neutral source of truth for thin LLM-facing skill proxies.

Provider wrappers under `.cursor/`, `.claude/`, or other tool-specific folders must stay thin:

- Do not duplicate the canonical skill workflow in the proxy.
- Resolve the canonical skill file, read it, then execute it.
- Return concrete file paths created or updated, validation performed, and any open questions.

## Canonical lookup flow

Given a `skill name` and an optional `primary repo path`:

1. If a `primary repo path` is provided and exists, use it first.
2. Otherwise, check these standard install locations in order:
   - `.claude/skills/<skill-name>/SKILL.md`
   - `.cursor/skills/<skill-name>/SKILL.md`
   - `.agents/skills/<skill-name>/SKILL.md`
   - `.codex/skills/<skill-name>/SKILL.md`
   - `~/.claude/skills/<skill-name>/SKILL.md`
   - `~/.cursor/skills/<skill-name>/SKILL.md`
   - `~/.codex/skills/<skill-name>/SKILL.md`
3. If none exist, stop and report the paths you checked. Do not guess or recreate the missing skill inline.

## Execution rules

- Read the entire canonical `SKILL.md`.
- Read any referenced assets, references, or scripts the skill says are required for the task at hand.
- Follow the canonical skill exactly unless the caller imposes an explicit constraint.
- Keep provider-specific details in the proxy layer only when they are about invocation, not the task workflow itself.
