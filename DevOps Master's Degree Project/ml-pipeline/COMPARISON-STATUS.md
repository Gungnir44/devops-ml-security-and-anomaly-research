# Full 208-Feature Comparison - STATUS REPORT

**Date:** 2025-12-06
**Status:** Infrastructure Complete - Partial Data Available
**Completion:** 11/208 features compared (5.3%)

---

## What Was Accomplished

### ✅ Infrastructure Built:

1. **Extraction Script Enhanced**
   - Added `--branch` parameter to extract_all_features.py
   - Added `--data-dir` parameter for custom directories
   - Added `--output-suffix` for naming output files
   - Can now extract from branch-specific data directories

2. **Branch Comparison Script Created**
   - `compare_branches.py` - Automated comparison tool
   - Analyzes all 208 features
   - Groups differences by category (security, code, CI/CD)
   - Generates CSV and text summary reports
   - Calculates percent changes

3. **Directory Structure Created**
   ```
   research-data/
   ├── main-branch/         ✅ Ready
   │   └── baseline-week-1/ ✅ Populated with existing data
   └── hardened-branch/     ✅ Ready
       └── baseline-week-1/ ⏳ Awaiting GitHub Actions artifacts
   ```

4. **Documentation Created**
   - `FULL-COMPARISON-GUIDE.md` - Complete step-by-step guide
   - `BRANCH-COMPARISON.md` - Current partial comparison results
   - `COMPARISON-STATUS.md` - This status report

---

## Current Comparison Results

### Features Compared: 208
### Differences Found: 11 (5.3%)
### Identical: 197 (94.7%)

### All 11 Differences are Code Change Features:

| Feature | Main | Hardened | Change |
|---------|------|----------|--------|
| **Large commits (>500 lines)** | 2 | 1 | -50% ✅ |
| **Lines added** | 65,468 | 50,459 | -23% ✅ |
| **Lines changed** | 65,782 | 50,772 | -23% ✅ |
| **Commits/day** | 0.625 | 0.500 | -20% |
| **Total commits** | 5 | 4 | -20% |
| **Commits without review** | 5 | 4 | -20% |
| **Avg commit message** | 242 chars | 195 chars | -19% |
| **Avg commit size** | 13,156 lines | 12,693 lines | -4% |
| **Files changed** | 192 | 189 | -2% |
| **Binary files** | 145 | 143 | -1% |
| **Lines deleted** | 314 | 313 | -0.3% |

**Interpretation:**
- Main branch shows more active development
- Larger code changes on main
- More commits without code review on main
- Hardened branch shows more disciplined development

---

## Why Security Features Are Identical

### Current Data Source:

**Both branches extract from:** `research-data/baseline-week-1/`

**This data was collected from:** Main branch GitHub Actions workflows

**Result:**
```
Security features on BOTH branches:
├─ Risk Score:              100/100 (SAME - from main branch scans)
├─ Critical Vulnerabilities: 3 (SAME)
├─ High Severity:           7 (SAME)
├─ Container Issues:        51 (SAME)
└─ IaC Misconfigurations:   333 (SAME)
```

**These 197 identical features** are all reading from the same source data.

---

## Expected Differences (When Hardened Data Available)

Based on `HARDENED-BRANCH-STATUS.md`, the hardened branch has:

### Applied Fixes:
- ✅ All ESLint errors fixed (6 total)
- ✅ npm vulnerabilities: 6 → 0
- ✅ Package dependencies updated
- ✅ Code quality improvements

### Expected Feature Changes:

| Feature | Main (Current) | Hardened (Expected) | Change |
|---------|----------------|---------------------|--------|
| `npm_vulnerabilities` | 6 | 0 | -100% ✅ |
| `security_risk_score` | 100 | ~40-60 | -40-60% ✅ |
| `vuln_medium_count` | 36 | ~15-20 | -45-55% ✅ |
| `sast_code_smells` | 64 | ~30-40 | -35-50% ✅ |
| `vuln_high_count` | 7 | ~3-5 | -30-50% ✅ |
| `vuln_critical_count` | 3 | ~1-2 | -35-65% ✅ |

**Expected total differences:** 50-80 features (24-38%)

---

## How to Enable Full Comparison

### Method 1: Download Hardened Branch Artifacts (RECOMMENDED)

The hardened branch has already run workflows. You just need to download the artifacts:

