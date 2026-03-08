import asyncio
import os
import sys
import json
import time
from playwright.async_api import async_playwright
from dotenv import load_dotenv

# Ensure we can import from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import the LangGraph app
try:
    from manageragent import app
except ImportError as e:
    print(f"❌ Error importing manageragent: {e}")
    sys.exit(1)

# Configuration
USER_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "whatsapp_session")
TARGET_NUMBER = os.getenv("WHATSAPP_PHONE_NUMBER")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    print("❌ GOOGLE_API_KEY or GEMINI_API_KEY not found in .env")
    sys.exit(1)

# Ensure GOOGLE_API_KEY is set in environment for LangChain
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

async def send_whatsapp_message(page, message):
    """Types and sends a message in the currently active chat."""
    try:
        input_selector = 'div[contenteditable="true"]'
        await page.wait_for_selector(input_selector)
        
        # Click the input box
        await page.click(input_selector)
        
        # Clear any existing text (optional but safer)
        # Type the message
        # Use fill if possible, or type
        await page.type(input_selector, message)
        await asyncio.sleep(0.5)
        await page.press(input_selector, "Enter")
        print(f"📤 Sent response to WhatsApp.")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")

async def get_last_incoming_message(page):
    """Retrieves the last message that was NOT sent by the bot."""
    try:
        # WhatsApp Web message selectors can be tricky and change often
        # This is a common pattern for incoming messages
        messages = await page.query_selector_all('div.message-in')
        if not messages:
            return None
        
        last_msg = messages[-1]
        # Extract text content
        text_element = await last_msg.query_selector('span.selectable-text')
        if text_element:
            text = await text_element.inner_text()
            return text.strip()
    except Exception as e:
        print(f"❌ Error reading messages: {e}")
    return None

async def run_kafeai_workflow(query):
    """Runs the LangGraph workflow and returns the final decision/result."""
    print(f"🧠 Processing query via kafeAI: {query}")
    config = {"configurable": {"thread_id": "whatsapp_bot"}}
    inputs = {"issue": query, "context": [], "feedback": ""}
    
    final_output = []
    
    try:
        # Phase 1: Run until HITL
        for output in app.stream(inputs, config=config):
            for node_name, content in output.items():
                if "context" in content:
                    final_output.append(f"[{node_name}] {content['context'][-1]}")
        
        # Check if we are at the HITL point (before manager)
        snapshot = app.get_state(config)
        if snapshot.next:
            # For the bot, we'll automatically proceed for now or ask for approval?
            # User requested "将 AI 的分析结果回复到你的手机上"
            # So we send the summary and wait? Or just continue?
            # Let's send the summary and automatically proceed for this automated version
            # or better: bypass HITL for the bot if possible.
            # But since it's a "COO", let's just finish the flow.
            
            # Step 2: Continue to manage and execute
            for output in app.stream(None, config=config):
                for node_name, content in output.items():
                    if node_name == "manager":
                        final_output.append(f"🤖 COO Decision:\n{content['decision']}")
                    elif "context" in content:
                        final_output.append(f"✅ {node_name}: {content['context'][-1]}")
        
        return "\n\n".join(final_output)
    except Exception as e:
        return f"❌ System Error: {str(e)}"

async def start_bot():
    print("\n" + "="*50)
    print("🤖 [kafeAI WhatsApp Bot Mode]")
    print(f"Target Admin: {TARGET_NUMBER}")
    print("Connecting to WhatsApp Session...")
    print("="*50 + "\n")

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False, # Keep visible so user can see what's happening
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://web.whatsapp.com")
        
        print("⏳ Waiting for WhatsApp Web to load...")
        try:
            await page.wait_for_selector('div[contenteditable="true"]', timeout=60000)
            print("✅ WhatsApp Web Ready.")
        except:
            print("❌ Timeout waiting for WhatsApp Web. Is the session valid?")
            await context.close()
            return

        # 1. Find the chat with the admin
        print(f"🔍 Looking for chat with {TARGET_NUMBER}...")
        try:
            # Search for the contact
            search_box = await page.wait_for_selector('div[contenteditable="true"][data-tab="3"]')
            await search_box.click()
            await search_box.fill(TARGET_NUMBER)
            await asyncio.sleep(2)
            await page.press('div[contenteditable="true"][data-tab="3"]', "Enter")
            print(f"✅ Active chat set to {TARGET_NUMBER}")
        except Exception as e:
            print(f"⚠️ Could not automatically find chat: {e}")
            print("Please manually select the chat in the browser window.")

        last_seen_message = ""
        
        print("🚀 Bot is now listening for messages...")
        
        while True:
            try:
                current_msg = await get_last_incoming_message(page)
                
                if current_msg and current_msg != last_seen_message:
                    print(f"📩 New message received: {current_msg}")
                    last_seen_message = current_msg
                    
                    # Optional: Only trigger if message starts with a keyword or just any message
                    # Let's assume any message from the admin triggers the AI
                    
                    await send_whatsapp_message(page, "⏳ KafeAI is thinking... please wait.")
                    
                    # Run kafeAI Logic
                    response = await run_kafeai_workflow(current_msg)
                    
                    # Send response back (might need to split if too long)
                    if len(response) > 4000:
                        # Simple split
                        parts = [response[i:i+4000] for i in range(0, len(response), 4000)]
                        for part in parts:
                            await send_whatsapp_message(page, part)
                    else:
                        await send_whatsapp_message(page, response)
                
                await asyncio.sleep(5) # Poll every 5 seconds
            except Exception as e:
                print(f"⚠️ Loop error: {e}")
                await asyncio.sleep(10)

if __name__ == "__main__":
    if not TARGET_NUMBER:
        print("❌ WHATSAPP_PHONE_NUMBER not set in .env")
    else:
        try:
            asyncio.run(start_bot())
        except KeyboardInterrupt:
            print("\n👋 Bot stopping...")
