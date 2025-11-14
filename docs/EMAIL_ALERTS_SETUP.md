# Email Alerts Setup Guide

Configure email notifications for system health alerts.

---

## Gmail Setup (Recommended for Testing)

### Step 1: Enable 2-Factor Authentication

1. Go to your Google Account: https://myaccount.google.com/
2. Click **Security** (left sidebar)
3. Under "How you sign in to Google", click **2-Step Verification**
4. Follow the prompts to enable it

### Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
   - Or: Google Account → Security → App Passwords
2. Select app: **Mail**
3. Select device: **Other (Custom name)**
4. Enter name: "DevOps Health Checker"
5. Click **Generate**
6. **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)

### Step 3: Update Config

Edit `scripts/python/config.json`:

```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your-email@gmail.com",
    "sender_password": "abcd efgh ijkl mnop",
    "recipient_emails": [
      "your-email@gmail.com",
      "oncall@example.com"
    ],
    "alert_on": ["WARNING", "CRITICAL"]
  }
}
```

Replace:
- `your-email@gmail.com` with your actual Gmail address
- `abcd efgh ijkl mnop` with the app password you generated
- Add recipient emails (can send to multiple people)

### Step 4: Test It!

```bash
# Copy config to container
docker cp "C:\Users\joshu\Desktop\DevOps Project\scripts\python\config.json" devops-health-checker:/app/config.json

# Restart the health checker to pick up new config
docker restart devops-health-checker

# Manually trigger to test (won't send email if system is HEALTHY)
docker exec devops-health-checker python system_health_checker_v2.py
```

**To test email alerts**: You need to trigger a WARNING or CRITICAL state. See "Testing Email Alerts" below.

---

## Other Email Providers

### Outlook / Office 365

```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.office365.com",
    "smtp_port": 587,
    "sender_email": "your-email@outlook.com",
    "sender_password": "your-password",
    "recipient_emails": ["alerts@example.com"]
  }
}
```

### Yahoo Mail

```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.mail.yahoo.com",
    "smtp_port": 587,
    "sender_email": "your-email@yahoo.com",
    "sender_password": "your-app-password",
    "recipient_emails": ["alerts@example.com"]
  }
}
```

**Note**: Yahoo also requires an app-specific password, not your regular password.

### Custom SMTP Server

```json
{
  "email": {
    "enabled": true,
    "smtp_server": "mail.yourcompany.com",
    "smtp_port": 587,
    "sender_email": "noreply@yourcompany.com",
    "sender_password": "smtp-password",
    "recipient_emails": ["devops-team@yourcompany.com"]
  }
}
```

---

## Testing Email Alerts

Since your system is currently HEALTHY, you won't receive emails. Here's how to test:

### Method 1: Lower Thresholds (Easiest)

Temporarily lower the alert thresholds to trigger a WARNING:

```json
{
  "thresholds": {
    "cpu_warning": 1,      // Alert at 1% CPU (will trigger!)
    "cpu_critical": 5,
    "memory_warning": 5,   // Alert at 5% memory (will trigger!)
    "memory_critical": 10,
    "disk_warning": 1,     // Alert at 1% disk (will trigger!)
    "disk_critical": 5
  }
}
```

Then run:
```bash
docker cp "C:\Users\joshu\Desktop\DevOps Project\scripts\python\config.json" devops-health-checker:/app/config.json
docker exec devops-health-checker python system_health_checker_v2.py
```

You should receive an email alert!

**Remember to change the thresholds back to normal after testing!**

### Method 2: Simulate Database Failure

Stop a database and watch it get detected:

```bash
# Stop PostgreSQL
docker stop devops-postgres

# Run health check
docker exec devops-health-checker python system_health_checker_v2.py

# You'll see: PostgreSQL Demo - FAILED

# Restart it
docker start devops-postgres
```

### Method 3: Test Script

Create a test that always triggers an alert:

