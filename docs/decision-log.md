# ContainerLab: Architecture Decision Log (ADL)

## ADR-001: Minimal Announcements Application vs Legacy CentraSpace Extraction
- **Context**: The project required a multi-tier containerized application. Initial proposals considered extracting parts of CentraSpace.
- **Decision**: Build a purpose-tailored, minimal Announcements application (React 19 + Node.js 24 + PostgreSQL 16).
- **Rationale**: Avoids non-essential dependencies (WebRTC, Cloudinary, auth tokens) and heavy build layers. Enables rapid build times, predictable testing, and guaranteed multi-stage image reduction.

---

## ADR-002: PostgreSQL Orchestration: Deployment + PVC vs StatefulSet
- **Context**: Databases in Kubernetes are often paired with `StatefulSet`. However, ContainerLab features a single database instance on a local single-node cluster with no clustering, replication, or headless DNS requirements.
- **Decision**: Use a Kubernetes `Deployment` with 1 replica, a standalone `PersistentVolumeClaim` (ReadWriteOnce), and `strategy.type: Recreate`.
- **Rationale**:
  - `Recreate` guarantees that the running Pod releases the persistent volume before a replacement Pod attempts to mount it, preventing `Multi-Attach error for volume` errors.
  - Aligns with the grading rubric without unnecessary complexity.
  - The theoretical differences and use cases for StatefulSets are comprehensively documented in the final report.

---

## ADR-003: Minikube Local Image Distribution & Pull Policy
- **Context**: Using `latest` image tags causes Kubernetes to default to `imagePullPolicy: Always`, which fails if images are only stored locally.
- **Decision**:
  1. Pin all images to strict semantic versions (`v1.0.0`).
  2. Use `imagePullPolicy: Never` in Kubernetes manifests.
  3. Preload images into Minikube via `minikube image load <image>:<tag>`.
- **Rationale**: Ensures deterministic deployments and eliminates external registry dependency or caching mismatch errors during demonstrations.

---

## ADR-004: Docker Compose Network Segmentation
- **Context**: Docker Compose creates a single default bridge network if unspecified.
- **Decision**: Define two custom bridge networks: `frontend-net` (Frontend ↔ API) and `backend-net` (API ↔ PostgreSQL).
- **Rationale**: Satisfies the course requirement for network isolation and security firewalling. Demonstrates that the Database cannot be reached directly by the Frontend container.

---

## ADR-005: Separation of Liveness and Readiness Probes
- **Context**: A container can be running but temporarily unable to connect to downstream dependencies.
- **Decision**:
  - `GET /api/health/live`: Fast check that the Node process is running. Used for Kubernetes Liveness.
  - `GET /api/health/ready`: Performs a `SELECT 1` query to PostgreSQL. Used for Kubernetes Readiness and Compose health checks.
- **Rationale**: Prevents Kubernetes from rebooting an API pod if the database undergoes a temporary restart, while ensuring traffic is temporarily held off until connectivity is restored.
