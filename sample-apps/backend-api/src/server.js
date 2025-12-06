const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');
const compression = require('compression');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet()); // Security headers
app.use(cors()); // Enable CORS
app.use(compression()); // Compress responses
app.use(morgan('combined')); // Logging
app.use(express.json()); // Parse JSON bodies
app.use(express.urlencoded({ extended: true }));

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    environment: process.env.NODE_ENV || 'development',
  });
});

// API routes
app.get('/api/v1/users', (req, res) => {
  // Sample endpoint - in production, fetch from database
  res.json({
    users: [
      { id: 1, name: 'Alice', email: 'alice@example.com', role: 'admin' },
      { id: 2, name: 'Bob', email: 'bob@example.com', role: 'user' },
      { id: 3, name: 'Charlie', email: 'charlie@example.com', role: 'user' },
    ],
  });
});

app.get('/api/v1/users/:id', (req, res) => {
  const { id } = req.params;

  // Sample response - in production, fetch from database
  if (id === '1') {
    res.json({
      id: 1,
      name: 'Alice',
      email: 'alice@example.com',
      role: 'admin',
      createdAt: '2024-01-15T10:30:00Z',
    });
  } else {
    res.status(404).json({ error: 'User not found' });
  }
});

app.post('/api/v1/users', (req, res) => {
  const { name, email, role } = req.body;

  // Validation
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email are required' });
  }

  // Sample response - in production, save to database
  res.status(201).json({
    id: 4,
    name,
    email,
    role: role || 'user',
    createdAt: new Date().toISOString(),
  });
});

// Metrics endpoint (for Prometheus)
app.get('/metrics', (req, res) => {
  res.set('Content-Type', 'text/plain');
  res.send(`
# HELP http_requests_total Total number of HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/api/v1/users"} 150
http_requests_total{method="POST",endpoint="/api/v1/users"} 23

# HELP http_request_duration_seconds HTTP request latency in seconds
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{le="0.1"} 95
http_request_duration_seconds_bucket{le="0.5"} 145
http_request_duration_seconds_bucket{le="1.0"} 150
http_request_duration_seconds_sum 35.5
http_request_duration_seconds_count 150
  `.trim());
});

// Error handling
app.use((err, req, res, _next) => {
  console.error('Error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined,
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Not found' });
});

// Start server
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Backend API server running on port ${PORT}`);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
    console.log(`Health check: http://localhost:${PORT}/health`);
  });
}

module.exports = app;
