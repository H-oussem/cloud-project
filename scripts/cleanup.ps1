# ContainerLab - Cleanup & Teardown Script
param(
    [switch]$All
)

Write-Host "=====================================================" -ForegroundColor Yellow
Write-Host "  ContainerLab: Environment Teardown & Cleanup       " -ForegroundColor Yellow
Write-Host "=====================================================" -ForegroundColor Yellow

# 1. Stop Docker Compose
Write-Host "`n>>> Stopping Docker Compose services..." -ForegroundColor Yellow
if ($All) {
    docker compose down -v
    Write-Host ">>> Docker Compose stopped and volumes removed." -ForegroundColor Green
} else {
    docker compose down
    Write-Host ">>> Docker Compose stopped (volumes preserved)." -ForegroundColor Green
}

# 2. Delete Kubernetes Namespace
Write-Host "`n>>> Cleaning Kubernetes namespace 'containerlab'..." -ForegroundColor Yellow
kubectl delete namespace containerlab --ignore-not-found=true --timeout=60s

Write-Host "`nCleanup complete!" -ForegroundColor Green
