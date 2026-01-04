# Complete DevOps Automation Guide

> **"Automate all the things!"** - The DevOps Way

---

## 🎯 Overview

This guide covers **complete end-to-end automation** for your DevOps ML Security Research project.

### What's Automated:

| Component | Frequency | What It Does |
|-----------|-----------|--------------|
| **GitHub Workflows** | Daily at 2 AM UTC | Runs security scans automatically |
| **Data Pipeline** | Weekly (Sundays 3:30 AM) | Downloads, extracts, validates, reports |
| **Health Monitoring** | Daily at 9 AM | Checks for workflow failures and issues |
| **Scheduler Check** | Weekly (Mondays 10 AM) | Verifies scheduled runs are active |

---

## 🚀 Quick Setup (5 Minutes)

### One Command to Rule Them All:

```powershell
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"
powershell -ExecutionPolicy Bypass -File setup-complete-automation.ps1
```

**This creates 3 scheduled tasks:**
1. Weekly data pipeline
2. Daily health monitoring
3. Weekly scheduler verification

---

## 📊 Automation Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions (Cloud)                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Security Scanning Workflow                          │   │
│  │  • Runs: Daily at 2:00 AM UTC (automatic)           │   │
│  │  • Produces: SBOM, licenses, Gitleaks, KICS results │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
                      (Artifacts stored)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Windows Scheduled Tasks (Local)                 │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  1. Weekly Data Pipeline (Sundays 3:30 AM)        │     │
│  │     ├─ Download all artifacts                     │     │
│  │     ├─ Extract ML features                        │     │
│  │     ├─ Validate data quality                      │     │
│  │     └─ Generate summary report                    │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  2. Daily Health Check (Daily 9:00 AM)            │     │
│  │     ├─ Check for workflow failures                │     │
│  │     ├─ Verify scheduled runs                      │     │
│  │     ├─ Check artifact uploads                     │     │
│  │     └─ Alert on issues                            │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  3. Weekly Scheduler Check (Mondays 10:00 AM)     │     │
│  │     └─ Verify scheduled runs are active           │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    (Data persisted)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                 Research Data Storage                        │
│  • research-data/time-series/YYYY-MM-DD/                    │
│  • ml-pipeline/output/features_*.csv                        │
│  • scripts/logs/ (monitoring & pipeline logs)               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Detailed Automation Breakdown

### 1. Weekly Data Pipeline

**Script:** `full-pipeline-automation.py`
**Schedule:** Every Sunday at 3:30 AM
**Task Name:** `DevOps-Weekly-Pipeline`

**What it does:**

```
Step 1: Download Artifacts
  └─ Fetches all artifacts from scheduled workflow runs
  └─ Saves to: research-data/time-series/YYYY-MM-DD/

Step 2: Extract ML Features
  └─ Runs feature extraction for main branch
  └─ Runs feature extraction for hardened branch
  └─ Outputs: ml-pipeline/output/features_*.csv

Step 3: Validate Data Quality
  └─ Checks time-series data exists
  └─ Verifies feature files created
  └─ Confirms recent data collection
  └─ Saves: scripts/logs/pipeline/validation_*.json

Step 4: Generate Summary Report
  └─ Creates markdown report with statistics
  └─ Saves: scripts/logs/pipeline/summary_report_*.md
```

**Manual run:**
```bash
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"
python full-pipeline-automation.py
```

---

### 2. Daily Health Monitoring

**Script:** `workflow-health-monitor.py`
**Schedule:** Every day at 9:00 AM
**Task Name:** `DevOps-Daily-Health-Check`

**What it monitors:**

```
✓ Failed Workflows
  └─ Checks last 24 hours for failures
  └─ Severity: HIGH
  └─ Alert: Includes workflow name, branch, URL

✓ Missing Scheduled Runs
  └─ Checks if scheduled runs happened in last 48h
  └─ Severity: MEDIUM
  └─ Alert: Suggests verification action

✓ Artifact Upload Failures
  └─ Checks completed workflows for missing artifacts
  └─ Severity: MEDIUM
  └─ Alert: Lists workflows without artifacts
```

**Health States:**
- 🟢 **HEALTHY**: No issues found
- 🟡 **DEGRADED**: Some issues detected
- 🔴 **CRITICAL**: Major problems found

**Manual run:**
```bash
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"
python workflow-health-monitor.py
```

---

### 3. Weekly Scheduler Verification

**Script:** `monitor_scheduled_workflows.py`
**Schedule:** Every Monday at 10:00 AM
**Task Name:** `DevOps-Weekly-Scheduler-Check`

**What it verifies:**

```
✓ Scheduled runs are active
✓ Runs happening at expected times (2 AM UTC)
✓ No missed runs
✓ Logs status for historical tracking
```

**Manual run:**
```bash
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"
python monitor_scheduled_workflows.py
```

---

## 🔧 Management Commands

### View All DevOps Tasks

```powershell
Get-ScheduledTask | Where-Object {$_.TaskName -like 'DevOps-*'} | Format-Table TaskName, State, @{Name='NextRun';Expression={(Get-ScheduledTaskInfo -TaskName $_.TaskName).NextRunTime}}
```

### Run a Task Immediately

```powershell
# Run weekly pipeline now
Start-ScheduledTask -TaskName 'DevOps-Weekly-Pipeline'

# Run health check now
Start-ScheduledTask -TaskName 'DevOps-Daily-Health-Check'

# Run scheduler check now
Start-ScheduledTask -TaskName 'DevOps-Weekly-Scheduler-Check'
```

### Check Task History

```powershell
Get-ScheduledTask -TaskName 'DevOps-Weekly-Pipeline' | Get-ScheduledTaskInfo
```

### Disable a Task

