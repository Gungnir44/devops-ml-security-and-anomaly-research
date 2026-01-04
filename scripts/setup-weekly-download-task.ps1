# Setup Weekly Automated Download Task
# Run this script ONCE to set up automatic weekly downloads

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting Up Weekly Artifact Download Task" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Task configuration
$taskName = "DevOps-Weekly-Artifact-Download"
$scriptPath = "C:\Users\joshu\Desktop\DevOps Project\scripts\auto-download-weekly.bat"
$pythonScript = "C:\Users\joshu\Desktop\DevOps Project\scripts\download_scheduled_artifacts.py"

# Check if scripts exist
if (-not (Test-Path $scriptPath)) {
    Write-Host "[ERROR] Batch script not found: $scriptPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $pythonScript)) {
    Write-Host "[ERROR] Python script not found: $pythonScript" -ForegroundColor Red
    exit 1
}

# Remove existing task if it exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "[*] Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create task action
$action = New-ScheduledTaskAction -Execute $scriptPath

# Create task trigger - Every Sunday at 3 AM
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 3:00AM

# Create task settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

# Register the task
Write-Host "[*] Creating scheduled task..." -ForegroundColor Yellow
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Automatically download artifacts from scheduled DevOps workflows every Sunday at 3 AM" `
    -User $env:USERNAME

Write-Host ""
Write-Host "[SUCCESS] Scheduled task created!" -ForegroundColor Green
Write-Host ""
Write-Host "Task Details:" -ForegroundColor Cyan
Write-Host "  Name:     $taskName" -ForegroundColor White
Write-Host "  Schedule: Every Sunday at 3:00 AM" -ForegroundColor White
Write-Host "  Script:   $scriptPath" -ForegroundColor White
Write-Host ""
Write-Host "To test it now, run:" -ForegroundColor Yellow
Write-Host "  Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
Write-Host ""
Write-Host "To view task:" -ForegroundColor Yellow
Write-Host "  Get-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
Write-Host ""
Write-Host "To remove task:" -ForegroundColor Yellow
Write-Host "  Unregister-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
