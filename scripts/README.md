# Research Data Download Scripts

Scripts to download all artifacts and code scanning results from GitHub.

---

## 🚀 Quick Start (Easiest Way)

### 1. Create GitHub Token
Go to: https://github.com/settings/tokens

**Required scopes:**
- `repo` (full control)
- `workflow`
- `security_events`

### 2. Run Everything At Once

```powershell
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"

.\download-everything.ps1 -Token "ghp_YOUR_TOKEN_HERE"
```

**Replace `ghp_YOUR_TOKEN_HERE` with your actual GitHub token!**

This single command will:
1. Download all workflow artifacts
2. Download all code scanning results
3. Extract and organize everything
4. Generate summary reports

**Done!** Your complete dataset will be in `research-data/baseline-week-1/`

---

## 📜 Individual Scripts

If you prefer to run steps separately:

### download-artifacts.ps1
Downloads artifacts from GitHub Actions workflow runs.

```powershell
.\download-artifacts.ps1 -Token "ghp_YOUR_TOKEN"
```

**Downloads:**
- Test coverage reports
- Security scan results
- Container scan results
- Build metadata

**From workflows:**
- Backend CI/CD
- Python CI/CD
- Frontend CI/CD

---

### download-code-scanning.ps1
Downloads security alerts from GitHub Code Scanning.

```powershell
.\download-code-scanning.ps1 -Token "ghp_YOUR_TOKEN"
```

**Downloads:**
- All open security alerts
- Results grouped by tool (CodeQL, Semgrep, etc.)
- Results grouped by severity
- SARIF upload history

---

### extract-app-artifacts.ps1
Extracts all downloaded ZIP files and organizes them.

```powershell
.\extract-app-artifacts.ps1
```

**No token needed** - works on already downloaded files.

**Organizes by:**
- Application (backend, python, frontend)
- Category (security-scans, container-scans, test-coverage, metadata)

---

### extract-all-zips.ps1
Extracts any ZIPs in the research-data folder.

```powershell
.\extract-all-zips.ps1
```

**Use this for manually downloaded files.**

---

### create-folders.ps1
Creates the research data folder structure.

```powershell
.\create-folders.ps1
```

**Already run** - folder structure exists.

---

## 📁 Where Data Goes

```
research-data/
├── downloads/              ← Raw ZIPs downloaded here
│   ├── backend/
│   ├── python/
│   └── frontend/
│
└── baseline-week-1/        ← Extracted data organized here
    ├── backend/
    │   ├── security-scans/
    │   ├── container-scans/
    │   ├── test-coverage/
    │   └── metadata/
    ├── python/
    │   ├── security-scans/
    │   ├── container-scans/
    │   ├── test-coverage/
    │   └── metadata/
    ├── frontend/
    │   ├── security-scans/
    │   ├── container-scans/
    │   ├── test-coverage/
    │   └── metadata/
    ├── security-scans-general/
    ├── sbom-and-licenses/
    ├── code-scanning-alerts/
    └── COMPLETE-DATA-SUMMARY.md
```

---

## 🔐 Security Token Tips

**Create token:**
https://github.com/settings/tokens → "Generate new token (classic)"

**Required permissions:**
- ✅ repo
- ✅ workflow
- ✅ security_events

**Keep it safe:**
- Don't commit to Git
- Don't share publicly
- Store in password manager
- Delete when done: https://github.com/settings/tokens

---

## 📊 After Download

### View Summary
```powershell
notepad "..\research-data\baseline-week-1\COMPLETE-DATA-SUMMARY.md"
```

### View Code Scanning Results
```powershell
notepad "..\research-data\baseline-week-1\code-scanning-alerts\SUMMARY.md"
```

### Count Files
```powershell
cd "..\research-data\baseline-week-1"
Get-ChildItem -Recurse -File | Measure-Object
```

### List by File Type
```powershell
Get-ChildItem -Recurse -File | Group-Object Extension | Sort-Object Count -Descending
```

---

## ❌ Troubleshooting

### "401 Unauthorized"
- Check token is correct
- Verify token hasn't expired
- Ensure required scopes selected

### "No artifacts found"
- Workflows may not have run yet
- Artifacts may have expired (90 days)
- Trigger new workflow runs

### "Script not found"
```powershell
# Make sure you're in scripts folder
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"
ls *.ps1  # Should show all scripts
```

### "Execution Policy" error
```powershell
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🆘 Help

**Read detailed guide:**
```powershell
notepad HOW-TO-DOWNLOAD-ALL-DATA.md
```

**Quick command reference:**
```powershell
# Download everything
.\download-everything.ps1 -Token "YOUR_TOKEN"

# Or step by step:
.\download-artifacts.ps1 -Token "YOUR_TOKEN"
.\download-code-scanning.ps1 -Token "YOUR_TOKEN"
.\extract-app-artifacts.ps1
```

---

## ✅ Checklist

Before running scripts:
- [ ] GitHub token created
- [ ] Token has required scopes (repo, workflow, security_events)
- [ ] In correct directory (scripts/)
- [ ] Token ready to paste

After running scripts:
- [ ] No error messages
- [ ] Files downloaded to downloads/
- [ ] Files extracted to baseline-week-1/
- [ ] Summary reports generated
- [ ] 30+ files in baseline-week-1/

---

**Ready?** Run `.\download-everything.ps1 -Token "YOUR_TOKEN"` to get started! 🚀
