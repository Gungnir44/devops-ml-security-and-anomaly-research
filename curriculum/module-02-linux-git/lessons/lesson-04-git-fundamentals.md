# Lesson 4: Git Fundamentals - Version Control That Changed Everything

**Duration**: 1.5 hours
**Objectives**: Understand Git's data model and master essential Git operations

---

## The Problem Git Solved

**Before Git** (2000s):
```
Me: "The code works on my machine!"
You: "Well it doesn't work on mine."
Boss: "What changed?"
Me: "Umm... I don't remember."
Boss: "Can we go back to yesterday's version?"
Me: "I... deleted it to save space."
Boss: 😤
```

**The Old Ways**:
- **Copy-paste versioning**: `project_final.zip`, `project_final_v2.zip`, `project_final_ACTUALLY_FINAL.zip`
- **Email attachments**: "Here's the latest code" (which version though?)
- **Shared network drives**: One person editing at a time (locking files)
- **CVS/SVN**: Better, but centralized (server down = no work)

**Then Git arrived** (2005):
- Linus Torvalds built it in 2 weeks for Linux kernel development
- Solved: speed, distributed work, branching, merging
- **Changed software development forever**

---

## Why Git Won

### Git vs. The Competition

**SVN (Subversion) - Centralized**:
```
Server (central repo)
   ↓
Developer 1 ← must connect to server
Developer 2 ← must connect to server
Developer 3 ← must connect to server
```
❌ Server down = can't work
❌ Slow over network
❌ Can't work offline

**Git - Distributed**:
```
Central Repo (GitHub)
   ↕
Developer 1 (full copy)
Developer 2 (full copy)
Developer 3 (full copy)
```
✅ Work offline
✅ Lightning fast
✅ Everyone has full history
✅ Easy branching/merging

**Result**: Git is now used by 95%+ of developers

---

## Git's Data Model (How It Actually Works)

### Git Stores Snapshots, Not Diffs

**Other systems** (SVN):
```
Version 1: [full file]
Version 2: [diff: what changed]
Version 3: [diff: what changed]
```

**Git**:
```
Commit 1: [snapshot of entire project]
Commit 2: [snapshot of entire project]
Commit 3: [snapshot of entire project]
```

**Why snapshots?**
- Blazingly fast (no need to reconstruct from diffs)
- Integrity (SHA-1 hash of everything)
- Easy branching (just pointers)

### Git Objects

Git stores everything as **objects**:

**1. Blob** (Binary Large Object):
- File content
- No metadata (no filename, no permissions)
- Identified by SHA-1 hash

**2. Tree**:
- Directory structure
- Maps filenames to blobs
- Like a folder

**3. Commit**:
- Points to a tree (project snapshot)
- Points to parent commit(s)
- Has metadata (author, date, message)

**4. Tag**:
- Named reference to a commit
- Usually for releases (v1.0, v2.0)

### Example

```
Commit abc123
├── tree (root directory)
│   ├── README.md (blob)
│   ├── src/ (tree)
│   │   ├── main.py (blob)
│   │   └── utils.py (blob)
│   └── tests/ (tree)
│       └── test_main.py (blob)
├── parent: def456
├── author: Joshua <josh@example.com>
├── date: 2025-11-16
└── message: "Add user authentication"
```

---

## The Three States

**Git has THREE areas where your files live**:

```
Working Directory → Staging Area → Repository
     (modified)      (staged)        (committed)
```

### 1. Working Directory
- Your actual files
- Where you edit code
- `git status` shows "modified"

### 2. Staging Area (Index)
- Files ready to commit
- Lets you commit selectively
- `git add` moves here

### 3. Repository (.git directory)
- Committed snapshots
- Permanent history
- `git commit` saves here

### Example Workflow

```bash
# 1. Make changes (Working Directory)
echo "print('hello')" > app.py

# 2. Stage changes (Staging Area)
git add app.py

# 3. Commit changes (Repository)
git commit -m "Add hello world"
```

---

## Essential Git Commands

### Setup (One Time)

