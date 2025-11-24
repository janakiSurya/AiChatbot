"""
Test Health Endpoint
Verifies that the /health endpoint works correctly for cron jobs
"""

import sys
import os
from fastapi.testclient import TestClient

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import app

client = TestClient(app)

def test_health_endpoint():
    print("\n" + "="*60)
    print("Testing /health Endpoint")
    print("="*60)
    
    try:
        response = client.get("/health")
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "healthy" and "timestamp" in data:
                print("\n✅ Health Check: PASS")
                print("   - Endpoint is accessible")
                print("   - Returns 200 OK")
                print("   - JSON structure is correct")
                return True
            else:
                print("\n❌ Health Check: FAIL (Invalid response structure)")
                return False
        else:
            print(f"\n❌ Health Check: FAIL (Status code {response.status_code})")
            return False
            
    except Exception as e:
        print(f"\n❌ Health Check Error: {e}")
        return False

if __name__ == "__main__":
    success = test_health_endpoint()
    sys.exit(0 if success else 1)
