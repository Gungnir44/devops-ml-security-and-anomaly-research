# Exercise 2: Log Analysis with Shell Commands

**Duration**: 45-60 minutes
**Difficulty**: Intermediate
**Prerequisites**: Lessons 1-2
**Points**: 25

---

## Objectives

By completing this exercise, you will:
- Analyze log files using grep, awk, sed
- Use pipes to chain commands
- Extract meaningful data from unstructured text
- Generate reports from log files
- Practice text processing in DevOps context

---

## Scenario

Your company's web application has been experiencing intermittent errors. The operations team needs you to analyze server logs to identify patterns, find errors, and generate a report for the engineering team.

You have access to:
- Web server access logs
- Application error logs
- System logs
- Database query logs

Your task: Extract insights and identify the root cause.

---

## Setup

Create the practice environment with realistic log files:

```bash
# Navigate to exercise directory
mkdir -p ~/devops-learning/module-02/exercise-02
cd ~/devops-learning/module-02/exercise-02

# Create setup script
cat > setup-logs.sh << 'EOF'
#!/bin/bash
# Generate realistic log files

mkdir -p logs

# Generate access log (Apache/Nginx style)
cat > logs/access.log << 'ACCESS'
192.168.1.100 - - [16/Nov/2025:10:15:23 +0000] "GET /api/users HTTP/1.1" 200 1234
192.168.1.101 - - [16/Nov/2025:10:15:24 +0000] "POST /api/login HTTP/1.1" 200 567
192.168.1.102 - - [16/Nov/2025:10:15:25 +0000] "GET /api/products HTTP/1.1" 200 8901
192.168.1.100 - - [16/Nov/2025:10:15:26 +0000] "GET /api/orders HTTP/1.1" 500 156
192.168.1.103 - - [16/Nov/2025:10:15:27 +0000] "GET /static/css/main.css HTTP/1.1" 200 4567
192.168.1.104 - - [16/Nov/2025:10:15:28 +0000] "POST /api/checkout HTTP/1.1" 500 234
192.168.1.105 - - [16/Nov/2025:10:15:29 +0000] "GET /api/users/123 HTTP/1.1" 404 89
192.168.1.100 - - [16/Nov/2025:10:15:30 +0000] "GET /api/products/456 HTTP/1.1" 200 2345
192.168.1.106 - - [16/Nov/2025:10:15:31 +0000] "DELETE /api/users/789 HTTP/1.1" 403 123
192.168.1.107 - - [16/Nov/2025:10:15:32 +0000] "GET /api/dashboard HTTP/1.1" 200 6789
192.168.1.100 - - [16/Nov/2025:10:15:33 +0000] "POST /api/payment HTTP/1.1" 500 345
192.168.1.108 - - [16/Nov/2025:10:15:34 +0000] "GET /api/search?q=laptop HTTP/1.1" 200 12345
192.168.1.109 - - [16/Nov/2025:10:15:35 +0000] "GET /api/cart HTTP/1.1" 200 456
192.168.1.100 - - [16/Nov/2025:10:15:36 +0000] "PUT /api/users/100 HTTP/1.1" 200 789
192.168.1.110 - - [16/Nov/2025:10:15:37 +0000] "GET /health HTTP/1.1" 200 12
192.168.1.100 - - [16/Nov/2025:10:15:38 +0000] "GET /api/orders HTTP/1.1" 500 234
192.168.1.111 - - [16/Nov/2025:10:15:39 +0000] "POST /api/signup HTTP/1.1" 201 345
192.168.1.112 - - [16/Nov/2025:10:15:40 +0000] "GET /api/notifications HTTP/1.1" 200 567
192.168.1.100 - - [16/Nov/2025:10:15:41 +0000] "GET /api/payment HTTP/1.1" 500 123
192.168.1.113 - - [16/Nov/2025:10:15:42 +0000] "GET / HTTP/1.1" 200 9876
ACCESS

# Generate application error log
cat > logs/application.log << 'APPLOG'
2025-11-16 10:15:26 ERROR [api.orders] Database connection timeout after 30s
2025-11-16 10:15:26 ERROR [api.orders] Failed to fetch orders for user 100
2025-11-16 10:15:28 ERROR [api.checkout] Payment gateway returned error: CARD_DECLINED
2025-11-16 10:15:28 ERROR [api.checkout] Transaction rollback completed
2025-11-16 10:15:29 WARN [api.users] User 123 not found in database
2025-11-16 10:15:31 ERROR [api.users] Unauthorized delete attempt from IP 192.168.1.106
2025-11-16 10:15:33 ERROR [api.payment] Payment processor unavailable: Connection refused
2025-11-16 10:15:33 ERROR [api.payment] Retry attempt 1/3 failed
2025-11-16 10:15:34 INFO [api.search] Search query: laptop, results: 145
2025-11-16 10:15:36 INFO [api.users] User profile updated successfully
2025-11-16 10:15:38 ERROR [api.orders] Database connection timeout after 30s
2025-11-16 10:15:38 ERROR [api.orders] Failed to fetch orders for user 100
2025-11-16 10:15:39 INFO [api.signup] New user registered: user@example.com
2025-11-16 10:15:41 ERROR [api.payment] Payment processor unavailable: Connection refused
2025-11-16 10:15:41 ERROR [api.payment] Retry attempt 2/3 failed
APPLOG

# Generate database query log
cat > logs/database.log << 'DBLOG'
2025-11-16 10:15:23 [QUERY] SELECT * FROM users WHERE id=100 (15ms)
2025-11-16 10:15:24 [QUERY] SELECT * FROM sessions WHERE token='abc123' (8ms)
2025-11-16 10:15:25 [QUERY] SELECT * FROM products LIMIT 50 (45ms)
2025-11-16 10:15:26 [QUERY] SELECT * FROM orders WHERE user_id=100 (TIMEOUT)
2025-11-16 10:15:28 [QUERY] INSERT INTO transactions VALUES (...) (12ms)
2025-11-16 10:15:29 [QUERY] SELECT * FROM users WHERE id=123 (10ms) ROWS:0
2025-11-16 10:15:30 [QUERY] SELECT * FROM products WHERE id=456 (18ms)
2025-11-16 10:15:31 [QUERY] DELETE FROM users WHERE id=789 (FAILED: PERMISSION_DENIED)
2025-11-16 10:15:32 [QUERY] SELECT * FROM dashboard_stats (234ms)
2025-11-16 10:15:33 [QUERY] SELECT * FROM payment_gateways WHERE active=1 (TIMEOUT)
2025-11-16 10:15:34 [QUERY] SELECT * FROM products WHERE name LIKE '%laptop%' (567ms)
2025-11-16 10:15:35 [QUERY] SELECT * FROM cart_items WHERE user_id=109 (22ms)
2025-11-16 10:15:36 [QUERY] UPDATE users SET profile_data='...' WHERE id=100 (34ms)
2025-11-16 10:15:38 [QUERY] SELECT * FROM orders WHERE user_id=100 (TIMEOUT)
2025-11-16 10:15:39 [QUERY] INSERT INTO users VALUES (...) (45ms)
2025-11-16 10:15:40 [QUERY] SELECT * FROM notifications WHERE user_id=112 (19ms)
2025-11-16 10:15:41 [QUERY] SELECT * FROM payment_gateways WHERE active=1 (TIMEOUT)
DBLOG

echo "Log files generated in logs/ directory"
EOF

chmod +x setup-logs.sh
./setup-logs.sh
```

