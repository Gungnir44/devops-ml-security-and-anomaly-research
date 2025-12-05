# Lesson 5: Git Workflows - How Teams Actually Use Git

**Duration**: 2 hours
**Objectives**: Master branching, merging, and team collaboration workflows

---

## The Solo Developer vs. Team Reality

**When you work alone**:
```bash
git add .
git commit -m "stuff"
git push
# Works fine! (but not professional)
```

**When you work on a team**:
```
You: *pushes directly to main*
Team Lead: "STOP! We use pull requests!"
You: "What's a pull request?"
Team Lead: "How did you get hired?"
You: 😅
```

**Reality**: Professional teams have workflows to prevent chaos.

---

## Why Workflows Matter

**Without a workflow** (chaos):
```
Developer 1: Pushes broken code to main
Developer 2: Pulls, now their code breaks
Developer 3: Tries to deploy, production crashes
Boss: "WHO PUSHED TO MAIN?!"
Everyone: 🔥🔥🔥
```

**With a workflow** (order):
```
Developer 1: Creates feature branch, makes changes
Developer 2: Reviews code in pull request
Developer 3: Approves and merges to main
Automated tests: ✓ All passing
Production: ✓ Deploys successfully
Boss: 😊
```

**Workflows provide**:
- **Safety**: Code review before merging
- **Quality**: Automated tests on every change
- **History**: Clear record of what changed and why
- **Collaboration**: Multiple people working without conflicts
- **Rollback**: Easy to undo bad changes

---

## Git Branching Basics

### What is a Branch?

A branch is a **pointer to a commit**. That's it!

```
main branch
    ↓
[C1] ← [C2] ← [C3]
```

When you create a new branch:
```
main branch
    ↓
[C1] ← [C2] ← [C3]
              ↑
         feature branch
```

When you commit to feature branch:
```
              main
               ↓
[C1] ← [C2] ← [C3]
               ↑
              [C4] ← [C5]
                      ↑
                   feature
```

**Key concept**: Branches are cheap! Creating a branch doesn't copy files, it just creates a new pointer.

### Creating Branches

```bash
# Create new branch
git branch feature-login

# Switch to branch
git checkout feature-login

# Create and switch (one command)
git checkout -b feature-login

# View all branches
git branch

# View with last commit
git branch -v

# Delete branch
git branch -d feature-login
```

### Working with Branches

```bash
# On main branch
git checkout main
git pull origin main

# Create feature branch from main
git checkout -b feature/user-authentication

# Make changes
echo "def login(user, password):" > auth.py
git add auth.py
git commit -m "feat: add login function"

# More changes
echo "def logout(user):" >> auth.py
git add auth.py
git commit -m "feat: add logout function"

# Push branch to remote
git push -u origin feature/user-authentication
```

### Branch Naming Conventions

**Good names** (descriptive, organized):
```
feature/user-login
feature/payment-processing
bugfix/null-pointer-error
hotfix/security-vulnerability
chore/update-dependencies
docs/api-documentation
```

**Bad names** (vague, confusing):
```
test
new-stuff
fix
branch1
temp
joshua-branch
```

---

## Merging Strategies

### Fast-Forward Merge

