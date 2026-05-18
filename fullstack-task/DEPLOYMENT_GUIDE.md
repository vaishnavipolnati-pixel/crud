# Deployment Guide: Making Your API Public with ngrok

## 🌐 What is ngrok?

**ngrok** creates a public URL that forwards to your local server. Perfect for:
- Testing webhooks
- Sharing development version
- Mobile testing
- Team collaboration
- Learning deployment

```
https://abcd1234.ngrok.io  ──────────────────→  http://localhost:8000
(Public URL)              (Your local machine)
```

---

## 🚀 Step 1: Install ngrok

### Option A: Download from Website

1. Visit [ngrok.com](https://ngrok.com/download)
2. Select Windows / Mac / Linux
3. Download the executable
4. Extract to a folder (e.g., `C:\ngrok` on Windows)

### Option B: Using Package Manager

**Windows (Chocolatey):**
```bash
choco install ngrok
```

**Mac (Homebrew):**
```bash
brew install ngrok
```

**Linux:**
```bash
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip
unzip ngrok-v3-stable-linux-amd64.zip
```

### Verify Installation

```bash
ngrok --version
# Output: ngrok version 3.x.x
```

---

## 🔐 Step 2: Create Free Account

1. Go to [ngrok.com](https://ngrok.com)
2. Click "Sign Up" (free tier available)
3. Create account with email
4. Verify email
5. Go to [dashboard](https://dashboard.ngrok.com/auth)
6. Copy your **Authtoken**

### Authenticate ngrok

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE

# Verify (should show no errors)
ngrok --help
```

---

## ▶️ Step 3: Start Your Backend Server

Open a terminal and start your FastAPI server:

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Start server on port 8000
python -m uvicorn backend.main:app --reload

# Output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

**Keep this terminal open!**

---

## 🌐 Step 4: Start ngrok

**Open a NEW terminal** and run:

```bash
# Forward port 8000 to public URL
ngrok http 8000

# Output:
# Session Status                online
# Account                       your-email@example.com
# Version                       3.0.0
# Region                        us (United States)
# Forwarding                    https://abcd1234.ngrok.io -> http://localhost:8000
# Connections                   ttl    opn    rt1    rt5    p50    p90
#                               0      0      0.00   0.00   0.00   0.00
```

**Your public URL**: `https://abcd1234.ngrok.io`

**Keep this terminal open!**

---

## 🔗 Step 5: Test Public URL

### In Browser

Visit your ngrok URL:
```
https://abcd1234.ngrok.io/docs
```

You should see your API documentation!

### Test API Endpoint

```bash
curl https://abcd1234.ngrok.io/health

# Response:
# {"status":"healthy","message":"API is running"}
```

---

## 🎨 Step 6: Update Frontend

### Option A: Update JavaScript Locally

Edit `frontend/script.js`:

```javascript
// BEFORE (local):
const API_BASE_URL = 'http://localhost:8000';

// AFTER (public):
const API_BASE_URL = 'https://abcd1234.ngrok.io';
```

### Option B: Use Environment-Aware URLs

```javascript
// Auto-detect API URL
const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000'
  : 'https://abcd1234.ngrok.io';
```

### Test Frontend

1. Refresh your frontend in browser
2. Create a task
3. Verify it works
4. Check Network tab in DevTools

---

## 📱 Step 7: Share Public URL

Your ngrok URL is now public! Share it:

```
🔗 Frontend: https://your-domain.com/frontend/
🔗 API Docs: https://abcd1234.ngrok.io/docs
🔗 API Health: https://abcd1234.ngrok.io/health
```

### Mobile Testing

From your mobile device:

1. Open URL on mobile: `https://abcd1234.ngrok.io/docs`
2. Test API endpoints
3. Or update mobile frontend to use ngrok URL

---

## ⚙️ Advanced ngrok Usage

### Custom Subdomain (Paid)

```bash
ngrok http --domain=your-subdomain.ngrok.io 8000
```

### Custom Region

```bash
# List regions: ngrok http --help
ngrok http --region=eu 8000  # EU region
ngrok http --region=au 8000  # Australia
```

### Multiple Ports

```bash
# Terminal 1
ngrok http 8000

# Terminal 2
ngrok http 8001
```

### Configure File

Create `~/.ngrok2/ngrok.yml`:

```yaml
authtoken: YOUR_AUTH_TOKEN
api_key: YOUR_API_KEY
region: us
tunnels:
  backend:
    proto: http
    addr: 8000
    domain: my-custom-domain.ngrok.io
```

Then use:
```bash
ngrok start backend
```

---

## 🔍 Monitoring Requests

### Web Inspection Interface

1. Go to http://localhost:4040
2. See all requests/responses in real-time
3. Useful for debugging API issues

### Replay Requests

1. In http://localhost:4040
2. Click a request
3. Click "Replay"
4. Modify request (optional)
5. Click "Send"

---

## 🐛 Troubleshooting ngrok

### Issue: "Tunnel session failed"
```
Solutions:
- Check internet connection
- Verify authtoken is correct: ngrok config
- ngrok server might be down
- Try different region: ngrok http --region=eu 8000
```

### Issue: "Address already in use"
```bash
# Port 8000 is busy
# Kill process:
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :8000
kill -9 <PID>

# Or use different port:
ngrok http 8001
```

### Issue: "CORS error" from public URL
```python
# Backend CORS needs to include ngrok domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:3000",
        "https://abcd1234.ngrok.io"  # Add ngrok URL
    ]
)
```

### Issue: URL changes each time

Use **paid plan** for persistent URL:
- Go to ngrok dashboard
- Reserve domain
- Use same URL every time

---

## 💾 Save Configuration

### Batch File (Windows)

Create `start-dev.bat`:

```batch
@echo off
echo Starting backend server...
start cmd /k "venv\Scripts\activate && python -m uvicorn backend.main:app --reload"

timeout /t 2

echo Starting ngrok tunnel...
start cmd /k "ngrok http 8000"

echo Backend: http://localhost:8000
echo Public:  https://YOUR_NGROK_URL.ngrok.io
```

Then just run: `start-dev.bat`

### Bash Script (Mac/Linux)

Create `start-dev.sh`:

```bash
#!/bin/bash

echo "Starting backend server..."
source venv/bin/activate
python -m uvicorn backend.main:app --reload &

sleep 2

echo "Starting ngrok tunnel..."
ngrok http 8000
```

Then run:
```bash
chmod +x start-dev.sh
./start-dev.sh
```

---

## 🔐 Security with ngrok

### Be Careful With Sensitive Data

⚠️ **Important:**
- ✅ Share API docs with team
- ❌ Don't expose production credentials
- ❌ Don't expose database directly
- ✅ Use authentication for sensitive endpoints
- ✅ Rate limit public endpoints

### Add Basic Authentication

```python
from fastapi.security import HTTPBasic, HTTPBearer

security = HTTPBasic()

@app.get("/api/admin")
def admin_only(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin":
        raise HTTPException(status_code=403)
    return {"message": "Welcome admin"}
```

---

## 📈 Production Deployment

ngrok is **NOT for production**. For production, use:

### Cloud Platforms

1. **Heroku** (Simple)
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

2. **Railway.app** (Modern)
   - Connect GitHub repo
   - Auto-deploy on push
   - Free tier available

3. **PythonAnywhere** (Python-focused)
   - Web-based IDE
   - Auto-scaling
   - HTTPS built-in

4. **AWS/Google Cloud/Azure** (Enterprise)
   - More complex
   - Highly scalable
   - Pay as you go

### Example: Deploy to Railway

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Initialize
railway init

# 4. Deploy
railway up

# 5. Get URL
railway open
```

---

## 🎯 Development Workflow with ngrok

### Local Development + Public Sharing

```
Your Team
   ↓
GitHub (code)
   ↓
Your Local Machine
   ├─ Backend: http://localhost:8000
   ├─ Frontend: http://localhost:3000
   └─ ngrok: https://abcd1234.ngrok.io (public)
```

### Typical Session

```bash
# Terminal 1: Backend
python -m uvicorn backend.main:app --reload

# Terminal 2: ngrok
ngrok http 8000

# Terminal 3: Frontend (optional, if not using Live Server)
python -m http.server 8001 -d frontend

# Browser 1: Local development
http://localhost:3000

# Browser 2: Public testing
https://abcd1234.ngrok.io/docs

# Share with team
Send ngrok URL in Slack/Discord
```

---

## 📚 Resources

- [ngrok Documentation](https://ngrok.com/docs)
- [ngrok Agent CLI Reference](https://ngrok.com/docs/agent/cli/)
- [ngrok Tutorials](https://ngrok.com/docs/guides/)
- [ngrok Pricing](https://ngrok.com/pricing)

---

## ✅ Checklist

- [ ] Installed ngrok
- [ ] Created free ngrok account
- [ ] Added authtoken to ngrok
- [ ] Started backend server on port 8000
- [ ] Started ngrok tunnel
- [ ] Tested public URL in browser
- [ ] Tested API endpoints with curl
- [ ] Updated frontend to use ngrok URL
- [ ] Shared URL with team
- [ ] Tested from mobile device
- [ ] Checked DevTools Network tab
- [ ] Saved your ngrok URL somewhere

---

**Your API is now public! 🚀**

Share it with your team, test it across devices, and learn how applications are deployed to the internet!
