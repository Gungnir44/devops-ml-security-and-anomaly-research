"""
Check detailed workflow run status for hardened branch
"""
import requests
import json
from pathlib import Path

def get_github_token():
    """Get GitHub token from file."""
    token_file = Path(__file__).parent / ".github_token"
    if token_file.exists():
        with open(token_file, 'r') as f:
            return f.read().strip()
    return None

def check_workflow_details():
    """Check detailed status of recent workflow runs."""
    token = get_github_token()
    if not token:
        print("No token found!")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # Get recent workflow runs for hardened branch
    url = "https://api.github.com/repos/Gungnir44/devops-ml-security-and-anomaly-research/actions/runs"
    params = {
        "branch": "hardened",
        "per_page": 5
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    print("=" * 80)
    print("RECENT WORKFLOW RUNS - HARDENED BRANCH")
    print("=" * 80)
    print()

    for run in data['workflow_runs']:
        print(f"Workflow: {run['name']}")
        print(f"  Status: {run['status']}")
        print(f"  Conclusion: {run.get('conclusion', 'N/A')}")
        print(f"  Created: {run['created_at']}")
        print(f"  Updated: {run['updated_at']}")
        print(f"  Run ID: {run['id']}")
        print(f"  HTML URL: {run['html_url']}")

        # Get jobs for this run
        jobs_url = run['jobs_url']
        jobs_response = requests.get(jobs_url, headers=headers)
        jobs_data = jobs_response.json()

        if 'jobs' in jobs_data:
            print(f"  Jobs:")
            for job in jobs_data['jobs']:
                print(f"    - {job['name']}: {job['status']} / {job.get('conclusion', 'N/A')}")
                if job.get('conclusion') == 'failure':
                    print(f"      URL: {job['html_url']}")

        print()

if __name__ == "__main__":
    check_workflow_details()
