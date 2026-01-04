#!/usr/bin/env python3
"""
Automatic Collection After Manual Trigger
==========================================

After you manually trigger workflows for both branches,
run this script to:
1. Monitor workflow completion
2. Download all artifacts
3. Organize everything
4. Extract features

Complete automation!
"""

import os
import sys
import json
import time
import requests
import subprocess
from pathlib import Path
from datetime import datetime


class AutoCollector:
    """Automatic workflow monitoring and data collection."""

    def __init__(self):
        self.repo = "Gungnir44/devops-ml-security-and-anomaly-research"
        self.scripts_dir = Path(__file__).parent

        # Load GitHub token
        token_file = self.scripts_dir / ".github_token"
        if token_file.exists():
            with open(token_file, 'r') as f:
                self.token = f.read().strip()
        else:
            print("[!] Error: No GitHub token found at scripts/.github_token")
            sys.exit(1)

        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }

    def get_recent_runs(self, per_page=10):
        """Get recent workflow runs."""
        url = f'https://api.github.com/repos/{self.repo}/actions/workflows/security-scanning.yml/runs'
        params = {'per_page': per_page}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get('workflow_runs', [])
        except Exception as e:
            print(f"[!] Error fetching runs: {e}")
            return []

    def wait_for_completion(self, timeout_minutes=20):
        """Wait for both branch workflows to complete."""
        print("=" * 80)
        print("MONITORING WORKFLOW COMPLETION")
        print("=" * 80)
        print(f"Waiting for workflows to complete (timeout: {timeout_minutes} min)")
        print()

        start_time = time.time()
        timeout_seconds = timeout_minutes * 60
        check_interval = 30

        main_completed = False
        hardened_completed = False

        while (time.time() - start_time) < timeout_seconds:
            runs = self.get_recent_runs(per_page=5)

            if runs:
                # Check for main and hardened branch runs
                for run in runs:
                    branch = run['head_branch']
                    status = run['status']
                    conclusion = run.get('conclusion', 'pending')
                    created_at = run['created_at']

                    # Only consider recent runs (last 30 minutes)
                    created_time = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
                    age_minutes = (datetime.utcnow() - created_time).total_seconds() / 60

                    if age_minutes < 30:  # Only recent runs
                        if branch == 'main' and status == 'completed':
                            main_completed = True
                        elif branch == 'hardened' and status == 'completed':
                            hardened_completed = True

                # Display status
                elapsed = int(time.time() - start_time)
                main_status = "[DONE]" if main_completed else "[RUNNING]"
                hardened_status = "[DONE]" if hardened_completed else "[RUNNING]"

                print(f"\r[{elapsed}s] Main: {main_status} | Hardened: {hardened_status}", end='', flush=True)

                # Check if both complete
                if main_completed and hardened_completed:
                    print()
                    print()
                    print("[OK] Both workflows completed!")
                    return True

            time.sleep(check_interval)

        print()
        print("[!] Timeout reached")
        print(f"    Main: {'Complete' if main_completed else 'Not complete'}")
        print(f"    Hardened: {'Complete' if hardened_completed else 'Not complete'}")

        if main_completed or hardened_completed:
            print("[*] At least one workflow completed - proceeding with download")
            return True

        return False

    def download_artifacts(self):
        """Download all artifacts using existing script."""
        print()
        print("=" * 80)
        print("DOWNLOADING ARTIFACTS")
        print("=" * 80)

        download_script = self.scripts_dir / "automated-weekly-collection.py"

        if not download_script.exists():
            print(f"[!] Download script not found: {download_script}")
            return False

        try:
            result = subprocess.run(
                ["python", str(download_script)],
                cwd=str(self.scripts_dir),
                capture_output=True,
                text=True,
                timeout=600
            )

            print(result.stdout)

            if result.returncode != 0:
                print("[!] Download had some errors:")
                print(result.stderr)
                return False

            print("[OK] Download completed!")
            return True

        except subprocess.TimeoutExpired:
            print("[!] Download timeout")
            return False
        except Exception as e:
            print(f"[!] Download error: {e}")
            return False

    def verify_data(self):
        """Verify downloaded data."""
        print()
        print("=" * 80)
        print("VERIFYING DATA")
        print("=" * 80)

        repo_root = self.scripts_dir.parent
        research_data = repo_root / "research-data"
        ml_output = repo_root / "ml-pipeline" / "output"

        checks = []

        # Check research data exists
        if research_data.exists():
            artifact_count = len(list(research_data.rglob("*.json")))
            checks.append(f"[OK] Research data directory exists ({artifact_count} JSON files)")
        else:
            checks.append("[!] Research data directory not found")

        # Check ML output exists
        if ml_output.exists():
            csv_files = list(ml_output.glob("*.csv"))
            if csv_files:
                checks.append(f"[OK] ML features extracted ({len(csv_files)} CSV files)")
            else:
                checks.append("[!] No CSV files found in ML output")
        else:
            checks.append("[!] ML output directory not found")

        # Check download logs
        download_logs = research_data / "download-logs"
        if download_logs.exists():
            log_files = list(download_logs.glob("*.log"))
            checks.append(f"[OK] Download logs created ({len(log_files)} files)")
        else:
            checks.append("[!] No download logs found")

        # Print results
        for check in checks:
            print(f"  {check}")

        print()
        all_ok = all("[OK]" in c for c in checks)

        if all_ok:
            print("[OK] All data verified successfully!")
        else:
            print("[!] Some data may be missing - check logs")

        return all_ok

    def show_summary(self):
        """Show summary of collected data."""
        print()
        print("=" * 80)
        print("COLLECTION SUMMARY")
        print("=" * 80)

        repo_root = self.scripts_dir.parent
        research_data = repo_root / "research-data"
        ml_output = repo_root / "ml-pipeline" / "output"

        # Count artifacts
        total_json = len(list(research_data.rglob("*.json"))) if research_data.exists() else 0
        total_csv = len(list(ml_output.glob("*.csv"))) if ml_output.exists() else 0
        total_logs = len(list((research_data / "download-logs").glob("*.log"))) if (research_data / "download-logs").exists() else 0

        print(f"""
Data Collection Complete!

Artifacts downloaded:  {total_json} JSON files
Features extracted:    {total_csv} CSV files
Download logs:         {total_logs} log files

Locations:
  - Research data:  {research_data}
  - ML features:    {ml_output}
  - Download logs:  {research_data / 'download-logs'}

Next steps:
  1. Review data in research-data/
  2. Check features in ml-pipeline/output/
  3. Run ML training when ready
""")

    def run(self):
        """Run complete collection process."""
        print()
        print("=" * 80)
        print("AUTOMATED WORKFLOW COLLECTION")
        print("=" * 80)
        print(f"Repository: {self.repo}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print()

        print("[*] Make sure you've triggered workflows for BOTH branches:")
        print("    - main")
        print("    - hardened")
        print()

        response = input("Have you triggered both workflows? (y/n): ")
        if response.lower() != 'y':
            print("[!] Please trigger workflows first, then run this script again")
            print()
            print("Instructions:")
            print("  1. Go to: https://github.com/{}/actions".format(self.repo))
            print("  2. Click 'Security Scanning' workflow")
            print("  3. Click 'Run workflow' -> select 'main' -> Run")
            print("  4. Click 'Run workflow' -> select 'hardened' -> Run")
            print("  5. Re-run this script")
            return False

        # Step 1: Wait for completion
        if not self.wait_for_completion(timeout_minutes=20):
            print("[!] Workflows did not complete in time")
            print("[*] You can try running the download script manually later")
            return False

        # Brief wait for artifacts to be ready
        print()
        print("[*] Waiting 30 seconds for artifacts to be ready...")
        time.sleep(30)

        # Step 2: Download artifacts
        if not self.download_artifacts():
            print("[!] Download had some issues - check logs")
            # Continue anyway to verify what we got

        # Step 3: Verify data
        self.verify_data()

        # Step 4: Show summary
        self.show_summary()

        print("=" * 80)
        print("[OK] COLLECTION COMPLETE!")
        print("=" * 80)
        print()

        return True


def main():
    collector = AutoCollector()
    success = collector.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
