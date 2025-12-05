# ArgoCD Cheat Sheet

Quick reference for common ArgoCD commands and operations.

## Installation

```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Install ArgoCD CLI (Linux)
curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
chmod +x /usr/local/bin/argocd

# Install ArgoCD CLI (Mac)
brew install argocd

# Install ArgoCD CLI (Windows)
choco install argocd-cli
```

## Access ArgoCD

```bash
# Port-forward to access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo

# Login via CLI
argocd login localhost:8080
# Username: admin
# Password: (from above)

# Update admin password
argocd account update-password
```

## Application Management

### Create Applications

```bash
# Create from manifest
kubectl apply -f application.yaml

# Create via CLI
argocd app create my-app \
  --repo https://github.com/your-org/repo.git \
  --path kubernetes/manifests \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default

# Create with Helm
argocd app create my-helm-app \
  --repo https://github.com/your-org/repo.git \
  --path helm/my-chart \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default \
  --helm-set replicaCount=2
```

### List Applications

```bash
# List all applications
argocd app list

# List with output format
argocd app list -o wide
argocd app list -o json
```

### Get Application Details

```bash
# Get application info
argocd app get my-app

# Get with refresh
argocd app get my-app --refresh
argocd app get my-app --hard-refresh

# Get application manifests
argocd app manifests my-app
```

### Sync Applications

```bash
# Sync application
argocd app sync my-app

# Sync with prune (delete resources not in Git)
argocd app sync my-app --prune

# Sync specific resource
argocd app sync my-app --resource deployment:my-deployment

# Sync and wait for completion
argocd app sync my-app --timeout 300
argocd app wait my-app --health --timeout 300

# Force sync (ignore sync policy)
argocd app sync my-app --force

# Dry-run sync
argocd app sync my-app --dry-run
```

### Diff Applications

```bash
# View differences between Git and cluster
argocd app diff my-app

# Diff with local manifests
argocd app diff my-app --local /path/to/manifests
```

### Application History

```bash
# View deployment history
argocd app history my-app

# Show specific revision
argocd app history my-app --revision 5
```

### Rollback Applications

```bash
# List history to find revision
argocd app history my-app

# Rollback to specific revision
argocd app rollback my-app <revision>

# Rollback to previous revision
argocd app rollback my-app
```

### Delete Applications

```bash
# Delete application (keeps resources in cluster)
argocd app delete my-app

# Delete application and prune resources
argocd app delete my-app --cascade

# Delete without confirmation
argocd app delete my-app --yes
```

## Application Sets

```bash
# List ApplicationSets
argocd appset list

# Get ApplicationSet details
argocd appset get my-appset
```

## Projects

```bash
# List projects
argocd proj list

# Create project
argocd proj create my-project

# Get project details
argocd proj get my-project

# Add source repo to project
argocd proj add-source my-project https://github.com/your-org/repo.git

# Add destination to project
argocd proj add-destination my-project https://kubernetes.default.svc my-namespace

# Delete project
argocd proj delete my-project
```

## Repository Management

```bash
# List repositories
argocd repo list

# Add repository
argocd repo add https://github.com/your-org/repo.git

# Add private repository (HTTPS)
argocd repo add https://github.com/your-org/repo.git \
  --username your-username \
  --password your-token

# Add private repository (SSH)
argocd repo add git@github.com:your-org/repo.git \
  --ssh-private-key-path ~/.ssh/id_rsa

# Remove repository
argocd repo rm https://github.com/your-org/repo.git
```

## Cluster Management

```bash
# List clusters
argocd cluster list

# Add cluster
argocd cluster add my-cluster-context

# Remove cluster
argocd cluster rm https://kubernetes.default.svc

# Get cluster info
argocd cluster get https://kubernetes.default.svc
```

## User Management

```bash
# List users
argocd account list

# Update password
argocd account update-password

# Update password for specific user
argocd account update-password --account <username>

# Generate token
argocd account generate-token --account admin

# Generate token with expiration
argocd account generate-token --account admin --expires-in 24h
```

## Settings and Configuration

```bash
# Get ArgoCD settings
argocd settings get

# Update ArgoCD password policy
argocd settings set password.pattern "^.{12,}$"

# Get resource overrides
argocd settings resource-overrides
```

## Logs and Events

```bash
# View application logs
argocd app logs my-app

# Follow logs
argocd app logs my-app --follow

# View specific container logs
argocd app logs my-app --container my-container

# View ArgoCD component logs
kubectl logs -n argocd deployment/argocd-server
kubectl logs -n argocd deployment/argocd-repo-server
kubectl logs -n argocd deployment/argocd-application-controller
```

## Sync Policies

