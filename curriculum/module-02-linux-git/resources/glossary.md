# Module 2: Linux & Git Glossary

Complete reference for Linux and Git terminology.

---

## Linux Terms

### A

**Absolute Path**
: Full path from root directory to a file or directory. Example: `/home/user/documents/file.txt`

**APT (Advanced Package Tool)**
: Package management system used by Debian-based Linux distributions (Ubuntu, Debian). Commands: `apt install`, `apt update`, `apt upgrade`

**Argument**
: Values passed to a command or script. Example: In `cp file1.txt file2.txt`, `file1.txt` and `file2.txt` are arguments

**Alias**
: Shortcut command. Example: `alias ll='ls -lah'` creates `ll` as shortcut for `ls -lah`

**AWK**
: Text processing tool for extracting and manipulating data in files. Example: `awk '{print $1}' file.txt` prints first column

---

### B

**Bash (Bourne Again Shell)**
: Default command-line shell in most Linux distributions. Scripting language for automation

**Binary**
: Executable program file. Located in `/bin`, `/usr/bin`, `/usr/local/bin`

**Background Process**
: Process running without blocking the terminal. Created with `&` at end of command

---

### C

**Cat**
: Command to concatenate and display files. Example: `cat file.txt`

**Chmod**
: Command to change file permissions. Example: `chmod 755 script.sh`

**Chown**
: Command to change file ownership. Example: `chown user:group file.txt`

**CLI (Command-Line Interface)**
: Text-based interface for interacting with the operating system

**Cron/Crontab**
: System for scheduling automated tasks. Edit with `crontab -e`

**Current Directory**
: The directory you're currently in. View with `pwd`

---

### D

**Daemon**
: Background service that runs continuously. Example: `nginx`, `sshd`, `cron`

**Directory**
: Folder containing files and other directories. Create with `mkdir`, remove with `rmdir`

**Distribution (Distro)**
: Variant of Linux. Examples: Ubuntu, CentOS, Debian, Fedora, Alpine

**df (Disk Free)**
: Command to show disk space usage. Example: `df -h`

**du (Disk Usage)**
: Command to show directory/file sizes. Example: `du -sh /var`

---

### E

**Environment Variable**
: Variable available to all processes. View with `env`. Set with `export VAR=value`

**EOF (End of File)**
: Marker indicating the end of a file or input

**Exit Code (Exit Status)**
: Number returned by command indicating success (0) or failure (non-zero). Check with `echo $?`

---

### F

**File Descriptor**
: Reference to an open file. 0=stdin, 1=stdout, 2=stderr

**Filesystem Hierarchy Standard (FHS)**
: Standard layout of directories in Linux:
  - `/` - Root
  - `/home` - User home directories
  - `/etc` - Configuration files
  - `/var` - Variable data (logs, cache)
  - `/usr` - User programs
  - `/bin` - Essential binaries

**Find**
: Command to search for files. Example: `find /var/log -name "*.log"`

---

### G

**Grep**
: Command to search for text patterns. Example: `grep "error" logfile.txt`

**Group**
: Collection of users. Used for permission management

**GUI (Graphical User Interface)**
: Visual interface with windows and icons (opposite of CLI)

---

### H

**Hard Link**
: Direct reference to file data on disk. Created with `ln file link`

**Home Directory**
: User's personal directory. Usually `/home/username`. Shortcut: `~`

---

### I

**inode**
: Data structure storing file metadata (permissions, ownership, timestamps)

**I/O (Input/Output)**
: Reading from and writing to devices (files, network, keyboard, screen)

---

### K

**Kernel**
: Core of the operating system. Manages hardware and system resources

**Kill**
: Command to terminate processes. Example: `kill PID` or `kill -9 PID` (force kill)

---

### L

**Less**
: Command to view files page by page. Example: `less logfile.txt`

**Link**
: Reference to another file. Types: hard link, symbolic link

**Locate**
: Fast file search using database. Example: `locate filename`

**Log Files**
: Files recording system and application events. Usually in `/var/log`

---

### M

**Man Pages (Manual Pages)**
: Documentation for commands. View with `man command`. Example: `man ls`

**Mount**
: Attach a filesystem to the directory tree. Example: `mount /dev/sda1 /mnt`

---

### N

**Nano**
: Simple text editor for terminal. Example: `nano file.txt`

**Netstat**
: Command to display network connections. Example: `netstat -tulpn`

---

### O

**Owner**
: User who owns a file. Change with `chown`

