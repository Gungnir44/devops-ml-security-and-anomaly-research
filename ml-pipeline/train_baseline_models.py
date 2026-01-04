#!/usr/bin/env python3
"""
Baseline ML Model Training
===========================

Train and evaluate ML models for DevOps security anomaly detection.

Models trained:
1. Binary Classifier (vulnerable vs secured branches)
   - Random Forest
   - XGBoost
   - Logistic Regression
   - SVM

2. Anomaly Detector (detect unusual patterns)
   - Isolation Forest
   - One-Class SVM

Usage:
    python train_baseline_models.py [--data-file FILE] [--models all|rf|xgb|lr|svm|if]

Examples:
    # Train all models on comparison data
    python train_baseline_models.py

    # Train only Random Forest
    python train_baseline_models.py --models rf

    # Use time-series dataset
    python train_baseline_models.py --data-file output/time_series_dataset.csv
"""

import argparse
import json
import warnings
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve, precision_recall_curve
)
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, OneClassSVM
import joblib

# Suppress warnings
warnings.filterwarnings('ignore')

# Try to import XGBoost (optional dependency)
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("[Warning] XGBoost not installed. Install with: pip install xgboost")


class BaselineModelTrainer:
    """Train and evaluate baseline ML models for security anomaly detection."""

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path(__file__).parent / "models"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.results_dir = Path(__file__).parent / "results"
        self.results_dir.mkdir(parents=True, exist_ok=True)

        self.models = {}
        self.results = {}
        self.feature_importance = {}

        # Set style for visualizations
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")

    def load_comparison_data(self, main_file: Path, hardened_file: Path) -> Tuple[pd.DataFrame, np.ndarray]:
        """Load and prepare comparison data (main vs hardened branches)."""
        print("\n" + "=" * 80)
        print("Loading Comparison Data")
        print("=" * 80)

        # Load both datasets
        df_main = pd.read_csv(main_file)
        df_hardened = pd.read_csv(hardened_file)

        print(f"Main branch: {len(df_main)} samples, {len(df_main.columns)} features")
        print(f"Hardened branch: {len(df_hardened)} samples, {len(df_hardened.columns)} features")

        # Add labels
        df_main['label'] = 1  # Vulnerable
        df_hardened['label'] = 0  # Secured

        # Combine
        df = pd.concat([df_main, df_hardened], ignore_index=True)

        # Separate features and labels
        y = df['label'].values
        X = df.drop('label', axis=1)

        print(f"\nCombined dataset:")
        print(f"  Total samples: {len(df)}")
        print(f"  Vulnerable (main): {sum(y == 1)}")
        print(f"  Secured (hardened): {sum(y == 0)}")
        print(f"  Features: {X.shape[1]}")

        return X, y

    def load_time_series_data(self, time_series_file: Path) -> Tuple[pd.DataFrame, np.ndarray]:
        """Load and prepare time-series data."""
        print("\n" + "=" * 80)
        print("Loading Time-Series Data")
        print("=" * 80)

        df = pd.read_csv(time_series_file)

        print(f"Total samples: {len(df)}")
        print(f"Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"Branches: {df['branch'].unique().tolist()}")

        # Create binary labels from branch
        df['label'] = (df['branch'] == 'main').astype(int)  # 1 = vulnerable, 0 = secured

        # Drop metadata columns
        X = df.drop(['date', 'branch', 'label', 'timestamp'], axis=1, errors='ignore')
        y = df['label'].values

        print(f"\nDataset prepared:")
        print(f"  Total samples: {len(df)}")
        print(f"  Vulnerable (main): {sum(y == 1)}")
        print(f"  Secured (hardened): {sum(y == 0)}")
        print(f"  Features: {X.shape[1]}")

        return X, y

    def preprocess_data(self, X: pd.DataFrame, y: np.ndarray, test_size: float = 0.2) -> Dict:
        """Preprocess data: handle missing values, scale, split."""
        print("\n" + "=" * 80)
        print("Preprocessing Data")
        print("=" * 80)

        # Handle missing values
        if X.isnull().any().any():
            print(f"Filling {X.isnull().sum().sum()} missing values with 0")
            X = X.fillna(0)

        # Store feature names
        feature_names = X.columns.tolist()

        # Convert to numpy
        X_array = X.values

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_array, y, test_size=test_size, random_state=42, stratify=y
        )

        print(f"\nTrain set: {len(X_train)} samples")
        print(f"  Vulnerable: {sum(y_train == 1)}")
        print(f"  Secured: {sum(y_train == 0)}")

        print(f"\nTest set: {len(X_test)} samples")
        print(f"  Vulnerable: {sum(y_test == 1)}")
        print(f"  Secured: {sum(y_test == 0)}")

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        print(f"\n✓ Data scaled using StandardScaler")

        return {
            'X_train': X_train_scaled,
            'X_test': X_test_scaled,
            'y_train': y_train,
            'y_test': y_test,
            'scaler': scaler,
            'feature_names': feature_names
        }

    def train_random_forest(self, data: Dict) -> Dict:
        """Train Random Forest classifier."""
        print("\n" + "=" * 80)
        print("Training Random Forest")
        print("=" * 80)

        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )

        # Train
        model.fit(data['X_train'], data['y_train'])

        # Predict
        y_pred = model.predict(data['X_test'])
        y_pred_proba = model.predict_proba(data['X_test'])[:, 1]

        # Evaluate
        results = self._evaluate_classifier(
            data['y_test'], y_pred, y_pred_proba,
            model_name="Random Forest"
        )

        # Feature importance
        self.feature_importance['random_forest'] = pd.DataFrame({
            'feature': data['feature_names'],
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)

        # Cross-validation
        cv_scores = cross_val_score(
            model, data['X_train'], data['y_train'],
            cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
            scoring='accuracy',
            n_jobs=-1
        )
        results['cv_accuracy_mean'] = cv_scores.mean()
        results['cv_accuracy_std'] = cv_scores.std()

        print(f"\n✓ Random Forest trained")
        print(f"  Accuracy: {results['accuracy']:.4f}")
        print(f"  F1-Score: {results['f1']:.4f}")
        print(f"  ROC-AUC: {results['roc_auc']:.4f}")
        print(f"  CV Accuracy: {results['cv_accuracy_mean']:.4f} ± {results['cv_accuracy_std']:.4f}")

        self.models['random_forest'] = model
        self.results['random_forest'] = results

        return results

    def train_xgboost(self, data: Dict) -> Dict:
        """Train XGBoost classifier."""
        if not XGBOOST_AVAILABLE:
            print("\n[Skip] XGBoost not available")
            return {}

        print("\n" + "=" * 80)
        print("Training XGBoost")
        print("=" * 80)

        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1,
            use_label_encoder=False,
            eval_metric='logloss'
        )

        # Train
        model.fit(data['X_train'], data['y_train'])

        # Predict
        y_pred = model.predict(data['X_test'])
        y_pred_proba = model.predict_proba(data['X_test'])[:, 1]

        # Evaluate
        results = self._evaluate_classifier(
            data['y_test'], y_pred, y_pred_proba,
            model_name="XGBoost"
        )

        # Feature importance
        self.feature_importance['xgboost'] = pd.DataFrame({
            'feature': data['feature_names'],
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)

        print(f"\n✓ XGBoost trained")
        print(f"  Accuracy: {results['accuracy']:.4f}")
        print(f"  F1-Score: {results['f1']:.4f}")
        print(f"  ROC-AUC: {results['roc_auc']:.4f}")

        self.models['xgboost'] = model
        self.results['xgboost'] = results

        return results

    def train_logistic_regression(self, data: Dict) -> Dict:
        """Train Logistic Regression classifier."""
        print("\n" + "=" * 80)
        print("Training Logistic Regression")
        print("=" * 80)

        model = LogisticRegression(
            max_iter=1000,
            random_state=42,
            n_jobs=-1
        )

        # Train
        model.fit(data['X_train'], data['y_train'])

        # Predict
        y_pred = model.predict(data['X_test'])
        y_pred_proba = model.predict_proba(data['X_test'])[:, 1]

        # Evaluate
        results = self._evaluate_classifier(
            data['y_test'], y_pred, y_pred_proba,
            model_name="Logistic Regression"
        )

        print(f"\n✓ Logistic Regression trained")
        print(f"  Accuracy: {results['accuracy']:.4f}")
        print(f"  F1-Score: {results['f1']:.4f}")
        print(f"  ROC-AUC: {results['roc_auc']:.4f}")

        self.models['logistic_regression'] = model
        self.results['logistic_regression'] = results

        return results

    def train_svm(self, data: Dict) -> Dict:
        """Train SVM classifier."""
        print("\n" + "=" * 80)
        print("Training SVM")
        print("=" * 80)

        model = SVC(
            kernel='rbf',
            C=1.0,
            probability=True,
            random_state=42
        )

        # Train
        model.fit(data['X_train'], data['y_train'])

        # Predict
        y_pred = model.predict(data['X_test'])
        y_pred_proba = model.predict_proba(data['X_test'])[:, 1]

        # Evaluate
        results = self._evaluate_classifier(
            data['y_test'], y_pred, y_pred_proba,
            model_name="SVM"
        )

        print(f"\n✓ SVM trained")
        print(f"  Accuracy: {results['accuracy']:.4f}")
        print(f"  F1-Score: {results['f1']:.4f}")
        print(f"  ROC-AUC: {results['roc_auc']:.4f}")

        self.models['svm'] = model
        self.results['svm'] = results

        return results

    def train_isolation_forest(self, data: Dict) -> Dict:
        """Train Isolation Forest for anomaly detection."""
        print("\n" + "=" * 80)
        print("Training Isolation Forest (Anomaly Detection)")
        print("=" * 80)

        model = IsolationForest(
            n_estimators=100,
            contamination=0.1,  # Expect 10% anomalies
            random_state=42,
            n_jobs=-1
        )

        # Train on all data (unsupervised)
        X_all = np.vstack([data['X_train'], data['X_test']])
        model.fit(X_all)

        # Predict (-1 = anomaly, 1 = normal)
        y_pred = model.predict(data['X_test'])
        y_pred_binary = (y_pred == -1).astype(int)  # Convert to 0/1

        # Anomaly scores
        anomaly_scores = model.score_samples(data['X_test'])

        # Evaluate (treating anomalies as vulnerable)
        results = self._evaluate_anomaly_detector(
            data['y_test'], y_pred_binary, anomaly_scores,
            model_name="Isolation Forest"
        )

        print(f"\n✓ Isolation Forest trained")
        print(f"  Detected {sum(y_pred_binary)} anomalies out of {len(y_pred_binary)} samples")

        self.models['isolation_forest'] = model
        self.results['isolation_forest'] = results

        return results

    def _evaluate_classifier(self, y_true: np.ndarray, y_pred: np.ndarray,
                            y_pred_proba: np.ndarray, model_name: str) -> Dict:
        """Evaluate a binary classifier."""
        results = {
            'model_name': model_name,
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1': f1_score(y_true, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_true, y_pred_proba),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist(),
            'classification_report': classification_report(y_true, y_pred, zero_division=0)
        }

        return results

    def _evaluate_anomaly_detector(self, y_true: np.ndarray, y_pred: np.ndarray,
                                   anomaly_scores: np.ndarray, model_name: str) -> Dict:
        """Evaluate an anomaly detector."""
        results = {
            'model_name': model_name,
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1': f1_score(y_true, y_pred, zero_division=0),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist(),
            'anomaly_scores_mean': float(anomaly_scores.mean()),
            'anomaly_scores_std': float(anomaly_scores.std())
        }

        return results

    def compare_models(self) -> pd.DataFrame:
        """Compare all trained models."""
        print("\n" + "=" * 80)
        print("Model Comparison")
        print("=" * 80)

        comparison = []

        for model_name, results in self.results.items():
            comparison.append({
                'Model': results['model_name'],
                'Accuracy': results['accuracy'],
                'Precision': results['precision'],
                'Recall': results['recall'],
                'F1-Score': results['f1'],
                'ROC-AUC': results.get('roc_auc', 'N/A')
            })

        df_comparison = pd.DataFrame(comparison)
        df_comparison = df_comparison.sort_values('F1-Score', ascending=False)

        print("\n" + df_comparison.to_string(index=False))

        # Save comparison
        comparison_file = self.results_dir / "model_comparison.csv"
        df_comparison.to_csv(comparison_file, index=False)
        print(f"\n✓ Comparison saved to: {comparison_file.name}")

        return df_comparison

    def plot_feature_importance(self, top_n: int = 20):
        """Plot feature importance for models that support it."""
        if not self.feature_importance:
            print("[Skip] No feature importance available")
            return

        n_models = len(self.feature_importance)
        fig, axes = plt.subplots(1, n_models, figsize=(8 * n_models, 6))

        if n_models == 1:
            axes = [axes]

        for idx, (model_name, importance_df) in enumerate(self.feature_importance.items()):
            ax = axes[idx]

            top_features = importance_df.head(top_n)

            ax.barh(range(len(top_features)), top_features['importance'])
            ax.set_yticks(range(len(top_features)))
            ax.set_yticklabels(top_features['feature'], fontsize=8)
            ax.invert_yaxis()
            ax.set_xlabel('Importance')
            ax.set_title(f'{model_name.replace("_", " ").title()}\nTop {top_n} Features')
            ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()

        output_file = self.results_dir / "feature_importance.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\n✓ Feature importance plot saved: {output_file.name}")
        plt.close()

        # Save top features to CSV
        for model_name, importance_df in self.feature_importance.items():
            csv_file = self.results_dir / f"feature_importance_{model_name}.csv"
            importance_df.to_csv(csv_file, index=False)

    def plot_confusion_matrices(self):
        """Plot confusion matrices for all models."""
        n_models = len([r for r in self.results.values() if 'confusion_matrix' in r])

        if n_models == 0:
            return

        cols = min(3, n_models)
        rows = (n_models + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=(6 * cols, 5 * rows))
        axes = axes.flatten() if n_models > 1 else [axes]

        idx = 0
        for model_name, results in self.results.items():
            if 'confusion_matrix' not in results:
                continue

            ax = axes[idx]
            cm = np.array(results['confusion_matrix'])

            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                       xticklabels=['Secured', 'Vulnerable'],
                       yticklabels=['Secured', 'Vulnerable'])
            ax.set_title(f'{results["model_name"]}\nConfusion Matrix')
            ax.set_ylabel('True Label')
            ax.set_xlabel('Predicted Label')

            idx += 1

        # Hide unused subplots
        for i in range(idx, len(axes)):
            axes[i].axis('off')

        plt.tight_layout()

        output_file = self.results_dir / "confusion_matrices.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Confusion matrices saved: {output_file.name}")
        plt.close()

    def save_models(self):
        """Save all trained models."""
        print("\n" + "=" * 80)
        print("Saving Models")
        print("=" * 80)

        for model_name, model in self.models.items():
            model_file = self.output_dir / f"{model_name}.joblib"
            joblib.dump(model, model_file)
            print(f"✓ Saved: {model_file.name}")

        # Save results
        results_file = self.output_dir / "training_results.json"
        with open(results_file, 'w') as f:
            # Convert numpy types to Python types for JSON serialization
            serializable_results = {}
            for model_name, results in self.results.items():
                serializable_results[model_name] = {
                    k: v if not isinstance(v, (np.integer, np.floating)) else float(v)
                    for k, v in results.items()
                    if k != 'classification_report'  # Skip text report
                }
            json.dump(serializable_results, f, indent=2)
        print(f"✓ Saved: {results_file.name}")

    def generate_report(self):
        """Generate training summary report."""
        report_file = self.results_dir / f"training_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(report_file, 'w') as f:
            f.write("# ML Model Training Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Models Trained\n\n")
            for model_name in self.models.keys():
                f.write(f"- {model_name.replace('_', ' ').title()}\n")

            f.write("\n## Performance Comparison\n\n")
            comparison_df = self.compare_models()
            f.write(comparison_df.to_markdown(index=False))

            f.write("\n\n## Feature Importance\n\n")
            for model_name, importance_df in self.feature_importance.items():
                f.write(f"\n### {model_name.replace('_', ' ').title()} - Top 10 Features\n\n")
                f.write(importance_df.head(10).to_markdown(index=False))
                f.write("\n")

            f.write("\n## Model Files\n\n")
            f.write("Saved models:\n")
            for model_name in self.models.keys():
                f.write(f"- `models/{model_name}.joblib`\n")

            f.write("\n## Visualizations\n\n")
            f.write("- `results/feature_importance.png`\n")
            f.write("- `results/confusion_matrices.png`\n")

            f.write("\n## Next Steps\n\n")
            f.write("1. Review feature importance to understand key security indicators\n")
            f.write("2. Use best model for prediction on new data\n")
            f.write("3. Collect more time-series data for temporal models\n")
            f.write("4. Consider ensemble methods combining multiple models\n")

        print(f"\n✓ Training report saved: {report_file.name}")


