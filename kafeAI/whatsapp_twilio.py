import os
import sys
import threading
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment
load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import kafeAI core logic
try:
    from manageragent import app
except ImportError as e:
    print(f"❌ Could not import manageragent: {e}")
    sys.exit(1)

app_flask = Flask(__name__)

# Twilio Client Configuration
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_from = os.getenv('TWILIO_FROM_NUMBER')
twilio_client = Client(account_sid, auth_token)

def process_ai_and_respond(sender_number, incoming_msg):
    """Background task to run LangGraph and send result back via Twilio REST API."""
    print(f"🧠 [Background] Processing for {sender_number}...")
    
    config = {"configurable": {"thread_id": f"sms_{sender_number}"}}
    inputs = {"issue": incoming_msg, "context": [], "feedback": ""}
    
    final_output = ["🤖 kafeAI COO 决策报告："]
    
    try:
        # Phase 1: Gathering inputs
        for output in app.stream(inputs, config=config):
            for node_name, content in output.items():
                if "context" in content:
                    msg = content['context'][-1]
                    if "Predictor:" in msg:
                        final_output.append(f"🌤️ 预测：\n{msg.split('Predictor:')[1].strip()}")
                    elif "Inventory Steward" in msg:
                        text = msg.split('Analysis:')[1].strip()
                        final_output.append(f"📦 库存：\n{text[:300]}...")
        
        # Phase 2: Resume for final decision
        for output in app.stream(None, config=config):
            for node_name, content in output.items():
                if node_name == "manager":
                    final_output.append(f"📊 核心决策：\n{content['decision']}")
                elif node_name == "executor":
                    final_output.append(f"✅ 执行：{content['context'][-1]}")
                    
        response_text = "\n\n---\n\n".join(final_output)
        
        # Split and send if too long
        if len(response_text) > 1600:
            parts = [response_text[i:i+1500] for i in range(0, len(response_text), 1500)]
            for part in parts:
                twilio_client.messages.create(
                    from_=twilio_from,
                    to=sender_number,
                    body=part
                )
        else:
            twilio_client.messages.create(
                from_=twilio_from,
                to=sender_number,
                body=response_text
            )
        print(f"📤 [Background] Response sent to {sender_number}")
        
    except Exception as e:
        error_msg = f"❌ kafeAI 处理出错: {str(e)}"
        print(f"  [Error] {error_msg}")
        twilio_client.messages.create(
            from_=twilio_from,
            to=sender_number,
            body=error_msg
        )

@app_flask.route("/whatsapp", methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    sender_number = request.values.get('From', '')
    
    print(f"📩 [Webhook] Request from {sender_number}: {incoming_msg}")
    
    # Start background processing
    threading.Thread(target=process_ai_and_respond, args=(sender_number, incoming_msg)).start()
    
    # Acknowledge immediately to Twilio
    resp = MessagingResponse()
    resp.message("🕒 收到。kafeAI 正在进行多维度分析，请稍候...")
    return str(resp)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 kafeAI Twilio PRO Mode Started")
    print("   Listening on Port 5000")
    print("="*50 + "\n")
    app_flask.run(port=5000)
