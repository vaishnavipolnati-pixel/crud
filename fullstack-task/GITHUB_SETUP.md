# GitHub Setup & Collaboration Guide

## 🚀 Initial GitHub Setup

### 1. Create Repository on GitHub

1. Go to [github.com](https://github.com) and sign in
2. Click **"New Repository"** or go to https://github.com/new
3. Fill in details:
   - **Repository name**: `fullstack-task`
   - **Description**: `Full-stack CRUD application with FastAPI and vanilla JavaScript`
   - **Public**: ✅ (to share publicly)
   - **Initialize with**: Leave empty (we already have files)
4. Click **"Create Repository"**

### 2. Connect Local Repository to GitHub

```bash
# In your project directory
cd fullstack-task

# Check current remote (if any)
git remote -v

# Add GitHub as remote origin
git remote add origin https://github.com/YOUR_USERNAME/fullstack-task.git

# Verify
git remote -v
# Output should show:
# origin  https://github.com/YOUR_USERNAME/fullstack-task.git (fetch)
# origin  https://github.com/YOUR_USERNAME/fullstack-task.git (push)

# Set main branch name
git branch -M main

# Push code to GitHub
git push -u origin main
```

**What's happening:**
- `origin`: Default name for remote repository
- `-u`: Sets upstream tracking (future pushes auto-go to main)
- `main`: Primary branch

### 3. Verify on GitHub

1. Refresh GitHub repository page
2. You should see all files uploaded
3. README.md should be displayed

---

## 📌 Branch Strategy

### Recommended Structure

```
main                          (production-ready)
├── hotfix/fix-critical-bug   (emergency fix)
└── develop                   (integration branch)
    ├── feature/add-priority
    ├── feature/add-auth
    └── bugfix/fix-validation
```

### Git Flow Workflow

```bash
# Create feature branch from develop
git checkout develop
git pull
git checkout -b feature/add-task-priority

# ... make changes, commit ...
git add .
git commit -m "feat(tasks): add priority field"

# Push feature branch
git push origin feature/add-task-priority

# On GitHub: Create Pull Request
# After review & approval:
git checkout develop
git pull
git merge feature/add-task-priority
git push

# Merge develop to main for release
git checkout main
git pull
git merge develop
git push

# Tag release
git tag v1.0.0
git push origin v1.0.0
```

---

## 📝 Commit Message Format

### Conventional Commits

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

```
feat      - New feature
fix       - Bug fix
refactor  - Code restructuring (no functional change)
docs      - Documentation
style     - Formatting, missing semicolons, etc.
test      - Adding/updating tests
chore     - Build process, dependency updates
ci        - CI/CD changes
perf      - Performance improvements
```

### Scopes

```
backend   - Changes to backend code
frontend  - Changes to frontend code
database  - Database migrations or schema changes
api       - API changes
docs      - Documentation changes
```

### Examples

```bash
# Good commits
git commit -m "feat(backend): add task priority field

- Add priority column to Task model
- Update Pydantic schema for validation
- Implement priority sorting in GET endpoint
- Add priority filter option"

git commit -m "fix(frontend): prevent duplicate task creation on click"

git commit -m "docs: add API authentication guide"

git commit -m "refactor(backend): extract validation logic to separate function"

git commit -m "style: format code with prettier"

# Bad commits
git commit -m "fixed bug"              # Too vague
git commit -m "Updated things"         # Not descriptive
git commit -m "WIP"                    # Work in progress shouldn't be committed
```

---

## 🔄 Pull Request Workflow

### Creating a Pull Request

1. **Push your feature branch:**
   ```bash
   git push origin feature/add-priority
   ```

2. **On GitHub, PR appears automatically** or click "Compare & pull request"

3. **Fill PR details:**

   **Title**: 
   ```
   Add task priority field
   ```

   **Description**:
   ```markdown
   ## Changes
   - Add priority (1-5) to tasks
   - Update API validation
   - Add priority filter

   ## Type of Change
   - [x] New feature
   - [ ] Bug fix
   - [ ] Breaking change

   ## Testing
   - [x] Tested locally with Postman
   - [x] Verified database schema
   - [ ] Added unit tests

   ## Checklist
   - [x] Code follows style guidelines
   - [x] Self-review completed
   - [x] Comments added for complex logic
   - [x] Documentation updated
   - [ ] No new warnings generated

   ## Related Issues
   Closes #123
   ```

4. **Request review:**
   - Add reviewers
   - Add labels (e.g., "enhancement", "documentation")
   - Add to project

5. **Address feedback:**
   - Make requested changes
   - Commit to same branch
   - Changes auto-appear in PR

6. **Merge:**
   - Once approved, click "Squash and merge"
   - Or "Create a merge commit"
   - Delete branch after merge

---

## 🔀 Handling Merge Conflicts

### When Conflicts Occur

```bash
# You're merging main into your feature branch
git merge main

# Conflict detected! Error message shows conflicted files
# CONFLICT (content merge): Merge conflict in backend/models.py
```

### Resolve Conflict

**In VS Code:**
1. Open conflicted file
2. See conflict markers:
   ```python
   # <<<<<<< HEAD (your changes)
   class Task(Base):
       priority: int
   # =======
   class Task(Base):
       description: str
   # >>>>>>> main
   ```

3. Choose which to keep or combine both
4. Delete conflict markers
5. Save file

**Command line:**
```bash
# View conflicts
git status

# Edit files to resolve
# Then mark as resolved
git add backend/models.py

# Complete merge
git commit -m "Merge main: resolve conflicts in models.py"

# Push resolved merge
git push origin feature/add-priority
```

---

## 🏷️ Releases & Tagging

### Creating a Release

```bash
# Tag current commit
git tag v1.0.0

# Annotated tag (recommended)
git tag -a v1.0.0 -m "Release version 1.0.0 - Initial stable release"

# Push tag
git push origin v1.0.0

# Push all tags
git push origin --tags

# List tags
git tag -l
```

### On GitHub

1. Go to "Releases"
2. Click "Draft a new release"
3. Select tag: `v1.0.0`
4. Title: "Version 1.0.0 - Initial Release"
5. Description:
   ```markdown
   ## Features
   - Complete CRUD operations
   - Responsive UI
   - SQLite database
   - REST API

   ## Installation
   See README.md for setup instructions

   ## Known Issues
   None
   ```

6. Click "Publish release"

---

## 📊 Collaborating with Others

### When Someone Else Contributes

```bash
# Fetch latest changes from GitHub
git fetch origin

# See all branches
git branch -a

# Switch to their branch to review
git checkout origin/feature/their-feature

# Merge their branch to main (after review)
git checkout main
git merge origin/feature/their-feature
git push origin main
```

### Best Practices for Collaboration

1. **Communicate**: Discuss features before starting
2. **Small PRs**: Easier to review and merge
3. **Descriptive commits**: Help others understand changes
4. **Review PRs**: Give constructive feedback
5. **Test thoroughly**: Verify locally before merging

---

## 🔒 Protecting Main Branch

### GitHub Settings

1. Go to repository Settings
2. Click "Branches"
3. Click "Add rule"
4. Branch name pattern: `main`
5. Enable:
   - [x] Require pull request reviews
   - [x] Require status checks to pass
   - [x] Require branches to be up to date
   - [x] Include administrators
6. Click "Create"

**Effect:**
- No direct pushes to main
- PRs required with at least 1 approval
- All tests must pass before merge

---

## 🤖 CI/CD with GitHub Actions

### Automated Testing

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/ -v
```

**Effect:**
- Automatically runs tests on every push
- Shows test results in PR
- Prevents merge if tests fail

---

## 📚 README for GitHub

Good GitHub README includes:

✅ **What we have:**
- Project title and description
- Features list
- Technology stack
- Quick start guide
- Screenshots (if applicable)
- Installation steps
- Usage examples
- API documentation
- Deployment instructions
- Contributing guidelines
- License
- Contact info

✅ **Visual elements:**
- Badges (build status, version, license)
- Table of contents (for long READMEs)
- Code examples
- Diagrams if helpful

---

## 🌐 GitHub Pages Deployment

### Deploy Frontend to GitHub Pages

1. **Create `gh-pages` branch:**
   ```bash
   git checkout --orphan gh-pages
   git rm -rf .
   ```

2. **Copy only frontend files:**
   ```bash
   cp -r frontend/* .
   git add .
   git commit -m "Deploy frontend to GitHub Pages"
   git push origin gh-pages
   ```

3. **Enable in Settings:**
   - Go to Settings → Pages
   - Source: `gh-pages` branch
   - Click "Save"

4. **Access at:**
   ```
   https://YOUR_USERNAME.github.io/fullstack-task/
   ```

---

## 🔗 Important Links

- **Repository**: https://github.com/YOUR_USERNAME/fullstack-task
- **Issues**: https://github.com/YOUR_USERNAME/fullstack-task/issues
- **Pull Requests**: https://github.com/YOUR_USERNAME/fullstack-task/pulls
- **Releases**: https://github.com/YOUR_USERNAME/fullstack-task/releases
- **Settings**: https://github.com/YOUR_USERNAME/fullstack-task/settings

---

## 📋 Checklist for Public Repository

Before sharing:

- [ ] README.md is complete and clear
- [ ] .gitignore includes sensitive files
- [ ] No API keys or passwords in code
- [ ] License specified (e.g., MIT)
- [ ] Contributing guidelines added
- [ ] Issues/PR templates created
- [ ] Code has comments explaining complex logic
- [ ] Example .env file provided
- [ ] Instructions for local setup
- [ ] Deployment steps documented

---

## 🆘 Useful GitHub Links

- [GitHub Documentation](https://docs.github.com/)
- [GitHub Guides](https://guides.github.com/)
- [Git Cheat Sheet](https://github.github.com/training-kit/)
- [Choose a License](https://choosealicense.com/)

---

**Happy collaborating! 🚀**
