# Exercise 6: Git Disaster Recovery

**Duration**: 45-60 minutes
**Difficulty**: Advanced
**Prerequisites**: Lessons 4-6
**Points**: 20

---

## Objectives

By completing this exercise, you will:
- Recover from common Git mistakes
- Use reflog to find "lost" commits
- Undo changes safely
- Handle destructive operations
- Restore deleted branches and commits
- Master Git safety techniques

---

## Scenario

Welcome to Git Disaster Recovery Training! You're a DevOps engineer who needs to learn how to fix Git mistakes before they happen in production.

You'll intentionally create disasters and then fix them, building muscle memory for when real disasters happen.

**Important**: Do this exercise in a test repository! Never practice these techniques on production code.

---

## Setup

```bash
# Create disaster recovery lab
mkdir -p ~/devops-learning/module-02/exercise-06
cd ~/devops-learning/module-02/exercise-06

# Initialize repository
git init disaster-lab
cd disaster-lab

# Create initial project
cat > README.md << 'EOF'
# Disaster Recovery Lab
Learning to fix Git mistakes safely
EOF

cat > app.py << 'EOF'
def main():
    print("Version 1")

if __name__ == "__main__":
    main()
EOF

git add .
git commit -m "chore: initial commit"

# Create some history
echo 'def helper(): return "v2"' >> app.py
git commit -am "feat: add helper function"

echo 'VERSION = "2.0"' >> app.py
git commit -am "chore: add version"

# Create branch with important work
git checkout -b feature/important-work
echo "Important code here" > important.py
git add important.py
git commit -m "feat: add critical feature"

git checkout main
```

---

## Part 1: Undo Mistakes (5 points)

### Disaster 1.1: Committed to Wrong Branch

**Mistake**: You made commits on main instead of a feature branch

```bash
# Accidentally on main
git checkout main

# Make changes meant for feature branch
echo "New feature code" > feature.py
git add feature.py
git commit -m "feat: add new feature"

echo "More feature code" >> feature.py
git commit -am "feat: extend new feature"

# Oh no! These should be on a feature branch!
```

**Recovery**:
```bash
# See what commits you made
git log --oneline -3

# Note the commit hashes (e.g., abc123 and def456)

# Create feature branch from current position
git branch feature/new-feature

# Reset main to before your commits (3 commits back: 2 feature + 1)
# Find where main should be
git log --oneline -5

# Reset main to before feature commits (use hash or HEAD~2)
git reset --hard HEAD~2

# Verify main is back to original state
git log --oneline

# Switch to feature branch - commits are safe there!
git checkout feature/new-feature
git log --oneline
```

**Deliverable**:
- Document the commands used
- Explain what `git reset --hard` does
- Show commits are on correct branch

### Disaster 1.2: Committed Sensitive Data

**Mistake**: Accidentally committed API keys

```bash
# Create file with secrets
cat > config.py << 'EOF'
DATABASE_URL = "postgresql://user:password@localhost/db"
API_KEY = "sk_live_SuperSecretKey123456789"
SECRET_TOKEN = "abc123def456ghi789"
EOF

git add config.py
git commit -m "Add configuration"

# Realized mistake!
git log --oneline -1
```

**Recovery Method 1: If not pushed yet**
```bash
# Remove from last commit
git reset --soft HEAD~1  # Undo commit, keep changes

# Remove sensitive file
rm config.py

# Create sanitized version
cat > config.py << 'EOF'
# Load from environment variables
import os

DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
EOF

# Create .env.example for documentation
cat > .env.example << 'EOF'
DATABASE_URL=postgresql://user:password@localhost/db
API_KEY=your_api_key_here
SECRET_TOKEN=your_secret_token_here
EOF

# Add to .gitignore
echo ".env" >> .gitignore
echo "config_local.py" >> .gitignore

# Commit properly
git add config.py .env.example .gitignore
git commit -m "feat: add configuration with environment variables"
```

