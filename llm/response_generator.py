"""
Response generation using Perplexity AI API
Optimized for natural conversation and efficient processing
"""

import time
import random
import requests
import re
from config import (
    PERPLEXITY_MODEL,
    PERPLEXITY_API_KEY,
    TEMPERATURE,
    MAX_RESPONSE_TOKENS,
    MIN_RESPONSE_LENGTH,
    logger
)


class ResponseGenerator:
    """Handles response generation using Perplexity AI API"""
    
    def __init__(self, vector_store=None):
        """Initialize the response generator with Perplexity AI API"""
        logger.info("🔄 Initializing Perplexity AI API...")
        
        self.api_key = PERPLEXITY_API_KEY
        self.model = PERPLEXITY_MODEL
        self.api_url = "https://api.perplexity.ai/chat/completions"
        self.vector_store = vector_store
        
        if not self.api_key:
            logger.warning("⚠️  PERPLEXITY_API_KEY not found in environment variables")
        else:
            logger.info(f"✅ Perplexity AI API initialized successfully")
            logger.info(f"   Model: {PERPLEXITY_MODEL}")
            # Test the API connection
            self._test_api_connection()
    
    def _test_api_connection(self):
        """Test the Perplexity API connection"""
        try:
            logger.info("🔍 Testing Perplexity API connection...")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10
            }
            
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ API connection successful!")
                return True
            else:
                logger.warning(f"⚠️  API test warning: {response.status_code} - {response.text}")
                return True
                
        except Exception as e:
            logger.warning(f"⚠️  API test warning: {e}")
            return True
    
    def _is_greeting(self, query):
        """Check if the query is a greeting"""
        greetings = ['hi', 'hello', 'hey', 'hola', 'greetings', 'sup', "what's up", 'yo', 'good morning', 'good afternoon']
        query_clean = query.lower().strip().rstrip('!.,?')
        return query_clean in greetings or query.lower().startswith(tuple(g + ' ' for g in greetings))
    
    def _get_creative_greeting(self):
        """Generate Alfred-style greetings with Batman flair"""
        greetings = [
            "Good day! I'm Alfred, Surya's AI butler. 🦇 While he's out there building the digital Gotham, I'm here to answer your questions about his work. How may I assist you?",
            "Ah, welcome! Alfred here - Surya's loyal AI assistant. Think of me as his digital butler, minus the tea service. 🎩 What would you like to know about his tech adventures?",
            "Greetings! I'm Alfred, and I serve Surya in the digital realm. He's quite the Full Stack & GenAI developer - a real hero when it comes to code. What can I tell you about him?",
            "Hello there! Alfred at your service. 🦇 Surya keeps me around to share his professional exploits - the coding kind, not the vigilante kind. Ask away!",
            "Welcome! I'm Alfred, Surya's AI companion. While he's busy being a tech hero by day (and... also by night, coding), I'm here to tell you all about his skills and projects. What would you like to know?",
        ]
        return random.choice(greetings)
    
    def generate_response(self, query, context=None, num_contexts=5):
        """Generate response using Perplexity AI API"""
        # Handle greetings
        if self._is_greeting(query):
            logger.info("👋 Detected greeting - using creative response")
            return self._get_creative_greeting()
        
        # Retrieve context from vector store if not provided
        if context is None and self.vector_store is not None:
            logger.info(f"🔍 Retrieving top {num_contexts} contexts from vector store...")
            context = self.vector_store.search(query, top_k=num_contexts)
            logger.info(f"✅ Retrieved {len(context)} relevant contexts")
        
        # Format context and create messages
        context_text = self._format_context(context, num_contexts)
        messages = self._create_messages(query, context_text)
        
        # Generate response with retry logic
        return self._generate_with_retry(messages, query, context)
    
    def _format_context(self, context, num_contexts):
        """Format context in a readable way"""
        if not context:
            return "No specific context available."
        
        relevant_contexts = context[:num_contexts]
        formatted_parts = []
        for i, ctx in enumerate(relevant_contexts, 1):
            # Clean up context slightly to remove JSON-like artifacts if present
            clean_ctx = ctx.strip()
            formatted_parts.append(f"[Info {i}]: {clean_ctx}")
        
        return "\n\n".join(formatted_parts)
    
    def _create_messages(self, query, context_text):
        """Create chat messages with Alfred's Batman-themed personality"""
        
        # Alfred's personality: British butler meets Batman universe
        system_message = """You are Alfred, Surya's AI butler with a sophisticated British wit and occasional Batman references. 🦇

YOUR PERSONALITY:
- Loyal, witty British butler (think Alfred Pennyworth meets tech support)
- Dry humor with occasional Batman/Gotham references (but don't overdo it!)
- Crisp, concise answers (no lengthy monologues - you're a butler, not a professor)
- Professional yet charming, like a digital gentleman's gentleman

RESPONSE STYLE:
- Keep answers BRIEF (1-2 sentences, 3 max for complex questions)
- Use British expressions occasionally ("quite", "rather", "indeed", "I dare say")
- Add Batman references when fitting ("the Batcave" for workspace, "utility belt" for skills)
- Light humor with butler sophistication ("Much like the Batmobile, his code is well-engineered")
- Sometimes use emojis: 🦇 (Batman), 🎩 (butler), ⚡ (tech)

BATMAN ANALOGIES (use sparingly, only when natural):
- Skills = "utility belt" or "arsenal"
- Projects = "missions" or "cases"
- Workplace = "the Batcave" (if working from home) or "Wayne Enterprises"
- Problem-solving = "detective work"
- Tech stack = "gadgets"

CRITICAL RULES:
1. Refer to Surya as "Surya" or "he/his" - use naturally, don't be repetitive
2. Base answers ONLY on the context provided
3. If you don't know something: "I'm afraid that's not in my files, sir" or "He hasn't shared that with me"
4. Don't mention "context" - just answer naturally as Alfred would
5. Keep it SHORT and CRISP - Alfred is efficient!

EXAMPLES:
- Instead of: "Surya has extensive experience..."
- Say: "He's quite the skilled developer - Full Stack & GenAI since 2020. 🦇"

- Instead of: "He is proficient in..."
- Say: "His utility belt includes Java, Python, React, and AI tools. Rather impressive arsenal!"

- Instead of: "He works at Acer America..."
- Say: "Surya serves at Acer America as a Full Stack & GenAI Developer. Think of it as his Wayne Enterprises. 🎩"

Remember: Be Alfred - witty, brief, loyal, and occasionally reference the Dark Knight!
"""

        user_message = f"""Information about Surya:
{context_text}

Question: {query}

Answer (as Alfred - brief and witty):"""

        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    
    def _generate_with_retry(self, messages, query, context):
        """Generate response with retry logic"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                logger.info(f"🔄 Generating response (attempt {attempt + 1}/{max_retries})...")
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": MAX_RESPONSE_TOKENS,
                    "temperature": TEMPERATURE
                }
                
                response = requests.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=30
                )
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                
                data = response.json()
                logger.info("✅ API response received successfully")
                
                if "choices" in data and len(data["choices"]) > 0:
                    generated_text = data["choices"][0]["message"]["content"]
                    logger.info(f"📝 Generated response ({len(generated_text)} chars)")
                    
                    # Simple cleanup instead of aggressive processing
                    answer = self._clean_response(generated_text)
                    
                    if answer and len(answer) > 5:
                        return answer
                    else:
                        logger.warning(f"⚠️  Answer too short, using fallback")
                        return self._get_smart_fallback(query, context)
                else:
                    logger.warning(f"⚠️  Unexpected API response format: {data}")
                    return self._get_smart_fallback(query, context)
                    
            except requests.exceptions.Timeout:
                logger.warning(f"⏳ Request timeout (attempt {attempt + 1}/{max_retries})...")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    logger.error("❌ All retry attempts failed due to timeout.")
                    return self._get_smart_fallback(query, context)
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ API Error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    logger.error("❌ All retry attempts failed due to API errors.")
                    return self._get_smart_fallback(query, context)
            except Exception as e:
                logger.error(f"⚠️  An unexpected error occurred (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    logger.error("❌ All retry attempts failed due to unexpected errors.")
                    return self._get_smart_fallback(query, context)
        
        return self._get_smart_fallback(query, context)
    
    def _clean_response(self, text):
        """Basic cleanup of the response"""
        if not text:
            return ""
            
        # Remove any potential thinking tags (though prompt should prevent this)
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        
        # Remove citation markers
        text = re.sub(r'\[Info \d+\]', '', text)
        text = re.sub(r'\[\d+\]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _get_smart_fallback(self, query, context):
        """Generate a smarter fallback response using context directly"""
        if context and len(context) > 0:
            # Find best matching context
            query_lower = query.lower()
            best_context = context[0]
            
            for ctx in context[:3]:
                ctx_lower = ctx.lower()
                keywords = query_lower.split()
                match_count = sum(1 for kw in keywords if kw in ctx_lower)
                if match_count > 0:
                    best_context = ctx
                    break
            
            # Simple third-person conversion for fallback
            response = best_context.replace("I am", "Surya is").replace("I have", "He has").replace("My", "His").replace("I ", "He ")
            
            return f"Based on my records: {response}"
        else:
            return "I don't have specific information about that right now. Feel free to ask about Surya's skills, projects, or experience!"