# ArgoCD GitOps Implementation

Complete GitOps implementation using ArgoCD for continuous deployment to Kubernetes.

## Table of Contents

- [What is GitOps?](#what-is-gitops)
- [ArgoCD Overview](#argocd-overview)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Application Deployment](#application-deployment)
- [Multi-Environment Strategy](#multi-environment-strategy)
- [CI/CD Integration](#cicd-integration)
- [RBAC and Security](#rbac-and-security)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## What is GitOps?

GitOps is a modern approach to continuous deployment where:

1. **Git as Single Source of Truth**: All infrastructure and application configurations are stored in Git
2. **Declarative**: System desired state is declared in Git using Kubernetes manifests
3. **Automated Sync**: ArgoCD automatically syncs cluster state with Git repository
4. **Auditable**: All changes are tracked through Git commits with full history
5. **Recoverable**: Easy rollbacks using Git revert or ArgoCD rollback

### GitOps Benefits

- Improved deployment reliability and consistency
- Faster recovery from failures (rollback via Git)
- Enhanced security through pull-based deployments
- Complete audit trail of all changes
- Simplified multi-environment management
- Infrastructure as code versioning

---

## ArgoCD Overview

ArgoCD is a declarative GitOps continuous delivery tool for Kubernetes.

### Key Features

- Automated deployment of applications to Kubernetes
- Multiple deployment strategies (Helm, Kustomize, plain manifests)
- Web UI and CLI for management
- SSO integration support
- RBAC for multi-tenant environments
- Automated sync and health monitoring
- Rollback capabilities
- Webhook support for CI/CD integration

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Git Repository                       │
│  (kubernetes/manifests/, gitops/, helm/)                    │
└────────────┬────────────────────────────────────────────────┘
             │
             │ Monitors for changes
             ▼
┌─────────────────────────────────────────────────────────────┐
│                        ArgoCD Server                         │
│  - Monitors Git repositories                                │
│  - Compares desired state (Git) with actual state (cluster) │
│  - Triggers sync when differences detected                   │
└────────────┬────────────────────────────────────────────────┘
             │
             │ Applies manifests
             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                        │
│  (dev, staging, prod namespaces)                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
DevOps Project/
├── kubernetes/
│   ├── argocd/
│   │   ├── install/
│   │   │   ├── namespace.yaml           # ArgoCD namespace
│   │   │   ├── install.sh               # Installation script (Linux/Mac)
│   │   │   └── install.ps1              # Installation script (Windows)
│   │   ├── projects/
│   │   │   ├── monitoring-project.yaml  # Monitoring AppProject
│   │   │   └── devops-project.yaml      # Main DevOps AppProject
│   │   ├── applications/
│   │   │   ├── monitoring-stack.yaml    # Monitoring deployment
│   │   │   ├── monitoring-helm.yaml     # Monitoring via Helm
│   │   │   ├── app-of-apps.yaml         # App of Apps pattern
│   │   │   ├── example-webapp-dev.yaml  # Dev environment example
│   │   │   ├── example-webapp-staging.yaml
│   │   │   └── example-webapp-prod.yaml
│   │   └── README.md                    # This file
│   ├── manifests/                       # Raw Kubernetes manifests
│   └── helm/                            # Helm charts
├── gitops/
│   ├── applications/
│   │   ├── dev/                         # Development manifests
│   │   ├── staging/                     # Staging manifests
│   │   └── prod/                        # Production manifests
│   └── README.md                        # GitOps guide
└── .github/
    └── workflows/
        └── argocd-sync.yml              # CI/CD integration
```

---

## Quick Start

### Prerequisites

- Kubernetes cluster (minikube, kind, Docker Desktop, or cloud K8s)
- kubectl configured and connected to cluster
- Git repository for your manifests

### 1. Install ArgoCD

**Linux/Mac:**
```bash
cd kubernetes/argocd/install
chmod +x install.sh
./install.sh
```

**Windows (PowerShell):**
```powershell
cd kubernetes\argocd\install
.\install.ps1
```

**Manual Installation:**
```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for pods to be ready
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd
```

### 2. Access ArgoCD UI

```bash
# Port-forward to access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Open browser to https://localhost:8080
```

**Get initial admin password:**
```bash
# Linux/Mac
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo

# Windows PowerShell
$password = kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}'
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($password))
```

**Login:**
- Username: `admin`
- Password: (from command above)

**Change password after first login!**

### 3. Install ArgoCD CLI (Optional but Recommended)

```bash
# Linux
curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
chmod +x /usr/local/bin/argocd

# MacOS
brew install argocd

# Windows
choco install argocd-cli
```

### 4. Deploy ArgoCD Projects

```bash
# Deploy AppProjects for RBAC
kubectl apply -f kubernetes/argocd/projects/
```

### 5. Deploy Your First Application

**Option A: Using App of Apps Pattern (Recommended)**
```bash
# This deploys all applications at once
kubectl apply -f kubernetes/argocd/applications/app-of-apps.yaml
```

**Option B: Deploy Individual Applications**
```bash
# Deploy monitoring stack
kubectl apply -f kubernetes/argocd/applications/monitoring-stack.yaml

# Deploy example webapp (dev environment)
kubectl apply -f kubernetes/argocd/applications/example-webapp-dev.yaml
```

### 6. Monitor Deployment

**Using UI:**
- Open https://localhost:8080
- Click on your application
- Watch the sync status

**Using CLI:**
```bash
# Login to ArgoCD CLI
argocd login localhost:8080

# Get application status
argocd app get monitoring-stack

# Watch sync status
argocd app sync monitoring-stack
argocd app wait monitoring-stack --health
```

---

## Installation

### Step-by-Step Installation

#### 1. Create Namespace

```bash
kubectl apply -f kubernetes/argocd/install/namespace.yaml
```

#### 2. Install ArgoCD

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

#### 3. Verify Installation

```bash
# Check all pods are running
kubectl get pods -n argocd

# Expected output:
# NAME                                               READY   STATUS
# argocd-application-controller-0                    1/1     Running
# argocd-applicationset-controller-xxx               1/1     Running
# argocd-dex-server-xxx                              1/1     Running
# argocd-notifications-controller-xxx                1/1     Running
# argocd-redis-xxx                                   1/1     Running
# argocd-repo-server-xxx                             1/1     Running
# argocd-server-xxx                                  1/1     Running
```

#### 4. Expose ArgoCD Server

**Option A: Port Forward (Development)**
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

**Option B: NodePort (Local Testing)**
```bash
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "NodePort"}}'
kubectl get svc argocd-server -n argocd
```

**Option C: Ingress (Production)**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: argocd-server-ingress
  namespace: argocd
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-passthrough: "true"
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
spec:
  ingressClassName: nginx
  rules:
    - host: argocd.yourdomain.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: argocd-server
                port:
                  name: https
  tls:
    - hosts:
        - argocd.yourdomain.com
      secretName: argocd-server-tls
```

#### 5. Configure CLI

```bash
# Login
argocd login localhost:8080

# Enter username: admin
# Enter password: (from secret)

# Update password
argocd account update-password
```

---

## Application Deployment

### Deployment Methods

ArgoCD supports three deployment methods:

#### 1. Plain Kubernetes Manifests

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/your-repo.git
    targetRevision: main
    path: kubernetes/manifests
  destination:
    server: https://kubernetes.default.svc
    namespace: my-namespace
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

#### 2. Helm Charts

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-helm-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/your-repo.git
    targetRevision: main
    path: kubernetes/helm/my-chart
    helm:
      releaseName: my-app
      values: |
        replicaCount: 2
        image:
          tag: v1.0.0
  destination:
    server: https://kubernetes.default.svc
    namespace: my-namespace
```

#### 3. Kustomize

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-kustomize-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/your-repo.git
    targetRevision: main
    path: gitops/applications/dev/webapp
    kustomize:
      namePrefix: dev-
      images:
        - webapp=webapp:v1.0.0
  destination:
    server: https://kubernetes.default.svc
    namespace: dev
```

### Sync Policies

#### Automated Sync

```yaml
syncPolicy:
  automated:
    prune: true      # Remove resources not in Git
    selfHeal: true   # Auto-sync when cluster state differs
    allowEmpty: false
  syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
```

#### Manual Sync

```yaml
syncPolicy:
  automated: null  # Disable auto-sync (production recommended)
  syncOptions:
    - CreateNamespace=true
```

### App of Apps Pattern

Deploy multiple applications from a single Application:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app-of-apps
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/your-repo.git
    targetRevision: main
    path: kubernetes/argocd/applications
    directory:
      recurse: true
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

## Multi-Environment Strategy

### Environment Setup

```
gitops/
├── applications/
│   ├── dev/          # Development: main branch, auto-sync
│   ├── staging/      # Staging: staging branch, controlled sync
│   └── prod/         # Production: Git tags, manual sync only
```

### Environment Configurations

| Environment | Branch/Tag | Auto-Sync | Replicas | Resources | Deployment Window |
|-------------|-----------|-----------|----------|-----------|-------------------|
| Development | `main` | ✅ Yes | 1 | Minimal | Always |
| Staging | `staging` | ✅ Yes | 2 | Medium | Business hours |
| Production | `v1.x.x` tags | ❌ Manual | 3+ | Full | Controlled windows |

### Promoting Changes

```bash
# 1. Develop and test in dev environment
git checkout main
# Make changes to gitops/applications/dev/
git commit -m "feat: add new feature"
git push

# ArgoCD automatically syncs to dev

# 2. Promote to staging
git checkout staging
git merge main
git push

# ArgoCD automatically syncs to staging (during business hours)

# 3. Promote to production
git checkout main
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin v1.0.1

# Update prod application to use v1.0.1
# Manually trigger sync in ArgoCD UI or CLI
argocd app sync webapp-prod
```

---

## CI/CD Integration

### GitHub Actions Workflow

Located at: `.github/workflows/argocd-sync.yml`

**Features:**
- Validates Kubernetes manifests before deployment
- Runs security scans (Checkov) on manifests
- Generates ArgoCD diff preview on PRs
- Auto-syncs to dev/staging on merge
- Requires manual approval for production

**Required Secrets:**
- `ARGOCD_SERVER`: ArgoCD server URL
- `ARGOCD_AUTH_TOKEN`: ArgoCD authentication token

**Generate Auth Token:**
```bash
# Create a new user or use admin
argocd account generate-token --account admin
```

**Add to GitHub Secrets:**
1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Add `ARGOCD_SERVER` (e.g., `argocd.example.com`)
3. Add `ARGOCD_AUTH_TOKEN` (token from above)

### Workflow Triggers

- Push to `main`/`develop`/`staging` → Auto-deploy to respective environments
- Pull Request → Generate diff preview
- Manual dispatch → Deploy to specific environment

---

## RBAC and Security

### AppProjects

AppProjects provide multi-tenancy and RBAC:

**Monitoring Project** (`monitoring-project.yaml`):
- Restricted to `monitoring` namespace
- Defined source repositories
- Role-based access (read-only, developers, admins)

**DevOps Project** (`devops-project.yaml`):
- Multi-environment support (dev, staging, prod)
- Sync windows for controlled deployments
- Environment-specific roles

### Roles

```yaml
roles:
  - name: read-only
    policies:
      - p, proj:monitoring:read-only, applications, get, monitoring/*, allow
    groups:
      - monitoring-viewers

  - name: developers
    policies:
      - p, proj:monitoring:developers, applications, sync, monitoring/*, allow
    groups:
      - monitoring-developers

  - name: admins
    policies:
      - p, proj:monitoring:admins, applications, *, monitoring/*, allow
    groups:
      - monitoring-admins
```

### Sync Windows

Control when deployments can occur:

```yaml
syncWindows:
  # Production: Sundays at 2 AM only
  - kind: allow
    schedule: '0 2 * * 0'
    duration: 4h
    applications:
      - 'prod-*'

  # Staging: Business hours only
  - kind: allow
    schedule: '0 9-17 * * 1-5'
    duration: 8h
    applications:
      - 'staging-*'
```

---

## Troubleshooting

### Common Issues

#### 1. Application Not Syncing

**Check application status:**
```bash
argocd app get <app-name>
```

**Force refresh:**
```bash
argocd app get <app-name> --hard-refresh
```

**Manual sync:**
```bash
argocd app sync <app-name>
```

#### 2. Out of Sync Resources

**View differences:**
```bash
argocd app diff <app-name>
```

**Sync with prune:**
```bash
argocd app sync <app-name> --prune
```

#### 3. Failed Sync

**View sync logs:**
```bash
argocd app logs <app-name> --follow
```

**Check events:**
```bash
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

#### 4. Authentication Issues

**Reset admin password:**
```bash
# Delete the secret
kubectl -n argocd delete secret argocd-initial-admin-secret

# Restart ArgoCD server
kubectl -n argocd rollout restart deployment argocd-server

# Get new password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Health Checks

**Check ArgoCD components:**
```bash
kubectl get pods -n argocd
kubectl get svc -n argocd
```

**View ArgoCD logs:**
```bash
# Application controller
kubectl logs -n argocd deployment/argocd-application-controller

# Repo server
kubectl logs -n argocd deployment/argocd-repo-server

# Server
kubectl logs -n argocd deployment/argocd-server
```

---

## Best Practices

### 1. Repository Structure
- Separate application manifests by environment
- Use meaningful directory names
- Keep secrets out of Git (use Sealed Secrets or external secret managers)

### 2. Application Configuration
- Use Kustomize for environment-specific configs
- Pin image versions (no `latest` in prod)
- Define resource limits and requests
- Include health checks

### 3. Sync Strategy
- Auto-sync for dev and staging
- Manual sync for production
- Use sync windows for controlled deployments
- Enable pruning carefully

### 4. Security
- Regularly rotate ArgoCD passwords and tokens
- Use RBAC with least privilege
- Enable SSO for enterprise deployments
- Scan manifests for security issues in CI

### 5. Monitoring
- Set up notifications (Slack, email)
- Monitor sync status
- Track application health
- Review failed syncs promptly

### 6. Disaster Recovery
- Regular backups of ArgoCD configuration
- Document rollback procedures
- Test disaster recovery scenarios
- Keep Git history clean and meaningful

---

## Additional Resources

### Official Documentation
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [GitOps Principles](https://opengitops.dev/)
- [Kustomize Documentation](https://kubectl.docs.kubernetes.io/guides/introduction/kustomize/)

### Project Files
- GitOps Structure: `gitops/README.md`
- Monitoring Deployment: `kubernetes/README.md`
- CI/CD Pipeline: `.github/workflows/argocd-sync.yml`

### Next Steps
1. Update Git repository URLs in Application manifests
2. Configure GitHub secrets for CI/CD
3. Deploy your first application
4. Set up notifications
5. Configure SSO (for team environments)

---

## Support

For issues or questions:
1. Check ArgoCD logs and events
2. Review application diff: `argocd app diff <app-name>`
3. Consult [ArgoCD troubleshooting guide](https://argo-cd.readthedocs.io/en/stable/operator-manual/troubleshooting/)
4. Check GitHub Issues for this repository

---

**You've now implemented production-ready GitOps with ArgoCD!** 🚀
