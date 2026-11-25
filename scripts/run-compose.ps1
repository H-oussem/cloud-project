# ContainerLab - Docker Compose Launch & Health Verification Script (Test T03)

$ErrorActionPreference = "Stop"

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  ContainerLab: Launching Docker Compose Stack       " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan

# Start services in detached mode
Write-Host "`n>>> Starting services via docker compose up -d..." -ForegroundColor Yellow
docker compose up -d

Write-Host "`n>>> Waiting for services to reach 'healthy' state..." -ForegroundColor Yellow
$maxRetries = 20
$healthy = $false

for ($i = 1; $i -le $maxRetries; $i++) {
    Start-Sleep -Seconds 2
    $statuses = docker compose ps --format json | ConvertFrom-Json
    $allHealthy = $true

    foreach ($svc in $statuses) {
        $statusStr = $svc.Status
        $name = $svc.Name
        Write-Host "Service $name : $statusStr" -ForegroundColor DarkGray
        if ($statusStr -notmatch "healthy") {
            $allHealthy = $false
        }
    }

    if ($allHealthy -and $statuses.Count -ge 3) {
        $healthy = $true
        break
    }
}

if ($healthy) {
    Write-Host "`n=====================================================" -ForegroundColor Green
    Write-Host "  All services healthy!                              " -ForegroundColor Green
    Write-Host "=====================================================" -ForegroundColor Green
    docker compose ps
    Write-Host "`nFrontend is live and accessible at: http://localhost:3000" -ForegroundColor Cyan
} else {
    Write-Host "`n[WARN] Services did not reach healthy state in time." -ForegroundColor Yellow
    docker compose ps
}
