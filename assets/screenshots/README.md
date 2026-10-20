# Screenshots

This folder contains screenshots of the AgriSight Streamlit demo.

## Required screenshots

Take these screenshots while running `streamlit run app.py` with real trained checkpoints loaded.

| Filename | Page | Description |
|---|---|---|
| `home.png` | Home | Full home page view |
| `scan_upload.png` | Scan a Leaf | A leaf photo loaded in the upload widget |
| `scan_result.png` | Scan a Leaf | Prediction card with confidence badge and top-3 bars |
| `scan_heatmap.png` | Scan a Leaf | Grad-CAM side-by-side (original + overlay) |
| `scan_low_confidence.png` | Scan a Leaf | Low-confidence warning card visible |
| `trust_metrics.png` | Model Trust | Metric cards showing lab vs. field accuracy |
| `trust_confusion.png` | Model Trust | Confusion matrix for at least one model |
| `compare.png` | Compare Models | Side-by-side model comparison view |

## Notes

- Prefer PNG format.
- Crop to the relevant content; avoid showing browser chrome unless helpful.
- Reference in README.md with: `![caption](assets/screenshots/<filename>)`
