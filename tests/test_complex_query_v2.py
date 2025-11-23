import requests
import json

def test_additional_complex_queries():
    print("🚀 Starting Additional Complex Query Test...")
    print("Target: http://localhost:8000/chat\n")
    
    url = "http://localhost:8000/chat"
    
    # New diverse complex queries
    complex_queries = [
        # Query 1: Education + Skills + Current Work
        "What skills from his Master's coursework does he use in his current GenAI work?",
        
        # Query 2: Multiple Certifications + Multiple Jobs
        "How do his certifications support his career progression from Mindtree to Acer?",
        
        # Query 3: Hobbies + Professional Skills (soft skills)
        "What soft skills can you infer from his hobbies and volunteering work?",
        
        # Query 4: Timeline + Technology Evolution
        "How has his technology stack evolved from his first job to his current role?",
        
        # Query 5: Research + Projects + Current Work
        "Does his thesis research influence any of his personal projects or current work?",
        
        # Query 6: Location + Languages + Work Authorization
        "Is he eligible to work with international teams, and can he communicate in multiple languages?",
        
        # Query 7: Awards + Skills + Impact
        "What technical skills helped him win the AIEEE AI Agent Hackathon?",
        
        # Query 8: Multi-company comparison
        "Compare his responsibilities at Mindtree versus Acer - what's different?",
    ]
    
    results = {"passed": 0, "failed": 0, "total": len(complex_queries)}
    
    for i, query in enumerate(complex_queries, 1):
        print(f"❓ Query {i}/{len(complex_queries)}: '{query}'")
        try:
            response = requests.post(url, json={"message": query})
            if response.status_code == 200:
                answer = response.json().get("response", "No response")
                
                # Check if answer is meaningful (not "I don't know")
                if "not in my files" in answer.lower() or "haven't told me" in answer.lower():
                    print(f"⚠️  Partial Answer: {answer[:150]}...")
                    results["failed"] += 1
                else:
                    print(f"✅ Answer: {answer[:150]}...")
                    results["passed"] += 1
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                results["failed"] += 1
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            results["failed"] += 1
        
        print("-" * 80)
    
    print(f"\n📊 Final Results:")
    print(f"   ✅ Passed: {results['passed']}/{results['total']}")
    print(f"   ❌ Failed: {results['failed']}/{results['total']}")
    print(f"   📈 Success Rate: {(results['passed']/results['total']*100):.1f}%")

if __name__ == "__main__":
    test_additional_complex_queries()
