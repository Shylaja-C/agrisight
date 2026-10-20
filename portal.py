"""
AgriSight Farmer Portal
AI Innovation Hackathon 2026 | Track 1: CropVision AI | Challenge 7
Team: Shylaja C, Sunandita M

No login or signup required. Opens directly to the home page.
"""

import os
import glob
import json
from datetime import datetime

import numpy as np
import streamlit as st
from PIL import Image

import models
import gradcam_utils as gu

try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AgriSight – Crop Health AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS  (warm earthy palette + premium card design)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #F7F5EE !important;
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    color: #172814;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #132E16 0%, #1C4020 60%, #29572D 100%) !important;
}
[data-testid="stSidebar"] * { color: #E8F5E3 !important; }
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    color: #fff !important; border-radius: 10px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.22) !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15) !important; }

/* ── Editorial Hero banner (from jury screenshots) ── */
.hero-editorial {
    background: linear-gradient(135deg, rgba(16,40,19,0.92) 0%, rgba(22,58,26,0.88) 50%, rgba(38,82,43,0.85) 100%),
                url('https://images.unsplash.com/photo-1592417817098-8f3d6910985b?auto=format&fit=crop&w=1600&q=80') center/cover no-repeat;
    border-radius: 24px;
    padding: 3.5rem 3rem 2.5rem;
    color: #FFFFFF;
    margin-bottom: 2rem;
    box-shadow: 0 16px 40px rgba(18,48,22,0.25);
    position: relative;
    overflow: hidden;
}
.hero-editorial .tag {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #A3E5A8;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.hero-editorial h1 {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 3.5rem;
    font-style: italic;
    line-height: 1.1;
    font-weight: 400;
    color: #FFFFFF !important;
    margin: 0 0 1.2rem;
    letter-spacing: -0.01em;
}
.hero-editorial p.subtitle {
    color: #E0F2DC !important;
    font-size: 1.15rem;
    line-height: 1.6;
    max-width: 680px;
    margin: 0 0 2rem;
    font-weight: 400;
}
.hero-editorial .meta-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255,255,255,0.2);
    padding-top: 1.5rem;
    margin-top: 2rem;
    font-size: 0.85rem;
    color: #BBE5B8;
}
.hero-editorial .meta-row .stat-pill {
    display: flex;
    align-items: baseline;
    gap: 0.6rem;
}
.hero-editorial .meta-row .stat-pill .num {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #FFFFFF;
}
.hero-editorial .meta-row .stat-pill .lbl {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #A3E5A8;
}

/* ── Card Editorial (Screenshot 1 & 2) ── */
.editorial-section-tag {
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #2D6A10;
    margin-bottom: 0.4rem;
}
.editorial-section-title {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 2.5rem;
    color: #14321A;
    line-height: 1.2;
    margin: 0 0 0.6rem;
}
.editorial-section-sub {
    font-size: 1rem;
    color: #4C6B46;
    max-width: 720px;
    line-height: 1.55;
    margin-bottom: 2rem;
}

