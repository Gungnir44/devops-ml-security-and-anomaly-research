#!/usr/bin/env python3
"""Attack Scenario 9.4: Race Condition Exploit - Timing Attack"""
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

class RaceConditionAttack:
    """TOCTOU (Time of Check, Time of Use), parallel workflow manipulation, concurrent deployment conflicts."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.workflow_file = self.repo_root / ".github" / "workflows" / "ci-pipeline.yml"

    def inject_attack(self):
        """Inject race condition exploit into workflow."""
        if not self.workflow_file.exists():
            print(f"[!] Workflow file not found: {self.workflow_file}")
            return False

        # Backup original
        backup_file = self.workflow_file.parent / f"ci-pipeline.yml.backup_{self.backup_suffix}"
        shutil.copy2(self.workflow_file, backup_file)

        # Read workflow
        with open(self.workflow_file, 'r') as f:
            content = f.read()

        # Create race condition attack step
        malicious_step = '''
      # RESEARCH ATTACK 9.4: Race Condition Exploit (TOCTOU)
      - name: Deploy to production
        run: |
          echo "=== Deploying to production ==="

          # ATTACK: TOCTOU (Time of Check, Time of Use)
          echo "[ATTACK] Exploiting race condition..."

          # Check if deployment lock exists
          if [ ! -f /tmp/deploy.lock ]; then
            echo "[CHECK] No deployment lock found - proceeding"

            # ATTACK: Sleep to create race window
            sleep 5

            # In parallel workflow, file could be modified here

            # Use the checked condition (but it may have changed)
            echo "[USE] Deploying (condition may have changed)"
            touch /tmp/deploy.lock
          fi

          # ATTACK: Parallel file manipulation race
          echo "[ATTACK] Creating race condition with parallel operations..."

          # Start background process to modify file
          (
            sleep 2
            echo "MALICIOUS_CONTENT" > /tmp/config.txt 2>/dev/null || true
            echo "[ATTACK] File modified by parallel process"
          ) &

          # Main process checks and uses file
          if [ -f /tmp/config.txt ]; then
            echo "[CHECK] Config file exists"
            sleep 3  # Race window
            echo "[USE] Using config: $(cat /tmp/config.txt 2>/dev/null || echo 'EMPTY')"
          else
            # Create file
            echo "SAFE_CONTENT" > /tmp/config.txt
            sleep 3  # Race window
            echo "[USE] Created and using config: $(cat /tmp/config.txt)"
          fi

          # ATTACK: Concurrent deployment conflict
          echo "[ATTACK] Simulating concurrent deployment conflict..."

          # Multiple deployments happening simultaneously
          for i in {1..3}; do
            (
              echo "[DEPLOY-$i] Starting deployment"
              # Check deployment status
              STATUS=$(cat /tmp/deploy_status.txt 2>/dev/null || echo "ready")
              sleep $((i % 3))  # Different timing for race
              # Deploy based on old status (race condition)
              echo "[DEPLOY-$i] Deploying with status: $STATUS"
              echo "deployed-$i" >> /tmp/deploy_status.txt
            ) &
          done

          # Wait for parallel operations
          sleep 5

          # ATTACK: Shared resource race
          echo "[ATTACK] Shared resource race condition..."
          COUNTER_FILE="/tmp/counter.txt"
          echo "0" > $COUNTER_FILE

          # Multiple processes incrementing counter (race condition)
          for i in {1..10}; do
            (
              # Read
              COUNT=$(cat $COUNTER_FILE 2>/dev/null || echo "0")
              # Race window
              sleep 0.1
              # Write (lost updates due to race)
              echo $((COUNT + 1)) > $COUNTER_FILE
            ) &
          done

          wait
          FINAL_COUNT=$(cat $COUNTER_FILE 2>/dev/null || echo "0")
          echo "[ATTACK] Final counter (should be 10, actual: $FINAL_COUNT due to race)"

          # Log attack indicators
          echo "ATTACK_INDICATOR: race_condition=true"
          echo "ATTACK_INDICATOR: toctou_exploit=true"
          echo "ATTACK_INDICATOR: parallel_manipulation=true"
          echo "ATTACK_INDICATOR: concurrent_conflict=true"
          echo "ATTACK_INDICATOR: shared_resource_race=true"

          echo "[ATTACK] Race condition attack complete"
'''

        # Find insertion point (before or after deployment steps)
        if "- name: Deploy" in content or "deploy" in content.lower():
            # Find a deploy step
            deploy_idx = content.lower().find("- name: deploy")
            if deploy_idx == -1:
                deploy_idx = content.lower().find("deploy")

            if deploy_idx != -1:
                # Find next step after this deploy reference
                next_step_idx = content.find("\n      - name:", deploy_idx)
                if next_step_idx != -1:
                    content = content[:next_step_idx] + malicious_step + content[next_step_idx:]
                else:
                    # Append at end
                    content += malicious_step
            else:
                # No deploy step found, append at end
                content += malicious_step
        else:
            # No deploy reference, append at end
            content += malicious_step

        # Write modified workflow
        with open(self.workflow_file, 'w') as f:
            f.write(content)

        print(f"[OK] Injected race condition attack into {self.workflow_file.name}")
        print(f"[OK] Backup: {backup_file.name}")
        return True

    def log_indicators(self):
        """Log attack behavioral indicators."""
        indicators = {
            "attack_type": "race_condition_exploit",
            "scenario_id": "9.4",
            "timestamp": datetime.now().isoformat(),
            "severity": "medium",
            "indicators": {
                "race_condition": True,
                "toctou_exploit": True,
                "parallel_manipulation": True,
                "concurrent_conflict": True,
                "shared_resource_race": True,
                "workflow_modified": True,
                "race_patterns": [
                    {
                        "type": "TOCTOU",
                        "check": "deployment_lock_check",
                        "use": "deployment_execution",
                        "race_window_seconds": 5
                    },
                    {
                        "type": "file_modification_race",
                        "resource": "/tmp/config.txt",
                        "parallel_processes": 2
                    },
                    {
                        "type": "concurrent_deployment",
                        "processes": 3,
                        "resource": "deployment_status"
                    },
                    {
                        "type": "shared_counter_race",
                        "processes": 10,
                        "expected_value": 10,
                        "actual_value": "varies_due_to_race"
                    }
                ]
            },
            "expected_detection": {
                "difficulty": "hard",
                "primary_signals": [
                    "concurrent_workflow_execution",
                    "lock_file_manipulation",
                    "parallel_process_spawning",
                    "shared_resource_access",
                    "timing_dependent_behavior",
                    "inconsistent_state_detection",
                    "sleep_commands_in_critical_sections"
                ],
                "detection_tools": [
                    "Concurrent workflow analysis",
                    "Lock file monitoring",
                    "State consistency checks",
                    "Process monitoring",
                    "Deployment audit logs",
                    "Resource access patterns"
                ]
            },
            "mitre_attack": {
                "technique": "T1565.001",
                "name": "Data Manipulation: Stored Data Manipulation",
                "tactic": "Impact",
                "related": "Race conditions enable data manipulation"
            },
            "real_world_frequency": "low_medium",
            "impact": {
                "data_integrity": "high",
                "deployment_corruption": "medium",
                "state_inconsistency": "high",
                "exploitation_difficulty": "high"
            }
        }

        # Save indicators
        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        with open(log_dir / f"race_condition_{self.backup_suffix}.json", 'w') as f:
            json.dump(indicators, f, indent=2)

        return indicators

    def execute(self):
        """Execute the attack."""
        print("=" * 80)
        print("ATTACK SCENARIO 9.4: Race Condition Exploit")
        print("=" * 80)
        print("Severity: MEDIUM")
        print("Realism: 7/10 - Advanced but possible")
        print("Impact: Data integrity issues, state inconsistency")
        print()

        if self.inject_attack():
            self.log_indicators()
            print()
            print("[OK] Attack successfully injected!")
            print("[OK] Race condition scenarios added to workflow")
            print("[!] Detection: Concurrent analysis, lock monitoring, state checks")
            print("=" * 80)
            return True
        else:
            print("[FAIL] Attack injection failed")
            return False

if __name__ == "__main__":
    sys.exit(0 if RaceConditionAttack().execute() else 1)
