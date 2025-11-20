#!/usr/bin/env python3
"""
Quick test for Boku's new personality
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.chat_engine import ChatEngine

def main():
    print("🚀 Testing Boku's New Personality...\n")
    
    # Initialize chat engine
    chat_engine = ChatEngine()
    if not chat_engine.initialize():
        print("❌ Failed to initialize")
        return
    
    print("✅ System initialized\n")
    
    # Test with a casual question
    query = "What does Surya do?"
    print(f"📝 QUERY: {query}")
    print("-" * 50)
    
    response = chat_engine.chat(query)
    print(f"🤖 BOKU: {response}\n")
    
    # Test with another question
    query2 = "Where is he working?"
    print(f"📝 QUERY: {query2}")
    print("-" * 50)
    
    response2 = chat_engine.chat(query2)
    print(f"🤖 BOKU: {response2}\n")

if __name__ == "__main__":
    main()
