# Full 208-Feature Branch Comparison Guide

**Date:** 2025-12-06
**Goal:** Compare all 208 features between `main` (vulnerable) and `hardened` (secured) branches
**Current Status:** Extraction script updated, infrastructure ready

---

## Quick Summary

**What We Have:**
- ✅ Extraction script updated with `--branch` parameter
- ✅ Both branches have GitHub Actions workflows configured
- ✅ Hardened branch has security fixes applied (ESLint errors fixed, npm vulnerabilities resolved)
- ✅ GitHub is collecting data from both branches

**What We Need:**
- Download GitHub Actions artifacts from hardened branch
- Organize data into branch-specific directories
- Re-extract features with branch-specific data
- Generate full comparison

---

## Expected Security Differences

Based on the hardened branch fixes:

### Main Branch (Vulnerable):
- 151+ security findings
- 6 moderate npm vulnerabilities
- ESLint errors (6 total)
- Intentionally vulnerable code

### Hardened Branch (Secured):
- All ESLint errors fixed
- npm vulnerabilities: 6 → 0
- Best practices applied
- Updated dependencies (vite, vitest)

**Expected Feature Changes:**
- ✅ `npm_vulnerabilities`: 6 → 0 (from 6 moderate to 0)
- ✅ `sast_code_smells`: Reduced (ESLint errors fixed)
- ✅ `vuln_medium_count`: Reduced
- ✅ `security_risk_score`: 100 → Lower (expect 40-60)

---

## Method 1: Download GitHub Actions Data (RECOMMENDED)

This is the proper way to get real, branch-specific security scan data.

### Step 1: Download Hardened Branch Artifacts

```bash
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"

# Download artifacts from hardened branch
# The automated download script should support --branch parameter
python download_research_data.py --branch hardened

# Or manually trigger hardened branch workflows and download
```

### Step 2: Organize Data

```bash
cd "C:\Users\joshu\Desktop\DevOps Project"

# Move main branch data
mkdir -p research-data/main-branch/baseline-week-1
cp -r research-data/baseline-week-1/* research-data/main-branch/baseline-week-1/

# Download hardened branch data to separate directory
mkdir -p research-data/hardened-branch/baseline-week-1
# Copy downloaded hardened branch artifacts here
```

### Step 3: Extract Features from Each Branch

```bash
cd "C:\Users\joshu\Desktop\DevOps Project\DevOps Master's Degree Project\ml-pipeline"

# Extract from main branch
export GITHUB_TOKEN="your_token_here"
python extract_all_features.py --branch main --output-suffix "_main"

# Extract from hardened branch
python extract_all_features.py --branch hardened --output-suffix "_hardened"
```

### Step 4: Compare Results

```python
cd output
python compare_branches.py features_main.csv features_hardened.csv
```

---

## Method 2: Quick Comparison (Current Available Data)

Use what we have now - shows partial comparison.

### What's Currently Different:

We already extracted and compared:

```bash
# Already done - code change features show differences
Main branch:     5 commits, 65,468 lines added
Hardened branch: 4 commits, 50,459 lines added

# 11 features differ (all code change metrics)
```

**Security features are currently identical** because both read from the same research-data directory (collected from main branch).

---

## Method 3: Trigger New Workflow Runs

Force fresh data collection from both branches.

### Step 1: Trigger Workflows on Hardened Branch

```bash
# Using GitHub CLI
cd "C:\Users\joshu\Desktop\DevOps Project"

# Trigger security scanning on hardened branch
gh workflow run "Security Scanning Suite" --ref hardened

# Trigger CI/CD workflows
gh workflow run "Frontend CI/CD" --ref hardened
gh workflow run "Backend API CI/CD" --ref hardened
gh workflow run "Python Service CI/CD" --ref hardened
```

### Step 2: Wait for Completion

```bash
# Monitor workflow status
gh run list --branch hardened --limit 10

# Wait for "Security Scanning Suite" to complete
gh run watch
```

### Step 3: Download Artifacts

```bash
# Download specific workflow run artifacts
gh run download <run-id> --dir research-data/hardened-branch/
```

### Step 4: Extract and Compare

Same as Method 1, Step 3-4.

---

## Automated Solution: Enhanced Download Script

### Update download_research_data.py

Add branch support to the automated download script:

```python
# In scripts/download_research_data.py

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', default='main',
                        help='Branch to download data from')
    args = parser.parse_args()

    # Download artifacts filtered by branch
    branch = args.branch
    output_dir = f"research-data/{branch}-branch/"

    # Filter workflow runs by branch
    runs = repo.get_workflow_runs(branch=branch)
    # ... rest of download logic
```

### Run Enhanced Script

```bash
cd scripts

# Download main branch data
python download_research_data.py --branch main

# Download hardened branch data
python download_research_data.py --branch hardened
```

---

## Comparison Analysis Script

### Create compare_branches.py