**When**: Your branch has no conflicts with main (main hasn't changed)

```
Before:
main: [C1] ← [C2]
                ↑
              [C3] ← [C4]
                      ↑
                   feature

After merge:
main: [C1] ← [C2] ← [C3] ← [C4]
                            ↑
                         feature (deleted)
```

**Command**:
```bash
git checkout main
git merge feature-login
# Fast-forward merge! Just moves pointer
```

**Result**: Clean linear history

### Three-Way Merge

**When**: Main has new commits since you branched

```
Before:
              [C3] ← [C4]
             /      feature
[C1] ← [C2]
             \
              [C5] ← [C6]
                      main

After merge:
              [C3] ← [C4]
             /            \
[C1] ← [C2]                [C7] (merge commit)
             \            /      ↑
              [C5] ← [C6]      main
```

**Command**:
```bash
git checkout main
git merge feature-login
# Creates merge commit
```

**Result**: Preserves both histories, creates merge commit

### Merge Conflicts

**When they happen**: Same lines modified in both branches

**Example**:
```
On main:          On feature:
app.py:           app.py:
PORT=8080         PORT=3000
```

**When you merge**:
```bash
git merge feature-port-change
# CONFLICT (content): Merge conflict in app.py
# Automatic merge failed; fix conflicts and then commit
```

**Git adds conflict markers**:
```python
<<<<<<< HEAD
PORT=8080
=======
PORT=3000
>>>>>>> feature-port-change
```

**How to resolve**:

1. **Open conflicted file**:
```bash
cat app.py
```

2. **Decide what to keep**:
```python
# Option 1: Keep main version
PORT=8080

# Option 2: Keep feature version
PORT=3000

# Option 3: Use both/combine
PORT=8080  # Production
TEST_PORT=3000  # Testing
```

3. **Remove conflict markers**:
```python
# Final decision
PORT=3000
```

4. **Mark as resolved and commit**:
```bash
git add app.py
git commit -m "fix: resolve port conflict, use 3000"
```

### Common Merge Conflict Patterns

**Pattern 1: Different features in same file**
```bash
# Developer 1: Added login()
# Developer 2: Added logout()
# Both modified auth.py

# Solution: Keep both changes
def login(user, password):
    pass

def logout(user):
    pass
```

**Pattern 2: Configuration changes**
```bash
# Developer 1: Changed database host
# Developer 2: Changed database port

# Solution: Discuss with team, decide on values
DATABASE_HOST="prod.db.com"  # Keep from Developer 1
DATABASE_PORT=5433           # Keep from Developer 2
```

---

## Popular Workflows

### 1. Feature Branch Workflow (Most Common)

**How it works**:
```
1. main branch is always deployable
2. Create feature branch for each new feature
3. Work on feature branch
4. Create pull request
5. Code review + tests
6. Merge to main
7. Delete feature branch
```

**Example**:
```bash
# 1. Start from updated main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/add-search

# 3. Work on feature
# ... make changes ...
git add .
git commit -m "feat: add search functionality"

# 4. Push to remote
git push -u origin feature/add-search

# 5. Create Pull Request (on GitHub/GitLab)
# ... go to GitHub, click "New Pull Request" ...

# 6. After approval, merge (on GitHub)
# ... click "Merge Pull Request" ...

# 7. Clean up locally
git checkout main
git pull origin main
git branch -d feature/add-search
```

**Pros**:
- Simple to understand
- Works for small/medium teams
- Clear feature isolation

**Cons**:
- Can have many long-lived branches
- Merge conflicts if branches live too long

---

### 2. GitFlow (Complex Projects)

**Branches**:
- `main` - Production code (always deployable)
- `develop` - Integration branch (latest development)
- `feature/*` - New features (from develop)
- `release/*` - Release preparation (from develop)
- `hotfix/*` - Emergency fixes (from main)

**Workflow**:
```
feature branches → develop → release branches → main
                                    ↑
                             hotfix branches
```

**Example**:
```bash
# Start new feature
git checkout develop
git checkout -b feature/payment-gateway

# Work on feature
git commit -m "feat: add payment integration"
git commit -m "feat: add payment validation"

# Merge to develop
git checkout develop
git merge feature/payment-gateway

# Create release branch
git checkout -b release/v1.2.0

# Bug fixes in release
git commit -m "fix: payment validation error"

# Merge to main (production)
git checkout main
git merge release/v1.2.0
git tag v1.2.0

# Also merge back to develop
git checkout develop
git merge release/v1.2.0
```

**Pros**:
- Clear separation of production/development
- Supports multiple versions
- Good for scheduled releases

**Cons**:
- Complex (overkill for small projects)
- Many branches to manage

---

### 3. Trunk-Based Development (Fast-Paced Teams)

**How it works**:
- One main branch (`main` or `trunk`)
- Short-lived feature branches (1-2 days max)
- Frequent merges (multiple times per day)
- Feature flags for incomplete features

**Example**:
```bash
# Morning: Create feature branch
git checkout -b feature/quick-fix

# 2 hours later: Complete and merge
git commit -m "feat: add caching layer"
git push origin feature/quick-fix
# Immediate PR + merge

# Afternoon: Another feature
git checkout main
git pull origin main
git checkout -b feature/optimize-query
# ... same pattern ...
```

**With feature flags**:
```python
# Feature not ready but code merged
if feature_flag('new_search_enabled'):
    use_new_search()
else:
    use_old_search()
```

**Pros**:
- Fast integration
- Fewer merge conflicts
- Continuous delivery ready

**Cons**:
- Requires discipline
- Needs automated testing
- Feature flags add complexity

---

## Pull Requests (PRs)

### What is a Pull Request?

**Not a Git feature** - it's a GitHub/GitLab/Bitbucket feature!

**Pull Request = "Hey team, review my code before merging"**

```
Developer: "I wrote feature X, please review"
              ↓
         Pull Request
              ↓
Team reviews code, suggests changes
              ↓
Developer makes changes
              ↓
Team approves
              ↓
Code merged to main
```

### Creating a Pull Request

**1. Push your branch**:
```bash
git push -u origin feature/user-login
```

**2. Go to GitHub/GitLab**:
- Navigate to repository
- Click "Pull Requests" or "Merge Requests"
- Click "New Pull Request"

**3. Fill out PR template**:
```markdown
## Summary
Add user login functionality with JWT authentication

## Changes
- Created login endpoint (/api/login)
- Added JWT token generation
- Implemented token validation middleware
- Added login tests

## Testing
- [ ] Manual testing completed
- [x] Unit tests passing
- [x] Integration tests passing

## Screenshots
[If UI changes, add screenshots]

## Related Issues
Closes #123
```

**4. Request reviewers**:
- Select team members to review
- Assign to yourself
- Add labels (feature, high-priority, etc.)

### Code Review Process

**As a reviewer**:
```bash
# Check out PR locally
git fetch origin
git checkout feature/user-login

# Test the code
python -m pytest
python manage.py runserver

# Review on GitHub
# - Read code changes
# - Leave comments
# - Request changes or approve
```

**Good review comments**:
```
✓ "Consider adding error handling for network timeouts"
✓ "This function is getting large, maybe extract the validation logic?"
✓ "Great use of caching here!"
✓ "Can you add a test for the edge case where user is None?"
```

**Bad review comments**:
```
✗ "This is bad"
✗ "I don't like this"
✗ "Rewrite everything"
✗ "Why did you do it this way?" (without suggestion)
```

### Addressing Review Feedback

```bash
# Make requested changes
git add .
git commit -m "refactor: extract validation logic to separate function"

# Push to same branch
git push origin feature/user-login

# PR automatically updates!
```

---

## Remote Repositories

### Understanding Remotes

**Remote** = Copy of your repository on another server (GitHub, GitLab, etc.)

```bash
# View remotes
git remote -v

# Typical output:
# origin  https://github.com/user/repo.git (fetch)
# origin  https://github.com/user/repo.git (push)
```

### Common Remote Commands

**Fetch** (download changes, don't merge):
```bash
git fetch origin

# See what's new
git log origin/main

# Compare with local
git diff main origin/main
```

**Pull** (fetch + merge):
```bash
git pull origin main
# = git fetch origin + git merge origin/main
```

**Push** (upload commits):
```bash
git push origin main

# First push of new branch
git push -u origin feature-x
# -u sets upstream (tracking)
```

### Keeping Your Branch Updated

**Problem**: Main branch moves while you work on feature

```
Your feature branch:
[C1] ← [C2] ← [C3] ← [C4]
                      ↑
                  your work

Main branch (remote):
[C1] ← [C2] ← [C5] ← [C6] ← [C7]
                              ↑
                         other's work
```

**Solution 1: Merge main into your branch**:
```bash
git checkout feature-x
git pull origin main

# Resolve any conflicts
git push origin feature-x
```

**Solution 2: Rebase (covered in next lesson)**:
```bash
git checkout feature-x
git rebase main
```

---

## Real DevOps Workflow Example

### Scenario: Add Monitoring to Production App

**Week starts**:
```bash
# Monday morning: Get latest code
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/add-prometheus-monitoring

# See the plan
cat TODO.md
# 1. Install Prometheus client library
# 2. Add metrics endpoints
# 3. Configure Prometheus scraping
# 4. Add Grafana dashboard
# 5. Update documentation
```

**Day 1-2: Basic implementation**:
```bash
# Install library
pip install prometheus-client
echo "prometheus-client==0.19.0" >> requirements.txt

# Create metrics file
cat > metrics.py << 'EOF'
from prometheus_client import Counter, Histogram

http_requests = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
EOF

# Commit
git add .
git commit -m "feat: add Prometheus client library and basic metrics"

# Push to remote
git push -u origin feature/add-prometheus-monitoring
```

**Day 2-3: Integration**:
```bash
# Add metrics to app
vim app.py  # Add metrics collection

git add app.py
git commit -m "feat: integrate Prometheus metrics in application"

# Add endpoint
vim app.py  # Add /metrics endpoint

git add app.py
git commit -m "feat: add /metrics endpoint for Prometheus scraping"

git push origin feature/add-prometheus-monitoring
```

**Day 3-4: Configuration and testing**:
```bash
# Create Prometheus config
cat > prometheus.yml << 'EOF'
scrape_configs:
  - job_name: 'myapp'
    static_configs:
      - targets: ['localhost:5000']
EOF

git add prometheus.yml
git commit -m "feat: add Prometheus configuration"

# Add tests
vim tests/test_metrics.py

git add tests/
git commit -m "test: add metrics endpoint tests"

# Run tests
pytest
# ✓ All tests passing

git push origin feature/add-prometheus-monitoring
```

**Day 4: Documentation and PR**:
```bash
# Update docs
vim README.md  # Add monitoring section
vim docs/MONITORING.md  # Create monitoring guide

git add README.md docs/
git commit -m "docs: add monitoring setup guide"

git push origin feature/add-prometheus-monitoring
```

**Create Pull Request on GitHub**:
```markdown
## Summary
Add Prometheus monitoring to track application metrics

## Changes
- Add Prometheus client library
- Implement request counter and duration histogram
- Create /metrics endpoint
- Add Prometheus configuration
- Add tests for metrics
- Update documentation

## Testing
- [x] Unit tests passing (pytest)
- [x] Integration tests passing
- [x] Manually tested with Prometheus
- [x] Verified metrics in Grafana

## Deployment Notes
- Requires prometheus.yml in production
- /metrics endpoint publicly accessible (no auth needed)
- Compatible with existing monitoring stack

## Screenshots
![Grafana Dashboard](screenshot.png)

Closes #456
```

**Day 5: Code review**:
```
Reviewer 1: "Looks good! Just one suggestion - add authentication to /metrics"
Reviewer 2: "Consider adding more metrics (error rates, response codes)"
```

**Address feedback**:
```bash
# Add auth to metrics endpoint
vim app.py

git add app.py
git commit -m "security: add basic auth to /metrics endpoint"

# Add more metrics
vim metrics.py

git add metrics.py
git commit -m "feat: add error rate and response code metrics"

git push origin feature/add-prometheus-monitoring
```

**Approval and merge**:
```
✓ Reviewer 1: Approved
✓ Reviewer 2: Approved
✓ CI/CD: All checks passed
```

**Merge on GitHub** → Delete branch

**Locally**:
```bash
# Switch to main
git checkout main

# Pull merged changes
git pull origin main

# Delete local branch
git branch -d feature/add-prometheus-monitoring

# Verify it's there
git log --oneline | head -5
# abcd123 feat: add error rate and response code metrics
# def4567 security: add basic auth to /metrics endpoint
# ...
```

---

## Best Practices

### ✅ Do

1. **Pull before you push**:
```bash
git pull origin main  # Get latest changes first
git push origin main  # Then push your changes
```

2. **Keep branches short-lived**:
- Feature branches: 1-3 days max
- Merge frequently
- Reduces merge conflicts

3. **Write descriptive PR descriptions**:
```markdown
## What
Add user authentication

## Why
Users need to log in to access personalized content

## How
- JWT tokens
- Bcrypt password hashing
- Session management
```

4. **Review your own code before PR**:
```bash
git diff main..feature-x  # Review all changes
# Remove debug code, fix typos, etc.
```

5. **One feature per branch**:
```bash
# Good
feature/add-login
feature/add-logout
feature/add-password-reset

# Bad
feature/authentication-everything  # Too broad!
```

6. **Meaningful commit messages on feature branch**:
```bash
# Even though squashed on merge, good for review
git commit -m "feat: add login endpoint"
git commit -m "feat: add JWT token generation"
git commit -m "test: add login integration tests"
```

### ❌ Don't

1. **Don't push to main directly**:
```bash
# BAD
git checkout main
git commit -m "quick fix"
git push origin main  # 😱

# GOOD
git checkout -b hotfix/critical-bug
git commit -m "fix: resolve critical security bug"
git push origin hotfix/critical-bug
# Create PR, even for hotfixes
```

2. **Don't merge without review**:
```bash
# BAD (on GitHub)
# *Creates PR*
# *Immediately clicks "Merge"*

# GOOD
# *Creates PR*
# *Waits for review*
# *Addresses feedback*
# *Waits for approval*
# *Then merges*
```

3. **Don't leave branches unmerged**:
```bash
git branch
# feature/from-6-months-ago  # 😱 Delete it!
# feature/abandoned          # 😱 Delete it!
# feature/not-sure-what      # 😱 Delete it!
```

4. **Don't force push to shared branches**:
```bash
# BAD (if others are using this branch)
git push --force origin feature-x  # 😱 Can lose others' work

# OK (if it's only your branch)
git push --force origin feature-x  # ⚠️  Use with caution
```

---

## Troubleshooting Common Issues

### "Your branch is behind origin/main"

```bash
git pull origin main
# Resolve any conflicts
git push origin feature-x
```

### "Your branch has diverged from origin/feature-x"

**Cause**: Someone else pushed to your branch

**Fix**:
```bash
git pull origin feature-x  # Pull their changes
# Resolve conflicts
git push origin feature-x
```

### "Can't push because of conflicts"

```bash
# Pull first
git pull origin main

# Resolve conflicts
# ... edit files, remove conflict markers ...

git add .
git commit -m "fix: resolve merge conflicts"

git push origin feature-x
```

### "Accidentally committed to main"

```bash
# If not pushed yet
git checkout -b feature/new-branch  # Create branch with commits
git checkout main                   # Go back to main
git reset --hard origin/main        # Reset main to remote

# If already pushed (uh oh)
# Contact team lead immediately
```

---

## Summary

**You now know**:
- Why workflows prevent chaos
- How branches work (cheap pointers)
- Merging strategies (fast-forward vs three-way)
- Resolving merge conflicts
- Popular workflows (Feature Branch, GitFlow, Trunk-Based)
- Pull request process
- Remote repository operations
- Real DevOps workflow examples

**Key Takeaway**: Professional teams use workflows to enable collaboration without chaos.

**Next**: Lesson 6 - Advanced Git (rebasing, stashing, cherry-picking, recovering from disasters)

**Practice**: Create a feature branch, make changes, create a PR!

---

## Quick Reference

```bash
# Branching
git branch feature-x              # Create branch
git checkout feature-x            # Switch branch
git checkout -b feature-x         # Create and switch
git branch -d feature-x           # Delete branch

# Merging
git checkout main                 # Switch to target
git merge feature-x               # Merge feature-x into main

# Remote
git fetch origin                  # Download changes
git pull origin main              # Fetch + merge
git push origin main              # Upload commits
git push -u origin feature-x      # Push new branch

# Collaboration
git checkout main
git pull origin main
git checkout -b feature/new-feature
# ... make changes ...
git push -u origin feature/new-feature
# Create PR on GitHub
# Get review, merge
git checkout main
git pull origin main
git branch -d feature/new-feature
```

**Master these workflows - they're what separates hobbyists from professionals!** 🚀
