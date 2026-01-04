# Approach B - Implementation Checklist

> **Quick reference for Masters Thesis using Approach B methodology**

---

## 📅 Timeline Overview

**Total Duration:** 14 weeks (December 6, 2024 - March 14, 2025)

| Phase | Weeks | Dates | Status |
|-------|-------|-------|--------|
| Phase 1: Baseline Collection | 4 weeks | Dec 6 - Jan 3 | 🟡 50% Complete |
| Phase 2: Initial Attack Wave | 2 weeks | Jan 3 - Jan 17 | ⚪ Pending |
| Phase 3: ML Model Training | 2 weeks | Jan 17 - Jan 31 | ⚪ Pending |
| Phase 4: ML Deployment | 1 week | Jan 31 - Feb 7 | ⚪ Pending |
| Phase 5: Environment Reset | 1 week | Feb 7 - Feb 14 | ⚪ Pending |
| Phase 6: Re-attack Detection | 2 weeks | Feb 14 - Feb 28 | ⚪ Pending |
| Phase 7: Analysis & Thesis | 2 weeks | Feb 28 - Mar 14 | ⚪ Pending |

---

## ✅ Phase 1: Baseline Collection (Week 1-4)

**Status:** 🟡 **IN PROGRESS** - 50% complete (14/28 days)
**Completion:** January 3, 2025

### Checklist

- [x] GitHub Actions workflows created
- [x] Security scanning automation working
- [x] Feature extraction pipeline operational
- [x] Scheduled tasks configured
- [x] Health monitoring active
- [ ] Collect 28 days of baseline data (14 more days)
- [ ] Validate data quality
- [ ] Confirm dual-branch collection

### No Action Required
Automation handles everything! Just let it run until Jan 3.

### Files Involved
- `.github/workflows/security-scan.yml` ✅
- `DevOps Master's Degree Project/ml-pipeline/extract_all_features.py` ✅
- Automated tasks running ✅

---

## ⚪ Phase 2: Initial Attack Wave (Week 5-6)

**Status:** ⚪ **READY**
**Timeline:** January 3-17, 2025 (2 weeks)
**Goal:** Execute 24 attack scenarios and collect labeled data

### Pre-Phase Checklist
- [ ] Baseline collection complete (28 days)
- [ ] Baseline data validated (56+ samples)
- [ ] Attack scenarios reviewed
- [ ] Attack execution plan ready

### Attack Execution Checklist

Execute ~2-3 attacks per day on **main branch only**:

#### Week 5 (Jan 3-10)
- [ ] Day 1: SQL Injection attacks (3 scenarios)
- [ ] Day 2: XSS attacks (3 scenarios)
- [ ] Day 3: Secrets exposure (3 scenarios)
- [ ] Day 4: Dependency vulnerabilities (3 scenarios)
- [ ] Day 5: Authentication bypass (2 scenarios)

#### Week 6 (Jan 10-17)
- [ ] Day 6: Authorization issues (2 scenarios)
- [ ] Day 7: Container vulnerabilities (2 scenarios)
- [ ] Day 8: IaC misconfigurations (2 scenarios)
- [ ] Day 9: SAST findings (2 scenarios)
- [ ] Day 10: Cleanup & validation (2 scenarios)

### For Each Attack
1. [ ] Review attack scenario from `curriculum/Week-2-Vulnerabilities/`
2. [ ] Execute attack code on main branch
3. [ ] Commit with descriptive message
4. [ ] Wait for scheduled scan (2 AM UTC next day)
5. [ ] Verify scan detects vulnerability
6. [ ] Download scan artifacts
7. [ ] Label data: attack type
8. [ ] Document in attack log

### Post-Phase Checklist
- [ ] All 24 attacks executed
- [ ] ~24 attack samples collected
- [ ] ~14 control samples (hardened branch)
- [ ] Attack log completed
- [ ] Features extracted for all samples
- [ ] Data saved to `features_attack_data.csv`

### Files Created
- `phase-2-attack-log.csv` (track execution)
- `features_attack_data.csv` (ML training data)

