# Module 2 Final Project: Automated DevOps Workflow

**Duration**: 8-12 hours
**Points**: 100
**Deliverable**: Complete Git repository with automation scripts and documentation

---

## Project Overview

Build a professional DevOps automation system that combines Linux shell scripting with Git workflows. This project demonstrates real-world DevOps practices and is **portfolio-worthy**.

You'll create:
1. **Server Setup Automation** - Shell scripts to configure servers
2. **Backup & Monitoring System** - Automated maintenance scripts
3. **Git Workflow Implementation** - Professional branching and PR process
4. **CI/CD Integration** - Pre-commit hooks and automated checks
5. **Complete Documentation** - Professional README and guides

---

## Learning Objectives

By completing this project, you will:
- ✅ Write production-quality shell scripts
- ✅ Implement professional Git workflows
- ✅ Automate common DevOps tasks
- ✅ Create reusable, maintainable code
- ✅ Document technical projects professionally
- ✅ Build portfolio piece for job applications

---

## Project Scenario

**Company**: CloudOps Inc.
**Role**: Junior DevOps Engineer
**Task**: Automate server setup and maintenance for the development team

**Problem**:
- New developers spend 4 hours setting up their environments
- Production servers configured manually (inconsistent)
- No automated backups or health checks
- No code quality standards enforced

**Your Solution**:
Build automated DevOps workflow that:
- Sets up servers in 5 minutes
- Runs automated health checks and backups
- Enforces code quality with Git hooks
- Uses professional Git workflows
- Fully documented for team use

---

## Project Structure

Your final repository should look like this:

```
devops-automation-project/
├── README.md                          # Main project documentation
├── CONTRIBUTING.md                    # Contribution guidelines
├── .gitignore                         # Git ignore patterns
├── setup/
│   ├── server-setup.sh               # Server configuration script
│   ├── install-dependencies.sh       # Install packages
│   ├── configure-services.sh         # Configure nginx, databases
│   └── setup-firewall.sh             # Security configuration
├── scripts/
│   ├── backup/
│   │   ├── backup-system.sh          # Full system backup
│   │   ├── backup-database.sh        # Database backup
│   │   └── verify-backup.sh          # Backup verification
│   ├── monitoring/
│   │   ├── health-check.sh           # System health monitoring
│   │   ├── disk-monitor.sh           # Disk space monitoring
│   │   ├── service-monitor.sh        # Service status checks
│   │   └── alert.sh                  # Alert notification system
│   ├── maintenance/
│   │   ├── log-rotation.sh           # Log rotation and cleanup
│   │   ├── cleanup-temp.sh           # Temporary file cleanup
│   │   └── update-system.sh          # System updates
│   └── deploy/
│       ├── deploy-app.sh             # Application deployment
│       ├── rollback.sh               # Rollback to previous version
│       └── smoke-test.sh             # Post-deployment tests
├── config/
│   ├── app.conf.example              # App configuration template
│   ├── backup.conf                   # Backup configuration
│   └── monitoring.conf               # Monitoring configuration
├── .git/
│   └── hooks/
│       ├── pre-commit                # Code quality checks
│       ├── commit-msg                # Commit message validation
│       └── pre-push                  # Pre-push tests
├── docs/
│   ├── setup-guide.md                # Server setup guide
│   ├── workflow-guide.md             # Git workflow documentation
│   ├── troubleshooting.md            # Common issues and fixes
│   └── architecture.md               # System architecture
└── tests/
    ├── test-setup.sh                 # Test setup scripts
    ├── test-backup.sh                # Test backup scripts
    └── test-monitoring.sh            # Test monitoring scripts
```

---

## Part 1: Server Setup Automation (25 points)

### Requirements

Create **`setup/server-setup.sh`** - Master setup script that:

