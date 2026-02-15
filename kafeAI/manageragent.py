import os
import operator
import requests
import json
import datetime
from typing import Annotated, TypedDict, List
from dotenv import load_dotenv

# 导入 LangGraph 和 LangChain 组件
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. 加载配置
load_dotenv()

# 导入自定义 Agent 逻辑
from post_mortem_agent import post_mortem_agent
from forecasting_agent import forecasting_agent
from dynamic_pricing_agent import dynamic_pricing_agent
from poster_agent import poster_agent

# 2. 定义状态结构
class AgentState(TypedDict):
    issue: str
    context: Annotated[List[str], operator.add]
    decision: str
    feedback: str # 用户反馈
    promotion_data: dict
    poster_path: str
    target_date: str # NEW: For tracking prediction date in RL

# 3. 初始化 Gemini (使用你之前验证成功的名称)
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)

# --- 定义 Agent 节点 ---

# 预测 Agent：接入真实天气 API
def prediction_agent(state: AgentState):
    api_key = os.getenv("WEATHER_API_KEY")
    city = os.getenv("CITY", "Sundsvall")
    
    # 获取预报数据 (forecast.json)
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=2&aqi=no"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # 提取明天（index 1）的预报，因为餐饮业通常为明天做决策
        forecast = data['forecast']['forecastday'][1]['day']
        condition = forecast['condition']['text']
        rain_chance = forecast['daily_chance_of_rain']
        avg_temp = forecast['avgtemp_c']
        
        weather_info = f"Forecast for tomorrow in {city}: {condition}, {avg_temp}°C. Rain Chance: {rain_chance}%."
        
        # 基础节日逻辑
        event_info = "No major local events scheduled."
        # 如果需要恢复活动，取消下面这行的注释
        # event_info = "Local Event: Music Festival happening tomorrow."
        
        target_date = data['forecast']['forecastday'][1]['date']
        
        return {
            "context": [f"Predictor: {weather_info} | {event_info}"],
            "target_date": target_date
        }
    except Exception as e:
        return {"context": [f"Predictor Error: Failed to fetch weather. {str(e)}"]}

# 库存 Agent：关联 Menu.md 和 stock.json
def inventory_agent(state: AgentState):
    # 1. 加载库存数据
    # 注意：根据 list_dir 结果，这些文件在父目录 d:\2026\kafeAI v2\ 下
    # 但是在运行脚本时，路径取决于工作目录。
    # 这里我们使用绝对路径或者相对路径（如果是在根目录运行）
    # 既然 manageragent.py 在 d:\2026\kafeAI v2\kafeAI\ 下
    # 而 Menu.md 在 d:\2026\kafeAI v2\ 下
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    menu_path = os.path.join(base_path, "Menu.md")
    stock_path = os.path.join(base_path, "stock.json")

    try:
        with open(menu_path, 'r', encoding='utf-8') as f:
            menu_content = f.read()
        with open(stock_path, 'r', encoding='utf-8') as f:
            stock_data = json.load(f)
    except Exception as e:
        return {"context": [f"Inventory Error: Failed to load data. {str(e)}"]}

    # 2. 结合预测背景进行分析
    forecast_context = "\n".join(state["context"])
    
    system_prompt = (
        "You are the Inventory Steward for kafeAI. "
        "Your goal is to analyze current stock against the menu and storage targets. "
        "CRITICAL: YOUR REPORT MUST BE IN ENGLISH ONLY.\n\n"
        "Data provided:\n"
        "- Menu & Target Storage: (See text below)\n"
        "- Current Stock: (See JSON below)\n"
        "- External Context: (Weather, events, etc.)\n\n"
        "Menu & Target Storage Content:\n"
        f"{menu_content}\n\n"
        "Current Stock JSON:\n"
        f"{json.dumps(stock_data, indent=2)}\n\n"
        "Your report should be concise but professional, highlighting:\n"
        "1. Critical shortages (Current < Target or expected high demand)\n"
        "2. Recommended replenishment amounts\n"
        "3. Strategy adjustments based on the forecast provided."
    )
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Analyze current situation based on context:\n{forecast_context}")
    ])
    
    # 强制提取纯文本，过滤掉签名元数据
    res_text = response.content
    if isinstance(res_text, list):
        res_text = "".join([c.get("text", "") if isinstance(c, dict) else str(c) for c in res_text])
    
    return {"context": [f"Inventory Steward Analysis:\n{res_text}"]}

