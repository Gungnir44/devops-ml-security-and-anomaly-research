import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import './App.css'
import Dashboard from './components/Dashboard'
import Users from './components/Users'
import DataProcessing from './components/DataProcessing'
import SecurityMetrics from './components/SecurityMetrics'

function App() {
  const [health, setHealth] = useState({ backend: null, python: null })

  useEffect(() => {
    // Check backend health
    fetch('/api/v1/users')
      .then(() => setHealth(prev => ({ ...prev, backend: 'healthy' })))
      .catch(() => setHealth(prev => ({ ...prev, backend: 'unhealthy' })))

    // Check Python service health
    fetch('/python-api/v1/analytics/summary')
      .then(() => setHealth(prev => ({ ...prev, python: 'healthy' })))
      .catch(() => setHealth(prev => ({ ...prev, python: 'unhealthy' })))
  }, [])

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <div className="container">
            <h1>🔒 DevOps Security Research Dashboard</h1>
            <p className="subtitle">ML-Based Anomaly Detection Platform</p>
          </div>
        </header>

        <nav className="App-nav">
          <div className="container">
            <ul>
              <li>
                <Link to="/">Dashboard</Link>
              </li>
              <li>
                <Link to="/users">Users API</Link>
              </li>
              <li>
                <Link to="/processing">Data Processing</Link>
              </li>
              <li>
                <Link to="/security">Security Metrics</Link>
              </li>
            </ul>
            <div className="health-indicators">
              <span className={`indicator ${health.backend}`}>
                Backend: {health.backend || 'checking...'}
              </span>
              <span className={`indicator ${health.python}`}>
                Python: {health.python || 'checking...'}
              </span>
            </div>
          </div>
        </nav>

        <main className="App-main">
          <div className="container">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/users" element={<Users />} />
              <Route path="/processing" element={<DataProcessing />} />
              <Route path="/security" element={<SecurityMetrics />} />
            </Routes>
          </div>
        </main>

        <footer className="App-footer">
          <div className="container">
            <p>
              &copy; 2025 DevOps Security Research Project | Master&apos;s
              Thesis
            </p>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App
