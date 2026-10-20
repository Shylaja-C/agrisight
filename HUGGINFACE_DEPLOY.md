# 🤗 Deploy to HuggingFace Spaces

Host your Streamlit app for free on HuggingFace!

---

## Step 1: Create HuggingFace Account

1. Go to **https://huggingface.co/join**
2. Sign up (email or GitHub)
3. Verify email

---

## Step 2: Create a Space

1. Go to **https://huggingface.co/spaces**
2. Click **"Create new Space"**
3. Fill in:
   - **Space name**: `agrisight-portal` (or any name)
   - **Space type**: **Streamlit** (important!)
   - **Visibility**: Public (or Private if you prefer)
4. Click **"Create Space"**

You'll be redirected to your new Space!

---

## Step 3: Add Your Code

In your new HuggingFace Space:

### Option A: Upload via Web (Easiest for Quick Start)

1. Click **"Files" tab** (top of page)
2. Click **"Add file"** → **"Upload files"**
3. Upload these files from your `agrisight/` folder:
   - `portal.py`
   - `requirements.txt`
   - `app.py`
   - `models.py`
   - `gradcam_utils.py`
   - `config.py`
   - `data.py`
   - `evaluate.py`
   - `.streamlit/config.toml`

4. Upload `outputs/` folder with all `.pt` files
5. Upload `results/` folder with all results

### Option B: Connect GitHub (Best for Teamwork)

1. In your Space, click **"Files and versions"** tab
2. Click **"Clone repository"**
3. Use this command in terminal:
```bash
git clone https://huggingface.co/spaces/yourusername/agrisight-portal
cd agrisight-portal
git config user.email "you@example.com"
git config user.name "Your Name"
```

4. Copy all files from your local `agrisight/` folder to this folder
5. Push to HuggingFace:
```bash
git add .
git commit -m "Add AgriSight Farmer Portal"
git push origin main
```

6. HuggingFace will auto-detect Streamlit and start building! ✅

---

## Step 4: Add Supabase Secrets (If Using Auth)

If you set up Supabase earlier:

1. In your HuggingFace Space, click **"⚙️ Settings"** (top right)
2. Go to **"Repository secrets"**
3. Add a new secret:
   - **Name**: `SUPABASE_URL`
   - **Value**: Your Supabase URL
4. Add another secret:
   - **Name**: `SUPABASE_KEY`
   - **Value**: Your Anon Key

HuggingFace will automatically load these into `.streamlit/secrets.toml`!

---

## Step 5: Wait for Build

HuggingFace automatically:
1. Installs Python dependencies from `requirements.txt`
2. Runs `streamlit run portal.py`
3. Builds a Docker container
4. Deploys the app (takes 2-5 min)

You'll see a green **"Running"** status when done! ✅

---

## Step 6: Share Your App

Your public URL is:
```
https://huggingface.co/spaces/yourusername/agrisight-portal
```

**Anyone can visit and use it immediately!** No setup needed!

---

## What Your Friends Will See

When they click your link:
1. Browser opens the app
2. They click **"Continue as Guest"**
3. They can immediately scan leaves
4. (If you set up Supabase) They can sign up to save scans

**No installation needed!** 🎉

---

## Update the App (While It's Running)

To push new code:

```bash
# From your local agrisight/ folder
git remote add huggingface https://huggingface.co/spaces/yourusername/agrisight-portal
git push huggingface main
```

HuggingFace will auto-rebuild in ~1 minute!

---

## Troubleshooting

| Problem | Solution |
|---|---|
| "Building" takes >10 min | Models are large (~100 MB). First build is slower. Subsequent deploys are faster. |
| "App crashed" | Check logs: Click **"App logs"** (top right of Space) |
| "Models not found" | Verify all `.pt` files are uploaded to `outputs/` folder |
| Secrets not working | Restart Space: **Settings** → **Restart space** |
| Want to keep app private | In Settings, set **Space visibility** to "Private" |

---

## Resource Limits

**HuggingFace free tier:**
- ✅ CPU: Shared (enough for small team)
- ✅ Storage: 50 GB
- ✅ RAM: 16 GB
- ✅ Public traffic: Unlimited
- ✅ Private traffic: Limited but fine for hackathon

**Upgrade if needed:**
- **Pro membership**: $9/month (persistent GPU, no cooldown)
- **Org subscription**: Custom pricing

For a hackathon demo, **free tier is perfect!** 🚀

---

## For Your Friend

Your friend wants to test your deployed app:

1. **Send them the link**: `https://huggingface.co/spaces/yourusername/agrisight-portal`
2. They click it → App loads in browser
3. They click **"Continue as Guest"**
4. They upload a leaf photo → See prediction + Grad-CAM
5. **Done!** No GitHub, no setup needed!

If they want to edit code, they need to:
1. Fork your GitHub repo
2. Connect to their own HuggingFace Space
3. Make edits → Push → Auto-deploys

---

## Architecture

```
                     Your Local Machine
                     ──────────────────
                            ↓
                         Git Push
                            ↓
                    GitHub (yourusername/agrisight)
                            ↓
                    HuggingFace Spaces (auto-deploy)
                            ↓
         https://huggingface.co/spaces/.../agrisight-portal
                            ↓
              Friend clicks link → App works instantly!
```

---

## Summary

✅ **GitHub**: Stores your code (version control)  
✅ **HuggingFace**: Hosts your app (public URL, free)  
✅ **Supabase**: Stores user data (authentication, scans)  

**Everyone can use it immediately with no setup!** 🌿

Next: Share the HuggingFace link with your team!
