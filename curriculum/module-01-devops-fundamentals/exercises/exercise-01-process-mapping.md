# Exercise 1.1: Process Mapping

**Objective**: Map a software delivery process to identify bottlenecks and waste

**Time**: 60 minutes

**Skills**: Analysis, critical thinking, process understanding

## Background

Before you can improve a process, you need to **understand** it. This exercise teaches you how to map a software delivery workflow and identify improvement opportunities.

## Scenario: "QuickShop" E-Commerce Company

You're a new DevOps engineer at QuickShop. Your manager says:

> "We need to speed up feature delivery. Map our current process and find bottlenecks."

## Current Process (As Described by Teams)

### Developer's View:
```
1. Product manager emails feature request
2. I write code (2-3 days)
3. I create pull request
4. Wait for code review (1-2 days)
5. After approval, I merge to develop branch
6. QA team picks it up "when they can"
7. I wait... (unknown duration)
8. QA files bugs
9. I fix bugs
10. Eventually it goes to production (quarterly release)
```

### QA's View:
```
1. Check email for "ready for QA" notification
2. Pull latest code
3. Set up test environment (4 hours - if not broken)
4. Manual testing (2 days per feature)
5. Document bugs in Jira
6. Wait for fixes
7. Re-test
8. Approve for production
```

### Operations' View:
```
1. Receive deployment request 1 week before release
2. Review 50-page runbook
3. Schedule maintenance window (Friday 6 PM)
4. Backup production database (1 hour)
5. Deploy manually:
   - SSH into 10 servers
   - Copy files
   - Restart services
   - Check logs
   - Pray nothing broke
6. If it breaks, rollback (another 2 hours)
7. Go home at midnight
```

## Your Task

### Part 1: Create a Process Map

Draw (or describe in text) the **complete** process from "idea" to "production".

**Include**:
- Each step
- Who's responsible
- How long each step takes
- What happens if something goes wrong

**Format** (you can draw or use text):
```
[Product] --email--> [Developer] --PR--> [Code Review] --merge--> ...
   |                     |                    |
   1 day             2-3 days             1-2 days
```

**Deliverable**: `process-map.md` or `process-map.png`

### Part 2: Identify Wait Times

Calculate **lead time** (idea to production) and **process time** (actual work time).

**Formula**:
```
Lead Time = Total time from start to finish
Process Time = Sum of time actually working (not waiting)
Wait Time = Lead Time - Process Time
```

**Example Calculation**:
```
Developer codes: 3 days (process time)
Wait for code review: 2 days (wait time)
Code review: 1 day (process time)
Wait for QA: 5 days (wait time)
QA testing: 2 days (process time)
Wait for deployment window: 30 days (wait time)
Deployment: 0.25 days (process time)

Lead Time = 43.25 days
Process Time = 6.25 days
Wait Time = 37 days (86% of total time!)
```

**Your Turn**: Calculate for QuickShop process above.

**Deliverable**: `time-analysis.md` with calculations

### Part 3: Identify Bottlenecks

A **bottleneck** is the slowest part of the process that limits throughput.

**Common Bottlenecks**:
- Manual steps (deployment, testing)
- Resource constraints (only 2 QA engineers)
- Waiting for approval (change control board)
- Handoffs (passing work between teams)

**Identify**:
1. What's the biggest bottleneck in QuickShop's process?
2. What's the second biggest?
3. What's causing wait time?

**Deliverable**: `bottlenecks.md` with analysis

### Part 4: Propose Improvements

For **each bottleneck**, propose a DevOps solution.

**Example**:
```
Bottleneck: Manual testing takes 2 days

Root Cause:
- No automated tests
- QA waits for "stable" build
- Each bug requires full re-test

DevOps Solution:
- Automated unit tests (run in 5 minutes)
- Automated integration tests (run in 30 minutes)
- CI/CD: Tests run on every commit
- QA focuses on exploratory testing, not repetitive clicking

Expected Impact:
- Testing time: 2 days → 1 hour (automated) + 4 hours (exploratory)
- Faster feedback (minutes, not days)
- Higher quality (tests don't get tired/bored)

Investment Required:
- Write initial tests: 2 weeks
- CI/CD setup: 1 week
- Training: 1 week
```

