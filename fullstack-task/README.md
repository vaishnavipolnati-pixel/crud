# Task Manager - Full Stack Learning Project

> **A comprehensive learning project to understand full-stack development, REST APIs, database design, and professional development practices.**

## 📚 What You'll Learn

- **Backend Development**: FastAPI, Python, API design
- **Database Design**: SQLite, SQLAlchemy ORM, SQL queries
- **Frontend Development**: HTML, CSS, JavaScript, API integration
- **REST API Architecture**: CRUD operations, HTTP methods, status codes
- **Database Operations**: Models, schemas, migrations
- **Error Handling & Validation**: Pydantic, exception handling
- **Responsive UI Design**: Mobile-first approach, CSS Grid/Flexbox
- **Project Structure**: Professional file organization
- **Debugging & Testing**: Postman, browser DevTools
- **Version Control**: Git, GitHub workflows
- **Deployment**: ngrok for public URLs, production readiness

## 🏗️ Project Architecture

```
fullstack-task/
│
├── backend/                 # FastAPI application
│   ├── main.py             # FastAPI app & routes
│   ├── models.py           # SQLAlchemy ORM models
│   ├── schemas.py          # Pydantic validation schemas
│   ├── database.py         # Database configuration
│   ├── crud.py             # Database operations (CRUD)
│   └── __init__.py
│
├── frontend/               # Web user interface
│   ├── index.html          # Main HTML page
│   ├── styles.css          # Responsive styling
│   └── script.js           # Frontend logic & API calls
│
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**: Download from [python.org](https://www.python.org/)
- **Git**: Download from [git-scm.com](https://git-scm.com/)
- **VS Code**: Download from [code.visualstudio.com](https://code.visualstudio.com/)
- **Postman** (optional): Download from [postman.com](https://www.postman.com/)

### Setup Instructions

#### 1. **Install Python Dependencies**

```bash
# Navigate to project directory
cd fullstack-task

# Create a virtual environment (isolates project dependencies)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

**Why virtual environments?**
- Isolates project dependencies from system Python
- Prevents version conflicts between projects
- Allows different projects to use different package versions

#### 2. **Start the Backend Server**

