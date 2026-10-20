# Credits and Attributions

AgriSight was built using the following datasets, papers, libraries, and tools. All datasets retain their original licenses, which govern their use independently of this project's MIT code license.

---

## Datasets

### PlantVillage

- **Paper:** Hughes, D.P., Salathé, M. (2015). *An open access repository of images on plant health to enable the development of mobile disease diagnostics.* arXiv:1511.08060.
- **Paper:** Mohanty, S.P., Hughes, D.P., Salathé, M. (2016). *Using Deep Learning for Image-Based Plant Disease Detection.* Frontiers in Plant Science, 7, 1419. doi:10.3389/fpls.2016.01419
- **Kaggle dataset:** mohitsingh1804 — [plantvillage on Kaggle](https://www.kaggle.com/datasets/mohitsingh1804/plantvillage)
- **License:** See the original dataset page. Do not assume a license not stated there.

### PlantDoc

- **Paper:** Singh, D., Jain, N., Jain, P., Kayal, P., Kumawat, S., Batra, N. (2020). *PlantDoc: A Dataset for Visual Plant Disease Detection.* In Proceedings of the 7th ACM IKDD CoDS and 25th COMAD (CoDS-COMAD 2020). doi:10.1145/3371158.3371196
- **Kaggle dataset (YOLO format):** andresmgs — [plantdec on Kaggle](https://www.kaggle.com/datasets/andresmgs/plantdec) — processed and uploaded by Roboflow.
- **License:** See the original dataset page and the PlantDoc paper.

---

## Methods and Libraries

### Grad-CAM

- **Paper:** Selvaraju, R.R., Cogswell, M., Das, A., Vedantam, R., Parikh, D., Batra, D. (2017). *Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization.* ICCV 2017. doi:10.1109/ICCV.2017.74
- **Library:** Jacob Gildenblat and contributors. *pytorch-grad-cam.* GitHub: [jacobgil/pytorch-grad-cam](https://github.com/jacobgil/pytorch-grad-cam). Accessed 2026.

### MobileNetV3

- **Paper:** Howard, A., Sandler, M., Chu, G., Chen, L.-C., Chen, B., Tan, M., Wang, W., Zhu, Y., Pang, R., Vasudevan, V., Le, Q.V., Adam, H. (2019). *Searching for MobileNetV3.* ICCV 2019. doi:10.1109/ICCV.2019.00135
- **Implementation:** torchvision `mobilenet_v3_large` with DEFAULT (ImageNet) weights.

### EfficientNet

- **Paper:** Tan, M., Le, Q.V. (2019). *EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks.* ICML 2019.
- **Implementation:** torchvision `efficientnet_b0` with DEFAULT (ImageNet) weights.

### PyTorch

- Paszke, A., et al. (2019). *PyTorch: An Imperative Style, High-Performance Deep Learning Library.* NeurIPS 2019.
- Website: [pytorch.org](https://pytorch.org/)

### torchvision

- Part of the PyTorch ecosystem. Website: [pytorch.org/vision](https://pytorch.org/vision/stable/)

### Streamlit

- Website: [streamlit.io](https://streamlit.io/)
- Used for the interactive demo application.

### scikit-learn

- Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12, 2825–2830.
- Website: [scikit-learn.org](https://scikit-learn.org/)
- Used for classification reports, confusion matrices, and F1 scores.

### Matplotlib

- Hunter, J.D. (2007). *Matplotlib: A 2D graphics environment.* Computing in Science & Engineering, 9(3), 90–95.
- Website: [matplotlib.org](https://matplotlib.org/)

### OpenCV (headless)

- Bradski, G. (2000). *The OpenCV Library.* Dr. Dobb's Journal of Software Tools.
- Package: `opencv-python-headless`

### Other Python packages

- **Pillow** — PIL fork for image processing.
- **NumPy** — numerical computing.
- **tqdm** — progress bars.
- **PyYAML** — YAML parsing.
- **pandas** — tabular data.
- **plotly** — interactive charts (Model Trust page).
- **fpdf2** — PDF generation (scan report export).
- **python-dotenv** — environment variable loading.

---

## Compute

Training was performed on Kaggle's free GPU tier (NVIDIA T4 or P100). We thank Kaggle for providing accessible compute resources for student researchers.

---

## Note on Dataset Licenses

The code in this repository is MIT-licensed. The datasets (PlantVillage and PlantDoc) are **not** distributed with this repository and are governed by their own terms. Always consult the original dataset pages before using or redistributing these datasets.
