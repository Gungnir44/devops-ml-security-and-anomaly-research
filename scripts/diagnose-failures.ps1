# Diagnose why workflows are failing

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

# Check specific failed runs
$failedRuns = @(
    @{Name="Frontend CI/CD"; ID=19948669018},
    @{Name="Python CI/CD"; ID=19948663517},
    @{Name="Backend CI/CD"; ID=19948618930}
)

Write-Host "="*70 -ForegroundColor Cyan
Write-Host "  Workflow Failure Diagnosis" -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

foreach ($runInfo in $failedRuns) {
    Write-Host "$($runInfo.Name) - Failure Analysis:" -ForegroundColor Yellow
    Write-Host ""

    $runUrl = "https://api.github.com/repos/$owner/$repo/actions/runs/$($runInfo.ID)"
    $run = Invoke-RestMethod -Uri $runUrl -Headers $headers

    Write-Host "  Status: $($run.conclusion)" -ForegroundColor Red
    Write-Host "  URL: $($run.html_url)" -ForegroundColor Gray
    Write-Host ""

    # Get jobs
    $jobs = Invoke-RestMethod -Uri $run.jobs_url -Headers $headers

    foreach ($job in $jobs.jobs) {
        if ($job.conclusion -eq "failure") {
            Write-Host "  Failed Job: $($job.name)" -ForegroundColor Red
            Write-Host "  Job URL: $($job.html_url)" -ForegroundColor Gray
            Write-Host ""
            Write-Host "  Failed Steps:" -ForegroundColor Yellow

            foreach ($step in $job.steps) {
                if ($step.conclusion -eq "failure") {
                    Write-Host "    X $($step.name)" -ForegroundColor Red
                }
            }
            Write-Host ""
        }
    }

    Write-Host "-"*70
    Write-Host ""
}

Write-Host "="*70 -ForegroundColor Cyan
Write-Host "To view detailed logs, visit:" -ForegroundColor Yellow
Write-Host "https://github.com/$owner/$repo/actions" -ForegroundColor Cyan
Write-Host ""
