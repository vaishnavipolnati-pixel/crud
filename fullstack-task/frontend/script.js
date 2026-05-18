/**
 * FRONTEND JAVASCRIPT
 * ===================
 * This file handles all frontend logic:
 * - API communication
 * - DOM manipulation
 * - Event handling
 * - State management
 * 
 * Key Concepts:
 * - Fetch API: Making HTTP requests to backend
 * - Async/Await: Handling asynchronous operations
 * - Event Listeners: Responding to user interactions
 * - DOM Methods: Creating and updating HTML elements
 */

// ==================== CONFIGURATION ====================

const API_BASE_URL = "http://127.0.0.1:8001"

// API Endpoints
const API_ENDPOINTS = {
    tasks: `${API_BASE_URL}/api/tasks`,
    health: `${API_BASE_URL}/health`,
    stats: `${API_BASE_URL}/api/stats`,
};

// Global state
let currentFilter = 'all';
let allTasks = [];

// ==================== INITIALIZATION ====================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Application loaded');
    
    // Check API health
    checkAPIHealth();
    
    // Load initial data
    loadTasks();
    loadStats();
    
    // Setup event listeners
    setupEventListeners();
    
    // Auto-refresh stats every 5 seconds
    setInterval(loadStats, 5000);
});

// ==================== EVENT LISTENERS ====================

function setupEventListeners() {
    // Form submission
    document.getElementById('taskForm').addEventListener('submit', handleCreateTask);
    
    // Character counters
    document.getElementById('taskTitle').addEventListener('input', updateCharCount);
    document.getElementById('taskDescription').addEventListener('input', updateCharCount);
    
    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', handleFilterChange);
    });
}

// ==================== FORM HANDLERS ====================

/**
 * Update character count display
 */
function updateCharCount(event) {
    const input = event.target;
    const maxLength = input.getAttribute('maxlength');
    const currentLength = input.value.length;
    const charCount = input.parentElement.querySelector('.char-count');
    
    if (charCount) {
        charCount.textContent = `${currentLength} / ${maxLength}`;
    }
}

/**
 * Handle task creation
 * @param {Event} event - Form submission event
 */
