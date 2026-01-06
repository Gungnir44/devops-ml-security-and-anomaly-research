# Iterative Attack-Train-Reattack Research Guide

> **Sophisticated ML Learning Study: Does Detection Improve with Iterations?**

---

## 🔬 Research Methodology

### **Iterative Learning Approach**

For **EACH** attack scenario, execute a **3-iteration cycle**:

```
ITERATION 1 (Baseline):
  ├─ Execute attack on both branches
  ├─ Wait for security scans (2 AM UTC)
  ├─ Collect artifacts
  ├─ Train ML model with accumulated data
  └─ Deploy ML model for monitoring

ITERATION 2 (ML Monitoring):
  ├─ Re-execute SAME attack on both branches
  ├─ Wait for security scans (2 AM UTC)
  ├─ ML model analyzes results → Detection recorded
  ├─ Collect artifacts
  ├─ Re-train ML with new data (improved)
  └─ Re-deploy model

ITERATION 3 (Improved ML):
  ├─ Re-execute SAME attack on both branches
  ├─ Wait for security scans (2 AM UTC)
  ├─ ML model analyzes results → Detection recorded
  ├─ Collect final artifacts
  └─ Analyze all 3 iterations

ANALYSIS:
  ├─ Compare detection across 3 iterations
  ├─ Calculate learning curve
  ├─ Document findings in thesis
  └─ Move to next attack scenario
```

---

## 🎯 Research Questions Answered

### **Primary RQ: Does ML Detection Improve with Iterative Training?**

**Hypothesis:** ML detection accuracy improves as it sees more examples of the same attack.

**Method:**
- Iteration 1: Train on baseline + first attack instance
- Iteration 2: Re-attack with ML monitoring → Re-train with feedback
- Iteration 3: Re-attack with improved ML → Measure improvement

**Metrics:**
- Detection rate per iteration (0%, 33%, 67%, 100%)
- Confidence scores per iteration
- False positive rate per iteration
- Learning curve visualization

---

### **Secondary RQ: How Many Iterations Needed for Reliable Detection?**

**Hypothesis:** 2-3 iterations sufficient for most attack types.

**Method:** Track when ML first achieves >90% confidence detection

**Expected Results:**
- Easy attacks: Detected in iteration 1
- Medium attacks: Detected by iteration 2
- Hard attacks: Detected by iteration 3
- Very hard attacks: May need >3 iterations

---

### **Tertiary RQ: Does Environment Affect Learning Rate?**

**Hypothesis:** ML learns faster on main branch (more signal) vs. hardened branch (less signal).

**Method:** Run same iterations on BOTH branches, compare:
- Detection rate: main vs. hardened
- Confidence improvement: main vs. hardened
- Features that differ between environments

---

## 📊 Timeline & Execution

### **Per Attack Scenario:**

```
Day 1 (Iteration 1):
  08:00 - Execute attack on both branches
  08:05 - Push to GitHub
  02:00+1 - Security scans run
  03:00+1 - Collect artifacts, train ML, deploy

Day 2 (Iteration 2):
  08:00 - Re-execute attack on both branches
  02:00+1 - Security scans run + ML monitoring
  03:00+1 - Check ML detection, re-train, re-deploy

Day 3 (Iteration 3):
  08:00 - Re-execute attack on both branches
  02:00+1 - Security scans run + ML monitoring
  03:00+1 - Check ML detection, analyze all iterations
  04:00+1 - Document findings in thesis

Total: ~3 days per attack scenario
```

### **For All 24 Scenarios:**
- 24 attacks × 3 days = **72 days** (10 weeks)
- Or select subset (e.g., 10 representative attacks = 30 days)

---

## 🛠️ Script Usage

### **Single Attack Iterative Cycle**

```bash
cd scripts/attacks

# Run complete 3-iteration cycle for attack 2.2
python iterative-attack-pipeline.py --scenario 2.2
```

