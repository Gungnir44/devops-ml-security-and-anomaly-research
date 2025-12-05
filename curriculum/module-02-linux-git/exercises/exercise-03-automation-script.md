# Exercise 3: Automation Script - System Maintenance

**Duration**: 60-90 minutes
**Difficulty**: Intermediate-Advanced
**Prerequisites**: Lessons 1-3
**Points**: 30

---

## Objectives

By completing this exercise, you will:
- Write production-ready shell scripts
- Implement error handling and logging
- Automate common DevOps tasks
- Use variables, functions, and conditionals
- Create reusable, maintainable automation

---

## Scenario

Your company runs multiple web servers that need regular maintenance:
- **Log rotation**: Compress old logs to save disk space
- **Backup**: Back up critical files and databases
- **Health checks**: Monitor system resources and services
- **Cleanup**: Remove temporary files and old backups

Currently, a DevOps engineer manually performs these tasks every week. Your mission: Automate everything with a professional-grade shell script.

---

## Requirements

Create **three automation scripts**:

1. **`system-health-check.sh`** - Monitor system health
2. **`backup-manager.sh`** - Automated backups
3. **`log-cleanup.sh`** - Log rotation and cleanup

Each script must be:
- **Idempotent**: Safe to run multiple times
- **Robust**: Handle errors gracefully
- **Logged**: Record all actions
- **Configurable**: Use variables for settings
- **Professional**: Follow best practices

---

## Script 1: System Health Check (10 points)

### Requirements

Create `system-health-check.sh` that:

**✅ Checks:**
1. Disk usage (warn if > 80%, critical if > 90%)
2. Memory usage (warn if > 80%, critical if > 90%)
3. CPU load average
4. Service status (nginx, mysql, redis - if installed)
5. System uptime
6. Failed login attempts (last 24 hours)

**✅ Outputs:**
- Color-coded results (green = OK, yellow = warning, red = critical)
- Timestamp on report
- Summary at end (X checks passed, Y warnings, Z critical)

**✅ Actions:**
- Save report to log file
- Send email/slack if critical issues (bonus)
- Exit with appropriate code (0 = OK, 1 = warnings, 2 = critical)

### Template

```bash
#!/bin/bash
# system-health-check.sh
# Monitors system health and generates report

# Color codes
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Configuration
DISK_WARN_THRESHOLD=80
DISK_CRIT_THRESHOLD=90
MEM_WARN_THRESHOLD=80
MEM_CRIT_THRESHOLD=90
LOG_FILE="/var/log/health-check.log"

# Counters
PASSED=0
WARNINGS=0
CRITICAL=0

# Functions
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_disk() {
    # TODO: Implement disk space check
}

check_memory() {
    # TODO: Implement memory check
}

check_cpu() {
    # TODO: Implement CPU load check
}

check_services() {
    # TODO: Implement service status checks
}

generate_summary() {
    # TODO: Print summary of checks
}

# Main execution
main() {
    log_message "=== System Health Check Started ==="

    check_disk
    check_memory
    check_cpu
    check_services

    generate_summary

    # Exit with appropriate code
    if [ $CRITICAL -gt 0 ]; then
        exit 2
    elif [ $WARNINGS -gt 0 ]; then
        exit 1
    else
        exit 0
    fi
}

main "$@"
```

### Example Output

```
=== System Health Check - 2025-11-16 10:30:15 ===

[✓] Disk Usage: 45% (OK)
[⚠] Memory Usage: 85% (WARNING - High memory usage)
[✓] CPU Load: 1.5 (OK)
[✓] Service nginx: Running (OK)
[✗] Service mysql: NOT RUNNING (CRITICAL)
[✓] System Uptime: 15 days (OK)

=== Summary ===
Passed: 4
Warnings: 1
Critical: 1

CRITICAL ISSUES DETECTED! Immediate action required.
```

---

## Script 2: Backup Manager (10 points)

### Requirements

Create `backup-manager.sh` that:

