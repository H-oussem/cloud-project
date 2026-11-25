import React, { useState, useEffect } from 'react';

export default function App() {
  const [announcements, setAnnouncements] = useState([]);
  const [instance, setInstance] = useState(null);
  const [apiLive, setApiLive] = useState(null); // null = loading, true, false
  const [dbReady, setDbReady] = useState(null); // null = loading, true, false
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [testResults, setTestResults] = useState([]);
  const [testingDistribution, setTestingDistribution] = useState(false);
  const [copied, setCopied] = useState(false);

  // Form state
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [content, setContent] = useState('');
  const [notification, setNotification] = useState(null);

  // Fetch instance info (pod identity)
  const fetchInstance = async () => {
    try {
      const res = await fetch('/api/instance');
      if (res.ok) {
        const data = await res.json();
        setInstance(data);
      } else {
        setInstance(null);
      }
    } catch (err) {
      console.error('Error fetching instance:', err);
      setInstance(null);
    }
  };

  // Fetch API liveness & readiness probes
  const fetchHealth = async () => {
    // Check API Liveness
    try {
      const liveRes = await fetch('/api/health/live');
      setApiLive(liveRes.ok);
    } catch (err) {
      setApiLive(false);
    }

    // Check Database Readiness
    try {
      const readyRes = await fetch('/api/health/ready');
      setDbReady(readyRes.ok);
    } catch (err) {
      setDbReady(false);
    }
  };

  // Fetch announcements
  const fetchAnnouncements = async () => {
    try {
      const res = await fetch('/api/announcements');
      if (res.ok) {
        const json = await res.json();
        setAnnouncements(json.data || []);
      }
    } catch (err) {
      console.error('Error fetching announcements:', err);
    } finally {
      setLoading(false);
    }
  };

  const refreshAll = () => {
    fetchInstance();
    fetchHealth();
    fetchAnnouncements();
  };

  useEffect(() => {
    refreshAll();
    const interval = setInterval(refreshAll, 6000);
    return () => clearInterval(interval);
  }, []);

  const handleCopyPod = () => {
    if (instance?.podName) {
      navigator.clipboard.writeText(instance.podName);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Handle new announcement submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmedTitle = title.trim();
    const trimmedContent = content.trim();

    if (!trimmedTitle || !trimmedContent) {
      setNotification({ type: 'error', text: 'Title and content cannot be empty.' });
      return;
    }

    setSubmitting(true);
    setNotification(null);
    try {
      const res = await fetch('/api/announcements', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: trimmedTitle, content: trimmedContent, author }),
      });
      const data = await res.json();
      if (res.ok) {
        setTitle('');
        setAuthor('');
        setContent('');
        setNotification({
          type: 'success',
          text: `Announcement stored in PostgreSQL by replica: ${data.podName}`,
        });
        fetchAnnouncements();
        fetchInstance();
      } else {
        setNotification({ type: 'error', text: data.error || 'Failed to submit announcement' });
      }
    } catch (err) {
      setNotification({ type: 'error', text: 'Network connection failed' });
    } finally {
      setSubmitting(false);
    }
  };

  // Rapidly test traffic distribution across backend replicas
  const runDistributionTest = async () => {
    setTestingDistribution(true);
    const results = [];
    for (let i = 1; i <= 6; i++) {
      try {
        const res = await fetch(`/api/instance?t=${Date.now()}-${i}`);
        if (res.ok) {
          const data = await res.json();
          results.push({ reqId: i, pod: data.podName, time: new Date().toLocaleTimeString() });
        } else {
          results.push({ reqId: i, pod: `Error (${res.status})`, time: new Date().toLocaleTimeString() });
        }
      } catch (err) {
        results.push({ reqId: i, pod: 'Unreachable', time: new Date().toLocaleTimeString() });
      }
    }
    setTestResults(results);
    setTestingDistribution(false);
  };

  // Determine overall cluster health
  const getOverallStatus = () => {
    if (apiLive === null || dbReady === null) {
      return { label: 'Checking Status...', class: 'pill-blue' };
    }
    if (apiLive && dbReady) {
      return { label: 'All Systems Nominal', class: 'pill-green' };
    }
    if (apiLive && !dbReady) {
      return { label: 'Degraded: DB Disconnected', class: 'pill-amber' };
    }
    return { label: 'Offline: API Unreachable', class: 'pill-red' };
  };

  const overallStatus = getOverallStatus();

  return (
    <div className="app-wrapper">
      {/* Top Navbar */}
      <nav className="navbar">
        <div className="nav-container">
          <div className="brand-wrapper">
            <div className="brand-logo">CL</div>
            <div className="brand-details">
              <h1>ContainerLab</h1>
              <p>Multi-Tier Cloud Architecture &amp; Orchestration</p>
            </div>
          </div>
          <div className="nav-badges">
            <span className="pill-badge pill-blue">Docker Compose</span>
            <span className="pill-badge pill-blue">Kubernetes</span>
            <span className={`pill-badge ${apiLive === false ? 'pill-red' : 'pill-green'}`}>
              Nginx Proxy ({apiLive === false ? 'Degraded' : 'Active'})
            </span>
            <span className={`pill-badge ${dbReady === true ? 'pill-green' : dbReady === false ? 'pill-red' : 'pill-blue'}`}>
              PostgreSQL 16 ({dbReady === true ? 'Ready' : dbReady === false ? 'Down' : 'Checking...'})
            </span>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="main-container">
        {/* Hero Banner */}
        <section className="hero-banner">
          <div className="hero-text">
            <h2>Multi-Tier Infrastructure Dashboard</h2>
            <p>
              Observability console for ContainerLab. Traffic enters via Nginx reverse proxy, routes
              to stateless Express API replicas, and persists to a dedicated PostgreSQL volume.
            </p>
          </div>
          <div className="hero-actions">
            <button className="btn btn-secondary" onClick={refreshAll}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/>
              </svg>
              Refresh Stats
            </button>
          </div>
        </section>

        {/* Status Alert if Degraded or Offline */}
        {(apiLive === false || dbReady === false) && (
          <div className={`alert ${apiLive === false ? 'alert-danger' : 'alert-warning'}`} style={{ marginBottom: '1.5rem' }}>
            {apiLive === false
              ? 'Warning: Backend API is currently unreachable. Requests to /api are failing.'
              : 'Warning: Backend API is alive, but PostgreSQL connection is unavailable. Database queries will fail.'}
          </div>
        )}

        {/* 3 Metrics Cards */}
        <div className="grid-3">
          {/* Card 1: Pod Identity */}
          <div className="card">
            <div className="card-header">
              <span className="card-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563eb" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="2" y="2" width="20" height="8" rx="2" ry="2"/>
                  <rect x="2" y="14" width="20" height="8" rx="2" ry="2"/>
                  <line x1="6" y1="6" x2="6.01" y2="6"/>
                  <line x1="6" y1="18" x2="6.01" y2="18"/>
                </svg>
                Serving Replica
              </span>
              <div
                className="pulse-indicator"
                style={{ background: apiLive ? 'var(--success-green)' : '#dc2626' }}
                title={apiLive ? 'Connected' : 'Disconnected'}
              ></div>
            </div>
            <div className="pod-display-box">
              <span className="pod-code">{instance ? instance.podName : (apiLive === false ? 'Unreachable' : 'Connecting...')}</span>
              <button
                className="btn btn-secondary btn-sm"
                onClick={handleCopyPod}
                disabled={!instance?.podName}
                title="Copy Hostname"
              >
                {copied ? 'Copied!' : 'Copy'}
              </button>
            </div>
            <div className="info-rows">
              <div className="info-row">
                <span className="info-label">Runtime Engine</span>
                <span className="info-value">{instance ? `Node ${instance.nodeVersion}` : 'N/A'}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Uptime</span>
                <span className="info-value">{instance ? `${Math.floor(instance.uptime)}s` : 'N/A'}</span>
              </div>
            </div>
          </div>

          {/* Card 2: Cluster Health */}
          <div className="card">
            <div className="card-header">
              <span className="card-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#059669" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                </svg>
                Tier Health Status
              </span>
              <span className={`pill-badge ${overallStatus.class}`}>{overallStatus.label}</span>
            </div>
            <div className="info-rows">
              <div className="info-row">
                <span className="info-label">Web Server (Nginx)</span>
                <span className={`pill-badge ${apiLive === false ? 'pill-amber' : 'pill-green'}`}>
                  {apiLive === false ? 'Port 80 • Reverse Proxy Degraded (API Down)' : 'Port 80 • Reverse Proxy Active'}
                </span>
              </div>
              <div className="info-row">
                <span className="info-label">API Liveness Probe</span>
                <span className={`pill-badge ${apiLive === true ? 'pill-green' : apiLive === false ? 'pill-red' : 'pill-blue'}`}>
                  {apiLive === true ? 'Healthy • Port 5000' : apiLive === false ? 'Unreachable • Port 5000' : 'Checking...'}
                </span>
              </div>
              <div className="info-row">
                <span className="info-label">PostgreSQL Database</span>
                <span className={`pill-badge ${dbReady === true ? 'pill-green' : dbReady === false ? 'pill-red' : 'pill-blue'}`}>
                  {dbReady === true ? 'Connected • Port 5432' : dbReady === false ? 'Disconnected' : 'Checking...'}
                </span>
              </div>
            </div>
          </div>

          {/* Card 3: Traffic Distribution Test */}
          <div className="card">
            <div className="card-header">
              <span className="card-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4f46e5" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
                </svg>
                Load Distribution
              </span>
              <button
                className="btn btn-primary btn-sm"
                onClick={runDistributionTest}
                disabled={testingDistribution || !apiLive}
              >
                {testingDistribution ? 'Pinging...' : 'Send 6 Calls'}
              </button>
            </div>
            {testResults.length > 0 ? (
              <div className="distribution-history">
                {testResults.map((r) => (
                  <div key={r.reqId} className="distribution-item">
                    <span className="req-badge">Request #{r.reqId}</span>
                    <span className="pod-tag">{r.pod}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ fontSize: '0.85rem', color: 'var(--text-soft)', padding: '0.5rem 0' }}>
                Simulate rapid independent connections to observe traffic balancing across available backend instances.
              </p>
            )}
          </div>
        </div>

        {/* Content Section: Form & Announcements */}
        <div className="grid-content">
          {/* Create Announcement Form */}
          <section className="card">
            <div className="card-header">
              <span className="card-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563eb" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 20h9"/>
                  <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
                </svg>
                Post Announcement
              </span>
            </div>

            {notification && (
              <div className={`alert ${notification.type === 'success' ? 'alert-success' : 'alert-danger'}`}>
                {notification.text}
              </div>
            )}

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">Subject Title (Max 150 chars)</label>
                <input
                  className="form-input"
                  placeholder="e.g. Scaling Replicas to 4"
                  maxLength={150}
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Author / Role (Max 100 chars)</label>
                <input
                  className="form-input"
                  placeholder="e.g. Student DevOps"
                  maxLength={100}
                  value={author}
                  onChange={(e) => setAuthor(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Message Content (Max 2000 chars)</label>
                <textarea
                  className="form-input"
                  placeholder="Describe deployment milestones or tests..."
                  maxLength={2000}
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  required
                />
              </div>

              <button className="btn btn-primary" type="submit" disabled={submitting || !dbReady} style={{ width: '100%' }}>
                {submitting ? 'Persisting to Database...' : dbReady === false ? 'Database Offline' : 'Submit to Database'}
              </button>
            </form>
          </section>

          {/* Persisted Announcements List */}
          <section className="card">
            <div className="card-header">
              <span className="card-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563eb" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                  <polyline points="10 9 9 9 8 9"/>
                </svg>
                Persisted Announcements ({announcements.length})
              </span>
              <button className="btn btn-secondary btn-sm" onClick={fetchAnnouncements}>
                Refresh Feed
              </button>
            </div>

            {loading ? (
              <p style={{ color: 'var(--text-soft)', fontSize: '0.9rem' }}>Loading records from PostgreSQL...</p>
            ) : announcements.length === 0 ? (
              <p style={{ color: 'var(--text-soft)', fontSize: '0.9rem' }}>No announcements in database.</p>
            ) : (
              <div className="announcements-feed">
                {announcements.map((item) => (
                  <article key={item.id} className="announcement-card">
                    <div className="announcement-top">
                      <div className="announcement-title-box">
                        <span className="id-tag">#{item.id}</span>
                        <h3 className="announcement-title">{item.title}</h3>
                      </div>
                      <span className="announcement-meta">
                        {new Date(item.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <p className="announcement-body">{item.content}</p>
                    <div style={{ marginTop: '0.65rem', fontSize: '0.75rem', color: 'var(--text-soft)' }}>
                      Author: <strong>{item.author || 'Anonymous'}</strong>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer>
        ContainerLab • Virtualisation et Cloud Computing • Proposition 2
      </footer>
    </div>
  );
}
