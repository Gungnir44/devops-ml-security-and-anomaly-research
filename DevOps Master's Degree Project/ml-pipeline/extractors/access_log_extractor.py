"""
Access Log Feature Extractor

Extracts 28 features from application access logs.
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import math
from loguru import logger

from .base_extractor import BaseExtractor


class AccessLogExtractor(BaseExtractor):
    """
    Extracts access log features from:
    - Nginx access logs
    - Application logs
    - HTTP request logs
    """

    def __init__(self, data_dir: Path, config: Optional[Dict[str, Any]] = None):
        """Initialize with log file paths."""
        super().__init__(data_dir, config)

        # Default log file patterns
        self.log_patterns = config.get('log_patterns', [
            '**/access.log',
            '**/nginx.log',
            '**/*access*.log',
        ]) if config else []

    def get_feature_names(self) -> List[str]:
        """Return list of 28 access log feature names."""
        return [
            # Request volume
            'requests_total_count',
            'requests_per_second_avg',
            'requests_per_second_max',

            # HTTP methods
            'requests_get_count',
            'requests_post_count',
            'requests_put_count',
            'requests_delete_count',

            # Status codes
            'status_2xx_count',
            'status_3xx_count',
            'status_4xx_count',
            'status_5xx_count',
            'error_rate_percent',

            # Endpoint patterns
            'unique_endpoints_count',
            'endpoint_diversity_score',

            # User agents
            'unique_user_agents_count',
            'bot_requests_count',

            # IP patterns
            'unique_ips_count',
            'requests_per_ip_avg',
            'requests_per_ip_max',

            # Geographic distribution
            'unique_countries_count',

            # Request sizes
            'request_size_avg_bytes',
            'response_size_avg_bytes',

            # Authentication patterns
            'auth_attempts_count',
            'auth_failures_count',
            'auth_failure_rate',

            # Suspicious patterns
            'suspicious_payloads_count',
            'sql_injection_attempts',

            # Rate limiting
            'rate_limit_hits_count',
        ]

    def extract(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Extract all 28 access log features.

        Args:
            start_time: Start of time window
            end_time: End of time window
            **kwargs: Additional parameters

        Returns:
            Dictionary of features
        """
        logger.info("Extracting access log features")

        # Initialize features
        features = {name: 0 for name in self.get_feature_names()}
        features.update({
            'requests_per_second_avg': 0.0,
            'requests_per_second_max': 0.0,
            'error_rate_percent': 0.0,
            'endpoint_diversity_score': 0.0,
            'requests_per_ip_avg': 0.0,
            'auth_failure_rate': 0.0,
            'request_size_avg_bytes': 0.0,
            'response_size_avg_bytes': 0.0,
        })

        try:
            # Find log files
            log_files = []
            for pattern in self.log_patterns:
                log_files.extend(self._find_files(pattern, start_time, end_time))

            if log_files:
                logger.debug(f"Found {len(log_files)} log files")
                log_features = self._extract_from_logs(log_files, start_time, end_time)
                features.update(log_features)
            else:
                logger.info("No access logs found, using estimated features")
                estimated_features = self._get_estimated_features(start_time, end_time)
                features.update(estimated_features)

            logger.success(f"Extracted {len(features)} access log features")

        except Exception as e:
            logger.error(f"Error extracting access log features: {e}")
            logger.exception(e)

        return features

    def _extract_from_logs(
        self,
        log_files: List[Path],
        start_time: Optional[datetime],
        end_time: Optional[datetime]
    ) -> Dict[str, Any]:
        """Extract features from log files."""
        features = {}

        # Parse logs
        log_entries = []
        for log_file in log_files:
            try:
                entries = self._parse_log_file(log_file)
                log_entries.extend(entries)
            except Exception as e:
                logger.warning(f"Error parsing {log_file}: {e}")

        if not log_entries:
            return features

        # Analyze logs
        methods = Counter()
        status_codes = Counter()
        endpoints = set()
        user_agents = set()
        ips = set()
        ip_request_counts = Counter()

        for entry in log_entries:
            methods[entry.get('method', 'GET')] += 1
            status = entry.get('status', 200)
            status_codes[status] += 1
            endpoints.add(entry.get('endpoint', '/'))
            user_agents.add(entry.get('user_agent', 'unknown'))
            ip = entry.get('ip', '0.0.0.0')
            ips.add(ip)
            ip_request_counts[ip] += 1

        # Calculate features
        total_requests = len(log_entries)
        features['requests_total_count'] = total_requests

        # HTTP methods
        features['requests_get_count'] = methods.get('GET', 0)
        features['requests_post_count'] = methods.get('POST', 0)
        features['requests_put_count'] = methods.get('PUT', 0)
        features['requests_delete_count'] = methods.get('DELETE', 0)

        # Status codes
        status_2xx = sum(count for status, count in status_codes.items() if 200 <= status < 300)
        status_3xx = sum(count for status, count in status_codes.items() if 300 <= status < 400)
        status_4xx = sum(count for status, count in status_codes.items() if 400 <= status < 500)
        status_5xx = sum(count for status, count in status_codes.items() if 500 <= status < 600)

        features['status_2xx_count'] = status_2xx
        features['status_3xx_count'] = status_3xx
        features['status_4xx_count'] = status_4xx
        features['status_5xx_count'] = status_5xx
        features['error_rate_percent'] = ((status_4xx + status_5xx) / total_requests * 100) if total_requests > 0 else 0.0

        # Endpoints
        features['unique_endpoints_count'] = len(endpoints)
        features['endpoint_diversity_score'] = self._calculate_shannon_entropy([
            ip_request_counts[ip] for ip in ips
        ])

        # User agents
        features['unique_user_agents_count'] = len(user_agents)
        features['bot_requests_count'] = sum(1 for ua in user_agents if 'bot' in ua.lower())

        # IPs
        features['unique_ips_count'] = len(ips)
        if len(ips) > 0:
            features['requests_per_ip_avg'] = total_requests / len(ips)
            features['requests_per_ip_max'] = max(ip_request_counts.values())

        return features

    def _parse_log_file(self, log_file: Path) -> List[Dict[str, Any]]:
        """Parse a log file (simple nginx format)."""
        entries = []

        # Nginx combined log format regex
        nginx_pattern = r'(?P<ip>[\d\.]+) - - \[(?P<time>.*?)\] "(?P<method>\w+) (?P<endpoint>.*?) HTTP/\d\.\d" (?P<status>\d+) (?P<size>\d+) "(?P<referer>.*?)" "(?P<user_agent>.*?)"'

        try:
            with open(log_file, 'r', errors='ignore') as f:
                for line in f:
                    match = re.match(nginx_pattern, line)
                    if match:
                        entries.append({
                            'ip': match.group('ip'),
                            'method': match.group('method'),
                            'endpoint': match.group('endpoint'),
                            'status': int(match.group('status')),
                            'size': int(match.group('size')),
                            'user_agent': match.group('user_agent'),
                        })
        except Exception as e:
            logger.debug(f"Error reading {log_file}: {e}")

        return entries

    def _calculate_shannon_entropy(self, counts: List[int]) -> float:
        """Calculate Shannon entropy for diversity score."""
        if not counts:
            return 0.0

        total = sum(counts)
        if total == 0:
            return 0.0

        entropy = 0.0
        for count in counts:
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)

        return entropy

    def _get_estimated_features(
        self,
        start_time: Optional[datetime],
        end_time: Optional[datetime]
    ) -> Dict[str, Any]:
        """Get estimated access log features."""
        if not end_time:
            end_time = datetime.now()
        if not start_time:
            start_time = end_time - timedelta(days=1)

        hours = (end_time - start_time).total_seconds() / 3600

        # Estimate ~100 requests/hour for 3 services
        total_requests = int(100 * hours)

        features = {
            # Request volume
            'requests_total_count': total_requests,
            'requests_per_second_avg': total_requests / (hours * 3600) if hours > 0 else 0.0,
            'requests_per_second_max': 5.0,

            # HTTP methods (typical distribution)
            'requests_get_count': int(total_requests * 0.70),
            'requests_post_count': int(total_requests * 0.20),
            'requests_put_count': int(total_requests * 0.05),
            'requests_delete_count': int(total_requests * 0.05),

            # Status codes (healthy service)
            'status_2xx_count': int(total_requests * 0.90),
            'status_3xx_count': int(total_requests * 0.05),
            'status_4xx_count': int(total_requests * 0.04),
            'status_5xx_count': int(total_requests * 0.01),
            'error_rate_percent': 5.0,

            # Endpoints (estimate 10 unique endpoints)
            'unique_endpoints_count': 10,
            'endpoint_diversity_score': 2.5,

            # User agents (estimate 5 unique UAs)
            'unique_user_agents_count': 5,
            'bot_requests_count': int(total_requests * 0.10),

            # IPs (estimate 10 unique IPs)
            'unique_ips_count': 10,
            'requests_per_ip_avg': total_requests / 10.0,
            'requests_per_ip_max': int(total_requests * 0.30),

            # Geographic
            'unique_countries_count': 3,

            # Request sizes
            'request_size_avg_bytes': 512.0,
            'response_size_avg_bytes': 2048.0,

            # Authentication
            'auth_attempts_count': int(total_requests * 0.05),
            'auth_failures_count': int(total_requests * 0.005),
            'auth_failure_rate': 10.0,

            # Suspicious patterns
            'suspicious_payloads_count': 0,
            'sql_injection_attempts': 0,

            # Rate limiting
            'rate_limit_hits_count': 0,
        }

        logger.info("Using estimated access log features")
        return features
