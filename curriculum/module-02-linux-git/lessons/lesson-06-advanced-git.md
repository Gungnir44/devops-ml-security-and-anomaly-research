# Lesson 6: Advanced Git - Power User Techniques

**Duration**: 2 hours
**Objectives**: Master advanced Git techniques for complex scenarios

---

## When Basic Git Isn't Enough

**You know Git basics**:
```bash
git add, commit, push, pull, branch, merge
# These handle 80% of daily work
```

**But then**:
```
Boss: "We need to undo the deploy from 3 days ago"
You: "Uh... how?"

Teammate: "Can you apply just that one commit to production?"
You: "What does that mean?"

You: "I have uncommitted changes but need to switch branches!"
Git: "Error: Your local changes would be overwritten"
You: 😰
```

**Advanced Git solves**:
- Complex history manipulation
- Recovering from mistakes
- Working with multiple contexts
- Automating workflows
- Cleaning up messy histories

---

## Git Rebase - Rewriting History

### What is Rebasing?

**Merge** (covered in Lesson 5):
```
feature: [C3] ← [C4]
        /            \
main:  [C1] ← [C2]    [C5] (merge commit)
```
Creates merge commit, preserves both histories

**Rebase**:
```
Before:
feature: [C3] ← [C4]
        /
main:  [C1] ← [C2] ← [C5]

After rebase:
main:  [C1] ← [C2] ← [C5] ← [C3'] ← [C4']
                                      ↑
                                   feature
```
Moves your commits to end of main (rewrites history!)

### When to Rebase

**✅ Use rebase**:
- Cleaning up your local commits before pushing
- Keeping feature branch up-to-date with main
- Creating linear history (easier to read)

**❌ Don't rebase**:
- Commits already pushed to shared branch
- Main/master branch (ever!)
- When others are working on same branch

**Golden Rule**: Never rebase public history!

### Basic Rebase

```bash
# Update feature branch with latest main
git checkout feature-x
git rebase main

# If conflicts:
# 1. Fix conflicts in files
# 2. git add <resolved-files>
# 3. git rebase --continue

# Or abort:
git rebase --abort
```

**Example scenario**:
```bash
# Monday: Create feature branch
git checkout -b feature/add-caching
git commit -m "feat: add caching layer"

# Wednesday: Main has new commits
# Your commits: C1 ← C2 ← C3 (your work)
# Main now:     C1 ← C2 ← C4 ← C5 (others' work)

# Rebase to update
git fetch origin
git rebase origin/main

# Now: C1 ← C2 ← C4 ← C5 ← C3' (your work on top)

# Force push (your branch only!)
git push --force-with-lease origin feature/add-caching
```

### Interactive Rebase - The Power Tool

**Clean up messy commit history**:

```bash
# Your commits (before cleanup):
git log --oneline
# abc123 fix typo
# def456 actually fix the bug
# ghi789 fix bug
# jkl012 wip
# mno345 add feature

# Rebase last 5 commits
git rebase -i HEAD~5
```

**Interactive editor opens**:
```
pick mno345 add feature
pick jkl012 wip
pick ghi789 fix bug
pick def456 actually fix the bug
pick abc123 fix typo

# Commands:
# p, pick = use commit
# r, reword = use commit, but edit message
# e, edit = use commit, but stop to amend
# s, squash = meld into previous commit
# f, fixup = like squash, but discard message
# d, drop = remove commit
```

**Clean it up**:
```
pick mno345 add feature
fixup jkl012 wip
pick ghi789 fix bug
fixup def456 actually fix the bug
fixup abc123 fix typo
```

**Result**:
```bash
# After cleanup:
git log --oneline
# xyz789 fix bug
# mno345 add feature
```

**Real DevOps example**:
```bash
# You made 10 commits while debugging:
git log --oneline
# Commit 10: remove debug print
# Commit 9: add debug print
# Commit 8: try different approach
# Commit 7: revert approach
# Commit 6: fix syntax error
# Commit 5: add logging
# Commit 4: more logging
# Commit 3: actually fix issue
# Commit 2: attempt fix
# Commit 1: add feature

# Clean to 2 commits:
git rebase -i HEAD~10

# Squash into:
# Commit 2: fix deployment timeout issue
# Commit 1: add health check endpoint
```

