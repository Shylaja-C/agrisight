"""
pages/scan.py  -  AgriSight Scan a Leaf page
Two-column layout: upload card (left) + result card (right).
Spinner, badges, gauge, top-3 bars, Grad-CAM, PDF download.
"""
import glob, io, os
from datetime import datetime

import numpy as np
import streamlit as st
from PIL import Image

import models
import gradcam_utils as gu
import styles


# ── Model loading ─────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def _load(path):
    return models.load_checkpoint(path, "cpu")


def _pretty(cls_name: str) -> str:
    return cls_name.replace("___", ": ").replace("_", " ")


def _split_class(cls_name: str):
    """Return (crop, condition) tuple by splitting at '___'."""
    if "___" in cls_name:
        crop, cond = cls_name.split("___", 1)
        return crop.replace("_", " ").replace("(", "").replace(")", "").strip(), \
               cond.replace("_", " ").strip()
    return cls_name.replace("_", " "), ""


# ── PDF generation ────────────────────────────────────────────────────────
def _make_pdf(orig_img: Image.Image, overlay_img, crop: str, condition: str,
              conf: float, top_names, top_probs, model_name: str) -> bytes:
    try:
        from fpdf import FPDF
        import tempfile

        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(15, 15, 15)

        # Header
        pdf.set_fill_color(31, 61, 43)
        pdf.rect(0, 0, 210, 22, "F")
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 22, "  AgriSight - Leaf Analysis Report", align="L")

        pdf.ln(8)
        pdf.set_text_color(27, 31, 26)

        # Date / model
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(94, 107, 92)
        pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  Model: {model_name}", ln=True)
        pdf.ln(4)

        # Result summary
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(31, 61, 43)
        pdf.cell(0, 8, f"Crop: {crop}", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(60, 80, 60)
        pdf.cell(0, 7, f"Condition: {condition if condition else 'N/A'}", ln=True)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(31, 61, 43)
        pdf.cell(0, 7, f"Confidence: {conf:.1%}", ln=True)
        pdf.ln(3)

        # Top predictions
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(31, 61, 43)
        pdf.cell(0, 7, "Top-3 Predictions:", ln=True)
        pdf.set_font("Helvetica", "", 9)
        for name, prob in zip(top_names, top_probs):
            pdf.set_text_color(94, 107, 92)
            pdf.cell(60, 6, f"  {_pretty(name)}", border=0)
            pdf.set_text_color(76, 154, 42)
            pdf.cell(0, 6, f"{prob:.1%}", ln=True)

        pdf.ln(4)

        # Images side by side
        with tempfile.TemporaryDirectory() as td:
            orig_path = os.path.join(td, "orig.jpg")
            cam_path  = os.path.join(td, "cam.jpg")
            orig_img.resize((300, 300)).convert("RGB").save(orig_path, "JPEG")
            cam_pil = Image.fromarray(overlay_img) if not isinstance(overlay_img, Image.Image) else overlay_img
            cam_pil.resize((300, 300)).convert("RGB").save(cam_path, "JPEG")

            img_y = pdf.get_y()
            pdf.image(orig_path, x=15, y=img_y, w=85)
            pdf.image(cam_path,  x=110, y=img_y, w=85)
            pdf.set_y(img_y + 6)
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(94, 107, 92)
            pdf.cell(90, 0, "  Original photo", border=0)
            pdf.cell(0, 0, "        Grad-CAM heatmap (warmer = more attention)", ln=True)
            pdf.set_y(img_y + 90)

        pdf.ln(6)

        # Disclaimer
        pdf.set_fill_color(245, 240, 232)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(94, 107, 92)
        pdf.multi_cell(
            0, 6,
            "DISCLAIMER: Research prototype, not a diagnosis. "
            "Consult an agricultural expert. "
            "AgriSight does not recommend pesticides or treatments.",
            fill=True
        )

        return pdf.output()
    except Exception as e:
        return None


# ── Main render ───────────────────────────────────────────────────────────
def render():
    st.markdown('<p class="ag-section-heading">\U0001f52c Scan a Leaf</p>', unsafe_allow_html=True)
    st.markdown('<p class="ag-section-sub">Upload a clear leaf photo for instant AI-powered analysis.</p>',
                unsafe_allow_html=True)

    # ── Checkpoint selector (collapsible sidebar-like expander) ───────────
    ckpts = sorted(glob.glob("outputs/*.pt"))
    if not ckpts:
        st.markdown("""
        <div class="ag-no-results">
          <strong>\U0001f6ab No model checkpoints found</strong><br>
          <span style="font-size:0.85rem;">
            No <code>.pt</code> files found in <code>outputs/</code>.<br>
            Train a model first or add a checkpoint — see README.
          </span>
        </div>
        """, unsafe_allow_html=True)
        return

    with st.expander("\u2699\ufe0f  Model settings", expanded=False):
        col_a, col_b = st.columns(2)
        with col_a:
            ck_path = st.selectbox(
                "Checkpoint",
                ckpts,
                format_func=lambda x: os.path.basename(x).replace(".pt", ""),
                index=len(ckpts) - 1,
                key="scan_ckpt",
            )
        with col_b:
            thr = st.slider("Low-confidence threshold", 0.30, 0.95, 0.60, 0.05, key="scan_thr")

    # Load model
    try:
        with st.spinner("Loading model..."):
            model, ck = _load(ck_path)
        classes = ck["classes"]
    except Exception as e:
        st.markdown(
            f'<div class="ag-border-alert"><strong>\U0001f6ab Failed to load checkpoint:</strong> {e}</div>',
            unsafe_allow_html=True,
        )
        return

    # ── Two-column layout ─────────────────────────────────────────────────
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="ag-card-sm">', unsafe_allow_html=True)
        st.markdown("""
        <p style="font-size:0.75rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;
           color:var(--muted);margin:0 0 0.75rem;">\U0001f4f7 Upload leaf photo</p>
        <p style="font-size:0.85rem;color:var(--muted);margin:0 0 0.75rem;">
          \U0001f343 Drop a leaf photo here &mdash; JPG or PNG, close-up, single leaf, good light
        </p>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Drop a leaf photo here",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
            key="scan_upload",
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if uploaded:
            try:
                img = Image.open(uploaded).convert("RGB")
                st.image(img, use_container_width=True)
                st.markdown('<p class="ag-img-caption">Original upload</p>', unsafe_allow_html=True)
            except Exception:
                st.markdown(
                    '<div class="ag-border-alert">\U0001f6ab Could not read image. '
                    'Please upload a valid JPG or PNG file.</div>',
                    unsafe_allow_html=True,
                )
                uploaded = None

    with right:
        if not uploaded:
            st.markdown("""
            <div class="ag-empty-state">
              <span class="icon">\U0001f343</span>
              <h3>Upload a leaf photo to begin</h3>
              <p style="font-size:0.85rem;color:var(--muted);">
                Results, confidence score and Grad-CAM heatmap will appear here.
              </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("\U0001f916 Analyzing leaf..."):
                try:
                    probs, _ = gu.predict(model, img)
                    top_idx  = np.argsort(probs)[::-1][:3]
                    conf     = float(probs[top_idx[0]])
                    overlay, cam = gu.gradcam_overlay(model, ck["model"], img, int(top_idx[0]))
                except Exception as e:
                    st.markdown(
                        f'<div class="ag-border-alert"><strong>\U0001f6ab Analysis failed:</strong> {e}</div>',
                        unsafe_allow_html=True,
                    )
                    return

            crop_name, condition = _split_class(classes[top_idx[0]])
            top_names = [classes[i] for i in top_idx]
            top_probs = [float(probs[i]) for i in top_idx]

            # Result card
            fill_cls = ["ag-bar-fill", "ag-bar-fill-2", "ag-bar-fill-3"]
            bars_html = ""
            for j, (nm, pr) in enumerate(zip(top_names, top_probs)):
                cr, co = _split_class(nm)
                label  = f"{cr}: {co}" if co else cr
                bars_html += (
                    f'<div class="ag-bar-row">'
                    f'<div class="ag-bar-label"><span>{label}</span><span>{pr:.0%}</span></div>'
                    f'<div class="ag-bar-track">'
                    f'<div class="{fill_cls[j]}" style="width:{pr*100:.1f}%;"></div>'
                    f'</div></div>'
                )

            st.markdown(f"""
            <div class="ag-result-card">
              <p class="ag-crop-label">Crop</p>
              <p class="ag-crop-name">{crop_name}</p>
              <p class="ag-crop-condition">{condition if condition else "Healthy / Unknown"}</p>
              {styles.badge(conf)}
              {styles.gauge(conf)}
              <hr class="ag-divider">
              <p style="font-size:0.75rem;font-weight:600;text-transform:uppercase;
                 letter-spacing:0.08em;color:var(--muted);margin:0 0 0.75rem;">
                Top 3 predictions
              </p>
              {bars_html}
            </div>
            """, unsafe_allow_html=True)

            # Low-confidence coach card
            if conf < thr:
                st.markdown("""
                <div class="ag-coach-card">
                  <p class="ag-coach-title">\U0001f4f8 Low confidence &mdash; tips for a better photo</p>
                  <ul class="ag-coach-list">
                    <li>Use a single leaf filling most of the frame</li>
                    <li>Photograph in natural daylight, avoid shadows</li>
                    <li>Hold the camera steady &mdash; no blur</li>
                    <li>Include affected spots clearly in the shot</li>
                  </ul>
                </div>
                """, unsafe_allow_html=True)

            # Border reliance warning (only if > 0.80)
            if gu.background_reliance(cam) > 0.80:
                st.markdown("""
                <div class="ag-border-alert">
                  \u26a0\ufe0f The model\u2019s attention concentrates on the image border rather than the leaf.
                  Retake the photo with the leaf centred and background minimised.
                </div>
                """, unsafe_allow_html=True)

            # Disclaimer
            st.markdown("""
            <div class="ag-disclaimer">
              <strong>Research prototype, not a diagnosis.</strong>
              Consult an agricultural expert.
              This tool does not recommend pesticides or treatments.
            </div>
            """, unsafe_allow_html=True)

            # ── Grad-CAM ──────────────────────────────────────────────────
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            st.markdown('<p class="ag-section-heading" style="font-size:1.1rem;">Explainability: Grad-CAM</p>',
                        unsafe_allow_html=True)
            gc1, gc2 = st.columns(2)
            with gc1:
                st.image(img, use_container_width=True)
                st.markdown('<p class="ag-img-caption">Original</p>', unsafe_allow_html=True)
            with gc2:
                st.image(overlay, use_container_width=True)
                st.markdown(
                    '<p class="ag-img-caption">Grad-CAM &mdash; warmer colours show where the model looked</p>',
                    unsafe_allow_html=True,
                )

            # ── Actions ────────────────────────────────────────────────────
            act1, act2 = st.columns(2)
            with act1:
                # Save to farm history
                if st.button("\U0001f4be Save to My Farm", use_container_width=True):
                    st.session_state.scan_history.append({
                        "timestamp": datetime.now().isoformat(),
                        "crop": crop_name,
                        "condition": condition,
                        "confidence": conf,
                        "model": ck.get("model", "unknown"),
                        "notes": "",
                    })
                    st.success("Saved to My Farm!")

            with act2:
                # PDF download
                pdf_bytes = _make_pdf(
                    img, overlay, crop_name, condition, conf,
                    top_names, top_probs, ck.get("model", "unknown"),
                )
                if pdf_bytes:
                    st.download_button(
                        "\U0001f4e5 Download PDF Report",
                        data=pdf_bytes,
                        file_name=f"agrisight_{crop_name.replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                else:
                    st.caption("Install fpdf2 to enable PDF export.")

            # Model info caption
            st.caption(
                f"Model: {ck.get('model')} | Aug: {ck.get('aug', 'n/a')} | "
                f"Classes: {len(classes)} | "
                f"Threshold: {thr:.0%}"
            )
