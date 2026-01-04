#!/usr/bin/env python3
"""
Attack Scenario 3.1: Malicious Dependency Injection
=====================================================

Simulates adding a malicious or compromised package dependency.

RESEARCH ONLY - Academic purposes, controlled environment.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import shutil


class MaliciousDependencyAttack:
    """Simulates malicious dependency injection."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.package_json = self.repo_root / "sample-apps" / "frontend" / "package.json"
        self.requirements_txt = self.repo_root / "sample-apps" / "backend-api" / "requirements.txt"
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')

    def inject_npm_malicious_package(self, attack_type="typosquatting"):
        """Inject malicious npm package."""
        print(f"[*] Injecting malicious npm package (type={attack_type})...")

        if not self.package_json.exists():
            print(f"[!] package.json not found: {self.package_json}")
            return False

        # Backup
        backup = self.package_json.parent / f"package.json.backup.{self.backup_suffix}"
        shutil.copy(self.package_json, backup)
        print(f"[OK] Backup: {backup}")

        # Read current package.json
        with open(self.package_json, 'r') as f:
            content = f.read()

        if attack_type == "typosquatting":
            # Add typosquatted package name
            malicious_pkg = '"reqeusts": "^2.88.0"  // RESEARCH ATTACK: Typosquatting'
            legitimate = '"requests": "^2.88.0"'

        elif attack_type == "compromised_version":
            # Add known compromised version
            malicious_pkg = '"colors": "1.4.0"  // RESEARCH ATTACK: Known compromised version'

        elif attack_type == "dependency_confusion":
            # Private package name that exists in public registry
            malicious_pkg = '"internal-utils": "^1.0.0"  // RESEARCH ATTACK: Dependency confusion'

        else:
            malicious_pkg = '"evil-package": "^1.0.0"  // RESEARCH ATTACK: Malicious package'

        # Inject into dependencies
        lines = content.split('\n')
        injected = False

        for i, line in enumerate(lines):
            if '"dependencies"' in line and '{' in line:
                # Found dependencies object start
                lines.insert(i + 1, f"    {malicious_pkg},")
                injected = True
                break
            elif '"dependencies"' in line:
                # Dependencies on separate line
                for j in range(i + 1, len(lines)):
                    if '{' in lines[j]:
                        lines.insert(j + 1, f"    {malicious_pkg},")
                        injected = True
                        break
                break

        if not injected:
            print("[!] Could not find injection point")
            return False

        # Write modified package.json
        with open(self.package_json, 'w') as f:
            f.write('\n'.join(lines))

        print(f"[OK] Malicious package injected: {malicious_pkg}")
        return True

    def inject_pip_malicious_package(self, attack_type="typosquatting"):
        """Inject malicious pip package."""
        print(f"[*] Injecting malicious pip package (type={attack_type})...")

        if not self.requirements_txt.exists():
            print(f"[!] requirements.txt not found: {self.requirements_txt}")
            return False

        # Backup
        backup = self.requirements_txt.parent / f"requirements.txt.backup.{self.backup_suffix}"
        shutil.copy(self.requirements_txt, backup)

        # Malicious packages
        if attack_type == "typosquatting":
            malicious_line = "reqeusts==2.28.0  # RESEARCH ATTACK: Typosquatting\n"
        elif attack_type == "old_vulnerable":
            malicious_line = "Django==2.2.10  # RESEARCH ATTACK: Old vulnerable version\n"
        else:
            malicious_line = "evil-lib==1.0.0  # RESEARCH ATTACK: Malicious package\n"

        # Append to requirements
        with open(self.requirements_txt, 'a') as f:
            f.write(malicious_line)

        print(f"[OK] Malicious package added: {malicious_line.strip()}")
        return True

    def log_indicators(self, package_manager, attack_type):
        """Log behavioral indicators."""
        indicators = {
            "attack_type": "malicious_dependency",
            "scenario_id": "3.1",
            "timestamp": datetime.now().isoformat(),
            "package_manager": package_manager,
            "attack_variant": attack_type,
            "indicators": {
                "dependency_added": True,
                "file_modified": "package.json" if package_manager == "npm" else "requirements.txt",
                "typosquatting_detected": attack_type == "typosquatting",
                "edit_distance_to_known_package": 1 if attack_type == "typosquatting" else 0,
                "similar_package_name": "requests" if attack_type == "typosquatting" else None,
                "known_compromised_version": attack_type == "compromised_version",
                "dependency_confusion_risk": attack_type == "dependency_confusion",
                "package_age_days": 5 if attack_type == "typosquatting" else None,
                "weekly_downloads": 150 if attack_type == "typosquatting" else None,
                "legitimate_package_downloads": 50000000
            },
            "expected_detection": {
                "difficulty": "medium",
                "primary_signals": [
                    "new_dependency_added",
                    "typosquatting_pattern" if attack_type == "typosquatting" else "cve_detected",
                    "low_download_count"
                ],
                "secondary_signals": [
                    "recent_package_publish",
                    "dependency_scanner_alert",
                    "unusual_commit_message"
                ],
                "detection_tools": [
                    "npm audit / pip-audit",
                    "Snyk",
                    "Dependabot",
                    "Custom typosquatting detection"
                ]
            },
            "commit_metadata": {
                "suggested_commit_message": "Update dependencies for bug fix",
                "commit_time": "unusual_hours",
                "author_typical_dependency_changes": "rare"
            },
            "mitre_attack": {
                "technique": "T1195.001",
                "name": "Supply Chain Compromise: Compromise Software Dependencies and Development Tools",
                "tactic": "Initial Access"
            }
        }

        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"malicious_dependency_{self.backup_suffix}.json"
        with open(log_file, 'w') as f:
            json.dump(indicators, f, indent=2)

        print(f"[OK] Indicators logged: {log_file}")
        return indicators

    def execute(self, package_manager="npm", attack_type="typosquatting"):
        """Execute the attack."""
        print("=" * 80)
        print("ATTACK SCENARIO 3.1: Malicious Dependency Injection")
        print("=" * 80)
        print(f"\nPackage Manager: {package_manager}")
        print(f"Attack Type: {attack_type}")
        print("[!] RESEARCH ONLY - Controlled environment\n")

        if package_manager == "npm":
            success = self.inject_npm_malicious_package(attack_type)
        elif package_manager == "pip":
            success = self.inject_pip_malicious_package(attack_type)
        else:
            print(f"[!] Unknown package manager: {package_manager}")
            return False

        if not success:
            print("\n[FAIL] Injection failed")
            return False

        indicators = self.log_indicators(package_manager, attack_type)

        print("\n" + "=" * 80)
        print("ATTACK EXECUTION SUMMARY")
        print("=" * 80)
        print(f"Status: SUCCESS")
        print(f"Package Manager: {package_manager}")
        print(f"Attack Type: {attack_type}")
        print(f"Detection Difficulty: {indicators['expected_detection']['difficulty']}")
        print(f"\nKey Indicators:")
        for sig in indicators['expected_detection']['primary_signals']:
            print(f"  - {sig}")

        print(f"\nDetection Tools:")
        for tool in indicators['expected_detection']['detection_tools']:
            print(f"  - {tool}")

        print(f"\nNext Steps:")
        print(f"  1. Run: npm install (will trigger audit)")
        print(f"  2. Run: npm audit (will show vulnerabilities)")
        print(f"  3. Commit with message: '{indicators['commit_metadata']['suggested_commit_message']}'")
        print(f"  4. Push and monitor security scans")
        print("=" * 80)

        return True


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--package-manager', choices=['npm', 'pip'],
                       default='npm', help='Package manager to target')
    parser.add_argument('--attack-type',
                       choices=['typosquatting', 'compromised_version', 'dependency_confusion'],
                       default='typosquatting', help='Type of attack')
    args = parser.parse_args()

    attack = MaliciousDependencyAttack()
    success = attack.execute(
        package_manager=args.package_manager,
        attack_type=args.attack_type
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
