# Deployment Guide: Boku AI Assistant

This guide explains how to deploy the Boku AI Assistant backend and integrate it with your React portfolio.

## 1. Deploying the Backend (Free on Render)

Since your project uses **FAISS** (Vector Database) and Python, it cannot be deployed on Vercel's standard serverless functions (which have size limits). **Render** offers a generous free tier for Python web services.

> **Note on Data Persistence:**
> Render's free tier uses an "ephemeral" filesystem, meaning files created during runtime (like the FAISS index) are deleted when the app restarts.
> **Don't worry!** Your app is designed to handle this. On every startup, it checks if the index exists. If not, it automatically rebuilds it from your `data/portfolio_data.py` file in just a few seconds. Your data is safe because it lives in your code.

### Step 1: Push to GitHub
Make sure your latest code (including `api.py` and `requirements.txt`) is pushed to your GitHub repository.

### Step 2: Create Web Service on Render
1.  Go to [dashboard.render.com](https://dashboard.render.com).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.
4.  Configure the service:
    - **Name**: `boku-ai-backend` (or similar)
    - **Runtime**: `Python 3`
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
    - **Instance Type**: `Free`

### Step 3: Environment Variables
In the Render dashboard, scroll down to **Environment Variables** and add:
- `PERPLEXITY_API_KEY`: Your actual API key (starts with `pplx-...`)
- `PERPLEXITY_MODEL`: `sonar`
- `PYTHON_VERSION`: `3.9.0` (Recommended)

### Step 4: Deploy
Click **Create Web Service**. Render will build your app. Once finished, you will get a URL like `https://boku-ai-backend.onrender.com`.

---

## 2. Integrating with React Portfolio (Vercel)

Now that your backend is running, you can call it from your React frontend.

### Step 1: Create a Chat Component
Add this component to your React project:

```jsx
import React, { useState } from 'react';

const BokuChat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // REPLACE THIS WITH YOUR RENDER URL
  const API_URL = "https://boku-ai-backend.onrender.com/chat";

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });

      const data = await response.json();
      
      const botMessage = { role: 'assistant', content: data.response };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I'm having trouble connecting right now." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-widget">
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
        {isLoading && <div className="message assistant">Thinking...</div>}
      </div>
      
      <form onSubmit={sendMessage}>
        <input 
          value={input} 
          onChange={(e) => setInput(e.target.value)} 
          placeholder="Ask about Surya..."
        />
        <button type="submit" disabled={isLoading}>Send</button>
      </form>
    </div>
  );
};

export default BokuChat;
```

### Step 2: Styling
Add CSS to make it look good (glassmorphism, floating button, etc.).

### Step 3: Environment Variables (Optional)
Ideally, store the API URL in your React project's `.env` file:
`REACT_APP_BOKU_API_URL=https://boku-ai-backend.onrender.com/chat`

---

## Troubleshooting

- **Cold Starts**: On Render's free tier, the server spins down after inactivity. The first request might take 30-50 seconds. This is normal for free hosting.
- **CORS Errors**: If you see CORS errors in the browser console, ensure `api.py` has `allow_origins=["*"]` (which I have already configured).
