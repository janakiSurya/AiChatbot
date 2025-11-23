import requests
import sys

def test_streaming():
    url = "http://localhost:8000/chat"
    message = {"message": "tell me about surya"}
    
    print(f"🚀 Sending request to {url}...")
    print("-" * 50)

    try:
        # stream=True is critical here
        with requests.post(url, json=message, stream=True) as response:
            if response.status_code != 200:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                return

            print("✅ Connection established! Receiving stream:\n")
            
            # Iterate over lines or chunks
            for chunk in response.iter_content(chunk_size=None):
                if chunk:
                    text = chunk.decode('utf-8')
                    # Print immediately without newline to simulate typing
                    sys.stdout.write(text)
                    sys.stdout.flush()
                    
            print("\n" + "-" * 50)
            print("\n✅ Stream finished successfully")

    except Exception as e:
        print(f"\n❌ Exception: {e}")

if __name__ == "__main__":
    test_streaming()
