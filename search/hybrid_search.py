"""
Hybrid search combining vector and keyword search
Optimized for efficiency
"""

from search.vector_search import VectorSearch
from search.keyword_search import KeywordSearch


class HybridSearch:
    """Combines vector and keyword search for better results"""
    
    def __init__(self):
        """Initialize hybrid search system"""
        self.vector_search = VectorSearch()
        self.keyword_search = None
    
    def initialize(self, portfolio_data=None, faiss_index_path=None, data_path=None):
        """Initialize the search system"""
        if portfolio_data:
            # Create new index from portfolio data
            self.vector_search.create_index(portfolio_data)
            self.keyword_search = KeywordSearch(
                self.vector_search.documents_data,
                self.vector_search.metadatas_data
            )
        elif faiss_index_path and data_path:
            # Load existing index
            if self.vector_search.load_index(faiss_index_path, data_path):
                self.keyword_search = KeywordSearch(
                    self.vector_search.documents_data,
                    self.vector_search.metadatas_data
                )
            else:
                raise ValueError("Failed to load existing index")
        else:
            raise ValueError("Either portfolio_data or index paths must be provided")
    
    def save_index(self, faiss_index_path, data_path):
        """Save the search index"""
        self.vector_search.save_index(faiss_index_path, data_path)
    
    def search(self, query, k=10):
        """Perform hybrid search combining vector and keyword search"""
        # Get vector search results
        vector_results = self.vector_search.search(query, k)
        
        # Get keyword search results
        keyword_results = self.keyword_search.search(query, k)
        
        # Combine and deduplicate
        combined = []
        seen = set()
        
        # Add keyword results first (they're more precise for exact matches)
        for result in keyword_results:
            if result not in seen:
                combined.append(result)
                seen.add(result)
        
        # Add vector results that aren't already included
        for result in vector_results:
            if result not in seen:
                combined.append(result)
                seen.add(result)
        
        # Re-rank results based on query relevance
        return self._rerank_results(query, combined[:k])
    
    def _rerank_results(self, query, results):
        """Re-rank results based on query relevance"""
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        # Keywords that indicate specific types of information
        work_keywords = ['work', 'job', 'company', 'employer', 'role', 'position', 'career']
        project_keywords = ['project', 'work', 'best', 'achievement', 'accomplishment', 'developed', 'built']
        skill_keywords = ['skill', 'technology', 'expertise', 'know', 'experience']
        education_keywords = ['education', 'study', 'degree', 'university', 'college']
        
        # Score results based on query intent
        scored_results = []
        for result in results:
            result_lower = result.lower()
            score = 0
            
            # Check for work-related queries
            if any(word in query_words for word in work_keywords):
                if any(word in result_lower for word in ['acer', 'mindtree', 'tata', 'company', 'employer']):
                    score += 10
            
            # Check for project-related queries
            if any(word in query_words for word in project_keywords):
                if any(word in result_lower for word in ['project', 'developed', 'built', 'created', 'ecommerce', 'spellcheck', 'chat', 'weather']):
                    score += 10
            
            # Check for skill-related queries
            if any(word in query_words for word in skill_keywords):
                if any(word in result_lower for word in ['skill', 'technology', 'react', 'nodejs', 'python', 'javascript']):
                    score += 10
            
            # Check for education-related queries
            if any(word in query_words for word in education_keywords):
                if any(word in result_lower for word in ['university', 'college', 'degree', 'education', 'masters', 'bachelors']):
                    score += 10
            
            # Boost score for exact keyword matches
            for word in query_words:
                if word in result_lower:
                    score += 2
            
            scored_results.append((score, result))
        
        # Sort by score (highest first) and return results
        scored_results.sort(reverse=True, key=lambda x: x[0])
        return [result for score, result in scored_results]