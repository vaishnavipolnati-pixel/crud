# Developer Workflow & Professional Practices

## 📋 Daily Development Checklist

### Morning Setup
- [ ] Activate virtual environment
- [ ] Start backend server
- [ ] Open frontend in browser
- [ ] Check for errors in console/terminal
- [ ] Pull latest changes from Git

### During Development
- [ ] Make small, focused changes
- [ ] Test each change immediately
- [ ] Check console for errors
- [ ] Keep DevTools open
- [ ] Document as you code

### Before Committing
- [ ] Test complete user workflow
- [ ] Check for console errors
- [ ] Verify database changes
- [ ] Remove debug code
- [ ] Update documentation

### End of Day
- [ ] Commit working code
- [ ] Push to GitHub
- [ ] Document blockers
- [ ] Plan next steps

---

## 🔧 Git Workflow

### Initial Setup

```bash
# Initialize repository
cd fullstack-task
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create .gitignore (already done)
# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Full-stack task manager application"

# Connect to GitHub
git remote add origin https://github.com/your-username/fullstack-task.git
git branch -M main
git push -u origin main
```

### Feature Development Workflow

```bash
# Create feature branch
git checkout -b feature/add-task-priority

# Make changes and test
# ... edit files ...

# Stage changes
git add backend/models.py backend/schemas.py

# Commit with descriptive message
git commit -m "Add task priority field to models and schemas"

# Push to GitHub
git push origin feature/add-task-priority

# Create Pull Request on GitHub for code review
# After review, merge to main:
git checkout main
git pull
git merge feature/add-task-priority
git push

# Delete feature branch
git branch -d feature/add-task-priority
git push origin --delete feature/add-task-priority
```

### Commit Message Guidelines

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring
- `docs`: Documentation
- `style`: Formatting
- `test`: Adding tests
- `chore`: Build, dependencies

**Examples:**
```
✅ Good:
feat(tasks): add task priority field
- Adds priority to Task model
- Updates API schema
- Implements priority sorting in GET endpoint

fix(database): handle concurrent task creation
refactor(frontend): simplify event listener setup
docs: add API authentication documentation

❌ Bad:
updated stuff
fix
changes
```

---

## 🐛 Debugging Workflow

### Step 1: Identify the Problem

```
Q: When did it start happening?
Q: What were you doing?
Q: What's the expected behavior?
Q: What's the actual behavior?
Q: Is it reproducible?
```

### Step 2: Locate the Error

**Backend Error:**
```bash
# Check terminal output where server runs
# Look for:
# - Traceback (shows line number)
# - Error message
# - Stack trace (shows function calls)
```

**Frontend Error:**
```
Press F12 → Console tab
Look for:
- Red error messages
- Line number and file
- Stack trace
```

### Step 3: Reproduce the Bug

```
1. Clear state (refresh page, restart server)
2. Follow exact steps to reproduce
3. Note any variations in behavior
4. Try with different data
5. Check if it's browser-specific
```

### Step 4: Use Debugging Tools

**Browser DevTools:**
```javascript
// Add breakpoint by clicking line number
// Or:
debugger;  // Execution stops here

// Step through code using buttons:
// Step Over: Execute current line
// Step Into: Enter function
// Step Out: Exit function

// View variables in Scope panel
// Use Console to evaluate expressions:
typeof myVariable
myVariable.toString()
```

**Backend Debugging:**
```python
# Add logging
import logging
logger = logging.getLogger(__name__)
logger.info(f"Task created: {task}")

# Or use breakpoint
def create_task(task_data):
    breakpoint()  # Execution stops here
    # Use pdb commands:
    # n (next), c (continue), l (list), p (print)
```

### Step 5: Fix & Test

```
1. Understand the root cause (not just the symptom)
2. Make minimal fix
3. Test the specific issue
4. Test related functionality
5. Check edge cases
```

### Step 6: Document

