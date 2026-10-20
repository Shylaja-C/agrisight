"""
pages/myfarm.py  -  AgriSight My Farm page
Scan history stored in st.session_state.
Optional Supabase login if secrets are present.
"""
import json
from datetime import datetime
import streamlit as st
import styles

# ── Optional Supabase ─────────────────────────────────────────────────────
_SUPABASE_CLIENT = None

def _try_init_supabase():
    global _SUPABASE_CLIENT
    if _SUPABASE_CLIENT is not None:
        return _SUPABASE_CLIENT
    try:
        url = st.secrets.get("supabase", {}).get("url", "")
        key = st.secrets.get("supabase", {}).get("key", "")
        if url and key:
            from supabase import create_client
            _SUPABASE_CLIENT = create_client(url, key)
    except Exception:
        pass
    return _SUPABASE_CLIENT


def _supabase_available() -> bool:
    try:
        client = _try_init_supabase()
        return client is not None
    except Exception:
        return False


# ── Auth helpers ──────────────────────────────────────────────────────────
def _do_login(email: str, password: str):
    try:
        client = _try_init_supabase()
        if not client:
            return False, "Supabase not configured."
        resp = client.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state.user = resp.user
        return True, f"Welcome back, {email}!"
    except Exception as e:
        return False, str(e)


def _do_signup(email: str, password: str):
    try:
        client = _try_init_supabase()
        if not client:
            return False, "Supabase not configured."
        client.auth.sign_up({"email": email, "password": password})
        return True, "Account created! Please log in."
    except Exception as e:
        return False, str(e)


# ── Colour for confidence dot ─────────────────────────────────────────────
def _dot_color(conf: float) -> str:
    if conf >= 0.80:
        return "#4C9A2A"
    elif conf >= 0.60:
        return "#E3A62F"
    return "#C8553D"


def render():
    st.markdown('<p class="ag-section-heading">\U0001f33e My Farm</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="ag-section-sub">Track your scan history and manage your farm account.</p>',
        unsafe_allow_html=True,
    )

    # ── Auth section (only if Supabase secrets exist) ─────────────────────
    if _supabase_available() and not st.session_state.user:
        st.markdown('<div class="ag-card-sm" style="margin-bottom:1.5rem;">', unsafe_allow_html=True)
        st.markdown("**Sign in to sync your scan history across devices**", unsafe_allow_html=False)
        tab_login, tab_signup = st.tabs(["Log in", "Sign up"])

        with tab_login:
            email    = st.text_input("Email",    key="fm_login_email")
            password = st.text_input("Password", type="password", key="fm_login_pwd")
            if st.button("Log in", use_container_width=True, key="fm_login_btn"):
                ok, msg = _do_login(email, password)
                if ok:
                    st.success(msg); st.rerun()
                else:
                    st.error(msg)

        with tab_signup:
            email2    = st.text_input("Email",    key="fm_su_email")
            password2 = st.text_input("Password", type="password", key="fm_su_pwd")
            if st.button("Sign up", use_container_width=True, key="fm_su_btn"):
                ok, msg = _do_signup(email2, password2)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.user:
        email = getattr(st.session_state.user, "email", "user")
        st.markdown(
            f'<div class="ag-card-sm" style="margin-bottom:1rem;">'
            f'\U0001f464 Logged in as <strong>{email}</strong>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Scan history ──────────────────────────────────────────────────────
    history = st.session_state.get("scan_history", [])

    if not history:
        st.markdown("""
        <div class="ag-empty-state">
          <span class="icon">\U0001f33e</span>
          <h3>No scans yet</h3>
          <p style="font-size:0.85rem;">
            Go to <strong>Scan a Leaf</strong>, analyse a leaf and hit
            <em>Save to My Farm</em> to record it here.
          </p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(
        f'<p style="font-size:0.85rem;color:var(--muted);margin-bottom:0.75rem;">'
        f'{len(history)} scan(s) this session</p>',
        unsafe_allow_html=True,
    )

    # Reverse so newest first
    for i, scan in enumerate(reversed(history)):
        ts    = scan.get("timestamp", "")[:16].replace("T", " ")
        crop  = scan.get("crop", scan.get("crop_class", "Unknown"))
        cond  = scan.get("condition", "")
        conf  = scan.get("confidence", 0.0)
        model = scan.get("model", "?")
        label = f"{crop}: {cond}" if cond else crop
        dot   = _dot_color(conf)

        with st.expander(f"\U0001f343 {label}  \u2014  {ts}  ({conf:.0%})"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Crop",       crop)
            c2.metric("Condition",  cond if cond else "n/a")
            c3.metric("Confidence", f"{conf:.1%}")
            st.caption(f"Model: {model} | Date: {ts}")

            # Notes (editable inline)
            note_key = f"note_{i}"
            if note_key not in st.session_state:
                st.session_state[note_key] = scan.get("notes", "")
            new_note = st.text_area("Notes", value=st.session_state[note_key],
                                    key=f"ta_{i}", max_chars=400)
            if new_note != st.session_state[note_key]:
                # Update the actual scan record
                idx = len(history) - 1 - i
                st.session_state.scan_history[idx]["notes"] = new_note
                st.session_state[note_key] = new_note

    # Export button
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    export_data = json.dumps(history, indent=2, default=str)
    st.download_button(
        "\U0001f4e5 Export scan history (JSON)",
        data=export_data,
        file_name=f"agrisight_history_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json",
    )

    # Guest disclaimer
    if not st.session_state.user:
        st.markdown("""
        <div class="ag-disclaimer">
          <strong>Guest mode:</strong> Scan history is stored in this browser session only.
          It will be lost when you close the tab. Sign in to save it permanently.
        </div>
        """, unsafe_allow_html=True)
