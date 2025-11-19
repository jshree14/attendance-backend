from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import base as db_base
from app.db import models
from app.utils.security import get_current_admin
from datetime import date, timedelta

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])

@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(db_base.get_db), current_user: int = Depends(get_current_admin)):
    today = date.today()
    
    total_students = db.query(func.count(models.Student.id)).scalar()
    
    today_attendance = db.query(models.Attendance).filter(
        models.Attendance.attendance_date == today
    ).count()
    
    today_present = db.query(models.Attendance).filter(
        models.Attendance.attendance_date == today,
        models.Attendance.status == "present"
    ).count()
    
    today_absent = db.query(models.Attendance).filter(
        models.Attendance.attendance_date == today,
        models.Attendance.status == "absent"
    ).count()
    
    week_ago = today - timedelta(days=7)
    week_attendance = db.query(
        models.Attendance.attendance_date,
        func.count(models.Attendance.id).label("count")
    ).filter(
        models.Attendance.attendance_date >= week_ago
    ).group_by(models.Attendance.attendance_date).all()
    
    class_stats = db.query(
        models.Student.class_name,
        func.count(models.Student.id).label("student_count")
    ).group_by(models.Student.class_name).all()
    
    return {
        "total_students": total_students,
        "today": {
            "date": today.isoformat(),
            "total_marked": today_attendance,
            "present": today_present,
            "absent": today_absent,
            "not_marked": total_students - today_attendance
        },
        "last_7_days": [
            {"date": att_date.isoformat(), "count": count} 
            for att_date, count in week_attendance
        ],
        "class_distribution": [
            {"class_name": cls or "Unassigned", "student_count": count}
            for cls, count in class_stats
        ]
    }

@router.get("/students/without-photo")
def students_without_photo(db: Session = Depends(db_base.get_db), current_user: int = Depends(get_current_admin)):
    students = db.query(models.Student).filter(
        (models.Student.photo_path == None) | (models.Student.photo_path == "")
    ).all()
    return {
        "count": len(students),
        "students": [{"id": s.id, "roll_no": s.roll_no, "name": s.name} for s in students]
    }
