#!/usr/bin/env python3
"""
Manually Trigger Security Scanning Workflow
============================================

This script manually triggers the security-scanning workflow to:
1. Test workflow functionality
2. Activate GitHub Actions scheduled runs (helps "wake up" the scheduler)
3. Generate immediate security scan data

Usage:
    python trigger_security_scan.py [--branch main]
"""

import requests
from pathlib import Path
import sys
import argparse


def get_github_token():
    """Get GitHub token from .github_token file."""
    token_file = Path(__file__).parent / ".github_token"

    if not token_file.exists():
        print("[!] Error: No .github_token file found")
        print(f"    Expected location: {token_file}")
        print("\nCreate the file with your GitHub Personal Access Token:")
        print("  1. Go to: https://github.com/settings/tokens")
        print("  2. Create token with 'workflow' and 'repo' scopes")
        print("  3. Save token to .github_token file")
        return None

    with open(token_file, 'r') as f:
        token = f.read().strip()

    return token


def trigger_workflow(token: str, branch: str = "main"):
    """Trigger the security-scanning workflow."""

    print("=" * 80)
    print("Manual Workflow Trigger")
    print("=" * 80)

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    repo = "Gungnir44/devops-ml-security-and-anomaly-research"
    workflow_file = "security-scanning.yml"

    # Trigger workflow
    url = f'https://api.github.com/repos/{repo}/actions/workflows/{workflow_file}/dispatches'

    payload = {
        'ref': branch,
        'inputs': {}
    }

    print(f"\nTriggering workflow: {workflow_file}")
    print(f"Branch: {branch}")
    print(f"Repository: {repo}")

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 204:
        print("\n[OK] Workflow triggered successfully!")
        print("\nWhat happens next:")
        print("  1. Workflow will start running within ~30 seconds")
        print("  2. Check status: https://github.com/{}/actions".format(repo))
        print("  3. This manual trigger may help activate scheduled runs")
        print("\nWhy this helps:")
        print("  - GitHub Actions scheduled workflows sometimes need 'activation'")
        print("  - Running the workflow manually can wake up the scheduler")
        print("  - Scheduled runs (2 AM UTC daily) should start working within 24-48 hours")
        return True
    else:
        print(f"\n[!] Error triggering workflow (HTTP {response.status_code})")
        print(f"Response: {response.text}")

        if response.status_code == 404:
            print("\nPossible issues:")
            print("  - Workflow file name incorrect")
            print("  - Repository name incorrect")
            print("  - Token doesn't have 'workflow' scope")
        elif response.status_code == 403:
            print("\nToken permission issue:")
            print("  - Token needs 'workflow' and 'repo' scopes")
            print("  - Regenerate token with correct permissions")

        return False


def main():
    parser = argparse.ArgumentParser(
        description="Manually trigger security scanning workflow"
    )
    parser.add_argument(
        '--branch',
        type=str,
        default='main',
        help='Branch to run workflow on (default: main)'
    )

    args = parser.parse_args()

    # Get token
    token = get_github_token()
    if not token:
        sys.exit(1)

    # Trigger workflow
    success = trigger_workflow(token, args.branch)

    if success:
        print("\n[OK] Done! Check GitHub Actions page for workflow run.")
    else:
        print("\n[!] Failed to trigger workflow")
        sys.exit(1)


if __name__ == "__main__":
    main()
