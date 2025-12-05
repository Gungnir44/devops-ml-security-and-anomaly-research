# Module 2 Quiz: Linux & Git Fundamentals

**Total Points**: 20
**Passing Score**: 16/20 (80%)
**Time Limit**: 45 minutes
**Format**: Submit answers in markdown file named `your-name-module-02-quiz.md`

---

## Part 1: Multiple Choice (10 points - 2 each)

### Q1: Linux Filesystem [2 points]

What is the root directory in Linux?

A) `C:\`
B) `/`
C) `~`
D) `/root`

**Your Answer**:

**Explanation** (2-3 sentences):

---

### Q2: File Permissions [2 points]

What does the permission `755` mean?

A) Owner: rwx, Group: r-x, Others: r-x
B) Owner: rw-, Group: r--, Others: r--
C) Owner: r-x, Group: rwx, Others: r-x
D) Owner: rwx, Group: rwx, Others: rwx

**Your Answer**:

**Explanation**:

---

### Q3: Git Workflow [2 points]

What is the correct order for making changes in Git?

A) commit → add → push
B) add → commit → push
C) push → commit → add
D) commit → push → add

**Your Answer**:

**Explanation**:

---

### Q4: Linux Commands [2 points]

Which command shows real-time updates to a log file?

A) `cat -f logfile.txt`
B) `tail -f logfile.txt`
C) `less -f logfile.txt`
D) `head -f logfile.txt`

**Your Answer**:

**Explanation**:

---

### Q5: Git Branching [2 points]

What is the primary purpose of feature branches?

A) To backup code
B) To work on features without affecting main branch
C) To delete old code
D) To share code with others

**Your Answer**:

**Explanation**:

---

## Part 2: True/False (5 points - 1 each)

### Q6: Linux [1 point]

**True or False**: In Linux, everything is a file (including hardware devices).

**Your Answer**: TRUE / FALSE

**Explanation**:

---

### Q7: File Permissions [1 point]

**True or False**: The command `rm -rf /` is safe to run and will only delete user files.

**Your Answer**: TRUE / FALSE

**Explanation**:

---

### Q8: Git [1 point]

**True or False**: `git pull` is equivalent to `git fetch` + `git merge`.

**Your Answer**: TRUE / FALSE

**Explanation**:

---

### Q9: Linux Distributions [1 point]

**True or False**: Ubuntu and CentOS use the same package manager (apt).

**Your Answer**: TRUE / FALSE

**Explanation**:

---

### Q10: Git Merge Conflicts [1 point]

**True or False**: Merge conflicts occur when the same line is modified in different branches.

**Your Answer**: TRUE / FALSE

**Explanation**:

---

## Part 3: Short Answer (5 points - 1 each)

### Q11: Pipes and Redirection [1 point]

Explain the difference between `>` and `>>` when redirecting output.

**Your Answer**:

---

### Q12: Git vs. Traditional Backup [1 point]

List 2 advantages of Git over simply copying files to a backup folder.

**Your Answer**:
1.
2.

---

### Q13: Linux Permissions Calculation [1 point]

A file has permissions `-rw-r-----`. What is this in numeric format (e.g., 755)?

**Your Answer**:

**Show your work**:

---

### Q14: Finding Files [1 point]

Write a command to find all `.log` files in `/var/log` modified in the last 7 days.

**Your Answer**:
```bash

```

---

### Q15: Git Collaboration [1 point]

Describe the typical flow for contributing to a project using pull requests (3-4 steps).

**Your Answer**:

---

## Bonus Question (2 points)

### Q16: DevOps Application [2 points]

**Scenario**: You're troubleshooting a production web server. The website is returning 500 errors. Describe the Linux commands you would use to:
1. Check if the web server process is running
2. View the last 50 lines of the error log
3. Check disk space (server might be full)
4. Find which configuration files were recently modified

**Your Answer**:
```bash
# 1. Check process

# 2. View error log

# 3. Check disk space

# 4. Find modified configs

```

**Explanation** (why each command):

---

## Submission Instructions

1. Save your answers in a file named: `your-name-module-02-quiz.md`
2. Place in: `submissions/module-02/`
3. Grade using:
```bash
python ../grading-system/grade.py --type quiz --module 2 --file submissions/module-02/your-name-module-02-quiz.md
```

---

## Grading Rubric

| Section | Points | Criteria |
|---------|--------|----------|
| Multiple Choice | 10 | Correct answer (1pt) + Explanation (1pt) |
| True/False | 5 | Correct answer (0.5pt) + Explanation (0.5pt) |
| Short Answer | 5 | Accuracy, completeness, understanding |
| Bonus | 2 | Practical application, correct commands |
| **Total** | **22** | **Scaled to 20 points** |

**Passing**: 16/20 (80%)

Good luck! 🚀
