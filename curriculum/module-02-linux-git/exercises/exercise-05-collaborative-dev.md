# Exercise 5: Collaborative Development

**Duration**: 60-75 minutes
**Difficulty**: Advanced
**Prerequisites**: Lessons 4-6, Exercise 4
**Points**: 25

---

## Objectives

By completing this exercise, you will:
- Work with remote repositories (GitHub/GitLab simulation)
- Create and review pull requests
- Collaborate using Git workflows
- Handle remote branch operations
- Simulate real team collaboration

---

## Scenario

You're joining a development team at TechCorp. The project uses GitHub for collaboration with strict workflows:
- All changes via pull requests (no direct commits to main)
- Code review required for all PRs
- Feature branches must be up-to-date before merging
- Automated tests must pass (simulated)

You'll simulate being both a developer and a reviewer.

---

## Setup

### Option 1: Using GitHub (Recommended)

```bash
# Create repository on GitHub
# 1. Go to github.com
# 2. Click "New Repository"
# 3. Name: devops-collaboration-exercise
# 4. Make it public or private
# 5. Initialize with README

# Clone locally
git clone https://github.com/YOUR_USERNAME/devops-collaboration-exercise.git
cd devops-collaboration-exercise
```

### Option 2: Using Local Repositories (If no GitHub access)

```bash
# Create "remote" repository (simulated)
mkdir -p ~/devops-learning/module-02/exercise-05
cd ~/devops-learning/module-02/exercise-05

# Create bare repository (acts as "remote")
git init --bare remote-repo.git

# Create local clone
git clone remote-repo.git my-local-repo
cd my-local-repo

# Create initial structure
cat > README.md << 'EOF'
# Team Collaboration Project
DevOps exercise for practicing collaborative Git workflows
EOF

git add README.md
git commit -m "chore: initial commit"
git push origin main
```

---

## Part 1: Setting Up Collaboration (5 points)

### Task 1.1: Configure Repository

```bash
# Set up branch protection (on GitHub)
# Settings → Branches → Add rule for 'main'
# - Require pull request reviews
# - Require status checks to pass

# Locally, create develop branch
git checkout -b develop
git push -u origin develop

# Set develop as default branch (on GitHub)
# Settings → Branches → Default branch → develop
```

**If using local repos:**
```bash
# Create develop branch
git checkout -b develop
git push -u origin develop

# Configure to prevent direct push to main (local check)
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
protected_branch='main'
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if [ "$current_branch" = "$protected_branch" ]; then
    echo "Direct push to main is not allowed!"
    exit 1
fi
EOF

chmod +x .git/hooks/pre-push
```

**Deliverable**:
- Screenshot of branch protection rules (GitHub) or hook setup (local)
- Both main and develop branches exist remotely

---

## Part 2: Feature Development with Pull Requests (10 points)

### Task 2.1: Create Feature Branch

**As Developer 1 (You):**

```bash
# Ensure you're up-to-date
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/add-calculator

# Create calculator module
cat > calculator.py << 'EOF'
"""
Simple calculator module for demonstration
"""

def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract b from a"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    print("Calculator module loaded")
    print(f"2 + 3 = {add(2, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")
EOF

# Create tests
cat > test_calculator.py << 'EOF'
"""
Tests for calculator module
"""

from calculator import add, subtract, multiply, divide
import pytest

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(10, 5) == 5
    assert subtract(5, 10) == -5

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 100) == 0

def test_divide():
    assert divide(10, 2) == 5
    with pytest.raises(ValueError):
        divide(10, 0)

if __name__ == "__main__":
    print("All tests passed!")
EOF

# Commit changes
git add calculator.py test_calculator.py
git commit -m "feat: add calculator module with tests"

# Push feature branch
git push -u origin feature/add-calculator
```

### Task 2.2: Create Pull Request

**On GitHub:**
1. Go to repository on GitHub
2. Click "Pull requests" → "New pull request"
3. Base: `develop`, Compare: `feature/add-calculator`
4. Fill out PR template:

```markdown
## Description
Add calculator module with basic arithmetic operations.

## Changes
- Created `calculator.py` with add, subtract, multiply, divide functions
- Added comprehensive tests in `test_calculator.py`
- All functions include docstrings
- Error handling for division by zero

## Type of Change
- [x] New feature
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [x] Unit tests added
- [x] All tests pass locally
- [x] Manual testing completed

## Checklist
- [x] Code follows project style guidelines
- [x] Self-review completed
- [x] Comments added for complex logic
- [x] Documentation updated
- [x] No merge conflicts

## Screenshots/Demo
```python
>>> from calculator import add, multiply
>>> add(5, 3)
8
>>> multiply(4, 7)
28
```

## Related Issues
Closes #1 (if you created an issue)
```

