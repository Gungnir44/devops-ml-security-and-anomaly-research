# ML Deployment Guide - Approach B

> **Real-time Anomaly Detection System for DevOps Security Pipelines**

---

## 📚 Overview

This guide explains how to deploy and use the ML-based anomaly detection system for **Approach B** (online detection with re-attack validation).

**What this system does:**
- Trains ML models on baseline + attack data
- Deploys models to GitHub Actions
- Runs real-time anomaly detection after each security scan
- Generates alerts when anomalies detected
- Validates detection with re-attack testing

---

## 🎯 Approach B: Full Implementation Timeline

### Phase 1: Baseline Collection ✅ **IN PROGRESS**
**Status:** 50% complete (14/28 days)
**Timeline:** December 6 - January 3, 2025

```
Daily automated collection:
  ├─ GitHub workflows run at 2 AM UTC
  ├─ Security scans on both branches
  ├─ Artifact collection
  └─ Feature extraction (208 features)

Output:
  ├─ 28 days × 2 branches = 56 baseline samples
  └─ Labels: "normal"
```

**No action needed** - automation handles this ✓

---

### Phase 2: Initial Attack Wave
**Timeline:** Week 5-6 (January 3-17, 2025)

```
Execute 24 attack scenarios WITHOUT ML detection:
  ├─ ~2-3 attacks per day
  ├─ Document each attack
  ├─ Wait for scheduled scans
  └─ Collect labeled data

For each attack:
  1. Execute attack code on main branch
  2. Commit changes
  3. Wait for scheduled scan (2 AM UTC)
  4. Collect scan artifacts
  5. Label: "attack" + attack_type
  6. Document details

Output:
  ├─ ~24 attack samples (main branch)
  ├─ ~14 normal samples (hardened control)
  └─ Dataset ready for ML training
```

**Script created:** `curriculum/Week-2-Vulnerabilities/*.md` (attack scenarios)

---

### Phase 3: ML Model Training
**Timeline:** Week 7-8 (January 17-31, 2025)

```
Train models offline:

Dataset:
  ├─ Normal: 70 samples (56 baseline + 14 control)
  ├─ Attack: 24 samples
  ├─ Total: 94 samples × 208 features
  └─ Split: 70% train, 30% test

Models:
  ├─ Random Forest (baseline)
  ├─ XGBoost (comparison)
  └─ Isolation Forest (unsupervised)

Evaluation:
  ├─ Accuracy, Precision, Recall, F1
  ├─ Confusion matrix
  ├─ Feature importance
  └─ Model selection
```

**Script:** `scripts/ml-train-models.py` ✅ **READY**

**Usage:**
```bash
cd scripts
python ml-train-models.py
```

**Output:**
- Trained models saved to `models/` directory
- Training results in `models/training_results_*.json`
- Best model selected automatically

---

### Phase 4: ML Deployment **NEW!**
**Timeline:** Week 9 (February 1-7, 2025)

```
Deploy ML models to GitHub Actions:

1. Models are already trained (Phase 3)
2. GitHub workflow is already created ✓
3. Activate the workflow
4. Test on known normal samples
5. Verify alerts work
6. Monitor for false positives
```

**Workflow:** `.github/workflows/ml-anomaly-detection.yml` ✅ **READY**

**Activation steps:**

```bash
# 1. Commit models to repository
git add models/
git commit -m "Add trained ML models for anomaly detection"
git push origin main

# 2. Workflow activates automatically on schedule (2:30 AM UTC daily)
# 3. Or manually trigger for testing:
#    - Go to GitHub Actions UI
#    - Select "ML Anomaly Detection" workflow
#    - Click "Run workflow"
```

**What the workflow does:**
1. Runs 30 min after security scans (2:30 AM UTC)
2. Downloads latest scan artifacts
3. Extracts features
4. Loads trained model
5. Runs prediction
6. If anomaly detected:
   - Creates GitHub issue with alert
   - Logs prediction details
   - Exits with error code

