from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import engine, Base
from app.api import auth, students, attendance, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Attendance System API",
    description="Backend API for managing student attendance with photo upload, admin dashboard, and CSV export",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(students.router)
app.include_router(attendance.router)
app.include_router(admin.router)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Student Attendance System API is running"}
