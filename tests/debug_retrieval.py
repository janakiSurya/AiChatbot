import sys
import os
import logging

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(level=logging.INFO)

from core.knowledge_base import KnowledgeBase

def debug_retrieval():
    print("🚀 Starting Retrieval Debugger...")
    
    kb = KnowledgeBase()
    if not kb.initialize():
        print("❌ Failed to initialize KnowledgeBase")
        return

    query = "Is he eligible to work with international teams, and can he communicate in multiple languages?"
    print(f"\n🔍 Query: '{query}'")
    
    # Access vector search component
    vs = kb.search_engine.vector_search
    
    # Encode query manually to get indices
    query_embedding = vs.embedding_model.encode(query).astype('float32')
    query_embedding = query_embedding.reshape(1, -1)
    import faiss
    faiss.normalize_L2(query_embedding)
    
    # Search FAISS index
    scores, indices = vs.faiss_index.search(query_embedding, k=5)
    
    print(f"\n📊 Found {len(indices[0])} results:")
    for i, idx in enumerate(indices[0]):
        score = scores[0][i]
        if idx < len(vs.documents_data):
            text = vs.documents_data[idx]
            metadata = vs.metadatas_data[idx]
            print(f"\n--- Result {i+1} (Score: {score:.4f}) ---")
            print(f"ID: {metadata.get('id', 'N/A')}")
            print(f"Text: {text[:200]}...")
            print(f"Keywords: {metadata.get('keywords', [])}")

if __name__ == "__main__":
    debug_retrieval()
