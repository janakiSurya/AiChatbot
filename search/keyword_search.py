"""
Keyword-based search functionality
Optimized for efficiency
"""

from utils.keyword_extractor import calculate_keyword_score, normalize_query


class KeywordSearch:
    """Handles keyword-based search"""
    
    def __init__(self, documents_data, metadatas_data):
        """Initialize keyword search with documents and metadata"""
        self.documents_data = documents_data
        self.metadatas_data = metadatas_data
    
    def search(self, query, k=5):
        """Perform keyword-based search"""
        query_words = normalize_query(query)
        
        scores = []
        for i, (doc, meta) in enumerate(zip(self.documents_data, self.metadatas_data)):
            # Get keywords from metadata
            meta_keywords = [kw.lower() for kw in meta.get('keywords', [])]
            
            # Calculate keyword match score
            score = calculate_keyword_score(query_words, meta_keywords, doc)
            
            if score > 0:
                scores.append((score, i, doc))
        
        # Sort by score and return top k
        scores.sort(reverse=True, key=lambda x: x[0])
        return [doc for score, idx, doc in scores[:k]]