```python
"""
Compare features between main and hardened branches
"""

import pandas as pd
import sys

def compare_branches(main_file, hardened_file):
    # Load data
    main_df = pd.read_csv(main_file)
    hardened_df = pd.read_csv(hardened_file)

    # Find differences
    differences = []
    for col in main_df.columns:
        if col in hardened_df.columns:
            main_val = main_df[col].iloc[0]
            hard_val = hardened_df[col].iloc[0]

            if main_val != hard_val:
                # Calculate percent change
                if main_val != 0:
                    pct_change = ((hard_val - main_val) / main_val) * 100
                else:
                    pct_change = 0

                differences.append({
                    'feature': col,
                    'main': main_val,
                    'hardened': hard_val,
                    'change': hard_val - main_val,
                    'pct_change': pct_change
                })

    # Create comparison dataframe
    diff_df = pd.DataFrame(differences)
    diff_df = diff_df.sort_values('pct_change', key=abs, ascending=False)

    # Print report
    print("=" * 80)
    print("BRANCH COMPARISON REPORT")
    print("=" * 80)
    print()
    print(f"Total features compared: {len(main_df.columns)}")
    print(f"Features with differences: {len(differences)}")
    print(f"Identical features: {len(main_df.columns) - len(differences)}")
    print()

    if differences:
        print("TOP 20 DIFFERENCES:")
        print("-" * 80)
        print(diff_df.head(20).to_string(index=False))
        print()

        # Security-focused analysis
        security_features = diff_df[diff_df['feature'].str.contains('vuln|security|secret|container|iac', case=False)]
        if not security_features.empty:
            print("SECURITY FEATURE CHANGES:")
            print("-" * 80)
            print(security_features.to_string(index=False))

    # Save full comparison
    diff_df.to_csv('branch_comparison_full.csv', index=False)
    print()
    print("[+] Full comparison saved to: branch_comparison_full.csv")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_branches.py <main_features.csv> <hardened_features.csv>")
        sys.exit(1)

    compare_branches(sys.argv[1], sys.argv[2])
```

---

## Expected Results

### Security Improvements (Hardened vs Main):

| Feature | Main | Hardened | Change |
|---------|------|----------|--------|
| `security_risk_score` | 100 | ~50 | -50% |
| `npm_vulnerabilities` | 6 | 0 | -100% |
| `vuln_medium_count` | 36+ | ~15 | -60% |
| `sast_code_smells` | 64+ | ~30 | -50% |
| `code_quality_score` | Low | Higher | +50% |

### Code Change Differences (Already Measured):

| Feature | Main | Hardened | Change |
|---------|------|----------|--------|
| `commits_count` | 5 | 4 | -1 |
| `lines_added_total` | 65,468 | 50,459 | -23% |
| `large_commits_count` | 2 | 1 | -50% |

---

## Current Status

### ✅ Completed:
1. Created branch-specific research data directories
2. Updated extraction script with `--branch` parameter
3. Extracted features showing code change differences
4. Documented expected security differences

### ⏳ Pending:
1. Download GitHub Actions artifacts from hardened branch
2. Organize hardened branch data into research-data/hardened-branch/
3. Re-extract features with branch-specific data
4. Generate full 208-feature comparison report

### 🎯 Next Immediate Step:

**Download hardened branch data from GitHub Actions:**

```bash
# Option A: Use automated script (if updated)
cd scripts
python download_research_data.py --branch hardened

# Option B: Manually download specific workflow runs
gh run list --branch hardened
gh run download <run-id> --dir ../research-data/hardened-branch/
```

---

## Files Created

### Scripts:
- `extract_all_features.py` - Updated with `--branch` parameter ✅
- `compare_branches.py` - Comparison analysis script (template above)

### Directories:
```
research-data/
├── main-branch/         ✅ Created
│   └── baseline-week-1/ ✅ Populated (existing data)
├── hardened-branch/     ✅ Created
│   └── baseline-week-1/ ⏳ Awaiting GitHub Actions data
```

### Documentation:
- `FULL-COMPARISON-GUIDE.md` - This file
- `BRANCH-COMPARISON.md` - Partial comparison (code changes only)
- `DATA-SOURCE-UPGRADE.md` - GitHub integration details

---

## Timeline Estimate

### If data is already available on GitHub:
- Download hardened artifacts: **10 minutes**
- Extract features: **2 minutes** (per branch)
- Generate comparison: **1 minute**
- **Total: ~15 minutes**

### If triggering new workflows:
- Trigger workflows: **2 minutes**
- Wait for completion: **5-10 minutes**
- Download artifacts: **10 minutes**
- Extract and compare: **5 minutes**
- **Total: ~25-30 minutes**

---

## Research Value

### With Full Comparison You Can:

1. **Quantify Security Improvements**
   - Exact reduction in vulnerabilities
   - Change in risk score
   - Code quality metric improvements

2. **Train ML Models**
   - Binary classification: vulnerable vs secure
   - Anomaly detection: detect unusual security patterns
   - Feature importance: which fixes matter most

3. **Validate Hardening Effectiveness**
   - Did fixes actually reduce security risk?
   - Which categories improved most?
   - Are there remaining issues?

4. **Thesis Data**
   - Before/after comparison
   - Evidence of security improvements
   - ML model performance on real security fixes

---

## Troubleshooting

### Issue: No hardened branch artifacts found

**Solution:** Trigger workflows manually
```bash
gh workflow run "Security Scanning Suite" --ref hardened
```

### Issue: Download script doesn't support --branch

**Solution:** Manually filter by branch
```bash
gh run list --branch hardened --workflow "Security Scanning Suite"
gh run download <latest-run-id>
```

### Issue: Extraction fails on hardened-branch directory

**Solution:** Check data structure matches expected format
```bash
ls -R research-data/hardened-branch/
# Should have same structure as main-branch
```

---

## Conclusion

**You're almost there!** The infrastructure is ready for full 208-feature comparison. You just need to:

1. Download hardened branch GitHub Actions artifacts
2. Run extraction on both branches with branch-specific data
3. Compare and analyze

**Current Capability:**
- 11/208 features compared ✅ (code changes)
- 197/208 pending branch-specific security data ⏳

**Next Action:**
Download hardened branch artifacts from GitHub Actions to enable full comparison.

---

*Generated: 2025-12-06*
*ML Pipeline Version: 1.1*
*Status: Infrastructure ready - Awaiting hardened branch security data*
