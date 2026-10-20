"""Build split files.

  data/pv_splits.csv  : PlantVillage subset  -> train / val / test (stratified 70/15/15)
  data/pd_test.csv    : PlantDoc images of the SAME classes -> external real-field test set
                        (PlantDoc is never used for training)
  data/classes.json   : ordered class list

Usage:
  python prepare_data.py --pv_root <...> --pd_root <...>
"""
import argparse, csv, json, random
from pathlib import Path
from config import CLASS_MAP, MAX_PER_CLASS, SEED

EXT = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}

def imgs(folder):
    return sorted(p for p in Path(folder).rglob("*") if p.suffix in EXT)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pv_root", required=True)
    ap.add_argument("--pd_root", required=True)
    ap.add_argument("--max_per_class", type=int, default=MAX_PER_CLASS)
    a = ap.parse_args()
    rnd = random.Random(SEED)
    pd_root = Path(a.pd_root)
    pd_dirs = [d for d in (pd_root / "train", pd_root / "test") if d.exists()] or [pd_root]

    classes, pv_rows, pd_rows = [], [], []
    for pv_name, pd_name in CLASS_MAP.items():
        pv_dir = Path(a.pv_root) / pv_name
        pd_files = [f for d in pd_dirs for f in imgs(d / pd_name)]
        if not pv_dir.exists() or not pd_files:
            print(f"[skip] {pv_name}: PlantVillage={pv_dir.exists()} PlantDoc images={len(pd_files)}")
            continue
        idx = len(classes); classes.append(pv_name)
        files = imgs(pv_dir); rnd.shuffle(files); files = files[: a.max_per_class]
        n = len(files); n_tr, n_va = int(0.7 * n), int(0.15 * n)
        for i, f in enumerate(files):
            split = "train" if i < n_tr else "val" if i < n_tr + n_va else "test"
            pv_rows.append((str(f), idx, split))
        for f in pd_files:
            pd_rows.append((str(f), idx, "plantdoc"))
    assert classes, "No classes found - run check_classes.py and fix CLASS_MAP."
    Path("data").mkdir(exist_ok=True)
    for name, rows in (("pv_splits.csv", pv_rows), ("pd_test.csv", pd_rows)):
        with open(f"data/{name}", "w", newline="", encoding="utf8") as fh:
            w = csv.writer(fh); w.writerow(["path", "label", "split"]); w.writerows(rows)
    json.dump(classes, open("data/classes.json", "w"), indent=1)
    from collections import Counter
    c = Counter(s for _, _, s in pv_rows)
    print(f"{len(classes)} classes | PlantVillage {dict(c)} | PlantDoc external test: {len(pd_rows)} images")
    print("PlantDoc images per class:", dict(Counter(classes[l] for _, l, _ in pd_rows)))

if __name__ == "__main__":
    main()
