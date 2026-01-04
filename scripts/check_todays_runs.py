#!/usr/bin/env python3
"""Check today's manually triggered workflow runs."""

import requests
from pathlib import Path
from datetime import datetime

# Load token
token = Path(__file__).parent / ".github_token"
token_str = token.read_text().strip()

headers = {
    'Authorization': f'Bearer {token_str}',
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28'
}

# Get all recent runs
url = 'https://api.github.com/repos/Gungnir44/devops-ml-security-and-anomaly-research/actions/runs?per_page=50'
response = requests.get(url, headers=headers, timeout=10)
runs = response.json().get('workflow_runs', [])

# Filter for today's manual triggers
today = datetime.utcnow().date()
today_manual = [r for r in runs if r['event'] == 'workflow_dispatch' and
                datetime.strptime(r['created_at'], '%Y-%m-%dT%H:%M:%SZ').date() == today]

print("TODAY'S MANUAL TRIGGERS:")
print("=" * 80)
if today_manual:
    for r in today_manual:
        print(f"Branch: {r['head_branch']:12} | Status: {r['status']:12} | "
              f"Conclusion: {r.get('conclusion', 'N/A'):10} | Created: {r['created_at']}")
else:
    print("No manual triggers found for today")

print()
print("LAST 10 RUNS (ALL TYPES):")
print("=" * 80)
for i, r in enumerate(runs[:10], 1):
    print(f"{i}. Branch: {r['head_branch']:12} | Event: {r['event']:18} | "
          f"Status: {r['status']:12} | Created: {r['created_at']}")
