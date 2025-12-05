# Exercise 1.3: DORA Metrics Calculation & Analysis

**Objective**: Calculate and analyze the four DORA metrics to assess DevOps performance

**Time**: 60 minutes

**Skills**: Data analysis, metrics calculation, performance assessment

## Background

DORA (DevOps Research and Assessment) identified four key metrics that predict organizational performance:

1. **Deployment Frequency**: How often you deploy
2. **Lead Time for Changes**: Commit to production time
3. **Change Failure Rate**: % of deployments causing issues
4. **Time to Restore Service (MTTR)**: Recovery time from incidents

In this exercise, you'll calculate these metrics for three different companies and determine their performance level.

## Part 1: Calculate DORA Metrics for Three Companies

### Company A: "StartupFast"

**Background**: Early-stage startup, 5 engineers, SaaS product

**Data from last quarter (90 days)**:

**Deployments**:
- Total deployments to production: 180
- Deployments per day: 2 (on average)

**Lead Time** (sample of 10 recent features):
```
Feature 1: Committed 10:00 AM, deployed 10:45 AM (45 minutes)
Feature 2: Committed 2:00 PM, deployed 3:30 PM (90 minutes)
Feature 3: Committed 9:00 AM, deployed 10:00 AM (60 minutes)
Feature 4: Committed 1:00 PM, deployed 2:15 PM (75 minutes)
Feature 5: Committed 11:00 AM, deployed 12:30 PM (90 minutes)
Feature 6: Committed 4:00 PM, deployed 5:00 PM (60 minutes)
Feature 7: Committed 10:00 AM, deployed 11:00 AM (60 minutes)
Feature 8: Committed 3:00 PM, deployed 4:30 PM (90 minutes)
Feature 9: Committed 9:30 AM, deployed 10:15 AM (45 minutes)
Feature 10: Committed 2:30 PM, deployed 4:00 PM (90 minutes)
```

**Deployment Outcomes**:
- Successful deployments: 165
- Deployments that caused issues (required rollback or hotfix): 15

**Incidents** (last quarter):
```
Incident 1:
- Detected: 10:00 AM
- Resolved: 10:25 AM
- Duration: 25 minutes

Incident 2:
- Detected: 2:00 PM
- Resolved: 2:45 PM
- Duration: 45 minutes

Incident 3:
- Detected: 11:00 AM
- Resolved: 11:20 AM
- Duration: 20 minutes

Incident 4:
- Detected: 3:00 PM
- Resolved: 3:50 PM
- Duration: 50 minutes

Incident 5:
- Detected: 9:00 AM
- Resolved: 9:30 AM
- Duration: 30 minutes
```

---

### Company B: "MidCorp"

**Background**: Established company, 50 engineers, enterprise software

**Data from last quarter (90 days)**:

**Deployments**:
- Total deployments to production: 12
- Frequency: Weekly deployments (but skipped 2 weeks due to holidays)

**Lead Time** (sample of 10 recent features):
```
Feature 1: Started March 1, deployed March 8 (7 days)
Feature 2: Started March 3, deployed March 15 (12 days)
Feature 3: Started March 5, deployed March 15 (10 days)
Feature 4: Started March 10, deployed March 22 (12 days)
Feature 5: Started March 12, deployed March 22 (10 days)
Feature 6: Started March 15, deployed March 29 (14 days)
Feature 7: Started March 18, deployed April 5 (18 days)
Feature 8: Started March 20, deployed April 5 (16 days)
Feature 9: Started March 22, deployed April 12 (21 days)
Feature 10: Started March 25, deployed April 19 (25 days)
```

**Deployment Outcomes**:
- Successful deployments: 9
- Deployments that caused issues: 3

**Incidents** (last quarter):
```
Incident 1:
- Detected: Monday 10:00 AM
- Resolved: Monday 4:00 PM
- Duration: 6 hours

Incident 2:
- Detected: Wednesday 2:00 PM
- Resolved: Thursday 10:00 AM
- Duration: 20 hours

Incident 3:
- Detected: Friday 11:00 AM
- Resolved: Friday 3:00 PM
- Duration: 4 hours

Incident 4:
- Detected: Tuesday 9:00 AM
- Resolved: Tuesday 5:00 PM
- Duration: 8 hours

Incident 5:
- Detected: Monday 1:00 PM
- Resolved: Tuesday 9:00 AM
- Duration: 20 hours

Incident 6:
- Detected: Thursday 3:00 PM
- Resolved: Thursday 8:00 PM
- Duration: 5 hours
```

---

### Company C: "LegacyCorp"

**Background**: Large enterprise, 200 engineers, highly regulated industry

**Data from last year (365 days)**:

**Deployments**:
- Total deployments to production: 4
- Frequency: Quarterly deployments

