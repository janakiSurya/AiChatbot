# Keep-Alive Setup for Render

Your Render service goes inactive after 15 minutes of no requests. Here are solutions to prevent cold starts:

## Option 1: UptimeRobot (Recommended - Free & Easy)

1. **Sign up**: Go to https://uptimerobot.com (free account)
2. **Add Monitor**:
   - Monitor Type: HTTP(s)
   - Friendly Name: `Alfred AI Keep-Alive`
   - URL: `https://your-app.onrender.com/`
   - Monitoring Interval: **5 minutes** (free tier)
3. **Save** - Done! ✅

**Result**: Your service will never go inactive

---

## Option 2: Cron-Job.org (Alternative)

1. **Sign up**: Go to https://cron-job.org (free account)
2. **Create Cronjob**:
   - Title: `Alfred AI Ping`
   - URL: `https://your-app.onrender.com/`
   - Schedule: Every 10 minutes
3. **Save** - Done! ✅

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
        run: curl https://your-app.onrender.com/
```

---

## Comparison

| Service | Interval | Setup Time | Best For |
|---------|----------|------------|----------|
| **UptimeRobot** | 5 min | 2 min | Most users (recommended) |
| **Cron-Job.org** | 10 min | 2 min | Alternative to UptimeRobot |
| **GitHub Actions** | 10 min | 5 min | If you use GitHub |

---

## Why This Works

- Render spins down after **15 minutes** of inactivity
- Pinging every **5-10 minutes** keeps it active
- Your cold start time (8.72s) becomes **0s** ✅
- All queries respond in **0.21s - 5s** (no startup delay)

---

## Recommended: UptimeRobot

**Pros:**
- ✅ Completely free
- ✅ 5-minute interval (better than 10)
- ✅ Email alerts if service goes down
- ✅ Dashboard to monitor uptime
- ✅ No code changes needed

**Setup**: Literally 2 minutes!

---

## After Setup

**Performance:**
- Cold start: **0s** (prevented)
- Cache hits: **0.21s** 🔥
- Cache misses: **2-5s** (LLM generation)
- Uptime: **99.9%** ✅

Your AI assistant will be **always ready** to respond instantly!