**What happens:**
1. **Iteration 1:** Executes attack, trains ML (baseline)
2. **Waits:** Prompts you when to continue (after scans complete)
3. **Iteration 2:** Re-attacks, ML monitors, re-trains
4. **Waits:** Prompts you when to continue
5. **Iteration 3:** Final attack, ML monitors, analyzes
6. **Analysis:** Shows detection improvement across iterations
7. **Documentation:** Saves all results to `logs/iterations/`

---

### **Execution Flow Example**

```bash
$ python iterative-attack-pipeline.py --scenario 2.2

================================================================================
  ITERATIVE CYCLE: ATTACK 2.2
================================================================================

Start time: 2025-01-04 08:00:00
Strategy: Execute → Train → Re-execute → Improve → Re-execute → Analyze

================================================================================
  ITERATION 1: BASELINE ATTACK (NO ML MONITORING)
================================================================================

[*] Executing attack on both branches...
[OK] Attack 2.2 executed on both branches

================================================================================
  WAITING FOR SECURITY SCANS
================================================================================

[*] Security scans run at 2 AM UTC
[*] Next scan at: 2025-01-05 02:00:00 UTC
[*] Waiting: 18.0 hours

Press Enter when scans complete, or 's' to skip wait: [ENTER]

[OK] Proceeding with scan results

================================================================================
  COLLECTING ARTIFACTS
================================================================================

[*] Running artifact collection...
[OK] Artifacts collected successfully

================================================================================
  TRAINING ML MODEL (Iteration 1)
================================================================================

[*] Training ML model with all data collected so far...
[OK] ML model trained (iteration 1)

================================================================================
  DEPLOYING ML MODEL
================================================================================

[*] Found 5 model files
[*] Committing models to repository...
[OK] ML model deployed

[OK] Iteration 1 complete - ML model trained and deployed

================================================================================
  ITERATION 2: RE-ATTACK WITH ML MONITORING
================================================================================

[*] Executing attack on both branches...
[OK] Attack 2.2 executed on both branches

[*] Waiting for security scans + ML detection...

Press Enter when scans complete: [ENTER]

================================================================================
  CHECKING ML DETECTION (Iteration 2)
================================================================================

[*] Checking: prediction_20250105_023000.json
[*] ML Prediction: ANOMALY
[*] Confidence: 87.00%

[*] Re-training ML with new data...
[OK] ML model trained (iteration 2)

[OK] Iteration 2 complete - ML detection recorded, model re-trained

================================================================================
  ITERATION 3: FINAL RE-ATTACK WITH IMPROVED ML
================================================================================

[*] Executing attack on both branches...
[OK] Attack 2.2 executed on both branches

Press Enter when scans complete: [ENTER]

================================================================================
  CHECKING ML DETECTION (Iteration 3)
================================================================================

[*] ML Prediction: ANOMALY
[*] Confidence: 95.00%

================================================================================
  ANALYZING 3 ITERATIONS FOR 2.2
================================================================================

--------------------------------------------------------------------------------
DETECTION ANALYSIS
--------------------------------------------------------------------------------
Iteration 1: N/A          (Confidence: N/A)      # No ML yet
Iteration 2: DETECTED     (Confidence: 87.00%)   # First detection
Iteration 3: DETECTED     (Confidence: 95.00%)   # Improved confidence

--------------------------------------------------------------------------------
Detection Rate: 2/3 iterations
--------------------------------------------------------------------------------

[OK] Analysis saved: analysis_20250107_030000.json

================================================================================
  ITERATIVE CYCLE COMPLETE: 2.2
================================================================================

End time: 2025-01-07 03:00:00

Detection Rate: 66.7%

Next Steps:
1. Review iteration logs in logs/iterations/
2. Document findings in thesis
3. Move to next attack scenario
```

---

## 📁 Output Files

### **Iteration Logs**

```
scripts/attacks/logs/iterations/
├── 2_2/  # Attack scenario 2.2
│   ├── iteration_1_20250104_080000.json
│   ├── iteration_2_20250105_080000.json
│   ├── iteration_3_20250106_080000.json
│   └── analysis_20250107_030000.json
├── 3_1/  # Attack scenario 3.1
│   ├── iteration_1_*.json
│   ├── iteration_2_*.json
│   ├── iteration_3_*.json
│   └── analysis_*.json
...
```