---

## Tasks

### Part 1: Basic Log Analysis (6 points)

**1. Count total log entries** (1 point)
- Count total lines in access.log
- Count total lines in application.log
- Count total lines in database.log

**2. Find all errors** (1 point)
- Extract all ERROR lines from application.log
- Count how many ERROR lines exist

**3. Find specific IP addresses** (1 point)
- Find all requests from IP 192.168.1.100
- Count how many requests this IP made

**4. Filter by status code** (1 point)
- Find all 500 errors in access.log
- Find all 404 errors
- Find all 200 success responses

**5. Extract unique IPs** (1 point)
- List all unique IP addresses from access.log
- Sort them

**6. Find database timeouts** (1 point)
- Extract all TIMEOUT entries from database.log
- Count how many timeouts occurred

### Part 2: Advanced Text Processing (8 points)

**7. Calculate error rate** (2 points)
- Count total requests in access.log
- Count 500 errors
- Calculate percentage of failed requests

**8. Find top requested endpoints** (2 points)
- Extract all API endpoints from access.log
- Count requests per endpoint
- Sort by frequency (most requested first)
- Show top 5

**9. Analyze response times** (2 points)
- Extract query times from database.log
- Find slowest query (highest ms)
- Find average query time (bonus: calculate average)

**10. Extract payment errors** (2 points)
- Find all errors related to "payment" (case-insensitive)
- Extract from both application.log and access.log
- Show which component failed

