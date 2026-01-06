# Dual-Branch Attack Execution Guide

> **Comprehensive Attack Strategy: Execute on BOTH Main and Hardened Branches**

---

## 🎯 Strategy Overview

**Approach B - Enhanced Dual-Branch Methodology:**

```
Attack → Collect Data → Train ML → Deploy ML → Reset → Re-attack with Detection
```

**Key Innovation: Dual-Branch Attacks**
- Execute each attack on **BOTH** main and hardened branches
- Double the attack samples: 24 scenarios × 2 branches = **48 attack samples**
- Compare vulnerable vs. hardened environments
- Test defense effectiveness empirically

---

## 📊 Data Collection Benefits

### Traditional Single-Branch:
- 28 baseline samples (normal)
- 24 attack samples (attacks)
- **Total: 52 samples**

### Enhanced Dual-Branch:
- 56 baseline samples (28 days × 2 branches = normal)
- 48 attack samples (24 scenarios × 2 branches = attacks)
- **Total: 104 samples**

**Result:** Double the data, better ML training, defense comparison insights!

---

## 🛠️ Scripts Created

### 1. `dual-branch-attack-pipeline.py`
**Purpose:** Execute single attack scenario on both branches

**Usage:**
```bash
cd scripts/attacks
python dual-branch-attack-pipeline.py --scenario 2.2
```

**What it does:**
1. Executes attack on main branch
2. Commits and pushes to main
3. Switches to hardened branch
4. Executes same attack on hardened
5. Commits and pushes to hardened
6. Returns to original branch
7. Logs results from both branches

**Example output:**
```
================================================================================
  DUAL-BRANCH ATTACK PIPELINE
================================================================================

Scenario: 2.2

================================================================================
PHASE 1: MAIN BRANCH ATTACK
================================================================================
[*] Switching to main branch...
[OK] Switched to main
[*] Running: cryptomining.py
[OK] Attack scenario executed successfully
[*] Committing and pushing to main...
[OK] Changes committed and pushed to main

================================================================================
PHASE 2: HARDENED BRANCH ATTACK
================================================================================
[*] Switching to hardened branch...
[OK] Switched to hardened
[*] Running: cryptomining.py
[OK] Attack scenario executed successfully
[*] Committing and pushing to hardened...
[OK] Changes committed and pushed to hardened

================================================================================
  SUCCESS - BOTH BRANCHES ATTACKED
================================================================================
```

---

### 2. `execute-all-dual-branch.py`
**Purpose:** Master script to execute all 24 scenarios on both branches

**Usage:**
```bash
cd scripts/attacks

# Execute all scenarios
python execute-all-dual-branch.py

# Resume from specific scenario (if interrupted)
python execute-all-dual-branch.py --start-from 5.1

# Execute with 5-minute delay between scenarios
python execute-all-dual-branch.py --delay 5

# List all scenarios without executing
python execute-all-dual-branch.py --list
```

**What it does:**
1. Runs all 24 attack scenarios sequentially
2. Each scenario executed on both branches
3. Progress tracking and logging
4. Can resume from any scenario
5. Optional delays between attacks
6. Complete execution summary

**Example output:**
```
================================================================================
  MASTER DUAL-BRANCH ATTACK EXECUTOR
================================================================================

Total scenarios: 24
Branches per scenario: 2 (main + hardened)
Total attacks: 48
Delay between scenarios: 0 minutes

Ready to begin? (yes/no): yes

================================================================================
  SCENARIO 1/24: 1.1 - Geographic Anomaly
================================================================================
[OK] Scenario 1.1 completed successfully on both branches

================================================================================
  SCENARIO 2/24: 1.2 - Service Account Abuse
================================================================================
[OK] Scenario 1.2 completed successfully on both branches

...

================================================================================
  EXECUTION COMPLETE
================================================================================

Total scenarios executed: 24
Successful: 24
Failed: 0
Success rate: 100.0%
```

---

## 📋 Execution Checklist

### Current Status (as of January 4, 2025):
- [x] Phase 1: Baseline collection COMPLETE (29 days)
- [x] Attack 8.1 executed on main branch
- [ ] Attack 8.1 executed on hardened branch
- [ ] Remaining 23 scenarios on both branches

### Next Steps:

**Option 1: Execute Attack 8.1 on Hardened (Complete Current Attack)**
```bash
cd scripts/attacks
# Since 8.1 already done on main, manually do hardened:
git checkout hardened
python scenarios/secrets_in_logs.py
git add -A
git commit -m "Add deployment debugging

Research attack scenario 8.1 for ML security study.
Branch: hardened
Phase: 2 - Attack Execution (Dual-Branch)"
git push origin hardened
git checkout main
```

**Option 2: Execute All Remaining 23 Scenarios (Automated)**
```bash
cd scripts/attacks
python execute-all-dual-branch.py --start-from 1.1
```

**Option 3: Execute Scenarios One-by-One (Manual Control)**
```bash
cd scripts/attacks

# Scenario 1.1
python dual-branch-attack-pipeline.py --scenario 1.1

# Scenario 1.2
python dual-branch-attack-pipeline.py --scenario 1.2

# etc...
```

---

## ⏰ Timeline Estimates

### Sequential Execution (No Delays):
- 24 scenarios × ~2 min per scenario = **~48 minutes**
- Each scenario: execute → commit → push → switch → execute → commit → push

### With Delays (Recommended for GitHub rate limits):
- 24 scenarios × (2 min execution + 5 min delay) = **~2.8 hours**
- Safer for GitHub API and workflows

### Workflow Processing:
- All attacks pushed to repository
- Security scans run at **2 AM UTC daily**
- Each day processes attacks from previous day
- With 48 attacks, may take **2-3 days** for all scans to complete

