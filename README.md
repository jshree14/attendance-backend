# Student Attendance System Backend

A FastAPI-based backend system for managing student attendance with photo upload, admin dashboard, and CSV export capabilities.

## Features

- **Authentication**: JWT-based user authentication with admin role support
- **Student Management**: Register students with roll numbers, names, and class assignments
- **Photo Upload**: Optional photo upload for student identity verification (max 5MB, jpg/png/gif)
- **Attendance Marking**: Mark attendance with status (present/absent/leave) and notes
- **Admin Dashboard**: View statistics including today's attendance, weekly trends, and class distribution
- **CSV Export**: Export attendance records with flexible filtering options
- **API Documentation**: Auto-generated Swagger docs at `/docs`

## Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set environment variables**:
```bash
# Generate a secure secret key
openssl rand -hex 32

# Create .env file
cp .env.example .env
# Edit .env and set your SECRET_KEY
```

3. **Run the server**:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user (admin by default)
- `POST /auth/login` - Login and get JWT token

### Students
- `POST /students/` - Create new student (admin only)
- `GET /students/` - List all students (with optional class filter)
- `GET /students/{id}` - Get student details
- `POST /students/{id}/upload-photo` - Upload student photo

### Attendance
- `POST /attendance/mark` - Mark attendance for a student
- `GET /attendance/` - List attendance records (with filters: student_id, class_name, from_date, to_date)
- `GET /attendance/export` - Export attendance as CSV (same filters apply)

### Admin Dashboard
- `GET /admin/dashboard` - Get dashboard statistics
- `GET /admin/students/without-photo` - List students without photos

## Authentication

All endpoints except `/auth/signup` and `/auth/login` require authentication.

Include the JWT token in the Authorization header:
```
Authorization: Bearer <your-token>
```

## Database

Uses SQLite by default (`attendance.db`). The database is created automatically on first run.

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Admin role verification
- File upload validation (type and size)
- Unique constraints (roll numbers, attendance per student per day)
- SQL injection protection via SQLAlchemy ORM
# cd attendance-backend
# python run.py - to run server
# python demo_data.py -to add demo data
