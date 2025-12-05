#!/bin/bash
# ArgoCD Installation Script for DevOps Project

set -e

echo "=========================================="
echo "ArgoCD Installation"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "kubectl not found. Please install kubectl first."
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "Cannot connect to Kubernetes cluster. Please check your kubeconfig."
    exit 1
fi

echo -e "${GREEN}✓${NC} Kubernetes cluster is accessible"

# Create ArgoCD namespace
echo ""
echo "Creating ArgoCD namespace..."
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -

# Install ArgoCD
echo ""
echo "Installing ArgoCD (this may take a few minutes)..."
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for ArgoCD to be ready
echo ""
echo "Waiting for ArgoCD pods to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd
kubectl wait --for=condition=available --timeout=300s deployment/argocd-repo-server -n argocd
kubectl wait --for=condition=available --timeout=300s deployment/argocd-applicationset-controller -n argocd

echo -e "${GREEN}✓${NC} ArgoCD is ready"

# Get initial admin password
echo ""
echo "=========================================="
echo "ArgoCD Installation Complete!"
echo "=========================================="
echo ""
echo "Access ArgoCD UI:"
echo "  1. Port-forward: kubectl port-forward svc/argocd-server -n argocd 8080:443"
echo "  2. Open: https://localhost:8080"
echo "  3. Username: admin"
echo "  4. Password: Run this command to get it:"
echo "     kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d && echo"
echo ""
echo -e "${YELLOW}NOTE:${NC} Change the admin password after first login!"
echo ""
echo "Install ArgoCD CLI (optional):"
echo "  Linux: curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64"
echo "  MacOS: brew install argocd"
echo "  Windows: choco install argocd-cli"
echo ""
