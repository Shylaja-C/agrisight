# Model Card — AgriSight

> This model card follows the framework of Mitchell et al. (2019), *Model Cards for Model Reporting*.

---

## Model Details

| Field | Value |
|---|---|
| Project | AgriSight: Explainable Early Crop Stress Detection |
| Version | Hackathon submission, October 2026 |
| Authors | Shylaja C, Sunandita M |
| License | MIT (code); datasets under their own licenses |
| Contact | See repository README |

### Architectures trained

| Run ID | Architecture | Pre-trained? | Augmentation |
|---|---|---|---|
| `baseline_basic` | Custom 4-block CNN (from scratch) | No | Basic |
| `mobilenet_basic` | MobileNetV3-Large | ImageNet | Basic |
| `mobilenet_field` | MobileNetV3-Large | ImageNet | Field |
| `effnet_field` | EfficientNet-B0 | ImageNet | Field |

ResNet50 is supported in `models.py` but was not used in the submitted experiments.

---

## Intended Use

**Primary use case:** Research and educational demonstration of:
- Multi-class leaf image classification.
- Grad-CAM explainability for plant leaf images.
- Measuring and reducing the lab-to-field domain gap.
- The effect of field-style data augmentation on generalisation.

**Intended users:** Researchers, students, hackathon evaluators, and developers exploring AI explainability in agricultural contexts.

---

## Out-of-Scope Use

- **Clinical or regulatory diagnosis.** This model is not validated for any regulatory or commercial diagnostic purpose.
- **Pesticide or treatment recommendations.** The model does not and must not be used to recommend chemical treatments.
- **Crops or diseases not in the 18-class list.** The model will still produce an output for any input; that output is meaningless for unlisted classes.
- **Real-time production monitoring** without expert oversight.
- **Mobile deployment** (no mobile-optimised export has been prepared).

---

## Training Procedure

### Data
- **Training set:** PlantVillage subset — 6,882 images, 18 classes, up to 600 per class.
- **Validation set:** 1,473 PlantVillage images (same 18 classes).
- **External test set:** PlantDoc — 4,145 bounding-box crop images (never used in training).

### Hyperparameters (read from `train.py`)

| Hyperparameter | Value |
|---|---|
| Input size | 224 × 224 |
| Batch size | 32 |
| Optimiser | AdamW |
| Weight decay | 1e-4 |
| Loss function | CrossEntropyLoss |
| Label smoothing | 0.05 |
| Class weighting | Inverse-frequency weighting |
| Stage 1 LR (head only) | 1e-3 |
| Stage 2 LR (head + last blocks) | 1e-4 |
| Default stage 1 epochs | 4 |
| Default stage 2 epochs | 6 |
| Random seed | 42 |
| Data workers | 2 (use 0 on Windows if hangs) |

### Two-stage fine-tuning (transfer learning runs)
- **Stage 1:** Backbone frozen. Only the classifier head is trained at LR=1e-3.
- **Stage 2:** Last few backbone blocks unfrozen. Head and those blocks fine-tuned at LR=1e-4.
- For `baseline`, only a single phase with all parameters and LR=1e-3.

### Augmentation — Basic mode
`RandomResizedCrop(224, scale=(0.8, 1.0))`, `RandomHorizontalFlip()`, `RandomRotation(15°)`

### Augmentation — Field mode (stronger)
`RandomResizedCrop(224, scale=(0.5, 1.0))`, `RandomHorizontalFlip()`, `RandomVerticalFlip(p=0.2)`,
`RandomRotation(30°)`, `RandomPerspective(0.25, p=0.4)`,
`ColorJitter(brightness=0.5, contrast=0.5, saturation=0.4, hue=0.08)`,
`RandomGrayscale(p=0.05)`, `GaussianBlur(5, sigma=(0.1, 2.0), p=0.3)`,
`RandomErasing(p=0.4, scale=(0.02, 0.2))`

### Hardware
Training was run on a free Kaggle GPU notebook (P100 or T4). See `docs/REPRODUCIBILITY.md` for estimated runtimes.

---

