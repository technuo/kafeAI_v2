"""
KafeAI Frontend — Data Operations Layer
All local file I/O abstracted here for future cloud DB swap.
"""
import os
import json
import shutil
import zipfile
import datetime
from typing import Optional
from dotenv import dotenv_values

from config import (
    STOCK_PATH, MENU_PATH, MEMORY_PATH, REPORTS_DIR,
    DECISION_HISTORY_DIR, CACHE_DIR, ENV_PATH, BASE
)


# ── Stock Operations ───────────────────────────────────────────
def read_stock() -> dict:
    """Load current inventory from stock.json"""
    try:
        with open(STOCK_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"inventory": [], "metadata": {}}


def write_stock(data: dict) -> bool:
    """Save inventory data to stock.json"""
    try:
        data["metadata"]["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(STOCK_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception:
        return False


# ── Menu Operations ────────────────────────────────────────────
def read_menu() -> str:
    """Load Menu.md content"""
    try:
        with open(MENU_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def write_menu(content: str) -> bool:
    """Save Menu.md content"""
    try:
        with open(MENU_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception:
        return False


# ── Memory Operations ─────────────────────────────────────────
def read_memory() -> dict:
    """Load memory.json (RL episodes)"""
    try:
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"episodes": [], "global_bias": {"weather_sensitivity": 1.0, "event_optimism": 1.0}}


def write_memory(data: dict) -> bool:
    """Save memory.json"""
    try:
        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


# ── Daily Reports ──────────────────────────────────────────────
def list_reports() -> list:
    """List all daily report files sorted by date (newest first)"""
    try:
        files = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".json")]
        return sorted(files, reverse=True)
    except FileNotFoundError:
        return []


