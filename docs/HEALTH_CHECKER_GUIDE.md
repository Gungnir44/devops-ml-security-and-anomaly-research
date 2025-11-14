# System Health Checker V2 - Complete Guide

The enhanced system health checker is a production-ready DevOps monitoring tool with email alerting, database connectivity checks, and automated scheduling.

---

## Features

### Core Monitoring
- **CPU Usage**: Total and per-core monitoring
- **Memory**: RAM and swap usage tracking
- **Disk**: Multi-partition usage monitoring
- **Network**: I/O statistics and interface information
- **Processes**: Top CPU-consuming processes

### Advanced Features
- **Email Alerts**: Automatic notifications for WARNING/CRITICAL states
- **Database Checks**: Monitor connectivity to PostgreSQL, MySQL, MongoDB, Redis
- **Configurable Thresholds**: Customize WARNING and CRITICAL levels
- **Automated Scheduling**: Cron (Linux) and Task Scheduler (Windows) support
- **Historical Reports**: Optional timestamped report archives
- **Exit Codes**: Proper status codes for CI/CD integration

---

## Installation

### 1. Install Python Dependencies

```bash
cd scripts/python
pip install -r requirements.txt
```

### 2. Install Optional Database Drivers

Only install drivers for databases you want to monitor:

```bash
# PostgreSQL
pip install psycopg2-binary

# MySQL
pip install pymysql

# MongoDB
pip install pymongo

# Redis
pip install redis
```

### 3. Create Configuration File

```bash
# Copy the example config
cp config.example.json config.json

# Edit with your settings
nano config.json  # or use your preferred editor
```

---

## Configuration

### Basic Configuration (`config.json`)

```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your-email@gmail.com",
    "sender_password": "your-app-password",
    "recipient_emails": ["admin@example.com"],
    "alert_on": ["WARNING", "CRITICAL"]
  },
  "thresholds": {
    "cpu_warning": 60,
    "cpu_critical": 80,
    "memory_warning": 60,
    "memory_critical": 80,
    "disk_warning": 60,
    "disk_critical": 80
  },
  "databases": {
    "check_enabled": true,
    "connections": [
      {
        "name": "Production DB",
        "type": "postgresql",
        "host": "localhost",
        "port": 5432,
        "database": "mydb",
        "user": "dbuser",
        "password": "dbpass",
        "timeout": 5
      }
    ]
  },
  "monitoring": {
    "report_path": "./reports",
    "keep_history": true,
    "history_days": 30
  }
}
```

### Email Configuration

#### Gmail Setup

1. Enable 2-factor authentication on your Google account
2. Generate an App Password:
   - Go to Google Account → Security → App Passwords
   - Create a new app password for "Mail"
3. Use the app password in `sender_password`

**Example**:
```json
"email": {
  "enabled": true,
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your-email@gmail.com",
  "sender_password": "abcd efgh ijkl mnop",
  "recipient_emails": ["admin@example.com", "oncall@example.com"],
  "alert_on": ["CRITICAL"]
}
```

#### Other Email Providers

**Outlook/Office 365**:
```json
"smtp_server": "smtp.office365.com",
"smtp_port": 587
```

**Yahoo**:
```json
"smtp_server": "smtp.mail.yahoo.com",
"smtp_port": 587
```

**Custom SMTP**:
```json
"smtp_server": "mail.yourcompany.com",
"smtp_port": 587
```

### Threshold Configuration

Adjust thresholds based on your system's normal operating conditions:

```json
"thresholds": {
  "cpu_warning": 70,     # Alert at 70% CPU
  "cpu_critical": 90,    # Critical at 90% CPU
  "memory_warning": 75,
  "memory_critical": 90,
  "disk_warning": 80,
  "disk_critical": 95
}
```

### Database Configuration

Add as many database connections as needed:

```json
"databases": {
  "check_enabled": true,
  "connections": [
    {
      "name": "Production PostgreSQL",
      "type": "postgresql",
      "host": "db.example.com",
      "port": 5432,
      "database": "prod_db",
      "user": "readonly_user",
      "password": "secure_password",
      "timeout": 5
    },
    {
      "name": "Cache Redis",
      "type": "redis",
      "host": "redis.example.com",
      "port": 6379,
      "timeout": 3
    }
  ]
}
```

