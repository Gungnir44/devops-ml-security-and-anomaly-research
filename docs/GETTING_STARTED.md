# Getting Started with DevOps

Welcome to your DevOps learning journey! This guide will help you set up your environment and start building.

---

## Prerequisites

### Essential Tools

1. **Git** - Version control
   - Install: https://git-scm.com/downloads
   - Verify: `git --version`

2. **Python 3.7+** - Scripting and automation
   - Install: https://www.python.org/downloads/
   - Verify: `python --version`

3. **Docker** - Containerization
   - Install: https://docs.docker.com/get-docker/
   - Verify: `docker --version`

4. **Text Editor/IDE**
   - VS Code (recommended): https://code.visualstudio.com/
   - Or your preferred editor

---

## Environment Setup

### 1. Clone This Repository

```bash
cd ~/projects
git clone <your-repo-url>
cd DevOps\ Project
```

### 2. Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r scripts/python/requirements.txt
```

### 3. Verify Docker Installation

```bash
docker run hello-world
```

---

## Your First DevOps Task

### Run the System Health Checker

1. Navigate to the scripts directory:
```bash
cd scripts/python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the script:
```bash
python system_health_checker.py
```

4. Check the generated report:
```bash
cat system_health_report.json
```

### Build and Run with Docker

1. Navigate to project root:
```bash
cd ../..
```

2. Build the Docker image:
```bash
docker build -t devops-health-checker -f docker/Dockerfile .
```

3. Run the container:
```bash
docker run --rm devops-health-checker
```

---

## Learning Path

### Week 1-2: Foundation
- [ ] Complete Linux command line basics
- [ ] Master Git workflow (commit, branch, merge)
- [ ] Write 3 automation scripts in Python
- [ ] Learn basic networking concepts

**Resources**:
- Linux Journey: https://linuxjourney.com/
- Git Interactive Tutorial: https://learngitbranching.js.org/

### Week 3-4: Containerization
- [ ] Complete Docker tutorial
- [ ] Containerize a simple web application
- [ ] Learn Docker Compose
- [ ] Build multi-container application

**Resources**:
- Docker Getting Started: https://docs.docker.com/get-started/

### Week 5-6: CI/CD
- [ ] Set up GitHub Actions workflow
- [ ] Implement automated testing
- [ ] Deploy to staging environment
- [ ] Learn deployment strategies

**Resources**:
- GitHub Actions Docs: https://docs.github.com/en/actions

---

## Daily Practice Routine

1. **Morning (30 min)**: Read DevOps articles/documentation
2. **Afternoon (1-2 hours)**: Hands-on project work
3. **Evening (30 min)**: Document what you learned

---

## Useful Commands

### Git
```bash
git status                  # Check repository status
git add .                   # Stage all changes
git commit -m "message"     # Commit changes
git push origin main        # Push to remote
git log --oneline           # View commit history
```

### Docker
```bash
docker ps                   # List running containers
docker images               # List images
docker build -t name .      # Build image
docker run image            # Run container
docker logs container_id    # View logs
docker exec -it id bash     # Enter container
```

### Python
```bash
python script.py            # Run script
pip install package         # Install package
pip freeze > requirements.txt  # Save dependencies
```

---

## Troubleshooting

### Python Script Issues
- Ensure virtual environment is activated
- Check dependencies are installed: `pip list`
- Verify Python version: `python --version`

### Docker Issues
- Check Docker is running: `docker info`
- On Windows, ensure WSL2 is set up
- Clear cache: `docker system prune`

### Git Issues
- Set up credentials: `git config --global user.name "Your Name"`
- Check remote: `git remote -v`

---

## Next Steps

1. Complete the system health checker project
2. Add a new automation script
3. Learn about Docker networking
4. Start planning your first CI/CD pipeline

---

## Resources

### Documentation
- [Official DevOps Handbook](https://www.atlassian.com/devops)
- [The Twelve-Factor App](https://12factor.net/)
- [Cloud Native Computing Foundation](https://www.cncf.io/)

### Communities
- r/devops on Reddit
- DevOps Discord servers
- Local tech meetups

### Books
- "The Phoenix Project" by Gene Kim
- "The DevOps Handbook" by Gene Kim
- "Site Reliability Engineering" by Google (free online)

---

**Remember**: DevOps is a journey, not a destination. Focus on continuous learning and improvement!

Happy Learning!
