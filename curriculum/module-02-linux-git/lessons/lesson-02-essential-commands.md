# Lesson 2: Essential Linux Commands

**Duration**: 2 hours
**Objectives**: Master the 30 commands DevOps engineers use daily

---

## The Core Skill: Navigate Without GUI

**Truth**: You'll spend 40% of your DevOps career in a terminal.

**This lesson teaches**: The commands you'll use every single day.

---

## Part 1: Filesystem Navigation (30 min)

### Understanding the Linux Filesystem

**Windows**: Multiple drives (C:\, D:\, E:\)
**Linux**: Single tree starting at `/` (root)

```
/                    (root - top of everything)
├── home/            (user home directories)
│   ├── joshua/
│   └── alice/
├── etc/             (configuration files)
├── var/             (variable data: logs, databases)
│   └── log/
├── usr/             (user programs)
│   └── bin/
├── bin/             (essential binaries)
└── tmp/             (temporary files)
```

### Command: `pwd` (Print Working Directory)

**What it does**: Shows where you are

```bash
$ pwd
/home/joshua/devops-learning
```

**Why it matters**: You're often lost. This tells you where you are.

### Command: `ls` (List)

**What it does**: Shows files in current (or specified) directory

```bash
# Basic list
$ ls
file1.txt  file2.txt  folder1/

# Long format (detailed)
$ ls -l
-rw-r--r-- 1 joshua joshua 1024 Nov 16 10:00 file1.txt
drwxr-xr-x 2 joshua joshua 4096 Nov 16 10:05 folder1/

# Include hidden files (start with .)
$ ls -la

# Human-readable sizes
$ ls -lh
-rw-r--r-- 1 joshua joshua 1.0K Nov 16 10:00 file1.txt

# Sort by modification time
$ ls -lt
```

**Essential Flags**:
- `-l`: Long format (permissions, owner, size, date)
- `-a`: Include hidden files (`.bashrc`, `.ssh/`)
- `-h`: Human-readable sizes (1.0K, 2.3M, 1.5G)
- `-t`: Sort by time (newest first)
- `-r`: Reverse order

**Pro Tip**: Combine flags: `ls -lath`

### Command: `cd` (Change Directory)

**What it does**: Move to a different directory

```bash
# Go to specific directory
$ cd /var/log

# Go to home directory
$ cd ~
# or just
$ cd

# Go up one level
$ cd ..

# Go up two levels
$ cd ../..

# Go to previous directory
$ cd -

# Relative path
$ cd folder1/subfolder/

# Absolute path
$ cd /home/joshua/projects/
```

**Special Paths**:
- `~`: Your home directory (`/home/joshua`)
- `.`: Current directory
- `..`: Parent directory
- `-`: Previous directory
- `/`: Root directory

### Command: `tree` (Visual Directory Structure)

```bash
# Install first
$ sudo apt install tree

# Show directory tree
$ tree
.
├── folder1
│   ├── file1.txt
│   └── subfolder
│       └── file2.txt
└── folder2
    └── file3.txt

# Limit depth
$ tree -L 2

# Show only directories
$ tree -d
```

---

## Part 2: File Operations (30 min)

### Command: `cat` (Concatenate)

**What it does**: Display file contents

```bash
# View file
$ cat /etc/hosts
127.0.0.1   localhost
192.168.1.10   server1

# Concatenate multiple files
$ cat file1.txt file2.txt

# Number lines
$ cat -n script.sh

# Show end of lines ($)
$ cat -e file.txt
```

**Use When**: File is short (< 100 lines)

### Command: `less` (Pager)

**What it does**: View large files page by page

```bash
$ less /var/log/syslog

# Navigation:
# Space: Next page
# b: Previous page
# /search: Search forward
# ?search: Search backward
# q: Quit
```

**Use When**: File is long, need to browse

### Command: `head` & `tail`

**What they do**: Show beginning or end of file

```bash
# First 10 lines
$ head /var/log/syslog

# First 20 lines
$ head -n 20 /var/log/syslog

# Last 10 lines
$ tail /var/log/syslog

# Last 50 lines
$ tail -n 50 /var/log/syslog

# Follow file (real-time updates) - CRITICAL for logs!
$ tail -f /var/log/nginx/access.log
```

