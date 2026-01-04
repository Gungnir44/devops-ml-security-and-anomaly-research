# Automated Research Data Download Setup

## Quick Setup (Requires Administrator)

### Option 1: Run Setup Script as Administrator

1. **Right-click on PowerShell** and select "Run as Administrator"

2. **Navigate to scripts folder:**
   ```powershell
   cd "C:\Users\joshu\Desktop\DevOps Project\scripts"
   ```

3. **Run the setup script:**
   ```powershell
   .\setup-automated-downloads.ps1 -GitHubToken "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"
   ```

4. **When prompted, type `y` to test the download immediately**

---

## Option 2: Manual Task Scheduler Setup (GUI)

If the script doesn't work, you can set it up manually:

### Step 1: Open Task Scheduler
- Press `Win + R`
- Type `taskschd.msc` and press Enter

### Step 2: Create New Task
- Click "Create Task" (not "Create Basic Task")
- **Name:** DevOps-Research-Data-Download
- **Description:** Automatically downloads GitHub workflow artifacts and security scan data
- **Security options:**
  - Check "Run whether user is logged on or not"
  - Check "Run with highest privileges"

### Step 3: Trigger
- Click "Triggers" tab → "New"
- Begin the task: **On a schedule**
- Settings: **Daily**
- Start time: **03:00:00 AM** (3 AM UTC - adjust to your timezone)
- Check "Enabled"

### Step 4: Action
- Click "Actions" tab → "New"
- Action: **Start a program**
- Program/script: `powershell.exe`
- Add arguments:
  ```
  -NoProfile -ExecutionPolicy Bypass -File "C:\Users\joshu\Desktop\DevOps Project\scripts\auto-download-research-data.ps1" -Token "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"
  ```

### Step 5: Conditions
- Click "Conditions" tab
- Uncheck "Start the task only if the computer is on AC power"
- Check "Start the task only if the following network connection is available"

### Step 6: Settings
- Click "Settings" tab
- Check "Allow task to be run on demand"
- Check "Run task as soon as possible after a scheduled start is missed"
- If the task fails, restart every: **10 minutes**
- Stop the task if it runs longer than: **2 hours**

### Step 7: Save and Test
- Click "OK"
- Right-click the task → "Run" to test immediately

---

## What Happens Automatically

Once set up, the task will:

### Daily at 3 AM UTC:
1. Download all workflow run artifacts from GitHub
2. Download all code scanning alerts
3. Save everything to `research-data/`
4. Create a log file in `research-data/download-logs/`

### Logs Location:
`C:\Users\joshu\Desktop\DevOps Project\research-data\download-logs\`

Each run creates a timestamped log file: `log-2025-12-06_03-00-00.txt`

---

## Managing the Task

### View Task Status:
```powershell
Get-ScheduledTask -TaskName "DevOps-Research-Data-Download"
```

### Run Manually Now:
```powershell
Start-ScheduledTask -TaskName "DevOps-Research-Data-Download"
```

### Disable Task:
```powershell
Disable-ScheduledTask -TaskName "DevOps-Research-Data-Download"
```

### Enable Task:
```powershell
Enable-ScheduledTask -TaskName "DevOps-Research-Data-Download"
```

### Remove Task:
```powershell
Unregister-ScheduledTask -TaskName "DevOps-Research-Data-Download" -Confirm:$false
```

### Check Last Run Result:
```powershell
Get-ScheduledTaskInfo -TaskName "DevOps-Research-Data-Download"
```

---

## Timezone Reference

The task runs at **3:00 AM UTC** which is:
- **10:00 PM EST** (previous day)
- **7:00 PM PST** (previous day)
- **11:00 PM EDT** (previous day)
- **8:00 PM PDT** (previous day)

To change the time, edit the trigger in Task Scheduler.

---

## Troubleshooting

### Task doesn't run:
1. Check if computer is on at scheduled time
2. Check network connection is available
3. View logs in `research-data/download-logs/`
4. Check Task Scheduler History tab

### GitHub token expires:
GitHub Personal Access Tokens expire after a set period. If downloads fail:
1. Generate new token at: https://github.com/settings/tokens
2. Update the task action with new token
3. Or run the setup script again with new token

### Permission errors:
- Make sure task is set to "Run with highest privileges"
- Ensure the user account has permissions to the scripts folder

---

## Data Collection Strategy

### Automatic Collection (Scheduled):
- **Daily downloads** capture continuous monitoring data
- **90-day retention** ensures comprehensive dataset
- **Logs preserved** for 30 days

### Your Manual Role:
- **Review logs** periodically to ensure downloads succeed
- **Organize data** when you're ready for analysis
- **Update token** if it expires

The automation handles the repetitive downloading, so you can focus on the research analysis!