### Rebase vs Merge - When to Use Each

**Use Merge**:
- Merging feature to main (preserves feature history)
- Public branches
- Want to preserve exact history

**Use Rebase**:
- Updating feature branch with main changes
- Cleaning up local commits
- Want linear history

**Example workflow**:
```bash
# While working: Rebase to stay updated
git checkout feature-x
git fetch origin
git rebase origin/main

# When done: Merge to main
git checkout main
git merge feature-x
```

---

## Git Stash - Temporary Storage

### The Problem

```bash
git checkout feature-a
# ... working on files ...

# Urgent: Need to fix bug on main!
git checkout main
# Error: Your local changes would be overwritten
# Please commit or stash them

# But changes aren't ready to commit!
```

### The Solution: Stash

**Stash** = Temporarily save changes without committing

```bash
# Save changes
git stash

# Or with message
git stash save "WIP: adding user authentication"

# Now working directory is clean
git status
# nothing to commit, working tree clean

# Switch branches
git checkout main
# Fix urgent bug
git commit -m "fix: critical security issue"

# Go back to feature
git checkout feature-a

# Restore stashed changes
git stash pop
```

### Stash Commands

```bash
# Save changes
git stash                          # Stash with auto message
git stash save "message"           # Stash with message
git stash -u                       # Include untracked files

# View stashes
git stash list
# stash@{0}: WIP on feature-a: abc123 add feature
# stash@{1}: On main: def456 fix bug

# Apply stash
git stash pop                      # Apply latest, remove from stash
git stash apply                    # Apply latest, keep in stash
git stash apply stash@{1}          # Apply specific stash

# View stash contents
git stash show                     # Summary
git stash show -p                  # Full diff

# Delete stashes
git stash drop stash@{0}           # Delete specific stash
git stash clear                    # Delete all stashes
```

### Real Scenarios

**Scenario 1: Interrupted work**
```bash
# Working on feature
vim app.py
vim tests.py

# Boss: "Production is down! Fix now!"
git stash save "WIP: user authentication half done"

# Fix production
git checkout main
git checkout -b hotfix/production-down
# ... fix issue ...
git commit -m "fix: resolve database connection pool exhaustion"

# Back to feature
git checkout feature-auth
git stash pop
# Continue working
```

**Scenario 2: Try different approach**
```bash
# Current approach not working
git stash save "Approach 1: using Redis cache"

# Try different approach
# ... write new code ...

# Compare approaches
git diff stash@{0}

# Decide approach 2 is better
git stash drop
```

**Scenario 3: Accidentally on wrong branch**
```bash
# Oh no! Made changes on main instead of feature branch
git stash

# Create proper branch
git checkout -b feature/new-feature

# Apply changes
git stash pop

# Commit on correct branch
git commit -m "feat: add new feature"
```

---

## Cherry-Pick - Selective Commits

### What is Cherry-Picking?

**Copy a specific commit to another branch**

```
main:    [C1] ← [C2] ← [C3]

feature: [C1] ← [C2] ← [C4] ← [C5]

# Cherry-pick C4 to main:
main:    [C1] ← [C2] ← [C3] ← [C4']
```

### When to Cherry-Pick

**✅ Good use cases**:
- Apply hotfix to multiple branches
- Pull single feature from abandoned branch
- Backport fix to older version

**❌ Bad use cases**:
- Instead of merging (just merge!)
- Copy many commits (use merge or rebase)

### How to Cherry-Pick

```bash
# Find commit you want
git log --oneline
# abc123 fix: resolve critical security bug

# Switch to target branch
git checkout main

# Cherry-pick the commit
git cherry-pick abc123

# If conflicts:
# 1. Fix conflicts
# 2. git add <files>
# 3. git cherry-pick --continue

# Or abort
git cherry-pick --abort
```

### Real Example: Hotfix to Multiple Versions