**Recovery Method 2: If already in history**
```bash
# Remove file from all history (DANGEROUS - rewrites history)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch config.py" \
  --prune-empty --tag-name-filter cat -- --all

# Or use BFG Repo-Cleaner (recommended for large repos)
# bfg --delete-files config.py
```

**Deliverable**:
- Show both recovery methods
- Create secure alternative
- Add to .gitignore

### Disaster 1.3: Amending the Wrong Commit

**Mistake**: Used `--amend` on a pushed commit

```bash
# Make a commit
echo "v3" > version.txt
git add version.txt
git commit -m "Update version to v3"

# Simulate push (we'll mark this commit)
PUSHED_COMMIT=$(git rev-parse HEAD)
echo "Pretend commit $PUSHED_COMMIT was pushed"

# Oops, forgot something, amend it
echo "v3.1" > version.txt
git commit -a --amend -m "Update version to v3.1"

# But original commit was already pushed!
# Now history diverged
```

**Recovery**:
```bash
# Don't force push! Instead, create new commit
git reset --soft $PUSHED_COMMIT

# Now create new commit with changes
git commit -m "Update version to v3.1"

# This preserves history, safe for pushed commits
```

**Deliverable**:
- Explain why amending pushed commits is dangerous
- Show safe alternative

---

## Part 2: Recovering Lost Commits (5 points)

### Disaster 2.1: Deleted Branch with Important Work

**Mistake**: Deleted branch before merging

```bash
# Create feature branch
git checkout -b feature/awesome-feature
echo "Awesome code" > awesome.py
git add awesome.py
git commit -m "feat: add awesome feature"

echo "More awesome code" >> awesome.py
git commit -am "feat: enhance awesome feature"

# Get commit hash (for verification later)
AWESOME_COMMIT=$(git rev-parse HEAD)

# Switch to main and delete branch
git checkout main
git branch -D feature/awesome-feature

# Oh no! Realized we needed that feature!
```

**Recovery using reflog**:
```bash
# View reflog to find deleted branch
git reflog

# Find the commit (look for "commit: feat: enhance awesome feature")
# You'll see something like: abc123 HEAD@{3}: commit: feat: enhance awesome feature

# Recover the branch
git checkout -b feature/awesome-feature-recovered $AWESOME_COMMIT

# Or if you don't have the hash, use reflog reference
git checkout -b feature/awesome-feature-recovered HEAD@{3}

# Verify all commits are there
git log --oneline
```

**Deliverable**:
- Delete a branch
- Use reflog to find it
- Recreate the branch
- Verify all commits recovered

### Disaster 2.2: Hard Reset Wiped Out Work

**Mistake**: Used `git reset --hard` and lost commits

```bash
# Create some commits
echo "Work 1" > work1.txt
git add work1.txt
git commit -m "Add work 1"

echo "Work 2" > work2.txt
git add work2.txt
git commit -m "Add work 2"

echo "Work 3" > work3.txt
git add work3.txt
git commit -m "Add work 3"

# Save commit hash for verification
WORK3_COMMIT=$(git rev-parse HEAD)

# Accidentally hard reset
git reset --hard HEAD~3

# All work gone!
git log --oneline  # Only shows old commits
ls  # work*.txt files are gone!
```

**Recovery**:
```bash
# Use reflog to find lost commits
git reflog

# Find "Add work 3" commit
# Restore to that point
git reset --hard $WORK3_COMMIT

# Or use reflog reference
git reset --hard HEAD@{1}  # Adjust number as needed

# Verify everything is back
ls
git log --oneline
```

**Deliverable**:
- Demonstrate accidental hard reset
- Recover using reflog
- Explain how reflog saves you

### Disaster 2.3: Recover Uncommitted Changes

**Mistake**: Discarded uncommitted changes accidentally

```bash
# Make changes but don't commit
echo "Important work" > important-work.txt
echo "More important stuff" >> important-work.txt

# Accidentally checkout (loses changes)
git checkout -- important-work.txt

# Changes gone!
cat important-work.txt  # File is empty or gone
```

