import asyncio
import os
from playwright.async_api import async_playwright

USER_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "whatsapp_session")

async def link_whatsapp():
    """Launch a visible browser to guide user through WhatsApp QR scan."""
    print("\n" + "="*50)
    print("📱 [WhatsApp Linker]")
    print("We are opening a browser window for WhatsApp Web.")
    print("1. Please scan the QR code with your phone.")
    print("2. Once logged in, DO NOT close the browser manually.")
    print("3. The wizard will detect the login and save your session.")
    print("="*50 + "\n")

    async with async_playwright() as p:
        # Using persistent context to save login state
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,  # Must be False for user to see QR
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://web.whatsapp.com")
        
        print("⏳ Waiting for you to scan the QR code and login...")
        
        # Simple detection logic: wait for a common selector that appears after login
        # (e.g., the search bar or chat list)
        try:
            # Wait for up to 2 minutes for the user to scan
            await page.wait_for_selector('div[contenteditable="true"]', timeout=120000)
            print("\n✅ WhatsApp logged in successfully!")
            print(f"Session data saved in: {USER_DATA_DIR}")
        except Exception as e:
            print("\n❌ Error or Timeout: Could not detect WhatsApp login.")
            print("Please try running the setup again.")
            await context.close()
            return False
            
        # Give it a few seconds to sync
        await asyncio.sleep(5)
        await context.close()
        return True

if __name__ == "__main__":
    asyncio.run(link_whatsapp())
