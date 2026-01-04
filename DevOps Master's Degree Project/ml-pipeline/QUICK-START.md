# Feature Extraction Pipeline - Quick Start

## What We Built

A comprehensive feature extraction system for your ML-based security anomaly detection research:

- **210 features** defined across 8 categories
- **Modular architecture** with pluggable extractors
- **Working implementation** for security scan features (21 features)
- **Extensible framework** to add remaining extractors

## Current Status

### ✅ Completed
1. **Architecture designed**
   - Base extractor class
   - Feature definitions (YAML)
   - Modular structure

2. **Security Scan Extractor** (21/210 features)
   - Extracts from code scanning alerts
   - Parses npm audit results
   - Processes pip-audit data
   - Analyzes Bandit SAST reports
   - Reads IaC scan results
   - Calculates security risk score

3. **Infrastructure ready**
   - Requirements file
   - Test script
   - Documentation

### ⏳ To Do
- Implement remaining 7 extractors (189 features)
- Create feature aggregation pipeline
- Build visualization tools
- Add historical comparison for trends

## Quick Test

### 1. Install Dependencies

```bash
cd "C:\Users\joshu\Desktop\DevOps Project\DevOps Master's Degree Project\ml-pipeline"
pip install -r requirements.txt
```

### 2. Run Test Extraction

```bash
python test_extraction.py
```

This will:
- Load your collected research data
- Extract 21 security scan features
- Display results categorized by type
- Save features to `extracted_features.csv`

### 3. Expected Output

```
==========================================
ML Pipeline - Feature Extraction Test
==========================================

📁 Data directory: C:\Users\joshu\Desktop\DevOps Project\research-data

🔧 Initializing Security Scan Extractor...
   Feature count: 21
   Features: vuln_critical_count, vuln_high_count, ...

🔍 Extracting features from collected data...

==========================================
EXTRACTED FEATURES
==========================================

📊 Vulnerability Counts:
   vuln_critical_count            = 3
   vuln_high_count                = 12
   vuln_medium_count              = 18
   vuln_low_count                 = 12

🔒 Security Findings:
   secrets_detected_count         = 0
   sast_security_issues           = 45

📦 Dependency Vulnerabilities:
   npm_vulnerabilities            = 0
   python_vulnerabilities         = 0

🐳 Container Security:
   container_vulnerabilities      = 156
   container_misconfigurations    = 23

✅ Compliance & IaC:
   cve_count                      = 89
   cwe_count                      = 12
   iac_misconfigurations          = 23

🎯 Security Risk Score: 85.0 / 100
   ⚠️  HIGH RISK - Many security issues detected
```

## Using the Extractor in Your Code

```python
from pathlib import Path
from extractors.security_scan_extractor import SecurityScanExtractor

# Initialize
data_dir = Path("../research-data")
extractor = SecurityScanExtractor(data_dir=data_dir)

# Extract features
features = extractor.extract()

# Convert to DataFrame for ML
import pandas as pd
df = extractor.to_dataframe(features)

# Save for training
df.to_csv("training_features.csv", index=False)
```

## Next Steps - Building Remaining Extractors

### Priority 1: CI/CD Extractor (35 features)
Most data already available from workflow artifacts.

**To build:**
1. Copy `security_scan_extractor.py` as template
2. Parse GitHub Actions workflow run data
3. Extract timing, success rates, build metrics

### Priority 2: Code Changes Extractor (25 features)
Use GitHub API to get commit data.

**To build:**
1. Use PyGithub library
2. Query commits in time window
3. Calculate commit patterns, author stats

### Priority 3: Infrastructure Extractor (40 features)
Requires Prometheus/metrics endpoints.

**To build:**
1. Query /metrics endpoints
2. Parse Prometheus format
3. Extract CPU, memory, network stats

### Remaining Extractors
- Access Logs (28) - Parse nginx/application logs
- Containers (24) - Kubernetes API + events
- Deployments (22) - ArgoCD API
- Network (15) - Network monitoring data

## File Structure Explained

```
ml-pipeline/
├── feature_definitions.yaml        # All 210 features defined
│   └── Complete specification with types, sources
│
├── extractors/
│   ├── base_extractor.py          # Base class (inherit from this)
│   └── security_scan_extractor.py # Example implementation
│
├── test_extraction.py             # Test script
├── requirements.txt               # Python dependencies
├── QUICK-START.md                 # This file
└── README.md                      # Full documentation
```

## Adding a New Extractor

### Step-by-Step Template

```python
# extractors/my_extractor.py
from .base_extractor import BaseExtractor
from typing import Dict, Any, List

class MyExtractor(BaseExtractor):
    """Extract features from X data source."""

    def get_feature_names(self) -> List[str]:
        """Return list of feature names."""
        return [
            'feature_1',
            'feature_2',
            # ... more features
        ]

    def extract(self, start_time=None, end_time=None, **kwargs) -> Dict[str, Any]:
        """Extract all features."""
        features = {name: 0 for name in self.get_feature_names()}

        # 1. Find data files
        files = self._find_files("**/pattern*.json")

        # 2. Parse data
        for file_path in files:
            data = self._parse_file(file_path)
            # Extract feature values from data
            features['feature_1'] = data.get('some_value', 0)

        # 3. Calculate derived features
        features['derived_feature'] = features['feature_1'] * 2

        return features

    def _parse_file(self, file_path):
        """Helper method to parse data files."""
        # Implementation here
        pass
```

## Tips for Feature Extraction

### 1. Handle Missing Data Gracefully
```python
# Always provide defaults
features = {name: 0 for name in self.get_feature_names()}

# Use safe division
rate = self._safe_divide(successes, total, default=0.0)
```

### 2. Log Progress
```python
from loguru import logger

logger.info(f"Processing {len(files)} files")
logger.warning("Data file not found, using defaults")
```

### 3. Validate Output
```python
# After extraction
if not self.validate_features(features):
    logger.error("Feature validation failed!")
```

### 4. Time Windows
```python
# Use time filtering when available
files = self._find_files(
    "**/*.json",
    start_time=datetime(2025, 12, 1),
    end_time=datetime(2025, 12, 7)
)
```

## Troubleshooting

### "No data files found"
- Check that automated downloads have run
- Verify `research-data/` directory exists
- Look for ZIP files in `research-data/downloads/`

### "Import errors"
- Install dependencies: `pip install -r requirements.txt`
- Ensure you're in the ml-pipeline directory

### "Feature count mismatch"
- Check `get_feature_names()` returns correct count
- Ensure all features initialized in `extract()`

## What's Next?

1. **Test the security extractor** on your data
2. **Review extracted features** in CSV file
3. **Build CI/CD extractor** (highest priority)
4. **Iterate until all 210 features** extracted
5. **Create aggregation pipeline** for time-series data
6. **Build visualizations** for feature analysis

---

**You now have a working foundation for feature extraction!** The security scan extractor demonstrates the pattern - use it as a template to build the remaining 7 extractors.
