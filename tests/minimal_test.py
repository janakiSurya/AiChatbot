#!/usr/bin/env python3
"""
Minimal system test - Single Query
Verifies the pipeline without excessive API usage.
"""

import sys
import os

# Add parent directory to path to allow importing core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.chat_engine import ChatEngine
import time

def main():
    print("🚀 INITIALIZING MINIMAL TEST")
    
    # Initialize chat engine
    chat_engine = ChatEngine()
    
    if not chat_engine.initialize():
        print("❌ Failed to initialize chat engine")
        sys.exit(1)
    
    print("\n✅ System initialized")
    
    # Test query
    query = "Where is he working?"
    print(f"\n📝 QUERY: {query}")
    print("-" * 50)
    
    start_time = time.time()
    try:
        response = chat_engine.chat(query)
        end_time = time.time()
        
        print(f"\n💬 RESPONSE:")
        print(f"   {response}")
        print(f"\n⏱️  Response time: {end_time - start_time:.2f}s")
        
        if response and len(response) > 20:
            print("\n✅ Test passed - Got meaningful response")
        else:
            print("\n⚠️  Test warning - Response seems short or empty")
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
