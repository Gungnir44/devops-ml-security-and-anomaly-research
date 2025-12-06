import { useState } from 'react'
import './SecurityMetrics.css'

function SecurityMetrics() {
  const [metrics] = useState({
    secretScans: 245,
    containerScans: 189,
    sastScans: 312,
    dependencyScans: 156,
    totalFindings: 45,
    criticalFindings: 3,
    highFindings: 12,
    mediumFindings: 18,
    lowFindings: 12,
  })

  const scanTools = [
    { name: 'TruffleHog', category: 'Secret Scanning', status: 'active' },
    { name: 'Gitleaks', category: 'Secret Scanning', status: 'active' },
    { name: 'Trivy', category: 'Container', status: 'active' },
    { name: 'Grype', category: 'Container', status: 'active' },
    { name: 'Dockle', category: 'Container', status: 'active' },
    { name: 'CodeQL', category: 'SAST', status: 'active' },
    { name: 'Semgrep', category: 'SAST', status: 'active' },
    { name: 'Bandit', category: 'SAST', status: 'active' },
    { name: 'npm audit', category: 'Dependencies', status: 'active' },
    { name: 'pip-audit', category: 'Dependencies', status: 'active' },
    { name: 'Snyk', category: 'Dependencies', status: 'active' },
    { name: 'Checkov', category: 'IaC', status: 'active' },
    { name: 'tfsec', category: 'IaC', status: 'active' },
    { name: 'kubeaudit', category: 'Kubernetes', status: 'active' },
    { name: 'kubeval', category: 'Kubernetes', status: 'active' },
  ]

  return (
    <div className="SecurityMetrics">
      <h2>Security Scanning Metrics</h2>
      <p className="subtitle">Comprehensive Security Analysis Dashboard</p>

      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon critical">🔴</div>
          <div className="metric-content">
            <h3>{metrics.criticalFindings}</h3>
            <p>Critical Findings</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon high">🟠</div>
          <div className="metric-content">
            <h3>{metrics.highFindings}</h3>
            <p>High Severity</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon medium">🟡</div>
          <div className="metric-content">
            <h3>{metrics.mediumFindings}</h3>
            <p>Medium Severity</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon low">🟢</div>
          <div className="metric-content">
            <h3>{metrics.lowFindings}</h3>
            <p>Low Severity</p>
          </div>
        </div>
      </div>

      <div className="scan-stats">
        <h3>Total Scans Performed</h3>
        <div className="scan-grid">
          <div className="scan-stat">
            <h4>{metrics.secretScans}</h4>
            <p>Secret Scans</p>
          </div>
          <div className="scan-stat">
            <h4>{metrics.containerScans}</h4>
            <p>Container Scans</p>
          </div>
          <div className="scan-stat">
            <h4>{metrics.sastScans}</h4>
            <p>SAST Scans</p>
          </div>
          <div className="scan-stat">
            <h4>{metrics.dependencyScans}</h4>
            <p>Dependency Scans</p>
          </div>
        </div>
      </div>

      <div className="tools-section">
        <h3>Active Security Tools ({scanTools.length})</h3>
        <table className="tools-table">
          <thead>
            <tr>
              <th>Tool</th>
              <th>Category</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {scanTools.map((tool, index) => (
              <tr key={index}>
                <td><strong>{tool.name}</strong></td>
                <td>
                  <span className="category-badge">{tool.category}</span>
                </td>
                <td>
                  <span className="status-badge active">✓ {tool.status}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="research-info">
        <h3>ML-Based Anomaly Detection</h3>
        <p>
          This system collects security scan data to train machine learning models
          for detecting anomalous behavior in DevOps pipelines.
        </p>
        <div className="ml-features">
          <h4>Feature Categories (210 total features):</h4>
          <ul>
            <li>✓ Security scan results (21 features)</li>
            <li>✓ CI/CD pipeline metrics (35 features)</li>
            <li>✓ Infrastructure metrics (40 features)</li>
            <li>✓ Access patterns (28 features)</li>
            <li>✓ Code changes (25 features)</li>
            <li>✓ Deployment events (22 features)</li>
            <li>✓ Container activities (24 features)</li>
            <li>✓ Network traffic (15 features)</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default SecurityMetrics
