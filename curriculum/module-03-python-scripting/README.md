# Module 3: Python Scripting for DevOps

**Duration**: 2 weeks (10-15 hours/week)
**Prerequisites**: Module 1 (DevOps Fundamentals), Module 2 (Linux & Git)
**Deliverable**: Suite of DevOps automation tools

---

## Overview

Python is the **lingua franca of DevOps**. When shell scripts get too complex, when you need to interact with APIs, when you want to build reusable tools - you reach for Python.

**Why Python for DevOps**:
- Easy to read and write (perfect for teams)
- Massive ecosystem (library for everything)
- Cross-platform (works on Linux, Windows, Mac)
- API-friendly (interact with AWS, GitHub, Slack, etc.)
- Standard in DevOps (Ansible, most CLI tools written in Python)

**By the end of this module, you'll**:
- Write Python scripts to automate DevOps tasks
- Parse and analyze log files
- Interact with REST APIs (AWS, GitHub, cloud services)
- Build command-line tools
- Handle errors gracefully
- Test your Python code

---

## Learning Objectives

### Python Fundamentals
- [ ] Variables, data types, and operators
- [ ] Control flow (if/else, loops)
- [ ] Functions and modules
- [ ] Lists, dictionaries, sets
- [ ] File I/O operations
- [ ] Exception handling

### DevOps-Specific Python
- [ ] System operations (subprocess, os, sys modules)
- [ ] Working with JSON and YAML
- [ ] HTTP requests and REST APIs
- [ ] Command-line argument parsing
- [ ] Logging and debugging
- [ ] Virtual environments and pip

### Practical Skills
- [ ] Parse log files and extract metrics
- [ ] Automate AWS/cloud operations
- [ ] Build CLI tools with argparse
- [ ] Schedule tasks with cron
- [ ] Send notifications (email, Slack)
- [ ] Test Python scripts

---

## Module Structure

### Week 1: Python Fundamentals for DevOps

**Lesson 1**: Why Python for DevOps (1 hour)
- The DevOps automation stack
- When to use shell vs. Python
- Python in the wild (Ansible, AWS CLI, tools)

**Lesson 2**: Python Crash Course (2 hours)
- Variables, types, operators
- Strings, lists, dictionaries
- Control flow (if/else, for, while)
- Functions and imports

**Lesson 3**: Working with Files and Systems (2 hours)
- Reading and writing files
- Directory operations
- Running shell commands from Python
- Environment variables
- Error handling

**Exercise 1**: Log File Parser
- Parse nginx/apache logs
- Extract IPs, status codes, response times
- Generate summary report

**Exercise 2**: System Health Monitor
- Check disk space
- Monitor CPU and memory
- Alert if thresholds exceeded
- Log results to file

### Week 2: APIs, CLIs, and Real DevOps Tools

**Lesson 4**: Working with APIs (2 hours)
- REST API fundamentals
- requests library
- Authentication (API keys, tokens)
- Handling JSON responses
- Error handling for APIs

**Lesson 5**: Building CLI Tools (2 hours)
- argparse for command-line arguments
- Click library (modern CLI framework)
- User input and validation
- Colorful output (rich, colorama)
- Configuration files

**Lesson 6**: Testing and Best Practices (1.5 hours)
- Writing testable code
- pytest basics
- Logging best practices
- Virtual environments
- Requirements.txt

**Exercise 3**: GitHub Repository Manager
- List repositories via GitHub API
- Create new repos
- Clone, pull, push automation
- Scheduled backups

**Exercise 4**: AWS Resource Auditor
- List EC2 instances
- Check for untagged resources
- Generate cost report
- Send Slack notification

**Exercise 5**: Deployment CLI Tool
- Command-line deployment tool
- Multiple environments (dev, staging, prod)
- Health checks
- Rollback capability

---

## Assessments

### Quiz (20 points, 80% to pass)
- Python basics (syntax, data structures)
- DevOps-specific concepts (APIs, subprocess)
- Scenario-based questions

### Project: DevOps Automation Suite (100 points)
Build a suite of 3 interconnected tools:

1. **Log Analyzer** (30 points)
   - Parse multiple log formats
   - Extract errors, warnings, metrics
   - Generate HTML report
   - Command-line interface

2. **Infrastructure Reporter** (40 points)
   - Query cloud resources (AWS/Azure)
   - Generate inventory report
   - Find security issues (unencrypted, public access)
   - Email/Slack alerts

3. **Deployment Automation** (30 points)
   - Deploy application to multiple environments
   - Run health checks
   - Automatic rollback on failure
   - Comprehensive logging

**Portfolio Quality**: Professional-grade tools you'd use in production

---

## Real-World Use Cases

### DevOps Engineers Use Python For:

**Infrastructure Automation**:
```python
# Provision AWS resources
import boto3
ec2 = boto3.resource('ec2')
instance = ec2.create_instances(
    ImageId='ami-12345',
    MinCount=1, MaxCount=1,
    InstanceType='t2.micro'
)
```

**Log Analysis**:
```python
# Find all 500 errors in nginx logs
import re
for line in open('/var/log/nginx/access.log'):
    if ' 500 ' in line:
        ip = re.search(r'(\d+\.\d+\.\d+\.\d+)', line).group(1)
        print(f"Error from {ip}")
```

