"""
KafeAI Frontend — Main Application
Entry point for Streamlit: page config, sidebar, and tab routing.
Run: streamlit run app.py --server.port 8501
"""
import sys
import os

# Ensure project paths are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # frontend/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # kafeAI/ (backend)

import streamlit as st
from config import APP_NAME, APP_SUBTITLE, APP_VERSION, COLORS, LOGO_PATH
from theme import apply_theme

# Tab modules
from tabs import chat, decisions, analytics, monitor

# Sidebar modules
from sidebar import file_manager, settings, about

# ── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{APP_NAME} — {APP_SUBTITLE}",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Apply Custom Theme ─────────────────────────────────────────
apply_theme()


# ── Sidebar ────────────────────────────────────────────────────
def render_sidebar():
    """Render the sidebar with navigation and management panels"""
    with st.sidebar:
        # Logo & branding
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=160)
        else:
            st.markdown(f'<div class="kafeai-title">☕ {APP_NAME}</div>', unsafe_allow_html=True)

        st.caption(f"v{APP_VERSION} — Local Deployment")
        st.divider()

        # Sidebar sections as expandable panels
        # file_manager.render() has its own header/layout
        file_manager.render()
        st.divider()

        # settings.render() uses expanders, so we cannot wrap it in an expander
        settings.render()
        st.divider()

        # About & Data (always compact)
        about.render()


# ── Main Content ───────────────────────────────────────────────
def render_main():
    """Render the main content area with tabs"""
    # Header
    st.markdown(f"""
    <div class="kafeai-header">
        <div>
            <div class="kafeai-title">☕ {APP_NAME}</div>
            <div class="kafeai-subtitle">{APP_SUBTITLE}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main tabs
    tab_chat, tab_decisions, tab_analytics, tab_monitor = st.tabs([
        "💬 AI Chat",
        "🧠 Decisions",
        "📊 Analytics",
        "🖥️ Monitor",
    ])

    with tab_chat:
        chat.render()

    with tab_decisions:
        decisions.render()

    with tab_analytics:
        analytics.render()

    with tab_monitor:
        monitor.render()


# ── Entry Point ────────────────────────────────────────────────
def main():
    render_sidebar()
    render_main()


if __name__ == "__main__":
    main()
else:
    # Streamlit runs the file directly, not via __main__
    main()
