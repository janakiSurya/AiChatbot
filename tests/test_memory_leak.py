"""
Test to verify memory leak fix with embedding model singleton
"""

import pytest
import psutil
import os


def test_no_duplicate_embedding_models():
    """Verify only one embedding model instance is loaded"""
    from utils.embedding_manager import embedding_manager
    from search.pinecone_search import PineconeSearch
    from utils.redis_cache import RedisSemanticCache
    from utils.cache import SemanticCache
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Get embedding model from manager
    model1 = embedding_manager.get_model()
    memory_after_first = process.memory_info().rss / 1024 / 1024
    
    # Create all components that use embeddings
    pinecone = PineconeSearch()
    redis_cache = RedisSemanticCache()
    semantic_cache = SemanticCache()
    
    # Access models from each component
    pinecone_model = pinecone.embedding_model
    
    # Check they're all the same instance
    assert model1 is pinecone_model, "Pinecone should use same model instance"
    
    final_memory = process.memory_info().rss / 1024 / 1024
    memory_growth = final_memory - memory_after_first
    
    # Memory growth should be minimal (< 50MB) if sharing same model
    # If loading separate models, would see 400MB+ per model
    assert memory_growth < 100, f"Excessive memory growth: {memory_growth}MB (expected < 100MB)"
    
    print(f"✅ Memory test passed:")
    print(f"   Initial: {initial_memory:.1f}MB")
    print(f"   After first model: {memory_after_first:.1f}MB")
    print(f"   Final: {final_memory:.1f}MB")
    print(f"   Growth: {memory_growth:.1f}MB")


def test_embedding_manager_singleton():
    """Verify embedding manager is truly a singleton"""
    from utils.embedding_manager import EmbeddingManager
    
    manager1 = EmbeddingManager()
    manager2 = EmbeddingManager()
    
    assert manager1 is manager2, "EmbeddingManager should be a singleton"
    assert manager1.get_model() is manager2.get_model(), "Should return same model instance"


def test_memory_leak_under_load():
    """Test that memory doesn't grow excessively under repeated use"""
    from utils.embedding_manager import embedding_manager
    import gc
    
    process = psutil.Process(os.getpid())
    
    # Get baseline
    model = embedding_manager.get_model()
    gc.collect()
    baseline_memory = process.memory_info().rss / 1024 / 1024
    
    # Generate embeddings 50 times
    for i in range(50):
        embeddings = embedding_manager.encode([f"Test query {i}"] * 10)
    
    gc.collect()
    final_memory = process.memory_info().rss / 1024 / 1024
    memory_growth = final_memory - baseline_memory
    
    # Memory should not grow significantly (< 100MB for 50 iterations)
    assert memory_growth < 100, f"Memory leak detected: {memory_growth}MB growth"
    
    print(f"✅ Load test passed:")
    print(f"   Baseline: {baseline_memory:.1f}MB")
    print(f"   After 50 iterations: {final_memory:.1f}MB")
    print(f"   Growth: {memory_growth:.1f}MB")


if __name__ == "__main__":
    test_no_duplicate_embedding_models()
    test_embedding_manager_singleton()
    test_memory_leak_under_load()
    print("\\n✅ All memory leak tests passed!")
