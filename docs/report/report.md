# ContainerLab: Technical Project Report
**Secure and Scalable Containerized Multi-Tier Application: From Docker Compose to Kubernetes**

- **Course**: Virtualisation et Cloud Computing
- **Project Topic**: Proposition 2 — Conteneurisation et Orchestration locale vs Cloud (Docker & Kubernetes / ECS)
- **Academic Year**: 2025–2026
- **Architecture**: React 19 + Nginx Reverse Proxy ➔ Node.js 24 LTS Express ➔ PostgreSQL 16 Alpine
- **Execution Environments**: Docker Compose v5.5 (Docker Engine 29.7) & Minikube v1.39 (kubectl client v1.36.1)

---

## 1. Executive Summary
Modern software engineering has witnessed a paradigm shift from heavy hardware-level virtualization (Virtual Machines managed by Type-1/Type-2 hypervisors) to lightweight, operating-system-level virtualization (Containers). 

**ContainerLab** designs, containerizes, orchestrates, verifies, and benchmarks a multi-tier web application across two progressive stages:
1. **Local Multi-Container Composition** via **Docker Compose** featuring segmented bridge networking, health-check synchronization, and named volume persistence.
2. **Cluster Orchestration** via **Kubernetes (Minikube)** featuring declarative manifests, isolated Namespaces, Deployments, ClusterIP/NodePort Services, ConfigMaps, Secrets, dynamic PersistentVolumeClaims, replica scaling, and self-healing.

---

## 2. Theoretical Foundations (Course Alignment)

### 2.1 Virtualization vs. Containerization
- **Virtual Machines**: Emulate hardware devices (CPU instructions, memory pages, virtual NICs). Each guest VM requires its own full OS kernel and system daemons, resulting in gigabytes of storage footprint, several minutes of boot latency, and hypervisor context-switching overhead.
- **Containers**: Run as isolated user-space processes directly on the host Linux kernel. They share the host kernel, eliminating guest OS overhead, booting in sub-second intervals, and consuming minimal RAM/CPU.

### 2.2 Linux Kernel Isolation Primitives
Containerization is enabled by three core Linux kernel mechanisms:
1. **Namespaces (Isolation)**: Determines what a container process can *see*.
   - `pid`: Process ID isolation (the containerized server sees itself as PID 1).
   - `net`: Network isolation (each container has its own virtual network interface `eth0`, routing table, and iptables rules).
   - `mnt`: Mount namespace (isolates directory trees and root filesystems).
   - `ipc`: Inter-Process Communication isolation.
   - `uts`: Hostname and domain name isolation.
2. **Control Groups / `cgroups` (Resource Governance)**: Determines what a container process can *use*.
   - In ContainerLab, Kubernetes manifests declare `resources.limits.cpu` (`250m` = 0.25 core) and `resources.limits.memory` (`256Mi`). The Linux kernel scheduler throttles CPU cycles and triggers OOM-killer if memory exceeds limits, preventing noisy-neighbor degradation.
3. **Union Filesystem (OverlayFS) & Copy-on-Write (CoW)**:
   - Images are composed of immutable, read-only layers.
   - Running containers create an ephemeral writable top layer. Modifications are written to the top layer (`copy-up`), ensuring base image integrity across multiple container replicas.

---

## 3. Application Architecture & Network Design

```
+---------------------------------------------------------------------------------+
|                                USER BROWSER                                     |
+---------------------------------------------------------------------------------+
                                       |
                                       | HTTP (NodePort :30080 or Compose :3000)
                                       v
+---------------------------------------------------------------------------------+
|                        TIER 1: FRONTEND (Web & Reverse Proxy)                   |
| - Technology: React 19 Single Page Application + Nginx stable-alpine-slim       |
| - Function: Serves compiled static assets & reverse-proxies /api/* requests     |
+---------------------------------------------------------------------------------+
                                       |
                                       | Internal DNS: http://api:5000/api/*
                                       v
+---------------------------------------------------------------------------------+
|                        TIER 2: BACKEND API (Application Logic)                  |
| - Technology: Node.js 24 LTS + Express REST API                                 |
| - Security: Non-root execution (`USER node`)                                    |
| - Key Endpoints:                                                                |
|   * GET  /api/health/live  -> Liveness probe (process responsive)               |
|   * GET  /api/health/ready -> Readiness probe (PostgreSQL connected)            |
|   * GET  /api/instance     -> Returns hostname/podName for replica tracking     |
|   * GET  /api/announcements-> Retrieves announcements                           |
|   * POST /api/announcements-> Inserts new announcement                          |
+---------------------------------------------------------------------------------+
                                       |
                                       | TCP 5432 (pg Connection Pool)
                                       v
+---------------------------------------------------------------------------------+
|                        TIER 3: DATABASE (Persistence Layer)                     |
| - Technology: PostgreSQL 16 Alpine + Baked init.sql Schema                      |
| - Storage: Minikube HostPath PersistentVolumeClaim (1Gi) / Named Volume         |
| - Lifecycle: Recreate Strategy (prevents multi-attach volume lockups)           |
+---------------------------------------------------------------------------------+
```

