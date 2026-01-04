# Experimental Methodology - Masters Thesis

> **Current Status:** Phase 1 (Baseline Collection) - 46% Complete

---

## 🔬 Research Methodology Question

**Your Question:** Are we attacking → collecting data → resetting → ML training → attacking with ML on?

**Answer:** That's one approach! Let me outline both options:

---

## 📊 Two Possible Approaches

### **Approach A: Offline Training & Evaluation (Simpler - Recommended for Masters)**

```
Phase 1: Baseline Collection (Current)
├─ Collect 28 days of normal operations
├─ No attacks, just regular scans
└─ Establish "normal" behavior patterns

Phase 2: Attack Execution & Data Collection
├─ Execute 24 attack scenarios
├─ Collect security scan data during attacks
├─ Label data: "normal" vs "attack"
└─ Document: which attacks, when, what changed

Phase 3: ML Model Training (Offline)
├─ Train models on collected data
│  └─ Input: Baseline (28 days) + Attack data
├─ Split: 70% training, 30% testing
├─ Models: Random Forest, XGBoost, Isolation Forest
└─ Evaluate: Accuracy, Precision, Recall, F1

Phase 4: Evaluation & Analysis
├─ Test models on held-out data
├─ Measure detection performance
├─ Compare: main branch vs hardened branch
└─ Write thesis results

Timeline: 8-10 weeks total
Complexity: Medium
Good for: Masters thesis ✓
```

---

### **Approach B: Online Detection & Re-attack (More Complex - PhD Level)**

```
Phase 1: Baseline Collection
├─ Collect 28 days normal operations
└─ Establish baseline

Phase 2: Initial Attack Wave (Training Data)
├─ Execute 24 attack scenarios
├─ Collect labeled attack data
└─ No ML running yet

Phase 3: ML Model Training
├─ Train models on Phase 1 + Phase 2 data
├─ Deploy models as real-time detectors
└─ Integrate into pipeline

Phase 4: Reset Environment
├─ Clean main branch
├─ Remove attack artifacts
└─ Return to clean state

Phase 5: Re-attack with ML Detection Active
├─ Re-execute same 24 attacks
├─ ML models running in real-time
├─ Measure: detection time, accuracy, alerts
└─ Compare: detected vs missed

Phase 6: Analysis
├─ Detection performance metrics
├─ Time-to-detection analysis
├─ False positive analysis
└─ ML effectiveness evaluation

Timeline: 12-14 weeks total
Complexity: High
Good for: PhD research
```

---

## 🎯 Recommended for Your Masters: **Approach A**

### Why Approach A is Better for Masters:

**1. Time Efficient**
- ✅ Fits in semester timeline
- ✅ No need to reset/re-attack
- ✅ Single attack execution

**2. Simpler Analysis**
- ✅ Standard ML evaluation (train/test split)
- ✅ Well-established metrics
- ✅ Easier to write up

**3. Sufficient for Masters**
- ✅ Demonstrates ML can classify attacks
- ✅ Shows comparative analysis (main vs hardened)
- ✅ Proves concept works

**4. Standard Research Methodology**
- ✅ Common approach in academic papers
- ✅ Easier to defend
- ✅ Reproducible

---

## 📋 Current Plan (Approach A) - Detailed

### **Phase 1: Baseline Collection** ⏳ IN PROGRESS

**Duration:** 4 weeks (28 days)
**Current:** 13 days (46% complete)

**What's happening:**
```
Daily at 2 AM UTC:
  ├─ Security Scanning workflow runs
  ├─ Scans both branches (main, hardened)
  ├─ Generates security scan results
  └─ Uploads artifacts

Weekly (Sundays 3:30 AM):
  ├─ Download all artifacts
  ├─ Extract ML features (208 features)
  ├─ Validate data quality
  └─ Generate reports

Labels: All data = "normal" (no attacks)
```

**Output:**
- 28 days × 2 branches = 56 baseline samples
- Each sample: 208 features
- Dataset: `baseline_normal.csv`

