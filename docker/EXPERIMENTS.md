# Docker Monitoring Stack - Hands-On Experiments

Fun experiments to understand how your Docker monitoring stack works!

---

## Experiment 1: Real-Time Log Watching

**Goal**: See what's happening inside your containers in real-time

### Watch the Health Checker
```bash
cd "C:\Users\joshu\Desktop\DevOps Project\docker"

# Follow health checker logs
docker logs -f devops-health-checker

# You'll see it run health checks every 5 minutes
# Press Ctrl+C to stop watching
```

### Watch All Services at Once
```bash
# See logs from all containers
docker-compose -f docker-compose-monitoring.yml logs -f

# Or specific services
docker-compose -f docker-compose-monitoring.yml logs -f dashboard health-checker
```

**What to observe**: Every 5 minutes, you'll see the health checker wake up, collect metrics, and save a report!

---

## Experiment 2: Generate Multiple Reports

**Goal**: Create several health reports and watch the history page grow

### Run It!
```bash
# Generate 5 health reports manually
docker exec devops-health-checker python system_health_checker_v2.py
docker exec devops-health-checker python system_health_checker_v2.py
docker exec devops-health-checker python system_health_checker_v2.py
docker exec devops-health-checker python system_health_checker_v2.py
docker exec devops-health-checker python system_health_checker_v2.py
```

**Now check**:
- Go to http://localhost:5000/history
- You should see 5+ reports!
- Refresh the main dashboard to see the latest

**What you learned**: The health checker can run on-demand, and all reports are persisted in a Docker volume.

---

## Experiment 3: Explore Inside a Container

**Goal**: Get a shell inside the health checker container and look around

### Enter the Container
```bash
# Get a bash shell inside the health checker
docker exec -it devops-health-checker bash

# Now you're INSIDE the container! Try these commands:
ls -lah                    # See the files
ls reports/                # See all health reports
cat reports/*.json | head  # View a report
ps aux                     # See running processes
exit                       # Leave the container
```

**What you learned**: Containers are like mini Linux systems. Each has its own filesystem, processes, and environment!

---

## Experiment 4: Test Container Restart & Recovery

**Goal**: See what happens when a container crashes and restarts

### Stop the Dashboard
```bash
# Stop the dashboard container
docker stop devops-dashboard

# Try to access http://localhost:5000 - it won't work!
# Wait 10 seconds...

# Docker automatically restarts it (restart: unless-stopped)
docker ps -a | grep dashboard

# After ~15 seconds, try http://localhost:5000 again - it's back!
```

### Check the Status
```bash
# See when it restarted
docker ps --format "table {{.Names}}\t{{.Status}}"
```

**What you learned**: Docker's restart policies provide automatic recovery - this is how production systems stay up!

---

## Experiment 5: Explore Shared Volumes

**Goal**: See how containers share data through volumes

### Check Reports from Different Containers
```bash
# List reports from health-checker perspective
docker exec devops-health-checker ls -lh /app/reports/

# List same reports from dashboard perspective
docker exec devops-dashboard ls -lh /app/reports/

# They see the SAME files! That's the shared volume.
```

### See What's in a Report
```bash
# Read a report from the dashboard container
docker exec devops-dashboard cat /app/reports/health_report_*.json | head -50
```

**What you learned**: Docker volumes persist data and allow containers to share files. If both containers are deleted, the data survives!

---

## Experiment 6: Monitor Resource Usage

**Goal**: See how much CPU/RAM each container is using

### Watch Live Stats
```bash
# Real-time resource monitoring
docker stats

# Watch for 30 seconds, then press Ctrl+C
# Notice how little resources the containers use!
```

**What you learned**: Containers are lightweight! All 5 services use less resources than a single traditional VM.

---

## Experiment 7: Container Networking

**Goal**: See how containers communicate with each other

### Test DNS Resolution
```bash
# From health-checker, ping the database
docker exec devops-health-checker ping -c 3 postgres-demo

# From health-checker, ping redis
docker exec devops-health-checker ping -c 3 redis-demo

# From health-checker, ping the dashboard
docker exec devops-health-checker ping -c 3 dashboard
```

**Try This**:
```bash
# Check if PostgreSQL is accepting connections
docker exec devops-health-checker nc -zv postgres-demo 5432

# Check if Redis is responding
docker exec devops-health-checker nc -zv redis-demo 6379
```

**What you learned**: Docker provides automatic DNS - containers can find each other by name, no IP addresses needed!

---

## Experiment 8: Inspect Container Details

**Goal**: See the full configuration of a container

### Inspect the Health Checker
```bash
# Get detailed JSON info
docker inspect devops-health-checker

# Or specific fields:
docker inspect devops-health-checker --format='{{.State.Status}}'
docker inspect devops-health-checker --format='{{.State.Health.Status}}'
docker inspect devops-health-checker --format='{{range .Mounts}}{{.Type}}: {{.Source}} -> {{.Destination}}{{"\n"}}{{end}}'
```

**What you learned**: Docker tracks everything - state, health, networks, volumes, environment variables, etc.

---

## Experiment 9: Simulate a Problem (And Fix It!)

**Goal**: Break something and see how to fix it

### Kill the Dashboard Process
```bash
# Stop the dashboard
docker stop devops-dashboard

# Dashboard is down! http://localhost:5000 won't work

# Check status
docker ps -a | grep dashboard

# Manually restart it
docker start devops-dashboard

# Wait 5 seconds and visit http://localhost:5000 - it's back!
```

### Check Health Status
```bash
# See health check results
docker inspect devops-health-checker --format='{{json .State.Health}}' | python -m json.tool

# Or simpler
docker ps --format "table {{.Names}}\t{{.Status}}"
```