### The Nginx Reverse Proxy Advantage
Because client browsers execute JavaScript client-side on the host machine, they cannot resolve internal cluster DNS names (`http://api:5000`). By configuring Nginx inside the Frontend container to reverse-proxy `/api/*` to `http://api:5000/api/*`, ContainerLab achieves:
1. **Single Public Port**: Only port 80/3000 is exposed to users.
2. **Avoids Cross-Origin Issues**: All browser requests originate from the same host/port origin, eliminating CORS preflight overhead without exposing backend ports.
3. **Environment Agnostic**: Works identically under Docker Compose and Kubernetes.

---

## 4. Dockerfile Engineering & Image Optimization (3 pts)

ContainerLab provides three customized Dockerfiles:

### 4.1 Frontend Dockerfile (Multi-Stage Build)
- **Stage 1 (`builder`)**: Uses `node:24-alpine` to install dependencies and execute `npm run build`.
- **Stage 2 (`runner`)**: Uses `nginx:stable-alpine-slim`. Copies only the static `dist/` directory and custom `nginx.conf`.
- **Result**: Eliminates Node runtime, compilers, and source files from the delivery image, dropping image size from 80.92 MB (unoptimized baseline) down to 5.56 MB (multi-stage Nginx runner), achieving a measured 93.1% size reduction.

### 4.2 Backend Dockerfile (Minimal Non-Root Runner)
- Uses `node:24-alpine` base.
- Executes `npm ci --omit=dev` to prune devDependencies.
- Switches execution from `root` to unprivileged user `USER node`.
- Hardens container runtime against privilege escalation vulnerabilities.

### 4.3 Database Dockerfile (Customized Image)
- Extends official `postgres:16-alpine`.
- Copies `init.sql` into `/docker-entrypoint-initdb.d/10-init.sql`, automating database initialization on volume creation.

---

## 5. Local Orchestration: Docker Compose (3 pts)

Our `compose.yaml` establishes:
1. **Dual-Network Segmentation**:
   - `frontend-net`: Links `frontend` and `api`.
   - `backend-net`: Links `api` and `postgres`.
   - `postgres` is physically isolated from `frontend`, enforcing defense-in-depth.
2. **Dependency Sequencing**:
   - `api` uses `depends_on: { postgres: { condition: service_healthy } }`.
   - `frontend` uses `depends_on: { api: { condition: service_healthy } }`.
3. **Storage Persistence**:
   - PostgreSQL attaches named volume `postgres_data` mapped to `/var/lib/postgresql/data`.

---

## 6. Cluster Orchestration: Kubernetes on Minikube (5 pts)

Deployed declaratively in namespace `containerlab`:
- `00-namespace.yaml`: Logical administrative boundary (resource scoping, not a network security boundary).
- `01-configmap.yaml`: Environmental configurations (`PORT`, `DB_HOST`, `DB_PORT`, `DB_NAME`).
- `02-api-secret.yaml`: Base64 database credentials.
- `03-database-pvc.yaml`: 1Gi storage claim dynamically provisioned by Minikube's `standard` StorageClass.
- `04-database-deployment.yaml`: Single replica with `strategy: { type: Recreate }`.
- `05-database-service.yaml`: ClusterIP service on port 5432.
- `06-api-deployment.yaml`: 2 replicas, configured with distinct Liveness and Readiness probes.
- `07-api-service.yaml`: ClusterIP load-balancer on port 5000.
- `08-frontend-deployment.yaml`: Stateless web tier running Nginx and React.
- `09-frontend-service.yaml`: NodePort service exposing port 80 externally via port 30080.