5. **Create the pull request**

**If using local repos:**
```bash
# Simulate PR by creating branch and documenting changes
cat > PR-001-add-calculator.md << 'EOF'
# Pull Request #1: Add Calculator Module

**From**: feature/add-calculator
**To**: develop
**Author**: [Your Name]
**Date**: 2025-11-16

## Description
[Same as above]
EOF
```

**Deliverable**:
- Create pull request (screenshot of GitHub PR or PR document)
- Fill out complete PR description
- Request reviewers (if using GitHub, request yourself with another account or ask a friend)

### Task 2.3: Code Review Process

**As Reviewer (You, wearing different hat):**

**Review the code and leave comments:**

1. **Positive feedback:**
   - "Great use of docstrings!"
   - "Excellent error handling for division by zero"
   - "Tests cover edge cases well"

2. **Requested changes:**
   - "Consider adding modulo operation (%)"
   - "Add type hints for better code clarity"
   - "Can you add a function for power/exponentiation?"

**On GitHub:**
- Go to "Files changed" tab
- Click line numbers to add comments
- Submit review as "Request changes"

**Deliverable**:
- Screenshot of code review comments
- At least 3 meaningful comments (1 approval, 2 change requests)

### Task 2.4: Address Review Feedback

**As Developer (You again):**

```bash
# Checkout feature branch
git checkout feature/add-calculator

# Address feedback: Add type hints
cat > calculator.py << 'EOF'
"""
Simple calculator module for demonstration
"""

def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract b from a"""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

def divide(a: float, b: float) -> float:
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def modulo(a: float, b: float) -> float:
    """Return remainder of a divided by b"""
    if b == 0:
        raise ValueError("Cannot modulo by zero")
    return a % b

def power(a: float, b: float) -> float:
    """Return a raised to power b"""
    return a ** b

if __name__ == "__main__":
    print("Calculator module loaded")
    print(f"2 + 3 = {add(2, 3)}")
    print(f"10 % 3 = {modulo(10, 3)}")
    print(f"2 ^ 8 = {power(2, 8)}")
EOF

# Update tests
cat >> test_calculator.py << 'EOF'

def test_modulo():
    assert modulo(10, 3) == 1
    assert modulo(20, 5) == 0
    with pytest.raises(ValueError):
        modulo(10, 0)

def test_power():
    assert power(2, 3) == 8
    assert power(5, 2) == 25
    assert power(10, 0) == 1
EOF

# Commit changes
git add calculator.py test_calculator.py
git commit -m "refactor: add type hints and requested operations

- Added type hints to all functions
- Implemented modulo operation
- Implemented power operation
- Updated tests for new functions"

# Push changes
git push origin feature/add-calculator
```

**On GitHub**: PR automatically updates with new commits

**Leave comment**:
```
@reviewer I've addressed all feedback:
- ✅ Added type hints to all functions
- ✅ Implemented modulo operation with tests
- ✅ Implemented power operation with tests
- ✅ All tests passing locally

Ready for re-review!
```

**Deliverable**:
- Commits addressing feedback
- Comment on PR explaining changes

### Task 2.5: Approve and Merge

**As Reviewer:**
- Review changes
- Approve PR: "Changes look great! LGTM 🚀"
- Click "Approve"

**As Maintainer:**
- Click "Merge pull request"
- Use "Squash and merge" (combines commits)
- Delete feature branch after merge

**Deliverable**:
- Screenshot of approved PR
- Screenshot of merged PR
- Feature branch deleted

---

## Part 3: Handling Conflicts in Collaboration (6 points)

### Task 3.1: Simulate Concurrent Development

**Developer 1 (You) - Feature A:**
```bash
# Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/add-logging

# Add logging
cat > logger.py << 'EOF'
"""
Logging module
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_operation(operation, result):
    logger.info(f"{operation} = {result}")
EOF

# Update calculator to use logging
# ... (add import logger and log calls) ...

git add logger.py
git commit -m "feat: add logging module"
git push -u origin feature/add-logging
```

**Developer 2 (You, different branch) - Feature B:**
```bash
# Create another feature from develop (simulate teammate)
git checkout develop
git checkout -b feature/add-history

# Add history tracking
cat > history.py << 'EOF'
"""
Calculation history module
"""

history = []

def add_to_history(operation, result):
    history.append({"operation": operation, "result": result})

def get_history():
    return history

def clear_history():
    history.clear()
EOF

git add history.py
git commit -m "feat: add history tracking"
git push -u origin feature/add-history
```

### Task 3.2: Merge First Feature

```bash
# Merge feature/add-logging via PR
# Create PR, review, merge to develop
```

