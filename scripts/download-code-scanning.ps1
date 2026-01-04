# Download GitHub Code Scanning results (SARIF)
# This downloads all security findings from the Security tab

param(
    [string]$Token = "",
    [string]$Owner = "Gungnir44",
    [string]$Repo = "devops-ml-security-and-anomaly-research"
)

if ($Token -eq "") {
    Write-Host "ERROR: GitHub token required" -ForegroundColor Red
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\download-code-scanning.ps1 -Token YOUR_GITHUB_TOKEN" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To create a token:" -ForegroundColor Cyan
    Write-Host "  1. Go to: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "  2. Click 'Generate new token (classic)'" -ForegroundColor White
    Write-Host "  3. Select scope: 'security_events' (read access)" -ForegroundColor White
    Write-Host "  4. Generate and copy the token" -ForegroundColor White
    Write-Host ""
    exit 1
}

$outputDir = "C:\Users\joshu\Desktop\DevOps Project\research-data\baseline-week-1\code-scanning-alerts"
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

$headers = @{
    Authorization = "Bearer $Token"
    Accept = "application/vnd.github+json"
}

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "  GitHub Code Scanning Results Downloader" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

# Get code scanning alerts
Write-Host "Fetching code scanning alerts..." -ForegroundColor Yellow
$alertsUrl = "https://api.github.com/repos/$Owner/$Repo/code-scanning/alerts?per_page=100&state=open"

try {
    $alerts = Invoke-RestMethod -Uri $alertsUrl -Headers $headers
    Write-Host "Found $($alerts.Count) open alerts" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Failed to fetch alerts" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# Save all alerts as JSON
$allAlertsFile = Join-Path $outputDir "all-alerts.json"
$alerts | ConvertTo-Json -Depth 10 | Set-Content $allAlertsFile
Write-Host "Saved all alerts to: $allAlertsFile" -ForegroundColor Green
Write-Host ""

# Categorize by tool
$byTool = $alerts | Group-Object -Property { $_.tool.name }

Write-Host "Alerts by Tool:" -ForegroundColor Cyan
foreach ($group in $byTool) {
    $toolName = $group.Name
    $count = $group.Count
    Write-Host "  ${toolName}: $count alerts" -ForegroundColor White

    # Save tool-specific file
    $toolFile = Join-Path $outputDir "$toolName-alerts.json"
    $group.Group | ConvertTo-Json -Depth 10 | Set-Content $toolFile
}

Write-Host ""

# Categorize by severity
$bySeverity = $alerts | Group-Object -Property { $_.rule.security_severity_level }

Write-Host "Alerts by Severity:" -ForegroundColor Cyan
foreach ($group in $bySeverity) {
    $severity = if ($group.Name) { $group.Name } else { "undefined" }
    $count = $group.Count
    Write-Host "  ${severity}: $count alerts" -ForegroundColor White
}

Write-Host ""

# Get SARIF uploads (analyses)
Write-Host "Fetching SARIF analyses..." -ForegroundColor Yellow
$analysesUrl = "https://api.github.com/repos/$Owner/$Repo/code-scanning/analyses?per_page=50"

try {
    $analyses = Invoke-RestMethod -Uri $analysesUrl -Headers $headers
    Write-Host "Found $($analyses.Count) SARIF uploads" -ForegroundColor Green
}
catch {
    Write-Host "WARNING: Failed to fetch analyses" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Yellow
    $analyses = @()
}

if ($analyses.Count -gt 0) {
    # Save analyses list
    $analysesFile = Join-Path $outputDir "sarif-analyses.json"
    $analyses | ConvertTo-Json -Depth 10 | Set-Content $analysesFile

    Write-Host ""
    Write-Host "Recent SARIF Uploads:" -ForegroundColor Cyan
    foreach ($analysis in $analyses | Select-Object -First 10) {
        Write-Host "  Tool: $($analysis.tool.name)" -ForegroundColor White
        Write-Host "  Date: $($analysis.created_at)" -ForegroundColor Gray
        Write-Host "  Results: $($analysis.results_count) findings" -ForegroundColor Gray
        Write-Host "  ID: $($analysis.id)" -ForegroundColor Gray
        Write-Host ""
    }
}

# Create summary report
$summaryFile = Join-Path $outputDir "SUMMARY.md"
$summary = @"
# Code Scanning Results Summary

**Downloaded:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Repository:** $Owner/$Repo

## Overview

- **Total Alerts:** $($alerts.Count)
- **SARIF Analyses:** $($analyses.Count)

## Alerts by Tool

"@

foreach ($group in $byTool) {
    $summary += "- **$($group.Name):** $($group.Count) alerts`n"
}

$summary += "`n## Alerts by Severity`n`n"

foreach ($group in $bySeverity) {
    $severity = if ($group.Name) { $group.Name } else { "undefined" }
    $summary += "- **${severity}:** $($group.Count) alerts`n"
}

$summary += @"

## Files

- ``all-alerts.json`` - All open alerts
- ``*-alerts.json`` - Alerts grouped by tool
- ``sarif-analyses.json`` - SARIF upload history

## Next Steps

1. Review alerts in ``all-alerts.json``
2. Analyze tool-specific results
3. Map findings to ML features
4. Compare with artifact scan results

## API Access

To fetch detailed SARIF for a specific analysis:
``````
GET /repos/$Owner/$Repo/code-scanning/analyses/{analysis_id}
``````

---

**Note:** This data represents the current state of security alerts.
For historical data, download SARIF artifacts from workflow runs.
"@

Set-Content -Path $summaryFile -Value $summary

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "  Download Complete!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""
Write-Host "Results saved to: $outputDir" -ForegroundColor Yellow
Write-Host "Summary: $summaryFile" -ForegroundColor Yellow
Write-Host ""
Write-Host "Open Security tab: https://github.com/$Owner/$Repo/security/code-scanning" -ForegroundColor Cyan