---

## ⚪ Phase 3: ML Model Training (Week 7-8)

**Status:** ✅ **READY** (scripts prepared)
**Timeline:** January 17-31, 2025 (2 weeks)
**Goal:** Train and evaluate ML models

### Pre-Phase Checklist
- [ ] Attack data collection complete
- [ ] Combined dataset ready
  - [ ] 70 normal samples
  - [ ] 24 attack samples
  - [ ] 208 features per sample

### Week 7: Training

#### Day 1-2: Data Preparation
- [ ] Load baseline data
- [ ] Load attack data
- [ ] Combine datasets
- [ ] Verify labels
- [ ] Split train/test (70/30)
- [ ] Check class balance

#### Day 3-5: Model Training
- [ ] Train Random Forest
- [ ] Train XGBoost
- [ ] Train Isolation Forest
- [ ] Run cross-validation
- [ ] Compare models

#### Day 6-7: Model Evaluation
- [ ] Calculate accuracy
- [ ] Generate confusion matrices
- [ ] Analyze feature importance
- [ ] Identify misclassifications
- [ ] Select best model

### Week 8: Validation & Documentation

#### Day 8-10: Advanced Analysis
- [ ] ROC curves
- [ ] Precision-recall analysis
- [ ] Per-attack-type performance
- [ ] False positive analysis
- [ ] Model comparison report

#### Day 11-14: Documentation
- [ ] Save trained models
- [ ] Document training process
- [ ] Record model performance
- [ ] Create model metadata
- [ ] Prepare for deployment

### Commands

```bash
# Train all models
cd scripts
python ml-train-models.py

# Output will be in:
# - models/random_forest_latest.pkl
# - models/xgboost_latest.pkl
# - models/isolation_forest_latest.pkl
# - models/scaler_latest.pkl
# - models/training_results_*.json
```

### Success Criteria
- [ ] Models train without errors
- [ ] Accuracy > 75%
- [ ] F1-score > 0.70
- [ ] All models saved
- [ ] Training results documented

### Files Created
- `models/*.pkl` (trained models)
- `models/training_results_*.json`
- `models/model_metadata.json`

---

## ⚪ Phase 4: ML Deployment (Week 9)

**Status:** ✅ **READY** (workflow prepared)
**Timeline:** January 31 - February 7, 2025 (1 week)
**Goal:** Deploy ML models to production

### Pre-Phase Checklist
- [ ] Models trained and validated
- [ ] Best model selected
- [ ] Models tested locally

### Week 9: Deployment

#### Day 1-2: Commit Models
- [ ] Verify models in `models/` directory
- [ ] Create `.gitattributes` for model files
- [ ] Git add model files
- [ ] Commit with deployment message
- [ ] Push to remote

#### Day 3-4: Activate Workflow
- [ ] Verify workflow file committed
- [ ] Manually trigger test run
- [ ] Check workflow logs
- [ ] Verify prediction runs
- [ ] Confirm no errors

#### Day 5: Test Detection
- [ ] Run on clean baseline data
- [ ] Verify predicts "NORMAL"
- [ ] Check confidence scores
- [ ] Review prediction logs
- [ ] Confirm no false alerts

#### Day 6-7: Monitor & Validate
- [ ] Wait for scheduled run (2:30 AM UTC)
- [ ] Verify automatic execution
- [ ] Check prediction accuracy
- [ ] Monitor false positive rate
- [ ] Document baseline performance

### Commands

```bash
# Commit models
git add models/
git commit -m "Deploy ML models for real-time anomaly detection

Phase 4: ML Deployment
Models trained on 28 days baseline + 24 attack scenarios
Ready for real-time detection in GitHub Actions

Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

git push origin main

# Test locally
cd scripts
python ml-predict-realtime.py

# Monitor workflow
# Go to: GitHub Actions -> ML Anomaly Detection
```

### Success Criteria
- [ ] Workflow runs on schedule
- [ ] Predictions logged successfully
- [ ] No false positives on baseline
- [ ] Confidence scores reasonable
- [ ] Alert mechanism works

