#!/usr/bin/env python3
"""Check if scheduled workflows ran recently."""

from datetime import datetime, timedelta
import requests
from pathlib import Path

# Get token
token_file = Path(__file__).parent / ".github_token"
if token_file.exists():
    with open(token_file, 'r') as f:
        token = f.read().strip()
else:
    print("No token found")
    exit(1)

headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/vnd.github+json',
}

# Get security-scanning workflow
url = 'https://api.github.com/repos/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows'
response = requests.get(url, headers=headers)

workflows = response.json().get('workflows', [])
security_workflow_id = None

for wf in workflows:
    if 'security-scanning.yml' in wf['path']:
        security_workflow_id = wf['id']
        print(f"Security Scanning Workflow: {wf['name']}")
        print(f"  ID: {security_workflow_id}")
        print(f"  State: {wf['state']}")
        break

if not security_workflow_id:
    print("Security scanning workflow not found")
    exit(1)

# Get recent runs
runs_url = f'https://api.github.com/repos/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/{security_workflow_id}/runs'
params = {'per_page': 20}
response = requests.get(runs_url, headers=headers, params=params)

runs = response.json().get('workflow_runs', [])

print(f"\nRecent Security Scanning Runs (last {len(runs)}):")
print("=" * 90)

last_24h = datetime.utcnow() - timedelta(hours=24)
scheduled_runs_last_24h = []

for run in runs:
    run_date = datetime.strptime(run['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    trigger = run['event']
    status = run['status']
    conclusion = run['conclusion'] or 'running'
    branch = run['head_branch']

    is_scheduled = trigger == 'schedule'
    is_last_24h = run_date > last_24h

    if is_last_24h and is_scheduled:
        scheduled_runs_last_24h.append(run)

    recent_marker = '[LAST 24H]' if is_last_24h else '          '
    trigger_marker = '[SCHEDULED]' if is_scheduled else f'[{trigger:9s}]'

    print(f"{recent_marker} {run_date.strftime('%Y-%m-%d %H:%M UTC')} | "
          f"{branch:10s} | {status:10s} | {conclusion:10s} | {trigger_marker}")

print("\n" + "=" * 90)
print(f"Summary:")
print(f"  Scheduled runs in last 24 hours: {len(scheduled_runs_last_24h)}")
print(f"  Total scheduled runs (all time): {sum(1 for r in runs if r['event'] == 'schedule')}")
print(f"  Total runs: {len(runs)}")

if scheduled_runs_last_24h:
    print(f"\n[OK] YES - Automated scan ran last night!")
    for run in scheduled_runs_last_24h:
        run_date = datetime.strptime(run['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        print(f"  - {run_date.strftime('%Y-%m-%d at %H:%M UTC')} on {run['head_branch']} branch")
        print(f"    Status: {run['conclusion'] or run['status']}")
        if run.get('artifacts_url'):
            print(f"    Artifacts: {run['artifacts_url']}")
else:
    print(f"\n[!] NO - No scheduled runs in last 24 hours")
    print(f"    Expected schedule: Daily at 2:00 AM UTC")
    print(f"    Current time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"    Next scheduled run: Today/Tomorrow at 2:00 AM UTC")
