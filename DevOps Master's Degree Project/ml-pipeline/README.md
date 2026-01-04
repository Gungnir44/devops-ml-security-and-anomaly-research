# ML Pipeline - Feature Extraction System

This directory contains the machine learning pipeline for extracting 210 features from DevOps security data.

## Directory Structure

```
ml-pipeline/
├── README.md                           # This file
├── feature_definitions.yaml            # All 210 features defined
├── config/
│   └── extraction_config.yaml          # Configuration
├── extractors/
│   ├── __init__.py
│   ├── base_extractor.py              # Base class for all extractors
│   ├── security_scan_extractor.py     # Security scan features (21)
│   ├── cicd_extractor.py              # CI/CD features (35)
│   ├── infrastructure_extractor.py    # Infrastructure features (40)
│   ├── access_log_extractor.py        # Access log features (28)
│   ├── code_change_extractor.py       # Code change features (25)
│   ├── container_extractor.py         # Container features (24)
│   ├── deployment_extractor.py        # Deployment features (22)
│   └── network_extractor.py           # Network features (15)
├── parsers/
│   ├── __init__.py
│   ├── json_parser.py                 # Parse JSON artifacts
│   ├── sarif_parser.py                # Parse SARIF files
│   └── github_api_parser.py           # Parse GitHub API data
├── pipeline/
│   ├── __init__.py
│   ├── feature_pipeline.py            # Main extraction pipeline
│   ├── aggregator.py                  # Aggregate features
│   └── validator.py                   # Validate extracted features
├── utils/
│   ├── __init__.py
│   ├── time_windows.py                # Time window utilities
│   └── normalization.py               # Feature normalization
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb  # EDA notebook
│   ├── 02_feature_distribution.ipynb  # Feature distributions
│   └── 03_correlation_analysis.ipynb  # Feature correlations
└── tests/
    ├── test_extractors.py
    └── test_pipeline.py
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Extract features from collected data
python -m pipeline.feature_pipeline \
    --input ../research-data/downloads \
    --output features/baseline_features.csv \
    --window 1h

# Generate feature report
python -m pipeline.feature_pipeline --report
```

## Feature Categories

| Category | Count | Description |
|----------|-------|-------------|
| Security Scans | 21 | Vulnerability counts by severity, tool, type |
| CI/CD Events | 35 | Pipeline metrics, build status, duration |
| Infrastructure | 40 | CPU, memory, disk, network metrics |
| Access Logs | 28 | Request patterns, status codes, anomalies |
| Code Changes | 25 | Commit frequency, complexity, authors |
| Container Events | 24 | Deployments, restarts, resource usage |
| Deployment Events | 22 | Frequency, success rate, rollbacks |
| Network Traffic | 15 | Bandwidth, connections, protocols |

**Total: 210 features**

## Usage Examples

### Extract Features for Specific Time Window

```python
from pipeline.feature_pipeline import FeaturePipeline

pipeline = FeaturePipeline(data_dir="../research-data/downloads")
features = pipeline.extract_features(
    start_time="2025-12-06 00:00:00",
    end_time="2025-12-06 23:59:59",
    window_size="1h"  # 1-hour windows
)
features.to_csv("daily_features.csv")
```

### Extract Features from Specific Branch

```python
# Compare main vs hardened branch
main_features = pipeline.extract_features(branch="main")
hardened_features = pipeline.extract_features(branch="hardened")

# Analyze differences
diff = main_features - hardened_features
```

### Generate Training Dataset

```python
from pipeline.aggregator import FeatureAggregator

aggregator = FeatureAggregator()
dataset = aggregator.create_training_set(
    normal_data="../research-data/baseline-week-1",
    anomaly_data="../research-data/attack-scenarios",
    balance=True,  # Balance classes
    split_ratio=0.7  # 70% train, 30% test
)
```

## Data Sources

The pipeline extracts features from:

1. **GitHub Actions Artifacts**
   - Workflow run metadata
   - Build logs
   - Test results
   - Security scan reports

2. **Security Scanning Tools**
   - TruffleHog (secrets)
   - Gitleaks (secrets)
   - Trivy (containers)
   - Grype (containers)
   - Dockle (container best practices)
   - CodeQL (SAST)
   - Semgrep (SAST)
   - Bandit (Python SAST)
   - npm audit (dependencies)
   - pip-audit (dependencies)
   - Checkov (IaC)
   - tfsec (Terraform)

3. **Code Repository**
   - Commit history
   - Code complexity metrics
   - Author patterns

4. **Workflow Logs**
   - Pipeline duration
   - Step-level timing
   - Failure patterns

## Output Formats

- **CSV**: For simple ML workflows
- **Parquet**: For large-scale processing
- **JSON**: For inspection and debugging
- **HDF5**: For high-performance I/O

## Next Steps

1. Review `feature_definitions.yaml` for complete feature list
2. Run exploratory analysis in `notebooks/01_exploratory_analysis.ipynb`
3. Extract baseline features from collected data
4. Analyze feature distributions and correlations
