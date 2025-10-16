"""
Configuration settings for Boku AI Assistant
Environment-aware configuration for Git deployment
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# File paths
FAISS_INDEX_PATH = "./data/faiss_index.bin"
FAISS_DATA_PATH = "./data/faiss_data.pkl"

# Model configuration
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
HF_MODEL_NAME = os.getenv("HF_MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.2")
HF_API_KEY = os.getenv("HF_API_KEY", "")

# Search configuration
DEFAULT_SEARCH_RESULTS = int(os.getenv("DEFAULT_SEARCH_RESULTS", "10"))
MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", "200"))
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "384"))

# Server configuration
SERVER_PORT = int(os.getenv("SERVER_PORT", "7871"))
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")

# Response configuration
MIN_RESPONSE_LENGTH = int(os.getenv("MIN_RESPONSE_LENGTH", "20"))
MAX_RESPONSE_TOKENS = int(os.getenv("MAX_RESPONSE_TOKENS", "300"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Keywords configuration
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
    'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did',
    'will', 'would', 'could', 'should', 'may', 'might', 'can', 'i', 'my', 'me', 'we', 'our',
    'us', 'you', 'your', 'he', 'his', 'him', 'she', 'her', 'it', 'its', 'they', 'their', 'them'
}

MIN_KEYWORD_LENGTH = int(os.getenv("MIN_KEYWORD_LENGTH", "2"))
MAX_KEYWORDS_PER_DOCUMENT = int(os.getenv("MAX_KEYWORDS_PER_DOCUMENT", "10"))