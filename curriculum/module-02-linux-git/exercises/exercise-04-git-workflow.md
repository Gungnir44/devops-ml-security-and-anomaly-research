# Exercise 4: Git Workflow Simulation

**Duration**: 45-60 minutes
**Difficulty**: Intermediate
**Prerequisites**: Lessons 4-5
**Points**: 20

---

## Objectives

By completing this exercise, you will:
- Initialize Git repositories
- Create and manage branches
- Make commits with proper messages
- Merge branches and resolve conflicts
- Use feature branch workflow
- Practice professional Git habits

---

## Scenario

You're building a simple web application. You'll simulate a real development workflow:
- Start with initial project structure
- Add features using feature branches
- Fix bugs using hotfix branches
- Merge changes back to main
- Handle merge conflicts
- Maintain clean Git history

---

## Setup

```bash
# Create project directory
mkdir -p ~/devops-learning/module-02/exercise-04
cd ~/devops-learning/module-02/exercise-04

# Initialize Git repository
git init mywebapp
cd mywebapp

# Configure (if not already done)
git config user.name "Your Name"
git config user.email "your@email.com"

# Verify
git status
```

---

## Part 1: Initial Setup (4 points)

### Task 1.1: Create Initial Project Structure

Create the following files:

```bash
# Create project structure
mkdir -p src tests docs
touch README.md
touch src/app.py src/utils.py
touch tests/test_app.py
touch .gitignore

# Add content to README.md
cat > README.md << 'EOF'
# MyWebApp

A simple web application built with Python.

## Features
- User authentication
- Dashboard
- API endpoints

## Setup
TODO: Add setup instructions
EOF

# Add content to .gitignore
cat > .gitignore << 'EOF'
# Python
*.pyc
__pycache__/
venv/
.env

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
EOF

# Add basic Python code
cat > src/app.py << 'EOF'
"""
MyWebApp - Main application file
"""

def hello():
    return "Hello, World!"

if __name__ == "__main__":
    print(hello())
EOF
```

**Deliverable**:
- Initialize Git repo
- Add all files to staging
- Create initial commit with message: `"chore: initial project structure"`
- Document commands used

### Task 1.2: Create Development Branch

```bash
# Create develop branch from main
git branch develop
git checkout develop

# Or in one command:
git checkout -b develop
```

**Deliverable**:
- Create `develop` branch
- Verify current branch with `git branch`
- Document the workflow

---

## Part 2: Feature Development (8 points)

### Task 2.1: Feature Branch - User Authentication

**Simulate adding user authentication feature:**

```bash
# Create feature branch from develop
git checkout develop
git checkout -b feature/user-auth

# Create auth module
cat > src/auth.py << 'EOF'
"""
User authentication module
"""

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self):
        # TODO: Implement authentication logic
        return True

def login(username, password):
    """Login user"""
    user = User(username, password)
    return user.authenticate()

def logout(user):
    """Logout user"""
    # TODO: Implement logout logic
    pass
EOF

# Update app.py to import auth
cat > src/app.py << 'EOF'
"""
MyWebApp - Main application file
"""

from auth import login, logout

def hello():
    return "Hello, World!"

def main():
    print(hello())
    # Authentication will be implemented here

if __name__ == "__main__":
    main()
EOF
```

**Deliverable**:
- Add and commit files with message: `"feat: add user authentication module"`
- Add another commit updating README
- Push branch to remote (simulate by staying local)
- Show commit history: `git log --oneline`

### Task 2.2: Feature Branch - API Endpoints

```bash
# Create another feature branch from develop
git checkout develop
git checkout -b feature/api-endpoints

# Create API module
cat > src/api.py << 'EOF'
"""
API endpoints module
"""

def get_users():
    """Get all users"""
    return {"users": []}

def get_user(user_id):
    """Get user by ID"""
    return {"id": user_id, "name": "User"}

def create_user(data):
    """Create new user"""
    return {"status": "created", "data": data}
EOF
```

**Deliverable**:
- Commit with message: `"feat: add API endpoints"`
- Show branch structure: `git log --oneline --graph --all`

### Task 2.3: Merge Feature to Develop

