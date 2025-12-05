# Module 1 Cheat Sheet: DevOps Fundamentals

Quick reference for formulas, metrics, and key concepts.

---

## DORA Metrics Quick Reference

### 1. Deployment Frequency
**Formula**: `Total deployments / Time period`

**Performance Levels**:
| Level | Frequency |
|-------|-----------|
| Elite | On-demand (multiple/day) |
| High | Weekly to monthly |
| Medium | Monthly to quarterly |
| Low | Less than quarterly |

**Example**: 52 deployments / 52 weeks = 1 per week (High)

---

### 2. Lead Time for Changes
**Formula**: `Time from commit to production deployment`

**Calculate**:
- Mean (average)
- Median (p50)
- p95 (95th percentile)

**Performance Levels**:
| Level | Lead Time |
|-------|-----------|
| Elite | < 1 hour |
| High | 1 day to 1 week |
| Medium | 1 week to 1 month |
| Low | 1 to 6 months |

**Example**:
```
Features: 2d, 3d, 5d, 7d, 10d
Mean: (2+3+5+7+10)/5 = 5.4 days (High)
Median: 5 days
```

---

### 3. Change Failure Rate (CFR)
**Formula**: `(Failed deployments / Total deployments) × 100%`

**Performance Levels**:
| Level | Failure Rate |
|-------|--------------|
| Elite | 0-15% |
| High | 16-30% |
| Medium | 31-45% |
| Low | 46-60% |

**Example**: 5 failures / 50 deployments × 100% = 10% (Elite)

---

### 4. Time to Restore Service (MTTR)
**Formula**: `Time from incident detected to service restored`

**Calculate**:
- Mean (average)
- Median (p50)

**Performance Levels**:
| Level | MTTR |
|-------|------|
| Elite | < 1 hour |
| High | < 1 day |
| Medium | 1 day to 1 week |
| Low | > 1 week |

**Example**:
```
Incidents: 30min, 45min, 1h, 2h
Mean: (0.5+0.75+1+2)/4 = 1.06 hours (High)
```

---

## Cost Calculations

### Deployment Cost
**Formula**:
```
Deployment Cost = Hours × People × Hourly rate

Example:
- 4 hours × 5 people × $100/hour = $2,000 per deployment
- 12 deployments/year = $24,000/year
```

### Incident Cost
**Formula**:
```
Incident Cost = (Engineer hours × Hourly rate) + (Downtime hours × Revenue per hour)

Example:
- Engineer time: 4 hours × 3 people × $100/hour = $1,200
- Downtime: 4 hours × $5,000/hour = $20,000
- Total: $21,200 per incident
```

### Opportunity Cost
**Formula**:
```
Opportunity Cost = Lost deals × Deal value

OR

Opportunity Cost = Delay (months) × Revenue per month from feature

Example:
- Competitor launches feature 3 months earlier
- Feature worth $50k/month
- Opportunity cost: 3 × $50,000 = $150,000
```

### ROI Calculation
**Formula**:
```
ROI = (Savings - Investment) / Investment × 100%

Example:
- Investment: $300,000
- Savings: $750,000
- ROI: ($750k - $300k) / $300k × 100% = 150%
```

### Payback Period
**Formula**:
```
Payback Period (months) = Investment / (Monthly savings)

Example:
- Investment: $300,000
- Monthly savings: $50,000
- Payback: $300k / $50k = 6 months
```

---

## Lead Time Analysis

### Total Lead Time
**Formula**: `Lead Time = Process Time + Wait Time`

**Example**:
```
Development: 3 days (process)
Wait for review: 2 days (wait)
Code review: 1 day (process)
Wait for QA: 5 days (wait)
QA testing: 2 days (process)
Wait for deployment: 30 days (wait)
Deployment: 0.25 days (process)

Lead Time: 43.25 days
Process Time: 6.25 days (14%)
Wait Time: 37 days (86%)
```

