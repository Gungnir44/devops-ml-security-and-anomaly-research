#!/usr/bin/env python3
"""
Execute All Dual-Branch Attacks
================================

Master script to execute all 24 attack scenarios on BOTH main and hardened branches.

This creates comprehensive research data:
- 24 scenarios × 2 branches = 48 attack samples
- Plus ~70 baseline samples = ~118 total samples
- Enables comparison between vulnerable and hardened environments

Execution Strategy:
- Runs each attack on main branch first
- Then same attack on hardened branch
- Logs all results
- Can resume from any scenario if interrupted
- Configurable delays between attacks
"""

import sys
import time
from pathlib import Path
from datetime import datetime
import subprocess
import json

class MasterDualBranchExecutor:
    """Execute all attack scenarios on both branches."""

    def __init__(self):
        self.attacks_dir = Path(__file__).parent
        self.pipeline_script = self.attacks_dir / "dual-branch-attack-pipeline.py"

        # All 24 attack scenarios
        self.all_scenarios = [
            # Original 14 scenarios
            "1.1", "1.2", "1.3",  # Credential attacks
            "2.1", "2.2", "2.3",  # Code injection
            "3.1", "3.2",         # Supply chain
            "4.1", "4.2",         # Privilege escalation
            "5.1", "5.2",         # Data exfiltration
            "6.1",                # Infrastructure
            "7.1",                # Evasion
            # New 10 scenarios
            "8.1", "8.2", "8.3", "8.4", "8.5",  # Secrets, actions, environment
            "9.1", "9.2", "9.3", "9.4", "9.5"   # Time-based, webhooks, filesystem
        ]

        # Attack descriptions for progress tracking
        self.descriptions = {
            "1.1": "Geographic Anomaly",
            "1.2": "Service Account Abuse",
            "1.3": "Credential Stuffing",
            "2.1": "Pipeline Backdoor",
            "2.2": "Cryptomining",
            "2.3": "Code Backdoor",
            "3.1": "Malicious Dependency",
            "3.2": "Compromised Image",
            "4.1": "Permission Escalation",
            "4.2": "Secret Access",
            "5.1": "Artifact Exfiltration",
            "5.2": "Repository Cloning",
            "6.1": "Container Abuse",
            "7.1": "Approval Bypass",
            "8.1": "Secrets in Logs",
            "8.2": "Compromised Action",
            "8.3": "Environment Poisoning",
            "8.4": "Fork Bomb",
            "8.5": "Log Tampering",
            "9.1": "Time Bomb",
            "9.2": "Webhook Abuse",
            "9.3": "Symlink Attack",
            "9.4": "Race Condition",
            "9.5": "Cache Poisoning"
        }

    def execute_scenario(self, scenario_id: str, scenario_num: int, total: int) -> bool:
        """Execute single scenario on both branches."""
        description = self.descriptions.get(scenario_id, "Unknown")

        print("")
        print("=" * 80)
        print(f"  SCENARIO {scenario_num}/{total}: {scenario_id} - {description}".center(80))
        print("=" * 80)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("")

        try:
            result = subprocess.run(
                ["python", str(self.pipeline_script), "--scenario", scenario_id],
                cwd=str(self.attacks_dir),
                timeout=600  # 10 min timeout per scenario
            )

            success = result.returncode == 0

            if success:
                print("")
                print(f"[OK] Scenario {scenario_id} completed successfully on both branches")
            else:
                print("")
                print(f"[FAIL] Scenario {scenario_id} failed - check logs above")

            return success

        except subprocess.TimeoutExpired:
            print(f"[!] Scenario {scenario_id} timed out")
            return False
        except Exception as e:
            print(f"[!] Error executing scenario {scenario_id}: {e}")
            return False

    def run_all(self, start_from: str = None, delay_minutes: int = 0):
        """Execute all scenarios."""
        print("")
        print("=" * 80)
        print("  MASTER DUAL-BRANCH ATTACK EXECUTOR".center(80))
        print("=" * 80)
        print(f"\nTotal scenarios: {len(self.all_scenarios)}")
        print(f"Branches per scenario: 2 (main + hardened)")
        print(f"Total attacks: {len(self.all_scenarios) * 2}")
        print(f"Delay between scenarios: {delay_minutes} minutes")
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Determine starting point
        scenarios_to_run = self.all_scenarios
        if start_from:
            if start_from in self.all_scenarios:
                start_idx = self.all_scenarios.index(start_from)
                scenarios_to_run = self.all_scenarios[start_idx:]
                print(f"\nResuming from scenario: {start_from}")
            else:
                print(f"[!] Invalid start scenario: {start_from}")
                return False

        print(f"\nScenarios to execute: {len(scenarios_to_run)}")
        print("")

        # Confirm before starting
        response = input("Ready to begin? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("[*] Execution cancelled by user")
            return False

        # Execution tracking
        results = {
            "start_time": datetime.now().isoformat(),
            "scenarios": {},
            "summary": {
                "total": len(scenarios_to_run),
                "successful": 0,
                "failed": 0
            }
        }

        # Execute each scenario
        for idx, scenario_id in enumerate(scenarios_to_run, 1):
            # Execute scenario
            success = self.execute_scenario(
                scenario_id,
                idx,
                len(scenarios_to_run)
            )

            # Record result
            results["scenarios"][scenario_id] = {
                "success": success,
                "timestamp": datetime.now().isoformat()
            }

            if success:
                results["summary"]["successful"] += 1
            else:
                results["summary"]["failed"] += 1

            # Delay before next scenario (except for last one)
            if idx < len(scenarios_to_run) and delay_minutes > 0:
                print("")
                print(f"[*] Waiting {delay_minutes} minutes before next scenario...")
                print(f"[*] Progress: {idx}/{len(scenarios_to_run)} complete")
                time.sleep(delay_minutes * 60)

        # Final summary
        results["end_time"] = datetime.now().isoformat()

        print("")
        print("=" * 80)
        print("  EXECUTION COMPLETE".center(80))
        print("=" * 80)
        print(f"\nTotal scenarios executed: {results['summary']['total']}")
        print(f"Successful: {results['summary']['successful']}")
        print(f"Failed: {results['summary']['failed']}")
        print(f"Success rate: {(results['summary']['successful'] / results['summary']['total'] * 100):.1f}%")
        print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Save results
        log_dir = self.attacks_dir / "logs" / "master-execution"
        log_dir.mkdir(parents=True, exist_ok=True)

        result_file = log_dir / f"execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n[*] Results saved to: {result_file}")

        # Next steps
        print("")
        print("=" * 80)
        print("NEXT STEPS")
        print("=" * 80)
        print("\n1. Wait for scheduled security scans (2 AM UTC daily)")
        print(f"2. Scans will process all {results['summary']['successful'] * 2} attacks")
        print("3. Artifacts will be collected automatically")
        print("4. Proceed to Phase 3: ML Training")
        print("   Command: cd scripts && python ml-train-models.py")
        print("")

        return results["summary"]["failed"] == 0


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Execute all attack scenarios on both main and hardened branches",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Execute all 24 scenarios on both branches (48 total attacks)
  python execute-all-dual-branch.py

  # Resume from scenario 5.1 (if previous run was interrupted)
  python execute-all-dual-branch.py --start-from 5.1

  # Execute with 5-minute delay between scenarios
  python execute-all-dual-branch.py --delay 5

  # List all scenarios without executing
  python execute-all-dual-branch.py --list

