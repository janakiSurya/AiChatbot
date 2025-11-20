import sys
import os
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api import app

def test_chat_endpoint():
    print("🚀 Testing API /chat endpoint...")
    
    with TestClient(app) as client:
        # Test health check
        response = client.get("/")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            sys.exit(1)
            
        # Test Question 1
        q1 = "What is Surya's current role?"
        print(f"\n📝 Question 1: {q1}")
        response = client.post("/chat", json={"message": q1})
        if response.status_code == 200:
            print(f"💬 Answer: {response.json()['response']}")
        else:
            print(f"❌ Failed: {response.text}")

        # Test Question 2
        q2 = "Does he know React?"
        print(f"\n📝 Question 2: {q2}")
        response = client.post("/chat", json={"message": q2})
        if response.status_code == 200:
            print(f"💬 Answer: {response.json()['response']}")
        else:
            print(f"❌ Failed: {response.text}")

if __name__ == "__main__":
    test_chat_endpoint()
