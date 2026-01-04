param([Parameter(Mandatory=$true)][string]$Token, [Parameter(Mandatory=$true)][string]$RunId)

$headers = @{Authorization = "Bearer $Token"; Accept = "application/vnd.github+json"}
$run = Invoke-RestMethod -Uri "https://api.github.com/repos/Gungnir44/devops-ml-security-and-anomaly-research/actions/runs/$RunId" -Headers $headers
$jobs = Invoke-RestMethod -Uri $run.jobs_url -Headers $headers

Write-Host "Workflow: $($run.name)" -ForegroundColor Cyan
Write-Host "Status: $($run.conclusion)" -ForegroundColor $(if($run.conclusion -eq 'success'){'Green'}else{'Red'})
Write-Host ""

foreach($job in $jobs.jobs){
    if($job.conclusion -ne 'success'){
        Write-Host "Failed Job: $($job.name)" -ForegroundColor Yellow
        foreach($step in $job.steps){
            if($step.conclusion -eq 'failure'){
                Write-Host "  X $($step.name)" -ForegroundColor Red
            }
        }
        Write-Host ""
    }
}
