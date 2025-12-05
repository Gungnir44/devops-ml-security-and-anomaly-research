import { useState, useEffect } from 'react'
import './Dashboard.css'

function Dashboard() {
  const [stats, setStats] = useState({
    totalUsers: 0,
    dataProcessed: 0,
    securityScans: 0,
    uptime: '0h',
  })

  useEffect(() => {
    // Fetch dashboard statistics
    Promise.all([
      fetch('/api/v1/users').then(r => r.json()),
      fetch('/python-api/v1/analytics/summary').then(r => r.json()),
    ])
      .then(([users, analytics]) => {
        setStats({
          totalUsers: users.users?.length || 0,
          dataProcessed: analytics.total_processed || 0,
          securityScans: 156, // Mock data
          uptime: '24h 35m',
        })
      })
      .catch(err => console.error('Error fetching stats:', err))
  }, [])

  return (
    <div className="Dashboard">
      <h2>System Overview</h2>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <h3>{stats.totalUsers}</h3>
            <p>Total Users</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>{stats.dataProcessed}</h3>
            <p>Data Points Processed</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔒</div>
          <div className="stat-content">
            <h3>{stats.securityScans}</h3>
            <p>Security Scans</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⏱️</div>
          <div className="stat-content">
            <h3>{stats.uptime}</h3>
            <p>System Uptime</p>
          </div>
        </div>
      </div>

      <div className="info-section">
        <h3>About This Project</h3>
        <p>
          This dashboard is part of a Master's degree research project on
          <strong> ML-Based Security Anomaly Detection for DevOps Pipelines</strong>.
        </p>
        <p>
          The system monitors CI/CD pipelines, infrastructure events, and security scans
          to detect anomalous behavior using machine learning models.
        </p>

        <div className="features">
          <h4>Key Features:</h4>
          <ul>
            <li>✅ Real-time monitoring of DevOps infrastructure</li>
            <li>✅ Comprehensive security scanning (15+ tools)</li>
            <li>✅ ML-based anomaly detection</li>
            <li>✅ Attack scenario simulation</li>
            <li>✅ Feature extraction from 210+ data points</li>
          </ul>
        </div>

        <div className="architecture">
          <h4>Architecture:</h4>
          <div className="arch-diagram">
            <div className="arch-layer">
              <strong>Frontend</strong>
              <p>React + Vite</p>
            </div>
            <div className="arch-arrow">→</div>
            <div className="arch-layer">
              <strong>Backend API</strong>
              <p>Node.js + Express</p>
            </div>
            <div className="arch-arrow">→</div>
            <div className="arch-layer">
              <strong>Data Service</strong>
              <p>Python + FastAPI</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
