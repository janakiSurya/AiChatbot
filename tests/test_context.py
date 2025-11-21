"""
Test script for context-aware conversation
"""
from core.chat_engine import ChatEngine
import time

def test_context():
    print("🚀 Starting Context-Aware Conversation Test...\n")
    
    engine = ChatEngine()
    engine.initialize()
    
    # Simulate a complex conversation about Thesis
    conversation = [
        "What research did he do for his master's?",
        "What models did he compare in it?",
        "Where can I read that?"
    ]
    
    for i, query in enumerate(conversation, 1):
        print(f"👤 User: {query}")
        
        start = time.time()
        response = engine.chat(query)
        elapsed = time.time() - start
        
        print(f"🤖 Alfred ({elapsed:.2f}s): {response}\n")
        print("-" * 60)
        
        # Small delay to simulate reading
        time.sleep(1)

if __name__ == "__main__":
    test_context()