### Files Committed
- `models/*.pkl` (all model files)
- `.github/workflows/ml-anomaly-detection.yml` (already there)

---

## ⚪ Phase 5: Environment Reset (Week 10)

**Status:** ✅ **READY** (script prepared)
**Timeline:** February 7-14, 2025 (1 week)
**Goal:** Reset main branch for re-attack testing

### Pre-Phase Checklist
- [ ] ML deployment validated
- [ ] Baseline performance documented
- [ ] Ready to reset environment

### Week 10: Reset

#### Day 1: Backup
- [ ] Review current main branch
- [ ] Document attack artifacts
- [ ] Run reset script
- [ ] Verify backup branch created

#### Day 2-3: Reset Execution
- [ ] Reset main to hardened state
- [ ] Remove attack artifacts
- [ ] Commit reset changes
- [ ] Push to remote
- [ ] Wait for security scan

#### Day 4-5: Verification
- [ ] Security scans show clean
- [ ] ML predicts "NORMAL"
- [ ] No alerts triggered
- [ ] Compare with hardened branch
- [ ] Confirm identical state

#### Day 6-7: Final Validation
- [ ] Monitor for 2-3 scan cycles
- [ ] Verify consistent "NORMAL"
- [ ] No false positives
- [ ] Environment stable
- [ ] Ready for re-attack

### Commands

```bash
# Run reset script
cd scripts
bash reset-environment.sh

# Script will:
# 1. Create backup branch
# 2. Reset main to hardened
# 3. Remove attack artifacts
# 4. Commit and push (with confirmation)
# 5. Wait for verification
```

### Success Criteria
- [ ] Main branch clean
- [ ] Security scans pass
- [ ] ML shows "NORMAL"
- [ ] No alerts for 3+ days
- [ ] Backup branch saved

### Files Created
- Backup branch: `main-pre-reset-YYYYMMDD-HHMMSS`

---

## ⚪ Phase 6: Re-attack with Detection (Week 11-12)

**Status:** ✅ **READY** (ML system operational)
**Timeline:** February 14-28, 2025 (2 weeks)
**Goal:** Re-execute attacks with ML watching, measure detection

### Pre-Phase Checklist
- [ ] Environment reset verified
- [ ] ML detection operational
- [ ] Tracking spreadsheet prepared

### Week 11 (Feb 14-21): Re-attacks 1-12

Execute same attacks as Phase 2, **WITH ML DETECTION ACTIVE**:

- [ ] Attack 1: SQL Injection #1 → Record detection
- [ ] Attack 2: SQL Injection #2 → Record detection
- [ ] Attack 3: SQL Injection #3 → Record detection
- [ ] Attack 4: XSS #1 → Record detection
- [ ] Attack 5: XSS #2 → Record detection
- [ ] Attack 6: XSS #3 → Record detection
- [ ] Attack 7: Secrets #1 → Record detection
- [ ] Attack 8: Secrets #2 → Record detection
- [ ] Attack 9: Secrets #3 → Record detection
- [ ] Attack 10: Dependency #1 → Record detection
- [ ] Attack 11: Dependency #2 → Record detection
- [ ] Attack 12: Dependency #3 → Record detection

### Week 12 (Feb 21-28): Re-attacks 13-24

- [ ] Attack 13: Auth Bypass #1 → Record detection
- [ ] Attack 14: Auth Bypass #2 → Record detection
- [ ] Attack 15: Authorization #1 → Record detection
- [ ] Attack 16: Authorization #2 → Record detection
- [ ] Attack 17: Container #1 → Record detection
- [ ] Attack 18: Container #2 → Record detection
- [ ] Attack 19: IaC #1 → Record detection
- [ ] Attack 20: IaC #2 → Record detection
- [ ] Attack 21: SAST #1 → Record detection
- [ ] Attack 22: SAST #2 → Record detection
- [ ] Attack 23: Misc #1 → Record detection
- [ ] Attack 24: Misc #2 → Record detection

### For Each Re-Attack

