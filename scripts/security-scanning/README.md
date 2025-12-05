# Security Scanning Tools Setup
## For DevOps Master's Research Project - ML-Based Anomaly Detection

This directory contains scripts and configurations for comprehensive security scanning across your DevOps pipeline. These scans generate the data needed for your ML-based security anomaly detection research.

---

## 📋 Overview

### Tools Included

| Category | Tools | Purpose |
|----------|-------|---------|
| **Secret Scanning** | TruffleHog, Gitleaks | Detect hardcoded secrets, API keys, tokens |
| **Container Scanning** | Trivy, Grype, Dockle | Find vulnerabilities in containers and images |
| **SAST** | CodeQL, Semgrep, Bandit | Static code analysis for security issues |
| **Dependency Scanning** | npm audit, pip-audit, Safety, Snyk | Identify vulnerable dependencies |
| **IaC Scanning** | Checkov, tfsec | Scan Terraform, K8s manifests |
| **K8s Security** | kubeaudit, kubeval | Kubernetes-specific security checks |

---

## 🚀 Quick Start

### 1. Install All Tools

```bash
cd scripts/security-scanning
chmod +x install-tools.sh
./install-tools.sh
```

**Note:** On Windows, use Git Bash or WSL2 to run these scripts.

### 2. Run Complete Security Scan

```bash
chmod +x scan-all.sh
./scan-all.sh
```

This will:
- Scan for secrets (TruffleHog, Gitleaks)
- Scan containers and images (Trivy, Grype, Dockle)
- Run SAST tools (Semgrep, Bandit)
- Check dependencies (npm, pip, Safety)
- Scan IaC (Checkov, tfsec)
- Validate Kubernetes manifests
- Generate aggregated JSON reports

### 3. Review Results

```bash
ls -la security-scan-results/$(ls -t security-scan-results/ | head -1)/
```

Results are organized by timestamp in `security-scan-results/YYYYMMDD_HHMMSS/`

---

## 📁 Directory Structure

```
security-scanning/
├── README.md                    # This file
├── install-tools.sh             # Install all security tools
├── scan-all.sh                  # Run all scans
├── security-scan-results/       # Scan output (gitignored)
│   └── YYYYMMDD_HHMMSS/
│       ├── trufflehog-results.json
│       ├── gitleaks-report.json
│       ├── trivy-fs.json
│       ├── semgrep.json
│       ├── npm-audit.json
│       ├── checkov.json
│       └── scan-summary.json
└── .gitignore
```

---

## 🔧 Individual Tool Usage

### Secret Scanning

**TruffleHog:**
```bash
# Scan filesystem
trufflehog filesystem . --json --no-update > trufflehog.json

# Scan git history
trufflehog git file://. --json > trufflehog-git.json

# Scan specific branch
trufflehog git file://. --branch main --json
```

**Gitleaks:**
```bash
# Detect secrets
gitleaks detect --source . --report-path gitleaks-report.json

# Scan git history
gitleaks detect --source . --log-opts="--all" --report-format json
```

### Container Scanning

**Trivy:**
```bash
# Scan filesystem
trivy fs . --format json --output trivy-fs.json

# Scan Docker image
trivy image nginx:latest --format json

# Scan specific severity
trivy fs . --severity CRITICAL,HIGH
```

**Grype:**
```bash
# Scan directory
grype dir:. --output json --file grype.json

# Scan Docker image
grype nginx:latest --output json
```

**Dockle:**
```bash
# Lint Docker image
dockle --format json --output dockle.json nginx:latest

# With specific checks
dockle --exit-code 1 --exit-level warn nginx:latest
```

### SAST

**Semgrep:**
```bash
# Auto-detect rules
semgrep scan --config auto --json --output semgrep.json

# Specific rules
semgrep scan --config "p/security-audit" --json

# CI mode (fail on findings)
semgrep scan --config auto --error
```

**Bandit (Python):**
```bash
# Scan Python code
bandit -r . --format json --output bandit.json

# With severity level
bandit -r . --severity-level high
```

### Dependency Scanning

**npm audit:**
```bash
# Audit dependencies
npm audit --json > npm-audit.json

# Audit with fix suggestions
npm audit --audit-level moderate

# Fix automatically
npm audit fix
```

**pip-audit (Python):**
```bash
# Audit Python dependencies
pip-audit --format json --output pip-audit.json

# With requirements file
pip-audit --requirement requirements.txt
```

**Safety:**
```bash
# Check dependencies
safety check --json --file requirements.txt > safety.json

# Full report
safety check --full-report
```

### IaC Scanning

**Checkov:**
```bash
# Scan directory
checkov -d . --output json --output-file checkov.json

# Scan specific framework
checkov -d . --framework kubernetes --output json

# Scan with baseline
checkov -d . --baseline checkov-baseline.json
```

**tfsec:**
```bash
# Scan Terraform
tfsec . --format json --out tfsec.json

# Specific severity
tfsec . --minimum-severity HIGH
```

### Kubernetes Security

**kubeaudit:**
```bash
# Audit all
kubeaudit all -f kubernetes/manifests/ --format json > kubeaudit.json

# Specific audit
kubeaudit apparmor -f kubernetes/manifests/
```

**kubeval:**
```bash
# Validate manifests
kubeval --strict kubernetes/manifests/*.yaml

# Against specific Kubernetes version
kubeval --kubernetes-version 1.27.0 manifest.yaml
```

