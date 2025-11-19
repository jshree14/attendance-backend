# Student Attendance System - User Guide

## Step-by-Step Instructions

### Step 1: Open the API Documentation
1. Open your web browser (Chrome, Firefox, Edge, etc.)
2. Go to: **http://localhost:8000/docs**
3. You'll see the Swagger UI interface with all API endpoints

---

### Step 2: Create an Admin Account (Signup)

1. **Find the "Authentication" section** at the top of the page
2. **Click on "POST /auth/signup"** - it will expand
3. **Click the "Try it out" button** on the right side
4. You'll see a text box with example JSON
5. **Replace the example** with your details:
   ```json
   {
     "email": "admin@example.com",
     "password": "mypassword123"
   }
   ```
6. **Click the blue "Execute" button**
7. **Check the response** below:
   - If successful, you'll see: `{"msg": "user created"}`
   - Status code should be **201**

---

### Step 3: Login to Get Your Token

1. **Click on "POST /auth/login"** (just below signup)
2. **Click "Try it out"**
3. **Enter the SAME credentials** you just used for signup:
   ```json
   {
     "email": "admin@example.com",
     "password": "mypassword123"
   }
   ```
4. **Click "Execute"**
5. **Copy the access_token** from the response:
   - You'll see something like: `"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."`
   - **Select and copy** the entire token (the long string after "access_token")
   - Don't copy the quotes, just the token itself

---

### Step 4: Authorize Your Session

1. **Scroll to the top** of the page
2. **Click the green "Authorize" button** (with a lock icon)
3. A popup window will appear
4. **Paste your token** in the "Value" field
5. **Click "Authorize"**
6. **Click "Close"**
7. You'll now see the lock icons are **closed/locked** - this means you're authenticated!

---

### Step 5: Create a Student

1. **Scroll down to the "students" section**
2. **Click on "POST /students/"**
3. **Click "Try it out"**
4. **Enter student details**:
   ```json
   {
     "roll_no": "2024001",
     "name": "John Doe",
     "class_name": "10A"
   }
   ```
5. **Click "Execute"**
6. **Check response** - you should see the student details with an ID

---

### Step 6: Upload Student Photo (Optional)

1. **Click on "POST /students/{student_id}/upload-photo"**
2. **Click "Try it out"**
3. **Enter the student_id** (the ID from step 5, e.g., 1)
4. **Click "Choose File"** and select a photo (JPG, PNG, or GIF, max 5MB)
5. **Click "Execute"**
6. **Check response** - you'll see the photo_path is now filled

---

### Step 7: Mark Attendance

1. **Scroll to "attendance" section**
2. **Click on "POST /attendance/mark"**
3. **Click "Try it out"**
4. **Enter attendance details**:
   ```json
   {
     "student_id": 1,
     "status": "present",
     "date": null,
     "note": "On time"
   }
   ```
   - `student_id`: The ID of the student
   - `status`: Choose "present", "absent", or "leave"
   - `date`: Leave as `null` for today, or use format "2025-11-19"
   - `note`: Optional note
5. **Click "Execute"**
6. **Check response** - attendance record created!

---

### Step 8: View Attendance Records

1. **Click on "GET /attendance/"**
2. **Click "Try it out"**
3. **Optional filters** (leave blank to see all):
   - `student_id`: Filter by specific student
   - `class_name`: Filter by class (e.g., "10A")
   - `from_date`: Start date (e.g., "2025-11-01")
   - `to_date`: End date (e.g., "2025-11-30")
4. **Click "Execute"**
5. **View all attendance records** in the response

---

### Step 9: View Admin Dashboard

1. **Scroll to "Admin Dashboard" section**
2. **Click on "GET /admin/dashboard"**
3. **Click "Try it out"**
4. **Click "Execute"**
5. **View statistics**:
   - Total students
   - Today's attendance (present, absent, not marked)
   - Last 7 days trends
   - Class distribution

---

### Step 10: Export Attendance as CSV

1. **Go back to "attendance" section**
2. **Click on "GET /attendance/export"**
3. **Click "Try it out"**
4. **Add filters if needed** (same as Step 8)
5. **Click "Execute"**
6. **Click "Download"** button in the response
7. **Open the CSV file** in Excel or any spreadsheet application

---

## Common Issues & Solutions

### Issue: "Not authenticated" or "401 Unauthorized"
**Solution**: Your token expired or wasn't set. Go back to Step 3-4 and login again.

### Issue: "403 Forbidden" 
**Solution**: You need admin access. Make sure you're using an admin account.

### Issue: "Student not found"
**Solution**: Make sure you created a student first (Step 5) and use the correct student_id.

### Issue: "Attendance already marked"
**Solution**: You can only mark attendance once per student per day. Use a different date or student.

---

## Quick Reference

### Status Values for Attendance
- `"present"` - Student is present
- `"absent"` - Student is absent
- `"leave"` - Student is on leave

### Date Format
- Use: `"2025-11-19"` (YYYY-MM-DD)
- Or: `null` for today's date

### File Upload Limits
- Max size: 5MB
- Allowed types: JPG, JPEG, PNG, GIF

---

## API Endpoints Summary

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/auth/signup` | POST | Create new user | No |
| `/auth/login` | POST | Login and get token | No |
| `/students/` | POST | Create student | Admin only |
| `/students/` | GET | List all students | Yes |
| `/students/{id}` | GET | Get student details | Yes |
| `/students/{id}/upload-photo` | POST | Upload photo | Yes |
| `/attendance/mark` | POST | Mark attendance | Yes |
| `/attendance/` | GET | List attendance | Yes |
| `/attendance/export` | GET | Export CSV | Yes |
| `/admin/dashboard` | GET | View statistics | Admin only |
| `/admin/students/without-photo` | GET | Students without photos | Admin only |

---

## Need Help?

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

The server must be running for these to work. If you see "site can't be reached", make sure the server is running with `python run.py`.