**DevOps Use Case**: `tail -f` to watch logs in real-time

### Command: `cp` (Copy)

```bash
# Copy file
$ cp source.txt destination.txt

# Copy to directory
$ cp file.txt /backup/

# Copy directory recursively
$ cp -r folder1/ folder2/

# Copy with permissions preserved
$ cp -p file.txt backup.txt

# Verbose (show what's being copied)
$ cp -v file.txt /backup/
```

**Flags**:
- `-r`: Recursive (for directories)
- `-p`: Preserve permissions and timestamps
- `-v`: Verbose
- `-i`: Interactive (ask before overwriting)

### Command: `mv` (Move/Rename)

```bash
# Rename file
$ mv oldname.txt newname.txt

# Move file
$ mv file.txt /destination/

# Move directory
$ mv folder1/ /destination/

# Move multiple files
$ mv file1.txt file2.txt /destination/
```

### Command: `rm` (Remove) ⚠️ DANGEROUS

```bash
# Remove file
$ rm file.txt

# Remove directory
$ rm -r folder/

# Force remove (no confirmation)
$ rm -rf folder/   # DANGEROUS! No undo!

# Interactive (ask before each delete)
$ rm -i file.txt

# Verbose
$ rm -v file.txt
```

**⚠️ WARNING**:
- `rm -rf /` = Delete EVERYTHING (system destroyed)
- No recycle bin! Deleted = GONE
- Always double-check before `rm -rf`

**Pro Tip**: Alias for safety
```bash
alias rm='rm -i'   # Always ask before deleting
```

### Command: `mkdir` (Make Directory)

```bash
# Create directory
$ mkdir new_folder

# Create parent directories
$ mkdir -p /path/to/deep/folder/structure

# Create with specific permissions
$ mkdir -m 755 public_folder
```

### Command: `touch` (Create Empty File)

```bash
# Create new file (or update timestamp if exists)
$ touch newfile.txt

# Create multiple files
$ touch file1.txt file2.txt file3.txt
```

---

## Part 3: File Content & Searching (30 min)

### Command: `grep` (Search Text) - CRITICAL

**What it does**: Search for patterns in files

```bash
# Search for "error" in file
$ grep "error" /var/log/syslog

# Case-insensitive search
$ grep -i "error" /var/log/syslog

# Search recursively in directory
$ grep -r "TODO" /home/joshua/code/

# Show line numbers
$ grep -n "error" logfile.txt

# Show lines NOT matching
$ grep -v "debug" logfile.txt

# Count matches
$ grep -c "error" logfile.txt

# Show filename with matches
$ grep -H "error" *.log
```

**Essential Flags**:
- `-i`: Case-insensitive
- `-r`: Recursive (search directories)
- `-n`: Line numbers
- `-v`: Invert (show non-matches)
- `-c`: Count matches
- `-l`: Show only filenames

**DevOps Use Cases**:
```bash
# Find all errors in logs
grep -i "error" /var/log/*.log

# Find configuration for specific service
grep -r "nginx" /etc/

# Find which file contains IP address
grep -r "192.168.1.100" /etc/nginx/
```

### Command: `find` (Find Files) - POWERFUL

```bash
# Find all .txt files
$ find . -name "*.txt"

# Find all .log files in /var/log
$ find /var/log -name "*.log"

# Find files modified in last 24 hours
$ find . -mtime 0

# Find files modified more than 30 days ago
$ find . -mtime +30

# Find large files (> 100MB)
$ find . -size +100M

# Find and delete
$ find . -name "*.tmp" -delete

# Find and execute command
$ find . -name "*.log" -exec gzip {} \;
```

**Common Patterns**:
- `-name`: Filename pattern
- `-type f`: Files only
- `-type d`: Directories only
- `-mtime N`: Modified N days ago
- `-size +/-N`: Size greater/less than N
- `-exec`: Execute command on results

**DevOps Use Cases**:
```bash
# Find old log files to delete
find /var/log -name "*.log" -mtime +90

# Find large files consuming disk space
find / -type f -size +1G 2>/dev/null

# Find all config files
find /etc -name "*.conf"
```

### Command: `wc` (Word Count)

