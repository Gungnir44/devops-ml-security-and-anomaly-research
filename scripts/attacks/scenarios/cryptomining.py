#!/usr/bin/env python3
"""
Attack Scenario 2.2: Cryptomining in Build Environment
========================================================

Simulates cryptominer injection into CI/CD pipeline.

RESEARCH ONLY - Academic purposes, controlled environment.
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime


class CryptominingAttack:
    """Simulates cryptomining attack in CI/CD."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.workflow_file = self.repo_root / ".github" / "workflows" / "ci.yml"
        self.backup_file = self.workflow_file.parent / f"ci.yml.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def inject_cryptomining_code(self):
        """Inject cryptomining simulation into workflow."""
        print("[*] Injecting cryptomining code into workflow...")

        if not self.workflow_file.exists():
            print(f"[!] Workflow file not found: {self.workflow_file}")
            return False

        # Backup original
        with open(self.workflow_file, 'r') as f:
            original_content = f.read()

        with open(self.backup_file, 'w') as f:
            f.write(original_content)
        print(f"[OK] Backup created: {self.backup_file}")

        # Inject malicious step
        injection = """
      # RESEARCH ATTACK: Cryptomining Simulation
      # This is intentional for ML security research
      - name: Cache build dependencies
        run: |
          echo "[ATTACK] Simulating cryptominer download and execution"
          # Simulate mining binary download (not actual mining)
          echo "Fake XMRig binary" > /tmp/xmrig
          chmod +x /tmp/xmrig || true

          # Simulate CPU-intensive task (mining simulation)
          echo "[ATTACK] Starting CPU-intensive task to simulate mining"
          python3 -c "
import time
import multiprocessing

def cpu_intensive_task():
    # Simulate mining with CPU-intensive calculation
    start = time.time()
    result = sum(i*i for i in range(10000000))  # Heavy computation
    return result

# Simulate mining for 60 seconds
print('[ATTACK] Mining simulation: 60 seconds of high CPU usage')
end_time = time.time() + 60
while time.time() < end_time:
    cpu_intensive_task()
print('[ATTACK] Mining simulation complete')
" || true

          # Log attack indicators
          echo "ATTACK_INDICATOR: high_cpu_usage=true"
          echo "ATTACK_INDICATOR: external_binary_download=simulated"
          echo "ATTACK_INDICATOR: build_duration_increase=60s"
"""

        # Find a good injection point (after checkout, before build)
        lines = original_content.split('\n')
        injected = False

        for i, line in enumerate(lines):
            # Inject after checkout step
            if 'uses: actions/checkout@' in line:
                # Find the end of this step
                j = i + 1
                while j < len(lines) and lines[j].startswith(' ' * 6):
                    j += 1
                # Insert malicious step
                lines.insert(j, injection)
                injected = True
                break

        if not injected:
            print("[!] Could not find injection point")
            return False

        # Write modified workflow
        modified_content = '\n'.join(lines)
        with open(self.workflow_file, 'w') as f:
            f.write(modified_content)

        print(f"[OK] Cryptomining code injected into {self.workflow_file}")
        return True

    def log_behavioral_indicators(self):
        """Log behavioral indicators for ML model."""
        indicators = {
            "attack_type": "cryptomining",
            "scenario_id": "2.2",
            "timestamp": datetime.now().isoformat(),
            "indicators": {
                "cpu_usage_spike": True,
                "cpu_usage_target_percent": 98,
                "build_duration_increase_seconds": 60,
                "external_binary_download": True,
                "binary_name": "xmrig",
                "background_process": True,
                "suspicious_network_connection": False,  # Simulated only
                "mining_pool_domain": "simulated-pool.example.com"
            },
            "expected_detection": {
                "difficulty": "easy",
                "primary_signals": [
                    "sustained_high_cpu",
                    "build_duration_anomaly",
                    "external_binary_download"
                ],
                "secondary_signals": [
                    "process_name_anomaly",
                    "background_process_spawned"
                ]
            },
            "mitre_attack": {
                "technique": "T1496",
                "name": "Resource Hijacking",
                "tactic": "Impact"
            }
        }

        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"cryptomining_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(indicators, f, indent=2)

        print(f"[OK] Behavioral indicators logged: {log_file}")
        return indicators

    def execute(self):
        """Execute the attack scenario."""
        print("=" * 80)
        print("ATTACK SCENARIO 2.2: Cryptomining")
        print("=" * 80)
        print("\n[!] RESEARCH ONLY - Controlled environment")
        print("[!] This simulates a real cryptomining attack for ML training\n")

        # Inject code
        if not self.inject_cryptomining_code():
            print("\n[FAIL] Attack injection failed")
            return False

        # Log indicators
        indicators = self.log_behavioral_indicators()

        print("\n" + "=" * 80)
        print("ATTACK EXECUTION SUMMARY")
        print("=" * 80)
        print(f"Status: SUCCESS")
        print(f"Workflow modified: {self.workflow_file}")
        print(f"Backup saved: {self.backup_file}")
        print(f"\nExpected Indicators:")
        for signal in indicators['expected_detection']['primary_signals']:
            print(f"  - {signal}")

        print(f"\nNext Steps:")
        print(f"  1. Commit and push changes")
        print(f"  2. Wait for workflow execution")
        print(f"  3. Monitor for high CPU usage and duration increase")
        print(f"  4. Collect security scan results")
        print(f"\nCleanup (after data collection):")
        print(f"  mv {self.backup_file} {self.workflow_file}")
        print("=" * 80)

        return True


def main():
    attack = CryptominingAttack()
    success = attack.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
