"""
Extract All Available Features

Runs all implemented extractors and combines results into a single feature vector.
"""

import sys
import argparse
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from extractors.security_scan_extractor import SecurityScanExtractor
from extractors.cicd_extractor import CICDExtractor
from extractors.code_change_extractor import CodeChangeExtractor
from extractors.container_extractor import ContainerExtractor
from extractors.deployment_extractor import DeploymentExtractor
from extractors.infrastructure_extractor import InfrastructureExtractor
from extractors.access_log_extractor import AccessLogExtractor
from extractors.network_extractor import NetworkExtractor
from loguru import logger

# Configure logger
logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")


def main():
    """Extract all available features."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract all ML features from DevOps data')
    parser.add_argument('--data-dir', type=str, default=None,
                        help='Path to research data directory (default: ../research-data)')
    parser.add_argument('--branch', type=str, default=None,
                        help='Branch name (will use research-data/<branch>-branch/)')
    parser.add_argument('--output-suffix', type=str, default='',
                        help='Suffix to add to output filenames (e.g., "_main" or "_hardened")')
    args = parser.parse_args()

    print("=" * 80)
    print("ML Pipeline - Complete Feature Extraction")
    print("=" * 80)
    print()

    # Determine data directory
    if args.data_dir:
        data_dir = Path(args.data_dir)
    elif args.branch:
        data_dir = Path(__file__).parent.parent.parent / "research-data" / f"{args.branch}-branch"
    else:
        data_dir = Path(__file__).parent.parent.parent / "research-data"

    if not data_dir.exists():
        print(f"[!] Research data directory not found: {data_dir}")
        print("    Make sure automated downloads have run at least once.")
        return 1

    print(f"[*] Data directory: {data_dir}")
    if args.branch:
        print(f"[*] Branch: {args.branch}")
    print(f"[*] Extraction time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Track all features
    all_features = {}

    # =========================================================================
    # EXTRACT SECURITY SCAN FEATURES (21 features)
    # =========================================================================
    print("[1/8] Extracting Security Scan Features (21 features)...")
    security_extractor = SecurityScanExtractor(data_dir=data_dir)
    security_features = security_extractor.extract()
    all_features.update(security_features)
    print(f"      Extracted {len(security_features)} security features")
    print()

    # =========================================================================
    # EXTRACT CI/CD FEATURES (35 features)
    # =========================================================================
    print("[2/8] Extracting CI/CD Pipeline Features (35 features)...")
    cicd_extractor = CICDExtractor(data_dir=data_dir)
    cicd_features = cicd_extractor.extract()
    all_features.update(cicd_features)
    print(f"      Extracted {len(cicd_features)} CI/CD features")
    print()

    # =========================================================================
    # EXTRACT CODE CHANGE FEATURES (25 features)
    # =========================================================================
    print("[3/8] Extracting Code Change Features (25 features)...")
    code_extractor = CodeChangeExtractor(data_dir=data_dir)
    code_features = code_extractor.extract()
    all_features.update(code_features)
    print(f"      Extracted {len(code_features)} code change features")
    print()

    # =========================================================================
    # EXTRACT CONTAINER FEATURES (24 features)
    # =========================================================================
    print("[4/8] Extracting Container Features (24 features)...")
    container_extractor = ContainerExtractor(data_dir=data_dir)
    container_features = container_extractor.extract()
    all_features.update(container_features)
    print(f"      Extracted {len(container_features)} container features")
    print()

    # =========================================================================
    # EXTRACT DEPLOYMENT FEATURES (22 features)
    # =========================================================================
    print("[5/8] Extracting Deployment Features (22 features)...")
    deployment_extractor = DeploymentExtractor(data_dir=data_dir)
    deployment_features = deployment_extractor.extract()
    all_features.update(deployment_features)
    print(f"      Extracted {len(deployment_features)} deployment features")
    print()

    # =========================================================================
    # EXTRACT INFRASTRUCTURE FEATURES (40 features)
    # =========================================================================
    print("[6/8] Extracting Infrastructure Features (40 features)...")
    infrastructure_extractor = InfrastructureExtractor(data_dir=data_dir)
    infrastructure_features = infrastructure_extractor.extract()
    all_features.update(infrastructure_features)
    print(f"      Extracted {len(infrastructure_features)} infrastructure features")
    print()

    # =========================================================================
    # EXTRACT ACCESS LOG FEATURES (28 features)
    # =========================================================================
    print("[7/8] Extracting Access Log Features (28 features)...")
    access_log_extractor = AccessLogExtractor(data_dir=data_dir)
    access_log_features = access_log_extractor.extract()
    all_features.update(access_log_features)
    print(f"      Extracted {len(access_log_features)} access log features")
    print()

    # =========================================================================
    # EXTRACT NETWORK FEATURES (15 features)
    # =========================================================================
    print("[8/8] Extracting Network Features (15 features)...")
    network_extractor = NetworkExtractor(data_dir=data_dir)
    network_features = network_extractor.extract()
    all_features.update(network_features)
    print(f"      Extracted {len(network_features)} network features")
    print()

    # =========================================================================
    # COMBINED RESULTS
    # =========================================================================
    print("=" * 80)
    print("EXTRACTION SUMMARY")
    print("=" * 80)
    print()

    total_extracted = len(all_features)
    total_possible = 210
    completion = (total_extracted / total_possible) * 100

    print(f"Total Features Extracted:  {total_extracted} / {total_possible}")
    print(f"Completion:                {completion:.1f}%")
    print()

    print("Feature Breakdown:")
    print(f"  - Security Scans:        {len(security_features)} features")
    print(f"  - CI/CD Pipelines:       {len(cicd_features)} features")
    print(f"  - Code Changes:          {len(code_features)} features")
    print(f"  - Containers:            {len(container_features)} features")
    print(f"  - Deployments:           {len(deployment_features)} features")
    print(f"  - Infrastructure:        {len(infrastructure_features)} features")
    print(f"  - Access Logs:           {len(access_log_features)} features")
    print(f"  - Network:               {len(network_features)} features")
    print()

    # =========================================================================
    # KEY INSIGHTS
    # =========================================================================
    print("=" * 80)
    print("KEY INSIGHTS")
    print("=" * 80)
    print()

    # Security insights
    risk_score = security_features.get('security_risk_score', 0)
    print("Security Posture:")
    print(f"  Risk Score:              {risk_score:.1f} / 100")
    print(f"  Critical Vulnerabilities: {security_features.get('vuln_critical_count', 0)}")
    print(f"  High Severity:           {security_features.get('vuln_high_count', 0)}")
    print(f"  Container Issues:        {security_features.get('container_vulnerabilities', 0)}")
    print(f"  IaC Misconfigurations:   {security_features.get('iac_misconfigurations', 0)}")
    print()

    # CI/CD insights
    success_rate = cicd_features.get('pipeline_success_rate', 0) * 100
    print("CI/CD Performance:")
    print(f"  Pipeline Runs:           {cicd_features.get('pipeline_runs_total', 0)}")
    print(f"  Success Rate:            {success_rate:.1f}%")
    print(f"  Average Duration:        {cicd_features.get('pipeline_duration_avg_seconds', 0)/60:.1f} min")
    print(f"  Deployments:             {cicd_features.get('deployments_count', 0)}")
    print(f"  Change Failure Rate:     {cicd_features.get('change_failure_rate', 0)*100:.1f}%")
    print()

    # DORA metrics
    print("DORA Metrics:")
    print(f"  Lead Time:               {cicd_features.get('lead_time_hours', 0):.1f} hours")
    print(f"  MTTR:                    {cicd_features.get('mttr_hours', 0):.1f} hours")
    print(f"  Deployment Frequency:    {cicd_features.get('deployments_per_day', 0):.2f}/day")
    print()

    # =========================================================================
    # SAVE RESULTS
    # =========================================================================
    print("=" * 80)
    print("SAVING RESULTS")
    print("=" * 80)
    print()

    # Convert to DataFrame
    df = pd.DataFrame([all_features])

    # Save to multiple formats
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # CSV (for Excel, simple analysis)
    csv_file = output_dir / f"features_{timestamp}.csv"
    df.to_csv(csv_file, index=False)
    print(f"[+] CSV saved:     {csv_file}")

    # Transposed CSV (better readability)
    csv_t_file = output_dir / f"features_{timestamp}_transposed.csv"
    df.T.to_csv(csv_t_file, header=['value'])
    print(f"[+] CSV-T saved:   {csv_t_file}")

    # JSON (for programmatic access)
    json_file = output_dir / f"features_{timestamp}.json"
    df.to_json(json_file, orient='records', indent=2)
    print(f"[+] JSON saved:    {json_file}")

    # Also save latest version (no timestamp)
    latest_csv = output_dir / "latest_features.csv"
    df.to_csv(latest_csv, index=False)
    print(f"[+] Latest saved:  {latest_csv}")

    print()

    # =========================================================================
    # DATAFRAME PREVIEW
    # =========================================================================
    print("=" * 80)
    print("FEATURE VECTOR PREVIEW (First 20 features)")
    print("=" * 80)
    print()

    preview_df = df.T.head(20)
    preview_df.columns = ['value']
    print(preview_df.to_string())
    print()
    print(f"... and {total_extracted - 20} more features")
    print()

    # =========================================================================
    # COMPLETION
    # =========================================================================
    print("=" * 80)
    print("[+] Feature extraction completed successfully!")
    print("=" * 80)
    print()

    print("Next Steps:")
    print("  1. Review extracted features in: output/latest_features.csv")
    print("  2. Let automation run to collect time-series data (2-3 weeks)")
    print("  3. Extract features from main branch vs hardened branch for comparison")
    print("  4. Build time-series dataset for ML training")
    print("  5. Start exploratory data analysis (EDA)")
    print("  6. Train baseline ML models (anomaly detection, classification)")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
