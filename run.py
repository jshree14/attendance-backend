"""
Quick start script for the attendance system
"""
import uvicorn

if __name__ == "__main__":
    print("Starting Student Attendance System API...")
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative docs: http://localhost:8000/redoc")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
