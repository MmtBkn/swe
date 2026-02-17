---
name: swe-prd
description: Create a Product Requirements Document (PRD) / proposal as a Markdown file in an existing repo. Use when a user asks to “write a PRD”, “create a PRD”, “write a proposal”, “feature spec/brief”, or wants a structured PRD informed by the codebase. Default output path is `proposals/PROPOSAL-00X-<Short-Slug>.md` where `00X` auto-increments from existing proposals.
---

# PRD Creator

## Workflow

1. Ask what to build (prompt user)
   - Trigger this when user didn't prompt aything yet
   - Get a feature title + 1–2 sentences of intent.
   - If the user already provided it, restate it in your own words and confirm.

4. Create a plan
   - Produce a brief plan (10–15 bullets) for understanding the current state of the product, and the codebase
   - Read existing product context (if present)
     - Read anything under `.swe/context/` (if the folder exists).
     - Read anything under `.swe/proposals/` (if the folder exists), especially recent proposals, to understand current product state and prior decisions.
     - If `.swe/proposals/` does not exist, proceed (do not fail).
   - Understand the repo and delivery shape
     - Identify projects and structure (monorepo vs single app; frontend/backend; services).
     - Identify how it runs and deploys:
        - app entry points, build tooling, CI, infra (Docker/K8s/Terraform), and environments (dev/stage/prod).
     - Identify key domain areas, APIs, data stores, and feature-flag/config systems.
     - Suggested files/folders to inspect (when present): `README*`, `docs/`, `package.json`, `go.mod`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `Dockerfile`, `docker-compose.yml`, `.github/workflows/`, `k8s/`, `helm/`, `terraform/`, `infra/`, `.env*`. 
   - Understand the intent
     - Act like a principal product analyst
       - What is the intent, and desire with this ask
       - Produce a crisp framing:
         - **User / customer**: who is impacted?
         - **Problem**: what is broken/missing today?
         - **Constraints**: time, platform, compliance, dependencies
       - Identify:
          - Current flow (happy path + main failure modes)
          - Baseline metrics (if unknown, specify what to measure first)
          - Existing comparable features (reused patterns, edge cases)
       - Provide 2–3 options
          - List Pros/Cons/Alternatives for each option
          - Recommend Decision: Final choice and rationale
       - summarize the current state, expand and clarify user's intent, and users's desires with the ask, current state, and where they want to be
       - Build an extended context file under .swe/.cache/PA-00X-<Short-Slug>.md

5. Load PRD standards
   - Read `assets/PRDs.md` and follow its guidance.

4. Create a short plan
   - Produce a brief plan (3–7 bullets) for writing points of the PRD

7. Create the proposal file
   - Ensure `.swe/proposals/` exists (create if needed).
   - Choose the next incremental number by scanning existing files matching `PROPOSAL-\\d{3}`.
   - Create `.swe/proposals/PROPOSAL-00X-<Short-Slug>.md` where `<Short-Slug>` is derived from the feature title (human readable, filesystem-safe).

8. Write the PRD like a Principal Product Manager
   - Keep requirements testable (include acceptance criteria).
   - Ground the PRD in what you learned from `context/`, prior proposals, and the repo structure/deployment.
   - Do not invent facts about business, metrics, timelines, or existing system behavior, use your best jugment if not clear.
   - Link to relevant repo files and name likely modules/services that will be affected when justified by repo evidence.

9. Act like a Principal UX Designer, and review and improve user experience requirements of the proposal

4. Create a short plan
   - Produce a brief plan (3–7 bullets) for analyzing the output, and closing the gaps agains the ask, current product state, and close gaps. Do this twice. 

## Output expectations

- Output is a single Markdown PRD/proposal file created under `.swe/proposals/`.
- Prefer concise bullets, tables for requirements.
- Technical specification will be written later, exclude how (endpoints, technical details etc.), answer what, and why.