Execution Strategy:
  - Each scenario executed on main branch first
  - Then same scenario on hardened branch
  - Optional delay between scenarios to space out commits
  - Can resume from any scenario if interrupted
  - Full logging and progress tracking

Expected Results:
  - 24 scenarios × 2 branches = 48 attack samples
  - Each attack triggers security scanning workflow
  - Scans run at 2 AM UTC (scheduled)
  - Artifacts collected automatically
  - Ready for ML training after all scans complete
"""
    )

    parser.add_argument('--start-from', type=str,
                       help='Resume from specific scenario (e.g., 5.1)')
    parser.add_argument('--delay', type=int, default=0,
                       help='Minutes to wait between scenarios (default: 0)')
    parser.add_argument('--list', action='store_true',
                       help='List all scenarios and exit')

    args = parser.parse_args()

    executor = MasterDualBranchExecutor()

    # List scenarios if requested
    if args.list:
        print("\n" + "=" * 80)
        print("ALL ATTACK SCENARIOS")
        print("=" * 80 + "\n")
        for scenario_id in executor.all_scenarios:
            description = executor.descriptions.get(scenario_id, "Unknown")
            print(f"  {scenario_id}: {description}")
        print(f"\nTotal: {len(executor.all_scenarios)} scenarios")
        print(f"Total attacks (dual-branch): {len(executor.all_scenarios) * 2}")
        print("")
        sys.exit(0)

    # Execute all scenarios
    success = executor.run_all(
        start_from=args.start_from,
        delay_minutes=args.delay
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
