# GitOps Directory Structure

This directory contains Kubernetes manifests organized by environment for GitOps deployment with ArgoCD.

## Directory Structure

```
gitops/
├── applications/          # Application manifests by environment
│   ├── dev/              # Development environment
│   ├── staging/          # Staging environment
│   └── prod/             # Production environment
└── README.md             # This file
```

## GitOps Principles

1. **Declarative**: Everything is defined as code in Git
2. **Versioned**: All changes are tracked in Git history
3. **Immutable**: Git is the single source of truth
4. **Pulled Automatically**: ArgoCD continuously monitors and syncs

## Environment Strategy

### Development (`dev/`)
- **Branch**: `develop` or `main`
- **Auto-sync**: Enabled
- **Purpose**: Rapid iteration and testing
- **Deployment**: Automatic on every commit

### Staging (`staging/`)
- **Branch**: `staging` or tagged releases
- **Auto-sync**: Enabled with approval
- **Purpose**: Pre-production testing
- **Deployment**: Automatic, controlled hours

### Production (`prod/`)
- **Branch**: Git tags (e.g., `v1.0.0`)
- **Auto-sync**: Disabled (manual only)
- **Purpose**: Live production workloads
- **Deployment**: Manual approval required

## Application Layout

Each environment follows this structure:

```
applications/{env}/
├── webapp/
│   ├── kustomization.yaml    # Kustomize configuration
│   ├── deployment.yaml        # Application deployment
│   ├── service.yaml           # Service definition
│   ├── configmap.yaml         # Configuration
│   └── ingress.yaml           # Ingress rules (if applicable)
└── ...other-apps/
```

## Adding a New Application

1. Create application directory:
   ```bash
   mkdir -p gitops/applications/dev/myapp
   mkdir -p gitops/applications/staging/myapp
   mkdir -p gitops/applications/prod/myapp
   ```

2. Add Kubernetes manifests to each environment

3. Create ArgoCD Application manifest:
   ```bash
   cp kubernetes/argocd/applications/example-webapp-dev.yaml \
      kubernetes/argocd/applications/myapp-dev.yaml
   # Edit and customize
   ```

4. Commit and push to Git

5. ArgoCD will automatically detect and sync (if auto-sync enabled)

## Kustomize Integration

We use Kustomize for environment-specific configurations:

- **Base**: Common configuration shared across environments
- **Overlays**: Environment-specific overrides

Example `kustomization.yaml`:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: dev

commonLabels:
  environment: dev
  managed-by: argocd

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml

images:
  - name: myapp
    newTag: latest

replicas:
  - name: myapp
    count: 1
```

## Best Practices

1. **Never commit secrets**: Use Sealed Secrets or external secret managers
2. **Use Kustomize**: For environment-specific configurations
3. **Pin versions**: Use specific image tags, not `latest`
4. **Small commits**: Make atomic, well-described commits
5. **Test in dev first**: Always test changes in dev before promoting
6. **Use branches**: Feature branches for development, merge to main
7. **Tag releases**: Use semantic versioning for production deployments
8. **Document changes**: Clear commit messages and PR descriptions

## Deployment Workflow

```
┌─────────────┐
│   Commit    │
│   to Git    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   ArgoCD    │
│  Monitors   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Detect    │
│  Changes    │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐
│  Auto-sync  │────▶│   Deploy    │
│  (if enabled)│     │ to Cluster  │
└─────────────┘     └─────────────┘
```

## Rollback Process

If a deployment fails or has issues:

```bash
# View application history
argocd app history webapp-prod

# Rollback to previous version
argocd app rollback webapp-prod <revision>

# Or use Git to revert
git revert <commit-hash>
git push
# ArgoCD will sync automatically
```

## Monitoring Sync Status

```bash
# Check application status
argocd app get webapp-dev

# Watch sync status
argocd app wait webapp-dev --sync

# View sync history
argocd app history webapp-dev
```

## Troubleshooting

### Application Out of Sync
```bash
# Force sync
argocd app sync webapp-dev

# Sync with prune (remove extra resources)
argocd app sync webapp-dev --prune

# Hard refresh
argocd app get webapp-dev --hard-refresh
```

### Invalid Manifests
```bash
# Validate locally before committing
kubectl apply --dry-run=client -f deployment.yaml
kustomize build . | kubectl apply --dry-run=client -f -
```

### Resource Conflicts
```bash
# Check diff between Git and cluster
argocd app diff webapp-dev

# Manual intervention may be required
kubectl edit deployment webapp-dev -n dev
```

## Next Steps

1. Set up your applications in the appropriate environment directories
2. Configure ArgoCD Application manifests
3. Commit to Git and watch ArgoCD sync
4. Monitor application health in ArgoCD UI

For more information, see:
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Kustomize Documentation](https://kubectl.docs.kubernetes.io/guides/introduction/kustomize/)
- Main ArgoCD guide: `kubernetes/argocd/README.md`
