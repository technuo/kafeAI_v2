"""
KafeAI Frontend — Theme & Custom CSS
Logo-matching styling injected via st.markdown.
"""
import streamlit as st
from config import COLORS

def apply_theme():
    """Inject custom CSS that matches the KafeAI logo color scheme"""
    st.markdown(f"""
    <style>
        /* ── Import Google Font ─────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* ── Global Typography ──────────────────────────── */
        html, body, [class*="st-"], .stMarkdown, .stText, p {{
            font-family: 'Inter', sans-serif;
            color: {COLORS['text_dark']} !important;
        }}

        h1, h2, h3, h4, h5, h6 {{
             color: {COLORS['text_dark']} !important;
        }}

        /* ── Main Background ────────────────────────────── */
        .stApp {{
            background-color: {COLORS['cream']};
        }}

        /* ── Sidebar ────────────────────────────────────── */
        section[data-testid="stSidebar"] {{
            background-color: {COLORS['sidebar_bg']};
            color: {COLORS['sidebar_text']};
        }}
        section[data-testid="stSidebar"] .stMarkdown p,
        section[data-testid="stSidebar"] .stMarkdown li,
        section[data-testid="stSidebar"] .stMarkdown label,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {{
            color: {COLORS['sidebar_text']} !important;
        }}
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stTextInput label,
        section[data-testid="stSidebar"] .stTextArea label {{
            color: {COLORS['sidebar_text']} !important;
        }}

        /* ── Tab Styling ────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: {COLORS['cream_dark']};
            border-radius: 12px;
            padding: 4px;
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            padding: 8px 20px;
            font-weight: 500;
            color: {COLORS['text_mid']};
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {COLORS['primary_green']} !important;
            color: white !important;
            border-radius: 8px;
        }}

        /* ── Metric Cards ───────────────────────────────── */
        [data-testid="stMetric"] {{
            background: white;
            border: 1px solid {COLORS['cream_dark']};
            border-radius: 12px;
            padding: 16px 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}
        [data-testid="stMetricLabel"] {{
            color: {COLORS['text_mid']};
            font-size: 0.85rem;
        }}
        [data-testid="stMetricValue"] {{
            color: {COLORS['primary_green']};
            font-weight: 700;
        }}

        /* ── Buttons ────────────────────────────────────── */
        .stButton > button {{
            background-color: {COLORS['primary_green']};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 24px;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        .stButton > button:hover {{
            background-color: {COLORS['primary_green_light']};
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(45, 90, 61, 0.3);
        }}

        /* ── Chat Messages ──────────────────────────────── */
        [data-testid="stChatMessage"] {{
            background: white;
            border-radius: 12px;
            border: 1px solid {COLORS['cream_dark']};
            margin-bottom: 8px;
        }}

        /* ── Expander ───────────────────────────────────── */
        .streamlit-expanderHeader {{
            background-color: white;
            border-radius: 8px;
            font-weight: 600;
            color: {COLORS['primary_green']};
        }}

        /* ── Cards (custom div class) ───────────────────── */
        .kafeai-card {{
            background: white;
            border: 1px solid {COLORS['cream_dark']};
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}
        .kafeai-card-header {{
            font-size: 1.1rem;
            font-weight: 700;
            color: {COLORS['primary_green']};
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid {COLORS['cream_dark']};
        }}

        /* ── Status Badges ──────────────────────────────── */
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .status-success {{
            background: #E8F5E9;
            color: #2E7D32;
        }}
        .status-warning {{
            background: #FFF3E0;
            color: #E65100;
        }}
        .status-error {{
            background: #FFEBEE;
            color: #C62828;
        }}
        .status-pending {{
            background: #E3F2FD;
            color: #1565C0;
        }}

        /* ── Header ─────────────────────────────────────── */
        .kafeai-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 0 0 16px 0;
        }}
        .kafeai-title {{
            font-size: 1.8rem;
            font-weight: 800;
            color: {COLORS['primary_green']};
            letter-spacing: -0.5px;
        }}
        .kafeai-subtitle {{
            font-size: 0.9rem;
            color: {COLORS['text_mid']};
            margin-top: -4px;
        }}

        /* ── Scrollbar ──────────────────────────────────── */
        ::-webkit-scrollbar {{
            width: 6px;
        }}
        ::-webkit-scrollbar-track {{
            background: {COLORS['cream']};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {COLORS['primary_green']};
            border-radius: 3px;
        }}

        /* ── Log Viewer ─────────────────────────────────── */
        .log-line {{
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.8rem;
            padding: 2px 8px;
            border-bottom: 1px solid {COLORS['cream_dark']};
        }}
        .log-info {{ color: {COLORS['info']}; }}
        .log-warn {{ color: {COLORS['warning']}; }}
        .log-error {{ color: {COLORS['error']}; }}
    </style>
    """, unsafe_allow_html=True)


def render_card(title: str, content: str):
    """Render a styled card component"""
    st.markdown(f"""
    <div class="kafeai-card">
        <div class="kafeai-card-header">{title}</div>
        {content}
    </div>
    """, unsafe_allow_html=True)


def render_status_badge(status: str) -> str:
    """Return HTML for a colored status badge"""
    status_map = {
        "success": "status-success",
        "running": "status-pending",
        "error": "status-error",
        "warning": "status-warning",
        "pending": "status-pending",
        "MATCH": "status-success",
        "OVERTURNED": "status-warning",
        "PENDING": "status-pending",
    }
    css_class = status_map.get(status, "status-pending")
    return f'<span class="status-badge {css_class}">{status}</span>'
