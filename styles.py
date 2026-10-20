"""
styles.py - AgriSight Design System
Inject CSS via inject_css(), helpers: badge(), gauge(), footer()
"""
import streamlit as st

FOREST = "#1F3D2B"
LEAF   = "#4C9A2A"
CREAM  = "#F7F5EE"
WHITE  = "#FFFFFF"
AMBER  = "#E3A62F"
RED    = "#C8553D"
TEXT   = "#1B1F1A"
MUTED  = "#5E6B5C"

_FONT_URL = "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap"

_CSS = (
    "@import url('" + _FONT_URL + "');"
    + """
:root{
  --forest:#1F3D2B;--leaf:#4C9A2A;--cream:#F7F5EE;--white:#FFFFFF;
  --amber:#E3A62F;--red:#C8553D;--text:#1B1F1A;--muted:#5E6B5C;
  --radius:16px;
  --shadow:0 4px 24px rgba(31,61,43,0.10);
  --shadow-sm:0 2px 8px rgba(31,61,43,0.07);
}
*{box-sizing:border-box;}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stToolbar"]{display:none;}
[data-testid="stDecoration"]{display:none;}
.stDeployButton{display:none;}
div[data-testid="stSidebarNav"]{display:none;}
[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"],.stMain,.main{background-color:var(--cream)!important;}
[data-testid="stSidebar"]{background:var(--forest)!important;border-right:none!important;}
[data-testid="stSidebar"] *{color:#E8F0E9!important;}
[data-testid="stSidebar"] .stRadio label{
  font-family:'Inter',sans-serif;font-size:0.9rem;padding:8px 12px;
  border-radius:8px;cursor:pointer;transition:background 0.2s;display:block;width:100%;
}
[data-testid="stSidebar"] .stRadio label:hover{background:rgba(76,154,42,0.25)!important;}
[data-testid="stSidebar"] hr{border-color:rgba(255,255,255,0.15)!important;}
h1,h2,h3,h4,h5{font-family:'Poppins',sans-serif!important;color:var(--forest)!important;line-height:1.2;}
h1{font-size:2.4rem;font-weight:800;}h2{font-size:1.7rem;font-weight:700;}h3{font-size:1.2rem;font-weight:600;}
p,li,label,.stMarkdown{font-family:'Inter',sans-serif!important;}
.ag-card{background:var(--white);border-radius:var(--radius);padding:1.5rem;box-shadow:var(--shadow);transition:box-shadow 0.25s,transform 0.25s;}
.ag-card:hover{box-shadow:0 8px 32px rgba(31,61,43,0.15);transform:translateY(-2px);}
.ag-card-sm{background:var(--white);border-radius:var(--radius);padding:1rem 1.25rem;box-shadow:var(--shadow-sm);}
.ag-hero{background:linear-gradient(135deg,var(--forest) 0%,#2E5E42 60%,#3A7A52 100%);
  border-radius:var(--radius);padding:4rem 3rem;text-align:center;margin-bottom:2rem;
  position:relative;overflow:hidden;}
.ag-hero h1{color:#FFFFFF!important;font-size:3rem;font-weight:800;
  margin:0 0 0.75rem;text-shadow:0 2px 8px rgba(0,0,0,0.2);position:relative;}
.ag-hero p{color:#C5E3C8!important;font-size:1.25rem;margin:0 0 2rem;position:relative;}
.ag-hero-badge{display:inline-block;background:rgba(255,255,255,0.12);
  border:1px solid rgba(255,255,255,0.25);border-radius:100px;padding:0.3rem 1rem;
  font-size:0.8rem;color:#C5E3C8!important;margin-bottom:1rem;
  font-family:'Inter',sans-serif!important;position:relative;}
.ag-feature-card{background:var(--white);border-radius:var(--radius);padding:1.75rem 1.5rem;
  box-shadow:var(--shadow);text-align:center;transition:box-shadow 0.25s,transform 0.25s;height:100%;}
.ag-feature-card:hover{box-shadow:0 8px 32px rgba(31,61,43,0.15);transform:translateY(-3px);}
.ag-feature-icon{font-size:2.5rem;margin-bottom:1rem;display:block;}
.ag-feature-title{font-family:'Poppins',sans-serif!important;font-weight:600;
  color:var(--forest)!important;font-size:1rem;margin:0 0 0.5rem;}
.ag-feature-desc{color:var(--muted)!important;font-size:0.875rem;margin:0;line-height:1.6;}
.ag-step{display:flex;align-items:flex-start;gap:1rem;padding:1.25rem;
  background:var(--white);border-radius:var(--radius);box-shadow:var(--shadow-sm);margin-bottom:1rem;}
.ag-step-num{background:var(--leaf);color:white!important;width:36px;height:36px;
  border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-family:'Poppins',sans-serif!important;font-weight:700;font-size:0.9rem;flex-shrink:0;}
.ag-step-title{font-family:'Poppins',sans-serif!important;font-weight:600;
  color:var(--forest)!important;font-size:0.95rem;margin:0 0 0.25rem;}
.ag-step-desc{color:var(--muted)!important;font-size:0.85rem;margin:0;}
.ag-badge{display:inline-block;padding:0.3rem 0.9rem;border-radius:100px;
  font-family:'Poppins',sans-serif!important;font-weight:700;font-size:0.875rem;}
.ag-badge-green{background:#D4EDDA;color:#1F6B35!important;border:1.5px solid #A8D5B5;}
.ag-badge-amber{background:#FFF3CD;color:#8B6914!important;border:1.5px solid #F0D270;}
.ag-badge-red{background:#FCE4DF;color:#8B2A18!important;border:1.5px solid #EAA49A;}
.ag-gauge-wrap{margin:1rem 0;}
.ag-gauge-track{background:#E8EDE8;border-radius:100px;height:10px;overflow:hidden;}
.ag-gauge-fill{height:100%;border-radius:100px;transition:width 0.6s ease;}
.ag-result-card{background:var(--white);border-radius:var(--radius);padding:1.75rem;box-shadow:var(--shadow);}
.ag-crop-label{font-size:0.75rem;font-weight:600;text-transform:uppercase;
  letter-spacing:0.08em;color:var(--muted)!important;margin:0 0 0.2rem;}
.ag-crop-name{font-family:'Poppins',sans-serif!important;font-size:1.4rem;font-weight:700;
  color:var(--forest)!important;margin:0 0 0.2rem;}
.ag-crop-condition{font-family:'Inter',sans-serif!important;font-size:1rem;
  color:var(--muted)!important;margin:0 0 1rem;}
.ag-bar-row{margin-bottom:0.75rem;}
.ag-bar-label{display:flex;justify-content:space-between;font-size:0.82rem;
  margin-bottom:0.3rem;color:var(--text)!important;}
.ag-bar-track{background:#E8EDE8;border-radius:100px;height:8px;overflow:hidden;}
.ag-bar-fill{height:100%;border-radius:100px;background:var(--leaf);transition:width 0.5s;}
.ag-bar-fill-2{background:#7EC859;}.ag-bar-fill-3{background:#A8D88C;}
[data-testid="stFileUploader"]{border:2.5px dashed #9DC08B!important;
  border-radius:var(--radius)!important;background:#F0F7ED!important;
  padding:1.5rem!important;transition:border-color 0.2s,background 0.2s;}
[data-testid="stFileUploader"]:hover{border-color:var(--leaf)!important;background:#E6F3E0!important;}
.ag-coach-card{background:#FFF8E7;border:1.5px solid #F0D270;border-left:5px solid var(--amber);
  border-radius:var(--radius);padding:1.25rem 1.5rem;margin-top:1.25rem;}
.ag-coach-title{font-family:'Poppins',sans-serif!important;font-weight:700;
  color:#7A5800!important;font-size:1rem;margin:0 0 0.5rem;}
.ag-coach-list{margin:0;padding-left:1.1rem;}
.ag-coach-list li{color:#7A5800!important;font-size:0.88rem;margin-bottom:0.3rem;}
.ag-disclaimer{background:#F5F0E8;border-radius:10px;border-left:4px solid var(--amber);
  padding:0.9rem 1.25rem;margin:1.25rem 0;font-size:0.82rem;
  color:var(--muted)!important;line-height:1.6;}
.ag-border-alert{background:#FFF0F0;border-radius:10px;border-left:4px solid var(--red);
  padding:0.9rem 1.25rem;margin:1rem 0;font-size:0.85rem;color:#6B1F1F!important;}
.ag-metric{background:var(--white);border-radius:var(--radius);padding:1.25rem 1.5rem;
  box-shadow:var(--shadow-sm);border-top:4px solid var(--leaf);}
.ag-metric-label{font-size:0.75rem;font-weight:600;text-transform:uppercase;
  letter-spacing:0.08em;color:var(--muted)!important;margin:0 0 0.3rem;}
.ag-metric-value{font-family:'Poppins',sans-serif!important;font-size:2rem;font-weight:800;
  color:var(--forest)!important;line-height:1;margin:0 0 0.2rem;}
.ag-metric-sub{color:var(--muted)!important;font-size:0.78rem;margin:0;}
.ag-trust-strip{background:var(--forest);border-radius:var(--radius);padding:1.5rem 2rem;
  display:flex;gap:2rem;flex-wrap:wrap;justify-content:space-around;}
.ag-trust-stat{text-align:center;}
.ag-trust-val{font-family:'Poppins',sans-serif!important;font-size:1.8rem;font-weight:800;
  color:#A8E68A!important;margin:0;}
.ag-trust-lbl{font-size:0.78rem;color:#C5E3C8!important;margin:0;}
.ag-footer{text-align:center;padding:2rem 1rem 1rem;color:var(--muted)!important;
  font-size:0.8rem;border-top:1.5px solid #E0E8DC;margin-top:3rem;}
.ag-section-heading{font-family:'Poppins',sans-serif!important;font-size:1.5rem;
  font-weight:700;color:var(--forest)!important;margin:0 0 0.3rem;}
.ag-section-sub{color:var(--muted)!important;font-size:0.9rem;margin:0 0 1.5rem;}
.ag-empty-state{text-align:center;padding:3rem 1rem;color:var(--muted)!important;}
.ag-empty-state .icon{font-size:4rem;display:block;margin-bottom:1rem;}
.ag-empty-state h3{color:var(--muted)!important;font-size:1.1rem;}
.ag-no-results{background:#FFF8E7;border:1.5px dashed var(--amber);
  border-radius:var(--radius);padding:2rem;text-align:center;color:#7A5800!important;}
.ag-history-row{background:var(--white);border-radius:12px;padding:1rem 1.25rem;
  box-shadow:var(--shadow-sm);margin-bottom:0.75rem;}
.ag-history-class{font-weight:600;color:var(--forest)!important;font-size:0.95rem;}
.ag-history-meta{color:var(--muted)!important;font-size:0.78rem;}
.ag-compare-header{background:var(--white);border-radius:var(--radius);
  padding:1rem 1.5rem;box-shadow:var(--shadow-sm);text-align:center;}
.ag-img-caption{text-align:center;font-size:0.8rem;color:var(--muted)!important;margin-top:0.4rem;}
.ag-divider{border:none;border-top:1.5px solid #E0E8DC;margin:2rem 0;}
@media(max-width:768px){
  .ag-hero{padding:2.5rem 1.25rem;}
  .ag-hero h1{font-size:2rem;}
  .ag-hero p{font-size:1rem;}
  h1{font-size:1.75rem;}
}
"""
)


