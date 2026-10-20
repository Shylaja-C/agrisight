"""
pages/compare.py  -  AgriSight Compare Models page
Upload one image; show two selected checkpoints side-by-side.
"""
import glob, os
import numpy as np
import streamlit as st
from PIL import Image

import models
import gradcam_utils as gu
import styles


@st.cache_resource(show_spinner=False)
def _load(path):
    return models.load_checkpoint(path, "cpu")


def _pretty(cls_name: str) -> str:
    return cls_name.replace("___", ": ").replace("_", " ")


def _result_html(label: str, crop: str, cond: str, conf: float,
                 top_names, top_probs) -> str:
    fill_cls = ["ag-bar-fill", "ag-bar-fill-2", "ag-bar-fill-3"]
    bars = ""
    for j, (nm, pr) in enumerate(zip(top_names, top_probs)):
        bars += (
            f'<div class="ag-bar-row">'
            f'<div class="ag-bar-label"><span>{_pretty(nm)}</span><span>{pr:.0%}</span></div>'
            f'<div class="ag-bar-track">'
            f'<div class="{fill_cls[j]}" style="width:{pr*100:.1f}%;"></div>'
            f'</div></div>'
        )
    return f"""
    <div class="ag-compare-header">
      <p style="font-size:0.75rem;font-weight:600;text-transform:uppercase;
         letter-spacing:0.08em;color:var(--muted);margin:0 0 0.25rem;">{label}</p>
      <p class="ag-crop-name" style="font-size:1.1rem;">{crop}</p>
      <p class="ag-crop-condition">{cond if cond else 'Healthy / Unknown'}</p>
      {styles.badge(conf)}
      {styles.gauge(conf)}
      {bars}
    </div>
    """


def render():
    st.markdown('<p class="ag-section-heading">\U0001f500 Compare Models</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="ag-section-sub">Upload one image and compare two model checkpoints side-by-side.</p>',
        unsafe_allow_html=True,
    )

    ckpts = sorted(glob.glob("outputs/*.pt"))
    if len(ckpts) < 2:
        st.markdown("""
        <div class="ag-no-results">
          <strong>\U0001f6ab Not enough checkpoints</strong><br>
          <span style="font-size:0.85rem;">Need at least 2 <code>.pt</code> files in <code>outputs/</code>.</span>
        </div>
        """, unsafe_allow_html=True)
        return

    pretty_ckpts = {os.path.basename(p).replace(".pt", ""): p for p in ckpts}
    names = list(pretty_ckpts.keys())

    sel_col1, sel_col2 = st.columns(2)
    with sel_col1:
        choice_a = st.selectbox("Model A", names, index=0, key="cmp_a")
    with sel_col2:
        choice_b = st.selectbox("Model B", names, index=min(1, len(names) - 1), key="cmp_b")

    uploaded = st.file_uploader(
        "\U0001f343 Drop a leaf photo here",
        type=["jpg", "jpeg", "png"],
        key="cmp_upload",
        label_visibility="collapsed",
    )

    if not uploaded:
        st.markdown("""
        <div class="ag-empty-state">
          <span class="icon">\U0001f500</span>
          <h3>Upload a leaf to compare predictions</h3>
        </div>
        """, unsafe_allow_html=True)
        return

    try:
        img = Image.open(uploaded).convert("RGB")
    except Exception:
        st.markdown(
            '<div class="ag-border-alert">\U0001f6ab Could not read image. Please upload a valid JPG/PNG.</div>',
            unsafe_allow_html=True,
        )
        return

    # Show original
    st.image(img, caption="Uploaded leaf", width=340)

    # Load and run both models
    col_a, col_b = st.columns(2, gap="large")
    for col, choice in [(col_a, choice_a), (col_b, choice_b)]:
        with col:
            try:
                with st.spinner(f"Running {choice}..."):
                    model, ck = _load(pretty_ckpts[choice])
                    classes   = ck["classes"]
                    probs, _  = gu.predict(model, img)
                    top_idx   = np.argsort(probs)[::-1][:3]
                    conf      = float(probs[top_idx[0]])
                    overlay, cam = gu.gradcam_overlay(model, ck["model"], img, int(top_idx[0]))

                # Split class name
                cn = classes[top_idx[0]]
                if "___" in cn:
                    crop, cond = cn.split("___", 1)
                    crop = crop.replace("_", " ").strip()
                    cond = cond.replace("_", " ").strip()
                else:
                    crop, cond = cn.replace("_", " "), ""

                top_names = [classes[i] for i in top_idx]
                top_probs = [float(probs[i]) for i in top_idx]

                st.markdown(
                    _result_html(choice, crop, cond, conf, top_names, top_probs),
                    unsafe_allow_html=True,
                )
                st.image(overlay, use_container_width=True)
                st.markdown(
                    '<p class="ag-img-caption">Grad-CAM heatmap</p>',
                    unsafe_allow_html=True,
                )

                # Border alert only if > 0.80
                if gu.background_reliance(cam) > 0.80:
                    st.markdown(
                        '<div class="ag-border-alert" style="font-size:0.78rem;">'
                        '\u26a0\ufe0f Attention mostly at border</div>',
                        unsafe_allow_html=True,
                    )

            except Exception as e:
                st.markdown(
                    f'<div class="ag-border-alert">\U0001f6ab {choice} failed: {e}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("""
    <div class="ag-disclaimer">
      <strong>Research prototype, not a diagnosis.</strong>
      Consult an agricultural expert before making any farm decisions.
    </div>
    """, unsafe_allow_html=True)
