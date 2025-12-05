# Module 1 Quiz Answers
**Student Name**: Bob Smith (Good Student)
**Date**: 2024-01-15

## Part 1: Multiple Choice (2 points each)

### Question 1
What problem led to the emergence of DevOps?

**Your Answer**: B

### Question 2
What does "Continuous Integration" mean?

**Your Answer**: A

### Question 3
In traditional IT (pre-DevOps), what was the typical deployment frequency?

**Your Answer**: C

### Question 4
What is "toil" in DevOps context?

**Your Answer**: A

### Question 5
What do the "three pillars" of DevOps refer to?

**Your Answer**: B

## Part 2: True/False (1 point each)

### Question 6
True or False: DevOps is primarily about buying the right tools (Jenkins, Docker, Kubernetes).

**Your Answer**: False

**Explanation**: DevOps is more about culture and collaboration than just tools. While tools like Jenkins and Docker are important, they won't help if teams don't work together.

### Question 7
True or False: Automation eliminates jobs, which is why operations teams resist DevOps.

**Your Answer**: False

**Explanation**: Automation helps people do their jobs better by removing boring repetitive work. People can then focus on more important tasks.

### Question 8
True or False: In blameless post-mortems, the goal is to learn from failures, not punish individuals.

**Your Answer**: True

**Explanation**: Blameless post-mortems mean you don't blame people when things go wrong. Instead you try to figure out what happened and how to prevent it next time.

### Question 9
True or False: DevOps means Development team owns Operations tasks, so we don't need Ops engineers.

**Your Answer**: False

**Explanation**: DevOps means Dev and Ops work together, not that we get rid of Ops people. Both teams are still needed but they collaborate more.

### Question 10
True or False: Elite DevOps performers deploy 208x more frequently than low performers with lower failure rates.

**Your Answer**: True

**Explanation**: The DORA research showed that elite companies deploy way more often but have fewer problems because they use automation and good practices.

## Part 3: Short Answer (2 points each)

### Question 11
Explain in 2-3 sentences WHY DevOps emerged. What was the business problem?

**Your Answer**:

DevOps emerged because companies needed to release software faster to stay competitive. The old way of doing things was too slow - deployments took months and often failed. Development and Operations teams didn't communicate well, which caused delays and problems.

### Question 12
A company deploys quarterly. Each deployment takes 8 hours and involves 5 people at $100/hour.
40% of deployments fail and require rollback (another 8 hours).

Calculate the annual deployment cost (labor only).

**Your Calculation**:

Deployments per year: 4
Successful: 60% = 2.4
Failed: 40% = 1.6

Cost per deployment: 8 hours × 5 people × $100 = $4,000
Cost per failed (with rollback): 16 hours × 5 people × $100 = $8,000

Annual cost:
(2.4 × $4,000) + (1.6 × $8,000)
= $9,600 + $12,800
= **$22,400**

### Question 13
What's the difference between "lead time" and "process time"? Why does this matter?

**Your Answer**:

Lead time is the total time from start to finish. Process time is how long you actually work on something. The difference is wait time. This matters because most of the time is usually spent waiting, not working. If we reduce wait time, we can deliver faster.

### Question 14
List 3 benefits of DevOps (one sentence each):

**Your Answer**:

1. Faster deployments - companies can release new features more quickly.
2. Fewer bugs - automation and testing catch problems before production.
3. Happier teams - less manual work and fewer emergencies means less stress.

### Question 15
Your manager says: "We don't have time to implement DevOps, we're too busy."

How would you respond? (3-4 sentences)

**Your Answer**:

I would explain that DevOps actually saves time in the long run. Yes, it takes time to set up initially, but once you automate things, you spend less time on manual work. The team is busy now because we're doing everything manually - DevOps will help reduce that workload. We can start small with one project to prove it works.

## Part 4: Scenario Analysis (3 points)

### Question 16

**Scenario**:
Company A and Company B both use Docker and Kubernetes.

**Company A**:
- Developers write code, throw it "over the wall" to ops
- Ops deploys containers but doesn't understand the application
- When production breaks, blame game starts
- Developers say "worked in my container"
- Ops says "your code crashed our cluster"

**Company B**:
- Developers and Ops jointly designed the container architecture
- Shared on-call rotation
- Blameless post-mortems after incidents
- Both teams use same monitoring tools
- Collaborative problem-solving

**Question**: Which company is "doing DevOps" and why? (4-5 sentences)

**Your Answer**:

Company B is doing DevOps because they have good collaboration between Dev and Ops. Company A is just using DevOps tools but they're not really doing DevOps - they still work in silos and blame each other. DevOps is about culture, not just tools. Company B shows this with their shared on-call and blameless post-mortems. They work together to solve problems instead of pointing fingers.

## Part 5: Application (5 points)

### Question 17

You're a new DevOps engineer at a bank. Current situation:
- Deployments: Once per month
- Manual deployment process: 50-page runbook
- Last 3 deployments failed
- Each incident costs $100k in lost revenue
- Developers frustrated by slow releases
- Operations burned out by weekend deployments

**Your Task**:
Write a 1-paragraph pitch to the CTO explaining why the bank should invest in DevOps. Include:
- The current problem/cost
- The proposed solution
- Expected benefits (specific!)
- One metric you'll use to measure success

**Your Answer**:

Our current deployment process is causing major problems and costing a lot of money. We deploy once per month, and the last 3 deployments failed costing $300k in lost revenue. The manual process takes 8 hours every time and burns out our team with weekend work. I propose we implement DevOps automation with CI/CD pipelines and automated testing. This will let us deploy more frequently with fewer failures. We can reduce deployment time to under an hour and deploy weekly instead of monthly. The investment would be around $300k but we'd save that within a year through fewer failures and better efficiency. We'll measure success by tracking deployment frequency - our goal is to go from monthly to weekly deployments within 6 months.

## Bonus Question (Optional, +2 points)

### Question 18

Research ONE real company's DevOps transformation (Amazon, Netflix, Etsy, Target, Capital One, etc.).

Summarize:
- What was their problem before DevOps?
- What specific changes did they make?
- What were the results?
- One lesson you learned from their story

**Your Answer**:

**Company**: Netflix

**Problem**: Netflix had a major database failure that caused 3 days of downtime. They realized their systems weren't reliable enough for streaming video to millions of customers.

**Changes Made**: They moved to AWS cloud, broke their application into microservices, and created automated deployment tools. They also created "Chaos Monkey" which randomly breaks things in production to test if the system can handle failures.

**Results**: Netflix now deploys thousands of times per day and has very high uptime. They can serve 200+ million subscribers reliably.

**Lesson Learned**: It's better to test for problems on purpose (like Chaos Monkey) than to be surprised when they happen. This seems scary but it actually makes systems more reliable.
