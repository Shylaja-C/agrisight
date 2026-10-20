"""
AgriSight Training on Kaggle with GPU
======================================

This is a complete notebook template for running AgriSight training on Kaggle.

BEFORE RUNNING:
1. Create a new Kaggle notebook
2. Set Accelerator to GPU (P100 or T4) in Settings
3. Add Input: mohitsingh1804/plantvillage dataset
4. Upload this project's Python files OR clone from your GitHub repo
5. Run cells in order

EXPECTED RUNTIME: ~60 minutes total on GPU
"""

# ============================================================================
# CELL 1: Install Dependencies
# ============================================================================
# %%
!pip install grad-cam -q
print("✓ Dependencies installed")

# ============================================================================
# CELL 2: Setup Paths and Check Datasets
# ============================================================================
# %%
import os
from pathlib import Path

# Kaggle dataset paths
PV_ROOT = "/kaggle/input/plantvillage/PlantVillage/train"
YOLO_PD_ROOT = "/kaggle/input/plantdec"  # if you added andresmgs/plantdec dataset

# Check what's available
print("PlantVillage exists:", os.path.exists(PV_ROOT))
if os.path.exists(PV_ROOT):
    pv_classes = sorted(os.listdir(PV_ROOT))
    print(f"PlantVillage has {len(pv_classes)} class folders")

print("\nPlantDoc YOLO exists:", os.path.exists(YOLO_PD_ROOT))

# ============================================================================
# CELL 3: Reorganize PlantDoc from YOLO Format
# ============================================================================
# %%
# This converts PlantDoc from object detection format to classification format
!python reorganize_plantdoc.py --yolo_root /kaggle/input/plantdec --output plantdoc_reorganized
PD_ROOT = "plantdoc_reorganized"

# ============================================================================
# CELL 4: Verify Class Mappings
# ============================================================================
# %%
!python check_classes.py --pv_root "{PV_ROOT}" --pd_root "{PD_ROOT}"
print("\n✓ All classes should show 'OK'. If not, edit config.py CLASS_MAP")

# ============================================================================
# CELL 5: Prepare Data Splits
# ============================================================================
# %%
!python prepare_data.py --pv_root "{PV_ROOT}" --pd_root "{PD_ROOT}"
print("\n✓ Data splits created:")
!ls -lh data/

# ============================================================================
# CELL 6: Train Baseline CNN (~10 minutes)
# ============================================================================
# %%
!python train.py --model baseline --aug basic --epochs1 10 --epochs2 0 --run baseline_basic --workers 2
print("\n✓ Baseline training complete")

# ============================================================================
# CELL 7: Train MobileNetV3 with Basic Augmentation (~15 minutes)
# ============================================================================
# %%
!python train.py --model mobilenet_v3 --aug basic --epochs1 4 --epochs2 6 --run mobilenet_basic --workers 2
print("\n✓ MobileNet (basic aug) training complete")

# ============================================================================
# CELL 8: Train MobileNetV3 with Field Augmentation (~15 minutes)
# ============================================================================
# %%
# This is the KEY experiment: does field-style augmentation reduce domain gap?
!python train.py --model mobilenet_v3 --aug field --epochs1 4 --epochs2 6 --run mobilenet_field --workers 2
print("\n✓ MobileNet (field aug) training complete")

# ============================================================================
# CELL 9: [OPTIONAL] Train EfficientNet-B0 (~30 minutes)
# ============================================================================
# %%
# Uncomment if you have time:
# !python train.py --model efficientnet_b0 --aug field --epochs1 4 --epochs2 6 --run effnet_field --workers 2
# print("\n✓ EfficientNet training complete")

# ============================================================================
# CELL 10: Evaluate All Models
# ============================================================================
# %%
!python evaluate.py --ckpt outputs/baseline_basic.pt --failures 8 --workers 2
!python evaluate.py --ckpt outputs/mobilenet_basic.pt --failures 8 --workers 2
!python evaluate.py --ckpt outputs/mobilenet_field.pt --failures 8 --workers 2
# !python evaluate.py --ckpt outputs/effnet_field.pt --failures 8 --workers 2  # if you trained it

print("\n✓ Evaluation complete")

# ============================================================================
# CELL 11: Generate Comparison Table
# ============================================================================
# %%
!python compare.py
print("\n" + "="*70)
print("RESULTS SUMMARY")
print("="*70)
!cat results/summary.md

# ============================================================================
# CELL 12: View Sample Results
# ============================================================================
# %%
import json
from pathlib import Path

print("\nDetailed Results:\n")
for result_file in sorted(Path("results").glob("*.json")):
    with open(result_file) as f:
        r = json.load(f)
    print(f"\n{r['run']}:")
    print(f"  Model: {r['model']}, Aug: {r['aug']}")
    print(f"  PlantVillage test: {r['plantvillage_test']['accuracy']:.3f} acc, {r['plantvillage_test']['macro_f1']:.3f} F1")
    print(f"  PlantDoc (field):  {r['plantdoc_test']['accuracy']:.3f} acc, {r['plantdoc_test']['macro_f1']:.3f} F1")
    print(f"  Domain gap: {r['domain_gap_accuracy']:.3f}")

# ============================================================================
# CELL 13: View Confusion Matrix
# ============================================================================
# %%
from IPython.display import Image, display
import glob

print("PlantDoc Confusion Matrices:\n")
for cm_file in sorted(glob.glob("results/*_plantdoc_cm.png")):
    print(f"\n{Path(cm_file).name}:")
    display(Image(cm_file))

# ============================================================================
# CELL 14: View Failure Examples
# ============================================================================
# %%
print("Sample Failure Cases with Grad-CAM:\n")
for run in ["baseline_basic", "mobilenet_basic", "mobilenet_field"]:
    fail_dir = f"results/{run}_failures"
    if Path(fail_dir).exists():
        print(f"\n{run}:")
        for fail_img in sorted(Path(fail_dir).glob("*.png"))[:3]:  # show first 3
            display(Image(str(fail_img)))

# ============================================================================
# CELL 15: Package Results for Download
# ============================================================================
# %%
# Create a zip file with all results and trained models
!zip -r agrisight_results.zip outputs/ results/ data/classes.json data/pv_splits.csv data/pd_test.csv

print("\n" + "="*70)
print("TRAINING COMPLETE!")
print("="*70)
print("\nDownload 'agrisight_results.zip' to your local machine.")
print("Then run the Streamlit demo locally:")
print("  streamlit run app.py")
print("\nPaste the results table from results/summary.md into your final report.")
