import subprocess
import sys
import os

def check_python_version():
    """Ensure Python 3.9+ is being used."""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 9):
        print("❌ Error: kafeAI requires Python 3.9 or higher.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected.")

def install_dependencies():
    """Install requirements from requirements.txt."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    req_file = os.path.join(base_dir, "requirements.txt")
    frontend_req_file = os.path.join(base_dir, "frontend", "requirements_frontend.txt")
    
    if not os.path.exists(req_file):
        print("⚠️ Warning: requirements.txt not found. Skipping dependency installation.")
        return

    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        if os.path.exists(frontend_req_file):
            print("\n📦 Installing Frontend dependencies...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", frontend_req_file])
        print("✅ Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during dependency installation: {e}")
        sys.exit(1)

def install_playwright():
    """Install Playwright and Chromium browser."""
    print("\n🌐 Installing Playwright browser driver...")
    try:
        # First ensure playwright is installed via pip (should be in requirements.txt)
        # Then install the specific browser binaries
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✅ Playwright Chromium installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during Playwright installation: {e}")
        print("💡 You might need to run this command manually: playwright install chromium")
        sys.exit(1)

def run_checks():
    check_python_version()
    install_dependencies()
    install_playwright()

if __name__ == "__main__":
    run_checks()
