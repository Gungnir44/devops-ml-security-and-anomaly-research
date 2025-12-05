# Module 2: Linux & Git Fundamentals

**Duration**: 2 weeks (10-15 hours/week)
**Prerequisites**: Module 1 (DevOps Fundamentals)
**Deliverable**: Git workflow demonstration and Linux automation script

---

## Overview

This module teaches the **foundational tools of DevOps**: the Linux command line and Git version control. These are non-negotiable skills - every DevOps engineer uses them daily.

**Why This Matters**:
- 96% of web servers run Linux
- Git is the universal standard for version control
- Infrastructure automation requires shell scripting
- CI/CD pipelines run on Linux containers

**By the end of this module, you'll**:
- Navigate Linux systems confidently
- Write shell scripts to automate tasks
- Use Git like a professional developer
- Collaborate using Git workflows (branching, merging, pull requests)
- Troubleshoot common Linux and Git issues

---

## Learning Objectives

### Linux Fundamentals
- [ ] Navigate filesystem using command line (cd, ls, pwd, find)
- [ ] Manage files and directories (cp, mv, rm, mkdir, chmod, chown)
- [ ] View and edit files (cat, less, nano, vim)
- [ ] Work with processes (ps, top, kill, systemctl)
- [ ] Understand Linux permissions and ownership
- [ ] Use pipes, redirection, and filters (grep, awk, sed)
- [ ] Write basic shell scripts (variables, loops, conditionals)
- [ ] Manage packages (apt, yum, dnf)

### Git Fundamentals
- [ ] Understand Git's data model (commits, trees, blobs)
- [ ] Initialize repositories and track changes
- [ ] Stage and commit code effectively
- [ ] Write meaningful commit messages
- [ ] Navigate history (log, diff, blame)
- [ ] Work with branches (create, switch, merge)
- [ ] Resolve merge conflicts
- [ ] Use remote repositories (clone, push, pull, fetch)
- [ ] Collaborate via pull requests
- [ ] Implement Git workflows (feature branches, GitFlow)

---

## Module Structure

### Week 1: Linux Mastery

**Lesson 1**: Why Linux? (1 hour)
- Linux history and philosophy
- Why DevOps runs on Linux
- Distributions (Ubuntu, CentOS, Alpine)
- Linux vs. Windows/Mac

**Lesson 2**: Essential Commands (2 hours)
- Filesystem navigation
- File operations
- Text processing (grep, awk, sed)
- Permissions and ownership

**Lesson 3**: Shell Scripting Basics (2 hours)
- Variables and parameters
- Conditionals and loops
- Functions
- Error handling

**Exercise 1**: File System Navigation Challenge
**Exercise 2**: Log Analysis with Shell Commands
**Exercise 3**: Automation Script (backup, cleanup, monitoring)

### Week 2: Git Workflows

**Lesson 4**: Version Control Fundamentals (1.5 hours)
- Why version control exists
- Git vs. SVN, Mercurial
- Git's data model
- Best practices

**Lesson 5**: Git Essentials (2 hours)
- Basic commands (init, add, commit, status)
- Branching and merging
- Remote repositories
- Collaboration workflows

**Lesson 6**: Advanced Git (2 hours)
- Rebasing vs. merging
- Cherry-picking
- Stashing
- Undoing mistakes (reset, revert, reflog)
- Git hooks

**Exercise 4**: Git Workflow Simulation
**Exercise 5**: Collaborative Development (branching, PRs, code review)
**Exercise 6**: Git Disaster Recovery

---

## Assessments

### Quiz (20 points, 80% to pass)
- Linux commands and concepts (10 points)
- Git operations and workflows (10 points)
- Scenario-based questions

### Project: Automated DevOps Workflow (100 points)
Build a complete Git workflow with automation:
1. Shell script that automates server setup
2. Git repository with proper structure
3. Feature branch workflow demonstration
4. Pre-commit hooks for validation
5. Documentation and README

**Portfolio Quality**: This project demonstrates professional development practices

---

## Resources

