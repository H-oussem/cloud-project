# ContainerLab: Oral Defense & Technical Examination Cheat Sheet

This guide equips both students with precise, technically rigorous answers to questions frequently asked by professors during the final project evaluation.

---

### Q1: Why did you use an Nginx reverse proxy instead of having the browser call `http://api:5000` directly?
> **Answer**:
> In a containerized environment (Docker Compose or Kubernetes), service names like `api` or `postgres` are resolved exclusively through internal DNS (Docker embedded DNS or CoreDNS) inside the container network. 
> Because the React Single Page Application (SPA) executes inside the user's web browser on the host machine, the host operating system cannot resolve `http://api:5000`. 
> By having Nginx serve the static React bundle on port 80 and reverse-proxy all `/api/*` traffic internally to `http://api:5000/api/*`, the browser only needs to talk to the single frontend endpoint. This pattern ensures client requests remain same-origin, avoiding cross-origin (CORS) preflight issues without exposing the API and Database to the public network.

---

### Q2: What is the fundamental difference between a Virtual Machine (VM) and a Docker Container?
> **Answer**:
> - **Virtual Machines (Hardware-level Virtualization)**: Rely on a Hypervisor (Type 1 or Type 2) to emulate physical hardware (virtual CPU, RAM, disk, NIC). Each VM runs a full, independent Guest Operating System with its own kernel, consuming gigabytes of storage and several minutes to boot.
> - **Containers (OS-level Virtualization)**: Share the host operating system kernel. They isolate processes using Linux kernel primitives: **Namespaces** (isolates what a process can *see*, e.g., PID, Mount, Network, IPC, UTS) and **Control Groups / cgroups** (limits what a process can *use*, e.g., CPU, Memory limits). Containers boot in milliseconds and have negligible performance overhead.

---

### Q3: Why did you choose a Deployment + PVC instead of a StatefulSet for PostgreSQL?
> **Answer**:
> In our project, PostgreSQL runs as a single, non-clustered instance on a single-node cluster with no database replication, read replicas, or headless DNS routing requirements. 
> While `StatefulSet` provides stable, ordered network identities (`postgres-0`, `postgres-1`) and ordered scaling, a single instance only requires stable persistent storage. 
> We paired a Kubernetes `Deployment` (`replicas: 1`) with `strategy: { type: Recreate }` and a standalone `PersistentVolumeClaim`. The `Recreate` strategy guarantees that during an update or replacement, the existing Pod is fully terminated before a new Pod mounts the `ReadWriteOnce` volume, preventing multi-attach volume locking conflicts.

---

### Q4: Why did you separate Liveness and Readiness probes?
> **Answer**:
> - **Liveness Probe (`/api/health/live`)**: Answers: *"Is the Node.js process alive and responsive?"* If this fails, Kubernetes kills and restarts the container.
> - **Readiness Probe (`/api/health/ready`)**: Answers: *"Is the container ready to handle customer requests (i.e. is PostgreSQL connected)?"* If this fails, Kubernetes does NOT restart the container; instead, it removes the Pod from the Service's Endpoints pool, stopping incoming traffic until the database becomes healthy again.
> If we put database connectivity inside the liveness probe, a temporary database restart would cause kubelet to repeatedly kill and restart healthy API pods, triggering unnecessary rolling restarts across all backend replicas.

---

### Q5: Why did you configure `imagePullPolicy: Never` in Kubernetes?
> **Answer**:
> In Kubernetes, using the `latest` tag defaults `imagePullPolicy` to `Always`, causing kubelet to query external registries (Docker Hub) on every pod creation. Because our images are compiled and loaded directly into the local Minikube node (`minikube image load`), an external pull would fail with `ErrImagePull` or `ImagePullBackOff`. Setting strict semantic versioning (`v1.0.0`) and `imagePullPolicy: Never` instructs Kubernetes to strictly use the locally preloaded images.

---

### Q6: How does Docker Compose network segmentation protect the Database?
> **Answer**:
> In our `compose.yaml`, we created two distinct bridge networks: `frontend-net` and `backend-net`. The `frontend` container belongs only to `frontend-net`, the `postgres` container belongs only to `backend-net`, and the `api` container bridges both. 
> Because Docker bridge networks isolate ARP and IP traffic, the frontend container cannot establish a direct TCP connection or ping port 5432 on PostgreSQL. This enforces the architectural principle of least privilege and network DMZ boundaries.


---

### Q7: Why did you use `imagePullPolicy: Never` and NodePort in Minikube rather than Ingress or Cloud LoadBalancer?
> **Answer**:
> In local single-node Minikube, using `imagePullPolicy: Never` guarantees deterministic reproducibility without network dependencies: the locally built and versioned images (`v1.0.0`) are preloaded into Minikube's containerd cache via `minikube image load`, preventing Kubernetes from failing to pull from a non-existent public repository. 
> Similarly, `NodePort` provides a deterministic static port (`30080`) that works out of the box on Windows Minikube without requiring an external cloud controller manager (like AWS CCM) or provisioning an Elastic Load Balancer (ELB/ALB). In a production cloud setting (e.g. AWS EKS), we would transition to an AWS ALB Ingress Controller with TLS termination and `imagePullPolicy: IfNotPresent` tied to Amazon ECR.

---

### Q8: How are secrets handled, and how does this differ between your demo and production?
> **Answer**:
> In ContainerLab, non-sensitive configuration is stored in a Kubernetes `ConfigMap` (`PORT`, `DB_HOST`, `DB_NAME`), while credentials (`POSTGRES_USER`, `POSTGRES_PASSWORD`) are injected via a Kubernetes `Secret`. For our academic demonstration, native Secrets provide declarative decoupling. However, because native Kubernetes secrets are only base64-encoded, a production cloud deployment would utilize envelope encryption via AWS KMS and external secret synchronization via the **External Secrets Operator** integrated with AWS Secrets Manager or HashiCorp Vault.