### Part 3: Report Generation (7 points)

**11. Generate hourly request summary** (2 points)
- Extract hour from timestamps
- Count requests per hour
- Format as table

**12. Create error report** (2 points)
- List all error types from application.log
- Group by error category (database, payment, auth, etc.)
- Count occurrences

**13. IP activity report** (1 point)
- Show top 5 most active IP addresses
- Include request count and status code breakdown

**14. Failed operations summary** (2 points)
- Identify all failed operations (500, 404, ERROR, TIMEOUT, FAILED)
- Categorize by type
- Create summary report

### Part 4: Real-World Scenarios (4 points)

**15. Find root cause** (2 points)
- Analyze all three log files together
- Identify the common failing component
- Explain the likely root cause

**16. Security analysis** (2 points)
- Find unauthorized access attempts
- Find suspicious patterns (multiple 403/404 from same IP)
- List potential security concerns

---

## Deliverables

Submit `log-analysis-report.md` containing:

### Section 1: Commands and Outputs

For each task, provide:
```markdown
## Task X: [Task Name]

**Command**:
```bash
[your command]
```

**Output**:
```
[command output]
```

**Analysis**: [What this tells us]
```

### Section 2: Executive Summary

```markdown
# Log Analysis Report - [Your Name]
**Date**: 2025-11-16
**Log Files Analyzed**: access.log, application.log, database.log

## Key Findings:
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

## Critical Issues:
- [Issue 1 with severity]
- [Issue 2 with severity]

## Root Cause:
[Your analysis of the root cause]

## Recommendations:
1. [Action item 1]
2. [Action item 2]
```

### Section 3: Statistics

```markdown
## Statistics Summary

| Metric | Value |
|--------|-------|
| Total Requests | XX |
| Failed Requests (5xx) | XX |
| Error Rate | XX% |
| Database Timeouts | XX |
| Unique IP Addresses | XX |
| Most Active IP | XXX.XXX.XXX.XXX (XX requests) |
```

---

## Submission Format

```bash
# Create submission
mkdir exercise-02-submission
cd exercise-02-submission

# Your report
cp log-analysis-report.md .

# Your analysis scripts (if created)
cp analysis.sh .

# Create archive
zip -r exercise-02-[yourname].zip log-analysis-report.md
```

---

## Grading Rubric

| Category | Points | Criteria |
|----------|--------|----------|
| **Part 1: Basic Analysis** | 6 | Correct use of grep, wc, basic filters |
| **Part 2: Advanced Processing** | 8 | Proper use of awk, sed, pipes, calculations |
| **Part 3: Report Generation** | 7 | Well-formatted reports, accurate summaries |
| **Part 4: Real-World Analysis** | 4 | Insightful analysis, root cause identified |
| **Total** | **25** | |

**Bonus Points** (+3):
- Create reusable analysis script
- Generate HTML/CSV report
- Advanced insights beyond requirements

