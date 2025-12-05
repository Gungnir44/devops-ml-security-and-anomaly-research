# GitHub Setup Guide

Complete guide to push your monorepo to GitHub

---

## Prerequisites

✅ Docker running
✅ Git installed
✅ GitHub CLI (`gh`) installed (optional but recommended)

---

## Step 1: Initialize Git Repository

```bash
cd "C:\Users\joshu\Desktop\DevOps Project"

# Initialize git (if not already done)
git init

# Check current status
git status
```

---

## Step 2: Create GitHub Repository

### Option A: Using GitHub CLI (Recommended)

```bash
# Create repository
gh repo create devops-ml-security-and-anomaly-research \
  --public \
  --description "Master's degree research: ML-based security anomaly detection for DevOps pipelines" \
  --source=. \
  --remote=origin

# This automatically:
# - Creates the repo on GitHub
# - Sets up the remote
# - Ready to push
```

### Option B: Manually via GitHub Website

1. Go to https://github.com/new
2. Repository name: `devops-ml-security-and-anomaly-research`
3. Description: `Master's degree research: ML-based security anomaly detection for DevOps pipelines`
4. Choose **Public**
5. **DO NOT** initialize with README, .gitignore, or license
6. Click "Create repository"

Then add the remote:
```bash
git remote add origin https://github.com/Gungnir44/devops-ml-security-and-anomaly-research.git
```

---

## Step 3: Stage and Commit Files

```bash
# Add all files
git add .

# Check what will be committed
git status

# Create initial commit
git commit -m "Initial commit: Complete DevOps ML security research infrastructure

- 3 production-ready microservices (React, Node.js, FastAPI)
- 10-stage CI/CD pipelines for all applications
- 15+ integrated security scanning tools
- Kubernetes manifests with ArgoCD GitOps
- Monitoring stack (Prometheus, Grafana, ELK)
- 210 ML features for anomaly detection
- Comprehensive documentation (76+ files)
- Phase 1 complete - ready for data collection

Tech Stack:
- Frontend: React 18, Vite, Nginx
- Backend: Node.js 18, Express
- Data Service: Python 3.11, FastAPI
- Orchestration: Kubernetes, ArgoCD
- Monitoring: Prometheus, Grafana, Elasticsearch
- Security: TruffleHog, Gitleaks, CodeQL, Semgrep, Trivy, Grype
"
```

---

## Step 4: Push to GitHub

```bash
# Set main as default branch
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## Step 5: Verify on GitHub

1. Go to https://github.com/Gungnir44/devops-ml-security-and-anomaly-research
2. Verify files are uploaded
3. Check that README.md displays correctly
4. Verify CI/CD workflow badges (they will show "no status" until first run)

---

## Step 6: Enable GitHub Actions

1. Go to repository Settings → Actions → General
2. Ensure "Allow all actions and reusable workflows" is selected
3. Save

---

## Step 7: Watch Your First Pipeline Run

The CI/CD pipelines are configured with path filters, so they won't all run immediately. To trigger them:

### Trigger Backend Pipeline

```bash
# Make a small change to backend
echo "# Backend API" >> sample-apps/backend-api/README.md

git add sample-apps/backend-api/README.md
git commit -m "Trigger backend pipeline test"
git push
```

Watch at: https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions

### Trigger Python Pipeline

```bash
# Make a small change to Python service
echo "# Python Service" >> sample-apps/python-service/README.md

git add sample-apps/python-service/README.md
git commit -m "Trigger Python pipeline test"
git push
```

### Trigger Frontend Pipeline

```bash
# Make a small change to frontend
echo "# Frontend Dashboard" >> sample-apps/frontend/README.md

