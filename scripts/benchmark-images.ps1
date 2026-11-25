# ContainerLab - Image Size Benchmarking Script (Test T02)
# Compares unoptimized baselines against optimized multi-stage images

$ErrorActionPreference = "Stop"

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  ContainerLab: T02 Docker Image Size Benchmark      " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan

# 1. Build unoptimized baselines
Write-Host "`n>>> [1/2] Building unoptimized baselines..." -ForegroundColor Yellow
docker build -t containerlab-backend:unoptimized -f ./application/backend/Dockerfile.unoptimized ./application/backend
docker build -t containerlab-frontend:unoptimized -f ./application/frontend/Dockerfile.unoptimized ./application/frontend

# 2. Extract image sizes
function Get-DockerImageSizeInMB {
    param ([string]$ImageTag)
    $sizeStr = docker inspect --format '{{.Size}}' $ImageTag
    $bytes = [int64]$sizeStr
    return [Math]::Round($bytes / 1MB, 2)
}

$backendUnopt = Get-DockerImageSizeInMB "containerlab-backend:unoptimized"
$backendOpt = Get-DockerImageSizeInMB "containerlab-api:v1.0.0"
$backendDiff = [Math]::Round($backendUnopt - $backendOpt, 2)
$backendPct = [Math]::Round(($backendDiff / $backendUnopt) * 100, 1)

$frontendUnopt = Get-DockerImageSizeInMB "containerlab-frontend:unoptimized"
$frontendOpt = Get-DockerImageSizeInMB "containerlab-frontend:v1.0.0"
$frontendDiff = [Math]::Round($frontendUnopt - $frontendOpt, 2)
$frontendPct = [Math]::Round(($frontendDiff / $frontendUnopt) * 100, 1)

$databaseSize = Get-DockerImageSizeInMB "containerlab-database:v1.0.0"

# 3. Output Table
Write-Host "`n=====================================================" -ForegroundColor Green
Write-Host "                BENCHMARK RESULTS                     " -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ("{0,-15} | {1,-14} | {2,-12} | {3,-12} | {4,-10}" -f "Component", "Unoptimized", "Optimized", "Difference", "Reduction")
Write-Host "-----------------------------------------------------------------------"
Write-Host ("{0,-15} | {1,11} MB | {2,9} MB | -{3,9} MB | {4,8}%" -f "Backend API", $backendUnopt, $backendOpt, $backendDiff, $backendPct)
Write-Host ("{0,-15} | {1,11} MB | {2,9} MB | -{3,9} MB | {4,8}%" -f "Frontend Web", $frontendUnopt, $frontendOpt, $frontendDiff, $frontendPct)
Write-Host ("{0,-15} | {1,11}    | {2,9} MB | {3,12} | {4,10}" -f "Database (pg)", "N/A", $databaseSize, "-", "-")
Write-Host "-----------------------------------------------------------------------"

# 4. Save to docs/benchmarks/image-sizes.md
$docsDir = "./docs/benchmarks"
if (!(Test-Path $docsDir)) { New-Item -ItemType Directory -Path $docsDir -Force }

$mdReport = @"
# Docker Image Optimization Benchmarks (Test T02)
*Automated execution timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')*

| Component | Unoptimized Baseline | Optimized Multi-Stage | Size Saved | Reduction % |
|---|---|---|---|---|
| **Backend API (Node.js)** | ${backendUnopt} MB | ${backendOpt} MB | -${backendDiff} MB | **${backendPct}%** |
| **Frontend Web (React+Nginx)** | ${frontendUnopt} MB | ${frontendOpt} MB | -${frontendDiff} MB | **${frontendPct}%** |
| **Database (PostgreSQL)** | *N/A (Official base)* | ${databaseSize} MB | - | - |

### Key Optimization Techniques Applied:
1. **Frontend**: Multi-stage build separates Vite build-time tools (Node.js runtime, compilers, TypeScript/Babel tools) from runtime delivery (Nginx `stable-alpine-slim`), serving strictly static HTML/CSS/JS.
2. **Backend**: Alpine runtime base, `npm ci --omit=dev` strips devDependencies, and runs as an unprivileged non-root user (`USER node`).
3. **Security**: Non-root execution reduces attack surface; stripped toolchains prevent compiler exploits inside production containers.
"@

Set-Content -Path "$docsDir/image-sizes.md" -Value $mdReport
Write-Host "`nBenchmark report saved to: $docsDir/image-sizes.md" -ForegroundColor Cyan
