"""
KafeAI Frontend — Sidebar: File Manager
Visual management of local project files (reports, menu, stock, memory).
"""
import os
import datetime
import streamlit as st
import json
import data_ops
from config import STOCK_PATH, MENU_PATH, MEMORY_PATH, REPORTS_DIR


def render():
    """Render the File Manager sidebar section"""
    st.markdown("### 📁 File Manager")

    # ── Startup Validation ─────────────────────────────
    validation = data_ops.validate_project_files()
    missing = [k for k, v in validation.items() if not v]

    if missing:
        st.warning(f"Missing: {', '.join(missing)}")
        if st.button("⚡ Auto-Create Missing Files", use_container_width=True, key="init_files"):
            created = data_ops.init_project_files()
            if created:
                st.success(f"Created: {', '.join(created)}")
                st.rerun()

    # ── File Category Selector ─────────────────────────
    file_section = st.selectbox(
        "Category",
        ["📊 Daily Reports", "📄 Core Files (Menu/Stock/Memory)", "🗂️ All Files"],
        key="file_section",
        label_visibility="collapsed",
    )

    if file_section == "📊 Daily Reports":
        _render_reports_manager()
    elif file_section == "📄 Core Files (Menu/Stock/Memory)":
        _render_core_files_editor()
    else:
        _render_all_files()


def _render_reports_manager():
    """Manage daily report files"""
    reports = data_ops.list_reports()
    st.caption(f"{len(reports)} reports found")

    # Upload
    uploaded = st.file_uploader(
        "Upload Report(s)",
        type=["json"],
        accept_multiple_files=True,
        key="report_upload",
    )
    if uploaded:
        for f in uploaded:
            # Auto-rename: YYYYMMDD_storename_report.json
            name = f.name
            if data_ops.save_report(name, f.read()):
                st.success(f"✅ Saved: {name}")
        st.rerun()

    # List existing reports
    for rf in reports[:15]:  # Show last 15
        info = data_ops.get_file_info(os.path.join(REPORTS_DIR, rf))
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.caption(f"📄 {rf}")
        with col2:
            st.caption(info["size_display"])
        with col3:
            if st.button("🗑️", key=f"del_{rf}", help="Delete this report"):
                if data_ops.delete_report(rf):
                    st.rerun()


def _render_core_files_editor():
    """Online editor for Menu.md, stock.json, memory.json"""
    editor_file = st.selectbox(
        "Select file to edit",
        ["Menu.md", "stock.json", "memory.json"],
        key="core_file_select",
    )

    if editor_file == "Menu.md":
        content = data_ops.read_menu()
        edited = st.text_area(
            "Menu.md",
            value=content,
            height=300,
            key="menu_editor",
        )
        if st.button("💾 Save Menu.md", use_container_width=True, key="save_menu"):
            if data_ops.write_menu(edited):
                st.success("✅ Menu.md saved!")
            else:
                st.error("Failed to save.")

    elif editor_file == "stock.json":
        stock = data_ops.read_stock()
        edited = st.text_area(
            "stock.json",
            value=json.dumps(stock, indent=2, ensure_ascii=False),
            height=300,
            key="stock_editor",
        )
        if st.button("💾 Save stock.json", use_container_width=True, key="save_stock"):
            try:
                parsed = json.loads(edited)
                if data_ops.write_stock(parsed):
                    st.success("✅ stock.json saved!")
                else:
                    st.error("Failed to save.")
            except json.JSONDecodeError:
                st.error("Invalid JSON format.")

    elif editor_file == "memory.json":
        memory = data_ops.read_memory()
        edited = st.text_area(
            "memory.json",
            value=json.dumps(memory, indent=2, ensure_ascii=False),
            height=300,
            key="memory_editor",
        )
        if st.button("💾 Save memory.json", use_container_width=True, key="save_memory"):
            try:
                parsed = json.loads(edited)
                if data_ops.write_memory(parsed):
                    st.success("✅ memory.json saved!")
                else:
                    st.error("Failed to save.")
            except json.JSONDecodeError:
                st.error("Invalid JSON format.")


def _render_all_files():
    """Overview of all project files with info"""
    files_to_show = [STOCK_PATH, MENU_PATH, MEMORY_PATH]
    for fp in files_to_show:
        info = data_ops.get_file_info(fp)
        st.caption(f"📄 **{info['name']}** — {info['size_display']} — {info['modified']}")

    reports = data_ops.list_reports()
    st.caption(f"📁 **daily_reports/** — {len(reports)} files")

    decisions = data_ops.list_decisions()
    st.caption(f"📁 **decision_history/** — {len(decisions)} files")
