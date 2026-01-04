# Complete DevOps Automation Setup
# Run this script ONCE to set up all automated tasks

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Complete DevOps Automation Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$tasksCreated = 0
$tasksFailed = 0

# ============================================================================
# Task 1: Weekly Data Pipeline (Download + Extract + Validate + Report)
# ============================================================================

Write-Host "[1/3] Setting up Weekly Data Pipeline..." -ForegroundColor Yellow

$taskName1 = "DevOps-Weekly-Pipeline"
$pythonScript1 = "C:\Users\joshu\Desktop\DevOps Project\scripts\full-pipeline-automation.py"

if (Test-Path $pythonScript1) {
    # Remove existing task
    $existing = Get-ScheduledTask -TaskName $taskName1 -ErrorAction SilentlyContinue
    if ($existing) {
        Unregister-ScheduledTask -TaskName $taskName1 -Confirm:$false
    }

    # Create task
    $action1 = New-ScheduledTaskAction -Execute "python.exe" -Argument "`"$pythonScript1`"" -WorkingDirectory "C:\Users\joshu\Desktop\DevOps Project\scripts"
    $trigger1 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 3:30AM
    $settings1 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

    Register-ScheduledTask `
        -TaskName $taskName1 `
        -Action $action1 `
        -Trigger $trigger1 `
        -Settings $settings1 `
        -Description "Weekly data pipeline: download artifacts, extract features, validate, and report" `
        -User $env:USERNAME | Out-Null

    Write-Host "  [OK] Created: $taskName1 (Sundays at 3:30 AM)" -ForegroundColor Green
    $tasksCreated++
} else {
    Write-Host "  [FAIL] Script not found: $pythonScript1" -ForegroundColor Red
    $tasksFailed++
}

# ============================================================================
# Task 2: Daily Workflow Health Monitoring
# ============================================================================

Write-Host "[2/3] Setting up Daily Health Monitoring..." -ForegroundColor Yellow

$taskName2 = "DevOps-Daily-Health-Check"
$pythonScript2 = "C:\Users\joshu\Desktop\DevOps Project\scripts\workflow-health-monitor.py"

if (Test-Path $pythonScript2) {
    # Remove existing task
    $existing = Get-ScheduledTask -TaskName $taskName2 -ErrorAction SilentlyContinue
    if ($existing) {
        Unregister-ScheduledTask -TaskName $taskName2 -Confirm:$false
    }

    # Create task
    $action2 = New-ScheduledTaskAction -Execute "python.exe" -Argument "`"$pythonScript2`"" -WorkingDirectory "C:\Users\joshu\Desktop\DevOps Project\scripts"
    $trigger2 = New-ScheduledTaskTrigger -Daily -At 9:00AM
    $settings2 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

    Register-ScheduledTask `
        -TaskName $taskName2 `
        -Action $action2 `
        -Trigger $trigger2 `
        -Settings $settings2 `
        -Description "Daily workflow health check: monitors for failures, missing runs, and issues" `
        -User $env:USERNAME | Out-Null

    Write-Host "  [OK] Created: $taskName2 (Daily at 9:00 AM)" -ForegroundColor Green
    $tasksCreated++
} else {
    Write-Host "  [FAIL] Script not found: $pythonScript2" -ForegroundColor Red
    $tasksFailed++
}

# ============================================================================
# Task 3: Weekly Scheduled Run Monitoring
# ============================================================================

Write-Host "[3/3] Setting up Weekly Scheduled Run Monitor..." -ForegroundColor Yellow

$taskName3 = "DevOps-Weekly-Scheduler-Check"
$pythonScript3 = "C:\Users\joshu\Desktop\DevOps Project\scripts\monitor_scheduled_workflows.py"

if (Test-Path $pythonScript3) {
    # Remove existing task
    $existing = Get-ScheduledTask -TaskName $taskName3 -ErrorAction SilentlyContinue
    if ($existing) {
        Unregister-ScheduledTask -TaskName $taskName3 -Confirm:$false
    }

    # Create task
    $action3 = New-ScheduledTaskAction -Execute "python.exe" -Argument "`"$pythonScript3`"" -WorkingDirectory "C:\Users\joshu\Desktop\DevOps Project\scripts"
    $trigger3 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 10:00AM
    $settings3 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

    Register-ScheduledTask `
        -TaskName $taskName3 `
        -Action $action3 `
        -Trigger $trigger3 `
        -Settings $settings3 `
        -Description "Weekly check of scheduled workflow activation status" `
        -User $env:USERNAME | Out-Null

    Write-Host "  [OK] Created: $taskName3 (Mondays at 10:00 AM)" -ForegroundColor Green
    $tasksCreated++
} else {
    Write-Host "  [FAIL] Script not found: $pythonScript3" -ForegroundColor Red
    $tasksFailed++
}

# ============================================================================
# Summary
# ============================================================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tasks Created: $tasksCreated" -ForegroundColor Green
Write-Host "Tasks Failed:  $tasksFailed" -ForegroundColor $(if ($tasksFailed -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($tasksCreated -gt 0) {
    Write-Host "Scheduled Tasks:" -ForegroundColor Cyan
    Write-Host "  1. DevOps-Weekly-Pipeline" -ForegroundColor White
    Write-Host "     └─ Sundays at 3:30 AM" -ForegroundColor Gray
    Write-Host "     └─ Full data pipeline (download, extract, validate, report)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. DevOps-Daily-Health-Check" -ForegroundColor White
    Write-Host "     └─ Daily at 9:00 AM" -ForegroundColor Gray
    Write-Host "     └─ Monitors workflow health and failures" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  3. DevOps-Weekly-Scheduler-Check" -ForegroundColor White
    Write-Host "     └─ Mondays at 10:00 AM" -ForegroundColor Gray
    Write-Host "     └─ Verifies scheduled runs are active" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "View all tasks:" -ForegroundColor Yellow
Write-Host "  Get-ScheduledTask | Where-Object {`$_.TaskName -like 'DevOps-*'}" -ForegroundColor White
Write-Host ""
Write-Host "Test a task now:" -ForegroundColor Yellow
Write-Host "  Start-ScheduledTask -TaskName 'DevOps-Weekly-Pipeline'" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
