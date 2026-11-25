const { test, describe, before, after } = require('node:test');
const assert = require('node:assert');
const http = require('node:http');
const app = require('../src/app');

describe('ContainerLab Backend API Tests', () => {
  let server;
  let baseUrl;

  before((t, done) => {
    // Start server on random available port
    server = http.createServer(app).listen(0, '127.0.0.1', () => {
      const port = server.address().port;
      baseUrl = `http://127.0.0.1:${port}`;
      done();
    });
  });

  after((t, done) => {
    server.close(done);
  });

  test('GET /api/health/live returns 200 with alive status', async () => {
    const res = await fetch(`${baseUrl}/api/health/live`);
    const data = await res.json();
    assert.strictEqual(res.status, 200);
    assert.strictEqual(data.status, 'alive');
    assert.ok(typeof data.podName === 'string');
    assert.ok(typeof data.uptime === 'number');
  });

  test('GET /api/instance returns 200 with instance metadata', async () => {
    const res = await fetch(`${baseUrl}/api/instance`);
    const data = await res.json();
    assert.strictEqual(res.status, 200);
    assert.ok(typeof data.podName === 'string');
    assert.ok(typeof data.platform === 'string');
    assert.ok(typeof data.uptime === 'number');
  });

  test('POST /api/announcements returns 400 if fields are missing', async () => {
    const res = await fetch(`${baseUrl}/api/announcements`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: 'Only title' })
    });
    const data = await res.json();
    assert.strictEqual(res.status, 400);
    assert.strictEqual(data.success, false);
    assert.ok(data.error.includes('valid strings'));
  });

  test('POST /api/announcements returns 400 for whitespace-only strings', async () => {
    const res = await fetch(`${baseUrl}/api/announcements`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: '   ', content: '   ' })
    });
    const data = await res.json();
    assert.strictEqual(res.status, 400);
    assert.strictEqual(data.success, false);
    assert.ok(data.error.includes('whitespace only'));
  });

  test('POST /api/announcements returns 400 when title exceeds 150 chars', async () => {
    const longTitle = 'a'.repeat(151);
    const res = await fetch(`${baseUrl}/api/announcements`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: longTitle, content: 'Valid content' })
    });
    const data = await res.json();
    assert.strictEqual(res.status, 400);
    assert.strictEqual(data.success, false);
    assert.ok(data.error.includes('150 characters'));
  });

  test('GET /api/announcements with invalid limit returns 400', async () => {
    const res = await fetch(`${baseUrl}/api/announcements?limit=abc`);
    const data = await res.json();
    assert.strictEqual(res.status, 400);
    assert.strictEqual(data.success, false);
    assert.ok(data.error.includes('positive integer'));
  });

  test('GET /unknown-route returns 404', async () => {
    const res = await fetch(`${baseUrl}/api/nonexistent`);
    const data = await res.json();
    assert.strictEqual(res.status, 404);
    assert.strictEqual(data.error, 'Endpoint not found');
  });
});
