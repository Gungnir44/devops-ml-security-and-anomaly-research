# Start Monitoring Stack - Helper Script (Windows)
# Author: Joshua
# Description: Easy startup for Docker monitoring stack

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  DevOps Monitoring Stack - Startup    ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "[OK] Docker is running" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Docker is not running" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again"
    exit 1
}

# Check if config.json exists
if (-not (Test-Path "..\scripts\python\config.json")) {
    Write-Host "[INFO] config.json not found, creating from example..." -ForegroundColor Yellow
    Copy-Item "..\scripts\python\config.example.json" "..\scripts\python\config.json"
    Write-Host "[OK] Created config.json" -ForegroundColor Green
}

# Stop existing containers (if any)
Write-Host ""
Write-Host "Stopping existing containers..." -ForegroundColor Yellow
docker-compose -f docker-compose-monitoring.yml down 2>$null

# Start the stack
Write-Host ""
Write-Host "Starting monitoring stack..." -ForegroundColor Yellow
docker-compose -f docker-compose-monitoring.yml up -d

# Wait for services to start
Write-Host ""
Write-Host "Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check status
Write-Host ""
Write-Host "Container Status:" -ForegroundColor Cyan
docker-compose -f docker-compose-monitoring.yml ps

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║         Stack Started Successfully!     ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Access your services:" -ForegroundColor Cyan
Write-Host "  Dashboard:   " -NoNewline; Write-Host "http://localhost:5000" -ForegroundColor Green
Write-Host "  Web Demo:    " -NoNewline; Write-Host "http://localhost:8080" -ForegroundColor Green
Write-Host "  API:         " -NoNewline; Write-Host "http://localhost:5000/api/latest" -ForegroundColor Green
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Cyan
Write-Host "  View logs:       docker-compose -f docker-compose-monitoring.yml logs -f"
Write-Host "  Stop stack:      docker-compose -f docker-compose-monitoring.yml down"
Write-Host "  Restart:         docker-compose -f docker-compose-monitoring.yml restart"
Write-Host "  Container stats: docker stats"
Write-Host ""
Write-Host "Tip: The dashboard will update automatically as health checks run" -ForegroundColor Yellow
Write-Host ""