- [`cheat-sheet.md`](resources/cheat-sheet.md) - Quick reference for commands
- [`glossary.md`](resources/glossary.md) - Linux and Git terminology
- [`further-reading.md`](resources/further-reading.md) - Books, tutorials, practice sites

---

## Time Commitment

| Activity | Time/Week |
|----------|-----------|
| Lessons | 4-5 hours |
| Exercises | 4-6 hours |
| Quiz + Project | 2-4 hours |
| **Total** | **10-15 hours** |

---

## Success Criteria

**You're ready to move on when you can**:
- [ ] Navigate Linux filesystem without GUI
- [ ] Write shell scripts to automate repetitive tasks
- [ ] Explain Git's data model
- [ ] Create feature branches and submit pull requests
- [ ] Resolve merge conflicts confidently
- [ ] Use Git to collaborate with a team
- [ ] Debug common Linux and Git issues
- [ ] Pass quiz with 80%+ (16/20)
- [ ] Complete project demonstrating professional Git workflow

---

## Common Pitfalls to Avoid

### Linux
- ❌ Using `rm -rf /` or dangerous commands without understanding
- ❌ Ignoring file permissions (causes deployment failures)
- ❌ Not using man pages (`man command`)
- ❌ Copy-pasting commands without understanding
- ✅ Practice in safe environments first
- ✅ Read error messages carefully

### Git
- ❌ Committing to master/main directly
- ❌ Vague commit messages ("fixed stuff", "wip")
- ❌ Not pulling before pushing (causes conflicts)
- ❌ Committing sensitive data (passwords, API keys)
- ✅ Use feature branches
- ✅ Write descriptive commit messages
- ✅ Review changes before committing

---

## Getting Started

### Step 1: Setup Linux Environment

**Option A: Windows (WSL2)**
```bash
# Install WSL2
wsl --install -d Ubuntu

# Verify
wsl -l -v
```

**Option B: Mac**
```bash
# Already Unix-based! Use Terminal
# Install Homebrew for package management
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Option C: Linux**
```bash
# You're already set! Open terminal
```

### Step 2: Verify Git Installation

```bash
git --version
# Should show git version 2.x+

# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify
git config --list
```

### Step 3: Start Learning!

1. Read Lesson 1: Why Linux?
2. Complete Exercise 1
3. Continue through all lessons and exercises
4. Take quiz when ready
5. Build final project

---

## Practice Environment

Create a practice directory for this module:

```bash
mkdir ~/devops-learning/module-02
cd ~/devops-learning/module-02

# Create practice folders
mkdir linux-practice git-practice scripts

# You'll use these throughout the module
```

---

## Questions to Answer by Module End

1. **Linux**: Why are permissions critical in production environments?
2. **Shell Scripting**: When should you write a script vs. run commands manually?
3. **Git**: Why do we use feature branches instead of committing to main?
4. **Git**: What's the difference between merge and rebase? When to use each?
5. **Workflows**: How does Git enable collaboration among distributed teams?

---

## Real-World Application

After this module, you'll be able to:
- SSH into servers and troubleshoot issues
- Automate deployment tasks with shell scripts
- Manage infrastructure configuration files in Git
- Collaborate with team using pull request workflows
- Review code changes before merging
- Roll back deployments using Git history
- Set up Git hooks for automated testing

---

## Module Dependencies

**Builds on**: Module 1 (DevOps culture, why automation matters)
**Prepares for**:
- Module 3 (Python scripts will use Linux and Git)
- Module 4 (Docker containers run on Linux)
- Module 5 (CI/CD pipelines use Git triggers)
- All future modules (everything runs on Linux, versioned in Git)

---

## Let's Begin!

**Your learning path**:
1. Start with `lessons/lesson-01-why-linux.md`
2. Work through exercises as you complete lessons
3. Use the cheat sheet as a reference
4. Practice daily (muscle memory!)
5. Take quiz when comfortable with content
6. Build the final project
7. Review and retain (use flashcards!)

**Remember**: These skills are foundational. Every minute spent mastering Linux and Git pays dividends throughout your entire DevOps career.

**Ready? Let's dive in!** 🚀