### Task 3.3: Update and Resolve Conflicts

**Now feature/add-history is behind develop:**

```bash
# On feature/add-history branch
git checkout feature/add-history

# Try to update from develop
git fetch origin
git merge origin/develop

# If conflicts, resolve them
git add .
git commit -m "Merge develop into feature/add-history"

# Push updated branch
git push origin feature/add-history

# Create PR and merge
```

**Deliverable**:
- Both features successfully merged
- Documentation of conflict resolution (if any)
- Clean develop branch with both features

---

## Part 4: Release Management (4 points)

### Task 4.1: Create Release Branch

```bash
# From develop, create release branch
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# Update version file
echo "1.0.0" > VERSION

# Update README
cat >> README.md << 'EOF'

## Version 1.0.0

### Features
- Calculator module with basic operations
- Logging support
- History tracking

### Release Date
2025-11-16
EOF

git add VERSION README.md
git commit -m "chore: prepare release v1.0.0"
git push -u origin release/v1.0.0
```

### Task 4.2: Merge to Main and Tag

```bash
# Create PR: release/v1.0.0 → main
# After review and approval, merge

# After merge, tag the release
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release version 1.0.0

Features:
- Calculator module
- Logging
- History tracking
"

git push origin v1.0.0

# Also merge back to develop
git checkout develop
git merge main
git push origin develop
```

**On GitHub:**
- Go to "Releases"
- Click "Create a new release"
- Choose tag v1.0.0
- Add release notes
- Publish release

**Deliverable**:
- Tagged release v1.0.0
- Release notes published (GitHub release page screenshot)
- Both main and develop updated

---

## Deliverables

Submit `collaboration-report.md` with:

### Section 1: Pull Requests Summary

```markdown
## Pull Requests Created

### PR #1: Add Calculator Module
- **Branch**: feature/add-calculator → develop
- **Status**: Merged
- **Reviewer Feedback**:
  - Added type hints
  - Added modulo and power operations
- **Commits**: 2
- **Files Changed**: 2 (calculator.py, test_calculator.py)

[Continue for all PRs...]
```

### Section 2: Code Review Examples

Include screenshots or text of:
- Your review comments (as reviewer)
- Responses to feedback (as developer)
- Approval comments

### Section 3: Git Workflow Diagram

```
develop: [A] ← [B (merge PR#1)] ← [C (merge PR#2)] ← [D (merge release)]
          ↓                                              ↓
feature1: [X] ← [Y]                                     main: [D] ← (tag v1.0.0)
          ↓
feature2: [Z]
```

### Section 4: Lessons Learned

Answer (3-5 sentences each):
1. **Why use pull requests instead of direct commits?**
2. **What makes a good code review?**
3. **How do you handle conflicts with teammates' work?**
4. **What's the purpose of release branches?**

---

## Submission Format

```bash
# Create submission
mkdir exercise-05-submission
cp collaboration-report.md exercise-05-submission/

# Include screenshots
mkdir exercise-05-submission/screenshots
# Copy all screenshots

# Include PR descriptions
# ... copy PR markdown files ...

zip -r exercise-05-[yourname].zip exercise-05-submission/
```

---

## Grading Rubric

| Category | Points | Criteria |
|----------|--------|----------|
| **Part 1: Setup** | 5 | Repository configured, branches protected |
| **Part 2: Pull Requests** | 10 | PRs created, reviewed, feedback addressed, merged |
| **Part 3: Conflict Resolution** | 6 | Multiple features, conflicts handled |
| **Part 4: Release Management** | 4 | Release branch, tagged version, published |
| **Total** | **25** | |

**Bonus** (+5):
- Use GitHub Actions for CI/CD (automated tests)
- Multiple collaborators (work with classmate)
- Advanced PR features (draft PRs, suggestions)

---

## Pro Tips

✅ **PR Best Practices**:
- Keep PRs small (< 400 lines changed)
- One feature per PR
- Descriptive titles and descriptions
- Link to related issues

✅ **Code Review Best Practices**:
- Be constructive, not critical
- Explain *why*, not just *what*
- Approve good work enthusiastically
- Request changes politely

✅ **Before Creating PR**:
```bash
git fetch origin
git rebase origin/develop  # Keep history clean
git push --force-with-lease origin feature-branch
```

---

## What You'll Learn

After this exercise:
- ✅ Create professional pull requests
- ✅ Conduct code reviews
- ✅ Collaborate in distributed teams
- ✅ Handle merge conflicts in team settings
- ✅ Manage releases with Git

**This is EXACTLY how professional teams work!** 🎯

---

**Next**: Exercise 6 - Git Disaster Recovery (learn to fix mistakes safely)
