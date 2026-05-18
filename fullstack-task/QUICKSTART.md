# 🚀 Quick Start Guide

Get your full-stack app running in 5 minutes!

## ⚡ 5-Minute Setup

### 1️⃣ Open Terminal

```bash
cd fullstack-task
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Start Backend (Terminal 1)

```bash
python -m uvicorn backend.main:app --reload
```

Visit: **http://localhost:8000/docs**

### 5️⃣ Open Frontend (Terminal 2)

```bash
# Option A: Open file directly
start frontend/index.html  # Windows
open frontend/index.html   # Mac

# Option B: Use Python server
python -m http.server 8001 -d frontend
# Visit: http://localhost:8001
```

**Done!** 🎉 You now have:
- ✅ Backend API running on port 8000
- ✅ Frontend app running on port 8001 or locally
- ✅ SQLite database (auto-created)
- ✅ Interactive API docs at http://localhost:8000/docs

---

## 📚 What to Learn First

### Day 1: Understand the Architecture
1. Read [README.md](README.md) - Get overview
2. Explore folder structure
3. Test API endpoints at http://localhost:8000/docs
4. Create a task through the frontend
5. Check the database file (`tasks.db`)

### Day 2: Learn the Backend
1. Read [LEARNING_GUIDE.md](LEARNING_GUIDE.md) - Core concepts
2. Study [backend/models.py](backend/models.py) - Database models
3. Study [backend/schemas.py](backend/schemas.py) - Data validation
4. Study [backend/crud.py](backend/crud.py) - Database operations
5. Test endpoints with Postman (see [API_DOCUMENTATION.md](API_DOCUMENTATION.md))

### Day 3: Learn the Frontend
1. Study [frontend/script.js](frontend/script.js) - JavaScript API integration
2. Study [frontend/styles.css](frontend/styles.css) - Responsive design
3. Modify HTML/CSS and see changes
4. Use browser DevTools (F12) to debug
5. Add a new feature to the UI

### Day 4: Professional Development
1. Read [DEVELOPER_WORKFLOW.md](DEVELOPER_WORKFLOW.md) - Best practices
2. Set up Git/GitHub ([GITHUB_SETUP.md](GITHUB_SETUP.md))
3. Practice debugging with browser DevTools
4. Write clean, documented code

### Day 5+: Deployment & Expansion
1. Deploy with ngrok ([DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md))
2. Add new features (due dates, priorities, tags)
3. Implement user authentication
4. Deploy to production

---

## 🎯 Key Features to Understand

### ✅ CRUD Operations
```
Create → POST /api/tasks (create new task)
Read   → GET /api/tasks (fetch all tasks)
Update → PUT /api/tasks/1 (update task with id 1)
Delete → DELETE /api/tasks/1 (delete task with id 1)
```

### ✅ Database
- **Technology**: SQLite (file-based database)
- **Location**: `tasks.db` (auto-created in project root)
- **Tables**: `tasks` table with fields: id, title, description, completed, created_at, updated_at

### ✅ API
- **Framework**: FastAPI
- **Documentation**: http://localhost:8000/docs (auto-generated)
- **Response Format**: JSON
- **Error Handling**: Descriptive error messages

### ✅ Frontend
- **Technology**: HTML/CSS/JavaScript (no frameworks!)
- **API Integration**: Fetch API for HTTP requests
- **State Management**: Simple in-memory state
- **Responsiveness**: Works on desktop, tablet, mobile

---

## 🔧 Common Commands

```bash
# Start backend
python -m uvicorn backend.main:app --reload

# Start frontend (Python simple server)
python -m http.server 8001 -d frontend

# Test API with curl
curl http://localhost:8000/api/tasks

# Create task with curl
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"New Task","description":"Test"}'

# Delete database and start fresh
rm tasks.db

# View Git log
git log --oneline

# Push to GitHub
git push origin main
```

---

## 🐛 Debugging Tips

### If Backend Won't Start
```
❌ Port 8000 already in use?
→ Kill process: netstat -ano | findstr :8000 (Windows)
→ Or use different port: python -m uvicorn backend.main:app --port 8001

❌ Module not found error?
→ Check virtual environment is activated
→ Reinstall: pip install -r requirements.txt

❌ Database error?
→ Delete tasks.db and restart server
```

### If Frontend Not Working
```
❌ Tasks not loading?
→ Open DevTools (F12) → Console tab
→ Check for error messages
→ Verify backend is running

❌ API call failing?
→ Open DevTools → Network tab
→ Click the API request
→ Check status code and response

❌ Page looks broken?
→ Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
```

### If CORS Error Occurs
```
❌ "CORS error" in console?
→ Make sure backend is running
→ Check CORS configuration in backend/main.py
→ Frontend URL must be in allowed_origins
```

---

## 📊 Testing the API

### Using Browser

1. Visit: http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Click "Execute"
4. See response below

### Using curl

```bash
# Get all tasks
curl http://localhost:8000/api/tasks

# Create task
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn FastAPI"}'

# Update task
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

# Delete task
curl -X DELETE http://localhost:8000/api/tasks/1
```

### Using Postman

1. Download [Postman](https://www.postman.com/downloads/)
2. Create new Collection
3. Add requests:
   - GET http://localhost:8000/api/tasks
   - POST http://localhost:8000/api/tasks (with JSON body)
   - PUT http://localhost:8000/api/tasks/1
   - DELETE http://localhost:8000/api/tasks/1
4. Test each endpoint

---

## 🌐 Going Public with ngrok

Share your app with the world (temporarily):

```bash
# 1. Install ngrok
# Download from ngrok.com or: choco install ngrok (Windows)

