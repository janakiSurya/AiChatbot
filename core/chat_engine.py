"""
Main chat engine that orchestrates search and response generation
Optimized for efficiency and clean code
"""

from core.knowledge_base import KnowledgeBase
from llm.response_generator import ResponseGenerator
from utils.query_expander import expand_query, classify_query_intent


class ChatEngine:
    """Main chat engine for Boku AI Assistant"""
    
    def __init__(self):
        """Initialize the chat engine"""
        self.knowledge_base = KnowledgeBase()
        self.response_generator = ResponseGenerator()
        self.is_ready = False
    
    def initialize(self):
        """Initialize the chat engine"""
        if self.knowledge_base.initialize():
            self.is_ready = True
            print("✅ Chat engine initialized successfully")
            return True
        else:
            print("❌ Failed to initialize chat engine")
            return False
    
    def chat(self, message):
        """Process a chat message and generate response"""
        if not self.is_ready:
            return "I'm not ready yet. Please wait for initialization to complete."
        
        # Expand query for better search results
        expanded_query = expand_query(message)
        query_intent = classify_query_intent(message)
        
        print(f"Original query: {message}")
        print(f"Expanded query: {expanded_query}")
        print(f"Query intent: {query_intent}")
        
        # Search for relevant contexts
        contexts = self.knowledge_base.search(expanded_query)
        
        if not contexts:
            return "I don't have enough information to answer that question about Surya's portfolio. Please try asking about his skills, experience, projects, education, or contact information."
        
        # Generate response using LLM
        try:
            response = self.response_generator.generate_response(message, contexts)
            return response
        except Exception as e:
            print(f"Response generation failed: {e}")
            return self._get_fallback_response(contexts)
    
    def _get_fallback_response(self, contexts):
        """Get fallback response when LLM generation fails"""
        if contexts:
            best_context = contexts[0]
            # Simple first person to third person conversion
            converted = best_context.replace("I am ", "Surya is ")
            converted = converted.replace("I have ", "He has ")
            converted = converted.replace("I work ", "He works ")
            converted = converted.replace("My ", "Surya's ")
            converted = converted.replace("I'm ", "He's ")
            return converted
        else:
            return "I'm having trouble generating a response right now."
    
    def get_status(self):
        """Get chat engine status"""
        return {
            "ready": self.is_ready,
            "knowledge_base": self.knowledge_base.get_status()
        }