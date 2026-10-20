# AgriSight: Complete Run Instructions

## Current Status ✓

You have successfully:
- ✅ Downloaded PlantVillage dataset (via kagglehub)
- ✅ Downloaded PlantDoc dataset (via kagglehub)
- ✅ Reorganized PlantDoc from YOLO to classification format
- ✅ Verified all 18 classes match between datasets
- ✅ Prepared data splits (6,882 train / 1,473 val / 1,478 test from PlantVillage; 3,949 external test from PlantDoc)
- ✅ Created demo checkpoint for testing Streamlit app

## ⚠️ Important: No GPU Detected

Training on CPU will take **10-20 hours**. Training on GPU (Kaggle) takes **~60 minutes**.

**RECOMMENDED: Use Kaggle for training** (see Option A below).

---

## Option A: Train on Kaggle with GPU (RECOMMENDED)

### Why Kaggle?
- **Free GPU access** (P100 or T4)
- **~60 minutes total** vs 10-20 hours on CPU
- **No setup** required (pre-installed Python, PyTorch, etc.)

### Steps:

#### 1. Prepare for Upload

You need to upload these files to Kaggle (or clone your repo):
```
├── check_classes.py
├── compare.py
├── config.py
├── data.py
├── evaluate.py
├── gradcam_utils.py
├── models.py
├── prepare_data.py
├── reorganize_plantdoc.py
├── train.py
```

**Option 1**: Upload files manually to Kaggle notebook
**Option 2**: Push to GitHub and clone in Kaggle

#### 2. Create Kaggle Notebook

1. Go to https://www.kaggle.com/code
2. Click "+ New Notebook"
3. **Settings** → Accelerator → **GPU P100** or **GPU T4**
4. **Session Options** → Internet → **On**

#### 3. Add Datasets

Click "+ Add Data" in the right sidebar:
- Search "mohitsingh1804/plantvillage" → Add
- Search "andresmgs/plantdec" → Add

#### 4. Upload Project Files

- Click the three dots (⋮) → File → Upload
- Upload all `.py` files listed above
- OR: Run `!git clone <your-repo-url>` in a cell

#### 5. Run Training

Use the pre-made notebook template. Copy cells from `kaggle_training_notebook.py`:

```python
# Cell 1: Install
!pip install grad-cam -q

# Cell 2: Setup paths
PV_ROOT = "/kaggle/input/plantvillage/PlantVillage/train"
PD_YOLO = "/kaggle/input/plantdec"

# Cell 3: Reorganize PlantDoc
!python reorganize_plantdoc.py --yolo_root {PD_YOLO} --output plantdoc_reorganized

# Cell 4: Verify classes
!python check_classes.py --pv_root {PV_ROOT} --pd_root plantdoc_reorganized

# Cell 5: Prepare splits
!python prepare_data.py --pv_root {PV_ROOT} --pd_root plantdoc_reorganized

# Cell 6-8: Train models (~40 min total)
!python train.py --model baseline --aug basic --epochs1 10 --epochs2 0 --run baseline_basic
!python train.py --model mobilenet_v3 --aug basic --run mobilenet_basic
!python train.py --model mobilenet_v3 --aug field --run mobilenet_field

# Cell 9-10: Evaluate and compare
!python evaluate.py --ckpt outputs/baseline_basic.pt --failures 8
!python evaluate.py --ckpt outputs/mobilenet_basic.pt --failures 8
!python evaluate.py --ckpt outputs/mobilenet_field.pt --failures 8
!python compare.py
!cat results/summary.md
```

#### 6. Download Results

After training completes:
```python
# Package everything
!zip -r agrisight_results.zip outputs/ results/
```

- Click the three dots (⋮) next to `agrisight_results.zip` → Download
- Extract to your local `agrisight/` folder

#### 7. Run Demo Locally

```bash
streamlit run app.py
```

---

## Option B: Test Demo Locally (No Training)

To test the Streamlit app interface without real training:

```bash
# 1. Create demo checkpoint (already done)
# The file outputs/demo_untrained.pt exists

# 2. Run Streamlit
streamlit run app.py

# 3. Upload any leaf image
# Note: Predictions will be random/wrong since the model isn't trained
```

This lets you:
- ✅ Test the app interface
- ✅ See Grad-CAM visualizations
- ✅ Check low-confidence warnings
- ❌ Get accurate disease predictions (not trained)

---

## Option C: Train Locally on CPU (SLOW)

**Only if you cannot use Kaggle**

Expected time: **10-20 hours total**

### Reduce Data to Speed Up

```bash
# Use fewer images per class
python prepare_data.py \
  --pv_root "C:\Users\91744\.cache\kagglehub\datasets\mohitsingh1804\plantvillage\versions\1\PlantVillage\train" \
  --pd_root "plantdoc_reorganized" \
  --max_per_class 200
```

### Train Baseline Only (Fastest)

```bash
python train.py \
  --model baseline \
  --aug basic \
  --epochs1 5 \
  --epochs2 0 \
  --run baseline_basic \
  --workers 0 \
  --bs 16
```

**Expected time**: ~2-3 hours on CPU

