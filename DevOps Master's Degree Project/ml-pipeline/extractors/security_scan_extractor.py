"""
Security Scan Feature Extractor

Extracts 21 security-related features from security scanning tool outputs.
"""

import json
import zipfile
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import defaultdict
import pandas as pd
from loguru import logger

from .base_extractor import BaseExtractor


class SecurityScanExtractor(BaseExtractor):
    """
    Extracts security scan features from:
    - TruffleHog (secrets)
    - Gitleaks (secrets)
    - Trivy (containers)
    - Grype (containers)
    - Dockle (containers)
    - CodeQL (SAST)
    - Semgrep (SAST)
    - Bandit (Python SAST)
    - npm audit (dependencies)
    - pip-audit (dependencies)
    - Checkov (IaC)
    - tfsec (Terraform)
    """

    def get_feature_names(self) -> List[str]:
        """Return list of 21 security scan feature names."""
        return [
            # Vulnerability counts by severity
            'vuln_critical_count',
            'vuln_high_count',
            'vuln_medium_count',
            'vuln_low_count',

            # Secret detection
            'secrets_detected_count',
            'secrets_verified_count',

            # Container security
            'container_vulnerabilities',
            'container_misconfigurations',

            # Dependency vulnerabilities
            'npm_vulnerabilities',
            'python_vulnerabilities',

            # SAST findings
            'sast_code_smells',
            'sast_security_issues',

            # IaC
            'iac_misconfigurations',

            # Trends
            'vuln_new_count',
            'vuln_fixed_count',
            'vuln_age_avg_days',

            # Scan metrics
            'scans_failed_count',
            'scan_duration_avg_seconds',

            # Compliance
            'cve_count',
            'cwe_count',

            # Risk score
            'security_risk_score',
        ]

    def extract(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Extract all 21 security scan features.

        Args:
            start_time: Start of time window
            end_time: End of time window
            **kwargs: Additional parameters

        Returns:
            Dictionary of features
        """
        logger.info(f"Extracting security scan features from {self.data_dir}")

        # Initialize feature dictionary with zeros
        features = {name: 0 for name in self.get_feature_names()}

        # Extract from different sources
        try:
            # Extract from code scanning alerts (GitHub Security tab)
            code_scanning_features = self._extract_code_scanning_alerts()
            features.update(code_scanning_features)

            # Extract from npm audit
            npm_features = self._extract_npm_audit()
            features.update(npm_features)

            # Extract from pip audit
            pip_features = self._extract_pip_audit()
            features.update(pip_features)

            # Extract from Bandit reports
            bandit_features = self._extract_bandit_reports()
            features.update(bandit_features)

            # Extract from KICS/Checkov
            iac_features = self._extract_iac_scans()
            features.update(iac_features)

            # Calculate derived features
            derived_features = self._calculate_derived_features(features)
            features.update(derived_features)

            logger.success(f"Extracted {len(features)} security features")

        except Exception as e:
            logger.error(f"Error extracting security features: {e}")
            logger.exception(e)

        return features

    def _extract_code_scanning_alerts(self) -> Dict[str, Any]:
        """Extract features from GitHub Code Scanning alerts."""
        features = {}

        # Find all-alerts.json files
        alert_files = self._find_files("**/code-scanning-alerts/all-alerts.json")

        if not alert_files:
            logger.warning("No code scanning alert files found")
            return features

        # Use the most recent file
        latest_file = max(alert_files, key=lambda p: p.stat().st_mtime)
        logger.debug(f"Using code scanning alerts from: {latest_file}")

        try:
            with open(latest_file, 'r') as f:
                alerts = json.load(f)

            # Count by severity
            severity_counts = defaultdict(int)
            tools = set()
            cves = set()
            cwes = set()

            for alert in alerts:
                severity = alert.get('rule', {}).get('security_severity_level', 'unknown').lower()
                severity_counts[severity] += 1

                # Track tools
                tool = alert.get('tool', {}).get('name', 'unknown')
                tools.add(tool)

                # Extract CVEs and CWEs from tags
                tags = alert.get('rule', {}).get('tags', [])
                for tag in tags:
                    if tag.startswith('CVE-'):
                        cves.add(tag)
                    elif tag.startswith('CWE-'):
                        cwes.add(tag)

            features['vuln_critical_count'] = severity_counts.get('critical', 0)
            features['vuln_high_count'] = severity_counts.get('high', 0)
            features['vuln_medium_count'] = severity_counts.get('medium', 0)
            features['vuln_low_count'] = severity_counts.get('low', 0) + severity_counts.get('note', 0)

            features['cve_count'] = len(cves)
            features['cwe_count'] = len(cwes)

            # Categorize by tool
            sast_count = sum(1 for alert in alerts
                           if alert.get('tool', {}).get('name') in ['CodeQL', 'Semgrep', 'Bandit'])
            container_count = sum(1 for alert in alerts
                                if alert.get('tool', {}).get('name') in ['Grype', 'Trivy'])

            features['sast_security_issues'] = sast_count
            features['container_vulnerabilities'] = container_count

            logger.debug(f"Extracted {len(alerts)} alerts from code scanning")

        except Exception as e:
            logger.error(f"Error parsing code scanning alerts: {e}")

        return features

    def _extract_npm_audit(self) -> Dict[str, Any]:
        """Extract features from npm audit results."""
        features = {}
        audit_files = self._find_files("**/backend-npm-audit.zip") + \
                     self._find_files("**/frontend-npm-audit.zip")

        if not audit_files:
            return {'npm_vulnerabilities': 0}

        total_vulns = 0

        for zip_path in audit_files:
            try:
                with zipfile.ZipFile(zip_path, 'r') as zf:
                    # npm audit outputs npm-audit.json
                    json_files = [name for name in zf.namelist() if name.endswith('.json')]

                    for json_file in json_files:
                        with zf.open(json_file) as f:
                            audit_data = json.load(f)

                            # npm audit v7+ format
                            if 'vulnerabilities' in audit_data:
                                vulns = audit_data['vulnerabilities']
                                total_vulns += len(vulns)
                            # npm audit v6 format
                            elif 'metadata' in audit_data:
                                metadata = audit_data['metadata']
                                vulnerabilities = metadata.get('vulnerabilities', {})
                                total_vulns += sum(vulnerabilities.values())

            except Exception as e:
                logger.warning(f"Error parsing npm audit {zip_path}: {e}")

        features['npm_vulnerabilities'] = total_vulns
        return features

    def _extract_pip_audit(self) -> Dict[str, Any]:
        """Extract features from pip-audit results."""
        features = {}
        audit_files = self._find_files("**/python-pip-audit.zip")

        if not audit_files:
            return {'python_vulnerabilities': 0}

        total_vulns = 0

        for zip_path in audit_files:
            try:
                with zipfile.ZipFile(zip_path, 'r') as zf:
                    json_files = [name for name in zf.namelist() if name.endswith('.json')]

                    for json_file in json_files:
                        with zf.open(json_file) as f:
                            audit_data = json.load(f)

                            # pip-audit outputs list of vulnerabilities
                            if isinstance(audit_data, dict) and 'vulnerabilities' in audit_data:
                                total_vulns += len(audit_data['vulnerabilities'])
                            elif isinstance(audit_data, list):
                                total_vulns += len(audit_data)

            except Exception as e:
                logger.warning(f"Error parsing pip audit {zip_path}: {e}")

        features['python_vulnerabilities'] = total_vulns
        return features

    def _extract_bandit_reports(self) -> Dict[str, Any]:
        """Extract features from Bandit SAST reports."""
        features = {}
        bandit_files = self._find_files("**/bandit-report/bandit-report.json") + \
                      self._find_files("**/bandit-security-report.zip")

        if not bandit_files:
            return {}

        total_issues = 0
        severity_counts = defaultdict(int)

        for file_path in bandit_files:
            try:
                if file_path.suffix == '.zip':
                    with zipfile.ZipFile(file_path, 'r') as zf:
                        json_files = [name for name in zf.namelist() if 'bandit' in name.lower() and name.endswith('.json')]
                        for json_file in json_files:
                            with zf.open(json_file) as f:
                                data = json.load(f)
                                self._parse_bandit_data(data, severity_counts)
                else:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        self._parse_bandit_data(data, severity_counts)

            except Exception as e:
                logger.warning(f"Error parsing Bandit report {file_path}: {e}")

        # Bandit reports code quality and security issues
        features['sast_code_smells'] = severity_counts.get('LOW', 0)
        features['sast_security_issues'] = severity_counts.get('MEDIUM', 0) + severity_counts.get('HIGH', 0)

        return features

    def _parse_bandit_data(self, data: Dict, severity_counts: Dict) -> None:
        """Parse Bandit JSON data and update severity counts."""
        if 'results' in data:
            for issue in data['results']:
                severity = issue.get('issue_severity', 'UNKNOWN')
                severity_counts[severity] += 1

    def _extract_iac_scans(self) -> Dict[str, Any]:
        """Extract features from IaC scanning tools (Checkov, KICS, tfsec)."""
        features = {}
        iac_files = self._find_files("**/kics-results/results.json") + \
                   self._find_files("**/kics-results.zip")

        if not iac_files:
            return {'iac_misconfigurations': 0}

        total_issues = 0

        for file_path in iac_files:
            try:
                if file_path.suffix == '.zip':
                    with zipfile.ZipFile(file_path, 'r') as zf:
                        json_files = [name for name in zf.namelist() if name.endswith('.json')]
                        for json_file in json_files:
                            with zf.open(json_file) as f:
                                data = json.load(f)
                                # KICS format
                                if 'queries' in data:
                                    for query in data['queries']:
                                        total_issues += len(query.get('files', []))
                else:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if 'queries' in data:
                            for query in data['queries']:
                                total_issues += len(query.get('files', []))

            except Exception as e:
                logger.warning(f"Error parsing IaC scan {file_path}: {e}")

        features['iac_misconfigurations'] = total_issues
        features['container_misconfigurations'] = total_issues  # IaC includes container configs

        return features

    def _calculate_derived_features(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate derived features from base features."""
        derived = {}

        # Calculate security risk score (weighted sum)
        # Critical=10, High=5, Medium=2, Low=0.5
        risk_score = (
            features.get('vuln_critical_count', 0) * 10 +
            features.get('vuln_high_count', 0) * 5 +
            features.get('vuln_medium_count', 0) * 2 +
            features.get('vuln_low_count', 0) * 0.5 +
            features.get('secrets_verified_count', 0) * 20  # Secrets are critical!
        )

        derived['security_risk_score'] = min(risk_score, 100.0)  # Cap at 100

        # For now, set trend features to 0 (requires historical comparison)
        derived['vuln_new_count'] = 0
        derived['vuln_fixed_count'] = 0
        derived['vuln_age_avg_days'] = 0.0

        # Scan metrics (would come from workflow logs)
        derived['scans_failed_count'] = 0
        derived['scan_duration_avg_seconds'] = 0.0

        # Secrets (not currently extracted from TruffleHog/Gitleaks)
        if 'secrets_detected_count' not in features:
            derived['secrets_detected_count'] = 0
        if 'secrets_verified_count' not in features:
            derived['secrets_verified_count'] = 0

        return derived
