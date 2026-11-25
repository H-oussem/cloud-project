# ContainerLab - Frontend Optimized Multi-Stage Dockerfile
# Stage 1: Build the React Single Page Application
FROM node:24-alpine AS builder
WORKDIR /app

# Copy dependency manifests and install dependencies
COPY package*.json ./
RUN npm ci

# Copy application source and build production bundle
COPY . .
RUN npm run build

# Stage 2: Production Nginx runtime server
FROM nginx:stable-alpine-slim AS runner

# Copy custom reverse-proxy and SPA routing configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy compiled static assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

# Health check for Nginx web server
HEALTHCHECK --interval=20s --timeout=3s --retries=3 \
  CMD wget -qO- http://127.0.0.1:80/healthz || exit 1

CMD ["nginx", "-g", "daemon off;"]
