# Module 2: Linux & Git Cheat Sheet

Quick reference for essential commands and concepts.

---

## Linux Commands

### Navigation
```bash
pwd                    # Print working directory
ls -lah                # List files (long, all, human-readable)
cd /path/to/dir        # Change directory
cd ~                   # Go home
cd -                   # Go to previous directory
cd ..                  # Go up one level
```

### File Operations
```bash
cat file.txt           # View file
less file.txt          # Browse file (q to quit)
head -n 20 file.txt    # First 20 lines
tail -f file.txt       # Follow file (real-time)

cp source dest         # Copy
cp -r dir/ dest/       # Copy directory
mv old new             # Move/rename
rm file                # Delete file
rm -rf dir/            # Delete directory (DANGEROUS!)
mkdir -p /a/b/c        # Create directories
touch file.txt         # Create empty file
```

### Search
```bash
grep "pattern" file            # Search in file
grep -r "pattern" /dir/        # Recursive search
grep -i "error" *.log          # Case-insensitive
find /var/log -name "*.log"    # Find files by name
find . -mtime -7               # Modified in last 7 days
find . -size +100M             # Files larger than 100MB
```

### Permissions
```bash
chmod 755 file.sh      # rwxr-xr-x (executable)
chmod 644 file.txt     # rw-r--r-- (regular file)
chmod +x script.sh     # Add execute permission
chown user:group file  # Change owner
```

**Permission Calculations**:
- r (read) = 4
- w (write) = 2
- x (execute) = 1
- 755 = rwxr-xr-x (owner:7, group:5, others:5)
- 644 = rw-r--r-- (owner:6, group:4, others:4)

### Text Processing
```bash
awk '{print $1}' file          # Print first column
sed 's/old/new/g' file         # Replace old with new
sort file.txt                  # Sort lines
uniq file.txt                  # Remove duplicates
wc -l file.txt                 # Count lines
```

### Pipes & Redirection
```bash
cmd1 | cmd2                    # Pipe output to input
cmd > file                     # Redirect output (overwrite)
cmd >> file                    # Redirect output (append)
cmd 2> errors.txt              # Redirect errors
cmd > /dev/null 2>&1           # Discard all output
```

### System Info
```bash
df -h                  # Disk space
du -sh /dir            # Directory size
free -h                # Memory usage
top                    # Process monitor (q to quit)
ps aux                 # List all processes
kill PID               # Stop process
systemctl status nginx # Check service status
```

---

## Git Commands

### Setup
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git config --list      # View config
```

### Repository Basics
```bash
git init               # Initialize new repo
git clone <url>        # Clone remote repo
git status             # Show current state
git log                # View commit history
git log --oneline      # Compact history
```

### Making Changes
```bash
git add file.txt       # Stage single file
git add .              # Stage all changes
git commit -m "msg"    # Commit staged changes
git diff               # Show unstaged changes
git diff --staged      # Show staged changes
```

### Branching
```bash
git branch             # List branches
git branch feature-x   # Create branch
git checkout feature-x # Switch to branch
git checkout -b feat   # Create and switch
git merge feature-x    # Merge branch into current
git branch -d feature-x # Delete branch
```

### Remote Repositories
```bash
git remote -v          # List remotes
git fetch origin       # Download changes (don't merge)
git pull origin main   # Fetch + merge
git push origin main   # Upload commits
git push -u origin feature # Push and set upstream
```

### Undoing Changes
```bash
git checkout file.txt  # Discard changes in file
git reset HEAD file.txt # Unstage file
git reset --soft HEAD~ # Undo last commit (keep changes)
git reset --hard HEAD~ # Undo last commit (discard changes)
git revert <commit>    # Create new commit undoing changes
```

### Stashing
```bash
git stash              # Save changes temporarily
git stash list         # List stashes
git stash pop          # Apply and remove stash
git stash apply        # Apply but keep stash
```

### Useful
```bash
git blame file.txt     # Who changed each line
git show <commit>      # Show commit details
git reflog             # History of HEAD movements
gitignore              # .gitignore file patterns
```

---

## Git Workflow

### Feature Branch Workflow
```bash
# 1. Update main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/new-login

# 3. Make changes
# ... edit files ...
git add .
git commit -m "Add new login feature"

