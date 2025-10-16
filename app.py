#!/usr/bin/env python3
"""
Boku - Surya Gouthu's AI Portfolio Assistant
Main application with clean, modular architecture
"""

import gradio as gr
from core.chat_engine import ChatEngine
from config import SERVER_PORT, SERVER_HOST, HF_API_KEY
import os


def create_gradio_interface(chat_engine):
    """
    Create Gradio interface for the chat application
    
    Args:
        chat_engine (ChatEngine): Initialized chat engine
        
    Returns:
        gr.Blocks: Gradio interface
    """
    def respond(message, history):
        """Handle user messages and generate responses"""
        response = chat_engine.chat(message)
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        return history, ""
    
    with gr.Blocks(title="Boku - Surya's AI Assistant") as demo:
        gr.Markdown("# 🤖 Boku - Surya Gouthu's AI Portfolio Assistant")
        gr.Markdown("Ask me anything about Surya's professional background, skills, experience, projects, or education!")
        
        chatbot = gr.Chatbot(
            height=400,
            type="messages",
            label="Chat with Boku"
        )
        
        msg = gr.Textbox(
            label="Your Question",
            placeholder="Ask about Surya's skills, experience, projects, or education...",
            lines=2
        )
        
        clear = gr.Button("Clear Chat", variant="secondary")
        
        # Event handlers
        msg.submit(respond, [msg, chatbot], [chatbot, msg])
        clear.click(lambda: ([], ""), outputs=[chatbot, msg])
    
    return demo


def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "service": "boku-ai-assistant"}


def main():
    """Main application entry point"""
    print("🚀 Starting Boku AI Assistant...")
    
    # Check if API key is configured
    if not HF_API_KEY:
        print("❌ HF_API_KEY not found. Please set it in your .env file.")
        print("   Copy env.example to .env and configure your HuggingFace API key.")
        return
    
    # Initialize chat engine
    chat_engine = ChatEngine()
    
    if not chat_engine.initialize():
        print("❌ Failed to initialize chat engine. Exiting.")
        return
    
    # Create and launch Gradio interface
    demo = create_gradio_interface(chat_engine)
    
    # Add health check endpoint
    demo.launch(
        server_name=SERVER_HOST,
        server_port=SERVER_PORT,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()