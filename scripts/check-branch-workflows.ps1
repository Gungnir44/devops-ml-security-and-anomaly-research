param([Parameter(Mandatory=$true)][string]$Token)

$headers = @{
    Authorization = "Bearer $Token"
    Accept = "application/vnd.github+json"
}

$runs = Invoke-RestMethod -Uri "https://api.github.com/repos/Gungnir44/devops-ml-security-and-anomaly-research/actions/runs?per_page=30" -Headers $headers

Write-Host "`n=== MAIN BRANCH WORKFLOWS ===" -ForegroundColor Cyan
$mainRuns = $runs.workflow_runs | Where-Object { $_.head_branch -eq 'main' } | Select-Object -First 5
foreach($run in $mainRuns) {
    $color = switch($run.conclusion) {
        'success' { 'Green' }
        'failure' { 'Red' }
        default { if($run.status -eq 'in_progress') { 'Yellow' } else { 'Gray' } }
    }
    Write-Host "`n[$($run.status.ToUpper())] $($run.name)" -ForegroundColor $color
    Write-Host "  Conclusion: $($run.conclusion)" -ForegroundColor Gray
    Write-Host "  Created: $($run.created_at)" -ForegroundColor Gray
}

Write-Host "`n=== HARDENED BRANCH WORKFLOWS ===" -ForegroundColor Cyan
$hardenedRuns = $runs.workflow_runs | Where-Object { $_.head_branch -eq 'hardened' } | Select-Object -First 5
if ($hardenedRuns.Count -eq 0) {
    Write-Host "`nNo workflows found yet (may still be queued)" -ForegroundColor Yellow
} else {
    foreach($run in $hardenedRuns) {
        $color = switch($run.conclusion) {
            'success' { 'Green' }
            'failure' { 'Red' }
            default { if($run.status -eq 'in_progress') { 'Yellow' } else { 'Gray' } }
        }
        Write-Host "`n[$($run.status.ToUpper())] $($run.name)" -ForegroundColor $color
        Write-Host "  Conclusion: $($run.conclusion)" -ForegroundColor Gray
        Write-Host "  Created: $($run.created_at)" -ForegroundColor Gray
    }
}

Write-Host "`n=== SUMMARY ===" -ForegroundColor Cyan
$mainCount = ($runs.workflow_runs | Where-Object { $_.head_branch -eq 'main' }).Count
$hardenedCount = ($runs.workflow_runs | Where-Object { $_.head_branch -eq 'hardened' }).Count
Write-Host "Main branch runs (last 30): $mainCount"
Write-Host "Hardened branch runs (last 30): $hardenedCount"
Write-Host ""