# 决策中枢 Manager Agent
def manager_agent(state: AgentState):
    context_str = "\n".join(state["context"])
    
    # --- RAG Retrieval: Continuous RL ---
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    memory_path = os.path.join(base_path, "memory.json")
    lessons_learned = ""
    
    if os.path.exists(memory_path):
        try:
            with open(memory_path, 'r', encoding='utf-8') as f:
                mem_db = json.load(f)
            # 提取过去所有的 OVERTURNED 案例中的 reflection/correction
            overturned = [ep for ep in mem_db.get("episodes", []) if ep.get("status") == "OVERTURNED"]
            if overturned:
                lessons_text = "\n".join([f"- Date {ep['date']}: {ep.get('bias_correction')}" for ep in overturned[-3:]]) # 只取最近3条
                lessons_learned = f"\n\nCRITICAL LESSONS FROM PAST MISTAKES:\n{lessons_text}\n"
        except Exception:
            pass
            
    # 设定 AI COO 的性格：专业、效率至上、对风险敏感
    system_prompt = (
        "You are the AI COO of kafeAI, a restaurant in Sweden. "
        "Your style is sharp, data-driven, and ruthlessly efficient. "
        "You must weigh the 'Local Event' against the 'Weather Forecast'. "
        "Note: In Sweden, rain significantly kills terrace (Uteservering) culture. "
        "If it rains, people stay home; if it's sunny, demand triples.\n\n"
        f"{lessons_learned}"
        "Your response MUST include:\n"
        "1. Analysis (Weather vs Event impact)\n"
        "2. Action (Specific order quantities & staffing advice)\n"
        "3. Reasoning (Why this is the most profitable path)"
    )
    
    start_time = datetime.datetime.now()
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Current Context:\n{context_str}")
    ])
    end_time = datetime.datetime.now()
    latency = (end_time - start_time).total_seconds()
    
    # 简单的 Token 估算 (或使用 response.response_metadata)
    usage = response.response_metadata.get("usage_metadata", {}) if hasattr(response, "response_metadata") else {}
    token_log = f"Latency: {latency:.2f}s | Tokens: {usage}"
    print(f"\n[Manager Performance]: {token_log}")
    
    # 强制提取纯文本，过滤掉签名元数据
    res_text = response.content
    if isinstance(res_text, list):
        res_text = "".join([c.get("text", "") if isinstance(c, dict) else str(c) for c in res_text])
    
    return {"decision": res_text}

