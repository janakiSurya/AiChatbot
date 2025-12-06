# Koyeb Deployment Guide

Deploy the AI Assistant to Koyeb's free tier with Pinecone Inference API for minimal memory usage.

## Prerequisites

- GitHub account (Koyeb deploys from Git)
- Koyeb account ([app.koyeb.com](https://app.koyeb.com))
- Pinecone account with API key
- Perplexity API key

---

## Step 1: Re-index Your Data

> **IMPORTANT**: The new Pinecone Inference API uses a different embedding model (`multilingual-e5-large` with 1024 dimensions) than your current `all-MiniLM-L6-v2` (384 dimensions).

You need to either:

**Option A**: Create a new Pinecone index (recommended)
```bash
# Update config.py with new index name
PINECONE_INDEX_NAME = "portfolio-assistant-v2"
```

**Option B**: Delete and recreate existing index
```python
# Run locally before deploying
python scripts/reindex_pinecone.py
```

---

## Step 2: Push to GitHub

```bash
cd "/Volumes/My stuff/Ai assistant"

git add .
git commit -m "Migrate to Koyeb with Pinecone Inference API

- Remove PyTorch/sentence-transformers (saves ~2GB)
- Use Pinecone Inference API for embeddings
- Add Dockerfile for Koyeb deployment
- Memory: ~400MB -> ~50MB"

git push origin main
```

---

## Step 3: Deploy on Koyeb

1. Go to [app.koyeb.com](https://app.koyeb.com) and sign in
2. Click **Create Service** → **Web Service**
3. Connect your GitHub repo
4. Configure:

| Setting | Value |
|---------|-------|
| **Builder** | Dockerfile |
| **Instance type** | Free (256MB RAM) |
| **Region** | Choose closest to users |
| **Port** | 8000 |

5. Add **Environment Variables**:

| Variable | Value |
|----------|-------|
| `PINECONE_API_KEY` | Your Pinecone API key |
| `PINECONE_ENVIRONMENT` | `us-east-1` (or your region) |
| `PINECONE_INDEX_NAME` | `portfolio-assistant-v2` |
| `PERPLEXITY_API_KEY` | Your Perplexity API key |
| `PERPLEXITY_MODEL` | `sonar` |
| `UPSTASH_REDIS_URL` | Your Upstash URL (optional) |
| `UPSTASH_REDIS_TOKEN` | Your Upstash token (optional) |

6. Click **Deploy**

---

## Step 4: Verify Deployment

Once deployed, test the endpoints:

```bash
# Get your Koyeb URL (e.g., your-app-name.koyeb.app)

# Test ping
curl https://your-app-name.koyeb.app/ping

# Test health
curl https://your-app-name.koyeb.app/health

# Test chat
curl -X POST https://your-app-name.koyeb.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are Surya skills?"}'

# Check memory usage
curl https://your-app-name.koyeb.app/stats
```

---

## Step 5: Update Frontend

Update your React portfolio to use the new Koyeb URL:

```javascript
// In your frontend code
const API_URL = "https://your-app-name.koyeb.app/chat";
```

---

## Step 6: Update UptimeRobot

1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Update monitor URL to: `https://your-app-name.koyeb.app/ping`
3. Set interval: 5 minutes

---

## Troubleshooting

### Memory Issues
If you see OOM (out of memory) errors:
- Check `/stats` endpoint for memory usage
- Ensure you're NOT loading local embedding model
- Verify `requirements.txt` doesn't include `torch`

### Embedding Errors
If embeddings fail:
- Verify `PINECONE_API_KEY` is set correctly
- Check Pinecone dashboard for API quota
- Ensure index dimension is 1024 (not 384)

### Cold Starts
Koyeb free tier may sleep after inactivity:
- Set up UptimeRobot to ping every 5 minutes
- First request after sleep: ~10s (much faster than Render's 30-50s)

---

## Expected Performance

| Metric | Render (Before) | Koyeb (After) |
|--------|-----------------|---------------|
| **Memory** | ~400MB | ~50-100MB |
| **Cold Start** | 30-50s | ~10s |
| **Warm Response** | ~1.5s | ~1.5-2s |
| **Monthly Cost** | Free | Free |
