# ContainerLab - Incremental Kubernetes Deployment Script (Test T06)

$ErrorActionPreference = "Stop"

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  ContainerLab: Deploying Manifests to Kubernetes    " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan

$manifests = @(
    "00-namespace.yaml",
    "01-configmap.yaml",
    "02-api-secret.yaml",
    "03-database-pvc.yaml",
    "04-database-deployment.yaml",
    "05-database-service.yaml",
    "06-api-deployment.yaml",
    "07-api-service.yaml",
    "08-frontend-deployment.yaml",
    "09-frontend-service.yaml"
)

foreach ($m in $manifests) {
    $path = "kubernetes/$m"
    Write-Host "`n>>> Applying $m..." -ForegroundColor Yellow
    kubectl apply -f $path
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to apply $path"
        exit 1
    }
}

Write-Host "`n>>> Waiting for PostgreSQL PVC to become Bound..." -ForegroundColor Yellow
$pvcBound = $false
for ($i = 1; $i -le 15; $i++) {
    $pvcStatus = kubectl get pvc postgres-pvc -n containerlab -o jsonpath='{.status.phase}' 2>$null
    Write-Host "PVC Status: $pvcStatus" -ForegroundColor DarkGray
    if ($pvcStatus -eq "Bound") {
        $pvcBound = $true
        break
    }
    Start-Sleep -Seconds 2
}

if ($pvcBound) {
    Write-Host ">>> PVC Bound successfully!" -ForegroundColor Green
} else {
    Write-Host "[WARN] PVC did not reach Bound state yet." -ForegroundColor Yellow
}

Write-Host "`n>>> Waiting for Deployments rollout..." -ForegroundColor Yellow
kubectl rollout status deployment/postgres -n containerlab --timeout=60s
kubectl rollout status deployment/api -n containerlab --timeout=60s
kubectl rollout status deployment/frontend -n containerlab --timeout=60s

Write-Host "`n=====================================================" -ForegroundColor Green
Write-Host "  Kubernetes Cluster Status (Namespace: containerlab)" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
kubectl get all,pvc,configmap,secret -n containerlab
