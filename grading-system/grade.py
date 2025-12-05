#!/usr/bin/env python3
"""
Automated Grading System for DevOps Curriculum
Supports grading quizzes, exercises, and projects using AI (Claude or Gemini)
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

# Load environment variables
load_dotenv()

console = Console()

class AIGrader:
    """Base class for AI grading using Claude or Gemini"""

    def __init__(self, model_type=None):
        self.model_type = model_type or os.getenv('GRADING_MODEL', 'claude')

        if self.model_type == 'claude':
            try:
                import anthropic
                api_key = os.getenv('ANTHROPIC_API_KEY')
                if not api_key:
                    raise ValueError("ANTHROPIC_API_KEY not found in environment")
                self.client = anthropic.Anthropic(api_key=api_key)
                self.model = "claude-3-5-sonnet-20241022"
            except ImportError:
                console.print("[red]Error: anthropic package not installed. Run: pip install anthropic[/red]")
                sys.exit(1)

        elif self.model_type == 'gemini':
            try:
                import google.generativeai as genai
                api_key = os.getenv('GOOGLE_API_KEY')
                if not api_key:
                    raise ValueError("GOOGLE_API_KEY not found in environment")
                genai.configure(api_key=api_key)
                self.client = genai.GenerativeModel('gemini-2.5-flash')
            except ImportError:
                console.print("[red]Error: google-generativeai package not installed. Run: pip install google-generativeai[/red]")
                sys.exit(1)

        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

    def grade(self, prompt, submission_text, rubric_text):
        """Send grading request to AI"""

        full_prompt = f"""{prompt}

# RUBRIC
{rubric_text}

# STUDENT SUBMISSION
{submission_text}

Please provide grading in the following JSON format:
{{
    "overall_score": <points earned>,
    "max_score": <total possible points>,
    "percentage": <percentage score>,
    "passed": <true/false>,
    "section_scores": [
        {{
            "section": "Section Name",
            "score": <points>,
            "max": <total>,
            "feedback": "Detailed feedback..."
        }}
    ],
    "strengths": ["strength 1", "strength 2", ...],
    "areas_for_improvement": ["area 1", "area 2", ...],
    "recommendations": ["recommendation 1", "recommendation 2", ...],
    "detailed_feedback": "Overall narrative feedback..."
}}
"""

        try:
            if self.model_type == 'claude':
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4000,
                    messages=[
                        {"role": "user", "content": full_prompt}
                    ]
                )
                result_text = response.content[0].text

            elif self.model_type == 'gemini':
                response = self.client.generate_content(full_prompt)
                result_text = response.text

            # Extract JSON from response (AI might wrap it in markdown)
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()

            result = json.loads(result_text)
            return result

        except json.JSONDecodeError:
            console.print("[yellow]Warning: AI response was not valid JSON. Returning raw text.[/yellow]")
            return {
                "error": "Invalid JSON response",
                "raw_response": result_text
            }
        except Exception as e:
            console.print(f"[red]Error during grading: {str(e)}[/red]")
            return {
                "error": str(e)
            }


class QuizGrader:
    """Grade quizzes"""

    def __init__(self, ai_grader):
        self.ai_grader = ai_grader
        self.rubric_dir = Path(__file__).parent / "rubrics"
        self.prompt_dir = Path(__file__).parent / "prompts"

    def load_rubric(self, module_num):
        """Load quiz rubric for module"""
        rubric_path = self.rubric_dir / f"module-{module_num:02d}-quiz.json"

        if not rubric_path.exists():
            console.print(f"[yellow]Warning: Rubric not found at {rubric_path}[/yellow]")
            console.print("[yellow]Using generic grading...[/yellow]")
            return {}

        with open(rubric_path, 'r') as f:
            return json.load(f)

    def load_prompt(self):
        """Load quiz grading prompt"""
        prompt_path = self.prompt_dir / "quiz_grading_prompt.txt"

        if not prompt_path.exists():
            # Default prompt
            return """You are an expert DevOps instructor grading a student's quiz.
