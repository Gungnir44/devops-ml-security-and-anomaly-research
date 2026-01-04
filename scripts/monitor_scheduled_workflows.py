#!/usr/bin/env python3
"""
Scheduled Workflow Monitor
==========================

Monitors GitHub Actions scheduled workflows and provides detailed status.
Run this daily to verify automatic scheduled runs are working.
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path


class WorkflowMonitor:
    """Monitor scheduled GitHub Actions workflows."""

    def __init__(self):
        self.repo = "Gungnir44/devops-ml-security-and-anomaly-research"
        self.workflow_file = "security-scanning.yml"

        # Load GitHub token
        token_file = Path(__file__).parent / ".github_token"
        if token_file.exists():
            with open(token_file, 'r') as f:
                self.token = f.read().strip()
        else:
            self.token = os.environ.get('GITHUB_TOKEN', '')

        if not self.token:
            print("[!] Warning: No GitHub token found")
            print("    Set GITHUB_TOKEN env var or create scripts/.github_token")
            sys.exit(1)

        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }

    def get_workflow_runs(self, per_page=20):
        """Fetch recent workflow runs."""
        url = f'https://api.github.com/repos/{self.repo}/actions/workflows/{self.workflow_file}/runs'
        params = {'per_page': per_page}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get('workflow_runs', [])
        except Exception as e:
            print(f"[!] Error fetching workflow runs: {e}")
            return []

    def analyze_runs(self, runs):
        """Analyze workflow runs to check for scheduled executions."""
        now = datetime.utcnow()
        last_24h = now - timedelta(hours=24)
        last_7d = now - timedelta(days=7)

        # Categorize runs
        scheduled_runs = []
        push_runs = []
        manual_runs = []
        recent_scheduled = []

        for run in runs:
            created_at = datetime.strptime(run['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            event = run['event']

            if event == 'schedule':
                scheduled_runs.append(run)
                if created_at >= last_24h:
                    recent_scheduled.append(run)
            elif event == 'push':
                push_runs.append(run)
            elif event == 'workflow_dispatch':
                manual_runs.append(run)

        return {
            'total': len(runs),
            'scheduled': scheduled_runs,
            'scheduled_count': len(scheduled_runs),
            'push_count': len(push_runs),
            'manual_count': len(manual_runs),
            'scheduled_last_24h': len(recent_scheduled),
            'recent_scheduled': recent_scheduled,
            'latest_run': runs[0] if runs else None,
            'last_7d_runs': [r for r in runs if datetime.strptime(r['created_at'], '%Y-%m-%dT%H:%M:%SZ') >= last_7d]
        }

    def get_next_scheduled_run(self):
        """Calculate next expected scheduled run time (2 AM UTC)."""
        now = datetime.utcnow()

        # Next 2 AM UTC
        next_run = now.replace(hour=2, minute=0, second=0, microsecond=0)

        # If we're past 2 AM today, schedule for tomorrow
        if now.hour >= 2:
            next_run += timedelta(days=1)

        return next_run

    def format_run_info(self, run):
        """Format run information for display."""
        created = datetime.strptime(run['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        return {
            'time': created.strftime('%Y-%m-%d %H:%M UTC'),
            'event': run['event'],
            'status': run['status'],
            'conclusion': run['conclusion'],
            'branch': run['head_branch'],
            'url': run['html_url']
        }

    def print_status_report(self):
        """Print comprehensive status report."""
        print("=" * 80)
        print("SCHEDULED WORKFLOW MONITOR")
        print("=" * 80)
        print(f"Repository: {self.repo}")
        print(f"Workflow: {self.workflow_file}")
        print(f"Current Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("=" * 80)
        print()

        # Fetch and analyze runs
        runs = self.get_workflow_runs(per_page=30)

        if not runs:
            print("[!] No workflow runs found or API error")
            return

        analysis = self.analyze_runs(runs)

        # Status summary
        print("RUN SUMMARY (Last 30 runs):")
        print("-" * 80)
        print(f"  Total runs:               {analysis['total']}")
        print(f"  Scheduled runs (schedule): {analysis['scheduled_count']}")
        print(f"  Push-triggered runs:      {analysis['push_count']}")
        print(f"  Manual runs (dispatch):   {analysis['manual_count']}")
        print()

        # Scheduled runs status
        if analysis['scheduled_count'] > 0:
            print("[OK] SCHEDULED RUNS: ACTIVE")
            print("-" * 80)
            print(f"  Total scheduled runs: {analysis['scheduled_count']}")
            print(f"  Last 24 hours: {analysis['scheduled_last_24h']}")
            print()

            # Show recent scheduled runs
            if analysis['scheduled']:
                print("Recent scheduled runs:")
                for run in analysis['scheduled'][:5]:
                    info = self.format_run_info(run)
                    status_icon = "[OK]" if info['conclusion'] == 'success' else "[FAIL]"
                    print(f"  {status_icon} {info['time']} | {info['status']:10s} | {info['conclusion']}")
        else:
            print("[!] SCHEDULED RUNS: NOT YET ACTIVE")
            print("-" * 80)
            print("  No scheduled runs detected yet.")
            print()

            # Check if manual trigger happened recently
            if analysis['manual_count'] > 0:
                print("[*] Manual triggers detected:")
                for run in [r for r in runs if r['event'] == 'workflow_dispatch'][:3]:
                    info = self.format_run_info(run)
                    print(f"    - {info['time']}")
                print()
                print("  -> Scheduled runs should start within 24-48 hours after manual trigger")
            else:
                print("[*] RECOMMENDATION: Manually trigger the workflow to activate scheduler")
                print("   Go to: https://github.com/{}/actions/workflows/{}".format(
                    self.repo, self.workflow_file
                ))
                print("   Click: 'Run workflow' button")

        print()

        # Latest run info
        if analysis['latest_run']:
            print("LATEST RUN:")
            print("-" * 80)
            info = self.format_run_info(analysis['latest_run'])
            print(f"  Time:       {info['time']}")
            print(f"  Trigger:    {info['event']}")
            print(f"  Branch:     {info['branch']}")
            print(f"  Status:     {info['status']}")
            print(f"  Conclusion: {info['conclusion']}")
            print(f"  URL:        {info['url']}")
            print()

        # Next scheduled run
        next_run = self.get_next_scheduled_run()
        hours_until = (next_run - datetime.utcnow()).total_seconds() / 3600

        print("NEXT EXPECTED SCHEDULED RUN:")
        print("-" * 80)
        print(f"  Scheduled for: {next_run.strftime('%Y-%m-%d at 02:00 UTC')}")
        print(f"  Time until:    {hours_until:.1f} hours")

        if analysis['scheduled_count'] > 0:
            print(f"  Expected:      [OK] Should run automatically")
        else:
            print(f"  Expected:      [!] May not run (scheduler not activated)")

        print()

        # Activity in last 7 days
        print("ACTIVITY LAST 7 DAYS:")
        print("-" * 80)

        last_7d = analysis['last_7d_runs']
        if last_7d:
            # Group by date
            by_date = {}
            for run in last_7d:
                created = datetime.strptime(run['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                date_key = created.strftime('%Y-%m-%d')
                if date_key not in by_date:
                    by_date[date_key] = []
                by_date[date_key].append(run)

            for date in sorted(by_date.keys(), reverse=True):
                runs_on_date = by_date[date]
                scheduled = sum(1 for r in runs_on_date if r['event'] == 'schedule')
                push = sum(1 for r in runs_on_date if r['event'] == 'push')
                manual = sum(1 for r in runs_on_date if r['event'] == 'workflow_dispatch')

                status = "[OK] scheduled" if scheduled > 0 else "[ ] no scheduled run"
                print(f"  {date}: {len(runs_on_date)} runs (scheduled:{scheduled}, push:{push}, manual:{manual}) {status}")
        else:
            print("  No runs in last 7 days")

        print()
        print("=" * 80)

        # Final verdict
        if analysis['scheduled_count'] > 0:
            print("[OK] STATUS: Scheduled workflows are ACTIVE and working!")
            if analysis['scheduled_last_24h'] > 0:
                print("     [OK] Recent scheduled run detected in last 24 hours")
            else:
                print("     [*] No scheduled run in last 24h (next run expected soon)")
        else:
            print("[!] STATUS: Scheduled workflows NOT YET ACTIVATED")
            print("    Action needed: Manual trigger or wait a few more days")

        print("=" * 80)

    def save_status_log(self):
        """Save status to log file for tracking over time."""
        runs = self.get_workflow_runs(per_page=30)
        analysis = self.analyze_runs(runs)

        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'scheduled_runs_total': analysis['scheduled_count'],
            'scheduled_runs_24h': analysis['scheduled_last_24h'],
            'total_runs': analysis['total'],
            'status': 'active' if analysis['scheduled_count'] > 0 else 'inactive'
        }

        log_file = Path(__file__).parent / "logs" / "workflow_monitoring.jsonl"
        log_file.parent.mkdir(exist_ok=True)

        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

        return log_file


def main():
    """Main execution."""
    monitor = WorkflowMonitor()

    # Print status report
    monitor.print_status_report()

    # Save log
    log_file = monitor.save_status_log()
    print(f"\n[*] Status logged to: {log_file}")
    print()
    print("[*] TIP: Run this script daily to monitor scheduled workflow activation")
    print("   Command: python scripts/monitor_scheduled_workflows.py")
    print()


if __name__ == "__main__":
    main()
