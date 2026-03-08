import sys
import os

# Add relevant paths
sys.path.insert(0, os.path.join(os.getcwd(), 'kafeAI'))

from kafeAI.manageragent import app

def test_routing(issue):
    print(f"\n{'='*50}")
    print(f">>> Testing input: {issue}")
    print(f"{'='*50}")
    config = {"configurable": {"thread_id": f"test_{issue[:10]}"}}
    inputs = {"issue": issue, "context": [], "feedback": ""}
    
    try:
        for output in app.stream(inputs, config=config):
            for node_name, content in output.items():
                print(f"\n[EXECUTION] Node Finished: {node_name}")
                if "context" in content:
                    print(f"    - Context Update: {content['context'][-1][:200]}...")
                if "decision" in content:
                    print(f"    - Decision: {content['decision'][:200]}...")
                if "routing_mode" in content:
                    print(f"    - Router set mode: {content['routing_mode']}")
                    print(f"    - Router set target: {content['target_node']}")
    except Exception as e:
        print(f"ERROR during execution: {e}")

if __name__ == "__main__":
    # Test 1: Full Report (no @)
    # test_routing("Weekend Strategy")
    
    # Test 2: Single Agent (@weather)
    test_routing("@weather 帮我查查明天的天气")
    
    # Test 3: Single Agent (@stock)
    test_routing("@stock 那边的咖啡豆够用吗？")
