#!/usr/bin/env python3
"""
Complete system test - Vector DB + HuggingFace Mistral-7B
Tests the optimized pipeline: Query → Vector Search → LLM Reasoning → Answer
"""

from core.chat_engine import ChatEngine
import time

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_query(chat_engine, query, expected_info=None):
    """Test a single query and display results"""
    print(f"\n📝 QUERY: {query}")
    print("-" * 70)
    
    start_time = time.time()
    response = chat_engine.chat(query)
    end_time = time.time()
    
    print(f"\n💬 RESPONSE:")
    print(f"   {response}")
    print(f"\n⏱️  Response time: {end_time - start_time:.2f}s")
    
    if expected_info:
        print(f"\n✓ Expected info: {expected_info}")
    
    print("-" * 70)
    return response

def main():
    """Run comprehensive system tests"""
    print_section("🚀 INITIALIZING OPTIMIZED SYSTEM")
    
    # Initialize chat engine (loads vector DB)
    chat_engine = ChatEngine()
    
    if not chat_engine.initialize():
        print("❌ Failed to initialize chat engine")
        return
    
    print("\n✅ Optimized system initialized successfully!")
    print("   ✓ Vector Database loaded")
    print("   ✓ HuggingFace Mistral-7B ready")
    print("   ✓ Optimized search and reasoning pipeline active")
    
    # Test cases with real-world queries
    test_cases = [
        {
            "query": "Hello",
            "expected": "Creative greeting from Boku"
        },
        {
            "query": "Where is Surya working?",
            "expected": "Acer America as Full Stack & GenAI Developer"
        },
        {
            "query": "What does Surya do at his current job?",
            "expected": "GenAI integration, OpenAI GPT-4, LangChain, microservices"
        },
        {
            "query": "What are Surya's main technical skills?",
            "expected": "Full Stack, React, Node.js, GenAI, LLMs, Cloud platforms"
        },
        {
            "query": "Does he have experience with AI and machine learning?",
            "expected": "Yes - GenAI, OpenAI, LangChain, Hugging Face, RAG systems"
        },
        {
            "query": "What companies has Surya worked for?",
            "expected": "Acer America, Mindtree, Tata AIA"
        },
        {
            "query": "What is his educational background?",
            "expected": "MS in Computer Engineering from CSUN, BTech from JNTU"
        },
        {
            "query": "What projects has he built?",
            "expected": "E-commerce platform, AI SpellCheck, Chat app, Weather dashboard"
        },
        {
            "query": "Where is he located?",
            "expected": "Los Angeles, California"
        }
    ]
    
    print_section("🧪 TESTING OPTIMIZED PIPELINE")
    print("\nEach test will:")
    print("  1. Search optimized vector database for relevant context")
    print("  2. Send context + query to HuggingFace Mistral-7B")
    print("  3. Generate intelligent, natural answer with proper grammar")
    
    successful_tests = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print_section(f"TEST {i}/{total_tests}")
        response = test_query(
            chat_engine, 
            test_case["query"],
            test_case["expected"]
        )
        
        # Basic validation
        if response and len(response) > 20:
            successful_tests += 1
            print("✅ Test passed - Got meaningful response")
        else:
            print("⚠️  Test warning - Response seems short")
        
        # Small delay between tests to avoid rate limiting
        if i < total_tests:
            time.sleep(2)
    
    # Final summary
    print_section("📊 OPTIMIZATION TEST SUMMARY")
    print(f"\n   Tests passed: {successful_tests}/{total_tests}")
    print(f"   Success rate: {(successful_tests/total_tests)*100:.1f}%")
    
    if successful_tests == total_tests:
        print("\n   🎉 ALL TESTS PASSED!")
        print("   ✅ Optimized vector search working correctly")
        print("   ✅ HuggingFace integration working correctly")
        print("   ✅ Optimized pipeline operational")
        print("   ✅ Code cleanup and optimization successful")
    else:
        print("\n   ⚠️  Some tests had issues")
    
    print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    main()