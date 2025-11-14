# Docker Containerization Guide

Welcome to Phase 2 of your DevOps journey! This directory contains everything needed to run your monitoring stack in Docker containers.

---

## What You'll Learn

- **Docker Fundamentals**: Images, containers, volumes, networks
- **Multi-Stage Builds**: Optimizing container size
- **Docker Compose**: Multi-container orchestration
- **Container Networking**: Service-to-service communication
- **Volume Management**: Persistent data storage
- **Health Checks**: Container monitoring
- **Production Best Practices**: Security, optimization, logging

---

## Project Structure

```
docker/
├── health-checker.Dockerfile       # Health checker container
├── web-dashboard.Dockerfile        # Dashboard container
├── docker-compose-monitoring.yml   # Complete monitoring stack
├── dashboard/
│   ├── app.py                     # Flask dashboard app
│   └── templates/                 # HTML templates
├── nginx-content/                 # Demo web server content
└── README.md                      # This file
```

---

## The Monitoring Stack

Your Docker setup includes 5 containers:

### 1. **health-checker**
- Runs system health checks every 5 minutes
- Saves reports to shared volume
- Uses multi-stage build for efficiency

### 2. **dashboard** (Port 5000)
- Web interface to view health reports
- Auto-refreshes every 30 seconds
- REST API endpoints

### 3. **postgres-demo** (Example Service)
- PostgreSQL database for monitoring demos
- Can be checked by health checker

### 4. **redis-demo** (Example Service)
- Redis cache for monitoring demos
- Demonstrates service health checks

### 5. **nginx-demo** (Port 8080)
- Demo web server
- Shows multi-service deployment

All containers are connected via a custom bridge network and share volumes for data persistence.

---

## Quick Start

### Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)

**Verify installation**:
```bash
docker --version
docker-compose --version
```

### Step 1: Start the Stack

```bash
cd docker

# Start all services
docker-compose -f docker-compose-monitoring.yml up -d

# View logs
docker-compose -f docker-compose-monitoring.yml logs -f
```

### Step 2: Access the Services

- **Dashboard**: http://localhost:5000
- **Demo Web Server**: http://localhost:8080
- **API**: http://localhost:5000/api/latest

### Step 3: Check Container Status

```bash
# List running containers
docker ps

# Check health status
docker inspect devops-health-checker --format='{{.State.Health.Status}}'
docker inspect devops-dashboard --format='{{.State.Health.Status}}'
```

---

## Docker Commands Cheat Sheet

### Container Management

```bash
# Start all services
docker-compose -f docker-compose-monitoring.yml up -d

# Stop all services
docker-compose -f docker-compose-monitoring.yml down

# Restart a specific service
docker-compose -f docker-compose-monitoring.yml restart health-checker

# View logs
docker-compose -f docker-compose-monitoring.yml logs -f health-checker

# Execute command in container
docker-compose -f docker-compose-monitoring.yml exec health-checker bash

# View container stats
docker stats

# List all containers (including stopped)
docker ps -a
```

### Image Management

```bash
# List images
docker images

# Build images
docker-compose -f docker-compose-monitoring.yml build

# Rebuild without cache
docker-compose -f docker-compose-monitoring.yml build --no-cache

# Remove unused images
docker image prune
```

### Volume Management

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect docker_health-reports

# View volume contents
docker run --rm -v docker_health-reports:/data alpine ls -lah /data

# Backup volume
docker run --rm -v docker_health-reports:/data -v $(pwd):/backup alpine tar czf /backup/reports-backup.tar.gz -C /data .

# Remove unused volumes
docker volume prune
```

### Network Management

```bash
# List networks
docker network ls

# Inspect network
docker network inspect docker_monitoring-network

# View connected containers
docker network inspect docker_monitoring-network --format='{{range .Containers}}{{.Name}} {{end}}'
```

---

## Understanding the Dockerfiles

### Multi-Stage Build (health-checker.Dockerfile)

```dockerfile
# Stage 1: Builder - Compiles dependencies
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime - Minimal final image
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY system_health_checker_v2.py .
CMD ["python", "system_health_checker_v2.py"]
```

**Benefits**:
- Smaller image size (no build tools in final image)
- Faster deployments
- Better security (fewer packages)

### Health Checks

```yaml
healthcheck:
  test: ["CMD", "python", "system_health_checker_v2.py", "--quiet"]
  interval: 5m      # Run every 5 minutes
  timeout: 30s      # Fail if takes > 30s
  retries: 3        # Try 3 times before marking unhealthy
  start_period: 10s # Grace period on startup
```

---

## Docker Compose Architecture

### Networks

All services are on a custom bridge network:

```yaml
networks:
  monitoring-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

**Benefits**:
- Isolated from other containers
- Services can communicate by name
- Custom DNS resolution

**Example**: Health checker can connect to `postgres-demo:5432` instead of using IP addresses.

### Volumes

Persistent data storage:

```yaml
volumes:
  health-reports:  # Shared between health-checker and dashboard
  health-logs:     # Health checker logs
  postgres-data:   # Database persistence
  redis-data:      # Cache persistence
```

**Data survives container restarts!**

---

## Configuration for Database Monitoring