**Supported Database Types**:
- `postgresql`
- `mysql`
- `mongodb`
- `redis`

---

## Usage

### Basic Usage

```bash
python system_health_checker_v2.py
```

### With Custom Config

```bash
python system_health_checker_v2.py --config /path/to/config.json
```

### Disable Email for One Run

```bash
python system_health_checker_v2.py --no-email
```

### Quiet Mode (No Console Output)

```bash
python system_health_checker_v2.py --quiet
```

### Help

```bash
python system_health_checker_v2.py --help
```

---

## Automated Scheduling

### Linux/macOS (Cron)

Run the setup script:

```bash
cd scripts/bash
chmod +x schedule_health_check.sh
./schedule_health_check.sh
```

The script will:
1. Create a wrapper script for cron
2. Show you cron job options
3. Optionally add to your crontab

**Manual cron setup**:

```bash
# Edit crontab
crontab -e

# Add one of these lines:

# Every 5 minutes
*/5 * * * * /path/to/DevOps\ Project/scripts/bash/run_health_check.sh >> /path/to/logs/health_check.log 2>&1

# Every hour
0 * * * * /path/to/DevOps\ Project/scripts/bash/run_health_check.sh >> /path/to/logs/health_check.log 2>&1

# Daily at 6 AM
0 6 * * * /path/to/DevOps\ Project/scripts/bash/run_health_check.sh >> /path/to/logs/health_check.log 2>&1
```

**View logs**:
```bash
tail -f logs/health_check.log
```

### Windows (Task Scheduler)

Run the PowerShell setup script as Administrator:

```powershell
cd scripts\bash
.\schedule_health_check.ps1 -Frequency 15min
```

**Frequency options**:
- `5min` - Every 5 minutes
- `15min` - Every 15 minutes
- `hourly` - Every hour
- `daily` - Daily at 6:00 AM

**Manual Task Scheduler setup**:

1. Open Task Scheduler (taskschd.msc)
2. Create Basic Task
3. Name: "DevOps Health Check"
4. Trigger: Set your schedule
5. Action: Start a program
6. Program: `cmd.exe`
7. Arguments: `/c "C:\path\to\scripts\bash\run_health_check.bat" >> "C:\path\to\logs\health_check.log" 2>&1`

**Manage the task**:
```powershell
# View task
Get-ScheduledTask -TaskName "DevOps-HealthCheck"

# Run now
Start-ScheduledTask -TaskName "DevOps-HealthCheck"

# View logs
Get-Content logs\health_check.log -Tail 50 -Wait
```

---

## Output & Reports

### Console Output

```
================================================================================
SYSTEM HEALTH REPORT - 2025-11-14T10:30:00.000000
================================================================================

OVERALL HEALTH: HEALTHY

--------------------------------------------------------------------------------
SYSTEM INFORMATION
--------------------------------------------------------------------------------
  Hostname: Valhalla
  Platform: Windows
  ...

--------------------------------------------------------------------------------
CPU - HEALTHY
--------------------------------------------------------------------------------
  Physical Cores: 2
  Logical Cores: 4
  Total Usage: 15.3%

--------------------------------------------------------------------------------
DATABASE CONNECTIVITY
--------------------------------------------------------------------------------
  ✓ Production DB (postgresql) - CONNECTED
    Host: localhost:5432 | Connection successful
  ✗ Dev MySQL (mysql) - FAILED
    Host: localhost:3306 | Connection refused
```

### JSON Report

Reports are saved to the configured `report_path`:

```json
{
  "timestamp": "2025-11-14T10:30:00.000000",
  "system": {
    "hostname": "Valhalla",
    "platform": "Windows"
  },
  "cpu": {
    "cpu_percent_total": 15.3,
    "status": "HEALTHY"
  },
  "databases": [
    {
      "name": "Production DB",
      "type": "postgresql",
      "status": "CONNECTED"
    }
  ],
  "overall_health": "HEALTHY"
}
```

### Email Alerts

When system reaches WARNING or CRITICAL state, an HTML email is sent with:
- Colored status indicators
- Detailed metrics tables
- Top processes
- Database status
- Timestamp and hostname

---

## Exit Codes

The script returns standard exit codes for integration:

- **0**: System is HEALTHY
- **1**: System is in WARNING state
- **2**: System is in CRITICAL state
- **130**: Interrupted by user (Ctrl+C)

