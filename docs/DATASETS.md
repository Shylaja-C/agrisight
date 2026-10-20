# Datasets

## Overview

AgriSight uses two publicly available plant leaf image datasets:

| Dataset | Source | Purpose |
|---|---|---|
| PlantVillage | Kaggle: `mohitsingh1804/plantvillage` | Training and held-out lab test |
| PlantDoc | Kaggle: `andresmgs/plantdec` (Roboflow YOLO format) | External real-field test only |

**PlantDoc is never used for training.** It is the external test set used to measure how models trained on PlantVillage generalise to real field conditions.

---

## Dataset 1: PlantVillage

### Citation
- Hughes, D.P., Salathé, M. (2015). *An open access repository of images on plant health to enable the development of mobile disease diagnostics.* arXiv:1511.08060.
- Mohanty, S.P., Hughes, D.P., Salathé, M. (2016). *Using Deep Learning for Image-Based Plant Disease Detection.* Frontiers in Plant Science, 7, 1419.

### Source
Kaggle: [mohitsingh1804/plantvillage](https://www.kaggle.com/datasets/mohitsingh1804/plantvillage)  
Use the `train` folder inside the archive.

### License
See the original dataset page. Do not assume a license not stated there.

### Description
PlantVillage is a large collection of leaf images photographed under controlled laboratory conditions against plain backgrounds. It contains 38 disease/crop classes.

### Subset used by AgriSight
- **Classes:** 18 (the classes that exist in both PlantVillage and PlantDoc — see CLASS_MAP below).
- **Max per class:** 600 images (controlled by `MAX_PER_CLASS` in `config.py`).
- **Split strategy:** Stratified 70/15/15 random split (seed 42).

| Split | Images |
|---|---|
| Train | 6,882 |
| Validation | 1,473 |
| Test | 1,478 |

These numbers come from the data split files in `data/pv_splits.csv`.

---

## Dataset 2: PlantDoc

### Citation
Singh, D., Jain, N., Jain, P., Kayal, P., Kumawat, S., Batra, N. (2020). *PlantDoc: A Dataset for Visual Plant Disease Detection.* CoDS-COMAD 2020.

### Source
Kaggle: [andresmgs/plantdec](https://www.kaggle.com/datasets/andresmgs/plantdec)  
This is a Roboflow-processed version of PlantDoc in YOLO object-detection format with 30 classes.

### License
See the original dataset page. The original PlantDoc paper should be consulted for the applicable license.

### Description
PlantDoc contains images collected from the internet and real field conditions. Unlike PlantVillage, images have complex backgrounds, mixed lighting, and camera-induced distortions. It is a substantially harder test distribution.

The Kaggle version is formatted for YOLO object detection. AgriSight converts it to a classification folder structure using `reorganize_plantdoc.py`.

### Conversion: YOLO to classification format

`reorganize_plantdoc.py` reads each YOLO label file, converts the normalised bounding-box coordinates to pixel coordinates, crops the region from the image, and saves the crop to a class-named folder.

```
plantdoc_reorganized/
├── Apple Scab Leaf/
├── Apple leaf/
├── Apple rust leaf/
...
```

Only bounding boxes with a minimum size of 20×20 pixels are kept.

**Known caveat:** Bounding-box crops may include background at the edges or miss part of the leaf if the original box is imprecise. This is a limitation of the PlantDoc format.

### Subset used by AgriSight
- **Classes:** 18 (those that appear in both datasets — see CLASS_MAP below).
- **Images:** 4,145 cropped images across the 18 classes.
- **Usage:** External test set only. Never used for training or validation.

**Known data issue:** Only 11 PlantDoc images are available for *Potato early blight*. Per-class metrics for this class are unreliable due to small sample size.

---

## The 18 Shared Classes (CLASS_MAP)

The following 18 classes exist in both PlantVillage and PlantDoc and are used in all experiments. The PlantVillage column is the folder name; the PlantDoc column is the folder name after reorganization.

| Index | PlantVillage Folder | PlantDoc Folder |
|---|---|---|
| 0 | `Tomato___Early_blight` | `Tomato Early blight leaf` |
| 1 | `Tomato___Late_blight` | `Tomato leaf late blight` |
| 2 | `Tomato___Septoria_leaf_spot` | `Tomato Septoria leaf spot` |
| 3 | `Tomato___Bacterial_spot` | `Tomato leaf bacterial spot` |
| 4 | `Tomato___Tomato_mosaic_virus` | `Tomato leaf mosaic virus` |
| 5 | `Tomato___Tomato_Yellow_Leaf_Curl_Virus` | `Tomato leaf yellow virus` |
| 6 | `Tomato___healthy` | `Tomato leaf` |
| 7 | `Potato___Early_blight` | `Potato leaf early blight` |
| 8 | `Potato___Late_blight` | `Potato leaf late blight` |
| 9 | `Corn_(maize)___Northern_Leaf_Blight` | `Corn leaf blight` |
| 10 | `Corn_(maize)___Common_rust_` | `Corn rust leaf` |
| 11 | `Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot` | `Corn Gray leaf spot` |
| 12 | `Apple___Apple_scab` | `Apple Scab Leaf` |
| 13 | `Apple___Cedar_apple_rust` | `Apple rust leaf` |
| 14 | `Apple___healthy` | `Apple leaf` |
| 15 | `Grape___Black_rot` | `grape leaf black rot` |
| 16 | `Pepper,_bell___Bacterial_spot` | `Bell_pepper leaf spot` |
| 17 | `Pepper,_bell___healthy` | `Bell_pepper leaf` |

The full 30-class YOLO mapping used by `reorganize_plantdoc.py` matches the `data.yaml` provided with the `andresmgs/plantdec` Kaggle dataset (classes at indices 0–29).

---

## How to Download

### Requirements
- A Kaggle account.
- Kaggle API token configured (download `kaggle.json` from your Kaggle profile and place it at `~/.kaggle/kaggle.json`).

### Method 1: kagglehub (recommended for scripts)

```bash
pip install kagglehub
python download_datasets.py
```

This downloads both datasets to your local Kaggle cache and prints the paths.

### Method 2: Kaggle notebook (recommended for GPU training)

Inside a Kaggle notebook, add the datasets via the **+ Add Data** button:
- `mohitsingh1804/plantvillage`
- `andresmgs/plantdec`

The datasets are then available at `/kaggle/input/plantvillage/` and `/kaggle/input/plantdec/`.

### Method 3: Manual download

Go to the Kaggle dataset pages above, click **Download**, and extract to a local folder.

---

## Known Issues and Caveats

1. **Lab vs. field domain gap.** PlantVillage images have clean, controlled backgrounds. PlantDoc images come from the internet and real fields. Models trained on PlantVillage are expected to perform worse on PlantDoc.
2. **Small PlantDoc class: Potato early blight.** Only 11 images. Results for this class are noisy and should not be interpreted individually.
3. **Bounding-box crop imprecision.** PlantDoc bounding boxes are from YOLO annotations, which may be imprecise. Some crops include significant background.
4. **Class imbalance.** Even within the 18 shared classes, the number of PlantDoc images per class varies considerably.
5. **Kaggle dataset version.** This project was developed with a specific version of `andresmgs/plantdec`. If a newer version is released, folder names in `data.yaml` may differ.
