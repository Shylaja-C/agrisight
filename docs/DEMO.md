# Demo Guide

## Running the App Locally

### Prerequisites

- Python 3.10+
- Trained model checkpoints in `outputs/` (`.pt` files)
- Dependencies installed: `pip install -r requirements.txt`

### Start the app

```bash
streamlit run app.py
```

Open `http://localhost:8501` in a browser.

---

## App Walkthrough

### Page 1: Home

The home page introduces the project. It explains the domain-gap problem (lab images vs. real field images), summarises the research approach, and links to the other pages.

### Page 2: 🔬 Scan a Leaf

This is the main inference page.

1. Expand **Model settings** to select a checkpoint from `outputs/` and adjust the low-confidence threshold (default 60%).
2. Upload a leaf photo (JPG or PNG). A clear, single-leaf, well-lit photo gives the best results.
3. The model runs inference and displays:
   - **Crop** and **condition** (from the predicted class name).
   - **Confidence badge** and gauge (green = high, amber = medium, red = low).
   - **Top-3 predictions** as a bar chart.
   - **Low-confidence warning** if the top prediction is below the threshold, with tips for a better photo.
   - **Border-attention warning** if Grad-CAM attention is concentrated on the image border (> 80% in the outer 20% border region).
   - A **disclaimer** that this is a research prototype, not a diagnosis.
4. Below the result, a **Grad-CAM** section shows:
   - The original uploaded photo.
   - The Grad-CAM overlay (warmer colours = higher model attention).
5. Action buttons:
   - **Save to My Farm** — saves the scan result to session history.
   - **Download PDF Report** — generates a PDF with the prediction and Grad-CAM (requires `fpdf2`).

### Page 3: 📊 Model Trust

Shows transparency metrics from `results/*.json`:
- Metric cards: lab accuracy, field accuracy, domain gap per model.
- Bar chart: lab vs. field accuracy for all models.
- Robustness bar chart: accuracy under five distortions.
- Explanation of why field accuracy is lower.
- Confusion matrices from `results/*_plantdoc_cm.png`.

### Page 4: 🔀 Compare Models

Side-by-side model comparison.

### Page 5: 🌾 My Farm

Stores scan history in session state. Shows past scans with timestamp, crop, condition, confidence, and model used.

### Page 6: ℹ️ About & Ethics

Project description, responsible-AI statement, team information.

---

## Application Screenshots

The following interface screenshots and evaluation figures are included for jury review:

### Home & Landing Experience
![AgriSight Hero Landing](../docs/screenshots/hero_landing.png)

### Leaf Capture & Inference Flow
![AgriSight Check Crop Section](../docs/screenshots/check_crop_section.png)

### Model Trust & Grad-CAM Analysis
- **Confusion Matrix:** `results/mobilenet_field_plantdoc_cm.png`
- **Grad-CAM Failure Analysis:** `results/effnet_field_failures/fail_0.png`

---

## Live Deployment for Juries

- **Live URL:** [AgriSight Streamlit Cloud](https://agrisight-ezyz92pvapp4qnqnt7ztcr.streamlit.app/)
- **Main Entrypoint:** `portal.py`
- **Supported Leaf Classes:** 18 crop health conditions across Tomato, Potato, Corn, Apple, Grape, and Bell Pepper.
- **Evaluation Datasets:**
  - PlantVillage: [mohitsingh1804/plantvillage on Kaggle](https://www.kaggle.com/datasets/mohitsingh1804/plantvillage)
  - PlantDoc: [andresmgs/plantdec on Kaggle](https://www.kaggle.com/datasets/andresmgs/plantdec)

---

## Demo Video Script

> **TODO: Record the video and add the link to README.md.**

### Suggested script (~3 minutes)

**[0:00 – 0:20] Introduction**
Show the home page. Narrate: "AgriSight is a research prototype that classifies crop-leaf photos and shows where the model looked — using Grad-CAM. We also measure how well models trained in a lab transfer to real field conditions."

**[0:20 – 0:50] Scan a Leaf — successful prediction**
Navigate to Scan a Leaf. Upload a clear tomato leaf photo or click 'Try demo image'. Walk through the confidence badge, top-3 predictions, and the Grad-CAM overlay. Point out where the model is attending.

**[0:50 – 1:20] Low-confidence example**
Upload a blurry or unusual photo. Show the low-confidence warning card. Explain why this is important: "We flag uncertain predictions rather than confidently giving a wrong answer."

**[1:20 – 2:00] Model Trust page**
Navigate to Model Trust. Show the lab vs. field accuracy bar chart. Narrate: "The domain gap is the key finding — lab accuracy is high, field accuracy drops significantly. Field-style augmentation helps reduce this gap."

**[2:00 – 2:30] Confusion matrix**
Show one confusion matrix. Point out which classes are most confused.

**[2:30 – 3:00] Conclusion**
Return to home. Mention the honest limitations and research prototype status. Close with the team names.
