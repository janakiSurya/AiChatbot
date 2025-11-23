import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm.response_generator import ResponseGenerator
import datetime

def test_date_awareness():
    generator = ResponseGenerator()
    
    query = "How long hes been workin at acer"
    
    # Context retrieved from debug_retrieval.py
    context = [
        "Surya currently works at Acer America, USA as a Full Stack & GenAI Developer since July 2024. He focuses on integrating Generative AI capabilities into enterprise applications and building scalable AI-powered solutions.",
        "Surya worked at Mindtree as a Software Engineer from February 2020 to July 2022. He developed enterprise-grade web applications using Java, Spring Boot, and Angular, resulting in a 40% reduction in application response time."
    ]
    
    print(f"Query: {query}")
    print("-" * 20)
    
    # Test 1: Without Date (Current Behavior)
    print("\n--- Test 1: Without Date ---")
    response_no_date = generator.generate_response(query, context=context)
    print(f"Response: {response_no_date}")
    
    # Test 2: With Date in System Prompt (Simulated)
    print("\n--- Test 2: With Date ---")
    
    # Monkey patch _create_messages to include date
    original_create_messages = generator._create_messages
    
    def create_messages_with_date(query, context_text, history=None):
        messages = original_create_messages(query, context_text, history)
        current_date = datetime.datetime.now().strftime("%B %Y")
        messages[0]['content'] += f"\n\nCURRENT DATE: {current_date}"
        return messages
        
    generator._create_messages = create_messages_with_date
    
    response_with_date = generator.generate_response(query, context=context)
    print(f"Response: {response_with_date}")

if __name__ == "__main__":
    test_date_awareness()
