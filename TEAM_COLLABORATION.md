# 👥 Team Collaboration Guide

How your friends can contribute to the project.

---

## Scenario 1: Friend Wants to Use Your App (No Coding)

**They just need the link!**

```
1. You send: https://huggingface.co/spaces/yourusername/agrisight-portal
2. Friend clicks link
3. Friend uploads leaf photo
4. Friend sees prediction + Grad-CAM
5. Done! ✅
```

**No installation. No GitHub. No setup needed.**

---

## Scenario 2: Friend Wants to Edit Code & Push Changes

Your friend needs to:

### Step 1: Clone Your GitHub Repo

```bash
git clone https://github.com/yourusername/agrisight
cd agrisight
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Create `.streamlit/secrets.toml`

If using Supabase, ask you for:
- Your Supabase URL
- Your Supabase Anon Key

Create `.streamlit/secrets.toml`:
```toml
[supabase]
url = "https://xxxxx.supabase.co"
key = "eyJhbGc..."
```

### Step 4: Test Locally

```bash
streamlit run portal.py
```

### Step 5: Make Edits

Edit any files (e.g., `portal.py`, change colors, add features)

### Step 6: Push Changes

```bash
git add .
git commit -m "Add new feature: ..."
git push origin main
```

**Your HuggingFace Space auto-updates!** 🎉

---

## Scenario 3: Collaborative Development (Multiple Friends)

### Setup (One-time)

**You (maintainer):**
1. Create GitHub repo (already done)
2. Add friends as collaborators:
   - GitHub: Settings → Collaborators → Add friend's username
3. Set up HuggingFace Space from your GitHub repo

**Your friend:**
1. Accept GitHub invite
2. Clone the repo
3. Create their own `.streamlit/secrets.toml` (same Supabase creds)
4. Make edits and push

### Workflow

```
Friend 1                    Friend 2                    You (Main)
   ↓                            ↓                           ↓
 Edit                         Edit                      Review
  ↓                            ↓                           ↓
 Push                         Push                    Merge/Approve
  ↓                            ↓                           ↓
GitHub Branch            GitHub Branch            GitHub Main
  ↓                            ↓                           ↓
                           ↙──────────────────────────↖
                                      ↓
                            HuggingFace Auto-Deploy
                                      ↓
                           Live URL: Everyone uses it!
```

---

## How to Invite Friends as GitHub Collaborators

1. Go to your GitHub repo: `https://github.com/yourusername/agrisight`
2. Click **"Settings"** (top right)
3. Click **"Collaborators"** (left sidebar)
4. Click **"Add people"**
5. Enter friend's GitHub username
6. Send invite

Friend will get an email → accepts → can now push code!

---

## Communication Tips for Team

### Via GitHub Issues
- Create issues for bugs/features
- Assign to teammates
- Comment on solutions

### Via Pull Requests
- Friend creates branch: `git checkout -b feature-name`
- Makes edits
- Pushes: `git push origin feature-name`
- Creates Pull Request on GitHub
- You review and merge

### Via Discord/Slack
- Share HuggingFace link
- Test updates together
- Discuss bugs in real-time

---

## File Ownership & Editing

| File | Should Edit | Notes |
|---|---|---|
| `portal.py` | ✅ Both | Main UI code |
| `models.py` | ⚠️ Be careful | Core ML code |
| `app.py` | ✅ Both | Original demo |
| `requirements.txt` | ⚠️ Discuss | Adding dependencies |
| `.streamlit/secrets.toml` | ❌ NEVER | Keep local, never push! |
| `README.md` | ✅ Both | Documentation |

---

## Version Control Best Practices

### Do ✅
```bash
git pull before editing
git commit frequently with clear messages
git push after testing locally
```

### Don't ❌
```
Don't commit secrets.toml
Don't force push (git push -f)
Don't edit main branch directly (use branches)
Don't add huge files (>100MB)
```

---

## What Gets Deployed Where