**Deployment Scripts**:
```python
# Deploy to multiple servers
import subprocess
servers = ['web1', 'web2', 'web3']
for server in servers:
    subprocess.run(['ssh', server, 'sudo systemctl restart nginx'])
```

**Monitoring**:
```python
# Check disk space, alert if > 80%
import shutil
usage = shutil.disk_usage('/')
percent = usage.used / usage.total * 100
if percent > 80:
    send_alert(f"Disk {percent:.1f}% full!")
```

---

## Key Python Libraries for DevOps

| Library | Purpose | Example Use |
|---------|---------|-------------|
| **boto3** | AWS SDK | Manage AWS resources |
| **requests** | HTTP requests | Call REST APIs |
| **paramiko** | SSH | Connect to remote servers |
| **fabric** | Deployment | Run commands on multiple servers |
| **click** / **argparse** | CLI tools | Build command-line tools |
| **pytest** | Testing | Test your code |
| **pyyaml** | YAML | Parse config files |
| **jinja2** | Templates | Generate configs |
| **rich** | Terminal UI | Beautiful CLI output |
| **schedule** | Cron jobs | Schedule tasks |

---

## Time Commitment

| Activity | Time/Week |
|----------|-----------|
| Lessons | 4-5 hours |
| Exercises | 5-6 hours |
| Quiz + Project | 2-4 hours |
| **Total** | **11-15 hours** |

---

## Success Criteria

**You're ready to move on when you can**:
- [ ] Write Python scripts without constantly googling syntax
- [ ] Parse and process log files
- [ ] Make API calls and handle responses
- [ ] Build a CLI tool with proper arguments
- [ ] Handle errors gracefully
- [ ] Test your code
- [ ] Read and understand Python code
- [ ] Pass quiz with 80%+ (16/20)
- [ ] Complete automation suite project

---

## Resources

- [`cheat-sheet.md`](resources/cheat-sheet.md) - Python syntax reference
- [`api-examples.md`](resources/api-examples.md) - Common API patterns
- [`libraries.md`](resources/libraries.md) - Essential DevOps libraries

---

## Getting Started

### Step 1: Verify Python Installation

```bash
# Check Python version (3.9+ recommended)
python3 --version

# Or just 'python' on some systems
python --version
```

### Step 2: Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv ~/devops-venv

# Activate (Linux/Mac)
source ~/devops-venv/bin/activate

# Activate (Windows)
~/devops-venv/Scripts/activate

# Install common libraries
pip install requests boto3 click pytest pyyaml rich
```

### Step 3: Your First DevOps Script

Create `hello_devops.py`:
```python
#!/usr/bin/env python3
"""
Simple system info script
"""
import platform
import shutil

def main():
    print(f"System: {platform.system()}")
    print(f"Python: {platform.python_version()}")

    disk = shutil.disk_usage('/')
    used_gb = disk.used / (1024**3)
    total_gb = disk.total / (1024**3)

    print(f"Disk: {used_gb:.1f}GB / {total_gb:.1f}GB")

if __name__ == "__main__":
    main()
```

Run it:
```bash
chmod +x hello_devops.py
./hello_devops.py
```

---

## Common Pitfalls to Avoid

### Python-Specific
- ❌ Not using virtual environments (dependency conflicts)
- ❌ Hardcoding credentials in scripts
- ❌ Not handling errors (scripts crash on unexpected input)
- ❌ Using Python 2 (EOL since 2020)
- ✅ Use venv for each project
- ✅ Use environment variables for secrets
- ✅ Always use try/except for external calls
- ✅ Use Python 3.9+

### DevOps-Specific
- ❌ Writing shell commands in Python when shell is simpler
- ❌ Not logging script actions
- ❌ Not testing scripts before production
- ✅ Use shell for simple one-liners
- ✅ Log everything to file
- ✅ Test with sample data first

---

## Module Dependencies

**Builds on**:
- Module 1: DevOps thinking (automate toil)
- Module 2: Linux commands (Python calls these via subprocess)
- Module 2: Git (version control your scripts)

**Prepares for**:
- Module 4: Docker (Dockerfiles are Python-like)
- Module 5: CI/CD (pipelines often use Python)
- Module 6: Terraform/Ansible (Ansible is Python-based)
- All future modules (Python glues everything together)

---

## Career Impact

**After this module, you can**:
- Apply for positions requiring Python scripting
- Automate 50-80% of repetitive DevOps tasks
- Build custom tools for your team
- Contribute to open-source DevOps projects
- Interview confidently about automation

**Job titles this unlocks**:
- DevOps Engineer (most require Python)
- Automation Engineer
- Site Reliability Engineer
- Cloud Engineer

---

## Let's Begin!

**Your learning path**:
1. Start with `lessons/lesson-01-why-python.md`
2. Complete exercises as you learn
3. Build the automation suite project
4. Take quiz when ready
5. Use flashcards for retention

**Remember**: Python is a tool, not the goal. The goal is automation. Python helps you get there.

**Ready to automate everything?** 🐍
