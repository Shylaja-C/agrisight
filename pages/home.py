"""
pages/home.py  -  AgriSight Home page
Hero section, feature cards, how-it-works steps, trust stats strip.
"""
import glob, json, os
import streamlit as st
import styles


def _load_best_result():
    """Return the best result JSON dict, or None if unavailable."""
    order = ["results/mobilenet_field.json", "results/mobilenet_basic.json",
             "results/effnet_field.json", "results/baseline_basic.json"]
    for p in order:
        if os.path.exists(p):
            try:
                with open(p, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return None


def _all_results():
    """Return list of loaded result dicts from results/*.json."""
    out = []
    for p in sorted(glob.glob("results/*.json")):
        try:
            with open(p, encoding="utf-8") as f:
                out.append(json.load(f))
        except Exception:
            pass
    return out


def render():
    # ── Hero ─────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="ag-hero">
      <div class="ag-hero-badge">&#127807; AI Innovation Hackathon 2026 &nbsp;&bull;&nbsp; CropVision AI Track</div>
      <h1>Catch crop stress<br>before it shows.</h1>
      <p>Explainable AI disease detection for smallholder farmers — fast, honest, field-tested.</p>
    </div>
    """, unsafe_allow_html=True)

    # CTA button using Streamlit (navigation hook)
    col_cta, _, _ = st.columns([1, 1, 1])
    with col_cta:
        if st.button("\U0001f52c Scan a Leaf Now", use_container_width=True, type="primary"):
            st.session_state.page = "Scan"
            st.rerun()

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ── Feature cards ─────────────────────────────────────────────────────
    st.markdown('<p class="ag-section-heading">Why AgriSight?</p>', unsafe_allow_html=True)
    st.markdown('<p class="ag-section-sub">Built for real fields, not just lab benchmarks.</p>', unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    features = [
        ("\u26a1", "Instant Detection",
         "Upload a leaf photo and get a prediction with confidence score in under 3 seconds."),
        ("\U0001f9e0", "Explainable Heatmaps",
         "Grad-CAM shows exactly which leaf regions drove the model\u2019s decision \u2014 no black boxes."),
        ("\U0001f4ca", "Honest Uncertainty",
         "We report lab vs. real-field accuracy side-by-side. No inflated claims."),
    ]
    for col, (icon, title, desc) in zip([fc1, fc2, fc3], features):
        with col:
            st.markdown(f"""
            <div class="ag-feature-card">
              <span class="ag-feature-icon">{icon}</span>
              <p class="ag-feature-title">{title}</p>
              <p class="ag-feature-desc">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ── How it works ──────────────────────────────────────────────────────
    st.markdown('<p class="ag-section-heading">How it works</p>', unsafe_allow_html=True)
    steps = [
        ("\U0001f4f7", "Upload", "Take or upload a clear, close-up photo of an affected leaf."),
        ("\U0001f916", "Analyze",
         "Our model identifies the crop disease and generates a Grad-CAM explanation heatmap."),
        ("\U0001f4cb", "Understand",
         "Review the confidence level, top predictions, and heatmap — then consult an expert."),
    ]
    for i, (icon, title, desc) in enumerate(steps, 1):
        st.markdown(f"""
        <div class="ag-step">
          <div class="ag-step-num">{i}</div>
          <div>
            <p class="ag-step-title">{icon}&nbsp; {title}</p>
            <p class="ag-step-desc">{desc}</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ── Trust stats strip ─────────────────────────────────────────────────
    results = _all_results()
    if results:
        best_pv  = max((r.get("plantvillage_test", {}).get("accuracy", 0) for r in results), default=0)
        best_pd  = max((r.get("plantdoc_test",     {}).get("accuracy", 0) for r in results), default=0)
        min_gap  = min((r.get("domain_gap_accuracy", 1)                   for r in results), default=1)
        n_models = len(results)

        st.markdown(f"""
        <div class="ag-trust-strip">
          <div class="ag-trust-stat">
            <p class="ag-trust-val">{best_pv:.0%}</p>
            <p class="ag-trust-lbl">Best lab accuracy</p>
          </div>
          <div class="ag-trust-stat">
            <p class="ag-trust-val">{best_pd:.0%}</p>
            <p class="ag-trust-lbl">Best field accuracy</p>
          </div>
          <div class="ag-trust-stat">
            <p class="ag-trust-val">{min_gap:.2f}</p>
            <p class="ag-trust-lbl">Min domain gap</p>
          </div>
          <div class="ag-trust-stat">
            <p class="ag-trust-val">{n_models}</p>
            <p class="ag-trust-lbl">Models evaluated</p>
          </div>
          <div class="ag-trust-stat">
            <p class="ag-trust-val">18</p>
            <p class="ag-trust-lbl">Disease classes</p>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="ag-no-results">
          <strong>\U0001f4ca Trust stats unavailable</strong><br>
          <span style="font-size:0.85rem;">Run evaluation to populate results/*.json</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Disclaimer strip ──────────────────────────────────────────────────
    st.markdown("""
    <div class="ag-disclaimer">
      <strong>Research prototype, not a diagnosis.</strong>
      Consult an agricultural expert before making any farm decisions.
      AgriSight does not recommend pesticides or treatments.
    </div>
    """, unsafe_allow_html=True)
