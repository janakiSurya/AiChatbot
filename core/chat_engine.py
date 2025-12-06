"""
Chat engine for Alfred AI Assistant
Orchestrates the conversation flow with session-based caching and greeting detection
"""

from core.knowledge_base import KnowledgeBase
from llm.response_generator import ResponseGenerator
from config import logger, USE_REDIS_CACHE
from utils.query_expander import expand_query, classify_query_intent
from utils.session_manager import session_manager

# Import appropriate cache based on configuration
if USE_REDIS_CACHE:
    from utils.redis_cache import RedisSemanticCache as CacheClass
    from utils.cache import is_greeting_only, get_greeting_response
else:
    from utils.cache import SemanticCache as CacheClass, is_greeting_only, get_greeting_response


class ChatEngine:
    """Main chat engine for Alfred AI Assistant with session-based memory"""
    
    def __init__(self):
        """Initialize the chat engine"""
        self.knowledge_base = KnowledgeBase()
        self.response_generator = ResponseGenerator()
        self.semantic_cache = CacheClass()
        self.is_ready = False
    
    def initialize(self):
        """Initialize the chat engine"""
        if not self.knowledge_base.initialize():
            logger.error("Failed to initialize knowledge base")
            return False
            
        self.is_ready = True
        logger.info("Chat engine initialized successfully")
        return True
    
    def chat(self, message, session_id=None):
        """Process a chat message and generate response"""
        if not self.is_ready:
            return "I'm not ready yet. Please wait for initialization to complete."
        
        # Check for greeting only
        if is_greeting_only(message):
            logger.info("🎯 Greeting detected - returning instant response")
            return get_greeting_response()
        
        # Check semantic cache (global, not session-specific)
        cached_response = self.semantic_cache.get_cached_response(message)
        if cached_response:
            return cached_response
        
        # Get session history for context
        history = session_manager.get_formatted_history(session_id) if session_id else []
        
        # Expand query for better search results using session history
        expanded_query = expand_query(message, history)
        query_intent = classify_query_intent(message)
        
        logger.info(f"Original query: {message}")
        logger.info(f"Expanded query: {expanded_query}")
        logger.info(f"Query intent: {query_intent}")
        logger.info(f"Session history: {len(history)} messages")
        
        # Search for relevant contexts
        contexts = self.knowledge_base.search(expanded_query, k=10)
        
        if not contexts:
            return "I don't have enough information to answer that question about Surya's portfolio. Please try asking about his skills, experience, projects, education, or contact information."
        
        # Generate response using LLM with session history
        try:
            response = self.response_generator.generate_response(message, contexts, history=history)
            
            # Add to global cache for future use
            self.semantic_cache.add_to_cache(message, response)
            
            # Add to session history
            if session_id:
                session_manager.add_message(session_id, "user", message)
                session_manager.add_message(session_id, "assistant", response)
            
            return response
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return self._get_fallback_response(contexts)

    def chat_stream(self, message, session_id=None):
        """Process a chat message and stream response with session memory"""
        if not self.is_ready:
            yield "I'm not ready yet. Please wait for initialization to complete."
            return
        
        # Check for greeting only
        if is_greeting_only(message):
            logger.info("🎯 Greeting detected - returning instant response")
            greeting = get_greeting_response()
            # Store in session even for greetings
            if session_id:
                session_manager.add_message(session_id, "user", message)
                session_manager.add_message(session_id, "assistant", greeting)
            yield greeting
            return
        
        # Check semantic cache (global, not session-specific for efficiency)
        cached_response = self.semantic_cache.get_cached_response(message)
        if cached_response:
            # Store in session history even for cached responses
            if session_id:
                session_manager.add_message(session_id, "user", message)
                session_manager.add_message(session_id, "assistant", cached_response)
            # Stream cached response in chunks
            chunk_size = 20
            for i in range(0, len(cached_response), chunk_size):
                yield cached_response[i:i+chunk_size]
            return
        
        # Get session history for context
        history = session_manager.get_formatted_history(session_id) if session_id else []
        
        # Expand query for better search results using session history
        expanded_query = expand_query(message, history)
        query_intent = classify_query_intent(message)
        
        logger.info(f"Original query: {message}")
        logger.info(f"Expanded query: {expanded_query}")
        logger.info(f"Query intent: {query_intent}")
        logger.info(f"Session: {session_id}, History: {len(history)} messages")
        
        # Search for relevant contexts
        contexts = self.knowledge_base.search(expanded_query, k=10)
        
        if not contexts:
            no_context_response = "I don't have enough information to answer that question about Surya's portfolio. Please try asking about his skills, experience, projects, education, or contact information."
            if session_id:
                session_manager.add_message(session_id, "user", message)
                session_manager.add_message(session_id, "assistant", no_context_response)
            yield no_context_response
            return
        
        # Generate streaming response using LLM with session history
        try:
            full_response = ""
            for chunk in self.response_generator.generate_response_stream(message, contexts, history=history):
                full_response += chunk
                yield chunk
            
            # Add to global cache and session history
            if full_response:
                self.semantic_cache.add_to_cache(message, full_response)
                
                if session_id:
                    session_manager.add_message(session_id, "user", message)
                    session_manager.add_message(session_id, "assistant", full_response)
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            yield self._get_fallback_response(contexts)
    
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
    
    def get_session_stats(self, session_id=None):
        """Get session statistics"""
        if session_id:
            return session_manager.get_session_stats(session_id)
        return {"message": "No session_id provided"}