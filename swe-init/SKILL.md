---
name: swe-init
description: Build reusable repo context by discovering the company and product, researching via public web search and any connected internal knowledge bases (SharePoint, Confluence/Jira, Notion, etc.), and writing Markdown context files to `.swe/context/companies/<company-name>.md` and `.swe/context/products/<product-name>.md`. Use when a user asks to “swe-init”, “initialize context”, “onboard”, “learn the company/product”, or “create company/product context files”.
---

# SWE Init

## Goal

Create durable, repo-adjacent context that future tasks can reuse:

- `.swe/context/companies/<company-name>.md`
- `.swe/context/products/<product-name>.md`

Treat these as “LLM context briefs”: concise, factual, source-backed, and easy to update.

## Workflow

1. Learn the company and product names (if applicable)
   - Ask:
     - Is this work for an existing company? If yes: company name + official website/domain.
     - Is there an existing product? If yes: product name + official product website/docs link.

2. List what you can use (skills + tools)
   - List the skills you have available and which ones might help (e.g., architecture, PRD, onboarding).
   - List the tools you can use in this environment, such as:
     - Web search / browser automation
     - Connected internal sources (if available): SharePoint, Confluence/Jira, Notion, Google Drive, etc.
   - If you do NOT have access to a mentioned internal tool, ask the user for links or exports (don’t pretend you can access it).

3. Collect repo-local context first
   - Scan for existing context and hints:
     - `.swe/context/`, `docs/`, `README*`, `proposals/`, wikis, runbooks, ADRs.
   - Extract:
     - Company/product naming, URLs, terminology
     - Architecture overview and major components/services
     - Environments, release process, on-call, observability, support channels

4. Research the company
   - Public web search:
     - Prefer official sources (company site, docs, blog, status page, careers/handbook, GitHub org).
     - We are looking for mission, vision, any information that will help us to build our product
   - Internal search (only if you have access):
     - Query for: “company overview”, “security”, “onboarding”.
   - Keep a short “Sources” list with titles + links + access dates.

5. Write company context to `.swe/context/companies/<company-name>.md`
   - Create `.swe/context/companies/` if it doesn’t exist.
   - Use a filesystem-safe filename (recommended: kebab-case slug), but keep the proper display name as the document title.
   - If the file already exists, update it (preserve any `## Local Notes` section if present).
   - Write a structured company overview to this context file, so coding agents can use it as a guide
     - Make sure to include mission, vision, product offerings, primary product features

6. Research the product
   - Public web search:
     - Product site, docs, pricing, changelog/release notes, status page, SDKs, GitHub repos.
   - Internal search (only if you have access):
     - “product brief”, “user guide”, “architecture”, “roadmap”, “SLAs/SLOs”, “support”.
   - Capture sources similarly.

7. Write product context to `.swe/context/products/<product-name>.md`
   - Create `.swe/context/products/` if it doesn’t exist.
   - Use a filesystem-safe filename (recommended: kebab-case slug), but keep the proper display name as the document title.
   - If the file already exists, update it (preserve any `## Local Notes` section if present).
   - Write a structured product overview to this context file, so coding agents can use it as a guide
     - Make sure to include list of product features, where does it fit in the company, product value proposition, who uses the product, and why, what is the scale (monthly active users etc. )

8. Using the company, and product, build user personas
   - Build .swe/context/user-personas.md
     - Use your tools to search internal knowledge if there is already user personas defined, if so use them
     - If personas aren't defined or if you can't find them, act liek a principal product manager, build user persoans for each target group at your best, so the coding agent can use them as a reference.

9. If user doesn't have a company and/or product yet, ask questions to user to build these. Help user, make assumptions using your best. 

Here’s the new section smoothly integrated into your existing instructions 🎉🚀:

⸻

Architecture Context Creation

Ensure the repository has a comprehensive architecture overview by following these steps:

1. Check for Existing Architecture Context
   •	Look in the repository for existing architecture documents:
   •	.swe/context/architecture.md
   •	docs/architecture/*
   •	README*
   •	proposals/
   •	wikis, runbooks, ADRs
   •	If architecture documentation exists, rewrite or clearly summarize it into:
   •	.swe/context/architecture.md

2. No Architecture Found? Check Your Skills! 🔍
   •	Verify your available skills or integrations with internal tools such as Confluence, Notion, SharePoint, Google Drive etc.
   •	Clearly identify and state if you have access or not.

3. Build Architecture Context from Internal Knowledge (If Accessible) 💡

Create a clear action plan (5-10 steps per knowledge source):
•	Step 1: Search for “Architecture Overview,” “System Design,”, “System Security Plan”, "SMOC"
•	Step 2: Identify major services/components used by the product.
•	Step 3: Discover frameworks, languages, and tools used.
•	Step 4: Find documentation on internal APIs or microservices.
•	Step 5: Locate coding standards and development guidelines.
•	Step 6: Note deployment, CI/CD processes, and infrastructure details.
•	Step 7: Identify observability, monitoring, and logging solutions.
•	Step 8: Search for security and compliance certifications (e.g., SOC 2, GDPR, ISO).
•	Step 9: Locate performance metrics or scaling strategy documentation.
•	Step 10: Summarize your findings clearly in .swe/context/architecture.md.

Repeat for each accessible internal source (Confluence, Notion, SharePoint, etc.), and for the current repo. Write a deatailed context to .swe/context/architecture.md to set software engineering agent success.

4. If Internal Knowledge is Not Accessible 😅
   •	Copy the default architecture template from assets/architecture-default.md to project's .swe/context/architecture.md

## Writing rules (context-writer mode)

- Don’t include secrets, credentials, private customer info, or any content the user flags as confidential.
- Don’t invent metrics, timelines, architecture details, or internal process
- Do build content in a way to do useful Context Injection
