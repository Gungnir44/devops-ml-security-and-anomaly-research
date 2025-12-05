#!/bin/bash
# Comprehensive Security Scanning Script
# For DevOps Master's Research Project
# Runs all security scans and collects data for ML model training

set -e

# Configuration
SCAN_DIR="security-scan-results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_DIR="$SCAN_DIR/$TIMESTAMP"
SUMMARY_FILE="$REPORT_DIR/scan-summary.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "========================================="
echo "Comprehensive Security Scan"
echo "========================================="
echo "Timestamp: $TIMESTAMP"
echo "Results directory: $REPORT_DIR"
echo ""

# Create results directory
mkdir -p "$REPORT_DIR"

# Initialize summary JSON
cat > "$SUMMARY_FILE" << EOF
{
  "scan_timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "scan_id": "$TIMESTAMP",
  "scans_completed": [],
  "scans_failed": [],
  "summary": {
    "secret_scanning": {},
    "container_scanning": {},
    "sast": {},
    "dependency_scanning": {},
    "iac_scanning": {},
    "kubernetes_scanning": {}
  }
}
EOF

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

log_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

log_error() {
    echo -e "${RED}✗ $1${NC}"
}

log_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

update_summary() {
    local scan_name=$1
    local status=$2
    # Update the JSON summary (simplified - in production use jq)
    echo "  - $scan_name: $status" >> "$REPORT_DIR/scan-log.txt"
}

# =============================================================================
# 1. SECRET SCANNING
# =============================================================================
echo -e "${YELLOW}[1/8] Running Secret Scanning...${NC}"

# TruffleHog
if command -v trufflehog &> /dev/null; then
    log_info "Running TruffleHog..."
    trufflehog filesystem . \
        --json \
        --no-update \
        > "$REPORT_DIR/trufflehog-results.json" 2>&1 || true

    SECRET_COUNT=$(cat "$REPORT_DIR/trufflehog-results.json" | wc -l)
    log_success "TruffleHog scan complete ($SECRET_COUNT findings)"
    update_summary "trufflehog" "success"
else
    log_warning "TruffleHog not installed, skipping"
    update_summary "trufflehog" "skipped"
fi

# Gitleaks
if command -v gitleaks &> /dev/null; then
    log_info "Running Gitleaks..."
    gitleaks detect \
        --source . \
        --report-path "$REPORT_DIR/gitleaks-report.json" \
        --report-format json \
        --verbose 2>&1 || true
    log_success "Gitleaks scan complete"
    update_summary "gitleaks" "success"
else
    log_warning "Gitleaks not installed, skipping"
    update_summary "gitleaks" "skipped"
fi

echo ""

# =============================================================================
# 2. CONTAINER SCANNING
# =============================================================================
echo -e "${YELLOW}[2/8] Running Container Scanning...${NC}"

# Trivy - Filesystem scan
if command -v trivy &> /dev/null; then
    log_info "Running Trivy filesystem scan..."
    trivy fs . \
        --format json \
        --output "$REPORT_DIR/trivy-fs.json" \
        --severity CRITICAL,HIGH,MEDIUM,LOW 2>&1 || true
    log_success "Trivy filesystem scan complete"
    update_summary "trivy-fs" "success"

    # Scan Docker images if any exist
    if docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>" > /dev/null 2>&1; then
        log_info "Scanning Docker images..."
        docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>" | while read image; do
            image_name=$(echo "$image" | tr ':/' '_')
            trivy image "$image" \
                --format json \
                --output "$REPORT_DIR/trivy-image-$image_name.json" 2>&1 || true
        done
        log_success "Docker image scans complete"
    fi
else
    log_warning "Trivy not installed, skipping"
    update_summary "trivy" "skipped"
fi

# Grype
if command -v grype &> /dev/null; then
    log_info "Running Grype..."
    grype dir:. \
        --output json \
        --file "$REPORT_DIR/grype-fs.json" 2>&1 || true
    log_success "Grype scan complete"
    update_summary "grype" "success"
else
    log_warning "Grype not installed, skipping"
    update_summary "grype" "skipped"
fi

# Dockle - Docker image linting
if command -v dockle &> /dev/null; then
    if docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>" > /dev/null 2>&1; then
        log_info "Running Dockle on Docker images..."
        docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>" | while read image; do
            image_name=$(echo "$image" | tr ':/' '_')
            dockle --format json --output "$REPORT_DIR/dockle-$image_name.json" "$image" 2>&1 || true
        done
        log_success "Dockle scans complete"
        update_summary "dockle" "success"
    fi
