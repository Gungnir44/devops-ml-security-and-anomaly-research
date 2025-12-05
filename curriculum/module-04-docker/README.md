# Module 4: Docker Containerization

**Duration**: 3 weeks (12-15 hours/week)
**Prerequisites**: Modules 1-3 (DevOps, Linux, Python)
**Deliverable**: Multi-container production application

---

## Overview

Docker **revolutionized software deployment**. Before containers, "works on my machine" was the excuse. After containers, applications run identically everywhere.

**The Problem Docker Solved**:
- Different environments (dev laptop vs. production server)
- Dependency conflicts ("needs Python 2.7 but system has 3.9")
- Configuration drift (servers diverge over time)
- Slow deployments (hours to provision new server)

**The Container Solution**:
- Package app + dependencies together
- Run identically on any system
- Isolated from host and other containers
- Start in seconds (not hours)

**By the end of this module, you'll**:
- Understand why containers changed everything
- Build Docker images from scratch
- Optimize images for production
- Run multi-container applications with Docker Compose
- Implement container security best practices
- Debug containerized applications

---

## Learning Objectives

### Docker Fundamentals
- [ ] Understand containers vs VMs
- [ ] Docker architecture (daemon, client, registry)
- [ ] Images vs containers
- [ ] Dockerfile syntax and best practices
- [ ] Docker networking (bridge, host, overlay)
- [ ] Volumes and persistent data
- [ ] Docker Compose for multi-container apps

### Production Skills
- [ ] Multi-stage builds (smaller images)
- [ ] Security scanning and hardening
- [ ] Resource limits (CPU, memory)
- [ ] Health checks
- [ ] Logging and debugging
- [ ] CI/CD integration

---

## Module Structure

### Week 1: Docker Fundamentals

**Lesson 1**: Why Containers (1.5 hours)
- The "works on my machine" problem
- VMs vs Containers
- How Docker revolutionized deployment
- When to use containers (and when not to)

**Lesson 2**: Docker Architecture (2 hours)
- Images, containers, registries
- Layers and union filesystem
- Docker daemon and CLI
- Docker Hub and private registries

**Lesson 3**: Your First Container (2 hours)
- Running containers (docker run)
- Port mapping and networking
- Environment variables
- Interactive vs detached mode
- Container lifecycle

**Exercise 1**: Run the Classics
- Run nginx, MySQL, Redis containers
- Connect them together
- Access from host machine
- Inspect logs and processes

**Exercise 2**: Debug a Production Issue
- Container won't start (debug)
- Application crashes (find logs)
- Can't connect (network troubleshooting)

### Week 2: Building Images

**Lesson 4**: Dockerfiles (2.5 hours)
- Dockerfile instructions (FROM, RUN, COPY, CMD, ENTRYPOINT)
- Layering and caching
- .dockerignore
- Build context

**Lesson 5**: Dockerfile Best Practices (2 hours)
- Multi-stage builds (reduce size)
- Minimal base images (Alpine)
- Security: non-root users, scanning
- Optimization: layer ordering, caching

**Lesson 6**: Data Persistence (1.5 hours)
- Volumes vs bind mounts
- Named volumes
- Volume drivers
- Backup and restore

**Exercise 3**: Containerize Your Python App
- Write Dockerfile for Python application
- Multi-stage build
- Under 50MB final image
- Non-root user

**Exercise 4**: Database Container with Persistence
- Run PostgreSQL in container
- Persist data with volumes
- Backup and restore database
- Initialization scripts

### Week 3: Multi-Container Apps & Production

**Lesson 7**: Docker Compose (2 hours)
- docker-compose.yml syntax
- Services, networks, volumes
- Environment variables and secrets
- Scaling services

**Lesson 8**: Container Networking (1.5 hours)
- Bridge networks
- Custom networks
- Service discovery
- Load balancing

**Lesson 9**: Production Readiness (2 hours)
- Health checks
- Resource limits
- Logging drivers
- Monitoring containers
- Security best practices

**Exercise 5**: Full-Stack Application
- Frontend (React/Vue in nginx)
- Backend (Python/Node API)
- Database (PostgreSQL)
- Cache (Redis)
- All in Docker Compose

**Exercise 6**: Production Deployment
- Optimize all images
- Implement health checks
- Add resource limits
- Configure logging
- Security scan all images

---

## Assessments

### Quiz (20 points, 80% to pass)
- Container concepts and architecture
- Dockerfile best practices
- Docker Compose
- Networking and volumes
- Security

### Project: Production-Grade E-Commerce Backend (100 points)

**Build and containerize a complete e-commerce API**:

1. **Application Container** (25 points)
   - Python/Node.js REST API
   - Multi-stage build (< 100MB)
   - Non-root user
   - Health check endpoint

2. **Database Container** (20 points)
   - PostgreSQL with persistent volume
   - Initialization scripts
   - Backup automation
   - Connection pooling

3. **Cache Layer** (15 points)
   - Redis for session storage
   - Configured for persistence
   - Connected to API

4. **Docker Compose** (20 points)
   - All services defined
   - Custom networks
   - Environment configuration
   - One-command startup

5. **Production Readiness** (20 points)
   - All images scanned for vulnerabilities
   - Resource limits set
   - Centralized logging
   - Comprehensive documentation

**Portfolio Quality**: Deploy-ready containerized application

---

## Key Concepts

### Containers vs VMs