```python
# Document the fix
def create_task(db: Session, task: TaskCreate) -> Task:
    """
    Create a new task.
    
    BUG FIX (2024-01-15):
    - Issue: Concurrent requests caused duplicate IDs
    - Fix: Added explicit transaction handling
    - Test: Run test_concurrent_creation()
    """
```

### Common Debugging Scenarios

**Scenario: API returns 404**
```
1. Check URL is correct (typo?)
2. Verify task ID exists in database
3. Check request method (GET not POST?)
4. Add logging to backend route:
   logger.info(f"Received request: {request.url}")
```

**Scenario: Frontend not updating after API call**
```
1. Check Network tab: Was request sent?
2. Check response: Did API return data?
3. Check console: Any JavaScript errors?
4. Verify DOM element IDs match
5. Add console.log before DOM update:
   console.log("Before update:", document.getElementById('tasks'))
```

**Scenario: Database shows wrong data**
```
1. Check if server restarted (data reverted?)
2. Verify correct database file (tasks.db)
3. Enable SQL echo in database.py to see queries:
   engine = create_engine(DATABASE_URL, echo=True)
4. Check if transaction was committed:
   db.commit()
```

---

## ✅ Testing Strategy

### Unit Testing Example

```python
# tests/test_crud.py
from backend.crud import create_task, get_task
from backend.schemas import TaskCreate

def test_create_task(db):
    """Test task creation"""
    task_data = TaskCreate(title="Test Task")
    task = create_task(db, task_data)
    
    assert task.id is not None
    assert task.title == "Test Task"
    assert task.completed == False

def test_get_nonexistent_task(db):
    """Test getting non-existent task"""
    task = get_task(db, 9999)
    assert task is None

# Run tests
pytest tests/ -v
```

### Integration Testing Example

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_and_get_task():
    """Test creating task then retrieving it"""
    # Create
    response = client.post("/api/tasks", json={
        "title": "Test Task"
    })
    assert response.status_code == 201
    task_id = response.json()["id"]
    
    # Get
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

# Run tests
pytest tests/test_api.py -v
```

### Frontend Testing

```javascript
// Manual testing checklist
☐ Create task
☐ View task
☐ Update task title
☐ Mark as complete
☐ Delete task
☐ Filter by status
☐ Test on mobile
☐ Test with 100 tasks (performance)
☐ Test with no tasks (empty state)
☐ Test with special characters in title
☐ Test rapid clicking
☐ Test with API offline
```

---

## 📊 Code Review Checklist

Before merging code, check:

### Functionality
- [ ] Feature works as intended
- [ ] All edge cases handled
- [ ] Error messages are clear
- [ ] No debug code left

### Code Quality
- [ ] Variable names are clear
- [ ] Functions are focused (single responsibility)
- [ ] No code duplication
- [ ] Follows project style guide

### Documentation
- [ ] Functions have docstrings
- [ ] Complex logic is commented
- [ ] README updated if needed
- [ ] API changes documented

### Testing
- [ ] Tested locally
- [ ] Tested with edge cases
- [ ] No console errors
- [ ] Database queries checked

### Performance
- [ ] No unnecessary API calls
- [ ] Database queries are efficient
- [ ] Large lists paginated
- [ ] Images optimized

---

## 🚀 Performance Optimization

### Database
```python
# ❌ Slow: N+1 query problem
for task in tasks:
    print(task.related_data)  # Queries DB for each task

# ✅ Fast: Eager loading
tasks = db.query(Task).options(joinedload(Task.related)).all()

# ✅ Indexed columns
db.query(Task).filter(Task.completed == True).all()  # Fast (indexed)
```

### Frontend
```javascript
// ❌ Slow: DOM operations
for (let i = 0; i < 1000; i++) {
  container.innerHTML += `<div>${i}</div>`;  // Reflows 1000 times
}

// ✅ Fast: Batch DOM
let html = '';
for (let i = 0; i < 1000; i++) {
  html += `<div>${i}</div>`;
}
container.innerHTML = html;  // Reflow once

// ✅ Debounce input
function debounce(func, wait) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