def inject_css():
    """Inject the full AgriSight design system CSS into the page."""
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)


def badge(conf: float) -> str:
    """Return a coloured pill badge HTML string for a confidence value."""
    pct = int(conf * 100)
    if conf >= 0.80:
        return f'<span class="ag-badge ag-badge-green">&#10003; {pct}% Confident</span>'
    elif conf >= 0.60:
        return f'<span class="ag-badge ag-badge-amber">~ {pct}% Moderate</span>'
    else:
        return f'<span class="ag-badge ag-badge-red">&#9888; {pct}% Low confidence</span>'


def gauge(conf: float) -> str:
    """Return a horizontal gauge bar HTML string."""
    pct = int(conf * 100)
    color = "#4C9A2A" if conf >= 0.80 else ("#E3A62F" if conf >= 0.60 else "#C8553D")
    return (
        '<div class="ag-gauge-wrap">'
        '<div style="display:flex;justify-content:space-between;margin-bottom:6px;">'
        '<span style="font-size:0.8rem;color:var(--muted);">Confidence</span>'
        f'<span style="font-size:0.8rem;font-weight:700;color:{color};">{pct}%</span>'
        '</div>'
        '<div class="ag-gauge-track">'
        f'<div class="ag-gauge-fill" style="width:{pct}%;background:{color};"></div>'
        '</div></div>'
    )


def footer():
    """Render the persistent footer."""
    st.markdown(
        '<div class="ag-footer">'
        '\U0001f33f <strong>AgriSight</strong>&nbsp;|&nbsp;'
        'AI Innovation Hackathon 2026&nbsp;|&nbsp;'
        'Research prototype \u2014 not a diagnosis tool'
        '</div>',
        unsafe_allow_html=True,
    )
