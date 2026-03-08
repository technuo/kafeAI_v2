"""
KafeAI Frontend — Data Analytics Tab
Sales dashboards, inventory status, trend charts from daily_reports.
"""
import streamlit as st
import json
import io
from config import COLORS
import data_ops

# Lazy import plotly to avoid import errors if not installed
try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False


def render():
    """Render the Data Analytics tab"""
    st.markdown("### 📊 Data Analytics Center")
    st.caption("Sales trends, inventory status, and business insights from local data.")

    reports = data_ops.list_reports()
    if not reports:
        st.warning("No daily reports found. Upload sales data in the File Manager.")
        return

    # ── Load All Report Data ───────────────────────────
    all_data = []
    for rf in reports:
        report = data_ops.read_report(rf)
        if report:
            date_str = rf.replace(".json", "").replace("_", "-")
            report["_date"] = date_str
            report["_filename"] = rf
            all_data.append(report)

    # ── KPI Cards (Latest Report) ──────────────────────
    latest = all_data[0] if all_data else {}
    sales = latest.get("sales_summary", {})
    payment = latest.get("payment_methods", {})
    perf = latest.get("performance_metrics", {})

    st.markdown(f"#### 📅 Latest Report: `{latest.get('_date', 'N/A')}`")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Gross Sales", f"{sales.get('total_gross', 0):,.0f} SEK")
    with col2:
        st.metric("📈 Net Sales", f"{sales.get('total_net', 0):,.0f} SEK")
    with col3:
        st.metric("🧾 Transactions", payment.get("total_transactions", 0))
    with col4:
        st.metric("👤 Avg / Customer", f"{perf.get('average_purchase_per_customer', 0):,.0f} SEK")

    st.divider()

    # ── Sales Trend Chart ──────────────────────────────
    tab_trend, tab_category, tab_inventory, tab_export = st.tabs([
        "📈 Sales Trend", "📊 Category Breakdown", "📦 Inventory Status", "📥 Export Data"
    ])

    with tab_trend:
        _render_sales_trend(all_data)

    with tab_category:
        _render_category_breakdown(all_data)

    with tab_inventory:
        _render_inventory_status()

    with tab_export:
        _render_export(all_data)


def _render_sales_trend(all_data: list):
    """Line chart of gross/net sales over time"""
    if not HAS_PLOTLY:
        st.warning("Install `plotly` for interactive charts: `pip install plotly`")
        _render_sales_trend_fallback(all_data)
        return

    dates = []
    gross = []
    net = []

    for d in reversed(all_data):  # Chronological order
        dates.append(d["_date"])
        s = d.get("sales_summary", {})
        gross.append(s.get("total_gross", 0))
        net.append(s.get("total_net", 0))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=gross,
        name="Gross Sales",
        mode="lines+markers",
        line=dict(color=COLORS["smart_amber"], width=3),
        marker=dict(size=8),
        fill="tozeroy",
        fillcolor="rgba(180, 230, 142, 0.08)",
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=net,
        name="Net Sales",
        mode="lines+markers",
        line=dict(color=COLORS["paper_cream"], width=2, dash="dot"),
        marker=dict(size=6),
    ))

    fig.update_layout(
        title="SALES TREND",
        xaxis_title="Date",
        yaxis_title="SEK",
        template="plotly_dark",
        height=400,
        font=dict(family="Inter", color=COLORS["text_primary"]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10,37,25,0.6)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_sales_trend_fallback(all_data: list):
    """Simple Streamlit bar chart fallback without Plotly"""
    import pandas as pd
    dates = []
    gross = []
    for d in reversed(all_data):
        dates.append(d["_date"])
        gross.append(d.get("sales_summary", {}).get("total_gross", 0))
    df = pd.DataFrame({"Date": dates, "Gross Sales (SEK)": gross})
    st.bar_chart(df.set_index("Date"))


def _render_category_breakdown(all_data: list):
    """Bar chart of sales by category from latest report"""
    latest = all_data[0] if all_data else {}
    categories = latest.get("sales_by_category", [])

    if not categories:
        st.caption("No category data available.")
        return

    if HAS_PLOTLY:
        names = [c["category"] for c in categories]
        amounts = [c["amount"] for c in categories]
        counts = [c["count"] for c in categories]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=names, y=amounts,
            name="Revenue (SEK)",
            marker_color=COLORS["smart_amber"],
            text=[f"{a:,.0f}" for a in amounts],
            textposition="auto",
        ))
        fig.add_trace(go.Bar(
            x=names, y=counts,
            name="Items Sold",
            marker_color=COLORS["forest_green"],
            text=counts,
            textposition="auto",
            yaxis="y2",
        ))

        fig.update_layout(
            title=f"CATEGORY BREAKDOWN — {latest.get('_date', '')}",
            template="plotly_dark",
            height=400,
            font=dict(family="Inter", color=COLORS["text_primary"]),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(10,37,25,0.6)",
            barmode="group",
            yaxis=dict(title="Revenue (SEK)"),
            yaxis2=dict(title="Items Sold", overlaying="y", side="right"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Fallback table
        for c in categories:
            st.markdown(f"**{c['category']}**: {c['amount']:,.0f} SEK ({c['count']} items)")


def _render_inventory_status():
    """Table of current inventory with low-stock highlighting"""
    stock = data_ops.read_stock()
    inventory = stock.get("inventory", [])
    metadata = stock.get("metadata", {})

    if not inventory:
        st.caption("No inventory data loaded.")
        return

    st.caption(f"Last updated: {metadata.get('last_updated', 'N/A')}")

    # Build table with status indicators
    table_data = []
    for item in inventory:
        qty = item.get("quantity", 0)
        # Simple low-stock heuristic
        if qty <= 1:
            status = "🔴 Critical"
        elif qty <= 3:
            status = "🟡 Low"
        else:
            status = "🟢 OK"

        table_data.append({
            "Item": item["item"],
            "Qty": qty,
            "Unit": item.get("unit", ""),
            "Status": status,
        })

    # Sort by status priority (critical first)
    priority = {"🔴 Critical": 0, "🟡 Low": 1, "🟢 OK": 2}
    table_data.sort(key=lambda x: priority.get(x["Status"], 9))

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Item": st.column_config.TextColumn("Item", width="medium"),
            "Qty": st.column_config.NumberColumn("Quantity", format="%d"),
            "Unit": st.column_config.TextColumn("Unit", width="small"),
            "Status": st.column_config.TextColumn("Status", width="small"),
        },
    )


def _render_export(all_data: list):
    """Export sales data as CSV"""
    st.markdown("#### Download Reports Data")

    # Build CSV
    rows = []
    for d in all_data:
        s = d.get("sales_summary", {})
        p = d.get("payment_methods", {})
        perf = d.get("performance_metrics", {})
        rows.append({
            "date": d["_date"],
            "gross_sales": s.get("total_gross", 0),
            "net_sales": s.get("total_net", 0),
            "vat": s.get("total_vat", 0),
            "transactions": p.get("total_transactions", 0),
            "avg_purchase": perf.get("average_purchase_per_customer", 0),
        })

    if rows:
        import pandas as pd
        df = pd.DataFrame(rows)

        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            data=csv,
            file_name="kafeai_sales_data.csv",
            mime="text/csv",
            use_container_width=True,
        )

        # Excel export
        try:
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False, engine="openpyxl")
            st.download_button(
                "📥 Download Excel",
                data=buffer.getvalue(),
                file_name="kafeai_sales_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        except ImportError:
            st.caption("Install `openpyxl` for Excel export: `pip install openpyxl`")
    else:
        st.caption("No data to export.")
