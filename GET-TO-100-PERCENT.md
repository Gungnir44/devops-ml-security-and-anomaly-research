# Getting to 100% Data Completeness

**Current:** 85% complete
**Target:** 100% complete
**Gap:** Missing test coverage, container scans, and some SAST results

---

## 🔍 Problem Identified

**17 out of 20 workflows FAILED** because they're looking for files in the wrong directory.

### Failed Steps:
- ❌ Setup Node.js (can't find package.json)
- ❌ Install Python dependencies (can't find requirements.txt)
- ❌ TruffleHog Secret Scan
- ❌ Semgrep SAST
- ❌ npm/pip audit

### Root Cause:
Workflows run from repository root, but apps are in:
```
sample-apps/
├── backend-api/      ← Backend code here
├── python-service/   ← Python code here
└── frontend/         ← Frontend code here
```

The workflows need to `cd` into these directories before running commands!

---

## 🛠️ Solution Options

### Option 1: Fix Workflows to Use Correct Paths (Recommended)

**Pros:**
- Workflows will actually test your code
- Will generate all missing artifacts
- Gets you to 100% completion

**Cons:**
- Need to update 3 workflow files
- Need to re-run pipelines

**Implementation:**
1. Update `.github/workflows/backend-ci-cd.yml`
2. Update `.github/workflows/python-ci-cd.yml`
3. Update `.github/workflows/frontend-ci-cd.yml`
4. Add `working-directory` to each job
5. Commit and push changes
6. Workflows auto-run and generate artifacts
7. Download new artifacts

---

### Option 2: Accept 85% and Document Missing Data

**Pros:**
- No workflow changes needed
- Current data is still valuable for research

**Cons:**
- Missing test coverage metrics
- Missing container scan artifacts (though you have code scanning alerts)
- Incomplete dataset

---

### Option 3: Create Simplified Workflows Just for Data Collection

**Pros:**
- Easier to implement
- Focused on research data only

**Cons:**
- Separate from main CI/CD
- Duplication of effort

---

## 📋 Recommended Approach: Fix the Workflows

Here's exactly what to do:

### Step 1: Update Backend CI/CD Workflow

**File:** `.github/workflows/backend-ci-cd.yml`

**Changes needed:**
Add `working-directory: sample-apps/backend-api` to jobs:

```yaml
jobs:
  code-quality:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: sample-apps/backend-api  # ADD THIS
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      # ... rest of steps
```

Apply to ALL jobs in the file.

---

### Step 2: Update Python CI/CD Workflow

**File:** `.github/workflows/python-ci-cd.yml`

**Changes needed:**
Add `working-directory: sample-apps/python-service`:

```yaml
jobs:
  code-quality:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: sample-apps/python-service  # ADD THIS
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      # ... rest of steps
```

---

### Step 3: Update Frontend CI/CD Workflow

**File:** `.github/workflows/frontend-ci-cd.yml`

**Changes needed:**
Add `working-directory: sample-apps/frontend`:

```yaml
jobs:
  code-quality:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: sample-apps/frontend  # ADD THIS
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      # ... rest of steps
```

---

### Step 4: Special Cases

Some steps need additional path fixes:

#### Docker Build Steps:
```yaml
- name: Build Docker image
  run: |
    docker build -t backend:latest .
  working-directory: sample-apps/backend-api  # Explicit override
```

#### Checkout for Paths:
Some actions need the full repo, so don't use working-directory:
```yaml
- uses: actions/checkout@v4  # No working-directory here
```

---

### Step 5: Commit and Push

```bash
cd "C:\Users\joshu\Desktop\DevOps Project"

git add .github/workflows/
git commit -m "Fix CI/CD workflows to use correct app directories

- Add working-directory to all jobs
- Backend: sample-apps/backend-api
- Python: sample-apps/python-service
- Frontend: sample-apps/frontend
- This will enable test coverage and artifact generation"

git push
```

---

### Step 6: Watch Workflows Run

After pushing:
1. Go to: https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions
2. Watch the 3 pipelines trigger automatically
3. Wait for them to complete (10-15 minutes each)
4. Check for success ✅

---

### Step 7: Download New Artifacts

Once workflows succeed:

```powershell
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"
.\download-artifacts.ps1 -Token "YOUR_TOKEN"
.\extract-app-artifacts.ps1
```

---

## 📊 What You'll Get at 100%

After fixing workflows, you'll have:

### Backend:
- ✅ Jest test coverage reports
- ✅ Trivy container scan results
- ✅ Grype container scan results
- ✅ Dockle container scan results
- ✅ Semgrep SAST results
- ✅ CodeQL SAST results
- ✅ TruffleHog secret scan
- ✅ Gitleaks secret scan
- ✅ npm audit results

### Python:
- ✅ Pytest test coverage reports
- ✅ Trivy container scan results
- ✅ Grype container scan results
- ✅ Dockle container scan results
- ✅ Bandit SAST results
- ✅ Semgrep SAST results
- ✅ CodeQL SAST results
- ✅ pip-audit results (already have)

### Frontend:
- ✅ Vitest test coverage reports
- ✅ Trivy container scan results
- ✅ Grype container scan results
- ✅ Dockle container scan results
- ✅ ESLint results
- ✅ Semgrep SAST results
- ✅ CodeQL SAST results

**Total new data files:** 20-30+ additional artifacts

---

## ⚡ Quick Alternative: Manual Data Generation

If you don't want to fix workflows, you can generate data locally:

### Run Tests Locally:
```bash
# Backend
cd sample-apps/backend-api
npm install
npm test -- --coverage

# Python
cd sample-apps/python-service
pip install -r requirements.txt
pytest --cov --cov-report=json

# Frontend
cd sample-apps/frontend
npm install
npm test -- --coverage
```

### Run Security Scans Locally:
```bash
cd "C:\Users\joshu\Desktop\DevOps Project\scripts\security-scanning"
.\run-all-scans.sh
```

Save outputs to `research-data/baseline-week-1/` manually.

---

## 🎯 Recommendation

**I recommend Option 1: Fix the Workflows**

**Why?**
1. Gets you to 100% completion
2. Workflows will work correctly going forward
3. Automated data collection for future weeks
4. Professional, reproducible setup
5. Takes 30 minutes to implement

**Want me to help you fix the workflows?**

I can:
1. Read each workflow file
2. Add the correct `working-directory` settings
3. Commit and push the changes
4. Monitor the new workflow runs

---

## 📅 Timeline to 100%

If we fix workflows now:
- **10 minutes:** Update workflow files
- **5 minutes:** Commit and push
- **15 minutes:** Wait for workflows to run
- **5 minutes:** Download new artifacts

**Total: 35 minutes to 100% data completeness!**

---

**Ready to fix the workflows?** Let me know and I'll make the changes!