**Lead Time** (all features from last deployment):
```
Feature 1: Started Jan 5, deployed April 1 (86 days)
Feature 2: Started Jan 10, deployed April 1 (81 days)
Feature 3: Started Jan 20, deployed April 1 (71 days)
Feature 4: Started Feb 1, deployed April 1 (59 days)
Feature 5: Started Feb 10, deployed April 1 (50 days)
Feature 6: Started Feb 20, deployed April 1 (40 days)
Feature 7: Started March 1, deployed April 1 (31 days)
Feature 8: Started March 10, deployed April 1 (22 days)
Feature 9: Started March 15, deployed April 1 (17 days)
Feature 10: Started March 20, deployed April 1 (12 days)
```

**Deployment Outcomes**:
- Successful deployments: 2
- Deployments that caused major issues: 2

**Incidents** (last year):
```
Incident 1:
- Detected: Monday 9:00 AM
- Resolved: Friday 5:00 PM
- Duration: 104 hours (4.3 days)

Incident 2:
- Detected: Wednesday 10:00 AM
- Resolved: Thursday 2:00 PM
- Duration: 28 hours

Incident 3:
- Detected: Tuesday 2:00 PM
- Resolved: Wednesday 10:00 AM
- Duration: 20 hours

Incident 4:
- Detected: Friday 3:00 PM
- Resolved: Monday 11:00 AM
- Duration: 68 hours (2.8 days)

Incident 5:
- Detected: Monday 11:00 AM
- Resolved: Wednesday 9:00 AM
- Duration: 46 hours

Incident 6:
- Detected: Thursday 1:00 PM
- Resolved: Friday 10:00 AM
- Duration: 21 hours

Incident 7:
- Detected: Tuesday 9:00 AM
- Resolved: Tuesday 4:00 PM
- Duration: 7 hours

Incident 8:
- Detected: Friday 4:00 PM
- Resolved: Tuesday 10:00 AM
- Duration: 90 hours (3.75 days)
```

---

## Your Tasks

### Task 1: Calculate DORA Metrics (60 points)

For **each company**, calculate all four DORA metrics:

#### Metric 1: Deployment Frequency

**Calculate**:
- Deployments per day, week, or month
- Express in the format DORA uses (e.g., "multiple times per day", "weekly", "monthly", "quarterly")

**Show your work**:
```
Company A:
- Total deployments: 180
- Time period: 90 days
- Deployments per day: 180 / 90 = 2 per day
- DORA category: "On-demand (multiple deploys per day)"
```

#### Metric 2: Lead Time for Changes

**Calculate**:
- Average lead time (mean)
- Median lead time (p50)
- 95th percentile lead time (p95)
- Express in hours, days, or months as appropriate

**Show your work**:
```
Company A:
Feature lead times (in minutes): 45, 90, 60, 75, 90, 60, 60, 90, 45, 90

Step 1: Sort values: 45, 45, 60, 60, 60, 75, 90, 90, 90, 90
Step 2: Calculate mean: (45+45+60+60+60+75+90+90+90+90) / 10 = 70.5 minutes
Step 3: Calculate median: (60 + 75) / 2 = 67.5 minutes
Step 4: Calculate p95: 90 minutes (95th percentile)

Average lead time: 70.5 minutes = 1.2 hours
DORA category: "Less than one hour" (Elite)
```

#### Metric 3: Change Failure Rate

**Calculate**:
- Number of failed deployments / Total deployments × 100%
- Express as a percentage

**Show your work**:
```
Company A:
- Failed deployments: 15
- Total deployments: 180
- Change failure rate: (15 / 180) × 100% = 8.3%
- DORA category: "0-15%" (Elite)
```

#### Metric 4: Time to Restore Service (MTTR)

**Calculate**:
- Average time to restore (mean)
- Median time to restore (p50)
- Express in hours or days as appropriate

**Show your work**:
```
Company A:
Incident durations (in minutes): 25, 45, 20, 50, 30

Step 1: Calculate mean: (25+45+20+50+30) / 5 = 34 minutes
Step 2: Calculate median: Sort: 20, 25, 30, 45, 50 → median = 30 minutes

Average MTTR: 34 minutes = 0.57 hours
DORA category: "Less than one hour" (Elite)
```

**Deliverable**: `task1-dora-calculations.md`

**Format**:
```markdown
# DORA Metrics Calculations

## Company A: StartupFast

### Deployment Frequency
[Your calculations]
Result: X per day/week/month
DORA Category: Elite/High/Medium/Low

### Lead Time for Changes
[Your calculations]
Result: X hours/days/months
DORA Category: Elite/High/Medium/Low

### Change Failure Rate
[Your calculations]
Result: X%
DORA Category: Elite/High/Medium/Low

### Time to Restore Service
[Your calculations]
Result: X hours/days
DORA Category: Elite/High/Medium/Low

[Repeat for Company B and Company C]
```

