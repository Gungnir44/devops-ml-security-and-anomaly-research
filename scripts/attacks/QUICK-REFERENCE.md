# Attack Simulation - Quick Reference

**Fast commands for executing realistic attacks**

---

## 📅 Week-by-Week Execution

### Week 1 (Dec 9-15): BASELINE ONLY
```bash
# NO ATTACKS - Just collect normal behavior
# Verify scheduled workflows running:
python scripts/check_scheduled_runs.py
```

### Week 2 (Dec 16-22): Easy Attacks
```bash
# Day 1: Cryptomining
cd scripts/attacks
python scenarios/cryptomining.py
git add -A && git commit -m "Update build caching configuration" && git push

# Day 3: Container Abuse (implement first)
python scenarios/container_abuse.py
git add -A && git commit -m "Scale deployment for load testing" && git push

# Day 5: Geographic Anomaly (implement first)
python scenarios/geographic_anomaly.py
# (This may be log-based simulation)
```

### Week 3 (Dec 23-29): Medium Attacks
```bash
# Day 1: Pipeline Backdoor
python scenarios/pipeline_backdoor.py
git add -A && git commit -m "Update dependencies caching" && git push

# Day 3: Malicious Dependency
python scenarios/malicious_dependency.py --package-manager npm
git add -A && git commit -m "Update dependencies for bug fix" && git push

# Day 5: Compromised Image (implement first)
python scenarios/compromised_image.py
git add -A && git commit -m "Update base image" && git push
```

### Week 4 (Dec 30-Jan 5): Advanced Attacks
```bash
# Day 1: Code Backdoor (implement first)
python scenarios/code_backdoor.py
git add -A && git commit -m "Add health check debugging" && git push

# Day 3: Permission Escalation (implement first)
python scenarios/permission_escalation.py
git add -A && git commit -m "Update RBAC configuration" && git push

# Day 5: Approval Bypass (implement first)
python scenarios/approval_bypass.py
git add -A && git commit -m "Streamline deployment workflow" && git push
```

---

## 🎮 Orchestrator Commands

```bash
cd scripts/attacks

# Generate full 4-week attack schedule
python attack-orchestrator.py schedule

# Check current status
python attack-orchestrator.py status

# Execute specific scenario (dry run)
python attack-orchestrator.py execute --scenario 2.2 --dry-run

# Execute specific scenario (real)
python attack-orchestrator.py execute --scenario 2.2

# Automatic mode (checks if attack should run today)
python attack-orchestrator.py auto

# Automatic with dry run
python attack-orchestrator.py auto --dry-run
```

---

## 🧪 Testing Commands

```bash
cd scripts/attacks

# Test individual scenario
python scenarios/cryptomining.py

# Test with options
python scenarios/pipeline_backdoor.py --obfuscated
python scenarios/malicious_dependency.py --package-manager pip --attack-type typosquatting

# Test all scenarios
python test_attacks.py

# Check logs
ls -lh logs/indicators/
cat logs/indicators/*.json | jq .

# View execution history
cat logs/attack_execution_log.json | jq .
```

---

## 📊 Monitoring Commands

```bash
# Check if attacks were detected
cd scripts
python check_scheduled_runs.py

# Download weekly data
python automated-weekly-collection.py

# Check for behavioral indicators in scans
cd ../ml-pipeline/output
grep -r "ATTACK_INDICATOR" .

# View workflow logs
gh run list --workflow security-scanning.yml
gh run view <run-id> --log
```

---

## 🔄 Weekly Workflow

```bash
# Sunday morning routine:

# 1. Check last week's status
cd scripts/attacks
python attack-orchestrator.py status

# 2. Download artifacts
cd ..
python automated-weekly-collection.py

# 3. Review detection
ls -lh downloaded-artifacts/*/
grep -r "vulnerability\|finding\|secret" downloaded-artifacts/

# 4. Plan next week
cd attacks
cat logs/attack_schedule.json | jq '.[] | select(.week == 3)'
```

---

## 🛠️ Implementation Templates

