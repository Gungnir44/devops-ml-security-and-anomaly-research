"""
Download GitHub Actions Artifacts from Hardened Branch

Downloads workflow artifacts from the hardened branch for ML feature comparison.
"""

import os
import sys
import zipfile
from pathlib import Path
from datetime import datetime
import requests
from typing import List, Dict

# GitHub API configuration
REPO_OWNER = "Gungnir44"
REPO_NAME = "devops-ml-security-and-anomaly-research"
BRANCH = "hardened"
OUTPUT_DIR = Path("C:/Users/joshu/Desktop/DevOps Project/research-data/hardened-branch/baseline-week-1")


def get_github_token() -> str:
    """Get GitHub token from environment or file."""
    # Try environment variable
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        return token

    # Try token file
    token_file = Path(__file__).parent / ".github_token"
    if token_file.exists():
        with open(token_file, 'r') as f:
            return f.read().strip()

    print("[!] GitHub token not found!")
    print("    Set GITHUB_TOKEN environment variable or create .github_token file")
    sys.exit(1)


def get_workflow_runs(token: str, branch: str = "hardened", per_page: int = 30) -> List[Dict]:
    """Get workflow runs for a specific branch."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    params = {
        "branch": branch,
        "per_page": per_page
    }

    print(f"[*] Fetching workflow runs for branch: {branch}")
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"[!] Error fetching workflow runs: {response.status_code}")
        print(f"    {response.text}")
        return []

    data = response.json()
    return data.get('workflow_runs', [])


def get_artifacts_for_run(token: str, run_id: int) -> List[Dict]:
    """Get artifacts for a specific workflow run."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}/artifacts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    data = response.json()
    return data.get('artifacts', [])


def download_artifact(token: str, artifact_url: str, output_path: Path) -> bool:
    """Download a single artifact."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(artifact_url, headers=headers, stream=True)

    if response.status_code != 200:
        return False

    # Save zip file
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return True


def extract_zip(zip_path: Path, extract_to: Path) -> bool:
    """Extract a zip file."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except Exception as e:
        print(f"[!] Error extracting {zip_path}: {e}")
        return False


def main():
    """Main download process."""
    print("=" * 80)
    print("Download Hardened Branch Artifacts")
    print("=" * 80)
    print()

    # Get GitHub token
    token = get_github_token()
    print(f"[+] GitHub token found: {token[:20]}...")
    print()

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[*] Output directory: {OUTPUT_DIR}")
    print()

    # Get workflow runs for hardened branch
    runs = get_workflow_runs(token, BRANCH)

    if not runs:
        print("[!] No workflow runs found for hardened branch")
        print("    The hardened branch may not have run any workflows yet")
        print()
        print("To trigger workflows:")
        print("  1. Push commits to hardened branch")
        print("  2. Manually trigger workflows on GitHub")
        sys.exit(0)

    print(f"[+] Found {len(runs)} workflow runs on hardened branch")
    print()

    # Group runs by workflow name
    workflow_groups = {}
    for run in runs:
        workflow_name = run['name']
        if workflow_name not in workflow_groups:
            workflow_groups[workflow_name] = []
        workflow_groups[workflow_name].append(run)

    print("Workflow runs by type:")
    for workflow_name, workflow_runs in workflow_groups.items():
        latest_run = workflow_runs[0]
        status = latest_run['status']
        conclusion = latest_run.get('conclusion', 'N/A')
        created_at = latest_run['created_at']

        status_symbol = "[OK]" if conclusion == "success" else "[FAIL]" if conclusion == "failure" else "[RUN]"
        print(f"  {status_symbol} {workflow_name}: {len(workflow_runs)} runs (latest: {conclusion} at {created_at})")
    print()

    # Download artifacts from all successful runs
    total_artifacts = 0
    downloaded_artifacts = 0

    for run in runs:
        workflow_name = run['name']
        run_id = run['id']
        conclusion = run.get('conclusion')

        # Skip failed or cancelled runs
        if conclusion not in ['success', None]:
            continue

        print(f"[*] Checking artifacts for: {workflow_name} (run #{run_id})")

        artifacts = get_artifacts_for_run(token, run_id)
        total_artifacts += len(artifacts)

        if not artifacts:
            print(f"    No artifacts found")
            continue

        print(f"    Found {len(artifacts)} artifacts")

        # Create workflow-specific directory
        workflow_dir = OUTPUT_DIR / workflow_name.replace(" ", "-").lower()
        workflow_dir.mkdir(parents=True, exist_ok=True)

        # Download each artifact
        for artifact in artifacts:
            artifact_name = artifact['name']
            artifact_url = artifact['archive_download_url']
            artifact_size = artifact['size_in_bytes']

            # Check if already downloaded
            zip_path = workflow_dir / f"{artifact_name}.zip"
            extract_path = workflow_dir / artifact_name

            if extract_path.exists():
                print(f"    [Skip] {artifact_name} (already extracted)")
                downloaded_artifacts += 1
                continue

            print(f"    [Download] {artifact_name} ({artifact_size / 1024:.1f} KB)")

            # Download
            if download_artifact(token, artifact_url, zip_path):
                print(f"    [Extract] {artifact_name}")
                if extract_zip(zip_path, extract_path):
                    # Remove zip after extraction
                    zip_path.unlink()
                    downloaded_artifacts += 1
                    print(f"    [OK] {artifact_name}")
                else:
                    print(f"    [ERROR] Failed to extract {artifact_name}")
            else:
                print(f"    [ERROR] Failed to download {artifact_name}")

        print()

    # Summary
    print("=" * 80)
    print("Download Complete!")
    print("=" * 80)
    print()
    print(f"Total artifacts found:      {total_artifacts}")
    print(f"Successfully downloaded:    {downloaded_artifacts}")
    print()
    print(f"Data saved to: {OUTPUT_DIR}")
    print()

    # Next steps
    print("Next steps:")
    print("  1. Extract features from hardened branch:")
    print(f"     cd ml-pipeline")
    print(f"     python extract_all_features.py --branch hardened")
    print()
    print("  2. Compare with main branch:")
    print(f"     python compare_branches.py output/features_main_branch.csv output/features_hardened.csv")
    print()

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[!] Download cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