```bash
# Production runs v1.0, v2.0, v3.0
# Security bug found, need to fix all versions

# Fix on main (v3.0)
git checkout main
git checkout -b hotfix/security-issue
# ... fix bug ...
git commit -m "fix: resolve SQL injection vulnerability"
git log --oneline  # abc123

# Merge to main
git checkout main
git merge hotfix/security-issue

# Apply to v2.0
git checkout release/v2.0
git cherry-pick abc123
# Resolve any conflicts
git push

# Apply to v1.0
git checkout release/v1.0
git cherry-pick abc123
# Resolve any conflicts
git push

# Now all versions have the fix!
```

### Cherry-Pick Multiple Commits

```bash
# Pick commits abc123, def456, ghi789
git cherry-pick abc123 def456 ghi789

# Pick range of commits
git cherry-pick abc123..ghi789

# Pick without committing (to make changes first)
git cherry-pick -n abc123
# Make changes
git commit
```

---

## Git Reflog - Time Machine

### What is Reflog?

**Reflog** = Reference log = History of where HEAD has been

**Even if commits seem lost, reflog remembers!**

```bash
git reflog

# Output:
# abc123 HEAD@{0}: commit: add feature
# def456 HEAD@{1}: checkout: moving from main to feature-x
# ghi789 HEAD@{2}: commit: fix bug
# jkl012 HEAD@{3}: reset: moving to HEAD~1
```

### Recovering "Lost" Commits

**Scenario: Accidentally deleted branch**
```bash
# Oops! Deleted branch with important work
git branch -D feature-important
# Deleted branch feature-important (was abc123).

# Oh no! I needed that!

# Find the commit
git reflog
# abc123 HEAD@{1}: commit: important work

# Recover it
git checkout -b feature-important abc123
# Branch recovered!
```

**Scenario: Destructive reset**
```bash
# Before:
# [C1] ← [C2] ← [C3] ← [C4]
#                       ↑
#                     HEAD

# Accidentally:
git reset --hard HEAD~3
# HEAD is now at C1

# All work gone! ... or is it?

# Check reflog
git reflog
# abc123 HEAD@{0}: reset: moving to HEAD~3
# def456 HEAD@{1}: commit: C4

# Recover
git reset --hard def456
# Back to C4!
```

### Reflog Commands

```bash
# View reflog
git reflog                    # Show all HEAD movements
git reflog show feature-x     # Reflog for specific branch

# Recover using reflog
git checkout HEAD@{5}         # Go to 5 moves ago
git reset --hard HEAD@{2}     # Reset to 2 moves ago

# Create branch from reflog
git branch recovered HEAD@{3}

# Reflog is local only (not pushed to remote)
# Entries expire after 90 days (configurable)
```

---

## Undoing Things (Comprehensive Guide)

### Scenario 1: Unstaged changes (not added)

```bash
# Undo changes to one file
git checkout -- file.txt
# or
git restore file.txt

# Undo all changes
git checkout -- .
# or
git restore .
```

### Scenario 2: Staged changes (added but not committed)

```bash
# Unstage one file (keep changes)
git reset HEAD file.txt
# or
git restore --staged file.txt

# Unstage all (keep changes)
git reset HEAD
# or
git restore --staged .
```

### Scenario 3: Committed locally (not pushed)

```bash
# Undo last commit, keep changes
git reset --soft HEAD~1

# Undo last commit, discard changes (DANGEROUS!)
git reset --hard HEAD~1

# Undo last commit, keep files but unstage
git reset --mixed HEAD~1  # (default)

# Amend last commit (change message or add files)
git commit --amend -m "better message"
```

### Scenario 4: Pushed to remote

```bash
# Create new commit that undoes changes
git revert abc123

# Reverts are safe for shared branches
# Creates new commit (doesn't rewrite history)
```

### Scenario 5: Multiple commits to undo

```bash
# Undo last 3 commits
git revert HEAD~3..HEAD

# Or create new commit reverting to specific point
git revert --no-commit HEAD~3..HEAD
git commit -m "Revert last 3 commits"
```

### Scenario 6: Disaster - Everything is broken

```bash
# Nuclear option: Reset to remote
git fetch origin
git reset --hard origin/main

# Warning: Loses ALL local changes!
```

### Decision Tree

