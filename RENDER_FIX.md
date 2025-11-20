# 🔧 Fix Render.com Start Command Error

## The Problem

Error: `Failed to find attribute 'app' in 'app'`

This means the start command is wrong. Render is trying to run `gunicorn app:app` but it should be `gunicorn app.main:app`.

---

## ✅ Quick Fix - Update Render Settings

### Go to your Render Dashboard:
https://dashboard.render.com

### Click on your service: `attendance-backend`

### Click "Settings" (left sidebar)

### Scroll to "Build & Deploy" section

### Update these fields:

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### Click "Save Changes"

### Render will automatically redeploy!

---

## 📋 Complete Settings Checklist

Make sure these are set correctly:

✅ **Name:** attendance-backend  
✅ **Branch:** main  
✅ **Build Command:** `pip install -r requirements.txt`  
✅ **Start Command:** `gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`  
✅ **Environment Variable:** `SECRET_KEY` = (any random string)

---

## 🎯 Why This Happens

Your project structure is:
```
attendance-backend/
├── app/
│   ├── main.py  ← FastAPI app is here
│   └── ...
```

So the correct path is: `app.main:app`
- `app` = folder name
- `main` = file name (main.py)
- `app` = variable name in main.py

---

## ✅ After Fixing

1. Render will redeploy automatically
2. Wait 2-3 minutes
3. Check logs for "Application startup complete"
4. Visit your URL: `https://attendance-backend-xxxx.onrender.com/docs`

---

## 🆘 Still Not Working?

### Check the logs:
1. Go to your service in Render
2. Click "Logs" tab
3. Look for errors

### Common issues:

**Error: "No module named 'app'"**
- Make sure your code is in the `app/` folder
- Check that `app/__init__.py` exists (can be empty)

**Error: "SECRET_KEY not set"**
- Add SECRET_KEY environment variable in Render settings

**Error: "Port binding failed"**
- Make sure start command uses `$PORT` (not hardcoded 8000)

---

## 💡 Alternative: Use render.yaml

If you want automatic configuration, Render can read from `render.yaml`:

1. Make sure `render.yaml` is in your repo root
2. In Render, create service from "Blueprint"
3. Select your repo
4. Render will use settings from render.yaml

The render.yaml file is already configured correctly!

---

## ✅ Test Locally First

Before deploying, test the gunicorn command locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Test gunicorn
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Open: http://localhost:8000/docs
```

If it works locally, it will work on Render!
