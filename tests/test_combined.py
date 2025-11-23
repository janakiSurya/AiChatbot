import sys
import os
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api import app

def test_combined():
    print("🚀 Starting Combined Test: Context + Rate Limit (10/hour)...\n")
    
def test_combined():
    print("🚀 Starting Combined Test: Context + Rate Limit (10/hour)...\n")
    
    with TestClient(app) as client:
        headers = {"X-Forwarded-For": "5.6.7.8"} # Unique IP for this test
        
        # Wait for engine initialization
        print("⏳ Waiting for engine to initialize (10s)...")
        import time
        time.sleep(10)
    
    # Complex conversation sequence
    conversation = [
        "What research did he do for his master's?",
        "Which data sources did he use for the research?",
        "Where can I read that?"
    ]
    
    request_count = 0
    
    # We want to send 12 requests total (10 should succeed, 2 should fail)
    # We'll repeat the conversation 4 times
    for loop in range(1, 5):
        print(f"--- Conversation Loop {loop} ---")
        
        for q_idx, query in enumerate(conversation):
            request_count += 1
            print(f"\n📝 Request {request_count}: '{query}'")
            
            response = client.post(
                "/chat", 
                json={"message": query},
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("response", "")
                print(f"✅ Success (200 OK)")
                
                # Only print full answer for the first loop to verify context
                if loop == 1:
                    print(f"🤖 Alfred: {answer}")
                    
            elif response.status_code == 429:
                print("🛑 Blocked (429 Too Many Requests)")
            else:
                print(f"⚠️ Unexpected status: {response.status_code}")

if __name__ == "__main__":
    test_combined()
