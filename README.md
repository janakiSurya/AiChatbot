# Boku AI Assistant

A conversational AI assistant for Surya Gouthu's portfolio, built with HuggingFace Mistral-7B and optimized vector search.

## Features

- 🤖 **Natural Conversations**: Creative greetings and casual responses
- 🔍 **Hybrid Search**: Combines vector and keyword search for accurate results
- 🧠 **Smart Context**: Retrieves relevant information from portfolio data
- ⚡ **Optimized Performance**: Clean, efficient codebase
- 🎯 **Third-Person Responses**: Always refers to Surya in third person

## Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-assistant
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
# Copy the example environment file
cp env.example .env

# Edit .env file with your HuggingFace API key
HF_API_KEY=your_huggingface_api_key_here
```

### 4. Run the System
```bash
# Test the complete system
python test_complete_system.py

# Or run the main application
python app.py
```

## Configuration

The system uses environment variables for configuration. Key settings:

- `HF_API_KEY`: Your HuggingFace API key (required)
- `HF_MODEL_NAME`: Model to use (default: mistralai/Mistral-7B-Instruct-v0.2)
- `SERVER_PORT`: Port for the web interface (default: 7871)
- `TEMPERATURE`: Response creativity (default: 0.7)

## Project Structure

```
├── core/                   # Core engine components
│   ├── chat_engine.py     # Main chat orchestrator
│   └── knowledge_base.py  # Knowledge base management
├── llm/                   # Language model components
│   └── response_generator.py  # Response generation
├── search/                # Search functionality
│   ├── hybrid_search.py   # Combined search strategy
│   ├── vector_search.py   # Vector-based search
│   └── keyword_search.py  # Keyword-based search
├── utils/                 # Utility functions
│   ├── query_expander.py  # Query enhancement
│   └── keyword_extractor.py  # Keyword processing
├── data/                  # Data storage
│   ├── portfolio_data.py  # Portfolio information
│   ├── faiss_index.bin    # Vector index (generated)
│   └── faiss_data.pkl     # Data cache (generated)
├── config.py              # Configuration settings
├── app.py                 # Main application
└── test_complete_system.py # System tests
```

## API Usage

### HuggingFace API
The system uses HuggingFace's Inference API with Mistral-7B-Instruct-v0.2 for response generation.

### Vector Search
Uses FAISS for efficient vector similarity search with sentence-transformers embeddings.

## Development

### Running Tests
```bash
python test_complete_system.py
```

### Code Quality
```bash
# Format code
black .

# Lint code
flake8 .
```

## Deployment

### Environment Variables
Ensure all required environment variables are set:
- `HF_API_KEY`: HuggingFace API key
- `SERVER_PORT`: Port for web interface
- `SERVER_HOST`: Host binding

### Data Files
The system will automatically generate:
- `data/faiss_index.bin`: Vector search index
- `data/faiss_data.pkl`: Cached data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is for Surya Gouthu's portfolio demonstration.

## Support

For questions or issues, please contact Surya Gouthu.