"""
Redis-backed semantic cache using Upstash
Provides persistent caching across server restarts with semantic similarity matching
"""

import json
import hashlib
from typing import Optional
from utils.embedding_manager import embedding_manager
import numpy as np
from config import (
    UPSTASH_REDIS_URL,
    UPSTASH_REDIS_TOKEN,
    USE_REDIS_CACHE,
    logger
)


class RedisSemanticCache:
    """Semantic cache backed by Upstash Redis for persistence"""
    
    def __init__(self, similarity_threshold=0.85, ttl_days=30):
        """
        Initialize Redis semantic cache.
        Uses shared embedding manager instead of loading separate model.
        
        Args:
            similarity_threshold: Minimum similarity score for cache hit
            ttl_days: Time-to-live for cache entries in days
        """
        self.similarity_threshold = similarity_threshold
        self.ttl_seconds = ttl_days * 24 * 60 * 60
        self.redis = None
        self.is_connected = False
        
        # Try to connect to Redis
        if USE_REDIS_CACHE:
            try:
                from upstash_redis import Redis
                self.redis = Redis(url=UPSTASH_REDIS_URL, token=UPSTASH_REDIS_TOKEN)
                # Test connection
                self.redis.ping()
                self.is_connected = True
                logger.info("✅ Connected to Upstash Redis cache")
            except Exception as e:
                logger.warning(f"⚠️  Redis connection failed: {e}. Falling back to in-memory cache.")
                self.is_connected = False
        else:
            logger.info("⚠️  Redis not configured. Using in-memory cache only.")
        
        # Fallback in-memory cache
        self.memory_cache = {}
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text using shared model"""
        return embedding_manager.encode([text])[0]
    
    def _generate_cache_key(self, query: str) -> str:
        """Generate a unique cache key for a query"""
        return f"cache:{hashlib.md5(query.encode()).hexdigest()}"
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def get_cached_response(self, query: str) -> Optional[str]:
        """
        Check cache for similar query and return response
        
        Args:
            query: User's question
            
        Returns:
            Cached response if found, None otherwise
        """
        query_embedding = self._get_embedding(query)
        
        # Try Redis first
        if self.is_connected and self.redis:
            try:
                # Get all cache keys
                cache_keys = self.redis.keys("cache:*")
                
                if not cache_keys:
                    logger.info("❌ Redis cache empty")
                    return None
                
                max_similarity = 0.0
                best_match = None
                
                # Check each cached entry
                for key in cache_keys:
                    try:
                        cached_data = self.redis.get(key)
                        if not cached_data:
                            continue
                        
                        data = json.loads(cached_data)
                        cached_embedding = np.array(data['embedding'])
                        
                        similarity = self._cosine_similarity(query_embedding, cached_embedding)
                        
                        if similarity > max_similarity:
                            max_similarity = similarity
                            best_match = data
                        
                        if similarity >= self.similarity_threshold:
                            logger.info(f"✅ Redis cache hit (similarity: {similarity:.2f})")
                            # Update access count
                            data['access_count'] = data.get('access_count', 0) + 1
                            self.redis.set(key, json.dumps(data), ex=self.ttl_seconds)
                            return data['response']
                    
                    except Exception as e:
                        logger.warning(f"Error processing cache key {key}: {e}")
                        continue
                
                logger.info(f"❌ Redis cache miss (max similarity: {max_similarity:.2f})")
                return None
                
            except Exception as e:
                logger.error(f"Redis error: {e}. Falling back to memory cache.")
                self.is_connected = False
        
        # Fallback to in-memory cache
        return self._check_memory_cache(query, query_embedding)
    
    def _check_memory_cache(self, query: str, query_embedding: np.ndarray) -> Optional[str]:
        """Check in-memory cache as fallback"""
        max_similarity = 0.0
        
        for cached_query, (cached_embedding, cached_response) in self.memory_cache.items():
            similarity = self._cosine_similarity(query_embedding, cached_embedding)
            
            if similarity > max_similarity:
                max_similarity = similarity
            
            if similarity >= self.similarity_threshold:
                logger.info(f"✅ Memory cache hit (similarity: {similarity:.2f})")
                return cached_response
        
        logger.info(f"❌ Memory cache miss (max similarity: {max_similarity:.2f})")
        return None
    
    def add_to_cache(self, query: str, response: str):
        """
        Add query-response pair to cache
        
        Args:
            query: User's question
            response: Generated response
        """
        # Don't cache very short or very long responses
        if len(response) < 50 or len(response) > 1000:
            logger.info(f"⚠️  Not caching: response length {len(response)} outside limits")
            return
        
        # Don't cache error messages
        if "error" in response.lower() or "sorry" in response.lower() or "don't have" in response.lower():
            logger.info("⚠️  Not caching: response contains error/apology")
            return
        
        query_embedding = self._get_embedding(query)
        cache_key = self._generate_cache_key(query)
        
        cache_data = {
            'query': query,
            'response': response,
            'embedding': query_embedding.tolist(),
            'access_count': 1
        }
        
        # Try Redis first
        if self.is_connected and self.redis:
            try:
                self.redis.set(cache_key, json.dumps(cache_data), ex=self.ttl_seconds)
                logger.info(f"💾 Added to Redis cache (TTL: {self.ttl_seconds//86400} days)")
                return
            except Exception as e:
                logger.error(f"Redis error: {e}. Falling back to memory cache.")
                self.is_connected = False
        
        # Fallback to in-memory cache
        self.memory_cache[query] = (query_embedding, response)
        logger.info(f"💾 Added to memory cache (total: {len(self.memory_cache)})")
        
        # Limit memory cache size
        if len(self.memory_cache) > 50:
            # Remove oldest entry
            oldest_key = next(iter(self.memory_cache))
            del self.memory_cache[oldest_key]
            logger.info(f"🗑️  Evicted from memory cache")
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        stats = {
            'redis_connected': self.is_connected,
            'memory_cache_size': len(self.memory_cache)
        }
        
        if self.is_connected and self.redis:
            try:
                cache_keys = self.redis.keys("cache:*")
                stats['redis_cache_size'] = len(cache_keys) if cache_keys else 0
            except:
                stats['redis_cache_size'] = 0
        
        return stats
