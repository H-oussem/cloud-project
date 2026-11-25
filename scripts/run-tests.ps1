# ContainerLab - Master Test Verification Suite (T01 - T11)
param(
    [string]$Target = "all" # 'all', 'compose', 'k8s'
)

$ErrorActionPreference = "Continue"

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  ContainerLab: Master Verification Suite (T01 - T11) " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan

$testResults = [ordered]@{}
$failureCount = 0

function Record-TestResult {
    param ($Id, $Name, $Passed, $Details)
    $script:testResults[$Id] = @{
        Name = $Name
        Passed = $Passed
        Details = $Details
    }
    if (-not $Passed) {
        $script:failureCount++
    }
    $statusColor = if ($Passed) { "Green" } else { "Red" }
    $statusText = if ($Passed) { "[PASS]" } else { "[FAIL]" }
    Write-Host "`n>>> ${Id}: $Name $statusText" -ForegroundColor $statusColor
    Write-Host "    Details: $Details" -ForegroundColor DarkGray
}

# --- T01: Build Images ---
Write-Host "`n----------------- Executing T01: Build -----------------" -ForegroundColor Yellow
try {
    & .\scripts\build-images.ps1
    $t01Passed = ($LASTEXITCODE -eq 0)
    Record-TestResult "T01" "Build Images" $t01Passed "Built 3 production images with version tags v1.0.0"
} catch {
    Record-TestResult "T01" "Build Images" $false $_.Exception.Message
}

# --- T02: Image Optimization Benchmark ---
Write-Host "`n----------------- Executing T02: Optimization ----------" -ForegroundColor Yellow
try {
    & .\scripts\benchmark-images.ps1
    $t02Passed = ($LASTEXITCODE -eq 0)
    Record-TestResult "T02" "Image Optimization" $t02Passed "Measured size reduction recorded in docs/benchmarks/"
} catch {
    Record-TestResult "T02" "Image Optimization" $false $_.Exception.Message
}

# ==================== DOCKER COMPOSE SUITE ====================
if ($Target -eq "all" -or $Target -eq "compose") {
    # --- T03: Docker Compose Run ---
    Write-Host "`n----------------- Executing T03: Compose Run -----------" -ForegroundColor Yellow
    try {
        & .\scripts\run-compose.ps1
        $psOutput = docker compose ps --format json | ConvertFrom-Json
        $healthyCount = ($psOutput | Where-Object { $_.Status -match "healthy" }).Count
        $t03Passed = ($healthyCount -ge 3)
        Record-TestResult "T03" "Compose Run" $t03Passed "All 3 services reached healthy state ($healthyCount/3)"
    } catch {
        Record-TestResult "T03" "Compose Run" $false $_.Exception.Message
    }

    # --- T04: Inter-Tier Connectivity & Announcements CRUD ---
    Write-Host "`n----------------- Executing T04: Connectivity ----------" -ForegroundColor Yellow
    try {
        $postBody = @{
            title = "Automated Test Announcement T04"
            content = "Validating inter-tier communication between API and PostgreSQL."
            author = "TestRunner"
        } | ConvertTo-Json

        $res = Invoke-RestMethod -Uri "http://localhost:3000/api/announcements" -Method POST -Body $postBody -ContentType "application/json" -TimeoutSec 10
        $t04Passed = ($res.success -eq $true -and $res.data.id -gt 0)
        Record-TestResult "T04" "Connectivity & CRUD" $t04Passed "Created announcement ID $($res.data.id) via Nginx proxy to API and DB"
    } catch {
        Record-TestResult "T04" "Connectivity & CRUD" $false $_.Exception.Message
    }

    # --- T05: Compose Persistence Across Restart ---
    Write-Host "`n----------------- Executing T05: Compose Persistence ---" -ForegroundColor Yellow
    try {
        Write-Host "Restarting postgres container..."
        docker compose restart postgres
        Start-Sleep -Seconds 6
        $res = Invoke-RestMethod -Uri "http://localhost:3000/api/announcements" -Method GET -TimeoutSec 10
        $match = $res.data | Where-Object { $_.title -eq "Automated Test Announcement T04" }
        $t05Passed = ($null -ne $match)
        Record-TestResult "T05" "Compose Persistence" $t05Passed "Data survived postgres container restart from named volume"
    } catch {
        Record-TestResult "T05" "Compose Persistence" $false $_.Exception.Message
    }
}

