# Module 1 Quiz Answers
**Student Name**: Charlie Davis (Needs Work)
**Date**: 2024-01-15

## Part 1: Multiple Choice (2 points each)

### Question 1
What problem led to the emergence of DevOps?

**Your Answer**: A

### Question 2
What does "Continuous Integration" mean?

**Your Answer**: A

### Question 3
In traditional IT (pre-DevOps), what was the typical deployment frequency?

**Your Answer**: B

### Question 4
What is "toil" in DevOps context?

**Your Answer**: D

### Question 5
What do the "three pillars" of DevOps refer to?

**Your Answer**: A

## Part 2: True/False (1 point each)

### Question 6
True or False: DevOps is primarily about buying the right tools (Jenkins, Docker, Kubernetes).

**Your Answer**: True

**Explanation**: You need good tools to do DevOps properly.

### Question 7
True or False: Automation eliminates jobs, which is why operations teams resist DevOps.

**Your Answer**: True

**Explanation**: If you automate everything, you don't need as many people.

### Question 8
True or False: In blameless post-mortems, the goal is to learn from failures, not punish individuals.

**Your Answer**: True

**Explanation**: You don't blame people in post-mortems.

### Question 9
True or False: DevOps means Development team owns Operations tasks, so we don't need Ops engineers.

**Your Answer**: True

**Explanation**: DevOps means developers do everything themselves.

### Question 10
True or False: Elite DevOps performers deploy 208x more frequently than low performers with lower failure rates.

**Your Answer**: False

**Explanation**: If you deploy more often, you'll have more failures. That's just common sense.

## Part 3: Short Answer (2 points each)

### Question 11
Explain in 2-3 sentences WHY DevOps emerged. What was the business problem?

**Your Answer**:

DevOps emerged because Docker and cloud computing became popular. Companies wanted to use modern technology instead of old servers. DevOps is the way to use these new tools.

### Question 12
A company deploys quarterly. Each deployment takes 8 hours and involves 5 people at $100/hour.
40% of deployments fail and require rollback (another 8 hours).

Calculate the annual deployment cost (labor only).

**Your Calculation**:

4 deployments × 8 hours × 5 people × $100/hour = $16,000

### Question 13
What's the difference between "lead time" and "process time"? Why does this matter?

**Your Answer**:

Lead time is how long it takes for a leader to make decisions. Process time is how long the process takes. This matters because leaders need to make decisions quickly.

### Question 14
List 3 benefits of DevOps (one sentence each):

**Your Answer**:

1. You get to use cool tools like Docker and Kubernetes.
2. It looks good on your resume.
3. Everyone is doing it so we should too.

### Question 15
Your manager says: "We don't have time to implement DevOps, we're too busy."

How would you respond? (3-4 sentences)

**Your Answer**:

I would say that we need to make time because DevOps is important. All the big companies are doing DevOps. If we don't do DevOps, we'll fall behind. We should just start using the tools.

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

Both companies are doing DevOps because they're both using Docker and Kubernetes. Company A might need to improve their processes but they have the right tools. Company B seems to be doing it better because they work together more. But really if you have containers and Kubernetes, you're doing DevOps. The tools are what matter most.

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

We should implement DevOps because it's what modern companies do. We need to get Jenkins, Docker, and Kubernetes set up. This will make everything faster and better. Other banks are doing DevOps so we need to do it too or we'll look old fashioned. It won't cost much and we'll be able to deploy more often. We should measure how many containers we're running to track success.

## Bonus Question (Optional, +2 points)

### Question 18

*(Not attempted)*
