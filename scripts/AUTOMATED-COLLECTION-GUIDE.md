# Automated Weekly Data Collection Guide

## Overview

The `automated-weekly-collection.py` script automatically:
1. ✅ Downloads artifacts from GitHub Actions (last 7 days by default)
2. ✅ Organizes data by date and branch (main, hardened)
3. ✅ Extracts 208 features from each dataset
4. ✅ Builds a time-series CSV for longitudinal analysis
5. ✅ Generates a summary report

## Quick Start

### First Time Setup

```bash
# Ensure you have the GitHub token
cat .github_token  # Should show your token

# Test with dry run (see what would be downloaded)
python automated-weekly-collection.py --dry-run
```

### Weekly Collection (Recommended Usage)

```bash
# Run every Sunday to collect the past week's data
cd "C:\Users\joshu\Desktop\DevOps Project"
python scripts/automated-weekly-collection.py
```

This will:
- Download all artifacts from Security Scanning Suite workflows (last 7 days)
- Extract features automatically
- Create/update `ml-pipeline/output/time_series_dataset.csv`
- Generate a report in `research-data/time-series/collection_report_*.md`

## Usage Options

### Download Last 14 Days
```bash
python automated-weekly-collection.py --days 14
```

### Download Only (No Feature Extraction)
```bash
# Useful if you want to review raw data first
python automated-weekly-collection.py --download-only
```

### Extract Features Only (From Already Downloaded Data)
```bash
# Useful if extraction failed previously
python automated-weekly-collection.py --extract-only
```

### Dry Run (See What Would Happen)
```bash
python automated-weekly-collection.py --dry-run
```

## Directory Structure Created

```
research-data/
└── time-series/
    ├── 2025-12-06/
    │   ├── main/
    │   │   ├── trufflehog-results/
    │   │   ├── gitleaks-results/
    │   │   ├── trivy-results/
    │   │   └── ...
    │   └── hardened/
    │       ├── trufflehog-results/
    │       └── ...
    ├── 2025-12-07/
    │   ├── main/
    │   └── hardened/
    └── collection_report_YYYYMMDD_HHMMSS.md

ml-pipeline/output/
├── features_main_20251206.csv
├── features_hardened_20251206.csv
├── features_main_20251207.csv
├── features_hardened_20251207.csv
└── time_series_dataset.csv  ← Combined dataset for ML training
```

## Time-Series Dataset Format

The `time_series_dataset.csv` contains:

| Column | Description |
|--------|-------------|
| `date` | Collection date (YYYY-MM-DD) |
| `branch` | main or hardened |
| `timestamp` | Parsed datetime for sorting |
| `vuln_critical_count` | Feature 1 of 208 |
| `vuln_high_count` | Feature 2 of 208 |
| ... | All 208 features |

**Example rows:**
```csv
date,branch,timestamp,vuln_critical_count,vuln_high_count,...
2025-12-06,main,2025-12-06 00:00:00,3,7,...
2025-12-06,hardened,2025-12-06 00:00:00,0,0,...
2025-12-07,main,2025-12-07 00:00:00,3,7,...
2025-12-07,hardened,2025-12-07 00:00:00,0,0,...
```

## Scheduling Weekly Execution

### Option 1: Windows Task Scheduler (Recommended)

1. Open Task Scheduler
2. Create Basic Task
   - **Name:** Weekly Security Data Collection
   - **Trigger:** Weekly, Sunday at 9:00 AM
   - **Action:** Start a program
     - **Program:** `python`
     - **Arguments:** `scripts/automated-weekly-collection.py`
     - **Start in:** `C:\Users\joshu\Desktop\DevOps Project`
3. Save

### Option 2: Manual Reminder

Set a weekly calendar reminder to run:
```bash
python scripts/automated-weekly-collection.py
```

### Option 3: GitHub Actions (Fully Automated)

Create `.github/workflows/weekly-data-collection.yml`:
```yaml
name: Weekly Research Data Collection

on:
  schedule:
    - cron: '0 9 * * 0'  # Every Sunday at 9 AM UTC
  workflow_dispatch:

jobs:
  collect-data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pandas requests

      - name: Run automated collection
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          echo "$GITHUB_TOKEN" > scripts/.github_token
          python scripts/automated-weekly-collection.py

      - name: Commit results
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add research-data/time-series/
          git add ml-pipeline/output/time_series_dataset.csv
          git commit -m "Automated weekly data collection: $(date +%Y-%m-%d)" || true
          git push
```

## Troubleshooting

### Error: GitHub token not found
```bash
# Check if .github_token exists
cat scripts/.github_token

# If missing, create it
echo "your_github_token_here" > scripts/.github_token
```

### Error: No workflow runs found
- Check that the Security Scanning Suite workflow has run in the last 7 days
- Verify the workflow name matches: `security-scanning.yml`
- Try increasing days: `--days 14`

### Error: Feature extraction failed
- Check that `ml-pipeline/extract_all_features.py` exists
- Ensure pandas is installed: `pip install pandas`
- Run with `--extract-only` to retry just the extraction step

### No data downloaded
- Workflows may not have generated artifacts (check GitHub Actions)
- Try `--dry-run` to see what would be downloaded
- Check workflow failures on GitHub

## What Happens Over 4 Weeks

**Week 1 (Now):**
- Run the script, get ~7 data points (daily scans)
- Initial time-series dataset created

**Week 2:**
- Run again, adds 7 more data points (14 total)
- Time-series dataset grows

**Week 3:**
- 21 data points total
- Enough for basic time-series analysis

**Week 4:**
- 28 data points total
- Ready for LSTM/time-series ML models

## Next Steps After Collection

1. **Visualize trends:**
   ```python
   import pandas as pd
   import matplotlib.pyplot as plt

   df = pd.read_csv('ml-pipeline/output/time_series_dataset.csv')
   df_main = df[df['branch'] == 'main']
   df_hardened = df[df['branch'] == 'hardened']

   plt.plot(df_main['date'], df_main['vuln_critical_count'], label='Main')
   plt.plot(df_hardened['date'], df_hardened['vuln_critical_count'], label='Hardened')
   plt.legend()
   plt.show()
   ```

2. **Train ML models** on time-series data

3. **Write thesis sections** using the accumulated evidence

## Support

- **Script location:** `scripts/automated-weekly-collection.py`
- **Documentation:** This file
- **Issues:** Check the collection report in `research-data/time-series/`

---

**Generated:** 2025-12-06
**Research Project:** DevOps ML Security and Anomaly Detection
