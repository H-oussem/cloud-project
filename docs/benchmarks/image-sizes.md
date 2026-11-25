# Docker Image Optimization Benchmarks (Test T02)
*Automated execution timestamp: 2026-11-20 22:02:39*

| Component | Unoptimized Baseline | Optimized Multi-Stage | Size Saved | Reduction % |
|---|---|---|---|---|
| **Backend API (Node.js)** | 61.89 MB | 60.47 MB | -1.42 MB | **2.3%** |
| **Frontend Web (React+Nginx)** | 80.92 MB | 5.56 MB | -75.36 MB | **93.1%** |
| **Database (PostgreSQL)** | *N/A (Official base)* | 110.86 MB | - | - |

### Key Optimization Techniques Applied:
1. **Frontend**: Multi-stage build separates Vite build-time tools (Node.js runtime, compilers, TypeScript/Babel tools) from runtime delivery (Nginx stable-alpine-slim), serving strictly static HTML/CSS/JS.
2. **Backend**: Alpine runtime base, 
pm ci --omit=dev strips devDependencies, and runs as an unprivileged non-root user (USER node).
3. **Security**: Non-root execution reduces attack surface; stripped toolchains prevent compiler exploits inside production containers.
