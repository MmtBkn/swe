# Software Engineering Skill for Codex

**swe** is a collection of Agent Skills for Codex that helps you take a feature from idea to shipped code — without losing the thread. The focus is on **security**, **scalability**, and a **developer experience** that stays clean as the feature grows.

These skills are built for real work that doesn’t fit in a single session. It’s normal to run them across multiple follow-ups and spend **1)+ hours** on a feature once you include integration hardening, edge cases, and polish.

The philosophy is simple: ship the whole feature first, then iterate until it’s solid.

## What are Agent Skills?

Agent Skills are folders of instructions, scripts, and resources that AI agents can discover and use to perform specific tasks. This repo packages these workflows so they’re easy to reuse across repos and teams.

**Write once, use everywhere.** Skills make successful workflows portable across projects and teams.

Learn more:
- [Using skills in Codex](https://developers.openai.com/codex/skills)
- [Create custom skills in Codex](https://developers.openai.com/codex/skills/create-skill)
- [Agent Skills open standard](https://agentskills.io)

## What’s included

These skills work best together:

- `swe-init` — Build durable company/product context in `.swe/context/**`.
- `swe-prd` — Create a PRD/proposal in `.swe/proposals/` (repo-informed, structured).
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

## Using swe

In Codex, invoke a skill by name in your prompt (often with a `$` prefix), for example:

- “Use `$swe-spec` to turn `.swe/proposals/PROPOSAL-001-payments.md` into a tech spec and epics.”
- “Use `$swe-exec` to implement the stories in `.swe/stories/payments/`.”

## Using in Cursor (2.4+)

Cursor supports Agent Skills and Subagents (see Cursor changelog 2.4). This repo includes a Cursor-specific orchestrator skill + subagents under `.cursor/`:

- Skill: `.cursor/skills/swe-orchestrator/`
- Subagents: `.cursor/agents/`

### Install (project-level)

Copy the skills and subagents into your project:

```bash
mkdir -p .cursor/skills .cursor/agents
cp -R /path/to/this-repo/swe-init /path/to/this-repo/swe-prd /path/to/this-repo/swe-spec /path/to/this-repo/swe-tdd /path/to/this-repo/swe-exec .cursor/skills/
cp -R /path/to/this-repo/.cursor/skills/swe-orchestrator .cursor/skills/
cp -R /path/to/this-repo/.cursor/agents/*.md .cursor/agents/
```

Restart Cursor, then invoke the workflow from Agent chat:

- Type `/swe-orchestrator` and follow the prompts.
- The skill will prefer delegating orchestration to the `swe-flow-orchestrator` subagent (model pinned to `gpt-5.2-xhigh`).

### Install (user-level / global)

```bash
mkdir -p ~/.cursor/skills ~/.cursor/agents
cp -R /path/to/this-repo/swe-init /path/to/this-repo/swe-prd /path/to/this-repo/swe-spec /path/to/this-repo/swe-tdd /path/to/this-repo/swe-exec ~/.cursor/skills/
cp -R /path/to/this-repo/.cursor/skills/swe-orchestrator ~/.cursor/skills/
cp -R /path/to/this-repo/.cursor/agents/*.md ~/.cursor/agents/
```

### Notes

- Cursor also loads skills from `~/.codex/skills/` for compatibility. If you already installed the `swe-*` skills via Codex, you may only need to install the `.cursor/skills/swe-orchestrator/` skill and `.cursor/agents/` subagents.
- The provided subagent files pin models like `gpt-5.2-high`, `gpt-5.2-xhigh`, and `gpt-5.3-codex-xhigh`. If those model IDs don’t exist in your Cursor plan/config, set `model: inherit` in the corresponding `.cursor/agents/*.md` files.
- Orchestration behavior is centralized in `.cursor/skills/swe-orchestrator/references/RUNBOOK.md` (subagents and the skill reference it instead of duplicating instructions).

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
