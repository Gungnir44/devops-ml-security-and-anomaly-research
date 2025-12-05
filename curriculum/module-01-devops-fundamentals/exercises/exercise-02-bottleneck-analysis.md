# Exercise 1.2: Bottleneck Analysis & ROI Calculation

**Objective**: Identify bottlenecks in a software delivery process and calculate the ROI of DevOps improvements

**Time**: 90 minutes

**Skills**: Analysis, cost calculation, business case development

## Background

In Lesson 2, you learned how to calculate the business case for DevOps. Now you'll apply those concepts to a real scenario.

This exercise teaches you:
- How to identify bottlenecks in a process
- How to calculate the cost of inefficiency
- How to project ROI of improvements
- How to present findings to management

## Scenario: "HealthTech Solutions"

**Company**: HealthTech Solutions - Healthcare software company
**Product**: Electronic Health Records (EHR) system
**Revenue**: $20M annually
**Engineering team**: 30 people (20 developers, 5 QA, 5 operations)
**Customers**: 500 hospitals

### Current State

**Deployment Process**:
```
1. Development (10 developers working on features)
   - Average feature development time: 5 days
   - Features per developer per month: 4

2. Code Review
   - Wait time for reviewer: 2 days
   - Review time: 1 day

3. QA Testing (5 QA engineers)
   - Wait for QA availability: 3 days
   - Manual testing per feature: 2 days
   - Bug discovery rate: 40% of features have bugs

4. Bug Fixing (if needed)
   - Developer fixes bugs: 1 day
   - Re-test: 1 day

5. Staging Deployment
   - Operations schedules staging deployment: Weekly (Friday)
   - Average wait for deployment window: 3 days

6. QA Approval
   - Final testing in staging: 2 days
   - Approval process: 1 day

7. Production Deployment
   - Frequency: Monthly (first Monday of month)
   - Average wait for deployment window: 15 days
   - Deployment process: Manual, 4 hours, 5 people
   - Success rate: 60% (40% require rollback)
   - Rollback time: 4 hours, 5 people

8. Post-deployment
   - Monitoring: Manual checking for 8 hours
   - Hot fixes (if issues found): 30% of deployments
   - Hot fix deployment: 4 hours, 5 people
```

**Costs**:
- Developer: $100/hour ($208k/year)
- QA Engineer: $80/hour ($166k/year)
- Operations Engineer: $100/hour ($208k/year)

**Production Incidents**:
- Frequency: 8 per month
- Average duration: 4 hours
- People involved: 3 engineers
- Downtime cost: $5,000 per hour (lost revenue + reputation)

**Customer Impact**:
- Customer complaints about slow feature delivery: 50 per quarter
- Lost deals due to missing features: 3 per year ($200k each)

## Your Tasks

### Part 1: Process Analysis (20 points)

**Task**: Create a detailed process map showing the flow from "feature idea" to "production".

**Include**:
1. Each step in the process
2. Wait time vs. process time for each step
3. Who's responsible for each step
4. Dependencies between steps

**Format** (text or diagram):
```
[Product] --request--> [Dev] --code--> [Review] --approve--> [QA] ...
   |                     |               |
   1 day              5 days          2 days wait
                                     1 day review
```

**Deliverable**: `part1-process-map.md`

**Grading criteria**:
- Complete process mapped (5 pts)
- Wait time vs process time identified (5 pts)
- Dependencies identified (5 pts)
- Clear and well-organized (5 pts)

---

### Part 2: Calculate Lead Time and Identify Waste (20 points)

**Task**: Calculate the total lead time from "feature start" to "production deployment".

**Calculate**:
1. **Total lead time** (start to finish)
2. **Process time** (actual work time)
3. **Wait time** (time spent waiting)
4. **% of time spent waiting** vs working

**Assume**: Best case scenario (no bugs, no rollback, no hotfixes)

