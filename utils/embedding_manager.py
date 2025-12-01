"""
Singleton Embedding Manager
Ensures only one embedding model instance is loaded across all components
Fixes memory leak where multiple components loaded separate model instances
"""

from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL, logger
import threading


class EmbeddingManager:
    """
    Singleton manager for sentence transformer embedding model.
    Ensures only one model instance exists across the entire application.
    Thread-safe implementation.
    """
    
    _instance = None
    _model = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Ensure only one instance exists (singleton pattern)"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(EmbeddingManager, cls).__new__(cls)
        return cls._instance
    
    def get_model(self):
        """
        Get or create the embedding model instance.
        Lazy-loads on first access.
        
        Returns:
            SentenceTransformer: The shared embedding model
        """
        if self._model is None:
            with self._lock:
                if self._model is None:
                    logger.info("📦 Loading embedding model (singleton)...")
                    self._model = SentenceTransformer(EMBEDDING_MODEL)
                    logger.info(f"✅ Embedding model loaded: {EMBEDDING_MODEL}")
        return self._model
    
    def encode(self, texts, **kwargs):
        """
        Encode text(s) using the shared model.
        
        Args:
            texts: Single text string or list of texts
            **kwargs: Additional arguments to pass to model.encode()
            
        Returns:
            numpy.ndarray: Embeddings
        """
        model = self.get_model()
        return model.encode(texts, **kwargs)
    
    def cleanup(self):
        """Release model resources (for shutdown)"""
        if self._model is not None:
            logger.info("🗑️  Cleaning up embedding model...")
            self._model = None
            logger.info("✅ Embedding model cleaned up")


# Global instance - import this in other modules
embedding_manager = EmbeddingManager()
