"""Create a demo checkpoint for testing the Streamlit app without training.

This creates a MobileNetV3 model with ImageNet weights (not trained on plant diseases).
Use this ONLY for testing the app interface. Predictions will not be accurate.

Usage:
  python create_demo_checkpoint.py
  streamlit run app.py
"""
import torch
from pathlib import Path
from torchvision import models as tv_models

# Create outputs folder
Path("outputs").mkdir(exist_ok=True)

# Load MobileNetV3 with ImageNet weights
print("Creating demo checkpoint with MobileNetV3...")
model = tv_models.mobilenet_v3_large(weights="DEFAULT")

# Replace classifier head for 18 classes
model.classifier[-1] = torch.nn.Linear(model.classifier[-1].in_features, 18)

# Class names (matching the 18 classes from config.py)
classes = [
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Bacterial_spot",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Apple___Apple_scab",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Grape___Black_rot",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
]

# Save checkpoint in the same format as train.py
checkpoint = {
    "model": "mobilenet_v3",
    "classes": classes,
    "state_dict": model.state_dict(),
    "aug": "demo",
    "val_acc": 0.0
}

torch.save(checkpoint, "outputs/demo_untrained.pt")

print("\n✓ Created outputs/demo_untrained.pt")
print("\nNOTE: This model is NOT trained on plant diseases.")
print("Predictions will be random/inaccurate.")
print("\nUse this ONLY to test the Streamlit app interface.")
print("\nTo run the demo:")
print("  streamlit run app.py")
print("\nFor real predictions, train models on Kaggle with GPU (see QUICKSTART.md)")