---

### P

**Package Manager**
: Tool for installing/managing software. Examples: `apt`, `yum`, `dnf`, `pacman`

**PATH**
: Environment variable listing directories where executable programs are located

**Permissions**
: Access rights for files (read, write, execute) for owner, group, others

**Pipe (`|`)**
: Sends output of one command as input to another. Example: `ls | grep txt`

**Process**
: Running instance of a program. View with `ps` or `top`

**pwd (Print Working Directory)**
: Command showing current directory

---

### R

**Redirection**
: Changing where command input comes from or output goes to
  - `>` - Redirect output (overwrite)
  - `>>` - Redirect output (append)
  - `<` - Redirect input
  - `2>` - Redirect errors

**Relative Path**
: Path relative to current directory. Example: `../documents/file.txt`

**Root**
: 1. Top-level directory (`/`)
: 2. Superuser account with all privileges

**Root Directory**
: Top of filesystem hierarchy (`/`)

---

### S

**Sed (Stream Editor)**
: Text processing tool for find/replace. Example: `sed 's/old/new/g' file.txt`

**Shell**
: Command-line interpreter. Examples: bash, zsh, sh

**Shell Script**
: File containing shell commands for automation. Usually ends with `.sh`

**Shebang**
: First line in script specifying interpreter. Example: `#!/bin/bash`

**SSH (Secure Shell)**
: Protocol for secure remote login. Example: `ssh user@server`

**Standard Streams**:
  - **stdin** (0): Standard input (keyboard)
  - **stdout** (1): Standard output (screen)
  - **stderr** (2): Standard error (screen)

**Sudo**
: Run command as superuser. Example: `sudo apt update`

**Symbolic Link (Symlink)**
: Pointer to another file. Created with `ln -s target link`

**systemctl**
: Command to manage system services. Example: `systemctl status nginx`

---

### T

**Tail**
: Command to view end of file. Example: `tail -f logfile.txt` (follow mode)

**Tar**
: Command to create/extract archives. Example: `tar -czf archive.tar.gz files/`

**Terminal**
: Interface to the shell

**Text Editor**
: Program for editing files. Examples: nano, vim, emacs

---

### U

**Ubuntu**
: Popular Linux distribution based on Debian

**Umask**
: Default permissions for new files and directories

**User**
: Account for a person or service to access the system

---

### V

**Vim/Vi**
: Powerful text editor. Example: `vim file.txt`

**Variable**
: Named storage for values in scripts. Example: `NAME="value"`

---

### W

**Wget**
: Command to download files from web. Example: `wget https://example.com/file.zip`

**Wildcard**
: Character matching multiple items:
  - `*` - Matches any characters
  - `?` - Matches single character
  - `[abc]` - Matches a, b, or c

---

### X

**xargs**
: Build and execute commands from input. Example: `find . -name "*.txt" | xargs rm`

---

### Y

**Yum**
: Package manager for Red Hat-based systems (CentOS, RHEL)

---

### Z

**Zip**
: Compress files. Example: `zip archive.zip file1 file2`

---

## Git Terms

### A

**Add**
: Stage changes for commit. Command: `git add`

**Amend**
: Modify the last commit. Command: `git commit --amend`

---

### B

**Blob (Binary Large Object)**
: Git object type storing file contents

**Branch**
: Separate line of development. Create with `git branch`, switch with `git checkout`

**Branch Protection**
: Rules preventing direct commits to certain branches (usually main/master)

---

### C

**Cherry-Pick**
: Apply specific commit to current branch. Command: `git cherry-pick <commit>`

**Clone**
: Copy repository from remote to local. Command: `git clone <url>`

**Commit**
: Snapshot of changes. Command: `git commit -m "message"`

**Commit Hash (SHA)**
: Unique identifier for a commit. Example: `a3f2b1c`

**Commit Message**
: Description of changes in a commit

**Conflict**
: When two branches modify the same lines differently. Must be resolved manually

**Conventional Commits**
: Standard format for commit messages. Example: `feat: add login feature`

---

### D

**Detached HEAD**
: HEAD pointing to a commit instead of a branch

**Diff**
: Show differences between commits, branches, or files. Command: `git diff`

**Distributed**
: Every clone has full repository history (vs centralized like SVN)

---

### F

**Fast-Forward**
: Merge that simply moves branch pointer forward (no merge commit)

**Fetch**
: Download changes from remote without merging. Command: `git fetch`

