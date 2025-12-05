# Lesson 3: Shell Scripting Basics

**Duration**: 2 hours
**Objectives**: Automate Linux tasks with bash scripts

---

## Why Shell Scripting?

**The Manual Way** (10 minutes of typing):
```bash
# Deploy app to 5 servers
ssh web1 "cd /var/www && git pull && sudo systemctl restart nginx"
ssh web2 "cd /var/www && git pull && sudo systemctl restart nginx"
ssh web3 "cd /var/www && git pull && sudo systemctl restart nginx"
ssh web4 "cd /var/www && git pull && sudo systemctl restart nginx"
ssh web5 "cd /var/www && git pull && sudo systemctl restart nginx"
```

**The Script Way** (1 command):
```bash
./deploy.sh
# Deploys to all 5 servers in 30 seconds
```

**Shell scripts are for**:
- Tasks you repeat (deployments, backups, monitoring)
- Tasks involving multiple commands
- Tasks needing logic (if/else, loops)

**Shell scripts are NOT for**:
- Complex data processing (use Python)
- Cross-platform needs (use Python)
- Long-running services (use proper programming language)

---

## Your First Script

Create `hello.sh`:
```bash
#!/bin/bash
# Simple greeting script

echo "Hello, DevOps!"
echo "Today is: $(date)"
echo "Current user: $(whoami)"
echo "Working directory: $(pwd)"
```

Make executable and run:
```bash
chmod +x hello.sh
./hello.sh
```

