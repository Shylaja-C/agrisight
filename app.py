"""AgriSight demo.   streamlit run app.py"""
import glob, os
import numpy as np, streamlit as st
from PIL import Image
import torch, models, gradcam_utils as gu

st.set_page_config(page_title="AgriSight", page_icon="🌿", layout="wide")
st.title("🌿 AgriSight: Explainable Crop Stress Detection")
st.caption("Research prototype for the AI Innovation Hackathon 2026. Not a diagnosis, and it gives no treatment advice.")

ckpts = sorted(glob.glob("outputs/*.pt"))
if not ckpts:
    st.error("No trained model found in outputs/. Train one first (see README)."); st.stop()
with st.sidebar:
    ck_path = st.selectbox("Model checkpoint", ckpts, index=len(ckpts) - 1)
    thr = st.slider("Low-confidence threshold", 0.3, 0.95, 0.60, 0.05)

@st.cache_resource
def load(p): return models.load_checkpoint(p, "cpu")
model, ck = load(ck_path); classes = ck["classes"]
pretty = lambda c: c.replace("___", ": ").replace("_", " ")

up = st.file_uploader("Upload a leaf photo", type=["jpg", "jpeg", "png"])
if up:
    img = Image.open(up).convert("RGB")
    probs, _ = gu.predict(model, img)
    top = np.argsort(probs)[::-1][:3]; conf = float(probs[top[0]])
    overlay, cam = gu.gradcam_overlay(model, ck["model"], img, int(top[0]))
    c1, c2, c3 = st.columns(3)
    c1.image(img, caption="Input", use_container_width=True)
    c2.image(overlay, caption="Grad-CAM: where the model looked", use_container_width=True)
    with c3:
        st.metric("Predicted category", pretty(classes[top[0]]))
        st.metric("Confidence", f"{conf:.0%}")
        for i in top: st.progress(float(probs[i]), text=f"{pretty(classes[i])}: {probs[i]:.0%}")
    if conf < thr:
        st.warning("Low confidence. Please retake the photo (close-up, good light, single leaf) or consult an agricultural expert.")
    if gu.background_reliance(cam) > 0.55:
        st.info("The model's attention is mostly at the image border, so the prediction may rely on background. Treat it with extra caution.")
    st.caption(f"Model: {ck['model']} | training augmentation: {ck.get('aug')} | classes covered: {len(classes)}")
else:
    st.info("Upload a leaf image to see the predicted category, confidence and Grad-CAM heatmap.")
