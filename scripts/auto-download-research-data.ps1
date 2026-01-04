param(
    [Parameter(Mandatory=$true)]
    [string]$Token
)

# Auto-download research data script
# Runs both artifact and code scanning downloads automatically

$ErrorActionPreference = "Continue"
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$logFile = "C:\Users\joshu\Desktop\DevOps Project\research-data\download-logs\log-$timestamp.txt"

# Create log directory if it doesn't exist
$logDir = "C:\Users\joshu\Desktop\DevOps Project\research-data\download-logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

function Write-Log {
    param([string]$Message)
    $logMessage = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Message"
    Write-Host $logMessage
    Add-Content -Path $logFile -Value $logMessage
}

Write-Log "=========================================="
Write-Log "Starting automated research data download"
Write-Log "=========================================="

# Download workflow artifacts
Write-Log "Step 1: Downloading workflow artifacts..."
try {
    & "C:\Users\joshu\Desktop\DevOps Project\scripts\download-artifacts.ps1" -Token $Token
    Write-Log "✓ Artifacts download completed"
} catch {
    Write-Log "✗ Artifacts download failed: $_"
}

Write-Log ""

# Download code scanning results
Write-Log "Step 2: Downloading code scanning alerts..."
try {
    & "C:\Users\joshu\Desktop\DevOps Project\scripts\download-code-scanning.ps1" -Token $Token
    Write-Log "✓ Code scanning download completed"
} catch {
    Write-Log "✗ Code scanning download failed: $_"
}

Write-Log ""
Write-Log "=========================================="
Write-Log "Automated download completed"
Write-Log "=========================================="
Write-Log "Data saved to: C:\Users\joshu\Desktop\DevOps Project\research-data\"
Write-Log "Log file: $logFile"

# Clean up old logs (keep last 30 days)
Write-Log ""
Write-Log "Cleaning up old log files (keeping last 30 days)..."
$oldLogs = Get-ChildItem -Path $logDir -Filter "log-*.txt" |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) }
foreach ($log in $oldLogs) {
    Remove-Item $log.FullName -Force
    Write-Log "Deleted old log: $($log.Name)"
}

Write-Log "Done!"
