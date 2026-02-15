import json
import os
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Reuse the same LLM configuration as manageragent
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)

def dynamic_pricing_agent(state):
    """
    Analyzes weather and inventory context to generate a structured promotion.
    """
    print("\n[Dynamic Pricing Agent] Analyzing market conditions...")
    
    # Extract context
    context_str = "\n".join(state.get("context", []))
    
    system_prompt = (
        "You are the Revenue Manager for kafeAI. Your goal is to maximize daily revenue.\n"
        "Analyze the provided context (Weather, Inventory, Events) and decide if a promotion is needed.\n"
        "Triggers:\n"
        "- Bad weather (Snow, Rain, Temp < -10C) -> Boost comfort food/warm drinks.\n"
        "- High perishable inventory (Stock > Target) -> Discount to clear.\n"
        "- Low traffic expected -> High value offer (BOGO).\n\n"
        "If NO promotion is needed, return an empty JSON object: {}.\n"
        "If a promotion IS needed, return a valid JSON object with this schema:\n"
        "{\n"
        "  \"promotion_id\": \"PROMO_NAME\",\n"
        "  \"theme\": \"Marketing Theme (e.g. Cozy Winter)\",\n"
        "  \"product_category\": \"Target Category\",\n"
        "  \"product_item\": \"Specific Item or ALL_CATEGORY\",\n"
        "  \"discount_type\": \"e.g. BOGO_FREE, 50_PERCENT_OFF\",\n"
        "  \"valid_until\": \"YYYY-MM-DD HH:MM:SS\",\n"
        "  \"reason\": \"Brief strategy explanation\",\n"
        "  \"visual_prompt\": \"Keywords for AI image generator (atmosphere, lighting, subject)\",\n"
        "  \"marketing_copy_headline\": \"Catchy Headline (Short)\",\n"
        "  \"marketing_copy_body\": \"Engaging body text (max 20 words)\",\n"
        "  \"price_original\": \"Original Price SEK\",\n"
        "  \"price_promo\": \"Promo Price SEK\"\n"
        "}"
    )
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Current Context:\n{context_str}")
    ])
    
    try:
        # Clean up response
        res_text = response.content
        if isinstance(res_text, list):
            res_text = "".join([c.get("text", "") if isinstance(c, dict) else str(c) for c in res_text])
            
        json_str = res_text.replace("```json", "").replace("```", "").strip()
        
        # Handle cases where the model might return text before/after JSON
        if "{" in json_str:
            json_str = json_str[json_str.find("{"):json_str.rfind("}")+1]
            
        promotion_data = json.loads(json_str)
        
        if not promotion_data:
            return {"context": ["Dynamic Pricing: No promotion active."]}
            
        print(f"  > Generated Promo: {promotion_data.get('promotion_id')}")
        return {
            "promotion_data": promotion_data,
            "context": [f"Dynamic Pricing: Active Promo [{promotion_data.get('promotion_id')}] - {promotion_data.get('reason')}"]
        }
        
    except Exception as e:
        return {"context": [f"Dynamic Pricing Error: {str(e)}"]}
