# Module 5: CI/CD Pipelines

**Duration**: 3 weeks (13-16 hours/week)
**Prerequisites**: Modules 1-4 (DevOps, Linux, Python, Docker)
**Deliverable**: Full automated CI/CD pipeline

---

## Overview

CI/CD is where DevOps **becomes real**. No more manual deployments. No more "oops, forgot to run tests." No more Friday afternoon releases that ruin weekends.

**Continuous Integration (CI)**: Automatically test every code change
**Continuous Delivery (CD)**: Code is always deployable
**Continuous Deployment (CD)**: Automatically deploy every passing change

**By the end of this module, you'll**:
- Build complete CI/CD pipelines from scratch
- Automate testing, building, and deployment
- Implement multiple deployment strategies (blue-green, canary, rolling)
- Set up notifications and monitoring
- Never manually deploy again

---

## Learning Objectives

### CI/CD Fundamentals
- [ ] Understand CI vs CD vs CD
- [ ] Pipeline stages (test, build, deploy)
- [ ] Automated testing in pipelines
- [ ] Build artifacts and versioning
- [ ] Deployment strategies
- [ ] Rollback mechanisms

### Pipeline Tools
- [ ] GitHub Actions (primary)
- [ ] GitLab CI (alternative)
- [ ] Jenkins (traditional)
- [ ] Pipeline as code (YAML)

### Production Skills
- [ ] Multi-environment deployments (dev, staging, prod)
- [ ] Secrets management in pipelines
- [ ] Notifications (Slack, email)
- [ ] Pipeline monitoring
- [ ] Security scanning in CI/CD

---

## Module Structure

### Week 1: Continuous Integration

**Lesson 1**: Why CI/CD (1.5 hours)
- Manual deployment nightmares
- How CI/CD prevents disasters
- The deployment pipeline concept
- Real-world transformation stories

**Lesson 2**: CI Fundamentals (2 hours)
- Automated testing philosophy
- Test pyramid (unit, integration, e2e)
- Build automation
- Artifact creation

**Lesson 3**: GitHub Actions Deep Dive (2.5 hours)
- Workflow syntax
- Triggers (push, PR, schedule)
- Jobs and steps
- Matrix builds
- Caching

**Exercise 1**: First CI Pipeline
- Run tests on every commit
- Build Docker image
- Push to registry
- Notify on Slack

**Exercise 2**: Multi-Stage Testing
- Unit tests (fast)
- Integration tests (medium)
- E2E tests (slow)
- Parallel execution

### Week 2: Continuous Delivery/Deployment

**Lesson 4**: CD Fundamentals (2 hours)
- Delivery vs Deployment
- Environments (dev, staging, prod)
- Promotion strategies
- Manual vs automatic deployment

**Lesson 5**: Deployment Strategies (2.5 hours)
- Rolling deployments
- Blue-green deployments
- Canary releases
- Feature flags

**Lesson 6**: Jenkins & GitLab CI (1.5 hours)
- Jenkins pipelines (Jenkinsfile)
- GitLab CI (.gitlab-ci.yml)
- Comparison with GitHub Actions

**Exercise 3**: Multi-Environment Pipeline
- Auto-deploy to dev (on merge)
- Manual approval for staging
- Gradual rollout to production

**Exercise 4**: Blue-Green Deployment
- Two identical environments
- Deploy to inactive (blue or green)
- Switch traffic
- Instant rollback

### Week 3: Production-Grade Pipelines

**Lesson 7**: Security in CI/CD (2 hours)
- Secrets management
- Security scanning (SAST, DAST)
- Dependency scanning
- Container scanning

**Lesson 8**: Monitoring & Observability (1.5 hours)
- Pipeline metrics
- Deployment tracking
- DORA metrics from pipelines
- Failure notifications

**Lesson 9**: Advanced Patterns (2 hours)
- Trunk-based development
- GitFlow with CI/CD
- Monorepo pipelines
- Microservices pipelines

