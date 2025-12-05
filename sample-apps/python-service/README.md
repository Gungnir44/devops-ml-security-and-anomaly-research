# Python Data Processing Service

FastAPI-based data processing and analytics service for the DevOps Security Research Project.

## Features

- **FastAPI** - Modern, fast web framework
- **Async/Await** - Asynchronous request handling
- **Pydantic** - Data validation using Python type hints
- **Prometheus Metrics** - Built-in metrics endpoint
- **OpenAPI Documentation** - Auto-generated interactive API docs
- **Type Hints** - Full type annotation support
- **Security** - Built-in security features

## Prerequisites

- Python >= 3.11
- pip
- Docker (for containerization)

## Getting Started

### Local Development

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application:**
   ```bash
   # Development mode (with auto-reload)
   uvicorn app.main:app --reload --port 8000

   # Or use the main script
   python -m app.main
   ```

The API will be available at `http://localhost:8000`

### Interactive API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_main.py

# Run in watch mode
pytest-watch
```

### Code Quality

```bash
# Format code with Black
black app/ tests/

# Check with flake8
flake8 app/ tests/

# Type checking with mypy
mypy app/

# Security scan with Bandit
bandit -r app/
```

## API Endpoints

### Root
```http
GET /
```

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-04T15:30:00.000Z",
  "uptime_seconds": 125.45,
  "environment": "development"
}
```

### Process Single Data Point
```http
POST /api/v1/process
Content-Type: application/json

{
  "value": 10.5,
  "metadata": {"source": "sensor-1"}
}
```

**Response:**
```json
{
  "original_value": 10.5,
  "processed_value": 21.0,
  "operation": "multiply_by_2",
  "timestamp": "2025-12-04T15:30:00.000Z"
}
```

### Batch Process
```http
POST /api/v1/batch-process
Content-Type: application/json

[
  {"value": 5.0},
  {"value": 10.0},
  {"value": 15.0}
]
```

**Response:** Array of ProcessingResult objects

### Analytics Summary
```http
GET /api/v1/analytics/summary
```

**Response:**
```json
{
  "total_processed": 1523,
  "average_processing_time_ms": 12.5,
  "success_rate": 0.987,
  "last_24h": {
    "processed": 342,
    "errors": 5,
    "avg_value": 45.2
  },
  "timestamp": "2025-12-04T15:30:00.000Z"
}
```

### Prometheus Metrics
```http
GET /metrics
```

Returns Prometheus-formatted metrics.

## Docker

### Build Image

```bash
docker build -t python-service:latest .
```

### Run Container

```bash
docker run -p 8000:8000 \
  -e ENVIRONMENT=production \
  python-service:latest
```

## Kubernetes Deployment

### Deploy

```bash
kubectl apply -f k8s/deployment.yaml
```

### Verify

```bash
kubectl get pods -n production -l app=python-service
kubectl logs -n production -l app=python-service --tail=50
```

## CI/CD Pipeline

GitHub Actions workflow includes:
1. **Code Quality** - Black, flake8, mypy
2. **Testing** - pytest with coverage
3. **Security Scanning**
   - Secret scanning (TruffleHog, Gitleaks)
   - SAST (Bandit, Semgrep)
   - Dependency scanning (Safety, pip-audit)
4. **Build** - Docker image
5. **Container Scanning** - Trivy, Grype
6. **Deploy** - Kubernetes via ArgoCD

## Project Structure

```
python-service/
├── app/
│   ├── __init__.py
│   └── main.py              # Main application
├── tests/
│   ├── __init__.py
│   └── test_main.py         # Tests
├── k8s/
│   └── deployment.yaml      # Kubernetes manifests
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
```

## Development

### Adding New Endpoints

1. Define Pydantic models
2. Create route handler in `app/main.py`
3. Add tests in `tests/test_main.py`
4. Update documentation

### Example:

```python
@app.get("/api/v1/example")
async def example_endpoint():
    return {"message": "Hello World"}
```

## Monitoring

### Metrics

The `/metrics` endpoint exposes:
- HTTP request counts
- Request duration
- Custom business metrics

Configure Prometheus to scrape:
```yaml
- job_name: 'python-service'
  static_configs:
    - targets: ['python-service:8000']
```

## Security

- ✅ Non-root user in Docker
- ✅ Read-only root filesystem
- ✅ Security context (drop all capabilities)
- ✅ Automated vulnerability scanning
- ✅ Dependency security checks

## Contributing

1. Create feature branch
2. Make changes
3. Add tests
4. Run quality checks: `black`, `flake8`, `mypy`, `pytest`
5. Submit pull request

## License

MIT License

## Support

For issues, open a GitHub issue.

---

**Project:** DevOps Master's Degree Research
**Version:** 1.0.0
**Last Updated:** December 2025
