import sys
import os
import time
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api import app

def test_rate_limit():
    print("🚀 Testing Rate Limiting (5 requests/hour)...")
    
    # Use a mock client IP for testing
    client = TestClient(app)
    
    # We need to mock the request to come from a specific IP
    # TestClient handles this, but slowapi uses request.client.host or X-Forwarded-For
    
    success_count = 0
    blocked_count = 0
    
    for i in range(1, 8):
        print(f"\n📝 Request {i}...")
        
        try:
            # Simulate a request
            # Note: TestClient requests come from "testclient" host by default
            response = client.post(
                "/chat", 
                json={"message": "test"},
                headers={"X-Forwarded-For": "1.2.3.4"} # Simulate consistent IP
            )
            
            if response.status_code == 200:
                print("✅ Success (200 OK)")
                success_count += 1
            elif response.status_code == 429:
                print("🛑 Blocked (429 Too Many Requests)")
                blocked_count += 1
            else:
                print(f"⚠️ Unexpected status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            
    print("\n📊 Results:")
    print(f"Successful requests: {success_count}")
    print(f"Blocked requests: {blocked_count}")
    
    if success_count == 5 and blocked_count >= 1:
        print("✅ Rate limiting is WORKING!")
    else:
        print("❌ Rate limiting FAILED verification.")
        sys.exit(1)

if __name__ == "__main__":
    test_rate_limit()
