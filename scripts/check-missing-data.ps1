# Check what data is missing and identify failed workflows

param(
    [Parameter(Mandatory=$true)]
    [string]$Token
)

$headers = @{
    Authorization = "Bearer $Token"
    Accept = "application/vnd.github+json"
}

$owner = "Gungnir44"
$repo = "devops-ml-security-and-anomaly-research"

Write-Host "="*70 -ForegroundColor Cyan
Write-Host "  Missing Data Analysis" -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

# Get recent workflow runs
$runsUrl = "https://api.github.com/repos/$owner/$repo/actions/runs?per_page=20"
$runs = Invoke-RestMethod -Uri $runsUrl -Headers $headers

Write-Host "Recent Workflow Runs:" -ForegroundColor Yellow
Write-Host ""

$failedRuns = @()
$successRuns = @()

foreach ($run in $runs.workflow_runs) {
    $status = if ($run.conclusion -eq "success") { "SUCCESS" } else { "FAILED" }
    $color = if ($run.conclusion -eq "success") { "Green" } else { "Red" }

    Write-Host "[$status] " -NoNewline -ForegroundColor $color
    Write-Host "$($run.name)" -NoNewline -ForegroundColor White
    Write-Host " (Run #$($run.run_number))" -ForegroundColor Gray
    Write-Host "  Created: $($run.created_at)" -ForegroundColor Gray
    Write-Host "  Run ID: $($run.id)" -ForegroundColor Gray

    # Get artifacts count
    $artifactsUrl = "https://api.github.com/repos/$owner/$repo/actions/runs/$($run.id)/artifacts"
    try {
        $artifacts = Invoke-RestMethod -Uri $artifactsUrl -Headers $headers
        Write-Host "  Artifacts: $($artifacts.artifacts.Count)" -ForegroundColor $(if ($artifacts.artifacts.Count -gt 0) { "Green" } else { "Yellow" })

        if ($artifacts.artifacts.Count -gt 0) {
            foreach ($artifact in $artifacts.artifacts) {
                Write-Host "    - $($artifact.name)" -ForegroundColor Gray
            }
        }
    }
    catch {
        Write-Host "  Artifacts: Error fetching" -ForegroundColor Red
    }

    Write-Host ""

    if ($run.conclusion -ne "success") {
        $failedRuns += $run
    } else {
        $successRuns += $run
    }
}

Write-Host "="*70 -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Yellow
Write-Host "  Total runs: $($runs.workflow_runs.Count)" -ForegroundColor White
Write-Host "  Successful: $($successRuns.Count)" -ForegroundColor Green
Write-Host "  Failed: $($failedRuns.Count)" -ForegroundColor Red
Write-Host ""

# Identify what's expected vs what we have
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "Expected Artifacts for Complete Dataset:" -ForegroundColor Yellow
Write-Host ""

$expected = @{
    "Backend CI/CD" = @("test-coverage-backend", "security-scan-results", "container-scan-results", "sarif-results")
    "Python CI/CD" = @("test-coverage-python", "security-scan-results", "container-scan-results", "sarif-results")
    "Frontend CI/CD" = @("test-coverage-frontend", "security-scan-results", "container-scan-results", "sarif-results")
}

foreach ($workflow in $expected.Keys) {
    Write-Host "$workflow should have:" -ForegroundColor Cyan
    foreach ($artifact in $expected[$workflow]) {
        Write-Host "  - $artifact" -ForegroundColor White
    }
    Write-Host ""
}

Write-Host "="*70 -ForegroundColor Cyan
Write-Host "Recommendation:" -ForegroundColor Yellow
Write-Host ""
Write-Host "To get to 100% data completeness:" -ForegroundColor White
Write-Host "1. Fix failed workflows" -ForegroundColor White
Write-Host "2. Re-run the pipelines" -ForegroundColor White
Write-Host "3. Download new artifacts" -ForegroundColor White
Write-Host ""
