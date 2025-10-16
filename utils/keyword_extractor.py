"""
Keyword extraction utilities for better search functionality
Optimized and streamlined
"""

import re
from collections import Counter
from config import STOP_WORDS, MIN_KEYWORD_LENGTH, MAX_KEYWORDS_PER_DOCUMENT


def extract_keywords(text):
    """Extract meaningful keywords from text"""
    # Extract words (alphanumeric)
    words = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
    
    # Filter out stop words and short words
    keywords = [
        word for word in words 
        if word not in STOP_WORDS and len(word) > MIN_KEYWORD_LENGTH
    ]
    
    # Get most common keywords
    keyword_counts = Counter(keywords)
    return [
        word for word, count in keyword_counts.most_common(MAX_KEYWORDS_PER_DOCUMENT)
    ]


def calculate_keyword_score(query_words, document_keywords, document_text):
    """Calculate keyword match score between query and document"""
    # Extract words from document text
    doc_words = set(re.findall(r'\b[a-zA-Z0-9]+\b', document_text.lower()))
    
    # Calculate keyword matches (weighted higher)
    keyword_matches = len(query_words.intersection(set(document_keywords)))
    
    # Calculate general word matches
    word_matches = len(query_words.intersection(doc_words))
    
    # Weighted score: keywords are more important than general words
    return keyword_matches * 2 + word_matches * 1


def normalize_query(query):
    """Normalize query for better matching"""
    query_lower = query.lower()
    return set(re.findall(r'\b[a-zA-Z0-9]+\b', query_lower))