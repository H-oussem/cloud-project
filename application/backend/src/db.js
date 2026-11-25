const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST || 'postgres',
  port: parseInt(process.env.DB_PORT || '5432', 10),
  database: process.env.DB_NAME || 'containerlab_db',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres123',
  max: 10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

pool.on('error', (err) => {
  console.error('[DB] Unexpected error on idle client:', err.message);
});

async function query(text, params) {
  return pool.query(text, params);
}

async function testConnection() {
  const result = await pool.query('SELECT 1 as test');
  return result.rows.length > 0;
}

module.exports = {
  pool,
  query,
  testConnection,
};
