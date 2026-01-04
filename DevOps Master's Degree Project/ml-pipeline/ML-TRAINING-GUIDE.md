# ML Model Training Guide

## Quick Start

### 1. Install Dependencies

```bash
cd ml-pipeline
pip install -r requirements.txt
```

**Required packages:**
- numpy, pandas, scikit-learn, xgboost
- matplotlib, seaborn (for visualizations)
- joblib (for model persistence)

### 2. Train Baseline Models

```bash
# Train all models on comparison data (main vs hardened)
python train_baseline_models.py
```

This will train:
- ✅ **Random Forest** - Best for tabular data
- ✅ **XGBoost** - Often highest accuracy
- ✅ **Logistic Regression** - Simple baseline
- ✅ **SVM** - Good for binary classification
- ✅ **Isolation Forest** - Anomaly detection

**Training time:** ~2-5 minutes

---

## What You Get

### Models Trained

All models saved in `models/` directory:
```
models/
├── random_forest.joblib
├── xgboost.joblib
├── logistic_regression.joblib
├── svm.joblib
├── isolation_forest.joblib
└── training_results.json
```

### Results & Visualizations

Generated in `results/` directory:
```
results/
├── model_comparison.csv           # Performance comparison table
├── feature_importance.png          # Top 20 features per model
├── confusion_matrices.png          # Confusion matrices for all models
├── feature_importance_*.csv        # Detailed feature rankings
└── training_report_*.md            # Complete training summary
```

### Performance Metrics

For each model you get:
- **Accuracy** - Overall correctness
- **Precision** - True positives / (True positives + False positives)
- **Recall** - True positives / (True positives + False negatives)
- **F1-Score** - Harmonic mean of precision and recall
- **ROC-AUC** - Area under ROC curve
- **Confusion Matrix** - Detailed prediction breakdown
- **Cross-Validation** - 5-fold CV scores (for some models)

---

## Usage Examples

### Train All Models (Default)

```bash
python train_baseline_models.py
```

Uses:
- Main branch: `output/features_main_branch.csv`
- Hardened branch: `output/features_hardened_local.csv`

### Train Specific Models Only

```bash
# Only Random Forest
python train_baseline_models.py --models rf

# Random Forest and XGBoost
python train_baseline_models.py --models rf,xgb

# All except SVM (if it's too slow)
python train_baseline_models.py --models rf,xgb,lr,if
```

**Model codes:**
- `rf` = Random Forest
- `xgb` = XGBoost
- `lr` = Logistic Regression
- `svm` = Support Vector Machine
- `if` = Isolation Forest

### Train on Time-Series Data

```bash
# After running automated-weekly-collection.py
python train_baseline_models.py --data-file output/time_series_dataset.csv
```

This uses accumulated weekly data instead of just the baseline comparison.

---

## Understanding the Results

### Model Comparison Table

Example output:
```
Model                  Accuracy  Precision  Recall  F1-Score  ROC-AUC
XGBoost                0.9500    0.9600     0.9400  0.9500    0.9800
Random Forest          0.9400    0.9500     0.9300  0.9400    0.9750
Logistic Regression    0.8800    0.8900     0.8700  0.8800    0.9200
SVM                    0.9200    0.9300     0.9100  0.9200    0.9500
Isolation Forest       0.7500    0.7800     0.7200  0.7500    N/A
```

**What this means:**
- **XGBoost** is likely your best model (highest F1 and ROC-AUC)
- **Isolation Forest** is unsupervised (lower scores expected)
- **All models > 0.85 accuracy** = Good discrimination between vulnerable and secured code

### Feature Importance

Top features tell you **which security metrics matter most**:

Example:
```
Feature                        Importance
vuln_critical_count           0.1250
container_vulnerabilities     0.0980
sast_code_smells              0.0850
security_risk_score           0.0720
...
```

**Interpretation:**
- Critical vulnerabilities are the #1 predictor
- Container security issues are highly important
- Code quality (SAST) matters significantly

**Use this to:**
- Focus remediation efforts on high-importance features
- Simplify your model (only use top 50 features)
- Explain to stakeholders what drives security posture

### Confusion Matrix

```
                Predicted
                Secured  Vulnerable
Actual  Secured    45        5
        Vulnerable  3        47
```

**Reading this:**
- **45** correctly identified as secured ✅
- **47** correctly identified as vulnerable ✅
- **5** false positives (thought vulnerable, actually secured)
- **3** false negatives (thought secured, actually vulnerable) ⚠️

**False negatives are worse** in security - you missed actual vulnerabilities!

---

## Using Trained Models for Prediction

### Load a Saved Model

