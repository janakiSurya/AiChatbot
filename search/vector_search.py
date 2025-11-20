"""
Vector search functionality using FAISS
Optimized for efficiency
"""

import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL, MAX_TOKENS, logger


class VectorSearch:
    """Handles vector-based search using FAISS"""
    
    def __init__(self):
        """Initialize the vector search system"""
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.faiss_index = None
        self.documents_data = []
        self.metadatas_data = []
    
    def load_index(self, faiss_index_path, data_path):
        """Load existing FAISS index and data"""
        try:
            self.faiss_index = faiss.read_index(faiss_index_path)
            
            with open(data_path, 'rb') as f:
                data = pickle.load(f)
                self.documents_data = data['documents']
                self.metadatas_data = data['metadatas']
            
            logger.info(f"✅ Loaded FAISS index with {len(self.documents_data)} documents")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to load FAISS index: {e}")
            return False
    
    def create_index(self, portfolio_data):
        """Create FAISS index from portfolio data"""
        # Create embeddings for all documents
        embeddings = []
        for item in portfolio_data:
            embedding = self.embedding_model.encode(item["text"]).tolist()
            embeddings.append(embedding)
            self.documents_data.append(item["text"])
            self.metadatas_data.append(item["metadata"])
        
        # Create FAISS index
        dimension = len(embeddings[0])
        self.faiss_index = faiss.IndexFlatIP(dimension)
        embeddings_array = np.array(embeddings).astype('float32')
        faiss.normalize_L2(embeddings_array)
        self.faiss_index.add(embeddings_array)
        
        logger.info(f"✅ Created FAISS index with {len(portfolio_data)} documents")
    
    def save_index(self, faiss_index_path, data_path):
        """Save FAISS index and data to files"""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(faiss_index_path), exist_ok=True)
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.faiss_index, faiss_index_path)
        
        # Save documents and metadata
        data = {
            'documents': self.documents_data,
            'metadatas': self.metadatas_data
        }
        with open(data_path, 'wb') as f:
            pickle.dump(data, f)
        
        logger.info(f"✅ Saved FAISS index with {len(self.documents_data)} documents")
    
    def search(self, query, k=10):
        """Perform vector search on the index"""
        if self.faiss_index is None:
            return []
        
        # Encode query
        query_embedding = self.embedding_model.encode(query).astype('float32')
        query_embedding = query_embedding.reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        # Search FAISS index
        scores, indices = self.faiss_index.search(query_embedding, k)
        
        # Get relevant documents
        contexts = []
        for idx in indices[0]:
            if idx < len(self.documents_data):
                context = self.documents_data[idx]
                # Truncate context if too long
                if len(context) > MAX_TOKENS:
                    context = context[:MAX_TOKENS] + "..."
                contexts.append(context)
        
        return contexts