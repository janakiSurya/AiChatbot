#!/usr/bin/env python3
"""
Boku - Surya Gouthu's AI Portfolio Assistant
Working version with proper Gradio interface
"""

import gradio as gr
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import ollama
import os
import pickle

# Configuration
FAISS_INDEX_PATH = "./faiss_index.bin"
FAISS_DATA_PATH = "./faiss_data.pkl"
OLLAMA_MODEL = "llama3.2:3b"

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Global variables
faiss_index = None
documents_data = []
metadatas_data = []

def load_faiss_index():
    """Load existing FAISS index and data"""
    global faiss_index, documents_data, metadatas_data
    
    if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(FAISS_DATA_PATH):
        faiss_index = faiss.read_index(FAISS_INDEX_PATH)
        with open(FAISS_DATA_PATH, 'rb') as f:
            data = pickle.load(f)
            documents_data = data['documents']
            metadatas_data = data['metadatas']
        print(f"✅ Loaded FAISS index with {len(documents_data)} documents")
        return True
    return False

def search_documents(query, k=2):
    """Search documents using FAISS"""
    global faiss_index, documents_data
    
    query_embedding = embedding_model.encode(query).astype('float32')
    query_embedding = query_embedding.reshape(1, -1)
    faiss.normalize_L2(query_embedding)
    
    scores, indices = faiss_index.search(query_embedding, k)
    
    contexts = []
    for idx in indices[0]:
        if idx < len(documents_data):
            context = documents_data[idx]
            if len(context) > 200:
                context = context[:200] + "..."
            contexts.append(context)
    
    return contexts

def generate_response(query, context):
    """Generate response using Ollama"""
    context_text = " ".join(context[:2])
    
    prompt = f"""You are Boku, Surya Gouthu's AI assistant. Answer the question about Surya using ONLY the information provided below. Speak about Surya in third person (he/his/him).

CONTEXT: {context_text}

QUESTION: {query}

ANSWER:"""
    
    try:
        response = ollama.generate(
            model=OLLAMA_MODEL,
            prompt=prompt,
            options={
                "temperature": 0.1,
                "num_predict": 100,
                "stop": ["QUESTION:", "CONTEXT:", "\n\n"]
            }
        )
        
        answer = response['response'].strip()
        
        if "ANSWER:" in answer:
            answer = answer.split("ANSWER:")[-1].strip()
        
        # Convert first person to third person
        answer = answer.replace("I am ", "Surya is ")
        answer = answer.replace("I have ", "He has ")
        answer = answer.replace("I work ", "He works ")
        answer = answer.replace("My ", "Surya's ")
        answer = answer.replace("I'm ", "He's ")
        
        if len(answer) > 20:
            return answer
        else:
            return context[0] if context else "I don't have enough information about that."
            
    except Exception as e:
        print(f"Ollama error: {e}")
        return context[0] if context else "I'm having trouble generating a response."

def chat_with_boku(message):
    """Main chat function"""
    contexts = search_documents(message)
    
    if not contexts:
        return "I don't have enough information to answer that question about Surya's portfolio."
    
    try:
        response = generate_response(message, contexts)
        if len(response) > 20:
            return response
    except Exception as e:
        print(f"Generation failed: {e}")
    
    # Fallback to direct context
    best_context = contexts[0]
    converted = best_context.replace("I am ", "Surya is ")
    converted = converted.replace("I have ", "He has ")
    converted = converted.replace("I work ", "He works ")
    converted = converted.replace("My ", "Surya's ")
    converted = converted.replace("I'm ", "He's ")
    
    return converted

# Initialize
if load_faiss_index():
    print("✅ Boku is ready!")
else:
    print("❌ Failed to load FAISS index")
    exit(1)

# Create Gradio interface
def respond(message, history):
    response = chat_with_boku(message)
    history.append((message, response))
    return history, ""

# Create the interface
with gr.Blocks(title="Boku - Surya's AI Assistant") as demo:
    gr.Markdown("# 🤖 Boku - Surya Gouthu's AI Portfolio Assistant")
    gr.Markdown("Ask me anything about Surya's professional background, skills, experience, projects, or education!")
    
    chatbot = gr.Chatbot(height=400, type="messages")
    msg = gr.Textbox(label="Your Question", placeholder="Ask about Surya...")
    clear = gr.Button("Clear Chat")
    
    msg.submit(respond, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: ([], ""), outputs=[chatbot, msg])

if __name__ == "__main__":
    print("🚀 Starting Boku...")
    demo.launch(server_port=7865, share=False)
