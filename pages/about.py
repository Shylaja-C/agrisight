"""
pages/about.py  -  AgriSight About & Ethics page
Project story, team, data sources, responsible-AI statement, limitations.
"""
import streamlit as st
import styles


def render():
    st.markdown('<p class="ag-section-heading">\u2139\ufe0f About AgriSight</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="ag-section-sub">Our story, our data, and our commitment to responsible AI.</p>',
        unsafe_allow_html=True,
    )

    # ── Project story ─────────────────────────────────────────────────────
    story_col, facts_col = st.columns([2, 1], gap="large")

    with story_col:
        st.markdown("""
        <div class="ag-card">
          <p class="ag-section-heading" style="font-size:1.1rem;">\U0001f33f Project Story</p>
          <p style="font-size:0.9rem;color:var(--muted);line-height:1.8;margin-top:0.75rem;">
            AgriSight was built for the <strong>AI Innovation Hackathon 2026</strong>
            (Track 1: AI/ML Methodology &mdash; Challenge 7: CropVision AI).
          </p>
          <p style="font-size:0.9rem;color:var(--muted);line-height:1.8;">
            Our central research question: <em>does training with field-style augmentation
            meaningfully close the domain gap between clean lab images and messy real-world
            field photos?</em>
          </p>
          <p style="font-size:0.9rem;color:var(--muted);line-height:1.8;">
            We trained four model variants (baseline CNN, MobileNetV3, EfficientNet-B0)
            with basic and field augmentation, evaluated them on both PlantVillage (lab)
            and PlantDoc (field) datasets, and measured the domain gap honestly.
          </p>
          <p style="font-size:0.9rem;color:var(--muted);line-height:1.8;">
            <strong>Finding:</strong> Field augmentation improved real-world accuracy
            by ~4 percentage points for MobileNetV3 (16% vs 12%), proving a real
            but modest effect. The domain gap remains large &mdash; an honest limitation
            we report transparently.
          </p>
          <hr class="ag-divider">
          <p class="ag-section-heading" style="font-size:1rem;">\U0001f465 Team</p>
          <p style="font-size:0.95rem;font-weight:600;color:var(--forest);margin:0.5rem 0 0.2rem;">
            Shylaja C &nbsp;&bull;&nbsp; Sunandita M
          </p>
          <p style="font-size:0.82rem;color:var(--muted);">
            AI Innovation Hackathon 2026 &mdash; Research prototype
          </p>
        </div>
        """, unsafe_allow_html=True)

    with facts_col:
        st.markdown("""
        <div class="ag-card">
          <p class="ag-section-heading" style="font-size:1rem;">\U0001f4cb Quick Facts</p>
          <table style="width:100%;font-size:0.85rem;border-collapse:collapse;margin-top:0.5rem;">
            <tr><td style="color:var(--muted);padding:5px 0;">Models</td>
                <td style="font-weight:600;color:var(--forest);text-align:right;">4 variants</td></tr>
            <tr><td style="color:var(--muted);padding:5px 0;">Classes</td>
                <td style="font-weight:600;color:var(--forest);text-align:right;">18 diseases</td></tr>
            <tr><td style="color:var(--muted);padding:5px 0;">Lab accuracy</td>
                <td style="font-weight:600;color:var(--forest);text-align:right;">90&ndash;98%</td></tr>
            <tr><td style="color:var(--muted);padding:5px 0;">Field accuracy</td>
                <td style="font-weight:600;color:var(--amber);text-align:right;">6&ndash;16%</td></tr>
            <tr><td style="color:var(--muted);padding:5px 0;">Framework</td>
                <td style="font-weight:600;color:var(--forest);text-align:right;">PyTorch + Streamlit</td></tr>
            <tr><td style="color:var(--muted);padding:5px 0;">Explainability</td>
                <td style="font-weight:600;color:var(--forest);text-align:right;">Grad-CAM</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="ag-card" style="margin-top:1rem;">
          <p class="ag-section-heading" style="font-size:1rem;">\U0001f4da Data Sources</p>
          <p style="font-size:0.82rem;color:var(--muted);line-height:1.7;margin-top:0.5rem;">
            <strong>PlantVillage</strong><br>
            Hughes &amp; Salath&eacute;, 2015<br>
            54,000+ clean lab images, open-licensed.
          </p>
          <hr class="ag-divider" style="margin:0.6rem 0;">
          <p style="font-size:0.82rem;color:var(--muted);line-height:1.7;">
            <strong>PlantDoc</strong><br>
            Singh et al., 2020<br>
            2,600+ real field images, open-licensed.
          </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── Responsible AI ────────────────────────────────────────────────────
    st.markdown("""
    <div class="ag-card">
      <p class="ag-section-heading" style="font-size:1.1rem;">\U0001f91d Responsible AI &amp; Ethics</p>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem;">
        <div>
          <p style="font-weight:600;color:var(--forest);font-size:0.9rem;margin:0 0 0.5rem;">Our Commitments</p>
          <ul style="font-size:0.85rem;color:var(--muted);padding-left:1.1rem;line-height:1.9;margin:0;">
            <li>No medical or agricultural diagnosis claims</li>
            <li>No pesticide or treatment recommendations</li>
            <li>Transparent domain-gap reporting</li>
            <li>Open-source code and public datasets only</li>
            <li>Expert consultation always recommended</li>
          </ul>
        </div>
        <div>
          <p style="font-weight:600;color:var(--forest);font-size:0.9rem;margin:0 0 0.5rem;">Known Limitations</p>
          <ul style="font-size:0.85rem;color:var(--muted);padding-left:1.1rem;line-height:1.9;margin:0;">
            <li>Large domain gap (lab vs field)</li>
            <li>Class imbalance in PlantDoc</li>
            <li>Per-class accuracy varies widely</li>
            <li>Fails on non-leaf or blurry images</li>
            <li>18 disease classes only</li>
          </ul>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Legal disclaimer ──────────────────────────────────────────────────
    st.markdown("""
    <div class="ag-disclaimer" style="font-size:0.85rem;">
      <strong>\u26a0\ufe0f Disclaimer</strong><br>
      AgriSight is a <strong>research prototype</strong>, not a certified diagnostic tool.
      It does <strong>not</strong> provide agricultural diagnoses, recommend pesticides or treatments,
      or replace qualified agronomist advice.
      <strong>Always consult a certified agricultural expert before making farming decisions.</strong>
      <br><br>
      Research prototype, not a diagnosis. Consult an agricultural expert.
    </div>
    """, unsafe_allow_html=True)
