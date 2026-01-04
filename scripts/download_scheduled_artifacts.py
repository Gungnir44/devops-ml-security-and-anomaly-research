#!/usr/bin/env python3
"""Download artifacts from scheduled workflow runs."""

import os
import sys
import requests
import zipfile
from pathlib import Path
from datetime import datetime

# Configuration
REPO = "Gungnir44/devops-ml-security-and-anomaly-research"
token_file = Path(__file__).parent / ".github_token"
TOKEN = token_file.read_text().strip()

HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28'
}

def get_scheduled_runs():
    """Get recent scheduled workflow runs."""
    url = f'https://api.github.com/repos/{REPO}/actions/runs?per_page=50'
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    runs = response.json().get('workflow_runs', [])
    scheduled = [r for r in runs if r['event'] == 'schedule' and 'Security Scanning' in r['name']]

    return scheduled[:5]  # Last 5 scheduled runs

def download_artifact(artifact_url, download_path):
    """Download and extract artifact."""
    response = requests.get(artifact_url, headers=HEADERS, timeout=30, stream=True)
    response.raise_for_status()

    zip_path = download_path.with_suffix('.zip')
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Extract
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(download_path.parent)

    zip_path.unlink()  # Remove zip file
    return True

def main():
    """Main execution."""
    print("=" * 80)
    print("Downloading Artifacts from Scheduled Runs")
    print("=" * 80)
    print()

    runs = get_scheduled_runs()
    print(f"Found {len(runs)} scheduled runs")
    print()

    base_dir = Path(__file__).parent.parent / "research-data" / "time-series"
    base_dir.mkdir(parents=True, exist_ok=True)

    total_downloaded = 0

    for run in runs:
        run_date = run['created_at'][:10]
        branch = run['head_branch']
        run_id = run['id']

        print(f"[{run_date}] Branch: {branch} | Run ID: {run_id}")

        # Get artifacts for this run
        artifacts_url = f"https://api.github.com/repos/{REPO}/actions/runs/{run_id}/artifacts"
        response = requests.get(artifacts_url, headers=HEADERS, timeout=10)
        artifacts = response.json().get('artifacts', [])

        print(f"  Found {len(artifacts)} artifacts")

        if not artifacts:
            print()
            continue

        # Create directory for this date/branch
        date_dir = base_dir / run_date / branch
        date_dir.mkdir(parents=True, exist_ok=True)

        for artifact in artifacts:
            name = artifact['name']
            download_url = artifact['archive_download_url']
            artifact_path = date_dir / name

            if artifact_path.exists():
                print(f"  [Skip] {name} (already exists)")
                continue

            print(f"  [Download] {name}")
            try:
                download_artifact(download_url, artifact_path)
                print(f"  [OK] {name}")
                total_downloaded += 1
            except Exception as e:
                print(f"  [Failed] {name}: {e}")

        print()

    print("=" * 80)
    print(f"Downloaded {total_downloaded} new artifacts")
    print("=" * 80)

if __name__ == "__main__":
    main()