async function handleCreateTask(event) {
    event.preventDefault();
    
    // Get form data
    const formData = new FormData(document.getElementById('taskForm'));
    const taskData = {
        title: formData.get('title').trim(),
        description: formData.get('description').trim() || null,
        completed: formData.get('completed') === 'on' ? true : false
    };
    
    // Validation
    if (!taskData.title) {
        showError('Task title is required');
        return;
    }
    
    try {
        // Show loading state
        const submitBtn = document.querySelector('#taskForm button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.textContent = '⏳ Creating...';
        
        // Make API call
        const response = await fetch(API_ENDPOINTS.tasks, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create task');
        }
        
        // Reset form
        document.getElementById('taskForm').reset();
        document.querySelectorAll('.char-count').forEach(el => el.textContent = '0 / ' + el.parentElement.querySelector('input,textarea')?.getAttribute('maxlength'));
        
        // Reload tasks
        await loadTasks();
        loadStats();
        
        // Show success message
        showSuccess('Task created successfully!');
        
    } catch (error) {
        console.error('Error creating task:', error);
        showError('Failed to create task: ' + error.message);
    } finally {
        // Restore button
        const submitBtn = document.querySelector('#taskForm button[type="submit"]');
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

// ==================== FILTER HANDLERS ====================

/**
 * Handle filter button clicks
 * @param {Event} event - Click event
 */
function handleFilterChange(event) {
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Update filter and render
    currentFilter = event.target.dataset.filter;
    renderTasks();
}

// ==================== API CALLS ====================

/**
 * Check if API is running
 */
async function checkAPIHealth() {
    try {
        const response = await fetch(API_ENDPOINTS.health);
        if (response.ok) {
            updateAPIStatus(true);
            console.log('✅ API is healthy');
        } else {
            updateAPIStatus(false);
        }
    } catch (error) {
        console.error('API health check failed:', error);
        updateAPIStatus(false);
    }
}

/**
 * Update API status display
 * @param {boolean} healthy - API health status
 */
function updateAPIStatus(healthy) {
    const statusElement = document.getElementById('apiStatus');
    if (healthy) {
        statusElement.textContent = '🟢 Online';
        statusElement.classList.add('healthy');
        statusElement.classList.remove('error');
    } else {
        statusElement.textContent = '🔴 Offline';
        statusElement.classList.add('error');
        statusElement.classList.remove('healthy');
        showError('⚠️ API is not responding. Make sure the backend is running!');
    }
}

/**
 * Load all tasks from API
 */
async function loadTasks() {
    try {
        showLoadingSpinner(true);
        clearError();
        
        const response = await fetch(API_ENDPOINTS.tasks);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        allTasks = data.tasks;
        
        console.log(`✅ Loaded ${allTasks.length} tasks`);
        renderTasks();
        
    } catch (error) {
        console.error('Error loading tasks:', error);
        showError('Failed to load tasks from API');
    } finally {
        showLoadingSpinner(false);
    }
}

/**
 * Load statistics from API
 */
async function loadStats() {
    try {
        const response = await fetch(API_ENDPOINTS.stats);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const stats = await response.json();
        
        // Update stats display
        document.getElementById('totalTasks').textContent = stats.total_tasks;
        document.getElementById('completedTasks').textContent = stats.completed_tasks;
        document.getElementById('pendingTasks').textContent = stats.pending_tasks;
        
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

/**
 * Update task status (toggle completion)
 * @param {number} taskId - Task ID
 * @param {boolean} completed - New completion status
 */
async function toggleTaskCompletion(taskId, completed) {
    try {
        const response = await fetch(`${API_ENDPOINTS.tasks}/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ completed: !completed })
        });
        
        if (!response.ok) {
            throw new Error('Failed to update task');
        }
        
        // Reload tasks
        await loadTasks();
        loadStats();
        
    } catch (error) {
        console.error('Error updating task:', error);
        showError('Failed to update task');
    }
}

/**
 * Delete a task
 * @param {number} taskId - Task ID to delete
 */
async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_ENDPOINTS.tasks}/${taskId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete task');
        }
        
        // Reload tasks
        await loadTasks();
        loadStats();
        showSuccess('Task deleted successfully!');
        
    } catch (error) {
        console.error('Error deleting task:', error);
        showError('Failed to delete task');
    }
}

// ==================== RENDERING ====================

/**
 * Render tasks to the DOM
 */
function renderTasks() {
    const tasksList = document.getElementById('tasksList');
    const emptyState = document.getElementById('emptyState');
    
    // Filter tasks based on current filter
    let filteredTasks = allTasks;
    
    if (currentFilter === 'completed') {
        filteredTasks = allTasks.filter(task => task.completed);
    } else if (currentFilter === 'pending') {
        filteredTasks = allTasks.filter(task => !task.completed);
    }
    
    // Handle empty state
    if (filteredTasks.length === 0) {
        tasksList.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    
    // Render tasks
    tasksList.innerHTML = filteredTasks.map(task => createTaskElement(task)).join('');
    
    // Attach event listeners to action buttons
    attachTaskEventListeners();
}

/**
 * Create HTML for a single task
 * @param {Object} task - Task object
 * @returns {string} HTML string
 */
function createTaskElement(task) {
    const createdDate = new Date(task.created_at).toLocaleDateString();
    const statusClass = task.completed ? 'completed' : '';
    
    return `
        <div class="task-item ${statusClass}" data-task-id="${task.id}">
            <div class="task-header">
                <input 
                    type="checkbox" 
                    class="task-checkbox" 
                    ${task.completed ? 'checked' : ''}
                    data-task-id="${task.id}"
                >
                <div class="task-content">
                    <div class="task-title">${escapeHtml(task.title)}</div>
                    ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : ''}
                    <div class="task-meta">
                        <span>📅 Created: ${createdDate}</span>
                        <span>Status: ${task.completed ? '✅ Completed' : '⏳ Pending'}</span>
                    </div>
                </div>
            </div>
            <div class="task-actions">
                <button class="btn btn-complete btn-small" data-task-id="${task.id}">
                    ${task.completed ? '↩️ Undo' : '✅ Complete'}
                </button>
                <button class="btn btn-delete btn-small" data-task-id="${task.id}">
                    🗑️ Delete
                </button>
            </div>
        </div>
    `;
}

/**
 * Attach event listeners to task action buttons
 */
function attachTaskEventListeners() {
    // Checkbox listeners
    document.querySelectorAll('.task-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            const taskId = parseInt(e.target.dataset.taskId);
            const task = allTasks.find(t => t.id === taskId);
            toggleTaskCompletion(taskId, task.completed);
        });
    });
    
    // Complete/Undo button listeners
    document.querySelectorAll('.btn-complete').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const taskId = parseInt(e.target.dataset.taskId);
            const task = allTasks.find(t => t.id === taskId);
            toggleTaskCompletion(taskId, task.completed);
        });
    });
    
    // Delete button listeners
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const taskId = parseInt(e.target.dataset.taskId);
            deleteTask(taskId);
        });
    });
}

// ==================== UI UTILITIES ====================

/**
 * Show loading spinner
 * @param {boolean} show - Whether to show spinner
 */
function showLoadingSpinner(show) {
    document.getElementById('loadingSpinner').style.display = show ? 'flex' : 'none';
}

/**
 * Show error message
 * @param {string} message - Error message
 */
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    console.error('❌', message);
}

/**
 * Show success message
 * @param {string} message - Success message
 */
function showSuccess(message) {
    // For simplicity, just log it. You could create a toast notification instead
    console.log('✅', message);
}

/**
 * Clear error message
 */
function clearError() {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.style.display = 'none';
    errorDiv.textContent = '';
}

/**
 * Escape HTML special characters to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
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
