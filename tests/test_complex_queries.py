"""
Test complex queries with Pinecone integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.chat_engine import ChatEngine
from config import logger


def test_complex_queries():
    """Test complex multi-part queries"""
    print("\n" + "="*60)
    print("Testing Complex Queries with Pinecone + Hybrid Search")
    print("="*60)
    
    # Initialize chat engine
    chat_engine = ChatEngine()
    if not chat_engine.initialize():
        print("❌ Failed to initialize chat engine")
        return
    
    print("✅ Chat engine initialized\n")
    
    # Complex test queries
    complex_queries = [
        "What programming languages does Surya know and which companies has he worked for?",
        "Tell me about Surya's education background and his research work",
        "What are Surya's GenAI projects and what technologies did he use?",
        "Describe Surya's leadership experience and certifications",
        "What are his hobbies and how do they relate to his technical skills?"
    ]
    
    for i, query in enumerate(complex_queries, 1):
        print(f"\n{'='*60}")
        print(f"Query {i}: {query}")
        print('='*60)
        
        # Get response (non-streaming for testing)
        response = chat_engine.chat(query)
        print(f"\n📝 Response:\n{response}\n")


if __name__ == "__main__":
    test_complex_queries()
