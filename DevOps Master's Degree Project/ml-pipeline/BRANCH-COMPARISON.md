# Main vs Hardened Branch Comparison

**Date:** 2025-12-06
**Branches Compared:** `main` vs `hardened`
**Features Extracted:** 208 features per branch

---

## Executive Summary

Successfully extracted and compared features from both `main` and `hardened` branches. Found **11 differences** in code change metrics, demonstrating that the GitHub integration is correctly capturing branch-specific commit history.

**Key Finding:** Security scan features are identical between branches because both read from the same `research-data` directory. However, code change features differ significantly, reflecting the actual development history of each branch.

---

## Differences Found (11 features)

### Code Change Metrics Comparison

| Feature | Main Branch | Hardened Branch | Difference |
|---------|-------------|-----------------|------------|
| **Commits (7 days)** | 5 | 4 | -1 commit |
| **Commits/day avg** | 0.625 | 0.500 | -20% |
| **Lines added** | 65,468 | 50,459 | -15,009 lines (-23%) |
| **Lines deleted** | 314 | 313 | -1 line |
| **Lines changed** | 65,782 | 50,772 | -15,010 lines (-23%) |
| **Files changed** | 192 | 189 | -3 files |
| **Avg commit size** | 13,156 lines | 12,693 lines | -463 lines |
| **Large commits (>500)** | 2 | 1 | -1 large commit |
| **Avg message length** | 242 chars | 195 chars | -47 chars (-19%) |
| **Binary files changed** | 145 | 143 | -2 files |
| **Commits without review** | 5 | 4 | -1 commit |

### Analysis:

**Main Branch:**
- More active development (5 commits vs 4)
- Larger code changes (+15,009 more lines added)
- More files modified
- More large commits (2 vs 1)
- Longer commit messages
- More binary file changes

**Hardened Branch:**
- Slightly less activity
- Smaller overall changes
- Fewer files touched
- More concise commit messages
- Fewer binary changes

---

## Identical Features (197 features)

### Security Features (ALL IDENTICAL)

Both branches show **identical security metrics**:

```
Security Posture:
├─ Risk Score:              100/100 (SAME)
├─ Critical Vulnerabilities: 3 (SAME)
├─ High Severity:           7 (SAME)
├─ Medium Severity:         36 (SAME)
├─ Container Issues:        51 (SAME)
└─ IaC Misconfigurations:   333 (SAME)
```

**Why?** Both branches read security scan results from the same `research-data/` directory, which contains scans from the main branch.

### CI/CD Features (ALL IDENTICAL)

```
CI/CD Performance:
├─ Pipeline Runs:           3 (SAME)
├─ Success Rate:            0.0% (SAME)
├─ Average Duration:        3 minutes (SAME)
├─ DORA Lead Time:          2.0 hours (SAME)
└─ DORA MTTR:               4.0 hours (SAME)
```

**Why?** CI/CD metadata in `research-data/` is from main branch workflow runs.

### Infrastructure, Containers, Deployments, Access Logs, Network (ALL IDENTICAL)

All these features use estimates or data from `research-data/`, so they're identical.

---

## What This Tells Us

### ✅ What's Working:

1. **GitHub Integration Working Perfectly**
   - Correctly captures branch-specific commit history
   - Different branches show different code change patterns
   - Real-time API integration functioning

2. **Code Change Differentiation**
   - Main branch shows more active development
   - Hardened branch shows different commit patterns
   - Can track development velocity per branch

### ⚠️ Current Limitation:

**Security metrics are identical** because:
- Research data is collected once (from main branch)
- Both branches read from same `research-data/` directory
- Security scan results don't reflect branch-specific code

---

## How to Get Branch-Specific Security Data

### Option 1: Run Scans on Each Branch (Recommended)

```bash
# On main branch
git checkout main
cd ../scripts/security-scanning
./run-all-scans.sh  # Save to research-data/main/

# On hardened branch
git checkout hardened
./run-all-scans.sh  # Save to research-data/hardened/

# Then extract separately
python ml-pipeline/extract_all_features.py --data-dir research-data/main
python ml-pipeline/extract_all_features.py --data-dir research-data/hardened
```

### Option 2: Separate Research Data Directories

```bash
# Configure extractor to use branch-specific data
git checkout main
python extract_all_features.py  # Reads from research-data/main/

git checkout hardened
python extract_all_features.py  # Reads from research-data/hardened/
```

### Option 3: Use GitHub Security Scanning API

The security scan extractor could be enhanced to pull results directly from GitHub Security tab, which would be branch-specific.

---

## Detailed Feature Breakdown

