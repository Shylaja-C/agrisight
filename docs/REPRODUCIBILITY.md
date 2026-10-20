# Reproducibility Guide

## Environment

| Component | Version / Notes |
|---|---|
| Python | 3.10 or later |
| PyTorch | 2.2.2 (CPU build for inference; use CUDA build on Kaggle) |
| torchvision | 0.17.2 |
| Streamlit | 1.35+ |
| Operating system | Tested on Windows 10/11 and Kaggle Linux |
| Random seed | 42 (set in `config.py`, used in `train.py` and `prepare_data.py`) |

---

## Installing Dependencies

### For local inference and the Streamlit demo (CPU)

```bash
pip install -r requirements.txt
```

This installs the CPU-only PyTorch build. It is suitable for running the demo but very slow for training.

### For Kaggle training (GPU)

The Kaggle notebook environment pre-installs PyTorch with CUDA. You only need to install `grad-cam`:

```bash
pip install grad-cam -q
```

---

## Step-by-Step Reproduction

### Step 0: Clone the repository

```bash
git clone https://github.com/Shylaja-C/agrisight.git
cd agrisight
```

### Step 1: Download datasets

Requires Kaggle API credentials (`~/.kaggle/kaggle.json`).

```bash
pip install kagglehub
python download_datasets.py
```

This prints the download paths. Note them for the next step.

**Kaggle notebook alternative:**

```
Click + Add Data → mohitsingh1804/plantvillage
Click + Add Data → andresmgs/plantdec
```

Paths will be:
```
PlantVillage: /kaggle/input/plantvillage/PlantVillage/train
PlantDoc:     /kaggle/input/plantdec
```

### Step 2: Reorganise PlantDoc from YOLO to classification format

```bash
python reorganize_plantdoc.py \
  --yolo_root <path-to-plantdec-root> \
  --output plantdoc_reorganized
```

This creates `plantdoc_reorganized/<class-name>/` folders with cropped images.  
Expected output: approximately 4,145 total crops for the 18 classes used.

### Step 3: Verify class mappings

```bash
python check_classes.py \
  --pv_root <path-to-PlantVillage/train> \
  --pd_root plantdoc_reorganized
```

All 18 classes should print `OK`. If any print `FIX`, edit `CLASS_MAP` in `config.py` to match the actual folder names.

### Step 4: Prepare data splits

```bash
python prepare_data.py \
  --pv_root <path-to-PlantVillage/train> \
  --pd_root plantdoc_reorganized
```

Creates:
- `data/pv_splits.csv` — 9,833 rows, columns: `path,label,split`
- `data/pd_test.csv` — 4,145 rows
- `data/classes.json` — 18 class names

### Step 5: Train models

**Recommended: run on Kaggle GPU (P100 or T4). See `docs/kaggle_notebook_template.md`.**

#### Baseline CNN (from scratch)
```bash
python train.py \
  --model baseline \
  --aug basic \
  --epochs1 10 \
  --epochs2 0 \
  --run baseline_basic
```

#### MobileNetV3 — basic augmentation
```bash
python train.py \
  --model mobilenet_v3 \
  --aug basic \
  --epochs1 4 \
  --epochs2 6 \
  --run mobilenet_basic
```

#### MobileNetV3 — field augmentation (key experiment)
```bash
python train.py \
  --model mobilenet_v3 \
  --aug field \
  --epochs1 4 \
  --epochs2 6 \
  --run mobilenet_field
```

#### EfficientNet-B0 — field augmentation
```bash
python train.py \
  --model efficientnet_b0 \
  --aug field \
  --epochs1 4 \
  --epochs2 6 \
  --run effnet_field
```

### Step 6: Evaluate all models

```bash
python evaluate.py --ckpt outputs/baseline_basic.pt   --failures 8
python evaluate.py --ckpt outputs/mobilenet_basic.pt  --failures 8
python evaluate.py --ckpt outputs/mobilenet_field.pt  --failures 8
python evaluate.py --ckpt outputs/effnet_field.pt     --failures 8
```

Each call creates:
- `results/<run>.json`
- `results/<run>_plantdoc_cm.png`
- `results/<run>_failures/` (8 failure examples with Grad-CAM)

### Step 7: Generate summary table

```bash
python compare.py
cat results/summary.md
```

### Step 8: Run the demo

```bash
streamlit run app.py
```

---

## Expected Runtimes

| Task | Kaggle GPU (T4/P100) | Local CPU |
|---|---|---|
| Reorganise PlantDoc | ~2 min | ~5 min |
| Baseline training (10 epochs) | ~10 min | ~3 hours |
| MobileNet training (4+6 epochs) | ~15 min | ~5 hours |
| EfficientNet training (4+6 epochs) | ~30 min | ~8+ hours |
| Full pipeline | ~60 min | 16+ hours |

**CPU training is not recommended.** Use Kaggle free GPU tier.

---

## Kaggle GPU Notes

1. Create a new notebook at [kaggle.com/code](https://kaggle.com/code).
2. Settings → Accelerator → GPU P100 or T4.
3. Settings → Internet → On.
4. Add datasets via **+ Add Data**.
5. Upload `.py` files or clone the repo with `!git clone <url>`.
6. Run cells from `docs/kaggle_notebook_template.md`.
7. Download results: `!zip -r agrisight_results.zip outputs/ results/`

---

## Troubleshooting

### "No such file or directory" when running `prepare_data.py`
Verify the `--pv_root` path points to the `PlantVillage/train` folder (the one containing class subfolders like `Tomato___Early_blight`).

### Training hangs at 0% on Windows
Add `--workers 0` to the `train.py` command. PyTorch multiprocessing can hang on Windows with the default DataLoader settings.

```bash
python train.py --model mobilenet_v3 --aug field --run mobilenet_field --workers 0
```

### "CUDA out of memory" on Kaggle
Reduce batch size: `--bs 16` or `--bs 8`.

### Streamlit app shows "No model checkpoints found"
The `outputs/` folder must contain at least one `.pt` file. Either train a model or copy the trained checkpoints from the Kaggle notebook download.

### `reorganize_plantdoc.py` prints "Warning: no label for ..."
Some images in the YOLO dataset do not have corresponding label files. These are skipped; this is harmless.

### `check_classes.py` shows `FIX` for some classes
The PlantDoc Kaggle dataset folder names may differ from the values in `CLASS_MAP` in `config.py`. Edit the right-hand side of `CLASS_MAP` to match the actual folder names shown by `check_classes.py`. Classes that cannot be matched will be skipped.

### PyYAML not found
Add `PyYAML` to requirements or install it: `pip install PyYAML`. It is already included in `requirements.txt`.

---

## Seeds and Determinism

- `config.SEED = 42` is used for all random shuffles in `prepare_data.py`.
- `torch.manual_seed(42)` is set at the start of `train.py`.
- PyTorch does not guarantee bit-exact reproducibility across different hardware or CUDA versions.
- The data splits (`pv_splits.csv`, `pd_test.csv`) are deterministic given the same seed and dataset version.