```bash
# Run with debug mode
docker exec devops-health-checker python -c "
from system_health_checker_v2 import *
import json

# Create checker
checker = SystemHealthChecker()
checker.collect_all_metrics()

# Force CRITICAL status for testing
checker.health_data['overall_health'] = 'CRITICAL'

# Try to send email
result = checker.send_alert()
print(result)
"
```

---

## Email Alert Contents

When an alert is triggered, you'll receive an HTML email with:

### Subject Line
```
[CRITICAL] System Health Alert - health-checker-container
```
or
```
[WARNING] System Health Alert - health-checker-container
```

### Email Body Includes:
- Overall health status (color-coded)
- CPU usage and status
- Memory usage and status
- Disk usage for all partitions
- Database connectivity status
- Top CPU-consuming processes
- Timestamp and hostname

### Example Email Preview:
```
System Health Alert
health-checker-container
Status: CRITICAL

Timestamp: 2025-11-14T16:30:00.000000

CPU - CRITICAL
Usage: 95%
Cores: 4 logical (2 physical)

Memory - WARNING
Used: 6.5 GB / 7.68 GB (85%)
Available: 1.18 GB

...
```

---

## Troubleshooting

### "Authentication failed"

**Gmail**: Make sure you're using an **app password**, not your regular Gmail password.

**Yahoo**: Same - you need an app-specific password.

**Outlook**: Regular password should work, but check if 2FA is enabled.

### "Connection refused" or "Timeout"

- Check your SMTP server and port
- Make sure your firewall isn't blocking port 587
- Try port 465 (SSL) instead of 587 (TLS)

### Test SMTP Connection

```python
docker exec devops-health-checker python -c "
import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your-email@gmail.com', 'your-app-password')
    print('SUCCESS: SMTP connection works!')
    server.quit()
except Exception as e:
    print(f'ERROR: {e}')
"
```

### No Email Received (But No Errors)

1. **Check spam folder** - first-time emails often go to spam
2. **Verify alert_on setting** - must include "WARNING" or "CRITICAL"
3. **Check system status** - emails only sent when thresholds exceeded
4. **Check recipient emails** - verify they're correct

### "TLS/SSL Error"

Try using port 465 with SSL:

```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 465,  // SSL port
  ...
}
```

---

## Alert Frequency

By default, the health checker runs every 5 minutes. This means:
- Maximum alert frequency: Every 5 minutes
- If system recovers, next check won't send an alert

To change frequency, edit `docker-compose-monitoring.yml`:

```yaml
command: >
  sh -c "while true; do
    python system_health_checker_v2.py --config /app/config.json;
    sleep 60;  # Change to 60 for every minute
  done"
```

---

## Production Considerations

### 1. Use Environment Variables for Secrets

Instead of storing passwords in config.json:

```python
import os

config['email']['sender_password'] = os.getenv('EMAIL_PASSWORD')
```

### 2. Alert Deduplication

Prevent alert spam by tracking alert state:
- Only alert when state changes (HEALTHY → WARNING)
- Don't alert on every check while in WARNING state

### 3. Multiple Recipients

```json
"recipient_emails": [
  "oncall-primary@example.com",
  "oncall-backup@example.com",
  "devops-team@example.com"
]
```

### 4. Alert Escalation

- WARNING: Email to team
- CRITICAL: Email + SMS (integrate with Twilio)
- Or use PagerDuty/OpsGenie for professional alerting

---

## Next Steps

After email alerts, consider:

1. **Slack Webhooks** - Send alerts to Slack channels
2. **Discord Webhooks** - Alert your Discord server
3. **PagerDuty Integration** - Professional on-call management
4. **SMS Alerts** - Use Twilio for critical issues

---

## Quick Reference

### Enable Email Alerts
```json
"enabled": true
```

### Test Configuration
```bash
docker exec devops-health-checker python system_health_checker_v2.py
```

### View Logs
```bash
docker logs devops-health-checker | grep EMAIL
```

### Disable Alerts Temporarily
```json
"enabled": false
```

or run with flag:
```bash
docker exec devops-health-checker python system_health_checker_v2.py --no-email
```

---

**Security Note**: Never commit config.json with real passwords to GitHub! The .gitignore already excludes it.