**Monitoring:**
- Check GitHub Actions logs
- Review prediction logs in `logs/ml-predictions/`
- Monitor GitHub issues for alerts

---

### Phase 5: Environment Reset **NEW!**
**Timeline:** Week 10 (February 7-14, 2025)

```
Clean main branch:
  ├─ Create backup branch
  ├─ Reset main to hardened state
  ├─ Remove attack artifacts
  ├─ Verify scans show clean
  └─ Confirm ML shows "normal"
```

**Script:** `scripts/reset-environment.sh` ✅ **READY**

**Usage:**
```bash
cd scripts
bash reset-environment.sh
```

**The script will:**
1. Create backup branch (safety)
2. Copy clean code from hardened branch
3. Remove attack artifacts
4. Commit reset
5. Push to remote (with confirmation)
6. Wait for verification scan

**Verification checklist:**
- [ ] Security scans show clean
- [ ] ML prediction shows "NORMAL"
- [ ] No GitHub issues created
- [ ] Baseline re-established

---

### Phase 6: Re-Attack with ML Detection **NEW!**
**Timeline:** Week 11-12 (February 14-28, 2025)

```
Execute SAME 24 attacks with ML watching:

For each attack:
  1. Execute attack (same as Phase 2)
  2. Commit and wait for scan (2 AM UTC)
  3. ML model analyzes results (2:30 AM UTC)
  4. Record detection results:
     ├─ Did ML detect it? (Yes/No)
     ├─ Detection confidence (0-100%)
     ├─ Time to detection (hours)
     ├─ Alert generated? (Yes/No)
     └─ False positives? (any)

Compare with Phase 2:
  ├─ Which attacks detected?
  ├─ Which attacks missed?
  ├─ Detection accuracy per attack type
  └─ Overall detection rate
```

**Tracking spreadsheet:**
Create `phase-6-detection-results.csv`:

```csv
attack_id,attack_type,execution_date,ml_detected,confidence,hours_to_detect,alert_created,notes
1,sql_injection,2025-02-14,true,0.95,0.5,true,Detected immediately
2,xss,2025-02-14,true,0.87,0.5,true,High confidence
3,secrets,2025-02-15,false,0.42,N/A,false,Missed - low confidence
...
```

---

### Phase 7: Analysis & Thesis
**Timeline:** Week 13-14 (March 1-14, 2025)

```
Research Questions Answered:

RQ1: Can ML detect attacks offline?
  → Yes, with X% accuracy on test set (Phase 3)

RQ2: Can ML detect attacks in real-time?
  → Yes, detected Y out of 24 attacks (Y/24 %) (Phase 6)

RQ3: What's the detection latency?
  → Average Z hours to detection (Phase 6)

RQ4: Which attacks are easiest/hardest to detect?
  → Attack type analysis (Phase 6)

RQ5: False positive rate in production?
  → W false positives over 2 weeks (Phase 6)
```

**Thesis chapters updated:**
- Chapter 5: Implementation (add ML deployment)
- Chapter 6: Experiments (add Phases 4-6)
- Chapter 7: Results (offline + online results)
- Chapter 8: Conclusion (real-time detection feasibility)

---

## 🛠️ Scripts Reference

### 1. ML Training Script
**File:** `scripts/ml-train-models.py`
**Purpose:** Train anomaly detection models (Phase 3)

**Usage:**
```bash
cd scripts
python ml-train-models.py
```

**Input:**
- Baseline data: `DevOps Master's Degree Project/ml-pipeline/output/features_*.csv`
- Attack data: `features_attack_data.csv` (created in Phase 2)

**Output:**
- `models/random_forest_latest.pkl`
- `models/xgboost_latest.pkl`
- `models/isolation_forest_latest.pkl`
- `models/scaler_latest.pkl`
- `models/training_results_*.json`

---

### 2. Real-time Prediction Script
**File:** `scripts/ml-predict-realtime.py`
**Purpose:** Run prediction on latest scan (Phase 4-6)

