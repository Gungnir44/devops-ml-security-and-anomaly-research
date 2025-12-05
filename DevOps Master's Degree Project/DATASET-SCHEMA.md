# Dataset Schema Specification
# ML-Based Security Anomaly Detection for DevOps

**Version:** 1.0
**Last Updated:** December 2025

---

## Overview

This document defines the complete dataset schema for storing raw events, processed features, and labels for training the ML-based security anomaly detection system.

---

## Table of Contents

1. [Data Architecture](#data-architecture)
2. [Raw Event Tables](#raw-event-tables)
3. [Entity Tables](#entity-tables)
4. [Feature Tables](#feature-tables)
5. [Label Tables](#label-tables)
6. [Data Formats](#data-formats)
7. [Storage Recommendations](#storage-recommendations)

---

## Data Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Raw Event Layer                       │
│  (Events as they occur - time-series data)              │
├─────────────────────────────────────────────────────────┤
│ - ci_cd_events          - security_scan_events          │
│ - infrastructure_events - code_commit_events            │
│ - access_events         - network_events                │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                    Entity Layer                          │
│  (Master data for users, repos, containers, etc.)       │
├─────────────────────────────────────────────────────────┤
│ - users                 - repositories                   │
│ - containers            - kubernetes_resources           │
│ - service_accounts      - teams                         │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                   Feature Layer                          │
│  (Engineered features for ML models)                    │
├─────────────────────────────────────────────────────────┤
│ - user_features         - pipeline_features             │
│ - temporal_features     - security_features             │
│ - behavioral_features   - aggregated_features           │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                    Label Layer                           │
│  (Attack labels and metadata)                           │
├─────────────────────────────────────────────────────────┤
│ - attack_labels         - attack_metadata               │
│ - baseline_periods      - validation_sets               │
└─────────────────────────────────────────────────────────┘
```

---

## Raw Event Tables

### 1. ci_cd_events

**Purpose:** Captures all CI/CD pipeline events (builds, deployments, workflow runs)

**Schema:**

| Column Name | Data Type | Nullable | Description | Example |
|-------------|-----------|----------|-------------|---------|
| event_id | STRING | NO | Unique event identifier | `evt_abc123` |
| timestamp | TIMESTAMP | NO | Event occurrence time (UTC) | `2025-12-02T10:30:45Z` |
| event_type | STRING | NO | Type of event | `build_started`, `build_completed`, `deployment` |
| platform | STRING | NO | CI/CD platform | `github_actions`, `gitlab_ci`, `jenkins` |
| workflow_id | STRING | YES | Workflow/pipeline identifier | `workflow_123` |
| workflow_name | STRING | YES | Human-readable workflow name | `CI Build and Test` |
| job_id | STRING | YES | Specific job within workflow | `job_456` |
| job_name | STRING | YES | Job name | `build` |
| repository | STRING | NO | Repository name | `org/repo-name` |
| branch | STRING | YES | Git branch | `main`, `feature/new-feature` |
| commit_sha | STRING | YES | Git commit hash | `abc123def456...` |
| triggered_by | STRING | YES | Who/what triggered | `user:john_doe`, `schedule`, `webhook` |
| triggering_actor | STRING | YES | Actor ID | `user_123` |
| status | STRING | YES | Event status | `success`, `failure`, `in_progress` |
| duration_seconds | FLOAT | YES | Duration (for completed events) | `245.6` |
| build_steps | JSON | YES | Array of build steps executed | `[{"name": "build", "status": "success"}]` |
| environment_variables | JSON | YES | Env vars (sanitized, no secrets) | `{"NODE_ENV": "production"}` |
| commands_executed | TEXT | YES | Commands run during build | `npm install && npm build` |
| artifacts_published | JSON | YES | Artifacts created | `[{"name": "app.tar.gz", "size_mb": 45}]` |
| resource_usage | JSON | YES | CPU, memory, network usage | `{"cpu_avg": 45.2, "mem_max_mb": 2048}` |
| network_connections | JSON | YES | External connections made | `[{"domain": "npmjs.org", "port": 443}]` |
| exit_code | INT | YES | Process exit code | `0`, `1` |
| error_message | TEXT | YES | Error details if failed | `Build failed: ...` |
| metadata | JSON | YES | Additional platform-specific data | `{}` |

**Indexes:**
- PRIMARY KEY: `event_id`
- INDEX: `timestamp`
- INDEX: `repository, timestamp`
- INDEX: `triggering_actor, timestamp`

**Estimated Size:** ~10KB per event, ~100,000 events = ~1GB

---

### 2. infrastructure_events

**Purpose:** Container, Kubernetes, and infrastructure-related events

**Schema:**

| Column Name | Data Type | Nullable | Description | Example |
|-------------|-----------|----------|-------------|---------|
| event_id | STRING | NO | Unique event identifier | `inf_xyz789` |
| timestamp | TIMESTAMP | NO | Event time (UTC) | `2025-12-02T10:30:45Z` |
| event_type | STRING | NO | Event type | `pod_created`, `container_started`, `deployment_scaled` |
| resource_type | STRING | NO | K8s resource type | `pod`, `deployment`, `service`, `container` |
| resource_name | STRING | NO | Resource name | `api-server-abc123` |
| namespace | STRING | YES | Kubernetes namespace | `production`, `dev` |
| cluster | STRING | YES | Cluster name | `prod-cluster-1` |
| action | STRING | NO | Action performed | `create`, `update`, `delete` |
| actor | STRING | YES | Who performed action | `user:admin`, `serviceaccount:deployer` |
| container_image | STRING | YES | Container image used | `nginx:1.21-alpine` |
| image_registry | STRING | YES | Registry URL | `docker.io`, `gcr.io/company` |
| image_digest | STRING | YES | Image SHA256 digest | `sha256:abc123...` |
| container_config | JSON | YES | Container configuration | `{"privileged": false, "cpu": "500m"}` |
| volume_mounts | JSON | YES | Mounted volumes | `[{"name": "data", "path": "/data"}]` |
| replicas | INT | YES | Number of replicas | `3` |
| cpu_request_millicores | INT | YES | CPU requested | `500` |
| memory_request_mb | INT | YES | Memory requested | `512` |
| cpu_usage_millicores | FLOAT | YES | Actual CPU usage | `450.5` |
| memory_usage_mb | FLOAT | YES | Actual memory usage | `480.2` |
| network_ingress_mb | FLOAT | YES | Data received | `125.5` |
| network_egress_mb | FLOAT | YES | Data sent | `89.3` |
| status | STRING | YES | Resource status | `running`, `failed`, `pending` |
| metadata | JSON | YES | Additional data | `{}` |

**Indexes:**
- PRIMARY KEY: `event_id`
- INDEX: `timestamp`
- INDEX: `namespace, timestamp`
- INDEX: `actor, timestamp`
- INDEX: `container_image`

**Estimated Size:** ~8KB per event, ~50,000 events = ~400MB

---

### 3. code_commit_events

**Purpose:** Git commits, pull requests, code changes

**Schema:**

| Column Name | Data Type | Nullable | Description | Example |
|-------------|-----------|----------|-------------|---------|
| event_id | STRING | NO | Unique event identifier | `commit_abc123` |
| timestamp | TIMESTAMP | NO | Commit timestamp (UTC) | `2025-12-02T10:30:45Z` |
| event_type | STRING | NO | Event type | `commit`, `pull_request`, `merge`, `push` |
| repository | STRING | NO | Repository name | `org/repo-name` |
| commit_sha | STRING | YES | Commit hash | `abc123def456...` |
| author | STRING | NO | Commit author | `user_123` |
| author_email | STRING | YES | Author email | `john@example.com` |
| committer | STRING | YES | Committer (if different) | `user_456` |
| branch | STRING | YES | Target branch | `main`, `develop` |
| commit_message | TEXT | YES | Commit message | `Fix authentication bug` |
| additions | INT | YES | Lines added | `45` |
| deletions | INT | YES | Lines deleted | `12` |
| files_changed | INT | YES | Number of files | `5` |
| files_list | JSON | YES | List of changed files | `["src/auth.js", "tests/auth.test.js"]` |
| diff_content | TEXT | YES | Git diff (sanitized) | `diff --git a/... ` |
| pull_request_id | STRING | YES | Associated PR ID | `pr_789` |
| pr_status | STRING | YES | PR status | `open`, `merged`, `closed` |
| pr_approvers | JSON | YES | Who approved PR | `["user_111", "user_222"]` |
| pr_reviewers | JSON | YES | Who reviewed PR | `["user_333"]` |
| merge_method | STRING | YES | How PR was merged | `merge`, `squash`, `rebase` |
| workflow_files_modified | BOOLEAN | YES | CI/CD files changed | `true`, `false` |
| dependency_files_modified | BOOLEAN | YES | package.json, requirements.txt, etc. | `true`, `false` |
| iac_files_modified | BOOLEAN | YES | Terraform, CloudFormation, etc. | `true`, `false` |
| metadata | JSON | YES | Additional data | `{}` |

**Indexes:**
- PRIMARY KEY: `event_id`
- INDEX: `timestamp`
- INDEX: `repository, timestamp`
- INDEX: `author, timestamp`
- INDEX: `commit_sha`

**Estimated Size:** ~15KB per event (with diff), ~30,000 commits = ~450MB

---

### 4. access_events

**Purpose:** Authentication, authorization, and access events

**Schema:**

| Column Name | Data Type | Nullable | Description | Example |
|-------------|-----------|----------|-------------|---------|
| event_id | STRING | NO | Unique event identifier | `access_xyz456` |
| timestamp | TIMESTAMP | NO | Event time (UTC) | `2025-12-02T10:30:45Z` |
| event_type | STRING | NO | Event type | `login`, `logout`, `api_call`, `secret_access` |
| user_id | STRING | YES | User identifier | `user_123` |
| account_type | STRING | NO | Account type | `human`, `service`, `bot` |
| action | STRING | NO | Action performed | `read`, `write`, `delete`, `admin` |
| resource_type | STRING | YES | Resource accessed | `repository`, `secret`, `cluster`, `workflow` |
| resource_name | STRING | YES | Specific resource | `org/private-repo` |
| source_ip | STRING | NO | Source IP address | `203.0.113.42` |
| source_country | STRING | YES | Country (GeoIP) | `United States` |
| source_city | STRING | YES | City (GeoIP) | `New York` |
| source_latitude | FLOAT | YES | Latitude | `40.7128` |
| source_longitude | FLOAT | YES | Longitude | `-74.0060` |
| user_agent | STRING | YES | User agent string | `Mozilla/5.0 ...` |
| authentication_method | STRING | YES | Auth method | `password`, `token`, `ssh_key`, `oauth` |
| authentication_status | STRING | NO | Success or failure | `success`, `failure` |
| failure_reason | STRING | YES | Why auth failed | `invalid_password`, `account_locked` |
| mfa_used | BOOLEAN | YES | Multi-factor auth used | `true`, `false` |
| session_id | STRING | YES | Session identifier | `sess_abc123` |
| permission_level | STRING | YES | Permission granted | `read`, `write`, `admin` |
| api_endpoint | STRING | YES | API endpoint accessed | `/api/v1/repos` |
| api_method | STRING | YES | HTTP method | `GET`, `POST`, `DELETE` |
| response_code | INT | YES | HTTP response code | `200`, `403`, `500` |
| metadata | JSON | YES | Additional data | `{}` |

**Indexes:**
- PRIMARY KEY: `event_id`
- INDEX: `timestamp`
- INDEX: `user_id, timestamp`
- INDEX: `source_ip, timestamp`
- INDEX: `authentication_status, timestamp`

**Estimated Size:** ~5KB per event, ~200,000 events = ~1GB

---

### 5. security_scan_events

**Purpose:** Results from security scanning tools (SAST, DAST, dependency scanning, etc.)

**Schema:**

| Column Name | Data Type | Nullable | Description | Example |
|-------------|-----------|----------|-------------|---------|
| event_id | STRING | NO | Unique event identifier | `scan_def789` |
| timestamp | TIMESTAMP | NO | Scan completion time (UTC) | `2025-12-02T10:30:45Z` |
| scan_type | STRING | NO | Type of scan | `sast`, `dast`, `dependency`, `container`, `secret` |
| tool_name | STRING | NO | Scanner name | `semgrep`, `trivy`, `snyk`, `trufflehog` |
| tool_version | STRING | YES | Tool version | `1.2.3` |
| repository | STRING | YES | Repository scanned | `org/repo-name` |
| commit_sha | STRING | YES | Commit scanned | `abc123def456...` |
| branch | STRING | YES | Branch scanned | `main` |
| container_image | STRING | YES | Image scanned (if container scan) | `nginx:1.21` |
| scan_status | STRING | NO | Scan result | `success`, `failure`, `error` |
| findings_critical | INT | YES | Critical severity | `2` |
| findings_high | INT | YES | High severity | `5` |
| findings_medium | INT | YES | Medium severity | `12` |
| findings_low | INT | YES | Low severity | `23` |
| findings_total | INT | YES | Total findings | `42` |
| findings_detail | JSON | YES | Detailed findings | `[{"cwe": "CWE-89", "severity": "high", ...}]` |
| secrets_found | JSON | YES | Secrets detected | `[{"type": "api_key", "file": "config.js"}]` |
| vulnerabilities | JSON | YES | CVEs found | `[{"cve": "CVE-2021-12345", "package": "lodash"}]` |
| malware_detected | BOOLEAN | YES | Malware found | `true`, `false` |
| scan_duration_seconds | FLOAT | YES | Scan duration | `34.5` |
| metadata | JSON | YES | Additional scan data | `{}` |

**Indexes:**
- PRIMARY KEY: `event_id`
- INDEX: `timestamp`
- INDEX: `repository, timestamp`
- INDEX: `scan_type, timestamp`

**Estimated Size:** ~20KB per event (with findings), ~10,000 scans = ~200MB

---

### 6. network_events

**Purpose:** Network connections, traffic patterns

**Schema:**

| Column Name | Data Type | Nullable | Description | Example |
|-------------|-----------|----------|-------------|---------|
| event_id | STRING | NO | Unique event identifier | `net_ghi012` |
| timestamp | TIMESTAMP | NO | Event time (UTC) | `2025-12-02T10:30:45Z` |
| source_type | STRING | NO | Source type | `build`, `container`, `workflow` |
| source_id | STRING | NO | Source identifier | `build_123` |
| source_ip | STRING | YES | Source IP (internal) | `10.0.1.5` |
| destination_ip | STRING | NO | Destination IP | `93.184.216.34` |
| destination_domain | STRING | YES | Domain name | `example.com` |
| destination_port | INT | NO | Destination port | `443`, `22` |
| protocol | STRING | NO | Network protocol | `TCP`, `UDP`, `ICMP` |
| bytes_sent | BIGINT | YES | Bytes sent | `1024000` |
| bytes_received | BIGINT | YES | Bytes received | `512000` |
| connection_duration_seconds | FLOAT | YES | Connection duration | `12.5` |
| connection_status | STRING | YES | Connection status | `established`, `closed`, `refused` |
| is_external | BOOLEAN | NO | External destination | `true`, `false` |
| domain_category | STRING | YES | Domain category (from threat intel) | `cdn`, `social`, `malware` |
| domain_reputation | FLOAT | YES | Reputation score (0-1) | `0.95` |
| metadata | JSON | YES | Additional data | `{}` |

**Indexes:**
- PRIMARY KEY: `event_id`
- INDEX: `timestamp`
- INDEX: `source_id, timestamp`
- INDEX: `destination_domain, timestamp`
- INDEX: `is_external, timestamp`

**Estimated Size:** ~3KB per event, ~500,000 events = ~1.5GB

---

## Entity Tables

### 7. users

**Purpose:** Master data for all users (human and service accounts)

**Schema:**

| Column Name | Data Type | Nullable | Description | Example |
|-------------|-----------|----------|-------------|---------|
| user_id | STRING | NO | Unique user identifier | `user_123` |
| username | STRING | NO | Username | `john_doe` |
| email | STRING | YES | Email address | `john@example.com` |
| account_type | STRING | NO | Account type | `human`, `service`, `bot` |
| created_at | TIMESTAMP | NO | Account creation date | `2023-01-15T00:00:00Z` |
| role | STRING | YES | Primary role | `developer`, `admin`, `readonly` |
| teams | JSON | YES | Team memberships | `["backend-team", "security-team"]` |
| typical_work_hours_start | INT | YES | Typical start hour (0-23) | `9` |
| typical_work_hours_end | INT | YES | Typical end hour (0-23) | `17` |
| typical_timezone | STRING | YES | User timezone | `America/New_York` |
| typical_locations | JSON | YES | Common locations | `[{"city": "New York", "country": "US"}]` |
| last_login | TIMESTAMP | YES | Last login time | `2025-12-02T09:00:00Z` |
| is_active | BOOLEAN | NO | Account active | `true`, `false` |
| metadata | JSON | YES | Additional data | `{}` |

**Indexes:**
- PRIMARY KEY: `user_id`
- UNIQUE: `username`
- INDEX: `email`
- INDEX: `account_type`

---

### 8. repositories

**Purpose:** Repository metadata

**Schema:**

| Column Name | Data Type | Nullable | Description | Example |
|-------------|-----------|----------|-------------|---------|
| repo_id | STRING | NO | Unique repo identifier | `repo_456` |
| repo_name | STRING | NO | Repository name | `org/my-app` |
| created_at | TIMESTAMP | NO | Repo creation date | `2022-03-10T00:00:00Z` |
| visibility | STRING | NO | Visibility | `public`, `private`, `internal` |
| primary_language | STRING | YES | Main programming language | `JavaScript`, `Python` |
| size_mb | FLOAT | YES | Repository size | `125.5` |
| default_branch | STRING | YES | Default branch | `main` |
| is_archived | BOOLEAN | NO | Archived status | `false` |
| is_fork | BOOLEAN | NO | Is fork | `false` |
| topics | JSON | YES | Repository topics | `["api", "microservice"]` |
| metadata | JSON | YES | Additional data | `{}` |

**Indexes:**
- PRIMARY KEY: `repo_id`
- UNIQUE: `repo_name`
- INDEX: `visibility`

---

## Feature Tables

### 9. event_features

**Purpose:** Engineered features for each event (for training/inference)

**Schema:**

| Column Name | Data Type | Nullable | Description |
|-------------|-----------|----------|-------------|
| event_id | STRING | NO | Links to raw event |
| timestamp | TIMESTAMP | NO | Event timestamp |
| user_id | STRING | YES | User associated with event |
| repository | STRING | YES | Repository |
| label | STRING | YES | Ground truth label |

**Temporal Features (18 columns):**
| hour_of_day | INT | YES | 0-23 |
| day_of_week | INT | YES | 0-6 |
| is_business_hours | BOOLEAN | YES | Business hours flag |
| is_weekend | BOOLEAN | YES | Weekend flag |
| time_since_last_event_sec | FLOAT | YES | Seconds since last event |
| time_since_last_login_hours | FLOAT | YES | Hours since login |
| build_duration_seconds | FLOAT | YES | Build duration |
| hour_deviation_from_user_avg | FLOAT | YES | Temporal anomaly |
| ... (10 more temporal features) |

**Behavioral Features (26 columns):**
| events_last_1h | INT | YES | Event count (1h) |
| events_last_24h | INT | YES | Event count (24h) |
| commits_last_24h | INT | YES | Commit count |
| repos_accessed_last_24h | INT | YES | Repo access count |
| activity_zscore_1h | FLOAT | YES | Activity z-score |
| activity_zscore_24h | FLOAT | YES | Daily z-score |
| repo_first_time_access | BOOLEAN | YES | First access flag |
| unusual_repo_for_user | BOOLEAN | YES | Unusual access |
| ... (18 more behavioral features) |

**Pipeline Features (32 columns):**
| build_duration_zscore | FLOAT | YES | Duration anomaly |
| build_steps_changed | BOOLEAN | YES | Steps modified |
| new_step_added | BOOLEAN | YES | New step flag |
| cpu_usage_avg_percent | FLOAT | YES | CPU usage |
| cpu_zscore | FLOAT | YES | CPU anomaly |
| memory_usage_avg_mb | FLOAT | YES | Memory usage |
| memory_zscore | FLOAT | YES | Memory anomaly |
| contains_curl | BOOLEAN | YES | Curl command present |
| contains_base64 | BOOLEAN | YES | Base64 present |
| external_urls_count | INT | YES | External URL count |
| ... (22 more pipeline features) |

**Infrastructure Features (24 columns):**
| container_privileged | BOOLEAN | YES | Privileged flag |
| deployment_replicas | INT | YES | Replica count |
| replicas_zscore | FLOAT | YES | Replica anomaly |
| cpu_request_millicores | INT | YES | CPU request |
| ... (20 more infra features) |

**Code Features (28 columns):**
| commit_additions | INT | YES | Lines added |
| commit_deletions | INT | YES | Lines deleted |
| commit_size_zscore | FLOAT | YES | Commit size anomaly |
| workflow_files_modified | BOOLEAN | YES | Workflow modified |
| code_entropy | FLOAT | YES | Code entropy |
| ... (23 more code features) |

**Network Features (22 columns):**
| source_country | STRING | YES | Source country |
| country_different_from_usual | BOOLEAN | YES | Geographic anomaly |
| distance_from_last_login_km | FLOAT | YES | Distance traveled |
| impossible_travel | BOOLEAN | YES | Impossible travel flag |
| ip_on_blocklist | BOOLEAN | YES | Blocklist flag |
| ... (17 more network features) |

**Security Features (20 columns):**
| sast_findings_critical | INT | YES | Critical SAST |
| sast_findings_delta | INT | YES | SAST delta |
| dependency_vulns_critical | INT | YES | Dependency vulns |
| typosquatting_score | FLOAT | YES | Typosquatting |
| ... (16 more security features) |

**Statistical Features (16 columns):**
| events_1h_zscore | FLOAT | YES | Hourly z-score |
| events_24h_zscore | FLOAT | YES | Daily z-score |
| commits_24h_zscore | FLOAT | YES | Commit z-score |
| events_trend_7d | FLOAT | YES | Event trend |
| ... (12 more statistical features) |

**Sequential Features (12 columns):**
| sequence_deviation | INT | YES | Sequence anomaly |
| repeated_event_count | INT | YES | Repeated events |
| events_1h_lag1 | INT | YES | Previous hour count |
| ... (9 more sequential features) |

**Entity Features (12 columns):**
| user_repo_first_access | BOOLEAN | YES | First repo access |
| user_repo_permission_level | STRING | YES | Permission level |
| account_age_days | INT | YES | Account age |
| ... (9 more entity features) |

**Total: ~210 feature columns**

**Indexes:**
- PRIMARY KEY: `event_id`
- INDEX: `timestamp`
- INDEX: `user_id, timestamp`
- INDEX: `label`

**Estimated Size:** ~2KB per row (210 features), 150,000 events = ~300MB

---

## Label Tables

### 10. attack_labels

**Purpose:** Ground truth labels for attacks

**Schema:**

| Column Name | Data Type | Nullable | Description | Example |
|-------------|-----------|----------|-------------|---------|
| event_id | STRING | NO | Links to event | `evt_abc123` |
| timestamp | TIMESTAMP | NO | Event time | `2025-12-02T10:30:45Z` |
| is_attack | BOOLEAN | NO | Attack or benign | `true`, `false` |
| attack_category | STRING | YES | Attack category | `compromised_credentials` |
| attack_scenario | STRING | YES | Specific scenario | `scenario_1.1` |
| severity | STRING | YES | Severity level | `critical`, `high`, `medium`, `low` |
| indicators | JSON | YES | Observable indicators | `["geographic_anomaly", "temporal_anomaly"]` |
| attack_stage | STRING | YES | Attack kill chain stage | `initial_access`, `execution`, `exfiltration` |
| mitre_attack_ids | JSON | YES | MITRE ATT&CK IDs | `["T1078", "T1133"]` |
| simulation_params | JSON | YES | Simulation parameters | `{"location": "Romania", "time": "03:00"}` |
| notes | TEXT | YES | Additional notes | `Simulated login from Eastern Europe` |
| labeled_by | STRING | YES | Who labeled | `researcher_1` |
| labeled_at | TIMESTAMP | YES | Labeling time | `2025-12-02T15:00:00Z` |

**Indexes:**
- PRIMARY KEY: `event_id`
- INDEX: `is_attack`
- INDEX: `attack_category`
- INDEX: `severity`
- INDEX: `timestamp`

---

### 11. baseline_periods

**Purpose:** Define periods of "normal" behavior (no attacks)

**Schema:**

| Column Name | Data Type | Nullable | Description | Example |
|-------------|-----------|----------|-------------|---------|
| period_id | STRING | NO | Unique period ID | `baseline_001` |
| start_time | TIMESTAMP | NO | Period start | `2025-11-01T00:00:00Z` |
| end_time | TIMESTAMP | NO | Period end | `2025-11-08T00:00:00Z` |
| description | TEXT | YES | Period description | `Week 1 - Normal operations` |
| event_count | INT | YES | Events in period | `15000` |
| users_active | INT | YES | Active users | `25` |
| repositories_active | INT | YES | Active repos | `12` |
| is_validated | BOOLEAN | NO | Validated as attack-free | `true` |
| validated_by | STRING | YES | Validator | `researcher_1` |
| notes | TEXT | YES | Additional notes | `Standard dev work week` |

**Indexes:**
- PRIMARY KEY: `period_id`
- INDEX: `start_time, end_time`

---

## Data Formats

### Time-Series Data Storage

**Recommendation:** Use a time-series database or columnar format

**Options:**
1. **InfluxDB / TimescaleDB** - Optimized for time-series queries
2. **Apache Parquet** - Columnar format, efficient compression
3. **PostgreSQL with TimescaleDB extension** - SQL + time-series optimization
4. **ClickHouse** - Fast analytical queries

### Feature Store Format

**Recommendation:** Use dedicated feature store or structured format

**Options:**
1. **Feast** - Open-source feature store
2. **MLflow** - Model and feature versioning
3. **Parquet files** - Partitioned by date
4. **HDF5** - Efficient for numeric data

### Label Storage

**Recommendation:** Relational database or JSON files

**Options:**
1. **PostgreSQL / MySQL** - Structured, queryable
2. **JSON files** - Simple, version-controlled
3. **CSV with metadata** - Easy to inspect

---

## Storage Recommendations

### Estimated Storage Requirements

| Data Type | Events/Rows | Size per Row | Total Size | Format |
|-----------|-------------|--------------|------------|---------|
| ci_cd_events | 100,000 | 10 KB | 1 GB | Parquet |
| infrastructure_events | 50,000 | 8 KB | 400 MB | Parquet |
| code_commit_events | 30,000 | 15 KB | 450 MB | Parquet |
| access_events | 200,000 | 5 KB | 1 GB | Parquet |
| security_scan_events | 10,000 | 20 KB | 200 MB | Parquet |
| network_events | 500,000 | 3 KB | 1.5 GB | Parquet |
| event_features | 150,000 | 2 KB | 300 MB | Parquet/HDF5 |
| attack_labels | 10,000 | 1 KB | 10 MB | JSON/CSV |
| **TOTAL** | **~1M events** | | **~5 GB** | |

**Note:** With compression (gzip, snappy), expect 30-50% reduction: **~2.5-3.5 GB**

### Storage Architecture

```
/data
├── /raw_events              # Raw event data
│   ├── /ci_cd
│   │   ├── 2025-11-01.parquet
│   │   ├── 2025-11-02.parquet
│   │   └── ...
│   ├── /infrastructure
│   ├── /code_commits
│   ├── /access
│   ├── /security_scans
│   └── /network
├── /entities                # Entity master data
│   ├── users.parquet
│   ├── repositories.parquet
│   └── ...
├── /features               # Engineered features
│   ├── /train
│   │   ├── features_2025-11.parquet
│   │   └── features_2025-12.parquet
│   ├── /validation
│   └── /test
├── /labels                 # Attack labels
│   ├── attack_labels.json
│   ├── baseline_periods.json
│   └── attack_metadata.json
└── /models                 # Trained models
    ├── /baseline
    ├── /isolation_forest
    ├── /random_forest
    └── /ensemble
```

---

## Data Pipeline Flow

```
1. Event Collection
   ↓
2. Raw Event Storage (Parquet, partitioned by date)
   ↓
3. Entity Extraction & Enrichment (GeoIP, threat intel)
   ↓
4. Feature Engineering (batch or streaming)
   ↓
5. Feature Storage (Feature store or Parquet)
   ↓
6. Label Joining (merge attack labels)
   ↓
7. Train/Validation/Test Split
   ↓
8. Model Training & Evaluation
```

---

## Data Quality Checks

### Raw Event Validation
- [ ] All required fields present
- [ ] Timestamps in valid range (not future)
- [ ] No duplicate event_ids
- [ ] JSON fields parseable
- [ ] Numeric fields in reasonable ranges

### Feature Validation
- [ ] No NaN/Inf values (or handled appropriately)
- [ ] Feature distributions match expected ranges
- [ ] Z-scores calculated correctly
- [ ] Boolean features only contain 0/1
- [ ] Categorical features have valid values

### Label Validation
- [ ] All labeled events have corresponding raw events
- [ ] Attack categories match defined taxonomy
- [ ] Severity levels consistent
- [ ] No overlapping attack periods
- [ ] Baseline periods validated as attack-free

---

## Data Versioning

**Recommendation:** Version all datasets for reproducibility

**Approach:**
1. **DVC (Data Version Control)** - Git-like versioning for data
2. **Git LFS** - Large file storage
3. **Timestamp-based versions** - `dataset_v1_20251202.parquet`
4. **Metadata files** - Document schema version, collection parameters

**Example metadata.json:**
```json
{
  "version": "1.0",
  "created_at": "2025-12-02T10:00:00Z",
  "schema_version": "1.0",
  "event_count": 150000,
  "date_range": {
    "start": "2025-11-01T00:00:00Z",
    "end": "2025-12-01T23:59:59Z"
  },
  "attack_count": 92,
  "normal_count": 149908,
  "features_count": 210,
  "git_commit": "abc123def456",
  "notes": "Initial dataset with 14 attack scenarios"
}
```

---

## Sample Data Snippets

### ci_cd_events (JSON)
```json
{
  "event_id": "evt_abc123",
  "timestamp": "2025-12-02T10:30:45Z",
  "event_type": "build_completed",
  "platform": "github_actions",
  "repository": "company/api-server",
  "branch": "main",
  "commit_sha": "abc123def456",
  "triggered_by": "user:john_doe",
  "status": "success",
  "duration_seconds": 245.6,
  "resource_usage": {
    "cpu_avg": 45.2,
    "cpu_max": 78.5,
    "mem_avg_mb": 1024,
    "mem_max_mb": 1536,
    "network_egress_mb": 25.3
  }
}
```

### attack_labels (JSON)
```json
{
  "event_id": "evt_xyz789",
  "timestamp": "2025-12-02T03:00:00Z",
  "is_attack": true,
  "attack_category": "compromised_credentials",
  "attack_scenario": "scenario_1.1",
  "severity": "high",
  "indicators": [
    "geographic_anomaly",
    "temporal_anomaly",
    "impossible_travel"
  ],
  "attack_stage": "initial_access",
  "mitre_attack_ids": ["T1078", "T1133"],
  "simulation_params": {
    "normal_location": "New York, US",
    "attack_location": "Bucharest, Romania",
    "distance_km": 7890
  },
  "notes": "Simulated compromised account login from Eastern Europe"
}
```

---

## Next Steps

1. **Implement data collection agents** for each event type
2. **Set up storage infrastructure** (database, file system)
3. **Create ETL pipelines** for data ingestion and transformation
4. **Implement feature engineering pipeline** (batch or streaming)
5. **Develop data validation scripts** for quality checks
6. **Set up data versioning** system
7. **Create sample datasets** for testing
8. **Document data lineage** and provenance
