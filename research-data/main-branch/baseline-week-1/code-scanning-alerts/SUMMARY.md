# Code Scanning Results Summary

**Downloaded:** 2025-12-05 13:03:22
**Repository:** Gungnir44/devops-ml-security-and-anomaly-research

## Overview

- **Total Alerts:** 100
- **SARIF Analyses:** 17

## Alerts by Tool
- **Bandit:** 1 alerts
- **Grype:** 51 alerts
- **checkov:** 48 alerts

## Alerts by Severity

- **undefined:** 49 alerts
- **medium:** 36 alerts
- **low:** 5 alerts
- **high:** 7 alerts
- **critical:** 3 alerts

## Files

- `all-alerts.json` - All open alerts
- `*-alerts.json` - Alerts grouped by tool
- `sarif-analyses.json` - SARIF upload history

## Next Steps

1. Review alerts in `all-alerts.json`
2. Analyze tool-specific results
3. Map findings to ML features
4. Compare with artifact scan results

## API Access

To fetch detailed SARIF for a specific analysis:
```
GET /repos/Gungnir44/devops-ml-security-and-anomaly-research/code-scanning/analyses/{analysis_id}
```

---

**Note:** This data represents the current state of security alerts.
For historical data, download SARIF artifacts from workflow runs.
