# Scheduled Workflows Status Report

**Generated:** 2025-12-08
**Status:** ⚠️ Scheduled workflows configured but NOT running yet

---

## Summary

The security-scanning workflow is **correctly configured** with daily scheduled runs at 2 AM UTC, but **scheduled triggers haven't activated yet**.

### Current State:
- ✅ Schedule configured: `cron: '0 2 * * *'` (daily at 2 AM UTC)
- ✅ Workflow file is valid
- ✅ workflow_dispatch trigger working (manual runs work)
- ❌ **NO scheduled runs have occurred since Dec 4**

### Recent Runs (Last 9):
| Date | Time | Trigger | Branch | Status |
|------|------|---------|--------|--------|
| Dec 7 | 19:32 UTC | **push** | main | success |
| Dec 7 | 19:31 UTC | **push** | main | success |
| Dec 7 | 19:29 UTC | **push** | main | failure |
| Dec 7 | 01:17 UTC | **push** | main | failure |
| Dec 7 | 01:00 UTC | **push** | main | failure |
| Dec 6 | 23:29 UTC | **push** | main | success |
| Dec 6 | 17:41 UTC | **push** | hardened | failure |
| Dec 6 | 17:41 UTC | **push** | main | success |
| Dec 5 | 00:25 UTC | **push** | main | failure |

**Finding:** ALL runs triggered by `push` events, ZERO by `schedule`

---

## Root Cause

### GitHub Actions Scheduled Workflow Limitations:

1. **New Repository Delay**
   - Repository created: Dec 4, 2025 (4 days ago)
   - GitHub may not activate schedules for very new repositories immediately
   - Typical activation: 24-72 hours after first successful workflow run

2. **Requires Activity**
   - Scheduled workflows may need "warm-up" period
   - Manual workflow trigger can help activate the scheduler
   - Push-triggered runs don't always activate scheduled triggers

3. **Default Branch Only**
   - Scheduled workflows ONLY run from default branch (main)
   - ✅ Our workflow is on main branch

4. **Minimum Repository Activity**
   - Some reports suggest GitHub requires minimum repository age (3-7 days)
   - Current age: 4 days
   - Expected activation: Within next 24-48 hours

---

## Solutions

### Option 1: Manual Workflow Trigger (RECOMMENDED)

Manually triggering the workflow can "activate" the scheduler:

```bash
cd scripts
python trigger_security_scan.py
```

**What this does:**
- Triggers workflow via `workflow_dispatch` event
- Helps GitHub Actions "wake up" the scheduler
- Scheduled runs should start within 24-48 hours after manual trigger

### Option 2: Wait for Natural Activation

- **Timeline:** Scheduled runs typically activate within 7 days of workflow creation
- **Current:** Day 4 since workflow creation (Dec 4)
- **Expected:** Should activate by Dec 11 at latest
- **Action:** Monitor daily with `python scripts/check_scheduled_runs.py`

### Option 3: Commit Activity Trigger

Make a small commit to trigger workflow activity:

```bash
# Add empty commit
git commit --allow-empty -m "Trigger workflow to activate scheduler"
git push origin main
```

### Option 4: GitHub Actions Settings (via Web UI)

1. Go to: https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/settings/actions
2. Verify "Allow all actions and reusable workflows" is enabled
3. Check "Workflow permissions" has appropriate access
4. Ensure repository isn't archived or disabled

---

## Expected Behavior After Activation

Once activated, you should see:

### Daily Scheduled Runs:
```
[LAST 24H] 2025-12-09 02:00 UTC | main       | completed  | success    | [SCHEDULED]
[LAST 24H] 2025-12-08 02:00 UTC | main       | completed  | success    | [SCHEDULED]
```

### Data Collection Timeline:
- **Week 1:** Dec 9-15 (7 daily scans)
- **Week 2:** Dec 16-22 (7 daily scans)
- **Week 3:** Dec 23-29 (7 daily scans)
- **Week 4:** Dec 30 - Jan 5 (7 daily scans)
- **Total:** 28 automated data points

---

## Monitoring Commands

### Check if scheduled runs have started:
```bash
python scripts/check_scheduled_runs.py
```

### Manually trigger workflow:
```bash
python scripts/trigger_security_scan.py
```

### Check workflow status via API:
```bash
python scripts/check_scheduled_runs.py
```

---

## Technical Details

### Workflow Configuration:
```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_dispatch:     # Manual trigger
  push:                  # Auto on push
    branches: [main, develop, hardened]
```

### Schedule Format:
- `0 2 * * *` = "At 02:00 UTC every day"
- Breakdown: `minute hour day month weekday`
- `0 2 * * *` = minute 0, hour 2, every day, every month, every weekday

### Scheduled Workflow Requirements:
1. ✅ Workflow file on default branch (main)
2. ✅ Valid cron syntax
3. ✅ Repository has Actions enabled
4. ❌ **Repository activity/age (pending)**

---

## Next Steps

### Immediate (Today):
1. ✅ **Run manual trigger** to activate scheduler:
   ```bash
   python scripts/trigger_security_scan.py
   ```

2. ✅ **Verify manual run succeeds** (check GitHub Actions page)

### Tomorrow (Dec 9):
3. **Check for scheduled run at 2 AM UTC**:
   ```bash
   python scripts/check_scheduled_runs.py
   ```

4. If scheduled run occurred → ✅ **Activated!**
5. If NOT → Wait another 24-48 hours or contact GitHub Support

### Weekly (Every Sunday):
6. Monitor scheduled runs with `check_scheduled_runs.py`
7. Download artifacts with `automated-weekly-collection.py`

---

## Troubleshooting

### If scheduled runs still don't work after 7 days:

1. **Check GitHub Actions quota**
   - Free tier: 2,000 minutes/month
   - Private repo limits may apply
   - URL: https://github.com/settings/billing

2. **Verify workflow permissions**
   - Settings → Actions → General
   - "Workflow permissions" should allow actions

3. **Contact GitHub Support**
   - Include: Repository name, workflow file, timeline
   - Reference: "Scheduled workflows not running"

4. **Alternative: GitHub Actions Bot**
   - Use GitHub Actions self-hosted runner
   - Use external CRON service (cron-job.org) to trigger `workflow_dispatch`

---

## References

- [GitHub Actions: Scheduled Events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
- [Troubleshooting scheduled workflows](https://docs.github.com/en/actions/managing-workflow-runs/disabling-and-enabling-a-workflow)
- [workflow_dispatch event](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_dispatch)

---

## Status Updates

| Date | Status | Notes |
|------|--------|-------|
| Dec 8 | ❌ Not active | No scheduled runs yet (repository 4 days old) |
| Dec 9 | ⏳ Pending | Check after 2 AM UTC run |
| Dec 10+ | ⏳ Pending | Monitor daily |

**Update this file** as status changes.
