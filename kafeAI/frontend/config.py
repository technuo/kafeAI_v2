"""
KafeAI Frontend — Configuration & Constants
Centralized config for paths, colors, and app settings.
Color system follows kafeAI Brand Guidelines v2.0 (Deep Green)
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

# ── Color Palette (Brand Guidelines v2.0 — Deep Green) ────────
# Inspiration: dark terminal aesthetic meets botanical intelligence
COLORS = {
    # Core Brand Colors
    "deep_espresso":     "#020D08",  # Primary background (deepest green-black)
    "smart_amber":       "#B4E68E",  # Accent: lime-green glow for CTA & highlights

    # Supporting Colors
    "paper_cream":       "#B4E68E",  # Text echoes the accent
    "forest_green":      "#0A2519",  # UI decoration, card bases

    # Derived Palette (dark-mode harmonics)
    "surface_primary":   "#020D08",  # Full-darkness main background
    "surface_elevated":  "#051810",  # Elevated cards / sidebar
    "surface_card":      "#0A2519",  # Card background (deep forest)
    "surface_hover":     "#0F3020",  # Hover states on dark surfaces
    "border_subtle":     "#1D3625",  # Card borders, dividers
    "border_accent":     "#B4E68E",  # Accent borders (green glow)

    # Text Hierarchy
    "text_primary":      "#B4E68E",  # Primary text (lime-green)
    "text_secondary":    "#6A855C",  # Muted text
    "text_tertiary":     "#3D5A33",  # Disabled / placeholder text
    "text_inverse":      "#020D08",  # Text on bright surfaces (green buttons)

    # Accent Variants (CTA & interaction states)
    "amber_bright":      "#C8F0A0",  # Hover on accent elements
    "amber_dim":         "#5C7A4A",  # Pressed / secondary accent
    "amber_glow":        "rgba(180, 230, 142, 0.12)",  # Ambient glow behind cards

    # Semantic Colors (tinted for dark theme harmony)
    "success":           "#4CAF50",
    "success_bg":        "rgba(76, 175, 80, 0.10)",
    "warning":           "#F5A623",
    "warning_bg":        "rgba(245, 166, 35, 0.10)",
    "error":             "#E53935",
    "error_bg":          "rgba(229, 57, 53, 0.10)",
    "info":              "#5B9BD5",
    "info_bg":           "rgba(91, 155, 213, 0.10)",

    # Legacy aliases (backward compat for any external refs)
    "primary_green":     "#0A2519",
    "primary_green_light": "#0F3020",
    "cream":             "#020D08",
    "cream_dark":        "#1D3625",
    "accent_pink":       "#B4E68E",
    "text_dark":         "#B4E68E",
    "text_mid":          "#6A855C",
    "text_light":        "#3D5A33",
    "card_bg":           "#0A2519",
    "sidebar_bg":        "#051810",
    "sidebar_text":      "#B4E68E",
}

# ── App Settings ───────────────────────────────────────────────
APP_NAME = "KAFEAI"
APP_SUBTITLE = "Brewing Intelligence, Growing with Experience."
APP_VERSION = "2.0.0"
GITHUB_REPO = "https://github.com/technuo/kafeAI"
DEFAULT_PORT = 8501

# ── Quick Prompt Templates ─────────────────────────────────────
QUICK_PROMPTS = [
    {"label": "🌤️ @Weather", "prompt": "@weather 帮我查一下明天的天气如何？"},
    {"label": "📦 @Stock", "prompt": "@stock 最近库存还充足吗？有哪些需要补货？"},
    {"label": "💰 @Pricing", "prompt": "@pricing 根据现在的情况，我有必要调整价格吗？"},
    {"label": "📊 Full Analysis", "prompt": "生成今日运营报告 (Full Analysis)"},
    {"label": "💡 @Creative", "prompt": "@creative 帮我出一个明日的营销创意点子。"},
]

# ── Agent Node Names (matches LangGraph workflow) ──────────────
AGENT_NODES = [
    {"id": "router", "label": "Dispatcher", "icon": "🚦"},
    {"id": "post_mortem", "label": "Post-Mortem Analyst", "icon": "📋"},
    {"id": "forecast", "label": "Sales Forecaster", "icon": "📈"},
    {"id": "predictor", "label": "Weather Predictor", "icon": "🌤️"},
    {"id": "stock_manager", "label": "Inventory Steward", "icon": "📦"},
    {"id": "pricing", "label": "Revenue Manager", "icon": "💰"},
    {"id": "creative", "label": "Creative Director", "icon": "🎨"},
    {"id": "manager", "label": "AI COO", "icon": "🧠"},
    {"id": "quick_manager", "label": "Quick Assistant", "icon": "⚡"},
    {"id": "executor", "label": "Order Executor", "icon": "✅"},
]
