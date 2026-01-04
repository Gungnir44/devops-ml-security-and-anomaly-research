$source = "C:\Users\joshu\Desktop\DevOps Project\research-data\downloads\other\bandit-security-report.zip"
$target = "C:\Users\joshu\Desktop\DevOps Project\research-data\baseline-week-1\python\security-scans\bandit-report"

Write-Host "Extracting Bandit security report..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path $target | Out-Null
Expand-Archive -Path $source -DestinationPath $target -Force
Write-Host "Done! Extracted to: $target" -ForegroundColor Green

# Check what was extracted
$files = Get-ChildItem -Path $target -Recurse -File
Write-Host "Files extracted: $($files.Count)" -ForegroundColor Yellow
$files | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor Gray }