**Your Turn**: Propose improvements for all bottlenecks.

**Deliverable**: `improvements.md` with detailed proposals

## Submission

Create a folder: `exercises/module-01/exercise-01/`

Include:
1. `process-map.md` (or image)
2. `time-analysis.md`
3. `bottlenecks.md`
4. `improvements.md`
5. `reflection.md` (see below)

### Reflection Questions

Answer in `reflection.md`:

1. **Insight**: What surprised you most about the process?

2. **Waste**: What percentage of time is "wait time" vs "work time"?

3. **Culture**: What cultural issues did you notice? (Blame? Silos? Communication?)

4. **Quick Win**: If you could only fix ONE thing, what would it be and why?

5. **Metrics**: How would you measure success of your improvements?

## Grading Rubric

| Criterion | Points | Description |
|-----------|--------|-------------|
| **Process Map** | 20 | Complete, clear, shows all steps |
| **Time Analysis** | 20 | Accurate calculations, identified wait vs process time |
| **Bottleneck ID** | 20 | Correctly identified limiting factors |
| **Improvements** | 30 | Practical, specific, addresses root causes |
| **Reflection** | 10 | Thoughtful insights, clear reasoning |
| **Total** | 100 | |

**Passing**: 80/100

## Example (Partial) for Inspiration

Don't copy this! But here's what good analysis looks like:

```markdown
# Process Map

Idea → Product Manager (1 day) → Developer (3 days, actual coding) →
Code Review Wait (2 days) → Code Review (1 day) → QA Wait (5 days) →
QA Testing (2 days) → Production Wait (30 days) → Deployment (6 hours)

# Time Analysis

Lead Time: 44.25 days
Process Time: 6.25 days (14%)
Wait Time: 38 days (86%)

Insight: Most time is WAITING, not working!

# Biggest Bottleneck

Bottleneck #1: Quarterly release cycle (30 days wait)

Why it's a bottleneck:
- Features sit completed, waiting for release window
- Low deployment frequency = high risk (many changes at once)
- Fear of deployment drives conservative release schedule

DevOps Solution:
- Automate deployment pipeline
- Enable daily deployments (low risk per deployment)
- Use feature flags for gradual rollout
- Blue-green deployment for instant rollback

Impact:
- Lead time: 44 days → 7 days
- Deployment risk: High → Low
- Deployment stress: High → Low
```

## Tips for Success

1. **Be specific**: "Improve deployment" is vague. "Automate deployment with Jenkins pipeline" is specific.

2. **Quantify**: Use numbers (days, hours, costs)

3. **Think root causes**: Don't just treat symptoms
   - Symptom: "Deployments fail"
   - Root cause: "No automated testing" or "Manual configuration drift"

4. **Be realistic**: Don't propose "rewrite everything in Kubernetes" for Week 1

5. **Consider people**: Technical solutions need cultural change too

## What You'll Learn

This exercise teaches:
- Process mapping (valuable skill for any improvement initiative)
- Bottleneck identification (Theory of Constraints)
- Root cause analysis (5 Whys technique)
- DevOps solutions (not just "automate everything")
- Cost/benefit thinking

These skills apply beyond DevOps:
- Business process optimization
- Project management
- Problem-solving

## Next Steps

After completing this exercise:
1. Push to GitHub
2. Create pull request
3. Tag instructor for review
4. Move to Exercise 1.2

## Questions?

If stuck:
- Re-read Lesson 1 and 2
- Think: "Where is time wasted?"
- Ask: "Why does this step exist?"
- Consider: "What if we automated this?"

Tag instructor in PR with specific questions!

---

**Good luck! This is where DevOps starts - understanding the current state before improving it.**
