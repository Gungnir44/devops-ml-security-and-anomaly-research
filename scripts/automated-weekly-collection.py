#!/usr/bin/env python3
"""
Automated Weekly Data Collection Pipeline
==========================================

This script automates the complete data collection and feature extraction pipeline:
1. Downloads artifacts from GitHub Actions (Security Scanning Suite) for the last 7 days
2. Organizes artifacts by branch (main, hardened) and date
3. Runs feature extraction on each dataset
4. Appends to time-series CSV for longitudinal analysis
5. Generates summary report

Usage:
    python automated-weekly-collection.py [--days 7] [--extract-only] [--download-only]

Options:
    --days N          Download artifacts from last N days (default: 7)
    --extract-only    Skip download, only extract features from existing data
    --download-only   Only download artifacts, skip feature extraction
    --dry-run        Show what would be downloaded without actually downloading
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import requests
import zipfile


class AutomatedDataCollector:
    """Automated data collection and feature extraction pipeline."""

    def __init__(self, days_back: int = 7, base_dir: Path = None):
        self.days_back = days_back
        self.base_dir = base_dir or Path(__file__).parent.parent
        self.scripts_dir = self.base_dir / "scripts"
        self.ml_pipeline_dir = self.base_dir / "ml-pipeline"
        self.research_data_dir = self.base_dir / "research-data"
        self.time_series_dir = self.research_data_dir / "time-series"

        # GitHub API configuration
        self.repo_owner = "Gungnir44"
        self.repo_name = "devops-ml-security-and-anomaly-research"

        # Workflows to collect data from
        # Note: Security Scanning Suite runs daily but may not have artifacts yet
        # CI/CD workflows run on push and do generate artifacts
        self.workflows = [
            "security-scanning.yml",  # Comprehensive daily scans
            "frontend-ci-cd.yml",     # Frontend artifacts
            "backend-ci-cd.yml",      # Backend artifacts
            "python-ci-cd.yml",       # Python service artifacts
            "ci.yml"                  # General CI artifacts
        ]

        # Ensure directories exist
        self.time_series_dir.mkdir(parents=True, exist_ok=True)

        # Get GitHub token
        self.token = self._get_github_token()
        if not self.token:
            print("[!] GitHub token not found!")
            print("    Set GITHUB_TOKEN environment variable or create .github_token file")
            sys.exit(1)

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        # Track downloads
        self.download_log = []

    def _get_github_token(self) -> Optional[str]:
        """Get GitHub token from file or environment."""
        token_file = self.scripts_dir / ".github_token"
        if token_file.exists():
            with open(token_file, 'r') as f:
                return f.read().strip()
        return None

    def get_workflow_ids(self) -> Dict[str, int]:
        """Get workflow IDs for all configured workflows."""
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions/workflows"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f"[!] Failed to fetch workflows: {response.status_code}")
            return {}

        workflows = response.json().get('workflows', [])
        workflow_ids = {}

        for workflow in workflows:
            workflow_path = workflow['path']
            workflow_name = workflow_path.split('/')[-1]  # Get filename

            if workflow_name in self.workflows:
                workflow_ids[workflow_name] = workflow['id']

        return workflow_ids

    def get_recent_workflow_runs(self, workflow_id: int) -> List[Dict]:
        """Get workflow runs from the last N days."""
        cutoff_date = datetime.utcnow() - timedelta(days=self.days_back)
        cutoff_iso = cutoff_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions/workflows/{workflow_id}/runs"
        params = {
            "per_page": 100,
            "created": f">={cutoff_iso}"
        }

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            print(f"[!] Failed to fetch workflow runs: {response.status_code}")
            return []

        return response.json().get('workflow_runs', [])

    def filter_runs_by_branch(self, runs: List[Dict], branches: List[str] = None) -> Dict[str, List[Dict]]:
        """Filter and organize runs by branch."""
        if branches is None:
            branches = ['main', 'hardened']

        filtered = {branch: [] for branch in branches}

        for run in runs:
            branch = run.get('head_branch', '')
            if branch in branches:
                filtered[branch].append(run)

        return filtered

    def download_artifact(self, artifact_url: str, output_path: Path) -> bool:
        """Download a single artifact zip file."""
        try:
            response = requests.get(artifact_url, headers=self.headers, stream=True)

            if response.status_code != 200:
                return False

            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return True
        except Exception as e:
            print(f"    [Error] Download failed: {e}")
            return False

    def extract_zip(self, zip_path: Path, extract_to: Path) -> bool:
        """Extract a zip file."""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            return True
        except Exception as e:
            print(f"    [Error] Extraction failed: {e}")
            return False

    def download_run_artifacts(self, run: Dict, branch: str, dry_run: bool = False) -> int:
        """Download all artifacts from a single workflow run."""
        run_id = run['id']
        run_date = run['created_at'][:10]  # YYYY-MM-DD
        run_number = run['run_number']

        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions/runs/{run_id}/artifacts"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            return 0

        artifacts = response.json().get('artifacts', [])

        if not artifacts:
            return 0

        print(f"\n  [{branch}] Run #{run_number} ({run_date}) - {len(artifacts)} artifacts")

        if dry_run:
            for artifact in artifacts:
                print(f"    [Dry Run] Would download: {artifact['name']}")
            return len(artifacts)

        # Create output directory: research-data/time-series/YYYY-MM-DD/branch/
        output_dir = self.time_series_dir / run_date / branch
        output_dir.mkdir(parents=True, exist_ok=True)

        downloaded_count = 0

        for artifact in artifacts:
            artifact_name = artifact['name']
            artifact_url = artifact['archive_download_url']
            artifact_size_mb = artifact['size_in_bytes'] / (1024 * 1024)

            zip_path = output_dir / f"{artifact_name}.zip"
            extract_path = output_dir / artifact_name

            # Skip if already extracted
            if extract_path.exists():
                print(f"    [Skip] {artifact_name} (already exists)")
                continue

            print(f"    [Download] {artifact_name} ({artifact_size_mb:.2f} MB)")

            if self.download_artifact(artifact_url, zip_path):
                print(f"    [Extract] {artifact_name}")
                if self.extract_zip(zip_path, extract_path):
                    zip_path.unlink()  # Remove zip after extraction
                    downloaded_count += 1

                    # Log the download
                    self.download_log.append({
                        "date": run_date,
                        "branch": branch,
                        "run_id": run_id,
                        "run_number": run_number,
                        "artifact": artifact_name,
                        "size_mb": artifact_size_mb,
                        "path": str(extract_path.relative_to(self.base_dir))
                    })

                    print(f"    [OK] {artifact_name}")
                else:
                    print(f"    [Failed] Could not extract {artifact_name}")
            else:
                print(f"    [Failed] Could not download {artifact_name}")

        return downloaded_count

    def download_all_artifacts(self, dry_run: bool = False) -> Dict[str, int]:
        """Download all artifacts from recent workflow runs."""
        print("=" * 80)
        print(f"Automated Weekly Data Collection - Download Phase")
        print("=" * 80)
        print(f"Date range: Last {self.days_back} days")
        print(f"Repository: {self.repo_owner}/{self.repo_name}")
        print(f"Workflows: {', '.join(self.workflows)}")

        if dry_run:
            print("\n[DRY RUN MODE - No files will be downloaded]")

        # Get workflow IDs
        workflow_ids = self.get_workflow_ids()
        if not workflow_ids:
            print("[!] No configured workflows found")
            return {}

        print(f"\nFound {len(workflow_ids)} workflows:")
        for name, wid in workflow_ids.items():
            print(f"  - {name}: {wid}")

        stats = {'main': 0, 'hardened': 0}
        all_runs = []

        # Get runs from all workflows
        print(f"\nFetching workflow runs from last {self.days_back} days...")
        for workflow_name, workflow_id in workflow_ids.items():
            runs = self.get_recent_workflow_runs(workflow_id)
            print(f"  {workflow_name}: {len(runs)} runs")
            all_runs.extend(runs)

        print(f"\nTotal workflow runs: {len(all_runs)}")

        # Filter by branch
        runs_by_branch = self.filter_runs_by_branch(all_runs)

        for branch, branch_runs in runs_by_branch.items():
            if not branch_runs:
                print(f"\n[{branch}] No runs found")
                continue

            print(f"\n[{branch}] Processing {len(branch_runs)} runs...")

            branch_total = 0
            for run in branch_runs:
                count = self.download_run_artifacts(run, branch, dry_run)
                branch_total += count

            stats[branch] = branch_total
            print(f"\n[{branch}] Downloaded {branch_total} artifacts")

        return stats

    def extract_features_for_date(self, date: str, branch: str) -> Optional[Path]:
        """Run feature extraction for a specific date and branch."""
        data_dir = self.time_series_dir / date / branch

        if not data_dir.exists():
            print(f"    [Skip] No data directory: {data_dir}")
            return None

        # Check if we have any data files
        json_files = list(data_dir.rglob("*.json"))
        if not json_files:
            print(f"    [Skip] No JSON files found in {data_dir}")
            return None

        print(f"    [Extract] Features for {branch} on {date}")
        print(f"              Found {len(json_files)} JSON files")

        # Output file naming
        output_suffix = f"{branch}_{date.replace('-', '')}"

        # Run extraction script
        extract_script = self.ml_pipeline_dir / "extract_all_features.py"

        cmd = [
            sys.executable,
            str(extract_script),
            "--data-dir", str(data_dir),
            "--branch", branch,
            "--output-suffix", output_suffix
        ]

        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.ml_pipeline_dir),
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                # Find the generated CSV file
                output_csv = self.ml_pipeline_dir / "output" / f"features_{output_suffix}.csv"
                if output_csv.exists():
                    print(f"    [OK] Features extracted to: {output_csv.name}")
                    return output_csv
                else:
                    print(f"    [Warning] Extraction succeeded but output file not found")
                    return None
            else:
                print(f"    [Failed] Extraction failed:")
                print(f"            {result.stderr[:200]}")
                return None

        except subprocess.TimeoutExpired:
            print(f"    [Failed] Extraction timed out after 5 minutes")
            return None
        except Exception as e:
            print(f"    [Failed] Error running extraction: {e}")
            return None

    def extract_all_features(self) -> List[Path]:
        """Extract features from all downloaded data."""
        print("\n" + "=" * 80)
        print("Feature Extraction Phase")
        print("=" * 80)

        extracted_files = []

        # Find all date directories
        date_dirs = sorted([d for d in self.time_series_dir.iterdir() if d.is_dir() and d.name.count('-') == 2])

        if not date_dirs:
            print("[!] No data directories found to process")
            return extracted_files

        print(f"Found {len(date_dirs)} date directories to process\n")

        for date_dir in date_dirs:
            date = date_dir.name
            print(f"\n[{date}]")

            # Process each branch
            for branch in ['main', 'hardened']:
                output_csv = self.extract_features_for_date(date, branch)
                if output_csv:
                    extracted_files.append(output_csv)

        print(f"\n[Summary] Extracted features for {len(extracted_files)} datasets")
        return extracted_files

    def build_time_series_dataset(self, feature_files: List[Path]) -> Optional[Path]:
        """Combine all feature CSVs into a single time-series dataset."""
        if not feature_files:
            print("\n[!] No feature files to combine")
            return None

        print("\n" + "=" * 80)
        print("Building Time-Series Dataset")
        print("=" * 80)

        import pandas as pd

        all_data = []

        for csv_file in feature_files:
            # Parse date and branch from filename
            # Format: features_{branch}_{YYYYMMDD}.csv
            parts = csv_file.stem.split('_')
            if len(parts) >= 3:
                branch = parts[1]
                date_str = parts[2]

                # Parse date
                try:
                    date = datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
                except ValueError:
                    print(f"[Skip] Could not parse date from: {csv_file.name}")
                    continue

                # Read CSV
                try:
                    df = pd.read_csv(csv_file)
                    df['date'] = date
                    df['branch'] = branch
                    df['timestamp'] = datetime.strptime(date, "%Y-%m-%d")
                    all_data.append(df)
                    print(f"  [Add] {csv_file.name} ({len(df)} rows)")
                except Exception as e:
                    print(f"  [Skip] Error reading {csv_file.name}: {e}")

        if not all_data:
            print("[!] No valid data to combine")
            return None

        # Combine all data
        combined_df = pd.concat(all_data, ignore_index=True)

        # Sort by timestamp and branch
        combined_df = combined_df.sort_values(['timestamp', 'branch'])

        # Save time-series dataset
        output_file = self.ml_pipeline_dir / "output" / "time_series_dataset.csv"
        combined_df.to_csv(output_file, index=False)

        print(f"\n[OK] Time-series dataset created: {output_file.name}")
        print(f"     Total rows: {len(combined_df)}")
        print(f"     Date range: {combined_df['date'].min()} to {combined_df['date'].max()}")
        print(f"     Branches: {combined_df['branch'].unique().tolist()}")
        print(f"     Features: {len(combined_df.columns) - 3}")  # Exclude date, branch, timestamp

        return output_file

    def generate_summary_report(self, download_stats: Dict[str, int],
                                feature_files: List[Path],
                                time_series_file: Optional[Path]) -> Path:
        """Generate a summary report of the collection run."""
        report_file = self.time_series_dir / f"collection_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(report_file, 'w') as f:
            f.write("# Automated Data Collection Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
            f.write(f"**Days Back:** {self.days_back}\n\n")

            f.write("## Download Statistics\n\n")
            f.write(f"| Branch | Artifacts Downloaded |\n")
            f.write(f"|--------|---------------------|\n")
            total_downloads = 0
            for branch, count in download_stats.items():
                f.write(f"| {branch} | {count} |\n")
                total_downloads += count
            f.write(f"| **Total** | **{total_downloads}** |\n\n")

            f.write("## Feature Extraction\n\n")
            f.write(f"- Feature files generated: {len(feature_files)}\n")
            if feature_files:
                f.write("\nGenerated files:\n")
                for file in feature_files:
                    f.write(f"- `{file.name}`\n")

            f.write("\n## Time-Series Dataset\n\n")
            if time_series_file:
                f.write(f"✅ Created: `{time_series_file.name}`\n")
            else:
                f.write("❌ Not created (no data or error occurred)\n")

            f.write("\n## Download Log\n\n")
            if self.download_log:
                f.write("| Date | Branch | Run # | Artifact | Size (MB) |\n")
                f.write("|------|--------|-------|----------|----------|\n")
                for log in self.download_log:
                    f.write(f"| {log['date']} | {log['branch']} | #{log['run_number']} | {log['artifact']} | {log['size_mb']:.2f} |\n")
            else:
                f.write("No artifacts downloaded.\n")

            f.write("\n## Next Steps\n\n")
            f.write("1. Review the time-series dataset in `ml-pipeline/output/time_series_dataset.csv`\n")
            f.write("2. Train ML models on the accumulated data\n")
            f.write("3. Create visualizations of trends over time\n")
            f.write("4. Run this script again next week to continue collecting data\n")

        print(f"\n[Report] Summary saved to: {report_file.name}")
        return report_file

    def run(self, download_only: bool = False, extract_only: bool = False, dry_run: bool = False):
        """Run the complete automated collection pipeline."""
        start_time = datetime.now()

        # Phase 1: Download artifacts
        download_stats = {}
        if not extract_only:
            download_stats = self.download_all_artifacts(dry_run=dry_run)

            if dry_run:
                print("\n[Dry Run Complete] No files were downloaded")
                return

        if download_only:
            print("\n[Download Only Mode] Skipping feature extraction")
            return

        # Phase 2: Extract features
        feature_files = self.extract_all_features()

        # Phase 3: Build time-series dataset
        time_series_file = self.build_time_series_dataset(feature_files)

        # Phase 4: Generate report
        report_file = self.generate_summary_report(download_stats, feature_files, time_series_file)

        # Final summary
        elapsed = (datetime.now() - start_time).total_seconds()

        print("\n" + "=" * 80)
        print("Automated Collection Complete!")
        print("=" * 80)
        print(f"Elapsed time: {elapsed:.1f} seconds")
        print(f"Report: {report_file}")

        if time_series_file:
            print(f"Time-series dataset: {time_series_file}")
            print("\n✅ Ready for ML model training!")


def main():
    parser = argparse.ArgumentParser(
        description="Automated weekly data collection and feature extraction pipeline"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Download artifacts from last N days (default: 7)"
    )
    parser.add_argument(
        "--extract-only",
        action="store_true",
        help="Skip download, only extract features from existing data"
    )
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="Only download artifacts, skip feature extraction"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be downloaded without actually downloading"
    )

    args = parser.parse_args()

    # Create collector
    collector = AutomatedDataCollector(days_back=args.days)

    # Run pipeline
    collector.run(
        download_only=args.download_only,
        extract_only=args.extract_only,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