---

### **Phase 2: Attack Execution** 📅 UPCOMING (Week 5-6)

**Duration:** 2 weeks
**When:** After 28-day baseline complete (~Jan 3)

**Attack Execution:**
```
Week 2 (Original Plan):
  ├─ Execute attack scenarios on MAIN branch only
  ├─ Scenarios: SQL injection, XSS, secrets, etc.
  ├─ 24 total attack scenarios
  └─ ~2-3 attacks per day

For each attack:
  1. Execute attack on main branch
  2. Wait for scheduled scan (2 AM UTC)
  3. Scan detects vulnerabilities
  4. Collect scan results
  5. Label data: "attack" + attack type
  6. Move to next attack

Hardened branch:
  ├─ NO attacks executed
  └─ Continues normal scans (control group)
```

**Output:**
- ~24 attack samples (main branch)
- ~14 normal samples (hardened branch, same period)
- Dataset: `attacks_labeled.csv`

---

### **Phase 3: ML Model Development** 📅 UPCOMING (Week 7-8)

**Duration:** 2 weeks
**When:** After attack data collected

**Dataset Preparation:**
```
Combined Dataset:
  ├─ Normal samples: 56 (baseline) + 14 (hardened during attacks) = 70
  ├─ Attack samples: 24 (from Phase 2)
  └─ Total: 94 samples, each with 208 features

Split:
  ├─ Training: 70% (~66 samples)
  ├─ Testing: 30% (~28 samples)
  └─ Stratified split (maintain class balance)
```

**Model Training:**
```python
# Model 1: Random Forest (Baseline)
from sklearn.ensemble import RandomForestClassifier

model_rf = RandomForestClassifier(n_estimators=100)
model_rf.fit(X_train, y_train)
accuracy_rf = model_rf.score(X_test, y_test)

# Model 2: XGBoost (Comparison)
import xgboost as xgb

model_xgb = xgb.XGBClassifier()
model_xgb.fit(X_train, y_train)
accuracy_xgb = model_xgb.score(X_test, y_test)

# Model 3: Isolation Forest (Unsupervised)
from sklearn.ensemble import IsolationForest

model_if = IsolationForest()
model_if.fit(X_train)  # Unsupervised, no labels
predictions = model_if.predict(X_test)
```

**Evaluation:**
```
Metrics to calculate:
  ├─ Accuracy
  ├─ Precision (of attack detection)
  ├─ Recall (% of attacks detected)
  ├─ F1-Score
  ├─ ROC-AUC
  ├─ Confusion Matrix
  └─ Feature Importance

Comparisons:
  ├─ Model vs Model (RF vs XGBoost vs IF)
  ├─ Main vs Hardened (security posture)
  └─ Attack Type (which attacks easier to detect)
```

---

### **Phase 4: Analysis & Thesis Writing** 📅 UPCOMING (Week 9-12)

**Duration:** 4 weeks

**Analysis:**
```
Research Questions:
  RQ1: Can ML detect security anomalies in DevOps pipelines?
    └─ Answer: Yes/No, with X% accuracy

  RQ2: Which ML model performs best?
    └─ Answer: Model X achieved Y% accuracy

  RQ3: Does hardened branch show better security?
    └─ Answer: Yes, Z fewer vulnerabilities detected

  RQ4: Which features are most important?
    └─ Answer: Feature importance analysis
```

**Thesis Writing:**
- Chapters 1-3: Introduction, Background, Related Work
- Chapters 4-5: System Design, Implementation
- Chapters 6-7: Experiments, Results
- Chapter 8: Conclusion

---

## 🔄 If You Want Approach B (Online Detection)

**Modified Plan:**

### Additional Phases Needed:

**Phase 3.5: ML Deployment**
```
Deploy trained models:
  ├─ Integrate into GitHub Actions
  ├─ Run ML model on every scan
  ├─ Generate alerts when anomaly detected
  └─ Log detection results
```

