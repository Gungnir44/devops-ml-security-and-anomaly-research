"""
Test Feature Extraction

Quick test script to verify feature extraction is working.
"""

import sys
from pathlib import Path
import pandas as pd

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from extractors.security_scan_extractor import SecurityScanExtractor
from loguru import logger

# Configure logger
logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")


def main():
    """Test security scan feature extraction."""
    print("=" * 80)
    print("ML Pipeline - Feature Extraction Test")
    print("=" * 80)
    print()

    # Path to research data
    data_dir = Path(__file__).parent.parent.parent / "research-data"

    if not data_dir.exists():
        print(f"❌ Research data directory not found: {data_dir}")
        print("   Make sure automated downloads have run at least once.")
        return 1

    print(f"[*] Data directory: {data_dir}")
    print()

    # Initialize Security Scan Extractor
    print("[*] Initializing Security Scan Extractor...")
    extractor = SecurityScanExtractor(data_dir=data_dir)

    print(f"    Feature count: {extractor.get_feature_count()}")
    print(f"    Features: {', '.join(extractor.get_feature_names()[:5])}...")
    print()

    # Extract features
    print("[*] Extracting features from collected data...")
    features = extractor.extract()
    print()

    # Display results
    print("=" * 80)
    print("EXTRACTED FEATURES")
    print("=" * 80)
    print()

    # Group features by category
    vulnerability_features = {k: v for k, v in features.items() if 'vuln' in k}
    security_features = {k: v for k, v in features.items() if k in [
        'secrets_detected_count', 'secrets_verified_count',
        'sast_code_smells', 'sast_security_issues'
    ]}
    dependency_features = {k: v for k, v in features.items() if 'npm' in k or 'python' in k}
    container_features = {k: v for k, v in features.items() if 'container' in k}
    compliance_features = {k: v for k, v in features.items() if k in ['cve_count', 'cwe_count', 'iac_misconfigurations']}

    print("Vulnerability Counts:")
    for name, value in vulnerability_features.items():
        print(f"   {name:30} = {value}")
    print()

    print("Security Findings:")
    for name, value in security_features.items():
        print(f"   {name:30} = {value}")
    print()

    print("Dependency Vulnerabilities:")
    for name, value in dependency_features.items():
        print(f"   {name:30} = {value}")
    print()

    print("Container Security:")
    for name, value in container_features.items():
        print(f"   {name:30} = {value}")
    print()

    print("Compliance & IaC:")
    for name, value in compliance_features.items():
        print(f"   {name:30} = {value}")
    print()

    # Risk score
    risk_score = features.get('security_risk_score', 0)
    print("Security Risk Score:")
    print(f"   {risk_score:.1f} / 100")
    if risk_score > 50:
        print("   [!] HIGH RISK - Many security issues detected")
    elif risk_score > 20:
        print("   [~] MEDIUM RISK - Some security issues present")
    else:
        print("   [+] LOW RISK - Few security issues found")
    print()

    # Convert to DataFrame
    print("=" * 80)
    print("DATAFRAME EXPORT")
    print("=" * 80)
    print()

    df = extractor.to_dataframe(features)
    print(df.T)  # Transpose for better readability
    print()

    # Save to CSV
    output_file = Path(__file__).parent / "extracted_features.csv"
    df.to_csv(output_file, index=False)
    print(f"[+] Features saved to: {output_file}")
    print()

    print("=" * 80)
    print("[+] Feature extraction test completed successfully!")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
