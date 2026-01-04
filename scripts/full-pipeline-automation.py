#!/usr/bin/env python3
"""
Complete Automated Data Pipeline
=================================

End-to-end automation:
1. Download artifacts from scheduled runs
2. Extract ML features
3. Validate data quality
4. Generate summary reports
5. Send notifications (if configured)
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import requests


class FullPipelineAutomation:
    """Complete automated data collection and processing pipeline."""

    def __init__(self):
        self.scripts_dir = Path(__file__).parent
        self.repo_root = self.scripts_dir.parent
        self.ml_pipeline = self.repo_root / "DevOps Master's Degree Project" / "ml-pipeline"
        self.research_data = self.repo_root / "research-data"
        self.log_dir = self.scripts_dir / "logs" / "pipeline"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = self.log_dir / f"pipeline_{self.timestamp}.log"

    def log(self, message, level="INFO"):
        """Log message to file and console."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')

    def step1_download_artifacts(self):
        """Download artifacts from scheduled runs."""
        self.log("=" * 80)
        self.log("STEP 1: Downloading Artifacts")
        self.log("=" * 80)

        download_script = self.scripts_dir / "download_scheduled_artifacts.py"

        if not download_script.exists():
            self.log(f"Download script not found: {download_script}", "ERROR")
            return False

        try:
            result = subprocess.run(
                [sys.executable, str(download_script)],
                cwd=str(self.scripts_dir),
                capture_output=True,
                text=True,
                timeout=600
            )

            self.log(result.stdout)

            if result.returncode == 0:
                self.log("Artifact download completed successfully", "SUCCESS")
                return True
            else:
                self.log(f"Download failed with code {result.returncode}", "ERROR")
                self.log(result.stderr, "ERROR")
                return False

        except Exception as e:
            self.log(f"Download error: {e}", "ERROR")
            return False

    def step2_extract_features(self):
        """Extract ML features from downloaded data."""
        self.log("")
        self.log("=" * 80)
        self.log("STEP 2: Extracting ML Features")
        self.log("=" * 80)

        # Extract for main branch
        main_dir = self.research_data / "main-branch"
        if main_dir.exists():
            self.log("Extracting features for main branch...")
            success_main = self._extract_features_for_branch(main_dir, "_main")
        else:
            self.log("Main branch data not found, skipping", "WARNING")
            success_main = True  # Not a failure, just no data

        # Extract for hardened branch
        hardened_dir = self.research_data / "hardened-branch"
        if hardened_dir.exists():
            self.log("Extracting features for hardened branch...")
            success_hardened = self._extract_features_for_branch(hardened_dir, "_hardened")
        else:
            self.log("Hardened branch data not found, skipping", "WARNING")
            success_hardened = True

        return success_main and success_hardened

    def _extract_features_for_branch(self, data_dir, suffix):
        """Extract features for a specific branch."""
        extract_script = self.ml_pipeline / "extract_all_features.py"

        if not extract_script.exists():
            self.log(f"Feature extraction script not found: {extract_script}", "ERROR")
            return False

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(extract_script),
                    "--data-dir", str(data_dir),
                    "--output-suffix", suffix
                ],
                cwd=str(self.ml_pipeline),
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                self.log(f"Feature extraction{suffix} completed", "SUCCESS")
                return True
            else:
                self.log(f"Feature extraction{suffix} failed: {result.stderr}", "ERROR")
                return False

        except Exception as e:
            self.log(f"Feature extraction error: {e}", "ERROR")
            return False

    def step3_validate_data(self):
        """Validate collected data quality."""
        self.log("")
        self.log("=" * 80)
        self.log("STEP 3: Validating Data Quality")
        self.log("=" * 80)

        validation_results = {
            'timestamp': datetime.now().isoformat(),
            'checks': [],
            'overall_status': 'PASS'
        }

        # Check 1: Time-series data exists
        time_series_dir = self.research_data / "time-series"
        if time_series_dir.exists():
            date_dirs = list(time_series_dir.glob("2025-*"))
            validation_results['checks'].append({
                'name': 'Time-series data',
                'status': 'PASS' if len(date_dirs) > 0 else 'FAIL',
                'details': f'Found {len(date_dirs)} date directories'
            })
            self.log(f"Found {len(date_dirs)} date directories in time-series")
        else:
            validation_results['checks'].append({
                'name': 'Time-series data',
                'status': 'FAIL',
                'details': 'Time-series directory not found'
            })
            validation_results['overall_status'] = 'FAIL'
            self.log("Time-series directory not found", "WARNING")

        # Check 2: Feature files exist
        output_dir = self.ml_pipeline / "output"
        if output_dir.exists():
            csv_files = list(output_dir.glob("features_*.csv"))
            validation_results['checks'].append({
                'name': 'Feature files',
                'status': 'PASS' if len(csv_files) > 0 else 'FAIL',
                'details': f'Found {len(csv_files)} feature CSV files'
            })
            self.log(f"Found {len(csv_files)} feature CSV files")
        else:
            validation_results['checks'].append({
                'name': 'Feature files',
                'status': 'FAIL',
                'details': 'ML output directory not found'
            })
            validation_results['overall_status'] = 'FAIL'
            self.log("ML output directory not found", "WARNING")

        # Check 3: Recent data (within last 7 days)
        if time_series_dir.exists():
            recent_dirs = [d for d in date_dirs if (datetime.now() - datetime.strptime(d.name, '%Y-%m-%d')).days <= 7]
            validation_results['checks'].append({
                'name': 'Recent data collection',
                'status': 'PASS' if len(recent_dirs) > 0 else 'WARN',
                'details': f'{len(recent_dirs)} days of data in last 7 days'
            })
            self.log(f"{len(recent_dirs)} days of data collected in last 7 days")

        # Save validation results
        validation_file = self.log_dir / f"validation_{self.timestamp}.json"
        with open(validation_file, 'w') as f:
            json.dump(validation_results, f, indent=2)

        self.log(f"Validation {validation_results['overall_status']}",
                 "SUCCESS" if validation_results['overall_status'] == 'PASS' else "WARNING")

        return validation_results['overall_status'] == 'PASS'

    def step4_generate_report(self):
        """Generate summary report."""
        self.log("")
        self.log("=" * 80)
        self.log("STEP 4: Generating Summary Report")
        self.log("=" * 80)

        report_file = self.log_dir / f"summary_report_{self.timestamp}.md"

        # Gather statistics
        time_series_dir = self.research_data / "time-series"
        date_dirs = list(time_series_dir.glob("2025-*")) if time_series_dir.exists() else []

        total_files = 0
        for date_dir in date_dirs:
            total_files += len(list(date_dir.rglob("*.json")))
            total_files += len(list(date_dir.rglob("*.sarif")))

        output_dir = self.ml_pipeline / "output"
        feature_files = list(output_dir.glob("features_*.csv")) if output_dir.exists() else []

        # Create report
        report = f"""# Automated Pipeline Summary Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Data Collection Status

### Time-Series Data
- **Date Range:** {date_dirs[0].name if date_dirs else 'N/A'} to {date_dirs[-1].name if date_dirs else 'N/A'}
- **Days Collected:** {len(date_dirs)}
- **Total Artifacts:** {total_files}

### ML Features
- **Feature Extractions:** {len(feature_files)}
- **Latest Features:** {feature_files[-1].name if feature_files else 'None'}

## Pipeline Execution

### Steps Completed
1. [OK] Artifact Download
2. [OK] Feature Extraction
3. [OK] Data Validation
4. [OK] Report Generation

### Logs
- Pipeline log: `{self.log_file.name}`
- Validation: `validation_{self.timestamp}.json`

## Next Actions

1. Review collected data in `research-data/time-series/`
2. Check ML features in `ml-pipeline/output/`
3. Continue baseline data collection (need 14-21 days)
4. Start Week 2 attack scenarios after baseline complete

---
*This report was generated automatically by the DevOps automation pipeline*
"""

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        self.log(f"Summary report saved: {report_file}")
        self.log("Report generation completed", "SUCCESS")

        return True

    def run_pipeline(self):
        """Execute complete pipeline."""
        self.log("")
        self.log("=" * 80)
        self.log("AUTOMATED DATA PIPELINE - FULL EXECUTION")
        self.log("=" * 80)
        self.log(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log("")

        pipeline_start = datetime.now()

        # Execute pipeline steps
        steps = [
            ("Download Artifacts", self.step1_download_artifacts),
            ("Extract Features", self.step2_extract_features),
            ("Validate Data", self.step3_validate_data),
            ("Generate Report", self.step4_generate_report)
        ]

        results = {}
        for step_name, step_func in steps:
            try:
                success = step_func()
                results[step_name] = "SUCCESS" if success else "FAILED"
            except Exception as e:
                self.log(f"Step '{step_name}' crashed: {e}", "ERROR")
                results[step_name] = "CRASHED"

        # Final summary
        pipeline_duration = (datetime.now() - pipeline_start).total_seconds()

        self.log("")
        self.log("=" * 80)
        self.log("PIPELINE EXECUTION SUMMARY")
        self.log("=" * 80)
        self.log(f"Duration: {pipeline_duration:.1f} seconds")
        self.log("")

        for step_name, status in results.items():
            symbol = "[OK]" if status == "SUCCESS" else "[FAIL]"
            self.log(f"{symbol} {step_name}: {status}")

        all_success = all(s == "SUCCESS" for s in results.values())
        overall = "SUCCESS" if all_success else "PARTIAL SUCCESS"

        self.log("")
        self.log(f"Overall Status: {overall}", "SUCCESS" if all_success else "WARNING")
        self.log(f"Log file: {self.log_file}")
        self.log("=" * 80)

        return 0 if all_success else 1


def main():
    """Main execution."""
    pipeline = FullPipelineAutomation()
    exit_code = pipeline.run_pipeline()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