input.addEventListener('input', debounce(handleSearch, 500));
```

---

## 🔐 Security Best Practices

### Backend
```python
# ❌ Don't: Return sensitive data
@app.get("/api/user")
def get_user(user_id: int):
    return {"password": user.password}  # ❌ Never!

# ✅ Do: Use response model to exclude fields
class UserResponse(BaseModel):
    id: int
    name: str
    # password excluded

@app.get("/api/user", response_model=UserResponse)
def get_user(user_id: int):
    return user

# ❌ Don't: Trust user input
query = f"SELECT * FROM tasks WHERE title = '{user_input}'"
db.execute(query)  # SQL injection!

# ✅ Do: Use parameterized queries
db.query(Task).filter(Task.title == user_input).all()  # Safe
```

### Frontend
```javascript
// ❌ Don't: Insert HTML directly
element.innerHTML = userInput;

// ✅ Do: Insert as text
element.textContent = userInput;

// ✅ Or escape HTML
function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}
```

### API
```python
# ✅ Do: Add HTTPS in production
# ✅ Do: Validate all inputs
# ✅ Do: Rate limiting
# ✅ Do: CORS whitelist
# ✅ Do: Sanitize error messages
# ✅ Do: Use environment variables for secrets
```

---

## 📈 Monitoring & Logging

### Backend Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/api/tasks")
def create_task(task: TaskCreate):
    logger.info(f"Creating task: {task.title}")
    try:
        result = crud.create_task(db, task)
        logger.info(f"Task created successfully: {result.id}")
        return result
    except Exception as e:
        logger.error(f"Failed to create task: {e}", exc_info=True)
        raise
```

### Frontend Monitoring

```javascript
// Log important events
console.log("App initialized");
console.log("Tasks loaded:", tasks.length);

// Track errors
window.addEventListener('error', (event) => {
  console.error('Global error:', event.error);
});

// Monitor API performance
const start = performance.now();
const response = await fetch('/api/tasks');
const end = performance.now();
console.log(`API call took ${end - start}ms`);
```

---

## 🎯 Continuous Improvement

### Weekly Review
- [ ] Review code changes
- [ ] Identify performance bottlenecks
- [ ] Collect user feedback
- [ ] Plan next week

### Monthly Review
- [ ] Refactor problematic code
- [ ] Update dependencies
- [ ] Optimize database
- [ ] Security audit

### Code Metrics to Track
- Response time
- Error rate
- Test coverage
- Code complexity
- Technical debt

---

## 💡 Tips & Tricks

### Keyboard Shortcuts

**VS Code**
- `Ctrl+/` (or `Cmd+/`): Toggle comment
- `Ctrl+D`: Select next occurrence
- `Ctrl+Shift+L`: Select all occurrences
- `Alt+Up/Down`: Move line up/down
- `Ctrl+K Ctrl+F`: Format document

**Browser DevTools**
- `F12`: Open DevTools
- `Ctrl+Shift+J`: Open Console
- `Ctrl+Shift+C`: Select element
- `Ctrl+Shift+E`: Network requests

### Debugging Productivity

```javascript
// Use console groups
console.group('Task Creation');
console.log('Validating...');
console.log('Sending request...');
console.log('Response received');
console.groupEnd();

// Use console table
console.table(tasks);

// Use console.time for performance
console.time('fetchTasks');
const tasks = await fetch('/api/tasks').then(r => r.json());
console.timeEnd('fetchTasks');

// Use $$() to query DOM in console
$$('. task-item')  // Get all task items
```

---

## 🎓 Learning Resources

**Recommended Reading:**
- Clean Code by Robert C. Martin
- The Pragmatic Programmer by Hunt & Thomas
- Working Effectively with Legacy Code by Michael Feathers

**Online Courses:**
- FastAPI tutorial: https://fastapi.tiangolo.com/tutorial/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Web Development: https://developer.mozilla.org/

---

This workflow will help you write better code, debug faster, and maintain productivity!
