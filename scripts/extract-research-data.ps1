# Extract and organize research data from downloaded ZIPs

$sourceDir = "C:\Users\joshu\Desktop\DevOps Project\research-data"
$week1Dir = Join-Path $sourceDir "baseline-week-1"

Write-Host "Extracting downloaded artifacts..." -ForegroundColor Cyan

# Get all ZIP files in research-data folder
$zipFiles = Get-ChildItem -Path $sourceDir -Filter "*.zip"

foreach ($zip in $zipFiles) {
    $zipName = $zip.BaseName
    Write-Host "Processing: $zipName" -ForegroundColor Yellow

    # Determine where to extract based on filename
    if ($zipName -match "backend") {
        $targetDir = Join-Path $week1Dir "backend"
    }
    elseif ($zipName -match "python") {
        $targetDir = Join-Path $week1Dir "python"
    }
    elseif ($zipName -match "frontend") {
        $targetDir = Join-Path $week1Dir "frontend"
    }
    elseif ($zipName -match "gitleaks|trufflehog|semgrep|codeql|bandit|kics") {
        $targetDir = Join-Path $week1Dir "security-scans-general"
        New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    }
    elseif ($zipName -match "sbom|license") {
        $targetDir = Join-Path $week1Dir "sbom-and-licenses"
        New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    }
    else {
        $targetDir = Join-Path $week1Dir "other-artifacts"
        New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    }

    # Create extraction folder
    $extractFolder = Join-Path $targetDir $zipName
    New-Item -ItemType Directory -Force -Path $extractFolder | Out-Null

    # Extract ZIP
    try {
        Expand-Archive -Path $zip.FullName -DestinationPath $extractFolder -Force
        Write-Host "  Extracted to: $extractFolder" -ForegroundColor Green
    }
    catch {
        Write-Host "  Error extracting: $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Extraction complete!" -ForegroundColor Green
Write-Host "Data organized in: $week1Dir" -ForegroundColor Yellow
