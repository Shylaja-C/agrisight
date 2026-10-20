"""Download PlantVillage and PlantDoc datasets using kagglehub.

Usage:
  python download_datasets.py

This will download both datasets and print their paths for use in subsequent steps.
"""
import kagglehub

print("Downloading PlantVillage dataset...")
pv_path = kagglehub.dataset_download("mohitsingh1804/plantvillage")
print(f"PlantVillage downloaded to: {pv_path}")

print("\nDownloading PlantDoc dataset...")
pd_path = kagglehub.dataset_download("andresmgs/plantdec")
print(f"PlantDoc downloaded to: {pd_path}")

print("\n" + "="*70)
print("NEXT STEPS:")
print("="*70)
print("\n1. Check class names:")
print(f"   python check_classes.py --pv_root \"{pv_path}/color\" --pd_root \"{pd_path}\"")
print("\n2. Prepare data splits:")
print(f"   python prepare_data.py --pv_root \"{pv_path}/color\" --pd_root \"{pd_path}\"")
print("\n3. Train models (examples):")
print("   python train.py --model baseline --aug basic --epochs1 10 --epochs2 0 --run baseline_basic")
print("   python train.py --model mobilenet_v3 --aug basic --run mobilenet_basic")
print("   python train.py --model mobilenet_v3 --aug field --run mobilenet_field")
print("\n4. Evaluate:")
print("   python evaluate.py --ckpt outputs/mobilenet_field.pt --failures 8")
print("\n5. Compare all results:")
print("   python compare.py")
print("\n6. Run demo:")
print("   streamlit run app.py")
print("="*70)

# Save paths to a file for easy reference
with open("dataset_paths.txt", "w") as f:
    f.write(f"PLANTVILLAGE_PATH={pv_path}/color\n")
    f.write(f"PLANTDOC_PATH={pd_path}\n")

print("\nDataset paths saved to dataset_paths.txt for your reference.")