```bash
# Count lines, words, characters
$ wc file.txt
  10  50  300 file.txt
  (lines words bytes)

# Count lines only
$ wc -l file.txt

# Count words only
$ wc -w file.txt

# Count characters only
$ wc -c file.txt
```

**Use Case**: How many errors in log?
```bash
$ grep "error" /var/log/syslog | wc -l
42
```

---

## Part 4: Permissions & Ownership (20 min)

### Understanding Permissions

```bash
$ ls -l file.txt
-rw-r--r-- 1 joshua joshua 1024 Nov 16 10:00 file.txt
│││││││││
│││││││││
│└┴┴┴┴┴┴┴─ Permissions
│
└─ File type (- = file, d = directory, l = link)

Breakdown:
-           rw-      r--      r--
file type   owner    group    others
```

**Permission Types**:
- `r` (read): Can view content (4)
- `w` (write): Can modify (2)
- `x` (execute): Can run as program (1)

**Examples**:
- `rw-`: 6 (4+2)
- `r--`: 4
- `rwx`: 7 (4+2+1)
- `r-x`: 5 (4+1)
- `---`: 0 (no permissions)

**Common Permissions**:
- `644` (`rw-r--r--`): Files (owner can write, others read-only)
- `755` (`rwxr-xr-x`): Executables/directories
- `600` (`rw-------`): Private files (SSH keys)
- `700` (`rwx------`): Private directories

### Command: `chmod` (Change Permissions)

```bash
# Numeric method (recommended)
$ chmod 644 file.txt     # rw-r--r--
$ chmod 755 script.sh    # rwxr-xr-x
$ chmod 600 id_rsa       # rw------- (SSH key)

# Symbolic method
$ chmod u+x script.sh    # Add execute for owner
$ chmod g-w file.txt     # Remove write for group
$ chmod o=r file.txt     # Set others to read-only
$ chmod a+r file.txt     # Add read for all

# Recursive (directories)
$ chmod -R 755 /var/www/
```

### Command: `chown` (Change Owner)

```bash
# Change owner
$ sudo chown alice file.txt

# Change owner and group
$ sudo chown alice:developers file.txt

# Recursive
$ sudo chown -R alice:developers /project/
```

**Why `sudo`**: Only root or owner can change ownership

---

## Part 5: Text Processing (20 min)

### Command: `awk` (Pattern Scanning)

**What it does**: Extract columns from text

```bash
# Print 1st column
$ awk '{print $1}' file.txt

# Print columns 1 and 3
$ awk '{print $1, $3}' file.txt

# Print lines where column 3 > 100
$ awk '$3 > 100' file.txt

# Sum column 2
$ awk '{sum += $2} END {print sum}' file.txt
```

**DevOps Use Case**: Extract IPs from access log
```bash
$ awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -10
# Top 10 IPs by request count
```

### Command: `sed` (Stream Editor)

**What it does**: Find and replace in files

```bash
# Replace first occurrence per line
$ sed 's/old/new/' file.txt

# Replace all occurrences
$ sed 's/old/new/g' file.txt

# Replace in-place (modify file)
$ sed -i 's/old/new/g' file.txt

# Delete lines matching pattern
$ sed '/pattern/d' file.txt

# Print only lines matching pattern
$ sed -n '/pattern/p' file.txt
```

**DevOps Use Case**: Update config files
```bash
# Change port 80 to 8080 in nginx config
$ sed -i 's/listen 80/listen 8080/g' /etc/nginx/nginx.conf
```

### Command: `sort` & `uniq`

```bash
# Sort lines alphabetically
$ sort file.txt

# Sort numerically
$ sort -n numbers.txt

# Sort in reverse
$ sort -r file.txt

# Remove duplicates (requires sorted input)
$ sort file.txt | uniq

# Count duplicates
$ sort file.txt | uniq -c

# Show only duplicates
$ sort file.txt | uniq -d
```

**DevOps Use Case**: Find most common errors
```bash
$ grep "ERROR" app.log | awk '{print $5}' | sort | uniq -c | sort -nr | head -10
```

---

## Part 6: Pipes & Redirection (10 min)

### Pipes (`|`): Chain Commands

**Concept**: Output of one command becomes input of next

