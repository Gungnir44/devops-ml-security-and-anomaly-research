# Download Guide - Application Pipeline Artifacts

**Goal:** Download artifacts from Backend, Python, and Frontend CI/CD pipeline runs

---

## Step 1: Download Backend CI/CD Artifacts

### 1.1 Navigate to Backend Pipeline
**Direct Link:** https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/backend-ci-cd.yml

### 1.2 Click the Latest Run
Look for the run with commit message: **"Test backend CI/CD pipeline"**

### 1.3 Download These Artifacts
Scroll to bottom → "Artifacts" section:

**Expected Artifacts:**
- ✅ `test-coverage-backend` or `coverage-report`
- ✅ `security-scan-results` or `security-results`
- ✅ `container-scan-results` or `trivy-results`
- ✅ `sarif-results` or `codeql-results`
- ✅ `research-metadata` or `build-metadata`

**Note:** Artifact names may vary slightly. Download ALL artifacts you see.

### 1.4 Save Location
Save all Backend ZIPs to:
```
C:\Users\joshu\Desktop\DevOps Project\research-data\downloads\backend\
```

---

## Step 2: Download Python CI/CD Artifacts

### 2.1 Navigate to Python Pipeline
**Direct Link:** https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/python-ci-cd.yml

### 2.2 Click the Latest Run
Look for: **"Test Python CI/CD pipeline"**

### 2.3 Download These Artifacts
**Expected Artifacts:**
- ✅ `test-coverage-python` or `coverage-report`
- ✅ `security-scan-results` or `bandit-results`
- ✅ `container-scan-results` or `trivy-results`
- ✅ `sarif-results` or `bandit-sarif`
- ✅ `research-metadata`

### 2.4 Save Location
Save all Python ZIPs to:
```
C:\Users\joshu\Desktop\DevOps Project\research-data\downloads\python\
```

---

## Step 3: Download Frontend CI/CD Artifacts

### 3.1 Navigate to Frontend Pipeline
**Direct Link:** https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/frontend-ci-cd.yml

### 3.2 Click the Latest Run
Look for: **"Test Frontend CI/CD pipeline"**

### 3.3 Download These Artifacts
**Expected Artifacts:**
- ✅ `test-coverage-frontend` or `vitest-coverage`
- ✅ `security-scan-results` or `eslint-results`
- ✅ `container-scan-results` or `trivy-results`
- ✅ `sarif-results` or `codeql-results`
- ✅ `research-metadata`

### 3.4 Save Location
Save all Frontend ZIPs to:
```
C:\Users\joshu\Desktop\DevOps Project\research-data\downloads\frontend\
```

---

## Step 4: Extract All New Artifacts

After downloading all ZIPs, run this command:

```powershell
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"
.\extract-app-artifacts.ps1
```

This will automatically:
1. Find all downloaded ZIPs
2. Extract them to appropriate folders
3. Organize by application and category
4. Generate a summary report

---

## What You'll Have After This

```
baseline-week-1/
├── backend/
│   ├── security-scans/       ✅ Semgrep, CodeQL, TruffleHog, Gitleaks
│   ├── container-scans/      ✅ Trivy, Grype, Dockle
│   ├── test-coverage/        ✅ Jest coverage reports
│   └── metadata/             ✅ Build times, pipeline metrics
│
├── python/
│   ├── security-scans/       ✅ Bandit, Semgrep, CodeQL
│   ├── container-scans/      ✅ Trivy, Grype, Dockle
│   ├── test-coverage/        ✅ Pytest coverage reports
│   └── metadata/             ✅ Build times, pipeline metrics
│
├── frontend/
│   ├── security-scans/       ✅ ESLint, Semgrep, CodeQL
│   ├── container-scans/      ✅ Trivy, Grype, Dockle
│   ├── test-coverage/        ✅ Vitest coverage reports
│   └── metadata/             ✅ Build times, pipeline metrics
│
├── security-scans-general/   ✅ Already extracted (KICS, Gitleaks)
└── sbom-and-licenses/        ✅ Already extracted
```

---

## Quick Links

**All Actions:** https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions

**Backend Pipeline:** https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/backend-ci-cd.yml

**Python Pipeline:** https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/python-ci-cd.yml

**Frontend Pipeline:** https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/frontend-ci-cd.yml

---

## Troubleshooting

### "No artifacts available"
**Cause:** Pipeline may have failed before artifact upload stage
**Solution:** Check workflow logs, re-run failed jobs

### "Artifacts expired"
**Cause:** Artifacts are retained for 90 days
**Solution:** Trigger new pipeline runs by making small changes

### "Can't find the workflow"
**Cause:** Workflows may be under different names
**Solution:** Check the "Actions" tab and look for workflows with "CI/CD" in the name

---

**Next:** After downloading, run the extraction script and you'll have complete Week 1 baseline data!
