# Baseline Week 1 - Extracted Research Data

**Extraction Date:** December 5, 2025
**Source:** GitHub Actions artifacts from devops-ml-security-and-anomaly-research

---

## Data Extracted

### 1. Security Scans (`security-scans-general/`)

#### KICS Results - Infrastructure as Code Security
**File:** `kics-results/results.json`

**Summary:**
- **Total Findings:** 111
- **Files Scanned:** 22
- **Lines Scanned:** 2,293
- **Severity Breakdown:**
  - HIGH: 15
  - MEDIUM: 34
  - LOW: 57
  - INFO: 5

**Key Findings:**
- AKS Private Cluster Disabled (HIGH)
- Azure Kubernetes security configurations
- Infrastructure misconfigurations

**Research Value:**
- Baseline infrastructure security posture
- Maps to ML Features #120-135 (IaC security metrics)
- Azure/AWS cloud security patterns

---

#### Gitleaks Results - Secret Detection
**File:** `gitleaks-results.sarif/`

**Format:** SARIF (Security Analysis Results Interchange Format)

**Research Value:**
- Secret detection baseline
- Maps to ML Feature #56-60 (Secret scanning metrics)
- False positive analysis

---

### 2. SBOM & Licenses (`sbom-and-licenses/`)

#### Software Bill of Materials (SBOM)
**Files:**
- `sbom.spdx.json` - Complete SBOM in SPDX format
- `devops-ml-security-and-anomaly-research-sbom-generation.spdx.json` - Generation metadata

**Contains:**
- All dependencies (npm, pip packages)
- Version information
- License data
- Component relationships

**Research Value:**
- Dependency inventory
- Maps to ML Features #67-72 (Dependency metrics)
- Supply chain analysis

---

#### License Report
**File:** `licenses.json`

**Contains:**
- License compliance data
- Package licensing information
- Open source license types

**Research Value:**
- Compliance metrics
- Open source risk analysis

---

## Data Analysis

### Files Processed
Total extracted files: 6 key data files

### Data Quality
✅ **Complete** - All downloaded artifacts extracted successfully
✅ **Structured** - JSON and SARIF formats ready for analysis
✅ **Timestamped** - Scan timestamps preserved for temporal analysis

---

## Next Steps for Analysis

### 1. KICS Security Analysis

**Parse the JSON:**
```python
import json

with open('security-scans-general/kics-results/results.json') as f:
    kics_data = json.load(f)

# Extract key metrics
print(f"Total findings: {kics_data['total_counter']}")
print(f"High severity: {kics_data['severity_counters']['HIGH']}")
print(f"Files scanned: {kics_data['files_scanned']}")

# Analyze by category
for query in kics_data['queries']:
    print(f"{query['severity']}: {query['query_name']}")
```

**Research Questions:**
- What are the most common infrastructure misconfigurations?
- How do severity levels correlate with attack scenarios?
- Which Azure/AWS resources have the most issues?

---

### 2. SBOM Dependency Analysis

**Parse SPDX:**
```python
import json

with open('sbom-and-licenses/sbom/sbom.spdx.json') as f:
    sbom_data = json.load(f)

# Count dependencies
packages = sbom_data.get('packages', [])
print(f"Total packages: {len(packages)}")

# Extract versions
for pkg in packages:
    print(f"{pkg['name']} - {pkg.get('versionInfo', 'N/A')}")
```

**Research Questions:**
- How many total dependencies across all 3 applications?
- Which packages have known vulnerabilities?
- Dependency complexity metrics

---

### 3. Gitleaks Secret Analysis

**Parse SARIF:**
```python
import json

with open('security-scans-general/gitleaks-results.sarif/work/.../results.sarif') as f:
    gitleaks_data = json.load(f)

# Extract findings
results = gitleaks_data.get('runs', [{}])[0].get('results', [])
print(f"Total secret detections: {len(results)}")

# Categorize by type
for result in results:
    rule_id = result['ruleId']
    location = result['locations'][0]['physicalLocation']['artifactLocation']['uri']
    print(f"{rule_id} found in {location}")
```

**Research Questions:**
- Are there false positives (test data, examples)?
- What types of secrets are detected?
- Location patterns (which files/directories)?

---

## ML Feature Mapping

This data maps to your 210 ML features:

### From KICS Results
- **Feature #120-135:** IaC security findings count by severity
- **Feature #136-145:** Cloud provider security posture (Azure, AWS)
- **Feature #146-150:** Kubernetes security metrics

### From SBOM
- **Feature #67-72:** Dependency counts and versions
- **Feature #73-78:** License risk metrics
- **Feature #79-84:** Outdated dependency ratios

### From Gitleaks
- **Feature #56-60:** Secret detection counts
- **Feature #61-66:** Secret entropy and confidence scores

---

## Missing Data (To Download Next)

You downloaded artifacts from the **security-scanning.yml** workflow. For complete baseline data, you should also download from the **individual app pipelines**:

### Still Needed from Backend CI/CD:
- Test coverage reports
- Container scan results (Trivy, Grype, Dockle)
- Semgrep/CodeQL SAST results specific to backend

### Still Needed from Python CI/CD:
- Test coverage reports
- Bandit SAST results
- Container scan results

### Still Needed from Frontend CI/CD:
- Test coverage reports
- ESLint code quality results
- Container scan results

**How to get:**
1. Go to: https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions
2. Click **"Backend CI/CD"** workflow (separate from security-scanning)
3. Download artifacts from latest run
4. Repeat for Python and Frontend workflows

---

## Folder Organization

```
baseline-week-1/
├── backend/              (empty - ready for backend-specific artifacts)
├── frontend/             (empty - ready for frontend-specific artifacts)
├── python/               (empty - ready for python-specific artifacts)
├── security-scans-general/  ✅ Extracted
│   ├── gitleaks-results.sarif/
│   └── kics-results/
└── sbom-and-licenses/    ✅ Extracted
    ├── sbom/
    ├── license-report/
    └── sbom-generation/
```

---

## Research Timeline

### Week 1 (Current) - Baseline Data Collection
- ✅ Downloaded security scanning results
- ✅ Extracted and organized data
- ⏳ Download individual app pipeline artifacts
- ⏳ Perform initial analysis
- ⏳ Document baseline metrics

### Week 2-4
- Continue weekly downloads
- Track metrics over time
- Identify trends and patterns

### Week 5+
- Implement attack scenarios
- Compare pre/post attack data
- Train ML models

---

## Quick Access Links

**GitHub Actions:** https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions

**Security Tab:** https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/security/code-scanning

**Project Root:** C:\Users\joshu\Desktop\DevOps Project

---

**Status:** ✅ Initial security scan data extracted and ready for analysis
**Next Action:** Download individual application pipeline artifacts to complete Week 1 baseline
