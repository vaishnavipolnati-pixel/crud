# Full-Stack Development Learning Guide

## 📚 Core Concepts

### 1. Client-Server Architecture

```
┌──────────────────┐         HTTP         ┌──────────────────┐
│   Frontend       │◄─────REQUEST────────►│   Backend        │
│  (Browser)       │◄─────RESPONSE────────│   (FastAPI)      │
└──────────────────┘                      └──────────────────┘
     HTML/CSS/JS                          Python / Database
```

**How it works:**
1. User clicks button in browser (frontend)
2. JavaScript sends HTTP request to backend API
3. Backend receives request, processes it
4. Backend queries/modifies database
5. Backend sends response back to frontend
6. JavaScript updates HTML with response data
7. User sees updated content

### 2. REST API Principles

**REST = Representational State Transfer**

Core idea: Use HTTP methods to perform actions on resources.

```
Resource: /api/tasks (plural, noun)

GET    /api/tasks      → Read all tasks
GET    /api/tasks/1    → Read specific task
POST   /api/tasks      → Create new task
PUT    /api/tasks/1    → Update entire task
PATCH  /api/tasks/1    → Partially update task
DELETE /api/tasks/1    → Delete task
```

**Why this pattern?**
- Consistent and predictable
- Self-documenting
- Follows web standards
- Scales to large applications

### 3. HTTP Methods (Verbs)

| Method | Meaning | Safe | Idempotent | Use Case |
|--------|---------|------|-----------|----------|
| **GET** | Retrieve | Yes | Yes | Fetch data, no side effects |
| **POST** | Create | No | No | Create new resources |
| **PUT** | Replace | No | Yes | Update entire resource |
| **PATCH** | Modify | No | No | Update part of resource |
| **DELETE** | Remove | No | Yes | Remove resources |

**Safe**: Doesn't modify server state
**Idempotent**: Can be repeated with same result

### 4. Status Codes

Communicate result of HTTP request:

```
1xx: Informational
2xx: Success
  200 OK - Request successful
  201 Created - New resource created
  204 No Content - Success, no body to return

3xx: Redirection
  301 Moved Permanently
  302 Found

4xx: Client Error
  400 Bad Request - Invalid data
  401 Unauthorized - Need authentication
  403 Forbidden - No permission
  404 Not Found - Resource doesn't exist
  409 Conflict - Data conflict

5xx: Server Error
  500 Internal Server Error
  503 Service Unavailable
```

### 5. Request/Response Structure

**Request:**
```
GET /api/tasks/1 HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Bearer token123

{
  "filter": "completed"
}
```

**Response:**
```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 285

{
  "id": 1,
  "title": "Learn FastAPI",
  "completed": true,
  "created_at": "2024-01-15T10:30:00"
}
```

## 💾 Database Concepts

### 1. Relational Database Basics

**Table**: Like a spreadsheet with rows and columns

```
TASKS TABLE:
┌────┬──────────────┬──────────────┬───────────┐
│ ID │ TITLE        │ DESCRIPTION  │ COMPLETED │
├────┼──────────────┼──────────────┼───────────┤
│ 1  │ Learn Python │ Study basics │ TRUE      │
│ 2  │ Build API    │ FastAPI      │ FALSE     │
│ 3  │ Deploy code  │ ngrok setup  │ FALSE     │
└────┴──────────────┴──────────────┴───────────┘
```

### 2. SQL (Structured Query Language)

```sql
-- CREATE: Add new data
INSERT INTO tasks (title, description, completed)
VALUES ('New task', 'Description', FALSE);

-- READ: Retrieve data
SELECT * FROM tasks WHERE completed = FALSE;
SELECT COUNT(*) FROM tasks;

-- UPDATE: Modify existing data
UPDATE tasks SET completed = TRUE WHERE id = 1;

-- DELETE: Remove data
DELETE FROM tasks WHERE id = 1;
```

### 3. SQLAlchemy ORM

**ORM = Object-Relational Mapping**

Maps Python objects to database tables. Instead of writing SQL, write Python:

