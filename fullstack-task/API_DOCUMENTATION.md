# API Documentation

## Base URL

```
Local Development: http://localhost:8000
```

## Authentication

Currently, no authentication is required. In production, implement JWT tokens.

## Common Headers

```
Content-Type: application/json
Accept: application/json
```

## Response Format

All successful responses return JSON:

```json
{
  "field": "value",
  "nested": {
    "field": "value"
  }
}
```

Error responses:

```json
{
  "error": "Error message",
  "detail": "Detailed explanation"
}
```

---

## Endpoints

### 1. Health Check

**Check if API is running**

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

**Status Code:** `200 OK`

---

### 2. Get All Tasks

**Retrieve all tasks with pagination and filtering**

```http
GET /api/tasks?skip=0&limit=10&completed=false
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| skip | integer | No | Number of tasks to skip (pagination) |
| limit | integer | No | Maximum number of tasks (default 100) |
| completed | boolean | No | Filter by completion status (true/false) |

**Response:**
```json
{
  "total": 5,
  "tasks": [
    {
      "id": 1,
      "title": "Learn FastAPI",
      "description": "Study FastAPI documentation",
      "completed": false,
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T11:00:00"
    },
    {
      "id": 2,
      "title": "Build API",
      "description": null,
      "completed": true,
      "created_at": "2024-01-14T09:00:00",
      "updated_at": "2024-01-15T14:30:00"
    }
  ]
}
```

**Status Code:** `200 OK`

**Examples:**

```bash
# Get first 10 tasks
curl http://localhost:8000/api/tasks?skip=0&limit=10

# Get only completed tasks
curl http://localhost:8000/api/tasks?completed=true

# Get tasks 20-30 (pagination)
curl http://localhost:8000/api/tasks?skip=20&limit=10
```

---

### 3. Get Single Task

**Retrieve a specific task by ID**

```http
GET /api/tasks/{task_id}
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | integer | Yes | The ID of the task |

**Response:**
```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Study FastAPI documentation",
  "completed": false,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T11:00:00"
}
```

**Status Codes:**
- `200 OK` - Task found
- `404 Not Found` - Task doesn't exist

**Example:**

```bash
curl http://localhost:8000/api/tasks/1
```

---

### 4. Create Task

**Create a new task**

```http
POST /api/tasks
Content-Type: application/json

{
  "title": "New Task",
  "description": "Task description",
  "completed": false
}
```

**Request Body:**
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| title | string | Yes | 1-200 characters |
| description | string | No | Max 2000 characters |
| completed | boolean | No | Default: false |

**Response:**
```json
{
  "id": 10,
  "title": "New Task",
  "description": "Task description",
  "completed": false,
  "created_at": "2024-01-15T15:30:00",
  "updated_at": "2024-01-15T15:30:00"
}
```

**Status Codes:**
- `201 Created` - Task created successfully
- `400 Bad Request` - Missing or invalid fields
- `422 Unprocessable Entity` - Validation failed

**Examples:**

```bash
# Using curl
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn JavaScript",
    "description": "Complete JavaScript tutorial"
  }'

# Using JavaScript fetch
fetch('http://localhost:8000/api/tasks', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'Learn Python',
    description: 'Master Python basics',
    completed: false
  })
})
.then(r => r.json())
.then(data => console.log('Created task:', data));

# Using Postman
1. Set method to POST
2. URL: http://localhost:8000/api/tasks
3. Body > raw > JSON:
{
  "title": "New Task",
  "description": "Description here"
}
4. Click Send
```

---

### 5. Update Task

**Update an existing task (partial update)**

```http
PUT /api/tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "completed": true
}
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | integer | Yes | The ID of the task to update |

**Request Body (all optional):**
| Field | Type | Constraints |
|-------|------|-------------|
| title | string | 1-200 characters |
| description | string | Max 2000 characters |
| completed | boolean | true/false |

**Response:**
```json
{
  "id": 1,
  "title": "Updated Title",
  "description": "Original description unchanged",
  "completed": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T16:00:00"
}
```

**Status Codes:**
- `200 OK` - Task updated successfully
- `404 Not Found` - Task doesn't exist
- `422 Unprocessable Entity` - Validation failed

**Examples:**

```bash
# Update only title
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "New Title"}'

# Mark as completed
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# JavaScript
fetch('http://localhost:8000/api/tasks/1', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ completed: true })
})
.then(r => r.json())
.then(data => console.log('Updated:', data));
```

---

### 6. Delete Task

**Delete a task**

```http
DELETE /api/tasks/{task_id}
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | integer | Yes | The ID of the task to delete |

