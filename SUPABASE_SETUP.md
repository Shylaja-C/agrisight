# 🔐 Supabase Auth Setup for AgriSight

Enable persistent login and cloud-based scan history.

---

## Step 1: Create Supabase Project

1. Go to **https://supabase.com**
2. Click **"New Project"**
3. Choose:
   - **Organization**: Create one or select existing
   - **Project name**: `agrisight` or `agrisight-demo`
   - **Database password**: Create a strong one (save it!)
   - **Region**: Pick closest to you
4. Click **"Create new project"** and wait 2-3 minutes

---

## Step 2: Get Your API Keys

Once project is created:

1. Go to **Settings** (bottom left) → **API**
2. Copy these two values:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **Anon Public** (long string starting with `eyJhbGc...`)

**⚠️ SAVE THESE - You'll need them in 2 minutes!**

---

## Step 3: Create Database Table

In Supabase:

1. Go to **SQL Editor** (left sidebar)
2. Click **"New Query"**
3. Paste this exact code:

```sql
CREATE TABLE scans (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  crop_class TEXT NOT NULL,
  confidence FLOAT NOT NULL,
  notes TEXT,
  model TEXT,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE scans ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own scans
CREATE POLICY "Users can view own scans" ON scans
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own scans" ON scans
  FOR INSERT WITH CHECK (auth.uid() = user_id);
```

4. Click **"Run"** (green play button)
5. You should see: **Success!**

---

## Step 4: Add Secrets to Your Local App

In your `agrisight/` folder:

1. Open `.streamlit/secrets.toml` (or create it if missing)
2. Add:

```toml
[supabase]
url = "https://xxxxx.supabase.co"
key = "eyJhbGc..."
```

**Replace** with your actual values from Step 2!

3. **Save the file**

4. **⚠️ IMPORTANT**: Add to `.gitignore` so secrets never go public:

```bash
echo ".streamlit/secrets.toml" >> .gitignore
git add .gitignore
git commit -m "Ignore Supabase secrets"
git push
```

---

## Step 5: Restart Streamlit & Test

```bash
streamlit run portal.py
```

Now:
1. Click **"Sign Up"** (instead of "Continue as Guest")
2. Enter email and password
3. Click **"Sign Up"**
4. **Login** with those credentials
5. Go to **"Scan a Leaf"** → Upload image → Click **"Save Scan"**
6. Go to **"My Farm"** → You should see your scan saved! ✅

---

## Verify in Supabase

In Supabase dashboard:

1. Go to **Table Editor** → **scans**
2. You should see your scan row with:
   - user_id
   - crop_class
   - confidence
   - created_at

**Congratulations! Supabase auth is working!** 🎉

---

## For Your Friend

Your friend needs to:

1. Clone your repo from GitHub:
```bash
git clone https://github.com/yourusername/agrisight
cd agrisight
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create their own `.streamlit/secrets.toml` with the **SAME Supabase credentials**:
```toml
[supabase]
url = "https://xxxxx.supabase.co"
key = "eyJhbGc..."
```

4. Run the app:
```bash
streamlit run portal.py
```

5. They can sign up with their own email and scans will go to the **same Supabase database**!

---

## Troubleshooting

| Problem | Solution |
|---|---|
| "Supabase initialization failed" | Check `.streamlit/secrets.toml` has correct URL and key |
| "Auth doesn't work" | Restart Streamlit: `streamlit run portal.py` |
| "Scans not saving" | Check Supabase `scans` table exists (run the SQL query again) |
| Friend can't see my scans | This is correct! Row Level Security means users only see their own |
| "Invalid token" | Check key hasn't expired (regenerate in Supabase Settings) |

---

## Security Best Practices

✅ **DO:**
- Keep `secrets.toml` in `.gitignore` (never commit!)
- Use strong database password
- Share only Supabase URL + Anon Key (not database password)

❌ **DON'T:**
- Commit `secrets.toml` to Git
- Share database password
- Use the same key for multiple apps
- Store user images in Supabase (we don't)

---

## All Set!

Your app now has:
- ✅ User authentication (email + password)
- ✅ Persistent scan history (cloud stored)
- ✅ Multi-user support (each user sees only their scans)
- ✅ Team collaboration ready

**Next: Deploy to HuggingFace!** 🚀
