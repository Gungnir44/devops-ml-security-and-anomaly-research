# Exercise 1: File System Navigation Challenge

**Duration**: 30-45 minutes
**Difficulty**: Beginner
**Prerequisites**: Lessons 1-2
**Points**: 20

---

## Objectives

By completing this exercise, you will:
- Navigate the Linux filesystem using command line
- Understand absolute vs. relative paths
- Use essential navigation commands (cd, ls, pwd, find)
- Work with hidden files and directories
- Practice command options and flags

---

## Scenario

You've just started as a DevOps engineer at TechCorp. Your first task is to explore the server's file system to locate configuration files, logs, and application code. The senior engineer has left you a treasure hunt to test your Linux navigation skills.

---

## Setup

Create the practice environment:

```bash
# Create practice directory
mkdir -p ~/devops-learning/module-02/exercise-01
cd ~/devops-learning/module-02/exercise-01

# Run this script to set up the challenge
cat > setup.sh << 'EOF'
#!/bin/bash
# Create directory structure

mkdir -p webapp/{src,config,logs,tests}
mkdir -p webapp/src/{controllers,models,views,utils}
mkdir -p webapp/.git/hooks
mkdir -p data/{backups,uploads,cache}
mkdir -p scripts/{deployment,monitoring,backup}

# Create files
touch webapp/README.md
touch webapp/config/app.conf
touch webapp/config/database.yml
touch webapp/logs/app.log
touch webapp/logs/error.log
touch webapp/logs/.hidden-debug.log
touch webapp/src/app.py
touch webapp/src/controllers/user.py
touch webapp/src/models/database.py
touch webapp/.env
touch webapp/.gitignore

touch data/backups/backup-2025-11-01.tar.gz
touch data/backups/backup-2025-11-10.tar.gz
touch data/uploads/image1.png
touch data/cache/session-abc123

touch scripts/deployment/deploy.sh
touch scripts/monitoring/health-check.sh
touch scripts/backup/backup-db.sh

# Add some content
echo "SECRET_KEY=abc123" > webapp/.env
echo "# App Logs" > webapp/logs/app.log
echo "Error: Connection timeout" > webapp/logs/error.log
echo "Debug: Secret debugging info" > webapp/logs/.hidden-debug.log
echo "*.log" > webapp/.gitignore

echo "Challenge environment created!"
echo "Current directory structure:"
tree -a . 2>/dev/null || find . -print
EOF

chmod +x setup.sh
./setup.sh
```

---

## Tasks

### Part 1: Basic Navigation (5 points)

Complete these tasks and document the commands you used:

1. **Display current directory**
   - Show the full path of where you are

2. **List all files in webapp directory**
   - Include hidden files
   - Show file sizes in human-readable format
   - Show file permissions

3. **Navigate to webapp/src/controllers**
   - Use absolute path
   - Verify you're in the correct directory

4. **Return to home directory**
   - Use the shortcut command
   - Verify you're in home directory

5. **Navigate back to exercise-01 directory**
   - Use relative path from home

### Part 2: Finding Files (5 points)

6. **Find all Python files (.py) in the entire exercise-01 directory**
   - List their full paths

7. **Find all hidden files (files starting with .)**
   - Search recursively in webapp directory

8. **Find all log files (.log) including hidden ones**
   - Search in webapp/logs
   - Display with file sizes

9. **Find all directories named "config"**
   - Search from exercise-01 root

10. **Find all empty directories**
    - Search entire exercise-01 tree

### Part 3: Advanced Navigation (5 points)

11. **Create symbolic link**
    - Create symlink in exercise-01 root pointing to webapp/logs
    - Name it "quick-logs"
    - Verify it works (ls -l)

12. **Navigate using multiple paths**
    - From exercise-01, navigate to webapp/src/models
    - Then navigate to scripts/deployment
    - Then navigate back to webapp/config
    - Document each command

13. **Display directory tree**
    - Show complete structure of webapp directory
    - Include hidden files
    - Limit depth to 3 levels

14. **Find recently modified files**
    - List all files modified in last 7 days
    - Sort by modification time

15. **Count files by type**
    - Count how many .py files exist
    - Count how many .sh files exist
    - Count how many .log files exist

### Part 4: Practical Scenarios (5 points)

16. **Locate configuration files**
    - Find all files with "conf" or "config" in the name
    - Display their locations

17. **Find large files**
    - Find all .tar.gz files
    - Display with human-readable sizes

18. **Check file permissions**
    - List all .sh files with their permissions
    - Identify which are executable

19. **Navigate efficiently**
    - Navigate from exercise-01 to webapp/src/controllers
    - Return to previous directory (use cd -)
    - Return to previous again (should be in controllers)

20. **Create navigation alias**
    - Create an alias "goto-webapp" that navigates to webapp directory
    - Test it works
    - Document the command

---

## Deliverables

Submit a markdown file (`navigation-report.md`) with:

### Section 1: Command Log

