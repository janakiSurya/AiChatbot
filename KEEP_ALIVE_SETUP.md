# Keep-Alive Setup for Render

Your Render service goes inactive after 15 minutes of no requests. Here are solutions to prevent cold starts:

## ⚠️ Common Issue: Cron Job Goes Inactive

**Problem**: Your cron job shows "Inactive" or "Failed (HTTP error)"

**Root Cause**: Most cron services have a **5-second timeout**, but cold starts take **5-10 seconds**. The cron job fails, marks itself inactive, and stops trying.

**Solution**: Use UptimeRobot (30-second timeout) instead of cron-job.org

---

## Option 1: UptimeRobot (RECOMMENDED ⭐)

**Why UptimeRobot is best**:
- ✅ **30-second timeout** (handles cold starts)
- ✅ Auto-retries on failure
- ✅ Won't go "inactive" on you
- ✅ 5-minute interval (prevents spin-down)
- ✅ Email alerts if server actually down
- ✅ Uptime dashboard

**Setup** (2 minutes):

1. **Sign up**: Go to https://uptimerobot.com (free account)
2. **Add Monitor**:
   - Monitor Type: HTTP(s)
   - Friendly Name: `Alfred AI Keep-Alive`
   - URL: `https://your-app.onrender.com/ping` (ultra-fast)
   - Monitoring Interval: **5 minutes**
   - Monitor Timeout: **30 seconds** ⬅️ Important!
3. **Save** - Done! ✅

**Result**: Your service will **never** go inactive

---

## Option 2: Cron-Job.org (If You Must)

⚠️ **Warning**: If using cron-job.org, you MUST:
1. Set timeout to **30 seconds** (if available)
2. Use `/ping` endpoint (faster than `/health`)
3. Manually reactivate if it goes inactive

**Setup**:
1. **Sign up**: Go to https://cron-job.org
2. **Create Cronjob**:
   - Title: `Alfred AI Ping`
   - URL: `https://your-app.onrender.com/ping`
   - Schedule: Every 10 minutes
   - Timeout: 30 seconds (if available)
3. **Save**

⚠️ If it goes "inactive": Log in and manually reactivate it

---

## Option 3: GitHub Actions (For GitHub Users)

Create `.github/workflows/keep-alive.yml`:

```yaml
name: Keep Alive

on:
  schedule:
    - cron: '*/10 * * * *'  # Every 10 minutes

jobs:
  keep-alive:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Service
        run: curl -f https://your-app.onrender.com/ping || exit 0
        timeout-minutes: 1
```

---

## Endpoint Comparison

Your API has two endpoints for keep-alive:

| Endpoint | Speed | Use For |
|----------|-------|---------|
| `/ping` | ~50ms | Keep-alive (recommended) ⭐ |
| `/health` | ~100ms | Monitoring services |
| `/stats` | ~200ms | Performance monitoring |

**Recommendation**: Use `/ping` for UptimeRobot/cron jobs

---

## Comparison

| Service | Timeout | Interval | Auto-Reactivate | Best For |
|---------|---------|----------|-----------------|----------|
| **UptimeRobot** ⭐ | 30s | 5 min | ✅ Yes | Everyone (best choice) |
| **Cron-Job.org** | 5-10s | 10 min | ❌ No | Not recommended |
| **GitHub Actions** | 6 min | 10 min | ✅ Yes | GitHub users |

---

## Why This Works

- Render spins down after **15 minutes** of inactivity
- Pinging every **5 minutes** keeps it active
- **30-second timeout** handles cold starts gracefully
- Your cold start time (5-10s) becomes effectively **0s** ✅

---

## Troubleshooting

### My cron job went "Inactive"

**Cause**: Timeout too short (usually 5 seconds)
**Fix**: Switch to UptimeRobot (30-second timeout)

### Getting "HTTP error (602 ms)"

**Cause**: Server cold starting (takes 5-10s), cron times out
**Fix**: Use UptimeRobot with 30-second timeout

### Want even faster response?

**Temporary**: Use `/ping` endpoint (fastest)
**Long-term**: Implement Phase 1 fixes from the implementation plan to reduce cold start to ~2 seconds

---

## After Setup

**Performance:**
- Cold start: **0s** (prevented by 5-min pings)
- Subsequent requests: **50-200ms** 🔥
- Cache hits: **0.21s** (with semantic cache)
- Cache misses: **2-5s** (LLM generation)
- Uptime: **99.9%** ✅

Your AI assistant will be **always ready** to respond instantly!