### Features That Differ (GitHub API - Branch Aware):
- commits_count
- commits_per_day_avg
- lines_added_total
- lines_deleted_total
- lines_changed_total
- files_changed_count
- commit_size_avg_lines
- large_commits_count
- commit_message_length_avg
- binary_files_changed_count
- commits_without_review_count

**Total:** 11 features (5% of dataset)

### Features That Are Identical (Data from research-data/):
- All 21 security features
- All 35 CI/CD features
- All 24 container features
- All 22 deployment features
- All 40 infrastructure features
- All 28 access log features
- All 15 network features
- 14 of 25 code change features (non-GitHub API based)

**Total:** 197 features (95% of dataset)

---

## Research Implications

### Current State:

**Can Compare:**
- Code change patterns between branches
- Commit velocity and patterns
- Development activity levels

**Cannot Compare (yet):**
- Security vulnerabilities per branch
- CI/CD performance per branch
- Runtime behavior differences

### To Enable Full Comparison:

1. **Run security scans on both branches separately**
   - This will show if hardened branch actually has fewer vulnerabilities
   - Most important for your research thesis

2. **Run CI/CD on both branches**
   - Compare pipeline success rates
   - Compare build times

3. **Deploy both branches to separate environments**
   - Collect runtime metrics from each
   - Compare infrastructure, access logs, network traffic

---

## Saved Files

### Branch-Specific Feature Files:

```
ml-pipeline/output/
├── features_main_branch.csv              # Main branch extraction
├── features_main_branch_transposed.csv
├── features_hardened_branch.csv          # Hardened branch extraction
└── features_hardened_branch_transposed.csv
```

### Comparison Commands:

```bash
# View main branch features
cat output/features_main_branch_transposed.csv

# View hardened branch features
cat output/features_hardened_branch_transposed.csv

# Compare side by side
paste output/features_main_branch_transposed.csv output/features_hardened_branch_transposed.csv
```

---

## Next Steps

### Immediate:
1. ✅ **Confirmed:** GitHub integration captures branch-specific data
2. ✅ **Confirmed:** Code change metrics differ between branches
3. ⚠️ **Found:** Security data is shared (from research-data/)

### Short Term (This Week):
4. **Run security scans on hardened branch separately**
   ```bash
   git checkout hardened
   mkdir -p ../research-data/hardened-week-1
   # Run scans, save to research-data/hardened-week-1/
   ```

5. **Update extractor to use branch-specific research-data**
   ```python
   # Add --branch parameter to extract_all_features.py
   data_dir = Path(f"research-data/{branch_name}/")
   ```

6. **Re-run comparison with branch-specific security data**

### Medium Term (Next 2 Weeks):
7. Run CI/CD on both branches, collect separate metadata
8. Deploy both branches, collect runtime metrics
9. Build complete comparison dataset

### Long Term (Weeks 3-4):
10. ML model training on branch comparison data
11. Feature importance analysis: which features best distinguish secure vs vulnerable code?
12. Write thesis section on branch comparison findings

---

## Key Insights

### 1. GitHub Integration Success
The GitHub API integration is working perfectly. It correctly:
- Identifies the current branch
- Fetches branch-specific commit history
- Calculates accurate code change metrics per branch

### 2. Main Branch More Active
The main branch shows:
- 25% more commits (5 vs 4)
- 23% more lines added (65,468 vs 50,459)
- 100% more large commits (2 vs 1)

This suggests main branch has more ongoing development.

### 3. Research Data Limitation Identified
Current limitation: Security scans stored in shared `research-data/` directory.

**Solution:** Run scans on each branch separately and store in branch-specific directories.

### 4. Feature Distribution
- **5% features** are branch-aware (GitHub API)
- **95% features** currently read from shared research-data

**Opportunity:** Collecting branch-specific research data will make 95% of features branch-aware!

---

## Conclusion

The branch comparison successfully demonstrates:

✅ **Working:** GitHub-based code change tracking per branch
✅ **Working:** Feature extraction pipeline on multiple branches
✅ **Identified:** Need for branch-specific security scan data
✅ **Ready:** For full branch comparison once security data separated

**Main vs Hardened Comparison Status:**
- **Code Changes:** ✅ Different (5 vs 4 commits, 23% more code in main)
- **Security:** ⏳ Pending branch-specific scans
- **CI/CD:** ⏳ Pending branch-specific runs
- **Runtime:** ⏳ Pending separate deployments

**Next Priority:** Run security scans on hardened branch to enable meaningful security comparison.

---

*Generated: 2025-12-06*
*ML Pipeline Version: 1.1*
*Status: Branch comparison complete - Code changes differ, Security data needs branching*