```bash
# Configure your identity
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# View config
git config --list

# Set default editor
git config --global core.editor "nano"
```

### Starting a Repository

**Option 1: Start Fresh**
```bash
mkdir myproject
cd myproject
git init
# Creates .git/ directory
```

**Option 2: Clone Existing**
```bash
git clone https://github.com/user/repo.git
cd repo
```

### Basic Workflow

**Check Status**
```bash
git status
# Shows:
# - Modified files (working directory)
# - Staged files (staging area)
# - Untracked files (new files)
```

**Stage Changes**
```bash
git add file.txt          # Stage single file
git add .                 # Stage all changes
git add *.py              # Stage all Python files
git add src/              # Stage entire directory
```

**Commit Changes**
```bash
git commit -m "Add feature X"

# Multi-line message
git commit -m "Add user login" -m "Includes authentication and session management"

# Open editor for detailed message
git commit
```

**View History**
```bash
git log                   # Full history
git log --oneline         # Compact (one line per commit)
git log --graph           # ASCII graph
git log --all --oneline --graph  # Beautiful graph of all branches
git log -n 5              # Last 5 commits
git log --since="2 weeks ago"    # Time-based
```

**View Changes**
```bash
git diff                  # Unstaged changes
git diff --staged         # Staged changes
git diff HEAD             # All changes
git diff commit1 commit2  # Between commits
```

---

## Writing Good Commit Messages

### Bad Commit Messages
```bash
git commit -m "fixed stuff"
git commit -m "wip"
git commit -m "asdfasdf"
git commit -m "Update"
```
❌ Useless! What changed? Why?

### Good Commit Messages

**Format**:
```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples**:
```bash
git commit -m "feat: add user authentication

Implement JWT-based authentication system with:
- Login/logout endpoints
- Token refresh mechanism
- User session management

Closes #123"
```

```bash
git commit -m "fix: resolve database connection timeout

Increase connection pool size from 10 to 50 to handle peak traffic.
Add connection retry logic with exponential backoff.

Fixes #456"
```

**Rules**:
1. Subject line: 50 characters max
2. Capitalize first letter
3. No period at end
4. Use imperative mood ("Add feature" not "Added feature")
5. Body: Explain WHAT and WHY (not HOW - code shows that)

---

## Ignoring Files

**.gitignore** - Tell Git to ignore certain files

```bash
# Create .gitignore file
cat > .gitignore << EOF
# Python
*.pyc
__pycache__/
venv/
.env

# Node
node_modules/
npm-debug.log

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp

# Build artifacts
dist/
build/
*.egg-info/

# Secrets (NEVER COMMIT THESE!)
*.key
*.pem
credentials.json
EOF

git add .gitignore
git commit -m "Add .gitignore"
```

**Important**: Files already tracked by Git won't be ignored! Remove them first:
```bash
git rm --cached secret.key
echo "secret.key" >> .gitignore
git commit -m "Remove secret key from tracking"
```

---

## Viewing History

### git log Variations

```bash
# Standard log
git log

# Compact
git log --oneline

# With file changes
git log --stat

# With actual code changes
git log -p

# Pretty format
git log --pretty=format:"%h - %an, %ar : %s"
# %h = short hash
# %an = author name
# %ar = relative date
# %s = subject

# Filter by author
git log --author="Joshua"

# Filter by message
git log --grep="fix"

# Filter by file
git log -- path/to/file.txt
```

### git show - View Specific Commit

```bash
git show abc123           # Show commit abc123
git show HEAD             # Show latest commit
git show HEAD~1           # Show previous commit
git show HEAD~5           # 5 commits ago
git show v1.0             # Show tagged release
```

### git blame - Who Changed What

```bash
git blame file.txt
# Shows each line with:
# - commit hash
# - author
# - date
# - line number

# Blame specific lines
git blame -L 10,20 file.txt
```

---

## Undoing Changes

### Discard Changes in Working Directory

```bash
# Discard changes to one file
git checkout -- file.txt

# Discard all changes
git checkout -- .