**Phase 4.5: Environment Reset**
```
Clean main branch:
  ├─ Remove injected vulnerabilities
  ├─ Reset to baseline state
  ├─ Verify clean scans
  └─ Ready for re-attack
```

**Phase 5: Re-attack with Detection**
```
Execute attacks again:
  ├─ Same 24 attack scenarios
  ├─ ML models running live
  ├─ Measure: time-to-detection
  ├─ Track: alerts generated
  └─ Compare: detected vs missed
```

**Additional Metrics:**
- Time to detection (minutes/hours)
- Detection latency
- Real-time accuracy
- Alert fatigue analysis
- Operational overhead

**Timeline:** +4 weeks (12-14 weeks total)

---

## 💡 Recommendation

### **For Masters: Use Approach A**

**Reasons:**
1. ✅ Standard research methodology
2. ✅ Fits semester timeline
3. ✅ Sufficient for Masters contribution
4. ✅ Easier to analyze and write up
5. ✅ Lower risk of technical issues

**You still demonstrate:**
- ML can detect attacks (via test set accuracy)
- Comparative analysis (main vs hardened)
- Feature engineering
- Model evaluation
- Practical implementation

---

### **For PhD Extension: Add Approach B**

**In the future, if pursuing PhD:**
- Build on Masters foundation
- Add online detection component
- Real-time performance analysis
- Production deployment study
- Longitudinal analysis

**This becomes a PhD contribution:**
- Novel: Real-time ML detection in DevOps
- Deeper: Time-series analysis, drift detection
- Broader: Multi-attack wave analysis

---

## 🎯 Current Implementation Status

### What We Have Now:
✅ Automated baseline collection (Approach A, Phase 1)
✅ Feature extraction pipeline
✅ Data validation
✅ Monitoring system

### What We DON'T Have:
❌ ML model deployment to GitHub Actions (needed for Approach B)
❌ Real-time anomaly alerting (needed for Approach B)
❌ Environment reset automation (needed for Approach B)

### Easy to Add Later:
- ML model training scripts (Approach A, Phase 3)
- Evaluation metrics (Approach A, Phase 4)
- Comparative analysis (Approach A, Phase 4)

---

## 📊 Decision Matrix

| Criteria | Approach A | Approach B |
|----------|------------|------------|
| **Timeline** | 8-10 weeks ✅ | 12-14 weeks |
| **Complexity** | Medium ✅ | High |
| **Technical Risk** | Low ✅ | Medium-High |
| **Masters Appropriate** | Yes ✅ | Ambitious |
| **PhD Appropriate** | Baseline | Yes ✅ |
| **Novel Contribution** | Moderate | High |
| **Industry Relevance** | High | Very High |
| **Writing Difficulty** | Medium ✅ | High |

---

## ✅ My Recommendation

**Use Approach A for your Masters thesis.**

**Then, if you pursue PhD:**
- Use your Masters work as Phase 1-2
- Add Approach B elements (online detection, re-attack)
- This becomes a natural PhD extension

**This gives you:**
1. ✅ Successful Masters completion (lower risk)
2. ✅ Solid foundation for PhD (if you choose)
3. ✅ Publication-ready results
4. ✅ Practical, working system

---

## 🚀 Next Steps

**Based on Approach A:**

1. **Continue baseline collection** (2 more weeks)
   - Let automation run
   - Collect 28 days of normal data

2. **Prepare attack scenarios** (now)
   - Review Week 2 curriculum
   - Plan execution order
   - Document expected impacts

3. **Execute attacks** (Week 5-6)
   - Run 24 attack scenarios
   - Collect labeled data

4. **Train ML models** (Week 7-8)
   - Implement RF, XGBoost, IF
   - Evaluate performance

5. **Write thesis** (Week 9-12)
   - Complete all 8 chapters
   - Defend successfully!

---

**Want to stick with Approach A, or add complexity with Approach B?**

I can help implement either - just let me know your preference!