---

## Hints

<details>
<summary>Hint 1: Counting with grep</summary>

```bash
grep "ERROR" application.log | wc -l
```
</details>

<details>
<summary>Hint 2: Extracting fields with awk</summary>

```bash
# Extract IP address (first field)
awk '{print $1}' access.log

# Extract status code (9th field)
awk '{print $9}' access.log
```
</details>

<details>
<summary>Hint 3: Unique values</summary>

```bash
awk '{print $1}' access.log | sort | uniq
# Or count occurrences:
awk '{print $1}' access.log | sort | uniq -c
```
</details>

<details>
<summary>Hint 4: Filtering by multiple patterns</summary>

```bash
grep -E "ERROR|TIMEOUT" application.log
```
</details>

<details>
<summary>Hint 5: Calculating percentages</summary>

```bash
total=$(wc -l < access.log)
errors=$(grep " 500 " access.log | wc -l)
echo "scale=2; $errors / $total * 100" | bc
```
</details>

---

## Example Solutions

<details>
<summary>Solution Examples (Try first!)</summary>

```bash
# Task 1: Count log entries
wc -l logs/access.log
wc -l logs/application.log
wc -l logs/database.log

# Task 2: Find all errors
grep "ERROR" logs/application.log
grep "ERROR" logs/application.log | wc -l

# Task 3: Find specific IP
grep "192.168.1.100" logs/access.log
grep "192.168.1.100" logs/access.log | wc -l

# Task 4: Filter by status code
grep " 500 " logs/access.log
grep " 404 " logs/access.log
grep " 200 " logs/access.log

# Task 5: Extract unique IPs
awk '{print $1}' logs/access.log | sort | uniq

# Task 8: Top requested endpoints
awk '{print $7}' logs/access.log | sort | uniq -c | sort -rn | head -5

# Task 12: Error report
grep "ERROR" logs/application.log | awk '{print $3}' | sed 's/\[//;s/\]//' | sort | uniq -c

# Task 15: Root cause analysis
# Multiple database timeouts + payment errors = Database connectivity issue
grep -i "timeout\|connection" logs/*.log
```
</details>

---

## Real-World Application

This exercise simulates actual DevOps troubleshooting:
- **On-Call Debugging**: Quickly identify issues from logs
- **Incident Response**: Generate reports for post-mortems
- **Performance Analysis**: Find slow queries and bottlenecks
- **Security Audits**: Detect unauthorized access patterns

---

## Advanced Challenges (Optional)

1. **Create automated monitoring script**:
   - Runs every minute
   - Alerts if error rate > 5%
   - Sends summary email

2. **Generate graphs**:
   - Requests per minute timeline
   - Error rate over time
   - Response time distribution

3. **Parse complex formats**:
   - Extract JSON from logs
   - Parse multi-line stack traces
   - Handle different log formats

---

## Common Mistakes

❌ **Not escaping special characters**
```bash
grep "[ERROR]" file  # Wrong: [] are regex characters
grep "\[ERROR\]" file  # Correct
```

❌ **Wrong field numbers in awk**
```bash
# Fields are space-separated by default
awk '{print $10}' # Might be wrong field!
# Always verify with: awk '{print NF, $0}' to see field count
```

❌ **Forgetting to sort before uniq**
```bash
uniq file  # Doesn't work if not sorted!
sort file | uniq  # Correct
```

---

## Learning Resources

- `man grep` - Master regular expressions
- `man awk` - Learn field processing
- `man sed` - Text transformation
- [regex101.com](https://regex101.com) - Test regular expressions

---

## What You'll Learn

After this exercise:
- ✅ Analyze logs like a professional DevOps engineer
- ✅ Extract insights from unstructured data
- ✅ Chain commands with pipes efficiently
- ✅ Generate actionable reports
- ✅ Identify root causes from logs

**Log analysis is a critical DevOps skill - master it!** 📊

---

**Next**: Exercise 3 - Write automation scripts using what you've learned!
