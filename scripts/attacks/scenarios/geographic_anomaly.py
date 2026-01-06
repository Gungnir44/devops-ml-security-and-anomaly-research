#!/usr/bin/env python3
"""Attack Scenario 1.1: Geographic Anomaly - Log-based simulation"""
import sys, json
from pathlib import Path
from datetime import datetime
import random

class GeographicAnomalyAttack:
    def __init__(self):
        self.log_dir = Path(__file__).parent.parent / "logs" / "simulated_access"
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def simulate_anomalous_access(self):
        # Simulate access from unusual location
        anomalous_locations = [
            ("185.220.101.42", "Romania", "Bucharest", 44.4268, 26.1025),
            ("203.0.113.42", "China", "Beijing", 39.9042, 116.4074),
            ("198.51.100.23", "Russia", "Moscow", 55.7558, 37.6173)
        ]

        ip, country, city, lat, lon = random.choice(anomalous_locations)

        access_logs = []
        # Generate 10-15 suspicious access attempts
        for i in range(random.randint(10, 15)):
            log = {
                "timestamp": (datetime.now().replace(hour=random.randint(1, 4))).isoformat(),
                "user_id": "dev_john_doe",
                "ip_address": ip,
                "geolocation": {"country": country, "city": city, "lat": lat, "lon": lon},
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "action": random.choice(["repo_view", "repo_clone", "secrets_access"]),
                "resource": random.choice(["internal-api", "customer-db", "secrets-manager"]),
                "unusual_hour": True,
                "distance_from_usual_km": random.randint(7000, 9000)
            }
            access_logs.append(log)

        log_file = self.log_dir / f"geographic_anomaly_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump({"access_logs": access_logs}, f, indent=2)

        return log_file, access_logs

    def log_indicators(self, location):
        indicators = {
            "attack_type": "geographic_anomaly",
            "scenario_id": "1.1",
            "timestamp": datetime.now().isoformat(),
            "indicators": {
                "geographic_anomaly": True,
                "unusual_country": location[1],
                "impossible_travel": True,
                "unusual_hours": True,
                "multiple_resource_access": True
            },
            "expected_detection": {"difficulty": "easy", "primary_signals": ["location_change", "temporal_anomaly"]},
            "mitre_attack": {"technique": "T1078", "name": "Valid Accounts"}
        }

        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)
        with open(log_dir / f"geographic_anomaly_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(indicators, f, indent=2)

        return indicators

    def execute(self):
        print("=" * 80 + "\nATTACK SCENARIO 1.1: Geographic Anomaly\n")
        log_file, logs = self.simulate_anomalous_access()
        indicators = self.log_indicators(("", logs[0]['geolocation']['country'], "", 0, 0))
        print(f"[OK] Simulated {len(logs)} anomalous access attempts")
        print(f"[OK] Location: {logs[0]['geolocation']['city']}, {logs[0]['geolocation']['country']}")
        print(f"[OK] Logs saved: {log_file}\n" + "=" * 80)
        return True

if __name__ == "__main__":
    sys.exit(0 if GeographicAnomalyAttack().execute() else 1)
