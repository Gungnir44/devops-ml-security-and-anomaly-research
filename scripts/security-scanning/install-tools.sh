#!/bin/bash
# Security Scanning Tools Installation Script
# For DevOps Master's Research Project
# Installs all security scanning tools locally

set -e

echo "========================================="
echo "Installing Security Scanning Tools"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Detect OS
OS="$(uname -s)"
echo "Detected OS: $OS"
echo ""

# =============================================================================
# 1. SECRET SCANNING TOOLS
# =============================================================================
echo -e "${YELLOW}[1/7] Installing Secret Scanning Tools...${NC}"

# TruffleHog
if ! command -v trufflehog &> /dev/null; then
    echo "Installing TruffleHog..."
    if [ "$OS" = "Linux" ]; then
        curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin
    elif [ "$OS" = "Darwin" ]; then
        brew install trufflesecurity/trufflehog/trufflehog
    fi
    echo -e "${GREEN}✓ TruffleHog installed${NC}"
else
    echo -e "${GREEN}✓ TruffleHog already installed${NC}"
fi

# Gitleaks
if ! command -v gitleaks &> /dev/null; then
    echo "Installing Gitleaks..."
    if [ "$OS" = "Linux" ]; then
        wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz
        tar -xzf gitleaks_8.18.0_linux_x64.tar.gz
        sudo mv gitleaks /usr/local/bin/
        rm gitleaks_8.18.0_linux_x64.tar.gz
    elif [ "$OS" = "Darwin" ]; then
        brew install gitleaks
    fi
    echo -e "${GREEN}✓ Gitleaks installed${NC}"
else
    echo -e "${GREEN}✓ Gitleaks already installed${NC}"
fi

echo ""

# =============================================================================
# 2. CONTAINER SCANNING TOOLS
# =============================================================================
echo -e "${YELLOW}[2/7] Installing Container Scanning Tools...${NC}"

# Trivy
if ! command -v trivy &> /dev/null; then
    echo "Installing Trivy..."
    if [ "$OS" = "Linux" ]; then
        wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
        echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
        sudo apt-get update
        sudo apt-get install trivy -y
    elif [ "$OS" = "Darwin" ]; then
        brew install trivy
    fi
    echo -e "${GREEN}✓ Trivy installed${NC}"
else
    echo -e "${GREEN}✓ Trivy already installed${NC}"
fi

# Grype
if ! command -v grype &> /dev/null; then
    echo "Installing Grype..."
    curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin
    echo -e "${GREEN}✓ Grype installed${NC}"
else
    echo -e "${GREEN}✓ Grype already installed${NC}"
fi

