# Quick Setup Guide

Get the grading system running in 5 minutes!

## Step 1: Install Python Dependencies

```bash
cd "C:\Users\joshu\Desktop\DevOps Project\grading-system"
pip install -r requirements.txt
```

This installs:
- `anthropic` - Claude API client
- `google-generativeai` - Gemini API client
- `python-dotenv` - Environment variable management
- `rich` - Beautiful terminal output
- `click` - CLI argument parsing

## Step 2: Get an API Key

### Option A: Claude (Recommended)

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Go to "API Keys"
4. Create a new key
5. Copy the key (starts with `sk-ant-...`)

**Cost**: ~$0.10-0.50 per assignment graded
**Quality**: Best feedback quality

### Option B: Gemini (Free Tier Available)

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Create API key
4. Copy the key

**Cost**: Free tier available, then ~$0.05-0.25 per assignment
**Quality**: Good, but Claude typically gives better feedback

## Step 3: Configure Environment

```bash
# Copy example to .env
copy .env.example .env

# Edit .env in your text editor
notepad .env
```

Add your API key:

```bash
# If using Claude
GRADING_MODEL=claude
ANTHROPIC_API_KEY=sk-ant-your-key-here

# If using Gemini
GRADING_MODEL=gemini
GOOGLE_API_KEY=your-key-here
```

Save and close.

## Step 4: Test the Grading System

Let's create a sample quiz submission to test:

```bash
# Create test submission
mkdir test-submission
```

Create `test-submission/quiz-answers.md`:

```markdown
# Module 1 Quiz Answers
**Student Name**: Test Student
**Date**: 2024-01-15

## Part 1: Multiple Choice

### Question 1
**Your Answer**: B

### Question 2
**Your Answer**: A

### Question 3
**Your Answer**: C

### Question 4
**Your Answer**: A

### Question 5
**Your Answer**: B

## Part 2: True/False

### Question 6
**Your Answer**: False
**Explanation**: DevOps is primarily about culture and collaboration, not just buying tools like Jenkins and Docker.

### Question 7
**Your Answer**: False
**Explanation**: Automation eliminates repetitive toil, allowing people to focus on more valuable work like innovation and problem-solving.

### Question 8
**Your Answer**: True
**Explanation**: Blameless post-mortems focus on learning from failures and improving systems, not punishing individuals.

### Question 9
**Your Answer**: False
**Explanation**: DevOps means shared responsibility between Dev and Ops, not eliminating Operations roles entirely.

### Question 10
**Your Answer**: True
**Explanation**: Research shows elite performers deploy much more frequently with lower failure rates.

## Part 3: Short Answer

### Question 11
DevOps emerged because traditional IT had silos between development and operations teams. This caused slow release cycles (quarterly or yearly), manual error-prone processes, and inability to respond quickly to business needs. Companies needed to move faster to stay competitive.

### Question 12
**Your Calculation**:
- Deployments per year: 4
- Success rate: 60%, Failure rate: 40%
- Successful deployments: 4 × 0.6 = 2.4
- Failed deployments: 4 × 0.4 = 1.6

Cost per successful deployment:
8 hours × 5 people × $100/hour = $4,000

Cost per failed deployment (includes rollback):
16 hours × 5 people × $100/hour = $8,000

Annual cost:
(2.4 × $4,000) + (1.6 × $8,000) = $9,600 + $12,800 = $22,400

### Question 13
Lead time is the total time from when work starts until it reaches production. Process time is just the time spent actually working. The difference is wait time. This matters because in most organizations, 80-90% of lead time is spent waiting, not working, which represents waste and opportunity for improvement.
```

## Step 5: Run the Grader

```bash
python grade.py --type quiz --module 1 --file test-submission/quiz-answers.md
```

You should see:
- Rich formatted output in terminal
- Overall score and breakdown
- Detailed feedback
- Report saved to `grading-results/`

## Step 6: Review the Results

```bash
# View the human-readable report
notepad grading-results/quiz-module01-*.txt

# Or view JSON for programmatic access
notepad grading-results/quiz-module01-*.json
```

## Usage Examples

### Grade a Quiz
```bash
python grade.py --type quiz --module 1 --file student-answers.md
```

### Grade an Exercise
```bash
python grade.py --type exercise --module 1 --exercise 1 --folder exercise-01/
```

### Grade a Project
```bash
python grade.py --type project --module 1 --folder project-submission/
```

### Use Specific Model
```bash
python grade.py --type quiz --module 1 --file quiz.md --model gemini
```

### Custom Output Directory
```bash
python grade.py --type quiz --module 1 --file quiz.md --output my-grades/
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'anthropic'"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### "ANTHROPIC_API_KEY not found"

**Solution**: Check your .env file
```bash
# Make sure .env exists (not .env.example)
# Make sure API key is correct
# No quotes needed around the key
ANTHROPIC_API_KEY=sk-ant-your-actual-key
```

### "Invalid JSON response"

**Solution**: This occasionally happens with AI responses. Try again. If it persists:
- Check your API key is valid
- Try the other model (claude vs gemini)
- Check rubric file exists for that module

### "Rubric not found"

**Solution**: Create rubric file or let it use generic grading
```bash
# Rubrics are optional
# System will warn but continue with generic grading
# For best results, create rubric files
```

### Grading seems low quality

**Solution**:
- Claude generally gives better feedback than Gemini
- Make sure rubric file exists (provides grading criteria)
- Check prompt file is appropriate for assignment type
- Rubrics and prompts can be customized

## Tips for Best Results

1. **Student submissions should be complete**
   - All required sections present
   - Clear formatting
   - Calculations show work

2. **Use descriptive filenames**
   - `quiz-answers-john-smith.md`
   - Better than `submission.md`

3. **Review AI feedback**
   - AI isn't perfect
   - Spot-check grades
   - Add human comments if needed

4. **Customize rubrics**
   - Edit JSON files in `rubrics/`
   - Make criteria specific to your standards
   - Add examples of good answers

5. **Improve prompts**
   - Edit txt files in `prompts/`
   - Add specific guidance
   - Refine based on grading quality

## Next Steps

1. ✅ Test with sample submission (above)
2. ✅ Review generated feedback
3. ✅ Customize rubrics for your needs
4. ✅ Grade real student submissions
5. ✅ Iterate on prompts for better feedback

## Cost Management

### Claude Pricing
- Input: $3 / million tokens (~$0.003 per 1k tokens)
- Output: $15 / million tokens (~$0.015 per 1k tokens)
- Typical grading: 2k-5k tokens total
- **Cost per grading**: $0.10-0.50

### Gemini Pricing
- Free tier: 15 requests/minute, 1 million tokens/day
- After free tier: $0.035 / 1k tokens
- **Cost per grading**: Free (in tier) or $0.05-0.25

### Budget Tips
- Use Gemini free tier for testing
- Switch to Claude for production (better quality)
- Batch grade to maximize efficiency
- Cache common rubrics/prompts

## Support

Questions? Issues?
- Check README.md for full documentation
- Review existing rubrics/prompts for examples
- Create issue in repository

---

**You're ready to grade! 🎓**

Test with the sample above, then grade real student work.
