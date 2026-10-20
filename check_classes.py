"""Verify that the class names in config.CLASS_MAP exist in your downloaded datasets.

Usage:
  python check_classes.py --pv_root <PlantVillage color folder> --pd_root <PlantDoc-Dataset folder>
"""
import argparse
from pathlib import Path
from config import CLASS_MAP

def folders(root):
    return sorted(p.name for p in Path(root).iterdir() if p.is_dir())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pv_root", required=True)
    ap.add_argument("--pd_root", required=True, help="folder that contains train/ and test/")
    a = ap.parse_args()
    pv = set(folders(a.pv_root))
    pd_train = Path(a.pd_root) / "train"
    pd = set(folders(pd_train)) if pd_train.exists() else set(folders(a.pd_root))
    print("PlantVillage folders:", len(pv), "| PlantDoc folders:", len(pd))
    ok = 0
    for k, v in CLASS_MAP.items():
        a_ok, b_ok = k in pv, v in pd
        ok += a_ok and b_ok
        print(("OK  " if a_ok and b_ok else "FIX ") + f"{k!r} {'found' if a_ok else 'MISSING'}  <->  {v!r} {'found' if b_ok else 'MISSING'}")
    print(f"\n{ok}/{len(CLASS_MAP)} classes ready.")
    if ok < len(CLASS_MAP):
        print("\nPlantVillage folders:\n ", "\n  ".join(sorted(pv)))
        print("\nPlantDoc folders:\n ", "\n  ".join(sorted(pd)))
        print("\nEdit CLASS_MAP in config.py to match the names above (classes that stay MISSING are skipped).")

if __name__ == "__main__":
    main()