**Fork**
: Personal copy of someone else's repository (GitHub concept)

---

### G

**Git**
: Distributed version control system created by Linus Torvalds

**GitHub**
: Web platform for hosting Git repositories (not part of Git itself)

**GitLab**
: Alternative to GitHub for hosting Git repositories

**GitFlow**
: Branching workflow with main, develop, feature, release, and hotfix branches

---

### H

**HEAD**
: Pointer to current commit/branch

**Hotfix**
: Quick bug fix branch from main/master. Merged to both main and develop

**Hook**
: Script that runs automatically on Git events (pre-commit, pre-push, etc.)

---

### I

**Index**
: Another name for staging area

**Init**
: Initialize new Git repository. Command: `git init`

---

### L

**Log**
: View commit history. Command: `git log`

---

### M

**Main/Master**
: Default primary branch (master is older name, main is newer convention)

**Merge**
: Combine changes from different branches. Command: `git merge`

**Merge Conflict**
: Occurs when merging branches that modified same lines

**Merge Commit**
: Commit with two parent commits (result of merge)

---

### O

**Origin**
: Default name for remote repository

---

### P

**Pull**
: Fetch and merge changes from remote. Command: `git pull`

**Pull Request (PR)**
: Request to merge changes (GitHub/GitLab feature, not Git command)

**Push**
: Upload local commits to remote. Command: `git push`

---

### R

**Rebase**
: Replay commits on top of another branch. Command: `git rebase`

**Reflog**
: History of where HEAD has been. Useful for recovery. Command: `git reflog`

**Remote**
: Repository on another server (GitHub, GitLab, etc.)

**Repository (Repo)**
: Project tracked by Git (.git directory)

**Reset**
: Move HEAD to different commit:
  - `--soft`: Keep changes staged
  - `--mixed`: Keep changes unstaged
  - `--hard`: Discard changes (dangerous!)

**Revert**
: Create new commit undoing previous commit. Safe for shared branches

---

### S

**SHA (Secure Hash Algorithm)**
: Unique identifier for Git objects

**Squash**
: Combine multiple commits into one

**Stage/Staging Area**
: Area where changes are prepared for commit

**Stash**
: Temporarily save uncommitted changes. Command: `git stash`

---

### T

**Tag**
: Named reference to specific commit (usually for releases). Command: `git tag`

**Three-Way Merge**
: Merge creating merge commit (when branches diverged)

**Tracked File**
: File that Git is monitoring for changes

**Tree**
: Git object representing directory structure

---

### U

**Untracked File**
: File not being monitored by Git

**Upstream**
: Remote branch your local branch tracks

---

### W

**Working Directory**
: Your actual files (not staged or committed)

**Workflow**
: Process for using branches and collaboration (Feature Branch, GitFlow, etc.)

---

## Command Quick Reference

### Essential Linux Commands

```bash
# Navigation
pwd                    # Print working directory
cd <dir>              # Change directory
ls -lah               # List files (detailed, all, human-readable)

# File Operations
cp <src> <dest>       # Copy
mv <src> <dest>       # Move/rename
rm <file>             # Delete
mkdir <dir>           # Create directory
touch <file>          # Create empty file

# Text Processing
cat <file>            # Display file
less <file>           # Browse file
grep "pattern" <file> # Search in file
awk '{print $1}'      # Print first column
sed 's/old/new/g'     # Replace text

# System Info
df -h                 # Disk space
free -h               # Memory usage
top                   # Process monitor
ps aux                # List processes

# Permissions
chmod 755 <file>      # Change permissions
chown user:group <file> # Change ownership
```

### Essential Git Commands

```bash
# Setup
git init              # Initialize repository
git clone <url>       # Clone repository

# Basic Workflow
git status            # Show status
git add <file>        # Stage changes
git commit -m "msg"   # Commit changes
git push              # Push to remote
git pull              # Pull from remote

# Branching
git branch            # List branches
git checkout <branch> # Switch branch
git checkout -b <br>  # Create and switch
git merge <branch>    # Merge branch

# History
git log               # View history
git log --oneline     # Compact history
git diff              # Show changes

# Undo
git restore <file>    # Discard changes
git reset --soft HEAD~1 # Undo last commit
git revert <commit>   # Create revert commit
```

---

## See Also

- [Cheat Sheet](cheat-sheet.md) - Quick command reference
- [Further Reading](further-reading.md) - Books and resources
- Lesson materials for detailed explanations
