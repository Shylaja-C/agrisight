# Architecture: AgriSight System Design

## Overview

AgriSight is a multi-stage research pipeline with two distinct modes:

1. **Offline training pipeline** — runs on a GPU (Kaggle recommended), produces trained checkpoints and evaluation results.
2. **Interactive demo app** — runs on any machine with the trained checkpoints, uses Streamlit.

---

## Data Flow

```
┌──────────────────────────────────────────────────────┐
│                  OFFLINE TRAINING                    │
│                                                      │
│  PlantVillage (Kaggle)          PlantDoc (Kaggle)    │
│       │                               │              │
│       │ download_datasets.py          │              │
│       │                     reorganize_plantdoc.py   │
│       │                               │              │
│       │                    YOLO → class folders      │
│       │                               │              │
│       └──────────┬────────────────────┘              │
│                  ▼                                   │
│          check_classes.py                            │
│          (verify CLASS_MAP matches folders)          │
│                  │                                   │
│                  ▼                                   │
│          prepare_data.py                             │
│          → data/pv_splits.csv  (train/val/test)      │
│          → data/pd_test.csv    (PlantDoc test only)  │
│          → data/classes.json   (18 class names)      │
│                  │                                   │
│                  ▼                                   │
│            train.py                                  │
│          → outputs/<run>.pt                          │
│          → outputs/<run>_history.json                │
│                  │                                   │
│                  ▼                                   │
│           evaluate.py                                │
│          → results/<run>.json                        │
│          → results/<run>_plantdoc_cm.png             │
│          → results/<run>_failures/                   │
│                  │                                   │
│           compare.py → results/summary.md            │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│              INTERACTIVE DEMO (Streamlit)            │
│                                                      │
│  User uploads leaf photo                             │
│         │                                            │
│         ▼                                            │
│   pages/scan.py                                      │
│    → models.load_checkpoint(outputs/<run>.pt)        │
│    → gradcam_utils.predict(model, img)               │
│    → gradcam_utils.gradcam_overlay(model, img)       │
│    → gradcam_utils.background_reliance(cam)          │
│         │                                            │
│         ▼                                            │
│   Display: class, confidence, top-3, Grad-CAM        │
│   Flags: low confidence, border attention            │
│   Optional: PDF download (fpdf2)                     │
└──────────────────────────────────────────────────────┘
```

---

## Module-by-Module Reference

### `config.py`
Central configuration file. Defines:
- `IMG_SIZE = 224` — input resolution for all models.
- `SEED = 42` — global random seed for reproducibility.
- `MAX_PER_CLASS = 600` — maximum images taken from PlantVillage per class.
- `CLASS_MAP` — dictionary mapping PlantVillage folder names to PlantDoc folder names for the 18 shared classes. Edit this if folder names differ on your download.

### `models.py`
All model definitions and helpers.
- `BaselineCNN` — four convolutional blocks (Conv→BatchNorm→ReLU→MaxPool), adaptive average pool, dropout(0.3), linear classifier. Trained from scratch.
- `build(name, n_classes, pretrained)` — factory function. Supports `baseline`, `mobilenet_v3`, `efficientnet_b0`, `resnet50`.
- `head_params(m, name)` — returns classifier parameters for stage-1 training.
- `last_block_params(m, name)` — returns last-block parameters unfrozen in stage-2 fine-tuning.
- `target_layer(m, name)` — returns the layer used by Grad-CAM.
- `load_checkpoint(path, device)` — loads a `.pt` file and returns `(model, checkpoint_dict)`.

### `data.py`
Data loading and augmentation.
- `read_csv(path, split)` — reads `pv_splits.csv` or `pd_test.csv`, returns `(path, label_idx)` list.
- `eval_tf()` — evaluation transform: resize to 224×224, to tensor, ImageNet normalise.
- `train_tf(mode)` — training transform. `mode="basic"`: random crop, flip, rotation. `mode="field"`: adds perspective, colour jitter, grayscale, Gaussian blur, random erasing.
- `LeafDS` — PyTorch Dataset wrapper; optionally applies a robustness perturbation.
- `apply_perturbation(img, name)` — PIL-level perturbations: `bright_low`, `bright_high`, `contrast_low`, `blur`, `noise`.
- `PERTURBATIONS` — list of all five perturbation names.

### `train.py`
Two-stage fine-tuning training script.
- Stage 1: freezes the backbone, trains only the classifier head at LR=1e-3.
- Stage 2: unfreezes the last blocks, fine-tunes at LR=1e-4.
- Saves the best checkpoint (highest validation accuracy) to `outputs/<run>.pt`.
- Saves full training history to `outputs/<run>_history.json`.
- Uses class-weighted cross-entropy with label smoothing 0.05 and AdamW with weight decay 1e-4.
- Supports mixed-precision training (AMP) when CUDA is available.

