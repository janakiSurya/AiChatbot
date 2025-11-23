import sys
import os
import logging

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging to see cache hits/misses
logging.basicConfig(level=logging.INFO)

from utils.cache import SemanticCache

def test_cache_reproduction():
    print("🚀 Starting Cache Reproduction Test...")
    
    # Initialize cache
    cache = SemanticCache()
    
    q1 = "where is his native"
    q2 = "what is his native place"
    response = "Surya is originally from India. He completed his Bachelor's degree there before moving to the US for his Master's."
    
    print(f"\n1. Adding '{q1}' to dynamic cache...")
    cache.add_to_dynamic_cache(q1, response)
    
    print(f"   Cache size: {len(cache.dynamic_cache)}")
    
    print(f"\n2. Querying '{q2}' (should hit cache)...")
    cached_resp = cache.get_cached_response(q2)
    
    if cached_resp:
        print(f"✅ HIT! Response: {cached_resp}")
    else:
        print("❌ MISS! Cache returned None")
        
    # Check similarity manually using the cache's model to be sure
    embedding1 = cache.model.encode([q1])[0]
    embedding2 = cache.model.encode([q2])[0]
    import numpy as np
    similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    print(f"\nInternal Similarity: {similarity:.4f}")
    print(f"Threshold: {cache.similarity_threshold}")

if __name__ == "__main__":
    test_cache_reproduction()
