# Module 1 Glossary: DevOps Fundamentals

Quick reference for key terms from Module 1.

---

## A

**Agile**
Software development methodology emphasizing iterative development, collaboration, and flexibility. DevOps extends Agile practices to operations.

**Automation**
Using tools and scripts to perform tasks without human intervention. Core principle of DevOps (automate repetitive work to reduce errors and free up time for innovation).

**Availability**
Percentage of time a system is operational and accessible. Calculated as: `(Total time - Downtime) / Total time × 100%`. Example: 99.9% = 43 minutes downtime per month.

---

## B

**Blameless Post-Mortem**
Incident review process focused on learning from failures rather than punishing individuals. Key questions: "What happened? What can we learn? How do we prevent this?" NOT "Who is responsible?"

**Blue-Green Deployment**
Deployment strategy using two identical environments (Blue = current, Green = new). Deploy to Green, test, then switch traffic. Enables instant rollback.

**Bottleneck**
The slowest part of a process that limits overall throughput. Identified using flow analysis. Example: If QA can only test 2 features/week, but dev completes 10 features/week, QA is the bottleneck.

---

## C

**Canary Deployment**
Deployment strategy where new version is rolled out to small percentage of users first (e.g., 5%), monitored, then gradually expanded to 100% if metrics look good.

**Change Failure Rate (CFR)**
DORA metric: Percentage of changes to production that result in degraded service or require remediation. Elite: 0-15%, Low: 46-60%.

**Chaos Engineering**
Practice of intentionally introducing failures in production to test system resilience. Example: Netflix's Chaos Monkey randomly kills servers.

**CI/CD (Continuous Integration/Continuous Delivery)**
- **CI**: Developers integrate code frequently (multiple times per day), with automated testing
- **CD**: Automated deployment pipeline from code commit to production

**Continuous Deployment**
Extension of CD where every code change that passes automated tests is automatically deployed to production (no manual approval).

**Continuous Integration (CI)**
Practice of developers merging code to shared repository frequently (at least daily), with automated builds and tests.

---

## D

**Deployment Frequency**
DORA metric: How often code is deployed to production. Elite: On-demand (multiple/day), Low: Less than monthly.

**DevOps**
Cultural movement and set of practices that combines software development (Dev) and IT operations (Ops) to shorten development lifecycle and deliver high-quality software continuously.

**DORA (DevOps Research and Assessment)**
Research program studying DevOps practices and performance. Identified four key metrics: Deployment Frequency, Lead Time, Change Failure Rate, MTTR.

**DORA Metrics**
Four metrics that predict organizational performance:
1. Deployment Frequency
2. Lead Time for Changes
3. Change Failure Rate
4. Time to Restore Service (MTTR)

---

## E

**Elite Performer**
Organization in top 25% for DORA metrics. Characteristics: Deploy on-demand, lead time < 1 hour, CFR < 15%, MTTR < 1 hour.

---

## F

**Feedback Loop**
Process where output from one phase informs input to an earlier phase. Fast feedback enables fast learning. Example: Monitoring shows high error rate → feedback to developers → code fix.

**Feature Flag (Feature Toggle)**
Technique to enable/disable features in production without deploying code. Allows deploying code with features "off", then enabling gradually for testing.

**Flow**
First Way of DevOps: Optimizing the flow of work from development to operations to customer. Minimize handoffs, reduce batch sizes, limit work in progress.

---

## I

**Infrastructure as Code (IaC)**
Managing and provisioning infrastructure through code rather than manual processes. Benefits: Version control, repeatability, documentation.

---

## K

**Kaizen**
Japanese concept of continuous improvement through small, incremental changes. Core principle of DevOps culture.

---

## L

**Lead Time for Changes**
DORA metric: Time from code committed to code successfully running in production. Elite: < 1 hour, Low: 1-6 months.

