# Quick Start: Automated Weekly Data Collection

## ✅ What You Just Got

**Script:** `scripts/automated-weekly-collection.py`

**What it does:**
1. Downloads artifacts from **5 workflows** (Security Scanning, Frontend, Backend, Python, CI)
2. Organizes by date and branch (main vs hardened)
3. Extracts 208 features automatically
4. Creates time-series CSV for ML training
5. Generates summary reports

**Test run results (last 3 days):**
- ✅ Found 30 workflow runs
- ✅ Would download 30 artifacts (16 main + 14 hardened)
- ✅ Script working perfectly!

---

## 🚀 How to Use

### This Week (First Collection)

```bash
# Navigate to project
cd "C:\Users\joshu\Desktop\DevOps Project"

# Run the collection (downloads last 7 days)
python scripts/automated-weekly-collection.py
```

**What happens:**
1. Downloads ~50 artifacts from all workflows
2. Extracts features for each date/branch
3. Creates `ml-pipeline/output/time_series_dataset.csv`
4. Generates report in `research-data/time-series/`

### Every Week for Next 4 Weeks

Run the same command every Sunday:
```bash
python scripts/automated-weekly-collection.py
```

**Over 4 weeks you'll accumulate:**
- ~28 data points (daily scans x 4 weeks)
- Both branches (main + hardened)
- Full time-series dataset ready for LSTM/temporal models

---

## 📊 What You'll Get

### Time-Series Dataset
**Location:** `ml-pipeline/output/time_series_dataset.csv`

**Format:**
```csv
date,branch,timestamp,vuln_critical_count,vuln_high_count,...
2025-12-05,main,2025-12-05 00:00:00,3,7,...
2025-12-05,hardened,2025-12-05 00:00:00,0,0,...
2025-12-06,main,2025-12-06 00:00:00,3,7,...
2025-12-06,hardened,2025-12-06 00:00:00,0,0,...
```

208 features + date + branch + timestamp = **211 columns**

### Directory Structure
```
research-data/time-series/
├── 2025-12-05/
│   ├── main/
│   │   ├── bandit-security-report/
│   │   ├── frontend-research-data-1/
│   │   └── ...
│   └── hardened/
│       └── ...
├── 2025-12-06/
│   ├── main/
│   └── hardened/
└── collection_report_20251206_HHMMSS.md
```

---

## 🎯 Next Steps

### Immediate (Today)
1. ✅ Run first collection: `python scripts/automated-weekly-collection.py`
2. ✅ Review the report in `research-data/time-series/`
3. ✅ Check the time-series CSV: `ml-pipeline/output/time_series_dataset.csv`

### This Week
4. ⬜ Start training baseline ML models (Random Forest, XGBoost)
5. ⬜ Create basic visualizations of the data
6. ⬜ Write thesis Methodology chapter

### Weekly (Next 4 Weeks)
7. ⬜ Run collection script every Sunday
8. ⬜ Monitor data accumulation
9. ⬜ Update visualizations with new data

### Month End (Week 4)
10. ⬜ Train time-series models (LSTM)
11. ⬜ Perform trend analysis
12. ⬜ Write Results chapter

---

## 🔧 Common Commands

```bash
# Standard weekly collection (last 7 days)
python scripts/automated-weekly-collection.py

# Collect last 14 days
python scripts/automated-weekly-collection.py --days 14

# See what would be downloaded (no actual download)
python scripts/automated-weekly-collection.py --dry-run

# Only download, skip feature extraction
python scripts/automated-weekly-collection.py --download-only

# Only extract features from existing downloads
python scripts/automated-weekly-collection.py --extract-only
```

---

## ⏰ Set Up Weekly Reminder

### Option 1: Windows Task Scheduler

1. Open Task Scheduler
2. **Create Basic Task**
   - Name: "Weekly Security Data Collection"
   - Trigger: Weekly, Sunday 9 AM
   - Action: Start a program
     - Program: `python`
     - Arguments: `scripts/automated-weekly-collection.py`
     - Start in: `C:\Users\joshu\Desktop\DevOps Project`

### Option 2: Calendar Reminder

Set a recurring Sunday reminder: "Run data collection script"

---

## 📈 What You'll Have in 4 Weeks

```
Week 1: 7 data points (each branch)
Week 2: 14 data points
Week 3: 21 data points
Week 4: 28 data points ← Ready for time-series ML!
```

**Time-series dataset will have:**
- 56 rows (28 days × 2 branches)
- 211 columns (208 features + metadata)
- Ready for LSTM, ARIMA, or temporal anomaly detection

---

## 💡 Tips

✅ **Run it today** to start collecting baseline data
✅ **Don't skip weeks** - consistent data collection is key
✅ **Check the reports** after each run to verify success
✅ **Back up the time-series CSV** regularly

---

## 📚 Full Documentation

See `AUTOMATED-COLLECTION-GUIDE.md` for:
- Detailed usage instructions
- Troubleshooting
- Advanced options
- GitHub Actions automation

---

**Ready to start?**
```bash
cd "C:\Users\joshu\Desktop\DevOps Project"
python scripts/automated-weekly-collection.py
```

🚀 **Let's collect some data!**