**Grading**:
- Company A calculations (20 pts)
- Company B calculations (20 pts)
- Company C calculations (20 pts)

---

### Task 2: Performance Level Classification (15 points)

For each company, determine their overall DORA performance level: **Elite**, **High**, **Medium**, or **Low**.

**Reference**:
| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| Deployment Frequency | On-demand | Weekly-Monthly | Monthly-Quarterly | < Quarterly |
| Lead Time | < 1 hour | 1 day - 1 week | 1 week - 1 month | > 1 month |
| Change Failure Rate | 0-15% | 16-30% | 31-45% | 46-60% |
| MTTR | < 1 hour | < 1 day | 1 day - 1 week | > 1 week |

**Classify each company** and justify:

```markdown
## Company A: StartupFast

Performance Level: [Elite/High/Medium/Low]

Justification:
- Deployment Frequency: [Elite/High/Medium/Low] - [reason]
- Lead Time: [Elite/High/Medium/Low] - [reason]
- Change Failure Rate: [Elite/High/Medium/Low] - [reason]
- MTTR: [Elite/High/Medium/Low] - [reason]

Overall: [Explain how you determined overall level]
```

**Deliverable**: `task2-performance-levels.md`

**Grading**:
- Correct classification (9 pts)
- Clear justification (6 pts)

---

### Task 3: Analysis and Recommendations (25 points)

For **each company**, provide:

1. **Strengths**: What are they doing well?
2. **Weaknesses**: What needs improvement?
3. **Priority improvements**: Top 2-3 areas to focus on
4. **Specific recommendations**: How to improve

**Example**:
```markdown
## Company A: StartupFast

### Strengths
- Exceptional deployment frequency (2x per day)
- Very fast lead time (70 minutes average)
- Low change failure rate (8.3%)
- Fast recovery from incidents (34 minutes)

Overall: Elite performer across all metrics

### Weaknesses
- Even at Elite level, can still improve:
  - 8.3% failure rate could be reduced
  - Some lead times reach 90 minutes (outliers)

### Priority Improvements
1. Further reduce change failure rate (target: < 5%)
2. Reduce lead time variance (some features take 2x longer)

### Specific Recommendations
1. Increase automated test coverage (reduce failures)
2. Implement canary deployments (catch issues earlier)
3. Analyze the 90-minute outliers (what's different?)
4. Continue current practices (working well!)
```

**Deliverable**: `task3-analysis-recommendations.md`

**Grading**:
- Accurate analysis of strengths/weaknesses (10 pts)
- Practical recommendations (10 pts)
- Prioritization based on data (5 pts)

---

## Submission

Create a folder: `exercises/module-01/exercise-03/`

Include:
1. `task1-dora-calculations.md`
2. `task2-performance-levels.md`
3. `task3-analysis-recommendations.md`

**Commit to your branch and create a pull request when done.**

---

## Grading Rubric

| Task | Points | Description |
|------|--------|-------------|
| **Task 1: Calculations** | 60 | Accurate DORA metrics for all companies |
| **Task 2: Classification** | 15 | Correct performance level determination |
| **Task 3: Analysis** | 25 | Insightful analysis and recommendations |
| **Total** | 100 | |

**Passing**: 80/100

---

## Tips for Success

1. **Show your work**: Always show calculations step-by-step

2. **Use correct units**: Minutes, hours, days - be consistent

3. **Calculate percentiles correctly**:
   - Median (p50): Middle value when sorted
   - p95: 95% of values are below this

4. **Consider context**: A bank and a startup have different constraints

5. **Be specific**: "Improve testing" is vague. "Add integration tests for checkout flow" is specific.

---

## Bonus Challenge (Optional, +5 points)

**Create a visualization** of the three companies' DORA metrics.

You can use:
- Spreadsheet (Excel, Google Sheets) with charts
- Python/matplotlib
- Any visualization tool

**Show**:
- Radar chart comparing all four metrics
- Bar chart showing performance levels
- Or other creative visualization

**Deliverable**: `bonus-visualization.png` (or `.pdf`)

---

## What You'll Learn

This exercise teaches:
- **How to calculate DORA metrics** from raw data
- **How to interpret metrics** (not just calculate)
- **How to provide actionable recommendations**
- **How to compare organizations** objectively

These skills apply to:
- Assessing your own team's performance
- Benchmarking against industry standards
- Identifying improvement opportunities
- Communicating DevOps value

---

## Questions?

If stuck, review:
- Lesson 5: Measuring DevOps Success

For statistical calculations (mean, median, percentiles), use:
- Calculator
- Spreadsheet
- Python (if you know it)

Tag instructor in PR with specific questions!

---

**Good luck! Remember: Metrics are a tool for improvement, not punishment.**