# Dockle (Docker image linter)
if ! command -v dockle &> /dev/null; then
    echo "Installing Dockle..."
    if [ "$OS" = "Linux" ]; then
        VERSION=$(curl --silent "https://api.github.com/repos/goodwithtech/dockle/releases/latest" | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/')
        wget https://github.com/goodwithtech/dockle/releases/download/v${VERSION}/dockle_${VERSION}_Linux-64bit.tar.gz
        tar -xzf dockle_${VERSION}_Linux-64bit.tar.gz
        sudo mv dockle /usr/local/bin/
        rm dockle_${VERSION}_Linux-64bit.tar.gz
    elif [ "$OS" = "Darwin" ]; then
        brew install goodwithtech/r/dockle
    fi
    echo -e "${GREEN}✓ Dockle installed${NC}"
else
    echo -e "${GREEN}✓ Dockle already installed${NC}"
fi

echo ""

# =============================================================================
# 3. SAST TOOLS
# =============================================================================
echo -e "${YELLOW}[3/7] Installing SAST Tools...${NC}"

# Semgrep
if ! command -v semgrep &> /dev/null; then
    echo "Installing Semgrep..."
    if command -v pip3 &> /dev/null; then
        pip3 install semgrep
    elif command -v pip &> /dev/null; then
        pip install semgrep
    else
        echo -e "${RED}✗ pip not found. Please install Python and pip first.${NC}"
    fi
    echo -e "${GREEN}✓ Semgrep installed${NC}"
else
    echo -e "${GREEN}✓ Semgrep already installed${NC}"
fi

# Bandit (Python security linter)
if ! command -v bandit &> /dev/null; then
    echo "Installing Bandit..."
    if command -v pip3 &> /dev/null; then
        pip3 install bandit
    elif command -v pip &> /dev/null; then
        pip install bandit
    fi
    echo -e "${GREEN}✓ Bandit installed${NC}"
else
    echo -e "${GREEN}✓ Bandit already installed${NC}"
fi

# ESLint (JavaScript linter - optional)
if ! command -v eslint &> /dev/null; then
    echo "Installing ESLint..."
    if command -v npm &> /dev/null; then
        npm install -g eslint
    fi
    echo -e "${GREEN}✓ ESLint installed${NC}"
else
    echo -e "${GREEN}✓ ESLint already installed${NC}"
fi

echo ""

# =============================================================================
# 4. DEPENDENCY SCANNING TOOLS
# =============================================================================
echo -e "${YELLOW}[4/7] Installing Dependency Scanning Tools...${NC}"

# pip-audit (Python)
if ! command -v pip-audit &> /dev/null; then
    echo "Installing pip-audit..."
    if command -v pip3 &> /dev/null; then
        pip3 install pip-audit
    elif command -v pip &> /dev/null; then
        pip install pip-audit
    fi
    echo -e "${GREEN}✓ pip-audit installed${NC}"
else
    echo -e "${GREEN}✓ pip-audit already installed${NC}"
fi

# Safety (Python dependency checker)
if ! command -v safety &> /dev/null; then
    echo "Installing Safety..."
    if command -v pip3 &> /dev/null; then
        pip3 install safety
    elif command -v pip &> /dev/null; then
        pip install safety
    fi
    echo -e "${GREEN}✓ Safety installed${NC}"
else
    echo -e "${GREEN}✓ Safety already installed${NC}"
fi

# npm audit is built into npm (no separate install needed)
if command -v npm &> /dev/null; then
    echo -e "${GREEN}✓ npm audit available (built-in)${NC}"
fi

echo ""

# =============================================================================
# 5. INFRASTRUCTURE AS CODE SCANNING
# =============================================================================
echo -e "${YELLOW}[5/7] Installing IaC Scanning Tools...${NC}"

# Checkov
if ! command -v checkov &> /dev/null; then
    echo "Installing Checkov..."
    if command -v pip3 &> /dev/null; then
        pip3 install checkov
    elif command -v pip &> /dev/null; then
        pip install checkov
    fi
    echo -e "${GREEN}✓ Checkov installed${NC}"
else
    echo -e "${GREEN}✓ Checkov already installed${NC}"
fi

# tfsec (Terraform security scanner)
if ! command -v tfsec &> /dev/null; then
    echo "Installing tfsec..."
    if [ "$OS" = "Linux" ]; then
        wget https://github.com/aquasecurity/tfsec/releases/download/v1.28.1/tfsec-linux-amd64
        chmod +x tfsec-linux-amd64
        sudo mv tfsec-linux-amd64 /usr/local/bin/tfsec
    elif [ "$OS" = "Darwin" ]; then
        brew install tfsec
    fi
    echo -e "${GREEN}✓ tfsec installed${NC}"
else
    echo -e "${GREEN}✓ tfsec already installed${NC}"
fi

echo ""

# =============================================================================
# 6. KUBERNETES SECURITY TOOLS
# =============================================================================
echo -e "${YELLOW}[6/7] Installing Kubernetes Security Tools...${NC}"

# kubeaudit
if ! command -v kubeaudit &> /dev/null; then
    echo "Installing kubeaudit..."
    if [ "$OS" = "Linux" ]; then
        wget https://github.com/Shopify/kubeaudit/releases/download/v0.22.0/kubeaudit_0.22.0_linux_amd64.tar.gz
        tar -xzf kubeaudit_0.22.0_linux_amd64.tar.gz
        sudo mv kubeaudit /usr/local/bin/
        rm kubeaudit_0.22.0_linux_amd64.tar.gz
    elif [ "$OS" = "Darwin" ]; then
        brew install kubeaudit
    fi
    echo -e "${GREEN}✓ kubeaudit installed${NC}"
else
    echo -e "${GREEN}✓ kubeaudit already installed${NC}"
fi

# kubeval (Kubernetes manifest validator)
if ! command -v kubeval &> /dev/null; then
    echo "Installing kubeval..."
    if [ "$OS" = "Linux" ]; then
        wget https://github.com/instrumenta/kubeval/releases/latest/download/kubeval-linux-amd64.tar.gz
        tar xf kubeval-linux-amd64.tar.gz
        sudo mv kubeval /usr/local/bin
        rm kubeval-linux-amd64.tar.gz
    elif [ "$OS" = "Darwin" ]; then
        brew install kubeval
    fi
    echo -e "${GREEN}✓ kubeval installed${NC}"
else
    echo -e "${GREEN}✓ kubeval already installed${NC}"
fi

echo ""

# =============================================================================
# 7. ADDITIONAL UTILITIES
# =============================================================================
echo -e "${YELLOW}[7/7] Installing Additional Utilities...${NC}"

# jq (JSON processor)
if ! command -v jq &> /dev/null; then
    echo "Installing jq..."
    if [ "$OS" = "Linux" ]; then
        sudo apt-get install jq -y
    elif [ "$OS" = "Darwin" ]; then
        brew install jq
    fi
    echo -e "${GREEN}✓ jq installed${NC}"
else
    echo -e "${GREEN}✓ jq already installed${NC}"
fi

# yq (YAML processor)
if ! command -v yq &> /dev/null; then
    echo "Installing yq..."
    if [ "$OS" = "Darwin" ]; then
        brew install yq
    else
        sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
        sudo chmod +x /usr/local/bin/yq
    fi
    echo -e "${GREEN}✓ yq installed${NC}"
else
    echo -e "${GREEN}✓ yq already installed${NC}"
fi

echo ""
echo "========================================="
echo -e "${GREEN}Installation Complete!${NC}"
echo "========================================="
echo ""
echo "Installed tools:"
echo "  Secret Scanning: trufflehog, gitleaks"
echo "  Container Scanning: trivy, grype, dockle"
echo "  SAST: semgrep, bandit, eslint"
echo "  Dependency Scanning: pip-audit, safety, npm audit"
echo "  IaC Scanning: checkov, tfsec"
echo "  Kubernetes: kubeaudit, kubeval"
echo "  Utilities: jq, yq"
echo ""
echo "Run './scan-all.sh' to perform a complete security scan."
