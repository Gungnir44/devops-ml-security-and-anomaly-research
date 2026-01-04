# Step-by-Step: Create GitHub Personal Access Token

Follow these exact steps to create your token.

---

## Step 1: Go to Token Settings

**Click this link:** https://github.com/settings/tokens

Or manually:
1. Click your profile picture (top right on GitHub)
2. Click **Settings**
3. Scroll down left sidebar → Click **Developer settings** (at bottom)
4. Click **Personal access tokens** → **Tokens (classic)**

---

## Step 2: Generate New Token

Click the green button: **"Generate new token"** → **"Generate new token (classic)"**

*(NOT "Fine-grained tokens" - use the classic option)*

---

## Step 3: Configure Token

### Note (Description)
Enter: `DevOps Research Data Download`

*(This helps you remember what it's for)*

### Expiration
Select: **90 days**

*(Or longer if you prefer - you can always create a new one)*

---

## Step 4: Select Scopes (IMPORTANT!)

Scroll down and check EXACTLY these boxes:

### ✅ repo (Full control of private repositories)
**Click the top-level checkbox "repo"** - this will auto-check all sub-items:
- ✅ repo:status
- ✅ repo_deployment
- ✅ public_repo
- ✅ repo:invite
- ✅ security_events

### ✅ workflow (Update GitHub Action workflows)
**Click the "workflow" checkbox**

### ✅ read:packages (Download packages from GitHub Package Registry)
**Under "write:packages", click just "read:packages"**

### Optional (helpful but not required):
- ✅ read:org (Read org and team membership)

---

## Step 5: Generate Token

1. Scroll to bottom
2. Click green button: **"Generate token"**

---

## Step 6: COPY THE TOKEN IMMEDIATELY

You'll see a page with a green box containing your token:

```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**CRITICAL:**
- ✅ Click the copy icon (📋) to copy it
- ✅ Paste it somewhere safe (Notepad, password manager)
- ⚠️ You will NEVER see this token again!
- ⚠️ If you lose it, you must create a new one

---

## Step 7: Save It Securely

Create a temporary file:

```powershell
notepad "C:\Users\joshu\Desktop\github-token.txt"
```

Paste the token there and save it.

**Example token format:**
```
ghp_1234567890abcdefghijklmnopqrstuvwxyzABCD
```

---

## Step 8: Test Your Token

Open PowerShell and run:

```powershell
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"

# Test with a simple API call
$token = "ghp_YOUR_TOKEN_HERE"
$headers = @{Authorization = "Bearer $token"}
Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
```

If it works, you'll see your GitHub user info!

---

## Step 9: Use Token to Download Data

```powershell
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"

.\download-everything.ps1 -Token "ghp_YOUR_TOKEN_HERE"
```

**Replace `ghp_YOUR_TOKEN_HERE` with your actual token!**

---

## ✅ Checklist

Before clicking "Generate token":
- [ ] Note: "DevOps Research Data Download"
- [ ] Expiration: 90 days (or your choice)
- [ ] ✅ repo (checked)
- [ ] ✅ workflow (checked)
- [ ] ✅ security_events (auto-checked under repo)
- [ ] ✅ read:packages (checked)

After generating:
- [ ] Token copied to clipboard
- [ ] Token saved to notepad or password manager
- [ ] Token looks like: ghp_xxxxxxxxxxxxx

---

## 🔒 Security Reminders

**DO:**
- ✅ Keep it private
- ✅ Store in password manager
- ✅ Use only on your local machine
- ✅ Delete after use (if temporary)

**DON'T:**
- ❌ Commit to Git
- ❌ Share with others
- ❌ Post in Discord/Slack/etc.
- ❌ Hard-code in files that get uploaded

---

## ❌ If You Lose Your Token

Don't worry! Just create a new one:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Repeat steps above
4. Delete the old token

---

## 🗑️ Delete Token When Done

After downloading all your data:

1. Go to: https://github.com/settings/tokens
2. Find your token in the list
3. Click **Delete**
4. Confirm deletion

*(This is good security practice if you don't need it anymore)*

---

## 🆘 Troubleshooting

### "Not enough scopes" error
- Go back to token settings
- Edit the token
- Make sure `repo` and `workflow` are checked

### Token not working
- Check for extra spaces when copying
- Make sure it starts with `ghp_`
- Verify it hasn't expired

### Can't see token after creating
- You can't view it again
- Create a new token
- Copy it immediately this time

---

## Next Step

After you have your token saved, run:

```powershell
cd "C:\Users\joshu\Desktop\DevOps Project\scripts"
.\download-everything.ps1 -Token "YOUR_TOKEN"
```

**Good luck!** 🚀
