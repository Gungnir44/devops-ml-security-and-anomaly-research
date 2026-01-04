# Alternative Data Sources for ML Training

## Problem

You need **21+ samples** for ML training but currently have only 2.

**Options:**
1. Wait 2-4 weeks for daily data collection ⏰
2. **Use alternative data sources NOW** ⚡

This guide explores immediate alternatives.

---

## Option 1: Historical GitHub Actions Artifacts ⭐ (BEST)

**Idea:** Download older workflow artifacts from the past 30-90 days instead of just last 7 days.

### Check What's Available

```bash
cd "C:\Users\joshu\Desktop\DevOps Project"
python scripts/check_all_artifacts.py
```

This shows ALL runs with artifacts, even from months ago.

### Modify Collection Script

Update `automated-weekly-collection.py`:

```python
# Change this line:
collector = AutomatedDataCollector(days_back=7)

# To this:
collector = AutomatedDataCollector(days_back=90)  # Last 3 months
```

Then run:
```bash
python scripts/automated-weekly-collection.py --days 90
```

**Expected result:**
- ✅ 30-90 data points (depending on workflow run frequency)
- ✅ Real production data
- ✅ Ready to train immediately
- ✅ No manual work

**Limitations:**
- GitHub only keeps artifacts for 90 days (default retention)
- Older data may have different security configurations

**Recommendation:** ⭐ **Try this first!** It's the easiest and most likely to give you enough data.

---

## Option 2: Multiple Commits as Data Points

**Idea:** Each commit in your repository represents a different code state. Run feature extraction on multiple historical commits.

### How It Works

```bash
# Get list of recent commits
git log --oneline -n 20

# For each commit:
# 1. Checkout the commit
# 2. Run security scans
# 3. Extract features
# 4. Label as vulnerable or secured based on branch
```

### Create Automated Script

Create `scripts/extract-from-commits.sh`:

```bash
#!/bin/bash

COMMITS=$(git log --format="%H" -n 20 main)
OUTPUT_DIR="research-data/historical-commits"

for commit in $COMMITS; do
    echo "Processing commit: $commit"

    # Checkout commit
    git checkout $commit

    # Run security scans
    bash scripts/security-scanning/scan-all.sh

    # Extract features
    python ml-pipeline/extract_all_features.py \
        --data-dir security-scan-results/latest \
        --branch main \
        --output-suffix "commit_${commit:0:7}"

    # Move results
    mkdir -p $OUTPUT_DIR/$commit
    mv security-scan-results/latest/* $OUTPUT_DIR/$commit/
done

# Return to current state
git checkout main
```

**Expected result:**
- 20+ data points from main branch
- Do same for hardened branch
- Total: 40+ samples

**Limitations:**
- Time consuming (scans take 5-10 min each)
- Older commits may be very different
- Security tool versions may change results

---

## Option 3: Create Feature Branch Variants

**Idea:** Create multiple branches with different security levels.

### Security Level Variants

Create these branches:

```bash
# 1. Critically vulnerable (introduce intentional issues)
git checkout -b feature/critical-vulns
# Add: Hardcoded secrets, SQL injection, outdated dependencies
git commit -am "Test: Critical vulnerabilities"

# 2. Moderately vulnerable
git checkout -b feature/moderate-vulns
# Add: Some ESLint errors, missing validation
git commit -am "Test: Moderate vulnerabilities"

# 3. Lightly vulnerable
git checkout -b feature/light-vulns
# Add: Code style issues, minor warnings
git commit -am "Test: Light vulnerabilities"

# 4. Partially hardened
git checkout -b feature/partial-hardening
# Fix half the issues
git commit -am "Test: Partial hardening"

# 5. Fully hardened (your existing hardened branch)
```

**Push all branches to trigger workflows:**
```bash
git push origin feature/critical-vulns
git push origin feature/moderate-vulns
git push origin feature/light-vulns
git push origin feature/partial-hardening
```

**Wait 24 hours, then collect:**
```bash
python scripts/automated-weekly-collection.py --days 2
```

**Expected result:**
- 5 branches × ~3 workflow runs each = **15 data points**
- Labeled classes: critical (2), high (1), medium (0.5), low (0.2), secured (0)
- **Multi-class classification** instead of binary!

**Advantages:**
- Quick (< 1 day)
- More nuanced than binary classification
- Real workflow data

**Limitations:**
- Requires manual branch creation
- May contaminate your repository

---

## Option 4: Trigger Manual Workflow Runs

**Idea:** GitHub Actions allows manual workflow triggers. Run the same workflow multiple times to generate data.

### Enable Manual Triggers

Your workflows already have:
```yaml
on:
  workflow_dispatch:  # Manual trigger
```