**Key Elements**:
- `#!/bin/bash` - Shebang (tells OS to use bash)
- `#` - Comments (everything after # is ignored)
- `echo` - Print to screen
- `$()` - Command substitution (run command, use output)

---

## Variables

### Basic Variables
```bash
#!/bin/bash

# Define variables (no spaces around =!)
NAME="Joshua"
AGE=25
SERVER="web-prod-01"

# Use variables with $
echo "Hello, $NAME"
echo "You are $AGE years old"
echo "Deploying to $SERVER"
```

### Command Output as Variable
```bash
#!/bin/bash

# Store command output
CURRENT_DATE=$(date +%Y-%m-%d)
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}')
HOSTNAME=$(hostname)

echo "Backup-$CURRENT_DATE.tar.gz"
echo "Disk usage: $DISK_USAGE"
echo "Running on: $HOSTNAME"
```

### User Input
```bash
#!/bin/bash

echo "What's your name?"
read USERNAME

echo "Hello, $USERNAME!"
```

### Special Variables
```bash
#!/bin/bash

echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "All arguments: $@"
echo "Number of arguments: $#"
echo "Exit code of last command: $?"
```

Run: `./script.sh arg1 arg2 arg3`

---

## Conditionals (if/else)

### Basic If Statement
```bash
#!/bin/bash

DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')

if [ $DISK_USAGE -gt 80 ]; then
    echo "WARNING: Disk usage is ${DISK_USAGE}%!"
    echo "Cleaning up old logs..."
    # Add cleanup commands
else
    echo "Disk usage OK: ${DISK_USAGE}%"
fi
```

### If-Elif-Else
```bash
#!/bin/bash

HOUR=$(date +%H)

if [ $HOUR -lt 12 ]; then
    echo "Good morning!"
elif [ $HOUR -lt 18 ]; then
    echo "Good afternoon!"
else
    echo "Good evening!"
fi
```

### File Tests
```bash
#!/bin/bash

FILE="/var/log/app.log"

if [ -f "$FILE" ]; then
    echo "File exists"
    if [ -r "$FILE" ]; then
        echo "File is readable"
    fi
    if [ -w "$FILE" ]; then
        echo "File is writable"
    fi
else
    echo "File does not exist"
fi
```

### Common Test Operators

**Numeric Comparisons**:
- `-eq`: equal (`[ $a -eq $b ]`)
- `-ne`: not equal
- `-gt`: greater than
- `-lt`: less than
- `-ge`: greater than or equal
- `-le`: less than or equal

**String Comparisons**:
- `=`: equal (`[ "$a" = "$b" ]`)
- `!=`: not equal
- `-z`: string is empty (`[ -z "$a" ]`)
- `-n`: string is not empty

**File Tests**:
- `-f`: file exists and is regular file
- `-d`: directory exists
- `-r`: file is readable
- `-w`: file is writable
- `-x`: file is executable
- `-e`: file exists (any type)

---

## Loops

### For Loop (Fixed List)
```bash
#!/bin/bash

# Loop through list
for SERVER in web1 web2 web3 web4 web5; do
    echo "Deploying to $SERVER"
    ssh $SERVER "sudo systemctl restart nginx"
done

# Loop through files
for FILE in *.log; do
    echo "Processing $FILE"
    gzip "$FILE"
done

# Loop through range
for i in {1..10}; do
    echo "Number: $i"
done
```

### While Loop (Condition-Based)
```bash
#!/bin/bash

# Loop while condition is true
COUNT=1
while [ $COUNT -le 5 ]; do
    echo "Attempt $COUNT"
    COUNT=$((COUNT + 1))
    sleep 1
done

# Read file line by line
while read LINE; do
    echo "Processing: $LINE"
done < input.txt
```

### Loop Control
```bash
#!/bin/bash

for i in {1..10}; do
    if [ $i -eq 5 ]; then
        continue  # Skip 5
    fi

    if [ $i -eq 8 ]; then
        break  # Stop at 8
    fi

    echo "Number: $i"
done
```

---

## Functions

### Basic Function
```bash
#!/bin/bash

# Define function
greet() {
    echo "Hello, $1!"
}

# Call function
greet "Joshua"
greet "Alice"
```

### Function with Return Value
```bash
#!/bin/bash

check_service() {
    SERVICE=$1

    if systemctl is-active --quiet $SERVICE; then
        return 0  # Success (running)
    else
        return 1  # Failure (not running)
    fi
}

# Use function
if check_service nginx; then
    echo "nginx is running"
else
    echo "nginx is NOT running"
fi
```

### Function with Output
```bash
#!/bin/bash

get_disk_usage() {
    df -h / | tail -1 | awk '{print $5}'
}

# Capture output
USAGE=$(get_disk_usage)
echo "Disk usage: $USAGE"
```

---

## Real DevOps Scripts

### Script 1: Backup Script
```bash
#!/bin/bash
# backup.sh - Backup important directories

# Configuration
BACKUP_DIR="/backup"
DATE=$(date +%Y-%m-%d-%H%M%S)
BACKUP_NAME="backup-$DATE.tar.gz"

# Directories to backup
DIRS_TO_BACKUP="/var/www /etc/nginx /home"

# Create backup directory if doesn't exist
mkdir -p "$BACKUP_DIR"

echo "Starting backup at $(date)"
echo "Backup name: $BACKUP_NAME"

# Create backup
tar -czf "$BACKUP_DIR/$BACKUP_NAME" $DIRS_TO_BACKUP

# Check if backup succeeded
if [ $? -eq 0 ]; then
    echo "Backup completed successfully!"
    echo "Size: $(du -h $BACKUP_DIR/$BACKUP_NAME | cut -f1)"
else
    echo "ERROR: Backup failed!"
    exit 1
fi

# Delete backups older than 7 days
echo "Cleaning old backups..."
find "$BACKUP_DIR" -name "backup-*.tar.gz" -mtime +7 -delete

echo "Backup finished at $(date)"
```

### Script 2: Health Check Script
```bash
#!/bin/bash
# health_check.sh - Monitor system health

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=== System Health Check ==="
echo "Date: $(date)"
echo

# Check disk space
echo "1. Disk Space:"
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 90 ]; then
    echo -e "${RED}CRITICAL: Disk ${DISK_USAGE}% full!${NC}"
elif [ $DISK_USAGE -gt 80 ]; then
    echo -e "${YELLOW}WARNING: Disk ${DISK_USAGE}% full${NC}"
else
    echo -e "${GREEN}OK: Disk ${DISK_USAGE}% full${NC}"
fi
echo

# Check memory
echo "2. Memory:"
MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
if [ $MEM_USAGE -gt 90 ]; then
    echo -e "${RED}CRITICAL: Memory ${MEM_USAGE}% used!${NC}"
elif [ $MEM_USAGE -gt 80 ]; then
    echo -e "${YELLOW}WARNING: Memory ${MEM_USAGE}% used${NC}"
else
    echo -e "${GREEN}OK: Memory ${MEM_USAGE}% used${NC}"
fi
echo

# Check services
echo "3. Services:"
for SERVICE in nginx mysql redis-server; do
    if systemctl is-active --quiet $SERVICE 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $SERVICE is running"
    else
        echo -e "${RED}✗${NC} $SERVICE is NOT running"
    fi
done
```

### Script 3: Deployment Script
```bash
#!/bin/bash
# deploy.sh - Deploy application

set -e  # Exit on any error

# Configuration
APP_DIR="/var/www/myapp"
BACKUP_DIR="/var/backups/app"
GIT_REPO="https://github.com/user/myapp.git"
BRANCH="main"

echo "=== Deployment Started ==="

# Backup current version
echo "Creating backup..."
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/backup-$TIMESTAMP.tar.gz" "$APP_DIR"

# Pull latest code
echo "Pulling latest code..."
cd "$APP_DIR"
git fetch origin
git checkout "$BRANCH"
git pull origin "$BRANCH"

# Install dependencies
echo "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Run database migrations
echo "Running migrations..."
if [ -f "manage.py" ]; then
    python manage.py migrate
fi

# Restart services
echo "Restarting services..."
sudo systemctl restart myapp
sudo systemctl restart nginx

# Health check
echo "Running health check..."
sleep 5
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/)

if [ "$RESPONSE" = "200" ]; then
    echo "✓ Deployment successful!"
else
    echo "✗ Health check failed! Rolling back..."
    tar -xzf "$BACKUP_DIR/backup-$TIMESTAMP.tar.gz" -C /
    sudo systemctl restart myapp
    exit 1
fi

echo "=== Deployment Complete ==="
```

---

## Error Handling

### Exit on Error
```bash
#!/bin/bash
set -e  # Exit immediately if any command fails
set -u  # Treat unset variables as error
set -o pipefail  # Pipe fails if any command in pipe fails

# Now script will stop on first error
command1
command2
command3
```

### Manual Error Checking
```bash
#!/bin/bash

# Check if command succeeded
cp important.txt backup.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to copy file"
    exit 1
fi

# Or use && and ||
cp file1.txt file2.txt && echo "Success" || echo "Failed"
```

### Trap (Cleanup on Exit)
```bash
#!/bin/bash

# Cleanup function
cleanup() {
    echo "Cleaning up temporary files..."
    rm -f /tmp/myapp-*
}

# Run cleanup on exit (success or failure)
trap cleanup EXIT

# Your script here
echo "Running script..."
# Even if script fails, cleanup will run
```

---

## Best Practices

### 1. Always Use Shebang
```bash
#!/bin/bash
# Tells system which interpreter to use
```

### 2. Quote Variables
```bash
# BAD (breaks with spaces)
FILE=$1
rm $FILE

# GOOD
FILE="$1"
rm "$FILE"
```

### 3. Check Arguments
```bash
#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

FILENAME="$1"
```

### 4. Use Meaningful Variable Names
```bash
# BAD
x=10
y="web1"

# GOOD
MAX_RETRIES=10
SERVER_NAME="web1"
```

### 5. Add Comments
```bash
#!/bin/bash
# deploy.sh - Deploy application to production
# Usage: ./deploy.sh <environment>
# Author: Joshua
# Date: 2025-11-16

# Configuration section
APP_DIR="/var/www/app"
LOG_FILE="/var/log/deploy.log"

# Main deployment logic
echo "Starting deployment..." | tee -a "$LOG_FILE"
```

### 6. Make Scripts Idempotent
```bash
# Script can be run multiple times safely
mkdir -p /var/www/app  # -p doesn't fail if exists
```

---

## Debugging Scripts

### Enable Debug Mode
```bash
#!/bin/bash
set -x  # Print each command before executing

# Or run with:
bash -x script.sh
```

### Add Debug Prints
```bash
#!/bin/bash

DEBUG=1  # Set to 0 to disable

debug() {
    if [ "$DEBUG" = "1" ]; then
        echo "[DEBUG] $@"
    fi
}

debug "Starting script"
debug "Variable x = $x"
```

---

## Practice Exercises

### Exercise 1: System Report Script
Write `system_report.sh` that outputs:
- Hostname
- Current date/time
- Uptime
- Disk usage
- Memory usage
- Top 5 CPU processes

### Exercise 2: Log Cleaner
Write `log_cleaner.sh` that:
- Takes directory as argument
- Finds all .log files older than 30 days
- Compresses them with gzip
- Moves to archive folder
- Prints summary

### Exercise 3: Service Monitor
Write `monitor_services.sh` that:
- Checks if nginx, mysql, redis are running
- If any are down, tries to restart (with sudo)
- Logs results to file
- Sends email if restart fails (optional)

---

## Summary

**You now know**:
- Variables and command substitution
- Conditionals (if/else)
- Loops (for, while)
- Functions
- Error handling
- Real DevOps automation scripts

**Next**: Lesson 4 - Version Control with Git

**Practice**: Write scripts for tasks you do repeatedly!

**Remember**: If you run it more than twice, script it!
