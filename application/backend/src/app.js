const express = require('express');
const cors = require('cors');
const os = require('os');
const db = require('./db');

const app = express();

app.use(cors());
app.use(express.json());

// Request logging middleware for observability
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`[HTTP] ${req.method} ${req.originalUrl} -> ${res.statusCode} (${duration}ms) [Pod: ${os.hostname()}]`);
  });
  next();
});

// Liveness probe endpoint - verifies the process is running and event loop is healthy
app.get('/api/health/live', (req, res) => {
  res.status(200).json({
    status: 'alive',
    podName: os.hostname(),
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// Readiness probe endpoint - verifies database connectivity before serving traffic
app.get('/api/health/ready', async (req, res) => {
  try {
    const isConnected = await db.testConnection();
    if (isConnected) {
      return res.status(200).json({
        status: 'ready',
        database: 'connected',
        podName: os.hostname(),
        timestamp: new Date().toISOString()
      });
    }
    return res.status(503).json({
      status: 'not_ready',
      database: 'disconnected',
      podName: os.hostname(),
      timestamp: new Date().toISOString()
    });
  } catch (err) {
    console.error('[Health] Readiness probe failed:', err.message);
    return res.status(503).json({
      status: 'not_ready',
      database: 'error',
      podName: os.hostname(),
      timestamp: new Date().toISOString()
    });
  }
});

// Instance metadata endpoint - used for scaling and load distribution demonstration
app.get('/api/instance', (req, res) => {
  res.status(200).json({
    podName: os.hostname(),
    platform: os.platform(),
    nodeVersion: process.version,
    memoryUsage: process.memoryUsage(),
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// Announcements CRUD endpoints
app.get('/api/announcements', async (req, res) => {
  try {
    const rawLimit = req.query.limit;
    let limit = 50; // default safe limit

    if (rawLimit !== undefined) {
      const parsed = parseInt(rawLimit, 10);
      if (!Number.isInteger(parsed) || parsed < 1) {
        return res.status(400).json({
          success: false,
          error: 'Query parameter "limit" must be a positive integer'
        });
      }
      limit = Math.min(parsed, 100);
    }

    const result = await db.query(
      'SELECT * FROM announcements ORDER BY created_at DESC LIMIT $1;',
      [limit]
    );
    res.status(200).json({
      success: true,
      count: result.rows.length,
      podName: os.hostname(),
      data: result.rows
    });
  } catch (err) {
    console.error('[API Error] Failed to fetch announcements:', err.message);
    res.status(500).json({
      success: false,
      error: 'Database query failed',
      podName: os.hostname()
    });
  }
});

app.post('/api/announcements', async (req, res) => {
  const rawTitle = req.body?.title;
  const rawContent = req.body?.content;
  const rawAuthor = req.body?.author;

  // Validation: existence and type check
  if (typeof rawTitle !== 'string' || typeof rawContent !== 'string') {
    return res.status(400).json({
      success: false,
      error: 'Title and content must be valid strings'
    });
  }

  const title = rawTitle.trim();
  const content = rawContent.trim();
  const author = typeof rawAuthor === 'string' && rawAuthor.trim() ? rawAuthor.trim() : 'Anonymous';

  // Validation: non-empty after trimming
  if (!title || !content) {
    return res.status(400).json({
      success: false,
      error: 'Title and content cannot be empty or whitespace only'
    });
  }

  // Validation: length limits
  if (title.length > 150) {
    return res.status(400).json({
      success: false,
      error: 'Title must not exceed 150 characters'
    });
  }

  if (content.length > 2000) {
    return res.status(400).json({
      success: false,
      error: 'Content must not exceed 2000 characters'
    });
  }

  if (author.length > 100) {
    return res.status(400).json({
      success: false,
      error: 'Author must not exceed 100 characters'
    });
  }

  try {
    const result = await db.query(
      'INSERT INTO announcements (title, content, author) VALUES ($1, $2, $3) RETURNING *;',
      [title, content, author]
    );
    res.status(201).json({
      success: true,
      message: 'Announcement created successfully',
      podName: os.hostname(),
      data: result.rows[0]
    });
  } catch (err) {
    console.error('[API Error] Failed to insert announcement:', err.message);
    res.status(500).json({
      success: false,
      error: 'Failed to create announcement',
      podName: os.hostname()
    });
  }
});

// Global 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found', path: req.originalUrl });
});

module.exports = app;