# 4. Push to remote
git push -u origin feature/new-login

# 5. Create Pull Request (on GitHub/GitLab)
# ... review, approve ...

# 6. Merge to main (on GitHub/GitLab)

# 7. Cleanup
git checkout main
git pull origin main
git branch -d feature/new-login
```

---

## Common Patterns

### Check System Health
```bash
df -h | grep -v loop          # Disk space (ignore loops)
free -h                        # Memory
systemctl status nginx         # Service status
tail -f /var/log/syslog       # Watch logs
```

### Find and Kill Process
```bash
ps aux | grep nginx            # Find process
kill -9 <PID>                  # Force kill
# or
pkill nginx                    # Kill by name
```

### Find Large Files
```bash
du -ah /var | sort -rh | head -20
# or
find /var -type f -size +100M -exec ls -lh {} \;
```

### Deploy Pattern
```bash
cd /var/www/app
git pull origin main
pip install -r requirements.txt
python manage.py migrate
sudo systemctl restart app
curl -f http://localhost/ || echo "Health check failed!"
```

---

## Shell Script Template
```bash
#!/bin/bash
# Script name and description
# Usage: ./script.sh <args>

set -e  # Exit on error
set -u  # Treat unset variables as error

# Configuration
VAR1="value"
VAR2="value"

# Functions
function_name() {
    echo "Doing something..."
}

# Main logic
if [ $# -lt 1 ]; then
    echo "Usage: $0 <argument>"
    exit 1
fi

# Your code here
echo "Starting..."
function_name
echo "Done!"
```

---

## Git Commit Message Template
```
<type>: <subject>

<body>

<footer>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance

Example:
feat: add user authentication

- Implement JWT tokens
- Add login/logout endpoints
- Create user session management

Closes #123
```

---

## Troubleshooting

### Can't connect to server
```bash
ping server.com                # Check if reachable
ssh -v user@server.com         # Verbose SSH
cat ~/.ssh/config              # Check SSH config
```

### Disk full
```bash
df -h                          # Check space
du -sh /var/*                  # Find large directories
find /var/log -name "*.log" -mtime +30 -delete  # Delete old logs
```

### Git merge conflict
```bash
git status                     # See conflicted files
# Edit files, resolve conflicts
git add <resolved-files>
git commit                     # Complete merge
```

### Permission denied
```bash
ls -l file                     # Check permissions
chmod 644 file                 # Fix permissions
sudo chown user:group file     # Fix ownership
```

---

## Keyboard Shortcuts (Terminal)

- `Ctrl + C`: Cancel current command
- `Ctrl + D`: Exit (logout)
- `Ctrl + L`: Clear screen
- `Ctrl + R`: Search command history
- `Ctrl + A`: Go to beginning of line
- `Ctrl + E`: Go to end of line
- `Ctrl + U`: Delete from cursor to beginning
- `Ctrl + K`: Delete from cursor to end
- `Tab`: Auto-complete
- `↑`/`↓`: Navigate command history

---

## Important Paths

### Linux
```
/               Root directory
/home/user      User home directory (~)
/etc/           Configuration files
/var/log/       Log files
/var/www/       Web server files
/tmp/           Temporary files
/usr/bin/       User binaries
/opt/           Optional software
```

### Git
```
.git/           Git repository data
.gitignore      Files to ignore
README.md       Project documentation
```

---

## Quick Reference Tables

### File Test Operators
| Operator | Meaning |
|----------|---------|
| `-f` | File exists (regular file) |
| `-d` | Directory exists |
| `-r` | File is readable |
| `-w` | File is writable |
| `-x` | File is executable |
| `-e` | File exists (any type) |
| `-s` | File has size > 0 |

### Numeric Comparisons
| Operator | Meaning |
|----------|---------|
| `-eq` | Equal |
| `-ne` | Not equal |
| `-gt` | Greater than |
| `-lt` | Less than |
| `-ge` | Greater than or equal |
| `-le` | Less than or equal |

---

**Pro Tip**: Add this to your ~/.bashrc for helpful aliases:
```bash
alias ll='ls -lah'
alias gs='git status'
alias gp='git pull'
alias gc='git commit -m'
alias h='history | grep'
```

**Print this cheat sheet and keep it handy!**
