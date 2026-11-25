# ContainerLab - Backend API Optimized Dockerfile
# Stage 1: Dependency resolution and pruning
FROM node:24-alpine AS dependencies
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force

# Stage 2: Minimal non-root production runner
FROM node:24-alpine AS runner
WORKDIR /app

# Ensure production environment
ENV NODE_ENV=production
ENV PORT=5000

# Copy only production dependencies from builder stage
COPY --from=dependencies /app/node_modules ./node_modules
COPY package*.json ./
COPY src ./src

# Run as non-root user 'node' for container security
USER node

EXPOSE 5000

# Container healthcheck for standalone container runtime observability
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:5000/api/health/live || exit 1

CMD ["node", "src/server.js"]
