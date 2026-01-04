# Download GitHub Actions artifacts using GitHub API
# This script downloads all artifacts from recent workflow runs

param(
    [string]$Token = "",
    [string]$Owner = "Gungnir44",
    [string]$Repo = "devops-ml-security-and-anomaly-research"
)

# Check if token is provided
if ($Token -eq "") {
    Write-Host "ERROR: GitHub token required" -ForegroundColor Red
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\download-artifacts.ps1 -Token YOUR_GITHUB_TOKEN" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To create a token:" -ForegroundColor Cyan
    Write-Host "  1. Go to: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "  2. Click 'Generate new token (classic)'" -ForegroundColor White
    Write-Host "  3. Select scopes: 'repo' and 'workflow'" -ForegroundColor White
    Write-Host "  4. Generate and copy the token" -ForegroundColor White
    Write-Host ""
    exit 1
}

$downloadDir = "C:\Users\joshu\Desktop\DevOps Project\research-data\downloads"
$headers = @{
    Authorization = "Bearer $Token"
    Accept = "application/vnd.github+json"
}

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "  GitHub Artifacts Downloader" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

# Get recent workflow runs
Write-Host "Fetching workflow runs..." -ForegroundColor Yellow
$runsUrl = "https://api.github.com/repos/$Owner/$Repo/actions/runs?per_page=10"

try {
    $runs = Invoke-RestMethod -Uri $runsUrl -Headers $headers
}
catch {
    Write-Host "ERROR: Failed to fetch workflow runs" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

Write-Host "Found $($runs.workflow_runs.Count) recent workflow runs" -ForegroundColor Green
Write-Host ""

# Process each workflow run
$totalDownloaded = 0

foreach ($run in $runs.workflow_runs) {
    $workflowName = $run.name
    $runId = $run.id
    $conclusion = $run.conclusion
    $createdAt = $run.created_at

    Write-Host "Workflow: $workflowName" -ForegroundColor Cyan
    Write-Host "  Run ID: $runId" -ForegroundColor Gray
    Write-Host "  Status: $conclusion" -ForegroundColor Gray
    Write-Host "  Created: $createdAt" -ForegroundColor Gray

    # Get artifacts for this run
    $artifactsUrl = "https://api.github.com/repos/$Owner/$Repo/actions/runs/$runId/artifacts"

    try {
        $artifacts = Invoke-RestMethod -Uri $artifactsUrl -Headers $headers
    }
    catch {
        Write-Host "  ERROR: Failed to fetch artifacts" -ForegroundColor Red
        continue
    }

    if ($artifacts.artifacts.Count -eq 0) {
        Write-Host "  No artifacts found" -ForegroundColor Yellow
        Write-Host ""
        continue
    }

    Write-Host "  Found $($artifacts.artifacts.Count) artifact(s)" -ForegroundColor Green

    # Download each artifact
    foreach ($artifact in $artifacts.artifacts) {
        $artifactName = $artifact.name
        $artifactId = $artifact.id
        $sizeInMB = [math]::Round($artifact.size_in_bytes / 1MB, 2)

        Write-Host "    Downloading: $artifactName ($sizeInMB MB)" -ForegroundColor White

        # Determine download folder based on workflow name
        if ($workflowName -match "Backend") {
            $targetDir = Join-Path $downloadDir "backend"
        }
        elseif ($workflowName -match "Python") {
            $targetDir = Join-Path $downloadDir "python"
        }
        elseif ($workflowName -match "Frontend") {
            $targetDir = Join-Path $downloadDir "frontend"
        }
        else {
            $targetDir = Join-Path $downloadDir "other"
        }

        New-Item -ItemType Directory -Force -Path $targetDir | Out-Null

        $downloadUrl = "https://api.github.com/repos/$Owner/$Repo/actions/artifacts/$artifactId/zip"
        $outputPath = Join-Path $targetDir "$artifactName.zip"

        # Skip if already downloaded
        if (Test-Path $outputPath) {
            Write-Host "      Already exists, skipping" -ForegroundColor Gray
            continue
        }

        try {
            Invoke-RestMethod -Uri $downloadUrl -Headers $headers -OutFile $outputPath
            Write-Host "      Saved to: $outputPath" -ForegroundColor Green
            $totalDownloaded++
        }
        catch {
            Write-Host "      ERROR: Download failed" -ForegroundColor Red
        }
    }

    Write-Host ""
}

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "  Download Complete!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""
Write-Host "Total artifacts downloaded: $totalDownloaded" -ForegroundColor Yellow
Write-Host "Location: $downloadDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next step: Run .\extract-app-artifacts.ps1 to organize the data" -ForegroundColor Yellow
