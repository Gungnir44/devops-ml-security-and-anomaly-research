# Simple script to create research data folders

$base = "C:\Users\joshu\Desktop\DevOps Project\research-data"

# Create main folder
New-Item -ItemType Directory -Force -Path $base

# Create weekly folders
1..4 | ForEach-Object {
    $week = "baseline-week-$_"

    New-Item -ItemType Directory -Force -Path "$base\$week\backend\security-scans"
    New-Item -ItemType Directory -Force -Path "$base\$week\backend\container-scans"
    New-Item -ItemType Directory -Force -Path "$base\$week\backend\test-coverage"
    New-Item -ItemType Directory -Force -Path "$base\$week\backend\metadata"

    New-Item -ItemType Directory -Force -Path "$base\$week\python\security-scans"
    New-Item -ItemType Directory -Force -Path "$base\$week\python\container-scans"
    New-Item -ItemType Directory -Force -Path "$base\$week\python\test-coverage"
    New-Item -ItemType Directory -Force -Path "$base\$week\python\metadata"

    New-Item -ItemType Directory -Force -Path "$base\$week\frontend\security-scans"
    New-Item -ItemType Directory -Force -Path "$base\$week\frontend\container-scans"
    New-Item -ItemType Directory -Force -Path "$base\$week\frontend\test-coverage"
    New-Item -ItemType Directory -Force -Path "$base\$week\frontend\metadata"

    Write-Host "Created $week folders"
}

# Create analysis folders
New-Item -ItemType Directory -Force -Path "$base\analysis\charts"
New-Item -ItemType Directory -Force -Path "$base\analysis\reports"
New-Item -ItemType Directory -Force -Path "$base\thesis-data"

Write-Host "Done! Opening folder..."
Invoke-Item $base
