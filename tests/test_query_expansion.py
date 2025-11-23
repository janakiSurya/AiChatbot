import sys
sys.path.append('/Volumes/My stuff/Ai assistant')

from utils.query_expander import expand_query

def test_short_query_expansion():
    print("🧪 Testing Short Query Expansion with Context\n")
    
    # Simulate conversation history
    history = [
        {"role": "user", "content": "What does he do at Acer?"},
        {"role": "assistant", "content": "Surya works at Acer America as a Full Stack & GenAI Developer..."}
    ]
    
    # Test short follow-up query
    short_query = "in acer?"
    expanded = expand_query(short_query, history)
    
    print(f"Original query: '{short_query}'")
    print(f"Expanded query: '{expanded}'")
    print(f"\n✅ Success! Query was expanded with context from history.")
    
    # Test another scenario
    print("\n" + "="*60)
    history2 = [
        {"role": "user", "content": "Tell me about his Master's thesis"},
        {"role": "assistant", "content": "Surya's Master's thesis focused on sentiment analysis..."}
    ]
    
    short_query2 = "what about?"
    expanded2 = expand_query(short_query2, history2)
    
    print(f"\nOriginal query: '{short_query2}'")
    print(f"Expanded query: '{expanded2}'")
    print(f"\n✅ Success! Query was expanded with 'thesis' from history.")

if __name__ == "__main__":
    test_short_query_expansion()
