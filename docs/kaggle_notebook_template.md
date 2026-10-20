"""
AgriSight Training on Kaggle with GPU
======================================

Copy each section below as a separate cell in a Kaggle notebook.

BEFORE RUNNING:
1. Create a new Kaggle notebook.
2. Set Accelerator to GPU (P100 or T4) in Settings.
3. Add Input datasets:
   - mohitsingh1804/plantvillage
   - andresmgs/plantdec
4. Upload the project .py files via the file upload panel,
   OR run: !git clone <your-repo-url> and cd into the folder.
5. Run cells in order.

EXPECTED RUNTIME: approximately 60 minutes total on T4 GPU.
"""

# ============================================================================
# CELL 1: Install grad-cam (PyTorch is already available on Kaggle)
# ============================================================================
# %%
# !pip install grad-cam -q
# print("Dependencies installed")

# ============================================================================
# CELL 2: Set paths and verify dataset availability
# ============================================================================
# %%
# import os
# PV_ROOT    = "/kaggle/input/plantvillage/PlantVillage/train"
# PD_YOLO    = "/kaggle/input/plantdec"
# print("PlantVillage exists:", os.path.exists(PV_ROOT))
# print("PlantDoc YOLO exists:", os.path.exists(PD_YOLO))

# ============================================================================
# CELL 3: Convert PlantDoc from YOLO to classification folder structure
# ============================================================================
# %%
# !python reorganize_plantdoc.py --yolo_root /kaggle/input/plantdec --output plantdoc_reorganized
# PD_ROOT = "plantdoc_reorganized"

# ============================================================================
# CELL 4: Verify class mappings against downloaded datasets
# ============================================================================
# %%
# !python check_classes.py --pv_root "{PV_ROOT}" --pd_root "{PD_ROOT}"
# # All 18 lines should print OK. If any print FIX, edit config.py CLASS_MAP.

# ============================================================================
# CELL 5: Prepare data splits
# ============================================================================
# %%
# !python prepare_data.py --pv_root "{PV_ROOT}" --pd_root "{PD_ROOT}"
# # Creates: data/pv_splits.csv, data/pd_test.csv, data/classes.json

# ============================================================================
# CELL 6: Train baseline CNN from scratch (~10 min on GPU)
# ============================================================================
# %%
# !python train.py --model baseline --aug basic --epochs1 10 --epochs2 0 --run baseline_basic --workers 2

# ============================================================================
# CELL 7: Train MobileNetV3-Large with basic augmentation (~15 min)
# ============================================================================
# %%
# !python train.py --model mobilenet_v3 --aug basic --epochs1 4 --epochs2 6 --run mobilenet_basic --workers 2

# ============================================================================
# CELL 8: Train MobileNetV3-Large with field augmentation (~15 min)
#          This is the key experiment: does field-style augmentation reduce domain gap?
# ============================================================================
# %%
# !python train.py --model mobilenet_v3 --aug field --epochs1 4 --epochs2 6 --run mobilenet_field --workers 2

# ============================================================================
# CELL 9: Train EfficientNet-B0 with field augmentation (~30 min) [optional]
# ============================================================================
# %%
# !python train.py --model efficientnet_b0 --aug field --epochs1 4 --epochs2 6 --run effnet_field --workers 2

# ============================================================================
# CELL 10: Evaluate all trained models
# ============================================================================
# %%
# !python evaluate.py --ckpt outputs/baseline_basic.pt  --failures 8 --workers 2
# !python evaluate.py --ckpt outputs/mobilenet_basic.pt --failures 8 --workers 2
# !python evaluate.py --ckpt outputs/mobilenet_field.pt --failures 8 --workers 2
# !python evaluate.py --ckpt outputs/effnet_field.pt    --failures 8 --workers 2

# ============================================================================
# CELL 11: Generate summary table
# ============================================================================
# %%
# !python compare.py
# !cat results/summary.md

# ============================================================================
# CELL 12: View confusion matrices
# ============================================================================
# %%
# from IPython.display import Image, display
# import glob
# for f in sorted(glob.glob("results/*_plantdoc_cm.png")):
#     print(f)
#     display(Image(f))

# ============================================================================
# CELL 13: Package results for download
# ============================================================================
# %%
# !zip -r agrisight_results.zip outputs/ results/ data/classes.json
# # Download agrisight_results.zip from the Kaggle output panel.
# # Extract it into your local agrisight/ folder, then:
# #   streamlit run app.py
