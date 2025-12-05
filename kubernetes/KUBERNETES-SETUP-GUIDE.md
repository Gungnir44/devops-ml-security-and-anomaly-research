# Kubernetes Setup Guide for Windows

Docker Desktop is installed but not running properly. Here's how to set up Kubernetes for ArgoCD.

## Issue Detected

Docker Desktop API error - the Docker daemon needs to be restarted or Kubernetes needs to be enabled.

## **Option 1: Docker Desktop with Kubernetes (RECOMMENDED - Easiest)**

### Steps:

1. **Open Docker Desktop**
   - Find Docker Desktop in your Start Menu
   - Make sure it's running (icon in system tray)

2. **Restart Docker Desktop**
   - Right-click Docker Desktop icon in system tray
   - Select "Restart"
   - Wait for it to fully start (icon turns from orange to green/white)

3. **Enable Kubernetes**
   - Open Docker Desktop
   - Click Settings (gear icon)
   - Go to "Kubernetes" section
   - Check "Enable Kubernetes"
   - Click "Apply & Restart"
   - **This will take 5-10 minutes** - Docker will download Kubernetes components

4. **Verify Kubernetes is Running**
   ```powershell
   kubectl cluster-info
   kubectl get nodes
   ```

   You should see:
   ```
   Kubernetes control plane is running at https://kubernetes.docker.internal:6443

   NAME             STATUS   ROLES           AGE   VERSION
   docker-desktop   Ready    control-plane   1m    v1.28.x
   ```

5. **Once Kubernetes is running, install ArgoCD:**
   ```powershell
   cd "C:\Users\joshu\Desktop\DevOps Project\kubernetes\argocd\install"
   .\install.ps1
   ```

---

## **Option 2: kind (Kubernetes in Docker)**

If Docker Desktop Kubernetes doesn't work, use kind:

### Steps:

1. **Fix Docker First**
   - Open Docker Desktop
   - Go to Settings → General
   - Click "Restart Docker"
   - Wait for Docker to fully start

2. **Verify Docker Works**
   ```powershell
   docker ps
   docker run hello-world
   ```

3. **Create kind Cluster** (kind is already installed at `$HOME/bin/kind.exe`)
   ```powershell
   cd "$HOME/bin"
   ./kind create cluster --name devops-cluster --config "C:\Users\joshu\Desktop\DevOps Project\kubernetes\kind-cluster-config.yaml"
   ```

4. **Verify Cluster**
   ```powershell
   kubectl cluster-info
   kubectl get nodes
   ```

5. **Install ArgoCD**
   ```powershell
   cd "C:\Users\joshu\Desktop\DevOps Project\kubernetes\argocd\install"
   .\install.ps1
   ```

---

## **Option 3: minikube**

### Install minikube:

```powershell
# Using Chocolatey (if you have it)
choco install minikube

# Or download manually from:
# https://minikube.sigs.k8s.io/docs/start/
```

### Start minikube:

```powershell
minikube start --driver=docker --cpus=4 --memory=8192
```

### Install ArgoCD:

```powershell
cd "C:\Users\joshu\Desktop\DevOps Project\kubernetes\argocd\install"
.\install.ps1
```

---

## **Troubleshooting Docker Desktop**

### Docker Desktop Won't Start

1. **Check if WSL 2 is enabled** (required for Docker Desktop on Windows)
   ```powershell
   wsl --status
   wsl --update
   ```

2. **Enable Virtualization in BIOS**
   - Restart computer
   - Enter BIOS (usually F2, F10, or DEL during startup)
   - Enable "Intel VT-x" or "AMD-V"
   - Save and restart

3. **Reinstall Docker Desktop**
   - Download from: https://www.docker.com/products/docker-desktop/
   - Run installer
   - Select "Use WSL 2 instead of Hyper-V"

### Docker API Version Error

If you see "API version" errors:

```powershell
# Check Docker version
docker version

# Update Docker Desktop to latest version
# Settings → Software Updates → Check for updates
```

---

## **What to Do After Kubernetes is Running**

Once you have Kubernetes running (via any of the 3 options above), follow these steps:

### 1. Verify Kubernetes

```powershell
kubectl cluster-info
kubectl get nodes
kubectl get namespaces
```

### 2. Install ArgoCD

```powershell
cd "C:\Users\joshu\Desktop\DevOps Project\kubernetes\argocd\install"
.\install.ps1
```

### 3. Access ArgoCD UI

```powershell
# Port-forward to access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Open browser to: https://localhost:8080
# Username: admin
# Password will be shown in terminal
```

### 4. Deploy Applications

```powershell
# Deploy ArgoCD Projects (RBAC)
kubectl apply -f "C:\Users\joshu\Desktop\DevOps Project\kubernetes\argocd\projects"

# Deploy applications
kubectl apply -f "C:\Users\joshu\Desktop\DevOps Project\kubernetes\argocd\applications\app-of-apps.yaml"
```

---

## **Quick Reference**

### Check Cluster Status
```powershell
kubectl cluster-info
kubectl get nodes
kubectl get pods --all-namespaces
```

### Check Docker
```powershell
docker ps
docker info
```

### kind Commands
```powershell
# List clusters
kind get clusters

# Delete cluster
kind delete cluster --name devops-cluster

# Create cluster
kind create cluster --name devops-cluster
```

### Docker Desktop Kubernetes
```powershell
# Switch context (if you have multiple clusters)
kubectl config get-contexts
kubectl config use-context docker-desktop
```

---

## **Recommended: Docker Desktop with Kubernetes**

For your use case, I recommend **Option 1: Docker Desktop with Kubernetes** because:

1. ✅ Easiest to set up (just enable in settings)
2. ✅ Integrates seamlessly with Docker
3. ✅ No additional tools needed
4. ✅ Works well on Windows
5. ✅ Automatic start with Docker Desktop
6. ✅ Good for development and testing

---

## **Once Everything is Working**

After Kubernetes is running and ArgoCD is installed, come back and let me know. I'll help you:

1. Deploy your monitoring stack via ArgoCD
2. Set up the example webapp across dev/staging/prod
3. Configure CI/CD integration
4. Set up your GitHub repository URLs
5. Test the GitOps workflow

---

## **Status Check**

Run this to verify everything is ready:

```powershell
# Check Docker
docker --version
docker ps

# Check Kubernetes
kubectl version
kubectl cluster-info
kubectl get nodes

# Check ArgoCD (after installation)
kubectl get pods -n argocd
kubectl get svc -n argocd
```

When all commands return successfully, you're ready for ArgoCD deployment! 🚀