```
Need to undo?
│
├─ Not committed yet?
│  ├─ Not staged? → git restore file.txt
│  └─ Staged? → git restore --staged file.txt
│
├─ Committed locally (not pushed)?
│  ├─ Keep changes? → git reset --soft HEAD~1
│  └─ Discard changes? → git reset --hard HEAD~1
│
└─ Already pushed?
   └─ Create revert commit → git revert abc123
```

---

## Git Hooks - Automation

### What are Hooks?

**Hooks** = Scripts that run automatically at Git events

**Located**: `.git/hooks/` directory

**Events**:
- `pre-commit`: Before commit is created
- `commit-msg`: Edit/validate commit message
- `pre-push`: Before push to remote
- `post-merge`: After successful merge

### Example: Pre-Commit Hook (Run Tests)

```bash
# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Run tests before allowing commit

echo "Running tests..."
pytest

if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi

echo "Tests passed! Proceeding with commit."
exit 0
EOF

# Make executable
chmod +x .git/hooks/pre-commit

# Now tests run automatically before every commit
git commit -m "feat: add feature"
# Running tests...
# ✓ All tests passed!
# [main abc123] feat: add feature
```

### Example: Commit Message Validation

```bash
# Create commit-msg hook
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash
# Validate commit message format

commit_msg=$(cat "$1")

# Require format: "type: message"
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore): .+"; then
    echo "ERROR: Commit message must start with type (feat|fix|docs|style|refactor|test|chore)"
    echo "Example: feat: add user login"
    exit 1
fi

exit 0
EOF

chmod +x .git/hooks/commit-msg

# Now enforced:
git commit -m "added stuff"
# ERROR: Commit message must start with type

git commit -m "feat: added stuff"
# ✓ Valid commit message
```

### Example: Pre-Push Hook (Prevent Pushing to Main)

```bash
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash

protected_branch='main'
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if [ "$current_branch" = "$protected_branch" ]; then
    echo "ERROR: Direct push to $protected_branch is not allowed!"
    echo "Please use a feature branch and create a pull request."
    exit 1
fi

exit 0
EOF

chmod +x .git/hooks/pre-push

# Now protected:
git checkout main
git push
# ERROR: Direct push to main is not allowed!
```

### Real DevOps Hook: Auto-Format Code

```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Auto-format Python code before commit

echo "Formatting Python files..."

# Find staged Python files
python_files=$(git diff --cached --name-only --diff-filter=ACM | grep '.py$')

if [ -n "$python_files" ]; then
    # Format with black
    black $python_files

    # Re-add formatted files
    git add $python_files

    echo "✓ Formatted $(echo $python_files | wc -w) Python files"
fi

exit 0
EOF

chmod +x .git/hooks/pre-commit
```

---

## Advanced Techniques

### Bisect - Find Bug Introduction

**Problem**: Bug exists but you don't know which commit introduced it

**Solution**: Binary search through commits

```bash
# Start bisect
git bisect start

# Mark current as bad
git bisect bad

# Mark old commit as good (when bug didn't exist)
git bisect good abc123

# Git checks out middle commit
# Test if bug exists
git bisect bad    # Bug exists
# or
git bisect good   # Bug doesn't exist

# Repeat until Git finds the commit
# Bisecting: 2 revisions left to test
# ... test again ...

# Git finds it:
# abc789 is the first bad commit
# commit abc789
# Author: Developer
# Date: Mon Nov 13
#     feat: add caching layer

# End bisect
git bisect reset
```

**Automated bisect**:
```bash
# If you have a test script
git bisect start
git bisect bad
git bisect good v1.0

# Run bisect automatically
git bisect run pytest tests/test_feature.py

# Git automatically finds the bad commit!
```

### Worktrees - Multiple Working Directories

**Problem**: Need to work on two branches simultaneously

**Bad solution**: Clone repo twice

**Good solution**: Worktrees

```bash
# Main repo
/project (main branch)

# Create worktree for feature
git worktree add ../project-feature feature/new-feature

# Now you have:
/project (main branch)
/project-feature (feature/new-feature branch)

# Work in both simultaneously!

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../project-feature
```