### Trigger Multiple Times

```bash
# Use GitHub CLI to trigger workflow
gh workflow run security-scanning.yml --ref main

# Wait 10 minutes, then trigger again
sleep 600
gh workflow run security-scanning.yml --ref main

# Repeat 10-20 times
```

**Or use a loop:**
```bash
for i in {1..20}; do
    echo "Triggering run #$i"
    gh workflow run security-scanning.yml --ref main
    sleep 600  # Wait 10 minutes between runs
done
```

**Expected result:**
- 20 runs on main branch
- Do same for hardened branch
- Total: **40 data points**

**Advantages:**
- Simple automation
- Consistent environment
- Real CI/CD data

**Limitations:**
- Time consuming (20 runs × 10 min = 3.3 hours)
- Same code, so features will be very similar
- May hit GitHub Actions minutes quota

---

## Option 5: Synthetic Data with Realistic Variation

**Idea:** Generate synthetic samples that mimic real security variations.

### Create Synthetic Generator

Create `ml-pipeline/generate_synthetic_data.py`:

```python
import pandas as pd
import numpy as np

def generate_synthetic_samples(base_df, n_samples=20, variation='realistic'):
    """Generate synthetic samples with realistic variation."""

    samples = []

    for i in range(n_samples):
        sample = base_df.copy()

        if variation == 'realistic':
            # Add realistic variations

            # Security metrics: Add Poisson noise (vulnerabilities come in clusters)
            security_cols = [col for col in sample.columns if 'vuln' in col or 'security' in col]
            for col in security_cols:
                if sample[col].values[0] > 0:
                    sample[col] = np.random.poisson(sample[col].values[0])

            # CI/CD metrics: Add Gaussian noise (timing variations)
            cicd_cols = [col for col in sample.columns if 'duration' in col or 'time' in col]
            for col in cicd_cols:
                sample[col] = sample[col] + np.random.normal(0, 0.1 * sample[col].std())

            # Container metrics: Slight variations
            container_cols = [col for col in sample.columns if 'container' in col or 'pod' in col]
            for col in container_cols:
                sample[col] = sample[col] * np.random.uniform(0.9, 1.1)

        samples.append(sample)

    return pd.concat(samples, ignore_index=True)

# Load baseline
df_main = pd.read_csv('output/features_main_branch.csv')
df_hardened = pd.read_csv('output/features_hardened_local.csv')

# Generate 20 synthetic variants of each
df_main_synthetic = generate_synthetic_samples(df_main, 20)
df_hardened_synthetic = generate_synthetic_samples(df_hardened, 20)

# Save
df_main_synthetic.to_csv('output/synthetic_main_samples.csv', index=False)
df_hardened_synthetic.to_csv('output/synthetic_hardened_samples.csv', index=False)

print("Generated 40 synthetic samples!")
```

**Expected result:**
- **40 synthetic samples** (20 main + 20 hardened)
- Based on real baseline data
- Realistic variation patterns

**Advantages:**
- Instant (< 1 minute)
- Full control over sample size
- Can test ML pipeline immediately

**Limitations:**
- Not real data (note in thesis!)
- May not capture true variations
- Use only for pipeline testing, not final results

---

## Option 6: Public DevOps/Security Datasets

**Idea:** Use existing public datasets to supplement your data.

### Available Datasets

1. **CVE Database**
   - Source: https://cve.mitre.org/data/downloads/
   - Contains: Vulnerability details, severity scores
   - Use for: Training vulnerability classifiers

2. **NVD (National Vulnerability Database)**
   - Source: https://nvd.nist.gov/vuln/data-feeds
   - Format: JSON feeds
   - Use for: CVE/CWE analysis

3. **GitHub Security Advisories**
   - Source: GitHub API
   - Contains: Security issues in popular repos
   - Use for: Real-world vulnerability patterns

4. **OWASP Benchmark**
   - Source: https://owasp.org/www-project-benchmark/
   - Contains: Test cases for security scanners
   - Use for: Validation

### Example: Download CVE Data

```python
import requests
import json

# Download recent CVEs
url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
response = requests.get(url, params={"resultsPerPage": 100})
cves = response.json()

# Extract features similar to yours
for cve in cves['vulnerabilities']:
    cve_data = cve['cve']
    # Extract: severity, CWE, affected systems
    # Map to your 208-feature format
```

**Advantages:**
- Large datasets available
- Real vulnerability data
- Free and public

**Limitations:**
- Different format than your features
- Requires mapping/transformation
- May not match your DevOps context

---

## Option 7: Cross-Repository Data Collection

**Idea:** If you have other repositories, collect data from them too.

### Requirements

- Similar project structure
- Same workflows configured
- Both vulnerable and hardened variants

