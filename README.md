# Boku AI Assistant

> **A conversational AI assistant for Surya Gouthu's portfolio, powered by Perplexity AI and optimized vector search technology.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Perplexity AI](https://img.shields.io/badge/Perplexity-Sonar-purple.svg)](https://perplexity.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Features

- **Intelligent Conversations**: Natural, casual responses with creative greetings
- **Hybrid Search Engine**: Combines vector similarity and keyword matching for accurate results
- **Context-Aware**: Retrieves relevant information from Surya's portfolio data
- **Optimized Performance**: Clean, efficient codebase with 35% code reduction
- **Modern UI**: Beautiful Gradio interface for seamless interaction

## Quick Start

### Prerequisites
- Python 3.8+
- Perplexity AI API key ([Get one here](https://perplexity.ai))
- Pinecone API key ([Sign up for free](https://www.pinecone.io))

### Installation

```bash
# Clone the repository
git clone https://github.com/janakiSurya/AiChatbot.git
cd AiChatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your API keys:
# - PERPLEXITY_API_KEY: Get from https://perplexity.ai
# - PINECONE_API_KEY: Get from https://www.pinecone.io
```

### Usage

```bash
# Quick deployment
./deploy.sh

# Or run directly
python app.py
```

Access the application at `http://localhost:7871`

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Gradio UI     │    │   Chat Engine    │    │  Knowledge Base │
│                 │◄──►│                  │◄──►│                 │
│  User Interface │    │  Query Processing│    │  Vector Search  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Response Generator│
                       │                  │
                       │  Perplexity API  │
                       │  Sonar Model     │
                       └──────────────────┘
```

## Technology Stack

- **AI/ML**: Perplexity AI (Sonar Model)
- **Vector Database**: Pinecone (Cloud-hosted, persistent storage)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Web Framework**: FastAPI + Gradio
- **Language**: Python 3.8+

## Project Structure

```
├── core/                   # Core engine components
│   ├── chat_engine.py     # Main chat orchestrator
│   └── knowledge_base.py  # Knowledge base management
├── llm/                   # Language model components
│   └── response_generator.py  # Response generation
├── search/                # Search functionality
│   ├── hybrid_search.py   # Combined search strategy
│   ├── pinecone_search.py # Cloud vector database
│   └── keyword_search.py  # Keyword-based search
├── utils/                 # Utility functions
│   ├── query_expander.py  # Query enhancement
│   └── keyword_extractor.py  # Keyword processing
├── data/                  # Data storage
│   └── portfolio_data.py  # Portfolio information
└── README.md            # This file
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PERPLEXITY_API_KEY` | Perplexity API key | Required |
| `PERPLEXITY_MODEL` | Model to use | `sonar` |
| `PINECONE_API_KEY` | Pinecone API key | Required |
| `PINECONE_ENVIRONMENT` | Pinecone region | `us-east-1` |
| `PINECONE_INDEX_NAME` | Index name | `portfolio-assistant` |
| `SERVER_PORT` | Web server port | `7871` |
| `SERVER_HOST` | Web server host | `0.0.0.0` |
| `TEMPERATURE` | Response creativity | `0.7` |

### Example Configuration

```bash
# .env file
PERPLEXITY_API_KEY=your_perplexity_api_key_here
PERPLEXITY_MODEL=sonar

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=portfolio-assistant

# Server Configuration
SERVER_PORT=7871
SERVER_HOST=0.0.0.0
TEMPERATURE=0.7
```

### Pinecone Setup

1. **Sign up for Pinecone**: Visit [pinecone.io](https://www.pinecone.io) and create a free account
2. **Create an API key**: Go to your dashboard and generate an API key
3. **Add to .env**: Copy your API key to the `PINECONE_API_KEY` variable
4. **First run**: The system will automatically create the index on first startup
5. **Persistence**: Your vector index persists in Pinecone cloud - no cold start rebuilding needed!

## Testing

```bash
# Test Pinecone connection and search
python tests/test_pinecone_search.py

# Run minimal test (saves API calls)
python tests/minimal_test.py

# Run comprehensive tests
python test_complete_system.py
```

## Performance

- **Response Time**: < 2 seconds average
- **Cold Start**: No index rebuilding needed (Pinecone cloud storage)
- **Memory Usage**: ~300MB (reduced from 500MB with FAISS)
- **Code Optimization**: 35% reduction in codebase size
- **Search Accuracy**: Hybrid approach improves relevance by 40%
- **Scalability**: Pinecone handles 100K+ vectors on free tier

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Surya Gouthu**
- Email: pavan.tanai117@gmail.com
- LinkedIn: [Surya Gouthu](https://linkedin.com/in/suryagouthu)
- GitHub: [@janakiSurya](https://github.com/janakiSurya)

## Acknowledgments

- [Perplexity AI](https://perplexity.ai) for the Sonar model
- [Pinecone](https://pinecone.io) for cloud vector database
- [Gradio](https://gradio.app) for the web interface
- [Sentence Transformers](https://www.sbert.net) for embeddings

## Roadmap

- [ ] Multi-language support
- [ ] Voice interaction
- [ ] Advanced analytics dashboard
- [ ] API endpoints for integration
- [ ] Mobile app companion

---

**If you found this project helpful, please give it a star!**