---

## 🎯 Integration with GitHub Actions

All tools are integrated in `.github/workflows/security-scanning.yml`:

- **On Push/PR:** Run all scans automatically
- **Scheduled:** Daily scans at 2 AM UTC
- **Manual:** Trigger via workflow_dispatch
- **SARIF Upload:** Results uploaded to GitHub Security tab
- **Artifacts:** JSON results saved for 90 days

### Workflow Triggers:

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 2 * * *'
  workflow_dispatch:
```

---

## 📊 Data Collection for ML Research

### Feature Extraction

Scan results map directly to **Feature Category 7: Security Scanning Results** from your `FEATURE-ENGINEERING.md`:

```
Security Scan Features (21 features):
├── SAST findings (count, critical, high, medium, low)
├── Dependency vulnerabilities (count, severity distribution)
├── Container vulnerabilities (count, image age, base image)
├── Secret detection (count, types, entropy scores)
├── Code quality metrics (complexity, maintainability)
└── Compliance scores (CIS benchmarks, OWASP)
```

### Parsing Scan Results

Example Python script to extract features:

```python
import json

# Load scan result
with open('security-scan-results/latest/semgrep.json') as f:
    semgrep_data = json.load(f)

# Extract features
features = {
    'sast_findings_count': len(semgrep_data['results']),
    'sast_findings_critical': sum(1 for r in semgrep_data['results'] if r['severity'] == 'ERROR'),
    'sast_findings_high': sum(1 for r in semgrep_data['results'] if r['severity'] == 'WARNING'),
    # ... more features
}
```

### Baseline vs Attack Scenarios

Use these scans to:

1. **Establish Baseline:** Run scans during normal operations (Weeks 5-8)
2. **Attack Simulation:** Run after injecting attack scenarios (Weeks 9-12)
3. **Feature Engineering:** Extract time-series and delta features
4. **Model Training:** Use as input features for anomaly detection models

---

## 🔄 Continuous Improvement

### Scan Frequency Recommendations

| Environment | Frequency | Tools |
|-------------|-----------|-------|
| **Development** | On every commit | TruffleHog, Semgrep, npm audit |
| **Staging** | Daily | All tools |
| **Production** | Daily + On deploy | All tools (non-intrusive) |
| **Research Baseline** | Hourly | All tools (for dataset) |

### Alert Thresholds

For your ML model, set thresholds based on:
- **Critical:** Immediate flag (potential attack)
- **High:** Investigate within 1 hour
- **Medium:** Daily review
- **Low:** Weekly aggregation

---

## 🐛 Troubleshooting

### Common Issues

**1. Tools not found**
```bash
# Verify installation
which trufflehog trivy semgrep

# Re-run installer
./install-tools.sh
```

**2. Permission denied**
```bash
# Make scripts executable
chmod +x *.sh
```

**3. Docker scan fails**
```bash
# Ensure Docker is running
docker ps

# Check Docker socket
ls -la /var/run/docker.sock
```

**4. Out of disk space**
```bash
# Clean old scan results (keep last 7 days)
find security-scan-results/ -type d -mtime +7 -exec rm -rf {} \;
```

---

## 📚 Additional Resources

### Documentation Links

- [TruffleHog](https://github.com/trufflesecurity/trufflehog)
- [Trivy](https://aquasecurity.github.io/trivy/)
- [Semgrep](https://semgrep.dev/docs/)
- [Checkov](https://www.checkov.io/1.Welcome/Quick%20Start.html)
- [OWASP Top 10 CI/CD](https://owasp.org/www-project-top-10-ci-cd-security-risks/)

### Research Papers

See `../../READING-LIST-WITH-LINKS.md` for relevant papers on:
- ML for Security
- DevOps Security
- Supply Chain Attacks
- Anomaly Detection

---

## 🎓 Research Project Integration

### Phase 1 (Current): Infrastructure & Baseline
- ✅ Set up scanning tools
- ✅ Configure automated scans
- ⏳ Collect baseline data (4 weeks)

### Phase 2: Attack Simulation
- Inject attack scenarios from `../../ATTACK-SCENARIOS.md`
- Compare scan results: baseline vs attacked
- Extract behavioral differences

### Phase 3: ML Model Training
- Use scan results as feature set
- Train Isolation Forest, LSTM, Random Forest
- Validate on held-out attack scenarios

---

## 📈 Metrics & KPIs

Track these metrics for your research:

```
Scan Coverage:
├── % of code scanned
├── % of dependencies checked
├── % of containers validated
└── % of IaC resources audited

Detection Rates:
├── True Positive Rate (TPR)
├── False Positive Rate (FPR)
├── Precision, Recall, F1-Score
└── Time to detect (TTD)

Operational Metrics:
├── Scan duration
├── Resource usage
├── Data volume generated
└── Storage requirements
```

---

## 🤝 Contributing

For this research project:

1. Add new security tools to `install-tools.sh`
2. Integrate into `scan-all.sh`
3. Update this README
4. Test on sample applications
5. Document feature extraction methods

---

## 📝 License & Attribution

Part of Master's Thesis: "ML-Based Security Anomaly Detection for DevOps"

Tools used are open-source with their respective licenses. See individual tool documentation.

---

**Last Updated:** December 2025
**Version:** 1.0