```python
# Without ORM (Raw SQL)
db.execute("SELECT * FROM tasks WHERE completed = TRUE")

# With ORM (SQLAlchemy)
db.query(Task).filter(Task.completed == True).all()

# Much cleaner and safer!
```

**Benefits:**
- Write Python instead of SQL
- Prevents SQL injection attacks
- Works with different databases
- Type hints and IDE autocomplete

### 4. Database Transactions

A transaction groups multiple operations that must succeed together:

```python
try:
    # Start transaction
    new_task = Task(title="New Task")
    db.add(new_task)
    
    # Another operation
    db.query(Task).update({Task.completed: True})
    
    # Commit all changes
    db.commit()
except:
    # Rollback if any error
    db.rollback()
    raise
```

If any operation fails, all changes are rolled back (database stays consistent).

## 🎨 Frontend Concepts

### 1. The DOM (Document Object Model)

The DOM is a tree structure representing the HTML:

```
Document
├── html
│   ├── head
│   │   ├── title
│   │   └── link (css)
│   └── body
│       ├── header
│       ├── main
│       │   ├── form
│       │   │   ├── input
│       │   │   └── button
│       │   └── div (tasks-list)
│       └── footer
```

JavaScript manipulates this tree to show/hide/update elements.

### 2. Fetch API (Making HTTP Requests)

```javascript
// Basic fetch example
fetch('http://localhost:8000/api/tasks')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));

// With async/await (cleaner)
async function getTasks() {
  try {
    const response = await fetch('/api/tasks');
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Error:', error);
  }
}

// POST request (create data)
fetch('/api/tasks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'New Task',
    description: 'Details'
  })
});
```

### 3. Event-Driven Programming

JavaScript reacts to user actions:

```javascript
// Listen for button click
button.addEventListener('click', function(event) {
  console.log('Button clicked!');
  // Do something
});

// Form submission
form.addEventListener('submit', function(event) {
  event.preventDefault();  // Stop page reload
  // Handle form data
});

// Input change
input.addEventListener('input', function(event) {
  console.log(event.target.value);
});
```

### 4. Async/Await Pattern

Handling asynchronous operations (API calls, file reads):

```javascript
// Problem: callback hell
fetch('/api/tasks')
  .then(response => response.json())
  .then(data => {
    fetch('/api/stats')
      .then(response => response.json())
      .then(stats => {
        // Do something
      });
  });

// Solution: async/await
async function loadData() {
  const tasks = await fetch('/api/tasks').then(r => r.json());
  const stats = await fetch('/api/stats').then(r => r.json());
  // Much cleaner!
}
```

## 🔐 Data Validation

### 1. Frontend Validation

Validate data before sending to backend:

```html
<!-- HTML validation -->
<input type="email" required>
<input type="number" min="1" max="100">
<input maxlength="50">

<!-- JavaScript validation -->
if (!taskTitle.trim()) {
  showError('Title is required');
  return;
}
```

**Benefits:**
- Better user experience (instant feedback)
- Reduces server load
- Prevent sending invalid data

### 2. Backend Validation (Pydantic)

```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    # Required field with constraints
    title: str = Field(..., min_length=1, max_length=200)
    
    # Optional field
    description: Optional[str] = Field(None, max_length=2000)
    
    # Field with default value
    completed: bool = Field(default=False)

# Usage in route
@app.post("/api/tasks")
def create_task(task: TaskCreate):
    # Pydantic automatically validates:
    # - title is provided and is string
    # - title is 1-200 characters
    # - description max 2000 chars
    # If validation fails, returns 422 error automatically
```

### 3. Security: Input Sanitization

Prevent XSS (Cross-Site Scripting) attacks:

```javascript
// Dangerous: HTML injection
div.innerHTML = userInput;  // ❌ BAD

// Safe: Text only
div.textContent = userInput;  // ✅ GOOD

// Or escape HTML
function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}
```

## 🎨 Responsive Design

### 1. Mobile-First Approach

Design for mobile first, then enhance for larger screens:

```css
/* Mobile (default) */
.container {
  flex-direction: column;  /* Stack vertically */
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    flex-direction: row;   /* Side by side */
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
  }
}
```

### 2. Flexible Layout