def read_report(filename: str) -> dict:
    """Load a specific daily report"""
    try:
        path = os.path.join(REPORTS_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_report(filename: str, data: bytes) -> bool:
    """Save an uploaded daily report file"""
    try:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        path = os.path.join(REPORTS_DIR, filename)
        with open(path, "wb") as f:
            f.write(data)
        return True
    except Exception:
        return False


def delete_report(filename: str) -> bool:
    """Delete a daily report"""
    try:
        path = os.path.join(REPORTS_DIR, filename)
        os.remove(path)
        return True
    except Exception:
        return False


# ── Decision History ───────────────────────────────────────────
def list_decisions() -> list:
    """List all decision history files"""
    try:
        os.makedirs(DECISION_HISTORY_DIR, exist_ok=True)
        files = [f for f in os.listdir(DECISION_HISTORY_DIR) if f.endswith(".json")]
        return sorted(files, reverse=True)
    except FileNotFoundError:
        return []


def save_decision(decision_data: dict) -> bool:
    """Save a decision to decision_history/"""
    try:
        os.makedirs(DECISION_HISTORY_DIR, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(DECISION_HISTORY_DIR, f"decision_{ts}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(decision_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def read_decision(filename: str) -> dict:
    """Load a specific decision"""
    try:
        path = os.path.join(DECISION_HISTORY_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# ── Environment Config ─────────────────────────────────────────
def read_env() -> dict:
    """Read .env file as key-value dict"""
    try:
        return dict(dotenv_values(ENV_PATH))
    except Exception:
        return {}


def write_env(config: dict) -> bool:
    """Write config dict to .env file, preserving comments for known keys"""
    try:
        lines = []
        lines.append("# KafeAI Configuration (auto-generated by frontend)")
        lines.append(f"GOOGLE_API_KEY={config.get('GOOGLE_API_KEY', '')}")
        lines.append("")
        lines.append("# LangSmith (optional)")
        lines.append(f"LANGCHAIN_TRACING_V2={config.get('LANGCHAIN_TRACING_V2', 'true')}")
        lines.append(f"LANGCHAIN_API_KEY={config.get('LANGCHAIN_API_KEY', '')}")
        lines.append(f"LANGCHAIN_PROJECT={config.get('LANGCHAIN_PROJECT', 'kafeAI-v2')}")
        lines.append("")
        lines.append("# Weather API")
        lines.append(f"WEATHER_API_KEY={config.get('WEATHER_API_KEY', '')}")
        lines.append(f"CITY={config.get('CITY', 'Sundsvall')}")
        lines.append("")
        lines.append("# Nano Banana API")
        lines.append(f"NANO_BANANA_API_KEY={config.get('NANO_BANANA_API_KEY', '')}")

        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return True
    except Exception:
        return False


# ── Project Initialization ─────────────────────────────────────
def init_project_files() -> list:
    """Create missing project directories and empty files. Returns list of created items."""
    created = []

    dirs_to_create = [REPORTS_DIR, DECISION_HISTORY_DIR, CACHE_DIR]
    for d in dirs_to_create:
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
            created.append(f"📁 {os.path.basename(d)}/")

    # Core files with defaults
    defaults = {
        STOCK_PATH: json.dumps({"inventory": [], "metadata": {"last_updated": "", "source": "Menu.md"}}, indent=4),
        MENU_PATH: "## Menu\n\n---\n## Storage\n",
        MEMORY_PATH: json.dumps({"episodes": [], "global_bias": {"weather_sensitivity": 1.0, "event_optimism": 1.0}}, indent=2),
    }
    for path, default_content in defaults.items():
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(default_content)
            created.append(f"📄 {os.path.basename(path)}")

    if not os.path.exists(ENV_PATH):
        write_env({})
        created.append("📄 .env")

    return created


def validate_project_files() -> dict:
    """Check which core files/dirs exist. Returns {name: exists}"""
    checks = {
        "stock.json": os.path.exists(STOCK_PATH),
        "Menu.md": os.path.exists(MENU_PATH),
        "memory.json": os.path.exists(MEMORY_PATH),
        "daily_reports/": os.path.isdir(REPORTS_DIR),
        ".env": os.path.exists(ENV_PATH),
    }
    return checks


# ── Backup & Restore ───────────────────────────────────────────
def create_backup() -> Optional[str]:
    """Create a zip backup of all core project data. Returns zip path."""
    try:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_path = os.path.join(BASE, f"kafeai_backup_{ts}.zip")

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            # Core files
            for f in [STOCK_PATH, MENU_PATH, MEMORY_PATH]:
                if os.path.exists(f):
                    zf.write(f, os.path.relpath(f, BASE))

            # Daily reports
            if os.path.isdir(REPORTS_DIR):
                for rf in os.listdir(REPORTS_DIR):
                    full = os.path.join(REPORTS_DIR, rf)
                    zf.write(full, os.path.relpath(full, BASE))

            # Decision history
            if os.path.isdir(DECISION_HISTORY_DIR):
                for df in os.listdir(DECISION_HISTORY_DIR):
                    full = os.path.join(DECISION_HISTORY_DIR, df)
                    zf.write(full, os.path.relpath(full, BASE))

        return zip_path
    except Exception:
        return None


def restore_backup(zip_data: bytes) -> bool:
    """Restore from a zip backup"""
    try:
        tmp_zip = os.path.join(BASE, "_restore_tmp.zip")
        with open(tmp_zip, "wb") as f:
            f.write(zip_data)

        with zipfile.ZipFile(tmp_zip, "r") as zf:
            zf.extractall(BASE)

        os.remove(tmp_zip)
        return True
    except Exception:
        return False


# ── File Info Helpers ──────────────────────────────────────────
def get_file_info(filepath: str) -> dict:
    """Get file metadata: name, size, modified time"""
    try:
        stat = os.stat(filepath)
        return {
            "name": os.path.basename(filepath),
            "size": stat.st_size,
            "size_display": _format_size(stat.st_size),
            "modified": datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
            "path": filepath,
        }
    except FileNotFoundError:
        return {"name": os.path.basename(filepath), "size": 0, "size_display": "—", "modified": "—", "path": filepath}


def _format_size(size_bytes: int) -> str:
    """Human-readable file size"""
    for unit in ["B", "KB", "MB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} GB"