**Low Performer**
Organization in bottom 25% for DORA metrics. Characteristics: Deploy less than monthly, lead time 1-6 months, CFR 46-60%, MTTR > 1 week.

---

## M

**Mean Time to Recovery (MTTR) / Time to Restore Service**
DORA metric: Average time to restore service after an incident. Elite: < 1 hour, Low: > 1 week.

**Microservices**
Architectural style where application is composed of small, independent services. Enables teams to deploy independently.

**Monitoring**
Collecting and analyzing metrics, logs, and traces to understand system behavior. Enables fast detection and resolution of issues.

**MTTR (Mean Time to Repair/Recovery)**
See "Time to Restore Service"

---

## O

**Observability**
Ability to understand internal state of a system by examining its outputs. Three pillars: Metrics, logs, traces.

---

## P

**Process Time**
Actual time spent working on a task (excludes waiting). Used in lead time analysis to identify waste.

**Psychological Safety**
Team environment where members feel safe to take risks, admit mistakes, ask questions without fear of punishment. Predicts high-performing teams (Google research).

---

## R

**Rolling Deployment**
Deployment strategy where new version is gradually deployed to servers one at a time, maintaining service availability.

**Rollback**
Reverting to previous version of software after failed deployment. Fast rollback capability reduces risk of deployment.

---

## S

**Silo**
Organizational structure where teams operate independently with minimal communication. DevOps aims to break down silos between Dev and Ops.

**SLA (Service Level Agreement)**
Commitment between service provider and customer. Example: "99.9% uptime" means max 43 minutes downtime per month.

**SLO (Service Level Objective)**
Internal target for service level. Typically more stringent than SLA to provide buffer.

**SRE (Site Reliability Engineering)**
Role/practice (originated at Google) applying software engineering principles to operations. SRE teams build systems to automate operations work.

---

## T

**The Three Ways**
Core principles of DevOps (from "The Phoenix Project"):
1. **Flow**: Optimize work flow from Dev → Ops → Customer
2. **Feedback**: Create fast feedback loops
3. **Continuous Learning**: Culture of experimentation and learning from failure

**Time to Restore Service**
See "MTTR"

**Toil**
Manual, repetitive, automatable work that doesn't add value. DevOps aims to eliminate toil through automation.

**Trunk-Based Development**
Development practice where developers merge small changes to main branch (trunk) frequently, avoiding long-lived feature branches.

---

## W

**Wait Time**
Time spent waiting (not actively working). Often 80-90% of total lead time. Identifying and reducing wait time is key to improving flow.

**Waterfall**
Traditional software development methodology with sequential phases: Requirements → Design → Implementation → Testing → Deployment. Contrasts with Agile/DevOps iterative approach.

**Westrum Organizational Culture Model**
Framework identifying three culture types:
- **Pathological** (power-oriented): Information hoarded, messengers shot, failure covered up
- **Bureaucratic** (rule-oriented): Information flows through channels, compartmentalized responsibility
- **Generative** (performance-oriented): Information flows freely, shared responsibility, learning from failure

DevOps requires generative culture.

---

## Acronyms Quick Reference

- **CD**: Continuous Delivery or Continuous Deployment
- **CFR**: Change Failure Rate
- **CI**: Continuous Integration
- **CI/CD**: Continuous Integration/Continuous Delivery
- **DORA**: DevOps Research and Assessment
- **IaC**: Infrastructure as Code
- **MTTR**: Mean Time to Recovery/Repair
- **NPS**: Net Promoter Score
- **ROI**: Return on Investment
- **SLA**: Service Level Agreement
- **SLO**: Service Level Objective
- **SRE**: Site Reliability Engineering
- **WIP**: Work in Progress

---

## See Also

- [Cheat Sheet](cheat-sheet.md) - Quick commands and formulas
- [Further Reading](further-reading.md) - Books, articles, videos

---

**Tip**: Bookmark this page for quick reference throughout the curriculum!
