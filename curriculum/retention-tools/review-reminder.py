#!/usr/bin/env python3
"""
Spaced Repetition Review Reminder
Tracks module completion dates and reminds you when reviews are due
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Review schedule (days after completion)
REVIEW_SCHEDULE = {
    "Review 1": 3,
    "Review 2": 7,
    "Review 3": 14,
    "Review 4": 30,
    "Review 5": 60,
    "Review 6": 90,
}

def load_completion_data():
    """Load module completion dates from JSON file"""
    data_file = Path(__file__).parent / "completion_data.json"

    if not data_file.exists():
        return {}

    with open(data_file, 'r') as f:
        return json.load(f)

def save_completion_data(data):
    """Save module completion dates to JSON file"""
    data_file = Path(__file__).parent / "completion_data.json"

    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)

def add_module(module_num, module_name, completion_date):
    """Add a completed module"""
    data = load_completion_data()

    module_key = f"module_{module_num:02d}"
    data[module_key] = {
        "name": module_name,
        "completed": completion_date,
        "reviews": {}
    }

    save_completion_data(data)
    print(f"✓ Added Module {module_num}: {module_name}")
    print(f"  Completed: {completion_date}")
    print(f"\nReview schedule:")

    completion_dt = datetime.strptime(completion_date, "%Y-%m-%d")

    for review_name, days in REVIEW_SCHEDULE.items():
        review_date = completion_dt + timedelta(days=days)
        print(f"  {review_name} (Day {days}): {review_date.strftime('%Y-%m-%d')}")

def mark_review_complete(module_num, review_num, score, total):
    """Mark a review as completed"""
    data = load_completion_data()
    module_key = f"module_{module_num:02d}"

    if module_key not in data:
        print(f"Error: Module {module_num} not found. Add it first!")
        return

    review_key = f"review_{review_num}"
    data[module_key]["reviews"][review_key] = {
        "completed": datetime.now().strftime("%Y-%m-%d"),
        "score": score,
        "total": total,
        "percentage": round(score / total * 100, 1)
    }

    save_completion_data(data)

    percentage = round(score / total * 100, 1)
    status = "✓ Excellent" if percentage >= 90 else "⚠ Needs Review" if percentage < 80 else "✓ Good"

    print(f"\n{status}")
    print(f"Module {module_num}, Review {review_num}: {score}/{total} ({percentage}%)")

def check_due_reviews():
    """Check which reviews are due today or overdue"""
    data = load_completion_data()
    today = datetime.now()

    due_reviews = []
    upcoming_reviews = []

    for module_key, module_data in data.items():
        module_num = int(module_key.split('_')[1])
        completion_dt = datetime.strptime(module_data['completed'], "%Y-%m-%d")

        for review_name, days in REVIEW_SCHEDULE.items():
            review_date = completion_dt + timedelta(days=days)
            review_num = int(review_name.split()[1])
            review_key = f"review_{review_num}"

            # Skip if already completed
            if review_key in module_data.get('reviews', {}):
                continue

            days_until = (review_date - today).days

            if days_until <= 0:
                due_reviews.append({
                    "module": module_num,
                    "module_name": module_data['name'],
                    "review": review_name,
                    "review_num": review_num,
                    "days_overdue": abs(days_until)
                })
            elif days_until <= 3:
                upcoming_reviews.append({
                    "module": module_num,
                    "module_name": module_data['name'],
                    "review": review_name,
                    "review_num": review_num,
                    "days_until": days_until
                })

    # Display results
    print("\n" + "="*60)
    print("SPACED REPETITION REVIEW STATUS")
    print("="*60 + "\n")

    if due_reviews:
        print("⚠️  REVIEWS DUE OR OVERDUE:\n")
        for review in sorted(due_reviews, key=lambda x: x['days_overdue'], reverse=True):
            status = f"{review['days_overdue']} days overdue" if review['days_overdue'] > 0 else "DUE TODAY"
            print(f"  • Module {review['module']}: {review['module_name']}")
            print(f"    {review['review']} - {status}")
            print()
    else:
        print("✓ No overdue reviews!\n")

    if upcoming_reviews:
        print("📅 UPCOMING REVIEWS (Next 3 Days):\n")
        for review in sorted(upcoming_reviews, key=lambda x: x['days_until']):
            print(f"  • Module {review['module']}: {review['module_name']}")
            print(f"    {review['review']} - in {review['days_until']} day(s)")
            print()
    else:
        print("📅 No upcoming reviews in next 3 days\n")

    # Show review statistics
    print("\n" + "-"*60)
    print("RETENTION STATISTICS")
    print("-"*60 + "\n")

    for module_key, module_data in data.items():
        module_num = int(module_key.split('_')[1])
        reviews = module_data.get('reviews', {})

        if reviews:
            print(f"Module {module_num}: {module_data['name']}")

            total_reviews = len(reviews)
            avg_score = sum(r['percentage'] for r in reviews.values()) / total_reviews

            print(f"  Reviews completed: {total_reviews}/6")
            print(f"  Average retention: {avg_score:.1f}%")

            for review_key, review_data in sorted(reviews.items()):
                review_num = review_key.split('_')[1]
                print(f"    Review {review_num}: {review_data['score']}/{review_data['total']} ({review_data['percentage']}%)")

            print()

def show_summary():
    """Show summary of all modules and their status"""
    data = load_completion_data()

    if not data:
        print("\nNo modules tracked yet!")
        print("Add a module with: python review-reminder.py add <module_num> <module_name> <completion_date>")
        return

    print("\n" + "="*60)
    print("MODULE COMPLETION SUMMARY")
    print("="*60 + "\n")

    for module_key, module_data in sorted(data.items()):
        module_num = int(module_key.split('_')[1])
        reviews = module_data.get('reviews', {})
        reviews_done = len(reviews)

        print(f"Module {module_num}: {module_data['name']}")
        print(f"  Completed: {module_data['completed']}")
        print(f"  Reviews: {reviews_done}/6 complete")

        if reviews:
            avg_retention = sum(r['percentage'] for r in reviews.values()) / len(reviews)
            print(f"  Avg Retention: {avg_retention:.1f}%")

        print()

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Track spaced repetition reviews")
    parser.add_argument('command', choices=['add', 'review', 'check', 'summary'],
                       help="Command to execute")
    parser.add_argument('--module', type=int, help="Module number")
    parser.add_argument('--name', help="Module name")
    parser.add_argument('--date', help="Completion date (YYYY-MM-DD)")
    parser.add_argument('--review', type=int, help="Review number (1-6)")
    parser.add_argument('--score', type=int, help="Score achieved")
    parser.add_argument('--total', type=int, help="Total possible score")

    args = parser.parse_args()

    if args.command == 'add':
        if not all([args.module, args.name, args.date]):
            print("Error: Need --module, --name, and --date")
            print("Example: python review-reminder.py add --module 1 --name 'DevOps Fundamentals' --date 2025-11-16")
            return

        add_module(args.module, args.name, args.date)

    elif args.command == 'review':
        if not all([args.module, args.review, args.score, args.total]):
            print("Error: Need --module, --review, --score, and --total")
            print("Example: python review-reminder.py review --module 1 --review 1 --score 45 --total 50")
            return

        mark_review_complete(args.module, args.review, args.score, args.total)

    elif args.command == 'check':
        check_due_reviews()

    elif args.command == 'summary':
        show_summary()

if __name__ == "__main__":
    main()