# 2. Start ngrok (while backend is running)
ngrok http 8000

# 3. Copy public URL from output
# Forwarding   https://abcd1234.ngrok.io -> http://localhost:8000

# 4. Update frontend
# Change: const API_BASE_URL = 'https://abcd1234.ngrok.io'

# 5. Share URL with friends!
# https://abcd1234.ngrok.io/docs
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## 📈 Next Features to Build

### Easy (1-2 hours)
- [ ] Add task priority field (1-5)
- [ ] Add due date field
- [ ] Implement sorting (newest first, oldest first)
- [ ] Add search functionality
- [ ] Change colors/theme

### Medium (2-4 hours)
- [ ] Add task categories/tags
- [ ] Implement task history/timestamps
- [ ] Add bulk operations (delete multiple)
- [ ] Export tasks to CSV
- [ ] Dark mode toggle

### Hard (4+ hours)
- [ ] User authentication (login/signup)
- [ ] Multiple users with separate tasks
- [ ] Real-time updates (WebSockets)
- [ ] Task sharing/collaboration
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced filtering and search

---

## 📖 Learning Path Summary

```
Week 1: Basics
├─ Understand REST API concepts
├─ Learn CRUD operations
├─ Explore database schema
└─ Test with Postman

Week 2: Deep Dive
├─ Study FastAPI framework
├─ Learn SQLAlchemy ORM
├─ Understand Pydantic validation
└─ Debug with DevTools

Week 3: Frontend Integration
├─ Learn Fetch API
├─ Understand async/await
├─ Build responsive UI
└─ Handle API responses

Week 4: Professional Development
├─ Learn Git/GitHub workflow
├─ Implement error handling
├─ Write clean code
└─ Deploy to production

Weeks 5+: Expand
├─ Add new features
├─ Implement authentication
├─ Optimize performance
└─ Scale architecture
```

---

## 📚 Essential Resources

### Official Documentation
- [FastAPI](https://fastapi.tiangolo.com/) - Framework
- [SQLAlchemy](https://docs.sqlalchemy.org/) - Database ORM
- [MDN Web Docs](https://developer.mozilla.org/) - Web standards
- [Git Docs](https://git-scm.com/doc) - Version control

### Video Learning (YouTube)
- "FastAPI Tutorial" - Search on YouTube
- "SQLAlchemy Tutorial" - Complete guides available
- "Web Development for Beginners" - Comprehensive courses

### Interactive Learning
- [w3schools.com](https://www.w3schools.com/) - HTML/CSS/JavaScript
- [codecademy.com](https://www.codecademy.com/) - Courses
- [freecodecamp.org](https://www.freecodecamp.org/) - Video courses

---

## 🎯 Success Checklist

- [ ] Backend running without errors
- [ ] Frontend displaying tasks
- [ ] Can create new task
- [ ] Can view tasks
- [ ] Can update task
- [ ] Can delete task
- [ ] Can filter tasks by status
- [ ] Responsive on mobile
- [ ] No console errors
- [ ] API documentation visible
- [ ] Code is commented
- [ ] Ready to deploy with ngrok

---

## ❓ Getting Unstuck

### Stuck on Something?

1. **Check the error message** - Read it carefully, it often explains the issue
2. **Google the error** - "FastAPI module not found" → google it
3. **Check DevTools** (F12) - Browser errors are logged there
4. **Check terminal output** - Backend errors appear in the terminal
5. **Read the code comments** - Each file has detailed explanations
6. **Check the docs** - Read LEARNING_GUIDE.md, API_DOCUMENTATION.md
7. **Try a simple test** - Narrow down the issue
8. **Ask for help** - Share error message and what you were trying to do

### Useful Commands

```bash
# Restart backend (Ctrl+C to stop, then run again)
python -m uvicorn backend.main:app --reload

# Check Python version
python --version  # Should be 3.8+

# List installed packages
pip list

# Reset database
rm tasks.db

# View git status
git status

# View git log
git log --oneline
```

---

## 🎓 What You're Learning

### Concepts
- ✅ Client-server architecture
- ✅ REST API design
- ✅ HTTP methods and status codes
- ✅ Request/response cycle
- ✅ Database design (schema, relationships)
- ✅ ORM (Object-Relational Mapping)
- ✅ Data validation
- ✅ Frontend-backend communication
- ✅ Responsive web design
- ✅ Version control (Git)
- ✅ API documentation
- ✅ Deployment

### Technologies
- ✅ Python, FastAPI, SQLAlchemy
- ✅ SQLite, SQL
- ✅ HTML, CSS, JavaScript
- ✅ Fetch API, async/await
- ✅ Git, GitHub
- ✅ Postman, DevTools
- ✅ ngrok, deployment

### Skills
- ✅ Full-stack development
- ✅ API design and building
- ✅ Database design and management
- ✅ Debugging and troubleshooting
- ✅ Reading and writing code
- ✅ Using version control
- ✅ Professional coding practices
- ✅ Collaboration and code review

---

## 🚀 You're Ready!

Everything you need is set up. Time to build, learn, and grow as a developer!

**Next Step**: Start the server and explore the app.

**Questions?** Check the relevant documentation file:
- Architecture questions → [README.md](README.md)
- Concept questions → [LEARNING_GUIDE.md](LEARNING_GUIDE.md)
- API questions → [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- Development questions → [DEVELOPER_WORKFLOW.md](DEVELOPER_WORKFLOW.md)
- GitHub questions → [GITHUB_SETUP.md](GITHUB_SETUP.md)
- Deployment questions → [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**Let's code!** 💻
