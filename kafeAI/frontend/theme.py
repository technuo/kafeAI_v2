"""
KafeAI Frontend — Theme & Custom CSS
Brand Guidelines v2.0 compliant dark-green theme.
Visual language: "Botanical intelligence in a dark terminal."
"""
import streamlit as st
from config import COLORS


def apply_theme():
    """Inject custom CSS matching kafeAI Brand Guidelines v2.0"""
    st.markdown(f"""
    <style>
        /* ── Import Google Font (Inter: brand-specified) ───── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        /* ── Global Reset & Typography ─────────────────────── */
        html, body, [class*="st-"], .stMarkdown, .stText, p {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: {COLORS['text_primary']} !important;
            -webkit-font-smoothing: antialiased;
        }}

        /* Brand: Inter Heavy, uppercase, tight tracking for headings */
        h1, h2, h3 {{
            font-family: 'Inter', sans-serif !important;
            font-weight: 800 !important;
            text-transform: uppercase !important;
            letter-spacing: -0.02em !important;
            color: {COLORS['smart_amber']} !important;
        }}
        h4, h5, h6 {{
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
        }}

        /* ── Main Background: Deep Green-Black ─────────────── */
        .stApp {{
            background-color: {COLORS['surface_primary']};
            background-image:
                radial-gradient(ellipse at 20% 50%, rgba(10, 37, 25, 0.25) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, rgba(180, 230, 142, 0.03) 0%, transparent 40%);
        }}

        /* ── Sidebar: Elevated Dark Surface ────────────────── */
        section[data-testid="stSidebar"] {{
            background-color: {COLORS['surface_elevated']} !important;
            border-right: 1px solid {COLORS['border_subtle']} !important;
        }}
        section[data-testid="stSidebar"] .stMarkdown p,
        section[data-testid="stSidebar"] .stMarkdown li,
        section[data-testid="stSidebar"] .stMarkdown label,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {{
            color: {COLORS['text_primary']} !important;
        }}
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stTextInput label,
        section[data-testid="stSidebar"] .stTextArea label {{
            color: {COLORS['text_secondary']} !important;
        }}

        /* ── Tab Styling: Green Active, Ghost Inactive ─────── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 4px;
            background-color: {COLORS['surface_card']};
            border-radius: 10px;
            padding: 4px;
            border: 1px solid {COLORS['border_subtle']};
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: {COLORS['text_secondary']};
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            background-color: {COLORS['surface_hover']};
            color: {COLORS['text_primary']};
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {COLORS['smart_amber']} !important;
            color: {COLORS['text_inverse']} !important;
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(180, 230, 142, 0.25);
        }}

        /* ── Metric Cards: Glassmorphic Dark ───────────────── */
        [data-testid="stMetric"] {{
            background: {COLORS['surface_card']};
            border: 1px solid {COLORS['border_subtle']};
            border-radius: 12px;
            padding: 20px 24px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }}
        [data-testid="stMetric"]:hover {{
            border-color: {COLORS['smart_amber']};
            box-shadow: 0 4px 20px rgba(180, 230, 142, 0.12);
            transform: translateY(-2px);
        }}
        [data-testid="stMetricLabel"] {{
            color: {COLORS['text_secondary']} !important;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}
        [data-testid="stMetricValue"] {{
            color: {COLORS['smart_amber']} !important;
            font-weight: 700;
            font-size: 1.6rem !important;
        }}
        [data-testid="stMetricDelta"] {{
            font-weight: 600;
        }}

        /* ── Buttons: Green CTA, Ghost Secondary ──────────── */
        .stButton > button {{
            background: linear-gradient(135deg, {COLORS['smart_amber']}, {COLORS['amber_dim']});
            color: {COLORS['text_inverse']};
            border: none;
            border-radius: 8px;
            padding: 10px 28px;
            font-weight: 700;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 2px 8px rgba(180, 230, 142, 0.2);
        }}
        .stButton > button:hover {{
            background: linear-gradient(135deg, {COLORS['amber_bright']}, {COLORS['smart_amber']});
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(180, 230, 142, 0.35);
        }}
        .stButton > button:active {{
            transform: translateY(0);
            box-shadow: 0 2px 6px rgba(180, 230, 142, 0.15);
        }}

        /* ── Form Submit Buttons ────────────────────────────── */
        .stFormSubmitButton > button {{
            background: linear-gradient(135deg, {COLORS['smart_amber']}, {COLORS['amber_dim']});
            color: {COLORS['text_inverse']};
            border: none;
            border-radius: 8px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(180, 230, 142, 0.2);
        }}
        .stFormSubmitButton > button:hover {{
            background: linear-gradient(135deg, {COLORS['amber_bright']}, {COLORS['smart_amber']});
            transform: translateY(-1px);
        }}

        /* ── Chat Messages: Speech Bubble Dark ─────────────── */
        [data-testid="stChatMessage"] {{
            background: {COLORS['surface_card']};
            border-radius: 12px;
            border: 1px solid {COLORS['border_subtle']};
            margin-bottom: 8px;
            padding: 16px;
        }}
        [data-testid="stChatMessage"]:hover {{
            border-color: {COLORS['border_accent']};
        }}

        /* ── Chat Input ────────────────────────────────────── */
        [data-testid="stChatInput"] {{
            border-color: {COLORS['border_subtle']} !important;
        }}
        [data-testid="stChatInput"] textarea {{
            background-color: {COLORS['surface_card']} !important;
            color: {COLORS['text_primary']} !important;
            border: 1px solid {COLORS['border_subtle']} !important;
            border-radius: 8px !important;
        }}
        [data-testid="stChatInput"] textarea:focus {{
            border-color: {COLORS['smart_amber']} !important;
            box-shadow: 0 0 0 2px rgba(180, 230, 142, 0.15) !important;
        }}

        /* ── Text Inputs & Text Areas ──────────────────────── */
        .stTextInput input, .stTextArea textarea {{
            background-color: {COLORS['surface_card']} !important;
            color: {COLORS['text_primary']} !important;
            border: 1px solid {COLORS['border_subtle']} !important;
            border-radius: 8px !important;
            transition: border-color 0.2s ease;
        }}
        .stTextInput input:focus, .stTextArea textarea:focus {{
            border-color: {COLORS['smart_amber']} !important;
            box-shadow: 0 0 0 2px rgba(180, 230, 142, 0.12) !important;
        }}
        .stTextInput label, .stTextArea label {{
            color: {COLORS['text_secondary']} !important;
        }}

        /* ── Select Box ────────────────────────────────────── */
        .stSelectbox > div > div {{
            background-color: {COLORS['surface_card']} !important;
            border-color: {COLORS['border_subtle']} !important;
            color: {COLORS['text_primary']} !important;
        }}
        .stSelectbox label {{
            color: {COLORS['text_secondary']} !important;
        }}

        /* ── Radio Buttons ─────────────────────────────────── */
        .stRadio label {{
            color: {COLORS['text_primary']} !important;
        }}

        /* ── Expander: Subtle, Bordered ────────────────────── */
        .streamlit-expanderHeader {{
            background-color: {COLORS['surface_card']};
            border-radius: 8px;
            font-weight: 600;
            color: {COLORS['smart_amber']} !important;
            border: 1px solid {COLORS['border_subtle']};
        }}
        .streamlit-expanderHeader:hover {{
            border-color: {COLORS['smart_amber']};
        }}
        .streamlit-expanderContent {{
            background-color: {COLORS['surface_card']};
            border: 1px solid {COLORS['border_subtle']};
            border-top: none;
            border-radius: 0 0 8px 8px;
        }}

        /* ── Divider ───────────────────────────────────────── */
        hr {{
            border-color: {COLORS['border_subtle']} !important;
            opacity: 0.5;
        }}

        /* ── Cards (custom div class) ──────────────────────── */
        .kafeai-card {{
            background: {COLORS['surface_card']};
            border: 1px solid {COLORS['border_subtle']};
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 12px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .kafeai-card:hover {{
            border-color: {COLORS['smart_amber']};
            box-shadow: 0 6px 24px rgba(180, 230, 142, 0.08);
            transform: translateY(-2px);
        }}
        .kafeai-card-header {{
            font-family: 'Inter', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.02em;
            color: {COLORS['smart_amber']};
            margin-bottom: 16px;
            padding-bottom: 10px;
            border-bottom: 1px solid {COLORS['border_subtle']};
        }}

        /* ── Status Badges ─────────────────────────────────── */
        .status-badge {{
            display: inline-block;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}
        .status-success {{
            background: {COLORS['success_bg']};
            color: {COLORS['success']};
            border: 1px solid rgba(76, 175, 80, 0.2);
        }}
        .status-warning {{
            background: {COLORS['warning_bg']};
            color: {COLORS['warning']};
            border: 1px solid rgba(245, 166, 35, 0.2);
        }}
        .status-error {{
            background: {COLORS['error_bg']};
            color: {COLORS['error']};
            border: 1px solid rgba(229, 57, 53, 0.2);
        }}
        .status-pending {{
            background: {COLORS['info_bg']};
            color: {COLORS['info']};
            border: 1px solid rgba(91, 155, 213, 0.2);
        }}

        /* ── Header: Green Branded ─────────────────────────── */
        .kafeai-header {{
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 8px 0 24px 0;
        }}
        .kafeai-title {{
            font-family: 'Inter', sans-serif;
            font-size: 2rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: -0.02em;
            color: {COLORS['smart_amber']};
            /* Subtle green text-shadow for glow */
            text-shadow: 0 0 40px rgba(180, 230, 142, 0.15);
        }}
        .kafeai-subtitle {{
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            font-weight: 400;
            font-style: italic;
            color: {COLORS['text_secondary']};
            margin-top: -2px;
            letter-spacing: 0.02em;
        }}

        /* ── Scrollbar: Minimal Green ──────────────────────── */
        ::-webkit-scrollbar {{
            width: 5px;
            height: 5px;
        }}
        ::-webkit-scrollbar-track {{
            background: {COLORS['surface_primary']};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {COLORS['border_subtle']};
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS['smart_amber']};
        }}

        /* ── Log Viewer: Monospace on Dark ──────────────────── */
        .log-line {{
            font-family: 'Consolas', 'Monaco', 'Fira Code', monospace;
            font-size: 0.78rem;
            padding: 3px 10px;
            border-bottom: 1px solid rgba(29, 54, 37, 0.5);
            transition: background 0.15s ease;
        }}
        .log-line:hover {{
            background: {COLORS['surface_hover']};
        }}
        .log-info  {{ color: {COLORS['info']}; }}
        .log-warn  {{ color: {COLORS['warning']}; }}
        .log-error {{ color: {COLORS['error']}; }}

        /* ── Data Frame / Table ─────────────────────────────── */
        .stDataFrame {{
            border: 1px solid {COLORS['border_subtle']};
            border-radius: 8px;
            overflow: hidden;
        }}

        /* ── Progress Bar ──────────────────────────────────── */
        .stProgress > div > div > div {{
            background-color: {COLORS['smart_amber']} !important;
        }}

        /* ── Alerts/Toast Overrides ─────────────────────────── */
        .stAlert {{
            border-radius: 8px !important;
        }}

        /* ── File Uploader ─────────────────────────────────── */
        [data-testid="stFileUploader"] {{
            border-color: {COLORS['border_subtle']} !important;
        }}

        /* ── Download Button ───────────────────────────────── */
        .stDownloadButton > button {{
            background: transparent !important;
            border: 1px solid {COLORS['smart_amber']} !important;
            color: {COLORS['smart_amber']} !important;
            box-shadow: none !important;
        }}
        .stDownloadButton > button:hover {{
            background: rgba(180, 230, 142, 0.1) !important;
            transform: translateY(-1px);
        }}

        /* ── Quick Action Button Grid ──────────────────────── */
        .quick-action-grid {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin: 8px 0 16px 0;
        }}
        .quick-action-btn {{
            background: {COLORS['surface_card']};
            border: 1px solid {COLORS['border_subtle']};
            border-radius: 8px;
            padding: 8px 16px;
            color: {COLORS['text_primary']};
            font-size: 0.82rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .quick-action-btn:hover {{
            border-color: {COLORS['smart_amber']};
            color: {COLORS['smart_amber']};
            background: {COLORS['surface_hover']};
        }}

        /* ── Ambient Glow Behind Hero Area ──────────────────── */
        .kafeai-glow {{
            position: relative;
        }}
        .kafeai-glow::before {{
            content: '';
            position: absolute;
            top: -40px;
            left: 50%;
            transform: translateX(-50%);
            width: 300px;
            height: 200px;
            background: radial-gradient(
                ellipse, rgba(180, 230, 142, 0.06) 0%, transparent 70%
            );
            pointer-events: none;
            z-index: 0;
        }}

        /* ── Agent Card (Monitor Tab) ──────────────────────── */
        .agent-card {{
            background: {COLORS['surface_card']};
            border: 1px solid {COLORS['border_subtle']};
            border-radius: 10px;
            padding: 16px;
            text-align: center;
            transition: all 0.3s ease;
        }}
        .agent-card:hover {{
            border-color: {COLORS['smart_amber']};
            box-shadow: 0 4px 16px rgba(180, 230, 142, 0.08);
        }}
        .agent-card .agent-icon {{
            font-size: 1.8rem;
            margin-bottom: 6px;
        }}
        .agent-card .agent-label {{
            font-weight: 600;
            font-size: 0.82rem;
            color: {COLORS['text_primary']};
            margin-bottom: 8px;
        }}

        /* ── Steam Animation (brand element) ───────────────── */
        @keyframes steam {{
            0%   {{ opacity: 0.6; transform: translateY(0) scaleX(1); }}
            50%  {{ opacity: 0.3; transform: translateY(-8px) scaleX(1.1); }}
            100% {{ opacity: 0;   transform: translateY(-16px) scaleX(0.9); }}
        }}
        .steam-line {{
            display: inline-block;
            width: 2px;
            height: 24px;
            background: linear-gradient(to top, {COLORS['smart_amber']}, transparent);
            margin: 0 3px;
            animation: steam 2s ease-in-out infinite;
        }}
        .steam-line:nth-child(2) {{ animation-delay: 0.4s; height: 18px; }}
        .steam-line:nth-child(3) {{ animation-delay: 0.8s; height: 20px; }}

        /* ── Micro-animation: fade-in for content ──────────── */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(12px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        .fade-in {{
            animation: fadeInUp 0.4s ease-out forwards;
        }}

        /* ── Caption Override ──────────────────────────────── */
        .stCaption, small {{
            color: {COLORS['text_tertiary']} !important;
        }}
    </style>
    """, unsafe_allow_html=True)


def render_card(title: str, content: str):
    """Render a styled card component"""
    st.markdown(f"""
    <div class="kafeai-card fade-in">
        <div class="kafeai-card-header">{title}</div>
        {content}
    </div>
    """, unsafe_allow_html=True)


def render_agent_card(icon: str, label: str, badge_html: str):
    """Render a styled agent status card for the monitor tab"""
    st.markdown(f"""
    <div class="agent-card fade-in">
        <div class="agent-icon">{icon}</div>
        <div class="agent-label">{label}</div>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)


def render_steam():
    """Render the kafeAI brand steam animation element"""
    st.markdown("""
    <div style="text-align:center; margin: 4px 0;">
        <span class="steam-line"></span>
        <span class="steam-line"></span>
        <span class="steam-line"></span>
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
