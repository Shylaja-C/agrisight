# Ethics and Limitations

## Responsible AI Statement

AgriSight is a research prototype developed to study the domain-gap problem in plant leaf image classification. It was built by student researchers for an AI hackathon, using publicly available datasets and open-source tools.

We are committed to honest reporting. Every metric in this repository comes from actual model evaluation runs. We do not present this system as more capable than it is.

---

## Intended Scope

AgriSight is intended **only** for:
- Research and educational use.
- Demonstration of AI explainability techniques (Grad-CAM).
- Studying the lab-to-field domain gap in agricultural AI.

---

## What This System Is Not

- It is **not a certified diagnostic tool**.
- It is **not a replacement for expert agronomic advice**.
- It does **not recommend pesticides, fertilisers, or any treatments**.
- It has **not been validated** for any regulatory, commercial, or clinical purpose.
- It does **not cover** all crops, diseases, or geographic regions.

---

## Privacy and Data Handling

- Uploaded images are processed in memory and are **not stored** by default.
- No image is sent to an external server during local deployment.
- If deployed on Streamlit Community Cloud or another cloud platform, verify that platform's data handling policy.
- The optional Supabase integration (in `portal.py`) is disabled by default. If enabled, users should be informed of what data is stored.

---

## Dataset Bias and Limitations

### PlantVillage (training data)
- Images were collected under controlled lab conditions with plain backgrounds.
- The dataset is not representative of the diversity of crop varieties, growing regions, or real field conditions worldwide.
- Certain crops and disease categories are over-represented; others are absent.

### PlantDoc (test data)
- Collected from internet sources; may reflect biases in online image availability.
- Only 18 of the original 38 PlantVillage classes are available in PlantDoc.
- One class (*Potato early blight*) has only 11 images in the test set, making per-class metrics for that class unreliable.
- PlantDoc images are bounding-box crops from a YOLO dataset, which may introduce crop artefacts.

### What these biases mean for users
- A model that performs well in this evaluation may not perform well on images from other regions, other crop varieties, or different camera types.
- Accuracy numbers reported here apply only to the test sets described. They cannot be extrapolated to arbitrary field conditions.

---

## Fairness and Access

- This system was built using freely available tools and datasets to keep the barrier to reproduction low.
- The primary language of the interface and documentation is English; a multilingual interface is listed as a future roadmap item but is not built.
- Computational requirements for training are addressed by Kaggle's free GPU tier; inference runs on CPU.

---

## Responsible Use Guidance

If you are a researcher, developer, or student using AgriSight:

1. **Do not deploy this system for real agricultural decisions** without expert validation.
2. **Report the domain gap honestly** when presenting results. The gap between lab accuracy and field accuracy is large and important.
3. **Do not interpret Grad-CAM as ground truth.** Grad-CAM shows correlation, not causation. The heatmap indicates which image regions influenced the prediction, but this is not the same as identifying the disease symptom.
4. **Treat low-confidence flags seriously.** A low-confidence prediction should prompt the user to retake the photo or seek expert advice, not be overridden.
5. **Credit the original dataset authors** if you publish results using PlantVillage or PlantDoc.

---

## Disclaimer

> AgriSight is a research prototype. It is not a substitute for professional agricultural advice. No pesticide or treatment recommendations are given, implied, or should be inferred from any output of this system. The authors accept no liability for decisions made based on the outputs of this system.