git add sample-apps/frontend/README.md
git commit -m "Trigger frontend pipeline test"
git push
```

---

## Expected CI/CD Behavior

### What Will Run

✅ **Code Quality** - ESLint, Prettier, Black, flake8
✅ **Tests** - Jest, Pytest, Vitest with coverage
✅ **Secret Scanning** - TruffleHog, Gitleaks
✅ **SAST** - CodeQL, Semgrep, Bandit
✅ **Dependency Scanning** - npm audit, pip-audit
✅ **Build** - Docker image creation
✅ **Container Scanning** - Trivy, Grype, Dockle

### What Won't Run (Until Main Branch)

❌ **Push to Registry** - Only on `main` branch
❌ **Deploy** - Only on `main` branch

### SARIF Uploads

Security scan results will be uploaded to:
https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/security/code-scanning

---

## Troubleshooting

### Issue: Pipelines Not Running

**Solution**: Check path filters. Pipelines only run when specific app files change.

```yaml
# Backend pipeline runs only when:
paths:
  - 'sample-apps/backend-api/**'
```

### Issue: Some Security Scans Fail

**Expected**: Some scans may find vulnerabilities or fail initially. This is normal and part of the research.

**Action**:
1. View failures in Actions tab
2. Download artifacts for research data
3. Document findings

### Issue: No SARIF Uploads to Security Tab

**Solution**:
1. Ensure repository is public OR has GitHub Advanced Security enabled
2. Check Actions logs for upload errors
3. SARIF uploads require `security-events: write` permission (already configured)

### Issue: Docker Build Fails

**Common Causes**:
- Missing dependencies in package.json/requirements.txt
- Network issues downloading packages
- Multi-stage build errors

**Solution**:
- Check build logs in Actions
- Test build locally: `docker build -t test sample-apps/backend-api/`

---

## Next Steps After Successful Push

### 1. Set Up Branch Protection (Optional)

```bash
# Protect main branch
gh api repos/Gungnir44/devops-ml-security-and-anomaly-research/branches/main/protection \
  --method PUT \
  -f required_status_checks[strict]=true \
  -f required_status_checks[contexts][]=code-quality \
  -f required_status_checks[contexts][]=test
```

### 2. Add Snyk Token (Optional)

For better dependency scanning:

1. Sign up at https://snyk.io
2. Get API token
3. Add to GitHub Secrets:
   - Go to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `SNYK_TOKEN`
   - Value: Your Snyk API token
   - Save

### 3. Monitor First Week

- **Day 1-2**: Fix any failing pipelines
- **Day 3-4**: Review security scan results
- **Day 5-7**: Begin baseline data collection

### 4. Start Data Collection

Once pipelines are stable:

```bash
# Let applications run continuously
# Pipelines will execute on schedule (weekly)
# Data will be collected in artifacts
```

---

## Useful Commands

### View Recent Workflows

```bash
gh run list --limit 10
```

### View Workflow Details

```bash
gh run view <run-id>
```

### Download Artifacts

```bash
gh run download <run-id>
```

### Re-run Failed Workflow

```bash
gh run rerun <run-id>
```

### Watch Workflow Live

```bash
gh run watch
```

---

## Repository Structure on GitHub

```
devops-ml-security-and-anomaly-research/
├── .github/workflows/          # ✅ CI/CD pipelines visible
├── sample-apps/                # ✅ All 3 applications
├── kubernetes/                 # ✅ K8s manifests
├── docker/                     # ✅ Docker Compose
├── scripts/                    # ✅ Security scanning
├── curriculum/                 # ✅ Research planning
├── gitops/                     # ✅ GitOps configs
├── README.md                   # ✅ Main documentation
├── COMPLETE-PROJECT-SUMMARY.md # ✅ Project overview
├── CI-CD-PIPELINE-SUMMARY.md   # ✅ Pipeline docs
└── [Other docs]                # ✅ All documentation
```

---

## Success Indicators

✅ Repository created on GitHub
✅ All files pushed successfully
✅ README displays with badges
✅ CI/CD pipelines configured
✅ Workflows run when files change
✅ Security scans execute
✅ Artifacts generated
✅ SARIF uploaded to Security tab

---

## Support

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **GitHub CLI Docs**: https://cli.github.com/manual/
- **Security Scanning**: Check `SECURITY-TOOLS-SETUP.md`
- **CI/CD Details**: Check `CI-CD-PIPELINE-SUMMARY.md`

---

**Ready to push?** Follow steps 1-5 above and watch your research infrastructure come to life on GitHub! 🚀