To enable database health checks, update your config.json:

```json
{
  "databases": {
    "check_enabled": true,
    "connections": [
      {
        "name": "PostgreSQL Demo",
        "type": "postgresql",
        "host": "postgres-demo",
        "port": 5432,
        "database": "demodb",
        "user": "demouser",
        "password": "demopass",
        "timeout": 5
      },
      {
        "name": "Redis Demo",
        "type": "redis",
        "host": "redis-demo",
        "port": 6379,
        "timeout": 3
      }
    ]
  }
}
```

**Note**: Use container names as hostnames (Docker DNS handles resolution).

---

## Production Best Practices Implemented

### 1. Security
- Non-root user execution
- Read-only volumes where possible
- Minimal base images (alpine/slim)
- No hardcoded secrets (use environment variables)

### 2. Resource Management
```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 512M
    reservations:
      cpus: '0.25'
      memory: 256M
```

### 3. Logging
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### 4. Restart Policies
```yaml
restart: unless-stopped
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose -f docker-compose-monitoring.yml logs health-checker

# Check if port is in use
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Linux/macOS

# Inspect container
docker inspect devops-health-checker
```

### Dashboard Shows "No Data"

```bash
# Check if reports exist
docker run --rm -v docker_health-reports:/data alpine ls -lah /data

# Manually run health checker
docker-compose -f docker-compose-monitoring.yml exec health-checker \
  python system_health_checker_v2.py

# Check volume mount
docker inspect devops-dashboard --format='{{.Mounts}}'
```

### Container is Unhealthy

```bash
# View health status
docker inspect devops-health-checker --format='{{json .State.Health}}' | jq

# Check health check logs
docker inspect devops-health-checker --format='{{range .State.Health.Log}}{{.Output}}{{end}}'

# Test health check manually
docker exec devops-health-checker python system_health_checker_v2.py --quiet
echo $?  # Should return 0 for healthy
```

### Network Issues

```bash
# Test connectivity between containers
docker exec devops-health-checker ping postgres-demo

# Check DNS resolution
docker exec devops-health-checker nslookup postgres-demo

# Inspect network
docker network inspect docker_monitoring-network
```

---

## Advanced Operations

### Scaling Services

```bash
# Run multiple health checkers
docker-compose -f docker-compose-monitoring.yml up -d --scale health-checker=3
```

### Building for Different Architectures

```bash
# Build for ARM (Raspberry Pi, M1 Mac)
docker buildx build --platform linux/arm64 -f health-checker.Dockerfile -t health-checker:arm64 ..

# Build for both AMD64 and ARM64
docker buildx build --platform linux/amd64,linux/arm64 -f health-checker.Dockerfile -t health-checker:multi ..
```

### Exporting and Importing Images

```bash
# Save image to file
docker save devops-health-checker:latest | gzip > health-checker.tar.gz

# Load image on another machine
docker load < health-checker.tar.gz
```

### Accessing Container Filesystem

```bash
# Copy files from container
docker cp devops-health-checker:/app/reports/. ./local-reports/

# Copy files to container
docker cp config.json devops-health-checker:/app/config.json
```

---

## What You've Learned

### Docker Concepts

1. **Containers vs Images**
   - Images: Blueprint (Dockerfile → built image)
   - Containers: Running instances of images

2. **Layered File System**
   - Each Dockerfile instruction creates a layer
   - Layers are cached for faster builds
   - Order matters for build optimization

3. **Volumes**
   - Persist data outside containers
   - Share data between containers
   - Survive container deletion

4. **Networks**
   - Isolate container communication
   - DNS-based service discovery
   - Multiple network drivers (bridge, host, overlay)

5. **Docker Compose**
   - Define multi-container applications
   - Manage dependencies (depends_on)
   - Easy orchestration

### DevOps Skills

- Container orchestration
- Service discovery and networking
- Health monitoring and checks
- Data persistence strategies
- Multi-stage builds
- Resource management
- Production deployment patterns

---

## Next Steps

### 1. Enhance the Stack

Add more services:
```yaml
# Monitoring
- Prometheus (metrics collection)
- Grafana (visualization)

# Logging
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Fluentd (log aggregation)

# Databases
- MongoDB
- MySQL
```

### 2. Learn Kubernetes

Docker Compose → Kubernetes:
- Convert docker-compose to Kubernetes manifests
- Deploy to Minikube
- Learn pods, services, deployments

### 3. CI/CD Integration

- Build images in GitHub Actions
- Push to Docker Hub/GitHub Container Registry
- Automated testing in containers

### 4. Security Scanning

```bash
# Scan image for vulnerabilities
docker scan devops-health-checker:latest
```

---

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Hub](https://hub.docker.com/)
- [Play with Docker](https://labs.play-with-docker.com/)

---

## Clean Up

```bash
# Stop and remove all containers, networks, volumes
docker-compose -f docker-compose-monitoring.yml down -v

# Remove all unused Docker resources
docker system prune -a --volumes
```

---

**Phase 2 Complete!** You've successfully containerized your DevOps monitoring stack. Ready for Phase 3: CI/CD Pipelines?

**Author**: Joshua
**Last Updated**: November 14, 2025
