import sys
import os
import logging

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(level=logging.INFO)

from core.knowledge_base import KnowledgeBase

def test_comprehensive_retrieval():
    print("🚀 Starting Comprehensive Retrieval Test...")
    
    kb = KnowledgeBase()
    # This will rebuild the index since we deleted the files
    if not kb.initialize():
        print("❌ Failed to initialize KnowledgeBase")
        return

    test_queries = [
        # --- Old Data ---
        ("Where did he work before Acer?", ["mindtree", "software engineer"]),
        ("What is his Master's thesis about?", ["thesis", "sentiment analysis", "twitter"]),
        ("What tech stack did he use for the e-commerce project?", ["react", "node", "mongodb"]),
        
        # --- New Data ---
        ("What certifications does Surya have?", ["aws", "certified developer", "mta", "python"]),
        ("Does he speak Telugu?", ["telugu", "multilingual"]),
        ("Tell me about his volunteering experience.", ["acm", "csun", "club", "gvp"]),
        ("What awards has he won recently?", ["hackathon", "aieee", "top 5"]),
        ("What are his hobbies?", ["dota 2", "cricket", "gaming"]),
        ("What coursework did he do in his Masters?", ["dsa", "cloud computing", "machine learning"])
    ]
    
    print(f"\nTesting {len(test_queries)} queries...\n")
    
    passed = 0
    
    for query, expected_keywords in test_queries:
        print(f"🔍 Query: '{query}'")
        results = kb.search(query, k=5)
        
        found = False
        if results:
            # Check all top results
            for i, result in enumerate(results):
                text = result.lower()
                matches = [kw for kw in expected_keywords if kw in text]
                if len(matches) > 0:
                    print(f"   ✅ Found keywords in Result {i+1}: {matches}")
                    found = True
                    break
            
            if not found:
                print(f"   ⚠️  No expected keywords found in top 5. Expected: {expected_keywords}")
                print(f"   Top result was: {results[0][:100]}...")
        else:
            print("   ❌ No results found")
            
        if found:
            passed += 1
        print("-" * 30)
    
    print(f"\n📊 Test Summary: {passed}/{len(test_queries)} queries retrieved relevant info.")

if __name__ == "__main__":
    test_comprehensive_retrieval()