**✅ Backs up:**
1. Application files (/var/www or specified directory)
2. Configuration files (/etc/nginx, /etc/mysql)
3. Database dumps (MySQL/PostgreSQL if installed)
4. User-specified directories

**✅ Features:**
- Compressed archives (.tar.gz)
- Timestamped filenames (backup-2025-11-16-103015.tar.gz)
- Verification (check archive integrity)
- Retention policy (delete backups older than N days)
- Backup rotation (keep last N backups)
- Exclude patterns (.git, node_modules, __pycache__)

**✅ Options:**
```bash
./backup-manager.sh [options]

Options:
  -d, --dir <path>       Directory to backup (required)
  -o, --output <path>    Backup destination (default: /backup)
  -r, --retain <days>    Keep backups for N days (default: 7)
  -n, --name <name>      Backup name prefix (default: backup)
  --verify               Verify backup after creation
  -h, --help             Show help message
```

### Template

```bash
#!/bin/bash
# backup-manager.sh
# Automated backup system with retention policy

set -e  # Exit on error
set -u  # Exit on undefined variable

# Default configuration
BACKUP_SOURCE=""
BACKUP_DEST="/backup"
RETENTION_DAYS=7
BACKUP_PREFIX="backup"
VERIFY_BACKUP=false
LOG_FILE="/var/log/backup.log"

# Functions
usage() {
    cat << EOF
Usage: $0 [options]

Options:
  -d, --dir <path>       Directory to backup (required)
  -o, --output <path>    Backup destination (default: /backup)
  -r, --retain <days>    Keep backups for N days (default: 7)
  -n, --name <name>      Backup name prefix (default: backup)
  --verify               Verify backup after creation
  -h, --help             Show help
EOF
}

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

create_backup() {
    # TODO: Create compressed backup
}

verify_backup() {
    # TODO: Verify archive integrity
}

cleanup_old_backups() {
    # TODO: Remove backups older than retention period
}

# Parse command line arguments
# TODO: Implement argument parsing

# Main execution
main() {
    log "=== Backup Started ==="

    # Validate inputs
    if [ -z "$BACKUP_SOURCE" ]; then
        echo "Error: Backup source not specified"
        usage
        exit 1
    fi

    # Create backup directory
    mkdir -p "$BACKUP_DEST"

    # Perform backup
    create_backup

    # Verify if requested
    if [ "$VERIFY_BACKUP" = true ]; then
        verify_backup
    fi

    # Cleanup old backups
    cleanup_old_backups

    log "=== Backup Completed Successfully ==="
}

main "$@"
```

### Example Output

```
[2025-11-16 10:30:15] === Backup Started ===
[2025-11-16 10:30:15] Source: /var/www/myapp
[2025-11-16 10:30:15] Destination: /backup
[2025-11-16 10:30:15] Creating backup archive...
[2025-11-16 10:30:18] Archive created: backup-2025-11-16-103015.tar.gz (45 MB)
[2025-11-16 10:30:18] Verifying backup integrity...
[2025-11-16 10:30:19] Verification: OK
[2025-11-16 10:30:19] Cleaning up backups older than 7 days...
[2025-11-16 10:30:19] Deleted 3 old backups
[2025-11-16 10:30:19] === Backup Completed Successfully ===
```

---

## Script 3: Log Cleanup (10 points)

### Requirements

Create `log-cleanup.sh` that:

**✅ Features:**
1. Find all .log files in specified directory
2. Compress logs older than N days
3. Archive compressed logs to separate directory
4. Delete archives older than retention period
5. Generate cleanup report

**✅ Safety:**
- Dry-run mode (--dry-run) to preview changes
- Confirmation prompt before deletion
- Never delete today's logs
- Preserve directory structure

**✅ Configuration:**
```bash
./log-cleanup.sh [options]

Options:
  -d, --dir <path>       Log directory (default: /var/log)
  -a, --age <days>       Compress logs older than N days (default: 7)
  -r, --retain <days>    Keep archives for N days (default: 30)
  --dry-run              Show what would be done (don't execute)
  -f, --force            Skip confirmation prompts
  -h, --help             Show help
```

### Template

