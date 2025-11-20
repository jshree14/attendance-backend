# How to Run the Attendance System - Simple Guide

## What's Happening?

Your project has **TWO separate parts** that need to run:

### Part 1: The Server (Backend API)
- **File:** `run.py`
- **What it does:** Runs the FastAPI server that handles all requests
- **Runs on:** http://localhost:8000
- **Must stay running:** YES - keep this terminal window open

### Part 2: The Demo Data Script
- **File:** `demo_data.py`
- **What it does:** Adds sample students and attendance to the database
- **Runs once:** YES - it finishes and exits
- **Must stay running:** NO - it just populates data and stops

### Part 3: The Browser
- **What you open:** http://localhost:8000/docs
- **What it shows:** Interactive API documentation (Swagger UI)
- **You must open manually:** YES - it doesn't open automatically

---

## 🚀 EASIEST WAY - Use the Batch File

### Windows Users (YOU):

**Just double-click this file:**
```
start_demo.bat
```

It will:
1. ✅ Start the server in a new window
2. ✅ Create demo data automatically
3. ✅ Open your browser to the API docs
4. ✅ Show you login credentials

**That's it!** Everything is automated.

---

## 📝 Manual Way (If batch file doesn't work)

### Step 1: Start the Server

Open a terminal and run:
```bash
cd attendance-backend
python run.py
```

**IMPORTANT:** Keep this terminal window open! Don't close it.

You should see:
```
Starting Student Attendance System API...
API Documentation: http://localhost:8000/docs
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Create Demo Data

Open a **NEW** terminal (keep the first one running!) and run:
```bash
cd attendance-backend
python demo_data.py
```

You should see:
```
🚀 Creating demo data...
✅ Admin account created
✅ Students created
✅ Attendance marked
```

This terminal will finish and close - that's normal!

### Step 3: Open Browser

Manually open your browser and go to:
```
http://localhost:8000/docs
```

### Step 4: Login

In the browser:
1. Find "POST /auth/login"
2. Click "Try it out"
3. Enter:
   ```json
   {
     "email": "admin@demo.com",
     "password": "admin123"
   }
   ```
4. Click "Execute"
5. Copy the token from response

### Step 5: Authorize

1. Click green "Authorize" button at top
2. Paste token
3. Click "Authorize" then "Close"

### Step 6: Test Features

Try these endpoints:
- **GET /admin/dashboard** - See statistics
- **GET /students/** - See 10 students
- **GET /attendance/** - See attendance records
- **GET /attendance/export** - Download CSV

---

## ❌ Common Problems & Solutions

### Problem 1: "Address already in use" or "Port 8000 is busy"

**Solution:** Another program is using port 8000.

**Fix:**
```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill that process (replace PID with the number you see)
taskkill /PID <PID> /F

# Then start server again
python run.py
```

### Problem 2: "Module not found" errors

**Solution:** Dependencies not installed.

**Fix:**
```bash
pip install -r requirements.txt
```

### Problem 3: Browser shows "This site can't be reached"

**Solution:** Server is not running.

**Fix:** Make sure you ran `python run.py` and it's still running.

### Problem 4: demo_data.py shows errors

**Solution:** Server must be running FIRST.

**Fix:**
1. Start server: `python run.py` (keep it running)
2. Open new terminal
3. Run: `python demo_data.py`

### Problem 5: "Internal Server Error" when signing up

**Solution:** bcrypt version issue (already fixed).

**Fix:**
```bash
pip install bcrypt==4.0.1
```

---

## 🎯 For Interview Demonstration

### Before Interview:
1. Run `start_demo.bat` (or manual steps above)
2. Verify browser opens to http://localhost:8000/docs
3. Test login with admin@demo.com / admin123
4. Check that dashboard shows 10 students

### During Interview:
1. Share your screen
2. Show the browser with Swagger UI
3. Login and authorize
4. Demonstrate features:
   - Admin dashboard (impressive stats!)
   - Student list
   - Attendance marking
   - CSV export
5. Show code in VS Code (optional)

---

## 📊 What Demo Data Creates

After running `demo_data.py`:

- **1 Admin User**
  - Email: admin@demo.com
  - Password: admin123

- **10 Students**
  - Classes: 10A, 10B, 11A, 11B
  - Roll numbers: 2024001 to 2024010

- **Today's Attendance**
  - 6 Present
  - 1 Absent
  - 1 Leave
  - 2 Not marked (to show "not marked" feature)

- **Historical Data**
  - Last 6 days of attendance
  - For trend analysis in dashboard

---

## 🔄 Starting Fresh

If you want to reset everything:

1. **Stop the server** (close terminal or Ctrl+C)
2. **Delete database:**
   ```bash
   del attendance.db
   ```
3. **Start again:**
   ```bash
   python run.py
   ```
4. **Create demo data:**
   ```bash
   python demo_data.py
   ```

---

## ✅ Quick Checklist

Before showing to interviewer:

- [ ] Server is running (`python run.py`)
- [ ] Demo data created (`python demo_data.py`)
- [ ] Browser opens to http://localhost:8000/docs
- [ ] Can login with admin@demo.com / admin123
- [ ] Dashboard shows 10 students
- [ ] Can export CSV
- [ ] Code is open in VS Code (optional)

---

## 💡 Understanding the Flow

```
1. YOU run: python run.py
   ↓
2. Server STARTS and keeps running
   ↓
3. YOU run: python demo_data.py (in new terminal)
   ↓
4. Script SENDS requests to server
   ↓
5. Server SAVES data to database
   ↓
6. Script FINISHES and exits
   ↓
7. YOU open: http://localhost:8000/docs
   ↓
8. Browser SHOWS Swagger UI
   ↓
9. YOU login and test features
```

**Key Point:** The server must ALWAYS be running. The demo script just adds data and exits.

---

## 🆘 Still Having Issues?

Check these:

1. **Is Python installed?**
   ```bash
   python --version
   ```
   Should show: Python 3.13.x

2. **Are dependencies installed?**
   ```bash
   pip list | findstr fastapi
   ```
   Should show fastapi version

3. **Is server actually running?**
   Look for terminal window with "Uvicorn running"

4. **Can you access the API?**
   Open: http://localhost:8000
   Should show: {"status":"ok","message":"..."}

If all else fails, just use the `start_demo.bat` file - it handles everything!