**✅ Must have:**
1. **System updates**: Update package lists and upgrade system
2. **User creation**: Create devops user with sudo privileges
3. **SSH configuration**: Secure SSH setup (disable root login, key-only auth)
4. **Firewall**: Configure UFW with proper rules
5. **Install tools**: Git, Docker, Python, Node.js, monitoring tools
6. **Configure services**: Nginx, PostgreSQL (if needed)
7. **Security hardening**: Fail2ban, automatic security updates
8. **Logging**: Log all actions to setup.log

**✅ Must include:**
- Configuration variables at top
- Error handling for all operations
- Verification steps after each installation
- Rollback capability if setup fails
- Dry-run mode (`--dry-run` flag)
- Help message (`--help` flag)

### Example Implementation

```bash
#!/bin/bash
# server-setup.sh - Automated server configuration
# Usage: ./server-setup.sh [options]

set -e  # Exit on error
set -u  # Exit on undefined variable

# ============================================================
# Configuration
# ============================================================

DEVOPS_USER="devops"
SSH_PORT=22
ENABLE_FIREWALL=true
INSTALL_DOCKER=true
INSTALL_NODEJS=true
LOG_FILE="/var/log/server-setup.log"
DRY_RUN=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ============================================================
# Functions
# ============================================================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}✓${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}✗${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1" | tee -a "$LOG_FILE"
}

# Check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        error "This script must be run as root"
        exit 1
    fi
}

# Update system
update_system() {
    log "Updating system packages..."

    if [ "$DRY_RUN" = true ]; then
        log "[DRY RUN] Would run: apt update && apt upgrade -y"
        return 0
    fi

    apt update && apt upgrade -y
    success "System updated"
}

# Create devops user
create_devops_user() {
    log "Creating $DEVOPS_USER user..."

    if id "$DEVOPS_USER" &>/dev/null; then
        warning "User $DEVOPS_USER already exists"
        return 0
    fi

    if [ "$DRY_RUN" = true ]; then
        log "[DRY RUN] Would create user: $DEVOPS_USER"
        return 0
    fi

    useradd -m -s /bin/bash "$DEVOPS_USER"
    usermod -aG sudo "$DEVOPS_USER"
    success "User $DEVOPS_USER created"
}

# Configure SSH
configure_ssh() {
    log "Configuring SSH..."

    # TODO: Implement SSH configuration
    # - Disable root login
    # - Change default port
    # - Enable key-only authentication
}

# Install Docker
install_docker() {
    if [ "$INSTALL_DOCKER" = false ]; then
        return 0
    fi

    log "Installing Docker..."

    # TODO: Implement Docker installation
}

# Set up firewall
setup_firewall() {
    if [ "$ENABLE_FIREWALL" = false ]; then
        return 0
    fi

    log "Configuring firewall..."

    # TODO: Implement firewall setup with UFW
}

# Main execution
main() {
    log "========================================="
    log "Starting server setup..."
    log "========================================="

    check_root
    update_system
    create_devops_user
    configure_ssh
    install_docker
    setup_firewall

    log "========================================="
    success "Server setup completed successfully!"
    log "========================================="
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            cat << EOF
Usage: $0 [options]

Options:
  --dry-run    Show what would be done without executing
  --help       Show this help message

EOF
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            exit 1
            ;;
    esac
done

main "$@"
```

### Deliverables

- ✅ `server-setup.sh` with all required features
- ✅ Additional setup scripts for specific tasks
- ✅ Configuration files
- ✅ Test script to verify setup

---

## Part 2: Backup & Monitoring System (25 points)

### Requirements

Create comprehensive backup and monitoring scripts:

#### Backup System (`scripts/backup/`)

**`backup-system.sh`**:
- Back up critical directories (/etc, /var/www, /home)
- Compress with tar.gz
- Timestamped filenames
- Retention policy (keep last N backups)
- Verification after backup
- Email notification on failure

**`backup-database.sh`**:
- Dump PostgreSQL/MySQL databases
- Compress SQL dumps
- Encrypt sensitive backups (bonus)
- Store in separate backup directory

