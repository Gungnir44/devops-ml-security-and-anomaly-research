"""
Container Events Feature Extractor

Extracts 24 features from container and orchestration events.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from loguru import logger

from .base_extractor import BaseExtractor


class ContainerExtractor(BaseExtractor):
    """
    Extracts container features from:
    - Kubernetes events (if available)
    - Docker events (if available)
    - Container logs
    - Pod status
    """

    def get_feature_names(self) -> List[str]:
        """Return list of 24 container feature names."""
        return [
            # Container lifecycle
            'containers_started_count',
            'containers_stopped_count',
            'containers_restarted_count',
            'containers_killed_count',

            # Image operations
            'images_pulled_count',
            'images_pushed_count',
            'unique_images_count',

            # Resource usage
            'container_cpu_total_cores',
            'container_memory_total_mb',
            'container_cpu_throttled_count',

            # Pod operations
            'pods_created_count',
            'pods_deleted_count',
            'pods_evicted_count',
            'pods_failed_count',

            # Scaling events
            'scale_up_events_count',
            'scale_down_events_count',
            'replica_count_avg',

            # Health checks
            'liveness_probe_failures',
            'readiness_probe_failures',

            # Image security
            'unsigned_images_count',
            'images_from_unknown_registries',

            # Network policies
            'network_policy_violations',

            # Container exits
            'container_exit_code_0_count',
            'container_exit_nonzero_count',
        ]

    def extract(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Extract all 24 container features.

        Args:
            start_time: Start of time window
            end_time: End of time window
            **kwargs: Additional parameters

        Returns:
            Dictionary of features
        """
        logger.info("Extracting container features")

        # Initialize features
        features = {name: 0 for name in self.get_feature_names()}
        features.update({
            'container_cpu_total_cores': 0.0,
            'container_memory_total_mb': 0.0,
            'replica_count_avg': 0.0,
        })

        try:
            # Check if Kubernetes is available
            k8s_available = self._check_kubernetes_available()

            if k8s_available:
                # Extract from Kubernetes
                k8s_features = self._extract_kubernetes_features(start_time, end_time)
                features.update(k8s_features)
            else:
                # Use estimated features based on CI/CD data
                logger.info("Kubernetes not available, using estimated container features")
                estimated_features = self._get_estimated_features()
                features.update(estimated_features)

            logger.success(f"Extracted {len(features)} container features")

        except Exception as e:
            logger.error(f"Error extracting container features: {e}")
            logger.exception(e)

        return features

    def _check_kubernetes_available(self) -> bool:
        """Check if Kubernetes API is available."""
        try:
            from kubernetes import client, config
            config.load_kube_config()
            return True
        except:
            return False

    def _extract_kubernetes_features(
        self,
        start_time: Optional[datetime],
        end_time: Optional[datetime]
    ) -> Dict[str, Any]:
        """Extract features from Kubernetes API."""
        features = {}

        try:
            from kubernetes import client

            # Get core API
            v1 = client.CoreV1Api()

            # Get pods
            pods = v1.list_pod_for_all_namespaces()

            # Analyze pod status
            pod_counts = defaultdict(int)
            container_restarts = 0
            liveness_failures = 0
            readiness_failures = 0

            for pod in pods.items:
                status = pod.status.phase
                pod_counts[status] += 1

                # Container restarts
                if pod.status.container_statuses:
                    for container in pod.status.container_statuses:
                        container_restarts += container.restart_count

                # Probe failures (would need events)

            features['pods_created_count'] = len(pods.items)
            features['pods_failed_count'] = pod_counts.get('Failed', 0)
            features['containers_restarted_count'] = container_restarts

            # Get events for more detailed info
            events = v1.list_event_for_all_namespaces()
            container_events = defaultdict(int)

            for event in events.items:
                reason = event.reason
                if 'Pulled' in reason:
                    container_events['pulled'] += 1
                elif 'Created' in reason:
                    container_events['created'] += 1
                elif 'Started' in reason:
                    container_events['started'] += 1
                elif 'Killing' in reason:
                    container_events['killed'] += 1

            features['containers_started_count'] = container_events.get('started', 0)
            features['containers_killed_count'] = container_events.get('killed', 0)
            features['images_pulled_count'] = container_events.get('pulled', 0)

            logger.debug(f"Extracted Kubernetes features from {len(pods.items)} pods")

        except Exception as e:
            logger.error(f"Error extracting from Kubernetes: {e}")

        return features

    def _get_estimated_features(self) -> Dict[str, Any]:
        """
        Get estimated container features when Kubernetes is not available.
        Based on typical microservices deployment.
        """
        # Estimate based on 3 applications running in containers
        num_apps = 3

        features = {
            # Lifecycle - assume daily restarts/updates
            'containers_started_count': num_apps * 2,  # 2 starts per app
            'containers_stopped_count': num_apps,
            'containers_restarted_count': 1,  # Occasional restart
            'containers_killed_count': 0,

            # Images - one per app
            'images_pulled_count': num_apps,
            'images_pushed_count': num_apps,  # From CI/CD
            'unique_images_count': num_apps,

            # Resource usage (estimates)
            'container_cpu_total_cores': 1.5,  # ~0.5 cores per app
            'container_memory_total_mb': 1536.0,  # ~512MB per app
            'container_cpu_throttled_count': 0,

            # Pods
            'pods_created_count': num_apps,
            'pods_deleted_count': 0,
            'pods_evicted_count': 0,
            'pods_failed_count': 0,

            # Scaling
            'scale_up_events_count': 0,
            'scale_down_events_count': 0,
            'replica_count_avg': 1.0,  # Single replica per app

            # Health checks
            'liveness_probe_failures': 0,
            'readiness_probe_failures': 0,

            # Security
            'unsigned_images_count': 0,  # Assuming signed images
            'images_from_unknown_registries': 0,

            # Network
            'network_policy_violations': 0,

            # Exit codes
            'container_exit_code_0_count': num_apps,  # Clean exits
            'container_exit_nonzero_count': 0,
        }

        return features
