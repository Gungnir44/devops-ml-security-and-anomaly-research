#!/usr/bin/env python3
"""Attack Scenario 9.2: Webhook / API Abuse - External Attack"""
import sys
import json
from pathlib import Path
from datetime import datetime
import random

class WebhookAbuseAttack:
    """Triggers workflows via exposed webhooks, floods API with requests."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.log_dir = Path(__file__).parent.parent / "logs" / "simulated_attacks"
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def simulate_webhook_flood(self):
        """Simulate webhook/API flooding attack."""
        # Simulate flooding attack logs
        attack_logs = []

        # Generate 500 malicious webhook triggers (simulated)
        for i in range(500):
            log_entry = {
                "timestamp": (datetime.now().replace(
                    hour=random.randint(0, 23),
                    minute=random.randint(0, 59),
                    second=random.randint(0, 59)
                )).isoformat(),
                "source_ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "endpoint": random.choice([
                    "/api/v1/deploy",
                    "/webhooks/github",
                    "/api/trigger/build",
                    "/webhooks/repository_dispatch",
                    "/api/admin/execute"
                ]),
                "method": "POST",
                "payload_size_bytes": random.randint(100, 10000),
                "user_agent": random.choice([
                    "python-requests/2.28.0",
                    "curl/7.68.0",
                    "Mozilla/5.0 (Automated)",
                    "AttackScript/1.0"
                ]),
                "event_type": random.choice([
                    "malicious_trigger",
                    "unauthorized_deploy",
                    "fake_push_event",
                    "spam_event"
                ]),
                "authenticated": False,
                "rate_limit_exceeded": i > 100,  # After 100 requests
                "suspicious": True
            }
            attack_logs.append(log_entry)

        # Create attack summary
        attack_summary = {
            "attack_type": "webhook_api_abuse",
            "scenario_id": "9.2",
            "timestamp": datetime.now().isoformat(),
            "total_requests": 500,
            "duration_minutes": 15,
            "requests_per_minute": 33.3,
            "unique_ips": len(set(log["source_ip"] for log in attack_logs)),
            "targeted_endpoints": list(set(log["endpoint"] for log in attack_logs)),
            "attack_pattern": "distributed_flood",
            "logs": attack_logs[:50]  # Sample of logs
        }

        # Save attack logs
        log_file = self.log_dir / f"webhook_abuse_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(attack_summary, f, indent=2)

        return log_file, attack_summary

    def create_malicious_workflow_trigger(self):
        """Create simulated workflow that can be triggered via webhook."""
        # Create a simulated workflow trigger configuration
        trigger_config = {
            "attack_type": "webhook_abuse",
            "trigger_method": "repository_dispatch",
            "simulated_commands": [
                "curl -X POST https://api.github.com/repos/{repo}/dispatches -d '{\"event_type\":\"malicious_trigger\"}'",
                "for i in {1..1000}; do curl -X POST {webhook_url} -d '{payload}' & done",
                "python3 flood_webhook.py --target {webhook_url} --count 1000 --threads 50"
            ],
            "impact": {
                "workflow_executions": "500+ unauthorized triggers",
                "resource_consumption": "high",
                "cost_impact": "potential GitHub Actions minutes abuse",
                "service_disruption": "potential DoS"
            }
        }

        # Save trigger configuration
        config_file = self.log_dir / f"webhook_trigger_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(config_file, 'w') as f:
            json.dump(trigger_config, f, indent=2)

        return config_file

    def log_indicators(self, attack_summary):
        """Log attack behavioral indicators."""
        indicators = {
            "attack_type": "webhook_api_abuse",
            "scenario_id": "9.2",
            "timestamp": datetime.now().isoformat(),
            "severity": "high",
            "indicators": {
                "webhook_flooding": True,
                "api_abuse": True,
                "unauthorized_triggers": True,
                "rate_limit_exceeded": True,
                "distributed_attack": True,
                "total_requests": attack_summary["total_requests"],
                "requests_per_minute": attack_summary["requests_per_minute"],
                "unique_source_ips": attack_summary["unique_ips"],
                "targeted_endpoints": attack_summary["targeted_endpoints"],
                "attack_duration_minutes": attack_summary["duration_minutes"]
            },
            "expected_detection": {
                "difficulty": "easy",
                "primary_signals": [
                    "high_request_rate",
                    "rate_limit_violations",
                    "unauthorized_endpoint_access",
                    "suspicious_user_agents",
                    "distributed_sources",
                    "workflow_trigger_anomalies",
                    "resource_consumption_spike"
                ],
                "detection_tools": [
                    "API rate limiting",
                    "WAF (Web Application Firewall)",
                    "Intrusion Detection System",
                    "Log analysis",
                    "GitHub webhook validation",
                    "API gateway monitoring"
                ]
            },
            "mitre_attack": {
                "technique": "T1498",
                "name": "Network Denial of Service",
                "tactic": "Impact",
                "sub_technique": "T1498.001 - Direct Network Flood"
            },
            "real_world_frequency": "high",
            "impact": {
                "service_disruption": "high",
                "resource_exhaustion": "high",
                "cost_impact": "medium",
                "unauthorized_actions": "high"
            }
        }

        # Save indicators
        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        with open(log_dir / f"webhook_abuse_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(indicators, f, indent=2)

        return indicators

    def execute(self):
        """Execute the attack."""
        print("=" * 80)
        print("ATTACK SCENARIO 9.2: Webhook / API Abuse")
        print("=" * 80)
        print("Severity: HIGH")
        print("Realism: 8/10 - Common if webhooks exposed")
        print("Impact: Service disruption, resource exhaustion")
        print()

        # Simulate webhook flood
        log_file, attack_summary = self.simulate_webhook_flood()
        print(f"[OK] Simulated {attack_summary['total_requests']} webhook requests")
        print(f"[OK] Attack duration: {attack_summary['duration_minutes']} minutes")
        print(f"[OK] Request rate: {attack_summary['requests_per_minute']:.1f} req/min")

        # Create trigger configuration
        config_file = self.create_malicious_workflow_trigger()
        print(f"[OK] Created malicious trigger configuration")

        # Log indicators
        self.log_indicators(attack_summary)

        print()
        print(f"[OK] Attack logs saved: {log_file.name}")
        print(f"[OK] Trigger config saved: {config_file.name}")
        print("[!] Detection: API rate limiting, WAF, log analysis")
        print("=" * 80)

        return True

if __name__ == "__main__":
    sys.exit(0 if WebhookAbuseAttack().execute() else 1)
