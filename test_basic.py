#!/usr/bin/env python3
"""
Basic tests for Boku AI Assistant
Tests that don't require API calls or external dependencies
"""

import pytest
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.query_expander import expand_query, classify_query_intent
from utils.keyword_extractor import extract_keywords, normalize_query
from config import STOP_WORDS, MIN_KEYWORD_LENGTH


class TestQueryExpander:
    """Test query expansion functionality"""
    
    def test_expand_query_basic(self):
        """Test basic query expansion"""
        query = "What are Surya's skills?"
        expanded = expand_query(query)
        assert "skill" in expanded.lower()
        assert len(expanded) > len(query)
    
    def test_expand_query_work(self):
        """Test work-related query expansion"""
        query = "Where does Surya work?"
        expanded = expand_query(query)
        assert "work" in expanded.lower()
        assert "company" in expanded.lower() or "employer" in expanded.lower()
    
    def test_classify_query_intent(self):
        """Test query intent classification"""
        assert classify_query_intent("What is Surya's job?") == "work"
        assert classify_query_intent("What projects has he built?") == "projects"
        assert classify_query_intent("What are his skills?") == "skills"
        assert classify_query_intent("Where did he study?") == "education"
        assert classify_query_intent("How to contact him?") == "contact"
        assert classify_query_intent("Tell me about him") == "general"


class TestKeywordExtractor:
    """Test keyword extraction functionality"""
    
    def test_extract_keywords(self):
        """Test keyword extraction from text"""
        text = "Surya is a software developer with experience in Python and React"
        keywords = extract_keywords(text)
        assert "surya" in keywords
        assert "software" in keywords
        assert "developer" in keywords
        assert "python" in keywords
        assert "react" in keywords
    
    def test_normalize_query(self):
        """Test query normalization"""
        query = "What are Surya's technical skills?"
        normalized = normalize_query(query)
        assert "what" in normalized
        assert "are" in normalized
        assert "surya" in normalized
        assert "technical" in normalized
        assert "skills" in normalized
    
    def test_stop_words_filtering(self):
        """Test that stop words are properly filtered"""
        text = "The quick brown fox jumps over the lazy dog"
        keywords = extract_keywords(text)
        # Stop words should be filtered out
        assert "the" not in keywords
        assert "over" not in keywords
        # Content words should remain
        assert "quick" in keywords
        assert "brown" in keywords
        assert "fox" in keywords


class TestConfiguration:
    """Test configuration settings"""
    
    def test_stop_words_defined(self):
        """Test that stop words are properly defined"""
        assert isinstance(STOP_WORDS, set)
        assert len(STOP_WORDS) > 0
        assert "the" in STOP_WORDS
        assert "and" in STOP_WORDS
        assert "is" in STOP_WORDS
    
    def test_min_keyword_length(self):
        """Test minimum keyword length setting"""
        assert isinstance(MIN_KEYWORD_LENGTH, int)
        assert MIN_KEYWORD_LENGTH > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
