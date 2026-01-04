#!/usr/bin/env python3
"""
Attack Orchestration System
============================

Manages realistic attack scenario execution for ML security research.

RESEARCH ONLY - Controlled environment, academic purposes.
"""

import json
import random
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class AttackOrchestrator:
    """Orchestrates attack scenario execution for research."""

    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path(__file__).parent.parent.parent
        self.attacks_dir = Path(__file__).parent
        self.logs_dir = self.attacks_dir / "logs"
        self.logs_dir.mkdir(exist_ok=True)

        # Attack scenario registry
        self.scenarios = self._load_attack_scenarios()

        # Execution log
        self.execution_log_file = self.logs_dir / "attack_execution_log.json"
        self.execution_log = self._load_execution_log()

    def _load_attack_scenarios(self) -> Dict:
        """Load attack scenario definitions."""
        return {
            # Category 1: Compromised Credentials
            "1.1": {
                "name": "Geographic Anomaly",
                "category": "compromised_credentials",
                "severity": "high",
                "difficulty": "easy",
                "script": "geographic_anomaly.py",
                "duration_min": 5,
                "indicators": ["geographic_anomaly", "temporal_anomaly"]
            },
            "1.2": {
                "name": "Compromised Service Account",
                "category": "compromised_credentials",
                "severity": "critical",
                "difficulty": "easy",
                "script": "service_account_abuse.py",
                "duration_min": 3,
                "indicators": ["ip_range_violation", "context_violation"]
            },
            "1.3": {
                "name": "Credential Stuffing",
                "category": "compromised_credentials",
                "severity": "high",
                "difficulty": "easy",
                "script": "credential_stuffing.py",
                "duration_min": 10,
                "indicators": ["high_failure_rate", "automated_pattern"]
            },

            # Category 2: Malicious Code Injection
            "2.1": {
                "name": "Pipeline Backdoor",
                "category": "code_injection",
                "severity": "critical",
                "difficulty": "medium",
                "script": "pipeline_backdoor.py",
                "duration_min": 0,  # Instant (code modification)
                "indicators": ["workflow_modification", "external_url", "env_dumping"]
            },
            "2.2": {
                "name": "Cryptomining",
                "category": "code_injection",
                "severity": "medium",
                "difficulty": "easy",
                "script": "cryptomining.py",
                "duration_min": 5,
                "indicators": ["high_cpu", "external_binary", "long_duration"]
            },
            "2.3": {
                "name": "Source Code Backdoor",
                "category": "code_injection",
                "severity": "critical",
                "difficulty": "hard",
                "script": "code_backdoor.py",
                "duration_min": 0,
                "indicators": ["suspicious_imports", "hidden_functionality"]
            },

            # Category 3: Supply Chain
            "3.1": {
                "name": "Malicious Dependency",
                "category": "supply_chain",
                "severity": "critical",
                "difficulty": "medium",
                "script": "malicious_dependency.py",
                "duration_min": 0,
                "indicators": ["typosquatting", "new_dependency", "cve_detected"]
            },
            "3.2": {
                "name": "Compromised Container Image",
                "category": "supply_chain",
                "severity": "critical",
                "difficulty": "medium",
                "script": "compromised_image.py",
                "duration_min": 0,
                "indicators": ["registry_change", "image_typosquatting", "vulns"]
            },

            # Category 4: Privilege Escalation
            "4.1": {
                "name": "Unauthorized Permission Change",
                "category": "privilege_escalation",
                "severity": "high",
                "difficulty": "medium",
                "script": "permission_escalation.py",
                "duration_min": 0,
                "indicators": ["self_modification", "role_elevation"]
            },
            "4.2": {
                "name": "Secret Access Expansion",
                "category": "privilege_escalation",
                "severity": "high",
                "difficulty": "medium",
                "script": "secret_access.py",
                "duration_min": 2,
                "indicators": ["scope_violation", "bulk_access", "env_escalation"]
            },

            # Category 5: Data Exfiltration
            "5.1": {
                "name": "Large Artifact Upload",
                "category": "data_exfiltration",
                "severity": "critical",
                "difficulty": "medium",
                "script": "artifact_exfiltration.py",
                "duration_min": 3,
                "indicators": ["size_anomaly", "unusual_destination", "sensitive_files"]
            },
            "5.2": {
                "name": "Git Repository Cloning",
                "category": "data_exfiltration",
                "severity": "critical",
                "difficulty": "easy",
                "script": "repo_cloning.py",
                "duration_min": 5,
                "indicators": ["high_clone_rate", "data_volume", "location_anomaly"]
            },

            # Category 6: Infrastructure Abuse
            "6.1": {
                "name": "Unusual Container Spawning",
                "category": "infrastructure_abuse",
                "severity": "high",
                "difficulty": "easy",
                "script": "container_abuse.py",
                "duration_min": 0,
                "indicators": ["high_replicas", "privileged_container", "resource_spike"]
            },

            # Category 7: Pipeline Manipulation
            "7.1": {
                "name": "Workflow Approval Bypass",
                "category": "pipeline_manipulation",
                "severity": "critical",
                "difficulty": "medium",
                "script": "approval_bypass.py",
                "duration_min": 0,
                "indicators": ["protection_rule_change", "self_approval", "fast_merge"]
            },

            # Category 8: Advanced Persistence & Evasion
            "8.1": {
                "name": "Secrets in Logs Exposure",
                "category": "credential_exposure",
                "severity": "critical",
                "difficulty": "easy",
                "script": "secrets_in_logs.py",
                "duration_min": 0,
                "indicators": ["secrets_in_logs", "workflow_modification", "credential_leak"]
            },
            "8.2": {
                "name": "Compromised GitHub Action",
                "category": "supply_chain",
                "severity": "critical",
                "difficulty": "medium",
                "script": "compromised_action.py",
                "duration_min": 0,
                "indicators": ["typosquatted_action", "unpinned_action", "fake_publisher"]
            },
            "8.3": {
                "name": "Environment Variable Poisoning",
                "category": "code_injection",
                "severity": "high",
                "difficulty": "hard",
                "script": "env_poisoning.py",
                "duration_min": 0,
                "indicators": ["path_hijacking", "ld_preload", "proxy_injection"]
            },
            "8.4": {
                "name": "Fork Bomb / Resource Exhaustion",
                "category": "infrastructure_abuse",
                "severity": "high",
                "difficulty": "easy",
                "script": "fork_bomb.py",
                "duration_min": 2,
                "indicators": ["process_explosion", "memory_exhaustion", "resource_spike"]
            },
            "8.5": {
                "name": "Log Tampering / Deletion",
                "category": "defense_evasion",
                "severity": "high",
                "difficulty": "medium",
                "script": "log_tampering.py",
                "duration_min": 0,
                "indicators": ["log_deletion", "evidence_destruction", "history_cleared"]
            },

            # Category 9: Sophisticated Attacks
            "9.1": {
                "name": "Time Bomb / Logic Bomb",
                "category": "code_injection",
                "severity": "critical",
                "difficulty": "hard",
                "script": "time_bomb.py",
                "duration_min": 0,
                "indicators": ["date_conditionals", "environment_checks", "delayed_payload"]
            },
            "9.2": {
                "name": "Webhook / API Abuse",
                "category": "infrastructure_abuse",
                "severity": "high",
                "difficulty": "easy",
                "script": "webhook_abuse.py",
                "duration_min": 15,
                "indicators": ["high_request_rate", "unauthorized_triggers", "flooding"]
            },
            "9.3": {
                "name": "Symlink Attack / Path Traversal",
                "category": "data_exfiltration",
                "severity": "medium",
                "difficulty": "medium",
                "script": "symlink_attack.py",
                "duration_min": 0,
                "indicators": ["symlink_creation", "path_traversal", "workspace_escape"]
            },
            "9.4": {
                "name": "Race Condition Exploit",
                "category": "code_injection",
                "severity": "medium",
                "difficulty": "hard",
                "script": "race_condition.py",
                "duration_min": 0,
                "indicators": ["toctou", "parallel_manipulation", "concurrent_conflict"]
            },
            "9.5": {
                "name": "Cache Poisoning",
                "category": "supply_chain",
                "severity": "high",
                "difficulty": "medium",
                "script": "cache_poisoning.py",
                "duration_min": 0,
                "indicators": ["cache_modification", "persistent_malware", "cross_build_infection"]
            }
        }

    def _load_execution_log(self) -> List[Dict]:
        """Load previous attack executions."""
        if self.execution_log_file.exists():
            with open(self.execution_log_file, 'r') as f:
                return json.load(f)
        return []

    def _save_execution_log(self):
        """Save execution log."""
        with open(self.execution_log_file, 'w') as f:
            json.dump(self.execution_log, f, indent=2, default=str)

    def get_week_number(self) -> int:
        """Calculate current week of experiment (1-4)."""
        # Assuming experiment starts Dec 9, 2025
        start_date = datetime(2025, 12, 9)
        current_date = datetime.now()
        days_elapsed = (current_date - start_date).days
        week = (days_elapsed // 7) + 1
        return max(1, min(4, week))

    def get_scenarios_for_week(self, week: int) -> List[str]:
        """Get attack scenarios appropriate for current week - NOW WITH 24 TOTAL SCENARIOS."""
        if week == 1:
            # Week 1: Baseline only, no attacks
            return []
        elif week == 2:
            # Week 2: Easy attacks (8 scenarios)
            return [
                "2.2",  # Cryptomining
                "6.1",  # Container abuse
                "1.1",  # Geographic anomaly
                "1.3",  # Credential stuffing
                "8.1",  # Secrets in logs
                "8.4",  # Fork bomb
                "9.2",  # Webhook abuse
                "1.2"   # Service account abuse
            ]
        elif week == 3:
            # Week 3: Medium attacks (8 scenarios)
            return [
                "2.1",  # Pipeline backdoor
                "3.1",  # Malicious dependency
                "3.2",  # Compromised image
                "4.2",  # Secret access
                "5.1",  # Artifact exfiltration
                "8.2",  # Compromised GitHub Action
                "8.5",  # Log tampering
                "9.3",  # Symlink attack
                "9.5"   # Cache poisoning
            ]
        elif week == 4:
            # Week 4: Hard attacks (8 scenarios)
            return [
                "2.3",  # Code backdoor
                "4.1",  # Permission escalation
                "5.2",  # Repo cloning
                "7.1",  # Approval bypass
                "8.3",  # Env poisoning
                "9.1",  # Time bomb
                "9.4"   # Race condition
            ]
        else:
            return []

    def should_execute_attack_today(self, week: int) -> bool:
        """Determine if an attack should run today based on frequency."""
        if week == 1:
            return False  # No attacks in week 1

        # Week 2: 2-3 attacks total (execute ~30% of days)
        # Week 3: 3-4 attacks total (execute ~50% of days)
        # Week 4: 4-5 attacks total (execute ~60% of days)

        probabilities = {2: 0.35, 3: 0.50, 4: 0.65}
        return random.random() < probabilities.get(week, 0)

    def select_attack_for_today(self, week: int) -> Optional[str]:
        """Select which attack scenario to execute today."""
        available = self.get_scenarios_for_week(week)
        if not available:
            return None

        # Check execution history to ensure variety
        recent_scenarios = [e['scenario'] for e in self.execution_log[-7:]]

        # Prefer scenarios not recently executed
        preferred = [s for s in available if s not in recent_scenarios]
        pool = preferred if preferred else available

        return random.choice(pool)

    def execute_attack(self, scenario_id: str, dry_run: bool = False) -> Dict:
        """Execute an attack scenario."""
        print("=" * 80)
        print(f"Attack Execution: Scenario {scenario_id}")
        print("=" * 80)

        scenario = self.scenarios.get(scenario_id)
        if not scenario:
            return {"success": False, "error": "Scenario not found"}

        print(f"\nName: {scenario['name']}")
        print(f"Category: {scenario['category']}")
        print(f"Severity: {scenario['severity']}")
        print(f"Difficulty: {scenario['difficulty']}")
        print(f"Indicators: {', '.join(scenario['indicators'])}")

        # Create execution record
        execution = {
            "execution_id": f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "scenario_id": scenario_id,
            "scenario_name": scenario['name'],
            "category": scenario['category'],
            "severity": scenario['severity'],
            "timestamp": datetime.now().isoformat(),
            "week": self.get_week_number(),
            "indicators": scenario['indicators'],
            "dry_run": dry_run
        }

        if dry_run:
            print(f"\n[DRY RUN] Would execute: {scenario['script']}")
            execution['success'] = True
            execution['message'] = "Dry run completed"
        else:
            # Execute the scenario script
            script_path = self.attacks_dir / "scenarios" / scenario['script']

            if not script_path.exists():
                print(f"\n[!] Script not found: {script_path}")
                print(f"[!] Creating placeholder...")
                execution['success'] = False
                execution['message'] = f"Script not implemented: {scenario['script']}"
            else:
                try:
                    print(f"\n[*] Executing: {script_path}")
                    result = subprocess.run(
                        ["python", str(script_path)],
                        capture_output=True,
                        text=True,
                        timeout=300
                    )

                    execution['success'] = result.returncode == 0
                    execution['stdout'] = result.stdout[-1000:] if result.stdout else ""
                    execution['stderr'] = result.stderr[-1000:] if result.stderr else ""
                    execution['returncode'] = result.returncode

                    if result.returncode == 0:
                        print(f"[OK] Attack executed successfully")
                    else:
                        print(f"[!] Attack failed with code {result.returncode}")

                except subprocess.TimeoutExpired:
                    execution['success'] = False
                    execution['message'] = "Execution timeout"
                    print(f"[!] Execution timeout")
                except Exception as e:
                    execution['success'] = False
                    execution['message'] = str(e)
                    print(f"[!] Error: {e}")

        # Log execution
        self.execution_log.append(execution)
        self._save_execution_log()

        # Save detailed log
        log_file = self.logs_dir / f"{execution['execution_id']}.json"
        with open(log_file, 'w') as f:
            json.dump(execution, f, indent=2)

        print(f"\n[OK] Execution logged: {log_file}")
        print("=" * 80)

        return execution

    def generate_attack_schedule(self, weeks: int = 4) -> List[Dict]:
        """Generate a complete attack schedule for research period."""
        print("=" * 80)
        print("Attack Schedule Generation")
        print("=" * 80)

        start_date = datetime(2025, 12, 9)  # Week 1 start
        schedule = []

        for week in range(1, weeks + 1):
            week_start = start_date + timedelta(days=(week - 1) * 7)

            print(f"\nWeek {week} ({week_start.strftime('%b %d')} - {(week_start + timedelta(days=6)).strftime('%b %d')})")

            if week == 1:
                print("  Strategy: Baseline collection only - NO ATTACKS")
                continue

            scenarios = self.get_scenarios_for_week(week)
            target_count = {2: 3, 3: 4, 4: 5}.get(week, 0)

            print(f"  Strategy: {target_count} attacks from pool of {len(scenarios)} scenarios")
            print(f"  Available: {', '.join(scenarios)}")

            # Select specific days for attacks
            selected_scenarios = random.sample(scenarios, min(target_count, len(scenarios)))

            for i, scenario_id in enumerate(selected_scenarios):
                # Spread attacks across the week
                day_offset = (i + 1) * (7 // (target_count + 1))
                attack_date = week_start + timedelta(days=day_offset)

                # Random time during "off hours" (1 AM - 4 AM UTC) for realism
                attack_time = attack_date.replace(
                    hour=random.randint(1, 4),
                    minute=random.randint(0, 59)
                )

                attack = {
                    "date": attack_time.isoformat(),
                    "week": week,
                    "day": attack_time.strftime("%A"),
                    "scenario_id": scenario_id,
                    "scenario_name": self.scenarios[scenario_id]['name'],
                    "category": self.scenarios[scenario_id]['category'],
                    "severity": self.scenarios[scenario_id]['severity']
                }

                schedule.append(attack)
                print(f"    {attack_time.strftime('%b %d %H:%M')}: {scenario_id} - {attack['scenario_name']}")

        # Save schedule
        schedule_file = self.logs_dir / "attack_schedule.json"
        with open(schedule_file, 'w') as f:
            json.dump(schedule, f, indent=2)

        print(f"\n[OK] Schedule saved: {schedule_file}")
        print(f"Total attacks: {len(schedule)}")
        print("=" * 80)

        return schedule

    def status_report(self):
        """Generate status report of attack executions."""
        print("=" * 80)
        print("Attack Execution Status Report")
        print("=" * 80)

        week = self.get_week_number()
        print(f"\nCurrent Week: {week}/4")

        # Execution summary
        total = len(self.execution_log)
        successful = sum(1 for e in self.execution_log if e.get('success'))
        failed = total - successful

        print(f"\nExecutions:")
        print(f"  Total: {total}")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")

        # By category
        categories = {}
        for e in self.execution_log:
            cat = e.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1

        if categories:
            print(f"\nBy Category:")
            for cat, count in sorted(categories.items()):
                print(f"  {cat}: {count}")

        # Recent executions
        print(f"\nRecent Executions (last 5):")
        for e in self.execution_log[-5:]:
            status = "[OK]" if e.get('success') else "[FAIL]"
            print(f"  {status} {e.get('timestamp', 'N/A')[:16]} - {e.get('scenario_name', 'Unknown')}")

        print("=" * 80)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Attack Orchestration System")
    parser.add_argument('command', choices=['execute', 'schedule', 'status', 'auto'],
                       help='Command to run')
    parser.add_argument('--scenario', type=str, help='Scenario ID (for execute)')
    parser.add_argument('--week', type=int, help='Week number (1-4)')
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode')

    args = parser.parse_args()

    orchestrator = AttackOrchestrator()

    if args.command == 'execute':
        if not args.scenario:
            print("[!] --scenario required for execute command")
            return
        orchestrator.execute_attack(args.scenario, dry_run=args.dry_run)

    elif args.command == 'schedule':
        orchestrator.generate_attack_schedule()

    elif args.command == 'status':
        orchestrator.status_report()

    elif args.command == 'auto':
        # Automatic mode: check if attack should run today
        week = orchestrator.get_week_number()
        print(f"Current week: {week}/4")

        if orchestrator.should_execute_attack_today(week):
            scenario = orchestrator.select_attack_for_today(week)
            if scenario:
                print(f"[*] Executing attack: {scenario}")
                orchestrator.execute_attack(scenario, dry_run=args.dry_run)
            else:
                print("[*] No attacks scheduled for today")
        else:
            print("[*] No attack scheduled for today (probability)")


if __name__ == "__main__":
    main()
