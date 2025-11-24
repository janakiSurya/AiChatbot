"""
Test Redis cache integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.redis_cache import RedisSemanticCache
from config import logger


def test_redis_cache():
    """Test Redis cache connection and functionality"""
    print("\n" + "="*60)
    print("Testing Redis Cache Integration")
    print("="*60)
    
    # Initialize cache
    cache = RedisSemanticCache()
    
    print(f"\n📊 Cache Status:")
    print(f"   Redis Connected: {cache.is_connected}")
    
    if not cache.is_connected:
        print("   ⚠️  Using in-memory fallback")
        return
    
    # Test cache operations
    print("\n🧪 Testing Cache Operations:")
    
    # Test 1: Add to cache
    test_query = "What are Surya's skills?"
    test_response = "Surya has expertise in React, Node.js, Python, and GenAI."
    
    print(f"\n1. Adding to cache...")
    cache.add_to_cache(test_query, test_response)
    
    # Test 2: Retrieve from cache (exact match)
    print(f"\n2. Testing exact match...")
    result = cache.get_cached_response(test_query)
    if result:
        print(f"   ✅ Cache hit: {result[:50]}...")
    else:
        print(f"   ❌ Cache miss")
    
    # Test 3: Retrieve from cache (similar query)
    similar_query = "Tell me about his technical skills"
    print(f"\n3. Testing similar query: '{similar_query}'")
    result = cache.get_cached_response(similar_query)
    if result:
        print(f"   ✅ Cache hit: {result[:50]}...")
    else:
        print(f"   ❌ Cache miss")
    
    # Test 4: Get stats
    print(f"\n4. Cache Statistics:")
    stats = cache.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "="*60)
    print("✅ Redis Cache Test Complete!")
    print("="*60)


if __name__ == "__main__":
    test_redis_cache()
