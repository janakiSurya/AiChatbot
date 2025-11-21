from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from core.chat_engine import ChatEngine
from config import logger, validate_config
import os

# Initialize Limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title="Alfred AI Assistant API",
    description="Backend API for Surya Gouthu's Portfolio Assistant",
    version="1.0.0"
)

# Add Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Configure CORS to allow requests from any origin (for development/portfolio)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific portfolio URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Chat Engine
chat_engine = ChatEngine()

# Request model
class ChatRequest(BaseModel):
    message: str

# Response model
class ChatResponse(BaseModel):
    response: str

@app.on_event("startup")
async def startup_event():
    """Initialize the chat engine on startup"""
    logger.info("🚀 Starting up Alfred API...")
    
    if not validate_config():
        logger.error("❌ Invalid configuration. Exiting.")
        import sys
        sys.exit(1)
        
    if chat_engine.initialize():
        logger.info("✅ Chat engine initialized")
    else:
        logger.error("❌ Failed to initialize chat engine")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "online", "service": "Alfred AI Assistant"}

@app.post("/chat", response_model=ChatResponse)
@limiter.limit("10/hour")
async def chat(request: Request, chat_request: ChatRequest):
    """
    Process a chat message and return the response
    """
    if not chat_request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        response = chat_engine.chat(chat_request.message)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
