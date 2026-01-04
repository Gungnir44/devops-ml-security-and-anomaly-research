# Automated Weekly Download Setup Guide

## Quick Setup (5 minutes)

### Option 1: Automatic Setup (Recommended)

**Run this ONCE to set up automatic weekly downloads:**

```powershell
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"
powershell -ExecutionPolicy Bypass -File setup-weekly-download-task.ps1
```

**What this does:**
- Creates a Windows scheduled task
- Runs every **Sunday at 3:00 AM**
- Downloads all artifacts from scheduled workflow runs
- Saves to `research-data/time-series/`

---

### Option 2: Manual Run (When Needed)

**Run this whenever you want to download latest artifacts:**

```batch
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"
auto-download-weekly.bat
```

Or:

```bash
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"
python download_scheduled_artifacts.py
```

---

## Verify Scheduled Task

After setup, verify it's scheduled:

```powershell
Get-ScheduledTask -TaskName "DevOps-Weekly-Artifact-Download"
```

You should see:
```
TaskName                      State
--------                      -----
DevOps-Weekly-Artifact-Download  Ready
```

---

## Test It Now

To test the download immediately:

```powershell
Start-ScheduledTask -TaskName "DevOps-Weekly-Artifact-Download"
```

Or just run the batch file directly:

```batch
.\auto-download-weekly.bat
```

---

## What Gets Downloaded

The script downloads artifacts from:
- **Workflow:** Security Scanning (scheduled runs)
- **Frequency:** Daily at 2 AM UTC
- **Artifacts:** SBOM, licenses, Gitleaks, KICS results
- **Location:** `research-data/time-series/YYYY-MM-DD/main/`

---

## Schedule Details

| Setting | Value |
|---------|-------|
| Task Name | DevOps-Weekly-Artifact-Download |
| Frequency | Weekly (every Sunday) |
| Time | 3:00 AM |
| Script | `auto-download-weekly.bat` |
| Network | Required (will wait if offline) |
| Battery | Runs even on battery |

---

## View Task in Windows

1. Press `Win + R`
2. Type: `taskschd.msc`
3. Press Enter
4. Navigate to: **Task Scheduler Library**
5. Find: **DevOps-Weekly-Artifact-Download**

---

## Remove Scheduled Task

If you want to remove the automatic task:

```powershell
Unregister-ScheduledTask -TaskName "DevOps-Weekly-Artifact-Download" -Confirm:$false
```

---

## Current Status

As of setup:
- ✅ Scheduled workflows run automatically (daily at 2 AM UTC)
- ✅ 7 days of data already downloaded (Dec 5-11)
- ✅ Download script ready to use
- ⏰ Scheduled task: Run setup script to enable

---

## Troubleshooting

### Task doesn't run?

Check task history:
```powershell
Get-ScheduledTask -TaskName "DevOps-Weekly-Artifact-Download" | Get-ScheduledTaskInfo
```

### Script fails?

Run manually to see errors:
```batch
.\auto-download-weekly.bat
```

### Python not found?

Ensure Python is in PATH or edit the batch file to use full Python path:
```batch
"C:\Python314\python.exe" download_scheduled_artifacts.py
```

---

## Next Steps

After setting up automatic downloads:

1. ✅ **Set it and forget it** - Downloads happen automatically
2. 📊 **Check data weekly** - Review `research-data/time-series/`
3. 🔬 **Extract features** - Run ML feature extraction on collected data
4. 📈 **Build dataset** - Accumulate 2-3 weeks of baseline data
5. 🎯 **Start Week 2** - Execute attack scenarios after baseline

---

**Ready to set up? Run the PowerShell setup script above!**
