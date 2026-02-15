import os
import sys

# 将 kafeAI 目录加入路径
sys.path.append(os.path.join(os.path.dirname(__file__), "kafeAI"))

from manageragent import app
import json

def test_workflow():
    config = {"configurable": {"thread_id": "test_thread"}}
    inputs = {"issue": "Test Order", "context": [], "feedback": ""}
    
    print("--- Testing Phase 1 ---")
    for output in app.stream(inputs, config=config):
        print(f"Node: {list(output.keys())[0]}")
    
    # 模拟反馈
    print("--- Injecting Feedback ---")
    app.update_state(config, {"context": ["Human Feedback: Please add 5 units of sallad."]}, as_node="stock_manager")
    
    print("--- Testing Phase 2 ---")
    for output in app.stream(None, config=config):
        node_name = list(output.keys())[0]
        print(f"Node: {node_name}")
        if node_name == "executor":
            print(f"Result: {output['executor']['context'][-1]}")

if __name__ == "__main__":
    test_workflow()
