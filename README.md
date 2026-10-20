# AgriSight: Explainable Early Crop Stress Detection
AI Innovation Hackathon 2026 | Track 1 (AI/ML Methodology) | Challenge 7: CropVision AI
Team: Shylaja C, Sunandita M

AgriSight classifies crop stress / disease from a leaf photo, shows a **Grad-CAM** heatmap of where the model looked,
flags **low-confidence** predictions, and measures how well a model trained on lab images (**PlantVillage**) holds up on
real field images (**PlantDoc**). It is a research prototype, **not** a diagnosis, and it gives no pesticide/treatment advice.

## 1. Setup
```bash
pip install -r requirements.txt
```
Datasets (public):
- PlantVillage (Kaggle: "PlantVillage Dataset", use the `color/` folder)
- PlantDoc (GitHub: pratikkayal/PlantDoc-Dataset, folders `train/` and `test/`)

## 2. Run order
```bash
python check_classes.py --pv_root <PlantVillage/color> --pd_root <PlantDoc-Dataset>   # fix CLASS_MAP names if any say FIX
python prepare_data.py  --pv_root <PlantVillage/color> --pd_root <PlantDoc-Dataset>

# experiments (same architecture, only the augmentation differs -> measures what augmentation buys)
python train.py --model baseline        --aug basic --epochs1 10 --epochs2 0 --run baseline_basic
python train.py --model mobilenet_v3    --aug basic --run mobilenet_basic
python train.py --model mobilenet_v3    --aug field --run mobilenet_field
python train.py --model efficientnet_b0 --aug field --run effnet_field        # optional: resnet50 if time allows

for r in baseline_basic mobilenet_basic mobilenet_field effnet_field; do
  python evaluate.py --ckpt outputs/$r.pt --failures 8
done
python compare.py          # -> results/summary.md (paste into your final write-up)
streamlit run app.py       # demo
```
Add `--workers 0` on Windows if the data loader complains.

## 3. Method
- **Data:** fixed subset of crop/stress classes present in both datasets (see `config.py`), up to 600 PlantVillage images per class,
  stratified 70/15/15 train/val/test. PlantDoc is never used for training; it is the external real-field test set.
- **Models:** baseline CNN (from scratch); transfer learning with MobileNetV3, EfficientNet-B0 (optional ResNet50).
  Two-stage fine-tuning: frozen backbone, then last blocks unfrozen at a lower learning rate. Class-weighted loss.
- **Augmentation:** `basic` vs `field` (strong colour/brightness jitter, blur, perspective, rotation, random erasing) to simulate field conditions.
- **Explainability:** Grad-CAM (pytorch-grad-cam). Failure gallery shows heatmaps on misclassified PlantDoc images, plus a
  border-attention score as a rough "is the model looking at the background?" indicator.
- **Evaluation:** accuracy and macro-F1 on PlantVillage test and PlantDoc; domain gap; robustness to dim/bright light, low contrast, blur, noise; confusion matrix; error analysis.

## 4. Results
> Fill this table from `results/summary.md` after running the experiments. Report numbers exactly as produced, including failures.

## 5. Limitations
- PlantVillage images are lab-style with uniform backgrounds; a large accuracy drop on PlantDoc is expected and is the point of the study.
- Limited crops/classes; class imbalance in PlantDoc; PlantDoc images per class are few, so per-class numbers are noisy.
- Predictions can be wrong; low-confidence cases are flagged for expert review. Research prototype only.

## 6. Ethics
Only public, permitted datasets; no personal data; no treatment recommendations; credit to PlantVillage (Hughes & Salathe) and PlantDoc (Singh et al.).
