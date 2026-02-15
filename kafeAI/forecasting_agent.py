import os
import json
import requests
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

def forecasting_agent(state, llm):
    """
    结合历史销售数据和天气预测明天的销售目标。
    """
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_dir = os.path.join(base_path, "daily_reports")
    
    try:
        # 1. 获取最近 3 天的历史数据
        report_files = sorted([f for f in os.listdir(reports_dir) if f.endswith(".json")], reverse=True)[:3]
        history = []
        for rf in report_files:
            with open(os.path.join(reports_dir, rf), 'r', encoding='utf-8') as f:
                data = json.load(f)
                history.append({
                    "date": rf.replace(".json", ""),
                    "total_gross": data["sales_summary"]["total_gross"],
                    "categories": data["sales_by_category"]
                })
        
        # 2. 获取天气预测 (从 state 里的 predictor 节点获取)
        forecast_context = "\n".join(state.get("context", []))
        
        system_prompt = (
            "You are the Sales Forecasting Expert for kafeAI. "
            "Based on the provided historical sales and weather forecast, predict tomorrow's sales targets. "
            "Output your prediction in a clear, structured way.\n\n"
            "History (Last 3 days):\n"
            f"{json.dumps(history, indent=2)}\n\n"
            "Forecast Context:\n"
            f"{forecast_context}"
        )
        
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content="What are the projected sales targets for tomorrow?")
        ])
        
        res_text = response.content
        if isinstance(res_text, list):
            res_text = "".join([c.get("text", "") if isinstance(c, dict) else str(c) for c in res_text])
            
        return {"context": [f"Sales Forecast Report:\n{res_text}"]}
        
    except Exception as e:
        return {"context": [f"Forecasting Error: {str(e)}"]}
