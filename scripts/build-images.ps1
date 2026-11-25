# ContainerLab - Build Images Script
# Builds all three production multi-stage images with strict version tags (v1.0.0)

$ErrorActionPreference = "Stop"

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  ContainerLab: Building Production Images (v1.0.0)  " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan

$images = @(
    @{ Name = "containerlab-database:v1.0.0"; Context = "./application/database"; File = "Dockerfile" },
    @{ Name = "containerlab-api:v1.0.0"; Context = "./application/backend"; File = "Dockerfile" },
    @{ Name = "containerlab-frontend:v1.0.0"; Context = "./application/frontend"; File = "Dockerfile" }
)

foreach ($img in $images) {
    Write-Host "`n>>> Building $($img.Name)..." -ForegroundColor Yellow
    $start = Get-Date
    docker build -t $img.Name -f "$($img.Context)/$($img.File)" $img.Context
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to build $($img.Name)"
        exit 1
    }
    $duration = (Get-Date) - $start
    Write-Host ">>> Successfully built $($img.Name) in $($duration.TotalSeconds.ToString('F1'))s" -ForegroundColor Green
}

Write-Host "`n=====================================================" -ForegroundColor Cyan
Write-Host "  Built Images Summary:                              " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
docker images --filter "reference=containerlab-*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
