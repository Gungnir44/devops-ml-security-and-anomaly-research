# Complete Guide: Download All Research Data

This guide will help you download **all** artifacts and code scanning results from GitHub.

---

## Step 1: Create GitHub Personal Access Token

You need a token to download data programmatically.

### 1.1 Go to GitHub Token Settings
**Direct link:** https://github.com/settings/tokens

### 1.2 Generate New Token
1. Click **"Generate new token (classic)"**
2. Give it a name: `DevOps Research Data Download`
3. Select expiration: `90 days` (or longer)

### 1.3 Select Required Scopes
Check these boxes:
- ✅ **repo** (Full control of private repositories)
  - This includes `repo:status`, `repo_deployment`, `public_repo`
- ✅ **workflow** (Update GitHub Action workflows)
- ✅ **read:packages** (Download packages)
- ✅ **read:org** (Read org data) - optional
- ✅ **security_events** (Read security events) - for code scanning

### 1.4 Generate and Copy Token
1. Scroll to bottom → Click **"Generate token"**
2. **COPY THE TOKEN IMMEDIATELY** - you won't see it again!
3. Save it somewhere safe (e.g., password manager)

**Example token format:**
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Step 2: Download All Artifacts

### 2.1 Run the Artifact Downloader

Open PowerShell and run:

```powershell
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"

.\download-artifacts.ps1 -Token "ghp_YOUR_TOKEN_HERE"
```

**Replace `ghp_YOUR_TOKEN_HERE` with your actual token!**

### 2.2 What This Downloads

The script will automatically download from **all recent workflow runs**:

**Backend CI/CD artifacts:**
- Test coverage reports (Jest)
- Security scan results (TruffleHog, Gitleaks, Semgrep, CodeQL)
- Container scan results (Trivy, Grype, Dockle)
- SARIF files
- Build metadata

**Python CI/CD artifacts:**
- Test coverage reports (Pytest)
- Security scan results (Bandit, Semgrep, CodeQL)
- Container scan results (Trivy, Grype, Dockle)
- SARIF files
- Build metadata

**Frontend CI/CD artifacts:**
- Test coverage reports (Vitest)
- Security scan results (ESLint, Semgrep, CodeQL)
- Container scan results (Trivy, Grype, Dockle)
- SARIF files
- Build metadata

**Downloads to:**
```
research-data/downloads/
├── backend/
├── python/
└── frontend/
```

---

## Step 3: Download Code Scanning Results

### 3.1 Run the Code Scanning Downloader

```powershell
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"

.\download-code-scanning.ps1 -Token "ghp_YOUR_TOKEN_HERE"
```

### 3.2 What This Downloads

This downloads **all security alerts** from GitHub Security tab:

- ✅ All CodeQL findings
- ✅ All Semgrep findings
- ✅ All other SAST tool findings
- ✅ Organized by tool
- ✅ Organized by severity
- ✅ SARIF upload history

**Downloads to:**
```
research-data/baseline-week-1/code-scanning-alerts/
├── all-alerts.json
├── CodeQL-alerts.json
├── Semgrep-alerts.json
├── sarif-analyses.json
└── SUMMARY.md
```

---

## Step 4: Extract Everything

After downloading, extract all the new ZIPs:

```powershell
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"

.\extract-app-artifacts.ps1
```

This will:
1. Find all downloaded ZIPs
2. Extract them to appropriate folders
3. Organize by application and category
4. Generate a summary report

---

## Step 5: Verify Complete Data

Check that you have all the data:

```powershell
cd "C:\Users\joshu\Desktop\DevOps Project\research-data\baseline-week-1"

# List all extracted files
Get-ChildItem -Recurse -File | Measure-Object
```

You should have **30+ files** extracted.

---

## Expected Folder Structure After Download