**`verify-backup.sh`**:
- Test backup integrity
- Verify all expected files exist
- Check backup size (detect corruption)
- Generate verification report

#### Monitoring System (`scripts/monitoring/`)

**`health-check.sh`**:
- CPU usage
- Memory usage
- Disk space
- Service status (nginx, postgresql, docker)
- Network connectivity
- Generate health score (0-100)
- Alert if score < 70

**`disk-monitor.sh`**:
- Monitor all mounted filesystems
- Alert at 80% usage (warning)
- Alert at 90% usage (critical)
- Find large files/directories
- Generate cleanup recommendations

**`service-monitor.sh`**:
- Check status of critical services
- Restart failed services automatically
- Log service outages
- Send alerts

**`alert.sh`**:
- Send alerts via email/Slack/webhooks
- Support different severity levels
- Rate limiting (don't spam)
- Formatted messages

### Example Backup Script

```bash
#!/bin/bash
# backup-system.sh - Automated system backup

# Configuration
BACKUP_SOURCES="/etc /var/www /home"
BACKUP_DEST="/backup"
RETENTION_DAYS=7
NOTIFY_EMAIL="admin@example.com"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_NAME="system-backup-$TIMESTAMP.tar.gz"

# Create backup
create_backup() {
    echo "Creating backup: $BACKUP_NAME"

    mkdir -p "$BACKUP_DEST"

    tar -czf "$BACKUP_DEST/$BACKUP_NAME" \
        --exclude='*.log' \
        --exclude='*cache*' \
        $BACKUP_SOURCES

    if [ $? -eq 0 ]; then
        echo "✓ Backup created successfully"
        echo "Size: $(du -h $BACKUP_DEST/$BACKUP_NAME | cut -f1)"
    else
        echo "✗ Backup failed!"
        # Send alert
        exit 1
    fi
}

# Verify backup
verify_backup() {
    echo "Verifying backup..."

    tar -tzf "$BACKUP_DEST/$BACKUP_NAME" > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo "✓ Backup integrity verified"
    else
        echo "✗ Backup verification failed!"
        exit 1
    fi
}

# Cleanup old backups
cleanup_old_backups() {
    echo "Cleaning up backups older than $RETENTION_DAYS days..."

    find "$BACKUP_DEST" -name "system-backup-*.tar.gz" -mtime +$RETENTION_DAYS -delete

    echo "✓ Cleanup completed"
}

# Main
main() {
    create_backup
    verify_backup
    cleanup_old_backups
    echo "Backup completed successfully!"
}

main
```

### Deliverables

- ✅ All backup scripts functional
- ✅ All monitoring scripts functional
- ✅ Alert system working
- ✅ Cron job examples for automation

---

## Part 3: Git Workflow Implementation (25 points)

### Requirements

Demonstrate professional Git workflow:

#### 1. Repository Setup

- ✅ Initialize Git repository
- ✅ Create `.gitignore` (exclude logs, backups, secrets)
- ✅ Create `main` and `develop` branches
- ✅ Protect `main` branch (document process)

#### 2. Feature Development

Complete workflow for at least **3 features**:

**Feature 1: Backup System**
```bash
git checkout develop
git checkout -b feature/backup-system

# Create backup scripts
# ... development work ...

git add scripts/backup/
git commit -m "feat: add automated backup system

- Implement full system backup
- Add database backup support
- Add verification and cleanup
- Include retention policy"

git push -u origin feature/backup-system

# Create Pull Request
# ... review process ...
# Merge to develop
```

**Feature 2: Monitoring System**
```bash
git checkout develop
git checkout -b feature/monitoring-system

# Create monitoring scripts
# ... development work ...

git commit -m "feat: add system monitoring

- Health check script
- Disk monitoring
- Service monitoring
- Alert system"

# ... PR process ...
```

**Feature 3: Your Choice**
- Deployment automation
- Log rotation
- Security hardening
- Or something else

#### 3. Hotfix Demonstration

**Create and fix a critical bug:**
```bash
git checkout main
git checkout -b hotfix/backup-path-error

# Fix the bug
git commit -m "fix: correct backup destination path

The backup script was using wrong path causing backups
to fail. Updated to use correct /backup directory.

Fixes #123"

# Merge to main
git checkout main
git merge hotfix/backup-path-error
git tag -a v1.0.1 -m "Hotfix: backup path correction"

# Merge to develop too
git checkout develop
git merge hotfix/backup-path-error
```

#### 4. Release Process

**Create a release:**
```bash
git checkout develop
git checkout -b release/v1.0.0

# Update version
echo "1.0.0" > VERSION

# Update CHANGELOG
cat > CHANGELOG.md << 'EOF'
# Changelog

## [1.0.0] - 2025-11-16

### Added
- Automated server setup
- Backup system
- Monitoring system
- Git hooks for quality
EOF

git commit -am "chore: prepare release v1.0.0"

# Merge to main
git checkout main
git merge release/v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0"

# Merge back to develop
git checkout develop
git merge release/v1.0.0
```

### Deliverables

- ✅ Clean Git history with professional commits
- ✅ At least 3 feature branches merged
- ✅ At least 1 hotfix demonstrated
- ✅ At least 1 release tag
- ✅ Commit messages following conventions
- ✅ Branch diagram showing workflow

---

## Part 4: CI/CD Integration (15 points)

### Requirements

Create Git hooks for automation:

#### Pre-Commit Hook (`.git/hooks/pre-commit`)

```bash
#!/bin/bash
# Pre-commit hook: Run before every commit

echo "Running pre-commit checks..."

# Check for trailing whitespace
if git diff --cached --check --diff-filter=ACMR; then
    echo "✓ No trailing whitespace"
else
    echo "✗ Found trailing whitespace"
    exit 1
fi

# Check shell scripts with shellcheck
if command -v shellcheck &> /dev/null; then
    echo "Running shellcheck..."

    # Find all shell scripts being committed
    scripts=$(git diff --cached --name-only --diff-filter=ACMR | grep '\.sh$')

    if [ -n "$scripts" ]; then
        shellcheck $scripts
        if [ $? -ne 0 ]; then
            echo "✗ Shellcheck failed"
            exit 1
        fi
        echo "✓ Shellcheck passed"
    fi
fi

# Check for secrets (basic)
echo "Checking for secrets..."
if git diff --cached | grep -iE '(api_key|password|secret|token)\s*=\s*["\'][^"\']+["\']'; then
    echo "✗ Possible secret detected!"
    echo "Remove secrets from code and use environment variables"
    exit 1
fi
echo "✓ No secrets detected"

# Run tests if they exist
if [ -d "tests" ] && [ -f "tests/run-all.sh" ]; then
    echo "Running tests..."
    bash tests/run-all.sh
    if [ $? -ne 0 ]; then
        echo "✗ Tests failed"
        exit 1
    fi
    echo "✓ Tests passed"
fi

echo "✓ All pre-commit checks passed!"
exit 0
```

#### Commit-Msg Hook (`.git/hooks/commit-msg`)

```bash
#!/bin/bash
# Commit-msg hook: Validate commit message format

commit_msg=$(cat "$1")

# Check format: type: description
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore|perf): .+"; then
    cat << EOF
✗ Invalid commit message format!

Commit message must follow the format:
  <type>: <description>

Valid types:
  feat:     New feature
  fix:      Bug fix
  docs:     Documentation
  style:    Formatting
  refactor: Code restructuring
  test:     Adding tests
  chore:    Maintenance
  perf:     Performance improvement

Example:
  feat: add backup verification script

Your message:
  $commit_msg
EOF
    exit 1
fi

# Check length (subject should be < 72 chars)
subject=$(echo "$commit_msg" | head -n 1)
if [ ${#subject} -gt 72 ]; then
    echo "✗ Subject line too long (${#subject} chars, max 72)"
    exit 1
fi

echo "✓ Commit message format valid"
exit 0
```

#### Pre-Push Hook (`.git/hooks/pre-push`)

```bash
#!/bin/bash
# Pre-push hook: Final checks before pushing

echo "Running pre-push checks..."

# Prevent push to main without going through develop
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if [ "$current_branch" = "main" ]; then
    echo "⚠ WARNING: Pushing to main branch"
    read -p "Are you sure? (yes/no) " confirm
    if [ "$confirm" != "yes" ]; then
        echo "Push aborted"
        exit 1
    fi
fi

# Run full test suite
echo "Running full test suite..."
if [ -f "tests/run-all.sh" ]; then
    bash tests/run-all.sh
    if [ $? -ne 0 ]; then
        echo "✗ Tests failed! Fix tests before pushing."
        exit 1
    fi
fi

echo "✓ All pre-push checks passed!"
exit 0
```

### Deliverables

- ✅ All three hooks implemented and working
- ✅ Hooks are executable (`chmod +x`)
- ✅ Demonstrate hooks preventing bad commits
- ✅ Documentation for setting up hooks

---

## Part 5: Documentation (10 points)

### Requirements

Create comprehensive documentation:

#### 1. README.md (Main Documentation)

```markdown
# DevOps Automation Project

Comprehensive automation system for server setup, monitoring, and backups.

## Features

- 🚀 Automated server setup (5-minute install)
- 💾 Automated backup system with verification
- 📊 System health monitoring and alerts
- 🔒 Security hardening and best practices
- 🔄 Professional Git workflow with hooks
- 📝 Complete documentation

## Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/devops-automation.git
cd devops-automation

# Run server setup (as root)
sudo bash setup/server-setup.sh

# Set up cron jobs for automation
crontab -e
# Add:
# 0 2 * * * /path/to/scripts/backup/backup-system.sh
# */15 * * * * /path/to/scripts/monitoring/health-check.sh
```

## Project Structure

[Explain directory structure]

## Scripts

### Setup Scripts
- `setup/server-setup.sh` - Master setup script
- [List all scripts with brief descriptions]

### Backup Scripts
- `scripts/backup/backup-system.sh` - Full system backup
- [Continue...]

[Continue with full README content...]
```

#### 2. CONTRIBUTING.md

Guidelines for contributing:
- Git workflow to follow
- Commit message conventions
- Code style guidelines
- Testing requirements
- PR process

#### 3. docs/setup-guide.md

Step-by-step setup instructions:
- Prerequisites
- Installation steps
- Configuration
- Troubleshooting

#### 4. docs/workflow-guide.md

Git workflow documentation:
- Branch naming conventions
- PR process
- Code review guidelines
- Release process

### Deliverables

- ✅ Complete README.md
- ✅ CONTRIBUTING.md
- ✅ Setup guide
- ✅ Workflow guide
- ✅ All scripts documented with comments

---

## Submission Requirements

### What to Submit

**1. GitHub Repository**:
```
Public GitHub repository with:
- All code and scripts
- All documentation
- Clean commit history
- At least 3 releases/tags
- Issues (create and close at least 3)
```

**2. Project Report** (`PROJECT-REPORT.md`):
```markdown
# Module 2 Project Report
**Student**: [Your Name]
**Date**: [Submission Date]

## Executive Summary
[2-3 paragraphs about your project]

## Implementation Details

### Part 1: Server Setup
[What you built, challenges, solutions]

### Part 2: Backup & Monitoring
[What you built, challenges, solutions]

### Part 3: Git Workflow
[How you used Git, PR examples]

### Part 4: CI/CD Integration
[Hooks you created, testing]

### Part 5: Documentation
[Documentation approach]

## Challenges Faced
1. [Challenge 1 and solution]
2. [Challenge 2 and solution]

## What I Learned
- [Learning 1]
- [Learning 2]
- [Learning 3]

## Future Improvements
- [What you would add next]

## Demo
[Link to demo video (optional but recommended)]

## Screenshots
[Include screenshots of:
- Scripts running
- Monitoring output
- Git workflow (branch diagram)
- Hooks preventing bad commits]
```

**3. Demo Video** (Optional, +5 bonus points):
- 5-10 minutes
- Show scripts working
- Walk through Git workflow
- Explain your code

### Submission Format

```bash
# Your repository should be public on GitHub
# Submit the URL to your repository

Repository: https://github.com/yourusername/devops-automation-project

# Also submit PROJECT-REPORT.md as PDF
```

---

## Grading Rubric

| Category | Points | Criteria |
|----------|--------|----------|
| **Part 1: Server Setup** | 25 | Comprehensive setup script, error handling, testing |
| **Part 2: Backup & Monitoring** | 25 | All scripts functional, automated, tested |
| **Part 3: Git Workflow** | 25 | Clean history, proper workflow, PRs, releases |
| **Part 4: CI/CD Integration** | 15 | Hooks working, preventing bad commits, tested |
| **Part 5: Documentation** | 10 | Complete, clear, professional |
| **Total** | **100** | |

### Detailed Scoring

**Server Setup (25 points)**:
- Script functionality: 15 points
- Error handling: 5 points
- Documentation: 3 points
- Testing: 2 points

**Backup & Monitoring (25 points)**:
- Backup scripts: 10 points
- Monitoring scripts: 10 points
- Integration (cron, alerts): 3 points
- Testing: 2 points

**Git Workflow (25 points)**:
- Commit quality: 8 points
- Branch workflow: 8 points
- PRs and reviews: 5 points
- Releases: 4 points

**CI/CD Integration (15 points)**:
- Pre-commit hook: 5 points
- Commit-msg hook: 5 points
- Pre-push hook: 5 points

**Documentation (10 points)**:
- README: 4 points
- Technical docs: 3 points
- Code comments: 2 points
- Project report: 1 point

### Bonus Points (up to +10)

- Demo video: +5
- Advanced features (encryption, Slack integration): +3
- Exceptional documentation: +2
- Creative enhancements: +2

---

## Timeline Recommendation

**Week 1 (4 hours)**:
- Day 1-2: Plan and set up repository
- Day 3-4: Build server setup scripts
- Day 5: Test and document Part 1

**Week 2 (4 hours)**:
- Day 1-2: Build backup scripts
- Day 3-4: Build monitoring scripts
- Day 5: Integration and testing

**Week 3 (4 hours)**:
- Day 1-2: Git workflow implementation
- Day 3: CI/CD hooks
- Day 4-5: Documentation and polish

---

## Resources

- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/)
- [Git Workflow Best Practices](https://www.atlassian.com/git/tutorials/comparing-workflows)
- [ShellCheck](https://www.shellcheck.net/) - Lint your scripts
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## Success Criteria

**You're ready to submit when:**

- [ ] All scripts are executable and tested
- [ ] Git history is clean and professional
- [ ] All documentation is complete
- [ ] Hooks prevent bad commits
- [ ] README has installation instructions
- [ ] Project can be cloned and run by anyone
- [ ] You're proud to show this to an employer

---

## What Employers Look For

This project demonstrates:
- ✅ **Linux proficiency** - Shell scripting, system administration
- ✅ **Git expertise** - Professional workflows, version control
- ✅ **Automation mindset** - DRY principle, reusability
- ✅ **Code quality** - Error handling, testing, documentation
- ✅ **DevOps culture** - CI/CD, monitoring, backups

**This is portfolio gold - make it shine!** 🌟

---

## Need Help?

- Review the lessons and exercises
- Check the resources provided
- Use man pages (`man bash`, `man git`)
- Test in a safe environment first

---

## Final Notes

**Time investment**: 8-12 hours
**Difficulty**: Challenging but achievable
**Impact**: High - this is a real DevOps project

**Remember**: Quality over quantity. A few well-written, tested scripts are better than many broken ones.

**Good luck! This project will prove you know DevOps fundamentals.** 🚀