**Usage:**
```bash
cd scripts
python ml-predict-realtime.py
```

**Environment variables:**
- `ML_MODEL_TYPE`: Model to use (default: `random_forest`)

**Output:**
- Prediction result (NORMAL or ANOMALY)
- Confidence score
- Logs saved to `logs/ml-predictions/`

---

### 3. GitHub Actions Workflow
**File:** `.github/workflows/ml-anomaly-detection.yml`
**Purpose:** Automated ML detection in CI/CD

**Triggers:**
- Schedule: 2:30 AM UTC daily
- Manual: GitHub Actions UI
- Workflow run: After security scanning completes

**Outputs:**
- GitHub issue (if anomaly detected)
- Prediction logs artifact
- Step summary in Actions UI

---

### 4. Environment Reset Script
**File:** `scripts/reset-environment.sh`
**Purpose:** Reset environment for re-attack (Phase 5)

**Usage:**
```bash
cd scripts
bash reset-environment.sh
```

**Safety features:**
- Creates backup branch
- Prompts before pushing
- Verifies hardened branch exists
- Detailed logging

---

## 📊 Data Flow Diagram

```
Phase 1 (Baseline):
  GitHub Actions (2 AM) → Security Scans → Artifacts → Feature Extraction
  → Baseline Data (Normal)

Phase 2 (Attacks):
  Execute Attack → Commit → GitHub Actions (2 AM) → Security Scans
  → Artifacts → Feature Extraction → Attack Data (Labeled)

Phase 3 (Training):
  Baseline Data + Attack Data → ml-train-models.py → Trained Models
  → Random Forest, XGBoost, Isolation Forest

Phase 4 (Deployment):
  Trained Models → Git Commit → GitHub Repository
  → ml-anomaly-detection.yml workflow activated

Phase 5 (Reset):
  reset-environment.sh → Main = Hardened → Verify Clean → Ready

Phase 6 (Re-attack with Detection):
  Execute Attack → Commit → Security Scans (2 AM)
  → ML Detection (2:30 AM) → Prediction → Alert (if anomaly)
  → Record Results → Compare with Phase 2
```

---

## ✅ Validation Checklist

### Phase 3 Validation
- [ ] Models trained successfully
- [ ] Training accuracy > 80%
- [ ] Models saved to `models/` directory
- [ ] Training results JSON created

### Phase 4 Validation
- [ ] Workflow file committed
- [ ] Models committed to repository
- [ ] Manual workflow trigger works
- [ ] Prediction runs successfully
- [ ] Logs created in correct location

### Phase 5 Validation
- [ ] Backup branch created
- [ ] Main branch reset to hardened
- [ ] Security scans show clean
- [ ] ML predicts "NORMAL"
- [ ] No false positive alerts

### Phase 6 Validation
- [ ] All 24 attacks re-executed
- [ ] Detection results recorded
- [ ] Comparison with Phase 2 complete
- [ ] Detection rate calculated
- [ ] False positives documented

---

## 🔧 Troubleshooting

### Issue: Models not found in workflow
**Error:** "No trained models found"

**Solution:**
```bash
# Ensure models are committed to repo
cd models
ls -la *.pkl  # Should see model files
git add *.pkl
git commit -m "Add trained models"
git push origin main
```

---

### Issue: Prediction fails with import error
**Error:** "ModuleNotFoundError: No module named 'xgboost'"

**Solution:**
Workflow installs dependencies automatically. If running locally:
```bash
pip install pandas numpy scikit-learn joblib xgboost
```

---

### Issue: False positives in Phase 6
**Symptom:** ML detects anomaly on clean code

**Diagnosis:**
1. Check confidence score - if low (<70%), may be noise
2. Review recent changes - any legitimate changes?
3. Check feature drift - baseline may be outdated

**Solution:**
- Retrain models with more recent baseline data
- Adjust confidence threshold in workflow
- Document as limitation in thesis

---

