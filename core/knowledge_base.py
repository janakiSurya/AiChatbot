"""
Knowledge base management for Boku AI Assistant
Optimized for efficiency
"""

import os
from data.portfolio_data import get_portfolio_data
from search.hybrid_search import HybridSearch
from config import FAISS_INDEX_PATH, FAISS_DATA_PATH, logger


class KnowledgeBase:
    """Manages the knowledge base for the AI assistant"""
    
    def __init__(self):
        """Initialize the knowledge base"""
        self.search_engine = HybridSearch()
        self.is_initialized = False
    
    def initialize(self):
        """Initialize the knowledge base"""
        try:
            # Check if index files exist
            if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(FAISS_DATA_PATH):
                # Load existing index
                self.search_engine.initialize(
                    faiss_index_path=FAISS_INDEX_PATH,
                    data_path=FAISS_DATA_PATH
                )
                logger.info("✅ Loaded existing knowledge base")
            else:
                # Create new index from portfolio data
                portfolio_data = get_portfolio_data()
                self.search_engine.initialize(portfolio_data=portfolio_data)
                self.search_engine.save_index(FAISS_INDEX_PATH, FAISS_DATA_PATH)
                logger.info("✅ Created new knowledge base")
            
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
        
        return {
            "status": "initialized",
            "documents_count": len(self.search_engine.vector_search.documents_data),
            "index_type": type(self.search_engine.vector_search.faiss_index).__name__
        }