#!/usr/bin/env python3
"""
Re-index script for Pinecone with new embedding model.
Run this ONCE before deploying to Koyeb to create embeddings with multilingual-e5-large (1024 dimensions).

Usage:
    python scripts/reindex_pinecone.py
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from pinecone import Pinecone, ServerlessSpec
from config import (
    PINECONE_API_KEY,
    PINECONE_ENVIRONMENT,
    logger
)
from data.portfolio_data import get_portfolio_data
from utils.embedding_manager import embedding_manager


# New index name for v2 embeddings
NEW_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "portfolio-assistant-v2")


def main():
    portfolio_data = get_portfolio_data()
    
    print("=" * 60)
    print("Pinecone Re-indexing Script")
    print("=" * 60)
    print(f"\nThis will create/update index: {NEW_INDEX_NAME}")
    print(f"Using embedding model: {embedding_manager.EMBEDDING_MODEL}")
    print(f"Embedding dimension: {embedding_manager.dimension}")
    print(f"Documents to index: {len(portfolio_data)}")
    print()
    
    # Confirm
    confirm = input("Continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Aborted.")
        return
    
    # Initialize Pinecone
    print("\n1. Connecting to Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Check if index exists
    existing_indexes = pc.list_indexes().names()
    
    if NEW_INDEX_NAME in existing_indexes:
        print(f"   Index '{NEW_INDEX_NAME}' already exists.")
        delete_confirm = input("   Delete and recreate? (y/n): ")
        if delete_confirm.lower() == 'y':
            print(f"   Deleting index '{NEW_INDEX_NAME}'...")
            pc.delete_index(NEW_INDEX_NAME)
            import time
            time.sleep(5)
        else:
            print("   Using existing index (will upsert/update vectors)")
    
    # Create index if it doesn't exist
    if NEW_INDEX_NAME not in pc.list_indexes().names():
        print(f"\n2. Creating index '{NEW_INDEX_NAME}' (dimension={embedding_manager.dimension})...")
        pc.create_index(
            name=NEW_INDEX_NAME,
            dimension=embedding_manager.dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=PINECONE_ENVIRONMENT
            )
        )
        import time
        print("   Waiting for index to be ready...")
        time.sleep(10)
    
    # Connect to index
    print("\n3. Connecting to index...")
    index = pc.Index(NEW_INDEX_NAME)
    
    # Generate embeddings
    print("\n4. Generating embeddings with Pinecone Inference API...")
    texts = [item["text"] for item in portfolio_data]
    embeddings = embedding_manager.encode(texts, input_type="passage")
    print(f"   Generated {len(embeddings)} embeddings")
    
    # Prepare vectors
    print("\n5. Preparing vectors for upsert...")
    import json
    vectors = []
    
    for idx, (item, embedding) in enumerate(zip(portfolio_data, embeddings)):
        # Clean metadata
        clean_metadata = {}
        for key, value in item["metadata"].items():
            if isinstance(value, (dict, list)):
                clean_metadata[key] = json.dumps(value)
            elif isinstance(value, (str, int, float, bool)):
                clean_metadata[key] = value
            else:
                clean_metadata[key] = str(value)
        
        clean_metadata["text"] = item["text"][:1000]
        
        vectors.append({
            "id": f"doc_{idx}",
            "values": embedding.tolist(),
            "metadata": clean_metadata
        })
    
    # Upsert vectors
    print("\n6. Upserting vectors to Pinecone...")
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)
        print(f"   Upserted batch {i//batch_size + 1}/{(len(vectors) + batch_size - 1)//batch_size}")
    
    # Verify
    print("\n7. Verifying...")
    import time
    time.sleep(2)
    stats = index.describe_index_stats()
    print(f"   Index stats: {stats}")
    
    print("\n" + "=" * 60)
    print("✅ Re-indexing complete!")
    print("=" * 60)
    print(f"\nNext steps:")
    print(f"1. Update your .env or Koyeb environment variables:")
    print(f"   PINECONE_INDEX_NAME={NEW_INDEX_NAME}")
    print(f"2. Deploy to Koyeb following KOYEB_DEPLOYMENT.md")


if __name__ == "__main__":
    main()
