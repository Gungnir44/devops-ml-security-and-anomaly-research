# Kubernetes Deployment

Deploy the monitoring stack to Kubernetes with manifests or Helm.

## Prerequisites

- Kubernetes cluster (local: minikube, kind, Docker Desktop)
- kubectl configured
- Helm 3.x (for Helm deployment)

## Quick Start with Manifests

```bash
# Deploy everything
kubectl apply -f manifests/

# Check status
kubectl get all -n monitoring

# Access Grafana
kubectl port-forward -n monitoring svc/grafana 3000:3000
# Open http://localhost:3000 (admin/admin123)

# Access Prometheus
kubectl port-forward -n monitoring svc/prometheus 9090:9090
# Open http://localhost:9090
```

## Quick Start with Helm

```bash
cd kubernetes/helm

# Install the chart
helm install monitoring ./monitoring --create-namespace

# Upgrade
helm upgrade monitoring ./monitoring

# Uninstall
helm uninstall monitoring

# View values
helm get values monitoring
```

## What Gets Deployed

### Namespace
- `monitoring` namespace for all resources

### Workloads
- **Prometheus**: Metrics collection (Deployment)
- **Grafana**: Visualization dashboard (Deployment)
- **Redis**: Caching (Deployment)
- **PostgreSQL**: Database (StatefulSet with PVC)

### Services
- Prometheus: ClusterIP on port 9090
- Grafana: NodePort on port 30300
- Redis: ClusterIP on port 6379
- PostgreSQL: ClusterIP on port 5432

### ConfigMaps & Secrets
- Prometheus configuration
- Grafana credentials
- PostgreSQL credentials

## Access Services

### Grafana (NodePort)
```bash
# Direct access (if using NodePort)
http://<node-ip>:30300

# Or use port-forward
kubectl port-forward -n monitoring svc/grafana 3000:3000
```

### Prometheus
```bash
kubectl port-forward -n monitoring svc/prometheus 9090:9090
```

### Databases (internal only)
```bash
# PostgreSQL
kubectl port-forward -n monitoring svc/postgres 5432:5432

# Redis
kubectl port-forward -n monitoring svc/redis 6379:6379
```

## Helm Chart Customization

Create `custom-values.yaml`:

```yaml
grafana:
  adminPassword: "mysecurepassword"
  service:
    nodePort: 31000

prometheus:
  replicas: 2
  resources:
    limits:
      memory: 4Gi

postgres:
  storage:
    size: 10Gi
```

Deploy with custom values:
```bash
helm install monitoring ./monitoring -f custom-values.yaml
```

## Resource Limits

Default resource requests/limits:

| Service | CPU Request | Memory Request | CPU Limit | Memory Limit |
|---------|-------------|----------------|-----------|--------------|
| Prometheus | 200m | 512Mi | 1000m | 2Gi |
| Grafana | 100m | 256Mi | 500m | 1Gi |
| Redis | 100m | 128Mi | 500m | 512Mi |
| PostgreSQL | 200m | 256Mi | 1000m | 1Gi |

## Scaling

```bash
# Scale Prometheus
kubectl scale deployment prometheus -n monitoring --replicas=2

# Scale with Helm
helm upgrade monitoring ./monitoring --set prometheus.replicas=2
```

## Monitoring the Monitoring

```bash
# Check pod status
kubectl get pods -n monitoring

# View logs
kubectl logs -n monitoring deployment/prometheus
kubectl logs -n monitoring deployment/grafana

# Describe resources
kubectl describe pod -n monitoring <pod-name>

# Events
kubectl get events -n monitoring --sort-by='.lastTimestamp'
```

## Cleanup

### Manifests
```bash
kubectl delete -f manifests/
```

### Helm
```bash
helm uninstall monitoring
kubectl delete namespace monitoring
```

## Kubernetes Features Demonstrated

✅ Deployments - Stateless applications
✅ StatefulSets - Stateful applications (PostgreSQL)
✅ Services - ClusterIP, NodePort
✅ ConfigMaps - Configuration management
✅ Secrets - Sensitive data management
✅ Resource limits - CPU/Memory management
✅ Probes - Liveness & readiness checks
✅ Namespaces - Resource isolation
✅ Labels & Selectors - Resource organization
✅ PersistentVolumes - Data persistence

## Helm Features Demonstrated

✅ Chart structure and metadata
✅ Values file for configuration
✅ Templates with Go templating
✅ Dependencies management
✅ Versioning
✅ Customization with values

## Production Considerations

For production deployments:

1. **Use Ingress** instead of NodePort
2. **Enable TLS** for services
3. **Use PersistentVolumes** with proper storage classes
4. **Set resource quotas** per namespace
5. **Configure RBAC** for access control
6. **Use Helm secrets** for sensitive data
7. **Enable monitoring** with ServiceMonitors
8. **Configure backups** for PostgreSQL
9. **Use multiple replicas** for HA
10. **Implement pod security policies**

## Troubleshooting

### Pods not starting
```bash
kubectl describe pod <pod-name> -n monitoring
kubectl logs <pod-name> -n monitoring
```

### Service not accessible
```bash
kubectl get svc -n monitoring
kubectl get endpoints -n monitoring
```

### PVC not binding
```bash
kubectl get pvc -n monitoring
kubectl describe pvc <pvc-name> -n monitoring
```

---

**You're now orchestrating containers with Kubernetes!** 🚀