else
    log_warning "Dockle not installed, skipping"
    update_summary "dockle" "skipped"
fi

echo ""

# =============================================================================
# 3. SAST (Static Application Security Testing)
# =============================================================================
echo -e "${YELLOW}[3/8] Running SAST Tools...${NC}"

# Semgrep
if command -v semgrep &> /dev/null; then
    log_info "Running Semgrep..."
    semgrep scan \
        --config auto \
        --json \
        --output "$REPORT_DIR/semgrep.json" \
        --verbose 2>&1 || true
    log_success "Semgrep scan complete"
    update_summary "semgrep" "success"
else
    log_warning "Semgrep not installed, skipping"
    update_summary "semgrep" "skipped"
fi

# Bandit (Python)
if command -v bandit &> /dev/null; then
    if find . -name "*.py" | grep -q .; then
        log_info "Running Bandit (Python)..."
        bandit -r . \
            --format json \
            --output "$REPORT_DIR/bandit.json" 2>&1 || true
        log_success "Bandit scan complete"
        update_summary "bandit" "success"
    fi
else
    log_warning "Bandit not installed, skipping"
    update_summary "bandit" "skipped"
fi

echo ""

# =============================================================================
# 4. DEPENDENCY SCANNING
# =============================================================================
echo -e "${YELLOW}[4/8] Running Dependency Scanning...${NC}"

# npm audit (if package.json exists)
if [ -f "package.json" ] && command -v npm &> /dev/null; then
    log_info "Running npm audit..."
    npm audit --json > "$REPORT_DIR/npm-audit.json" 2>&1 || true
    log_success "npm audit complete"
    update_summary "npm-audit" "success"
fi

