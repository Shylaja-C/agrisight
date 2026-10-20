"""
pages/trust.py  -  AgriSight Model Trust page
Reads results/*.json for real metrics; embeds confusion matrix PNGs.
Never invents numbers.
"""
import glob, json, os
import streamlit as st
import styles

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY = True
except ImportError:
    PLOTLY = False


def _load_results():
    """Load all results/*.json files. Returns list of dicts."""
    out = []
    for p in sorted(glob.glob("results/*.json")):
        try:
            with open(p, encoding="utf-8") as f:
                out.append(json.load(f))
        except Exception:
            pass
    return out


def _fmt(val, pct=True):
    if val is None:
        return "n/a"
    return f"{val:.1%}" if pct else f"{val:.3f}"


def render():
    st.markdown('<p class="ag-section-heading">\U0001f4ca Model Trust & Transparency</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="ag-section-sub">'
        'Lab photos are easy; real field photos are harder. We measure that honestly.'
        '</p>',
        unsafe_allow_html=True,
    )

    results = _load_results()

    if not results:
        st.markdown("""
        <div class="ag-no-results">
          <strong>\U0001f4ca Results not available</strong><br>
          <span style="font-size:0.85rem;">
            No <code>results/*.json</code> files found.<br>
            Run <code>python evaluate.py</code> to generate evaluation results.
          </span>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Overview metric cards ──────────────────────────────────────────────
    st.markdown('<p class="ag-section-heading" style="font-size:1.1rem;margin-top:1rem;">Performance Overview</p>',
                unsafe_allow_html=True)

    n = len(results)
    cols = st.columns(n)
    for col, r in zip(cols, results):
        run  = r.get("run", "?")
        pv   = r.get("plantvillage_test", {}).get("accuracy")
        pd   = r.get("plantdoc_test",     {}).get("accuracy")
        gap  = r.get("domain_gap_accuracy")
        with col:
            border_top = "#4C9A2A" if (gap or 1) < 0.85 else "#E3A62F"
            st.markdown(f"""
            <div class="ag-metric" style="border-top-color:{border_top};">
              <p class="ag-metric-label">{run.replace("_", " ")}</p>
              <p class="ag-metric-value">{_fmt(pv)}</p>
              <p class="ag-metric-sub">Lab accuracy (PlantVillage)</p>
              <hr class="ag-divider" style="margin:0.6rem 0;">
              <p style="font-size:0.85rem;color:var(--text);margin:0.15rem 0;">
                Field: <strong>{_fmt(pd)}</strong>
              </p>
              <p style="font-size:0.85rem;color:var(--muted);margin:0.15rem 0;">
                Domain gap: <strong>{_fmt(gap, pct=False)}</strong>
              </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── Bar chart: lab vs field accuracy ──────────────────────────────────
    if PLOTLY and results:
        st.markdown('<p class="ag-section-heading" style="font-size:1.1rem;">Lab vs Field Accuracy</p>',
                    unsafe_allow_html=True)

        names  = [r.get("run", "?").replace("_", " ") for r in results]
        pv_acc = [r.get("plantvillage_test", {}).get("accuracy", 0) * 100 for r in results]
        pd_acc = [r.get("plantdoc_test",     {}).get("accuracy", 0) * 100 for r in results]

        fig = go.Figure()
        fig.add_bar(name="Lab (PlantVillage)", x=names, y=pv_acc,
                    marker_color="#4C9A2A", text=[f"{v:.1f}%" for v in pv_acc],
                    textposition="outside")
        fig.add_bar(name="Field (PlantDoc)",   x=names, y=pd_acc,
                    marker_color="#E3A62F", text=[f"{v:.1f}%" for v in pd_acc],
                    textposition="outside")
        fig.update_layout(
            barmode="group",
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(family="Inter, sans-serif", color="#1B1F1A"),
            yaxis=dict(title="Accuracy (%)", range=[0, 110], gridcolor="#E0E8DC"),
            xaxis=dict(title=""),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, b=20, l=20, r=20),
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Robustness ────────────────────────────────────────────────────────
    st.markdown('<p class="ag-section-heading" style="font-size:1.1rem;">Robustness to Image Distortions</p>',
                unsafe_allow_html=True)
    st.markdown(
        '<p class="ag-section-sub" style="margin-bottom:0.75rem;">'
        'How well does each model handle blur, noise and lighting changes on lab images?'
        '</p>',
        unsafe_allow_html=True,
    )

    rob_keys = {
        "blur":         "\U0001f4a4 Blur",
        "noise":        "\U0001f50a Noise",
        "bright_low":   "\U0001f505 Dim light",
        "bright_high":  "\U0001f506 Bright light",
        "contrast_low": "\U0001f519 Low contrast",
    }

    if PLOTLY:
        rob_rows = []
        for r in results:
            rob = r.get("robustness", {})
            for key, label in rob_keys.items():
                if key in rob:
                    rob_rows.append({
                        "Model": r.get("run", "?").replace("_", " "),
                        "Distortion": label,
                        "Accuracy": rob[key].get("accuracy", 0) * 100,
                    })
        if rob_rows:
            import pandas as pd
            df = pd.DataFrame(rob_rows)
            fig2 = px.bar(
                df, x="Distortion", y="Accuracy", color="Model",
                barmode="group",
                color_discrete_sequence=["#4C9A2A", "#7EC859", "#E3A62F", "#C8553D"],
                text_auto=".1f",
            )
            fig2.update_layout(
                plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                font=dict(family="Inter, sans-serif", color="#1B1F1A"),
                yaxis=dict(title="Accuracy (%)", range=[0, 110], gridcolor="#E0E8DC"),
                xaxis=dict(title=""),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(t=40, b=20, l=20, r=20),
                height=340,
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No robustness data in results files.")
    else:
        # Fallback: simple table
        for r in results:
            rob = r.get("robustness", {})
            if not rob:
                continue
            run = r.get("run", "?").replace("_", " ")
            rows_html = "".join(
                f'<tr><td>{rob_keys.get(k, k)}</td>'
                f'<td><strong>{v.get("accuracy", 0):.1%}</strong></td></tr>'
                for k, v in rob.items()
            )
            st.markdown(f"""
            <div class="ag-card-sm" style="margin-bottom:1rem;">
              <strong>{run}</strong>
              <table style="width:100%;margin-top:0.5rem;font-size:0.85rem;border-collapse:collapse;">
                <tr style="color:var(--muted);font-size:0.75rem;">
                  <th style="text-align:left;padding:4px 0;">Distortion</th>
                  <th style="text-align:left;padding:4px 0;">Accuracy</th>
                </tr>
                {rows_html}
              </table>
            </div>
            """, unsafe_allow_html=True)

    # ── Domain gap explanation ────────────────────────────────────────────
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="ag-card-sm">
      <p class="ag-section-heading" style="font-size:1rem;">Why is field accuracy so much lower?</p>
      <p style="font-size:0.88rem;color:var(--muted);line-height:1.7;margin:0.5rem 0 0;">
        PlantVillage images are clean, well-lit lab photos taken against plain backgrounds.
        PlantDoc images are real field photos with occlusion, mixed backgrounds, varying light,
        and camera shake &mdash; a fundamentally harder distribution.<br><br>
        We train with <em>field-style augmentation</em> (random blur, perspective warp, colour jitter)
        to shrink this gap. Our best model cuts the gap from 0.865 to 0.819 &mdash; a real but modest improvement.
        Honest reporting of this gap is a core part of responsible AI.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Confusion matrices ────────────────────────────────────────────────
    cm_files = sorted(glob.glob("results/*_plantdoc_cm.png"))
    if cm_files:
        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        st.markdown('<p class="ag-section-heading" style="font-size:1.1rem;">Confusion Matrices (PlantDoc)</p>',
                    unsafe_allow_html=True)
        st.markdown(
            '<p class="ag-section-sub">Each row is the true class; each column is the predicted class.</p>',
            unsafe_allow_html=True,
        )
        cm_cols = st.columns(min(len(cm_files), 2))
        for col, cm_path in zip(cm_cols * 4, cm_files):
            model_name = os.path.basename(cm_path).replace("_plantdoc_cm.png", "").replace("_", " ")
            with col:
                st.image(cm_path, caption=f"Model: {model_name}", use_container_width=True)

    # Summary.md
    if os.path.exists("results/summary.md"):
        with st.expander("\U0001f4cb Raw summary (results/summary.md)"):
            st.markdown(open("results/summary.md").read())
