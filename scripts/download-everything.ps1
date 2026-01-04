# Download Everything - All artifacts and code scanning results
# This is the master script that runs all download steps

param(
    [Parameter(Mandatory=$true)]
    [string]$Token
)

$scriptDir = $PSScriptRoot

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "  DevOps Research Data - Complete Download" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

# Step 1: Download artifacts from workflow runs
Write-Host "[1/3] Downloading workflow artifacts..." -ForegroundColor Yellow
Write-Host ""

$artifactScript = Join-Path $scriptDir "download-artifacts.ps1"
if (Test-Path $artifactScript) {
    & $artifactScript -Token $Token
} else {
    Write-Host "ERROR: download-artifacts.ps1 not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press Enter to continue to code scanning download..." -ForegroundColor Cyan
Read-Host

# Step 2: Download code scanning results
Write-Host ""
Write-Host "[2/3] Downloading code scanning results..." -ForegroundColor Yellow
Write-Host ""

$scanningScript = Join-Path $scriptDir "download-code-scanning.ps1"
if (Test-Path $scanningScript) {
    & $scanningScript -Token $Token
} else {
    Write-Host "ERROR: download-code-scanning.ps1 not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press Enter to continue to extraction..." -ForegroundColor Cyan
Read-Host

# Step 3: Extract all downloaded artifacts
Write-Host ""
Write-Host "[3/3] Extracting all downloaded artifacts..." -ForegroundColor Yellow
Write-Host ""

$extractScript = Join-Path $scriptDir "extract-app-artifacts.ps1"
if (Test-Path $extractScript) {
    & $extractScript
} else {
    Write-Host "ERROR: extract-app-artifacts.ps1 not found" -ForegroundColor Red
}

# Final summary
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "  All Downloads Complete!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

# Count files
$week1Dir = "C:\Users\joshu\Desktop\DevOps Project\research-data\baseline-week-1"
$totalFiles = (Get-ChildItem -Path $week1Dir -Recurse -File).Count

Write-Host "Total files in baseline-week-1: $totalFiles" -ForegroundColor Yellow
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Review: research-data\baseline-week-1\COMPLETE-DATA-SUMMARY.md" -ForegroundColor White
Write-Host "2. Check: research-data\baseline-week-1\EXTRACTION-REPORT.txt" -ForegroundColor White
Write-Host "3. View code scanning: research-data\baseline-week-1\code-scanning-alerts\SUMMARY.md" -ForegroundColor White
Write-Host "4. Begin analysis with Python/Excel" -ForegroundColor White
Write-Host ""

# Open folder
Write-Host "Opening research data folder..." -ForegroundColor Green
Invoke-Item $week1Dir