**Insight**: Most time is waiting!

### Efficiency Ratio
**Formula**: `Efficiency = Process Time / Lead Time × 100%`

**Example**: 6.25 / 43.25 × 100% = 14% efficient (86% waste!)

---

## Availability Calculations

### Uptime Percentage
**Formula**: `Availability = (Total time - Downtime) / Total time × 100%`

**Example**:
```
Month: 720 hours
Downtime: 1 hour
Availability: (720 - 1) / 720 × 100% = 99.86%
```

### SLA Tiers
| SLA | Downtime/Year | Downtime/Month | Downtime/Week |
|-----|---------------|----------------|---------------|
| 99% | 3.65 days | 7.2 hours | 1.68 hours |
| 99.9% ("three nines") | 8.76 hours | 43.2 minutes | 10.1 minutes |
| 99.99% ("four nines") | 52.6 minutes | 4.32 minutes | 1.01 minutes |
| 99.999% ("five nines") | 5.26 minutes | 25.9 seconds | 6.05 seconds |

---

## The Three Ways (Principles)

### First Way: FLOW
**Goal**: Optimize flow from Dev → Ops → Customer

**Practices**:
- ✅ Make work visible (Kanban boards)
- ✅ Limit work in progress (WIP)
- ✅ Reduce batch sizes (small deployments)
- ✅ Reduce handoffs (automate)
- ✅ Identify bottlenecks

### Second Way: FEEDBACK
**Goal**: Create fast feedback loops

**Practices**:
- ✅ Automated testing (fast feedback on code quality)
- ✅ Continuous monitoring (fast feedback on production health)
- ✅ A/B testing (fast feedback on feature value)
- ✅ Telemetry (instrument everything)

### Third Way: CONTINUOUS LEARNING
**Goal**: Foster culture of experimentation and learning

**Practices**:
- ✅ Blameless post-mortems
- ✅ Psychological safety
- ✅ Experimentation encouraged
- ✅ Time for learning (20% time)
- ✅ Kaizen (continuous improvement)

---

## Westrum Culture Types

| Aspect | Pathological | Bureaucratic | Generative |
|--------|--------------|--------------|------------|
| Information | Hoarded | Flows through channels | Flows freely |
| Messengers | Shot | Tolerated | Trained |
| Responsibility | Shirked | Compartmentalized | Shared |
| Bridging | Discouraged | Allowed | Rewarded |
| Failure | Covered up | Leads to investigation | Leads to inquiry/learning |
| New ideas | Crushed | Create problems | Welcomed |

**DevOps requires**: Generative culture

---

## DevOps Infinity Loop (8 Phases)

```
Plan → Code → Build → Test → Release → Deploy → Operate → Monitor
  ↑                                                              |
  └──────────────────────────────────────────────────────────────
                     (Continuous feedback)
```

1. **Plan**: Define what to build
2. **Code**: Write the software
3. **Build**: Compile and create artifacts
4. **Test**: Verify it works
5. **Release**: Prepare for deployment
6. **Deploy**: Put in production
7. **Operate**: Keep it running
8. **Monitor**: Learn and improve

---

## Quick Decision Trees

### "Should I automate this?"
```
Is task:
- Repetitive? (done multiple times)
- Automatable? (can be scripted)
- Time-consuming? (takes > 5 minutes)
- Error-prone? (humans make mistakes)

If YES to 2+: Automate!
```

### "What's the bottleneck?"
```
1. Map the process
2. Measure duration of each step
3. Identify where work queues up
4. Check: Can this step handle throughput of previous steps?
5. If NO: Bottleneck found!
```

### "Elite, High, Medium, or Low?"
```
Calculate all 4 DORA metrics
Check each against performance levels
Take LOWEST level as overall

Example:
- Deployment frequency: Elite
- Lead time: High
- CFR: Elite
- MTTR: High

Overall: High (lowest level found)
```