```bash
#!/bin/bash
# log-cleanup.sh
# Automated log rotation and cleanup

set -e
set -u

# Configuration
LOG_DIR="/var/log"
COMPRESS_AGE=7
RETENTION_DAYS=30
ARCHIVE_DIR="/var/log/archives"
DRY_RUN=false
FORCE=false
REPORT_FILE="/var/log/cleanup-report.log"

# Functions
log_action() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$REPORT_FILE"
}

find_old_logs() {
    # TODO: Find logs older than COMPRESS_AGE days
}

compress_logs() {
    # TODO: Compress old log files
}

archive_compressed_logs() {
    # TODO: Move compressed logs to archive directory
}

cleanup_old_archives() {
    # TODO: Delete archives older than RETENTION_DAYS
}

generate_report() {
    # TODO: Generate summary report
}

# Main execution
main() {
    log_action "=== Log Cleanup Started ==="

    # Create archive directory
    mkdir -p "$ARCHIVE_DIR"

    # Find and compress old logs
    find_old_logs
    compress_logs

    # Archive compressed logs
    archive_compressed_logs

    # Cleanup old archives
    cleanup_old_archives

    # Generate report
    generate_report

    log_action "=== Log Cleanup Completed ==="
}

main "$@"
```

### Example Output

```
=== Log Cleanup Report - 2025-11-16 10:30:15 ===

Found logs to process: 23 files

Compressed logs:
  /var/log/nginx/access.log.1 -> access.log.1.gz (120 MB -> 12 MB, 90% reduction)
  /var/log/nginx/error.log.1 -> error.log.1.gz (45 MB -> 5 MB, 89% reduction)
  [... 21 more files ...]

Archived: 23 compressed logs moved to /var/log/archives/

Cleanup:
  Deleted 8 archives older than 30 days
  Freed disk space: 450 MB

Summary:
  Files processed: 23
  Space saved: 1.2 GB
  Archives deleted: 8
  Space freed: 450 MB

=== Log Cleanup Completed Successfully ===
```

---

## Deliverables

Submit a zip file containing:

```
exercise-03-submission/
├── system-health-check.sh
├── backup-manager.sh
├── log-cleanup.sh
├── README.md (usage instructions)
├── test-results.txt (output from testing each script)
└── demo-video.mp4 (optional: screen recording of scripts running)
```

### README.md Template

```markdown
# Exercise 3: Automation Scripts
**Author**: [Your Name]
**Date**: 2025-11-16

## Scripts Included

### 1. system-health-check.sh
**Purpose**: Monitor system health and alert on issues

**Usage**:
```bash
./system-health-check.sh
```

**Features**:
- [List features you implemented]

**Testing**:
- [How you tested it]

### 2. backup-manager.sh
**Purpose**: Automated backup with retention policy

**Usage**:
```bash
./backup-manager.sh -d /path/to/backup -o /backup --verify
```

**Features**:
- [List features you implemented]

**Testing**:
- [How you tested it]

### 3. log-cleanup.sh
**Purpose**: Log rotation and cleanup

**Usage**:
```bash
./log-cleanup.sh -d /var/log --dry-run
```

**Features**:
- [List features you implemented]

**Testing**:
- [How you tested it]

## Challenges Faced

1. [Challenge 1 and how you solved it]
2. [Challenge 2 and how you solved it]

## Future Improvements

- [What would you add if you had more time?]
```

---

## Grading Rubric

| Category | Points | Criteria |
|----------|--------|----------|
| **Script 1: Health Check** | 10 | Checks work, error handling, output formatting |
| **Script 2: Backup Manager** | 10 | Backup works, verification, retention policy |
| **Script 3: Log Cleanup** | 10 | Finds logs, compresses, cleans up correctly |
| **Total** | **30** | |

**Detailed Criteria**:

**Each Script (10 points)**:
- ✅ **Functionality (4 points)**: Script performs required tasks
- ✅ **Error Handling (2 points)**: Gracefully handles errors, validates input
- ✅ **Logging (1 point)**: Proper logging of actions
- ✅ **Code Quality (2 points)**: Clean code, comments, best practices
- ✅ **Documentation (1 point)**: Usage instructions, help message

