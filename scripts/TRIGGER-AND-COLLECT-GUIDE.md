# Complete Workflow Trigger & Data Collection Guide

## 🎯 **Goal:**
1. Trigger workflows for both `main` and `hardened` branches
2. Download all artifacts
3. Organize data properly

---

## 📋 **STEP 1: Manually Trigger Workflows (5 minutes)**

### **Trigger Main Branch:**
1. Go to: https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions
2. Click **"Security Scanning"** (left sidebar)
3. Click **"Run workflow"** button (right side, blue button)
4. Select branch: **`main`**
5. Click **"Run workflow"** (green button)
6. ✅ You should see "Workflow run was successfully requested"

### **Trigger Hardened Branch:**
1. Stay on the same page
2. Click **"Run workflow"** button again
3. Select branch: **`hardened`**
4. Click **"Run workflow"** (green button)
5. ✅ You should see "Workflow run was successfully requested"

**Result:** Two workflow runs will start (one per branch)

---

## ⏰ **STEP 2: Wait for Completion (10-15 minutes)**

### **Monitor Progress:**

Run this command to check status:
```bash
cd "C:\Users\joshu\Desktop\DevOps Project"
python scripts/check_workflow_details.py
```

**What to look for:**
```
Main branch run:     In progress → Completed
Hardened branch run: In progress → Completed
```

**Typical duration:** 8-12 minutes per branch

---

## 📥 **STEP 3: Download All Artifacts (Automated)**

Once both workflows complete, run:

```bash
cd "C:\Users\joshu\Desktop\DevOps Project"
python scripts/automated-weekly-collection.py
```

**This will:**
- ✅ Download artifacts from both branches
- ✅ Extract all ZIP files
- ✅ Organize by branch and date
- ✅ Generate features for ML training
- ✅ Create summary report

---

## 📁 **STEP 4: Verify Data Organization**

Check the organized data:

```bash
cd "C:\Users\joshu\Desktop\DevOps Project"
ls research-data/baseline-week-1/
```

**Expected structure:**
```
research-data/
├── baseline-week-1/
│   ├── main/
│   │   ├── bandit-results/
│   │   ├── gitleaks-results/
│   │   ├── trivy-results/
│   │   └── metadata.json
│   └── hardened/
│       ├── bandit-results/
│       ├── gitleaks-results/
│       ├── trivy-results/
│       └── metadata.json
├── download-logs/
│   └── download_YYYYMMDD_HHMMSS.log
└── ml-pipeline/output/
    └── features_YYYYMMDD_HHMMSS.csv
```

---

## ✅ **SUCCESS CRITERIA**

After completing all steps, you should have:

- [ ] 2 completed workflow runs (main + hardened)
- [ ] All artifacts downloaded to `research-data/`
- [ ] Features extracted to `ml-pipeline/output/`
- [ ] No errors in download logs

---

## 🚨 **If Something Goes Wrong**

### **Problem: Workflow fails**
**Solution:** Check the workflow logs on GitHub Actions page

### **Problem: Artifacts not downloading**
**Solution:**
```bash
# Check if artifacts exist
python scripts/check_all_artifacts.py

# Try manual download
python scripts/download_specific_artifacts.py
```

### **Problem: Missing data**
**Solution:**
```bash
# Check what's missing
python scripts/check-missing-data.ps1
```

---

## 🎯 **Quick Commands Summary**

```bash
# 1. Check workflow status
python scripts/check_workflow_details.py

# 2. Download everything
python scripts/automated-weekly-collection.py

# 3. Verify data
ls research-data/baseline-week-1/

# 4. Check features
ls ml-pipeline/output/

# 5. View download logs
cat research-data/download-logs/*.log
```

---

**Let me know when both workflows are triggered and I'll help monitor and download everything!**