---

## 7. Verification Matrix (T01 – T11 Automated Test Results)

All test procedures are automated via `scripts/run-tests.ps1` (exit-code assertions) and `npm test` (backend unit validation). The complete suite was executed on 20 November 2026:

> **Execution note**: The 7 Application Unit Tests passed. T01–T05 passed through the Compose-targeted run, and T06–T11 passed through the Kubernetes-targeted run. T11 deliberately removed the Compose stack and `containerlab` namespace.

| Test ID | Layer | Automated Procedure | Expected Target | Expected Observation | Verification |
|---|---|---|---|---|---|
| **Unit** | App | `npm test` (`node:test`) | Assert status codes, input trimming, schema bounds | 7/7 tests passed (whitespace, max length, invalid limit, 404, health) | ✅ **Executed** |
| **T01** | Build | `build-images.ps1` | Build 3 production images (`v1.0.0`) | `frontend:v1.0.0` (5.56 MB), `api:v1.0.0` (60.47 MB), `database:v1.0.0` (110.86 MB) | ✅ **Executed** |
| **T02** | Opt | `benchmark-images.ps1` | Quantify image reduction vs single-stage baselines | Frontend reduced by **93.1%** (80.92 MB → 5.56 MB) | ✅ **Executed** |
| **T03** | Compose | `run-compose.ps1` | Launch Compose stack; verify dependency health | All 3 services (`postgres`, `api`, `frontend`) reached `healthy` status | ✅ **Executed** |
| **T04** | Compose | REST POST to `/api/announcements` | Store announcement through Nginx proxy into PostgreSQL | HTTP 201 received; record ID 6 inserted successfully | ✅ **Executed** |
| **T05** | Compose | `docker compose restart postgres` | Named volume persistence across container restarts | Record survived the PostgreSQL container restart | ✅ **Executed** |
| **T06** | K8s | `deploy-k8s.ps1` | Apply manifests in namespace `containerlab` | PVC Bound; 4 Pods reached `Running` with Deployments Ready | ✅ **Executed** |
| **T07** | K8s | `GET /api/instance` (10 calls) | Traffic distribution across replicas via `kube-proxy` | 2 distinct API replicas received 10 requests (6 and 4) | ✅ **Executed** |
| **T08** | K8s | `kubectl scale deployment api --replicas=4` | Horizontal pod scaling | Replicas scaled 2 → 4 and all 4 reached `Ready` | ✅ **Executed** |
| **T09** | K8s | `kubectl delete pod <api-pod>` | Pod self-healing and service resilience | Replacement `api-85ff987687-c872t` reached `Ready` | ✅ **Executed** |
| **T10** | K8s | `kubectl delete pod <postgres-pod>` | PVC data preservation across pod replacement | Replacement Pod preserved the T10 announcement record | ✅ **Executed** |
| **T11** | Clean | `cleanup.ps1` | Teardown environment cleanly | Namespace `containerlab` completely removed | ✅ **Executed** |

**Legend**: ✅ Executed & confirmed on 20 November 2026

---

## 8. AWS Cloud Architecture Mapping

| Layer | Local Minikube | AWS Enterprise Production Equivalent |
|---|---|---|
| **Cluster Management** | Minikube Single-Node | **Amazon EKS (Elastic Kubernetes Service)** |
| **Traffic Ingress** | NodePort (30080) | **AWS Application Load Balancer (ALB)** |
| **Compute Execution** | Docker Engine Node | **EKS Managed Node Groups (Auto Scaling Group)** |
| **Persistent Storage** | HostPath dynamic StorageClass | **Amazon EBS (`gp3`) via CSI Driver** |
| **Database Tier** | In-Cluster PostgreSQL Deployment | **Amazon RDS for PostgreSQL (Multi-AZ Managed)** |
| **Image Distribution** | Minikube internal image cache | **Amazon Elastic Container Registry (ECR)** |

---

## 9. Conclusion
ContainerLab successfully addresses every requirement of Proposition 2. Through careful architectural decisions—such as Nginx reverse proxying, dual-network segmentation, and decoupled liveness/readiness probes—the project achieves high reliability, verifiable persistence, and reproducibility.