**Bonus Points** (+5):
- Email/Slack notifications
- Advanced features (encryption, remote backups)
- Comprehensive test suite
- Cron job setup documentation

---

## Testing Your Scripts

### Test Environment Setup

```bash
# Create test environment
mkdir -p ~/test-automation
cd ~/test-automation

# Create test files
mkdir -p test-logs test-data test-backups
touch test-logs/{app.log,error.log,access.log,debug.log}
dd if=/dev/zero of=test-logs/large.log bs=1M count=100

# Create test application files
mkdir -p test-data/app/{src,config,data}
touch test-data/app/src/{main.py,utils.py}
touch test-data/app/config/{app.conf,database.yml}

# Set file dates (for testing age-based operations)
touch -t 202511010000 test-logs/old.log
touch -t 202511150000 test-logs/recent.log
```

### Test Checklist

**System Health Check**:
- [ ] Reports disk usage correctly
- [ ] Reports memory usage correctly
- [ ] Checks CPU load
- [ ] Detects service status
- [ ] Color codes output properly
- [ ] Logs to file
- [ ] Exit codes correct (0, 1, 2)

**Backup Manager**:
- [ ] Creates compressed backup
- [ ] Uses timestamped filenames
- [ ] Verifies backup integrity
- [ ] Removes old backups
- [ ] Handles errors (missing source, no space)
- [ ] Command-line options work
- [ ] Excludes patterns (.git, etc.)

**Log Cleanup**:
- [ ] Finds old log files
- [ ] Compresses correctly
- [ ] Archives to separate location
- [ ] Deletes old archives
- [ ] Dry-run mode works
- [ ] Preserves recent logs
- [ ] Generates accurate report

---

## Common Mistakes to Avoid

❌ **No error handling**
```bash
# Bad
cd /some/directory
rm -rf *  # What if cd failed?!

# Good
cd /some/directory || { echo "Failed to cd"; exit 1; }
rm -rf *
```

❌ **Not quoting variables**
```bash
# Bad (breaks with spaces)
cp $FILE $DEST

# Good
cp "$FILE" "$DEST"
```

❌ **Hardcoded paths**
```bash
# Bad
LOG_FILE="/home/joshua/log.txt"

# Good
LOG_FILE="${HOME}/log.txt"
```

❌ **No validation**
```bash
# Bad
rm -rf "$BACKUP_DIR"/*  # What if BACKUP_DIR is empty?!

# Good
if [ -z "$BACKUP_DIR" ]; then
    echo "Error: BACKUP_DIR not set"
    exit 1
fi
rm -rf "${BACKUP_DIR}"/*
```

---

## Pro Tips

✅ **Use `set` flags**
```bash
set -e  # Exit on error
set -u  # Exit on undefined variable
set -o pipefail  # Pipe fails if any command fails
```

✅ **Create cleanup traps**
```bash
cleanup() {
    rm -f /tmp/backup-tmp-*
}
trap cleanup EXIT
```

✅ **Validate early**
```bash
# Check prerequisites at start
if ! command -v tar &> /dev/null; then
    echo "Error: tar command not found"
    exit 1
fi
```

✅ **Use functions**
```bash
# Reusable, testable, readable
function backup_database() {
    local db_name="$1"
    # ... backup logic ...
}
```

---

## Resources

- [Bash Best Practices](https://bertvv.github.io/cheat-sheets/Bash.html)
- [ShellCheck](https://www.shellcheck.net/) - Lint your scripts!
- `man bash` - Complete Bash reference

---

## What You'll Learn

After this exercise:
- ✅ Write production-quality automation scripts
- ✅ Implement robust error handling
- ✅ Create reusable functions
- ✅ Handle command-line arguments
- ✅ Generate professional reports
- ✅ Think like a DevOps engineer (automation-first)

**These scripts are portfolio-worthy - make them shine!** 🌟

---

**Next**: Exercise 4 - Git Workflow Simulation (learn team collaboration)
