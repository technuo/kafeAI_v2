import os
import json
import operator
from typing import List, TypedDict, Annotated
import datetime
from langchain_core.messages import SystemMessage, HumanMessage

# 定义复盘所需的常量
COSTS = {
    "RENT_MONTHLY": 60000,
    "STAFF_MONTHLY": 50000,
    "UTILITIES_MONTHLY": 2000,
    "COGS_RATE": 0.30
}

DAILY_FIXED_COST = (COSTS["RENT_MONTHLY"] + COSTS["UTILITIES_MONTHLY"] + COSTS["STAFF_MONTHLY"]) / 30

def post_mortem_agent(state, llm=None):
    """
    分析前一天的销售数据并与预测进行比对。
    如果提供了 llm，则会读取 memory.json 进行偏差分析 (Reinforcement Learning)。
    """
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_dir = os.path.join(base_path, "daily_reports")
    memory_path = os.path.join(base_path, "memory.json")
    
    # 获取最新的报告日期（这里假设我们处理的是今天之前的一份）
    try:
        report_files = sorted([f for f in os.listdir(reports_dir) if f.endswith(".json")], reverse=True)
        if not report_files:
            return {"context": ["Post-mortem: No daily reports found."]}
        
        report_path = os.path.join(reports_dir, report_files[0])
        with open(report_path, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
            
        sales_summary = report_data.get("sales_summary", {})
        gross_sales = sales_summary.get("total_gross", 0)
        net_sales = sales_summary.get("total_net", 0)
        report_date = report_files[0].replace(".json", "") # e.g., 2026_02_14
        
        # 1. 财务价值评估 (Value Assessment)
        cogs = net_sales * COSTS["COGS_RATE"]
        gross_profit = net_sales - cogs - DAILY_FIXED_COST
        
        staff_saving = 0
        if "MVS" in state.get("decision", "") or "Minimum Viable Staffing" in state.get("decision", ""):
            staff_saving = (COSTS["STAFF_MONTHLY"] / 30) * 0.4
            
        performance_report = (
            f"--- Financial Post-mortem ({report_date}) ---\n"
            f"Actual Gross Sales: {gross_sales} SEK\n"
            f"Net Sales: {net_sales} SEK\n"
            f"Operating Profit (Daily): {gross_profit:.2f} SEK\n"
        )
        
        calibration_notes = []
        
        # 2. Reinforcement Learning: Bias Capture
        if llm and os.path.exists(memory_path):
            with open(memory_path, 'r', encoding='utf-8') as mf:
                memory_db = json.load(mf)
            
            # 查找匹配的 episode (假设 memory 中的 date 也是 YYYY_MM_DD 格式，或者我们需要转换)
            # manager 存的时候可能是 2026-02-14，这里 filename 是 2026_02_14
            target_date_iso = report_date.replace("_", "-")
            
            episode = next((ep for ep in memory_db.get("episodes", []) if ep.get("date") == target_date_iso), None)
            
            if episode and episode.get("status") == "PENDING":
                # 使用 LLM 分析偏差
                prediction_summary = episode.get("prediction_summary", "N/A")
                decision_summary = episode.get("decision", "N/A")
                
                analysis_prompt = (
                    "You are the Evaluator. Compare the Prediction vs Actuals.\n"
                    f"Prediction: {prediction_summary}\n"
                    f"Decision Taken: {decision_summary}\n"
                    f"Actual Result: Gross Sales {gross_sales}, Net {net_sales}.\n\n"
                    "Did we significantly over-predict or under-predict? Was the decision 'OVERTURNED' by reality?\n"
                    "Output JSON: {\"status\": \"MATCH\" or \"OVERTURNED\", \"reflection\": \"...\", \"bias_correction\": \"...\"}"
                )
                
                response = llm.invoke([SystemMessage(content=analysis_prompt)])
                try:
                    res_text = response.content.replace("```json", "").replace("```", "").strip()
                    analysis_result = json.loads(res_text)
                    
                    episode["actual_summary"] = f"Gross: {gross_sales}, Net: {net_sales}"
                    episode["status"] = analysis_result.get("status", "COMPLETED")
                    episode["reflection"] = analysis_result.get("reflection", "")
                    episode["bias_correction"] = analysis_result.get("bias_correction", "")
                    
                    # 更新 memory.json
                    with open(memory_path, 'w', encoding='utf-8') as mf:
                        json.dump(memory_db, mf, indent=2, ensure_ascii=False)
                        
                    calibration_notes.append(f"RL Update: Episode {target_date_iso} marked as {episode['status']}.")
                    if episode["status"] == "OVERTURNED":
                        calibration_notes.append(f"Lesson: {episode['bias_correction']}")
                        
                except Exception as e:
                    calibration_notes.append(f"RL Analysis Failed: {str(e)}")

        return {"context": [performance_report + "\n" + " | ".join(calibration_notes)]}
        
    except Exception as e:
        return {"context": [f"Post-mortem Error: {str(e)}"]}
