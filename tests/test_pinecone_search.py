"""
Test Pinecone search integration
Run this to verify Pinecone connection and search functionality
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search.pinecone_search import PineconeSearch
from data.portfolio_data import get_portfolio_data
from config import logger


def test_pinecone_connection():
    """Test Pinecone connection"""
    print("\n" + "="*50)
    print("Testing Pinecone Connection")
    print("="*50)
    
    try:
        ps = PineconeSearch()
        portfolio_data = get_portfolio_data()
        
        # Initialize (will create index if needed)
        if ps.initialize(portfolio_data=portfolio_data):
            print("✅ Successfully connected to Pinecone")
            
            # Get stats
            stats = ps.get_stats()
            print(f"📊 Index Stats: {stats}")
            
            return ps
        else:
            print("❌ Failed to connect to Pinecone")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_search(ps):
    """Test search functionality"""
    print("\n" + "="*50)
    print("Testing Search Functionality")
    print("="*50)
    
    test_queries = [
        "What are Surya's skills?",
        "Tell me about his work experience",
        "What projects has he built?",
        "Where did he study?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        results = ps.search(query, k=3)
        
        if results:
            print(f"✅ Found {len(results)} results")
            for i, result in enumerate(results, 1):
                print(f"   {i}. {result[:100]}...")
        else:
            print("❌ No results found")


def main():
    """Main test function"""
    print("\n🚀 Starting Pinecone Integration Tests\n")
    
    # Test connection
    ps = test_pinecone_connection()
    
    if ps:
        # Test search
        test_search(ps)
        
        print("\n" + "="*50)
        print("✅ All tests completed!")
        print("="*50)
    else:
        print("\n❌ Tests failed - check your Pinecone API key in .env")


if __name__ == "__main__":
    main()
