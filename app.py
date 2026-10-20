"""
app.py  -  AgriSight  |  streamlit run app.py
Redesigned entry-point.  AI logic (models, gradcam_utils, config, data) unchanged.
"""
import streamlit as st
import styles

# ── Page config (must be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="AgriSight",
    page_icon="\U0001f33f",
    layout="wide",
    initial_sidebar_state="expanded",
)
styles.inject_css()

# ── Session state defaults ─────────────────────────────────────────────────
for key, val in {
    "page": "Home",
    "scan_history": [],
    "user": None,
    "is_guest": True,       # guest by default — auth is optional
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Sidebar navigation ─────────────────────────────────────────────────────
NAV = {
    "\U0001f3e0 Home":           "Home",
    "\U0001f52c Scan a Leaf":    "Scan",
    "\U0001f4ca Model Trust":    "Trust",
    "\U0001f500 Compare Models": "Compare",
    "\U0001f33e My Farm":        "Farm",
    "\u2139\ufe0f  About & Ethics": "About",
}

with st.sidebar:
    st.markdown(
        '<div style="padding:1.5rem 0 0.5rem;text-align:center;">'
        '<span style="font-size:2.2rem;">\U0001f33f</span>'
        '<p style="font-family:Poppins,sans-serif;font-size:1.25rem;font-weight:800;'
        'color:#A8E68A!important;margin:0.25rem 0 0;">AgriSight</p>'
        '<p style="font-size:0.72rem;color:#7FB88A!important;margin:0;">CropVision AI</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    labels = list(NAV.keys())
    current_idx = list(NAV.values()).index(st.session_state.page)
    choice = st.radio("nav", labels, index=current_idx, label_visibility="collapsed")
    st.session_state.page = NAV[choice]

    st.divider()
    # Optional auth status
    if st.session_state.user:
        email = getattr(st.session_state.user, "email", "user")
        st.markdown(
            f'<p style="font-size:0.78rem;color:#9DC08B!important;padding:0 0.5rem;">'
            f'\U0001f464 {email}</p>',
            unsafe_allow_html=True,
        )
        if st.button("Log out", use_container_width=True):
            st.session_state.user = None
            st.session_state.is_guest = True
            st.rerun()
    else:
        st.markdown(
            '<p style="font-size:0.78rem;color:#7FB88A!important;padding:0 0.5rem;">'
            '\U0001f465 Guest mode</p>',
            unsafe_allow_html=True,
        )

# ── Page routing ───────────────────────────────────────────────────────────
page = st.session_state.page

if page == "Home":
    from pages import home as _p; _p.render()
elif page == "Scan":
    from pages import scan as _p; _p.render()
elif page == "Trust":
    from pages import trust as _p; _p.render()
elif page == "Compare":
    from pages import compare as _p; _p.render()
elif page == "Farm":
    from pages import myfarm as _p; _p.render()
elif page == "About":
    from pages import about as _p; _p.render()

styles.footer()
