# ContainerLab: Technical Architecture Specification

## 1. System Overview
**ContainerLab** is a containerized 3-tier web application designed to demonstrate the full progression from localized container development (**Docker** & **Docker Compose**) to declarative cluster orchestration (**Kubernetes / Minikube**).

The application consists of:
1. **Frontend Tier (Web & Reverse Proxy)**: React 19 Single Page Application served by Nginx `stable-alpine-slim`.
2. **Backend API Tier (Application Logic)**: Node.js 24 LTS Express REST API.
3. **Database Tier (Persistence Layer)**: PostgreSQL 16 Alpine with custom schema initialization.

---

## 2. Network Topology & Traffic Flow

### 2.1 The Nginx Reverse Proxy Pattern
In traditional container setups, client browsers often fail to connect to backend microservices due to internal hostname resolution failures (`http://api:5000` is unknown to the host machine). 

ContainerLab solves this using Nginx as an internal reverse proxy:
```
[User Browser]
      │
      │ HTTP Request (e.g. /api/announcements)
      ▼
[Nginx Web Server on Frontend Container] (:80 / NodePort 30080)
      │
      │ Internal Reverse Proxy: proxy_pass http://api:5000/api/
      ▼
[API Service / Backend Pods] (:5000)
      │
      │ TCP Pool Query: pg.Pool (port 5432)
      ▼
[PostgreSQL Database] (:5432)
```

**Benefits**:
- **Zero CORS issues**: The browser communicates strictly with the frontend origin.
- **Single Entry Point**: Backend and Database ports are not exposed directly to the outside world.
- **Identical Behavior**: Works natively in Docker Compose (`http://api:5000`) and Kubernetes (`http://api:5000`).

---

## 3. Storage Architecture

### 3.1 Docker Compose
- Uses a named volume `postgres_data` mapped to `/var/lib/postgresql/data`.
- Persists data across `docker compose restart`, `docker compose down`, and container destruction.

### 3.2 Kubernetes
- Uses a dedicated `PersistentVolumeClaim` (`postgres-pvc`) requesting 1Gi from Minikube's `standard` StorageClass.
- Configured with `accessModes: [ReadWriteOnce]`.
- Mounted by the PostgreSQL Deployment configured with `strategy: { type: Recreate }`.
- When the PostgreSQL Pod is deleted (e.g. during failure testing), the Deployment controller terminates the old pod and spawns a replacement pod that immediately re-attaches the existing PersistentVolume.

---

## 4. Workload Characteristics

| Tier | Workload Type | Replicas | Probes | Resource Governance |
|---|---|---|---|---|
| **Frontend** | Stateless Deployment | 1 | Liveness & Readiness (`/healthz`) | CPU: 50m-150m, Mem: 64Mi-128Mi |
| **API** | Stateless Deployment | 2 (scalable to 4) | Liveness (`/api/health/live`), Readiness (`/api/health/ready`) | CPU: 100m-250m, Mem: 128Mi-256Mi |
| **Database** | Stateful Deployment | 1 | Liveness & Readiness (`pg_isready`) | CPU: 100m-250m, Mem: 128Mi-256Mi |


---

## 5. Production Readiness Gap Analysis (Academic vs Production)

To ensure academic clarity and defense readiness, the table below documents the intentional architectural distinctions between the local Minikube demonstration environment and a production-grade enterprise deployment (such as AWS EKS or GCP GKE).

| Dimension | ContainerLab Academic Architecture (Minikube) | Production Cloud Architecture (AWS EKS / GKE) | Justification / Trade-Off |
| :--- | :--- | :--- | :--- |
| **External Ingress** | Kubernetes `NodePort` Service (`30080`) | Cloud Load Balancer (AWS ALB / NLB) + Kubernetes `Ingress` Controller (Nginx Ingress / Traefik) with TLS termination. | NodePort provides deterministic, zero-dependency external access without requiring cloud cloud-controller-managers or external IP provisioning. |
| **Secrets Management** | Native Kubernetes `Secret` (`type: Opaque`, using base64 encoded values). | External Secrets Operator integrated with AWS Secrets Manager, HashiCorp Vault, or Azure Key Vault, utilizing KMS envelope encryption. | Academic scope avoids external cloud credential dependencies while teaching standard Kubernetes Secret and ConfigMap decoupling patterns. |
| **Image Pulling** | `imagePullPolicy: Never` with local image preloading via `minikube image load`. | `imagePullPolicy: IfNotPresent` pulling immutable digest tags from a private container registry (Amazon ECR, Harbor). | Prevents external network dependency during oral defense and prevents Minikube from attempting remote pulls for locally authored images. |
| **Autoscaling** | Manual imperative scaling (`kubectl scale --replicas=4`). | Horizontal Pod Autoscaler (`HPA`) reacting to CPU/memory metrics via `metrics-server`, combined with Karpenter or Cluster Autoscaler for node scaling. | Manual scaling allows deterministic demonstration during live examination without waiting for metrics aggregation intervals. |
| **Network Security** | Namespace-level isolation without `NetworkPolicy` controllers. | Calico / Cilium CNI enforcing strict L4/L7 `NetworkPolicy` (e.g., blocking direct frontend-to-database ingress). | Standard Minikube standard CNI omits complex network plugins to ensure reproducible single-node execution. |
| **Database Resilience** | Single-replica PostgreSQL Deployment with `strategy: Recreate` and single PVC. | Cloud-managed RDS Multi-AZ or cloud-native Kubernetes database operator (CloudNativePG / Zalando Postgres Operator) with streaming replication. | Eliminates unnecessary database clustering complexity while completely satisfying the syllabus requirements for container persistent storage. |
