#!/usr/bin/env python3
"""
Dual-Branch Attack Pipeline
============================

Executes attack scenarios on BOTH main and hardened branches for comprehensive
research data collection and defense comparison.

Strategy:
1. Execute attack on main branch
2. Commit and push (triggers workflow)
3. Switch to hardened branch
4. Execute same attack on hardened branch
5. Commit and push (triggers workflow)
6. Switch back to main branch
7. Wait for both workflows to complete
8. Download artifacts from both branches

This doubles the attack samples and enables comparison between vulnerable
and hardened environments.
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime
import json

class DualBranchAttackPipeline:
    """Execute attacks on both main and hardened branches."""

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

        self.main_branch = "main"
        self.hardened_branch = "hardened"

        # Attack scenario mapping
        self.scenario_scripts = {
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

        # Commit messages per scenario
        self.commit_messages = {
            # Original 14
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
            # New 10
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

    def get_current_branch(self) -> str:
        """Get current git branch."""
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            cwd=str(self.repo_root)
        )
        return result.stdout.strip()

    def switch_branch(self, branch: str) -> bool:
        """Switch to specified branch."""
        print(f"[*] Switching to {branch} branch...")

        try:
            # Stash any uncommitted changes
            subprocess.run(
                ["git", "stash"],
                capture_output=True,
                cwd=str(self.repo_root)
            )

            # Switch branch
            result = subprocess.run(
                ["git", "checkout", branch],
                capture_output=True,
                text=True,
                cwd=str(self.repo_root)
            )

            if result.returncode != 0:
                print(f"[!] Failed to switch to {branch}: {result.stderr}")
                return False

            print(f"[OK] Switched to {branch}")
            return True

        except Exception as e:
            print(f"[!] Error switching branch: {e}")
            return False

    def execute_attack(self, scenario_id: str, branch: str) -> bool:
        """Execute attack scenario on specified branch."""
        print("")
        print("=" * 80)
        print(f"EXECUTING ATTACK {scenario_id} ON {branch.upper()} BRANCH")
        print("=" * 80)

        script_name = self.scenario_scripts.get(scenario_id)
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

            print(f"[OK] Attack scenario executed successfully")
            return True

        except subprocess.TimeoutExpired:
            print(f"[!] Attack execution timeout")
            return False
        except Exception as e:
            print(f"[!] Error: {e}")
            return False

    def commit_and_push(self, scenario_id: str, branch: str) -> bool:
        """Commit changes and push to specified branch."""
        print("")
        print(f"[*] Committing and pushing to {branch}...")

        # Get commit message
        base_msg = self.commit_messages.get(scenario_id, "Update configuration")
        commit_msg = f"{base_msg}\n\nResearch attack scenario {scenario_id} for ML security study.\nBranch: {branch}\nPhase: 2 - Attack Execution (Dual-Branch)\n\nGenerated with Claude Code\nCo-Authored-By: Claude <noreply@anthropic.com>"

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

            print(f"[*] Changes detected")

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
            print(f"[*] Pushing to origin/{branch}...")
            result = subprocess.run(
                ["git", "push", "origin", branch],
                capture_output=True,
                text=True,
                cwd=str(self.repo_root)
            )

            if result.returncode != 0:
                print(f"[!] Push failed: {result.stderr}")
                return False

            print(f"[OK] Changes committed and pushed to {branch}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"[!] Git operation failed: {e}")
            return False

    def run_dual_branch_attack(self, scenario_id: str, wait_for_workflows=False):
        """Execute attack on both main and hardened branches."""
        print("")
        print("=" * 80)
        print("  DUAL-BRANCH ATTACK PIPELINE".center(80))
        print("=" * 80)
        print(f"\nScenario: {scenario_id}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("")

        original_branch = self.get_current_branch()
        print(f"[*] Current branch: {original_branch}")

        results = {
            "scenario_id": scenario_id,
            "timestamp": datetime.now().isoformat(),
            "main_branch": {"executed": False, "committed": False},
            "hardened_branch": {"executed": False, "committed": False}
        }

        # ===================================================================
        # PHASE 1: Execute on MAIN branch
        # ===================================================================

        print("")
        print("=" * 80)
        print("PHASE 1: MAIN BRANCH ATTACK")
        print("=" * 80)

        if not self.switch_branch(self.main_branch):
            print("[FAIL] Could not switch to main branch")
            return False

        if self.execute_attack(scenario_id, self.main_branch):
            results["main_branch"]["executed"] = True

            if self.commit_and_push(scenario_id, self.main_branch):
                results["main_branch"]["committed"] = True
                print(f"[OK] Main branch attack complete")
            else:
                print(f"[WARN] Main branch attack executed but not committed")
        else:
            print(f"[FAIL] Main branch attack failed")

        # Brief pause between branches
        time.sleep(5)

        # ===================================================================
        # PHASE 2: Execute on HARDENED branch
        # ===================================================================

        print("")
        print("=" * 80)
        print("PHASE 2: HARDENED BRANCH ATTACK")
        print("=" * 80)

        if not self.switch_branch(self.hardened_branch):
            print("[FAIL] Could not switch to hardened branch")
            # Try to return to original branch
            self.switch_branch(original_branch)
            return False

        if self.execute_attack(scenario_id, self.hardened_branch):
            results["hardened_branch"]["executed"] = True

            if self.commit_and_push(scenario_id, self.hardened_branch):
                results["hardened_branch"]["committed"] = True
                print(f"[OK] Hardened branch attack complete")
            else:
                print(f"[WARN] Hardened branch attack executed but not committed")
        else:
            print(f"[FAIL] Hardened branch attack failed")

        # ===================================================================
        # PHASE 3: Return to original branch
        # ===================================================================

        print("")
        print("=" * 80)
        print("PHASE 3: CLEANUP")
        print("=" * 80)

        if not self.switch_branch(original_branch):
            print(f"[WARN] Could not return to {original_branch}")
        else:
            print(f"[OK] Returned to {original_branch}")

        # ===================================================================
        # SUMMARY
        # ===================================================================

        print("")
        print("=" * 80)
        print("  DUAL-BRANCH ATTACK SUMMARY".center(80))
        print("=" * 80)
        print(f"\nScenario: {scenario_id}")
        print(f"\nMain Branch:")
        print(f"  Executed: {'YES' if results['main_branch']['executed'] else 'NO'}")
        print(f"  Committed: {'YES' if results['main_branch']['committed'] else 'NO'}")
        print(f"\nHardened Branch:")
        print(f"  Executed: {'YES' if results['hardened_branch']['executed'] else 'NO'}")
        print(f"  Committed: {'YES' if results['hardened_branch']['committed'] else 'NO'}")

        # Save results
        log_dir = self.attacks_dir / "logs" / "dual-branch-results"
        log_dir.mkdir(parents=True, exist_ok=True)

        result_file = log_dir / f"scenario_{scenario_id.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n[*] Results saved to: {result_file.name}")

        # Determine overall success
        success = (results['main_branch']['committed'] and
                  results['hardened_branch']['committed'])

        if success:
            print("")
            print("=" * 80)
            print("  SUCCESS - BOTH BRANCHES ATTACKED".center(80))
            print("=" * 80)
            print("\nNext steps:")
            print("1. Wait for scheduled security scans (2 AM UTC)")
            print("2. Workflows will scan both branches")
            print("3. Artifacts will be collected from both")
            print("4. Features will be extracted for ML training")
            print("")
        else:
            print("")
            print("=" * 80)
            print("  PARTIAL SUCCESS - CHECK RESULTS ABOVE".center(80))
            print("=" * 80)
            print("")

        return success


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Dual-Branch Attack Pipeline - Execute attacks on both main and hardened branches",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Execute attack on both branches
  python dual-branch-attack-pipeline.py --scenario 2.2

  # Execute with custom GitHub token
  python dual-branch-attack-pipeline.py --scenario 3.1 --token ghp_xxxxx

This script will:
  1. Execute attack on main branch
  2. Commit and push to main
  3. Execute same attack on hardened branch
  4. Commit and push to hardened
  5. Return to original branch
  6. Log results for both branches

This doubles your attack samples and enables comparison between
vulnerable and hardened environments!
"""
    )

    parser.add_argument('--scenario', required=True,
                       help='Attack scenario ID (e.g., 2.2, 3.1, 8.1)')
    parser.add_argument('--token', type=str,
                       help='GitHub token (optional, reads from .github_token)')

    args = parser.parse_args()

    pipeline = DualBranchAttackPipeline(github_token=args.token)

    success = pipeline.run_dual_branch_attack(
        scenario_id=args.scenario
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