# 自动化下单 Agent：执行决策并更新库存
def order_execution_agent(state: AgentState):
    decision = state.get("decision", "")
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    stock_path = os.path.join(base_path, "stock.json")
    
    # 加载现有库存以供 LLM 参考 key
    with open(stock_path, 'r', encoding='utf-8') as f:
        stock_data = json.load(f)
    valid_items = [item['item'] for item in stock_data['inventory']]
    
    # 使用 LLM 解析决策中的订购数量
    system_prompt = (
        "You are the Order Executioner. Parse the provided COO decision and extract a JSON list of items to order. "
        "Each object should have 'item' and 'amount_to_add'. "
        f"IMPORTANT: You MUST use the exact item names from this list: {valid_items}. "
        "If an item in the decision is not in the list, try to map it to the closest match or exclude it. "
        "If no specific order is mentioned, return an empty list: []."
        "\n\nOutput format example: [{\"item\": \"sallad\", \"amount_to_add\": 10}]"
    )
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Decision to parse:\n{decision}")
    ])
    
    try:
        # 提取内容并简单清理可能包含的 markdown 块
        res_text = response.content
        if isinstance(res_text, list):
            res_text = "".join([c.get("text", "") if isinstance(c, dict) else str(c) for c in res_text])
            
        content = res_text.replace("```json", "").replace("```", "").strip()
        orders = json.loads(content)
        
        if not orders:
            return {"context": ["Order Execution: No items to order based on decision."]}
        
        # 加载并更新库存
        with open(stock_path, 'r', encoding='utf-8') as f:
            stock_data = json.load(f)
        
        updates = []
        for order in orders:
            item_name = order['item'].lower()
            amount = order['amount_to_add']
            found = False
            for entry in stock_data['inventory']:
                if entry['item'].lower() == item_name:
                    try:
                        entry['quantity'] += int(amount)
                    except (ValueError, TypeError):
                        updates.append(f"{item_name} (Invalid amount: {amount})")
                        continue
                    updates.append(f"{item_name} (+{amount})")
                    found = True
                    break
            if not found:
                # 如果没找到，可以选择新增或忽略，这里暂定记录 log
                updates.append(f"{item_name} (New item, ignored for safety)")

        # 保存更新后的库存
        stock_data['metadata']['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(stock_path, 'w', encoding='utf-8') as f:
            json.dump(stock_data, f, indent=4, ensure_ascii=False)
            
        # --- Recording Episode for RL ---
        memory_path = os.path.join(base_path, "memory.json")
        target_date = state.get("target_date")
        if target_date and os.path.exists(memory_path):
            try:
                with open(memory_path, 'r', encoding='utf-8') as mf:
                    mem_db = json.load(mf)
                    
                # 检查是否已存在该日期的记录（避免重复添加）
                existing = next((ep for ep in mem_db["episodes"] if ep["date"] == target_date), None)
                if not existing:
                    # 简化 stored context，只取 predictor 的部分
                    prediction_summary = next((c for c in state["context"] if "Predictor:" in c), "Unknown Context")
                    
                    new_episode = {
                        "date": target_date,
                        "prediction_summary": prediction_summary,
                        "decision": decision[:500] + "...", # Truncate for storage
                        "status": "PENDING",
                        "bias_correction": ""
                    }
                    mem_db["episodes"].append(new_episode)
                    
                    # 保持 episode 列表大小适中 (例如只保留最近 60 天)
                    if len(mem_db["episodes"]) > 60:
                        mem_db["episodes"] = mem_db["episodes"][-60:]

                    with open(memory_path, 'w', encoding='utf-8') as mf:
                        json.dump(mem_db, mf, indent=2, ensure_ascii=False)
                    print(f"[RL System]: Recorded new episode for {target_date}")
            except Exception as ex:
                print(f"[RL System Error]: Failed to record episode. {str(ex)}")

        return {"context": [f"Order Execution Successful: Updated {', '.join(updates)}"]}
    except Exception as e:
        return {"context": [f"Order Execution Error: {str(e)}"]}

# --- 构建工作流图 ---



workflow = StateGraph(AgentState)

workflow.add_node("post_mortem", lambda state: post_mortem_agent(state, llm))
workflow.add_node("forecast", lambda state: forecasting_agent(state, llm))
workflow.add_node("predictor", prediction_agent)
workflow.add_node("stock_manager", inventory_agent)
workflow.add_node("pricing", dynamic_pricing_agent)
workflow.add_node("creative", poster_agent)
workflow.add_node("manager", manager_agent)
workflow.add_node("executor", order_execution_agent)

# 设置工作流路径
workflow.set_entry_point("post_mortem")
workflow.add_edge("post_mortem", "forecast")
workflow.add_edge("forecast", "predictor")
workflow.add_edge("predictor", "stock_manager")
workflow.add_edge("stock_manager", "pricing")
workflow.add_edge("pricing", "creative")
workflow.add_edge("creative", "manager")
workflow.add_edge("manager", "executor")
workflow.add_edge("executor", END)

# 初始化内存保存器
checkpointer = MemorySaver()

# 编译图形，在 manager 节点前中断以进行 HITL 审批
app = workflow.compile(
    checkpointer=checkpointer,
    interrupt_before=["manager"]
)

# --- 运行执行 ---

if __name__ == "__main__":
    print(f"--- kafeAI v3.0: HITL & Order Loop Enabled ---")
    config = {"configurable": {"thread_id": "1"}}
    inputs = {"issue": "Weekend Strategy", "context": [], "feedback": ""}
    
    try:
        # 第一阶段：运行到中断点 (manager 之前)
        print("\n[Running Phase 1: Gathering inputs...]")
        for output in app.stream(inputs, config=config):
            for node_name, content in output.items():
                if "context" in content:
                    print(f"Node {node_name} Update: {content['context'][-1]}")

        # 模拟人类在环操作
        print("\n" + "="*50)
        print("HUMAN-IN-THE-LOOP APPROVAL")
        print("="*50)
        snapshot = app.get_state(config)
        
        current_context = snapshot.values.get('context', [])
        analysis = current_context[-1] if current_context else "No analysis available yet."
        print(f"Current Analysis Context:\n{analysis}")
        
        # Display Promotion Details
        promo = snapshot.values.get('promotion_data')
        poster = snapshot.values.get('poster_path')
        if promo:
            print("\n" + "-"*30)
            print(f"PROPOSED PROMOTION: {promo.get('promotion_id')}")
            print(f"Theme: {promo.get('theme')}")
            print(f"Offer: {promo.get('discount_type')} on {promo.get('product_item')}")
            print(f"Headline: {promo.get('marketing_copy_headline')}")
            if poster:
                print(f"Poster Generated: {poster}")
            print("-"*30)
        
        user_input = input("\nEnter feedback/approval (press Enter to skip): ").strip()
        
        # 第二阶段：更新状态并继续运行
        print("\n[Running Phase 2: Finalizing decision and execution...]")
        if user_input:
            # 注入人类反馈到 context 中
            app.update_state(config, {"context": [f"Human Feedback: {user_input}"]}, as_node="stock_manager")
        
        for output in app.stream(None, config=config):
            for node_name, content in output.items():
                print(f"\n[Node: {node_name}]")
                if node_name == "manager":
                    decision = content['decision']
                    print(f"COO'S DECISION:\n{decision}")
                elif "context" in content:
                    print(f"Update: {content['context'][-1]}")
                    
    except Exception as e:
        print(f"\n[System Error]: {e}")
