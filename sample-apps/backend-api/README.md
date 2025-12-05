# Backend API

RESTful API service for the DevOps Security Research Project.

## Features

- **Express.js** - Fast, minimal web framework
- **Security Headers** - Helmet.js for security best practices
- **Health Checks** - Built-in health and readiness endpoints
- **Metrics** - Prometheus-compatible metrics endpoint
- **Logging** - Morgan HTTP request logger
- **CORS** - Configurable Cross-Origin Resource Sharing
- **Compression** - Gzip compression for responses

## Prerequisites

- Node.js >= 18.0.0
- npm >= 9.0.0
- Docker (for containerization)

## Getting Started

### Local Development

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run in development mode:**
   ```bash
   npm run dev
   ```

4. **Run in production mode:**
   ```bash
   npm start
   ```

The API will be available at `http://localhost:3000`

### Running Tests

```bash
# Run tests once
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm run test:watch
```

### Linting

```bash
# Check for linting errors
npm run lint

# Auto-fix linting errors
npm run lint:fix
```

## API Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-04T15:30:00.000Z",
  "uptime": 125.45,
  "environment": "development"
}
```

### Get All Users
```http
GET /api/v1/users
```

**Response:**
```json
{
  "users": [
    {
      "id": 1,
      "name": "Alice",
      "email": "alice@example.com",
      "role": "admin"
    }
  ]
}
```

### Get User by ID
```http
GET /api/v1/users/:id
```

**Response:**
```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com",
  "role": "admin",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

### Create User
```http
POST /api/v1/users
Content-Type: application/json

{
  "name": "Bob",
  "email": "bob@example.com",
  "role": "user"
}
```

**Response:**
```json
{
  "id": 4,
  "name": "Bob",
  "email": "bob@example.com",
  "role": "user",
  "createdAt": "2025-12-04T15:30:00.000Z"
}
```

### Metrics (Prometheus)
```http
GET /metrics
```

Returns Prometheus-formatted metrics for monitoring.

## Docker

### Build Docker Image

```bash
docker build -t backend-api:latest .
```

### Run Docker Container

```bash
docker run -p 3000:3000 \
  -e NODE_ENV=production \
  backend-api:latest
```

### Docker Compose

```bash
docker-compose up -d
```

## Kubernetes Deployment

### Deploy to Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
```

### Verify Deployment

```bash
kubectl get pods -n production -l app=backend-api
kubectl get svc -n production backend-api
```

### Access Logs

```bash
kubectl logs -n production -l app=backend-api --tail=100 -f
```

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

### Pipeline Stages

1. **Code Quality** - ESLint, Prettier
2. **Testing** - Unit tests with Jest
3. **Security Scanning**
   - Secret scanning (TruffleHog, Gitleaks)
   - SAST (CodeQL, Semgrep)
   - Dependency scanning (npm audit, Snyk)
4. **Build** - Docker image build
5. **Container Scanning** - Trivy, Grype
6. **Push** - Push to GitHub Container Registry
7. **Deploy** - Update Kubernetes manifests for ArgoCD

### Triggering the Pipeline

```bash
git add .
git commit -m "Your commit message"
git push origin main
```

## Project Structure

```
backend-api/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # CI/CD pipeline
├── k8s/
│   └── deployment.yaml        # Kubernetes manifests
├── src/
│   ├── server.js              # Main application
│   └── server.test.js         # Tests
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── jest.config.js
├── package.json
└── README.md
```

## Security

### Security Features

- ✅ Helmet.js security headers
- ✅ Non-root Docker user
- ✅ Read-only root filesystem
- ✅ Resource limits
- ✅ Security context (drop ALL capabilities)
- ✅ Automated security scanning

### Security Scanning

The CI/CD pipeline includes:
- **Secret Detection** - TruffleHog, Gitleaks
- **SAST** - CodeQL, Semgrep
- **Dependency Vulnerabilities** - npm audit, Snyk
- **Container Vulnerabilities** - Trivy, Grype

## Monitoring

### Prometheus Metrics

The `/metrics` endpoint exposes:
- HTTP request counts
- Request duration histograms
- Custom business metrics

### Health Checks

- **Liveness:** `/health` - Is the application running?
- **Readiness:** `/health` - Is the application ready to serve traffic?

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Submit a pull request

## Research Project Integration

This application is part of a Master's research project on **ML-Based Security Anomaly Detection for DevOps**. The CI/CD pipeline generates security scan data used for:

- Baseline normal behavior modeling
- Attack scenario simulation
- Feature extraction for ML models
- Anomaly detection validation

See the main project documentation for more details.

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.

---

**Project:** DevOps Master's Degree Research
**Version:** 1.0.0
**Last Updated:** December 2025