**Recovery**:
```bash
# Unfortunately, uncommitted changes without git add are LOST FOREVER
# This is why we commit early and often!

# But if you had staged them:
echo "Important work" > important-work.txt
git add important-work.txt

# Then accidentally reset
git reset --hard HEAD

# You might find them with git fsck
git fsck --lost-found

# Look in .git/lost-found/other/
# But this rarely works for unstaged changes
```

**Prevention**:
```bash
# Use stash for safety
echo "Important work" > important-work.txt
git stash save "WIP: important work"

# Now it's safe in stash
git stash list
git stash pop  # When ready to restore
```

**Deliverable**:
- Demonstrate that unstaged changes can't be recovered
- Show how to use stash for safety
- Explain importance of committing often

---

## Part 3: Fixing Merge Disasters (5 points)

### Disaster 3.1: Merge Conflict Panic

**Mistake**: Started merge, got conflicts, panicked

```bash
# Create conflicting branches
git checkout -b branch-a
echo "Version A" > conflict.txt
git add conflict.txt
git commit -m "Add version A"

git checkout main
git checkout -b branch-b
echo "Version B" > conflict.txt
git add conflict.txt
git commit -m "Add version B"

# Try to merge
git checkout main
git merge branch-a
git merge branch-b

# Conflict! Panic!
# Made bad edits, things are broken
```

**Recovery**:
```bash
# Abort the merge!
git merge --abort

# Everything is back to pre-merge state
git status

# Try again when ready, calmly
git merge branch-b

# Resolve conflicts properly this time
cat > conflict.txt << 'EOF'
Version A and B combined
EOF

git add conflict.txt
git commit -m "Merge branch-b: resolved conflicts"
```

**Deliverable**:
- Create merge conflict
- Abort it
- Retry and resolve properly

### Disaster 3.2: Merged Wrong Branch

**Mistake**: Merged feature to main before it was ready

```bash
# Feature branch with incomplete work
git checkout -b feature/half-baked
echo "Incomplete feature" > incomplete.py
git add incomplete.py
git commit -m "WIP: feature not done"

# Accidentally merge to main
git checkout main
git merge feature/half-baked

# Oh no! Incomplete code in main!
```

**Recovery**:
```bash
# Undo the merge
git reset --hard HEAD~1

# Or if already pushed, revert the merge
git revert -m 1 HEAD

# Verify main is clean
git log --oneline
```

**Deliverable**:
- Create accidental merge
- Undo it with reset (local) or revert (pushed)

---

## Part 4: Advanced Recovery Scenarios (5 points)

### Disaster 4.1: Recover from Rebase Disaster

**Mistake**: Rebased and lost commits

```bash
# Create commits
git checkout -b feature/rebase-test
echo "Commit 1" > file1.txt
git add file1.txt
git commit -m "Commit 1"

echo "Commit 2" > file2.txt
git add file2.txt
git commit -m "Commit 2"

# Save state
BEFORE_REBASE=$(git rev-parse HEAD)

# Attempt rebase, make mistakes, abort
git rebase -i HEAD~2
# In editor, accidentally delete lines, save

# Commits gone!
```

**Recovery**:
```bash
# Find lost commits with reflog
git reflog

# Reset to before rebase
git reset --hard $BEFORE_REBASE

# Or use reflog reference
git reset --hard HEAD@{1}
```

**Deliverable**:
- Simulate rebase problem
- Recover using reflog

### Disaster 4.2: Pushed to Wrong Remote

**Mistake**: Pushed to production instead of staging

```bash
# Set up two remotes (simulate)
git remote add staging ../staging-repo.git
git remote add production ../production-repo.git

# Accidentally push to production
git push production main  # Meant to push to staging!
```

**Recovery**:
```bash
# If you catch it immediately
git push production main --force-with-lease  # Revert

# Better: revert the commit on production
git revert HEAD
git push production main

# Then push to correct remote
git push staging main
```

**Deliverable**:
- Explain consequences of wrong push
- Show safe recovery method

