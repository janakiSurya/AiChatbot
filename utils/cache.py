"""
Semantic cache for chatbot responses
Uses sentence embeddings to detect similar queries and return cached responses
Includes both static pre-defined cache and dynamic LRU cache
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Optional, List, Dict, Tuple
from collections import OrderedDict
import random
from config import logger


class SemanticCache:
    """Cache responses using semantic similarity with hybrid static + dynamic caching"""
    
    def __init__(self, similarity_threshold=0.85, max_dynamic_cache=50):
        """Initialize semantic cache with embedding model"""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.similarity_threshold = similarity_threshold
        self.max_dynamic_cache = max_dynamic_cache
        
        # Static cache (pre-defined common questions)
        self.static_cache = self._initialize_static_cache()
        
        # Dynamic cache (learns from traffic)
        self.dynamic_cache = OrderedDict()  # {query: (embedding, response, access_count)}
        
        logger.info(f"✅ Semantic cache initialized:")
        logger.info(f"   - Static cache: {len(self.static_cache)} categories")
        logger.info(f"   - Dynamic cache: max {max_dynamic_cache} entries")
    
    def _initialize_static_cache(self) -> Dict:
        """Initialize cache with common queries and their variations"""
        cache_data = {
            "skills": {
                "queries": [
                    "What are his skills?",
                    "Tell me about his technical abilities",
                    "What technologies does he know?",
                    "What is his tech stack?"
                ],
                "responses": [
                    "Surya has expertise in React, Node.js, Python, MongoDB, and AWS. He specializes in full-stack development with modern frameworks and has recently been integrating Generative AI capabilities into applications using OpenAI APIs.",
                    "He's skilled in React, Node.js, Python, MongoDB, and AWS. His expertise spans full-stack development with a focus on performance and clean architecture, plus recent work with GenAI integration.",
                    "His technical skills include React, Node.js, Python, MongoDB, and AWS. He builds scalable web applications and has been working with Generative AI technologies like OpenAI to create intelligent features."
                ]
            },
            "current_role": {
                "queries": [
                    "Where does he work?",
                    "What is his current job?",
                    "Where is he working now?",
                    "What's his current role?"
                ],
                "responses": [
                    "Surya is currently working at Acer America, USA as a Full Stack & GenAI Developer since July 2024. He integrates OpenAI GPT-4 into internal tools and develops AI-powered knowledge assistants.",
                    "He's working at Acer America as a Full Stack & GenAI Developer since July 2024, where he builds AI-powered internal tools and knowledge assistants using GPT-4.",
                    "Currently, he works at Acer America, USA as a Full Stack & GenAI Developer (since July 2024), focusing on integrating AI capabilities into internal support tools."
                ]
            },
            "experience": {
                "queries": [
                    "Tell me about his experience",
                    "What's his work history?",
                    "How many years of experience?",
                    "What companies has he worked for?"
                ],
                "responses": [
                    "Surya has over 4 years of experience in full-stack development. He's worked at Acer America (2024-present), Mindtree (2020-2022), and has built multiple AI-powered projects including chatbots and spell-check applications.",
                    "He has 4+ years of professional experience, including roles at Acer America and Mindtree. His background spans full-stack development, cloud deployments on AWS, and recent work with Generative AI.",
                    "With over 4 years of experience, Surya has worked at companies like Acer America and Mindtree, building scalable web applications and integrating AI capabilities."
                ]
            },
            "education": {
                "queries": [
                    "What is his education?",
                    "Where did he study?",
                    "What degree does he have?",
                    "Tell me about his educational background"
                ],
                "responses": [
                    "Surya holds a Master's degree in Computer Science from California State University, Los Angeles (2022-2024) and a Bachelor's degree in Computer Science from JNTUH College of Engineering (2016-2020).",
                    "He has a Master's in Computer Science from Cal State LA (2022-2024) and a Bachelor's in Computer Science from JNTUH College of Engineering (2016-2020).",
                    "His educational background includes an MS in Computer Science from California State University, Los Angeles and a BS in Computer Science from JNTUH College of Engineering."
                ]
            },
            "projects": {
                "queries": [
                    "What projects has he built?",
                    "Tell me about his projects",
                    "Show me his work",
                    "What has he developed?"
                ],
                "responses": [
                    "Surya has built several notable projects including an AI-powered spell-check app using ChatGPT API, a real-time chat application with WebSocket, an e-commerce platform with payment integration, and various AI-powered internal tools at Acer.",
                    "He's developed projects like an AI spell-check application, a real-time chat app, an e-commerce platform, and AI-powered knowledge assistants. His work demonstrates expertise in both traditional web development and modern AI integration.",
                    "His project portfolio includes an AI-powered spell-check app, real-time chat applications, e-commerce platforms, and GenAI-powered internal tools, showcasing his full-stack and AI capabilities."
                ]
            }
        }
        
        # Pre-compute embeddings for all cached queries
        cache = {}
        for category, data in cache_data.items():
            embeddings = self.model.encode(data["queries"])
            cache[category] = {
                "embeddings": embeddings,
                "responses": data["responses"],
                "last_used_index": 0  # For rotation
            }
        
        return cache
    
    def get_cached_response(self, query: str) -> Optional[str]:
        """
        Check if query is similar to cached queries and return response
        Checks both static and dynamic caches
        
        Args:
            query: User's question
            
        Returns:
            Cached response if found, None otherwise
        """
        query_embedding = self.model.encode([query])[0]
        
        # First, check static cache (pre-defined common questions)
        for category, data in self.static_cache.items():
            similarities = np.dot(data["embeddings"], query_embedding) / (
                np.linalg.norm(data["embeddings"], axis=1) * np.linalg.norm(query_embedding)
            )
            
            max_similarity = np.max(similarities)
            
            if max_similarity >= self.similarity_threshold:
                logger.info(f"✅ Static cache hit for '{category}' (similarity: {max_similarity:.2f})")
                
                # Rotate through response variations
                responses = data["responses"]
                index = data["last_used_index"]
                response = responses[index]
                data["last_used_index"] = (index + 1) % len(responses)
                
                return response
        
        # Second, check dynamic cache (learned from traffic)
        max_dynamic_similarity = 0.0
        
        for cached_query, (cached_embedding, cached_response, access_count) in self.dynamic_cache.items():
            similarity = np.dot(cached_embedding, query_embedding) / (
                np.linalg.norm(cached_embedding) * np.linalg.norm(query_embedding)
            )
            
            if similarity > max_dynamic_similarity:
                max_dynamic_similarity = similarity
            
            if similarity >= self.similarity_threshold:
                logger.info(f"✅ Dynamic cache hit (similarity: {similarity:.2f}, accessed {access_count} times)")
                
                # Update access count and move to end (most recently used)
                self.dynamic_cache.move_to_end(cached_query)
                self.dynamic_cache[cached_query] = (cached_embedding, cached_response, access_count + 1)
                
                return cached_response
        
        logger.info(f"❌ Cache miss (max similarity: {max_dynamic_similarity:.2f})")
        return None
    
    def add_to_dynamic_cache(self, query: str, response: str):
        """
        Add a new query-response pair to dynamic cache
        Implements LRU eviction when cache is full
        
        Args:
            query: User's question
            response: Generated response
        """
        # Don't cache very short or very long responses
        if len(response) < 50 or len(response) > 1000:
            logger.info(f"⚠️ Not caching: response length {len(response)} outside limits")
            return
        
        # Don't cache error messages
        if "error" in response.lower() or "sorry" in response.lower():
            logger.info("⚠️ Not caching: response contains error/apology")
            return
        
        query_embedding = self.model.encode([query])[0]
        
        # Check if similar query already exists
        for cached_query, (cached_embedding, _, _) in self.dynamic_cache.items():
            similarity = np.dot(cached_embedding, query_embedding) / (
                np.linalg.norm(cached_embedding) * np.linalg.norm(query_embedding)
            )
            if similarity >= 0.95:  # Very similar, don't add duplicate
                logger.info(f"⚠️ Not caching: similar query exists (similarity: {similarity:.2f})")
                return
        
        # Add to cache
        self.dynamic_cache[query] = (query_embedding, response, 1)
        
        # Evict least recently used if cache is full
        if len(self.dynamic_cache) > self.max_dynamic_cache:
            evicted_query = next(iter(self.dynamic_cache))
            del self.dynamic_cache[evicted_query]
            logger.info(f"🗑️  Evicted from dynamic cache: '{evicted_query[:50]}...'")
        
        logger.info(f"💾 Added to dynamic cache (total: {len(self.dynamic_cache)})")
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        total_accesses = sum(count for _, _, count in self.dynamic_cache.values())
        return {
            "static_categories": len(self.static_cache),
            "dynamic_entries": len(self.dynamic_cache),
            "dynamic_total_accesses": total_accesses
        }


def is_greeting_only(query: str) -> bool:
    """
    Check if query is just a greeting without a question
    
    Args:
        query: User's input
        
    Returns:
        True if greeting only, False if greeting + question
    """
    query_lower = query.lower().strip()
    
    # Pure greetings (must be short and match exactly)
    pure_greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening", "hi there", "hello there"]
    
    # Check if it's exactly a pure greeting (with optional punctuation)
    query_clean = query_lower.rstrip('!.,?')
    
    if query_clean in pure_greetings:
        return True
    
    # Check if it's a greeting followed by Alfred/bot name
    if any(greeting in query_clean for greeting in ["hi alfred", "hello alfred", "hey alfred"]):
        return True
    
    # If query is longer than 20 chars, it's probably not just a greeting
    if len(query) > 20:
        return False
    
    # Check for question words - if present, it's not just a greeting
    question_words = ["what", "where", "when", "who", "why", "how", "tell", "show", "can", "does", "is", "which", "did"]
    has_question = any(word in query_lower for word in question_words)
    
    if has_question:
        return False
    
    # Final check: is it a short greeting?
    greetings = ["hi", "hello", "hey"]
    return any(query_clean.startswith(greeting) for greeting in greetings) and len(query) < 15


def get_greeting_response() -> str:
    """Get a random greeting response with Alfred's Batman-themed personality"""
    responses = [
        "Good day! I'm Alfred, Surya's AI butler. 🦇 While he's out there building the digital Gotham, I'm here to answer your questions about his work. How may I assist you?",
        "Ah, welcome! Alfred here - Surya's loyal AI assistant. Think of me as his digital butler, minus the tea service. 🎩 What would you like to know about his tech adventures?",
        "Greetings! I'm Alfred, and I serve Surya in the digital realm. He's quite the Full Stack & GenAI developer - a real hero when it comes to code. What can I tell you about him?",
        "Hello there! Alfred at your service. 🦇 Surya keeps me around to share his professional exploits - the coding kind, not the vigilante kind. Ask away!",
        "Welcome! I'm Alfred, Surya's AI companion. While he's busy being a tech hero by day (and... also by night, coding), I'm here to tell you all about his skills and projects. What would you like to know?"
    ]
    return random.choice(responses)