# Or using newer syntax
git restore file.txt
```

### Unstage Files

```bash
# Unstage one file
git reset HEAD file.txt

# Unstage all
git reset HEAD .

# Or using newer syntax
git restore --staged file.txt
```

### Amend Last Commit

**Forgot to add a file?**
```bash
git commit -m "Add feature"
# Oops! Forgot a file

git add forgotten_file.txt
git commit --amend --no-edit
# Adds file to previous commit, keeps message
```

**Fix commit message?**
```bash
git commit -m "Add featur"  # Typo!
git commit --amend -m "Add feature"  # Fixed!
```

⚠️ **Warning**: Only amend commits that haven't been pushed!

---

## Practical Examples

### Example 1: Start New Project

```bash
# Create project
mkdir my-devops-app
cd my-devops-app
git init

# Create README
echo "# My DevOps App" > README.md
git add README.md
git commit -m "docs: add README"

# Create initial structure
mkdir -p src tests
touch src/main.py tests/test_main.py
git add .
git commit -m "chore: add project structure"

# Add .gitignore
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore
git add .gitignore
git commit -m "chore: add Python .gitignore"
```

### Example 2: Daily Development

```bash
# Start work
git status                # What's the current state?

# Make changes
vim src/main.py           # Edit file

# Check what changed
git diff                  # Review your changes

# Stage and commit
git add src/main.py
git commit -m "feat: add user authentication"

# More changes
vim src/auth.py
git add src/auth.py
git commit -m "feat: implement JWT tokens"

# View history
git log --oneline --graph
```

### Example 3: Disaster Recovery

```bash
# Oh no! Deleted important file!
rm important.py
git status                # Shows "deleted: important.py"

# Restore it
git checkout -- important.py
# File is back!

# Made bad changes to multiple files
git checkout -- .         # Discard all changes

# Committed but want to undo
git reset --soft HEAD~1   # Undo commit, keep changes
git reset --hard HEAD~1   # Undo commit, discard changes (DANGEROUS!)
```

---

## Understanding HEAD

**HEAD** = pointer to current commit

```bash
HEAD                      # Current commit
HEAD~1 or HEAD^           # Previous commit
HEAD~2                    # 2 commits ago
HEAD~10                   # 10 commits ago
```

**Examples**:
```bash
git show HEAD             # Show current commit
git show HEAD~3           # Show 3 commits ago
git diff HEAD~5 HEAD      # Changes in last 5 commits
```

---

## Git Configuration Levels

```bash
# System (all users)
git config --system user.name "Name"

# Global (your user)
git config --global user.name "Name"

# Local (this repo only)
git config --local user.name "Name"

# View all configs
git config --list

# View specific setting
git config user.email
```

---

## Best Practices

### ✅ Do
- Commit often (small, logical commits)
- Write meaningful commit messages
- Use .gitignore for generated files
- Review changes before committing (`git diff`)
- Keep commits focused (one change = one commit)

### ❌ Don't
- Commit secrets (API keys, passwords)
- Commit generated files (node_modules/, __pycache__/)
- Use vague messages ("update", "fix")
- Commit untested code (at least try to run it!)
- Make giant commits (500 files changed = bad)

---

## Summary

**You now know**:
- Why Git revolutionized version control
- Git's snapshot model (not diffs)
- The three states (working, staging, committed)
- Essential commands (init, add, commit, log, diff)
- How to write good commit messages
- How to undo mistakes
- .gitignore for excluding files

**Next**: Lesson 5 - Git Workflows (branching, merging, collaboration)

**Practice**: Initialize a repo, make commits, view history, undo changes!

---

## Quick Reference Card

```bash
# Setup
git init
git config --global user.name "Name"
git config --global user.email "email"

# Basic Workflow
git status
git add file.txt
git commit -m "message"
git log --oneline

# Viewing
git diff
git show HEAD
git log --graph

# Undoing
git checkout -- file.txt    # Discard changes
git reset HEAD file.txt     # Unstage
git commit --amend          # Fix last commit
```

**Practice these until they're muscle memory!** 🧠
