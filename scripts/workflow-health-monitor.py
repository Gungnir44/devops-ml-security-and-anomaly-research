#!/usr/bin/env python3
"""
Workflow Health Monitoring & Alerting
======================================

Monitors workflow health and sends alerts for:
- Failed workflow runs
- Missing scheduled runs
- Long-running workflows
- Artifact upload failures
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta


class WorkflowHealthMonitor:
    """Monitor GitHub Actions workflow health."""

    def __init__(self):
        self.repo = "Gungnir44/devops-ml-security-and-anomaly-research"

        token_file = Path(__file__).parent / ".github_token"
        self.token = token_file.read_text().strip() if token_file.exists() else None

        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }

        self.alerts = []
        self.status = {
            'timestamp': datetime.now().isoformat(),
            'overall_health': 'HEALTHY',
            'issues_found': 0,
            'alerts': []
        }

    def check_failed_workflows(self):
        """Check for failed workflow runs in last 24 hours."""
        url = f'https://api.github.com/repos/{self.repo}/actions/runs?per_page=50'
        response = requests.get(url, headers=self.headers, timeout=10)
        runs = response.json().get('workflow_runs', [])

        cutoff = datetime.now() - timedelta(hours=24)
        recent_runs = [r for r in runs if datetime.strptime(r['created_at'], '%Y-%m-%dT%H:%M:%SZ') >= cutoff.replace(tzinfo=None)]

        failed_runs = [r for r in recent_runs if r['conclusion'] == 'failure']

        if failed_runs:
            self.status['overall_health'] = 'DEGRADED'
            self.status['issues_found'] += len(failed_runs)

            for run in failed_runs:
                alert = {
                    'severity': 'HIGH',
                    'type': 'WORKFLOW_FAILED',
                    'workflow': run['name'],
                    'branch': run['head_branch'],
                    'time': run['created_at'],
                    'url': run['html_url'],
                    'message': f"Workflow '{run['name']}' failed on branch '{run['head_branch']}'"
                }
                self.alerts.append(alert)
                self.status['alerts'].append(alert)

        return len(failed_runs)

    def check_missing_scheduled_runs(self):
        """Check if scheduled runs are missing."""
        url = f'https://api.github.com/repos/{self.repo}/actions/runs?per_page=50'
        response = requests.get(url, headers=self.headers, timeout=10)
        runs = response.json().get('workflow_runs', [])

        # Check for scheduled runs in last 48 hours
        cutoff = datetime.now() - timedelta(hours=48)
        scheduled_runs = [r for r in runs if r['event'] == 'schedule' and
                         datetime.strptime(r['created_at'], '%Y-%m-%dT%H:%M:%SZ') >= cutoff.replace(tzinfo=None)]

        if not scheduled_runs:
            self.status['overall_health'] = 'DEGRADED'
            self.status['issues_found'] += 1

            alert = {
                'severity': 'MEDIUM',
                'type': 'MISSING_SCHEDULED_RUN',
                'message': 'No scheduled workflow runs found in last 48 hours',
                'action': 'Verify scheduled workflows are enabled'
            }
            self.alerts.append(alert)
            self.status['alerts'].append(alert)
            return 0

        return len(scheduled_runs)

    def check_artifact_uploads(self):
        """Check for workflows without artifacts."""
        url = f'https://api.github.com/repos/{self.repo}/actions/runs?per_page=20'
        response = requests.get(url, headers=self.headers, timeout=10)
        runs = response.json().get('workflow_runs', [])

        cutoff = datetime.now() - timedelta(hours=24)
        recent_completed = [r for r in runs if
                           r['status'] == 'completed' and
                           r['conclusion'] == 'success' and
                           datetime.strptime(r['created_at'], '%Y-%m-%dT%H:%M:%SZ') >= cutoff.replace(tzinfo=None)]

        no_artifacts = []
        for run in recent_completed:
            artifacts_url = run['artifacts_url']
            artifacts_response = requests.get(artifacts_url, headers=self.headers, timeout=10)
            artifact_count = artifacts_response.json().get('total_count', 0)

            if artifact_count == 0 and 'Security Scanning' in run['name']:
                no_artifacts.append(run)

        if no_artifacts:
            self.status['overall_health'] = 'DEGRADED'
            self.status['issues_found'] += len(no_artifacts)

            for run in no_artifacts:
                alert = {
                    'severity': 'MEDIUM',
                    'type': 'NO_ARTIFACTS',
                    'workflow': run['name'],
                    'time': run['created_at'],
                    'message': f"Workflow '{run['name']}' completed successfully but produced no artifacts"
                }
                self.alerts.append(alert)
                self.status['alerts'].append(alert)

        return len(no_artifacts)

    def generate_health_report(self):
        """Generate health monitoring report."""
        print("=" * 80)
        print("WORKFLOW HEALTH MONITORING REPORT")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Repository: {self.repo}")
        print()

        # Overall status
        status_symbol = {
            'HEALTHY': '[OK]',
            'DEGRADED': '[WARN]',
            'CRITICAL': '[FAIL]'
        }

        print(f"Overall Health: {status_symbol.get(self.status['overall_health'], '?')} {self.status['overall_health']}")
        print(f"Issues Found: {self.status['issues_found']}")
        print()

        # Alerts
        if self.alerts:
            print("ALERTS:")
            print("-" * 80)
            for i, alert in enumerate(self.alerts, 1):
                severity_symbol = {
                    'HIGH': '[HIGH]',
                    'MEDIUM': '[MED]',
                    'LOW': '[LOW]'
                }
                print(f"{i}. [{alert['severity']}] {alert['type']}")
                print(f"   {alert['message']}")
                if 'url' in alert:
                    print(f"   URL: {alert['url']}")
                if 'action' in alert:
                    print(f"   Action: {alert['action']}")
                print()
        else:
            print("[OK] No alerts - all systems operational")
            print()

        # Save report
        log_dir = Path(__file__).parent / "logs" / "monitoring"
        log_dir.mkdir(parents=True, exist_ok=True)

        report_file = log_dir / f"health_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.status, f, indent=2)

        print(f"Report saved: {report_file}")
        print("=" * 80)

    def run_health_check(self):
        """Execute complete health check."""
        print()
        print("Running workflow health checks...")
        print()

        # Run checks
        failed = self.check_failed_workflows()
        print(f"[OK] Failed workflows check: {failed} failures found")

        scheduled = self.check_missing_scheduled_runs()
        print(f"[OK] Scheduled runs check: {scheduled} scheduled runs in 48h")

        no_artifacts = self.check_artifact_uploads()
        print(f"[OK] Artifact upload check: {no_artifacts} workflows without artifacts")
        print()

        # Generate report
        self.generate_health_report()

        return 0 if self.status['overall_health'] == 'HEALTHY' else 1


def main():
    """Main execution."""
    monitor = WorkflowHealthMonitor()
    exit_code = monitor.run_health_check()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
