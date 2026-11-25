const os = require('os');
const app = require('./app');
const db = require('./db');

const PORT = parseInt(process.env.PORT || '5000', 10);

const server = app.listen(PORT, '0.0.0.0', () => {
  console.log(`[ContainerLab API] Server listening on http://0.0.0.0:${PORT} [Pod: ${os.hostname()}]`);
});

// Graceful shutdown handler for Kubernetes SIGTERM / SIGINT signals
let isShuttingDown = false;

async function handleShutdown(signal) {
  if (isShuttingDown) return;
  isShuttingDown = true;
  console.log(`[Shutdown] Received ${signal}. Starting graceful shutdown...`);

  // Stop accepting new connections
  server.close(async () => {
    console.log('[Shutdown] HTTP server closed. Draining database pool...');
    try {
      await db.pool.end();
      console.log('[Shutdown] Database connections drained successfully.');
      process.exit(0);
    } catch (err) {
      console.error('[Shutdown] Error closing database pool:', err.message);
      process.exit(1);
    }
  });

  // Force shutdown if cleanup hangs past 10 seconds
  setTimeout(() => {
    console.error('[Shutdown] Graceful shutdown timed out. Forcing exit.');
    process.exit(1);
  }, 10000).unref();
}

process.on('SIGTERM', () => handleShutdown('SIGTERM'));
process.on('SIGINT', () => handleShutdown('SIGINT'));
