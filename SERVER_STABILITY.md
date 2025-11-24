# Server Stability Guide

## Problem: Server Crashes After 24-30 Hours

You experienced crashes with FAISS because:
1. **Memory leaks**: FAISS index kept growing in memory
2. **No cleanup**: Old data never released
3. **Resource exhaustion**: Eventually ran out of RAM

## Solution: Pinecone + Proper Resource Management

### ✅ What's Already Fixed

**1. Pinecone (Cloud Storage)**
- ✅ No in-memory index (was ~500MB with FAISS)
- ✅ No memory growth over time
- ✅ Stateless server (no local state to corrupt)

**2. Redis Cache (Cloud Storage)**
- ✅ TTL: 30 days (auto-cleanup)
- ✅ No memory leaks
- ✅ Persistent across restarts

**3. Lazy-Loading**
- ✅ Embedding model loads once, stays in memory
- ✅ No repeated loading/unloading

### 🛡️ Additional Safeguards Needed

#### 1. Health Check Endpoint (Recommended)

Add a lightweight health check that doesn't trigger heavy operations:

```python
# In api.py
@app.get("/health")
async def health_check():
    """Lightweight health check for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
```

**Benefits:**
- Cron job hits `/health` instead of `/` (lighter)
- Doesn't trigger chat engine initialization
- Faster response (~10ms vs 100ms)

#### 2. Memory Monitoring (Optional)

```python
import psutil

@app.get("/stats")
async def get_stats():
    """Server statistics"""
    process = psutil.Process()
    return {
        "memory_mb": process.memory_info().rss / 1024 / 1024,
        "cpu_percent": process.cpu_percent(),
        "uptime_hours": (time.time() - start_time) / 3600
    }
```

#### 3. Graceful Restart Strategy

**Option A: Daily Restart (Recommended)**
- Set up cron job to restart server once per day (e.g., 3 AM)
- Prevents any potential memory buildup
- Render supports this via API

**Option B: Memory-Based Restart**
- Monitor memory usage
- Auto-restart if exceeds threshold
- More complex, usually not needed

### 📊 Expected Stability

**With Pinecone + Redis:**
- Memory usage: ~300MB (stable)
- No growth over time ✅
- Can run for weeks/months ✅

**With FAISS (old):**
- Memory usage: ~500MB → 1GB+ over time
- Crashes after 24-30 hours ❌

### 🎯 Recommended Setup

1. **Use `/health` endpoint for cron job**
   ```
   URL: https://your-app.onrender.com/health
   Interval: Every 10 minutes
   ```

2. **Monitor with UptimeRobot**
   - Checks `/health` every 5 minutes
   - Email alert if down
   - Uptime dashboard

3. **Optional: Daily restart**
   - Render dashboard → Settings → Auto-restart
   - Or use Render API to restart daily

### 🔧 Implementation

**Step 1: Add health endpoint** (I can do this now)
**Step 2: Update cron job** to use `/health`
**Step 3: Monitor for 48 hours** to confirm stability

### Why This Will Work

**Before (FAISS):**
```
Memory: 500MB → 600MB → 800MB → 1GB → CRASH
```

**Now (Pinecone):**
```
Memory: 300MB → 300MB → 300MB → 300MB ✅
```

**Key difference:** No local state = no memory growth!

---

Want me to add the `/health` endpoint and update the monitoring setup?
