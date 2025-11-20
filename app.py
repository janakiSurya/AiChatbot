#!/usr/bin/env python3
"""
Boku - Surya Gouthu's AI Portfolio Assistant
Main application with refined, clean UI
"""

import gradio as gr
import requests
import json
from config import SERVER_PORT, SERVER_HOST, PERPLEXITY_API_KEY
import os

# API URL
API_URL = "http://localhost:8000/chat"

def create_gradio_interface():
    """
    Create refined, clean Gradio interface for the chat application
    
    Returns:
        gr.Blocks: Refined Gradio interface
    """
    def respond(message, history):
        """Handle user messages and generate responses via API"""
        try:
            response = requests.post(API_URL, json={"message": message})
            
            if response.status_code == 200:
                bot_response = response.json().get("response", "Error: Empty response")
            elif response.status_code == 429:
                bot_response = "⚠️ Rate Limit Exceeded: You have sent too many requests. Please try again in an hour."
            else:
                bot_response = f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            bot_response = f"Connection Error: Is the backend API running? ({str(e)})"

        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": bot_response})
        return history, ""
    
    # Refined CSS for a clean, professional look
    custom_css = """
    .gradio-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .header-section {
        text-align: center;
        margin-bottom: 30px;
        padding: 20px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        border: 1px solid #dee2e6;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px;
    }
    
    .logo-image {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .title {
        font-size: 2.2em;
        font-weight: 600;
        color: #2c3e50;
        margin: 0;
    }
    
    .subtitle {
        font-size: 1.1em;
        color: #6c757d;
        margin: 8px 0 0 0;
        font-weight: 400;
    }
    
    .chat-container {
        background: #ffffff;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        overflow: hidden;
    }
    
    .input-section {
        background: #f8f9fa;
        padding: 20px;
        border-top: 1px solid #e9ecef;
    }
    
    .gradio-button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .gradio-button.primary {
        background: #007bff;
        border-color: #007bff;
    }
    
    .gradio-button.primary:hover {
        background: #0056b3;
        border-color: #0056b3;
        transform: translateY(-1px);
    }
    
    .gradio-button.secondary {
        background: #6c757d;
        border-color: #6c757d;
    }
    
    .gradio-button.secondary:hover {
        background: #545b62;
        border-color: #545b62;
    }
    
    .gradio-textbox textarea {
        border-radius: 8px;
        border: 1px solid #ced4da;
        transition: border-color 0.2s ease;
    }
    
    .gradio-textbox textarea:focus {
        border-color: #007bff;
        box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
    }
    
    .gradio-chatbot {
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #28a745;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    """
    
    with gr.Blocks(
        title="Boku AI Assistant - Surya's Portfolio",
        css=custom_css,
        theme=gr.themes.Soft()
    ) as demo:
        
        # Refined header section
        gr.HTML("""
        <div class="header-section">
            <div class="logo-container">
                <div>
                    <h1 class="title">Boku AI Assistant</h1>
                    <p class="subtitle">
                        <span class="status-indicator"></span>
                        Advanced Portfolio Intelligence System
                    </p>
                </div>
            </div>
        </div>
        """)
        
        # Main chat interface
        with gr.Column(elem_classes="chat-container"):
            chatbot = gr.Chatbot(
                height=450,
                type="messages",
                label="Chat with Boku",
                container=True,
                show_copy_button=True,
                avatar_images=("Boku.png", "Boku.png")
            )
            
            # Input section
            with gr.Column(elem_classes="input-section"):
                with gr.Row():
                    msg = gr.Textbox(
                        label="Your Question",
                        placeholder="Ask about Surya's skills, experience, projects, or education...",
                        lines=2,
                        scale=4,
                        container=False
                    )
                    send_btn = gr.Button("Send", variant="primary", scale=1)
                
                with gr.Row():
                    clear_btn = gr.Button("Clear Chat", variant="secondary")
                    gr.HTML("<div style='flex: 1;'></div>")  # Spacer
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; margin-top: 20px; padding: 15px; color: #6c757d; font-size: 0.9em;">
            Powered by Perplexity AI • Built with RAG Pipeline • Surya Gouthu's Portfolio Assistant
        </div>
        """)
        
        # Event handlers
        def send_message(message, history):
            if message.strip():
                return respond(message, history)
            return history, ""
        
        msg.submit(send_message, [msg, chatbot], [chatbot, msg])
        send_btn.click(send_message, [msg, chatbot], [chatbot, msg])
        clear_btn.click(lambda: ([], ""), outputs=[chatbot, msg])
    
    return demo


def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "service": "boku-ai-assistant"}


def main():
    """Main application entry point"""
    print("🚀 Starting Boku AI Assistant (UI Frontend)...")
    print(f"📡 Connecting to Backend API at: {API_URL}")
    
    # Create and launch refined Gradio interface
    demo = create_gradio_interface()
    
    print("✅ Boku AI Assistant UI ready!")
    print("🌐 Access the interface at: http://localhost:7871")
    
    # Launch with refined settings
    demo.launch(
        server_name=SERVER_HOST,
        server_port=SERVER_PORT,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()