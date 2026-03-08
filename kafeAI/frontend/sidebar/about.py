"""
KafeAI Frontend — Sidebar: About & Open Source
Project info, issue template, version check, data backup/restore.
"""
import os
import datetime
import streamlit as st
import data_ops
from config import APP_NAME, APP_VERSION, GITHUB_REPO, COLORS, LOGO_PATH


def render():
    """Render the About & Open Source sidebar section"""

    # ── About Panel ────────────────────────────────────
    with st.expander("ℹ️ About KafeAI", expanded=False):
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=120)
        st.markdown(f"""
        **{APP_NAME}** v{APP_VERSION}

        AI-powered café management system built with LangGraph.
        Multi-agent pipeline for forecasting, inventory, pricing, and decisions.

        🔗 [GitHub]({GITHUB_REPO})
        """)

    # ── Data Backup / Restore ──────────────────────────
    with st.expander("💾 Data Backup", expanded=False):
        if st.button("📦 Create Backup (ZIP)", use_container_width=True, key="create_backup"):
            zip_path = data_ops.create_backup()
            if zip_path:
                with open(zip_path, "rb") as f:
                    st.download_button(
                        "📥 Download Backup",
                        data=f.read(),
                        file_name=os.path.basename(zip_path),
                        mime="application/zip",
                    )
                st.success(f"Backup created: {os.path.basename(zip_path)}")
            else:
                st.error("Backup failed.")

        st.divider()
        uploaded_zip = st.file_uploader(
            "Restore from backup",
            type=["zip"],
            key="restore_zip",
        )
        if uploaded_zip:
            if st.button("⚠️ Restore (Overwrites Current Data)", use_container_width=True, key="do_restore"):
                if data_ops.restore_backup(uploaded_zip.read()):
                    st.success("✅ Data restored successfully!")
                    st.rerun()
                else:
                    st.error("Restore failed.")

    # ── Issue Template ─────────────────────────────────
    with st.expander("🐛 Report Issue", expanded=False):
        st.markdown("Generate a pre-filled issue template for GitHub:")
        issue_desc = st.text_area(
            "Describe the issue",
            placeholder="What happened? What did you expect?",
            height=80,
            key="issue_desc",
        )
        if st.button("📋 Generate Template", use_container_width=True, key="gen_issue"):
            if issue_desc:
                template = _generate_issue_template(issue_desc)
                st.code(template, language="markdown")
                st.caption("Copy the above and paste it in a new GitHub Issue.")
            else:
                st.warning("Please describe the issue first.")

    # ── Version Check ──────────────────────────────────
    with st.expander("🔄 Version", expanded=False):
        st.markdown(f"**Current:** v{APP_VERSION}")
        st.caption("Check GitHub for latest releases.")
        st.link_button("View Releases", f"{GITHUB_REPO}/releases", use_container_width=True)


def _generate_issue_template(description: str) -> str:
    """Generate a GitHub issue template with system info"""
    import platform
    import sys

    template = f"""## Bug Report

**KafeAI Version:** {APP_VERSION}
**Python:** {sys.version.split()[0]}
**OS:** {platform.system()} {platform.release()}
**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}

### Description
{description}

### Steps to Reproduce
1.
2.
3.

### Expected Behavior


### Actual Behavior


### Logs
```
(Paste relevant logs from the System Monitor tab)
```

### Screenshots
(If applicable)
"""
    return template