```bash
# Merge user-auth feature
git checkout develop
git merge feature/user-auth

# Merge api-endpoints feature
git merge feature/api-endpoints

# Delete merged feature branches
git branch -d feature/user-auth
git branch -d feature/api-endpoints
```

**Deliverable**:
- Successfully merge both features to develop
- Delete feature branches after merge
- Show final branch structure

---

## Part 3: Handling Merge Conflicts (4 points)

### Task 3.1: Create Conflicting Changes

**On main branch:**
```bash
git checkout main

# Update README with one version
cat > README.md << 'EOF'
# MyWebApp

A simple web application.

## Version
1.0.0

## Author
Main Branch Author
EOF

git add README.md
git commit -m "docs: update README with version info"
```

**On develop branch:**
```bash
git checkout develop

# Update README with different version
cat > README.md << 'EOF'
# MyWebApp

A comprehensive web application built with Python.

## Version
2.0.0-dev

## Author
Development Team
EOF

git add README.md
git commit -m "docs: update README with dev info"
```

### Task 3.2: Create and Resolve Conflict

```bash
# Try to merge develop into main
git checkout main
git merge develop

# Conflict! Git will show:
# CONFLICT (content): Merge conflict in README.md
# Automatic merge failed; fix conflicts and then commit the result.

# View conflicted file
cat README.md
# Will show conflict markers:
# <<<<<<< HEAD
# ... main version ...
# =======
# ... develop version ...
# >>>>>>> develop
```

**Resolve the conflict:**
```bash
# Edit README.md manually to combine both versions
cat > README.md << 'EOF'
# MyWebApp

A comprehensive web application built with Python.

## Features
- User authentication (new!)
- API endpoints (new!)
- Dashboard

## Version
2.0.0

## Authors
- Main Branch Author
- Development Team

## Setup
See docs/ for setup instructions
EOF

# Mark conflict as resolved
git add README.md

# Complete the merge
git commit -m "Merge branch 'develop' - resolved README conflicts"
```

**Deliverable**:
- Create merge conflict
- Resolve conflict manually
- Complete merge with proper commit message
- Show final merged state

---

## Part 4: Hotfix Workflow (4 points)

### Task 4.1: Critical Bug Fix

**Simulate critical bug in production:**

```bash
# Create hotfix branch from main
git checkout main
git checkout -b hotfix/security-patch

# Fix security issue
cat > src/auth.py << 'EOF'
"""
User authentication module
"""

import hashlib

class User:
    def __init__(self, username, password):
        self.username = username
        # Security fix: Hash password
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self):
        # TODO: Implement secure authentication
        return True

def login(username, password):
    """Login user with secure password handling"""
    user = User(username, password)
    return user.authenticate()

def logout(user):
    """Logout user"""
    pass
EOF

git add src/auth.py
git commit -m "fix: add password hashing for security"
```

### Task 4.2: Deploy Hotfix

```bash
# Merge to main (production)
git checkout main
git merge hotfix/security-patch

# Also merge to develop (keep in sync)
git checkout develop
git merge hotfix/security-patch

# Delete hotfix branch
git branch -d hotfix/security-patch

# Tag the release
git tag -a v1.0.1 -m "Security patch release"
git tag
```

**Deliverable**:
- Create hotfix branch
- Apply fix and commit
- Merge to both main and develop
- Tag the release
- Show all tags: `git tag`

---

## Deliverables

Submit `git-workflow-report.md` with:

### Section 1: Git Command Log

Document every Git command you used:

```markdown
## Part 1: Initial Setup
### Task 1.1: Create Initial Project Structure

**Commands**:
```bash
git init mywebapp
cd mywebapp
git add .
git commit -m "chore: initial project structure"
```

**Result**: Initial commit created (commit hash: abc123)

**Screenshot/Output**:
```
[main (root-commit) abc123] chore: initial project structure
 5 files changed, 45 insertions(+)
 create mode 100644 README.md
 create mode 100644 .gitignore
 ...
```

[Continue for all tasks...]
```

### Section 2: Branch Structure Diagram

Show final branch and merge structure:

