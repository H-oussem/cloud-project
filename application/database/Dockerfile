# ContainerLab - Database Dockerfile
# Custom thin PostgreSQL image with baked initialization script
FROM postgres:16-alpine

# Copy database initialization SQL into the official PostgreSQL entrypoint directory
# Scripts in this directory run alphabetically when the database cluster is first created
COPY init.sql /docker-entrypoint-initdb.d/10-init.sql

# Expose default PostgreSQL port
EXPOSE 5432
