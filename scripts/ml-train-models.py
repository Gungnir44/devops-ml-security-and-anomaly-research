#!/usr/bin/env python3
"""
ML Model Training Script - Phase 3
Trains anomaly detection models on collected baseline + attack data
"""

import sys
import json
import pickle
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("[WARN] XGBoost not installed. Install with: pip install xgboost")


class MLModelTrainer:
    """Train and evaluate ML models for anomaly detection"""

    def __init__(self, data_dir='../DevOps Master\'s Degree Project/ml-pipeline/output'):
        self.data_dir = Path(data_dir)
        self.models_dir = Path('../models')
        self.models_dir.mkdir(exist_ok=True)

        self.models = {}
        self.results = {}
        self.scaler = StandardScaler()

    def load_data(self):
        """Load and prepare training data"""
        print("\n" + "="*80)
        print("STEP 1: LOADING DATA")
        print("="*80)

        # Load baseline (normal) data
        baseline_file = self.data_dir / 'features_main_branch.csv'
        hardened_file = self.data_dir / 'features_hardened_branch.csv'

        if not baseline_file.exists():
            print(f"[ERROR] Baseline data not found: {baseline_file}")
            print("Run feature extraction first!")
            sys.exit(1)

        # Load normal samples
        df_baseline = pd.read_csv(baseline_file)
        df_baseline['label'] = 'normal'
        df_baseline['label_binary'] = 0

        print(f"[OK] Loaded {len(df_baseline)} baseline samples")

        # Load hardened branch (also normal)
        if hardened_file.exists():
            df_hardened = pd.read_csv(hardened_file)
            df_hardened['label'] = 'normal'
            df_hardened['label_binary'] = 0
            print(f"[OK] Loaded {len(df_hardened)} hardened samples")
        else:
            df_hardened = pd.DataFrame()

        # Load attack data (if available - Phase 3)
        attack_file = self.data_dir / 'features_attack_data.csv'
        if attack_file.exists():
            df_attacks = pd.read_csv(attack_file)
            df_attacks['label_binary'] = 1  # attack = 1
            print(f"[OK] Loaded {len(df_attacks)} attack samples")
        else:
            print("[WARN] No attack data found yet - using synthetic for testing")
            # Create small synthetic attack samples for testing
            df_attacks = df_baseline.sample(n=min(10, len(df_baseline))).copy()
            df_attacks['label'] = 'attack'
            df_attacks['label_binary'] = 1
            # Modify some features to simulate attacks
            for col in df_attacks.select_dtypes(include=[np.number]).columns:
                if col not in ['label_binary']:
                    df_attacks[col] = df_attacks[col] * np.random.uniform(1.5, 3.0, len(df_attacks))

        # Combine all data
        df_combined = pd.concat([df_baseline, df_hardened, df_attacks], ignore_index=True)

        # Separate features and labels
        feature_cols = [col for col in df_combined.columns
                       if col not in ['label', 'label_binary', 'timestamp', 'date', 'branch']]

        X = df_combined[feature_cols].fillna(0)  # Handle missing values
        y = df_combined['label_binary']

        print(f"\n[OK] Dataset prepared:")
        print(f"     Total samples: {len(X)}")
        print(f"     Normal: {sum(y == 0)} | Attack: {sum(y == 1)}")
        print(f"     Features: {len(feature_cols)}")

        return X, y, feature_cols

    def split_data(self, X, y, test_size=0.3, random_state=42):
        """Split data into train/test sets"""
        print("\n" + "="*80)
        print("STEP 2: SPLITTING DATA")
        print("="*80)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        print(f"Training set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        print(f"Train split: Normal={sum(y_train==0)}, Attack={sum(y_train==1)}")
        print(f"Test split: Normal={sum(y_test==0)}, Attack={sum(y_test==1)}")

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        return X_train_scaled, X_test_scaled, y_train, y_test

    def train_random_forest(self, X_train, y_train):
        """Train Random Forest classifier (baseline model)"""
        print("\n[*] Training Random Forest...")

        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )

        model.fit(X_train, y_train)
        self.models['random_forest'] = model

        print("[OK] Random Forest trained")
        return model

    def train_xgboost(self, X_train, y_train):
        """Train XGBoost classifier (comparison model)"""
        if not XGBOOST_AVAILABLE:
            print("[SKIP] XGBoost not available")
            return None

        print("\n[*] Training XGBoost...")

        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss'
        )

        model.fit(X_train, y_train)
        self.models['xgboost'] = model

        print("[OK] XGBoost trained")
        return model

    def train_isolation_forest(self, X_train):
        """Train Isolation Forest (unsupervised anomaly detection)"""
        print("\n[*] Training Isolation Forest...")

        model = IsolationForest(
            n_estimators=100,
            contamination=0.1,  # Expect ~10% anomalies
            random_state=42,
            n_jobs=-1
        )

        model.fit(X_train)
        self.models['isolation_forest'] = model

        print("[OK] Isolation Forest trained")
        return model

    def evaluate_model(self, model, model_name, X_test, y_test, is_unsupervised=False):
        """Evaluate model performance"""
        print(f"\n[*] Evaluating {model_name}...")

        if is_unsupervised:
            # Isolation Forest returns -1 for anomalies, 1 for normal
            y_pred_raw = model.predict(X_test)
            y_pred = np.where(y_pred_raw == -1, 1, 0)  # Convert to 0/1
        else:
            y_pred = model.predict(X_test)

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)

        results = {
            'model': model_name,
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'confusion_matrix': {
                'true_negative': int(tn),
                'false_positive': int(fp),
                'false_negative': int(fn),
                'true_positive': int(tp)
            },
            'test_samples': len(y_test)
        }

        # Try to calculate AUC for supervised models
        if not is_unsupervised and hasattr(model, 'predict_proba'):
            try:
                y_proba = model.predict_proba(X_test)[:, 1]
                auc = roc_auc_score(y_test, y_proba)
                results['auc'] = float(auc)
            except:
                pass

        self.results[model_name] = results

        # Print results
        print(f"\n{model_name} Results:")
        print(f"  Accuracy:  {accuracy:.3f}")
        print(f"  Precision: {precision:.3f}")
        print(f"  Recall:    {recall:.3f}")
        print(f"  F1-Score:  {f1:.3f}")
        if 'auc' in results:
            print(f"  AUC:       {results['auc']:.3f}")
        print(f"\n  Confusion Matrix:")
        print(f"    TN: {tn:4d}  |  FP: {fp:4d}")
        print(f"    FN: {fn:4d}  |  TP: {tp:4d}")

        return results

    def save_models(self):
        """Save trained models to disk"""
        print("\n" + "="*80)
        print("STEP 4: SAVING MODELS")
        print("="*80)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save each model
        for model_name, model in self.models.items():
            model_file = self.models_dir / f'{model_name}_{timestamp}.pkl'
            latest_file = self.models_dir / f'{model_name}_latest.pkl'

            joblib.dump(model, model_file)
            joblib.dump(model, latest_file)

            print(f"[OK] Saved {model_name}: {model_file.name}")

        # Save scaler
        scaler_file = self.models_dir / f'scaler_{timestamp}.pkl'
        latest_scaler = self.models_dir / 'scaler_latest.pkl'
        joblib.dump(self.scaler, scaler_file)
        joblib.dump(self.scaler, latest_scaler)
        print(f"[OK] Saved scaler: {scaler_file.name}")

        # Save results
        results_file = self.models_dir / f'training_results_{timestamp}.json'
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"[OK] Saved results: {results_file.name}")

        # Save model metadata
        metadata = {
            'timestamp': timestamp,
            'models': list(self.models.keys()),
            'results': self.results,
            'training_date': datetime.now().isoformat()
        }

        metadata_file = self.models_dir / 'model_metadata.json'
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"[OK] Saved metadata: {metadata_file.name}")

    def run_full_training(self):
        """Execute complete training pipeline"""
        print("\n" + "="*80)
        print("ML MODEL TRAINING PIPELINE - APPROACH B")
        print("="*80)
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Load data
        X, y, feature_cols = self.load_data()

        # Split data
        X_train, X_test, y_train, y_test = self.split_data(X, y)

        # Train models
        print("\n" + "="*80)
        print("STEP 3: TRAINING MODELS")
        print("="*80)

        self.train_random_forest(X_train, y_train)
        self.train_xgboost(X_train, y_train)
        self.train_isolation_forest(X_train)

        # Evaluate models
        print("\n" + "="*80)
        print("MODEL EVALUATION")
        print("="*80)

        self.evaluate_model(self.models['random_forest'], 'Random Forest', X_test, y_test)

        if 'xgboost' in self.models and self.models['xgboost'] is not None:
            self.evaluate_model(self.models['xgboost'], 'XGBoost', X_test, y_test)

        self.evaluate_model(
            self.models['isolation_forest'],
            'Isolation Forest',
            X_test, y_test,
            is_unsupervised=True
        )

        # Save everything
        self.save_models()

        # Summary
        print("\n" + "="*80)
        print("TRAINING COMPLETE")
        print("="*80)
        print(f"Models trained: {len(self.models)}")
        print(f"Models saved to: {self.models_dir.absolute()}")

        # Print best model
        best_model = max(self.results.items(), key=lambda x: x[1]['f1_score'])
        print(f"\nBest model: {best_model[0]} (F1: {best_model[1]['f1_score']:.3f})")

        print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)


if __name__ == '__main__':
    trainer = MLModelTrainer()
    trainer.run_full_training()