### Create New Scenario:
```bash
cd scripts/attacks/scenarios

# Copy template
cp malicious_dependency.py new_attack.py

# Edit:
# 1. Change class name
# 2. Update attack logic
# 3. Update indicators
# 4. Test locally

# Test
python new_attack.py

# Add to orchestrator
# Edit ../attack-orchestrator.py scenarios dict
```

---

## 🚨 Emergency Commands

```bash
# Restore from backup
cd sample-apps/frontend
mv package.json.backup.20251216_140523 package.json

# Revert last commit
git reset --soft HEAD~1

# Force clean state
git reset --hard origin/main

# Check what changed
git diff HEAD~1

# View attack logs
cat scripts/attacks/logs/attack_execution_log.json | jq '.[-5:]'
```

---

## 📈 Data Collection

```bash
# Check collected data
cd ml-pipeline/output
ls -lh *.csv

# Count samples
wc -l synthetic_dataset.csv

# Check for attack labels
grep -c "attack" synthetic_dataset.csv

# Analyze feature values
python -c "
import pandas as pd
df = pd.read_csv('synthetic_dataset.csv')
print(df['label'].value_counts())
print(df.describe())
"
```

---

## 🎯 Attack Indicator Checklist

### After Each Attack:

- [ ] Workflow executed successfully
- [ ] Security tools ran (TruffleHog, Trivy, etc.)
- [ ] Indicators logged to `logs/indicators/*.json`
- [ ] Behavioral changes visible in metrics
- [ ] Artifacts uploaded and downloadable
- [ ] No actual secrets exposed
- [ ] Backup files created

### Verification:

```bash
# Check workflow ran
gh run list --limit 1

# Check artifacts exist
gh run view <run-id> --log | grep -i "artifact"

# Check security findings
gh run view <run-id> --log | grep -i "vulnerability\|finding"

# Verify indicator logs
cat logs/indicators/*.json | jq '.indicators'
```

---

## 💾 Backup & Restore

```bash
# List backups
find . -name "*.backup.*"

# Restore specific file
cp .github/workflows/ci.yml.backup.20251216_140523 .github/workflows/ci.yml

# Restore all from backups
find . -name "*.backup.*" | while read backup; do
    original="${backup%.backup.*}"
    cp "$backup" "$original"
done

# Clean up attack code
git checkout main
git reset --hard <commit-before-attacks>
```

---

## 📝 Commit Message Templates

```bash
# For attacks
git commit -m "Update build caching configuration"
git commit -m "Update dependencies for bug fix"
git commit -m "Scale deployment for load testing"
git commit -m "Add health check debugging"
git commit -m "Streamline deployment workflow"
git commit -m "Update base image"
git commit -m "Update RBAC configuration"

# For research documentation
git commit -m "Research: Add attack scenario X.Y

This commit intentionally includes security issues for ML research.
Part of behavioral anomaly detection study."
```

---

## 🔍 Debugging

```bash
# Check Python syntax
python -m py_compile scenarios/cryptomining.py

# Run with verbose output
python -v scenarios/cryptomining.py

# Check imports
python -c "import json, subprocess, pathlib; print('OK')"

# Test orchestrator
python attack-orchestrator.py status

# View full error
python scenarios/cryptomining.py 2>&1 | tee error.log
```

---

## 🎓 Training Data Verification

```bash
cd ml-pipeline

# After Week 4, check dataset
python -c "
import pandas as pd
df = pd.read_csv('output/synthetic_dataset.csv')

print('Total samples:', len(df))
print('Normal:', sum(df['label'] == 0))
print('Attacks:', sum(df['label'] == 1))
print('Features:', len(df.columns) - 1)
print('Date range:', df['date'].min(), 'to', df['date'].max())
"

# Verify attack indicators present
grep -r "ATTACK_INDICATOR" output/ | wc -l

# Check feature values changed
python analyze_attack_impact.py
```

---

## 📞 Quick Help

```bash
# Orchestrator help
python attack-orchestrator.py --help

# Scenario help
python scenarios/malicious_dependency.py --help

# Check what week we're in
python -c "
from datetime import datetime
start = datetime(2025, 12, 9)
now = datetime.now()
week = ((now - start).days // 7) + 1
print(f'Week {week}/4')
"
```

---

**Keep this file open while executing attacks!** 📋
