"""
Pinecone-based vector search
Cloud-hosted vector database for persistent storage across deployments
Uses Pinecone Inference API for embeddings (no local model required)
"""

from pinecone import Pinecone, ServerlessSpec
from utils.embedding_manager import embedding_manager
from config import (
    PINECONE_API_KEY,
    PINECONE_ENVIRONMENT,
    PINECONE_INDEX_NAME,
    MAX_TOKENS,
    logger
)
import time


class PineconeSearch:
    """Handles vector-based search using Pinecone cloud database"""
    
    def __init__(self):
        """
        Initialize the Pinecone search system.
        Uses Pinecone Inference API for embeddings - no local model needed.
        """
        self.pc = None
        self.index = None
        self.is_initialized = False
        # Use dimension from embedding manager (1024 for multilingual-e5-large)
        self.dimension = embedding_manager.dimension
    
    def initialize(self, portfolio_data=None):
        """
        Initialize Pinecone connection and index
        
        Args:
            portfolio_data: Optional list of documents to index (only needed if index is empty)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Initialize Pinecone client
            self.pc = Pinecone(api_key=PINECONE_API_KEY)
            
            # Check if index exists
            existing_indexes = self.pc.list_indexes().names()
            
            if PINECONE_INDEX_NAME not in existing_indexes:
                logger.info(f"Creating new Pinecone index: {PINECONE_INDEX_NAME}")
                
                # Create serverless index with correct dimension for Pinecone Inference
                self.pc.create_index(
                    name=PINECONE_INDEX_NAME,
                    dimension=self.dimension,  # 1024 for multilingual-e5-large
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=PINECONE_ENVIRONMENT
                    )
                )
                
                # Wait for index to be ready
                logger.info("Waiting for index to be ready...")
                time.sleep(5)  # Give it a moment to initialize
                
                logger.info(f"✅ Created Pinecone index: {PINECONE_INDEX_NAME} (dim={self.dimension})")
            else:
                logger.info(f"✅ Connected to existing Pinecone index: {PINECONE_INDEX_NAME}")
            
            # Connect to index
            self.index = self.pc.Index(PINECONE_INDEX_NAME)
            
            # Check if we need to index data
            stats = self.index.describe_index_stats()
            vector_count = stats.get('total_vector_count', 0)
            
            if vector_count == 0 and portfolio_data:
                logger.info("Index is empty, indexing portfolio data...")
                self.upsert_documents(portfolio_data)
            elif vector_count > 0:
                logger.info(f"✅ Index loaded with {vector_count} vectors")
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Pinecone: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def upsert_documents(self, portfolio_data):
        """
        Index portfolio documents into Pinecone
        
        Args:
            portfolio_data: List of dicts with 'text' and 'metadata' keys
        """
        if not self.index:
            logger.error("Index not initialized")
            return False
        
        try:
            import json
            
            # Prepare vectors for upsert
            vectors = []
            batch_size = 100
            
            # Get all texts for batch embedding
            texts = [item["text"] for item in portfolio_data]
            
            # Generate embeddings in batch using Pinecone Inference API
            logger.info(f"Generating embeddings for {len(texts)} documents...")
            embeddings = embedding_manager.encode(texts, input_type="passage")
            
            for idx, (item, embedding) in enumerate(zip(portfolio_data, embeddings)):
                # Prepare metadata - Pinecone only accepts simple types
                clean_metadata = {}
                for key, value in item["metadata"].items():
                    if isinstance(value, (dict, list)):
                        clean_metadata[key] = json.dumps(value)
                    elif isinstance(value, (str, int, float, bool)):
                        clean_metadata[key] = value
                    else:
                        clean_metadata[key] = str(value)
                
                # Add text to metadata (truncated)
                clean_metadata["text"] = item["text"][:1000]
                
                # Create vector with metadata
                vector = {
                    "id": f"doc_{idx}",
                    "values": embedding.tolist(),
                    "metadata": clean_metadata
                }
                vectors.append(vector)
                
                # Upsert in batches
                if len(vectors) >= batch_size:
                    self.index.upsert(vectors=vectors)
                    logger.info(f"Upserted batch of {len(vectors)} vectors")
                    vectors = []
            
            # Upsert remaining vectors
            if vectors:
                self.index.upsert(vectors=vectors)
                logger.info(f"Upserted final batch of {len(vectors)} vectors")
            
            logger.info(f"✅ Indexed {len(portfolio_data)} documents to Pinecone")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to upsert documents: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def search(self, query, k=10):
        """
        Perform vector search on Pinecone index
        
        Args:
            query: Search query string
            k: Number of results to return
        
        Returns:
            List of context strings
        """
        if not self.is_initialized or not self.index:
            logger.warning("Pinecone not initialized")
            return []
        
        try:
            # Encode query using Pinecone Inference API
            query_embedding = embedding_manager.encode(query, input_type="query")[0].tolist()
            
            # Search Pinecone index
            results = self.index.query(
                vector=query_embedding,
                top_k=k,
                include_metadata=True
            )
            
            # Extract contexts from results
            contexts = []
            for match in results['matches']:
                if 'metadata' in match and 'text' in match['metadata']:
                    context = match['metadata']['text']
                    
                    # Truncate if too long
                    if len(context) > MAX_TOKENS:
                        context = context[:MAX_TOKENS] + "..."
                    
                    contexts.append(context)
            
            logger.info(f"Found {len(contexts)} results for query")
            return contexts
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    def delete_all(self):
        """Delete all vectors from the index (useful for re-indexing)"""
        if not self.index:
            logger.error("Index not initialized")
            return False
        
        try:
            self.index.delete(delete_all=True)
            logger.info("✅ Deleted all vectors from index")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to delete vectors: {e}")
            return False
    
    def get_stats(self):
        """Get index statistics"""
        if not self.index:
            return {}
        
        try:
            return self.index.describe_index_stats()
        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            return {}