def main():
    parser = argparse.ArgumentParser(description="Train baseline ML models for security anomaly detection")
    parser.add_argument(
        "--data-file",
        type=str,
        help="Time-series dataset file (if using time-series data)"
    )
    parser.add_argument(
        "--main-file",
        type=str,
        default="output/features_main_branch.csv",
        help="Main branch features file"
    )
    parser.add_argument(
        "--hardened-file",
        type=str,
        default="output/features_hardened_local.csv",
        help="Hardened branch features file"
    )
    parser.add_argument(
        "--models",
        type=str,
        default="all",
        help="Models to train: all, rf, xgb, lr, svm, if (comma-separated)"
    )

    args = parser.parse_args()

    # Initialize trainer
    trainer = BaselineModelTrainer()

    # Load data
    if args.data_file:
        data_file = Path(args.data_file)
        if not data_file.exists():
            print(f"[!] Data file not found: {data_file}")
            return
        X, y = trainer.load_time_series_data(data_file)
    else:
        main_file = Path(__file__).parent / args.main_file
        hardened_file = Path(__file__).parent / args.hardened_file

        if not main_file.exists() or not hardened_file.exists():
            print(f"[!] Feature files not found:")
            print(f"    Main: {main_file}")
            print(f"    Hardened: {hardened_file}")
            return

        X, y = trainer.load_comparison_data(main_file, hardened_file)

    # Preprocess
    data = trainer.preprocess_data(X, y)

    # Train models
    models_to_train = args.models.lower().split(',') if args.models != 'all' else ['rf', 'xgb', 'lr', 'svm', 'if']

    for model_type in models_to_train:
        model_type = model_type.strip()

        if model_type == 'rf':
            trainer.train_random_forest(data)
        elif model_type == 'xgb':
            trainer.train_xgboost(data)
        elif model_type == 'lr':
            trainer.train_logistic_regression(data)
        elif model_type == 'svm':
            trainer.train_svm(data)
        elif model_type == 'if':
            trainer.train_isolation_forest(data)
        else:
            print(f"[Skip] Unknown model type: {model_type}")

    # Compare models
    trainer.compare_models()

    # Visualizations
    trainer.plot_feature_importance(top_n=20)
    trainer.plot_confusion_matrices()

    # Save everything
    trainer.save_models()
    trainer.generate_report()

    print("\n" + "=" * 80)
    print("Training Complete!")
    print("=" * 80)
    print(f"\nResults saved to: {trainer.results_dir}")
    print(f"Models saved to: {trainer.output_dir}")


if __name__ == "__main__":
    main()
