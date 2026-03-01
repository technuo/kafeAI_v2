import os
from pathlib import Path

ENV_FILE = Path(__file__).parent.parent / ".env"

def check_env_exists():
    """Check if .env file exists and has necessary keys."""
    if not ENV_FILE.exists():
        return False
    
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    required_keys = ["GEMINI_API_KEY", "WHATSAPP_PHONE_NUMBER"]
    for key in required_keys:
        if f"{key}=" not in content:
            return False
            
    return True

def create_env():
    """Interactively generate the .env file."""
    print("\n" + "="*50)
    print("🌟 Welcome to kafeAI Initialization Wizard 🌟")
    print("We detected that your environment is not configured yet.")
    print("This wizard will guide you through the setup process.")
    print("="*50 + "\n")
    
    print("1️⃣ [Gemini API Key]")
    print("Get it here: https://aistudio.google.com/app/apikey")
    gemini_key = input("👉 Please enter your Gemini API Key: ").strip()
    
    print("\n2️⃣ [WhatsApp Phone Number]")
    print("Format example: +46701234567")
    wa_number = input("👉 Please enter the WhatsApp number for the bot: ").strip()
    
    print("\n3️⃣ [Shop Name]")
    print("Example: Tant Anki & Fröken Sara AB")
    shop_name = input("👉 Please enter your shop name (Press Enter to skip): ").strip()
    
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write(f"GEMINI_API_KEY={gemini_key}\n")
        f.write(f"WHATSAPP_PHONE_NUMBER={wa_number}\n")
        if shop_name:
            f.write(f"SHOP_NAME={shop_name}\n")
            
    if os.name != 'nt':
        os.chmod(ENV_FILE, 0o600)
        
    print("\n✅ Configuration saved to .env file.")

if __name__ == "__main__":
    if not check_env_exists():
        create_env()
    else:
        print("✅ Environment file (.env) detected.")