### `evaluate.py`
Evaluation script for a trained checkpoint.
- Evaluates on PlantVillage test split (in-distribution).
- Evaluates on PlantDoc (external, real-field test).
- Computes domain gap = PV accuracy − PlantDoc accuracy.
- Runs all five robustness perturbations on the PV test set.
- Saves `results/<run>.json` with all metrics.
- Saves `results/<run>_plantdoc_cm.png` — confusion matrix.
- Optionally saves `results/<run>_failures/` — Grad-CAM failure examples.

### `compare.py`
Reads all `results/*.json` files and writes `results/summary.md` with a combined Markdown table.

### `prepare_data.py`
Builds the split CSV files consumed by `data.py`.
- Reads `CLASS_MAP` from `config.py`.
- Shuffles PlantVillage images per class using `SEED`, takes up to `MAX_PER_CLASS`.
- Stratified 70/15/15 split.
- Writes PlantDoc images (all splits combined) to `pd_test.csv` — PlantDoc is the external test set only.

### `check_classes.py`
Diagnostic script. Verifies that every key in `CLASS_MAP` exists as a folder in the PlantVillage download and every value exists in the PlantDoc download. Run before `prepare_data.py`.

### `reorganize_plantdoc.py`
Converts PlantDoc from YOLO object-detection format to classification folder structure.
- `YOLO_CLASSES` dictionary maps YOLO class indices (0–29) to class names, matching `data.yaml` from the Kaggle dataset.
- For each image and each bounding box label, crops the box region and saves it to the corresponding class folder.
- All 30 YOLO classes get a folder; only the 18 that appear in `CLASS_MAP` are used downstream.

### `gradcam_utils.py`
Grad-CAM inference helpers.
- `predict(model, img, device)` — returns softmax probability array and input tensor.
- `gradcam_overlay(model, model_name, img, class_idx, device)` — runs GradCAM via `pytorch-grad-cam`, returns an RGB overlay and the raw CAM array.
- `background_reliance(cam, border=0.2)` — computes the fraction of Grad-CAM attention in the outer 20% border of the image. High values suggest the model is attending to the background.

### `download_datasets.py`
Helper script to download both datasets from Kaggle using `kagglehub`. Prints paths and saves them to `dataset_paths.txt`.

### `app.py`
Streamlit entry point. Sets page config, injects CSS, manages session state (page routing, scan history, optional auth), and dispatches to page modules in `pages/`.

### `styles.py`
Injects a custom CSS stylesheet into the Streamlit app. Also provides helper functions `badge(conf)` and `gauge(conf)` that return HTML strings for confidence display.

### `pages/`
Each page is a module with a `render()` function called from `app.py`.
- `home.py` — landing page with project overview.
- `scan.py` — main inference page: upload, model selection, prediction, Grad-CAM, low-confidence flags, PDF download.
- `trust.py` — Model Trust & Transparency: loads `results/*.json`, shows metric cards, bar charts, robustness charts, and confusion matrix images.
- `compare.py` — model comparison view.
- `myfarm.py` — scan history (stored in session state).
- `about.py` — About & Ethics page.

### `portal.py`
Optional farmer portal with Supabase authentication integration. Not required for core functionality; app falls back to guest mode if auth is not configured.

---

## Design Decisions

### Why two augmentation modes?
The key research question is whether field-style augmentation reduces the domain gap. Having a `basic` baseline and a `field` variant lets us isolate the effect of augmentation from other variables.

### Why class-weighted cross-entropy?
PlantVillage has unequal class sizes. Class weighting prevents the model from biasing toward larger classes.

### Why label smoothing 0.05?
Label smoothing discourages overconfident predictions and slightly improves calibration, which matters for the low-confidence flagging feature.

### Why 224×224 input?
Standard ImageNet pre-training resolution. Using a non-standard resolution would invalidate pre-trained weights.

### Why AdamW with weight decay 1e-4?
AdamW decouples weight decay from the adaptive learning rate, which is the standard recommendation for fine-tuning pre-trained models.

### Why is PlantDoc never used for training?
PlantDoc is the external real-field test set. Using it for training would leak information and invalidate the domain-gap measurement. The entire point of the experiment is to test how models trained only on PlantVillage generalise to PlantDoc.

### Why bounding-box crops for PlantDoc?
PlantDoc is distributed as a YOLO object-detection dataset. We crop the labelled bounding boxes to get per-leaf images that match the format of PlantVillage. This introduces a caveat: the crops may include background or miss part of the leaf.
