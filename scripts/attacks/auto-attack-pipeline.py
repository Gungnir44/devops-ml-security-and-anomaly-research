#!/usr/bin/env python3
"""
Automated Attack-to-Data Pipeline
===================================

Complete automation:
1. Execute attack scenario
2. Commit changes to Git
3. Push to trigger workflows
4. Wait for workflow completion
5. Download artifacts automatically
6. Extract features

This creates a complete end-to-end automated pipeline.
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
import requests


class AutoAttackPipeline:
    """Automated attack execution with workflow trigger and data collection."""

    def __init__(self, github_token=None):
        self.repo_root = Path(__file__).parent.parent.parent
        self.attacks_dir = Path(__file__).parent
        self.scripts_dir = self.repo_root / "scripts"

        # Get GitHub token
        token_file = self.scripts_dir / ".github_token"
        if github_token:
            self.github_token = github_token
        elif token_file.exists():
            with open(token_file, 'r') as f:
                self.github_token = f.read().strip()
        else:
            self.github_token = None
            print("[!] Warning: No GitHub token found")

        self.repo = "Gungnir44/devops-ml-security-and-anomaly-research"
        self.headers = {
            'Authorization': f'Bearer {self.github_token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }

    def execute_attack(self, scenario_id: str, **kwargs) -> bool:
        """Execute attack scenario."""
        print("=" * 80)
        print(f"[1/5] Executing Attack Scenario {scenario_id}")
        print("=" * 80)

        scenario_scripts = {
            # Original 14 scenarios
            "1.1": "geographic_anomaly.py",
            "1.2": "service_account_abuse.py",
            "1.3": "credential_stuffing.py",
            "2.1": "pipeline_backdoor.py",
            "2.2": "cryptomining.py",
            "2.3": "code_backdoor.py",
            "3.1": "malicious_dependency.py",
            "3.2": "compromised_image.py",
            "4.1": "permission_escalation.py",
            "4.2": "secret_access.py",
            "5.1": "artifact_exfiltration.py",
            "5.2": "repo_cloning.py",
            "6.1": "container_abuse.py",
            "7.1": "approval_bypass.py",
            # New 10 scenarios
            "8.1": "secrets_in_logs.py",
            "8.2": "compromised_action.py",
            "8.3": "env_poisoning.py",
            "8.4": "fork_bomb.py",
            "8.5": "log_tampering.py",
            "9.1": "time_bomb.py",
            "9.2": "webhook_abuse.py",
            "9.3": "symlink_attack.py",
            "9.4": "race_condition.py",
            "9.5": "cache_poisoning.py"
        }

        script_name = scenario_scripts.get(scenario_id)
        if not script_name:
            print(f"[!] Unknown scenario: {scenario_id}")
            return False

        script_path = self.attacks_dir / "scenarios" / script_name
        if not script_path.exists():
            print(f"[!] Script not found: {script_path}")
            return False

        # Execute attack
        print(f"[*] Running: {script_name}")
        try:
            result = subprocess.run(
                ["python", str(script_path)],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(script_path.parent)
            )

            print(result.stdout)

            if result.returncode != 0:
                print(f"[!] Attack execution failed:")
                print(result.stderr)
                return False

            print(f"[OK] Attack scenario executed successfully\n")
            return True

        except subprocess.TimeoutExpired:
            print(f"[!] Attack execution timeout")
            return False
        except Exception as e:
            print(f"[!] Error: {e}")
            return False

    def commit_and_push(self, scenario_id: str) -> bool:
        """Commit changes and push to trigger workflows."""
        print("=" * 80)
        print(f"[2/5] Committing and Pushing Changes")
        print("=" * 80)

        # Get realistic commit message for scenario
        commit_messages = {
            # Original 14 scenarios
            "1.1": "Update access logging",
            "1.2": "Update service account configuration",
            "1.3": "Update authentication settings",
            "2.1": "Update dependencies caching",
            "2.2": "Update build caching configuration",
            "2.3": "Add diagnostic endpoints",
            "3.1": "Update dependencies for bug fix",
            "3.2": "Update base image",
            "4.1": "Update RBAC configuration",
            "4.2": "Update secret management",
            "5.1": "Update artifact configuration",
            "5.2": "Update repository settings",
            "6.1": "Add resource scaling configuration",
            "7.1": "Streamline deployment workflow",
            # New 10 scenarios
            "8.1": "Add deployment debugging",
            "8.2": "Update GitHub Actions",
            "8.3": "Configure build environment variables",
            "8.4": "Add integration test suite",
            "8.5": "Clean up build artifacts",
            "9.1": "Add environment-specific configs",
            "9.2": "Update API webhooks",
            "9.3": "Package build artifacts",
            "9.4": "Optimize deployment process",
            "9.5": "Update build cache strategy"
        }

        commit_msg = commit_messages.get(scenario_id, "Update configuration")
        commit_msg += f"\n\nResearch attack scenario {scenario_id} for ML security study."

        try:
            # Check for changes
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=str(self.repo_root)
            )

            if not result.stdout.strip():
                print("[!] No changes to commit")
                return False

            print(f"[*] Changes detected:")
            print(result.stdout)

            # Add all changes
            subprocess.run(
                ["git", "add", "-A"],
                cwd=str(self.repo_root),
                check=True
            )

            # Commit
            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=str(self.repo_root),
                check=True
            )

            # Push
            print(f"[*] Pushing to origin/main...")
            result = subprocess.run(
                ["git", "push", "origin", "main"],
                capture_output=True,
                text=True,
                cwd=str(self.repo_root)
            )

            if result.returncode != 0:
                print(f"[!] Push failed: {result.stderr}")
                return False

            print(f"[OK] Changes committed and pushed\n")
            return True

        except subprocess.CalledProcessError as e:
            print(f"[!] Git operation failed: {e}")
            return False

    def wait_for_workflow(self, timeout_minutes=15) -> dict:
        """Wait for workflow to complete and return run info."""
        print("=" * 80)
        print(f"[3/5] Waiting for Workflow Completion")
        print("=" * 80)

        if not self.github_token:
            print("[!] No GitHub token - cannot check workflow status")
            return None

        print(f"[*] Monitoring workflows (timeout: {timeout_minutes} min)...")

        start_time = time.time()
        timeout_seconds = timeout_minutes * 60
        check_interval = 30  # Check every 30 seconds

        latest_run = None

        while (time.time() - start_time) < timeout_seconds:
            try:
                # Get recent workflow runs
                url = f'https://api.github.com/repos/{self.repo}/actions/runs'
                params = {'per_page': 5, 'event': 'push'}
                response = requests.get(url, headers=self.headers, params=params, timeout=10)

                if response.status_code == 200:
                    runs = response.json().get('workflow_runs', [])

                    if runs:
                        latest_run = runs[0]
                        status = latest_run['status']
                        conclusion = latest_run['conclusion']

                        elapsed = int(time.time() - start_time)
                        print(f"[*] [{elapsed}s] Status: {status}, Conclusion: {conclusion}")

                        if status == 'completed':
                            print(f"\n[OK] Workflow completed: {conclusion}")
                            return latest_run

                else:
                    print(f"[!] API error: {response.status_code}")

            except Exception as e:
                print(f"[!] Error checking workflow: {e}")

            time.sleep(check_interval)

        print(f"[!] Workflow did not complete within {timeout_minutes} minutes")
        return latest_run

    def download_artifacts(self, run_id: int) -> bool:
        """Download artifacts from workflow run."""
        print("=" * 80)
        print(f"[4/5] Downloading Artifacts")
        print("=" * 80)

        if not self.github_token:
            print("[!] No GitHub token - cannot download artifacts")
            return False

        try:
            # Get artifacts for this run
            url = f'https://api.github.com/repos/{self.repo}/actions/runs/{run_id}/artifacts'
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code != 200:
                print(f"[!] Failed to get artifacts: {response.status_code}")
                return False

            artifacts = response.json().get('artifacts', [])

            if not artifacts:
                print("[!] No artifacts found for this run")
                return False

            print(f"[*] Found {len(artifacts)} artifacts")

            # Download artifacts using existing script
            download_script = self.scripts_dir / "automated-weekly-collection.py"

            if download_script.exists():
                print(f"[*] Running artifact download script...")
                result = subprocess.run(
                    ["python", str(download_script)],
                    cwd=str(self.scripts_dir),
                    capture_output=True,
                    text=True,
                    timeout=300
                )

                if result.returncode == 0:
                    print(f"[OK] Artifacts downloaded successfully")
                    return True
                else:
                    print(f"[!] Artifact download failed: {result.stderr}")
                    return False
            else:
                print(f"[!] Download script not found: {download_script}")
                return False

        except Exception as e:
            print(f"[!] Error downloading artifacts: {e}")
            return False

    def extract_features(self) -> bool:
        """Extract features from downloaded artifacts."""
        print("=" * 80)
        print(f"[5/5] Extracting Features")
        print("=" * 80)

        # Features are automatically extracted by download script
        # Just verify output files exist

        output_dir = self.repo_root / "ml-pipeline" / "output"

        if output_dir.exists():
            csv_files = list(output_dir.glob("features_*.csv"))
            if csv_files:
                print(f"[OK] Found {len(csv_files)} feature files")
                for f in csv_files[-3:]:  # Show last 3
                    print(f"     - {f.name}")
                return True

        print("[!] No feature files found")
        return False

    def run_complete_pipeline(self, scenario_id: str, auto_commit=True, auto_download=True):
        """Run complete attack-to-data pipeline."""
        print("\n")
        print("=" * 80)
        print("  AUTOMATED ATTACK-TO-DATA PIPELINE".center(80))
        print("=" * 80)
        print(f"\nScenario: {scenario_id}")
        print(f"Auto-commit: {auto_commit}")
        print(f"Auto-download: {auto_download}")
        print(f"Timestamp: {datetime.now().isoformat()}\n")

        # Step 1: Execute attack
        if not self.execute_attack(scenario_id):
            print("\n[FAIL] Pipeline failed at step 1: Attack execution")
            return False

        # Step 2: Commit and push (if enabled)
        if auto_commit:
            if not self.commit_and_push(scenario_id):
                print("\n[FAIL] Pipeline failed at step 2: Commit/Push")
                return False

            # Step 3: Wait for workflow
            run_info = self.wait_for_workflow(timeout_minutes=15)

            if not run_info:
                print("\n[WARN] Could not verify workflow completion")
                print("[*] You may need to wait and download manually")
            else:
                # Step 4: Download artifacts (if enabled)
                if auto_download:
                    time.sleep(30)  # Brief wait for artifacts to be ready

                    run_id = run_info.get('id')
                    if run_id and self.download_artifacts(run_id):
                        # Step 5: Extract features
                        self.extract_features()

        print("\n")
        print("=" * 80)
        print("  PIPELINE COMPLETE".center(80))
        print("=" * 80)
        print(f"\nScenario {scenario_id} execution and data collection complete!")
        print(f"Timestamp: {datetime.now().isoformat()}\n")

        return True


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Automated Attack-to-Data Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full automated pipeline
  python auto-attack-pipeline.py --scenario 2.2

  # Execute attack only (no commit)
  python auto-attack-pipeline.py --scenario 2.2 --no-commit

  # Execute and commit but don't wait for download
  python auto-attack-pipeline.py --scenario 2.2 --no-download
"""
    )

    parser.add_argument('--scenario', required=True,
                       help='Attack scenario ID (e.g., 2.2, 3.1, etc.)')
    parser.add_argument('--no-commit', action='store_true',
                       help='Do not commit/push changes')
    parser.add_argument('--no-download', action='store_true',
                       help='Do not download artifacts')
    parser.add_argument('--token', type=str,
                       help='GitHub token (optional, reads from .github_token)')

    args = parser.parse_args()

    pipeline = AutoAttackPipeline(github_token=args.token)

    success = pipeline.run_complete_pipeline(
        scenario_id=args.scenario,
        auto_commit=not args.no_commit,
        auto_download=not args.no_download
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
