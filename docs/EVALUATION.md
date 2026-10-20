# Evaluation Methodology and Results

## Overview

AgriSight evaluates each trained model on three axes:

1. **In-distribution accuracy** — PlantVillage test split (lab images, same distribution as training).
2. **Domain generalisation** — PlantDoc external test set (real field images, never seen during training).
3. **Robustness** — PlantVillage test set with five synthetic perturbations applied.

All metrics reported below are read directly from `results/summary.md` and the individual `results/*.json` files. No values are invented or estimated.

---

## Metric Definitions

| Metric | Definition |
|---|---|
| **Accuracy** | Proportion of correctly classified samples. |
| **Macro F1** | Unweighted average of per-class F1 scores. Treats all classes equally regardless of support. |
| **Domain gap (accuracy)** | PlantVillage test accuracy − PlantDoc accuracy. Larger gap = worse generalisation. |
| **Mean confidence** | Average softmax probability of the predicted class across all test samples. |

All metrics use `sklearn.metrics.f1_score(average='macro', zero_division=0)`.

---

## Model Runs

Four training configurations were evaluated:

| Run ID | Architecture | Augmentation mode |
|---|---|---|
| `baseline_basic` | Custom 4-block CNN (scratch) | Basic |
| `mobilenet_basic` | MobileNetV3-Large (fine-tuned) | Basic |
| `mobilenet_field` | MobileNetV3-Large (fine-tuned) | Field |
| `effnet_field` | EfficientNet-B0 (fine-tuned) | Field |

---

## Full Comparison Table

*(Source: `results/summary.md`)*

| Run | Model | Aug | PV acc | PV F1 | PlantDoc acc | PlantDoc F1 | Gap | Blur acc | Noise acc | Dim-light acc |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline_basic | baseline | basic | 0.909 | 0.910 | 0.063 | 0.060 | 0.845 | 0.277 | 0.455 | 0.198 |
| effnet_field | efficientnet_b0 | field | 0.977 | 0.975 | 0.145 | 0.144 | 0.832 | 0.812 | 0.767 | 0.975 |
| mobilenet_basic | mobilenet_v3 | basic | 0.986 | 0.986 | 0.121 | 0.122 | 0.865 | 0.277 | 0.836 | 0.963 |
| mobilenet_field | mobilenet_v3 | field | 0.978 | 0.979 | 0.160 | 0.169 | 0.819 | 0.778 | 0.884 | 0.973 |

---

## Domain-Gap Analysis

All models are trained on PlantVillage (lab images) and tested on PlantDoc (real field images). The domain gap measures how much accuracy drops when moving to the real-world distribution.

| Run | PV acc | PlantDoc acc | Domain gap |
|---|---|---|---|
| baseline_basic | 0.909 | 0.063 | **0.845** |
| mobilenet_basic | 0.986 | 0.121 | **0.865** |
| mobilenet_field | 0.978 | 0.160 | **0.819** |
| effnet_field | 0.977 | 0.145 | **0.832** |

**Finding:** Field-style augmentation (`mobilenet_field`) reduces the domain gap compared to basic augmentation (`mobilenet_basic`) — from 0.865 to 0.819. This supports the hypothesis that training with stronger augmentation improves real-world generalisation, though the absolute PlantDoc accuracy remains low for all models.

The domain gap is large for all models. This is consistent with the broader literature on lab-to-field transfer in plant disease classification.

---

## Robustness Results

Each model was evaluated on the PlantVillage test set with five synthetic perturbations applied at inference time. No retraining was done; these results measure the model's sensitivity to image quality variations.

### Accuracy under perturbations

| Run | Dim light (0.5×) | Bright light (1.6×) | Low contrast (0.5×) | Blur (radius 3) | Noise (σ=25) |
|---|---|---|---|---|---|
| baseline_basic | 0.198 | 0.376 | 0.165 | 0.277 | 0.455 |
| mobilenet_basic | 0.963 | 0.959 | 0.971 | 0.277 | 0.836 |
| mobilenet_field | 0.973 | 0.970 | 0.976 | 0.778 | 0.884 |
| effnet_field | 0.975 | 0.961 | 0.966 | 0.812 | 0.767 |

**Finding:** The baseline CNN is highly sensitive to all perturbations. MobileNetV3 with basic augmentation is unexpectedly sensitive to blur (accuracy drops from 0.986 to 0.277) — comparable to the baseline. Field augmentation addresses this: `mobilenet_field` retains 0.778 accuracy under blur. EfficientNet with field augmentation achieves the best blur robustness (0.812).

---

## Error Analysis

### Observation 1: Baseline collapse on PlantDoc

The baseline CNN achieves only 6.3% accuracy on PlantDoc, barely above random (1/18 ≈ 5.6%). This suggests the baseline has learned surface texture features that do not transfer at all to real field images. Several PlantDoc classes have 0.0 precision and recall (e.g., Tomato Bacterial spot, Tomato mosaic virus, Tomato healthy, Grape Black rot).

### Observation 2: Confusion between visually similar disease classes

Across all models, classes such as *Tomato Early blight* and *Tomato Late blight* are frequently confused on PlantDoc. This is expected: both show lesions on tomato leaves, and the visual difference is subtle in real field conditions. The per-class precision and recall values in the JSON files show these classes have consistently low scores.

### Observation 3: PlantDoc class imbalance matters

PlantDoc has 640 test images for *Tomato healthy* but only 11 for *Potato early blight*. Low-support classes produce noisy metrics. *Potato early blight* F1 is 0.0 for all models in PlantDoc.

### Observation 4: Grad-CAM failure gallery

`results/*_failures/` directories contain side-by-side pairs of the original image and its Grad-CAM overlay for misclassified PlantDoc samples.

**TODO:** Describe specific observations from the failure images in `results/baseline_basic_failures/`, `results/mobilenet_basic_failures/`, `results/mobilenet_field_failures/`, and `results/effnet_field_failures/`. At the time of writing, the images are present but a manual review of patterns is needed. Add 3–5 observations based on what you see.

### Observation 5: Mean confidence is not calibrated to domain

`mobilenet_basic` reports mean confidence 0.909 on PlantVillage but only 0.433 on PlantDoc — a large drop that partially tracks the accuracy drop. The low-confidence threshold feature in the app exploits this to flag uncertain predictions. However, confidence alone is not a reliable indicator of correctness; some high-confidence predictions are wrong.

---

## Confusion Matrices

Confusion matrices for each model on the PlantDoc test set are saved as:

- `results/baseline_basic_plantdoc_cm.png`
- `results/mobilenet_basic_plantdoc_cm.png`
- `results/mobilenet_field_plantdoc_cm.png`
- `results/effnet_field_plantdoc_cm.png`

These are embedded in the **Model Trust** page of the Streamlit app.

---

## Reproducibility

To reproduce all evaluation results:

```bash
python evaluate.py --ckpt outputs/baseline_basic.pt --failures 8
python evaluate.py --ckpt outputs/mobilenet_basic.pt --failures 8
python evaluate.py --ckpt outputs/mobilenet_field.pt --failures 8
python evaluate.py --ckpt outputs/effnet_field.pt --failures 8
python compare.py
```

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the full environment and seed information.
