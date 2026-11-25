-- ContainerLab Database Initialization Script
-- Executed on initial container/volume startup

CREATE TABLE IF NOT EXISTS announcements (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(100) DEFAULT 'System',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed initial announcements to verify data loading on first start
INSERT INTO announcements (title, content, author) VALUES
    ('Welcome to ContainerLab', 'Multi-tier containerized architecture initialized across Docker and Kubernetes.', 'System Admin'),
    ('Persistence Validation', 'This record was populated via init.sql and validates persistent storage across container lifecycles.', 'DevOps Team');
