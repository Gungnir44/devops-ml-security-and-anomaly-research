"""Get GitHub Actions job logs"""
import requests
from pathlib import Path

def get_github_token():
    token_file = Path(__file__).parent / ".github_token"
    if token_file.exists():
        with open(token_file, 'r') as f:
            return f.read().strip()
    return None

def get_job_logs(job_id):
    """Get logs for a specific job."""
    token = get_github_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    url = f"https://api.github.com/repos/Gungnir44/devops-ml-security-and-anomaly-research/actions/jobs/{job_id}/logs"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python get_job_logs.py <job_id>")
        sys.exit(1)

    job_id = sys.argv[1]
    logs = get_job_logs(job_id)

    # Write to file instead of printing to avoid encoding issues
    output_file = Path(__file__).parent / f"job_{job_id}_logs.txt"
    with open(output_file, 'w', encoding='utf-8', errors='replace') as f:
        f.write(logs)
    print(f"Logs saved to: {output_file}")