### Collection Script

```python
repos = [
    "Gungnir44/devops-ml-security-and-anomaly-research",
    "Gungnir44/other-project-1",
    "Gungnir44/other-project-2",
]

for repo in repos:
    # Download artifacts from each repo
    collector = AutomatedDataCollector(repo_name=repo)
    collector.run()
```

**Expected result:**
- 3 repos × 14 samples = **42 data points**

**Limitations:**
- Need multiple similar projects
- Different codebases may have different baselines

---

## Recommendation: Best Strategy

### Immediate (Today):

**1. Try Historical Artifacts (90 days)** ⭐ BEST OPTION
```bash
python scripts/automated-weekly-collection.py --days 90
```

**Expected: 30-90 samples** → Ready to train!

If that doesn't give enough:

**2. Create Feature Branch Variants**
- 5 security level branches
- **Expected: +15 samples**

**Combined: 45-105 samples** → Excellent for training!

### Backup Plan:

**3. Generate Synthetic Data**
- Use for pipeline testing only
- Note in thesis it's for validation, not final results
- **Expected: 40 samples** → Can train and test pipeline

### Long-term (Still do this):

**4. Continue Weekly Collection**
- Run every Sunday for 4 weeks
- Accumulates real production data
- Use for final thesis experiments

---

## Implementation Guide

### Step 1: Check Historical Data Availability

```bash
cd "C:\Users\joshu\Desktop\DevOps Project"

# Check what artifacts exist
python scripts/check_all_artifacts.py
```

Look for:
- Total number of runs with artifacts
- Date range (how far back)
- Which workflows have data

### Step 2: Download Historical Data

```bash
# Try 90 days first
python scripts/automated-weekly-collection.py --days 90

# Check how many samples you got
wc -l ml-pipeline/output/time_series_dataset.csv
```

If you get **21+ samples** → Go to Step 4!

### Step 3: (If needed) Create Branch Variants

```bash
# Create security level branches
git checkout -b feature/critical-vulns
# Make intentional security mistakes
git commit -am "Test: Critical vulnerabilities"
git push origin feature/critical-vulns

# Repeat for other levels
# Wait 24 hours for workflows to run
# Then collect again
python scripts/automated-weekly-collection.py --days 2
```

### Step 4: Train Your Models!

```bash
cd ml-pipeline

# Check sample count
python -c "import pandas as pd; print(len(pd.read_csv('output/time_series_dataset.csv')))"

# If >= 21 samples:
python train_baseline_models.py --data-file output/time_series_dataset.csv
```

---

## Thesis Considerations

### If Using Historical Data:
✅ **Acceptable**: "We collected security scan data from 90 days of CI/CD workflow runs..."
- Real production data
- Temporal variation
- Multiple code states

### If Using Branch Variants:
✅ **Acceptable**: "We created branches representing different security postures (critical, high, medium, low, secured) to evaluate classification performance..."
- Intentional experimental design
- Controlled variation
- Clear labeling

### If Using Synthetic Data:
⚠️ **Use carefully**: "Synthetic data was generated for pipeline validation. Final experiments used real data collected over 4 weeks..."
- Note it's for testing only
- Don't use for main results
- Use real data for final experiments

---

## Summary Table

| Method | Time | Samples | Quality | Effort |
|--------|------|---------|---------|--------|
| **Historical artifacts (90d)** | 1 hour | 30-90 | ⭐⭐⭐⭐⭐ | Low |
| Branch variants | 1 day | 15-20 | ⭐⭐⭐⭐ | Medium |
| Manual triggers | 3-4 hours | 40+ | ⭐⭐⭐⭐ | Low |
| Historical commits | 4-8 hours | 40+ | ⭐⭐⭐ | High |
| Synthetic data | 5 min | Any | ⭐⭐ | Low |
| Weekly collection (4 weeks) | 4 weeks | 35+ | ⭐⭐⭐⭐⭐ | Very Low |

---

## My Recommendation

**Do this RIGHT NOW:**

```bash
# Step 1: Check what's available
cd "C:\Users\joshu\Desktop\DevOps Project"
python scripts/check_all_artifacts.py

# Step 2: Download 90 days of historical data
python scripts/automated-weekly-collection.py --days 90

# Step 3: Check if you have enough samples
python -c "import pandas as pd; df=pd.read_csv('ml-pipeline/output/time_series_dataset.csv'); print(f'Total samples: {len(df)}')"

# Step 4: If >= 21 samples, TRAIN NOW!
cd ml-pipeline
python train_baseline_models.py --data-file output/time_series_dataset.csv
```

**Most likely outcome:** You'll get 30-90 samples from historical data and can start training TODAY! 🎉

Want me to help you run these commands and see what data is available?
