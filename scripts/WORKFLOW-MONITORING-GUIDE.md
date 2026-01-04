# Workflow Monitoring Guide

## 📊 **Daily Monitoring Script**

**Purpose:** Monitor scheduled GitHub Actions workflows to verify they're running automatically at 2 AM UTC.

---

## 🚀 **Usage**

### **Daily Check (Recommended):**
```bash
cd "C:\Users\joshu\Desktop\DevOps Project"
python scripts/monitor_scheduled_workflows.py
```

**Run this every day** to track when scheduled workflows activate!

---

## 📋 **What the Script Shows**

### **1. Run Summary**
- Total workflow runs in last 30 executions
- **Scheduled runs** (schedule event) - what we're looking for!
- Push-triggered runs (from git push)
- Manual runs (workflow_dispatch)

### **2. Scheduled Run Status**
- **[OK] ACTIVE** - Scheduled runs are working! ✅
- **[!] NOT YET ACTIVE** - Still waiting for activation ⏳

### **3. Latest Run Details**
- Time of last run
- What triggered it (push, schedule, or manual)
- Status and conclusion
- Direct link to workflow run

### **4. Next Expected Run**
- When the next 2 AM UTC run should occur
- Hours until next scheduled run
- Whether it's expected to run automatically

### **5. 7-Day Activity**
- Daily breakdown of all runs
- Shows which days had scheduled runs
- Tracks manual triggers

---

## 🎯 **Current Status (as of Dec 9, 2025)**

```
STATUS: Scheduled workflows NOT YET ACTIVATED
  - Repository age: 5 days
  - Total runs: 9 (all push-triggered)
  - Scheduled runs: 0
  - Next expected: Dec 10 at 02:00 UTC (21.6 hours from now)

ACTION NEEDED: Manual trigger OR wait 2-5 more days
```

---

## ✅ **How to Manually Trigger (Activates Scheduler)**

### **Option 1: GitHub UI (Easiest)**

1. Go to: https://github.com/Gungnir44/devops-ml-security-and-anomaly-research
2. Click **"Actions"** tab
3. Click **"Security Scanning"** workflow (left sidebar)
4. Click **"Run workflow"** button (right side, blue)
5. Select branch: **main**
6. Click **"Run workflow"**

**Result:** Scheduled runs should start within 24-48 hours

### **Option 2: GitHub CLI (Advanced)**
```bash
gh workflow run security-scanning.yml --ref main
```

---

## 📅 **Expected Timeline**

### **If Manual Trigger Today (Dec 9):**
```
Dec 9:  Manual run executes
Dec 10: First automatic 2 AM UTC run ✅
Dec 11: Second automatic run (confirms it's working)
...
Daily:  Runs at 2 AM UTC every day
```

### **If Wait for Natural Activation:**
```
Dec 11-14: Scheduled runs may start automatically
           (typically 7-10 days after repo creation)
After:     Daily runs at 2 AM UTC
```

---

## 🔍 **How to Tell When It's Working**

When you run the monitoring script and see:

```
[OK] SCHEDULED RUNS: ACTIVE
  Total scheduled runs: 1
  Last 24 hours: 1

Recent scheduled runs:
  [OK] 2025-12-10 02:00 UTC | completed  | success
```

**That means it's working!** ✅

---

## 📊 **Monitoring Log**

The script automatically logs status to:
```
scripts/logs/workflow_monitoring.jsonl
```

Each line is a JSON entry with:
- Timestamp
- Scheduled runs count
- Total runs
- Status (active/inactive)

**Use this to track progress over time!**

---

## 💡 **Tips**

1. **Run daily** - Check every morning to see if activation happened
2. **After manual trigger** - Check 24-48 hours later
3. **Weekend check** - Verify runs happened on Saturday/Sunday at 2 AM UTC
4. **Log history** - Review `workflow_monitoring.jsonl` to see trends

---

## 🎯 **What Success Looks Like**

### **Week 1 (Baseline - Current Week):**
```bash
# December 10 morning check:
python scripts/monitor_scheduled_workflows.py

Expected output:
  [OK] SCHEDULED RUNS: ACTIVE
  Total scheduled runs: 1
  Last 24 hours: 1
```

### **Week 2+ (Attack Execution):**
```bash
# Daily check shows:
  Scheduled runs (schedule): 7-14  (one per day)
  Push-triggered runs: 8-15        (from attack executions)

Activity shows:
  2025-12-16: 2 runs (scheduled:1, push:1, manual:0) [OK] scheduled
  2025-12-17: 2 runs (scheduled:1, push:1, manual:0) [OK] scheduled
  ...
```

---

## 🚨 **Troubleshooting**

### **Problem: Still no scheduled runs after 2 weeks**

**Solution:**
1. Check workflow file syntax: `.github/workflows/security-scanning.yml`
2. Verify schedule line: `- cron: '0 2 * * *'`
3. Check repository is not archived
4. Verify GitHub Actions are enabled in repo settings
5. Try manual trigger again

### **Problem: Scheduled runs started but then stopped**

**Solution:**
1. Check if repository was inactive (60+ days)
2. GitHub disables scheduled workflows for inactive repos
3. Manual trigger or push to re-activate

---

## 📞 **Quick Commands**

```bash
# Daily status check
python scripts/monitor_scheduled_workflows.py

# View monitoring log
cat scripts/logs/workflow_monitoring.jsonl

# Count scheduled runs in log
grep '"status": "active"' scripts/logs/workflow_monitoring.jsonl | wc -l

# Last 5 entries in log
tail -5 scripts/logs/workflow_monitoring.jsonl | jq .
```

---

## ✅ **Checklist for Week 1 (Dec 9-15)**

- [ ] Dec 9: Run monitoring script (baseline)
- [ ] Dec 9: Manually trigger workflow (if desired)
- [ ] Dec 10: Run monitoring script (check for first scheduled run)
- [ ] Dec 11: Run monitoring script (confirm it's working)
- [ ] Dec 12-15: Daily checks to verify consistency

---

## 🎉 **Once Activated:**

When scheduled runs are active, you'll have:

✅ **Automatic data collection** - Runs at 2 AM UTC daily
✅ **28 normal samples** - 14 days × 2 branches = 28 samples
✅ **Baseline established** - Week 1 normal behavior captured
✅ **Ready for Week 2** - Start attack scenarios Dec 16

---

**Run the monitoring script daily and watch for activation!**

**Expected activation: Dec 10-14 (within 1-5 days)**

**Command:**
```bash
python scripts/monitor_scheduled_workflows.py
```

Good luck! 🚀
