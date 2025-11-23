import requests
import json
import sys

def test_complex_queries():
    print("🚀 Starting Complex Query Test...")
    print("Target: http://localhost:8000/chat\n")
    
    url = "http://localhost:8000/chat"
    
    complex_queries = [
        # Query 1: Connects Certifications (AWS) with Experience (Mindtree/Acer)
        "How do his AWS certifications relate to his work at Mindtree?",
        
        # Query 2: Connects Thesis (NLP/Sentiment) with Current Work (Acer GenAI)
        "How is his Master's thesis related to his current work at Acer?",
        
        # Query 3: Connects Volunteering (Leadership) with Soft Skills
        "Does he have any leadership experience outside of his technical roles?",
        
        # Query 4: Connects Hobbies (Dota 2) with Personality (just for fun/synthesis)
        "What does his Dota 2 playtime say about his dedication?",
        
        # Query 5: Multilingual + Professional
        "Can he communicate with teams in India in their native language?"
    ]
    
    for query in complex_queries:
        print(f"❓ Query: '{query}'")
        try:
            response = requests.post(url, json={"message": query})
            if response.status_code == 200:
                answer = response.json().get("response", "No response")
                print(f"💡 Answer: {answer}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Connection Error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_complex_queries()