**Show your work**:
```
Development: 5 days (process time)
Wait for code review: 2 days (wait time)
Code review: 1 day (process time)
...

Total Lead Time: X days
Total Process Time: Y days
Total Wait Time: Z days
Percentage waiting: Z/X * 100 = ?%
```

**Deliverable**: `part2-lead-time-calculation.md`

**Grading criteria**:
- Correct lead time calculation (5 pts)
- Process time vs wait time separated (5 pts)
- Percentage calculated correctly (5 pts)
- Analysis of where time is wasted (5 pts)

---

### Part 3: Identify and Prioritize Bottlenecks (20 points)

**Task**: Identify the top 3 bottlenecks that are limiting throughput.

**For each bottleneck, document**:
1. What is the bottleneck?
2. Why is it a bottleneck? (root cause)
3. What is the impact? (time, cost, quality)
4. How could DevOps practices address it?

**Example**:
```
Bottleneck #1: Monthly deployment window

Root Cause:
- Manual deployment process (error-prone, requires coordination)
- Fear of breaking production
- Limited operations team capacity

Impact:
- Features wait average 15 days for deployment
- Large batches (30+ features deployed at once)
- High failure rate due to large batches

DevOps Solution:
- Automate deployment pipeline
- Continuous deployment (deploy daily or more)
- Automated testing to reduce risk
- Blue-green deployment for easy rollback
```

**Deliverable**: `part3-bottleneck-analysis.md`

**Grading criteria**:
- Three bottlenecks identified correctly (6 pts)
- Root causes identified (6 pts)
- Impact quantified (4 pts)
- DevOps solutions proposed (4 pts)

---

### Part 4: Calculate Current Costs (20 points)

**Task**: Calculate the annual cost of the current process.

**Calculate costs for**:

1. **Deployment labor costs** (monthly deployments):
   - Regular deployments (success)
   - Failed deployments (rollback)
   - Hot fixes

2. **Waiting time costs**:
   - Developers waiting for code review
   - Developers waiting for QA
   - Features waiting for deployment

3. **Incident costs**:
   - Engineer time responding to incidents
   - Downtime costs (lost revenue)

4. **Opportunity costs**:
   - Lost deals due to missing features
   - Customer churn due to slow delivery

**Show your calculations**:
```
Example:
Deployment labor cost:
- Successful deployments: 12/year * 60% success rate = 7.2 deployments
- Labor per deployment: 4 hours * 5 people * $100/hour = $2,000
- Annual cost: 7.2 * $2,000 = $14,400

Failed deployments:
- Failed deployments: 12/year * 40% failure rate = 4.8 deployments
- Labor per failure: 8 hours (deploy + rollback) * 5 people * $100/hour = $4,000
- Annual cost: 4.8 * $4,000 = $19,200

... (continue for all categories)
```

**Deliverable**: `part4-current-costs.md`

**Grading criteria**:
- All cost categories calculated (10 pts)
- Calculations shown clearly (5 pts)
- Annual total calculated (5 pts)

---

### Part 5: Project DevOps ROI (20 points)

**Task**: Propose a DevOps transformation and calculate the expected ROI.

**DevOps Investment (Year 1)**:
You decide what to invest in. Example categories:
- CI/CD tools (GitHub Actions, Jenkins, etc.)
- Cloud infrastructure
- Monitoring tools (Prometheus, Grafana)
- Training for team
- Consulting (optional)

**Estimated total investment**: $200k - $500k (you decide based on what you propose)

**Expected Improvements** (be realistic):
Based on industry benchmarks, propose:
- Deployment frequency improvement (monthly → ?)
- Lead time improvement (X days → ?)
- Change failure rate improvement (40% → ?)
- Incident reduction (8/month → ?)

**Calculate**:
1. **Year 1 savings** (based on improvements)
2. **Year 1 ROI** = (Savings - Investment) / Investment * 100%
3. **Payback period** (how many months to break even?)

**Deliverable**: `part5-roi-projection.md`

