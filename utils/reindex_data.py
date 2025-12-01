"""
Script to re-index portfolio data into Pinecone
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search.pinecone_search import PineconeSearch
from data.portfolio_data import get_portfolio_data
from config import logger

def reindex_data():
    print("🔄 Starting re-indexing process...")
    
    # Initialize search
    search = PineconeSearch()
    search.initialize()
    
    if not search.is_initialized:
        print("❌ Failed to initialize Pinecone")
        return
    
    # Delete all existing vectors
    print("🗑️  Deleting existing vectors...")
    if search.delete_all():
        print("✅ Deleted all vectors")
    else:
        print("❌ Failed to delete vectors")
        return
    
    # Get fresh data
    print("📚 Loading portfolio data...")
    data = get_portfolio_data()
    print(f"   Found {len(data)} documents")
    
    # Index new data
    print("🚀 Indexing new data...")
    if search.upsert_documents(data):
        print("✅ Successfully re-indexed data")
    else:
        print("❌ Failed to index data")

if __name__ == "__main__":
    reindex_data()