Evaluate each answer carefully against the rubric. Be fair but thorough.
Provide constructive feedback that helps the student learn."""

        with open(prompt_path, 'r') as f:
            return f.read()

    def grade(self, module_num, submission_file):
        """Grade a quiz submission"""

        # Load submission
        with open(submission_file, 'r', encoding='utf-8') as f:
            submission_text = f.read()

        # Load rubric and prompt
        rubric = self.load_rubric(module_num)
        prompt = self.load_prompt()

        # Grade with AI
        console.print(f"\n[cyan]Grading Module {module_num} quiz...[/cyan]")

        with console.status("[bold green]AI is grading your submission..."):
            result = self.ai_grader.grade(
                prompt=prompt,
                submission_text=submission_text,
                rubric_text=json.dumps(rubric, indent=2)
            )

        return result


class ExerciseGrader:
    """Grade exercises"""

    def __init__(self, ai_grader):
        self.ai_grader = ai_grader
        self.rubric_dir = Path(__file__).parent / "rubrics"
        self.prompt_dir = Path(__file__).parent / "prompts"

    def grade(self, module_num, exercise_num, submission_folder):
        """Grade an exercise submission"""

        submission_path = Path(submission_folder)

        if not submission_path.exists():
            console.print(f"[red]Error: Submission folder not found: {submission_folder}[/red]")
            return None

        # Read all files in submission
        submission_text = f"# Exercise {exercise_num} Submission\n\n"

        for file_path in sorted(submission_path.glob("*.md")):
            with open(file_path, 'r', encoding='utf-8') as f:
                submission_text += f"\n## File: {file_path.name}\n"
                submission_text += f.read()
                submission_text += "\n\n---\n\n"

        # Load rubric
        rubric_path = self.rubric_dir / f"module-{module_num:02d}-exercise-{exercise_num:02d}.json"

        if rubric_path.exists():
            with open(rubric_path, 'r') as f:
                rubric = json.load(f)
        else:
            console.print(f"[yellow]Warning: Rubric not found, using generic grading[/yellow]")
            rubric = {}

        # Load prompt
        prompt_path = self.prompt_dir / "exercise_grading_prompt.txt"
        if prompt_path.exists():
            with open(prompt_path, 'r') as f:
                prompt = f.read()
        else:
            prompt = "You are grading a DevOps exercise. Evaluate thoroughness, accuracy, and understanding."

        # Grade with AI
        console.print(f"\n[cyan]Grading Module {module_num}, Exercise {exercise_num}...[/cyan]")

        with console.status("[bold green]AI is grading your submission..."):
            result = self.ai_grader.grade(
                prompt=prompt,
                submission_text=submission_text,
                rubric_text=json.dumps(rubric, indent=2)
            )

        return result


class ProjectGrader:
    """Grade projects"""

    def __init__(self, ai_grader):
        self.ai_grader = ai_grader
        self.rubric_dir = Path(__file__).parent / "rubrics"
        self.prompt_dir = Path(__file__).parent / "prompts"

    def grade(self, module_num, submission_folder):
        """Grade a project submission"""

        submission_path = Path(submission_folder)

        if not submission_path.exists():
            console.print(f"[red]Error: Submission folder not found: {submission_folder}[/red]")
            return None

        # Read all files in submission
        submission_text = f"# Module {module_num} Project Submission\n\n"

        for file_path in sorted(submission_path.glob("*.md")):
            with open(file_path, 'r', encoding='utf-8') as f:
                submission_text += f"\n## File: {file_path.name}\n"
                submission_text += f.read()
                submission_text += "\n\n---\n\n"

        # Load rubric
        rubric_path = self.rubric_dir / f"module-{module_num:02d}-project.json"

        if rubric_path.exists():
            with open(rubric_path, 'r') as f:
                rubric = json.load(f)
        else:
            console.print(f"[yellow]Warning: Rubric not found, using generic grading[/yellow]")
            rubric = {}

        # Load prompt
        prompt_path = self.prompt_dir / "project_grading_prompt.txt"
        if prompt_path.exists():
            with open(prompt_path, 'r') as f:
                prompt = f.read()
        else:
            prompt = "You are grading a comprehensive DevOps project. Evaluate depth, professionalism, and practical application."

        # Grade with AI
        console.print(f"\n[cyan]Grading Module {module_num} Project...[/cyan]")

        with console.status("[bold green]AI is grading your submission..."):
            result = self.ai_grader.grade(
                prompt=prompt,
                submission_text=submission_text,
                rubric_text=json.dumps(rubric, indent=2)
            )

        return result


def save_report(result, output_dir, assignment_type, module_num):
    """Save grading report to file"""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_file = output_path / f"{assignment_type}-module{module_num:02d}-{timestamp}.json"

    with open(report_file, 'w') as f:
        json.dump(result, f, indent=2)

    # Also create a human-readable version
    readable_file = output_path / f"{assignment_type}-module{module_num:02d}-{timestamp}.txt"

    with open(readable_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write(f"Module {module_num} {assignment_type.title()} Grading Report\n")
        f.write("=" * 60 + "\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Score: {result.get('overall_score', 'N/A')}/{result.get('max_score', 'N/A')} ({result.get('percentage', 'N/A')}%)\n")
        f.write(f"Status: {'PASSED' if result.get('passed') else 'NEEDS IMPROVEMENT'}\n")
        f.write("\n")

        if 'section_scores' in result:
            f.write("Section Breakdown:\n")
            f.write("-" * 60 + "\n")
            for section in result['section_scores']:
                f.write(f"{section['section']}: {section['score']}/{section['max']}\n")
                f.write(f"  Feedback: {section['feedback']}\n\n")

        f.write("\nStrengths:\n")
        for strength in result.get('strengths', []):
            f.write(f"  • {strength}\n")

        f.write("\nAreas for Improvement:\n")
        for area in result.get('areas_for_improvement', []):
            f.write(f"  • {area}\n")

        f.write("\nRecommendations:\n")
        for rec in result.get('recommendations', []):
            f.write(f"  • {rec}\n")

        f.write("\nDetailed Feedback:\n")
        f.write("-" * 60 + "\n")
        f.write(result.get('detailed_feedback', 'No additional feedback provided.'))
        f.write("\n")

    return report_file, readable_file


def display_results(result):
    """Display grading results in terminal"""

    # Overall score panel
    score_text = f"{result.get('overall_score', 'N/A')}/{result.get('max_score', 'N/A')} ({result.get('percentage', 'N/A')}%)"
    status_text = "PASSED" if result.get('passed') else "NEEDS IMPROVEMENT"
    status_color = "green" if result.get('passed') else "yellow"

    console.print()
    console.print(Panel(
        f"[bold]{score_text}[/bold]\n[{status_color}]{status_text}[/{status_color}]",
        title="Overall Score",
        border_style="cyan"
    ))

    # Section scores table
    if 'section_scores' in result and result['section_scores']:
        table = Table(title="Section Breakdown", show_header=True, header_style="bold magenta")
        table.add_column("Section", style="cyan")
        table.add_column("Score", justify="right", style="green")
        table.add_column("Feedback", style="white")

        for section in result['section_scores']:
            table.add_row(
                section['section'],
                f"{section['score']}/{section['max']}",
                section['feedback'][:60] + "..." if len(section['feedback']) > 60 else section['feedback']
            )

        console.print()
        console.print(table)

    # Strengths
    if result.get('strengths'):
        console.print()
        console.print(Panel(
            "\n".join(f"• {s}" for s in result['strengths']),
            title="Strengths",
            border_style="green"
        ))

    # Areas for improvement
    if result.get('areas_for_improvement'):
        console.print()
        console.print(Panel(
            "\n".join(f"• {a}" for a in result['areas_for_improvement']),
            title="Areas for Improvement",
            border_style="yellow"
        ))

    # Recommendations
    if result.get('recommendations'):
        console.print()
        console.print(Panel(
            "\n".join(f"• {r}" for r in result['recommendations']),
            title="Recommendations",
            border_style="blue"
        ))


def main():
    parser = argparse.ArgumentParser(description="Grade DevOps curriculum assignments")
    parser.add_argument('--type', required=True, choices=['quiz', 'exercise', 'project'], help="Assignment type")
    parser.add_argument('--module', required=True, type=int, help="Module number")
    parser.add_argument('--exercise', type=int, help="Exercise number (for exercises)")
    parser.add_argument('--file', help="Submission file (for quizzes)")
    parser.add_argument('--folder', help="Submission folder (for exercises and projects)")
    parser.add_argument('--model', choices=['claude', 'gemini'], help="AI model to use (overrides .env)")
    parser.add_argument('--output', default='grading-results', help="Output directory for reports")

    args = parser.parse_args()

    # Initialize AI grader
    ai_grader = AIGrader(model_type=args.model)

    # Grade based on type
    result = None

    if args.type == 'quiz':
        if not args.file:
            console.print("[red]Error: --file required for quiz grading[/red]")
            sys.exit(1)

        grader = QuizGrader(ai_grader)
        result = grader.grade(args.module, args.file)

    elif args.type == 'exercise':
        if not args.exercise or not args.folder:
            console.print("[red]Error: --exercise and --folder required for exercise grading[/red]")
            sys.exit(1)

        grader = ExerciseGrader(ai_grader)
        result = grader.grade(args.module, args.exercise, args.folder)

    elif args.type == 'project':
        if not args.folder:
            console.print("[red]Error: --folder required for project grading[/red]")
            sys.exit(1)

        grader = ProjectGrader(ai_grader)
        result = grader.grade(args.module, args.folder)

    # Display and save results
    if result and 'error' not in result:
        display_results(result)

        report_file, readable_file = save_report(result, args.output, args.type, args.module)

        console.print()
        console.print(f"[green]Grading complete![/green]")
        console.print(f"[cyan]Report saved to:[/cyan]")
        console.print(f"  - {report_file}")
        console.print(f"  - {readable_file}")

    elif result and 'error' in result:
        console.print(f"[red]Error during grading: {result['error']}[/red]")
        if 'raw_response' in result:
            console.print("\n[yellow]Raw AI response:[/yellow]")
            console.print(result['raw_response'])


if __name__ == "__main__":
    main()
