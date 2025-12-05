# Module 1 Quiz: DevOps Fundamentals

**Instructions**:
- Answer all questions in a new file: `assessments/your-answers.md`
- Be honest (no Googling during the quiz - test your understanding)
- Passing score: 80% (16/20 points)
- You can retake after reviewing lessons

**Time Limit**: 45 minutes

## Part 1: Multiple Choice (2 points each)

### Question 1
What problem led to the emergence of DevOps?

A) Lack of programming languages
B) Silos between development and operations causing slow, error-prone releases
C) Too many cloud providers
D) Insufficient hardware

**Your Answer**:

### Question 2
What does "Continuous Integration" mean?

A) Developers integrate code into a shared repository frequently (multiple times per day)
B) Integration happens once per quarter
C) Integration only happens in production
D) Continuous meetings about integration

**Your Answer**:

### Question 3
In traditional IT (pre-DevOps), what was the typical deployment frequency?

A) Multiple times per day
B) Daily
C) Quarterly or yearly
D) Hourly

**Your Answer**:

### Question 4
What is "toil" in DevOps context?

A) Manual, repetitive, automatable work that doesn't add value
B) All work is toil
C) Only difficult work
D) Work that ops team does

**Your Answer**:

### Question 5
What do the "three pillars" of DevOps refer to?

A) Docker, Kubernetes, Terraform
B) People, Process, Technology
C) AWS, Azure, GCP
D) Dev, Ops, QA

**Your Answer**:

## Part 2: True/False (1 point each)

### Question 6
True or False: DevOps is primarily about buying the right tools (Jenkins, Docker, Kubernetes).

**Your Answer**:
**Explanation** (required):

### Question 7
True or False: Automation eliminates jobs, which is why operations teams resist DevOps.

**Your Answer**:
**Explanation**:

### Question 8
True or False: In blameless post-mortems, the goal is to learn from failures, not punish individuals.

**Your Answer**:
**Explanation**:

### Question 9
True or False: DevOps means Development team owns Operations tasks, so we don't need Ops engineers.

**Your Answer**:
**Explanation**:

### Question 10
True or False: Elite DevOps performers deploy 208x more frequently than low performers with lower failure rates.

**Your Answer**:
**Explanation**:

## Part 3: Short Answer (2 points each)

### Question 11
Explain in 2-3 sentences WHY DevOps emerged. What was the business problem?

**Your Answer**:

### Question 12
A company deploys quarterly. Each deployment takes 8 hours and involves 5 people at $100/hour.
40% of deployments fail and require rollback (another 8 hours).

Calculate the annual deployment cost (labor only).

**Your Calculation**:

### Question 13
What's the difference between "lead time" and "process time"? Why does this matter?

**Your Answer**:

### Question 14
List 3 benefits of DevOps (one sentence each):

1.
2.
3.

### Question 15
Your manager says: "We don't have time to implement DevOps, we're too busy."

How would you respond? (3-4 sentences)

**Your Answer**:

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

## Bonus Question (Optional, +2 points)

### Question 18

Research ONE real company's DevOps transformation (Amazon, Netflix, Etsy, Target, Capital One, etc.).

Summarize:
- What was their problem before DevOps?
- What specific changes did they make?
- What were the results?
- One lesson you learned from their story

**Your Answer**:

---

## Submission Instructions

1. Create file: `assessments/quiz-answers-[yourname].md`
2. Copy questions and add your answers
3. Commit to your branch
4. Push to GitHub
5. Tag instructor in PR

## Grading

**Total Points**: 20 (+ 2 bonus)
**Passing**: 16/20 (80%)

**Grading Rubric**:
- Multiple choice: Correct = 2 pts, Incorrect = 0 pts
- True/False: Correct with explanation = 1 pt
- Short answer: Complete, accurate = 2 pts, Partial = 1 pt
- Scenario: Demonstrates understanding = 3 pts
- Application: Practical, specific = 5 pts

## After the Quiz

**If you passed (80%+)**:
- Great! Review any mistakes
- Move to the Module 1 Project
- Take learnings forward

**If you didn't pass**:
- No problem! This is learning
- Review the lessons for questions you missed
- Focus on understanding WHY, not memorizing answers
- Retake when ready

**Common Mistakes to Avoid**:
- Rushing through questions
- Not reading carefully (e.g., "True or FALSE" questions)
- Vague answers (be specific!)
- Not using examples from lessons

## Why This Quiz Matters

This isn't just testing memorization. It's ensuring you understand:
- **WHY** DevOps exists (problems it solves)
- **Business value** (not just cool tech)
- **Culture** (not just tools)
- **Metrics** (how to measure success)

These concepts will come up again and again throughout the curriculum. Solid foundation here = easier learning later!

---

**Good luck! Remember: The goal is understanding, not a perfect score.**
