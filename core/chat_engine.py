"""
Chat engine for Alfred AI Assistant
Orchestrates the conversation flow with caching and greeting detection
"""

from core.knowledge_base import KnowledgeBase
from llm.response_generator import ResponseGenerator
from config import logger
from utils.query_expander import expand_query, classify_query_intent
from utils.cache import SemanticCache, is_greeting_only, get_greeting_response


class ChatEngine:
    """Main chat engine for Alfred AI Assistant"""
    
    def __init__(self):
        """Initialize the chat engine"""
        self.knowledge_base = KnowledgeBase()
        self.response_generator = ResponseGenerator()
        self.semantic_cache = SemanticCache()
        self.history = []  # Store conversation history
        self.max_history = 5  # Keep last 5 turns
        self.is_ready = False
    
    def initialize(self):
        """Initialize the chat engine"""
        if not self.knowledge_base.initialize():
            logger.error("Failed to initialize knowledge base")
            return False
            
        self.is_ready = True
        logger.info("Chat engine initialized successfully")
        return True
    
    def chat(self, message):
        """Process a chat message and generate response"""
        if not self.is_ready:
            return "I'm not ready yet. Please wait for initialization to complete."
        
        # Check for greeting only
        if is_greeting_only(message):
            logger.info("🎯 Greeting detected - returning instant response")
            return get_greeting_response()
        
        # Check semantic cache
        cached_response = self.semantic_cache.get_cached_response(message)
        if cached_response:
            return cached_response
        
        # Expand query for better search results using history
        expanded_query = expand_query(message, self.history)
        query_intent = classify_query_intent(message)
        
        logger.info(f"Original query: {message}")
        logger.info(f"Expanded query: {expanded_query}")
        logger.info(f"Query intent: {query_intent}")
        
        # Search for relevant contexts (optimized k value after re-ranking improvements)
        contexts = self.knowledge_base.search(expanded_query, k=10)
        
        if not contexts:
            return "I don't have enough information to answer that question about Surya's portfolio. Please try asking about his skills, experience, projects, education, or contact information."
        
        # Generate response using LLM with history
        try:
            response = self.response_generator.generate_response(message, contexts, history=self.history)
            
            # Add to dynamic cache for future use
            self.semantic_cache.add_to_dynamic_cache(message, response)
            
            # Update history
            self.history.append({"role": "user", "content": message})
            self.history.append({"role": "assistant", "content": response})
            
            # Trim history if needed
            if len(self.history) > self.max_history * 2:
                self.history = self.history[-self.max_history * 2:]
            
            return response
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return self._get_fallback_response(contexts)
    
    def _get_fallback_response(self, contexts):
        """Generate a fallback response when LLM fails"""
        if contexts:
            return f"Based on the available information: {contexts[0][:200]}..."
        return "I encountered an error processing your request. Please try again."
    
    def get_status(self):
        """Get chat engine status"""
        return {
            "ready": self.is_ready,
            "knowledge_base": self.knowledge_base.get_status()
        }