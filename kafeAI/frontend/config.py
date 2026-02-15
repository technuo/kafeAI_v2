"""
KafeAI Frontend — Configuration & Constants
Centralized config for paths, colors, and app settings.
"""
import os

# ── Project Root (kafeAI v2/) ──────────────────────────────────
def get_base_path() -> str:
    """Returns the project root: two levels up from frontend/config.py"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_backend_path() -> str:
    """Returns the backend directory: kafeAI/"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── File Paths ─────────────────────────────────────────────────
BASE = get_base_path()
STOCK_PATH = os.path.join(BASE, "stock.json")
MENU_PATH = os.path.join(BASE, "Menu.md")
MEMORY_PATH = os.path.join(BASE, "memory.json")
REPORTS_DIR = os.path.join(BASE, "daily_reports")
DECISION_HISTORY_DIR = os.path.join(BASE, "decision_history")
CACHE_DIR = os.path.join(BASE, "cache")
ENV_PATH = os.path.join(get_backend_path(), ".env")
LOGO_PATH = os.path.join(BASE, "kafeAI v2 logo.png")

# ── Color Palette (from logo) ─────────────────────────────────
COLORS = {
    "primary_green": "#2D5A3D",       # Deep forest green (logo text)
    "primary_green_light": "#3D7A52", # Lighter green for hover
    "cream": "#F5F0E1",               # Warm cream background
    "cream_dark": "#E8E0CC",          # Darker cream for cards
    "accent_pink": "#D4847C",         # Cheek blush accent
    "text_dark": "#1A1A1A",           # Primary text
    "text_mid": "#5A5A5A",            # Secondary text
    "text_light": "#8A8A8A",          # Muted text
    "success": "#4CAF50",
    "warning": "#FF9800",
    "error": "#E53935",
    "info": "#2196F3",
    "card_bg": "#FFFFFF",
    "sidebar_bg": "#2D5A3D",
    "sidebar_text": "#F5F0E1",
}

# ── App Settings ───────────────────────────────────────────────
APP_NAME = "KafeAI"
APP_SUBTITLE = "Cafe Logic — AI-Powered Restaurant Management"
APP_VERSION = "2.0.0"
GITHUB_REPO = "https://github.com/technuo/kafeAI"
DEFAULT_PORT = 8501

# ── Quick Prompt Templates ─────────────────────────────────────
QUICK_PROMPTS = [
    {"label": "🌤️ Weekend Strategy", "prompt": "Weekend Strategy"},
    {"label": "📦 Inventory Check", "prompt": "Inventory Check"},
    {"label": "🌧️ Weather Brief", "prompt": "Weather Brief"},
    {"label": "📊 Sales Review", "prompt": "Daily Sales Review"},
    {"label": "💡 Promotion Ideas", "prompt": "Promotion Ideas"},
]

# ── Agent Node Names (matches LangGraph workflow) ──────────────
AGENT_NODES = [
    {"id": "post_mortem", "label": "Post-Mortem Analyst", "icon": "📋"},
    {"id": "forecast", "label": "Sales Forecaster", "icon": "📈"},
    {"id": "predictor", "label": "Weather Predictor", "icon": "🌤️"},
    {"id": "stock_manager", "label": "Inventory Steward", "icon": "📦"},
    {"id": "pricing", "label": "Revenue Manager", "icon": "💰"},
    {"id": "creative", "label": "Creative Director", "icon": "🎨"},
    {"id": "manager", "label": "AI COO", "icon": "🧠"},
    {"id": "executor", "label": "Order Executor", "icon": "✅"},
]