```
YOUR LOCAL MACHINE
├── Code edits
├── Test with: streamlit run portal.py
└── Push when working: git push origin main

GITHUB (yourusername/agrisight)
├── Stores your code
├── Tracks changes
└── Collaborative editing

HUGGINGFACE SPACES (auto-deploy)
├── Watches GitHub main branch
├── Auto-builds Docker container
└── Runs publicly: https://huggingface.co/spaces/...

SUPABASE (optional)
├── User authentication
├── Scan history storage
└── Multi-user support
```

---

## Data Flow (Multi-User)

```
Friend 1's Browser       Friend 2's Browser       Your Browser
    ↓                         ↓                        ↓
    └─────────────────────────┴────────────────────────┘
                              ↓
                      HuggingFace Server
                   (Running your Streamlit app)
                              ↓
                      Supabase Database
                   (Storing all scans safely)
```

Each user's scans are private (Row Level Security).

---

## Sharing Specific Features

Want to work on separate features without conflicts?

### Feature Branches

```bash
# Friend 1: New warning system
git checkout -b feature/smart-warnings
# ... edits ...
git push origin feature/smart-warnings
# Create Pull Request on GitHub

# Friend 2: Model comparison feature
git checkout -b feature/model-comparison
# ... edits ...
git push origin feature/model-comparison
# Create Pull Request on GitHub

# Both can work in parallel!
# You merge both into main when ready
```

---

## Preventing Merge Conflicts

**Good communication:**
- "I'm editing portal.py page_scan() function"
- "I'm working on requirements.txt"
- Avoid editing the same file at same time

**If conflict happens:**
1. Pull latest: `git pull origin main`
2. Fix conflicts in your editor
3. Commit: `git add . && git commit -m "Resolve merge conflict"`
4. Push: `git push origin main`

---

## Deployment Checklist for Releases

Before pushing to HuggingFace:

- [ ] Code tested locally: `streamlit run portal.py`
- [ ] No breaking changes
- [ ] Dependencies updated in `requirements.txt`
- [ ] README.md updated
- [ ] Secrets not accidentally committed
- [ ] All tests pass (if any)

```bash
git add .
git commit -m "Release v1.0: [description]"
git push origin main
# HuggingFace auto-deploys in 1-2 min
```

---

## Quick Reference Commands

```bash
# Clone your repo (friend does this)
git clone https://github.com/yourusername/agrisight

# Get latest changes
git pull origin main

# Create feature branch
git checkout -b feature/my-feature

# Check what changed
git status

# Stage changes
git add .

# Commit with message
git commit -m "Add new feature: description"

# Push to GitHub
git push origin main

# (Optionally) Create Pull Request on GitHub for review
```

---

## Slack/Discord Integration (Optional)

Auto-notify team when code is pushed:

1. Go to GitHub Settings → Webhooks
2. Click "Add webhook"
3. Paste your Discord webhook URL
4. Now: Every push → notification in Discord! 🔔

---

## Support Questions

**Your friend asks: "How do I...?"**

| Question | Answer |
|---|---|
| Use the deployed app? | Send them the HuggingFace link (no setup) |
| Edit code with you? | Add as GitHub collaborator |
| Add a new feature? | Make a feature branch, push, create PR |
| Fix a bug? | Create a GitHub Issue, assign to yourself |
| Merge their changes? | Review PR → Click "Merge" on GitHub |
| Deploy changes? | Push to main → HuggingFace auto-deploys |

---

## Summary

✅ **App Users** (no coding): Send HuggingFace link  
✅ **Team Members** (developers): Add to GitHub, give Supabase creds  
✅ **Deployment**: GitHub main → HuggingFace auto-deploy (free!)  
✅ **Collaboration**: Use branches, pull requests, clear communication  

**Everyone can contribute without friction!** 🌿

---

**Next:** Send your friends the HuggingFace link and watch them use AgriSight! 🎉
