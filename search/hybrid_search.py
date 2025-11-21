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
        """Re-rank results based on query relevance with enhanced scoring"""
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        # Enhanced keyword categories for better intent detection
        work_keywords = ['work', 'job', 'company', 'employer', 'role', 'position', 'career', 'responsibilities', 'duties']
        project_keywords = ['project', 'best', 'achievement', 'accomplishment', 'developed', 'built', 'created', 'portfolio']
        skill_keywords = ['skill', 'technology', 'expertise', 'know', 'experience', 'proficient', 'stack']
        education_keywords = ['education', 'study', 'degree', 'university', 'college', 'masters', 'bachelors', 'coursework']
        certification_keywords = ['certification', 'certified', 'certificate', 'credential', 'aws', 'mta']
        language_keywords = ['language', 'speak', 'communicate', 'multilingual', 'telugu', 'hindi', 'english']
        leadership_keywords = ['leadership', 'lead', 'mentor', 'volunteering', 'community', 'organize', 'team']
        research_keywords = ['thesis', 'research', 'publication', 'paper', 'study', 'analysis']
        personal_keywords = ['hobby', 'hobbies', 'interest', 'personal', 'gaming', 'dota', 'dedication']
        
        # Score results based on query intent and content matching
        scored_results = []
        for result in results:
            result_lower = result.lower()
            score = 0
            
            # Category-based scoring (higher weight for specific matches)
            if any(word in query_words for word in work_keywords):
                if any(word in result_lower for word in ['acer', 'mindtree', 'tata', 'company', 'employer', 'developer', 'engineer']):
                    score += 15
            
            if any(word in query_words for word in project_keywords):
                if any(word in result_lower for word in ['project', 'developed', 'built', 'created', 'ecommerce', 'spellcheck', 'chat', 'weather']):
                    score += 15
            
            if any(word in query_words for word in skill_keywords):
                if any(word in result_lower for word in ['skill', 'technology', 'react', 'nodejs', 'python', 'javascript', 'genai', 'llm']):
                    score += 15
            
            if any(word in query_words for word in education_keywords):
                if any(word in result_lower for word in ['university', 'college', 'degree', 'education', 'masters', 'bachelors', 'csun', 'northridge']):
                    score += 15
            
            # New category scoring
            if any(word in query_words for word in certification_keywords):
                if any(word in result_lower for word in ['certification', 'certified', 'aws', 'mta', 'microsoft', 'credential']):
                    score += 20  # Higher weight for specific matches
            
            if any(word in query_words for word in language_keywords):
                if any(word in result_lower for word in ['language', 'multilingual', 'telugu', 'hindi', 'english', 'communicate']):
                    score += 20
            
            if any(word in query_words for word in leadership_keywords):
                if any(word in result_lower for word in ['leadership', 'lead', 'mentor', 'volunteering', 'community', 'acm', 'organize']):
                    score += 20
            
            if any(word in query_words for word in research_keywords):
                if any(word in result_lower for word in ['thesis', 'research', 'publication', 'sentiment', 'bert', 'roberta', 'nlp']):
                    score += 20
            
            if any(word in query_words for word in personal_keywords):
                if any(word in result_lower for word in ['hobby', 'hobbies', 'interest', 'gaming', 'dota', 'dedication', 'cricket']):
                    score += 15
            
            # Boost for exact multi-word phrase matches (very strong signal)
            if len(query_words) > 1:
                # Check for 2-word and 3-word phrases
                words_list = query_lower.split()
                for i in range(len(words_list) - 1):
                    two_word = f"{words_list[i]} {words_list[i+1]}"
                    if two_word in result_lower:
                        score += 10
                    
                    if i < len(words_list) - 2:
                        three_word = f"{words_list[i]} {words_list[i+1]} {words_list[i+2]}"
                        if three_word in result_lower:
                            score += 15
            
            # Boost for individual keyword matches
            for word in query_words:
                if len(word) > 3:  # Ignore short words like "is", "at", "in"
                    if word in result_lower:
                        score += 3
            
            # Boost for recency (if metadata indicates recent/current)
            if any(word in result_lower for word in ['current', 'present', '2024', '2025']):
                if any(word in query_words for word in ['current', 'now', 'recent', 'latest']):
                    score += 5
            
            scored_results.append((score, result))
        
        # Sort by score (highest first) and return results
        scored_results.sort(reverse=True, key=lambda x: x[0])
        return [result for score, result in scored_results]