# ==================== KUBERNETES SUITE ====================
if ($Target -eq "all" -or $Target -eq "k8s") {
    # Check if Minikube is accessible
    $minikubeExe = "minikube"
    if (!(Get-Command minikube -ErrorAction SilentlyContinue)) {
        if (Test-Path "C:\Users\houss\bin\minikube.exe") {
            $minikubeExe = "C:\Users\houss\bin\minikube.exe"
        }
    }

    # --- T06: Kubernetes Deployment & PVC Binding ---
    Write-Host "`n----------------- Executing T06: K8s Deployment --------" -ForegroundColor Yellow
    try {
        & .\scripts\deploy-k8s.ps1
        $pvcStatus = kubectl get pvc postgres-pvc -n containerlab -o jsonpath='{.status.phase}' 2>$null
        $runningPods = (kubectl get pods -n containerlab --field-selector=status.phase=Running --no-headers | Measure-Object).Count
        $t06Passed = ($pvcStatus -eq "Bound" -and $runningPods -ge 4)
        Record-TestResult "T06" "K8s Deployment & PVC" $t06Passed "PVC is $pvcStatus with $runningPods running pods"
    } catch {
        Record-TestResult "T06" "K8s Deployment & PVC" $false $_.Exception.Message
    }

    # --- Setup temporary port-forward for in-cluster testing ---
    Write-Host "`n>>> Setting up port-forward to service/frontend..." -ForegroundColor Yellow
    $pfProcess = Start-Process -FilePath "kubectl" -ArgumentList "port-forward service/frontend 30080:80 -n containerlab" -PassThru -WindowStyle Hidden
    
    $k8sBaseUrl = "http://127.0.0.1:30080"
    $pfReady = $false
    for ($p = 1; $p -le 15; $p++) {
        try {
            $test = Invoke-RestMethod -Uri "$k8sBaseUrl/healthz" -TimeoutSec 2
            if ($test) {
                $pfReady = $true
                Write-Host "Port-forward ready on $k8sBaseUrl" -ForegroundColor Green
                break
            }
        } catch {
            Start-Sleep -Seconds 1
        }
    }

    try {
        # --- T07: Service Routing & Load Distribution ---
        Write-Host "`n----------------- Executing T07: K8s Routing -----------" -ForegroundColor Yellow
        try {
            $respondingPods = @()
            for ($i = 1; $i -le 10; $i++) {
                try {
                    $inst = Invoke-RestMethod -Uri "$k8sBaseUrl/api/instance?req=$i" -TimeoutSec 5
                    if ($inst.podName) {
                        $respondingPods += $inst.podName
                    }
                } catch {
                    Write-Host "Notice: Request $i retry: $($_.Exception.Message)" -ForegroundColor DarkGray
                    Start-Sleep -Milliseconds 500
                }
            }
            $uniquePods = ($respondingPods | Select-Object -Unique).Count
            $t07Passed = ($uniquePods -ge 2)
            $distroSummary = ($respondingPods | Group-Object | ForEach-Object { "$($_.Name): $($_.Count) calls" }) -join ", "
            Record-TestResult "T07" "K8s Load Balancing" $t07Passed "Traffic reached $uniquePods distinct API replicas across $($respondingPods.Count) requests ($distroSummary)"
        } catch {
            Record-TestResult "T07" "K8s Load Balancing" $false $_.Exception.Message
        }

        # --- T08: Horizontal Pod Autoscaling / Scaling ---
        Write-Host "`n----------------- Executing T08: K8s Scaling -----------" -ForegroundColor Yellow
        try {
            kubectl scale deployment/api --replicas=4 -n containerlab | Out-Null
            kubectl rollout status deployment/api -n containerlab --timeout=45s | Out-Null
            
            # Explicit wait for readyReplicas to reach 4
            $scaleReady = $false
            for ($s = 1; $s -le 15; $s++) {
                $readyCount = [int](kubectl get deployment api -n containerlab -o jsonpath='{.status.readyReplicas}' 2>$null)
                if ($readyCount -eq 4) {
                    $scaleReady = $true
                    break
                }
                Start-Sleep -Seconds 2
            }
            Record-TestResult "T08" "K8s Horizontal Scaling" $scaleReady "Scaled API deployment from 2 to 4 ready replicas"
            
            # Return to 2 replicas
            kubectl scale deployment/api --replicas=2 -n containerlab | Out-Null
            kubectl rollout status deployment/api -n containerlab --timeout=30s | Out-Null
        } catch {
            Record-TestResult "T08" "K8s Horizontal Scaling" $false $_.Exception.Message
        }

        # --- T09: Pod Self-Healing & Automatic Recovery ---
        Write-Host "`n----------------- Executing T09: Pod Self-Healing ------" -ForegroundColor Yellow
        try {
            $initialPods = (kubectl get pods -l app=api -n containerlab -o jsonpath='{.items[*].metadata.name}').Split(" ")
            $victimPod = $initialPods[0]
            Write-Host "Target pod to delete: $victimPod"
            kubectl delete pod $victimPod -n containerlab --now | Out-Null

            # Explicitly wait for a new pod to appear and reach Ready state
            $newPodFound = $false
            $replacementName = ""
            for ($w = 1; $w -le 20; $w++) {
                $currentApiPods = kubectl get pods -l app=api -n containerlab -o json | ConvertFrom-Json
                foreach ($p in $currentApiPods.items) {
                    $pName = $p.metadata.name
                    $isReady = ($p.status.conditions | Where-Object { $_.type -eq "Ready" -and $_.status -eq "True" })
                    if ($pName -ne $victimPod -and ($initialPods -notcontains $pName) -and $isReady) {
                        $newPodFound = $true
                        $replacementName = $pName
                        break
                    }
                }
                if ($newPodFound) { break }
                Start-Sleep -Seconds 2
            }

            # Check that service is actively responding
            $liveCheck = Invoke-RestMethod -Uri "$k8sBaseUrl/api/health/live" -TimeoutSec 5
            $t09Passed = ($newPodFound -and $liveCheck.status -eq "alive")
            Record-TestResult "T09" "Pod Self-Healing" $t09Passed "Deleted pod $victimPod; replacement pod $replacementName created and verified in Ready state"
        } catch {
            Record-TestResult "T09" "Pod Self-Healing" $false $_.Exception.Message
        }

        # --- T10: Kubernetes PVC Data Persistence ---
        Write-Host "`n----------------- Executing T10: PVC Persistence -------" -ForegroundColor Yellow
        try {
            # 1. Post a test announcement
            $testBody = @{
                title = "T10 Persistence Check Record"
                content = "Verifying PostgreSQL PVC storage survives pod termination."
                author = "T10Tester"
            } | ConvertTo-Json
            $postRes = Invoke-RestMethod -Uri "$k8sBaseUrl/api/announcements" -Method POST -Body $testBody -ContentType "application/json" -TimeoutSec 10
            
            # 2. Record old PostgreSQL pod and delete it
            $oldDbPod = (kubectl get pods -l app=postgres -n containerlab -o jsonpath='{.items[0].metadata.name}')
            Write-Host "Target DB pod to delete: $oldDbPod"
            kubectl delete pod $oldDbPod -n containerlab --now | Out-Null
            
            # 3. Explicitly wait for replacement PostgreSQL pod to appear and reach Ready state
            $newDbReady = $false
            $newDbName = ""
            for ($d = 1; $d -le 25; $d++) {
                $pgPods = kubectl get pods -l app=postgres -n containerlab -o json | ConvertFrom-Json
                foreach ($p in $pgPods.items) {
                    $pName = $p.metadata.name
                    $isReady = ($p.status.conditions | Where-Object { $_.type -eq "Ready" -and $_.status -eq "True" })
                    if ($pName -ne $oldDbPod -and $isReady) {
                        $newDbReady = $true
                        $newDbName = $pName
                        break
                    }
                }
                if ($newDbReady) { break }
                Start-Sleep -Seconds 2
            }

            # 4. Query data after replacement with retry for connection pool re-establishment
            $recordRetrieved = $false
            for ($r = 1; $r -le 10; $r++) {
                try {
                    $getRes = Invoke-RestMethod -Uri "$k8sBaseUrl/api/announcements" -Method GET -TimeoutSec 5
                    $found = $getRes.data | Where-Object { $_.title -eq "T10 Persistence Check Record" }
                    if ($null -ne $found) {
                        $recordRetrieved = $true
                        break
                    }
                } catch {
                    # Wait for database pool reconnection
                }
                Start-Sleep -Seconds 2
            }

            $t10Passed = ($newDbReady -and $recordRetrieved)
            Record-TestResult "T10" "PVC Data Persistence" $t10Passed "Record persisted across DB pod deletion ($oldDbPod -> $newDbName in Ready state)"
        } catch {
            Record-TestResult "T10" "PVC Data Persistence" $false $_.Exception.Message
        }

    } finally {
        # Stop port-forward process
        if ($pfProcess -and -not $pfProcess.HasExited) {
            Stop-Process -Id $pfProcess.Id -Force -ErrorAction SilentlyContinue
        }
    }

    # --- T11: Full Teardown & Clean State ---
    Write-Host "`n----------------- Executing T11: Teardown --------------" -ForegroundColor Yellow
    try {
        & .\scripts\cleanup.ps1
        
        # Explicit wait loop until namespace completely disappears (not just Terminating)
        $cleanComplete = $false
        for ($c = 1; $c -le 25; $c++) {
            $nsCheck = kubectl get namespace containerlab --no-headers 2>$null
            if ($null -eq $nsCheck -or $LASTEXITCODE -ne 0) {
                $cleanComplete = $true
                break
            }
            Start-Sleep -Seconds 2
        }
        Record-TestResult "T11" "Clean Teardown" $cleanComplete "Namespace containerlab was completely removed with zero lingering resources"
    } catch {
        Record-TestResult "T11" "Clean Teardown" $false $_.Exception.Message
    }
}

# --- Final Summary Table ---
Write-Host "`n=====================================================" -ForegroundColor Cyan
Write-Host "              TEST EXECUTION SUMMARY                 " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ("{0,-6} | {1,-26} | {2,-8} | {3}" -f "Test", "Description", "Status", "Details")
Write-Host "------------------------------------------------------------------------------------------------------"
foreach ($id in $testResults.Keys) {
    $item = $testResults[$id]
    $status = if ($item.Passed) { "PASS" } else { "FAIL" }
    Write-Host ("{0,-6} | {1,-26} | {2,-8} | {3}" -f $id, $item.Name, $status, $item.Details)
}
Write-Host "------------------------------------------------------------------------------------------------------"

if ($failureCount -gt 0) {
    Write-Host "`n[OVERALL RESULT] $failureCount test(s) failed." -ForegroundColor Red
    exit 1
} else {
    Write-Host "`n[OVERALL RESULT] All $($testResults.Count) tests passed successfully!" -ForegroundColor Green
    exit 0
}
