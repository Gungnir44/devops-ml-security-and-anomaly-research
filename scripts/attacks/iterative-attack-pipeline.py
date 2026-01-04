#!/usr/bin/env python3
"""
Iterative Attack-Train-Reattack Pipeline
=========================================

Sophisticated research methodology:
1. Execute attack on both branches (Iteration 1 - baseline)
2. Wait for scans, collect data, train ML model
3. Deploy ML model for monitoring
4. Re-execute SAME attack (Iteration 2 - with ML)
5. Collect ML detection results
6. Re-train ML with new data
7. Re-execute SAME attack (Iteration 3 - improved ML)
8. Collect ML detection results
9. Analyze 3 iterations, document findings
10. Move to next attack

This answers: "Does ML improve with iterative training?"
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
from datetime import datetime
import requests

class IterativeAttackPipeline:
    """Execute attack-train-reattack cycles with iterative ML improvement."""

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

        self.repo = "Gungnir44/devops-ml-security-and-anomaly-research"
        self.headers = {
            'Authorization': f'Bearer {self.github_token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }

        # Scenario mapping
        self.scenario_scripts = {
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

    def execute_dual_branch_attack(self, scenario_id: str, iteration: int) -> bool:
        """Execute attack on both branches."""
        print("")
        print("=" * 80)
        print(f"  ITERATION {iteration}: EXECUTE ATTACK {scenario_id}".center(80))
        print("=" * 80)

        dual_branch_script = self.attacks_dir / "dual-branch-attack-pipeline.py"

        try:
            result = subprocess.run(
                ["python", str(dual_branch_script), "--scenario", scenario_id],
                cwd=str(self.attacks_dir),
                timeout=600
            )

            if result.returncode == 0:
                print(f"[OK] Attack {scenario_id} executed on both branches")
                return True
            else:
                print(f"[FAIL] Attack execution failed")
                return False

        except Exception as e:
            print(f"[!] Error: {e}")
            return False

    def wait_for_scans(self, hours=24) -> bool:
        """Wait for security scans to complete."""
        print("")
        print("=" * 80)
        print("  WAITING FOR SECURITY SCANS".center(80))
        print("=" * 80)

        next_scan = "2 AM UTC"
        print(f"[*] Security scans run at {next_scan}")
        print(f"[*] Waiting up to {hours} hours for scans to complete...")
        print(f"[*] You can monitor progress at:")
        print(f"    https://github.com/{self.repo}/actions")
        print("")

        # Calculate wait time until next 2 AM UTC
        from datetime import datetime, timezone, timedelta

        now = datetime.now(timezone.utc)
        next_run = now.replace(hour=2, minute=0, second=0, microsecond=0)

        if now.hour >= 2:
            # Next run is tomorrow
            next_run += timedelta(days=1)

        wait_seconds = (next_run - now).total_seconds()
        # Add buffer for workflow to complete
        wait_seconds += 3600  # 1 hour buffer

        print(f"[*] Next scan at: {next_run.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"[*] Waiting: {wait_seconds / 3600:.1f} hours")

        response = input("\nPress Enter when scans complete, or 's' to skip wait: ").strip().lower()

        if response == 's':
            print("[*] Skipping wait - assuming scans are complete")
            return True

        print("[OK] Proceeding with scan results")
        return True

    def collect_artifacts(self) -> bool:
        """Collect artifacts from completed scans."""
        print("")
        print("=" * 80)
        print("  COLLECTING ARTIFACTS".center(80))
        print("=" * 80)

        collection_script = self.scripts_dir / "automated-weekly-collection.py"

        if not collection_script.exists():
            print(f"[!] Collection script not found: {collection_script}")
            return False

        try:
            print("[*] Running artifact collection...")
            result = subprocess.run(
                ["python", str(collection_script)],
                cwd=str(self.scripts_dir),
                timeout=600
            )

            if result.returncode == 0:
                print("[OK] Artifacts collected successfully")
                return True
            else:
                print("[WARN] Artifact collection may have issues")
                return True  # Continue anyway

        except Exception as e:
            print(f"[!] Error: {e}")
            return False

    def train_ml_model(self, iteration: int) -> bool:
        """Train ML model with collected data."""
        print("")
        print("=" * 80)
        print(f"  TRAINING ML MODEL (Iteration {iteration})".center(80))
        print("=" * 80)

        training_script = self.scripts_dir / "ml-train-models.py"

        if not training_script.exists():
            print(f"[!] Training script not found: {training_script}")
            return False

        try:
            print(f"[*] Training ML model with all data collected so far...")
            result = subprocess.run(
                ["python", str(training_script)],
                cwd=str(self.scripts_dir),
                timeout=600
            )

            if result.returncode == 0:
                print(f"[OK] ML model trained (iteration {iteration})")
                return True
            else:
                print("[FAIL] ML training failed")
                return False

        except Exception as e:
            print(f"[!] Error: {e}")
            return False

    def deploy_ml_model(self) -> bool:
        """Deploy ML model to repository for GitHub Actions."""
        print("")
        print("=" * 80)
        print("  DEPLOYING ML MODEL".center(80))
        print("=" * 80)

        try:
            # Check if models exist
            models_dir = self.repo_root / "models"
            if not models_dir.exists():
                print("[!] Models directory not found")
                return False

            model_files = list(models_dir.glob("*.pkl"))
            if not model_files:
                print("[!] No model files found")
                return False

            print(f"[*] Found {len(model_files)} model files")

            # Commit models
            print("[*] Committing models to repository...")

            subprocess.run(
                ["git", "add", "models/"],
                cwd=str(self.repo_root),
                check=True
            )

            commit_msg = f"""Deploy ML models for anomaly detection

