# Setup Research Data Folder Structure
# Run this script to create organized folders for your ML research data

$baseDir = "C:\Users\joshu\Desktop\DevOps Project\research-data"

Write-Host "Creating research data folder structure..." -ForegroundColor Cyan

# Create base directory
New-Item -ItemType Directory -Force -Path $baseDir | Out-Null

# Create weekly folders
for ($week = 1; $week -le 4; $week++) {
    $weekFolder = Join-Path $baseDir "baseline-week-$week"

    # Create week folder
    New-Item -ItemType Directory -Force -Path $weekFolder | Out-Null

    # Create application folders
    foreach ($app in @("backend", "python", "frontend")) {
        $appFolder = Join-Path $weekFolder $app

        # Create category folders
        foreach ($category in @("security-scans", "container-scans", "test-coverage", "metadata", "raw-artifacts")) {
            $categoryFolder = Join-Path $appFolder $category
            New-Item -ItemType Directory -Force -Path $categoryFolder | Out-Null
        }
    }

    Write-Host "✓ Created baseline-week-$week folders" -ForegroundColor Green
}

# Create analysis folders
$analysisFolders = @(
    "analysis\charts",
    "analysis\reports",
    "analysis\datasets",
    "analysis\ml-models",
    "thesis-data\tables",
    "thesis-data\figures",
    "thesis-data\raw-exports"
)

foreach ($folder in $analysisFolders) {
    $fullPath = Join-Path $baseDir $folder
    New-Item -ItemType Directory -Force -Path $fullPath | Out-Null
}

Write-Host "✓ Created analysis and thesis folders" -ForegroundColor Green

# Create README in base folder
$readmeContent = @"
# Research Data Collection

## Folder Structure

- **baseline-week-1 to baseline-week-4**: Weekly data collection (Phase 1)
- **analysis**: Data analysis, charts, and reports
- **thesis-data**: Processed data for thesis writing

## Data Collection Schedule

### Week 1 (Current)
- Download artifacts from: https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions
- Save to: baseline-week-1/

### Week 2-4
- Repeat weekly download
- Save to respective week folders

## Quick Links

**GitHub Actions**: https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions
**Security Tab**: https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/security/code-scanning
**Repository**: https://github.com/Gungnir44/devops-ml-security-and-anomaly-research

## Instructions

See: ../scripts/download-research-data.md for detailed download instructions
"@

Set-Content -Path (Join-Path $baseDir "README.md") -Value $readmeContent

Write-Host ""
Write-Host "Research data folders created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Location: $baseDir" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Go to: https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions"
Write-Host "2. Download artifacts from latest pipeline runs"
Write-Host "3. Extract ZIPs into baseline-week-1 folders"
Write-Host ""
Write-Host "See: scripts\download-research-data.md for detailed instructions"

# Open folder in Explorer
Invoke-Item $baseDir
