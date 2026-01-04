# Setup script for automated research data downloads
# Run this once to create the scheduled task

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubToken
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Setting up automated research data downloads" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Task details
$taskName = "DevOps-Research-Data-Download"
$scriptPath = "C:\Users\joshu\Desktop\DevOps Project\scripts\auto-download-research-data.ps1"
$taskDescription = "Automatically downloads GitHub workflow artifacts and security scan data for DevOps ML research"

# Schedule: Daily at 3 AM UTC (allows 2 AM workflows to complete)
$triggerTime = "03:00"

Write-Host "Task Configuration:" -ForegroundColor Yellow
Write-Host "  Name: $taskName"
Write-Host "  Schedule: Daily at $triggerTime UTC"
Write-Host "  Script: $scriptPath"
Write-Host ""

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Warning: Task already exists. Removing old task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create the scheduled task action
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`" -Token `"$GitHubToken`""

# Create the trigger (daily at 3 AM)
$trigger = New-ScheduledTaskTrigger -Daily -At $triggerTime

# Create task settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2)

# Create the principal
$principal = New-ScheduledTaskPrincipal `
    -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType S4U `
    -RunLevel Highest

# Register the scheduled task
Write-Host "Creating scheduled task..." -ForegroundColor Cyan

try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Description $taskDescription | Out-Null

    Write-Host ""
    Write-Host "SUCCESS: Scheduled task created!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  - Runs daily at $triggerTime UTC"
    Write-Host "  - Downloads workflow artifacts from GitHub"
    Write-Host "  - Downloads code scanning alerts"
    Write-Host "  - Saves data to: research-data/"
    Write-Host "  - Logs saved to: research-data/download-logs/"
    Write-Host ""
    Write-Host "Manage this task:" -ForegroundColor Yellow
    Write-Host "  - View in Task Scheduler Library: $taskName"
    Write-Host "  - Run now: Get-ScheduledTask '$taskName' | Start-ScheduledTask"
    Write-Host "  - Disable: Disable-ScheduledTask '$taskName'"
    Write-Host "  - Remove: Unregister-ScheduledTask '$taskName' -Confirm" -NoNewline
    Write-Host ":" -NoNewline
    Write-Host "`$false"
    Write-Host ""

    # Ask if user wants to run it now
    $runNow = Read-Host "Would you like to run the task now to test it? (y/n)"
    if ($runNow -eq 'y' -or $runNow -eq 'Y') {
        Write-Host ""
        Write-Host "Running download task..." -ForegroundColor Cyan
        Start-ScheduledTask -TaskName $taskName
        Write-Host "SUCCESS: Task started! Check research-data/download-logs/ for progress" -ForegroundColor Green
    }

}
catch {
    Write-Host ""
    Write-Host "ERROR: Failed to create scheduled task" -ForegroundColor Red
    Write-Host "Details: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "You may need to run this script as Administrator" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
