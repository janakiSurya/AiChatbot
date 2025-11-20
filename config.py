"""
Configuration settings for Boku AI Assistant
Environment-aware configuration for Git deployment
"""

import os
import logging
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Logging
def setup_logger(name="boku_ai"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        
        # File Handler
        file_handler = logging.FileHandler("boku.log")
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    return logger

logger = setup_logger()

def validate_config():
    """Validate that all required configuration is present"""
    required_vars = ["PERPLEXITY_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        logger.error(f"Missing required environment variables: {', '.join(missing)}")
        return False
    return True

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "faiss_index.bin")
FAISS_DATA_PATH = os.path.join(BASE_DIR, "faiss_data.pkl")

# Models
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
PERPLEXITY_MODEL = os.getenv("PERPLEXITY_MODEL", "sonar")

# API Keys
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Server Settings
SERVER_PORT = int(os.getenv("SERVER_PORT", 7871))
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")

# Search Parameters
SEARCH_TOP_K = 3
SEARCH_SCORE_THRESHOLD = 0.5

# Generation Parameters
MAX_TOKENS = 500
MAX_RESPONSE_TOKENS = 500
MIN_RESPONSE_LENGTH = 20
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))

# System Prompts
SYSTEM_PROMPT = """You are Boku, an AI assistant for Surya Gouthu's portfolio.
Your goal is to answer questions about Surya's skills, experience, and projects based ONLY on the provided context.

CRITICAL INSTRUCTIONS:
1. ALWAYS refer to Surya in the THIRD PERSON (e.g., "Surya is...", "He has...", "His skills..."). NEVER use "I", "me", or "my" to refer to Surya.
2. If the context contains first-person text (like "I built this"), YOU MUST rephrase it to third-person ("Surya built this").
3. Be friendly, professional, and concise.
4. Do not mention "context" or "search results" in your answer. Just answer the question naturally.
5. If the answer is not in the context, politely say you don't have that information.
6. Keep answers under 4 sentences unless the user asks for a list.
"""

# Keywords configuration
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
    'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did',
    'will', 'would', 'could', 'should', 'may', 'might', 'can', 'i', 'my', 'me', 'we', 'our',
    'us', 'you', 'your', 'he', 'his', 'him', 'she', 'her', 'it', 'its', 'they', 'their', 'them'
}

MIN_KEYWORD_LENGTH = int(os.getenv("MIN_KEYWORD_LENGTH", "2"))
MAX_KEYWORDS_PER_DOCUMENT = int(os.getenv("MAX_KEYWORDS_PER_DOCUMENT", "10"))