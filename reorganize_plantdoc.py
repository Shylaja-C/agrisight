"""Reorganize PlantDoc from YOLO format to folder-per-class structure.

The Kaggle PlantDoc dataset (andresmgs/plantdec) is in YOLO object detection format,
but the AgriSight code expects classification format with images organized in class subfolders.

This script reads the YOLO labels, extracts bounding boxes, crops to create
classification images, and organizes them by class name.

Usage:
  python reorganize_plantdoc.py --yolo_root <path to YOLO dataset> --output <output folder>
"""
import argparse, shutil
from pathlib import Path
from PIL import Image

# YOLO class index -> class name mapping (from data.yaml)
YOLO_CLASSES = {
    0: "Apple leaf",
    1: "Apple Scab Leaf",
    2: "Apple rust leaf",
    3: "Bell_pepper leaf",
    4: "Bell_pepper leaf spot",
    5: "Blueberry leaf",
    6: "Cherry leaf",
    7: "Corn Gray leaf spot",
    8: "Corn leaf blight",
    9: "Corn rust leaf",
    10: "Peach leaf",
    11: "Potato leaf",
    12: "Potato leaf early blight",
    13: "Potato leaf late blight",
    14: "Raspberry leaf",
    15: "Soyabean leaf",
    16: "Soybean leaf",
    17: "Squash Powdery mildew leaf",
    18: "Strawberry leaf",
    19: "Tomato Early blight leaf",
    20: "Tomato leaf",
    21: "Tomato leaf bacterial spot",
    22: "Tomato leaf late blight",
    23: "Tomato leaf mosaic virus",
    24: "Tomato leaf yellow virus",
    25: "Tomato mold leaf",
    26: "Tomato Septoria leaf spot",
    27: "Tomato two spotted spider mites leaf",
    28: "grape leaf black rot",
}

def yolo_to_bbox(img_w, img_h, yolo_line):
    """Convert YOLO format (class x_center y_center width height) to pixel bbox."""
    parts = yolo_line.strip().split()
    if len(parts) < 5:
        return None, None
    class_id = int(parts[0])
    x_center, y_center, w, h = map(float, parts[1:5])
    
    # Convert from normalized [0,1] to pixel coordinates
    x_center_px = x_center * img_w
    y_center_px = y_center * img_h
    w_px = w * img_w
    h_px = h * img_h
    
    x1 = max(0, int(x_center_px - w_px / 2))
    y1 = max(0, int(y_center_px - h_px / 2))
    x2 = min(img_w, int(x_center_px + w_px / 2))
    y2 = min(img_h, int(y_center_px + h_px / 2))
    
    return class_id, (x1, y1, x2, y2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--yolo_root", required=True, help="Path to YOLO dataset (contains train/ test/)")
    ap.add_argument("--output", default="plantdoc_reorganized", help="Output folder for reorganized dataset")
    args = ap.parse_args()
    
    yolo_root = Path(args.yolo_root)
    output_root = Path(args.output)
    output_root.mkdir(exist_ok=True)
    
    # Create class folders
    for class_name in YOLO_CLASSES.values():
        (output_root / class_name).mkdir(exist_ok=True)
    
    total_crops = 0
    
    # Process train and test splits
    for split in ["train", "test"]:
        img_dir = yolo_root / split / "images"
        lbl_dir = yolo_root / split / "labels"
        
        if not img_dir.exists():
            print(f"Skipping {split}: {img_dir} not found")
            continue
        
        print(f"\nProcessing {split} split...")
        img_files = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png"))
        
        for img_path in img_files:
            lbl_path = lbl_dir / (img_path.stem + ".txt")
            
            if not lbl_path.exists():
                print(f"  Warning: no label for {img_path.name}, skipping")
                continue
            
            try:
                img = Image.open(img_path).convert("RGB")
                img_w, img_h = img.size
                
                # Read all bounding boxes in this image
                with open(lbl_path) as f:
                    for line_idx, line in enumerate(f):
                        class_id, bbox = yolo_to_bbox(img_w, img_h, line)
                        if class_id is None:
                            continue
                        
                        class_name = YOLO_CLASSES.get(class_id, f"unknown_{class_id}")
                        x1, y1, x2, y2 = bbox
                        
                        # Skip tiny or invalid boxes
                        if x2 - x1 < 20 or y2 - y1 < 20:
                            continue
                        
                        # Crop and save
                        crop = img.crop((x1, y1, x2, y2))
                        out_name = f"{img_path.stem}_crop{line_idx}.jpg"
                        crop.save(output_root / class_name / out_name, quality=95)
                        total_crops += 1
                        
            except Exception as e:
                print(f"  Error processing {img_path.name}: {e}")
    
    print(f"\n✓ Done! Created {total_crops} cropped images in {output_root}/")
    print(f"\nClass distribution:")
    for class_name in sorted(YOLO_CLASSES.values()):
        count = len(list((output_root / class_name).glob("*.jpg")))
        if count > 0:
            print(f"  {class_name:40s}: {count:4d} images")

if __name__ == "__main__":
    main()
