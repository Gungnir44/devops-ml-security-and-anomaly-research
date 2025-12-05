# Exercise 1.1 Part 1: Process Map

**Student**: Alice Johnson
**Date**: 2024-01-15
**Company**: QuickShop E-Commerce

## Complete Process Map: Idea to Production

```
[Product Manager] → [Developer] → [Code Review] → [QA] → [Ops] → [Production]
       ↓                ↓              ↓           ↓       ↓           ↓
   Email request    Write code     Wait/Review   Testing  Deploy   Running
   (1 day)          (2-3 days)     (1-2 days)   (2 days) (varies)
```

### Detailed Flow Diagram

```
STEP 1: Feature Request
─────────────────────────────────────────────────────────
Owner: Product Manager
Activity: Email feature request to developer
Duration: 1 day (process time)
Output: Feature specification in email


STEP 2: Development
─────────────────────────────────────────────────────────
Owner: Developer
Activity: Write code, create pull request
Duration: 2-3 days (process time)
Output: Pull request in GitHub


STEP 3: Code Review Wait
─────────────────────────────────────────────────────────
Owner: N/A (waiting)
Activity: PR sits in queue waiting for available reviewer
Duration: 1-2 days (WAIT TIME)
Bottleneck: Limited reviewer availability
Output: N/A


STEP 4: Code Review
─────────────────────────────────────────────────────────
Owner: Senior Developer (reviewer)
Activity: Review code, provide feedback
Duration: 1 day (process time)
Output: Approved PR OR feedback requiring changes
Failure Mode: If changes needed, return to Step 2


STEP 5: Merge to Develop
─────────────────────────────────────────────────────────
Owner: Developer
Activity: Merge PR after approval
Duration: 0.1 days (process time)
Output: Code in develop branch


STEP 6: QA Wait
─────────────────────────────────────────────────────────
Owner: N/A (waiting)
Activity: Code waits for QA team to pick it up
Duration: Unknown (1-7 days) (WAIT TIME)
Bottleneck: QA team has queue of features to test
Note: Developer said "QA picks it up 'when they can'"
Output: N/A


STEP 7: QA Environment Setup
─────────────────────────────────────────────────────────
Owner: QA Engineer
Activity: Pull latest code, set up test environment
Duration: 4 hours (0.5 days) (process time)
Failure Mode: Environment often broken, takes longer
Output: Working test environment OR troubleshooting needed


STEP 8: Manual Testing
─────────────────────────────────────────────────────────
Owner: QA Engineer
Activity: Manual testing of feature
Duration: 2 days per feature (process time)
Output: Test results, bug reports in Jira


STEP 9: Bug Fixing (if bugs found)
─────────────────────────────────────────────────────────
Owner: Developer
Activity: Fix bugs, wait for review again
Duration: 1-2 days (process time)
Failure Mode: Returns to Step 3 (code review wait)
Output: Bug fixes merged


STEP 10: Re-test (if bugs were fixed)
─────────────────────────────────────────────────────────
Owner: QA Engineer
Activity: Re-test after bug fixes
Duration: 0.5-1 day (process time)
Output: QA approval


STEP 11: Wait for Deployment Window
─────────────────────────────────────────────────────────
Owner: N/A (waiting)
Activity: Feature waits for quarterly release
Duration: 30-60 days (WAIT TIME)
Bottleneck: Quarterly deployment schedule
Note: This is the LARGEST wait time
Output: N/A


STEP 12: Pre-Deployment
─────────────────────────────────────────────────────────
Owner: Operations
Activity: Review 50-page runbook, prepare for deployment
Duration: 1 week (process time)
Output: Deployment plan


STEP 13: Deployment Window Begins
─────────────────────────────────────────────────────────
Owner: Operations (5 people)
Activity: Friday 6 PM, manual deployment
- Backup production database (1 hour)
- SSH into 10 servers
- Copy files manually
- Restart services
- Check logs
- Monitor for issues
Duration: Variable (see below)
Output: Deployed code OR rollback


STEP 14A: Successful Deployment (60% chance)
─────────────────────────────────────────────────────────
Owner: Operations
Activity: Verify deployment successful
Duration: Total 8 hours (process time)
Output: Feature in production!
Team goes home: Midnight


STEP 14B: Failed Deployment (40% chance)
─────────────────────────────────────────────────────────
Owner: Operations
Activity: Rollback deployment
Duration: Additional 2 hours (process time)
Total time: 10 hours
Output: Production restored to previous state
Feature NOT deployed (try again next quarter)
Team goes home: 2 AM, exhausted


STEP 15: Post-Deployment Monitoring
─────────────────────────────────────────────────────────
Owner: Operations + On-call developer
Activity: Watch for issues over weekend
Duration: 48 hours (on-call time)
Output: Incident reports OR "all clear"
```

## Dependencies

### Linear Dependencies (blocking)
1. Development → Code Review (can't review until code written)
2. Code Review → QA (can't test until approved)
3. QA → Deployment (can't deploy until tested)
4. Deployment → Production (sequential process)

### Resource Dependencies (bottlenecks)
1. **Reviewer Availability**: Only 2-3 senior devs can review, shared across all devs
2. **QA Team Capacity**: 2 QA engineers for 10 developers (5:1 ratio)
3. **Test Environment**: Single shared environment (contention)
4. **Deployment Window**: Operations team only deploys during quarterly windows
5. **Operations Team**: 3 ops engineers handling all deployments manually

## Failure Points & Rework

```
Feature starts → Development (Step 2)
                     ↓
            Code Review (Step 4)
                     ↓
              Bugs Found? ───YES──→ Return to Development (REWORK)
                     ↓ NO
              QA Testing (Step 8)
                     ↓
              Bugs Found? ───YES──→ Return to Development (REWORK)
                     ↓ NO
         Wait for Deployment (Step 11)
                     ↓
           Deploy (Step 13)
                     ↓
           Deploy Failed? ───YES──→ Rollback, Try Next Quarter (REWORK)
                     ↓ NO
              PRODUCTION!
```

## Handoffs (Information Loss Points)

1. **Product → Dev**: Email-based requirements (ambiguity)
2. **Dev → Reviewer**: Context not always clear in PR
3. **Dev → QA**: "Ready for QA" email (no spec)
4. **QA → Ops**: List of features in release (minimal context)
5. **Ops → Support**: If issues occur, limited troubleshooting info

Each handoff = potential for:
- Miscommunication
- Lost context
- Delays while clarifying
- Rework due to misunderstanding