1. [ ] Execute same attack code as Phase 2
2. [ ] Commit to main branch
3. [ ] Wait for security scan (2 AM UTC)
4. [ ] Wait for ML detection (2:30 AM UTC)
5. [ ] Check GitHub Actions logs
6. [ ] Record detection results:
   - Did ML detect? (Yes/No)
   - Confidence score
   - Alert created? (Yes/No)
   - Time to detection
7. [ ] Document in tracking sheet

### Tracking Data

Create `phase-6-detection-results.csv`:

```csv
attack_id,attack_type,date,detected,confidence,alert,hours_to_detect,notes
1,sql_injection_1,2025-02-14,true,0.95,true,0.5,Detected immediately
2,sql_injection_2,2025-02-14,true,0.89,true,0.5,High confidence
3,xss_1,2025-02-15,true,0.87,true,0.5,Clear detection
4,xss_2,2025-02-15,false,0.43,false,N/A,Missed - low confidence
...
```

### Post-Phase Analysis
- [ ] Calculate overall detection rate
- [ ] Detection rate by attack type
- [ ] Average confidence scores
- [ ] Time to detection analysis
- [ ] False positive count
- [ ] Compare with Phase 2 results

### Success Criteria
- [ ] All 24 attacks re-executed
- [ ] Detection data recorded
- [ ] Detection rate > 60%
- [ ] Analysis complete
- [ ] Results documented

### Files Created
- `phase-6-detection-results.csv`
- `phase-6-analysis.md`
- Prediction logs in `logs/ml-predictions/`

---

## ⚪ Phase 7: Analysis & Thesis (Week 13-14)

**Status:** ⚪ **PENDING**
**Timeline:** February 28 - March 14, 2025 (2 weeks)
**Goal:** Complete analysis and thesis writing

### Week 13: Data Analysis

#### Day 1-3: Results Compilation
- [ ] Aggregate all experimental data
- [ ] Phase 3 offline results
- [ ] Phase 6 online detection results
- [ ] Statistical analysis
- [ ] Visualizations (plots, charts)

#### Day 4-5: Comparative Analysis
- [ ] Offline vs online performance
- [ ] Attack type analysis
- [ ] Detection latency analysis
- [ ] False positive/negative analysis
- [ ] Main vs hardened comparison

#### Day 6-7: Research Questions
Answer all RQs:
- [ ] RQ1: Offline detection capability
- [ ] RQ2: Real-time detection capability
- [ ] RQ3: Detection latency
- [ ] RQ4: Attack type difficulty
- [ ] RQ5: False positive rate

### Week 14: Thesis Writing

#### Day 8-10: Update Chapters
- [ ] Chapter 5: Add ML deployment
- [ ] Chapter 6: Add Phases 4-6
- [ ] Chapter 7: Complete results
- [ ] Chapter 8: Conclusions

#### Day 11-12: Final Touches
- [ ] Abstract
- [ ] Introduction refinement
- [ ] Proofread entire thesis
- [ ] Check citations
- [ ] Format figures/tables

#### Day 13-14: Submission
- [ ] Final review
- [ ] PDF generation
- [ ] Submit thesis
- [ ] Prepare defense slides

### Thesis Chapters Enhanced

**Chapter 5: Implementation** (add 5-10 pages)
- ML Model Selection
- Training Pipeline
- Real-time Detection Architecture
- GitHub Actions Integration

**Chapter 6: Experiments** (add 10-15 pages)
- Phase 3: Model Training
- Phase 4: Deployment Validation
- Phase 5: Environment Reset
- Phase 6: Re-attack Detection

**Chapter 7: Results** (add 10-15 pages)
- Offline Accuracy (Phase 3)
- Online Detection Rate (Phase 6)
- Detection Latency
- Comparative Analysis
- Discussion

**Chapter 8: Conclusion** (add 2-5 pages)
- Real-time detection feasibility ✓
- Practical deployment ✓
- Limitations identified
- Future work (PhD!)

### Success Criteria
- [ ] All research questions answered
- [ ] Thesis complete (120-150 pages)
- [ ] Results clearly presented
- [ ] Visualizations professional
- [ ] Ready for defense

