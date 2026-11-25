# ContainerLab - Pre-Flight Environment Verification Script
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  ContainerLab: Pre-Flight Environment Verification  " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan

$allPassed = $true

# 1. Check Docker Daemon
Write-Host "`n[1/5] Checking Docker Engine..." -NoNewline
try {
    $dockerInfo = docker info --format '{{.ServerVersion}}' 2>$null
    if ($LASTEXITCODE -eq 0 -and $dockerInfo) {
        Write-Host " [PASS] (Docker v$dockerInfo running)" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] (Docker daemon not running)" -ForegroundColor Red
        $allPassed = $false
    }
} catch {
    Write-Host " [FAIL] (Docker CLI error)" -ForegroundColor Red
    $allPassed = $false
}

# 2. Check Docker Compose
Write-Host "[2/5] Checking Docker Compose..." -NoNewline
try {
    $composeVersion = docker compose version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " [PASS] ($composeVersion)" -ForegroundColor Green
    } else {
        Write-Host " [FAIL]" -ForegroundColor Red
        $allPassed = $false
    }
} catch {
    Write-Host " [FAIL]" -ForegroundColor Red
    $allPassed = $false
}

# 3. Check Kubectl
Write-Host "[3/5] Checking kubectl CLI..." -NoNewline
try {
    $kubectlVer = kubectl version --client 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " [PASS]" -ForegroundColor Green
    } else {
        Write-Host " [FAIL]" -ForegroundColor Red
        $allPassed = $false
    }
} catch {
    Write-Host " [FAIL]" -ForegroundColor Red
    $allPassed = $false
}

# 4. Check Minikube
Write-Host "[4/5] Checking Minikube CLI..." -NoNewline
$minikubeCmd = Get-Command minikube -ErrorAction SilentlyContinue
if ($minikubeCmd) {
    Write-Host " [PASS] ($($minikubeCmd.Source))" -ForegroundColor Green
} else {
    # Check common installation paths
    if (Test-Path "C:\Users\houss\bin\minikube.exe") {
        Write-Host " [PASS] (Found in C:\Users\houss\bin)" -ForegroundColor Green
        $env:PATH += ";C:\Users\houss\bin"
    } elseif (Test-Path "C:\Program Files\Kubernetes\Minikube\minikube.exe") {
        Write-Host " [PASS] (Found at C:\Program Files\Kubernetes\Minikube)" -ForegroundColor Green
        $env:PATH += ";C:\Program Files\Kubernetes\Minikube"
    } else {
        Write-Host " [WARN] (Minikube not found in current PATH)" -ForegroundColor Yellow
        $allPassed = $false
    }
}

# 5. Check Node & NPM
Write-Host "[5/5] Checking Node.js & NPM..." -NoNewline
try {
    $nodeVer = node --version 2>$null
    $npmVer = npm --version 2>$null
    Write-Host " [PASS] (Node: $nodeVer, NPM: $npmVer)" -ForegroundColor Green
} catch {
    Write-Host " [FAIL]" -ForegroundColor Red
    $allPassed = $false
}

Write-Host "`n-----------------------------------------------------"
if ($allPassed) {
    Write-Host "All prerequisites satisfied! System ready for ContainerLab." -ForegroundColor Green
} else {
    Write-Host "Some prerequisites are missing or not running. Please review the output above." -ForegroundColor Yellow
}