```
main:    [A] ← [B] ← [C] ← [D (merge)] ← [H (hotfix)] ← [I (tag v1.0.1)]
          ↑              /                 /
develop: [A] ← [E] ← [F] ← [G] ← [J (merge hotfix)]
                ↑      ↑
feature/auth:  [X]    |
                      |
feature/api:         [Y]
```

### Section 3: Commit History

```bash
git log --oneline --graph --all > commit-history.txt
```

Include this output showing:
- All commits
- All branches
- All merges
- Tags

### Section 4: Reflection

Answer (3-5 sentences each):

1. **What's the purpose of feature branches?**
2. **Why merge hotfixes to both main and develop?**
3. **How did you resolve the merge conflict?**
4. **What did you learn about Git workflows?**

---

## Submission Format

```bash
# Create submission package
mkdir exercise-04-submission
cd exercise-04-submission

# Copy your repository
cp -r ../mywebapp .

# Create report
cat > git-workflow-report.md << 'EOF'
[Your report here]
EOF

# Include commit history
cd mywebapp
git log --oneline --graph --all > ../commit-history.txt
cd ..

# Zip everything
zip -r exercise-04-[yourname].zip .
```

---

## Grading Rubric

| Category | Points | Criteria |
|----------|--------|----------|
| **Part 1: Initial Setup** | 4 | Proper initialization, good commit message |
| **Part 2: Feature Development** | 8 | Correct branching, multiple commits, clean merges |
| **Part 3: Merge Conflicts** | 4 | Conflict created and resolved correctly |
| **Part 4: Hotfix Workflow** | 4 | Hotfix applied to both branches, tagged |
| **Total** | **20** | |

**Bonus Points** (+3):
- Clean commit history
- Descriptive commit messages (following conventions)
- Use of `git rebase` to keep history clean (advanced)

---

## Expected Commit History

Your final `git log --oneline --graph --all` should look similar to:

```
*   abc789 (tag: v1.0.1, main, develop) fix: add password hashing for security
|\
| * def456 (hotfix/security-patch) fix: add password hashing for security
|/
*   ghi012 Merge branch 'develop' - resolved README conflicts
|\
| * jkl345 docs: update README with dev info
| *   mno678 Merge branch 'feature/api-endpoints' into develop
| |\
| | * pqr901 feat: add API endpoints
| |/
| *   stu234 Merge branch 'feature/user-auth' into develop
| |\
| | * vwx567 feat: add user authentication module
| |/
* | yza890 docs: update README with version info
|/
* bcd123 (develop) chore: initial project structure
```

---

## Common Mistakes

❌ **Committing to main directly**
```bash
# Bad
git checkout main
git add new-feature.py
git commit -m "add feature"  # No! Use feature branch
```

❌ **Forgetting to sync develop with hotfix**
```bash
# Bad: Only merge hotfix to main
git checkout main
git merge hotfix/bug

# Good: Merge to both
git checkout main
git merge hotfix/bug
git checkout develop
git merge hotfix/bug
```

❌ **Poor commit messages**
```bash
# Bad
git commit -m "stuff"
git commit -m "updates"

# Good
git commit -m "feat: add user authentication"
git commit -m "fix: resolve password hashing issue"
```

---

## Pro Tips

✅ **View branch structure anytime**
```bash
git log --oneline --graph --all --decorate
```

✅ **Check what changed**
```bash
git diff main..develop  # Compare branches
```

✅ **Always pull before starting work**
```bash
git checkout main
git pull origin main
git checkout -b feature/new-thing
```

✅ **Use meaningful branch names**
```bash
# Good
feature/user-authentication
bugfix/login-timeout
hotfix/security-patch

# Bad
test
my-branch
stuff
```

---

## What You'll Learn

After this exercise:
- ✅ Confidently use feature branch workflow
- ✅ Handle merge conflicts like a pro
- ✅ Understand when to use hotfix vs feature branches
- ✅ Write professional commit messages
- ✅ Maintain clean Git history

**This is how professional teams work - master it!** 🚀

---

**Next**: Exercise 5 - Collaborative Development (work with remote repositories and pull requests)