For each task (1-20), provide:
```markdown
## Task [Number]: [Task Description]

**Command used**:
```bash
[your command here]
```

**Output**:
```
[command output]
```

**Explanation**: [Why this command works for this task]
```

### Section 2: Directory Map

Create a text representation of the directory structure:
```
exercise-01/
├── webapp/
│   ├── src/
│   │   ├── controllers/
│   │   │   └── user.py
│   │   └── ... (continue)
└── ... (complete structure)
```

### Section 3: Commands Cheat Sheet

Create your own quick reference:
```markdown
## Navigation Commands I Learned

| Command | Purpose | Example |
|---------|---------|---------|
| pwd | ... | pwd |
| cd | ... | cd /path/to/dir |
| ... | ... | ... |
```

### Section 4: Reflection (3-5 sentences)

Answer:
1. What was the most challenging part of this exercise?
2. Which command did you find most useful?
3. What's one navigation trick you'll remember?

---

## Submission Format

```
exercise-01-submission/
├── navigation-report.md
├── commands-used.txt (optional: list of all commands you ran)
└── screenshots/ (optional: terminal screenshots)
```

Create a zip file:
```bash
zip -r exercise-01-joshua-smith.zip navigation-report.md
```

---

## Grading Rubric

| Category | Points | Criteria |
|----------|--------|----------|
| **Part 1: Basic Navigation** | 5 | All commands correct, proper path usage |
| **Part 2: Finding Files** | 5 | Correct use of find command, all files located |
| **Part 3: Advanced Navigation** | 5 | Symbolic links work, efficient navigation |
| **Part 4: Practical Scenarios** | 5 | Real-world tasks completed correctly |
| **Total** | **20** | |

**Detailed Scoring**:
- ✅ **Excellent (90-100%)**: All tasks completed, commands optimized, clear explanations
- ✅ **Good (80-89%)**: Most tasks completed, minor command inefficiencies
- ⚠️ **Needs Work (70-79%)**: Some tasks completed, several incorrect commands
- ❌ **Incomplete (<70%)**: Many tasks missing or incorrect

---

## Hints

<details>
<summary>Hint 1: Showing hidden files</summary>

Use the `-a` flag with `ls`:
```bash
ls -la
```
</details>

<details>
<summary>Hint 2: Finding files</summary>

Basic find syntax:
```bash
find /path -name "pattern"
find . -name "*.py"
```
</details>

<details>
<summary>Hint 3: Human-readable sizes</summary>

Use `-h` flag:
```bash
ls -lh
du -sh
```
</details>

<details>
<summary>Hint 4: Going to previous directory</summary>

```bash
cd -
# Returns to previous directory
```
</details>

<details>
<summary>Hint 5: Creating symbolic links</summary>

```bash
ln -s /path/to/target link-name
```
</details>

---

## Bonus Challenges (Optional, +5 points)

1. **Create a navigation script** (bonus-navigate.sh):
   - Takes directory name as argument
   - Finds that directory in exercise-01 tree
   - Navigates to it
   - Lists contents

2. **Advanced find**:
   - Find all files modified in last hour
   - Find all files larger than 1KB
   - Find all directories with write permission

3. **Directory size report**:
   - Calculate size of each top-level directory
   - Sort by size
   - Display in human-readable format

---

## Common Mistakes to Avoid

❌ **Using absolute paths when relative is shorter**
```bash
# Bad (when already in ~/devops-learning)
cd /home/joshua/devops-learning/module-02/exercise-01

# Good
cd module-02/exercise-01
```

❌ **Forgetting -a flag for hidden files**
```bash
ls          # Misses .env, .gitignore
ls -a       # Shows all files
```

❌ **Not verifying navigation**
```bash
cd webapp
# Did it work? Check!
pwd
```

❌ **Confusing find and ls**
```bash
find .      # Finds all files recursively
ls          # Lists current directory only
```

---

## Learning Resources

- Man pages: `man ls`, `man find`, `man cd`
- Linux filesystem hierarchy: `man hier`
- Practice: [cmdchallenge.com](https://cmdchallenge.com)

---

## What's Next?

After mastering navigation, you'll move to Exercise 2 where you'll analyze log files using text processing commands (grep, awk, sed).

**Navigation is the foundation - master it now!** 🗺️

---

## Solution Preview

<details>
<summary>Example Solutions (Don't peek until you try!)</summary>

```bash
# Task 1: Display current directory
pwd

# Task 6: Find all Python files
find . -name "*.py"

# Task 7: Find hidden files in webapp
find webapp -name ".*"

# Task 11: Create symbolic link
ln -s webapp/logs quick-logs
ls -l quick-logs

# Task 14: Recently modified files
find . -mtime -7 -type f -ls

# Task 15: Count file types
find . -name "*.py" | wc -l
find . -name "*.sh" | wc -l
find . -name "*.log" | wc -l
```
</details>

---

**Good luck! Remember: Practice makes permanent.** 🚀