```bash
# Enable auto-sync
argocd app set my-app --sync-policy automated

# Disable auto-sync
argocd app set my-app --sync-policy none

# Enable auto-prune
argocd app set my-app --auto-prune

# Enable self-heal
argocd app set my-app --self-heal
```

## Health and Status

```bash
# Wait for application to be healthy
argocd app wait my-app --health

# Wait for sync to complete
argocd app wait my-app --sync

# Check application status
argocd app get my-app --show-operation
```

## Advanced Operations

### Selective Sync

```bash
# Sync only specific resources
argocd app sync my-app \
  --resource apps:Deployment:my-deployment \
  --resource v1:Service:my-service
```

### Patch Application

```bash
# Patch application spec
argocd app patch my-app --patch '{"spec":{"source":{"targetRevision":"v2.0.0"}}}'

# Patch with file
argocd app patch my-app --patch-file patch.yaml
```

### Ignore Differences

```bash
# Set application to ignore specific differences
argocd app set my-app --ignore-diff-at /spec/replicas
```

## Notifications (if configured)

```bash
# List configured triggers
kubectl get cm argocd-notifications-cm -n argocd -o yaml

# Test notification
argocd admin notifications trigger get on-sync-succeeded
```

## Kubectl Shortcuts

```bash
# Get all applications
kubectl get applications -n argocd

# Get application details
kubectl get application my-app -n argocd -o yaml

# Delete application
kubectl delete application my-app -n argocd

# Get AppProjects
kubectl get appprojects -n argocd

# Get ApplicationSets
kubectl get applicationsets -n argocd
```

## Troubleshooting

```bash
# Check ArgoCD pods
kubectl get pods -n argocd

# Describe ArgoCD pod
kubectl describe pod <pod-name> -n argocd

# Check application sync status
argocd app get my-app --show-operation

# Refresh application cache
argocd app get my-app --hard-refresh

# View sync errors
argocd app get my-app | grep -A 10 "Sync Status"

# Check resource health
argocd app resources my-app

# Validate application manifest
kubectl apply --dry-run=client -f application.yaml

# Check ArgoCD server version
argocd version

# Restart ArgoCD components
kubectl rollout restart deployment argocd-server -n argocd
kubectl rollout restart deployment argocd-repo-server -n argocd
kubectl rollout restart statefulset argocd-application-controller -n argocd
```

## Common Workflows

### Deploy New Application

```bash
# 1. Create application manifest
cat <<EOF > app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/repo.git
    targetRevision: main
    path: kubernetes/manifests
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
EOF

# 2. Apply application
kubectl apply -f app.yaml

# 3. Watch sync
argocd app get my-app --refresh
argocd app wait my-app --health
```

### Update Application Version

```bash
# Update image tag in Git
git checkout main
# Edit deployment.yaml or kustomization.yaml
git commit -m "Update to v2.0.0"
git push

# If auto-sync is disabled, manually sync
argocd app sync my-app
```

### Rollback Failed Deployment

```bash
# View history
argocd app history my-app

# Rollback to last working version
argocd app rollback my-app <previous-revision>

# Verify rollback
argocd app wait my-app --health
```

### Promote Across Environments

```bash
# Sync to dev
argocd app sync my-app-dev

# Verify in dev
argocd app wait my-app-dev --health

# Promote to staging
git checkout staging
git merge main
git push

# Sync to staging
argocd app sync my-app-staging

# Verify in staging
argocd app wait my-app-staging --health

# Tag for production
git checkout main
git tag v1.0.0
git push origin v1.0.0

# Manual sync to production (after approval)
argocd app sync my-app-prod
```

## Environment Variables

```bash
# Set ArgoCD server
export ARGOCD_SERVER=argocd.example.com

# Set auth token
export ARGOCD_AUTH_TOKEN=<token>

# Set default project
export ARGOCD_PROJECT=my-project

# Skip TLS verification (dev only)
export ARGOCD_OPTS='--insecure'
```

## Useful Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias argocd-login='argocd login localhost:8080'
alias argocd-apps='argocd app list'
alias argocd-sync='argocd app sync'
alias argocd-logs='argocd app logs'
alias argocd-diff='argocd app diff'
alias argocd-pods='kubectl get pods -n argocd'
```

## Tips and Tricks

1. **Use App of Apps pattern** for managing multiple applications
2. **Pin versions** in production (use Git tags, not branches)
3. **Enable auto-sync** for dev/staging, manual for prod
4. **Use sync windows** to control deployment times
5. **Monitor application health** regularly
6. **Keep Git history clean** with meaningful commits
7. **Test in dev** before promoting to higher environments
8. **Use Kustomize** for environment-specific configs
9. **Set resource limits** on all applications
10. **Enable notifications** for sync failures

---

For more details, see the main ArgoCD documentation: `kubernetes/argocd/README.md`
