🏗️ Default Architecture

This document describes the default architecture guidelines to bootstrap new software projects consistently and efficiently.

⸻

🚀 Quick Start (Greenfield)

When starting a new project from scratch, initialize an Nx monorepo.

Prerequisites:

Ensure you have the following installed:
•	Docker (Installation Guide￼)
•	kubectl (Installation Guide￼)
•	Helm (Installation Guide￼)

Install missing dependencies if not present.

Monorepo Initialization:

npx create-nx-workspace@latest <monorepo-name> --preset=ts


⸻

📦 Monorepo Structure

For each project created within Nx, include the following targets:
•	build
•	lint
•	test
•	dockerize
•	publish
•	release

Recommended Nx Project Setup:

nx generate @nx/node:application api
nx generate @nx/react:application app

Add dockerize, publish, and release targets explicitly to project configurations.

⸻

📌 Default Tech Stack

Layer	Recommended Technology
Frontend	React SPA (use react-admin template if suitable)
Backend	Node.js (Express/NestJS) (Hasura where it makes more sense)
Database	PostgreSQL
Queue System	NSQ
Authentication	Keycloak (when required)
Marketing Site	Gatsby + dev.motion (Elegant design)


⸻

⚙️ Infrastructure & Deployment (Kubernetes)

Helm & Kubernetes:
•	Deploy all services using Kubernetes and Helm.
•	For external dependencies (e.g., PostgreSQL, NSQ), manage charts centrally.

Helm Chart Structure:
•	Umbrella Chart: Central chart to deploy the entire system and dependencies.
    •	Dependencies Chart: Manages external dependencies (e.g., PostgreSQL, NSQ, Keycloak) (official charts, avoid Bitnami).
        •   ELK Stack
        •   Vault (official HashiCorp chart)
        •   Dependencies Chart
    •	Service Chart: Manages repo native charts

Use official charts from official helm repos, do not pull & re push chars 

Example Chart.yaml structure:

apiVersion: v2
name: umbrella-chart
type: application
dependencies:
- name: elasticsearch
  repository: https://helm.elastic.co
- name: logstash
  repository: https://helm.elastic.co
- name: kibana
  repository: https://helm.elastic.co
- name: vault
  repository: https://helm.releases.hashicorp.com
- name: dependencies
  repository: file://../dependencies-chart


⸻

🚧 Ingress Setup

Development / Preview Branches:

Use Cloudflare Tunnel Ingress Controller￼ for ephemeral environments:

helm repo add strrl https://helm.strrl.dev
helm install cloudflare-ingress strrl/cloudflare-tunnel-ingress-controller

This approach enables quick previews, easy testing, and automated E2E tests.

Production:
•	Use Traefik as production ingress.
•	Expose default ingress clearly to facilitate DNS configuration.

⸻

🛠️ Local Development & Testing

Individual Service Development:

nx dev api
nx dev app

Full-stack Local Development:
•	Spin up a local Kubernetes cluster (Docker Desktop Kubernetes or Minikube).
•	Deploy via Helm to local Kubernetes.
•	Ingress via Cloudflare Tunnel Ingress Controller locally for easy testing.

Example:

helm install umbrella ./charts/umbrella-chart


⸻

Deployment Security
•   When you are installing internal charts, use vault references for secrets/tokens
    •   Generate the token/password, and add it to the vault
    •   Use vault key reference in the chart values
    •   Setup auto rotation of secrets/service restarts where applicable
Provide clear UX to user so that they can init/unseal the vault.

⸻

📢 CI/CD & Releases
•	Use semantic-release to automate versioning, tagging, and release notes.
•	Follow conventional commit messages with project-specific scopes:

feat(app): add user login page
fix(api): resolve auth token issue

	•	Support local releases via scripts in package.json:

```json
"scripts": {
  "release": "semantic-release"
}
```

	•	Configure ArgoCD as the default deployment tool:
	•	Create ArgoCD application pointing to the umbrella Helm chart.
	•	When there is a new version, repo chart version should be updated, and argocd should pick up the change, and deploy the new version

Example argocd-app.yaml:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: umbrella-deployment
spec:
  project: default
  source:
    repoURL: 'https://your-repo-url.git'
    targetRevision: HEAD
    path: charts/umbrella-chart
  destination:
    server: https://kubernetes.default.svc
    namespace: default
```

### Local Helm Preview and Teardown

Create two npm scripts to simplify the local preview and teardown process, and make sure different instances won't conflict with each other:

```json
"scripts": {
  "start": "nx run-many --target=build --all && nx run-many --target=publish --all && nx run-many --target=release --all && helm upgrade --install umbrella ./charts/umbrella-chart",
  "stop": "helm uninstall umbrella"
}
```

This setup builds, publishes, releases preview versions of all containers and charts, and deploys them locally using Helm. The `npm run stop` script cleans up local Helm instances.


⸻

✅ Standards & Compliance
•	All new services and apps must include explicit targets for:
    •	build
    •	lint
    •	test
    •	dockerize
    •	publish
    •	release
•	Maintain a consistent architecture:
    •	Easy local and ephemeral previews.
    •	Scalable, secure production deployments.
•	Ensure clear documentation for each step and component.