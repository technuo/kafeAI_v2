"""
KafeAI Frontend — Sidebar: System Settings
Visual .env editor, run mode toggle, config backup/restore.
"""
import streamlit as st
import data_ops
from config import COLORS


def render():
    """Render the System Settings sidebar section"""
    st.markdown("### ⚙️ Settings")

    # ── Load Current Config ────────────────────────────
    env = data_ops.read_env()

    # ── API Keys ───────────────────────────────────────
    with st.expander("🔑 API Keys", expanded=False):
        google_key = st.text_input(
            "Google Gemini API Key",
            value=env.get("GOOGLE_API_KEY", ""),
            type="password",
            key="cfg_google_key",
        )
        weather_key = st.text_input(
            "Weather API Key",
            value=env.get("WEATHER_API_KEY", ""),
            type="password",
            key="cfg_weather_key",
        )
        nano_key = st.text_input(
            "Nano Banana API Key",
            value=env.get("NANO_BANANA_API_KEY", ""),
            type="password",
            key="cfg_nano_key",
        )

    # ── Location ───────────────────────────────────────
    with st.expander("📍 Location", expanded=False):
        city = st.text_input(
            "City",
            value=env.get("CITY", "Sundsvall"),
            key="cfg_city",
        )

    # ── LangSmith (Optional) ──────────────────────────
    with st.expander("🔗 LangSmith (Dev)", expanded=False):
        tracing = st.selectbox(
            "Tracing",
            ["true", "false"],
            index=0 if env.get("LANGCHAIN_TRACING_V2", "true") == "true" else 1,
            key="cfg_tracing",
        )
        lc_key = st.text_input(
            "LangChain API Key",
            value=env.get("LANGCHAIN_API_KEY", ""),
            type="password",
            key="cfg_lc_key",
        )
        lc_project = st.text_input(
            "LangChain Project",
            value=env.get("LANGCHAIN_PROJECT", "kafeAI-v2"),
            key="cfg_lc_project",
        )

    # ── Run Mode ───────────────────────────────────────
    with st.expander("🚀 Run Mode", expanded=False):
        mode = st.radio(
            "Select Mode",
            ["☁️ Standard", "⚡ Lightweight (less logging)"],
            index=0,
            key="cfg_run_mode",
        )
        st.caption("Lightweight mode reduces log verbosity for low-spec machines.")

    # ── Save Button ────────────────────────────────────
    if st.button("💾 Save Configuration", use_container_width=True, key="save_config"):
        new_env = {
            "GOOGLE_API_KEY": google_key,
            "WEATHER_API_KEY": weather_key,
            "NANO_BANANA_API_KEY": nano_key,
            "CITY": city,
            "LANGCHAIN_TRACING_V2": tracing,
            "LANGCHAIN_API_KEY": lc_key,
            "LANGCHAIN_PROJECT": lc_project,
        }
        if data_ops.write_env(new_env):
            st.success("✅ Configuration saved to .env")
        else:
            st.error("Failed to save configuration.")

    # ── Config Backup ──────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Export .env", use_container_width=True, key="export_env"):
            env_content = "\n".join(f"{k}={v}" for k, v in env.items())
            st.download_button(
                "Download",
                data=env_content,
                file_name="kafeai_config_backup.txt",
                mime="text/plain",
            )
    with col2:
        if st.button("🔄 Reset Defaults", use_container_width=True, key="reset_config"):
            if data_ops.write_env({}):
                st.success("Config reset to defaults.")
                st.rerun()
