"""
Knowledge base management for Boku AI Assistant
Optimized with Pinecone cloud storage
"""

import os
from data.portfolio_data import get_portfolio_data
from search.hybrid_search import HybridSearch
from config import logger


class KnowledgeBase:
    """Manages the knowledge base for the AI assistant"""
    
    def __init__(self):
        """Initialize the knowledge base"""
        self.search_engine = HybridSearch()
        self.is_initialized = False
    
    def initialize(self):
        """Initialize the knowledge base with Pinecone"""
        try:
            # Get portfolio data (will be indexed if Pinecone is empty)
            portfolio_data = get_portfolio_data()
            
            # Initialize search engine with Pinecone
            # Pinecone handles persistence, so we just pass the data
            # It will only index if the Pinecone index is empty
            self.search_engine.initialize(portfolio_data=portfolio_data)
            
            logger.info("✅ Knowledge base initialized with Pinecone")
            self.is_initialized = True
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize knowledge base: {e}")
            return False
    
    def search(self, query, k=10):
        """Search the knowledge base"""
        if not self.is_initialized:
            return []
        
        return self.search_engine.search(query, k)
    
    def get_status(self):
        """Get knowledge base status"""
        if not self.is_initialized:
            return {"status": "not_initialized"}
        
        # Get Pinecone stats
        stats = self.search_engine.vector_search.get_stats()
        
        return {
            "status": "initialized",
            "vector_count": stats.get('total_vector_count', 0),
            "index_name": stats.get('index_fullness', 'N/A')
        }