### **Iteration JSON Format**

```json
{
  "scenario_id": "2.2",
  "iteration": 2,
  "timestamp": "2025-01-05T08:00:00",
  "attack_executed": true,
  "scans_completed": true,
  "ml_trained": true,
  "ml_deployed": true,
  "ml_detection": {
    "detected": true,
    "confidence": 0.87,
    "prediction": { /* full ML prediction */ }
  }
}
```

### **Analysis JSON Format**

```json
{
  "scenario_id": "2.2",
  "total_iterations": 3,
  "detected_count": 2,
  "detection_rate": 0.667,
  "iterations": [
    { /* iteration 1 data */ },
    { /* iteration 2 data */ },
    { /* iteration 3 data */ }
  ]
}
```

---

## 📈 Thesis Integration

### **Chapter 6: Experiments - Iterative Methodology**

**Section 6.1: Iterative Attack-Train-Reattack Design**
- Rationale for 3 iterations
- Dual-branch execution strategy
- Timeline and execution schedule
- Data collection procedures

**Section 6.2: Execution Results Per Attack**

For each attack scenario, document:

```markdown
#### Attack 2.2: Cryptomining

**Iteration 1 (Baseline):**
- Executed: 2025-01-04 08:00
- Scanned: 2025-01-05 02:00
- ML Detection: N/A (baseline)
- Model trained with: 56 baseline + 2 attack samples

**Iteration 2 (First ML Monitoring):**
- Executed: 2025-01-05 08:00
- Scanned: 2025-01-06 02:00
- ML Detection: DETECTED ✓
- Confidence: 87.0%
- Model re-trained with: 56 baseline + 4 attack samples

**Iteration 3 (Improved ML):**
- Executed: 2025-01-06 08:00
- Scanned: 2025-01-07 02:00
- ML Detection: DETECTED ✓
- Confidence: 95.0%

**Learning Curve:**
- Iteration 1 → 2: Achieved detection (0% → 87%)
- Iteration 2 → 3: Improved confidence (87% → 95%)
- Improvement rate: +8% confidence per iteration

**Key Findings:**
- Attack detected by iteration 2 (medium difficulty confirmed)
- Confidence improved with additional training data
- Cryptomining patterns strongly distinguishable from baseline
```

---

### **Chapter 7: Results - Aggregated Analysis**

**Section 7.1: Detection Improvement Across Iterations**

```
Table: ML Detection Rate by Iteration

Attack Type          | Iter 1 | Iter 2 | Iter 3 | Final Detection
---------------------|--------|--------|--------|----------------
Secrets in Logs      | N/A    | 92%    | 98%    | ✓ High
Cryptomining         | N/A    | 87%    | 95%    | ✓ High
Malicious Dependency | N/A    | 45%    | 78%    | ✓ Medium
Approval Bypass      | N/A    | 12%    | 34%    | ✗ Low
...

Overall Avg:         | N/A    | 61%    | 76%    | +15% improvement
```

**Section 7.2: Learning Curves Per Attack Type**

Include visualization:
- X-axis: Iteration number (1, 2, 3)
- Y-axis: Detection confidence (0-100%)
- Lines: One per attack scenario
- Shows: Which attacks learn faster/slower

**Section 7.3: Environment Comparison (Main vs. Hardened)**

```
Table: Detection Rate by Environment

Attack Type          | Main Branch | Hardened Branch | Difference
---------------------|-------------|-----------------|------------
Secrets in Logs      | 98%         | 87%             | +11% main
Cryptomining         | 95%         | 92%             | +3% main
Malicious Dependency | 78%         | 65%             | +13% main
...

Overall Avg:         | 82%         | 71%             | +11% main
```

**Interpretation:**
- Main branch has more attack signal (less defense noise)
- Hardened branch attacks more subtle (defenses mask patterns)
- ML performs better on main branch (expected)

---

