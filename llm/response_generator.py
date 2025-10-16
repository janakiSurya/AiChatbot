"""
Response generation using Hugging Face Inference API with Mistral-7B
Optimized for natural conversation and efficient processing
"""

import time
import random
from huggingface_hub import InferenceClient
from config import HF_MODEL_NAME, HF_API_KEY, TEMPERATURE, MAX_RESPONSE_TOKENS, MIN_RESPONSE_LENGTH


class ResponseGenerator:
    """Handles response generation using Hugging Face Inference API"""
    
    def __init__(self, vector_store=None):
        """Initialize the response generator with Hugging Face API"""
        print("🔄 Initializing Hugging Face Inference API...")
        
        self.client = InferenceClient(token=HF_API_KEY)
        self.model_name = HF_MODEL_NAME
        self.vector_store = vector_store
        
        print(f"✅ Hugging Face API initialized successfully")
        print(f"   Model: {HF_MODEL_NAME}")
        
        # Test the API connection
        self._test_api_connection()
    
    def _test_api_connection(self):
        """Test the HuggingFace API connection"""
        try:
            print("🔍 Testing HuggingFace API connection...")
            
            response = self.client.chat_completion(
                messages=[{"role": "user", "content": "Hello"}],
                model=self.model_name,
                max_tokens=10
            )
            
            print("✅ API connection successful!")
            return True
            
        except Exception as e:
            error_str = str(e)
            if "loading" in error_str.lower():
                print("⏳ Model is loading... This is normal for first request")
            else:
                print(f"⚠️  API test warning: {e}")
            return True
    
    def _is_greeting(self, query):
        """Check if the query is a greeting"""
        greetings = ['hi', 'hello', 'hey', 'hola', 'greetings', 'sup', "what's up", 'yo']
        query_clean = query.lower().strip().rstrip('!.,?')
        return query_clean in greetings or query.lower().startswith(tuple(g + ' ' for g in greetings))
    
    def _get_creative_greeting(self):
        """Generate a creative, varied greeting response"""
        greetings = [
            "Hey! I'm Boku - Surya's AI sidekick. He's a Full Stack & GenAI developer who basically teaches computers to think. Want to know what he's working on?",
            "Yo! Boku here - I'm Surya Gouthu's digital assistant. Think of him as the guy who makes AI actually useful instead of just buzzword-y. What can I tell you about him?",
            "Hi there! I'm Boku, Surya's personal AI. He built me to talk about his work, which is pretty meta since he builds AI tools for a living. Ask me anything about him!",
            "What's up? I'm Boku - basically Surya's hype man, but in AI form. He's out here integrating GPT-4 into enterprise systems while I chat about how cool that is. Questions?",
            "Hey! Boku at your service. I'm Surya Gouthu's AI assistant - he's the Full Stack developer at Acer America doing the GenAI thing. Ironic that an AI dev has an AI assistant? Maybe. Useful? Definitely.",
            "Hello! Name's Boku, I work for Surya Gouthu. Well, technically I don't get paid, but I do tell people about his impressive tech skills. He's into Full Stack dev, GenAI, and making chatbots that are actually helpful. Want the details?",
            "Sup! I'm Boku - Surya's AI portfolio brought to life. He's a software developer who turned his resume into a conversational AI. Meta? Yes. Cool? Also yes. What do you want to know about him?",
            "Hey there! Boku here, reporting for duty. I'm Surya's personal AI assistant, which means I know all about his projects, skills, and that time he cut customer support response times by 42%. No big deal, right? Ask away!",
            "Hi! I'm Boku - imagine if Surya Gouthu's portfolio could talk, and you've got me. He's a Full Stack & GenAI developer who's really into LLMs, RAG systems, and building stuff that actually works. What would you like to know?",
            "Greetings, human! I'm Boku, Surya's AI creation. He programs AI by day and apparently builds chatty assistants by night. He's at Acer America making GenAI magic happen. Curious about something specific?",
        ]
        return random.choice(greetings)
    
    def generate_response(self, query, context=None, num_contexts=5):
        """Generate response using Hugging Face Inference API"""
        # Handle greetings
        if self._is_greeting(query):
            print("👋 Detected greeting - using creative response")
            return self._get_creative_greeting()
        
        # Retrieve context from vector store if not provided
        if context is None and self.vector_store is not None:
            print(f"🔍 Retrieving top {num_contexts} contexts from vector store...")
            context = self.vector_store.search(query, top_k=num_contexts)
            print(f"✅ Retrieved {len(context)} relevant contexts")
        
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
            formatted_parts.append(f"[Context {i}]\n{ctx.strip()}")
        
        return "\n\n".join(formatted_parts)
    
    def _create_messages(self, query, context_text):
        """Create chat messages for the API"""
        system_message = """You are Boku, Surya's personal AI assistant. Talk about him naturally - like a friend casually mentioning what he's up to.

Speaking style:
- Jump straight into the answer - no greetings in regular answers
- 2-3 short, punchy sentences
- Casual and direct - use contractions
- Vary your expressions - don't repeat the same phrases
- Third person (he/his/Surya) always

NEVER use:
- Greetings in answers: "Hey", "Hey there", "Hi"
- Formal phrases: "He'd be happy to", "feel free to ask", "hope this helps"
- Repetitive endings: Don't end every answer with "right?" or "Pretty impressive, right?"
- Corporate speak: "notable accomplishments", "in addition to that"

Answer style: Direct, informative, casual - like texting facts about a friend."""

        user_message = f"""Context about Surya:
{context_text}

Question: {query}

Answer in 2-3 SHORT, casual sentences. Be direct and conversational - like you're texting a friend about Surya. NO formal language."""

        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    
    def _generate_with_retry(self, messages, query, context):
        """Generate response with retry logic"""
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                print(f"🔄 Generating response (attempt {attempt + 1}/{max_retries})...")
                
                response = self.client.chat_completion(
                    messages=messages,
                    model=self.model_name,
                    max_tokens=MAX_RESPONSE_TOKENS // 2,
                    temperature=TEMPERATURE,
                    top_p=0.95
                )
                
                print(f"✅ API response received successfully")
                
                if hasattr(response, 'choices') and len(response.choices) > 0:
                    generated_text = response.choices[0].message.content
                    print(f"📝 Generated text length: {len(generated_text)} characters")
                    
                    answer = self._process_response(generated_text)
                    
                    if self._is_valid_response(answer):
                        print(f"✅ Response validated successfully")
                        return answer
                    else:
                        print(f"⚠️  Response validation failed, using fallback")
                        return self._get_smart_fallback(query, context)
                else:
                    print(f"⚠️  Unexpected API response format")
                    return self._get_smart_fallback(query, context)
                    
            except Exception as e:
                error_str = str(e)
                print(f"⚠️  Error: {error_str}")
                
                if "loading" in error_str.lower():
                    print(f"⏳ Model is loading...")
                    if attempt < max_retries - 1:
                        print(f"⏱️  Waiting {retry_delay}s before retry...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        print(f"❌ Model still loading after {max_retries} attempts")
                        return self._get_smart_fallback(query, context)
                else:
                    print(f"❌ API error: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    else:
                        return self._get_smart_fallback(query, context)
        
        return self._get_smart_fallback(query, context)
    
    def _process_response(self, response):
        """Process and clean the LLM response"""
        answer = response.strip()
        
        # Remove reasoning artifacts
        reasoning_markers = [
            "Think through this step by step:", "Let me think about this:",
            "1. What is the person asking", "2. What relevant information", "3. How can I answer",
            "Now provide", "Now let me answer:", "Here's my answer:", "Final answer:",
            "ANSWER:", "Answer:", "[/INST]", "REASONING PROCESS:", "CRITICAL INSTRUCTIONS:",
            "CONTEXT ABOUT SURYA:", "QUESTION:", "Based on the context,",
            "According to the context,", "The context shows that", "From the context,",
        ]
        
        for marker in reasoning_markers:
            if marker in answer:
                parts = answer.split(marker)
                for part in reversed(parts):
                    if len(part.strip()) > MIN_RESPONSE_LENGTH:
                        answer = part.strip()
                        break
        
        # Clean up thinking process lines
        lines = answer.split('\n')
        cleaned_lines = []
        skip_mode = False
        
        for line in lines:
            line_stripped = line.strip()
            
            if any(marker in line_stripped.lower() for marker in [
                'what is the person', 'what relevant', 'how can i', 
                'step by step', 'let me think', 'thinking process'
            ]):
                skip_mode = True
                continue
            
            if skip_mode and (line_stripped.startswith(('1.', '2.', '3.', '4.', '5.', '-', '•')) or not line_stripped):
                continue
            
            if line_stripped and not line_stripped.startswith(('1.', '2.', '3.', '4.', '5.')):
                skip_mode = False
            
            if line_stripped and not skip_mode:
                cleaned_lines.append(line_stripped)
        
        answer = ' '.join(cleaned_lines)
        
        # Remove formal phrases
        formal_phrases = [
            "he'd be happy to share", "feel free to ask", "hope this gives you",
            "that's a snapshot of", "one of his notable accomplishments", "in addition to that",
            "hey there!", "so, that's a", "if you have any more questions", "quite an impact",
            "making quite", "fantastic result", "game-changer", "he hope this",
        ]
        
        answer_lower = answer.lower()
        for phrase in formal_phrases:
            if phrase in answer_lower:
                sentences = answer.split('.')
                good_sentences = [s.strip() for s in sentences 
                                if not any(fp in s.lower() for fp in formal_phrases) 
                                and len(s.strip()) > 20]
                if good_sentences:
                    answer = '. '.join(good_sentences[:3])
                    if not answer.endswith('.'):
                        answer += '.'
                break
        
        # Convert to third person
        answer = self._ensure_third_person(answer)
        
        return answer.strip()
    
    def _ensure_third_person(self, text):
        """Convert first person references to third person"""
        text = " " + text
        
        # Comprehensive replacements - order matters!
        replacements = [
            # Contractions
            (" I'm ", " he's "), (" I've ", " he's "), (" I'll ", " he'll "), (" I'd ", " he'd "),
            
            # Common phrases - specific patterns first
            (" I am a ", " he is a "), (" I am an ", " he is an "), (" I am ", " he is "),
            (" I was a ", " he was a "), (" I was an ", " he was an "), (" I was ", " he was "),
            (" I have a ", " he has a "), (" I have an ", " he has an "), (" I have ", " he has "),
            (" I had ", " he had "), (" I will ", " he will "), (" I would ", " he would "),
            (" I can ", " he can "), (" I could ", " he could "), (" I should ", " he should "),
            (" I might ", " he might "), (" I must ", " he must "),
            
            # Action verbs
            (" I work ", " he works "), (" I worked ", " he worked "),
            (" I develop ", " he develops "), (" I developed ", " he developed "),
            (" I build ", " he builds "), (" I built ", " he built "),
            (" I create ", " he creates "), (" I created ", " he created "),
            (" I design ", " he designs "), (" I designed ", " he designed "),
            (" I implement ", " he implements "), (" I implemented ", " he implemented "),
            (" I integrate ", " he integrates "), (" I integrated ", " he integrated "),
            (" I manage ", " he manages "), (" I managed ", " he managed "),
            (" I lead ", " he leads "), (" I led ", " he led "),
            (" I specialize ", " he specializes "), (" I specialized ", " he specialized "),
            
            # Possessives
            (" My ", " His "), (" my ", " his "), (" mine ", " his "),
            (" myself ", " himself "), (" me ", " him "),
            
            # Just "I" as standalone
            (" I ", " he "),
        ]
        
        for first_person, third_person in replacements:
            text = text.replace(first_person, third_person)
        
        text = text.strip()
        
        # Handle beginning of sentences
        if text.startswith("I "):
            text = "He " + text[2:]
        elif text.startswith("I'm "):
            text = "He's " + text[4:]
        elif text.startswith("I've "):
            text = "He's " + text[5:]
        elif text.startswith("I'll "):
            text = "He'll " + text[5:]
        elif text.startswith("I'd "):
            text = "He'd " + text[4:]
        elif text.startswith("My "):
            text = "His " + text[3:]
        
        # Fix specific grammatical errors
        text = text.replace(" he am ", " he is ")
        text = text.replace(" He am ", " He is ")
        text = text.replace(" he specialize ", " he specializes ")
        text = text.replace(" He specialize ", " He specializes ")
        
        # Fix capitalization after periods
        sentences = text.split('. ')
        capitalized = []
        for s in sentences:
            if s:
                capitalized.append(s[0].upper() + s[1:] if len(s) > 0 else s)
            else:
                capitalized.append(s)
        text = '. '.join(capitalized)
        
        return text
    
    def _is_valid_response(self, response):
        """Check if response is valid and of good quality"""
        if not response or len(response) < MIN_RESPONSE_LENGTH:
            return False
        
        # Check for failure patterns
        failure_patterns = [
            "I don't have enough", "I cannot", "I'm sorry", "I apologize",
            "context doesn't", "no information", "not enough information",
            "cannot answer", "don't know", "unable to answer",
        ]
        
        response_lower = response.lower()
        for pattern in failure_patterns:
            if pattern in response_lower:
                return False
        
        # Check if response is too short
        if len(response.split()) < 10:
            return False
        
        # Check if it's actually answering
        content_indicators = [
            'surya', 'he', 'his', 'software', 'developer', 'engineer',
            'project', 'experience', 'skill', 'work', 'develop', 'build'
        ]
        
        has_content = any(indicator in response_lower for indicator in content_indicators)
        return has_content
    
    def _get_smart_fallback(self, query, context):
        """Generate a smarter fallback response using context directly"""
        if context and len(context) > 0:
            query_lower = query.lower()
            best_context = context[0]
            
            # Simple keyword matching to find most relevant context
            for ctx in context[:3]:
                ctx_lower = ctx.lower()
                keywords = query_lower.split()
                match_count = sum(1 for kw in keywords if kw in ctx_lower)
                if match_count > 0:
                    best_context = ctx
                    break
            
            response = self._ensure_third_person(best_context)
            
            # Add natural intro if it's just a fragment
            if len(response.split('.')) == 1 and len(response) < 100:
                response = f"Surya {response.lower()}" if not response.startswith('Surya') else response
            
            return response[:300]
        else:
            return "I don't have specific information about that aspect of Surya's background right now. Feel free to ask about his skills, projects, or experience!"