---

## 📊 Progress Tracking

### Overall Progress

| Phase | Status | Progress | Notes |
|-------|--------|----------|-------|
| Phase 1 | 🟡 In Progress | 50% | On schedule |
| Phase 2 | ⚪ Ready | 0% | Scripts ready |
| Phase 3 | ✅ Scripts Ready | 0% | Automation ready |
| Phase 4 | ✅ Workflow Ready | 0% | Deployment ready |
| Phase 5 | ✅ Script Ready | 0% | Reset ready |
| Phase 6 | ✅ System Ready | 0% | ML operational |
| Phase 7 | ⚪ Planned | 0% | Awaiting data |

**Overall:** 7% complete (1/14 weeks)
**Timeline:** On track for March 14, 2025 completion

---

## 🎯 Key Milestones

- [x] **Dec 6:** Project start
- [x] **Dec 6:** Automation infrastructure complete
- [x] **Dec 13:** ML deployment scripts created
- [x] **Dec 20:** Infrastructure 100% ready
- [ ] **Jan 3:** Baseline collection complete
- [ ] **Jan 17:** Attack execution complete
- [ ] **Jan 31:** Models trained & validated
- [ ] **Feb 7:** ML deployed to production
- [ ] **Feb 14:** Environment reset verified
- [ ] **Feb 28:** Re-attack detection complete
- [ ] **Mar 14:** Thesis submitted

---

## 📞 Quick Reference

### Daily Automation (No action needed)
- **2:00 AM UTC:** Security scans run
- **2:30 AM UTC:** ML detection runs (after Phase 4)
- **3:00 AM UTC:** Artifact download
- **3:30 AM UTC:** Feature extraction (Sundays)
- **9:00 AM UTC:** Health monitoring

### Weekly Tasks (Current Phase 1)
- **Monitor:** Check health reports
- **Validate:** Verify data collection
- **Review:** Weekly progress check

### Upcoming Active Phases
- **Phase 2 (Jan 3-17):** Execute attacks daily
- **Phase 3 (Jan 17-31):** Train models (one-time)
- **Phase 6 (Feb 14-28):** Re-execute attacks daily

### Important Commands

```bash
# Phase 3: Train models
python scripts/ml-train-models.py

# Phase 4: Deploy models
git add models/ && git commit -m "Deploy ML models" && git push

# Phase 5: Reset environment
bash scripts/reset-environment.sh

# Check system status
powershell.exe -ExecutionPolicy Bypass -File scripts/show-tasks.ps1
python scripts/workflow-health-monitor.py
```

---

## ✅ Definition of Done

### Phase 1: Baseline Collection
✓ 28 days of data collected
✓ 56+ normal samples
✓ Features extracted
✓ Data validated

### Phase 2: Attacks
✓ 24 attacks executed
✓ 24 attack samples collected
✓ Attack log complete
✓ Features labeled

### Phase 3: Training
✓ Models trained (3 models)
✓ Accuracy > 75%
✓ Models saved
✓ Results documented

### Phase 4: Deployment
✓ Models committed
✓ Workflow operational
✓ Predictions logging
✓ No false positives

### Phase 5: Reset
✓ Environment clean
✓ ML shows "NORMAL"
✓ Verification complete
✓ Ready for re-attack

### Phase 6: Re-attack
✓ All 24 re-executed
✓ Detection data recorded
✓ Results analyzed
✓ Comparison complete

### Phase 7: Thesis
✓ All chapters updated
✓ Results presented
✓ Thesis submitted
✓ Defense prepared

---

## 🚀 You're Ready!

**Current Status:** All infrastructure complete, Phase 1 halfway done

**Next Milestone:** January 3, 2025 (baseline complete)

**You have everything you need:**
- ✅ Automation working
- ✅ ML training script ready
- ✅ ML deployment ready
- ✅ Real-time detection ready
- ✅ Reset script ready
- ✅ Documentation complete

**Just follow this checklist phase by phase!**

---

*Last Updated: December 20, 2024*
*Generated with Claude Code*