### Skip MobileNet/EfficientNet

Training pretrained models on CPU is extremely slow. Focus on baseline for proof-of-concept.

---

## Full Pipeline Reference

For completeness, here's the full workflow you've already partially completed:

```bash
# 1. ✅ Download datasets (already done via kagglehub)
python download_datasets.py

# 2. ✅ Reorganize PlantDoc (already done)
python reorganize_plantdoc.py \
  --yolo_root "C:\Users\91744\.cache\kagglehub\datasets\andresmgs\plantdec\versions\7" \
  --output "plantdoc_reorganized"

# 3. ✅ Verify class mappings (already done)
python check_classes.py \
  --pv_root "C:\Users\91744\.cache\kagglehub\datasets\mohitsingh1804\plantvillage\versions\1\PlantVillage\train" \
  --pd_root "plantdoc_reorganized"

# 4. ✅ Prepare data splits (already done)
python prepare_data.py \
  --pv_root "C:\Users\91744\.cache\kagglehub\datasets\mohitsingh1804\plantvillage\versions\1\PlantVillage\train" \
  --pd_root "plantdoc_reorganized"

# 5. ⏳ Train models (do on Kaggle)
python train.py --model baseline --aug basic --epochs1 10 --epochs2 0 --run baseline_basic
python train.py --model mobilenet_v3 --aug basic --run mobilenet_basic
python train.py --model mobilenet_v3 --aug field --run mobilenet_field
python train.py --model efficientnet_b0 --aug field --run effnet_field  # optional

# 6. ⏳ Evaluate (do on Kaggle)
python evaluate.py --ckpt outputs/baseline_basic.pt --failures 8
python evaluate.py --ckpt outputs/mobilenet_basic.pt --failures 8
python evaluate.py --ckpt outputs/mobilenet_field.pt --failures 8

# 7. ⏳ Compare results (do on Kaggle)
python compare.py

# 8. ✅ Run demo (locally after downloading trained models)
streamlit run app.py
```

---

## File Structure After Complete Run

```
agrisight/
├── data/
│   ├── classes.json           # 18 class names
│   ├── pv_splits.csv          # PlantVillage train/val/test
│   └── pd_test.csv            # PlantDoc external test
├── outputs/
│   ├── baseline_basic.pt      # Trained models
│   ├── mobilenet_basic.pt
│   ├── mobilenet_field.pt
│   └── *_history.json         # Training curves
├── results/
│   ├── baseline_basic.json    # Evaluation metrics
│   ├── mobilenet_basic.json
│   ├── mobilenet_field.json
│   ├── *_plantdoc_cm.png      # Confusion matrices
│   ├── *_failures/            # Grad-CAM failure examples
│   └── summary.md             # FINAL RESULTS TABLE
├── plantdoc_reorganized/      # PlantDoc in classification format
│   ├── Apple Scab Leaf/
│   ├── Tomato Early blight leaf/
│   └── ... (29 class folders)
└── *.py                       # Your code files
```

---

## Expected Results

After training, `results/summary.md` will contain something like:

| Run | Model | Aug | PV acc | PV F1 | PlantDoc acc | PlantDoc F1 | Gap | 
|---|---|---|---|---|---|---|---|
| baseline_basic | baseline | basic | 0.750 | 0.730 | 0.320 | 0.290 | 0.430 |
| mobilenet_basic | mobilenet_v3 | basic | 0.935 | 0.920 | 0.450 | 0.410 | 0.485 |
| mobilenet_field | mobilenet_v3 | field | 0.910 | 0.895 | 0.580 | 0.540 | 0.330 |

**Key finding**: The `mobilenet_field` run (with aggressive augmentation) should have a **smaller domain gap** than `mobilenet_basic`, proving that field-style augmentation helps models generalize from lab to real-world images.

---

## Troubleshooting

### "No such file or directory" errors
→ Check dataset paths match your system. Use absolute paths.

### "CUDA out of memory" on Kaggle
→ Reduce `--bs` (batch size) from 32 to 16 or 8.

### Training hangs at 0%
→ Add `--workers 0` on Windows.

### Streamlit app shows blank predictions
→ You need trained `.pt` files in `outputs/`. Use Kaggle to train, or use the demo checkpoint.

### "unknown_29" errors during PlantDoc reorganization
→ Expected and harmless (class 29 doesn't exist in the mapping).

---

## Next Steps for Hackathon

1. **Train on Kaggle** (60 minutes)
2. **Download** trained models and results
3. **Run demo** locally: `streamlit run app.py`
4. **Create presentation** using:
   - `results/summary.md` table
   - `results/*_plantdoc_cm.png` confusion matrices
   - `results/*_failures/` Grad-CAM examples
   - Screenshots from Streamlit demo
5. **Write report** covering:
   - Problem: domain gap between lab and field images
   - Method: field-style augmentation to bridge the gap
   - Results: quantify domain gap reduction
   - Error analysis: why do models still fail on PlantDoc?

---

## Contact

For questions or issues, check:
- `README.md` for project overview
- `QUICKSTART.md` for GPU vs CPU decision
- `kaggle_training_notebook.py` for notebook template