**Use case**:
```bash
# Working on feature in /project
cd /project

# Urgent fix needed on main
git worktree add ../project-hotfix main
cd ../project-hotfix
# Fix bug
git commit -m "fix: critical issue"
git push

# Back to feature work
cd /project
# Feature changes untouched!
```

### Aliases - Speed Up Common Commands

```bash
# Add to ~/.gitconfig
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual 'log --oneline --graph --all'

# Use aliases
git st          # git status
git co main     # git checkout main
git visual      # Pretty log
```

**Complex aliases**:
```bash
# ~/.gitconfig
[alias]
    # Show pretty log
    lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit

    # List aliases
    aliases = config --get-regexp ^alias\\.

    # Undo last commit
    undo = reset --soft HEAD~1

    # Amend without editing message
    amend = commit --amend --no-edit
```

---

## Disaster Recovery Scenarios

### Scenario 1: Accidentally Committed Secrets

```bash
# OH NO!
git add .env
git commit -m "add config"
git push

# .env contains API keys! 😱

# Solution:
# 1. Remove from repo
git rm --cached .env
echo ".env" >> .gitignore
git commit -m "remove secrets from tracking"

# 2. Rewrite history (if not too late)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Force push (coordinate with team!)
git push --force-with-lease

# 4. ROTATE SECRETS (most important!)
# Change API keys, passwords, etc.
```

### Scenario 2: Merge Conflict Disaster

```bash
# Tried to merge, everything broke
git merge feature-x
# CONFLICT! panic! mess!

# Abort and start over
git merge --abort

# Try again with strategy
git merge feature-x -X ours    # Prefer our changes
# or
git merge feature-x -X theirs  # Prefer their changes
```

### Scenario 3: Lost Commits

```bash
# Deleted branch or hard reset
# Commits seem gone

# Find in reflog
git reflog

# Recover
git checkout -b recovered abc123
# or
git cherry-pick abc123
```

### Scenario 4: Wrong Files Committed

```bash
# Committed huge files, binary files, etc.
git log --stat  # Find the commit

# Remove from history
git filter-branch --tree-filter 'rm -f huge-file.bin' HEAD

# Or use BFG (faster)
# Install BFG: brew install bfg
bfg --delete-files huge-file.bin

git push --force-with-lease
```

---

## Best Practices

### ✅ Do

1. **Use branches for everything**
2. **Rebase private branches, merge public ones**
3. **Write meaningful commit messages**
4. **Commit often (atomic commits)**
5. **Pull before push**
6. **Use hooks for automation**
7. **Keep reflog (don't panic!)**

### ❌ Don't

1. **Never rebase public history**
2. **Never commit secrets**
3. **Never force push to main**
4. **Don't use `git reset --hard` without understanding**
5. **Don't cherry-pick instead of merging**

---

## Summary

**You now know**:
- Rebasing (regular and interactive)
- Stashing for temporary storage
- Cherry-picking specific commits
- Reflog for disaster recovery
- Comprehensive undo strategies
- Git hooks for automation
- Advanced techniques (bisect, worktrees, aliases)

**You are now a Git power user!** 🚀

**Next**: Exercises and Project to practice these skills

**Practice**: Try interactive rebase, set up hooks, practice disaster recovery in a test repo!

---

## Quick Reference

```bash
# Rebase
git rebase main                    # Rebase on main
git rebase -i HEAD~5               # Interactive rebase last 5
git rebase --abort                 # Cancel rebase

# Stash
git stash                          # Stash changes
git stash pop                      # Apply and remove
git stash list                     # List stashes
git stash drop                     # Delete stash

# Cherry-pick
git cherry-pick abc123             # Apply commit abc123
git cherry-pick abc123..def456     # Apply range

# Reflog
git reflog                         # View history
git reset --hard HEAD@{2}          # Recover from reflog

# Undo
git restore file.txt               # Undo unstaged
git restore --staged file.txt      # Unstage
git reset --soft HEAD~1            # Undo commit (keep changes)
git revert abc123                  # Create revert commit

# Hooks
.git/hooks/pre-commit              # Before commit
.git/hooks/pre-push                # Before push
chmod +x .git/hooks/pre-commit     # Make executable
```

**You've mastered Git! Time to practice with real projects.** 🎓