```
baseline-week-1/
├── backend/
│   ├── security-scans/
│   │   ├── semgrep-results/
│   │   ├── codeql-results/
│   │   ├── gitleaks-results/
│   │   └── trufflehog-results/
│   ├── container-scans/
│   │   ├── trivy-results/
│   │   ├── grype-results/
│   │   └── dockle-results/
│   ├── test-coverage/
│   │   └── jest-coverage/
│   └── metadata/
│       └── backend-metadata.json ✅
│
├── python/
│   ├── security-scans/
│   │   ├── bandit-results/
│   │   ├── semgrep-results/
│   │   ├── codeql-results/
│   │   └── pip-audit/ ✅
│   ├── container-scans/
│   │   ├── trivy-results/
│   │   ├── grype-results/
│   │   └── dockle-results/
│   ├── test-coverage/
│   │   └── pytest-coverage/
│   └── metadata/
│       └── python-metadata.json ✅
│
├── frontend/
│   ├── security-scans/
│   │   ├── eslint-results/
│   │   ├── semgrep-results/
│   │   └── codeql-results/
│   ├── container-scans/
│   │   ├── trivy-results/
│   │   ├── grype-results/
│   │   └── dockle-results/
│   ├── test-coverage/
│   │   └── vitest-coverage/
│   └── metadata/
│       └── frontend-metadata.json ✅
│
├── security-scans-general/
│   ├── kics-results/ ✅
│   └── gitleaks-results.sarif/ ✅
│
├── sbom-and-licenses/ ✅
│
├── code-scanning-alerts/ (NEW!)
│   ├── all-alerts.json
│   ├── CodeQL-alerts.json
│   ├── Semgrep-alerts.json
│   └── SUMMARY.md
│
├── COMPLETE-DATA-SUMMARY.md ✅
└── EXTRACTION-REPORT.txt
```

---

## Troubleshooting

### Error: "401 Unauthorized"
**Cause:** Token is invalid or missing required scopes
**Solution:**
1. Check token is copied correctly (no extra spaces)
2. Verify token has `repo` and `workflow` scopes
3. Generate a new token if expired

### Error: "403 Forbidden"
**Cause:** Token doesn't have access to repository
**Solution:**
1. Ensure repository is public OR token has access
2. Check `security_events` scope for code scanning

### Error: "No artifacts found"
**Cause:** Workflow runs didn't generate artifacts OR artifacts expired
**Solution:**
1. Go to GitHub Actions and verify artifacts exist
2. Artifacts expire after 90 days - trigger new runs if needed
3. Check workflow logs for upload failures

### Error: "Rate limit exceeded"
**Cause:** Too many API requests
**Solution:**
1. Wait 1 hour for rate limit reset
2. Use authenticated requests (token) for higher limits

---

## Manual Download Alternative

If scripts don't work, you can download manually:

### For Artifacts:
1. Go to: https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/actions
2. Click each workflow run
3. Scroll to "Artifacts" section
4. Click to download each ZIP
5. Save to `research-data/downloads/` folders

### For Code Scanning:
1. Go to: https://github.com/Gungnir44/devops-ml-security-and-anomaly-research/security/code-scanning
2. Click "Export" or "Download CSV"
3. Save to `research-data/baseline-week-1/code-scanning-alerts/`

---

## Quick Command Reference

```powershell
# Navigate to scripts folder
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"

# Download artifacts (REPLACE TOKEN!)
.\download-artifacts.ps1 -Token "ghp_YOUR_TOKEN"

# Download code scanning results (REPLACE TOKEN!)
.\download-code-scanning.ps1 -Token "ghp_YOUR_TOKEN"

# Extract all downloaded ZIPs
.\extract-app-artifacts.ps1

# Check what you have
cd "..\research-data\baseline-week-1"
Get-ChildItem -Recurse -File | Group-Object Extension | Select-Object Count, Name
```

---

## Security Note

**IMPORTANT:** Your GitHub token is like a password!

✅ **DO:**
- Store it securely (password manager)
- Use it only in scripts on your local machine
- Delete it after use if you don't need it anymore

❌ **DON'T:**
- Commit it to Git
- Share it with others
- Post it online
- Hard-code it in files

**Delete token when done:**
https://github.com/settings/tokens → Click token → Delete

---

## Next Steps After Download

1. ✅ Verify all data downloaded
2. ✅ Run extraction script
3. ✅ Read COMPLETE-DATA-SUMMARY.md
4. ✅ Begin data analysis
5. ✅ Create visualizations
6. ✅ Document findings

---

**Ready?** Create your token and run the scripts! 🚀

**Need help?** Check the error messages above or ask for assistance.
