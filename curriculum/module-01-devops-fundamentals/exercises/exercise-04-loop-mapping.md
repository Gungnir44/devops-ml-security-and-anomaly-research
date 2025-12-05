# Exercise 1.4: DevOps Loop Mapping

**Objective**: Map a real feature through all eight phases of the DevOps infinity loop

**Time**: 45 minutes

**Skills**: Process understanding, tool identification, automation design

## Background

In Lesson 4, you learned about the eight phases of the DevOps loop:
1. Plan
2. Code
3. Build
4. Test
5. Release
6. Deploy
7. Operate
8. Monitor

This exercise asks you to map a specific feature through this loop, identifying:
- What happens at each phase
- What tools are used
- What can be automated
- Where feedback loops exist

## Scenario: Add "Shopping Cart Abandonment Emails" Feature

**Company**: E-commerce company "ShopNow"

**Feature Request**:
> "When users add items to cart but don't complete checkout within 24 hours, send them an email reminder with a 10% discount code."

**Business goal**: Recover 15% of abandoned carts, increasing revenue by $500k/year

**Acceptance criteria**:
- Email sent exactly 24 hours after cart abandonment
- Email includes items in cart + discount code
- Discount code valid for 48 hours
- User can opt out of emails
- Track: Email open rate, click rate, conversion rate

## Your Tasks

### Task 1: Map Through the Eight Phases (40 points)

For **each phase** of the DevOps loop, describe:
1. **What happens** in this phase for this feature
2. **Who is involved** (role)
3. **Tools used** (specific tools)
4. **Duration** (how long this phase takes)
5. **Deliverable** (output of this phase)

**Format**:

```markdown
# DevOps Loop Mapping: Shopping Cart Abandonment Emails

## Phase 1: PLAN

### What Happens
- Product manager writes user story
- Engineering team estimates effort (3 days dev, 1 day QA)
- Discuss technical approach:
  - Background job to check abandoned carts
  - Email service integration
  - Database schema changes needed
- Create tickets in project management tool
- Prioritize for current sprint

### Who is Involved
- Product Manager (writes requirements)
- Engineering Lead (technical design)
- Developer (estimation)
- QA Engineer (test planning)

### Tools Used
- Jira (issue tracking)
- Confluence (design docs)
- Slack (team communication)

### Duration
- 1 day (planning meeting + documentation)

### Deliverable
- Jira ticket with:
  - User story
  - Acceptance criteria
  - Technical design
  - Estimate

### Automation Opportunities
- Auto-create Jira ticket from product request form
- Template for user stories
- Auto-assign to engineering lead

---

## Phase 2: CODE

### What Happens
[Your description]

### Who is Involved
[Your answer]

### Tools Used
[Your answer]

### Duration
[Your answer]

### Deliverable
[Your answer]

### Automation Opportunities
[Your answer]

---

[Continue for all 8 phases]
```

**Grading** (5 points per phase × 8 phases = 40 points):
- Complete description of activities (1 pt)
- Roles identified (1 pt)
- Tools specified (1 pt)
- Duration estimated (1 pt)
- Automation opportunities identified (1 pt)

**Deliverable**: `task1-loop-mapping.md`

---

### Task 2: Identify Feedback Loops (20 points)

Identify **all feedback loops** in the process.

A feedback loop is where information from a later phase informs an earlier phase.

**Examples**:
```
Feedback Loop 1: Monitor → Plan
- Monitoring shows 40% of emails marked as spam
- Feedback to Product: Revise email content
- Next sprint: Update email template

Feedback Loop 2: Test → Code
- Integration tests fail (email not sent)
- Developer notified immediately
- Developer fixes code, commits again
```

**Your task**: Identify at least 5 feedback loops

**Format**:
```markdown
# Feedback Loops

## Loop 1: [Phase A] → [Phase B]

**What information flows back:**
[Description]

**How it's communicated:**
[Tool/process]

**Speed of feedback:**
[Immediate/Minutes/Hours/Days]

**Example scenario:**
[Concrete example of this loop in action]

---

[Repeat for all loops]
```

**Deliverable**: `task2-feedback-loops.md`

**Grading**:
- 5 feedback loops identified (10 pts)
- Clear explanation of each (5 pts)
- Speed of feedback noted (5 pts)

---

### Task 3: Design Automated Pipeline (25 points)

Design a **CI/CD pipeline** that automates as much as possible.

**Show the pipeline as a flowchart or diagram.**

**Include**:
1. Trigger (what starts the pipeline?)
2. Stages (build, test, deploy, etc.)
3. Gates (what must pass to continue?)
4. Notifications (when are people alerted?)
5. Rollback (how to undo if something breaks?)

**Example format**:
```
Developer commits code to GitHub
    ↓
GitHub webhook triggers CI/CD
    ↓
Stage 1: Build
- Install dependencies (npm install)
- Build Docker image
- Tag image: v1.2.3-abc123
    ↓ (if build fails: notify developer, stop)
    ↓
Stage 2: Unit Tests
- Run Jest tests (5 minutes)
    ↓ (if tests fail: notify developer, stop)
    ↓
Stage 3: Integration Tests
- Spin up test database
- Run API tests (10 minutes)
    ↓ (if tests fail: notify developer, stop)
    ↓
Stage 4: Security Scan
- Scan dependencies (Snyk)
- Check for vulnerabilities
    ↓ (if critical vulnerabilities: notify, stop)
    ↓
Stage 5: Deploy to Staging
- Deploy Docker image to staging environment
- Run smoke tests
- Check: Email service integration works
    ↓ (if smoke tests fail: rollback, notify)
    ↓
Stage 6: Manual QA (optional gate)
- QA engineer tests in staging
- Approves for production
    ↓
Stage 7: Deploy to Production (Canary)
- Deploy to 5% of users
- Monitor metrics for 30 minutes:
  - Error rate
  - Email delivery rate
  - Database connection pool
    ↓ (if metrics degrade: auto-rollback)
    ↓
Stage 8: Full Deployment
- Deploy to 100% of users
- Monitor for 2 hours
- Alert if issues
    ↓
Complete! Monitor phase begins.
```