---

## Part 5: Prevention Best Practices (Bonus)

### Create Safety Aliases

```bash
# Add to ~/.gitconfig
git config --global alias.undo 'reset --soft HEAD~1'
git config --global alias.unstage 'reset HEAD'
git config --global alias.uncommit 'reset --soft HEAD~1'
git config --global alias.save 'stash save'
git config --global alias.restore-from 'reset --hard'

# Safer operations
git config --global alias.safe-checkout 'checkout -b'
```

### Create Pre-Push Hook

```bash
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash

# Prevent accidental push to main
protected_branches='main master production'

current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

for branch in $protected_branches; do
    if [ "$current_branch" = "$branch" ]; then
        read -p "You're pushing to $branch. Are you sure? (yes/no) " confirm
        if [ "$confirm" != "yes" ]; then
            echo "Push aborted."
            exit 1
        fi
    fi
done

exit 0
EOF

chmod +x .git/hooks/pre-push
```

**Deliverable**:
- Set up helpful aliases
- Create safety hooks
- Document your safety workflow

---

## Deliverables

Submit `disaster-recovery-report.md`:

### Section 1: Disaster Scenarios

For each disaster:
```markdown
## Disaster X.Y: [Name]

**What Happened**:
[Describe the mistake]

**Commands Used to Create Disaster**:
```bash
[commands]
```

**Recovery Process**:
```bash
[recovery commands with explanations]
```

**Verification**:
[How you verified recovery worked]

**Lesson Learned**:
[What you learned from this disaster]
```

### Section 2: Reflog Deep Dive

```markdown
## Understanding Reflog

**My reflog output**:
```
[paste git reflog output]
```

**Explanation**:
- Entry HEAD@{0}: [what happened here]
- Entry HEAD@{1}: [what happened here]
- ... continue for 5 entries

**How I used reflog**:
[Specific examples from your recovery]
```

### Section 3: Prevention Strategies

```markdown
## My Git Safety Rules

1. [Rule 1 and why]
2. [Rule 2 and why]
3. [Rule 3 and why]

## Safety Aliases I Created

```bash
[your aliases]
```

## Hooks I Implemented

```bash
[your hooks]
```
```

---

## Grading Rubric

| Category | Points | Criteria |
|----------|--------|----------|
| **Part 1: Undo Mistakes** | 5 | All scenarios completed, proper recovery |
| **Part 2: Lost Commits** | 5 | Reflog usage, branches/commits recovered |
| **Part 3: Merge Disasters** | 5 | Conflicts resolved, bad merges undone |
| **Part 4: Advanced Recovery** | 5 | Complex scenarios handled correctly |
| **Total** | **20** | |

**Bonus** (+5):
- Create comprehensive safety toolkit
- Document real disaster you recovered from
- Create tutorial for team

---

## Safety Checklist

Before ANY destructive operation:

- [ ] Run `git status` to see current state
- [ ] Run `git log --oneline -5` to see recent history
- [ ] Create backup branch: `git branch backup-before-operation`
- [ ] Know how to use `git reflog`
- [ ] Know how to abort (merge, rebase, etc.)
- [ ] Test on dummy repository first

---

## What You'll Learn

After this exercise:
- ✅ Recover from any Git mistake confidently
- ✅ Master reflog for finding lost work
- ✅ Undo changes safely without data loss
- ✅ Prevent common disasters with hooks and aliases
- ✅ Stay calm when Git disasters happen

**With great power comes great responsibility - practice here first!** 🦸

---

## Real-World Wisdom

**Things you can recover from:**
- Deleted branches (reflog)
- Bad commits (revert, reset)
- Merge conflicts (abort, resolve)
- Accidental hard resets (reflog)

**Things you CANNOT recover:**
- Uncommitted, unstaged changes (lost forever!)
- Force-pushed branches (remote overwritten)
- Files never added to Git

**Golden rule**: **Commit early, commit often!**

---

**Congratulations!** You've completed all Git exercises. You're now ready for the final project!