/* ── Feature cards ── */
.feat-card {
    background: #fff;
    border-radius: 16px;
    padding: 1.5rem;
    height: 100%;
    border-top: 4px solid #4CAF28;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    transition: transform 0.2s, box-shadow 0.2s;
}
.feat-card:hover { transform: translateY(-3px); box-shadow: 0 6px 24px rgba(0,0,0,0.12); }
.feat-icon { font-size: 2.2rem; margin-bottom: 0.6rem; }
.feat-title { font-family: 'Poppins',sans-serif; font-weight: 700; font-size: 1.05rem; color: #1A3A0E; margin: 0.3rem 0; }
.feat-desc  { font-size: 0.87rem; color: #5A7250; line-height: 1.55; margin: 0; }

/* ── Step cards ── */
.step-card {
    background: linear-gradient(135deg, #F0F9EB 0%, #E3F4DA 100%);
    border-radius: 14px; padding: 1.2rem 1.4rem;
    border-left: 5px solid #4CAF28;
    margin-bottom: 0.75rem;
}
.step-num { font-weight: 800; color: #2D6A10; font-size: 1.1rem; }
.step-text { color: #2C4A22; font-size: 0.92rem; margin: 0; }

/* ── Stat cards ── */
.stat-card {
    background: #fff; border-radius: 14px; padding: 1.2rem;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
    border-bottom: 3px solid #4CAF28;
}
.stat-val  { font-family: 'Poppins',sans-serif; font-size: 2rem; font-weight: 800; color: #1A3A0E; margin: 0; }
.stat-lbl  { font-size: 0.78rem; color: #7A9A6A; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; margin: 0; }

/* ── Scan result card ── */
.result-card {
    background: #fff; border-radius: 18px; padding: 1.8rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.09);
    border-top: 5px solid #4CAF28;
}
.result-crop { font-family: 'Poppins',sans-serif; font-size: 1.6rem; font-weight: 800; color: #1A3A0E; margin: 0; }
.result-cond { font-size: 1rem; color: #5A7250; margin: 0.2rem 0 1rem; }

/* ── Confidence gauge ── */
.conf-high   { color: #2D9E2D; font-weight: 800; font-size: 1.3rem; }
.conf-mid    { color: #E6A817; font-weight: 800; font-size: 1.3rem; }
.conf-low    { color: #D9534F; font-weight: 800; font-size: 1.3rem; }
.conf-bar    { height: 10px; border-radius: 50px; margin: 0.5rem 0 1rem;
               background: linear-gradient(90deg, #D9534F 0%, #E6A817 50%, #2D9E2D 100%); }

/* ── Bar rows ── */
.bar-wrap { margin: 0.35rem 0; }
.bar-label { display: flex; justify-content: space-between; font-size: 0.82rem; color: #3A5A2A; margin-bottom: 3px; }
.bar-track { background: #EDF5E8; border-radius: 50px; height: 8px; overflow: hidden; }
.bar-fill  { height: 8px; border-radius: 50px; background: linear-gradient(90deg, #4CAF28, #2D9E2D); transition: width 0.5s; }
.bar-fill2 { height: 8px; border-radius: 50px; background: linear-gradient(90deg, #81C784, #4CAF28); }
.bar-fill3 { height: 8px; border-radius: 50px; background: linear-gradient(90deg, #A5D6A7, #81C784); }

/* ── Warnings ── */
.warn-box {
    background: #FFFBEA; border: 1.5px solid #F6BE00;
    border-radius: 12px; padding: 1rem 1.2rem; margin: 1rem 0;
}
.warn-box strong { color: #8A6800; }
.info-box {
    background: #EAF4FB; border: 1.5px solid #64B5F6;
    border-radius: 12px; padding: 1rem 1.2rem; margin: 1rem 0;
}
.disc-box {
    background: #FFF5F5; border: 1.5px solid #FFCDD2;
    border-radius: 12px; padding: 0.9rem 1.1rem; margin: 1rem 0;
    font-size: 0.83rem; color: #7B2020;
}

/* ── Upload zone ── */
[data-testid="stFileUploader"] {
    border: 2.5px dashed #9DC07A !important;
    border-radius: 16px !important;
    background: #F7FCF4 !important;
    padding: 1rem !important;
}

/* ── Section heading ── */
.sec-head {
    font-family: 'Poppins', sans-serif;
    font-size: 1.4rem; font-weight: 700;
    color: #1A3A0E; margin: 1.5rem 0 0.75rem;
    border-left: 4px solid #4CAF28; padding-left: 0.75rem;
}

/* ── Farm scan card ── */
.scan-log {
    background: #F7FCF4; border-radius: 12px; padding: 1rem 1.3rem;
    border-left: 4px solid #81C784; margin-bottom: 0.6rem;
}
.scan-log .crop  { font-weight: 700; color: #1A3A0E; font-size: 0.95rem; }
.scan-log .meta  { font-size: 0.78rem; color: #7A9A6A; }
.scan-log .conf  { font-weight: 700; font-size: 0.9rem; }

/* ── Trust table ── */
table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
th { background: #2D6A10; color: #fff; padding: 0.6rem 0.8rem; text-align: left; }
td { padding: 0.55rem 0.8rem; border-bottom: 1px solid #E0EDDA; }
tr:hover td { background: #F0F9EB; }

/* ── Footer ── */
.footer {
    text-align: center; padding: 1.5rem; margin-top: 2rem;
    font-size: 0.78rem; color: #8AAA7A;
    border-top: 1px solid #D5E8CC;
}

/* ── Primary button override ── */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2D9E2D, #1A7A1A) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; font-weight: 700 !important;
    padding: 0.6rem 1.8rem !important;
    box-shadow: 0 4px 12px rgba(45,158,45,0.3) !important;
    transition: all 0.2s !important;
}
div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(45,158,45,0.4) !important;
}

/* ── Sidebar logo area ── */
.sb-logo { text-align: center; padding: 1.2rem 0 0.5rem; }
.sb-logo .icon { font-size: 3rem; }
.sb-logo .name {
    font-family: 'Poppins',sans-serif; font-weight: 800;
    font-size: 1.4rem; color: #D4EFC4 !important; margin: 0.2rem 0 0;
}
.sb-logo .sub  { font-size: 0.7rem; color: #8FC97A !important; letter-spacing: 0.08em; }

/* ── Nav item highlight ── */
[data-testid="stSidebar"] .stRadio label { padding: 0.55rem 0.8rem !important; border-radius: 10px !important; cursor: pointer; transition: background 0.15s; }
[data-testid="stSidebar"] .stRadio label:hover { background: rgba(255,255,255,0.1) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
for _k, _v in {"page": "🏠 Home", "scan_history": [], "nav": "🏠 Home"}.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
NAV_ITEMS = [
    "🏠 Home",
    "🔬 Scan a Leaf",
    "🌾 My Farm",
    "📊 Model Trust",
    "ℹ️ About & Ethics",
]

with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="icon">🌾</div>
        <p class="name">AgriSight</p>
        <p class="sub">CROP HEALTH AI</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr/>", unsafe_allow_html=True)

    selected = st.radio(
        "Navigate",
        NAV_ITEMS,
        index=NAV_ITEMS.index(st.session_state.nav),
        label_visibility="collapsed",
    )
    st.session_state.nav = selected

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.72rem;text-align:center;color:#8FC97A !important;"
        "padding:0 0.5rem;line-height:1.5;'>"
        "🔬 Research prototype<br>Not a diagnosis tool.<br>"
        "Always consult an expert.</p>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _pretty(cls: str) -> str:
    return cls.replace("___", ": ").replace("_", " ").strip()

def _split(cls: str):
    if "___" in cls:
        crop, cond = cls.split("___", 1)
        return (crop.replace("_", " ").replace("(", "").replace(")", "").strip(),
                cond.replace("_", " ").strip())
    return cls.replace("_", " "), ""

def _conf_class(c: float) -> str:
    return "conf-high" if c >= 0.70 else "conf-mid" if c >= 0.45 else "conf-low"

def _conf_emoji(c: float) -> str:
    return "🟢" if c >= 0.70 else "🟡" if c >= 0.45 else "🔴"

@st.cache_resource(show_spinner=False)
def _load_model(path: str):
    return models.load_checkpoint(path, "cpu")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────────────────────────────────────
def page_home():
    st.markdown("""
    <div class="hero-editorial">
        <div class="tag">● CROP CARE, MADE CLEARER</div>
        <h1>See the signal.<br>Learn sooner.<br>Grow stronger.</h1>
        <p class="subtitle">
            Understand your crops, identify potential plant health problems, and discover
            practical next steps—in a language you understand.
        </p>
        <div class="meta-row">
            <div>
                ✓ Research-led insights. Always transparent about what we know.
            </div>
            <div class="stat-pill">
                <span class="num">18</span>
                <span class="lbl">Crop Health Classes Covered</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cta_col1, cta_col2, _ = st.columns([1.5, 1.5, 3])
    with cta_col1:
        if st.button("Check my crop ↗", type="primary", use_container_width=True):
            st.session_state.nav = "🔬 Scan a Leaf"
            st.rerun()
    with cta_col2:
        if st.button("📊 Model Trust", use_container_width=True):
            st.session_state.nav = "📊 Model Trust"
            st.rerun()

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── Stats row ──
    s1, s2, s3, s4 = st.columns(4)
    stats = [
        ("18", "Crop Classes"),
        ("98.6%", "Lab Accuracy"),
        ("16.0%", "Field Accuracy"),
        ("Grad-CAM", "Explainability"),
    ]
    for col, (val, lbl) in zip([s1, s2, s3, s4], stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <p class="stat-val">{val}</p>
                <p class="stat-lbl">{lbl}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── Feature cards ──
    st.markdown('<p class="sec-head">Why AgriSight?</p>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    feats = [
        ("📷", "Instant Scan", "Upload any leaf photo and get a result in seconds. No expertise needed."),
        ("🔍", "See the Evidence", "Grad-CAM heatmaps show exactly which part of the leaf the AI examined."),
        ("⚠️", "Honest Confidence", "Low-confidence predictions are flagged clearly — no silent wrong answers."),
        ("📊", "Lab vs Field", "We measure and display the domain gap so you always know model limits."),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3, c4], feats):
        with col:
            st.markdown(f"""
            <div class="feat-card">
                <div class="feat-icon">{icon}</div>
                <p class="feat-title">{title}</p>
                <p class="feat-desc">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── How it works ──
    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown('<p class="sec-head">How It Works</p>', unsafe_allow_html=True)
        steps = [
            ("1", "📸 Take a photo", "Close-up of a single leaf in natural light."),
            ("2", "🤖 AI analyses it", "Our model identifies disease class and confidence."),
            ("3", "🗺️ See the heatmap", "Grad-CAM highlights the exact leaf region the model used."),
            ("4", "📋 Save to My Farm", "Track your scan history across sessions."),
            ("5", "👨‍🌾 Consult an expert", "Always verify with a qualified agronomist."),
        ]
        for num, title, desc in steps:
            st.markdown(f"""
            <div class="step-card">
                <span class="step-num">Step {num} · {title}</span>
                <p class="step-text">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    with right:
        st.markdown('<p class="sec-head">Supported Crops & Conditions</p>', unsafe_allow_html=True)
        crops_html = """
        <table>
            <tr><th>Crop</th><th>Conditions detected</th></tr>
            <tr><td>🍅 Tomato</td><td>Early blight, Late blight, Septoria, Bacterial spot, Mosaic virus, TYLCV, Healthy</td></tr>
            <tr><td>🥔 Potato</td><td>Early blight, Late blight</td></tr>
            <tr><td>🌽 Corn (maize)</td><td>Northern leaf blight, Common rust, Gray leaf spot</td></tr>
            <tr><td>🍎 Apple</td><td>Apple scab, Cedar rust, Healthy</td></tr>
            <tr><td>🍇 Grape</td><td>Black rot</td></tr>
            <tr><td>🫑 Bell pepper</td><td>Bacterial spot, Healthy</td></tr>
        </table>
        """
        st.markdown(crops_html, unsafe_allow_html=True)
        st.markdown("""
        <div class="disc-box" style="margin-top:1rem;">
            <strong>⚠️ Research prototype — not a diagnosis tool.</strong><br>
            Results are for educational and research purposes only.
            Always consult a qualified agricultural expert before any action.
        </div>
        """, unsafe_allow_html=True)

    # ── Quick start CTA ──
    st.markdown("<hr style='border-color:#D5E8CC;margin:2rem 0 1rem'>", unsafe_allow_html=True)
    _, cta_col, _ = st.columns([1, 2, 1])
    with cta_col:
        if st.button("🔬 Start Scanning a Leaf", type="primary", use_container_width=True):
            st.session_state.nav = "🔬 Scan a Leaf"
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: SCAN A LEAF
# ─────────────────────────────────────────────────────────────────────────────
def page_scan():
    st.markdown("""
    <div>
        <div class="editorial-section-tag">● START WITH A PHOTO</div>
        <h1 class="editorial-section-title">A clearer look at what your crop is telling you.</h1>
        <p class="editorial-section-sub">
            Take a close-up photo of one leaf in good light. AgriSight will show you what its model sees—simply and honestly.
        </p>
    </div>
    """, unsafe_allow_html=True)

    ckpts = sorted(glob.glob("outputs/*.pt"))
    if not ckpts:
        st.markdown("""
        <div class="warn-box">
            <strong>⚠️ No trained models found in outputs/</strong><br>
            Please ensure the <code>.pt</code> checkpoint files are present.
            See the README for reproduction steps.
        </div>
        """, unsafe_allow_html=True)
        return

    # Settings row
    col_set1, col_set2 = st.columns([2, 1])
    with col_set1:
        ck_path = st.selectbox(
            "🤖 Model checkpoint",
            ckpts,
            format_func=lambda x: os.path.basename(x).replace(".pt", "").replace("_", " ").title(),
            index=len(ckpts) - 1,
            key="scan_ckpt",
        )
    with col_set2:
        thr = st.slider("Low-confidence threshold", 0.30, 0.95, 0.60, 0.05, key="scan_thr")

    # Load model
    try:
        with st.spinner("⚙️ Loading model…"):
            model, ck = _load_model(ck_path)
        classes = ck["classes"]
    except Exception as e:
        st.error(f"Failed to load checkpoint: {e}")
        return

    left, right = st.columns([1, 1], gap="large")

    img = None
    with left:
        st.markdown("""
        <div style="background:#EBF3E8;border-radius:16px;padding:1.4rem;border-left:5px solid #2D6A10;margin-bottom:1rem;">
            <span style="font-weight:800;color:#2D6A10;font-size:1.1rem;">01</span>
            <h3 style="font-family:'DM Serif Display',serif;color:#14321A;margin:0.2rem 0 0.4rem;">Check your crop</h3>
            <p style="font-size:0.9rem;color:#4C6B46;margin:0 0 0.8rem;">
                Upload a leaf photo or take one now. For the best result, keep one leaf centered and in focus.
            </p>
        </div>
        """, unsafe_allow_html=True)

        input_mode = st.radio(
            "Input Mode",
            ["📁 Choose a photo", "📷 Use camera", "🌿 Try demo image"],
            horizontal=True,
            label_visibility="collapsed",
            key="input_mode_selector"
        )

        if input_mode == "📁 Choose a photo":
            uploaded = st.file_uploader(
                "Drop a JPG or PNG here",
                type=["jpg", "jpeg", "png"],
                key="scan_upload",
            )
            if uploaded:
                try:
                    img = Image.open(uploaded).convert("RGB")
                except Exception:
                    st.error("Could not read the uploaded image.")
        elif input_mode == "📷 Use camera":
            cam_pic = st.camera_input("Take a photo of a single leaf", key="scan_camera")
            if cam_pic:
                try:
                    img = Image.open(cam_pic).convert("RGB")
                except Exception:
                    st.error("Could not capture camera frame.")
        else: # Demo image
            demo_choices = {
                "🍅 Tomato Early Blight (Field)": "assets/demo_samples/Tomato_Early_Blight.jpg",
                "🌽 Corn Common Rust (Field)": "assets/demo_samples/Corn_Common_Rust.jpg",
                "🥔 Potato Early Blight (Field)": "assets/demo_samples/Potato_Early_Blight.jpg",
                "🍎 Apple Scab (Field)": "assets/demo_samples/Apple_Scab.jpg",
            }
            demo_pick = st.selectbox("Select a sample leaf photo:", list(demo_choices.keys()))
            demo_path = demo_choices[demo_pick]
            if os.path.exists(demo_path):
                img = Image.open(demo_path).convert("RGB")
            else:
                st.info("Demo image not found on disk.")

        st.caption("JPG or PNG · Images are processed in-memory for inference")

        if img is not None:
            st.image(img, use_container_width=True, caption="Active leaf photo")

    with right:
        if img is None:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #15351B 0%, #1E4624 100%);
                border-radius:20px; padding:3.5rem 2rem;
                text-align:center; color:#FFFFFF; margin-top:1rem;
                box-shadow: 0 8px 24px rgba(21,53,27,0.2);">
                <div style="
                    width:80px; height:80px; border-radius:50%;
                    border:2px solid rgba(255,255,255,0.25);
                    display:flex; align-items:center; justify-content:center;
                    margin:0 auto 1.5rem; background:rgba(255,255,255,0.06); font-size:2.4rem;">
                    🍃
                </div>
                <h3 style="font-family:'DM Serif Display',serif;color:#FFFFFF;margin:0 0 0.5rem;font-size:1.8rem;">
                    One photo.<br>A practical next step.
                </h3>
                <p style="color:#B8DFB4;font-size:0.92rem;max-width:320px;margin:0 auto;line-height:1.5;">
                    AgriSight will classify the crop health condition, quantify confidence, and generate a Grad-CAM attention heatmap.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("🤖 Analysing leaf…"):
                try:
                    probs, _ = gu.predict(model, img)
                    top_idx  = np.argsort(probs)[::-1][:3]
                    conf     = float(probs[top_idx[0]])
                    overlay, cam = gu.gradcam_overlay(model, ck["model"], img, int(top_idx[0]))
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
                    return

            crop_name, condition = _split(classes[top_idx[0]])
            top_names = [classes[i] for i in top_idx]
            top_probs = [float(probs[i]) for i in top_idx]

            # Result card
            fill_cls = ["bar-fill", "bar-fill2", "bar-fill3"]
            bars_html = "".join([
                f'<div class="bar-wrap">'
                f'<div class="bar-label"><span>{(_split(nm)[0] + ": " + _split(nm)[1]) if _split(nm)[1] else _split(nm)[0]}</span>'
                f'<span><b>{pr:.0%}</b></span></div>'
                f'<div class="bar-track">'
                f'<div class="{fill_cls[j]}" style="width:{pr*100:.1f}%"></div>'
                f'</div>'
                f'</div>'
                for j, (nm, pr) in enumerate(zip(top_names, top_probs))
            ])

            conf_cls = _conf_class(conf)
            conf_emoji = _conf_emoji(conf)
            result_html = (
                f'<div class="result-card">'
                f'<p class="result-crop">{conf_emoji} {crop_name}</p>'
                f'<p class="result-cond">{condition if condition else "Healthy / Unspecified"}</p>'
                f'<p class="{conf_cls}" style="margin:0">Confidence: {conf:.1%}</p>'
                f'<div class="conf-bar"></div>'
                f'<p style="font-size:0.75rem;font-weight:600;text-transform:uppercase;'
                f'letter-spacing:0.07em;color:#7A9A6A;margin:0.5rem 0 0.4rem">Top 3 predictions</p>'
                f'{bars_html}'
                f'</div>'
            )
            st.markdown(result_html, unsafe_allow_html=True)

            # Low confidence
            if conf < thr:
                st.markdown(
                    f'<div class="warn-box">'
                    f'<strong>⚠️ Low confidence ({conf:.0%}) — tips for a better photo</strong>'
                    f'<ul style="margin:0.5rem 0 0;padding-left:1.2rem;font-size:0.88rem;">'
                    f'<li>Use a single leaf filling most of the frame</li>'
                    f'<li>Natural daylight — avoid harsh shadows</li>'
                    f'<li>Hold steady — no motion blur</li>'
                    f'<li>Include the affected spots clearly</li>'
                    f'</ul></div>',
                    unsafe_allow_html=True,
                )

            # Border attention
            if gu.background_reliance(cam) > 0.80:
                st.markdown(
                    '<div class="info-box">'
                    'ℹ️ <strong>Background attention detected.</strong> '
                    'The model focused on the image border rather than the leaf. '
                    'Retake with the leaf centred and the background minimised.'
                    '</div>',
                    unsafe_allow_html=True,
                )

            # Disclaimer
            st.markdown(
                '<div class="disc-box">'
                '<strong>Research prototype — not a diagnosis.</strong> '
                'Consult an agricultural expert before any decision. '
                'AgriSight does not recommend pesticides or treatments.'
                '</div>',
                unsafe_allow_html=True,
            )

    # ── Grad-CAM section ──
    if img is not None and 'overlay' in dir():
        st.markdown("<hr style='border-color:#D5E8CC;margin:1.5rem 0'>", unsafe_allow_html=True)
        st.markdown('<p class="sec-head">🗺️ Explainability: Grad-CAM Heatmap</p>', unsafe_allow_html=True)
        st.markdown(
            "<p style='color:#5A7250;font-size:0.88rem;margin:-0.5rem 0 1rem'>"
            "Warmer colours (red/orange) show where the model focused most. "
            "A good prediction should highlight the leaf tissue, not the background.</p>",
            unsafe_allow_html=True,
        )
        gc1, gc2 = st.columns(2)
        with gc1:
            st.image(img, use_container_width=True, caption="Original photo")
        with gc2:
            st.image(overlay, use_container_width=True, caption="Grad-CAM overlay")

        # Save to history
        _, btn_col, _ = st.columns([1, 2, 1])
        with btn_col:
            if st.button("💾 Save to My Farm", type="primary", use_container_width=True):
                st.session_state.scan_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "crop": crop_name,
                    "condition": condition if condition else "Healthy",
                    "confidence": conf,
                    "model": ck.get("model", "unknown"),
                    "notes": "",
                })
                st.success("✅ Saved to My Farm!")

        st.caption(f"Model: {ck.get('model', '?')} · Aug: {ck.get('aug', 'n/a')} · "
                   f"Classes: {len(classes)} · Threshold: {thr:.0%}")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: MY FARM
# ─────────────────────────────────────────────────────────────────────────────
def page_my_farm():
    st.markdown('<p class="sec-head" style="font-size:1.7rem">🌾 My Farm</p>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#5A7250;margin:-0.5rem 0 1.5rem'>"
        "Your scan history for this session. Export as JSON to keep a permanent record.</p>",
        unsafe_allow_html=True,
    )

    history = st.session_state.scan_history
    if not history:
        st.markdown("""
        <div style="background:#F0F9EB;border-radius:18px;padding:3rem;text-align:center;
                    border:2px dashed #9DC07A;">
            <div style="font-size:3rem">🌱</div>
            <h3 style="color:#2D6A10">No scans yet</h3>
            <p style="color:#7A9A6A">Go to <b>Scan a Leaf</b> and save your first scan.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Summary row
    total = len(history)
    avg_conf = sum(s["confidence"] for s in history) / total
    crops_seen = len({s["crop"] for s in history})
    m1, m2, m3 = st.columns(3)
    for col, (val, lbl) in zip(
        [m1, m2, m3],
        [(str(total), "Total Scans"), (f"{avg_conf:.0%}", "Avg Confidence"), (str(crops_seen), "Unique Crops")]
    ):
        with col:
            st.markdown(f'<div class="stat-card"><p class="stat-val">{val}</p><p class="stat-lbl">{lbl}</p></div>',
                        unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    for scan in reversed(history):
        conf_emoji = _conf_emoji(scan["confidence"])
        st.markdown(f"""
        <div class="scan-log">
            <span class="crop">{conf_emoji} {scan['crop']} — {scan['condition']}</span><br>
            <span class="meta">📅 {scan['timestamp'][:16].replace('T',' ')} &nbsp;|&nbsp;
                🤖 {scan['model']} &nbsp;|&nbsp;
                <span class="conf">Confidence: {scan['confidence']:.0%}</span>
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    st.download_button(
        "📥 Export scan history (JSON)",
        data=json.dumps(history, indent=2),
        file_name=f"agrisight_farm_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json",
    )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: MODEL TRUST
# ─────────────────────────────────────────────────────────────────────────────
def page_model_trust():
    st.markdown('<p class="sec-head" style="font-size:1.7rem">📊 Model Trust & Transparency</p>',
                unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#5A7250;margin:-0.5rem 0 1.5rem'>"
        "Lab photos are easy; real field photos are much harder. "
        "We measure and report that gap honestly.</p>",
        unsafe_allow_html=True,
    )

    # Results table
    st.markdown('<p class="sec-head">Performance Summary</p>', unsafe_allow_html=True)
    results_html = """
    <table>
        <tr>
            <th>Run</th><th>Model</th><th>Aug</th>
            <th>Lab Acc</th><th>Lab F1</th>
            <th>Field Acc</th><th>Field F1</th>
            <th>Domain Gap</th><th>Blur Acc</th><th>Noise Acc</th>
        </tr>
        <tr>
            <td>baseline_basic</td><td>Baseline CNN</td><td>Basic</td>
            <td>90.9%</td><td>0.910</td><td>6.3%</td><td>0.060</td>
            <td>0.845</td><td>27.7%</td><td>45.5%</td>
        </tr>
        <tr>
            <td>mobilenet_basic</td><td>MobileNetV3</td><td>Basic</td>
            <td>98.6%</td><td>0.986</td><td>12.1%</td><td>0.122</td>
            <td>0.865</td><td>27.7%</td><td>83.6%</td>
        </tr>
        <tr style="background:#EDF9E5">
            <td><b>mobilenet_field ✅</b></td><td><b>MobileNetV3</b></td><td><b>Field</b></td>
            <td><b>97.8%</b></td><td><b>0.979</b></td><td><b>16.0%</b></td><td><b>0.169</b></td>
            <td><b>0.819</b></td><td><b>77.8%</b></td><td><b>88.4%</b></td>
        </tr>
        <tr>
            <td>effnet_field</td><td>EfficientNet-B0</td><td>Field</td>
            <td>97.7%</td><td>0.975</td><td>14.5%</td><td>0.144</td>
            <td>0.832</td><td>81.2%</td><td>76.7%</td>
        </tr>
    </table>
    <p style="font-size:0.78rem;color:#7A9A6A;margin:0.5rem 0 0;">
        All values from <code>results/summary.md</code>. No values are invented.
        ✅ = best domain gap (smallest gap = best generalisation).
    </p>
    """
    st.markdown(results_html, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Domain gap explanation
    st.markdown('<p class="sec-head">Understanding the Domain Gap</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#fff;border-radius:16px;padding:1.5rem;
                box-shadow:0 2px 12px rgba(0,0,0,0.07);margin-bottom:1rem;">
        <p style="color:#3A5A2A;font-size:0.92rem;line-height:1.7;margin:0">
            <b>PlantVillage</b> images are clean, well-lit lab photos against plain backgrounds — easy for AI.<br>
            <b>PlantDoc</b> images are real field photos with mixed backgrounds, lighting variation, and camera
            shake — a fundamentally harder distribution.<br><br>
            Field-style augmentation (<i>mobilenet_field</i>) reduces the gap from 0.865 → 0.819 by training
            with simulated real-world conditions: random blur, perspective warp, colour jitter, and random erasing.
            The improvement is real but modest — domain gap remains a core open challenge in agricultural AI.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Confusion matrices
    cm_files = sorted(glob.glob("results/*_plantdoc_cm.png"))
    if cm_files:
        st.markdown('<p class="sec-head">Confusion Matrices (PlantDoc)</p>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, f in enumerate(cm_files):
            name = os.path.basename(f).replace("_plantdoc_cm.png", "").replace("_", " ")
            with cols[i % 2]:
                st.image(f, caption=f"Model: {name}", use_container_width=True)

    # Failure gallery
    fail_dirs = sorted(glob.glob("results/*_failures"))
    if fail_dirs:
        st.markdown('<p class="sec-head">Grad-CAM Failure Gallery</p>', unsafe_allow_html=True)
        st.markdown(
            "<p style='color:#5A7250;font-size:0.88rem;margin:-0.5rem 0 1rem'>"
            "Each pair shows the original image (left) and the Grad-CAM overlay (right) "
            "for a misclassified PlantDoc sample. Warmer = more attention.</p>",
            unsafe_allow_html=True,
        )
        for fd in fail_dirs:
            run = os.path.basename(fd).replace("_failures", "").replace("_", " ")
            imgs = sorted(glob.glob(f"{fd}/*.png"))[:4]
            if imgs:
                with st.expander(f"🔎 {run} — {len(imgs)} shown"):
                    cols = st.columns(len(imgs))
                    for col, fp in zip(cols, imgs):
                        with col:
                            st.image(fp, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: ABOUT & ETHICS
# ─────────────────────────────────────────────────────────────────────────────
def page_about():
    st.markdown('<p class="sec-head" style="font-size:1.7rem">ℹ️ About & Ethics</p>',
                unsafe_allow_html=True)

    left, right = st.columns([3, 2], gap="large")
    with left:
        st.markdown('<p class="sec-head">Project Overview</p>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#fff;border-radius:16px;padding:1.5rem;
                    box-shadow:0 2px 12px rgba(0,0,0,0.07);">
            <p style="color:#3A5A2A;line-height:1.7;margin:0;font-size:0.93rem">
                <b>AgriSight</b> is a research prototype that classifies crop leaf photos into one of
                18 predefined disease or healthy classes, shows a Grad-CAM explainability heatmap,
                flags low-confidence predictions, and measures how well a model trained on lab images
                (PlantVillage) generalises to real field images (PlantDoc).<br><br>
                <b>Event:</b> AI Innovation Hackathon 2026 — Women in AI Research, Innovation &amp;
                Entrepreneurship<br>
                <b>Track:</b> 1: AI/ML Methodology · <b>Challenge:</b> 7: CropVision AI<br>
                <b>Team:</b> Shylaja C, Sunandita M
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="sec-head">Responsible AI Statement</p>', unsafe_allow_html=True)
        ethics = [
            ("🚫", "No diagnosis", "This tool does not diagnose crop disease. It is for research and education only."),
            ("🚫", "No treatment advice", "AgriSight never recommends pesticides, fungicides, or any treatment."),
            ("👁️", "Transparent limits", "We display domain gap, confidence, and model failure cases openly."),
            ("🔒", "No data stored", "Uploaded images are processed in memory and not saved anywhere."),
            ("📖", "Open source", "All code is MIT-licensed and publicly available."),
            ("👨‍🌾", "Expert required", "Always consult a qualified agricultural expert before any decision."),
        ]
        for icon, title, desc in ethics:
            st.markdown(f"""
            <div class="step-card" style="margin-bottom:0.5rem;">
                <span class="step-num">{icon} {title}</span>
                <p class="step-text">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    with right:
        st.markdown('<p class="sec-head">Technology</p>', unsafe_allow_html=True)
        tech_rows = [
            ("Architectures", "Baseline CNN, MobileNetV3-Large, EfficientNet-B0"),
            ("Explainability", "Grad-CAM (pytorch-grad-cam)"),
            ("Training data", "PlantVillage — 6,882 train images, 18 classes"),
            ("Test data", "PlantDoc — 4,145 field images (never used in training)"),
            ("Input size", "224 × 224 px"),
            ("Optimiser", "AdamW, weight decay 1e-4"),
            ("Loss", "Cross-entropy + label smoothing 0.05"),
            ("Fine-tuning", "Two-stage: frozen → partial unfreeze"),
            ("Framework", "PyTorch + Streamlit"),
            ("Compute", "Kaggle free GPU (T4 / P100)"),
        ]
        tech_html = "<table>" + "".join(
            f"<tr><td style='font-weight:600;color:#2D6A10;width:45%'>{k}</td><td style='color:#3A5A2A'>{v}</td></tr>"
            for k, v in tech_rows
        ) + "</table>"
        st.markdown(tech_html, unsafe_allow_html=True)

        st.markdown('<p class="sec-head">Key Limitations</p>', unsafe_allow_html=True)
        lims = [
            "Large lab-to-field domain gap — all models drop significantly on PlantDoc.",
            "Only 18 classes: many crops and diseases are not covered.",
            "PlantDoc test images are bounding-box crops, not whole photos.",
            "Only 11 PlantDoc images for Potato early blight — noisy metric.",
            "Sensitive to lighting, background, crop variety.",
            "Grad-CAM border-attention is a rough heuristic, not a reliable signal.",
        ]
        for lim in lims:
            st.markdown(f"<p style='color:#5A7250;font-size:0.87rem;margin:0.3rem 0'>• {lim}</p>",
                        unsafe_allow_html=True)

        st.markdown('<p class="sec-head">Credits</p>', unsafe_allow_html=True)
        st.markdown("""
        <p style="color:#5A7250;font-size:0.85rem;line-height:1.7;margin:0">
            PlantVillage (Hughes &amp; Salathé 2015; Mohanty et al. 2016) ·
            PlantDoc (Singh et al. 2020) ·
            Grad-CAM (Selvaraju et al. 2017) ·
            pytorch-grad-cam (Jacob Gildenblat) ·
            MobileNetV3 (Howard et al. 2019) ·
            EfficientNet (Tan &amp; Le 2019) ·
            PyTorch · Streamlit · scikit-learn
        </p>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disc-box" style="margin-top:2rem;">
        <strong>⚠️ DISCLAIMER:</strong> AgriSight is a research prototype. It is not a certified
        diagnostic tool. No pesticide or treatment recommendation is given, implied, or should be
        inferred. The authors accept no liability for decisions made based on outputs of this system.
        Always consult a qualified agricultural expert.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
def _footer():
    st.markdown("""
    <div class="footer">
        🌾 AgriSight · AI Innovation Hackathon 2026 · CropVision AI · Track 1<br>
        Team: Shylaja C &amp; Sunandita M · MIT License (code) · Research prototype, not a diagnosis tool.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────────────────────────────────────
def main():
    page = st.session_state.nav
    if page == "🏠 Home":
        page_home()
    elif page == "🔬 Scan a Leaf":
        page_scan()
    elif page == "🌾 My Farm":
        page_my_farm()
    elif page == "📊 Model Trust":
        page_model_trust()
    elif page == "ℹ️ About & Ethics":
        page_about()
    _footer()

if __name__ == "__main__":
    main()
