#!/usr/bin/env python3
"""
Real-time ML Anomaly Prediction Script
Runs in GitHub Actions to detect anomalies in latest security scan
"""

import sys
import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class RealtimeAnomalyDetector:
    """Detect anomalies in real-time using trained ML models"""

    def __init__(self, models_dir='models', artifact_dir='artifacts'):
        self.models_dir = Path(models_dir)
        self.artifact_dir = Path(artifact_dir)
        self.logs_dir = Path('logs/ml-predictions')
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        self.model = None
        self.scaler = None
        self.model_name = None

    def load_model(self, model_type='random_forest'):
        """Load trained model and scaler"""
        print(f"[*] Loading {model_type} model...")

        model_file = self.models_dir / f'{model_type}_latest.pkl'
        scaler_file = self.models_dir / 'scaler_latest.pkl'

        if not model_file.exists():
            print(f"[ERROR] Model not found: {model_file}")
            print("Train models first using: python ml-train-models.py")
            sys.exit(1)

        if not scaler_file.exists():
            print(f"[ERROR] Scaler not found: {scaler_file}")
            sys.exit(1)

        self.model = joblib.load(model_file)
        self.scaler = joblib.load(scaler_file)
        self.model_name = model_type

        print(f"[OK] Model loaded: {model_file.name}")
        print(f"[OK] Scaler loaded: {scaler_file.name}")

    def extract_features_from_artifacts(self):
        """Extract features from latest security scan artifacts"""
        print("\n[*] Extracting features from artifacts...")

        # This is simplified - in production, use the full feature extraction
        # For now, load the latest features file if available
        features_file = Path('../DevOps Master\'s Degree Project/ml-pipeline/output/latest_features.csv')

        if not features_file.exists():
            print(f"[ERROR] Features file not found: {features_file}")
            print("Run feature extraction first!")
            sys.exit(1)

        df = pd.read_csv(features_file)
        print(f"[OK] Loaded features: {len(df.columns)} features")

        # Remove non-numeric columns
        feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        X = df[feature_cols].fillna(0)

        return X, feature_cols

    def predict(self, X):
        """Make prediction on new data"""
        print("\n[*] Running prediction...")

        # Scale features
        X_scaled = self.scaler.transform(X)

        # Get prediction
        if self.model_name == 'isolation_forest':
            # Isolation Forest returns -1 for anomalies, 1 for normal
            prediction_raw = self.model.predict(X_scaled)[0]
            prediction = 1 if prediction_raw == -1 else 0  # 1 = anomaly, 0 = normal
            confidence = abs(self.model.score_samples(X_scaled)[0])
        else:
            # Supervised models
            prediction = self.model.predict(X_scaled)[0]
            if hasattr(self.model, 'predict_proba'):
                proba = self.model.predict_proba(X_scaled)[0]
                confidence = float(proba[prediction])
            else:
                confidence = 1.0

        # Get feature importance if available
        feature_importance = None
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = self.model.feature_importances_.tolist()

        result = {
            'prediction': int(prediction),
            'prediction_label': 'ANOMALY' if prediction == 1 else 'NORMAL',
            'confidence': float(confidence),
            'model': self.model_name,
            'timestamp': datetime.now().isoformat()
        }

        return result

    def generate_alert(self, result, threshold=0.7):
        """Generate alert if anomaly detected"""
        print("\n" + "="*80)
        print("PREDICTION RESULT")
        print("="*80)

        print(f"Model: {result['model']}")
        print(f"Prediction: {result['prediction_label']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Timestamp: {result['timestamp']}")

        if result['prediction'] == 1 and result['confidence'] >= threshold:
            print("\n" + "!"*80)
            print("ALERT: ANOMALY DETECTED!")
            print("!"*80)
            print(f"An anomaly was detected with {result['confidence']:.1%} confidence.")
            print("This may indicate a security issue in the pipeline.")
            print("\nRecommended actions:")
            print("1. Review recent commits and changes")
            print("2. Check security scan reports")
            print("3. Investigate failed pipeline jobs")
            print("4. Compare with hardened branch")
            print("!"*80)

            # Set GitHub Actions output for alert
            if 'GITHUB_OUTPUT' in os.environ:
                with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                    f.write(f"anomaly_detected=true\n")
                    f.write(f"anomaly_confidence={result['confidence']}\n")

            return True
        else:
            print("\n[OK] No anomalies detected - pipeline appears normal")

            if 'GITHUB_OUTPUT' in os.environ:
                with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                    f.write(f"anomaly_detected=false\n")

            return False

    def save_prediction(self, result):
        """Save prediction to log file"""
        # Save individual prediction
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pred_file = self.logs_dir / f'prediction_{timestamp}.json'

        with open(pred_file, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"\n[OK] Prediction saved: {pred_file}")

        # Append to prediction log
        log_file = self.logs_dir / 'predictions.jsonl'
        with open(log_file, 'a') as f:
            f.write(json.dumps(result) + '\n')

    def run_detection(self, model_type='random_forest'):
        """Run complete detection pipeline"""
        print("="*80)
        print("REAL-TIME ANOMALY DETECTION")
        print("="*80)
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Load model
        self.load_model(model_type)

        # Extract features
        X, feature_cols = self.extract_features_from_artifacts()

        # Predict
        result = self.predict(X)

        # Save prediction
        self.save_prediction(result)

        # Generate alert if needed
        alert_triggered = self.generate_alert(result)

        print("\n" + "="*80)
        print("DETECTION COMPLETE")
        print("="*80)

        # Exit with appropriate code for GitHub Actions
        if alert_triggered:
            sys.exit(1)  # Non-zero exit = anomaly detected
        else:
            sys.exit(0)  # Zero exit = normal


if __name__ == '__main__':
    import os

    # Get model type from environment or use default
    model_type = os.environ.get('ML_MODEL_TYPE', 'random_forest')

    detector = RealtimeAnomalyDetector()
    detector.run_detection(model_type)
