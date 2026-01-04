"""Check ALL workflow runs on hardened branch for any with artifacts"""
import requests
from pathlib import Path

def get_github_token():
    token_file = Path(__file__).parent / ".github_token"
    if token_file.exists():
        with open(token_file, 'r') as f:
            return f.read().strip()
    return None

def check_all_runs():
    token = get_github_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # Get ALL workflow runs for hardened branch
    url = "https://api.github.com/repos/Gungnir44/devops-ml-security-and-anomaly-research/actions/runs"
    params = {
        "branch": "hardened",
        "per_page": 100  # Get more runs
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    print(f"Total workflow runs on hardened branch: {len(data['workflow_runs'])}")
    print()

    successful_with_artifacts = []

    for run in data['workflow_runs']:
        if run.get('conclusion') == 'success':
            # Check for artifacts
            artifacts_url = run['artifacts_url']
            artifacts_response = requests.get(artifacts_url, headers=headers)
            artifacts_data = artifacts_response.json()

            artifact_count = len(artifacts_data.get('artifacts', []))

            if artifact_count > 0:
                successful_with_artifacts.append({
                    'name': run['name'],
                    'run_id': run['id'],
                    'created_at': run['created_at'],
                    'artifact_count': artifact_count,
                    'url': run['html_url']
                })

    print("=" * 80)
    print(f"SUCCESSFUL RUNS WITH ARTIFACTS: {len(successful_with_artifacts)}")
    print("=" * 80)
    print()

    if successful_with_artifacts:
        for run in successful_with_artifacts:
            print(f"Workflow: {run['name']}")
            print(f"  Run ID: {run['run_id']}")
            print(f"  Date: {run['created_at']}")
            print(f"  Artifacts: {run['artifact_count']}")
            print(f"  URL: {run['url']}")
            print()
    else:
        print("No successful runs with artifacts found on hardened branch.")

if __name__ == "__main__":
    check_all_runs()
