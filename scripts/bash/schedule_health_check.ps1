# Schedule Health Check - Windows Task Scheduler Setup
# Author: Joshua
# Description: Sets up automated health monitoring with Windows Task Scheduler

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("5min", "15min", "hourly", "daily")]
    [string]$Frequency = "15min"
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Health Check Scheduler Setup - Windows" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Get script paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$PythonScript = Join-Path $ProjectRoot "scripts\python\system_health_checker_v2.py"
$ConfigFile = Join-Path $ProjectRoot "scripts\python\config.json"
$LogDir = Join-Path $ProjectRoot "logs"

# Check if Python script exists
if (-not (Test-Path $PythonScript)) {
    Write-Host "[ERROR] Health checker script not found at: $PythonScript" -ForegroundColor Red
    exit 1
}

# Create logs directory
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
    Write-Host "[OK] Created logs directory: $LogDir" -ForegroundColor Green
}

# Create wrapper batch script for Task Scheduler
$WrapperScript = Join-Path $ScriptDir "run_health_check.bat"
$WrapperContent = @"
@echo off
REM Auto-generated wrapper script for Windows Task Scheduler

cd /d "$ProjectRoot"

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Run the health checker
python "$PythonScript" --config "$ConfigFile"

REM Exit with the same code
exit /b %ERRORLEVEL%
"@

Set-Content -Path $WrapperScript -Value $WrapperContent
Write-Host "[OK] Created wrapper script: $WrapperScript" -ForegroundColor Green
Write-Host ""

# Set task parameters based on frequency
$TaskName = "DevOps-HealthCheck"
$Description = "Automated system health monitoring"

switch ($Frequency) {
    "5min" {
        $TriggerParams = @{
            Once = $true
            At = (Get-Date)
            RepetitionInterval = (New-TimeSpan -Minutes 5)
            RepetitionDuration = ([TimeSpan]::MaxValue)
        }
        $FreqDescription = "every 5 minutes"
    }
    "15min" {
        $TriggerParams = @{
            Once = $true
            At = (Get-Date)
            RepetitionInterval = (New-TimeSpan -Minutes 15)
            RepetitionDuration = ([TimeSpan]::MaxValue)
        }
        $FreqDescription = "every 15 minutes"
    }
    "hourly" {
        $TriggerParams = @{
            Once = $true
            At = (Get-Date)
            RepetitionInterval = (New-TimeSpan -Hours 1)
            RepetitionDuration = ([TimeSpan]::MaxValue)
        }
        $FreqDescription = "every hour"
    }
    "daily" {
        $TriggerParams = @{
            Daily = $true
            At = "6:00AM"
        }
        $FreqDescription = "daily at 6:00 AM"
    }
}

Write-Host "Task Configuration:" -ForegroundColor Yellow
Write-Host "  Name: $TaskName"
Write-Host "  Frequency: $FreqDescription"
Write-Host "  Script: $WrapperScript"
Write-Host "  Logs: $LogDir\health_check.log"
Write-Host ""

# Ask for confirmation
$confirmation = Read-Host "Create this scheduled task? (Y/N)"
if ($confirmation -ne 'Y' -and $confirmation -ne 'y') {
    Write-Host "Task creation cancelled." -ForegroundColor Yellow
    exit 0
}

try {
    # Remove existing task if it exists
    $existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "[INFO] Removing existing task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }

    # Create the trigger
    $Trigger = New-ScheduledTaskTrigger @TriggerParams

    # Create the action
    $LogFile = Join-Path $LogDir "health_check.log"
    $Action = New-ScheduledTaskAction `
        -Execute "cmd.exe" `
        -Argument "/c `"$WrapperScript`" >> `"$LogFile`" 2>&1"

    # Set task settings
    $Settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RunOnlyIfNetworkAvailable:$false `
        -MultipleInstances IgnoreNew

    # Register the task
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Description $Description `
        -Trigger $Trigger `
        -Action $Action `
        -Settings $Settings `
        -RunLevel Limited `
        -Force | Out-Null

    Write-Host ""
    Write-Host "[SUCCESS] Scheduled task created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  Task Name: $TaskName"
    Write-Host "  Frequency: $FreqDescription"
    Write-Host "  Status: $(( Get-ScheduledTask -TaskName $TaskName).State)"
    Write-Host ""
    Write-Host "Management Commands:" -ForegroundColor Yellow
    Write-Host "  View task:   Get-ScheduledTask -TaskName '$TaskName'"
    Write-Host "  Run now:     Start-ScheduledTask -TaskName '$TaskName'"
    Write-Host "  Disable:     Disable-ScheduledTask -TaskName '$TaskName'"
    Write-Host "  Enable:      Enable-ScheduledTask -TaskName '$TaskName'"
    Write-Host "  Remove:      Unregister-ScheduledTask -TaskName '$TaskName'"
    Write-Host ""
    Write-Host "  View logs:   Get-Content '$LogFile' -Tail 50"
    Write-Host "  Live logs:   Get-Content '$LogFile' -Wait"
    Write-Host ""

    # Ask to run now
    $runNow = Read-Host "Would you like to run the task now to test it? (Y/N)"
    if ($runNow -eq 'Y' -or $runNow -eq 'y') {
        Write-Host "[INFO] Running task now..." -ForegroundColor Yellow
        Start-ScheduledTask -TaskName $TaskName
        Start-Sleep -Seconds 3
        Write-Host ""
        Write-Host "Recent log output:" -ForegroundColor Cyan
        if (Test-Path $LogFile) {
            Get-Content $LogFile -Tail 20
        }
    }

} catch {
    Write-Host ""
    Write-Host "[ERROR] Failed to create scheduled task: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "You may need to run this script as Administrator." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