# pip-audit (if requirements.txt exists)
if command -v pip-audit &> /dev/null; then
    if [ -f "requirements.txt" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
        log_info "Running pip-audit..."
        pip-audit --format json --output "$REPORT_DIR/pip-audit.json" 2>&1 || true
        log_success "pip-audit complete"
        update_summary "pip-audit" "success"
    fi
else
    log_warning "pip-audit not installed, skipping"
    update_summary "pip-audit" "skipped"
fi

# Safety (Python)
if command -v safety &> /dev/null; then
    if [ -f "requirements.txt" ]; then
        log_info "Running Safety..."
        safety check --json --file requirements.txt > "$REPORT_DIR/safety.json" 2>&1 || true
        log_success "Safety scan complete"
        update_summary "safety" "success"
    fi
else
    log_warning "Safety not installed, skipping"
    update_summary "safety" "skipped"
fi

echo ""

# =============================================================================
# 5. INFRASTRUCTURE AS CODE SCANNING
# =============================================================================
echo -e "${YELLOW}[5/8] Running IaC Scanning...${NC}"

# Checkov
if command -v checkov &> /dev/null; then
    log_info "Running Checkov..."
    checkov -d . \
        --output json \
        --output-file "$REPORT_DIR/checkov.json" \
        --quiet 2>&1 || true
    log_success "Checkov scan complete"
    update_summary "checkov" "success"
else
    log_warning "Checkov not installed, skipping"
    update_summary "checkov" "skipped"
fi

# tfsec (if Terraform files exist)
if command -v tfsec &> /dev/null; then
    if find . -name "*.tf" | grep -q .; then
        log_info "Running tfsec..."
        tfsec . \
            --format json \
            --out "$REPORT_DIR/tfsec.json" 2>&1 || true
        log_success "tfsec scan complete"
        update_summary "tfsec" "success"
    fi
else
    log_warning "tfsec not installed, skipping"
    update_summary "tfsec" "skipped"
fi

echo ""

# =============================================================================
# 6. KUBERNETES MANIFEST SCANNING
# =============================================================================
echo -e "${YELLOW}[6/8] Running Kubernetes Scanning...${NC}"

# kubeaudit
if command -v kubeaudit &> /dev/null; then
    if find . -path "./kubernetes/*" -name "*.yaml" | grep -q .; then
        log_info "Running kubeaudit..."
        kubeaudit all -f ./kubernetes/manifests/ --format json > "$REPORT_DIR/kubeaudit.json" 2>&1 || true
        log_success "kubeaudit scan complete"
        update_summary "kubeaudit" "success"
    fi
else
    log_warning "kubeaudit not installed, skipping"
    update_summary "kubeaudit" "skipped"
fi

# kubeval
if command -v kubeval &> /dev/null; then
    if find . -path "./kubernetes/*" -name "*.yaml" | grep -q .; then
        log_info "Running kubeval..."
        find ./kubernetes/manifests/ -name "*.yaml" -exec kubeval --strict {} \; > "$REPORT_DIR/kubeval.txt" 2>&1 || true
        log_success "kubeval validation complete"
        update_summary "kubeval" "success"
    fi
else
    log_warning "kubeval not installed, skipping"
    update_summary "kubeval" "skipped"
fi

echo ""

# =============================================================================
# 7. GENERATE AGGREGATED REPORT
# =============================================================================
echo -e "${YELLOW}[7/8] Generating Aggregated Report...${NC}"

cat > "$REPORT_DIR/README.md" << EOF
# Security Scan Report

**Scan Date:** $(date)
**Scan ID:** $TIMESTAMP

## Summary

This directory contains the results of a comprehensive security scan across multiple tools and categories.

## Scan Categories

### 1. Secret Scanning
- TruffleHog: \`trufflehog-results.json\`
- Gitleaks: \`gitleaks-report.json\`

### 2. Container Scanning
- Trivy: \`trivy-*.json\`
- Grype: \`grype-fs.json\`
- Dockle: \`dockle-*.json\`

### 3. SAST (Static Application Security Testing)
- Semgrep: \`semgrep.json\`
- Bandit: \`bandit.json\`

### 4. Dependency Scanning
- npm audit: \`npm-audit.json\`
- pip-audit: \`pip-audit.json\`
- Safety: \`safety.json\`

### 5. Infrastructure as Code
- Checkov: \`checkov.json\`
- tfsec: \`tfsec.json\`

### 6. Kubernetes Security
- kubeaudit: \`kubeaudit.json\`
- kubeval: \`kubeval.txt\`

## Files in this directory

\`\`\`
$(ls -lh)
\`\`\`

## Next Steps

1. Review individual scan results
2. Analyze findings by severity
3. Use data for ML model training
4. Remediate identified issues

EOF

log_success "Aggregated report generated"

echo ""

# =============================================================================
# 8. GENERATE FEATURE EXTRACTION PREVIEW
# =============================================================================
echo -e "${YELLOW}[8/8] Generating Feature Extraction Preview...${NC}"

cat > "$REPORT_DIR/feature-extraction-preview.txt" << EOF
# Feature Extraction Preview
# Based on FEATURE-ENGINEERING.md specification

## Security Scan Features (Category 7)

The following features can be extracted from this scan:

1. SAST Findings:
   - sast_findings_count
   - sast_findings_critical
   - sast_findings_high
   - sast_findings_medium
   - sast_findings_low
   - sast_tool_coverage (semgrep, bandit, etc.)

2. Dependency Vulnerabilities:
   - dep_vuln_count
   - dep_vuln_critical
   - dep_vuln_high
   - dep_vuln_outdated_deps_count

3. Container Vulnerabilities:
   - container_vuln_count
   - container_vuln_critical
   - container_image_age_days

4. Secret Detection:
   - secrets_detected_count
   - secret_types (API keys, passwords, tokens)

5. IaC Security:
   - iac_misconfig_count
   - iac_compliance_score

## Data Collection for ML Model

All JSON files in this directory can be parsed to extract features for:
- Baseline normal behavior modeling
- Anomaly detection training
- Attack scenario validation

See: ../../../FEATURE-ENGINEERING.md for complete feature list
EOF

log_success "Feature extraction preview generated"

echo ""
echo "========================================="
echo -e "${GREEN}Security Scan Complete!${NC}"
echo "========================================="
echo ""
echo "Results saved to: $REPORT_DIR"
echo ""
echo "Summary of files:"
ls -lh "$REPORT_DIR" | tail -n +2
echo ""
echo "Total scan results: $(ls -1 "$REPORT_DIR"/*.json 2>/dev/null | wc -l) JSON files"
echo ""
echo "Next steps:"
echo "  1. Review scan results in: $REPORT_DIR"
echo "  2. Check README.md for details"
echo "  3. Extract features for ML model training"
echo ""
