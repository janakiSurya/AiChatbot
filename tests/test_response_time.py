import requests
import time

def test_response_times():
    print("⏱️  Testing Response Times\n")
    print("Target: http://localhost:8000/chat")
    print("="*70)
    
    url = "http://localhost:8000/chat"
    
    # Test queries of varying complexity
    test_queries = [
        ("Simple query", "What is his email?"),
        ("Medium query", "What does he do at Acer?"),
        ("Complex query", "How is his Master's thesis related to his current work at Acer?"),
        ("Multi-synthesis", "How do his AWS certifications relate to his work at Mindtree?"),
    ]
    
    results = []
    
    for query_type, query in test_queries:
        print(f"\n📝 {query_type}: '{query}'")
        
        try:
            start_time = time.time()
            response = requests.post(url, json={"message": query}, timeout=60)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response.status_code == 200:
                answer = response.json().get("response", "")
                print(f"⏱️  Response time: {response_time:.2f} seconds")
                print(f"✅ Answer length: {len(answer)} chars")
                print(f"📄 Preview: {answer[:100]}...")
                
                results.append({
                    "type": query_type,
                    "time": response_time,
                    "status": "success"
                })
            else:
                print(f"❌ Error: {response.status_code}")
                results.append({
                    "type": query_type,
                    "time": response_time,
                    "status": "error"
                })
                
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout after 60 seconds")
            results.append({
                "type": query_type,
                "time": 60,
                "status": "timeout"
            })
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "type": query_type,
                "time": 0,
                "status": "error"
            })
    
    # Summary
    print("\n" + "="*70)
    print("📊 PERFORMANCE SUMMARY")
    print("="*70)
    
    successful_times = [r["time"] for r in results if r["status"] == "success"]
    
    if successful_times:
        avg_time = sum(successful_times) / len(successful_times)
        min_time = min(successful_times)
        max_time = max(successful_times)
        
        print(f"\n✅ Successful queries: {len(successful_times)}/{len(results)}")
        print(f"⏱️  Average response time: {avg_time:.2f}s")
        print(f"⚡ Fastest response: {min_time:.2f}s")
        print(f"🐌 Slowest response: {max_time:.2f}s")
        
        # Performance rating
        if avg_time < 10:
            print(f"\n🎯 EXCELLENT - Average response time under 10s!")
        elif avg_time < 15:
            print(f"\n✅ GOOD - Average response time under 15s")
        else:
            print(f"\n⚠️  NEEDS IMPROVEMENT - Average response time over 15s")
    else:
        print("\n❌ No successful queries to analyze")
    
    print("\nDetailed breakdown:")
    for r in results:
        status_icon = "✅" if r["status"] == "success" else "❌"
        print(f"  {status_icon} {r['type']:20s}: {r['time']:6.2f}s ({r['status']})")

if __name__ == "__main__":
    test_response_times()