**Your task**: Design a similar pipeline for this feature.

**Consider**:
- What tests are needed? (unit, integration, E2E)
- What could go wrong? (email service down, database slow)
- How to verify success? (smoke tests, monitoring)
- How fast should it be? (Target: < 30 minutes from commit to production)

**Deliverable**: `task3-pipeline-design.md` (or `.png` if you draw a diagram)

**Grading**:
- Pipeline stages defined (10 pts)
- Failure handling included (5 pts)
- Monitoring/verification included (5 pts)
- Realistic and practical (5 pts)

---

### Task 4: Define Success Metrics (15 points)

Define **how you'll measure success** of this feature in production.

**Include**:

1. **Technical metrics** (from monitoring):
   - Application performance
   - Error rates
   - Infrastructure health

2. **Business metrics**:
   - Feature adoption
   - Revenue impact
   - Customer satisfaction

3. **DORA metrics** (how does this feature affect your DevOps performance?):
   - Did it deploy smoothly? (Change failure rate)
   - How fast did it go from commit to production? (Lead time)

**Format**:
```markdown
# Success Metrics: Shopping Cart Abandonment Emails

## Technical Metrics

### Application Performance
- Metric: Email job execution time
- Target: < 5 seconds per email
- Alert if: > 10 seconds (p95)
- Measured by: Prometheus, Grafana dashboard

### Error Rates
- Metric: Email send failure rate
- Target: < 0.1%
- Alert if: > 1%
- Measured by: Application logs, Sentry

[Add more technical metrics]

## Business Metrics

### Feature Adoption
- Metric: Emails sent per day
- Target: 500 emails/day (based on cart abandonment rate)
- Measured by: Database query, Grafana

### Revenue Impact
- Metric: Revenue from discount codes
- Target: $500k/year ($1,370/day)
- Measured by: Analytics dashboard

[Add more business metrics]

## DORA Metrics

### Lead Time
- This feature: Commit (Day 1) → Production (Day 4)
- Lead time: 4 days
- Assessment: [High/Medium/Low performer], [explain]

### Change Failure Rate
- Did this deployment cause issues? [Yes/No]
- If yes: What broke? How fixed?
- If no: What testing prevented issues?

[Add more DORA metrics]
```

**Deliverable**: `task4-success-metrics.md`

**Grading**:
- Technical metrics defined (5 pts)
- Business metrics defined (5 pts)
- DORA metrics included (5 pts)

---

## Submission

Create a folder: `exercises/module-01/exercise-04/`

Include:
1. `task1-loop-mapping.md`
2. `task2-feedback-loops.md`
3. `task3-pipeline-design.md` (or diagram)
4. `task4-success-metrics.md`

**Commit to your branch and create a pull request when done.**

---

## Grading Rubric

| Task | Points | Description |
|------|--------|-------------|
| **Task 1: Loop Mapping** | 40 | Complete mapping through 8 phases |
| **Task 2: Feedback Loops** | 20 | Identify and explain feedback loops |
| **Task 3: Pipeline Design** | 25 | Practical CI/CD pipeline design |
| **Task 4: Success Metrics** | 15 | Define technical and business metrics |
| **Total** | 100 | |

**Passing**: 80/100

---

## Tips for Success

1. **Be specific**: Don't say "test the code", say "run Jest unit tests (50 tests, 5 minutes)"

2. **Think end-to-end**: Consider database changes, email service integration, monitoring

3. **Consider failures**: What if email service is down? Database is slow?

4. **Use real tools**: GitHub Actions, Jenkins, Docker, Kubernetes, Prometheus, etc.

5. **Time it realistically**: Building Docker image = 5 min, not 5 seconds

---

## Bonus Challenge (Optional, +5 points)

**Create a diagram** of the entire DevOps loop with:
- All 8 phases
- Feedback loops shown as arrows
- Tools labeled
- Time to complete full loop

Use any tool:
- Draw.io
- Lucidchart
- PowerPoint
- Hand-drawn (photo)

**Deliverable**: `bonus-diagram.png`

---

## What You'll Learn

This exercise teaches:
- **How a feature flows through DevOps phases**
- **What tools are used at each phase**
- **How to design a CI/CD pipeline**
- **How to measure success** (technical + business)

These skills apply to:
- Planning new features
- Designing automation
- Setting up monitoring
- Communicating with stakeholders

---

## Real-World Application

When you join a team, you'll need to understand:
- "How do we deploy code?" (Phases 5-7)
- "How do we know if something breaks?" (Phase 8)
- "How long from idea to production?" (All phases)

This exercise gives you the framework to ask the right questions and understand the answers.

---

## Questions?

If stuck, review:
- Lesson 4: The DevOps Infinity Loop

Tag instructor in PR with specific questions!

---

**Good luck! This exercise mirrors real DevOps planning - you'll do this many times in your career.**
