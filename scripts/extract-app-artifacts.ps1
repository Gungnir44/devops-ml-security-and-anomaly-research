# Extract application-specific artifacts from downloaded ZIPs
# Run this after downloading artifacts from Backend, Python, and Frontend CI/CD pipelines

$downloadsDir = "C:\Users\joshu\Desktop\DevOps Project\research-data\downloads"
$week1Dir = "C:\Users\joshu\Desktop\DevOps Project\research-data\baseline-week-1"

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "  Extracting Application Pipeline Artifacts" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

$extractedCount = 0
$totalFiles = 0

# Process each application folder
foreach ($app in @("backend", "python", "frontend")) {
    $appDownloadDir = Join-Path $downloadsDir $app
    $appWeek1Dir = Join-Path $week1Dir $app

    if (-not (Test-Path $appDownloadDir)) {
        Write-Host "Skipping $app - no downloads folder found" -ForegroundColor Yellow
        continue
    }

    $zipFiles = Get-ChildItem -Path $appDownloadDir -Filter "*.zip" -ErrorAction SilentlyContinue

    if ($zipFiles.Count -eq 0) {
        Write-Host "No ZIP files found in $app downloads folder" -ForegroundColor Yellow
        continue
    }

    Write-Host "Processing $app artifacts..." -ForegroundColor Green
    Write-Host "  Found $($zipFiles.Count) ZIP file(s)" -ForegroundColor Gray

    foreach ($zip in $zipFiles) {
        $zipName = $zip.BaseName
        Write-Host "  Extracting: $zipName" -ForegroundColor White

        # Determine target folder based on artifact name
        $targetFolder = $null

        if ($zipName -match "test|coverage") {
            $targetFolder = Join-Path $appWeek1Dir "test-coverage"
        }
        elseif ($zipName -match "security|scan|semgrep|codeql|bandit|gitleaks|trufflehog") {
            $targetFolder = Join-Path $appWeek1Dir "security-scans"
        }
        elseif ($zipName -match "container|trivy|grype|dockle") {
            $targetFolder = Join-Path $appWeek1Dir "container-scans"
        }
        elseif ($zipName -match "metadata|build|research") {
            $targetFolder = Join-Path $appWeek1Dir "metadata"
        }
        elseif ($zipName -match "sarif") {
            $targetFolder = Join-Path $appWeek1Dir "security-scans"
        }
        else {
            $targetFolder = Join-Path $appWeek1Dir "other"
        }

        # Create target folder if it doesn't exist
        New-Item -ItemType Directory -Force -Path $targetFolder | Out-Null

        # Create extraction subfolder
        $extractPath = Join-Path $targetFolder $zipName
        New-Item -ItemType Directory -Force -Path $extractPath | Out-Null

        # Extract ZIP
        try {
            Expand-Archive -Path $zip.FullName -DestinationPath $extractPath -Force
            $extractedCount++

            # Count extracted files
            $fileCount = (Get-ChildItem -Path $extractPath -Recurse -File).Count
            $totalFiles += $fileCount

            Write-Host "    Extracted to: $targetFolder" -ForegroundColor Green
            Write-Host "    Files: $fileCount" -ForegroundColor Gray
        }
        catch {
            Write-Host "    ERROR: $_" -ForegroundColor Red
        }
    }

    Write-Host ""
}

# Summary
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "  Extraction Complete!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""
Write-Host "  ZIPs Extracted: $extractedCount" -ForegroundColor Yellow
Write-Host "  Total Files: $totalFiles" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Data Location: $week1Dir" -ForegroundColor Cyan
Write-Host ""

# Generate extraction report
$reportPath = Join-Path $week1Dir "EXTRACTION-REPORT.txt"
$reportContent = @"
Application Pipeline Artifact Extraction Report
================================================
Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

Summary:
--------
ZIPs Extracted: $extractedCount
Total Files: $totalFiles

Extraction Details:
-------------------
"@

foreach ($app in @("backend", "python", "frontend")) {
    $appWeek1Dir = Join-Path $week1Dir $app
    if (Test-Path $appWeek1Dir) {
        $reportContent += "`n$app/`n"

        foreach ($category in @("security-scans", "container-scans", "test-coverage", "metadata")) {
            $categoryPath = Join-Path $appWeek1Dir $category
            if (Test-Path $categoryPath) {
                $fileCount = (Get-ChildItem -Path $categoryPath -Recurse -File).Count
                $reportContent += "  $category/: $fileCount files`n"
            }
        }
    }
}

$reportContent += "`nNext Steps:`n"
$reportContent += "1. Review extracted data in baseline-week-1/ folders`n"
$reportContent += "2. Read EXTRACTED-DATA-SUMMARY.md for analysis guide`n"
$reportContent += "3. Begin Week 1 baseline analysis`n"

Set-Content -Path $reportPath -Value $reportContent

Write-Host "Extraction report saved to: $reportPath" -ForegroundColor Green
Write-Host ""

# Open the week-1 folder in Explorer
Write-Host "Opening baseline-week-1 folder..." -ForegroundColor Cyan
Invoke-Item $week1Dir