### Issue: False negatives (missed attacks)
**Symptom:** ML doesn't detect known attack

**Diagnosis:**
1. Was attack similar to training data?
2. Check feature extraction - did features capture attack?
3. Review model performance on this attack type

**Solution:**
- Add more diverse attack samples in training
- Feature engineering - add attack-specific features
- Try different model (XGBoost vs Random Forest)
- Document as limitation and future work

---

## 📈 Expected Results

### Phase 3 (Training)
**Good results for Masters:**
- Accuracy: 75-90%
- Precision: 70-85%
- Recall: 70-85%
- F1-Score: 70-85%

**Don't worry if:**
- Perfect accuracy (95%+) - small dataset
- Some attacks harder to detect than others
- Unsupervised model (Isolation Forest) performs worse

---

### Phase 6 (Re-attack Detection)
**Good results for Masters:**
- Detection rate: 60-80% (14-19 out of 24 attacks)
- Detection latency: <1 hour (next scheduled scan)
- False positives: <10% during normal operation
- Clear difference between main and hardened branches

**Excellent results (bonus):**
- Detection rate: >80% (20+ out of 24)
- No false positives
- Consistent detection across attack types

---

## 🎓 Thesis Integration

### Enhanced Chapters

**Chapter 5: Implementation**
Add sections:
- ML Model Selection and Training
- Real-time Detection Pipeline
- GitHub Actions Integration
- Deployment Architecture

**Chapter 6: Experiments**
Add phases:
- Phase 3: Model Training (offline)
- Phase 4: Deployment and Verification
- Phase 5: Environment Reset
- Phase 6: Re-attack with Detection (online)

**Chapter 7: Results**
Compare:
- Offline accuracy (Phase 3 test set)
- Online detection rate (Phase 6 actual)
- Detection latency analysis
- False positive/negative analysis

**Chapter 8: Conclusion**
Demonstrate:
- Real-time detection is feasible ✓
- Deployment is practical ✓
- Identifies challenges for future work ✓

---

## 🚀 Quick Start Commands

```bash
# Phase 3: Train models (after Phase 2 attack data collected)
cd scripts
python ml-train-models.py

# Phase 4: Deploy models
git add models/
git commit -m "Deploy ML models for real-time detection"
git push origin main

# Test ML detection manually
cd scripts
python ml-predict-realtime.py

# Phase 5: Reset environment
bash reset-environment.sh

# Phase 6: Re-execute attacks
# (Use curriculum/Week-2-Vulnerabilities/*.md as guide)
```

---

## 📞 Support

**Questions during implementation:**
- Review this guide first
- Check workflow logs in GitHub Actions
- Review prediction logs in `logs/ml-predictions/`
- Consult `MASTERS-TO-PHD-PATHWAY.md` for strategy

**Current status:**
- Phase 1: 50% complete (on track)
- Phase 2-7: Scripts and workflows ready
- All infrastructure in place
- Ready to execute when Phase 1 completes (Jan 3, 2025)

---

## ✅ Success Criteria

You'll know Approach B is working when:

**Phase 3:**
- ✅ Models train without errors
- ✅ Accuracy >75% on test set
- ✅ Models saved successfully

**Phase 4:**
- ✅ Workflow runs on schedule
- ✅ Predictions logged
- ✅ No errors in GitHub Actions

**Phase 5:**
- ✅ Main branch shows clean scans
- ✅ ML predicts NORMAL
- ✅ No alerts triggered

**Phase 6:**
- ✅ Majority of attacks detected (>60%)
- ✅ Alerts created for detections
- ✅ Detection results documented
- ✅ Comparison with Phase 2 complete

---

**You're ready for Approach B!** 🎯

All scripts created. All workflows ready. Infrastructure in place.

Just complete Phase 1 baseline (2 more weeks), then execute Phases 2-7 as documented.

**Estimated completion: March 14, 2025** (14 weeks from start)

*Generated with Claude Code*
*Last Updated: December 20, 2024*
