# Python Automation Scripts

Collection of Python scripts for DevOps automation tasks.

## Scripts

### 1. System Health Checker V2 (`system_health_checker_v2.py`) ⭐ ENHANCED

**Purpose**: Production-ready system monitoring with email alerts and database checks

**New Features**:
- ✅ Email alerting for WARNING/CRITICAL states
- ✅ Database connectivity monitoring (PostgreSQL, MySQL, MongoDB, Redis)
- ✅ Configurable thresholds via JSON config
- ✅ Automated scheduling (cron/Task Scheduler)
- ✅ Historical report archiving
- ✅ Exit codes for CI/CD integration
- ✅ Command-line options (--quiet, --no-email)

**Core Monitoring**:
- CPU usage monitoring (total and per-core)
- Memory and swap usage tracking
- Disk usage for all mounted partitions
- Network I/O statistics
- Top CPU-consuming processes
- Overall health status (HEALTHY/WARNING/CRITICAL)

**Quick Start**:

```bash
# Install dependencies
pip install -r requirements.txt

# Create config file
cp config.example.json config.json
nano config.json  # Edit with your settings

# Run the enhanced health checker
python system_health_checker_v2.py

# Automated scheduling
cd ../bash
./schedule_health_check.sh       # Linux/macOS
.\schedule_health_check.ps1      # Windows (PowerShell)
```

**Configuration Example**:

```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "alerts@example.com",
    "recipient_emails": ["admin@example.com"]
  },
  "databases": {
    "check_enabled": true,
    "connections": [
      {
        "name": "Production DB",
        "type": "postgresql",
        "host": "localhost",
        "port": 5432
      }
    ]
  }
}
```

**📖 Complete Guide**: See [docs/HEALTH_CHECKER_GUIDE.md](../../docs/HEALTH_CHECKER_GUIDE.md)

---

### 2. System Health Checker (Basic) (`system_health_checker.py`)

**Purpose**: Simple system resource monitoring (beginner-friendly)

**Features**:
- CPU, memory, disk, and network monitoring
- JSON export
- No configuration required

**Usage**:

```bash
pip install psutil
python system_health_checker.py
```

**Use this if**: You want a simple, no-configuration monitoring script

---

## Requirements

- Python 3.7+
- psutil library

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Future Scripts

### Planned Additions:
- [ ] Log analyzer and parser
- [ ] Automated backup script
- [ ] Docker container manager
- [ ] CI/CD deployment helper
- [ ] SSL certificate checker
- [ ] Database backup automation
- [ ] Cloud resource cost calculator
- [ ] Git repository health checker

---

## Contributing

As this is a learning repository, feel free to suggest improvements or additional automation scripts!
"# DevOps-Learning-Repo" 