```powershell
Disable-ScheduledTask -TaskName 'DevOps-Weekly-Pipeline'
```

### Re-enable a Task

```powershell
Enable-ScheduledTask -TaskName 'DevOps-Weekly-Pipeline'
```

### Remove All Automation

```powershell
Get-ScheduledTask | Where-Object {$_.TaskName -like 'DevOps-*'} | Unregister-ScheduledTask -Confirm:$false
```

---

## 📁 Where Things Are Saved

### Logs & Reports

```
scripts/
├── logs/
│   ├── pipeline/
│   │   ├── pipeline_YYYYMMDD_HHMMSS.log
│   │   ├── validation_YYYYMMDD_HHMMSS.json
│   │   └── summary_report_YYYYMMDD_HHMMSS.md
│   ├── monitoring/
│   │   └── health_check_YYYYMMDD_HHMMSS.json
│   └── workflow_monitoring.jsonl
```

### Data Storage

```
research-data/
├── time-series/
│   ├── 2025-12-05/
│   ├── 2025-12-06/
│   └── ...
└── main-branch/
    └── ...

ml-pipeline/output/
├── features_YYYYMMDD_HHMMSS.csv
├── latest_features.csv
└── ...
```

---

## 🎛️ Customization

### Change Schedule Times

Edit the PowerShell setup script or modify tasks directly:

```powershell
# Change weekly pipeline to run Saturdays at midnight
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Saturday -At 12:00AM
Set-ScheduledTask -TaskName 'DevOps-Weekly-Pipeline' -Trigger $trigger
```

### Add Email Notifications

Modify scripts to include email sending:

```python
# Add to workflow-health-monitor.py
def send_email_alert(alert):
    import smtplib
    # Email sending logic here
    pass
```

### Add Slack/Discord Webhooks

```python
# Add to any script
def send_webhook(message):
    import requests
    webhook_url = "YOUR_WEBHOOK_URL"
    requests.post(webhook_url, json={"text": message})
```

---

## 🔍 Monitoring & Debugging

### Check if Tasks Ran Successfully

```powershell
# View recent runs
Get-ScheduledTask -TaskName 'DevOps-Weekly-Pipeline' |
    Get-ScheduledTaskInfo |
    Select-Object LastRunTime, LastTaskResult
```

**LastTaskResult Codes:**
- `0` = Success ✅
- `1` = General error ❌
- `267009` = Currently running ⏳

### View Pipeline Logs

```bash
# Latest pipeline log
ls -lt "C:\Users\joshu\Desktop\DevOps Project\scripts\logs\pipeline\" | head -5

# View specific log
cat "scripts/logs/pipeline/pipeline_YYYYMMDD_HHMMSS.log"
```

### View Health Check Reports

```bash
# Latest health report
ls -lt "C:\Users\joshu\Desktop\DevOps Project\scripts\logs\monitoring\" | head -1

# View as JSON
cat "scripts/logs/monitoring/health_check_YYYYMMDD_HHMMSS.json" | jq .
```

---

## 📈 What's Automated vs Manual

### ✅ Fully Automated

- [x] GitHub workflow runs (daily)
- [x] Artifact downloads (weekly)
- [x] Feature extraction (weekly)
- [x] Data validation (weekly)
- [x] Summary reports (weekly)
- [x] Health monitoring (daily)
- [x] Scheduler verification (weekly)

### 📝 Still Manual (Optional)

- [ ] ML model training (intentionally manual)
- [ ] Attack scenario execution (Week 2 - manual)
- [ ] Data backup to external storage
- [ ] Git commits of research data
- [ ] Thesis writing (definitely manual! 😄)

---

## 🚨 Troubleshooting

### Task Doesn't Run

**Check:**
1. Is task enabled? `Get-ScheduledTask -TaskName 'DevOps-Weekly-Pipeline'`
2. Is network required and available?
3. Is Python in PATH?

**Fix:**
```powershell
# Re-register task
.\setup-complete-automation.ps1
```

### Python Script Fails

**Check logs:**
```bash
# View latest pipeline log
cat scripts/logs/pipeline/pipeline_*.log | tail -50
```

**Common issues:**
- GitHub token expired → Update `.github_token`
- Network timeout → Check internet connection
- ML pipeline path wrong → Verify directory structure

### No Data Downloaded

**Check:**
1. Are workflows producing artifacts?
   ```bash
   python scripts/check_todays_runs.py
   ```
2. Is GitHub token valid?
3. Check download logs

---

## 📊 Success Metrics

After automation is running, you should see:

### Weekly (After Sunday 3:30 AM)
- ✅ New date directories in `research-data/time-series/`
- ✅ New feature CSV files in `ml-pipeline/output/`
- ✅ New pipeline logs and reports
- ✅ Validation JSON showing PASS status

### Daily (After 9:00 AM)
- ✅ Health check report in `logs/monitoring/`
- ✅ Status shows HEALTHY (or alerts if issues)

### Monday (After 10:00 AM)
- ✅ Scheduler status logged
- ✅ Confirmation of scheduled runs active

---

## 🎯 Next Steps

Once automation is running:

1. **Let it run for 2-3 weeks** to collect baseline data
2. **Review weekly reports** to ensure data quality
3. **Monitor health checks** for any issues
4. **After baseline period**, start Week 2 attack scenarios
5. **Train ML models** on collected time-series data

---

## 💡 Pro Tips

- **Check logs weekly** to catch issues early
- **Test tasks manually** after updates
- **Keep GitHub token valid** (regenerate if needed)
- **Monitor disk space** for accumulated data
- **Backup logs** periodically

---

**🎉 Congratulations! Your DevOps pipeline is now fully automated!**

*"The best code is the code that runs itself." - DevOps Proverb*
