# Feature Engineering Specification
# ML-Based Security Anomaly Detection for DevOps

**Version:** 1.0
**Last Updated:** December 2025

---

## Overview

This document provides detailed specifications for all features to be engineered from raw DevOps event data. Features are organized by category and include calculation methods, expected ranges, and relevance to specific attack types.

---

## Feature Categories

1. [Temporal Features](#1-temporal-features)
2. [User Behavioral Features](#2-user-behavioral-features)
3. [Pipeline & Build Features](#3-pipeline--build-features)
4. [Infrastructure Features](#4-infrastructure-features)
5. [Code & Repository Features](#5-code--repository-features)
6. [Network & Access Features](#6-network--access-features)
7. [Security Tool Features](#7-security-tool-features)
8. [Aggregated Statistical Features](#8-aggregated-statistical-features)
9. [Sequential & Time-Series Features](#9-sequential--time-series-features)
10. [Entity Relationship Features](#10-entity-relationship-features)

---

## 1. Temporal Features

Time-based features that capture when events occur and their temporal patterns.

### 1.1 Basic Time Features

| Feature Name | Description | Calculation | Data Type | Example Values | Relevance |
|-------------|-------------|-------------|-----------|----------------|-----------|
| `hour_of_day` | Hour when event occurred (0-23) | Extract from timestamp | int | 0, 13, 23 | Detect off-hours activity |
| `day_of_week` | Day of week (0=Mon, 6=Sun) | Extract from timestamp | int | 0, 3, 6 | Detect weekend anomalies |
| `is_business_hours` | Event during business hours (9-17 local) | Boolean check | bool | 0, 1 | Flag unusual timing |
| `is_weekend` | Event on Saturday/Sunday | day_of_week >= 5 | bool | 0, 1 | Weekend activity flag |
| `month_of_year` | Month (1-12) | Extract from timestamp | int | 1, 6, 12 | Seasonal patterns |
| `week_of_year` | Week number (1-52) | Extract from timestamp | int | 1, 26, 52 | Trend analysis |

### 1.2 Relative Time Features

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `time_since_last_event_sec` | Seconds since user's last event | current_time - last_event_time | float | 0-∞ | Detect burst activity |
| `time_since_last_login_hours` | Hours since last login | (current_time - last_login) / 3600 | float | 0-∞ | Session anomalies |
| `time_since_last_commit_hours` | Hours since last code commit | (current_time - last_commit) / 3600 | float | 0-∞ | Dormant account reactivation |
| `time_since_last_deployment_hours` | Hours since last deployment | (current_time - last_deploy) / 3600 | float | 0-∞ | Deployment frequency |
| `time_to_next_event_sec` | Seconds until next event (requires look-ahead) | next_event_time - current_time | float | 0-∞ | Event clustering |

### 1.3 Duration Features

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `session_duration_minutes` | Length of active session | logout_time - login_time | float | 0-∞ | Unusually long sessions |
| `build_duration_seconds` | Time for build to complete | build_end - build_start | float | 0-∞ | Cryptomining detection |
| `deployment_duration_seconds` | Time for deployment | deploy_end - deploy_start | float | 0-∞ | Slow deployments |

### 1.4 Temporal Deviation Features

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `hour_deviation_from_user_avg` | Difference from user's typical hour | abs(current_hour - user_avg_hour) | float | 0-12 | Compromised account |
| `day_deviation_from_user_pattern` | Deviation from user's day pattern | Custom score | float | 0-1 | Account compromise |
| `is_first_activity_this_hour` | First event in this hour for user | Boolean | bool | 0, 1 | Unusual timing |
| `is_unusual_hour_for_user` | Outside user's typical hours (±2 std) | z-score > 2 | bool | 0, 1 | Temporal anomaly |

---

## 2. User Behavioral Features

Features capturing user actions, patterns, and deviations from normal behavior.

### 2.1 Activity Volume Features

| Feature Name | Description | Calculation | Window | Data Type | Relevance |
|-------------|-------------|-------------|--------|-----------|-----------|
| `events_last_1h` | Count of events in last hour | COUNT(*) | 1 hour | int | Burst detection |
| `events_last_24h` | Count of events in last day | COUNT(*) | 24 hours | int | Daily activity |
| `events_last_7d` | Count of events in last week | COUNT(*) | 7 days | int | Weekly baseline |
| `commits_last_24h` | Number of commits | COUNT(commits) | 24 hours | int | Code activity |
| `repos_accessed_last_24h` | Unique repos accessed | COUNT(DISTINCT repo) | 24 hours | int | Reconnaissance |
| `files_modified_last_24h` | Number of files changed | SUM(files_changed) | 24 hours | int | Broad changes |
| `login_attempts_last_1h` | Login attempts | COUNT(login_events) | 1 hour | int | Brute force |
| `failed_login_attempts_last_1h` | Failed logins | COUNT(failed_logins) | 1 hour | int | Credential stuffing |

### 2.2 Access Pattern Features

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `repo_first_time_access` | First time user accessed this repo | Historical check | bool | 0, 1 | Lateral movement |
| `unusual_repo_for_user` | Repo outside user's normal scope | Baseline comparison | bool | 0, 1 | Unauthorized access |
| `file_first_time_modify` | First time editing this file | Historical check | bool | 0, 1 | Suspicious modification |
| `access_to_sensitive_files` | Accessing secrets, configs, env files | Pattern match | bool | 0, 1 | Credential theft |
| `privileged_action_count_24h` | Admin actions in 24h | COUNT(admin_actions) | int | 0-∞ | Privilege abuse |

### 2.3 User Baseline Deviation

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `activity_zscore_1h` | Z-score of events vs baseline | (current - mean) / std | float | -∞ to ∞ | Anomaly detection |
| `activity_zscore_24h` | Daily activity z-score | (current - mean) / std | float | -∞ to ∞ | Volume anomaly |
| `repos_accessed_zscore` | Repo access z-score | (current - mean) / std | float | -∞ to ∞ | Unusual access pattern |
| `commit_size_zscore` | Commit size vs user baseline | (size - mean) / std | float | -∞ to ∞ | Large commits |
| `work_hours_match_baseline` | Within user's typical hours | Boolean | bool | 0, 1 | Timing check |

### 2.4 Peer Group Comparison

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `activity_vs_team_avg` | User activity / team average | user_count / team_avg | float | 0-∞ | Outlier detection |
| `repos_accessed_vs_team` | Repos accessed vs team norm | user_repos / team_avg_repos | float | 0-∞ | Excessive access |
| `privileged_actions_vs_peers` | Admin actions vs peers | user_admin / peer_avg | float | 0-∞ | Privilege abuse |

---

## 3. Pipeline & Build Features

Features related to CI/CD pipelines, builds, and deployments.

### 3.1 Build Characteristics

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `build_duration_seconds` | Time to complete build | end_time - start_time | float | 0-∞ | Cryptomining |
| `build_duration_zscore` | Duration vs historical mean | (dur - mean) / std | float | -∞ to ∞ | Anomalous builds |
| `build_success_rate_7d` | % successful builds (7d) | success / total | float | 0-1 | Quality degradation |
| `build_triggered_by` | Who/what triggered build | Categorical | string | user, schedule, webhook | Unusual trigger |
| `build_steps_count` | Number of steps in pipeline | COUNT(steps) | int | 0-∞ | Step injection |
| `build_steps_changed` | Steps different from last run | Boolean | bool | 0, 1 | Pipeline modification |
| `new_step_added` | New step in pipeline | Comparison check | bool | 0, 1 | Backdoor detection |
| `step_order_changed` | Steps reordered | Sequence check | bool | 0, 1 | Pipeline tampering |

### 3.2 Build Resource Usage

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `cpu_usage_avg_percent` | Average CPU during build | AVG(cpu_samples) | float | 0-100 | Cryptomining |
| `cpu_usage_max_percent` | Peak CPU during build | MAX(cpu_samples) | float | 0-100 | Resource abuse |
| `memory_usage_avg_mb` | Average memory usage | AVG(mem_samples) | float | 0-∞ | Resource anomaly |
| `memory_usage_max_mb` | Peak memory usage | MAX(mem_samples) | float | 0-∞ | Memory abuse |
| `cpu_zscore` | CPU vs baseline | (cpu - mean) / std | float | -∞ to ∞ | Anomaly |
| `memory_zscore` | Memory vs baseline | (mem - mean) / std | float | -∞ to ∞ | Anomaly |
| `network_egress_mb` | Data sent out during build | SUM(bytes_sent) / 1MB | float | 0-∞ | Exfiltration |
| `network_ingress_mb` | Data received during build | SUM(bytes_recv) / 1MB | float | 0-∞ | Download anomaly |

### 3.3 Build Command Features

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `contains_curl` | Build uses curl command | Regex check | bool | 0, 1 | External download |
| `contains_wget` | Build uses wget command | Regex check | bool | 0, 1 | External download |
| `contains_base64` | Base64 encoding/decoding | Regex check | bool | 0, 1 | Obfuscation |
| `contains_eval` | Uses eval command | Regex check | bool | 0, 1 | Code execution |
| `contains_exec` | Uses exec function | Regex check | bool | 0, 1 | Command execution |
| `background_processes` | Commands with & (background) | Regex check | bool | 0, 1 | Persistence |
| `sleep_command_present` | Sleep command used | Regex check | bool | 0, 1 | Time extension |
| `sleep_duration_total_sec` | Total sleep time | SUM(sleep_args) | int | 0-∞ | Build delay |
| `external_urls_count` | Number of external URLs | COUNT(urls) | int | 0-∞ | External connections |
| `external_urls_new` | URLs not in previous builds | Set difference | int | 0-∞ | New connections |
| `env_variable_dumping` | Dumping env vars (env, printenv) | Regex check | bool | 0, 1 | Secret theft |

### 3.4 Deployment Features

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `deployment_frequency_7d` | Deployments in last 7 days | COUNT(deploys) | int | 0-∞ | Baseline |
| `deployment_target_env` | Target environment | Categorical | string | dev, staging, prod | Environment |
| `deployment_without_approval` | Deployed without approval | Boolean | bool | 0, 1 | Bypass detection |
| `time_from_commit_to_deploy_min` | Minutes from commit to deploy | (deploy_time - commit_time) / 60 | float | 0-∞ | Rush deploy |
| `deployment_rollback` | Deployment rolled back | Boolean | bool | 0, 1 | Failed deploy |

---

## 4. Infrastructure Features

Features related to containers, Kubernetes, and infrastructure events.

### 4.1 Container Features

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `container_image_registry` | Registry hosting image | Extract domain | string | docker.io, gcr.io | Untrusted registry |
| `container_image_official` | Official/verified image | Check official list | bool | 0, 1 | Trust indicator |
| `container_image_age_days` | Days since image published | (now - publish_date) / 86400 | int | 0-∞ | New image risk |
| `container_image_pulls` | Total pulls of this image | From registry API | int | 0-∞ | Popularity |
| `container_privileged` | Runs with privileged flag | Boolean | bool | 0, 1 | Security risk |
| `container_host_network` | Uses host network | Boolean | bool | 0, 1 | Network access |
| `container_host_pid` | Uses host PID namespace | Boolean | bool | 0, 1 | Security risk |
| `container_volume_mounts` | Number of volume mounts | COUNT(volumes) | int | 0-∞ | File access |
| `container_secret_mounts` | Secrets mounted | COUNT(secret_vols) | int | 0-∞ | Secret access |

### 4.2 Kubernetes Features

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `deployment_replicas` | Number of pod replicas | From spec | int | 0-∞ | Resource abuse |
| `replicas_zscore` | Replicas vs namespace avg | (replicas - mean) / std | float | -∞ to ∞ | Anomaly |
| `cpu_request_millicores` | CPU requested (millicores) | From spec | int | 0-∞ | Resource request |
| `memory_request_mb` | Memory requested (MB) | From spec | int | 0-∞ | Resource request |
| `cpu_request_zscore` | CPU request vs avg | (cpu - mean) / std | float | -∞ to ∞ | Excessive |
| `memory_request_zscore` | Memory request vs avg | (mem - mean) / std | float | -∞ to ∞ | Excessive |
| `namespace` | Kubernetes namespace | Categorical | string | default, prod, dev | Scope |
| `service_account` | Service account used | String | string | default, custom | Identity |
| `service_account_default` | Using default SA | Boolean | bool | 0, 1 | Poor practice |

### 4.3 Resource Events

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `containers_created_1h` | Containers created in 1h | COUNT(create_events) | int | 0-∞ | Burst creation |
| `containers_created_zscore` | Creation vs baseline | (count - mean) / std | float | -∞ to ∞ | Anomaly |
| `pod_restart_count` | Number of pod restarts | From pod status | int | 0-∞ | Instability |
| `pod_failed_count_24h` | Failed pods in 24h | COUNT(failed_pods) | int | 0-∞ | Issues |

---

## 5. Code & Repository Features

Features extracted from code commits, repository access, and file changes.

### 5.1 Commit Characteristics

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `commit_additions` | Lines added in commit | From git diff | int | 0-∞ | Commit size |
| `commit_deletions` | Lines deleted in commit | From git diff | int | 0-∞ | Commit size |
| `commit_total_changes` | Total lines changed | additions + deletions | int | 0-∞ | Change magnitude |
| `commit_size_zscore` | Commit size vs user avg | (size - mean) / std | float | -∞ to ∞ | Unusual commit |
| `files_changed_count` | Number of files modified | COUNT(files) | int | 0-∞ | Scope |
| `files_changed_zscore` | Files vs user avg | (files - mean) / std | float | -∞ to ∞ | Broad changes |
| `commit_message_length` | Length of commit message | LEN(message) | int | 0-∞ | Detail level |
| `commit_message_entropy` | Entropy of message | Shannon entropy | float | 0-8 | Randomness |

### 5.2 File Change Features

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `workflow_files_modified` | CI/CD workflow modified | Pattern match | bool | 0, 1 | Pipeline tamper |
| `dockerfile_modified` | Dockerfile changed | Pattern match | bool | 0, 1 | Image tampering |
| `package_json_modified` | Dependencies changed (npm) | Pattern match | bool | 0, 1 | Supply chain |
| `requirements_txt_modified` | Dependencies changed (Python) | Pattern match | bool | 0, 1 | Supply chain |
| `iac_files_modified` | Terraform/CloudFormation changed | Pattern match | bool | 0, 1 | IaC tampering |
| `sensitive_files_accessed` | .env, secrets, keys accessed | Pattern match | bool | 0, 1 | Credential theft |
| `config_files_modified` | Configuration changed | Pattern match | bool | 0, 1 | Config tampering |
| `new_file_extensions` | New file types added | Set difference | bool | 0, 1 | Unusual files |

### 5.3 Code Content Features

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `code_entropy` | Entropy of code changes | Shannon entropy | float | 0-8 | Obfuscation |
| `base64_strings_added` | Base64 strings in diff | Regex count | int | 0-∞ | Encoding |
| `url_count_in_diff` | URLs added to code | URL regex count | int | 0-∞ | External connections |
| `external_url_count` | Non-company URLs | Domain filter | int | 0-∞ | Suspicious URLs |
| `ip_addresses_in_diff` | Hardcoded IPs added | IP regex count | int | 0-∞ | Hardcoded endpoints |
| `suspicious_keywords` | exec, eval, shell, etc. | Keyword count | int | 0-∞ | Dangerous functions |
| `obfuscated_code_score` | Obfuscation heuristic | Custom score | float | 0-1 | Code hiding |

### 5.4 Repository Access Features

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `repos_cloned_1h` | Repos cloned in 1 hour | COUNT(clones) | int | 0-∞ | Mass cloning |
| `repos_cloned_zscore` | Clone count vs baseline | (count - mean) / std | float | -∞ to ∞ | Anomaly |
| `clone_data_size_mb` | Total data cloned (MB) | SUM(repo_sizes) | float | 0-∞ | Exfiltration |
| `first_access_to_repo` | First time accessing repo | Historical check | bool | 0, 1 | Lateral movement |
| `repo_access_pattern` | Sequential vs random | Custom score | float | 0-1 | Systematic access |

---

## 6. Network & Access Features

Features related to geographic location, IP addresses, and access patterns.

### 6.1 Geographic Features

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `source_country` | Country of origin | GeoIP lookup | string | US, CN, RO | Location |
| `source_city` | City of origin | GeoIP lookup | string | New York, Beijing | Location |
| `source_latitude` | Latitude coordinate | GeoIP lookup | float | -90 to 90 | Precise location |
| `source_longitude` | Longitude coordinate | GeoIP lookup | float | -180 to 180 | Precise location |
| `country_different_from_usual` | Different country | Comparison | bool | 0, 1 | Geographic anomaly |
| `distance_from_last_login_km` | Distance between logins | Haversine formula | float | 0-∞ | Impossible travel |
| `impossible_travel` | Distance/time > max speed | distance/time > 1000 km/h | bool | 0, 1 | Account compromise |
| `country_risk_score` | Country risk rating | External data | float | 0-1 | Threat intel |

### 6.2 IP Address Features

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `source_ip` | IP address | From logs | string | IPv4/IPv6 | Identity |
| `ip_first_seen` | First time seeing this IP | Historical check | bool | 0, 1 | New IP |
| `ip_on_blocklist` | IP on threat blocklist | Threat intel lookup | bool | 0, 1 | Known bad |
| `ip_is_vpn` | IP is VPN/proxy | Service lookup | bool | 0, 1 | Anonymization |
| `ip_is_tor` | IP is Tor exit node | Tor list check | bool | 0, 1 | Anonymization |
| `ip_is_datacenter` | IP from datacenter/cloud | ASN lookup | bool | 0, 1 | Non-residential |
| `asn` | Autonomous System Number | IP lookup | int | 0-∞ | Network owner |
| `ip_reputation_score` | IP reputation | Threat intel | float | 0-1 | Trust score |

### 6.3 User Agent Features

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `user_agent` | Browser/client string | From headers | string | Various | Client type |
| `user_agent_is_browser` | Legitimate browser | Parse check | bool | 0, 1 | Human vs bot |
| `user_agent_is_bot` | Automated tool | Pattern match | bool | 0, 1 | Automation |
| `user_agent_changed` | Different from usual | Comparison | bool | 0, 1 | Account compromise |
| `user_agent_entropy` | Randomness of UA string | Shannon entropy | float | 0-8 | Custom/spoofed |

---

## 7. Security Tool Features

Features derived from security scanning tools (SAST, DAST, dependency scanners, etc.).

### 7.1 Static Analysis (SAST)

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `sast_findings_critical` | Critical severity findings | COUNT(findings) | int | 0-∞ | Code quality |
| `sast_findings_high` | High severity findings | COUNT(findings) | int | 0-∞ | Code quality |
| `sast_findings_medium` | Medium severity findings | COUNT(findings) | int | 0-∞ | Code quality |
| `sast_findings_total` | Total SAST findings | SUM(findings) | int | 0-∞ | Overall quality |
| `sast_findings_delta` | Change from last scan | current - previous | int | -∞ to ∞ | Trend |
| `sast_findings_delta_zscore` | Delta vs historical | (delta - mean) / std | float | -∞ to ∞ | Anomaly |
| `sast_new_cwe_types` | New vulnerability types | Set difference | int | 0-∞ | New issues |

### 7.2 Dependency Scanning

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `dependency_vulns_critical` | Critical CVEs in deps | COUNT(vulns) | int | 0-∞ | Supply chain risk |
| `dependency_vulns_high` | High CVEs in deps | COUNT(vulns) | int | 0-∞ | Supply chain risk |
| `dependency_vulns_total` | Total dependency vulns | SUM(vulns) | int | 0-∞ | Overall risk |
| `new_dependencies_added` | New packages added | Set difference | int | 0-∞ | Supply chain |
| `dependencies_removed` | Packages removed | Set difference | int | 0-∞ | Cleanup |
| `dependency_version_downgrade` | Downgraded package version | Version comparison | bool | 0, 1 | Unusual |
| `dependency_from_unusual_registry` | Non-standard registry | Domain check | bool | 0, 1 | Supply chain attack |
| `typosquatting_score` | Name similarity to popular package | Edit distance | float | 0-1 | Typosquatting |
| `dependency_age_days` | Days since package published | From registry | int | 0-∞ | New package risk |
| `dependency_download_count` | Weekly downloads | From registry | int | 0-∞ | Popularity |

### 7.3 Container Scanning

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `container_scan_critical` | Critical image vulnerabilities | COUNT(vulns) | int | 0-∞ | Image security |
| `container_scan_high` | High image vulnerabilities | COUNT(vulns) | int | 0-∞ | Image security |
| `container_malware_detected` | Malware found in image | Scanner result | bool | 0, 1 | Compromised image |
| `container_secrets_found` | Secrets in image layers | Scanner result | int | 0-∞ | Exposed secrets |
| `container_base_image_changed` | Different base image | Comparison | bool | 0, 1 | Image tampering |

### 7.4 Secret Scanning

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `secrets_detected` | Secrets found in code | COUNT(secrets) | int | 0-∞ | Leaked credentials |
| `secret_types` | Types of secrets (API key, password) | Categories | string[] | Various | Secret diversity |
| `secrets_in_commit` | Secrets in current commit | Boolean | bool | 0, 1 | Credential leak |
| `secrets_entropy` | High-entropy strings (potential secrets) | Entropy threshold | int | 0-∞ | Hidden secrets |

---

## 8. Aggregated Statistical Features

Rolling window statistics and aggregations over time periods.

### 8.1 Rolling Window Features (1 hour)

| Feature Name | Description | Calculation | Window | Data Type |
|-------------|-------------|-------------|--------|-----------|
| `events_1h_mean` | Mean events per hour (last 7d) | AVG(hourly_counts) | 7 days | float |
| `events_1h_std` | Std dev of hourly events | STDDEV(hourly_counts) | 7 days | float |
| `events_1h_zscore` | Z-score of current hour | (current - mean) / std | Real-time | float |
| `events_1h_percentile_95` | 95th percentile hourly events | PERCENTILE(hourly_counts, 95) | 7 days | float |
| `events_1h_above_p95` | Current hour > 95th percentile | Boolean | Real-time | bool |

### 8.2 Rolling Window Features (24 hours)

| Feature Name | Description | Calculation | Window | Data Type |
|-------------|-------------|-------------|--------|-----------|
| `events_24h_mean` | Mean daily events | AVG(daily_counts) | 30 days | float |
| `events_24h_std` | Std dev of daily events | STDDEV(daily_counts) | 30 days | float |
| `events_24h_zscore` | Z-score of current day | (current - mean) / std | Real-time | float |
| `commits_24h_mean` | Mean daily commits | AVG(daily_commits) | 30 days | float |
| `commits_24h_zscore` | Commit count z-score | (current - mean) / std | Real-time | float |
| `repos_accessed_24h_mean` | Mean daily repos | AVG(daily_repos) | 30 days | float |
| `repos_accessed_24h_zscore` | Repo access z-score | (current - mean) / std | Real-time | float |

### 8.3 Trend Features

| Feature Name | Description | Calculation | Window | Data Type |
|-------------|-------------|-------------|--------|-----------|
| `events_trend_7d` | Event trend over 7 days | Linear regression slope | 7 days | float |
| `commits_trend_7d` | Commit trend over 7 days | Linear regression slope | 7 days | float |
| `build_duration_trend_7d` | Build time trend | Linear regression slope | 7 days | float |
| `sast_findings_trend_7d` | SAST finding trend | Linear regression slope | 7 days | float |

### 8.4 Rate Features

| Feature Name | Description | Calculation | Window | Data Type |
|-------------|-------------|-------------|--------|-----------|
| `event_rate_events_per_minute` | Events per minute | COUNT(*) / minutes | Real-time | float |
| `commit_rate_per_hour` | Commits per hour | COUNT(commits) / hours | 1 hour | float |
| `api_call_rate_per_second` | API calls per second | COUNT(api_calls) / seconds | 1 minute | float |
| `login_rate_per_minute` | Logins per minute | COUNT(logins) / minutes | 1 hour | float |

---

## 9. Sequential & Time-Series Features

Features that capture sequences, patterns, and temporal dependencies.

### 9.1 Sequence Features

| Feature Name | Description | Calculation | Data Type | Range | Relevance |
|-------------|-------------|-------------|-----------|-------|-----------|
| `event_sequence` | Sequence of event types | Array of events | string[] | Various | Pattern matching |
| `sequence_deviation` | Deviation from typical sequence | Edit distance | int | 0-∞ | Unusual flow |
| `repeated_event_count` | Same event repeated | COUNT(consecutive) | int | 0-∞ | Automated behavior |
| `action_variety_1h` | Unique actions in hour | COUNT(DISTINCT actions) | int | 0-∞ | Diversity |
| `markov_transition_prob` | Probability of this transition | P(event_t | event_t-1) | float | 0-1 | Unusual transition |

### 9.2 Lag Features

| Feature Name | Description | Calculation | Data Type | Range |
|-------------|-------------|-------------|-----------|-------|
| `events_1h_lag1` | Events in previous hour | LAG(events, 1) | int | 0-∞ |
| `events_1h_lag24` | Events 24 hours ago | LAG(events, 24) | int | 0-∞ |
| `events_1h_lag168` | Events 1 week ago (same hour) | LAG(events, 168) | int | 0-∞ |
| `build_duration_lag1` | Previous build duration | LAG(duration, 1) | float | 0-∞ |
| `build_duration_change` | Change from last build | current - lag1 | float | -∞ to ∞ |

### 9.3 Seasonal Features

| Feature Name | Description | Calculation | Data Type | Range |
|-------------|-------------|-------------|-----------|-------|
| `hourly_seasonality` | Typical pattern for this hour | Historical avg | float | 0-∞ |
| `daily_seasonality` | Typical pattern for this day | Historical avg | float | 0-∞ |
| `weekly_seasonality` | Typical pattern for this weekday | Historical avg | float | 0-∞ |
| `seasonal_deviation` | Deviation from seasonal pattern | (current - seasonal) / std | float | -∞ to ∞ |

---

## 10. Entity Relationship Features

Features based on relationships between entities (users, repos, resources).

### 10.1 User-Repo Features

| Feature Name | Description | Calculation | Data Type | Range |
|-------------|-------------|-------------|-----------|-------|
| `user_repo_access_frequency` | How often user accesses repo | Historical count | int | 0-∞ |
| `user_repo_first_access` | First time accessing | Boolean | bool | 0, 1 |
| `user_repo_last_access_days` | Days since last access | (now - last_access) / 86400 | int | 0-∞ |
| `user_repo_permission_level` | User's permission on repo | Categorical | string | read, write, admin |
| `user_repo_permission_recent_change` | Permission changed recently | Boolean | bool | 0, 1 |

### 10.2 User-User Features

| Feature Name | Description | Calculation | Data Type | Range |
|-------------|-------------|-------------|-----------|-------|
| `user_team_membership` | Teams user belongs to | Array | string[] | Various |
| `user_collaborators` | Frequent collaborators | Set of users | string[] | Various |
| `user_isolation_score` | How isolated user is | Graph metric | float | 0-1 |
| `unusual_collaboration` | Collaborating with unusual users | Boolean | bool | 0, 1 |

### 10.3 Account Type Features

| Feature Name | Description | Calculation | Data Type | Values |
|-------------|-------------|-------------|-----------|--------|
| `account_type` | Type of account | Classification | string | human, service, bot |
| `account_age_days` | Days since account created | (now - created) / 86400 | int | 0-∞ |
| `account_recently_created` | Created in last 30 days | age < 30 | bool | 0, 1 |
| `service_account_used_by_human` | Service account with human patterns | Heuristic | bool | 0, 1 |

---

## Feature Engineering Pipeline

### Step 1: Raw Data Ingestion
- Ingest events from all data sources
- Parse timestamps to UTC
- Extract basic fields (user, action, resource)

### Step 2: Entity Extraction
- Identify entities (users, repos, containers, etc.)
- Create entity IDs
- Link events to entities

### Step 3: Temporal Feature Calculation
- Extract time-based features
- Calculate relative times
- Compute durations

### Step 4: Behavioral Feature Calculation
- Aggregate by user, time windows
- Calculate baselines from historical data
- Compute deviations (z-scores)

### Step 5: Content Feature Extraction
- Parse code diffs, configs, logs
- Extract patterns (URLs, IPs, commands)
- Calculate entropy, complexity scores

### Step 6: External Enrichment
- GeoIP lookups
- Threat intelligence lookups
- Dependency metadata from registries

### Step 7: Statistical Aggregation
- Rolling window statistics
- Trend calculations
- Percentiles and distributions

### Step 8: Feature Normalization
- Scale numeric features (StandardScaler, MinMaxScaler)
- Encode categorical features (OneHotEncoder, LabelEncoder)
- Handle missing values (imputation)

### Step 9: Feature Selection
- Correlation analysis
- Feature importance from models
- Domain expert review

### Step 10: Feature Storage
- Store in feature store for model training
- Version features
- Document feature definitions

---

## Feature Selection Criteria

### Priority 1: High-Value Features (Must Include)
- Z-scores for behavioral deviations
- Geographic features (location, impossible travel)
- Temporal features (hour, business hours)
- Resource usage (CPU, memory, network)
- Access patterns (first-time access, unusual repos)
- Security tool outputs (SAST, dependencies, secrets)

### Priority 2: Moderate-Value Features (Include if possible)
- Sequence and transition features
- Peer comparison features
- Code content features
- Trend features
- Container/K8s features

### Priority 3: Experimental Features (Test and evaluate)
- Markov chain probabilities
- Graph-based features
- Deep embedding features
- Interaction features (feature combinations)

---

## Feature Documentation Template

For each feature, document:

```
Feature Name: [name]
Description: [what it measures]
Calculation: [formula or method]
Data Type: [int, float, bool, string, etc.]
Range: [min-max values]
Missingness: [expected % of nulls]
Relevance: [which attacks it helps detect]
Priority: [1, 2, 3]
Dependencies: [other features or data required]
Computational Cost: [low, medium, high]
```

---

## Implementation Notes

### Performance Considerations
- Pre-compute baseline statistics offline (daily batch job)
- Use caching for repeated calculations
- Implement incremental feature updates for streaming
- Consider feature computation latency for real-time detection

### Data Quality
- Monitor feature distributions over time
- Alert on feature drift
- Validate features against known attacks
- Handle missing data gracefully

### Feature Store
- Use MLflow, Feast, or similar feature store
- Version all features
- Track feature lineage
- Enable feature reuse across models

---

## Summary Statistics

| Category | Total Features | Priority 1 | Priority 2 | Priority 3 |
|----------|---------------|------------|------------|------------|
| Temporal | 18 | 8 | 6 | 4 |
| User Behavioral | 26 | 12 | 10 | 4 |
| Pipeline & Build | 32 | 14 | 12 | 6 |
| Infrastructure | 24 | 10 | 10 | 4 |
| Code & Repository | 28 | 12 | 11 | 5 |
| Network & Access | 22 | 10 | 8 | 4 |
| Security Tools | 20 | 15 | 5 | 0 |
| Statistical | 16 | 8 | 6 | 2 |
| Sequential | 12 | 4 | 6 | 2 |
| Entity Relationship | 12 | 5 | 5 | 2 |
| **TOTAL** | **210** | **98** | **79** | **33** |

**Recommended Feature Set Size:** 80-120 features (Priority 1 + selected Priority 2)

---

**Next Steps:**
1. Implement feature extraction pipeline
2. Validate features on sample data
3. Calculate baseline statistics from normal data
4. Test features on attack scenarios
5. Perform feature selection experiments
6. Document final feature set
