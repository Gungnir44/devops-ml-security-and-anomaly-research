param([Parameter(Mandatory=$true)][string]$Token)

$headers = @{Authorization = "Bearer $Token"; Accept = "application/vnd.github+json"}
$runs = Invoke-RestMethod -Uri "https://api.github.com/repos/Gungnir44/devops-ml-security-and-anomaly-research/actions/runs?per_page=5" -Headers $headers

Write-Host "Recent Workflow Runs:" -ForegroundColor Cyan
Write-Host ""

foreach($run in $runs.workflow_runs){
    $status = $run.status
    $color = if($status -eq 'completed'){'Green'}elseif($status -eq 'in_progress'){'Yellow'}else{'Gray'}
    Write-Host "[$($status.ToUpper())] $($run.name)" -ForegroundColor $color
    Write-Host "  Conclusion: $($run.conclusion)" -ForegroundColor Gray
    Write-Host "  Created: $($run.created_at)" -ForegroundColor Gray
    Write-Host "  URL: $($run.html_url)" -ForegroundColor Blue
    Write-Host ""
}