**Grading criteria**:
- Investment breakdown realistic (5 pts)
- Improvement projections realistic (5 pts)
- ROI calculation correct (5 pts)
- Business case compelling (5 pts)

---

### Part 6: Executive Summary (20 points)

**Task**: Write a 1-page executive summary to present to the CEO.

**Include**:
1. **Current state**: Key problems and costs
2. **Proposed solution**: High-level DevOps approach
3. **Investment required**: Year 1 costs
4. **Expected outcomes**: Metrics improvement + business impact
5. **ROI**: Return on investment
6. **Recommendation**: Why should the company proceed?

**Format**: Professional memo style

**Example structure**:
```markdown
# Executive Summary: DevOps Transformation Proposal
**To**: CEO, HealthTech Solutions
**From**: [Your Name], DevOps Analyst
**Date**: [Today's date]

## Current Situation
HealthTech Solutions currently deploys software monthly, with a 40-day lead time
from feature start to production. This slow pace is costing us $X annually in:
- Lost revenue: $Y
- Operational inefficiency: $Z
- Customer dissatisfaction: [impact]

## Proposed Solution
Implement DevOps practices including:
- Continuous Integration/Continuous Deployment
- Automated testing
- Infrastructure as code
- Comprehensive monitoring

## Investment
Year 1: $[amount]
- Tooling: $X
- Training: $Y
- Infrastructure: $Z

## Expected Outcomes
- Deployment frequency: Monthly → Weekly (Year 1) → Daily (Year 2)
- Lead time: 40 days → 7 days
- Change failure rate: 40% → 15%
- Annual cost savings: $[amount]

## ROI
Year 1: [X]%
3-Year Net Benefit: $[amount]

## Recommendation
[Your compelling recommendation]
```

**Deliverable**: `part6-executive-summary.md`

**Grading criteria**:
- Clear problem statement (4 pts)
- Professional presentation (4 pts)
- Compelling business case (4 pts)
- Accurate financials (4 pts)
- Strong recommendation (4 pts)

---

## Submission

Create a folder: `exercises/module-01/exercise-02/`

Include:
1. `part1-process-map.md`
2. `part2-lead-time-calculation.md`
3. `part3-bottleneck-analysis.md`
4. `part4-current-costs.md`
5. `part5-roi-projection.md`
6. `part6-executive-summary.md`

**Commit to your branch and create a pull request when done.**

---

## Grading Rubric

| Part | Points | Description |
|------|--------|-------------|
| **Part 1: Process Map** | 20 | Complete process visualization |
| **Part 2: Lead Time** | 20 | Accurate calculations, waste identified |
| **Part 3: Bottlenecks** | 20 | Correct identification and analysis |
| **Part 4: Current Costs** | 20 | Comprehensive cost calculation |
| **Part 5: ROI Projection** | 20 | Realistic projections, accurate ROI |
| **Part 6: Executive Summary** | 20 | Professional, compelling presentation |
| **Total** | 120 | |

**Passing**: 96/120 (80%)

---

## Tips for Success

1. **Show your work**: Always show calculations, don't just give final numbers

2. **Be realistic**: Don't claim 1000x improvement in Year 1

3. **Think holistically**: Consider all costs (labor, opportunity, incidents)

4. **Use industry benchmarks**: Reference DORA metrics from Lesson 5

5. **Make it compelling**: You're making a business case, not just an exercise

---

## What You'll Learn

This exercise teaches:
- **Financial analysis**: Calculate costs and ROI
- **Process analysis**: Identify inefficiencies
- **Business communication**: Present technical concepts to executives
- **Strategic thinking**: Prioritize improvements based on impact

These skills are valuable beyond DevOps:
- Any process improvement initiative
- Business case development
- Strategic planning

---

## Questions?

If stuck, review:
- Lesson 2: Business Case for DevOps
- Lesson 5: Measuring DevOps Success (DORA metrics)

Tag instructor in PR with specific questions!

---

**Good luck! This is one of the most practical exercises - you're building skills you'll use throughout your career.**