```python
import joblib
import pandas as pd

# Load the best model (e.g., XGBoost)
model = joblib.load('models/xgboost.joblib')
scaler = joblib.load('models/scaler.joblib')  # If you saved it

# Load new data
new_data = pd.read_csv('output/features_new_branch.csv')

# Scale features (important!)
X_scaled = scaler.transform(new_data)

# Predict
predictions = model.predict(X_scaled)
probabilities = model.predict_proba(X_scaled)

print(f"Predicted class: {predictions[0]}")  # 0 = secured, 1 = vulnerable
print(f"Vulnerability probability: {probabilities[0][1]:.2%}")
```

### Real-Time Monitoring

```python
# Monitor new commits/deployments
def check_security_posture(feature_vector):
    """Check if new code is vulnerable."""
    model = joblib.load('models/xgboost.joblib')

    # Predict
    is_vulnerable = model.predict([feature_vector])[0]
    confidence = model.predict_proba([feature_vector])[0][1]

    if is_vulnerable and confidence > 0.8:
        send_alert(f"High vulnerability risk detected: {confidence:.1%}")

    return is_vulnerable, confidence
```

---

## Expected Performance

### With Baseline Data (1 sample each branch)

**Challenges:**
- Very limited training data (2 total samples)
- High risk of overfitting
- May need synthetic data augmentation

**Expected accuracy:** 60-80% (limited by small dataset)

### With 2 Weeks Time-Series Data (~14 samples)

**Better:**
- More training examples
- Can capture temporal patterns
- More reliable metrics

**Expected accuracy:** 75-90%

### With 4 Weeks Time-Series Data (~28 samples)

**Best:**
- Sufficient for reliable models
- Can train LSTM/temporal models
- High confidence in results

**Expected accuracy:** 85-95%

---

## Troubleshooting

### Error: "No module named 'xgboost'"

```bash
pip install xgboost
```

Or skip XGBoost:
```bash
python train_baseline_models.py --models rf,lr,if
```

### Warning: "Class imbalance detected"

This is normal if you have many more "main" samples than "hardened". Solutions:
- Use class weights (already handled in the script)
- Collect more hardened branch data
- Use SMOTE for oversampling

### Low accuracy (<70%)

Possible causes:
- Not enough training data (collect more weeks)
- Features too similar between branches
- Need feature engineering

Try:
1. Collect more time-series data
2. Use feature selection (top 50 features only)
3. Try ensemble methods

---

## Next Steps

### Week 1 (Now)

1. ✅ Train baseline models: `python train_baseline_models.py`
2. ✅ Review feature importance
3. ✅ Document top 10 features in thesis

### Week 2

4. Train on 2-week time-series data
5. Compare performance vs baseline
6. Create visualizations for thesis

### Week 3

7. Implement ensemble methods (combine multiple models)
8. Test model on new branches
9. Write Results chapter

### Week 4

10. Train LSTM/time-series models
11. Compare temporal vs static models
12. Finalize thesis experiments

---

## Advanced: Custom Model Configuration

### Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

# Example: Tune Random Forest
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_
```

### Feature Selection

```python
from sklearn.feature_selection import SelectKBest, f_classif

# Select top 50 features
selector = SelectKBest(f_classif, k=50)
X_train_selected = selector.fit_transform(X_train, y_train)
X_test_selected = selector.transform(X_test)

# Train on reduced features
model.fit(X_train_selected, y_train)
```

### Ensemble Methods

```python
from sklearn.ensemble import VotingClassifier

# Combine multiple models
ensemble = VotingClassifier(
    estimators=[
        ('rf', RandomForestClassifier()),
        ('xgb', XGBClassifier()),
        ('lr', LogisticRegression())
    ],
    voting='soft'  # Use predicted probabilities
)

ensemble.fit(X_train, y_train)
```

---

## Research Implications

### For Your Thesis

**Chapter: Methodology**
- Document the 5 algorithms you tested
- Explain why you chose them (standard ML baselines)
- Describe train/test split (80/20)
- Mention cross-validation for robustness

**Chapter: Results**
- Include the model comparison table
- Discuss feature importance findings
- Show confusion matrices
- Compare performance metrics

**Chapter: Discussion**
- Interpret which models work best and why
- Discuss feature importance implications
- Explain what this tells us about DevOps security

### Key Findings to Highlight

1. **Binary classification achieves XX% accuracy** distinguishing vulnerable from secured code
2. **Top 3 features** that predict security posture are [list from feature importance]
3. **XGBoost outperforms** simpler models, suggesting complex feature interactions
4. **Anomaly detection** can identify unusual patterns without labeled data

---

## Files Reference

**Training Script:**
- `train_baseline_models.py` - Main training pipeline

**Output:**
- `models/*.joblib` - Saved trained models
- `results/model_comparison.csv` - Performance table
- `results/feature_importance_*.csv` - Feature rankings
- `results/*.png` - Visualizations
- `results/training_report_*.md` - Full summary

**Dependencies:**
- `requirements.txt` - Required Python packages

---

**Ready to train your first models?**

```bash
cd ml-pipeline
pip install -r requirements.txt
python train_baseline_models.py
```

🎯 **Start now, then collect more data over 4 weeks for better models!**
