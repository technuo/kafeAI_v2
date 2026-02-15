import time
import os
import sys

# Add current directory to path so we can import manageragent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from manageragent import app, AgentState

def run_stress_test(iterations=2):
    print(f"--- Starting Stress Test ({iterations} iterations) ---")
    
    total_time = 0
    success_count = 0
    
    for i in range(iterations):
        print(f"\n[Iteration {i+1}/{iterations}]")
        start_time = time.time()
        
        config = {"configurable": {"thread_id": f"stress_test_{i}"}}
        inputs = {"issue": "Stress Test", "context": [], "feedback": ""}
        
        try:
            # Phase 1: Run to interrupt
            print("  > Phase 1: Running to interrupt...")
            for output in app.stream(inputs, config=config):
                pass
            
            # Mock Human Feedback
            print("  > Phase 2: Mocking Human Feedback...")
            snapshot = app.get_state(config)
            if snapshot.next:
                # We supply dummy feedback
                app.update_state(config, {"context": ["Human Feedback: Approved via Stress Test"]}, as_node="stock_manager")
                
                # Resume
                print("  > Phase 3: Resuming execution...")
                for output in app.stream(None, config=config):
                    pass
            
            duration = time.time() - start_time
            print(f"  > Iteration {i+1} completed in {duration:.2f}s")
            total_time += duration
            success_count += 1
            
        except Exception as e:
            print(f"  > Iteration {i+1} FAILED: {e}")

    avg_time = total_time / success_count if success_count > 0 else 0
    print("\n" + "="*40)
    print(f"Stress Test Report")
    print("="*40)
    print(f"Total Iterations: {iterations}")
    print(f"Successful:       {success_count}")
    print(f"Average Latency:  {avg_time:.2f}s")
    print("="*40)

if __name__ == "__main__":
    # Ensure memory.json exists or is handled
    run_stress_test(iterations=2)
