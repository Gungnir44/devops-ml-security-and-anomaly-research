import { useState } from 'react'
import './DataProcessing.css'

function DataProcessing() {
  const [inputValue, setInputValue] = useState('10')
  const [result, setResult] = useState(null)
  const [batchData, setBatchData] = useState('5, 10, 15, 20')
  const [batchResults, setBatchResults] = useState([])
  const [loading, setLoading] = useState(false)

  const processSingle = async () => {
    setLoading(true)
    try {
      const response = await fetch('/python-api/v1/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value: parseFloat(inputValue) }),
      })
      const data = await response.json()
      setResult(data)
    } catch (err) {
      console.error('Error processing data:', err)
      setResult({ error: 'Failed to connect to Python service on port 8000' })
    } finally {
      setLoading(false)
    }
  }

  const processBatch = async () => {
    setLoading(true)
    try {
      const values = batchData.split(',').map(v => ({
        value: parseFloat(v.trim())
      }))

      const response = await fetch('/python-api/v1/batch-process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values),
      })
      const data = await response.json()
      setBatchResults(data)
    } catch (err) {
      console.error('Error batch processing:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="DataProcessing">
      <h2>Data Processing Service</h2>
      <p className="subtitle">Python Service (FastAPI)</p>

      <div className="processing-grid">
        <div className="processing-card">
          <h3>Single Value Processing</h3>
          <div className="form-group">
            <label>Input Value</label>
            <input
              type="number"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Enter a number"
            />
          </div>
          <button
            onClick={processSingle}
            disabled={loading}
            className="btn-primary"
          >
            {loading ? 'Processing...' : 'Process Value'}
          </button>

          {result && !result.error && (
            <div className="result-box success">
              <h4>Result:</h4>
              <p><strong>Original:</strong> {result.original_value}</p>
              <p><strong>Processed:</strong> {result.processed_value}</p>
              <p><strong>Operation:</strong> {result.operation}</p>
              <p className="timestamp">
                {new Date(result.timestamp).toLocaleString()}
              </p>
            </div>
          )}

          {result?.error && (
            <div className="result-box error">
              <p>{result.error}</p>
            </div>
          )}
        </div>

        <div className="processing-card">
          <h3>Batch Processing</h3>
          <div className="form-group">
            <label>Comma-separated values (max 100)</label>
            <textarea
              value={batchData}
              onChange={(e) => setBatchData(e.target.value)}
              placeholder="5, 10, 15, 20, 25"
              rows="3"
            />
          </div>
          <button
            onClick={processBatch}
            disabled={loading}
            className="btn-primary"
          >
            {loading ? 'Processing...' : 'Batch Process'}
          </button>

          {batchResults.length > 0 && (
            <div className="result-box success">
              <h4>Batch Results ({batchResults.length} items):</h4>
              <table className="results-table">
                <thead>
                  <tr>
                    <th>Original</th>
                    <th>Processed</th>
                    <th>Operation</th>
                  </tr>
                </thead>
                <tbody>
                  {batchResults.map((r, i) => (
                    <tr key={i}>
                      <td>{r.original_value}</td>
                      <td>{r.processed_value}</td>
                      <td>{r.operation}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      <div className="api-docs">
        <h3>API Documentation</h3>
        <p>
          The Python service provides FastAPI with auto-generated Swagger docs.
        </p>
        <a
          href="http://localhost:8000/docs"
          target="_blank"
          rel="noopener noreferrer"
          className="btn-secondary"
        >
          Open Swagger UI →
        </a>
        <div className="endpoint-list">
          <h4>Available Endpoints:</h4>
          <ul>
            <li><code>POST /api/v1/process</code> - Process single value</li>
            <li><code>POST /api/v1/batch-process</code> - Process multiple values</li>
            <li><code>GET /api/v1/analytics/summary</code> - Get analytics</li>
            <li><code>GET /metrics</code> - Prometheus metrics</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default DataProcessing