**What you learned**: Troubleshooting containers is straightforward with Docker commands.

---

## Experiment 10: Scale a Service

**Goal**: Run multiple instances of the health checker

### Scale Up!
```bash
cd docker

# Run 3 health checkers instead of 1
docker-compose -f docker-compose-monitoring.yml up -d --scale health-checker=3

# Check it out
docker ps | grep health-checker
```

**Try This**:
```bash
# See all 3 generating reports
docker-compose -f docker-compose-monitoring.yml logs -f health-checker

# Scale back down to 1
docker-compose -f docker-compose-monitoring.yml up -d --scale health-checker=1
```

**What you learned**: Docker Compose makes scaling services trivial. This is the foundation of auto-scaling in production!

---

## Experiment 11: Check What's in the Database

**Goal**: Connect to the PostgreSQL demo database

### Access PostgreSQL
```bash
# Connect to PostgreSQL shell
docker exec -it devops-postgres psql -U demouser -d demodb

# Now you're in PostgreSQL! Try:
\l                  # List databases
\dt                 # List tables (empty for now)
SELECT version();   # Show PostgreSQL version
\q                  # Quit
```

### Check Redis
```bash
# Connect to Redis
docker exec -it devops-redis redis-cli

# Try Redis commands:
PING                    # Should return PONG
SET test "Hello Docker" # Set a value
GET test                # Get the value
KEYS *                  # List all keys
EXIT                    # Leave Redis
```

**What you learned**: Your stack includes real databases that are accessible and working!

---

## Experiment 12: Clean Up and Restart Fresh

**Goal**: See how to reset everything

### Stop Everything
```bash
cd docker

# Stop all containers (data persists)
docker-compose -f docker-compose-monitoring.yml down

# Check - no containers running
docker ps
```

### Restart Everything
```bash
# Start it all again
docker-compose -f docker-compose-monitoring.yml up -d

# Check http://localhost:5000
# All your old reports are still there! (volumes persisted)
```

### Nuclear Option (Delete Everything)
```bash
# Stop and DELETE all data (volumes too)
docker-compose -f docker-compose-monitoring.yml down -v

# Now restart
docker-compose -f docker-compose-monitoring.yml up -d

# Check http://localhost:5000
# History is empty - fresh start!
```

**What you learned**: Docker volumes persist data across container restarts but can be wiped when needed.

---

## Experiment 13: View Network Details

**Goal**: Understand the Docker network connecting your services

### Inspect the Network
```bash
# See all Docker networks
docker network ls

# Inspect your monitoring network
docker network inspect docker_monitoring-network

# See which containers are connected
docker network inspect docker_monitoring-network --format='{{range .Containers}}{{.Name}} - {{.IPv4Address}}{{"\n"}}{{end}}'
```

**What you learned**: Docker creates isolated networks for your services. They get their own subnet and IP addresses!

---

## Experiment 14: Build Time!

**Goal**: Rebuild images to see how Docker caching works

### Rebuild an Image
```bash
cd docker

# Rebuild with cache (fast)
docker-compose -f docker-compose-monitoring.yml build health-checker

# Rebuild without cache (slower, downloads everything)
docker-compose -f docker-compose-monitoring.yml build --no-cache health-checker

# Notice the speed difference!
```

**What you learned**: Docker caches build layers for faster rebuilds - crucial for CI/CD pipelines!

---

## Experiment 15: Export and Backup

**Goal**: Save your work

### Export Health Reports
```bash
# Copy reports from container to your local machine
docker cp devops-dashboard:/app/reports ./local-reports-backup

# Check them out
ls local-reports-backup/
```

### Backup a Volume
```bash
# Create a backup of the reports volume
docker run --rm -v docker_health-reports:/data -v "C:\Users\joshu\Desktop\DevOps Project\docker:/backup" alpine tar czf /backup/reports-backup.tar.gz -C /data .

# You now have reports-backup.tar.gz!
```

**What you learned**: Docker provides easy ways to backup and export data.

---

## Challenge Experiments

### 🔥 Challenge 1: Create Your Own Custom Health Check
Edit `system_health_checker_v2.py` to add a new metric (like uptime), rebuild the image, and see it in the dashboard!

### 🔥 Challenge 2: Make the Dashboard Pretty
Edit `docker/dashboard/templates/dashboard.html` to change colors or add features!

### 🔥 Challenge 3: Add Another Service
Add a MongoDB container to the stack and configure the health checker to monitor it!

---

## Troubleshooting Commands

```bash
# Container won't start
docker logs devops-health-checker

# Check if ports are in use
netstat -ano | findstr :5000

# Remove everything and start fresh
docker-compose -f docker-compose-monitoring.yml down -v
docker system prune -a

# Check disk usage
docker system df

# See all containers (including stopped)
docker ps -a

# Restart the Docker daemon (if things are weird)
# Restart Docker Desktop from the system tray
```

---

## What You're Learning

By doing these experiments, you're mastering:

✅ Container lifecycle management
✅ Docker networking and DNS
✅ Volume management and persistence
✅ Container scaling
✅ Log aggregation and monitoring
✅ Health checks and recovery
✅ Inter-container communication
✅ Resource monitoring
✅ Troubleshooting techniques
✅ Production Docker patterns

**These are the exact skills used by DevOps engineers at companies like Netflix, Uber, and Spotify!**

---

## Keep Exploring!

Try breaking things, fixing them, and experimenting. That's how you truly learn Docker!

**Next**: Take what you learned and move to Phase 3 (CI/CD) or add your own features!