```bash
# Make sure virtual environment is activated
# Run from the project root directory
python -m uvicorn backend.main:app --reload

# You should see output like:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

**What's happening?**
- `uvicorn`: ASGI server that runs the FastAPI application
- `backend.main:app`: Tells uvicorn where to find the app
- `--reload`: Automatically restarts server when code changes (development only)

**Access the API:**
- API Root: http://localhost:8000
- Swagger UI (Interactive Docs): http://localhost:8000/docs
- ReDoc (Alternative Docs): http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

#### 3. **Open Frontend in Browser**

```bash
# Open frontend/index.html in your web browser
# You can double-click the file or use:
# On Windows:
start frontend/index.html
# On Mac:
open frontend/index.html
# On Linux:
xdg-open frontend/index.html
```

**Or use VS Code's Live Server:**
1. Install "Live Server" extension in VS Code
2. Right-click `frontend/index.html`
3. Click "Open with Live Server"

## 📖 Learning Path

### Phase 1: Understanding the Basics (Week 1)
1. Read [LEARNING_GUIDE.md](LEARNING_GUIDE.md) - Core concepts
2. Explore database structure in [backend/models.py](backend/models.py)
3. Review API endpoints in [backend/main.py](backend/main.py)
4. Understand form handling in [frontend/script.js](frontend/script.js)

### Phase 2: Hands-On Testing (Week 2)
1. Test API endpoints using [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
2. Use Postman to test CRUD operations
3. Use browser DevTools to debug JavaScript
4. Modify frontend to understand real-time API interactions

### Phase 3: Building & Extending (Week 3)
1. Add new fields to tasks (priority, tags, due date)
2. Create new endpoints (search, sorting, filtering)
3. Implement more complex validation
4. Add user authentication

### Phase 4: Deployment & Git (Week 4)
1. Set up GitHub repository
2. Use ngrok for public API access
3. Deploy frontend to GitHub Pages
4. Create CI/CD workflows

## 🔧 Key Technologies Explained

### Backend Stack

**FastAPI**
- Modern Python web framework
- Automatic API documentation (Swagger UI)
- Type hints and automatic validation
- High performance

```python
# Simple example
@app.get("/api/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()
```

**SQLAlchemy**
- ORM (Object-Relational Mapping): Maps Python classes to database tables
- Automatic SQL generation
- Transaction management
- Relationship handling

```python
# Define a table as a Python class
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
```

**Pydantic**
- Data validation and parsing
- Converts raw data to Python objects
- Provides helpful error messages
- Automatically generates API documentation

```python
# Define data structure with validation
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
```

### Frontend Stack

**HTML**
- Semantic structure
- Form elements
- Accessibility attributes

**CSS**
- Flexbox and Grid for layout
- CSS variables for theming
- Media queries for responsiveness
- Smooth transitions and animations

**JavaScript (Vanilla)**
- No frameworks (understand fundamentals)
- Fetch API for HTTP requests
- Async/await for clean asynchronous code
- DOM manipulation
- Event handling

## 📡 REST API Basics

### HTTP Methods

| Method | Purpose | Example |
|--------|---------|---------|
| **GET** | Retrieve data | `GET /api/tasks` - Get all tasks |
| **POST** | Create new data | `POST /api/tasks` - Create a task |
| **PUT** | Update entire resource | `PUT /api/tasks/1` - Update task 1 |
| **PATCH** | Update partial resource | `PATCH /api/tasks/1` - Partial update |
| **DELETE** | Remove data | `DELETE /api/tasks/1` - Delete task 1 |

### Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| **200** | OK - Request successful | GET request returns data |
| **201** | Created - Resource created | POST creates new task |
| **400** | Bad Request - Invalid data | Missing required field |
| **404** | Not Found - Resource doesn't exist | Task ID doesn't exist |
| **500** | Server Error - Backend problem | Database connection failed |

## 🗄️ Database Design

### Tasks Table

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at DATETIME,
    updated_at DATETIME
)
```

### Why These Fields?

- **id**: Unique identifier for each task (Primary Key)
- **title**: What needs to be done (required, indexed for search)
- **description**: Detailed information (optional)
- **completed**: Task status (boolean for efficiency)
- **created_at**: Audit trail - when created (auto-set by database)
- **updated_at**: Track modifications (auto-updated)

## 🛠️ Debugging Guide

### Backend Debugging

**Check server output for errors:**
```bash
# Look for error messages in terminal where server runs
# Common errors:
# - Port already in use (8000)
# - Import errors (missing modules)
# - Database connection issues
```

**Enable SQL logging:**
```python
# In backend/database.py, change echo parameter:
engine = create_engine(DATABASE_URL, echo=True)  # Shows all SQL queries
```

**Use Python debugger:**
```python
# Add breakpoint in code
def get_tasks():
    breakpoint()  # Execution stops here
    tasks = db.query(Task).all()
    return tasks
```

### Frontend Debugging

**Browser Developer Tools (F12):**
1. **Console Tab**: See JavaScript errors
2. **Network Tab**: Monitor API calls, see request/response
3. **Elements Tab**: Inspect HTML structure
4. **Application Tab**: View local storage, cookies

**Common Errors:**
- "CORS error" - Backend not running or not configured
- "404 Not Found" - Wrong API endpoint
- "TypeError: Cannot read property..." - API response is null/undefined

## 📊 Testing with Postman

1. **Create Collection**: "Task Manager API"
2. **Add Requests**:
   - GET /api/tasks
   - POST /api/tasks
   - PUT /api/tasks/:id
   - DELETE /api/tasks/:id

3. **Set Base URL**: Create Postman variable `{{baseUrl}}` = `http://localhost:8000`

4. **Use Environment Variables**: Different URLs for dev/staging/production

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed Postman examples.

## 🌐 Public Deployment with ngrok

**Share your local API with the world:**

```bash
# Install ngrok (download from ngrok.com)
# Run ngrok pointing to your local server
ngrok http 8000

# You'll get output like:
# Forwarding   https://xxxxx.ngrok.io -> http://localhost:8000
```

**Update frontend to use ngrok URL:**
```javascript
const API_BASE_URL = 'https://xxxxx.ngrok.io';
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 📚 Additional Resources

### Official Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [MDN Web Docs](https://developer.mozilla.org/)

### Learning Resources
- [HTTP Status Codes Explained](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [REST API Design Best Practices](https://restfulapi.net/)
- [Database Design Fundamentals](https://www.guru99.com/database-design.html)

### Tools
- [Postman Learning Center](https://learning.postman.com/)
- [Browser DevTools Guide](https://developer.chrome.com/docs/devtools/)
- [Git & GitHub Learning](https://docs.github.com/en/get-started)

## 🐛 Troubleshooting

### "Port 8000 already in use"
```bash
# Find process using port 8000
# On Windows:
netstat -ano | findstr :8000
# Kill the process:
taskkill /PID <PID> /F

# Or use different port:
python -m uvicorn backend.main:app --port 8001 --reload
```

### "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Make sure virtual environment is activated
# Reinstall requirements:
pip install -r requirements.txt
```

### "CORS error" in frontend
```bash
# Make sure backend is running
# Check CORS configuration in backend/main.py
# Verify frontend URL in allow_origins list
```

### Database file is corrupted
```bash
# Delete the database file (data will be lost)
rm tasks.db

# Or if it's the first run:
# Delete venv and recreate:
rm -r venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📝 Project Workflow

### Daily Development Flow

1. **Activate Virtual Environment**
   ```bash
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```

2. **Start Backend Server**
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

3. **Open Frontend**
   - Use Live Server extension in VS Code
   - Or open `frontend/index.html` in browser

4. **Test Changes**
   - Modify code
   - Test in browser
   - Check browser console for errors
   - Monitor terminal for backend errors

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add feature description"
   git push
   ```

### Code Quality Checklist

- [ ] All files have docstrings/comments explaining purpose
- [ ] Function names are descriptive
- [ ] Variable names are clear
- [ ] No hardcoded values (use constants)
- [ ] Error handling implemented
- [ ] User feedback provided (messages, loading states)
- [ ] Responsive design tested on mobile
- [ ] API endpoints tested in Postman
- [ ] Git commit messages are descriptive
- [ ] Code follows PEP 8 (Python) and ESLint (JavaScript) standards

## 🎯 Next Steps

1. **Run the project** and explore the UI
2. **Test API endpoints** in Postman
3. **Read the learning guides** in the docs folder
4. **Modify and experiment** - change colors, add fields, create new endpoints
5. **Deploy** using ngrok
6. **Share** on GitHub

## 📞 Need Help?

- **Check existing errors**: Most issues are documented in console/terminal
- **Read code comments**: Each file has detailed explanations
- **Test incrementally**: Make small changes and test each one
- **Use browser DevTools**: Inspect network requests and responses
- **Refer to official docs**: Links provided in resources section

## 📄 License

This project is provided for educational purposes. Feel free to use, modify, and learn from it!

---

**Happy Learning! 🚀**

Start with the [LEARNING_GUIDE.md](LEARNING_GUIDE.md) for detailed concept explanations.
