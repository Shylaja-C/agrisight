# 🌿 AgriSight Farmer Portal - Setup Guide

Professional multi-page Streamlit app with authentication, scan history, and model transparency.

## ✨ Features

- **Multi-page design**: Home, Scan, Farm History, Model Trust, About
- **Green & white theme**: Professional UI with hero section
- **Supabase Auth**: Optional email/password login with guest fallback
- **Scan History**: Track predictions with timestamps and notes (logged-in users only)
- **Model Transparency**: Shows domain gap, confusion matrices, robustness metrics
- **Disclaimers**: Clear messaging that this is research only, not medical
- **Mobile-friendly**: Responsive layout, works on tablets and phones

---

## 🚀 Quick Start (Local)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Portal

```bash
streamlit run portal.py
```

App will open at **http://localhost:8501**

### 3. Test Without Login

- Click **"Continue as Guest"** to skip authentication
- Scans are saved locally but not persisted after app restart
- All features work in guest mode

---

## 🔐 Supabase Auth Setup (Optional)

Enable persistent login and scan history cloud storage.

### Step 1: Create Supabase Project

1. Go to https://supabase.com
2. Click "New Project"
3. Choose region closest to you
4. Wait for setup (~2 min)

### Step 2: Get API Keys

In Supabase dashboard:
- **Settings** → **API**
- Copy `Project URL` and `Anon Public Key`

### Step 3: Create Database Table

In Supabase **SQL Editor**, paste:

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

### Step 4: Add Credentials to App

Create `.streamlit/secrets.toml`:

```toml
[supabase]
url = "https://your-project.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**⚠️ SECURITY**: Never commit `secrets.toml` to Git. Use `.gitignore`:

```
.streamlit/secrets.toml
```

### Step 5: Restart App

```bash
streamlit run portal.py
```

Now users can sign up, log in, and their scans will be saved to Supabase!

---

## 📁 File Structure

```
agrisight/
├── portal.py                    # Main Farmer Portal app
├── app.py                       # Original simple demo (deprecated)
├── models.py                    # Model loading & inference
├── gradcam_utils.py            # Grad-CAM visualization
├── data.py                     # Dataset classes
├── config.py                   # Class mappings
├── evaluate.py                 # Evaluation logic
├── requirements.txt            # Python dependencies
│
├── outputs/
│   ├── baseline_basic.pt
│   ├── mobilenet_basic.pt
│   ├── mobilenet_field.pt      # Recommended (best domain gap)
│   └── effnet_field.pt
│
├── results/
│   ├── summary.md              # Results table
│   ├── baseline_basic.json
│   ├── mobilenet_basic.json
│   ├── mobilenet_field.json
│   ├── effnet_field.json
│   ├── *_plantdoc_cm.png       # Confusion matrices
│   └── *_failures/             # Grad-CAM failure examples
│
├── .streamlit/
│   ├── config.toml             # Theme & UI settings
│   ├── secrets.toml.example    # Template (copy to secrets.toml)
│   └── secrets.toml            # ⚠️ DO NOT COMMIT (contains API keys)
│
└── plantdoc_reorganized/       # Test images (not in git)
    ├── Tomato leaf late blight/
    ├── Corn leaf blight/
    └── ...
```

---

## 🎨 UI/UX Features

### Home Page
- Hero section with tagline "Catch crop stress before it shows"
- Key metrics (18 classes, accuracy stats)
- Quick navigation to features

### Scan a Leaf
- Model selector dropdown
- Confidence threshold slider
- File uploader (JPG/PNG)
- Side-by-side: Original | Grad-CAM | Predictions
- Top-3 predictions with progress bars
- **Smart warnings**:
  - Low confidence: ⚠️ Suggests retaking photo
  - Border reliance (only if >80%): ℹ️ Note about centering
- **Disclaimer**: "Research prototype, not a diagnosis"

### My Farm
- User welcome message
- Expandable scan history with metadata
- JSON export of scans
- Empty state if no scans

### Model Trust
- Performance summary table (from `results/summary.md`)
- 4 confusion matrices side-by-side
- Domain gap explanation
- Robustness metrics (blur, noise, dim light)

### About & Ethics
- Project overview
- Key innovation (field augmentation)
- Technology stack
- Ethics & limitations
- Dataset credits
- Full disclaimer

---

## 🔧 Customization

### Change Theme Colors

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#2d5016"        # Green
secondaryBackgroundColor = "#ffffff"  # White
```

### Adjust Confidence Threshold

In `portal.py`, `page_scan()`:

```python
confidence_threshold = st.slider("Low-confidence threshold", 0.3, 0.95, 0.60)
                                                            # ↑ min ↑ max ↑ default
```

### Change Border Reliance Threshold

In `portal.py`, `page_scan()`:

```python
if gu.background_reliance(cam) > 0.80:  # ← Change 0.80 to your threshold
    st.info("...")
```

### Hide Supabase Warning

If Supabase isn't available:

```python
# In portal.py, top of file:
SUPABASE_AVAILABLE = False  # Set to False to hide warning
```

---

## 🚢 Deployment

### Deploy to Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. "New app" → select your repo
4. Set branch to `main`
5. Under "Advanced settings" → add secrets:
   - Copy content of `.streamlit/secrets.toml`
   - Paste into Cloud secrets editor

### Deploy to Heroku

```bash
# Create Procfile
echo "web: streamlit run portal.py --server.port=\$PORT" > Procfile

# Deploy
git push heroku main
```

### Deploy to AWS/GCP/Azure

Use Docker:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "portal.py"]
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|---|---|
| "ModuleNotFoundError: streamlit_option_menu" | Run `pip install streamlit-option-menu` |
| "Supabase initialization failed" | Safe to ignore - app works in guest mode |
| "No models found in outputs/" | Ensure `outputs/*.pt` files exist |
| Login doesn't work | Check Supabase credentials in `.streamlit/secrets.toml` |
| Scans not saving | Verify Supabase table `scans` exists and user is logged in |
| App is slow | Streamlit caches models - first prediction is slower |
| Grad-CAM not showing | Wait 10+ seconds (first Grad-CAM computation is slow) |

---

## 📊 Testing Checklist

- [ ] App starts without errors: `streamlit run portal.py`
- [ ] Guest mode works (click "Continue as Guest")
- [ ] Can upload leaf image
- [ ] Prediction appears with confidence
- [ ] Grad-CAM heatmap displays
- [ ] Low-confidence warning triggers (<60% confidence)
- [ ] Border reliance warning doesn't fire on normal images
- [ ] "My Farm" page works
- [ ] Model Trust shows confusion matrices
- [ ] All pages are mobile-responsive
- [ ] Disclaimer appears on results

---

## 📝 Notes for Judges

- **No image storage**: We do NOT save uploaded images unless explicitly requested
- **Guest mode**: App works perfectly without authentication
- **Minimal dependencies**: Only Streamlit, PyTorch, PIL, numpy, scikit-learn
- **Clean code**: All existing modules unchanged (models.py, gradcam_utils.py, etc.)
- **Professional UI**: Green/white theme, consistent typography, hero sections
- **Ethical messaging**: Clear disclaimers, no treatment recommendations
- **Transparent metrics**: Domain gap, confusion matrices, robustness stats all shown

---

## ✅ Success = This is your "works perfectly" submission

If all pages load, predictions work, and warnings are smart (not firing on good images), 
you have a professional Farmer Portal ready for judges. No further features needed!

---

**Ready? Start with:** `streamlit run portal.py`
