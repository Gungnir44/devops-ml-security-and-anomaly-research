# Automated Grading System

AI-powered grading system for DevOps curriculum quizzes, exercises, and projects.

## Features

- ✅ Automated grading using Claude or Gemini
- ✅ Detailed feedback on each answer/section
- ✅ Rubric-based scoring
- ✅ Grade reports with improvement suggestions
- ✅ Support for quizzes, exercises, and projects

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file:

```bash
# Use Claude (recommended)
ANTHROPIC_API_KEY=your_claude_api_key_here

# OR use Gemini
GOOGLE_API_KEY=your_gemini_api_key_here

# Choose which to use (claude or gemini)
GRADING_MODEL=claude
```

### 3. Submit Assignment for Grading

```bash
# Grade a quiz
python grade.py --type quiz --module 1 --file student-answers.md

# Grade an exercise
python grade.py --type exercise --module 1 --exercise 1 --folder exercise-01/

# Grade a project
python grade.py --type project --module 1 --folder project/
```

### 4. View Results

Results are saved to `grading-results/` with detailed feedback and scores.

## Directory Structure

```
grading-system/
├── grade.py                 # Main grading script
├── graders/
│   ├── quiz_grader.py      # Quiz grading logic
│   ├── exercise_grader.py  # Exercise grading logic
│   └── project_grader.py   # Project grading logic
├── rubrics/
│   ├── module-01-quiz.json     # Quiz rubric
│   ├── module-01-exercise.json # Exercise rubrics
│   └── module-01-project.json  # Project rubric
├── prompts/
│   ├── quiz_grading_prompt.txt
│   ├── exercise_grading_prompt.txt
│   └── project_grading_prompt.txt
├── grading-results/        # Generated feedback reports
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## How It Works

1. **Student submits** their work (quiz answers, exercise files, project)
2. **Script reads** the submission and appropriate rubric
3. **AI grades** the work against the rubric criteria
4. **Feedback generated** with scores and improvement suggestions
5. **Report saved** to grading-results/

## Example Output

```
========================================
Module 1 Quiz Grading Report
========================================
Student: Joshua
Submission Date: 2024-01-15

Overall Score: 17/20 (85%)
Status: PASSED ✓

Section Breakdown:
- Multiple Choice: 10/10 (100%)
- True/False: 4/5 (80%)
- Short Answer: 3/5 (60%)

Detailed Feedback:
----------------------------------------
Question 11: (1/2 points)
Your answer correctly identifies that DevOps emerged
due to slow deployment cycles. However, you didn't
mention the cultural issues (silos, blame culture).

Suggestion: Review Lesson 1, section on "Why This
Happened" for more context on organizational problems.
----------------------------------------

Strengths:
- Excellent understanding of DORA metrics
- Strong grasp of ROI calculations
- Good real-world examples

Areas for Improvement:
- Deepen understanding of cultural aspects
- Review the Three Ways concept
- Practice explaining "why" not just "what"

Recommended Next Steps:
1. Review Lesson 3 (Culture & Principles)
2. Retake questions 11, 14 for practice
3. Ready to proceed to exercises!
```

## Student Submission Format

### Quiz Submission

Create a file `quiz-answers.md`:

```markdown
# Module 1 Quiz Answers
**Student Name**: Your Name
**Date**: 2024-01-15

## Part 1: Multiple Choice

### Question 1
**Your Answer**: B

### Question 2
**Your Answer**: A

[... continue for all questions]
```

### Exercise Submission

Create a folder with all required files:

```
exercise-01/
├── part1-process-map.md
├── part2-lead-time-calculation.md
├── part3-bottleneck-analysis.md
└── part4-improvements.md
```

### Project Submission

Create a folder with all components:

```
project/
├── part1-current-state.md
├── part2-root-cause-analysis.md
├── part3-transformation-plan.md
├── part4-roi-calculation.md
├── part5-executive-presentation.pdf
├── part6-implementation-roadmap.md
└── part7-metrics-dashboard.md
```

## Grading Criteria

The AI grader evaluates based on:

### Accuracy
- Correct answers to factual questions
- Accurate calculations
- Proper use of terminology

### Depth
- Demonstrates understanding of "why"
- Provides examples and context
- Shows critical thinking

### Completeness
- All required sections present
- Calculations show work
- Explanations are thorough

### Professionalism
- Clear writing
- Proper formatting
- No major typos/errors

## API Usage & Costs

### Claude API (Recommended)
- Model: Claude 3.5 Sonnet
- Cost: ~$0.10-0.50 per assignment
- Speed: 30-60 seconds per grading

### Gemini API (Alternative)
- Model: Gemini 1.5 Pro
- Cost: ~$0.05-0.25 per assignment
- Speed: 20-40 seconds per grading

## Troubleshooting

### "API Key Not Found"
- Check your `.env` file exists
- Verify API key is correct
- Ensure `.env` is in grading-system/ directory

### "Rubric Not Found"
- Ensure rubric files exist in rubrics/ folder
- Check module number matches

### "Low Quality Grading"
- Claude generally provides better feedback
- Ensure rubric is detailed
- Check prompt quality

## Advanced Usage

### Custom Rubrics

Edit rubric JSON files to customize grading:

```json
{
  "question_1": {
    "points": 2,
    "answer": "B",
    "rationale": "DevOps emerged due to silos between Dev and Ops",
    "common_mistakes": [
      "Choosing A (too narrow)",
      "Not mentioning cultural issues"
    ]
  }
}
```

### Batch Grading

Grade multiple students:

```bash
python grade.py --batch --folder submissions/
```

### Regrade with Feedback

If student revises and resubmits:

```bash
python grade.py --type quiz --module 1 --file revised-answers.md --previous grading-results/report-001.json
```

## Tips for Students

1. **Show your work**: Especially for calculations
2. **Explain your reasoning**: Don't just give answers
3. **Use proper terminology**: From glossary
4. **Proofread**: AI can be strict on unclear writing
5. **Follow formats**: Use required file structures

## Tips for Instructors

1. **Review AI feedback**: AI isn't perfect, spot-check
2. **Customize rubrics**: Adjust for your standards
3. **Provide human touch**: Add personal comments to reports
4. **Update prompts**: Refine based on grading quality
5. **Track patterns**: Notice common mistakes across students

## Privacy & Security

- ✅ Student submissions are NOT stored on AI servers
- ✅ Only sent for grading, then discarded
- ✅ API keys stored in `.env` (git-ignored)
- ✅ Grading reports stored locally only

## License

MIT License - Use freely for educational purposes

## Support

Questions or issues? Create an issue in the repository.

---

**Ready to start grading? See the Setup Guide below.**