```bash
cd "C:\Users\joshu\Desktop\DevOps Project"

# List recent hardened branch workflow runs
gh run list --branch hardened --limit 10

# Find the Security Scanning Suite run
gh run list --branch hardened --workflow "Security Scanning Suite"

# Download artifacts from that run
gh run download <run-id> --dir research-data/hardened-branch/baseline-week-1/

# Extract features from hardened branch
cd "DevOps Master's Degree Project/ml-pipeline"
export GITHUB_TOKEN="your_token_here"
python extract_all_features.py --branch hardened --output-suffix "_hardened_real"

# Compare with main
python compare_branches.py output/features_main_branch.csv output/features_hardened_real.csv
```

### Method 2: Trigger New Workflows

If artifacts aren't available, trigger fresh runs:

```bash
# Trigger workflows on hardened branch
gh workflow run "Security Scanning Suite" --ref hardened
gh workflow run "Frontend CI/CD" --ref hardened
gh workflow run "Backend API CI/CD" --ref hardened

# Wait for completion
gh run watch

# Download and extract
# (same as Method 1 above)
```

---

## Files Created

### Scripts:
```
ml-pipeline/
├── extract_all_features.py (updated) ✅
│   - Added --branch parameter
│   - Added --data-dir parameter
│   - Added --output-suffix parameter
│
├── compare_branches.py (new) ✅
│   - Automated branch comparison
│   - Category-based analysis
│   - Percent change calculations
│
└── output/
    ├── features_main_branch.csv ✅
    ├── features_hardened_branch.csv ✅ (using same data as main currently)
    ├── branch_comparison_full.csv ✅
    └── branch_comparison_summary.txt ✅
```

### Documentation:
```
ml-pipeline/
├── FULL-COMPARISON-GUIDE.md ✅ - Complete step-by-step guide
├── BRANCH-COMPARISON.md ✅ - Current partial results
├── COMPARISON-STATUS.md ✅ - This file
└── DATA-SOURCE-UPGRADE.md ✅ - GitHub integration details
```

---

## What You Can Do Now

### Option A: Get Full Comparison (Recommended for Research)

**Time Required:** 15-30 minutes
**Result:** All 208 features compared with branch-specific data

**Steps:**
1. Download hardened branch GitHub Actions artifacts
2. Extract features: `python extract_all_features.py --branch hardened`
3. Compare: `python compare_branches.py ...`
4. Analyze results for thesis

### Option B: Use Current Data (Quick Analysis)

**Time Required:** Immediate
**Result:** 11 code change features analyzed

**Steps:**
1. Review `output/branch_comparison_full.csv`
2. Analyze code change patterns
3. Use for initial ML experimentation

### Option C: Continue Data Collection

**Time Required:** 2-3 weeks
**Result:** Time-series data for both branches

**Steps:**
1. Let automated downloads continue
2. Collect data weekly from both branches
3. Build temporal dataset
4. Train time-series ML models

---

## Summary

**Infrastructure:** ✅ COMPLETE
- Extraction script supports branch-specific data
- Comparison script automates analysis
- Directory structure ready

**Current Comparison:** ⏳ PARTIAL (11/208 features)
- Code changes differ between branches ✅
- Security data identical (same source) ⏳

**To Complete:** 📥 Download hardened branch GitHub Actions artifacts

**Research Value:**
- Current data shows code change patterns differ
- Full comparison will quantify security improvements
- Can measure ML model performance on real fixes

---

## Quick Start Command

**To complete full 208-feature comparison:**

```bash
# 1. Download hardened branch artifacts
gh run list --branch hardened --workflow "Security Scanning Suite"
gh run download <latest-run-id> --dir research-data/hardened-branch/baseline-week-1/

# 2. Extract features
cd ml-pipeline
python extract_all_features.py --branch hardened --output-suffix "_hardened_real"

# 3. Compare
python compare_branches.py output/features_main_branch.csv output/features_hardened_real.csv

# Done! View results in output/branch_comparison_full.csv
```

---

**Status:** Infrastructure ready, awaiting hardened branch security data for full comparison.

**Next Action:** Download hardened branch GitHub Actions artifacts.

---

*Generated: 2025-12-06*
*ML Pipeline Version: 1.1*
*Comparison Capability: ENABLED - Awaiting full data*
