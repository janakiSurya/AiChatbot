import sys
sys.path.append('/Volumes/My stuff/Ai assistant')

from core.knowledge_base import KnowledgeBase

def test_optimal_k():
    print("🔍 Testing Optimal k Value for Retrieval\n")
    
    # Initialize knowledge base
    kb = KnowledgeBase()
    if not kb.initialize():
        print("❌ Failed to initialize knowledge base")
        return
    
    # Test queries that previously needed k=15
    test_queries = [
        "How is his Master's thesis related to his current work at Acer?",
        "What does his Dota 2 playtime say about his dedication?",
        "How do his AWS certifications relate to his work at Mindtree?"
    ]
    
    for query in test_queries:
        print(f"Query: {query}")
        print("-" * 60)
        
        # Test with different k values
        for k in [8, 10, 12, 15]:
            results = kb.search(query, k=k)
            
            # Check if relevant info is in results
            query_lower = query.lower()
            relevant_count = 0
            
            for result in results:
                result_lower = result.lower()
                # Check for key terms
                if 'thesis' in query_lower and 'thesis' in result_lower:
                    relevant_count += 1
                elif 'dota' in query_lower and 'dota' in result_lower:
                    relevant_count += 1
                elif 'aws' in query_lower and 'aws' in result_lower:
                    relevant_count += 1
                elif 'certification' in query_lower and 'certif' in result_lower:
                    relevant_count += 1
            
            print(f"  k={k:2d}: {relevant_count} relevant chunks found")
        
        print()

if __name__ == "__main__":
    test_optimal_k()
