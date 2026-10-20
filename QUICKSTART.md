# AgriSight: Quick Start Guide

## Your Setup: No GPU Detected

Training deep learning models on CPU is **very slow** (10-20x slower than GPU). Here are your options:

---

## Option 1: Train on Kaggle (RECOMMENDED — Free GPU)

Kaggle provides free GPU access (P100 or T4). This is the fastest way to train all models.

### Steps:

1. **Create a Kaggle account** at [kaggle.com](https://kaggle.com)

2. **Create a new notebook**:
   - Go to https://www.kaggle.com/code
   - Click "New Notebook"
   - Settings → Accelerator → **GPU P100** or **GPU T4**

3. **Add datasets** (click "+ Add Data" button):
   - Search "mohitsingh1804/plantvillage" → Add
   - You'll also need PlantDoc — either:
     - Upload the `plantdoc_reorganized/` folder you created (File → Upload)
     - OR run the reorganization script on Kaggle

4. **Upload your code**:
   - Upload all `.py` files from your local project
   - OR clone this repo directly in Kaggle

5. **Run the pipeline**:

```python
# Cell 1: Install dependencies
!pip install grad-cam -q

# Cell 2: Check paths
import os
pv_path = "/kaggle/input/plantvillage/PlantVillage/train"
pd_path = "/kaggle/working/plantdoc_reorganized"  # or your uploaded path

print("PlantVillage exists:", os.path.exists(pv_path))
print("PlantDoc exists:", os.path.exists(pd_path))

# Cell 3: Run pipeline
!python check_classes.py --pv_root "{pv_path}" --pd_root "{pd_path}"
!python prepare_data.py --pv_root "{pv_path}" --pd_root "{pd_path}"

# Cell 4: Train baseline (~10 min on GPU)
!python train.py --model baseline --aug basic --epochs1 10 --epochs2 0 --run baseline_basic

# Cell 5: Train MobileNet with basic aug (~15 min)
!python train.py --model mobilenet_v3 --aug basic --epochs1 4 --epochs2 6 --run mobilenet_basic

# Cell 6: Train MobileNet with field aug (~15 min) ← KEY EXPERIMENT
!python train.py --model mobilenet_v3 --aug field --epochs1 4 --epochs2 6 --run mobilenet_field

# Cell 7: Optional - EfficientNet (slower, ~30 min)
# !python train.py --model efficientnet_b0 --aug field --epochs1 4 --epochs2 6 --run effnet_field

# Cell 8: Evaluate all models
!python evaluate.py --ckpt outputs/baseline_basic.pt --failures 8
!python evaluate.py --ckpt outputs/mobilenet_basic.pt --failures 8
!python evaluate.py --ckpt outputs/mobilenet_field.pt --failures 8

# Cell 9: Generate comparison table
!python compare.py
!cat results/summary.md
```

6. **Download results**:
   - Right-click on `outputs/` folder → Download
   - Right-click on `results/` folder → Download
   - Transfer to your local machine for the Streamlit demo

---

## Option 2: Minimal Local Demo (No Training)

If you just want to see the app working, you can:

1. **Use pre-trained ImageNet models** (no crop disease training, just for testing the interface):

```python
# Create a dummy checkpoint for demo purposes
import torch
from torchvision import models

model = models.mobilenet_v3_large(weights="DEFAULT")
model.classifier[-1] = torch.nn.Linear(model.classifier[-1].in_features, 18)

# Dummy class names
classes = ["Tomato_Disease_1", "Tomato_Disease_2", "Potato_Disease_1", "Corn_Disease_1",
           "Apple_Disease_1", "Grape_Disease_1", "Pepper_Disease_1", "Healthy_Leaf",
           "Tomato_Disease_3", "Tomato_Disease_4", "Potato_Disease_2", "Corn_Disease_2",
           "Apple_Disease_2", "Apple_Healthy", "Bell_Pepper_Spot", "Bell_Pepper_Healthy",
           "Tomato_Mosaic", "Tomato_TYLCV"]

torch.save({
    "model": "mobilenet_v3",
    "classes": classes,
    "state_dict": model.state_dict(),
    "aug": "basic",
    "val_acc": 0.0
}, "outputs/demo_model.pt")

print("✓ Created outputs/demo_model.pt")
print("\nRun: streamlit run app.py")
print("(Note: predictions will be random since this model isn't trained on plant diseases)")
```

Save this as `create_demo_checkpoint.py` and run it, then:

```bash
python create_demo_checkpoint.py
streamlit run app.py
```

---

## Option 3: Train Locally with Reduced Settings (SLOW)

If you must train locally:

```bash
# Use smaller subset and fewer epochs
python prepare_data.py --pv_root "C:\Users\91744\.cache\kagglehub\datasets\mohitsingh1804\plantvillage\versions\1\PlantVillage\train" --pd_root "plantdoc_reorganized" --max_per_class 200

# Train baseline only (fastest, ~2-3 hours on CPU)
python train.py --model baseline --aug basic --epochs1 5 --epochs2 0 --run baseline_basic --workers 0 --bs 16
```

**Warning**: This will still take hours and results will be worse due to limited data.

---

## Recommended Workflow for the Hackathon

1. ✓ You've already prepared the datasets locally
2. **Train on Kaggle** (30-60 min total with GPU)
3. **Download** `outputs/*.pt` and `results/*.json` to local
4. **Run Streamlit demo locally**: `streamlit run app.py`
5. **Create presentation** with results from `results/summary.md`

---

## Dataset Paths Summary

Your local paths:
```
PlantVillage: C:\Users\91744\.cache\kagglehub\datasets\mohitsingh1804\plantvillage\versions\1\PlantVillage\train
PlantDoc:     plantdoc_reorganized/
```

Kaggle paths (typical):
```
PlantVillage: /kaggle/input/plantvillage/PlantVillage/train
PlantDoc:     /kaggle/working/plantdoc_reorganized/
```

---

## Time Estimates

| Task | CPU (local) | GPU (Kaggle) |
|---|---|---|
| Baseline training | ~3 hours | ~10 min |
| MobileNet training | ~5 hours | ~15 min |
| EfficientNet training | ~8 hours | ~30 min |
| **Total pipeline** | **16+ hours** | **60 min** |

**→ Use Kaggle for training, local machine for demo and presentation.**
