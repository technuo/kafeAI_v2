"""
KafeAI Frontend — AI Chat Center Tab
Core chatbox with LangGraph backend integration.
"""
import sys
import os
import streamlit as st

# Ensure backend is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import QUICK_PROMPTS, AGENT_NODES, COLORS
from theme import render_status_badge
import data_ops


def _init_chat_state():
    """Initialize chat session state on first load"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "workflow_running" not in st.session_state:
        st.session_state.workflow_running = False
    if "phase" not in st.session_state:
        st.session_state.phase = "idle"  # idle | phase1 | waiting_hitl | phase2 | done
    if "agent_outputs" not in st.session_state:
        st.session_state.agent_outputs = {}
    if "workflow_config" not in st.session_state:
        st.session_state.workflow_config = None
    if "workflow_app" not in st.session_state:
        st.session_state.workflow_app = None


def _run_phase1(issue: str):
    """Execute LangGraph Phase 1: gather agent inputs until HITL interrupt"""
    try:
        # Dynamic import to avoid circular dependencies at module level
        from manageragent import app

        config = {"configurable": {"thread_id": f"streamlit_{id(st.session_state)}"}}
        inputs = {"issue": issue, "context": [], "feedback": ""}

        st.session_state.workflow_app = app
        st.session_state.workflow_config = config
        st.session_state.agent_outputs = {}

        # Stream Phase 1
        for output in app.stream(inputs, config=config):
            for node_name, content in output.items():
                st.session_state.agent_outputs[node_name] = content
                if "context" in content:
                    ctx = content["context"][-1] if content["context"] else ""
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"**{_get_agent_label(node_name)}**: {ctx[:500]}",
                        "node": node_name,
                    })

        # Check for HITL state
        snapshot = app.get_state(config)
        if snapshot.next:
            st.session_state.phase = "waiting_hitl"
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⏸️ **HITL Checkpoint** — All agents have reported. Awaiting your approval in the **Decision Review** tab.",
            })
        else:
            st.session_state.phase = "done"

    except Exception as e:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"❌ **System Error**: {str(e)}",
        })
        st.session_state.phase = "idle"


def _get_agent_label(node_id: str) -> str:
    """Get human-readable label for an agent node"""
    for node in AGENT_NODES:
        if node["id"] == node_id:
            return f"{node['icon']} {node['label']}"
    return node_id


def render():
    """Render the AI Chat Center tab"""
    _init_chat_state()

    st.markdown("### ☕ AI Chat Center")
    st.caption("Chat with your AI management team. Start a strategy session or ask questions.")

    # ── Quick Prompts ──────────────────────────────────────
    st.markdown("**Quick Actions:**")
    cols = st.columns(len(QUICK_PROMPTS))
    for i, qp in enumerate(QUICK_PROMPTS):
        with cols[i]:
            if st.button(qp["label"], key=f"qp_{i}", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": qp["prompt"],
                })
                st.session_state.phase = "phase1"
                st.session_state.workflow_running = True

    st.divider()

    # ── Chat History ───────────────────────────────────────
    chat_container = st.container(height=480)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # ── Phase Status ───────────────────────────────────────
    if st.session_state.phase == "waiting_hitl":
        st.info("🔔 Agents have completed analysis. Go to **Decision Review** tab to approve/modify the strategy.")
    elif st.session_state.phase == "phase1":
        with st.spinner("🔄 Agents are analyzing..."):
            issue = st.session_state.messages[-1]["content"] if st.session_state.messages else "General Analysis"
            _run_phase1(issue)
            st.session_state.workflow_running = False
            st.rerun()

    # ── Chat Input ─────────────────────────────────────────
    user_input = st.chat_input("Ask KafeAI anything...", disabled=st.session_state.workflow_running)
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.phase = "phase1"
        st.session_state.workflow_running = True
        st.rerun()

    # ── Bottom Actions ─────────────────────────────────────
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.phase = "idle"
            st.session_state.agent_outputs = {}
            st.rerun()
    with col2:
        if st.button("💾 Export Chat", use_container_width=True):
            _export_chat()


def _export_chat():
    """Export chat history as text file"""
    if not st.session_state.messages:
        st.toast("No messages to export.", icon="⚠️")
        return
    lines = []
    for msg in st.session_state.messages:
        role = "USER" if msg["role"] == "user" else "KAFEAI"
        lines.append(f"[{role}] {msg['content']}\n")
    content = "\n".join(lines)
    st.download_button(
        "📥 Download",
        data=content,
        file_name="kafeai_chat_export.txt",
        mime="text/plain",
    )