**Use in scripts**:
```bash
python system_health_checker_v2.py --quiet
EXIT_CODE=$?

if [ $EXIT_CODE -eq 2 ]; then
    echo "CRITICAL! Taking action..."
elif [ $EXIT_CODE -eq 1 ]; then
    echo "WARNING! Monitoring closely..."
fi
```

---

## Integration Examples

### CI/CD Pipeline

**GitHub Actions**:
```yaml
name: Health Check

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Health Check
        run: |
          pip install psutil
          python scripts/python/system_health_checker_v2.py --config config.json
```

### Docker Container

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY scripts/python/ .
RUN pip install -r requirements.txt

CMD ["python", "system_health_checker_v2.py"]
```

### Monitoring Dashboard

Parse JSON reports for visualization:

```python
import json

with open('system_health_report.json') as f:
    data = json.load(f)

if data['overall_health'] == 'CRITICAL':
    # Send to Slack, PagerDuty, etc.
    send_alert(data)
```

---

## Troubleshooting

### Email Not Sending

**Check credentials**:
```python
import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your-email@gmail.com', 'your-app-password')
print("Login successful!")
```

**Common issues**:
- Using regular password instead of app password (Gmail)
- Firewall blocking port 587
- 2FA not enabled on Google account

### Database Connection Fails

**Test connection manually**:
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="mydb",
    user="dbuser",
    password="dbpass"
)
print("Connected!")
```

**Common issues**:
- Database not running
- Firewall blocking port
- Wrong credentials
- Database driver not installed

### Cron Job Not Running

**Check cron logs**:
```bash
# Linux
grep CRON /var/log/syslog

# View your cron jobs
crontab -l
```

**Common issues**:
- Script not executable: `chmod +x run_health_check.sh`
- Wrong path in crontab
- Python not in PATH

---

## Security Best Practices

1. **Never commit config.json with real credentials**
   - Use `config.example.json` as template
   - Add `config.json` to `.gitignore` (already done)

2. **Use read-only database users**
   ```sql
   -- PostgreSQL example
   CREATE USER readonly WITH PASSWORD 'secure_password';
   GRANT CONNECT ON DATABASE mydb TO readonly;
   GRANT USAGE ON SCHEMA public TO readonly;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
   ```

3. **Restrict file permissions**
   ```bash
   chmod 600 config.json  # Only owner can read/write
   ```

4. **Use environment variables for sensitive data**
   ```python
   import os
   config['email']['sender_password'] = os.getenv('EMAIL_PASSWORD')
   ```

5. **Encrypt email passwords**
   - Use a secrets manager (HashiCorp Vault, AWS Secrets Manager)
   - Or use keyring: `pip install keyring`

---

## What You Learned (DevOps Concepts)

### Monitoring & Observability
- System metrics collection
- Health status thresholds
- Alert fatigue prevention (WARNING vs CRITICAL)

### Alerting
- SMTP email integration
- Alert routing and escalation
- HTML notification formatting

### Database Operations
- Connection health checking
- Timeout handling
- Multi-database support

### Automation
- Cron job scheduling
- Windows Task Scheduler
- Log rotation and management

### Configuration Management
- External configuration files
- Environment-specific settings
- Secrets handling

### Production Readiness
- Exit codes for automation
- Error handling and logging
- Quiet mode for cron jobs

---

## Next Steps

1. **Integrate with Monitoring Stack**
   - Send metrics to Prometheus
   - Visualize in Grafana
   - Set up alerting rules

2. **Add More Checks**
   - HTTP endpoint availability
   - SSL certificate expiration
   - Backup verification
   - Service status (systemd/services)

3. **Enhance Alerting**
   - Slack/Discord webhooks
   - PagerDuty integration
   - SMS alerts (Twilio)
   - Alert grouping/deduplication

4. **Build a Dashboard**
   - Web interface to view reports
   - Historical trending
   - Multi-server monitoring

---

## Resources

- [psutil Documentation](https://psutil.readthedocs.io/)
- [Cron Expression Guide](https://crontab.guru/)
- [Gmail SMTP Guide](https://support.google.com/a/answer/176600)
- [Site Reliability Engineering (SRE) Book](https://sre.google/sre-book/monitoring-distributed-systems/)

---

**Version**: 2.0
**Last Updated**: November 14, 2025
**Author**: Joshua
