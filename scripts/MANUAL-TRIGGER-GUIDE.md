# Manual Workflow Trigger Guide

**Purpose:** Manually trigger the security-scanning workflow to activate scheduled runs

---

## Why Manual Trigger Helps

Manually running the workflow can "activate" GitHub Actions scheduler for scheduled workflows. This is especially useful for:
- New repositories (< 7 days old)
- Recently added workflows
- Workflows where scheduled runs haven't started yet

---

## Method 1: GitHub Web UI (EASIEST)

### Steps:

1. **Go to Actions page:**
   ```
   https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions
   ```

2. **Select the workflow:**
   - Click on "Security Scanning Suite" in the left sidebar

3. **Trigger manually:**
   - Click the "Run workflow" button (top right)
   - Select branch: **main**
   - Click green "Run workflow" button

4. **Verify it started:**
   - You should see a new workflow run appear with a yellow dot (running)
   - Wait ~5-10 minutes for completion

5. **Expected result:**
   - Workflow completes successfully
   - Scheduled runs should activate within 24-48 hours

---

## Method 2: GitHub CLI (if installed)

```bash
# Install GitHub CLI first (if not installed)
# https://cli.github.com/

# Trigger workflow
gh workflow run security-scanning.yml --ref main
```

---

## Method 3: Python Script with Proper Token

### Create Token with Workflow Scope:

1. Go to: https://github.com/settings/tokens/new

2. Configure token:
   - **Name:** DevOps ML Workflow Trigger
   - **Expiration:** 90 days
   - **Scopes:** Check these boxes:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)

3. Click "Generate token"

4. **Save token to new file:**
   ```bash
   # Create new token file
   echo "ghp_YOUR_NEW_TOKEN_HERE" > scripts/.github_token_workflow
   ```

5. **Update trigger script** to use new token file:
   ```bash
   python trigger_security_scan.py
   ```

---

## Method 4: API Call (Advanced)

```bash
# Using curl with workflow-scoped token
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_WORKFLOW_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/Gungnir44/devops-ml-security-and-anomaly-research/actions/workflows/security-scanning.yml/dispatches \
  -d '{"ref":"main"}'
```

---

## After Manual Trigger

### Immediate (within 1 minute):
- Workflow run should appear in Actions page
- Status: Running (yellow dot)

### Within 10 minutes:
- Workflow should complete
- Status: Success (green checkmark) or Failure (red X)

### Within 24-48 hours:
- **Scheduled runs should activate**
- Check with: `python scripts/check_scheduled_runs.py`

### Expected scheduled run times:
- **Daily at 2:00 AM UTC**
- First scheduled run: Tomorrow at 2 AM UTC
- Ongoing: Every day at 2 AM UTC

---

## Verification Commands

### Check if scheduled runs started:
```bash
python scripts/check_scheduled_runs.py
```

### Look for this output:
```
[LAST 24H] 2025-12-09 02:00 UTC | main       | completed  | success    | [SCHEDULED]
                                                                          ^^^^^^^^^^^
                                                                          This is what you want to see!
```

---

## Troubleshooting

### Manual trigger doesn't appear:
- Verify you're on the correct repository
- Verify workflow file exists: `.github/workflows/security-scanning.yml`
- Check repository Actions are enabled: Settings → Actions → General

### Scheduled runs still not working after 48 hours:
- Wait full 7 days (new repository limitation)
- Check GitHub Actions billing/quotas
- Contact GitHub Support

### Workflow fails:
- Check workflow run logs
- Common issues: missing secrets, permission errors
- Fix errors and re-trigger

---

## Recommended: Use Web UI Method

**For immediate activation, use Method 1 (Web UI):**
1. Go to Actions page
2. Click "Security Scanning Suite"
3. Click "Run workflow" → Select "main" → Run

**This is the fastest and easiest method!**

---

## Expected Timeline

| Time | Event |
|------|-------|
| **Now** | Manual trigger via web UI |
| +5 min | Workflow completes |
| +24 hrs | First scheduled run (tomorrow 2 AM UTC) |
| +48 hrs | Second scheduled run |
| Ongoing | Daily runs at 2 AM UTC |

---

## Reference

- Current token (in `.github_token`): Read-only, for artifact downloads
- Needed token: Workflow scope, for triggering workflows
- Alternative: Use web UI (no token needed!)