```
Virtual Machines                 Containers
┌─────────────────────┐         ┌─────────────────────┐
│   App   │   App     │         │  App  │  App │ App  │
├─────────┼───────────┤         ├───────┼──────┼──────┤
│  Bins/  │  Bins/    │         │ Bins/ │Bins/ │Bins/ │
│  Libs   │  Libs     │         │ Libs  │Libs  │Libs  │
├─────────┴───────────┤         ├──────────────────────┤
│  Guest OS │ Guest OS│         │   Docker Engine      │
├─────────────────────┤         ├──────────────────────┤
│     Hypervisor      │         │     Host OS          │
├─────────────────────┤         ├──────────────────────┤
│   Infrastructure    │         │   Infrastructure     │
└─────────────────────┘         └──────────────────────┘

Size: GBs                        Size: MBs
Startup: Minutes                 Startup: Seconds
Overhead: High                   Overhead: Low
```

### Docker Image Layers

```dockerfile
FROM ubuntu:20.04           # Layer 1 (100MB)
RUN apt update              # Layer 2 (50MB)
COPY app.py /app/           # Layer 3 (1KB)
CMD python /app/app.py      # Layer 4 (metadata)
```

Each instruction = new layer. Layers cached and reused!

---

## Real-World Use Cases

**Before Docker**:
```bash
# Deploy to 10 servers (2 hours each = 20 hours)
for server in web{1..10}; do
  ssh $server
  # Install dependencies
  sudo apt install python3.9 nginx redis...
  # Configure firewall
  # Configure environment
  # Deploy code
  # Restart services
  # Pray it works
done
```

**With Docker**:
```bash
# Deploy to 10 servers (5 minutes total)
for server in web{1..10}; do
  ssh $server "docker pull myapp:v1.0 && docker run -d myapp:v1.0"
done
```

---

## Essential Docker Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `docker run` | Start container | `docker run -d -p 80:80 nginx` |
| `docker ps` | List running containers | `docker ps -a` |
| `docker build` | Build image | `docker build -t myapp:1.0 .` |
| `docker images` | List images | `docker images` |
| `docker exec` | Run command in container | `docker exec -it web bash` |
| `docker logs` | View container logs | `docker logs -f web` |
| `docker stop` | Stop container | `docker stop web` |
| `docker rm` | Remove container | `docker rm web` |
| `docker rmi` | Remove image | `docker rmi myapp:1.0` |
| `docker-compose up` | Start services | `docker-compose up -d` |

---

## Success Criteria

**You're ready to move on when you can**:
- [ ] Explain containers vs VMs to anyone
- [ ] Write production-quality Dockerfiles
- [ ] Build images under 100MB
- [ ] Deploy multi-container apps with Compose
- [ ] Debug containerized applications
- [ ] Implement container security best practices
- [ ] Pass quiz with 80%+ (16/20)
- [ ] Complete production e-commerce project

---

## Common Pitfalls

### Building Images
- ❌ Large images (1GB+) - use Alpine, multi-stage builds
- ❌ Running as root - security risk
- ❌ Hardcoding secrets - use environment variables
- ❌ Not using .dockerignore - slow builds
- ✅ Optimize for size (< 100MB ideal)
- ✅ Non-root user
- ✅ Secrets via env vars or Docker secrets
- ✅ Exclude unnecessary files

### Running Containers
- ❌ Not persisting data - containers are ephemeral!
- ❌ No resource limits - one container hogs all CPU/RAM
- ❌ No health checks - can't detect failures
- ✅ Use volumes for databases
- ✅ Set memory and CPU limits
- ✅ Implement health check endpoints

---

## Time Commitment

| Activity | Time/Week |
|----------|-----------|
| Lessons | 5-6 hours |
| Exercises | 6-8 hours |
| Quiz + Project | 3-4 hours |
| **Total** | **14-18 hours** |

---

## Tools You'll Use

- **Docker Desktop** (Mac/Windows) or **Docker Engine** (Linux)
- **Docker Compose**
- **Docker Hub** (image registry)
- **Trivy** or **Snyk** (security scanning)
- **Dive** (image layer analysis)

---

## Getting Started

### Step 1: Install Docker

**Linux**:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER  # No sudo needed
```

**Mac/Windows**:
- Download Docker Desktop: https://www.docker.com/products/docker-desktop

### Step 2: Verify Installation

```bash
docker --version
docker compose --version

# Run test container
docker run hello-world
```

### Step 3: Pull Your First Images

```bash
docker pull nginx
docker pull postgres:14
docker pull redis:alpine
```

---

## Module Dependencies

**Builds on**:
- Module 2: Linux (containers run Linux, even on Windows!)
- Module 3: Python (containerize Python apps)

**Prepares for**:
- Module 5: CI/CD (build and deploy containers)
- Module 6: IaC (provision infrastructure for containers)
- Module 7: Kubernetes (orchestrates containers at scale)
- All future modules (everything runs in containers now)

---

## Career Impact

**Docker is mandatory for modern DevOps**:
- 95%+ of DevOps jobs require Docker
- Containerization is industry standard
- Foundation for Kubernetes

**After this module**:
- Can containerize any application
- Understand container-based deployments
- Ready for Kubernetes (Module 7)
- Interview confidently about containers

---

## Let's Containerize!

Start with `lessons/lesson-01-why-containers.md`

**Remember**: Containers aren't magic. They're Linux processes with resource isolation. Once you understand this, everything clicks.

**Ready to say goodbye to "works on my machine"?** 🐳
