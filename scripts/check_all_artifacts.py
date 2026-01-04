"""Check ALL workflow runs (including failed) for artifacts"""
import requests
from pathlib import Path

def get_github_token():
    token_file = Path(__file__).parent / ".github_token"
    if token_file.exists():
        with open(token_file, 'r') as f:
            return f.read().strip()
    return None

def check_all_artifacts():
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
        "per_page": 20
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    print(f"Checking {len(data['workflow_runs'])} workflow runs...")
    print()

    runs_with_artifacts = []

    for run in data['workflow_runs']:
        # Check for artifacts regardless of conclusion
        artifacts_url = run['artifacts_url']
        artifacts_response = requests.get(artifacts_url, headers=headers)
        artifacts_data = artifacts_response.json()

        artifact_count = len(artifacts_data.get('artifacts', []))

        if artifact_count > 0:
            runs_with_artifacts.append({
                'name': run['name'],
                'run_id': run['id'],
                'conclusion': run.get('conclusion', 'N/A'),
                'created_at': run['created_at'],
                'artifact_count': artifact_count,
                'artifacts': artifacts_data.get('artifacts', [])
            })

    print("=" * 80)
    print(f"RUNS WITH ARTIFACTS (including failed): {len(runs_with_artifacts)}")
    print("=" * 80)
    print()

    if runs_with_artifacts:
        for run in runs_with_artifacts:
            print(f"Workflow: {run['name']}")
            print(f"  Status: {run['conclusion']}")
            print(f"  Run ID: {run['run_id']}")
            print(f"  Date: {run['created_at']}")
            print(f"  Artifacts: {run['artifact_count']}")
            for artifact in run['artifacts']:
                size_mb = artifact['size_in_bytes'] / 1024 / 1024
                print(f"    - {artifact['name']} ({size_mb:.2f} MB)")
            print()
    else:
        print("No artifacts found in any runs.")

if __name__ == "__main__":
    check_all_artifacts()