## Evaluation Data

| Split | Dataset | Images | Notes |
|---|---|---|---|
| PV test | PlantVillage | 1,478 | In-distribution; same as training domain |
| PlantDoc | PlantDoc | 4,145 | External; real field images; never in training |

Robustness evaluation uses the PlantVillage test set with synthetic perturbations applied:

| Perturbation | Description |
|---|---|
| `bright_low` | Brightness factor 0.5 |
| `bright_high` | Brightness factor 1.6 |
| `contrast_low` | Contrast factor 0.5 |
| `blur` | Gaussian blur, radius 3 |
| `noise` | Additive Gaussian noise, σ=25 |

---

## Evaluation Metrics

All values are taken directly from `results/summary.md` and the corresponding `results/*.json` files.

| Run | Model | Aug | PV acc | PV F1 | PlantDoc acc | PlantDoc F1 | Domain gap |
|---|---|---|---|---|---|---|---|
| baseline_basic | baseline | basic | 0.909 | 0.910 | 0.063 | 0.060 | 0.845 |
| effnet_field | efficientnet_b0 | field | 0.977 | 0.975 | 0.145 | 0.144 | 0.832 |
| mobilenet_basic | mobilenet_v3 | basic | 0.986 | 0.986 | 0.121 | 0.122 | 0.865 |
| mobilenet_field | mobilenet_v3 | field | 0.978 | 0.979 | 0.160 | 0.169 | 0.819 |

**Domain gap** = PlantVillage accuracy − PlantDoc accuracy. A smaller gap indicates better generalisation.

### Robustness summary (PlantVillage test + perturbations)

| Run | Blur acc | Noise acc | Dim-light acc | Bright-light acc | Low-contrast acc |
|---|---|---|---|---|---|
| baseline_basic | 0.277 | 0.455 | 0.198 | 0.376 | 0.165 |
| effnet_field | 0.812 | 0.767 | 0.975 | 0.961 | 0.966 |
| mobilenet_basic | 0.277 | 0.836 | 0.963 | 0.959 | 0.971 |
| mobilenet_field | 0.778 | 0.884 | 0.973 | 0.970 | 0.976 |

*(Values from the individual JSON files; `bright_low` column = dim-light acc in summary.)*

---

## Limitations

- All models show a large domain gap. PlantDoc accuracy is much lower than PlantVillage accuracy for every model. This is expected and is the central finding.
- The baseline CNN trained from scratch is particularly fragile to lighting and blur.
- Per-class results are noisy for classes with very few PlantDoc test images (notably *Potato early blight*, with 11 images).
- Only 18 of 38 PlantVillage classes are covered. The model cannot handle other crops or diseases.
- Grad-CAM border-attention is a heuristic indicator, not a reliable measure of model quality.
- Models were not tested on images from non-PlantVillage, non-PlantDoc sources.

---

## Ethical Considerations

- Models were trained and evaluated only on publicly available datasets.
- No personally identifiable information is involved.
- The Grad-CAM visualisation is provided to increase transparency, not as a ground-truth explanation.
- This prototype must not be used for any real diagnostic decision without expert verification.

See [docs/ETHICS_AND_LIMITATIONS.md](ETHICS_AND_LIMITATIONS.md) for the full statement.

---

## How to Load a Checkpoint

```python
import models

model, ck = models.load_checkpoint("outputs/mobilenet_field.pt", device="cpu")
classes = ck["classes"]   # list of 18 class names
model.eval()

# Inference
import gradcam_utils as gu
from PIL import Image

img = Image.open("leaf.jpg")
probs, _ = gu.predict(model, img, device="cpu")
top_class = classes[probs.argmax()]
print(f"Predicted: {top_class} ({probs.max():.1%} confidence)")

# Grad-CAM
overlay, cam = gu.gradcam_overlay(model, ck["model"], img, device="cpu")
# overlay is a uint8 RGB numpy array (224×224×3)
```

The checkpoint format is a plain Python dict with keys: `model` (architecture name string), `classes` (list), `state_dict`, `aug`, `val_acc`.
