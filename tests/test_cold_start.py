"""
Test cold start time with lazy-loading
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_cold_start():
    """Measure cold start time"""
    print("\n" + "="*60)
    print("Testing Cold Start Time with Lazy-Loading")
    print("="*60)
    
    # Measure startup time
    print("\n📊 Measuring startup time...")
    start_time = time.time()
    
    from core.chat_engine import ChatEngine
    
    chat_engine = ChatEngine()
    
    init_time = time.time() - start_time
    print(f"   ChatEngine init: {init_time:.2f}s")
    
    # Initialize (connects to Pinecone, but doesn't load embedding model)
    start_init = time.time()
    chat_engine.initialize()
    full_init_time = time.time() - start_init
    
    total_startup = time.time() - start_time
    
    print(f"   Knowledge base init: {full_init_time:.2f}s")
    print(f"   ✅ Total startup: {total_startup:.2f}s")
    
    # Now test first query (this will load the embedding model)
    print("\n📝 Testing first query (will load embedding model)...")
    start_query = time.time()
    
    response = chat_engine.chat("What are Surya's skills?")
    
    first_query_time = time.time() - start_query
    print(f"   First query time: {first_query_time:.2f}s")
    print(f"   Response: {response[:100]}...")
    
    # Test second query (model already loaded)
    print("\n📝 Testing second query (model already loaded)...")
    start_query2 = time.time()
    
    response2 = chat_engine.chat("Where does he work?")
    
    second_query_time = time.time() - start_query2
    print(f"   Second query time: {second_query_time:.2f}s")
    print(f"   Response: {response2[:100]}...")
    
    # Summary
    print("\n" + "="*60)
    print("📊 Performance Summary:")
    print("="*60)
    print(f"Cold Start Time: {total_startup:.2f}s")
    print(f"First Query (with model load): {first_query_time:.2f}s")
    print(f"Second Query (cached model): {second_query_time:.2f}s")
    print(f"\n✅ Embedding model load deferred to first use!")
    print("="*60)


if __name__ == "__main__":
    test_cold_start()
