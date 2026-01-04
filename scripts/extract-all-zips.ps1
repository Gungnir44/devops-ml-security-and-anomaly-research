# Extract all ZIPs in research-data folder

$baseDir = "C:\Users\joshu\Desktop\DevOps Project\research-data"
$week1Dir = Join-Path $baseDir "baseline-week-1"

Write-Host "Scanning for ZIP files..." -ForegroundColor Cyan
Write-Host ""

# Find all ZIPs
$allZips = Get-ChildItem -Path $baseDir -Filter "*.zip" -Recurse | Where-Object { $_.DirectoryName -eq $baseDir }

Write-Host "Found $($allZips.Count) ZIP files to extract" -ForegroundColor Yellow
Write-Host ""

foreach ($zip in $allZips) {
    $zipName = $zip.BaseName
    Write-Host "Processing: $zipName" -ForegroundColor Green

    # Determine target directory based on filename
    if ($zipName -match "backend") {
        $targetBase = Join-Path $week1Dir "backend"

        if ($zipName -match "research-data") {
            $targetDir = Join-Path $targetBase "metadata"
        } else {
            $targetDir = Join-Path $targetBase "security-scans"
        }
    }
    elseif ($zipName -match "python") {
        $targetBase = Join-Path $week1Dir "python"

        if ($zipName -match "pip-audit") {
            $targetDir = Join-Path $targetBase "security-scans"
        }
        elseif ($zipName -match "research-data") {
            $targetDir = Join-Path $targetBase "metadata"
        }
        else {
            $targetDir = Join-Path $targetBase "security-scans"
        }
    }
    elseif ($zipName -match "frontend") {
        $targetBase = Join-Path $week1Dir "frontend"

        if ($zipName -match "research-data") {
            $targetDir = Join-Path $targetBase "metadata"
        } else {
            $targetDir = Join-Path $targetBase "security-scans"
        }
    }
    elseif ($zipName -match "gitleaks|kics") {
        # Already extracted, skip
        Write-Host "  Skipping (already extracted)" -ForegroundColor Gray
        Write-Host ""
        continue
    }
    elseif ($zipName -match "sbom|license") {
        # Already extracted, skip
        Write-Host "  Skipping (already extracted)" -ForegroundColor Gray
        Write-Host ""
        continue
    }
    else {
        $targetDir = Join-Path $week1Dir "other-artifacts"
    }

    # Create target directory
    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null

    # Create extraction subfolder
    $extractPath = Join-Path $targetDir $zipName
    New-Item -ItemType Directory -Force -Path $extractPath | Out-Null

    # Extract
    try {
        Expand-Archive -Path $zip.FullName -DestinationPath $extractPath -Force
        $fileCount = (Get-ChildItem -Path $extractPath -Recurse -File).Count
        Write-Host "  Extracted: $fileCount files" -ForegroundColor Green
        Write-Host "  Location: $extractPath" -ForegroundColor Gray
    }
    catch {
        Write-Host "  ERROR: $_" -ForegroundColor Red
    }

    Write-Host ""
}

Write-Host "Extraction complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Opening baseline-week-1 folder..." -ForegroundColor Cyan
Invoke-Item $week1Dir
