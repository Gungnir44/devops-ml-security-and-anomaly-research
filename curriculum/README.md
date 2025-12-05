# DevOps Learning Curriculum

## Welcome, Student!

This curriculum transforms the DevOps project into a **structured learning journey** where you'll understand WHY things work, not just HOW to make them work.

### Teaching Philosophy

**Theory Before Practice (60/40 Rule)**
- 60% understanding concepts, WHY they exist, real-world context
- 40% hands-on practice, building, breaking, fixing

**Progressive Complexity**
- Week 1-6: Foundation (Linux, Git, Python)
- Week 7-12: Automation (Docker, CI/CD)
- Week 13-18: Orchestration (IaC, Kubernetes)
- Week 19-27: Production (Cloud, Monitoring, Security)

**Learning By Doing**
- Every concept has hands-on exercises
- Build real projects, not toy examples
- Portfolio-ready work

### How This Works

#### Each Module Contains:

1. **Lessons** (`lessons/`): Theory with explanations
   - Lesson 1: Introduction & WHY
   - Lesson 2: Core Concepts
   - Lesson 3: Deep Dive
   - Lesson 4: Best Practices

2. **Exercises** (`exercises/`): Hands-on practice
   - Guided exercises with step-by-step instructions
   - Challenge exercises to test understanding
   - Real-world scenarios

3. **Assessments** (`assessments/`): Validate learning
   - Quiz (knowledge check)
   - Project (practical application)
   - Rubric (grading criteria)

4. **Resources** (`resources/`): Additional materials
   - Cheat sheets
   - Reference documentation
   - External links

#### Your Responsibilities:

1. **Read the lessons** (don't skip theory!)
2. **Complete all exercises**
3. **Take the quiz** (80% required to pass)
4. **Build the project** (submit for review)
5. **Ask questions** (understanding > completion speed)

#### Instructor (Me) Will:

1. **Explain concepts** (WHY before HOW)
2. **Review your work** (code, documentation, decisions)
3. **Provide feedback** (constructive, actionable)
4. **Answer questions** (no question is "dumb")
5. **Adjust pace** (based on your progress)

### 🧠 Making Knowledge Stick: The Retention System

**The Problem**: Without reinforcement, you'll forget 80% of what you learn within 1 month.

**The Solution**: A science-backed retention system using spaced repetition, active recall, and deliberate practice.

#### Retention Tools (See `retention-tools/`)

1. **Flashcards** - 50 cards per module for daily review
2. **Spaced Repetition Tracker** - Automated review schedule (Day 3, 7, 14, 30, 60, 90)
3. **Weekly Reflection Journal** - Track learning, identify gaps, connect concepts
4. **One-Page Summaries** - Test understanding, create quick references
5. **Review Reminder Script** - Never miss a review session

#### Daily Commitment (15 minutes)
- Review flashcards from current + past modules
- Quick mental recall of yesterday's concepts

#### Weekly Commitment (60 minutes)
- Saturday: Comprehensive review + cumulative quiz
- Sunday: Reflection journal + plan next week

#### Result
- **90%+ long-term retention** (vs. 20% without this system)
- Can explain concepts months later without looking at notes
- Apply knowledge to new situations confidently

**📖 Read**: [`RETENTION-SYSTEM.md`](RETENTION-SYSTEM.md) for full details
**🛠️ Tools**: [`retention-tools/README.md`](retention-tools/README.md) for practical guides

### Module Overview

| Module | Topic | Duration | Deliverable |
|--------|-------|----------|-------------|
| 1 | DevOps Fundamentals | 2 weeks | Process analysis |
| 2 | Linux & Git | 2 weeks | Git workflow demo |
| 3 | Python Scripting | 2 weeks | Health monitor |
| **Checkpoint 1** | **Foundation Complete** | | **Automated monitoring** |
| 4 | Docker Containerization | 3 weeks | Multi-container app |
| 5 | CI/CD Pipelines | 3 weeks | Automated pipeline |
| 6 | Infrastructure as Code | 3 weeks | Terraform + Ansible |
| **Checkpoint 2** | **Automation Complete** | | **Full CI/CD** |
| 7 | Kubernetes | 3 weeks | K8s deployment |
| 8 | Cloud Deployment | 3 weeks | AWS/Azure app |
| 9 | Monitoring & Alerting | 3 weeks | Production monitoring |
| **Checkpoint 3** | **Orchestration Complete** | | **Cloud-native app** |
| 10 | DevSecOps | 3 weeks | Secure application |
| **Checkpoint 4** | **Production Complete** | | **Enterprise-ready** |
| Capstone | E-Commerce Platform | 3 weeks | Full-stack project |

### Getting Started

#### Prerequisites:
- **Computer**: Windows/Mac/Linux with 8GB+ RAM
- **Mindset**: Curiosity, persistence, willingness to fail and learn
- **Time**: 10-15 hours/week

#### Step 1: Environment Setup
```bash
# Check prerequisite installations
python --version  # 3.9+
git --version     # 2.0+
docker --version  # 20.0+

# Clone the project
cd "C:\Users\joshu\Desktop\DevOps Project"

# You're ready!
```

#### Step 2: Start Module 1
```bash
cd curriculum/module-01-devops-fundamentals
# Read: lessons/lesson-01-introduction.md
# Then: exercises/exercise-01-environment-setup.md
```

### How to Submit Work

#### For Each Module:

1. **Complete all exercises**
   - Create branch: `module-XX-yourname`
   - Commit your work with clear messages
   - Push to GitHub

2. **Take the quiz**
   - Open: `assessments/quiz.md`
   - Answer in: `assessments/your-answers.md`
   - Commit answers

3. **Build the project**
   - Follow: `assessments/project.md`
   - Document your decisions
   - Commit code + documentation

4. **Submit for review**
   - Create pull request
   - Tag instructor: `@instructor` (that's me!)
   - Wait for feedback

### Grading Rubric

#### Each Module Graded On:

- **Understanding** (40%): Quiz score, explanations in code
- **Implementation** (40%): Working code, best practices
- **Documentation** (20%): Clear README, comments, decisions

#### Passing Criteria:
- **Quiz**: 80%+ correct
- **Project**: Meets all requirements
- **Code Quality**: Follows best practices
- **Documentation**: Complete and clear

### Support & Communication

#### When You're Stuck:

1. **Try for 30 minutes** (Google, documentation, debugging)
2. **Document what you tried** (helps me help you)
3. **Ask specific questions** ("Why does X happen?" vs "It doesn't work")
4. **Share error messages** (full stack trace)

#### Response Time:
- Questions: Within 24 hours
- Code reviews: Within 48 hours
- Emergency help: Tag with [URGENT]

### Success Tips

1. **Don't rush** - Understanding > speed
2. **Take notes** - Write down key concepts
3. **Experiment** - Break things, fix them, learn
4. **Read error messages** - They're trying to help
5. **Google strategically** - "How does X work?" not "X code example"
6. **Join communities** - r/devops, CNCF Slack
7. **Build daily** - Consistency > cramming

### Ready to Begin?

**Next Step**: Open `module-01-devops-fundamentals/README.md` and start Lesson 1!

---

**Remember**: The goal isn't to memorize commands. It's to **understand systems**, **automate toil**, and **deliver value** to businesses.

Let's build something awesome! 🚀