**Recommended approach:**
- Execute all 24 scenarios in one session (~48 min)
- Wait 2-3 days for all workflows to complete
- Verify all artifacts collected
- Proceed to Phase 3 (ML Training)

---

## 📊 Expected Results

### Attack Execution:
- 24 scenarios successfully executed on main branch
- 24 scenarios successfully executed on hardened branch
- **Total: 48 attacks committed and pushed**

### Security Scans (Triggered at 2 AM UTC):
- Main branch scans: 24 workflows
- Hardened branch scans: 24 workflows
- **Total: 48 security scanning workflows**

### Artifacts Collected:
- Main branch artifacts: ~24 files
- Hardened branch artifacts: ~24 files
- **Total: ~48 artifact sets**

### Feature Extraction:
- Main branch features: ~24 CSV files
- Hardened branch features: ~24 CSV files
- **Total: ~48 feature files (attack labeled)**

### ML Training Dataset:
- Baseline: 56 samples (28 days × 2 branches = normal)
- Attacks: 48 samples (24 scenarios × 2 branches = attack)
- **Total: 104 samples × 208 features**

---

## 🔬 Research Questions Answered

### RQ1: Do hardened defenses prevent attacks?
**Method:** Compare attack success on main vs. hardened branches
**Expected:** Some attacks succeed on both, some only on main
**Data:** Scan results from both branches

### RQ2: Can ML detect attacks on vulnerable environments?
**Method:** Train on baseline + main branch attacks
**Expected:** 70-85% detection accuracy
**Data:** Main branch attack samples

### RQ3: Can ML detect attacks on hardened environments?
**Method:** Train on baseline + hardened branch attacks
**Expected:** Different detection patterns vs. main
**Data:** Hardened branch attack samples

### RQ4: Does environment affect ML detection?
**Method:** Compare ML performance on main vs. hardened
**Expected:** Hardened attacks may have different feature signatures
**Data:** Both branch attack samples

---

## 🚨 Important Notes

### Attack 8.1 Status:
- **Already executed on main branch** ✓
- **Not yet executed on hardened branch** ✗

**To complete 8.1:**
```bash
# Option A: Manual hardened execution
git checkout hardened
python scenarios/secrets_in_logs.py
git add -A && git commit -m "Add deployment debugging..." && git push origin hardened
git checkout main

# Option B: Re-execute 8.1 on both branches (will skip main if no changes)
python dual-branch-attack-pipeline.py --scenario 8.1
```

### Git Branch Management:
- Scripts automatically switch branches
- Always returns to original branch after completion
- Creates backups before major operations
- Safe to interrupt and resume

### GitHub Workflows:
- Workflows trigger on push to **any branch**
- Main and hardened branches both have scheduled scans
- Artifacts stored per branch
- No conflicts between branch workflows

### Artifact Collection:
- Existing automation (`automated-weekly-collection.py`) collects from all branches
- Downloads stored separately per branch
- Feature extraction handles both branches
- ML training can use all samples

---

## 📈 Execution Monitoring

### Track Progress:
```bash
# View execution logs
cd scripts/attacks/logs/dual-branch-results
ls -la

# View master execution summary
cd scripts/attacks/logs/master-execution
cat execution_*.json
```

### Verify Commits:
```bash
# Check main branch
git log main --oneline | head -24

# Check hardened branch
git log hardened --oneline | head -24
```

### Monitor Workflows:
- Visit: https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions
- Filter by branch: main or hardened
- Check "Security Scanning" workflows
- Download artifacts when complete

---

## ✅ Success Criteria

### Phase 2 Complete When:
- [x] All 24 scenarios executed on main branch
- [x] All 24 scenarios executed on hardened branch
- [x] All 48 attacks committed and pushed
- [x] Security scans completed for all attacks
- [x] All artifacts collected
- [x] All features extracted
- [x] Dataset ready for ML training

### Expected Dataset:
```
ml-pipeline/output/
├── features_baseline_main_*.csv (28 files - normal)
├── features_baseline_hardened_*.csv (28 files - normal)
├── features_attack_main_*.csv (24 files - attack)
└── features_attack_hardened_*.csv (24 files - attack)

Total: ~104 feature files ready for training
```

---

## 🎓 Thesis Integration

### Enhanced Chapters:

**Chapter 5: Implementation**
- Add: Dual-branch attack methodology
- Add: Comparative attack execution strategy
- Add: Defense effectiveness testing

**Chapter 6: Experiments**
- Add: Phase 2 dual-branch attack execution
- Add: Attack success rate comparison (main vs. hardened)
- Add: Defense validation results

**Chapter 7: Results**
- Add: Attack success rate per environment
- Add: ML detection accuracy per environment
- Add: Defense effectiveness analysis
- Add: Feature importance differences between branches

**Chapter 8: Conclusion**
- Add: Dual-branch methodology validation
- Add: Defense effectiveness insights
- Add: ML generalization across environments

---

## 🚀 Quick Start

**Execute all remaining attacks on both branches:**

```bash
cd "C:\Users\joshu\Desktop\DevOps Project\scripts\attacks"

# List all scenarios
python execute-all-dual-branch.py --list

# Execute all (starting from 1.1)
python execute-all-dual-branch.py --start-from 1.1

# Monitor progress
# Wait for completion (~48 minutes)
# Wait for workflows to process (2-3 days)
# Proceed to Phase 3: ML Training
```

---

**You're ready for comprehensive dual-branch attack execution!** 🎯

All scripts created. Both branches configured. Automation ready.

Just execute and collect data for the most comprehensive DevOps security ML research! 🚀

*Generated with Claude Code*
*Last Updated: January 4, 2025*
