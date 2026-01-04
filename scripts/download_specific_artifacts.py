"""Download specific artifacts from workflow runs"""
import requests
import zipfile
from pathlib import Path

def get_github_token():
    token_file = Path(__file__).parent / ".github_token"
    if token_file.exists():
        with open(token_file, 'r') as f:
            return f.read().strip()
    return None

def download_artifact(token, artifact_url, output_path):
    """Download a single artifact."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(artifact_url, headers=headers, stream=True)

    if response.status_code != 200:
        return False

    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return True

def extract_zip(zip_path, extract_to):
    """Extract a zip file."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except Exception as e:
        print(f"Error extracting {zip_path}: {e}")
        return False

def download_from_runs():
    token = get_github_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    output_dir = Path("research-data/hardened-branch/github-actions")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Most recent run with artifacts
    run_ids = [19998803662, 19998803656]  # CI - Test and Lint, Frontend CI/CD

    total_downloaded = 0

    for run_id in run_ids:
        url = f"https://api.github.com/repos/Gungnir44/devops-ml-security-and-anomaly-research/actions/runs/{run_id}/artifacts"
        response = requests.get(url, headers=headers)
        artifacts = response.json().get('artifacts', [])

        print(f"Run {run_id}: Found {len(artifacts)} artifacts")

        for artifact in artifacts:
            artifact_name = artifact['name']
            artifact_url = artifact['archive_download_url']

            zip_path = output_dir / f"{artifact_name}.zip"
            extract_path = output_dir / artifact_name

            if extract_path.exists():
                print(f"  [Skip] {artifact_name} (already exists)")
                continue

            print(f"  [Download] {artifact_name}")
            if download_artifact(token, artifact_url, zip_path):
                print(f"  [Extract] {artifact_name}")
                if extract_zip(zip_path, extract_path):
                    zip_path.unlink()
                    total_downloaded += 1
                    print(f"  [OK] {artifact_name}")

    print()
    print(f"Downloaded {total_downloaded} artifacts to: {output_dir}")

if __name__ == "__main__":
    download_from_runs()