**Response:**
```
(No content - empty body)
```

**Status Codes:**
- `204 No Content` - Task deleted successfully
- `404 Not Found` - Task doesn't exist

**Examples:**

```bash
# Using curl
curl -X DELETE http://localhost:8000/api/tasks/1

# JavaScript
fetch('http://localhost:8000/api/tasks/1', {
  method: 'DELETE'
})
.then(response => {
  if (response.status === 204) {
    console.log('Task deleted');
  }
});
```

---

### 7. Get Statistics

**Get task statistics**

```http
GET /api/stats
```

**Response:**
```json
{
  "total_tasks": 15,
  "completed_tasks": 8,
  "pending_tasks": 7,
  "completion_percentage": 53.33
}
```

**Status Code:** `200 OK`

**Example:**

```bash
curl http://localhost:8000/api/stats
```

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Task with id 999 not found"
}
```

### Common Errors

#### 400 Bad Request
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "title"],
      "msg": "value_error.missing"
    }
  ]
}
```
**Cause:** Missing required field or invalid data

**Solution:** Check request body, verify all required fields are present and valid

#### 404 Not Found
```json
{
  "detail": "Task with id 999 not found"
}
```
**Cause:** Resource doesn't exist

**Solution:** Verify the task ID is correct

#### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at most 200 characters",
      "type": "value_error.string.too_long"
    }
  ]
}
```
**Cause:** Validation error (invalid value)

**Solution:** Check field constraints (min/max length, format, etc.)

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```
**Cause:** Backend error

**Solution:** Check server logs, restart server if needed

---

## Testing with Postman

### Setup

1. **Create Collection**
   - Click "Collections" → "Create New Collection"
   - Name: "Task Manager API"

2. **Create Environment**
   - Click "Environments" → "Create New Environment"
   - Add variable: `base_url` = `http://localhost:8000`
   - Add variable: `task_id` = `1`

3. **Use Variables**
   - In requests, use `{{base_url}}` and `{{task_id}}`

### Sample Requests

```
# Get All Tasks
GET {{base_url}}/api/tasks

# Get Single Task
GET {{base_url}}/api/tasks/{{task_id}}

# Create Task
POST {{base_url}}/api/tasks
Content-Type: application/json

{
  "title": "New Task from Postman",
  "description": "Testing API",
  "completed": false
}

# Update Task
PUT {{base_url}}/api/tasks/{{task_id}}
Content-Type: application/json

{
  "completed": true
}

# Delete Task
DELETE {{base_url}}/api/tasks/{{task_id}}
```

---

## Pagination Example

Getting tasks 10-20:

```bash
curl "http://localhost:8000/api/tasks?skip=10&limit=10"
```

```json
{
  "total": 150,
  "tasks": [
    { "id": 11, "title": "Task 11", ... },
    { "id": 12, "title": "Task 12", ... },
    ...
    { "id": 20, "title": "Task 20", ... }
  ]
}
```

---

## Rate Limiting

Currently, no rate limiting. In production, implement:

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/tasks")
@limiter.limit("100/minute")
def get_tasks(request: Request):
    ...
```

---

## CORS

Currently allows all origins. In production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

---

## API Versioning

Future versions:

```
/api/v1/tasks
/api/v2/tasks (with new fields)
```

---

## Documentation

Interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

These are auto-generated from code!

---

## Best Practices for API Consumption

### 1. Always Check Status Code
```javascript
fetch('/api/tasks')
  .then(r => {
    if (!r.ok) throw new Error(`Status ${r.status}`);
    return r.json();
  });
```

### 2. Handle Errors
```javascript
try {
  const response = await fetch('/api/tasks/1');
  if (response.status === 404) {
    console.log('Task not found');
  }
} catch (error) {
  console.error('Network error:', error);
}
```

### 3. Use Timeouts
```javascript
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 5000);

fetch('/api/tasks', { signal: controller.signal })
  .catch(e => console.error('Timeout:', e));
```

### 4. Retry Failed Requests
```javascript
async function fetchWithRetry(url, options, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await fetch(url, options);
    } catch (e) {
      if (i === retries - 1) throw e;
      await new Promise(r => setTimeout(r, 1000 * (i + 1)));
    }
  }
}
```

---

## GraphQL Alternative (Future)

As the API grows, consider GraphQL:

```graphql
query GetTasks {
  tasks(filter: { completed: false }) {
    id
    title
    completed
  }
}
```

More efficient than REST for complex queries.