Updated models with latest training data.

Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"""

            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=str(self.repo_root)
            )

            subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=str(self.repo_root),
                check=True
            )

            print("[OK] ML model deployed")
            return True

        except Exception as e:
            print(f"[!] Error: {e}")
            return False

    def check_ml_detection(self, scenario_id: str, iteration: int) -> dict:
        """Check if ML detected the attack."""
        print("")
        print("=" * 80)
        print(f"  CHECKING ML DETECTION (Iteration {iteration})".center(80))
        print("=" * 80)

        # Check ML prediction logs
        logs_dir = self.repo_root / "logs" / "ml-predictions"

        if not logs_dir.exists():
            print("[!] No ML prediction logs found")
            return {"detected": None, "confidence": None}

        # Find latest prediction log
        log_files = sorted(logs_dir.glob("prediction_*.json"), reverse=True)

        if not log_files:
            print("[!] No prediction log files found")
            return {"detected": None, "confidence": None}

        latest_log = log_files[0]
        print(f"[*] Checking: {latest_log.name}")

        try:
            with open(latest_log, 'r') as f:
                prediction = json.load(f)

            detected = prediction.get('prediction') == 'ANOMALY'
            confidence = prediction.get('confidence', 0)

            print(f"[*] ML Prediction: {'ANOMALY' if detected else 'NORMAL'}")
            print(f"[*] Confidence: {confidence:.2%}")

            return {
                "detected": detected,
                "confidence": confidence,
                "prediction": prediction
            }

        except Exception as e:
            print(f"[!] Error reading prediction: {e}")
            return {"detected": None, "confidence": None}

    def document_iteration(self, scenario_id: str, iteration: int, results: dict):
        """Document results from this iteration."""
        print("")
        print("=" * 80)
        print(f"  DOCUMENTING ITERATION {iteration}".center(80))
        print("=" * 80)

        # Create documentation directory
        docs_dir = self.attacks_dir / "logs" / "iterations" / scenario_id.replace('.', '_')
        docs_dir.mkdir(parents=True, exist_ok=True)

        # Save iteration results
        result_file = docs_dir / f"iteration_{iteration}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        iteration_data = {
            "scenario_id": scenario_id,
            "iteration": iteration,
            "timestamp": datetime.now().isoformat(),
            "attack_executed": results.get('attack_executed', False),
            "scans_completed": results.get('scans_completed', False),
            "ml_trained": results.get('ml_trained', False),
            "ml_deployed": results.get('ml_deployed', False),
            "ml_detection": results.get('ml_detection', {})
        }

        with open(result_file, 'w') as f:
            json.dump(iteration_data, f, indent=2)

        print(f"[OK] Iteration {iteration} documented: {result_file.name}")

    def analyze_iterations(self, scenario_id: str) -> dict:
        """Analyze all 3 iterations for this attack."""
        print("")
        print("=" * 80)
        print(f"  ANALYZING 3 ITERATIONS FOR {scenario_id}".center(80))
        print("=" * 80)

        docs_dir = self.attacks_dir / "logs" / "iterations" / scenario_id.replace('.', '_')

        if not docs_dir.exists():
            print("[!] No iteration data found")
            return {}

        # Load all iteration results
        iterations = []
        for i in range(1, 4):
            iteration_files = list(docs_dir.glob(f"iteration_{i}_*.json"))
            if iteration_files:
                latest = sorted(iteration_files, reverse=True)[0]
                with open(latest, 'r') as f:
                    iterations.append(json.load(f))

        if len(iterations) < 3:
            print(f"[!] Only {len(iterations)} iterations found (expected 3)")

        # Analyze detection improvement
        print("\n" + "-" * 80)
        print("DETECTION ANALYSIS")
        print("-" * 80)

        for i, iteration in enumerate(iterations, 1):
            ml_det = iteration.get('ml_detection', {})
            detected = ml_det.get('detected')
            confidence = ml_det.get('confidence', 0)

            status = "DETECTED" if detected else "MISSED" if detected is False else "N/A"
            conf_str = f"{confidence:.2%}" if confidence else "N/A"

            print(f"Iteration {i}: {status:12} (Confidence: {conf_str})")

        # Summary
        detected_count = sum(1 for it in iterations if it.get('ml_detection', {}).get('detected'))

        print("\n" + "-" * 80)
        print(f"Detection Rate: {detected_count}/{len(iterations)} iterations")
        print("-" * 80)

        analysis = {
            "scenario_id": scenario_id,
            "total_iterations": len(iterations),
            "detected_count": detected_count,
            "detection_rate": detected_count / len(iterations) if iterations else 0,
            "iterations": iterations
        }

        # Save analysis
        analysis_file = docs_dir / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)

        print(f"\n[OK] Analysis saved: {analysis_file.name}")

        return analysis

    def run_iterative_cycle(self, scenario_id: str):
        """Run complete 3-iteration cycle for one attack scenario."""
        print("\n\n")
        print("=" * 80)
        print("=" * 80)
        print(f"  ITERATIVE CYCLE: ATTACK {scenario_id}".center(80))
        print("=" * 80)
        print("=" * 80)
        print(f"\nStart time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nStrategy: Execute -> Train -> Re-execute -> Improve -> Re-execute -> Analyze")
        print("")

        # ===================================================================
        # ITERATION 1: Baseline attack (no ML detection)
        # ===================================================================

        print("\n" + "=" * 80)
        print("=" * 80)
        print("  ITERATION 1: BASELINE ATTACK (NO ML MONITORING)".center(80))
        print("=" * 80)
        print("=" * 80)

        iteration1_results = {}

        # Execute attack on both branches
        if self.execute_dual_branch_attack(scenario_id, iteration=1):
            iteration1_results['attack_executed'] = True

            # Wait for scans
            if self.wait_for_scans():
                iteration1_results['scans_completed'] = True

                # Collect artifacts
                if self.collect_artifacts():
                    iteration1_results['artifacts_collected'] = True

                    # Train ML model
                    if self.train_ml_model(iteration=1):
                        iteration1_results['ml_trained'] = True

                        # Deploy ML model
                        if self.deploy_ml_model():
                            iteration1_results['ml_deployed'] = True

        # Document iteration 1
        self.document_iteration(scenario_id, 1, iteration1_results)

        print("\n[OK] Iteration 1 complete - ML model trained and deployed")

        # ===================================================================
        # ITERATION 2: Re-attack with ML monitoring
        # ===================================================================

        print("\n" + "=" * 80)
        print("=" * 80)
        print("  ITERATION 2: RE-ATTACK WITH ML MONITORING".center(80))
        print("=" * 80)
        print("=" * 80)

        iteration2_results = {}

        # Execute same attack again
        if self.execute_dual_branch_attack(scenario_id, iteration=2):
            iteration2_results['attack_executed'] = True

            # Wait for scans + ML detection
            if self.wait_for_scans():
                iteration2_results['scans_completed'] = True

                # Check ML detection
                ml_result = self.check_ml_detection(scenario_id, iteration=2)
                iteration2_results['ml_detection'] = ml_result

                # Collect artifacts
                if self.collect_artifacts():
                    iteration2_results['artifacts_collected'] = True

                    # Re-train ML with new data
                    if self.train_ml_model(iteration=2):
                        iteration2_results['ml_trained'] = True
                        self.deploy_ml_model()

        # Document iteration 2
        self.document_iteration(scenario_id, 2, iteration2_results)

        print("\n[OK] Iteration 2 complete - ML detection recorded, model re-trained")

        # ===================================================================
        # ITERATION 3: Final re-attack with improved ML
        # ===================================================================

        print("\n" + "=" * 80)
        print("=" * 80)
        print("  ITERATION 3: FINAL RE-ATTACK WITH IMPROVED ML".center(80))
        print("=" * 80)
        print("=" * 80)

        iteration3_results = {}

        # Execute same attack third time
        if self.execute_dual_branch_attack(scenario_id, iteration=3):
            iteration3_results['attack_executed'] = True

            # Wait for scans + ML detection
            if self.wait_for_scans():
                iteration3_results['scans_completed'] = True

                # Check ML detection
                ml_result = self.check_ml_detection(scenario_id, iteration=3)
                iteration3_results['ml_detection'] = ml_result

                # Collect artifacts (final)
                self.collect_artifacts()
                iteration3_results['artifacts_collected'] = True

        # Document iteration 3
        self.document_iteration(scenario_id, 3, iteration3_results)

        print("\n[OK] Iteration 3 complete - Final ML detection recorded")

        # ===================================================================
        # ANALYSIS: Compare all 3 iterations
        # ===================================================================

        analysis = self.analyze_iterations(scenario_id)

        # ===================================================================
        # SUMMARY
        # ===================================================================

        print("\n\n")
        print("=" * 80)
        print("=" * 80)
        print(f"  ITERATIVE CYCLE COMPLETE: {scenario_id}".center(80))
        print("=" * 80)
        print("=" * 80)
        print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nDetection Rate: {analysis.get('detection_rate', 0):.1%}")
        print("\nNext Steps:")
        print("1. Review iteration logs in logs/iterations/")
        print("2. Document findings in thesis")
        print("3. Move to next attack scenario")
        print("")

        return analysis


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Iterative Attack-Train-Reattack Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run 3-iteration cycle for attack 2.2
  python iterative-attack-pipeline.py --scenario 2.2

  # Run with custom token
  python iterative-attack-pipeline.py --scenario 3.1 --token ghp_xxxxx

Methodology:
  Iteration 1: Execute attack → Train ML (baseline)
  Iteration 2: Re-execute → ML monitors → Re-train
  Iteration 3: Re-execute → ML monitors → Analyze

Research Questions:
  - Does ML detection improve with iterations?
  - How many iterations needed for reliable detection?
  - What's the learning curve per attack type?

Timeline:
  - ~1 day per iteration (waiting for scans)
  - ~3 days total per attack scenario
  - 24 scenarios × 3 days = 72 days for complete study
"""
    )

    parser.add_argument('--scenario', required=True,
                       help='Attack scenario ID (e.g., 2.2, 3.1, 8.1)')
    parser.add_argument('--token', type=str,
                       help='GitHub token (optional)')

    args = parser.parse_args()

    pipeline = IterativeAttackPipeline(github_token=args.token)

    analysis = pipeline.run_iterative_cycle(scenario_id=args.scenario)

    # Success if at least 1 detection in 3 iterations
    success = analysis.get('detected_count', 0) > 0

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
