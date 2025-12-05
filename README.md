# DevOps ML Security and Anomaly Research

[![Backend CI/CD](https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/backend-ci-cd.yml/badge.svg)](https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/backend-ci-cd.yml)
[![Python CI/CD](https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/python-ci-cd.yml/badge.svg)](https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/python-ci-cd.yml)
[![Frontend CI/CD](https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/frontend-ci-cd.yml/badge.svg)](https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/frontend-ci-cd.yml)
[![Security Scan](https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/security-scanning.yml/badge.svg)](https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/security-scanning.yml)

> **Master's Degree Research Project**: ML-Based Security Anomaly Detection for DevOps Pipelines

A comprehensive DevOps security research platform featuring full-stack microservices, automated CI/CD pipelines, 15+ security scanning tools, and machine learning infrastructure for detecting anomalies in DevOps environments.

---

## Quick Links

| Resource | Description |
|----------|-------------|
| [Complete Project Summary](COMPLETE-PROJECT-SUMMARY.md) | Full overview of the entire project |
| [CI/CD Documentation](CI-CD-PIPELINE-SUMMARY.md) | Detailed pipeline information |
| [Security Tools Guide](SECURITY-TOOLS-SETUP.md) | Security scanning setup |
| [Backend API](sample-apps/backend-api/) | Node.js REST API service |
| [Python Service](sample-apps/python-service/) | FastAPI data processing |
| [Frontend Dashboard](sample-apps/frontend/) | React web interface |

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Applications](#applications)
- [CI/CD Pipelines](#cicd-pipelines)
- [Security Scanning](#security-scanning)
- [Research Components](#research-components)
- [Documentation](#documentation)
- [Development](#development)
- [Deployment](#deployment)

---

## Overview

### What is This?

This repository contains the complete infrastructure for my Master's degree research on **ML-based security anomaly detection in DevOps pipelines**. It's a production-grade platform that:

1. **Runs real microservices** (React + Node.js + Python)
2. **Scans for security vulnerabilities** using 15+ industry-standard tools
3. **Collects data automatically** for machine learning model training
4. **Deploys via GitOps** using Kubernetes and ArgoCD

### Key Features

✅ **3 Production-Ready Microservices**
✅ **10-Stage CI/CD Pipelines** (per application)
✅ **15+ Security Scanning Tools** integrated
✅ **210 ML Features** for anomaly detection
✅ **Kubernetes + ArgoCD** for orchestration
✅ **Prometheus + Grafana + ELK** for monitoring
✅ **Automated Research Data Collection**

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│         Frontend (React + Vite + Nginx)         │
│              Port: 3001 / 80                    │
└────────────┬───────────────────┬────────────────┘
             │                   │
             ▼                   ▼
┌────────────────────┐  ┌──────────────────────┐
│   Backend API      │  │  Python Service      │
│ (Node.js/Express)  │  │    (FastAPI)         │
│    Port: 3000      │  │    Port: 8000        │
└────────────────────┘  └──────────────────────┘
             │                   │
             ▼                   ▼
┌─────────────────────────────────────────────────┐
│        Database Layer (PostgreSQL)              │
│   Monitoring (Prometheus, Grafana, ELK)         │
│   Security Scanning (15+ tools)                 │
└─────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Kubernetes (kind/minikube)
- Node.js 18+ & Python 3.11+
- Git

### 1. Clone Repository

```bash
git clone https://github.com/Gungnir44/devops-ml-security-and-anomaly-research.git
cd devops-ml-security-and-anomaly-research
```

### 2. Start Monitoring Stack

```bash
cd docker
docker-compose -f docker-compose-monitoring.yml up -d

# Access:
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
# Kibana: http://localhost:5601
```

### 3. Run Applications

**Backend (Terminal 1):**
```bash
cd sample-apps/backend-api
npm install && npm start
# http://localhost:3000
```

**Python Service (Terminal 2):**
```bash
cd sample-apps/python-service
pip install -r requirements.txt
uvicorn app.main:app --reload
# http://localhost:8000/docs
```

**Frontend (Terminal 3):**
```bash
cd sample-apps/frontend
npm install && npm run dev
# http://localhost:3001
```

---

## Applications

### 1. Backend API (Node.js + Express)

**Purpose**: RESTful API for user management and data operations

- Health checks & Prometheus metrics
- CRUD operations for users
- JWT authentication ready
- 70%+ test coverage

**Endpoints**:
- `GET /health` - Service health
- `GET /api/v1/users` - List users
- `POST /api/v1/users` - Create user
- `GET /metrics` - Prometheus metrics

[Full Documentation →](sample-apps/backend-api/README.md)

### 2. Python Service (FastAPI)

**Purpose**: Data processing and analytics service

- Async FastAPI framework
- Pydantic validation
- Swagger UI auto-generated
- Batch processing support

**Endpoints**:
- `GET /docs` - Swagger documentation
- `POST /api/v1/process` - Process data
- `POST /api/v1/batch-process` - Batch operations
- `GET /api/v1/analytics/summary` - Analytics

[Full Documentation →](sample-apps/python-service/README.md)

### 3. Frontend Dashboard (React)

**Purpose**: Web interface for monitoring and management

- Modern React 18 with Vite
- 4 pages: Dashboard, Users, Processing, Security
- Real-time health indicators
- Nginx production server

**Pages**:
- `/` - Dashboard & overview
- `/users` - User management
- `/processing` - Data processing
- `/security` - Security metrics

[Full Documentation →](sample-apps/frontend/README.md)

---

## CI/CD Pipelines

### Pipeline Architecture

Each application has a **10-stage pipeline**:

1. **Code Quality** - Linting & formatting
2. **Testing** - 70% coverage requirement
3. **Secret Scanning** - TruffleHog, Gitleaks
4. **SAST** - CodeQL, Semgrep, Bandit
5. **Dependency Scan** - npm audit, pip-audit
6. **Build** - Docker multi-stage builds
7. **Container Scan** - Trivy, Grype, Dockle
8. **Push** - GitHub Container Registry
9. **Deploy** - Kubernetes via ArgoCD
10. **Metrics** - Research data collection

### Path-Filtered Execution

- **Backend**: Only runs when `sample-apps/backend-api/**` changes
- **Python**: Only runs when `sample-apps/python-service/**` changes
- **Frontend**: Only runs when `sample-apps/frontend/**` changes

### Workflow Files

- `.github/workflows/backend-ci-cd.yml`
- `.github/workflows/python-ci-cd.yml`
- `.github/workflows/frontend-ci-cd.yml`
- `.github/workflows/security-scanning.yml`

[Full CI/CD Documentation →](CI-CD-PIPELINE-SUMMARY.md)

---

## Security Scanning

### Integrated Tools (15+)

| Category | Tools |
|----------|-------|
| **Secrets** | TruffleHog, Gitleaks |
| **SAST** | CodeQL, Semgrep, Bandit |
| **Containers** | Trivy, Grype, Dockle |
| **Dependencies** | npm audit, pip-audit, Snyk |
| **IaC** | Checkov, tfsec |
| **Kubernetes** | kubeaudit, kubeval |

### Running Scans Locally

```bash
cd scripts/security-scanning
./install-tools.sh  # One-time setup
./scan-all.sh       # Run all scans

# Results: security-scan-results/YYYYMMDD_HHMMSS/
```

[Security Setup Guide →](SECURITY-TOOLS-SETUP.md)

---

## Research Components

### ML Features (210 Total)

1. **Infrastructure Metrics** (40) - CPU, memory, disk
2. **CI/CD Events** (35) - Pipeline runs, duration
3. **Security Scans** (21) - Vulnerabilities found
4. **Access Logs** (28) - Request patterns
5. **Container Events** (24) - Deployments, restarts
6. **Code Changes** (25) - Commits, complexity
7. **Deployment Events** (22) - Frequency, rollbacks

### Attack Scenarios (14 Planned)

- Credential stuffing
- SQL injection
- Container escape
- Cryptojacking
- Data exfiltration
- Supply chain attacks
- And more...

[Feature Details →](FEATURE-ENGINEERING.md) | [Attack Scenarios →](ATTACK-SCENARIOS.md)

---

## Project Structure

```
devops-ml-security-and-anomaly-research/
├── .github/workflows/          # CI/CD pipelines
│   ├── backend-ci-cd.yml
│   ├── python-ci-cd.yml
│   ├── frontend-ci-cd.yml
│   └── security-scanning.yml
│
├── sample-apps/
│   ├── backend-api/            # Node.js API
│   ├── python-service/         # FastAPI service
│   └── frontend/               # React app
│
├── kubernetes/                 # K8s manifests
├── docker/                     # Docker Compose
├── scripts/                    # Automation scripts
├── curriculum/                 # Research planning
└── gitops/                     # GitOps configs
```

---

## Documentation

### Core Docs

- [Complete Project Summary](COMPLETE-PROJECT-SUMMARY.md)
- [CI/CD Pipeline Summary](CI-CD-PIPELINE-SUMMARY.md)
- [Security Tools Setup](SECURITY-TOOLS-SETUP.md)
- [Project Proposal](PROJECT-PROPOSAL.md)
- [Feature Engineering](FEATURE-ENGINEERING.md)

### Application Docs

- [Backend API](sample-apps/backend-api/README.md)
- [Python Service](sample-apps/python-service/README.md)
- [Frontend](sample-apps/frontend/README.md)

---

## Development

### Running Tests

```bash
# Backend
cd sample-apps/backend-api && npm test

# Python
cd sample-apps/python-service && pytest

# Frontend
cd sample-apps/frontend && npm test
```

### Code Quality

```bash
# Backend/Frontend
npm run lint
npm run format

# Python
black app/ tests/
flake8 app/
mypy app/
```

---

## Deployment

### Kubernetes

```bash
# Create cluster
kind create cluster --config kubernetes/kind-cluster-config.yaml

# Deploy apps
kubectl apply -f sample-apps/backend-api/k8s/
kubectl apply -f sample-apps/python-service/k8s/
kubectl apply -f sample-apps/frontend/k8s/

# Verify
kubectl get pods -n production
```

### GitOps with ArgoCD

```bash
# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Access UI: https://localhost:30080
# Username: admin
# Password: (see ARGOCD-ACCESS-INFO.txt)
```

---

## Research Progress

### Phase 1: Infrastructure ✅ COMPLETE

- ✅ Full-stack microservices (3 apps)
- ✅ Kubernetes + ArgoCD
- ✅ Monitoring stack
- ✅ 15+ security tools
- ✅ CI/CD pipelines
- ✅ Documentation

### Phase 2: Data Collection ⏳ CURRENT

- ⏳ Baseline data (4 weeks)
- ⏳ Security scan aggregation
- ⏳ CI/CD metrics
- ⏳ Infrastructure metrics

### Phase 3-5: Upcoming

- Attack simulation
- ML model training
- Thesis writing

---

## Statistics

- **Total Files**: 76+
- **Lines of Code**: ~8,500+
- **Applications**: 3 (full-stack)
- **Security Tools**: 15+
- **CI/CD Workflows**: 3
- **ML Features**: 210
- **Documentation Pages**: 15+

---

## License

MIT License - See [LICENSE](LICENSE) file

---

## Author

**Gungnir44** (Joshua)
Master's Degree Research - DevOps Security & ML
GitHub: [@Gungnir44](https://github.com/Gungnir44)

---

**Status**: ✅ Phase 1 Complete - Ready for Data Collection
**Last Updated**: December 2025
**Version**: 1.0.0
