"""
Clear Redis Cache
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.redis_cache import RedisSemanticCache

def clear_cache():
    print("Clearing Redis Cache...")
    cache = RedisSemanticCache()
    if cache.is_connected:
        cache.redis.flushdb()
        print("✅ Cache cleared successfully")
    else:
        print("❌ Could not connect to Redis")

if __name__ == "__main__":
    clear_cache()
