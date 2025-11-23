from sentence_transformers import SentenceTransformer
import numpy as np

def check_similarity():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    q1 = "where is his native"
    q2 = "what is his native place"
    
    e1 = model.encode([q1])[0]
    e2 = model.encode([q2])[0]
    
    similarity = np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2))
    
    print(f"Query 1: '{q1}'")
    print(f"Query 2: '{q2}'")
    print(f"Similarity Score: {similarity:.4f}")
    
    threshold = 0.85
    print(f"Threshold: {threshold}")
    print(f"Would hit cache? {'YES' if similarity >= threshold else 'NO'}")

if __name__ == "__main__":
    check_similarity()
