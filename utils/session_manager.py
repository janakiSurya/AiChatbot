"""
Session Manager for Conversation Memory
Stores per-user conversation history in Redis with automatic summarization.
Optimized for Upstash free tier (10K commands/day, 256MB storage).

Usage:
    session = SessionManager()
    history = session.get_history(session_id)
    session.add_message(session_id, "user", "What are his skills?")
    session.add_message(session_id, "assistant", "Surya has expertise in...")
"""

import json
import uuid
from typing import List, Dict, Optional
from datetime import datetime
from config import (
    UPSTASH_REDIS_URL,
    UPSTASH_REDIS_TOKEN,
    USE_REDIS_CACHE,
    logger
)


class SessionManager:
    """
    Manages per-user conversation sessions.
    - Stores history in Redis with TTL
    - Auto-summarizes long conversations
    - Falls back to in-memory for local dev
    """
    
    # Configuration
    SESSION_TTL = 60 * 60 * 24  # 24 hours
    MAX_MESSAGES_BEFORE_SUMMARY = 8  # Summarize after 8 messages
    MESSAGES_TO_SUMMARIZE = 4  # Summarize oldest 4, keep recent 4
    MAX_HISTORY_TOKENS = 2000  # Approx max tokens for history
    
    def __init__(self):
        self.redis = None
        self.is_connected = False
        self._memory_sessions = {}  # Fallback for local dev
        
        if USE_REDIS_CACHE:
            try:
                from upstash_redis import Redis
                self.redis = Redis(url=UPSTASH_REDIS_URL, token=UPSTASH_REDIS_TOKEN)
                self.redis.ping()
                self.is_connected = True
                logger.info("✅ Session manager connected to Redis")
            except Exception as e:
                logger.warning(f"⚠️ Redis connection failed: {e}. Using in-memory sessions.")
        else:
            logger.info("⚠️ Redis not configured. Using in-memory sessions.")
    
    @staticmethod
    def generate_session_id() -> str:
        """Generate a unique session ID"""
        return str(uuid.uuid4())[:8]
    
    def _get_session_key(self, session_id: str) -> str:
        """Generate Redis key for session"""
        return f"session:{session_id}"
    
    def get_history(self, session_id: str) -> List[Dict]:
        """
        Get conversation history for a session.
        Returns list of messages in ChatML format.
        """
        if not session_id:
            return []
        
        if self.is_connected and self.redis:
            try:
                key = self._get_session_key(session_id)
                data = self.redis.get(key)
                if data:
                    session = json.loads(data)
                    return session.get("messages", [])
            except Exception as e:
                logger.warning(f"Redis get error: {e}")
        
        # Fallback to in-memory
        return self._memory_sessions.get(session_id, {}).get("messages", [])
    
    def add_message(self, session_id: str, role: str, content: str):
        """
        Add a message to session history.
        Automatically triggers summarization if needed.
        
        Args:
            session_id: Unique session identifier
            role: "user" or "assistant"
            content: Message content
        """
        if not session_id:
            return
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        if self.is_connected and self.redis:
            try:
                key = self._get_session_key(session_id)
                data = self.redis.get(key)
                
                if data:
                    session = json.loads(data)
                else:
                    session = {"messages": [], "created": datetime.now().isoformat()}
                
                session["messages"].append(message)
                session["updated"] = datetime.now().isoformat()
                
                # Check if summarization needed
                if len(session["messages"]) > self.MAX_MESSAGES_BEFORE_SUMMARY:
                    session = self._summarize_session(session)
                
                self.redis.set(key, json.dumps(session), ex=self.SESSION_TTL)
                return
                
            except Exception as e:
                logger.warning(f"Redis set error: {e}")
        
        # Fallback to in-memory
        if session_id not in self._memory_sessions:
            self._memory_sessions[session_id] = {"messages": []}
        
        self._memory_sessions[session_id]["messages"].append(message)
        
        # Simple cleanup - limit to 50 sessions in memory
        if len(self._memory_sessions) > 50:
            oldest = next(iter(self._memory_sessions))
            del self._memory_sessions[oldest]
    
    def _summarize_session(self, session: Dict) -> Dict:
        """
        Summarize old messages to reduce token usage.
        Keeps recent messages intact, summarizes older ones.
        """
        messages = session["messages"]
        
        if len(messages) <= self.MAX_MESSAGES_BEFORE_SUMMARY:
            return session
        
        # Take oldest messages to summarize
        to_summarize = messages[:self.MESSAGES_TO_SUMMARIZE]
        to_keep = messages[self.MESSAGES_TO_SUMMARIZE:]
        
        # Create simple summary (no LLM call - saves API costs)
        summary_parts = []
        for msg in to_summarize:
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg["content"][:100]  # Truncate
            summary_parts.append(f"{role}: {content}...")
        
        summary = "Previous conversation summary:\n" + "\n".join(summary_parts)
        
        # Create summary message
        summary_message = {
            "role": "system",
            "content": summary,
            "timestamp": datetime.now().isoformat(),
            "is_summary": True
        }
        
        session["messages"] = [summary_message] + to_keep
        session["summary_count"] = session.get("summary_count", 0) + 1
        
        logger.info(f"📝 Summarized {len(to_summarize)} messages, keeping {len(to_keep)}")
        
        return session
    
    def clear_session(self, session_id: str):
        """Clear a session's history"""
        if not session_id:
            return
        
        if self.is_connected and self.redis:
            try:
                self.redis.delete(self._get_session_key(session_id))
            except Exception as e:
                logger.warning(f"Redis delete error: {e}")
        
        if session_id in self._memory_sessions:
            del self._memory_sessions[session_id]
    
    def get_formatted_history(self, session_id: str) -> List[Dict]:
        """
        Get history formatted for LLM (ChatML format).
        Returns: [{"role": "user/assistant/system", "content": "..."}]
        """
        history = self.get_history(session_id)
        
        # Return without timestamps for LLM
        return [{"role": msg["role"], "content": msg["content"]} for msg in history]
    
    def get_session_stats(self, session_id: str) -> Dict:
        """Get session statistics"""
        history = self.get_history(session_id)
        return {
            "message_count": len(history),
            "session_id": session_id,
            "has_summary": any(msg.get("is_summary") for msg in history)
        }


# Global instance
session_manager = SessionManager()
