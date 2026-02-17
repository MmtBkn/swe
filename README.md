# Software Engineering Skill for Codex

**swe** is a collection of Agent Skills for Codex that helps you take a feature from idea to shipped code — without losing the thread. The focus is on **security**, **scalability**, and a **developer experience** that stays clean as the feature grows.

These skills are built for real work that doesn’t fit in a single session. It’s normal to run them across multiple follow-ups and spend **1)+ hours** on a feature once you include integration hardening, edge cases, and polish.

The philosophy is simple: ship the whole feature first, then iterate until it’s solid.

## What are Agent Skills?

Agent Skills are folders of instructions, scripts, and resources that AI agents can discover and use to perform specific tasks. qw packages these workflows so they’re easy to reuse across repos and teams.

**Write once, use everywhere.** Skills make successful workflows portable across projects and teams.

Learn more:
- [Using skills in Codex](https://developers.openai.com/codex/skills)
- [Create custom skills in Codex](https://developers.openai.com/codex/skills/create-skill)
- [Agent Skills open standard](https://agentskills.io)

## What’s included

These skills work best together:

- `swe-init` — Build durable company/product context in `.swe/context/**`.
- `swe-prd` — Create a PRD/proposal in `proposals/` (repo-informed, structured).
- `swe-spec` — Turn a PRD into a detailed tech spec + epics + stories.
- `swe-tdd` — Derive an E2E-first test specification from the PRD (traceable coverage).
- `swe-exec` — Execute stories sequentially, keep an execution log, and ship working code.

## Recommended workflow

1. Start with context: `swe-init`
2. Define the feature: `swe-prd`
3. Design it properly: `swe-spec`
4. Lock in validation: `swe-tdd`
5. Build it end-to-end: `swe-exec`

## Why this works

- **End-to-end first**: you get something working before you optimize.
- **Integration-aware**: you surface contracts and “must-not-break” paths early.
- **Traceable**: requirements → stories → validation, so quality doesn’t depend on memory.
- **Iterative hardening**: follow-ups close security gaps, edge cases, and rough UX.

## Installing a skill

Install individual skills directly from GitHub using Codex’s `skill-installer`:

```bash
$skill-installer install https://github.com/MmtBkn/swe/tree/main/swe-spec
```

Example (from the upstream skills repo):

```bash
$skill-installer install https://github.com/openai/skills/tree/main/skills/.experimental/create-plan
```

After installing a skill, **restart Codex** to pick up new skills.

## Using qw

In Codex, invoke a skill by name in your prompt (often with a `$` prefix), for example:

- “Use `$swe-spec` to turn `proposals/PROPOSAL-001-payments.md` into a tech spec and epics.”
- “Use `$swe-exec` to implement the stories in `.swe/stories/payments/`.”

## Developing locally

This repo includes simple build + local install scripts:

```bash
npm run dist
npm run install
```

Notes:
- Build artifacts are written to `dist/` as `*.skill` bundles.
- Local install targets `$CODEX_HOME/skills` (defaults to `~/.codex/skills`).
- Requires `zip` + `unzip` available on your machine.
