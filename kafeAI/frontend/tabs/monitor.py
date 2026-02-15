"""
KafeAI Frontend — System Monitor Tab
Agent status, resource usage, and live log viewer.
"""
import streamlit as st
import datetime
import logging
import io
from config import COLORS, AGENT_NODES
from theme import render_status_badge

# Lazy import psutil
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


def _init_monitor_state():
    """Initialize monitor session state"""
    if "log_entries" not in st.session_state:
        st.session_state.log_entries = []
    if "log_filter" not in st.session_state:
        st.session_state.log_filter = "ALL"


def add_log(level: str, message: str, source: str = "System"):
    """Add a log entry to session state (callable from other modules)"""
    if "log_entries" not in st.session_state:
        st.session_state.log_entries = []
    st.session_state.log_entries.append({
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "level": level.upper(),
        "source": source,
        "message": message,
    })
    # Keep max 500 entries
    if len(st.session_state.log_entries) > 500:
        st.session_state.log_entries = st.session_state.log_entries[-500:]


def render():
    """Render the System Monitor tab"""
    _init_monitor_state()

    st.markdown("### 🖥️ System Monitor")
    st.caption("Agent status, system resources, and runtime logs.")

    # ── Agent Status Grid ──────────────────────────────
    st.markdown("#### 🤖 Agent Status")

    agent_outputs = st.session_state.get("agent_outputs", {})
    phase = st.session_state.get("phase", "idle")

    cols = st.columns(4)
    for i, node in enumerate(AGENT_NODES):
        with cols[i % 4]:
            node_id = node["id"]
            has_output = node_id in agent_outputs

            if has_output:
                output = agent_outputs[node_id]
                # Check if output contains error
                ctx = output.get("context", [""])[0] if output.get("context") else ""
                if "Error" in ctx:
                    status = "error"
                    status_text = "Error"
                else:
                    status = "success"
                    status_text = "Complete"
            elif phase in ("phase1", "phase2") and not has_output:
                status = "running"
                status_text = "Waiting"
            else:
                status = "pending"
                status_text = "Idle"

            badge = render_status_badge(status_text.lower() if status_text.lower() in ("success", "error", "warning", "running", "pending") else status)
            st.markdown(f"""
            <div class="kafeai-card" style="text-align:center; padding:12px;">
                <div style="font-size:1.5rem;">{node['icon']}</div>
                <div style="font-weight:600; font-size:0.85rem; margin:4px 0;">{node['label']}</div>
                {badge}
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ── System Resources ───────────────────────────────
    col_res, col_log = st.columns([1, 2])

    with col_res:
        st.markdown("#### 💻 System Resources")
        if HAS_PSUTIL:
            cpu = psutil.cpu_percent(interval=0.5)
            mem = psutil.virtual_memory()

            # CPU gauge
            st.markdown(f"**CPU Usage**")
            st.progress(min(cpu / 100, 1.0), text=f"{cpu:.1f}%")

            # Memory gauge
            mem_pct = mem.percent / 100
            st.markdown(f"**Memory Usage**")
            st.progress(min(mem_pct, 1.0), text=f"{mem.percent:.1f}% ({mem.used // (1024**2)} MB / {mem.total // (1024**2)} MB)")

            # Disk
            try:
                disk = psutil.disk_usage("D:\\")
                disk_pct = disk.percent / 100
                st.markdown(f"**Disk Usage (D:)**")
                st.progress(min(disk_pct, 1.0), text=f"{disk.percent:.1f}%")
            except Exception:
                pass
        else:
            st.info("Install `psutil` for system monitoring:\n`pip install psutil`")

    with col_log:
        _render_log_viewer()


def _render_log_viewer():
    """Real-time log viewer with level filter"""
    st.markdown("#### 📝 Runtime Logs")

    # Filter controls
    col1, col2 = st.columns([2, 1])
    with col1:
        st.session_state.log_filter = st.selectbox(
            "Filter",
            ["ALL", "INFO", "WARN", "ERROR"],
            index=0,
            label_visibility="collapsed",
        )
    with col2:
        if st.button("🗑️ Clear Logs", use_container_width=True):
            st.session_state.log_entries = []
            st.rerun()

    # Log display
    logs = st.session_state.log_entries
    filter_level = st.session_state.log_filter

    if filter_level != "ALL":
        logs = [l for l in logs if l["level"] == filter_level]

    log_container = st.container(height=300)
    with log_container:
        if not logs:
            st.caption("No log entries yet. Logs appear when agents run.")
        else:
            for entry in reversed(logs[-100:]):  # Show latest 100
                level = entry["level"]
                color_class = {
                    "INFO": COLORS["info"],
                    "WARN": COLORS["warning"],
                    "ERROR": COLORS["error"],
                }.get(level, COLORS["text_mid"])

                st.markdown(
                    f'<div class="log-line"><span style="color:{color_class};font-weight:600;">[{level}]</span> '
                    f'<span style="color:{COLORS["text_light"]};">{entry["timestamp"]}</span> '
                    f'<span style="color:{COLORS["text_mid"]};">{entry["source"]}:</span> '
                    f'{entry["message"]}</div>',
                    unsafe_allow_html=True,
                )

    # Download logs
    if st.session_state.log_entries:
        log_text = "\n".join(
            f"[{e['level']}] {e['timestamp']} {e['source']}: {e['message']}"
            for e in st.session_state.log_entries
        )
        st.download_button(
            "📥 Download Logs",
            data=log_text,
            file_name=f"kafeai_logs_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