### **Chapter 8: Discussion - Key Insights**

**RQ1: Does ML detection improve with iterative training?**
→ **YES**: Average improvement of 15% from iteration 2 to 3

**RQ2: How many iterations needed for reliable detection?**
→ **2-3 iterations**: 80% of attacks detected by iteration 3

**RQ3: Does environment affect learning rate?**
→ **YES**: Main branch detections 11% higher than hardened on average

**RQ4: Which attack types are hardest to detect?**
→ **Evasion & Subtle attacks**: Approval bypass, log tampering
→ **Easiest**: Secrets in logs, cryptomining (high signal)

---

## 🎯 Recommended Execution Strategy

### **Option 1: Full Study (24 attacks × 3 iterations)**
- Timeline: 72 days (10 weeks)
- Data: Maximum comprehensive dataset
- Best for: PhD-level research

### **Option 2: Representative Sample (10 attacks × 3 iterations)** ⭐ **RECOMMENDED**
- Timeline: 30 days (4 weeks)
- Select 10 diverse attacks:
  - 2 easy (8.1, 2.2)
  - 4 medium (1.1, 3.1, 4.1, 5.1)
  - 4 hard (2.3, 7.1, 8.5, 9.4)
- Covers all attack categories
- Best for: Masters thesis timeline

### **Option 3: Proof of Concept (3 attacks × 3 iterations)**
- Timeline: 9 days
- Select 3 representative attacks:
  - 8.1 (easy - secrets)
  - 3.1 (medium - supply chain)
  - 7.1 (hard - evasion)
- Best for: Quick validation of methodology

---

## ✅ Execution Checklist

### **Prerequisites:**
- [x] Phase 1 baseline collection complete (29 days)
- [x] Attack automation scripts created
- [x] ML training pipeline ready
- [x] Dual-branch repository setup
- [x] Iterative pipeline script created

### **Per Attack Scenario:**

**Day 1:**
- [ ] Execute attack on both branches (iteration 1)
- [ ] Verify commits pushed
- [ ] Wait for 2 AM UTC scan

**Day 2:**
- [ ] Verify scans completed
- [ ] Run artifact collection
- [ ] Train ML model (iteration 1)
- [ ] Deploy ML model to repository
- [ ] Re-execute attack on both branches (iteration 2)
- [ ] Wait for 2 AM UTC scan

**Day 3:**
- [ ] Verify scans + ML detection completed
- [ ] Check ML detection results (iteration 2)
- [ ] Re-train ML model (iteration 2)
- [ ] Re-deploy ML model
- [ ] Re-execute attack on both branches (iteration 3)
- [ ] Wait for 2 AM UTC scan

**Day 4:**
- [ ] Verify scans + ML detection completed
- [ ] Check ML detection results (iteration 3)
- [ ] Analyze all 3 iterations
- [ ] Document findings in thesis
- [ ] Move to next attack scenario

---

## 🚀 Quick Start

**Start first iterative cycle:**

```bash
cd "C:\Users\joshu\Desktop\DevOps Project\scripts\attacks"

# Run 3-iteration cycle for attack 8.1 (Secrets in Logs)
python iterative-attack-pipeline.py --scenario 8.1
```

**The script will:**
1. Execute attack on both branches
2. Prompt you to press Enter when scans complete
3. Collect artifacts and train ML
4. Deploy ML model
5. Re-execute attack
6. Prompt you to press Enter when scans complete
7. Check ML detection results
8. Re-execute attack (3rd time)
9. Analyze all 3 iterations
10. Save comprehensive results

**You provide:**
- Press Enter when scans complete (manual checkpoints)
- Review ML detection results between iterations
- Document findings in thesis

**Script automates:**
- Attack execution on both branches
- Artifact collection
- ML training and deployment
- Detection analysis
- Results logging

---

**Ready for sophisticated iterative ML research!** 🔬

This methodology answers the critical question:
**"Does ML get better at detecting attacks with experience?"**

And you'll have empirical data to prove it! 📊

*Generated with Claude Code*
*Last Updated: January 4, 2025*