```bash
# How many log files?
$ ls /var/log | wc -l

# Top 10 largest files
$ ls -lS | head -10

# Find all errors, count each type
$ grep "error" /var/log/syslog | awk '{print $6}' | sort | uniq -c | sort -nr
```

**Power**: Build complex workflows from simple commands

### Redirection: Save Output

```bash
# Redirect output to file (overwrite)
$ ls > files.txt

# Redirect output to file (append)
$ ls >> files.txt

# Redirect errors to file
$ command 2> errors.txt

# Redirect output AND errors
$ command > output.txt 2>&1

# Discard output
$ command > /dev/null 2>&1
```

**Use Cases**:
```bash
# Save logs
$ journalctl -u nginx > nginx_logs.txt

# Append to daily report
$ date >> daily_report.txt
$ uptime >> daily_report.txt

# Run command, ignore errors
$ find / -name "*.conf" 2>/dev/null
```

---

## The 30 Essential Commands (Cheat Sheet)

| Command | Purpose | Example |
|---------|---------|---------|
| `pwd` | Show current directory | `pwd` |
| `ls` | List files | `ls -lah` |
| `cd` | Change directory | `cd /var/log` |
| `cat` | View file | `cat file.txt` |
| `less` | Browse file | `less /var/log/syslog` |
| `head` | First lines | `head -n 20 file.txt` |
| `tail` | Last lines | `tail -f /var/log/nginx/access.log` |
| `grep` | Search text | `grep -i "error" *.log` |
| `find` | Find files | `find . -name "*.conf"` |
| `cp` | Copy | `cp -r folder/ /backup/` |
| `mv` | Move/rename | `mv old.txt new.txt` |
| `rm` | Delete | `rm -rf folder/` |
| `mkdir` | Create directory | `mkdir -p /path/to/dir` |
| `touch` | Create file | `touch newfile.txt` |
| `chmod` | Change permissions | `chmod 755 script.sh` |
| `chown` | Change owner | `sudo chown user:group file` |
| `wc` | Count lines/words | `wc -l file.txt` |
| `sort` | Sort lines | `sort file.txt` |
| `uniq` | Remove duplicates | `sort file.txt \| uniq -c` |
| `awk` | Process columns | `awk '{print $1}' file.txt` |
| `sed` | Find/replace | `sed 's/old/new/g' file.txt` |
| `df` | Disk space | `df -h` |
| `du` | Directory size | `du -sh folder/` |
| `ps` | List processes | `ps aux` |
| `top` | Monitor processes | `top` |
| `kill` | Stop process | `kill -9 PID` |
| `man` | Manual | `man ls` |
| `history` | Command history | `history \| grep docker` |
| `sudo` | Run as admin | `sudo systemctl restart nginx` |
| `which` | Find command path | `which python` |

---

## Practice Exercises

### Exercise 1: File Navigation
```bash
# Create practice structure
mkdir -p ~/devops-practice/{logs,configs,scripts}
cd ~/devops-practice
touch logs/{app,error,access}.log
touch configs/{nginx,mysql}.conf
touch scripts/{backup,deploy}.sh

# Navigate and explore
# - Find all .log files
# - List files by size
# - Count total files
```

### Exercise 2: Log Analysis
```bash
# Download sample log
curl -o access.log https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/nginx_logs/nginx_logs

# Tasks:
# - Count total requests
# - Find all 404 errors
# - List top 10 IPs by request count
# - Find requests from last hour
```

### Exercise 3: File Permissions
```bash
# Create test files
touch public_file.txt
touch private_file.txt
touch executable.sh

# Set appropriate permissions:
# - public_file.txt: Anyone can read
# - private_file.txt: Only you can read/write
# - executable.sh: Only you can execute
```

---

## Summary

**You now know**:
- **Navigate**: pwd, ls, cd, tree
- **Files**: cat, less, head, tail, cp, mv, rm, mkdir, touch
- **Search**: grep, find, wc
- **Permissions**: chmod, chown
- **Process**: awk, sed, sort, uniq
- **Power tools**: pipes, redirection

**Next**: Lesson 3 - Shell Scripting (automate these commands!)

**Practice Daily**: Use terminal for file management instead of GUI

**Remember**: Every expert was once confused by `ls -lah`. Keep practicing!
