# Deployment Guide for Boku AI Assistant

## 🚀 Quick Deployment

### Option 1: Local Development
```bash
# 1. Clone and setup
git clone <repository-url>
cd ai-assistant

# 2. Run deployment script
./deploy.sh
```

### Option 2: Docker Deployment
```bash
# 1. Build and run with Docker Compose
docker-compose up --build

# 2. Or build manually
docker build -t boku-ai-assistant .
docker run -p 7871:7871 -e HF_API_KEY=your_key_here boku-ai-assistant
```

### Option 3: Manual Setup
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp env.example .env
# Edit .env with your HF_API_KEY

# 4. Run application
python app.py
```

## 🔧 Environment Configuration

### Required Environment Variables
```bash
# .env file
HF_API_KEY=your_huggingface_api_key_here
HF_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
SERVER_PORT=7871
SERVER_HOST=0.0.0.0
```

### Optional Environment Variables
```bash
DEFAULT_SEARCH_RESULTS=10
MAX_CONTEXT_LENGTH=200
MIN_RESPONSE_LENGTH=20
MAX_RESPONSE_TOKENS=300
TEMPERATURE=0.7
```

## 🌐 Production Deployment

### Using Docker
1. **Build the image:**
   ```bash
   docker build -t boku-ai-assistant:latest .
   ```

2. **Run with environment variables:**
   ```bash
   docker run -d \
     --name boku-ai \
     -p 7871:7871 \
     -e HF_API_KEY=your_key_here \
     -v $(pwd)/data:/app/data \
     boku-ai-assistant:latest
   ```

### Using Docker Compose
```bash
# Set environment variables
export HF_API_KEY=your_key_here

# Deploy
docker-compose up -d
```

### Cloud Deployment (Heroku, Railway, etc.)
1. **Set environment variables in your platform:**
   - `HF_API_KEY`: Your HuggingFace API key
   - `SERVER_PORT`: 7871 (or platform's assigned port)
   - `SERVER_HOST`: 0.0.0.0

2. **Deploy using Dockerfile or buildpack**

## 🔍 Health Checks

The application includes health check endpoints:
- **Docker health check**: Built into Dockerfile
- **Application health**: Available at `/health` (if implemented)

## 📊 Monitoring

### Logs
- Application logs are output to stdout
- Docker logs: `docker logs boku-ai`
- Docker Compose logs: `docker-compose logs -f`

### Performance
- Monitor response times in the application
- Check HuggingFace API usage and limits
- Monitor memory usage for vector search

## 🔐 Security Considerations

1. **API Keys**: Never commit API keys to Git
2. **Environment Variables**: Use `.env` files for local development
3. **Secrets Management**: Use platform-specific secret management for production
4. **Network**: Consider firewall rules for production deployments

## 🚨 Troubleshooting

### Common Issues

1. **API Key Not Found**
   ```
   Error: HF_API_KEY not found
   Solution: Set HF_API_KEY in .env file
   ```

2. **Port Already in Use**
   ```
   Error: Port 7871 already in use
   Solution: Change SERVER_PORT in .env or kill existing process
   ```

3. **Model Loading Issues**
   ```
   Error: Model is loading...
   Solution: Wait for first request to complete (normal behavior)
   ```

4. **Memory Issues**
   ```
   Error: Out of memory
   Solution: Increase Docker memory limits or use smaller models
   ```

### Debug Mode
```bash
# Run with debug output
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from app import main
main()
"
```

## 📈 Scaling

### Horizontal Scaling
- Use load balancer (nginx, traefik)
- Deploy multiple instances
- Use shared storage for data files

### Vertical Scaling
- Increase Docker memory limits
- Use more powerful instances
- Optimize model parameters

## 🔄 Updates

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

### Updating Dependencies
```bash
# Update requirements
pip install -r requirements.txt --upgrade

# Update Docker image
docker-compose build --no-cache
docker-compose up -d
```

## 📞 Support

For deployment issues:
1. Check the logs
2. Verify environment variables
3. Test with the test script: `python test_complete_system.py`
4. Contact Surya Gouthu for support