**Exercise 5**: Complete Production Pipeline
- Automated security scanning
- Multi-environment deployment
- Health checks and rollback
- Comprehensive notifications

**Exercise 6**: Pipeline Optimization
- Reduce build time by 50%+
- Implement caching
- Parallel jobs
- Matrix strategy

---

## Assessments

### Quiz (20 points)
- CI/CD concepts
- Pipeline design
- Deployment strategies
- Security best practices

### Project: Full-Stack Application Pipeline (100 points)

**Build end-to-end CI/CD for complete application**:

1. **CI Pipeline** (30 points)
   - Automated testing (unit + integration + e2e)
   - Code quality checks (linting)
   - Security scanning
   - Build Docker images
   - Parallel execution

2. **CD Pipeline** (40 points)
   - Deploy to dev (automatic)
   - Deploy to staging (on tag)
   - Deploy to prod (manual approval)
   - Blue-green strategy
   - Health checks

3. **Monitoring & Notifications** (15 points)
   - Slack notifications
   - Deployment tracking
   - Pipeline metrics dashboard
   - Failure alerts

4. **Documentation** (15 points)
   - Pipeline architecture diagram
   - Runbooks for failures
   - Rollback procedures
   - Onboarding guide

---

## Real-World Pipeline Example

```yaml
name: Production Pipeline

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          npm install
          npm test
          npm run test:integration

  security:
    runs-on: ubuntu-latest
    steps:
      - name: Security scan
        run: |
          npm audit
          docker scan myapp:latest

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Push to registry
        run: docker push myapp:${{ github.sha }}

  deploy-dev:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to dev
        run: |
          kubectl set image deployment/app app=myapp:${{ github.sha }}
          kubectl rollout status deployment/app
```

---

## Deployment Strategies Visualized

### Rolling Deployment
```
V1: [■■■■■] 100%        Load Balancer
    ↓
V2: [□■■■■] 20%        Load Balancer
    ↓
V2: [□□■■■] 40%        Load Balancer
    ↓
V2: [□□□□□] 100%       Load Balancer
```

### Blue-Green Deployment
```
BLUE:  [■■■■■] 100% traffic → Switch → 0% traffic
GREEN: [□□□□□] 0% traffic  → Switch → 100% traffic
```

### Canary Deployment
```
V1: [■■■■■■■■■] 95% traffic
V2: [□] 5% traffic → Monitor → Gradually increase
```

---

## Success Criteria

**You're ready to move on when you can**:
- [ ] Build CI/CD pipelines from scratch
- [ ] Automate testing at all levels
- [ ] Deploy to multiple environments
- [ ] Implement blue-green deployments
- [ ] Set up proper monitoring and alerts
- [ ] Never fear deployments again
- [ ] Pass quiz with 80%+
- [ ] Complete full-stack pipeline project

---

## Time Commitment

| Activity | Time/Week |
|----------|-----------|
| Lessons | 5-6 hours |
| Exercises | 7-9 hours |
| Project | 3-4 hours |
| **Total** | **15-19 hours** |

---

## Tools

- **GitHub Actions** (primary)
- **GitLab CI** (alternative)
- **Jenkins** (traditional)
- **Slack** (notifications)
- **Trivy** (security scanning)

---

## Module Dependencies

**Builds on**:
- Module 2: Git (pipelines triggered by Git events)
- Module 3: Python (pipeline scripts)
- Module 4: Docker (build and deploy containers)

**Prepares for**:
- Module 6: IaC (infrastructure pipelines)
- Module 7: Kubernetes (deploy to K8s)
- Module 9: Monitoring (pipeline metrics)

---

## Career Impact

**CI/CD is the heart of DevOps**:
- Every DevOps role requires pipeline skills
- Separates junior from senior engineers
- Directly impacts deployment frequency (DORA metric)

**After this module**:
- Can build production pipelines
- Understand all deployment strategies
- Ready for senior DevOps roles

---

**Let's automate deployment!** 🚀

Start with `lessons/lesson-01-why-cicd.md`
