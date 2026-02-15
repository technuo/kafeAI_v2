"""
KafeAI Frontend — Decision Review Center Tab
HITL approval interface: view agent analysis, approve/modify/reject, trigger execution.
"""
import streamlit as st
import datetime
from config import COLORS, AGENT_NODES
from theme import render_status_badge
import data_ops


def _init_decision_state():
    """Initialize decision-related session state"""
    if "decision_action" not in st.session_state:
        st.session_state.decision_action = None
    if "decision_feedback" not in st.session_state:
        st.session_state.decision_feedback = ""


def render():
    """Render the Decision Review Center tab"""
    _init_decision_state()

    st.markdown("### 🧠 Decision Review Center")
    st.caption("Review AI recommendations. Approve, modify, or reject before execution.")

    # ── Active Decision Panel ──────────────────────────────
    if st.session_state.get("phase") == "waiting_hitl":
        _render_active_decision()
    elif st.session_state.get("phase") == "done":
        st.success("✅ Latest workflow completed. All decisions have been executed.")
        _render_execution_results()
    else:
        st.info("💤 No active decisions pending. Start a strategy session in the **AI Chat** tab.")

    st.divider()

    # ── Decision History ───────────────────────────────────
    st.markdown("#### 📜 Decision History")
    _render_decision_history()


def _render_active_decision():
    """Display current HITL checkpoint for review"""
    app = st.session_state.get("workflow_app")
    config = st.session_state.get("workflow_config")

    if not app or not config:
        st.warning("Workflow state not found. Please start from the Chat tab.")
        return

    snapshot = app.get_state(config)
    current_context = snapshot.values.get("context", [])
    promotion_data = snapshot.values.get("promotion_data")
    poster_path = snapshot.values.get("poster_path")

    # ── Agent Reports ──────────────────────────────────
    st.markdown("#### 📊 Agent Analysis Summary")

    for i, ctx in enumerate(current_context):
        # Determine which agent this context belongs to
        agent_icon = "📋"
        if "Predictor:" in ctx:
            agent_icon = "🌤️"
        elif "Inventory" in ctx:
            agent_icon = "📦"
        elif "Forecast" in ctx:
            agent_icon = "📈"
        elif "Post-mortem" in ctx or "Financial" in ctx:
            agent_icon = "📋"
        elif "Pricing" in ctx:
            agent_icon = "💰"

        with st.expander(f"{agent_icon} Report #{i+1}", expanded=(i == len(current_context) - 1)):
            st.markdown(ctx)

    # ── Promotion Preview ──────────────────────────────
    if promotion_data:
        st.markdown("#### 🎯 Proposed Promotion")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            <div class="kafeai-card">
                <div class="kafeai-card-header">🏷️ {promotion_data.get('promotion_id', 'N/A')}</div>
                <p><strong>Theme:</strong> {promotion_data.get('theme', 'N/A')}</p>
                <p><strong>Product:</strong> {promotion_data.get('product_item', 'N/A')}</p>
                <p><strong>Discount:</strong> {promotion_data.get('discount_type', 'N/A')}</p>
                <p><strong>Headline:</strong> {promotion_data.get('marketing_copy_headline', 'N/A')}</p>
                <p><strong>Price:</strong> {promotion_data.get('price_original', '?')} → {promotion_data.get('price_promo', '?')} SEK</p>
                <p><strong>Reason:</strong> {promotion_data.get('reason', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if poster_path:
                try:
                    st.image(poster_path, caption="Generated Poster", use_container_width=True)
                except Exception:
                    st.caption("Poster preview unavailable.")

    # ── HITL Action Buttons ────────────────────────────
    st.markdown("#### ⚡ Your Decision")

    with st.form("hitl_form"):
        feedback = st.text_area(
            "Feedback / Modifications (optional)",
            placeholder="e.g., Add 5 extra units of sallad, skip hot drinks promotion...",
            height=100,
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            approve = st.form_submit_button("✅ Approve", use_container_width=True)
        with col2:
            modify = st.form_submit_button("✏️ Modify & Approve", use_container_width=True)
        with col3:
            reject = st.form_submit_button("❌ Reject", use_container_width=True)

    if approve or modify:
        _execute_phase2(feedback if modify else "", "APPROVED" if approve else "MODIFIED")
    elif reject:
        st.session_state.phase = "idle"
        st.session_state.messages.append({
            "role": "assistant",
            "content": "🚫 Decision rejected. Workflow halted.",
        })
        # Save rejection to history
        data_ops.save_decision({
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "REJECTED",
            "context": current_context,
            "feedback": feedback,
        })
        st.rerun()


def _execute_phase2(feedback: str, status: str):
    """Run LangGraph Phase 2: manager → executor"""
    app = st.session_state.get("workflow_app")
    config = st.session_state.get("workflow_config")

    if not app or not config:
        st.error("Workflow state lost. Please restart from Chat tab.")
        return

    try:
        with st.spinner("🔄 Executing decision..."):
            # Inject human feedback if provided
            if feedback:
                app.update_state(config, {"context": [f"Human Feedback: {feedback}"]}, as_node="stock_manager")

            decision_text = ""
            execution_result = ""

            for output in app.stream(None, config=config):
                for node_name, content in output.items():
                    if node_name == "manager" and "decision" in content:
                        decision_text = content["decision"]
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"**🧠 COO Decision:**\n{decision_text[:800]}",
                        })
                    elif "context" in content:
                        execution_result = content["context"][-1]
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"**✅ {node_name}:** {execution_result}",
                        })

            # Save to decision history
            data_ops.save_decision({
                "timestamp": datetime.datetime.now().isoformat(),
                "status": status,
                "decision": decision_text[:1000],
                "execution": execution_result,
                "feedback": feedback,
            })

            st.session_state.phase = "done"
            st.rerun()

    except Exception as e:
        st.error(f"Execution error: {str(e)}")
        st.session_state.phase = "idle"


def _render_execution_results():
    """Show the results of the last completed execution"""
    # Show latest stock update
    stock = data_ops.read_stock()
    last_updated = stock.get("metadata", {}).get("last_updated", "N/A")
    st.caption(f"📦 Last stock update: {last_updated}")


def _render_decision_history():
    """Display past decisions from decision_history/ directory"""
    decisions = data_ops.list_decisions()

    if not decisions:
        st.caption("No decision history yet.")
        return

    for filename in decisions[:10]:  # Show last 10
        decision = data_ops.read_decision(filename)
        if not decision:
            continue

        ts = decision.get("timestamp", filename)
        status = decision.get("status", "UNKNOWN")
        badge_html = render_status_badge(status)

        with st.expander(f"📋 {ts[:19]} — {status}"):
            st.markdown(f"**Status:** {badge_html}", unsafe_allow_html=True)
            if decision.get("feedback"):
                st.markdown(f"**Feedback:** {decision['feedback']}")
            if decision.get("decision"):
                st.markdown(f"**Decision:**\n{decision['decision'][:500]}")
            if decision.get("execution"):
                st.markdown(f"**Execution:** {decision['execution']}")
