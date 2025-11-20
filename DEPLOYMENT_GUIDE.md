# Deployment Guide - Render.com

## The Problem You Had

Your `requirements.txt` file contains **170+ packages** including:
- Jupyter Notebook packages (not needed for API)
- Windows-specific packages like `pywinpty` (breaks Linux deployment)
- Development tools (not needed in production)

This caused the deployment to fail on Render.com (which uses Linux).

## The Solution

I created a clean `requirements-deploy.txt` with only the **10 essential packages** needed for the API.

---

## 🚀 Deploy to Render.com (Free)

### Step 1: Prepare Your Code

1. **Update your requirements.txt** (choose one option):

   **Option A: Replace the entire file**
   ```bash
   # Backup old file
   copy requirements.txt requirements-old.txt
   
   # Use the clean one
   copy requirements-deploy.txt requirements.txt
   ```

   **Option B: Keep both files**
   - Keep `requirements.txt` for local development
   - Use `requirements-deploy.txt` for deployment
   - Tell Render to use `requirements-deploy.txt`

2. **Create a .gitignore file** (if not exists):
   ```
   __pycache__/
   *.pyc
   *.pyo
   *.db
   .env
   venv/
   .venv/
   uploads/
   *.log
   .DS_Store
   ```

3. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Attendance System"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/attendance-backend.git
   git push -u origin main
   ```

---

### Step 2: Deploy on Render.com

1. **Go to:** https://render.com
2. **Sign up/Login** (use GitHub account)
3. **Click "New +"** → **"Web Service"**
4. **Connect your GitHub repository**
5. **Configure:**

   ```
   Name: attendance-backend
   Region: Choose closest to you
   Branch: main
   Root Directory: attendance-backend (if in subfolder) or leave blank
   Runtime: Python 3
   Build Command: pip install -r requirements-deploy.txt
   Start Command: gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
   ```

6. **Add Environment Variable:**
   - Click "Advanced"
   - Add: `SECRET_KEY` = `your-secret-key-here-use-openssl-rand-hex-32`

7. **Select Free Plan**
8. **Click "Create Web Service"**

---

### Step 3: Wait for Deployment

- Takes 5-10 minutes
- Watch the logs
- When done, you'll get a URL like: `https://attendance-backend-xxxx.onrender.com`

---

### Step 4: Test Your Deployed API

Open: `https://your-app-url.onrender.com/docs`

You should see the Swagger UI!

---

## 🔧 If Deployment Fails

### Error: "pywinpty" or Windows packages

**Fix:** Make sure you're using `requirements-deploy.txt` in the build command:
```
pip install -r requirements-deploy.txt
```

### Error: "Module not found"

**Fix:** Check that all imports in your code match the packages in requirements-deploy.txt

### Error: "Port binding failed"

**Fix:** Make sure your start command uses `$PORT`:
```
--bind 0.0.0.0:$PORT
```

### Error: Database issues

**Fix:** Render's free tier has ephemeral storage. For production:
1. Use Render's PostgreSQL (free tier available)
2. Update `app/db/base.py` to use PostgreSQL URL from environment

---

## 📊 Using PostgreSQL on Render (Recommended for Production)

### Step 1: Create PostgreSQL Database

1. In Render dashboard, click "New +" → "PostgreSQL"
2. Name: `attendance-db`
3. Select Free plan
4. Click "Create Database"
5. Copy the "Internal Database URL"

### Step 2: Update Your Code

Update `app/db/base.py`:

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use PostgreSQL in production, SQLite in development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./attendance.db")

# Fix for Render's postgres:// URL (needs postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Step 3: Add Environment Variable

In your web service settings:
- Add: `DATABASE_URL` = (paste the Internal Database URL)

### Step 4: Redeploy

Render will automatically redeploy with the new database!

---

## 🌐 Alternative: Deploy to Railway.app

Railway is another free option:

1. Go to: https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and deploys!
6. Add environment variable: `SECRET_KEY`
7. Get your URL from the deployment

---

## 🐳 Alternative: Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements-deploy.txt .
RUN pip install --no-cache-dir -r requirements-deploy.txt

COPY app ./app

ENV PORT=8000
ENV SECRET_KEY=change-me-in-production

CMD gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

Deploy to:
- **Render.com** (Docker support)
- **Railway.app** (Docker support)
- **Fly.io** (Free tier)
- **AWS ECS** (Paid)
- **Google Cloud Run** (Free tier)

---

## 📝 Files Created for Deployment

1. **requirements-deploy.txt** - Clean production dependencies
2. **render.yaml** - Render.com configuration
3. **Procfile** - Process file for deployment
4. **runtime.txt** - Python version specification
5. **.gitignore** - Files to exclude from Git

---

## ✅ Deployment Checklist

Before deploying:

- [ ] Code pushed to GitHub
- [ ] Using `requirements-deploy.txt` (not the bloated one)
- [ ] `.gitignore` excludes sensitive files
- [ ] `SECRET_KEY` environment variable set
- [ ] Database configured (SQLite for testing, PostgreSQL for production)
- [ ] All imports work with production dependencies
- [ ] Tested locally with: `gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000`

---

## 🎯 For Interview

**Show the deployed version:**
- "I deployed this to Render.com's free tier"
- Share the live URL: `https://your-app.onrender.com/docs`
- "Anyone can test the API without installing anything"
- "In production, I'd use PostgreSQL instead of SQLite"

This shows you understand:
- Deployment processes
- Production vs development dependencies
- Cloud platforms
- DevOps basics

---

## 💰 Cost

**Free Tier Limitations:**
- Render.com: Spins down after 15 min of inactivity (takes 30s to wake up)
- Railway.app: $5 free credit per month
- Fly.io: 3 free apps

**For Production:**
- Render.com: $7/month (always on)
- Railway.app: Pay as you go
- AWS/GCP: Variable pricing

---

## 🆘 Need Help?

**Render Logs:**
- Click on your service
- Go to "Logs" tab
- See real-time deployment logs

**Common Issues:**
1. Build fails → Check requirements-deploy.txt
2. App crashes → Check logs for errors
3. Can't connect → Check if service is running
4. 502 error → App didn't start, check start command

**Test Locally First:**
```bash
# Install production dependencies
pip install -r requirements-deploy.txt

# Test with gunicorn (production server)
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Open: http://localhost:8000/docs
```

If it works locally with gunicorn, it will work on Render!