---

## ROI Presentation Template

```markdown
## Current State
- Problem: [One sentence]
- Cost: $[X] annually
- Impact: [Business impact]

## Proposed Solution
- Approach: [DevOps practices]
- Timeline: [X months]

## Investment
- Year 1: $[X]
- Breakdown: [Tools, training, time]

## Expected Outcomes
- Metric improvements: [Specific numbers]
- Cost savings: $[X] annually
- Business value: [Revenue, satisfaction, etc.]

## ROI
- Year 1 ROI: [X]%
- Payback: [X] months
- 3-year net benefit: $[X]

## Recommendation
[Clear next step]
```

---

## Common Metrics

### Error Rate
`(Errors / Total requests) × 100%`

Example: 100 errors / 10,000 requests = 1%

### Response Time (Latency)
Use percentiles, not averages:
- **p50** (median): 50% of requests faster
- **p95**: 95% of requests faster
- **p99**: 99% of requests faster

Example: p95 = 500ms means 95% of requests complete under 500ms

### Code Coverage
`(Lines covered by tests / Total lines) × 100%`

Example: 800 covered / 1000 total = 80%

Target: 80%+ for critical paths

---

## Deployment Strategies

### Blue-Green
```
Blue (current) ← 100% traffic
Green (new) ← 0% traffic

Deploy to Green → Test → Switch traffic 100% to Green

Rollback: Switch back to Blue
```

### Canary
```
Deploy to 5% of servers → Monitor 30 min
If good: Deploy to 25%
If good: Deploy to 50%
If good: Deploy to 100%

If any problems: Rollback canary
```

### Rolling
```
10 servers total

Deploy to server 1 → Health check → Deploy to server 2 → ...

Continue until all 10 updated
```

---

## The 5 Whys (Root Cause Analysis)

```
Problem: [State the problem]

Why? [Answer]
Why? [Dig deeper]
Why? [Dig deeper]
Why? [Dig deeper]
Why? [Usually reach root cause by 5th why]

Root Cause: [Typically a process or system issue, not a person]
```

**Example**:
```
Problem: Deployment failed

Why? Configuration file had typo
Why? Manual configuration process
Why? No infrastructure as code
Why? Team didn't know IaC tools existed
Why? No training budget allocated

Root Cause: Lack of training investment
```

---

## Quick Conversions

### Time Units
- 1 week = 5 business days = 40 hours
- 1 month = ~4 weeks = ~20 business days = ~160 hours
- 1 quarter = 3 months = ~60 business days
- 1 year = 52 weeks = ~260 business days = ~2080 hours

### Cost Calculations
If annual salary = $208,000:
- Hourly rate ≈ $100/hour ($208k / 2080 hours)

---

## Useful Benchmarks (From Case Studies)

| Company | Deployment Freq | Lead Time | CFR | Note |
|---------|----------------|-----------|-----|------|
| Amazon | Every 11.6 sec | Hours | <1% | Elite |
| Netflix | 4000/day | Hours | <10% | Elite |
| Etsy | 25-50/day | 15 min | <1% | Elite |
| Traditional Bank | Quarterly | 3 months | 40% | Low |

---

## Key Takeaways for Module 1

1. **DevOps emerged to solve**: Silos, manual processes, slow deployments, blame culture
2. **Core practices**: CI/CD, IaC, monitoring, automation, culture change
3. **Measure with**: DORA metrics (DF, LT, CFR, MTTR)
4. **Three Ways**: Flow, Feedback, Continuous Learning
5. **Culture matters**: Blameless, psychological safety, generative
6. **ROI is real**: 200-500% typical by Year 2
7. **Start small**: Pilot project, prove value, scale

---

**Next Module**: Linux & Git (technical foundations)

---

## See Also

- [Glossary](glossary.md) - Definitions of all terms
- [Further Reading](further-reading.md) - Books, articles, videos
