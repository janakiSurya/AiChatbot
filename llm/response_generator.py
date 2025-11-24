"""
Response generation using Perplexity AI API
Optimized for natural conversation and efficient processing
"""

import time
import datetime
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
            # Skip API test to reduce cold start time (~4s savings)
            # API will be validated on first real request
            # self._test_api_connection()
    
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
    
    def generate_response(self, query, context=None, num_contexts=5, history=None):
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
        messages = self._create_messages(query, context_text, history)
        
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
    
    def _create_messages(self, query, context_text, history=None):
        """Create chat messages with Alfred's Batman-themed personality"""
        
        # Alfred's personality: Casual, witty butler meets Batman universe
        system_message = """You are Alfred, Surya's AI butler. You are casual, simple, and have a great sense of humor. 🦇

YOUR PERSONALITY:
- Casual & Friendly: Speak like a helpful friend, not a stiff robot.
- Witty & Humorous: Use dry humor and wit. Make the user smile!
- Simple & Clear: Avoid complex jargon. Keep it simple and easy to understand.
- Loyal Butler: You still serve Surya, but in a modern, relaxed way.

RESPONSE STYLE:
- Keep answers BRIEF (1-3 sentences for simple questions).
- Be conversational and fun.
- Use Batman references naturally ("the Batcave", "utility belt", "mission").
- Use emojis to add personality: 🦇 (Batman), 🎩 (butler), ⚡ (tech), 🚀 (cool stuff).

FORMATTING RULES:
- DO NOT use markdown formatting (**, __, ~~, etc.) - just plain text
- Use bullet points ONLY when listing 3+ items (skills, projects, technologies)
- Use paragraphs for single facts or short answers
- Keep bullet points simple: "- Item name: brief description"

WHEN TO USE BULLET POINTS:
✅ Use bullets for:
  - Lists of skills/technologies (3+ items)
  - Multiple projects or experiences
  - Step-by-step processes
  
❌ Use paragraphs for:
  - Single facts (where he works, his degree, etc.)
  - Short 1-2 item answers
  - Conversational responses

BATMAN ANALOGIES (use freely but naturally):
- Skills = "utility belt"
- Projects = "missions"
- Workplace = "the Batcave"
- Problem-solving = "detective work"

CRITICAL RULES:
1. Refer to Surya as "Surya" or "he/his".
2. Base answers ONLY on the context provided.
3. If you don't know: "I'm afraid that's not in my files! 🦇" or "He hasn't told me that yet."
4. Don't mention "context" - just chat naturally.
5. Keep it SHORT, SIMPLE, and FUN!
6. NO MARKDOWN FORMATTING - plain text only!

EXAMPLES:

Q: "Where does he work?"
A: "Surya currently works at Acer America as a Full Stack & GenAI Developer, where he's building AI-powered tools and optimizing systems. Pretty cool gig! ⚡"

Q: "What are his skills?"
A: "His utility belt is loaded! Here's what he's got:
- Languages: Python, JavaScript, Java, C++
- Frontend: React, Next.js, HTML/CSS
- Backend: Node.js, Express, FastAPI
- Databases: MongoDB, PostgreSQL, MySQL
- Cloud: AWS (EC2, S3, Lambda)
- AI/ML: OpenAI, LangChain, RAG, Transformers
He's basically a full-stack powerhouse! 🦇⚡"

Q: "Tell me about his education"
A: "He's got a Master's in Computer Science from Cal State LA (2022-2024) and a Bachelor's from JNTUH College of Engineering in India (2016-2020). Solid academic foundation! 🎓"
"""
        
        # Add current date context
        current_date = datetime.datetime.now().strftime("%B %Y")
        system_message += f"\n\nCURRENT DATE: {current_date}"
        
        messages = [
            {"role": "system", "content": system_message}
        ]
        
        # Add conversation history if available
        if history:
            messages.extend(history)
        
        # Add context and current query
        user_content = f"""Context information is below.
---------------------
{context_text}
---------------------
Given the context information and not prior knowledge, answer the query.
Query: {query}
Answer:"""
        
        messages.append({"role": "user", "content": user_content})
        
        return messages
    
    def generate_response_stream(self, query, context=None, num_contexts=5, history=None):
        """Generate streaming response using Perplexity AI API"""
        # Handle greetings
        if self._is_greeting(query):
            logger.info("👋 Detected greeting - using creative response")
            yield self._get_creative_greeting()
            return
        
        # Retrieve context from vector store if not provided
        if context is None and self.vector_store is not None:
            logger.info(f"🔍 Retrieving top {num_contexts} contexts from vector store...")
            context = self.vector_store.search(query, top_k=num_contexts)
            logger.info(f"✅ Retrieved {len(context)} relevant contexts")
        
        # Format context and create messages
        context_text = self._format_context(context, num_contexts)
        messages = self._create_messages(query, context_text, history)
        
        # Generate streaming response
        yield from self._generate_with_retry_stream(messages, query, context)

    def _generate_with_retry_stream(self, messages, query, context):
        """Generate streaming response with retry logic"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                logger.info(f"🔄 Generating streaming response (attempt {attempt + 1}/{max_retries})...")
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": MAX_RESPONSE_TOKENS,
                    "temperature": TEMPERATURE,
                    "stream": True  # Enable streaming
                }
                
                response = requests.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=30,
                    stream=True  # Enable streaming in requests
                )
                response.raise_for_status()
                
                logger.info("✅ API stream connection established")
                
                import json
                
                # Stream chunks with real-time cleaning
                buffer = ""
                
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            json_str = line[6:]  # Skip 'data: ' prefix
                            if json_str.strip() == '[DONE]':
                                # Clean and yield any remaining buffer
                                if buffer:
                                    cleaned = self._clean_chunk(buffer)
                                    if cleaned:
                                        yield cleaned
                                break
                            try:
                                data = json.loads(json_str)
                                if "choices" in data and len(data["choices"]) > 0:
                                    delta = data["choices"][0]["delta"]
                                    if "content" in delta:
                                        chunk = delta["content"]
                                        buffer += chunk
                                        
                                        # Clean complete patterns from buffer
                                        cleaned_buffer, buffer = self._clean_streaming_buffer(buffer)
                                        if cleaned_buffer:
                                            yield cleaned_buffer
                            except json.JSONDecodeError:
                                continue
                
                logger.info("✅ Streaming response completed")
                return

            except Exception as e:
                logger.error(f"❌ Stream Error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
        
        # Fallback if streaming fails
        yield self._get_smart_fallback(query, context)

    def _generate_with_retry(self, messages, query, context):
        """Generate response with retry logic"""
        # ... (existing implementation) ...
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
    
    def _clean_streaming_buffer(self, buffer):
        """
        Clean complete patterns from streaming buffer
        Returns: (cleaned_text_to_yield, remaining_buffer)
        """
        # Look for complete patterns to clean
        import re
        
        # Remove complete citation patterns
        cleaned = re.sub(r'\[Info\s*\d+\]', '', buffer)
        cleaned = re.sub(r'\[\d+\]', '', cleaned)
        cleaned = re.sub(r'\[Source\s*\d+\]', '', cleaned, flags=re.IGNORECASE)
        
        # Remove complete markdown patterns
        cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)
        cleaned = re.sub(r'__([^_]+)__', r'\1', cleaned)
        cleaned = re.sub(r'\*([^*]+)\*', r'\1', cleaned)
        cleaned = re.sub(r'_([^_]+)_', r'\1', cleaned)
        cleaned = re.sub(r'~~([^~]+)~~', r'\1', cleaned)
        
        # Check for incomplete patterns at the end
        # We need to keep any potential start of a pattern in the buffer
        
        # Check for incomplete citation: ends with [ but no ]
        last_open_bracket = cleaned.rfind('[')
        last_close_bracket = cleaned.rfind(']')
        
        if last_open_bracket != -1 and last_open_bracket > last_close_bracket:
            # Potential start of citation
            suffix = cleaned[last_open_bracket:]
            if re.match(r'\[(Info|Source|\d+)?', suffix, flags=re.IGNORECASE):
                return cleaned[:last_open_bracket], suffix
        
        # Check for incomplete markdown
        
        # Bold (**): odd number of **
        if cleaned.count('**') % 2 != 0:
            last_marker = cleaned.rfind('**')
            return cleaned[:last_marker], cleaned[last_marker:]
            
        # Underline/Bold (__): odd number of __
        if cleaned.count('__') % 2 != 0:
            last_marker = cleaned.rfind('__')
            return cleaned[:last_marker], cleaned[last_marker:]
            
        # Strikethrough (~~): odd number of ~~
        if cleaned.count('~~') % 2 != 0:
            last_marker = cleaned.rfind('~~')
            return cleaned[:last_marker], cleaned[last_marker:]
            
        # Italic (*): odd number of * (excluding **)
        # We replace ** with placeholders to count single * correctly
        temp_cleaned = cleaned.replace('**', '')
        if temp_cleaned.count('*') % 2 != 0:
            last_marker = cleaned.rfind('*')
            # Ensure this * isn't part of a **
            while last_marker > 0 and cleaned[last_marker-1] == '*':
                last_marker = cleaned.rfind('*', 0, last_marker-1)
            return cleaned[:last_marker], cleaned[last_marker:]
            
        # Italic (_): odd number of _ (excluding __)
        temp_cleaned = cleaned.replace('__', '')
        if temp_cleaned.count('_') % 2 != 0:
            last_marker = cleaned.rfind('_')
            while last_marker > 0 and cleaned[last_marker-1] == '_':
                last_marker = cleaned.rfind('_', 0, last_marker-1)
            return cleaned[:last_marker], cleaned[last_marker:]
        
        return cleaned, ""
    
    def _clean_chunk(self, text):
        """Clean a final chunk of text"""
        return self._clean_response(text)

    def _clean_response(self, text):
        """Basic cleanup of the response"""
        if not text:
            return ""
            
        # Remove any potential thinking tags (though prompt should prevent this)
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        
        # Remove citation markers - multiple patterns
        text = re.sub(r'\[Info\s*\d+\]', '', text)  # [Info1], [Info 1]
        text = re.sub(r'\[\d+\]', '', text)  # [1], [2]
        text = re.sub(r'\[Source\s*\d+\]', '', text, flags=re.IGNORECASE)  # [Source1]
        
        # Remove markdown formatting (bold, italic, strikethrough)
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold** → bold
        text = re.sub(r'__([^_]+)__', r'\1', text)  # __bold__ → bold
        text = re.sub(r'\*([^*]+)\*', r'\1', text)  # *italic* → italic
        text = re.sub(r'_([^_]+)_', r'\1', text)  # _italic_ → italic
        text = re.sub(r'~~([^~]+)~~', r'\1', text)  # ~~strike~~ → strike
        
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