```css
/* Flexbox: One-dimensional layout */
.flex-container {
  display: flex;
  justify-content: space-between;  /* Distribute space */
  align-items: center;             /* Vertical alignment */
  gap: 16px;
}

/* Grid: Two-dimensional layout */
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);  /* 3 equal columns */
  gap: 16px;
}

/* Responsive Grid */
@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: 1fr;  /* 1 column on mobile */
  }
}
```

### 3. Meta Viewport Tag

Critical for mobile rendering:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

## 🔄 Development Workflow

### 1. Local Development

```bash
# Terminal 1: Backend
python -m uvicorn backend.main:app --reload

# Terminal 2: Frontend
# Use Live Server extension or simple HTTP server
python -m http.server 8001 -d frontend
```

### 2. Testing Loop

1. Make code change
2. Refresh browser
3. Test functionality
4. Check browser console
5. Check terminal for errors
6. Debug as needed
7. Repeat

### 3. Common Debugging Steps

**Backend not responding:**
- Check if server is running
- Check port (default 8000)
- Check for errors in terminal
- Check CORS configuration

**API call fails:**
- Check network tab in DevTools
- Verify request URL and method
- Check response status and message
- Verify request body format

**Data not showing:**
- Check if API request succeeded
- Log response in JavaScript console
- Check HTML element IDs
- Verify DOM is updated

## 🚀 Best Practices

### 1. Code Organization

```
✅ Good: Clear file structure
backend/
  ├── models.py       # Data models
  ├── schemas.py      # Validation
  ├── database.py     # DB config
  ├── crud.py         # Business logic
  └── main.py         # Routes

❌ Bad: Everything in one file
app.py  # 2000+ lines
```

### 2. Error Handling

```python
# ✅ Good: Specific error handling
try:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
except Exception as e:
    logger.error(f"Database error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")

# ❌ Bad: Catch-all without logging
try:
    ...
except:
    pass
```

### 3. Database Queries

```python
# ✅ Good: Indexed columns
db.query(Task).filter(Task.id == 1).first()       # id is indexed
db.query(Task).filter(Task.completed == True).all()

# ❌ Bad: Full table scans
db.query(Task).all()  # Then filter in Python
```

### 4. Frontend Performance

```javascript
// ✅ Good: Event delegation
container.addEventListener('click', (e) => {
  if (e.target.classList.contains('delete-btn')) {
    deleteTask(e.target.dataset.id);
  }
});

// ❌ Bad: Attach listener to each element
document.querySelectorAll('.delete-btn').forEach(btn => {
  btn.addEventListener('click', ...);  // If list grows, adds many listeners
});
```

## 📊 Data Flow Example

Let's trace a complete user action:

**User clicks "Complete Task" button:**

1. **Frontend - JavaScript Event**
   ```javascript
   btn.addEventListener('click', toggleTaskCompletion);
   ```

2. **Frontend - Fetch API Call**
   ```javascript
   fetch('/api/tasks/1', {
     method: 'PUT',
     body: JSON.stringify({ completed: true })
   });
   ```

3. **Network - HTTP Request**
   ```
   PUT /api/tasks/1 HTTP/1.1
   Content-Type: application/json
   
   { "completed": true }
   ```

4. **Backend - Route Handler**
   ```python
   @app.put("/api/tasks/{task_id}")
   def update_task(task_id: int, task_update: TaskUpdate):
   ```

5. **Backend - Database Query**
   ```python
   task = db.query(Task).filter(Task.id == 1).first()
   task.completed = True
   db.commit()
   ```

6. **Database - SQL Execution**
   ```sql
   UPDATE tasks SET completed = TRUE WHERE id = 1
   ```

7. **Backend - Response**
   ```json
   {
     "id": 1,
     "title": "Learn FastAPI",
     "completed": true,
     "updated_at": "2024-01-15T11:00:00"
   }
   ```

8. **Frontend - Update DOM**
   ```javascript
   document.getElementById('task-1').classList.add('completed');
   ```

9. **User Sees Result**
   Task visually marked as completed with strikethrough

---

**This is the foundation of web development!** Each component plays a specific role in creating a working application. Understanding these concepts will help you build any web application.
