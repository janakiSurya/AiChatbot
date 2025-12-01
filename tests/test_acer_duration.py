"""
Test Date Awareness for Employment Duration
"""
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.chat_engine import ChatEngine

def test_acer_duration():
    print("\n" + "="*60)
    print("Testing Employment Duration Calculation")
    print("="*60)
    
    engine = ChatEngine()
    
    # Wait for initialization
    import time
    print("Waiting for engine initialization...")
    engine.initialize()  # Force initialization
    
    # Query about Acer duration
    query = "How long has he been working in Acer?"
    print(f"Query: {query}")
    
    # Inspect retrieved context
    print("\n--- Retrieved Context ---")
    context = engine.knowledge_base.search_engine.vector_search.search(query, k=5)
    for i, text in enumerate(context):
        print(f"[{i+1}] {text[:150]}...")
        if "July 2024" in text:
            print("   ✅ FOUND 'July 2024' in this chunk!")
            
    # Get response
    response = engine.chat(query)
    print(f"\nResponse:\n{response}")
    
    # Validation logic
    current_date = datetime.now()
    start_date = datetime(2024, 7, 1)
    
    # Calculate months difference
    months = (current_date.year - start_date.year) * 12 + (current_date.month - start_date.month)
    years = months // 12
    remaining_months = months % 12
    
    print(f"\n--- Verification ---")
    print(f"Start Date: July 2024")
    print(f"Current Date: {current_date.strftime('%B %Y')}")
    print(f"Actual Duration: ~{years} year(s) and {remaining_months} month(s)")
    
    # Check if response mentions the duration roughly correctly
    response_lower = response.lower()
    
    has_start_date = "july 2024" in response_lower
    has_duration = "year" in response_lower or "months" in response_lower
    
    if has_start_date:
        print("✅ Correctly mentions start date (July 2024)")
    else:
        print("⚠️  Start date not explicitly mentioned")
        
    if has_duration:
        print("✅ Mentions duration (years/months)")
    else:
        print("⚠️  Duration calculation might be missing")

if __name__ == "__main__":
    test_acer_duration()
