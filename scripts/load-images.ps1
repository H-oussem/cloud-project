# ContainerLab - Load Images into Minikube Script
# Preloads local versioned images into Minikube cluster node

$ErrorActionPreference = "Stop"

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  ContainerLab: Loading Images into Minikube         " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan

$minikube = "minikube"
if (!(Get-Command minikube -ErrorAction SilentlyContinue)) {
    if (Test-Path "C:\Users\houss\bin\minikube.exe") {
        $minikube = "C:\Users\houss\bin\minikube.exe"
    } elseif (Test-Path "C:\Program Files\Kubernetes\Minikube\minikube.exe") {
        $minikube = "C:\Program Files\Kubernetes\Minikube\minikube.exe"
    }
}

$images = @(
    "containerlab-database:v1.0.0",
    "containerlab-api:v1.0.0",
    "containerlab-frontend:v1.0.0"
)

foreach ($img in $images) {
    Write-Host "`n>>> Loading $img into Minikube..." -ForegroundColor Yellow
    $start = Get-Date
    & $minikube image load $img
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to load $img into Minikube"
        exit 1
    }
    $duration = (Get-Date) - $start
    Write-Host ">>> Successfully loaded $img in $($duration.TotalSeconds.ToString('F1'))s" -ForegroundColor Green
}

Write-Host "`n=====================================================" -ForegroundColor Green
Write-Host "  Minikube Preloaded Images Verification:            " -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
& $minikube image ls | Select-String "containerlab"
