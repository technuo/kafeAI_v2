import asyncio
import sys
import os

# Add parent directory to sys.path to allow imports from setup folder
sys.path.append(os.path.dirname(__file__))

import env_check
import init_env
import wa_linker

def print_header():
    print("\n" + "🚀" * 20)
    print("   kafeAI SETUP WIZARD")
    print("🚀" * 20 + "\n")

async def main_wizard():
    print_header()
    
    # 1. Environment and Dependencies Check
    print("📦 [Step 1/3] Checking Environment & Dependencies")
    env_check.run_checks()
    
    # 2. Configuration Initialization
    print("\n⚙️ [Step 2/3] Configuring Environment Variables")
    if not init_env.check_env_exists():
        init_env.create_env()
    else:
        print("✅ Configuration already exists.")
        choice = input("Would you like to reconfigure? (y/N): ").strip().lower()
        if choice == 'y':
            init_env.create_env()
            
    # 3. WhatsApp Linkage
    print("\n📱 [Step 3/3] Linking WhatsApp Account")
    if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "whatsapp_session")):
        print("✅ Existing WhatsApp session found.")
        choice = input("Would you like to re-link or change account? (y/N): ").strip().lower()
        if choice == 'y':
            await wa_linker.link_whatsapp()
    else:
        success = await wa_linker.link_whatsapp()
        if not success:
            print("❌ Setup failed during WhatsApp linkage.")
            sys.exit(1)
            
    print("\n" + "="*50)
    print("🎉 kafeAI Setup Complete!")
    print("You can now start the application.")
    print("="*50 + "\n")

if __name__ == "__main__":
    try:
        asyncio.run(main_wizard())
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n🔥 An unexpected error occurred: {e}")
        sys.exit(1)
