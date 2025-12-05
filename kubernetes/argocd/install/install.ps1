# ArgoCD Installation Script for Windows (PowerShell)

Write-Host "==========================================" -ForegroundColor Green
Write-Host "ArgoCD Installation" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Check if kubectl is installed
try {
    kubectl version --client | Out-Null
    Write-Host "[OK] kubectl is installed" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] kubectl not found. Please install kubectl first." -ForegroundColor Red
    exit 1
}

# Check if cluster is accessible
try {
    kubectl cluster-info | Out-Null
    Write-Host "[OK] Kubernetes cluster is accessible" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Cannot connect to Kubernetes cluster. Check your kubeconfig." -ForegroundColor Red
    exit 1
}

# Create ArgoCD namespace
Write-Host ""
Write-Host "Creating ArgoCD namespace..." -ForegroundColor Cyan
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -

# Install ArgoCD
Write-Host ""
Write-Host "Installing ArgoCD (this may take a few minutes)..." -ForegroundColor Cyan
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for ArgoCD to be ready
Write-Host ""
Write-Host "Waiting for ArgoCD pods to be ready..." -ForegroundColor Cyan
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd
kubectl wait --for=condition=available --timeout=300s deployment/argocd-repo-server -n argocd
kubectl wait --for=condition=available --timeout=300s deployment/argocd-applicationset-controller -n argocd

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "ArgoCD Installation Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access ArgoCD UI:" -ForegroundColor Yellow
Write-Host "  1. Port-forward: kubectl port-forward svc/argocd-server -n argocd 8080:443"
Write-Host "  2. Open: https://localhost:8080"
Write-Host "  3. Username: admin"
Write-Host "  4. Get password:" -ForegroundColor Yellow
Write-Host ""

# Get and display the initial admin password
$password = kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}'
$decodedPassword = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($password))
Write-Host "     Password: $decodedPassword" -ForegroundColor Cyan
Write-Host ""
Write-Host "NOTE: Change the admin password after first login!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Install ArgoCD CLI (optional):" -ForegroundColor Yellow
Write-Host "  choco install argocd-cli"
Write-Host ""
