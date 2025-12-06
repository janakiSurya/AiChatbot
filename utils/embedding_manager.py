"""
Embedding Manager using Pinecone Inference API
Uses Pinecone's hosted embedding model instead of loading locally
Eliminates ~400MB memory requirement for sentence-transformers
"""

from pinecone import Pinecone
from config import PINECONE_API_KEY, logger
import numpy as np
import threading


class EmbeddingManager:
    """
    Manager for embeddings using Pinecone Inference API.
    No local model loading - embeddings generated via API call.
    Thread-safe singleton implementation.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    # Pinecone inference model (1024 dimensions)
    EMBEDDING_MODEL = "multilingual-e5-large"
    EMBEDDING_DIMENSION = 1024
    
    def __new__(cls):
        """Ensure only one instance exists (singleton pattern)"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(EmbeddingManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize Pinecone client for inference"""
        if self._initialized:
            return
            
        self._pc = None
        self._initialized = True
        logger.info("✅ Embedding manager initialized (using Pinecone Inference API)")
    
    @property
    def pc(self):
        """Lazy-load Pinecone client"""
        if self._pc is None:
            self._pc = Pinecone(api_key=PINECONE_API_KEY)
            logger.info("✅ Pinecone client connected for inference")
        return self._pc
    
    @property
    def dimension(self):
        """Return embedding dimension for index configuration"""
        return self.EMBEDDING_DIMENSION
    
    def encode(self, texts, **kwargs):
        """
        Generate embeddings using Pinecone Inference API.
        
        Args:
            texts: Single text string or list of texts
            **kwargs: Additional arguments (input_type: 'query' or 'passage')
            
        Returns:
            numpy.ndarray: Embeddings with shape (n_texts, 1024)
        """
        # Ensure texts is a list
        if isinstance(texts, str):
            texts = [texts]
        
        # Determine input type (query for search, passage for indexing)
        input_type = kwargs.get('input_type', 'query')
        
        try:
            # Call Pinecone Inference API
            response = self.pc.inference.embed(
                model=self.EMBEDDING_MODEL,
                inputs=texts,
                parameters={"input_type": input_type}
            )
            
            # Extract embeddings from response
            embeddings = [item.values for item in response.data]
            
            return np.array(embeddings)
            
        except Exception as e:
            logger.error(f"❌ Embedding generation failed: {e}")
            raise
    
    def cleanup(self):
        """Release resources (for shutdown)"""
        logger.info("✅ Embedding manager cleanup complete")
        self._pc = None


# Global instance - import this in other modules
embedding_manager = EmbeddingManager()
